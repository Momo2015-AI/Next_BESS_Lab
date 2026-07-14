"""角色权限管理 API

管理员可在此配置角色权限覆盖、用户权限覆盖，设置失效时间。
"""

import json
import uuid
from datetime import datetime, timezone

from flask import Blueprint, request
from sqlalchemy.orm import selectinload

from database import (
    DEFAULT_ROLE,
    DEFAULT_ROLE_PERMISSIONS,
    PERMISSION_KEYS,
    ROLES,
    RolePermission,
    User,
    UserPermissionOverride,
    db,
    get_effective_permissions,
    get_user_effective_role,
)
from routes.auth import role_required, token_required
from utils.api_response import error_response, success_response

rbac_bp = Blueprint("rbac", __name__)


# ==================== 角色与权限定义查询 ====================


@rbac_bp.route("/api/rbac/roles", methods=["GET"])
@token_required
def get_roles():
    """获取所有角色定义"""
    roles_data = []
    for role_code, info in ROLES.items():
        roles_data.append(
            {
                "code": role_code,
                "label": info["label"],
                "label_en": info["label_en"],
                "description": info["description"],
                "is_default": role_code == DEFAULT_ROLE,
            }
        )
    return success_response(data=roles_data)


@rbac_bp.route("/api/rbac/permissions", methods=["GET"])
@token_required
def get_permission_keys():
    """获取所有权限模块 key 及其默认角色权限映射"""
    return success_response(
        data={
            "permission_keys": PERMISSION_KEYS,
            "default_permissions": DEFAULT_ROLE_PERMISSIONS,
        }
    )


# ==================== 角色权限覆盖 ====================


@rbac_bp.route("/api/rbac/role-permissions", methods=["GET"])
@token_required
@role_required("admin")
def get_role_permissions():
    """获取所有角色的权限配置（含覆盖）"""
    result = {}
    for role_code in ROLES:
        # 默认权限
        default_perms = dict(DEFAULT_ROLE_PERMISSIONS.get(role_code, {}))
        # 检查是否有覆盖
        override = RolePermission.query.filter_by(role=role_code).first()
        override_data = None
        if override:
            now = datetime.now(timezone.utc)
            is_expired = override.expires_at is not None and override.expires_at <= now
            try:
                override_perms = json.loads(override.permissions or "{}")
            except (json.JSONDecodeError, ValueError):
                override_perms = {}
            override_data = {
                "id": override.id,
                "permissions": override_perms if not is_expired else {},
                "expires_at": override.expires_at.isoformat() if override.expires_at else None,
                "is_expired": is_expired,
                "note": override.note or "",
                "updated_at": override.updated_at.isoformat() if override.updated_at else None,
            }
            # 如果未过期，合并覆盖到默认权限
            if not is_expired:
                default_perms.update(override_perms)

        result[role_code] = {
            "default_permissions": dict(DEFAULT_ROLE_PERMISSIONS.get(role_code, {})),
            "effective_permissions": default_perms,
            "override": override_data,
        }
    return success_response(data=result)


@rbac_bp.route("/api/rbac/role-permissions/<role_code>", methods=["PUT"])
@token_required
@role_required("admin")
def update_role_permission(role_code):
    """设置/更新角色权限覆盖

    Body:
        permissions: dict, 权限映射 {"phase1": "full", ...}
        expires_at: string|null, ISO 时间，过期恢复默认
        note: string, 备注
    """
    if role_code not in ROLES:
        return error_response("角色不存在", status_code=404)

    data = request.get_json() or {}
    permissions = data.get("permissions", {})
    expires_at_str = data.get("expires_at")
    note = data.get("note", "")

    # 校验 permissions
    if not isinstance(permissions, dict):
        return error_response("permissions 必须是对象", status_code=400)

    for key, val in permissions.items():
        if key not in PERMISSION_KEYS:
            return error_response(f"未知的权限模块: {key}", status_code=400)
        if val not in ("full", "readonly", "hidden"):
            return error_response(f"权限级别必须为 full/readonly/hidden: {key}", status_code=400)

    # 解析过期时间
    expires_at = None
    if expires_at_str:
        try:
            expires_at = datetime.fromisoformat(expires_at_str)
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)
        except (ValueError, TypeError):
            return error_response("expires_at 格式无效，请使用 ISO 8601", status_code=400)

    override = RolePermission.query.filter_by(role=role_code).first()
    if override:
        override.permissions = json.dumps(permissions)
        override.expires_at = expires_at
        override.note = note
        override.created_by = request.current_user.id
    else:
        override = RolePermission(
            id=str(uuid.uuid4()),
            role=role_code,
            permissions=json.dumps(permissions),
            expires_at=expires_at,
            note=note,
            created_by=request.current_user.id,
        )
        db.session.add(override)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return error_response("保存失败", status_code=500)

    return success_response(
        data={
            "role": role_code,
            "permissions": permissions,
            "expires_at": expires_at.isoformat() if expires_at else None,
            "note": note,
        },
        message="角色权限已更新",
    )


@rbac_bp.route("/api/rbac/role-permissions/<role_code>", methods=["DELETE"])
@token_required
@role_required("admin")
def reset_role_permission(role_code):
    """重置角色权限到默认（删除覆盖）"""
    if role_code not in ROLES:
        return error_response("角色不存在", status_code=404)

    override = RolePermission.query.filter_by(role=role_code).first()
    if override:
        db.session.delete(override)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return error_response("重置失败", status_code=500)

    return success_response(message=f"角色 {role_code} 权限已重置为默认")


# ==================== 用户权限覆盖 ====================


@rbac_bp.route("/api/rbac/users", methods=["GET"])
@token_required
@role_required("admin")
def list_users():
    """获取所有用户列表（含权限覆盖信息）"""
    # 管理员可查看所有租户的用户
    users = User.query.options(selectinload(User.permission_override)).order_by(User.created_at.desc()).all()

    result = []
    for user in users:
        override = user.permission_override
        override_data = None
        if override:
            now = datetime.now(timezone.utc)
            is_expired = override.expires_at is not None and override.expires_at <= now
            try:
                override_perms = json.loads(override.permissions or "{}")
            except (json.JSONDecodeError, ValueError):
                override_perms = {}
            override_data = {
                "id": override.id,
                "temporary_role": override.temporary_role,
                "permissions": override_perms,
                "expires_at": override.expires_at.isoformat() if override.expires_at else None,
                "is_expired": is_expired,
                "note": override.note or "",
            }

        effective_role = get_user_effective_role(user)
        effective_perms = get_effective_permissions(user)

        result.append(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "effective_role": effective_role,
                "effective_permissions": effective_perms,
                "tenant_id": user.tenant_id,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "last_login": user.last_login.isoformat() if user.last_login else None,
                "override": override_data,
            }
        )

    return success_response(data=result)


@rbac_bp.route("/api/rbac/users/<user_id>/override", methods=["PUT"])
@token_required
@role_required("admin")
def set_user_override(user_id):
    """设置/更新用户权限覆盖

    Body:
        temporary_role: string|null, 临时角色（优先于原角色）
        permissions: dict, 精确权限覆盖 {"phase1": "full", ...}
        expires_at: string|null, ISO 时间，过期恢复默认
        note: string, 备注
    """
    user = User.query.get(user_id)
    if not user:
        return error_response("用户不存在", status_code=404)

    # 不允许覆盖 admin 用户（防止锁死系统）
    if user.role == "admin":
        return error_response("不可修改管理员的权限", status_code=403)

    data = request.get_json() or {}
    temporary_role = data.get("temporary_role")
    permissions = data.get("permissions", {})
    expires_at_str = data.get("expires_at")
    note = data.get("note", "")

    # 校验 temporary_role
    if temporary_role and temporary_role not in ROLES:
        return error_response("临时角色不存在", status_code=400)

    # 校验 permissions
    if not isinstance(permissions, dict):
        return error_response("permissions 必须是对象", status_code=400)

    for key, val in permissions.items():
        if key not in PERMISSION_KEYS:
            return error_response(f"未知的权限模块: {key}", status_code=400)
        if val not in ("full", "readonly", "hidden"):
            return error_response(f"权限级别必须为 full/readonly/hidden: {key}", status_code=400)

    # 解析过期时间
    expires_at = None
    if expires_at_str:
        try:
            expires_at = datetime.fromisoformat(expires_at_str)
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)
        except (ValueError, TypeError):
            return error_response("expires_at 格式无效，请使用 ISO 8601", status_code=400)

    override = UserPermissionOverride.query.filter_by(user_id=user_id).first()
    if override:
        override.temporary_role = temporary_role
        override.permissions = json.dumps(permissions)
        override.expires_at = expires_at
        override.note = note
        override.created_by = request.current_user.id
    else:
        override = UserPermissionOverride(
            id=str(uuid.uuid4()),
            user_id=user_id,
            temporary_role=temporary_role,
            permissions=json.dumps(permissions),
            expires_at=expires_at,
            note=note,
            created_by=request.current_user.id,
        )
        db.session.add(override)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return error_response("保存失败", status_code=500)

    return success_response(
        data={
            "user_id": user_id,
            "username": user.username,
            "temporary_role": temporary_role,
            "permissions": permissions,
            "expires_at": expires_at.isoformat() if expires_at else None,
            "note": note,
        },
        message="用户权限覆盖已更新",
    )


@rbac_bp.route("/api/rbac/users/<user_id>/override", methods=["DELETE"])
@token_required
@role_required("admin")
def reset_user_override(user_id):
    """重置用户权限（删除覆盖，恢复默认角色权限）"""
    user = User.query.get(user_id)
    if not user:
        return error_response("用户不存在", status_code=404)

    override = UserPermissionOverride.query.filter_by(user_id=user_id).first()
    if override:
        db.session.delete(override)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return error_response("重置失败", status_code=500)

    return success_response(message=f"用户 {user.username} 权限已恢复默认")


@rbac_bp.route("/api/rbac/users/<user_id>/role", methods=["PUT"])
@token_required
@role_required("admin")
def change_user_role(user_id):
    """永久更改用户角色（非临时覆盖）

    Body:
        role: string, 新角色代码
    """
    user = User.query.get(user_id)
    if not user:
        return error_response("用户不存在", status_code=404)

    if user.role == "admin":
        return error_response("不可修改管理员的角色", status_code=403)

    data = request.get_json() or {}
    new_role = data.get("role")

    if not new_role or new_role not in ROLES:
        return error_response("无效的角色代码", status_code=400)

    old_role = user.role
    user.role = new_role
    user.updated_at = datetime.now(timezone.utc)

    # 如果用户有权限覆盖中的临时角色，也清除
    override = UserPermissionOverride.query.filter_by(user_id=user_id).first()
    if override and override.temporary_role:
        override.temporary_role = None

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return error_response("角色更新失败", status_code=500)

    return success_response(
        data={
            "user_id": user_id,
            "username": user.username,
            "old_role": old_role,
            "new_role": new_role,
        },
        message=f"用户角色已从 {old_role} 更改为 {new_role}",
    )
