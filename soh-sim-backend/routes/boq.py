from flask import Blueprint, current_app, request

from database import BoqItem, BoqSection, Project, db
from routes.auth import token_required
from services.boq import bump_boq_version, save_boq_items
from utils.api_response import error_response, paginated_response, success_response

boq_bp = Blueprint("boq", __name__)


@boq_bp.route("/api/boq/sections", methods=["GET"])
@token_required
def get_boq_sections():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 50, type=int)
    pagination = BoqSection.query.order_by(BoqSection.sort_order).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return paginated_response(
        items=[s.to_dict() for s in pagination.items],
        page=pagination.page,
        page_size=pagination.per_page,
        total=pagination.total,
    )


@boq_bp.route("/api/boq/items", methods=["GET"])
@token_required
def get_boq_items():
    user = request.current_user
    project_id = request.args.get("project_id")
    is_alternative = request.args.get("is_alternative", "false").lower() == "true"
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 50, type=int)

    query = BoqItem.query
    if project_id:
        # 租户隔离：非 admin 必须校验 project_id 归属，避免读取任意租户 BOQ
        project = Project.query.get(project_id)
        if not project or (getattr(user, "role", None) != "admin" and project.tenant_id != user.tenant_id):
            return error_response("项目不存在", 404)  # 不暴露存在性，避免信息泄露
        query = query.filter_by(project_id=project_id)
    query = query.filter_by(is_alternative=is_alternative)
    pagination = query.order_by(BoqItem.section_code, BoqItem.seq).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return paginated_response(
        items=[i.to_dict() for i in pagination.items],
        page=pagination.page,
        page_size=pagination.per_page,
        total=pagination.total,
    )


@boq_bp.route("/api/boq/items", methods=["POST"])
@token_required
def save_boq_items_api():
    data = request.get_json()
    if not data:
        return error_response("invalid request body", 400)

    items_data = data.get("items", [])
    project_id = data.get("projectId")
    is_alternative = data.get("isAlternative", False)

    if not project_id:
        return error_response("projectId is required", 400)

    # 租户隔离：写入前校验 project 归属，避免越权写入他人 BOQ
    user = request.current_user
    project = Project.query.get(project_id)
    if not project or (getattr(user, "role", None) != "admin" and project.tenant_id != user.tenant_id):
        return error_response("项目不存在或无权访问", 403)

    try:
        saved = save_boq_items(db, BoqItem, project_id, items_data, is_alternative)
        return success_response(data=[i.to_dict() for i in saved], message=f"已保存 {len(saved)} 条")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"BOQ保存失败: {e}", exc_info=True)
        return error_response("保存失败，请重试", 500)


@boq_bp.route("/api/boq/version", methods=["POST"])
@token_required
def create_boq_version():
    data = request.get_json()
    if not data:
        return error_response("invalid request body", 400)

    project_id = data.get("projectId")
    if not project_id:
        return error_response("projectId is required", 400)

    # 租户隔离：改版前校验 project 归属，避免越权操作他人 BOQ 版本
    user = request.current_user
    project = Project.query.get(project_id)
    if not project or (getattr(user, "role", None) != "admin" and project.tenant_id != user.tenant_id):
        return error_response("项目不存在或无权访问", 403)

    new_version = bump_boq_version(db, BoqItem, project_id)
    return success_response(message=f"Version bumped to {new_version}")
