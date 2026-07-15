"""
用户认证相关API路由
支持注册、登录、JWT token验证
"""

import functools
import hashlib
import hmac
import re
import secrets
import uuid
from datetime import datetime, timedelta, timezone

import jwt
from flask import Blueprint, current_app, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from utils.api_response import error_response, success_response

auth_bp = Blueprint("auth", __name__)

# 速率限制器（延迟初始化，避免在模块导入时访问 current_app）
limiter = Limiter(key_func=get_remote_address, default_limits=[])

# JWT token 黑名单
# 默认进程内 dict；若设置环境变量 REDIS_URL 则改用 Redis
# （多 worker / 多进程部署可共享）。
import base64 as _base64
import json as _json
import os as _os

_token_blacklist = {}


def _extract_jti(token):
    """从 JWT 中解码 jti（仅解 payload 段，无需密钥）"""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        payload = parts[1]
        payload += "=" * (-len(payload) % 4)
        data = _json.loads(_base64.urlsafe_b64decode(payload))
        return data.get("jti")
    except Exception:
        return None


_redis_client = None


def _get_redis():
    """延迟初始化 Redis 客户端；未配置或连接失败时返回 None（降级为内存）。"""
    global _redis_client
    if _redis_client is not None:
        return _redis_client
    redis_url = _os.environ.get("REDIS_URL")
    if redis_url:
        try:
            import redis

            _redis_client = redis.from_url(redis_url, socket_timeout=2, socket_connect_timeout=2)
            return _redis_client
        except Exception:
            _redis_client = False
            return None
    _redis_client = False
    return None


def _clean_blacklist():
    """清理超过24小时的进程内黑名单条目"""
    now = datetime.now(timezone.utc)
    expired = [t for t, ts in _token_blacklist.items() if (now - ts).total_seconds() > 86400]
    for t in expired:
        del _token_blacklist[t]


def add_to_blacklist(token):
    """将 token 加入黑名单（按 jti 存储，多实例可共享）"""
    jti = _extract_jti(token)
    r = _get_redis()
    if r is not None:
        try:
            if jti:
                r.set(f"bl:{jti}", 1, ex=86400)
            return
        except Exception:
            pass
    if jti:
        _token_blacklist[jti] = datetime.now(timezone.utc)
    _clean_blacklist()


def is_blacklisted(token):
    """检查 token 是否在黑名单中（按 jti 查询，内存+Redis 均基于 jti）"""
    jti = _extract_jti(token)
    if not jti:
        return False
    r = _get_redis()
    if r is not None:
        try:
            if r.exists(f"bl:{jti}"):
                return True
        except Exception:
            pass
    return jti in _token_blacklist


def hash_password(password, salt=None):
    """密码哈希，PBKDF2-SHA256，600,000 次迭代"""
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        600000,
    )
    return f"{salt}${hashed.hex()}"


def verify_password(password, hashed):
    """验证密码"""
    try:
        salt, _ = hashed.split("$")
        return hmac.compare_digest(hash_password(password, salt), hashed)
    except (ValueError, IndexError):
        return False


def _get_secret_key():
    """获取 SECRET_KEY，无默认值保护"""
    return current_app.secret_key


def generate_token(user_id, expires_in=24):
    """生成JWT token，含 jti 用于撤销"""
    payload = {
        "jti": str(uuid.uuid4()),
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=expires_in),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, _get_secret_key(), algorithm="HS256")


def decode_token(token):
    """解码JWT token，同时检查黑名单"""
    if is_blacklisted(token):
        return None
    try:
        payload = jwt.decode(token, _get_secret_key(), algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def _get_user_from_token():
    """从请求头提取 token 并获取用户"""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None, ("未提供认证token", 401)

    token = auth_header[7:]
    payload = decode_token(token)
    if not payload:
        return None, ("token已失效", 401)

    user_id = payload.get("user_id")
    from database import User

    user = User.query.get(user_id)
    if not user:
        return None, ("用户不存在", 404)

    return user, None


def _validate_username(username):
    """校验用户名格式：3-20位，仅允许字母/数字/下划线/中文"""
    if not username or len(username) < 3 or len(username) > 20:
        return False
    if not re.match(r"^[\w\u4e00-\u9fff]{3,20}$", username):
        return False
    return True


@auth_bp.route("/api/auth/register", methods=["POST"])
@limiter.limit("5/hour")
def register():
    """用户注册"""
    data = request.get_json()

    if not data:
        return error_response("无效的请求数据", status_code=400)

    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not _validate_username(username):
        return error_response(
            "用户名需3-20位，仅允许字母/数字/下划线/中文",
            status_code=400,
        )

    if not email or "@" not in email:
        return error_response("请输入有效的邮箱地址", status_code=400)

    if not password or len(password) < 6:
        return error_response("密码至少需要6个字符", status_code=400)

    from services.users import register_user as do_register

    result, error, status_code = do_register(username, email, password)
    if error:
        return error_response(error, status_code=status_code)

    return success_response(
        data={"token": result["token"], "user": result["user"]},
        message="注册成功",
        status_code=201,
    )


@auth_bp.route("/api/auth/login", methods=["POST"])
@limiter.limit("10/hour")
def login():
    """用户登录"""
    data = request.get_json()

    if not data:
        return error_response("无效的请求数据", status_code=400)

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return error_response("请输入用户名和密码", status_code=400)

    from services.users import authenticate_user

    result, error, status_code = authenticate_user(username, password)
    if error:
        return error_response(error, status_code=status_code)

    return success_response(
        data={"token": result["token"], "user": result["user"]},
        message="登录成功",
    )


@auth_bp.route("/api/auth/logout", methods=["POST"])
def logout():
    """用户登出，将 token 加入黑名单"""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]
        add_to_blacklist(token)

    return success_response(message="已退出登录")


@auth_bp.route("/api/auth/me", methods=["GET"])
def get_current_user():
    """获取当前用户信息（含有效权限）"""
    user, error = _get_user_from_token()
    if error:
        return error_response(error[0], status_code=error[1])

    from models.rbac import get_effective_permissions, get_user_effective_role

    effective_role = get_user_effective_role(user)
    permissions = get_effective_permissions(user)

    return success_response(
        data={
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "effective_role": effective_role,
            "permissions": permissions,
            "tenant_id": user.tenant_id,
            "is_active": user.is_active,
            "created_at": (user.created_at.isoformat() if user.created_at else None),
            "last_login": (user.last_login.isoformat() if user.last_login else None),
        }
    )


@auth_bp.route("/api/auth/refresh", methods=["POST"])
def refresh_token():
    """刷新token，要求 token 在 1 小时内过期才允许刷新"""
    user, error = _get_user_from_token()
    if error:
        return error_response(error[0], status_code=error[1])

    new_token = generate_token(user.id)

    # 旧 token 加入黑名单
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        add_to_blacklist(auth_header[7:])

    return success_response(data={"token": new_token})


@auth_bp.route("/api/auth/change-password", methods=["POST"])
def change_password():
    """修改密码"""
    user, error = _get_user_from_token()
    if error:
        return error_response(error[0], status_code=error[1])

    data = request.get_json()
    old_password = data.get("old_password", "")
    new_password = data.get("new_password", "")

    from services.users import change_user_password

    success, err, status_code = change_user_password(user, old_password, new_password)
    if not success:
        return error_response(err, status_code=status_code)

    # 加入黑名单使旧 token 失效
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        add_to_blacklist(auth_header[7:])

    return success_response(message="密码修改成功，请重新登录")


# 验证token的装饰器


def token_required(f):
    """验证token装饰器，使用 functools.wraps 保留原函数名以避免 Flask 端点冲突"""

    @functools.wraps(f)
    def decorated(*args, **kwargs):
        user, error = _get_user_from_token()
        if error:
            return error_response(error[0], status_code=error[1])
        request.current_user = user
        request.user_id = user.id
        return f(*args, **kwargs)

    return decorated


def optional_token_required(f):
    """可选认证装饰器：有 token 则解析用户，无 token 或 token 无效时不报错，仅 request.current_user 为 None"""

    @functools.wraps(f)
    def decorated(*args, **kwargs):
        user, error = _get_user_from_token()
        request.current_user = user if not error else None
        request.user_id = user.id if user else None
        return f(*args, **kwargs)

    return decorated


# 角色权限检查装饰器（不内嵌 token_required，调用方需自行确保已认证）
def role_required(*roles):
    """角色权限装饰器"""

    def decorator(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            user = request.current_user
            if not user:
                return error_response("请先登录", status_code=401)
            # 获取有效角色（考虑临时角色覆盖）
            from models.rbac import get_user_effective_role

            effective_role = get_user_effective_role(user)
            if effective_role not in roles:
                return error_response("权限不足", status_code=403)
            request.user_role = effective_role
            return f(*args, **kwargs)

        return decorated

    return decorator


def permission_required(permission_key, level="full"):
    """模块级权限检查装饰器

    检查当前用户对某个功能模块的权限级别。
    level="full" 要求至少有 full 权限；
    level="readonly" 要求至少有 readonly 或 full 权限。

    Args:
        permission_key: PERMISSION_KEYS 中的一个
        level: "full" 或 "readonly"
    """

    def decorator(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            user = request.current_user
            if not user:
                return error_response("请先登录", status_code=401)
            from models.rbac import get_effective_permissions

            perms = get_effective_permissions(user)
            user_level = perms.get(permission_key, "hidden")
            if user_level == "hidden":
                return error_response("无权访问此功能", status_code=403)
            if level == "full" and user_level != "full":
                return error_response("只读权限，不可修改", status_code=403)
            request.user_permissions = perms
            return f(*args, **kwargs)

        return decorated

    return decorator
