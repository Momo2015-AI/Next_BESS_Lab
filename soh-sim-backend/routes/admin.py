"""
管理员配置 API

提供方案模板、系统配置等管理员专属功能。
"""

from flask import Blueprint, request

from database import db
from models.admin import DesignTemplate
from routes.auth import token_required
from utils.api_response import error_response, paginated_response, success_response

admin_bp = Blueprint("admin_api", __name__)


def _require_admin(user):
    """仅 admin 角色可操作"""
    if not user or user.role != "admin":
        return False
    return True


# ==================== 方案模板 CRUD ====================


@admin_bp.route("/api/admin/design-templates", methods=["GET"])
@token_required
def list_templates(user):
    """列出方案模板"""
    if not _require_admin(user):
        return error_response("仅管理员可访问", status_code=403)

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("page_size", 50, type=int)
    strategy = request.args.get("strategy")

    query = DesignTemplate.query.filter(DesignTemplate.status == "active")
    if strategy:
        query = query.filter(DesignTemplate.strategy == strategy)

    query = query.order_by(DesignTemplate.sort_order.asc(), DesignTemplate.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return paginated_response(
        items=[t.to_dict() for t in pagination.items],
        page=pagination.page,
        page_size=pagination.per_page,
        total=pagination.total,
    )


@admin_bp.route("/api/admin/design-templates/<template_id>", methods=["GET"])
@token_required
def get_template(user, template_id):
    """获取单个模板"""
    if not _require_admin(user):
        return error_response("仅管理员可访问", status_code=403)

    t = DesignTemplate.query.get(template_id)
    if not t:
        return error_response("模板不存在", status_code=404)
    return success_response(data=t.to_dict())


@admin_bp.route("/api/admin/design-templates", methods=["POST"])
@token_required
def create_template(user):
    """创建方案模板"""
    if not _require_admin(user):
        return error_response("仅管理员可访问", status_code=403)

    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    if not name:
        return error_response("模板名称不能为空")

    t = DesignTemplate(
        tenant_id=user.tenant_id,
        name=name,
        name_en=data.get("nameEn", ""),
        strategy=data.get("strategy", "balanced"),
        description=data.get("description", ""),
        cell_model=data.get("cellModel"),
        container_model=data.get("containerModel"),
        pcs_model=data.get("pcsModel"),
        default_duration=data.get("defaultDuration"),
        default_dod=data.get("defaultDod"),
        default_crate=data.get("defaultCrate"),
        is_default=data.get("isDefault", False),
        sort_order=data.get("sortOrder", 0),
    )

    # 如果设为默认，取消其他同策略的默认标记
    if t.is_default:
        DesignTemplate.query.filter(
            DesignTemplate.strategy == t.strategy,
            DesignTemplate.is_default.is_(True),
        ).update({"is_default": False})

    db.session.add(t)
    db.session.commit()

    return success_response(data=t.to_dict(), message="模板创建成功", status_code=201)


@admin_bp.route("/api/admin/design-templates/<template_id>", methods=["PUT"])
@token_required
def update_template(user, template_id):
    """更新方案模板"""
    if not _require_admin(user):
        return error_response("仅管理员可访问", status_code=403)

    t = DesignTemplate.query.get(template_id)
    if not t:
        return error_response("模板不存在", status_code=404)

    data = request.get_json(silent=True) or {}

    if "name" in data:
        t.name = data["name"].strip()
    if "nameEn" in data:
        t.name_en = data["nameEn"]
    if "strategy" in data:
        t.strategy = data["strategy"]
    if "description" in data:
        t.description = data["description"]
    if "cellModel" in data:
        t.cell_model = data["cellModel"]
    if "containerModel" in data:
        t.container_model = data["containerModel"]
    if "pcsModel" in data:
        t.pcs_model = data["pcsModel"]
    if "defaultDuration" in data:
        t.default_duration = data["defaultDuration"]
    if "defaultDod" in data:
        t.default_dod = data["defaultDod"]
    if "defaultCrate" in data:
        t.default_crate = data["defaultCrate"]
    if "isDefault" in data:
        if data["isDefault"] and not t.is_default:
            DesignTemplate.query.filter(
                DesignTemplate.strategy == t.strategy,
                DesignTemplate.is_default.is_(True),
            ).update({"is_default": False})
        t.is_default = data["isDefault"]
    if "sortOrder" in data:
        t.sort_order = data["sortOrder"]

    db.session.commit()
    return success_response(data=t.to_dict(), message="模板更新成功")


@admin_bp.route("/api/admin/design-templates/<template_id>", methods=["DELETE"])
@token_required
def delete_template(user, template_id):
    """删除方案模板（软删除）"""
    if not _require_admin(user):
        return error_response("仅管理员可访问", status_code=403)

    t = DesignTemplate.query.get(template_id)
    if not t:
        return error_response("模板不存在", status_code=404)
    if t.is_builtin:
        return error_response("内置模板不可删除", status_code=403)

    t.status = "deleted"
    db.session.commit()
    return success_response(message="模板已删除")


# ==================== 策略列表（供前端下拉） ====================


@admin_bp.route("/api/admin/design-strategies", methods=["GET"])
@token_required
def list_strategies(_user):
    """返回可用设计策略"""
    strategies = [
        {"key": "economic", "label": "经济优先", "labelEn": "Economic", "desc": "大容量集装箱，最小化 BOP 成本"},
        {"key": "balanced", "label": "均衡方案", "labelEn": "Balanced", "desc": "中等容量，最优 CAPEX/MWh"},
        {"key": "flexible", "label": "灵活分期", "labelEn": "Flexible", "desc": "小容量集装箱，便于分期部署"},
        {"key": "manufacturer", "label": "指定厂家", "labelEn": "Manufacturer", "desc": "按指定厂家筛选产品"},
    ]
    return success_response(data=strategies)
