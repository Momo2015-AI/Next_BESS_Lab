"""
仿真结果与校正因子模板API路由
仿真结果完整存储带日期戳，支持多模板管理
"""

from flask import Blueprint, current_app, request

from database import CorrectionTemplate, Project, ProjectVersion, SimulationResult, db
from routes.auth import role_required, token_required
from services.simulation import (
    create_simulation_result_service,
    create_template_service,
    seed_templates_service,
    update_template_service,
)
from utils.api_response import error_response, paginated_response, success_response

simulation_bp = Blueprint("simulation", __name__)


# ==================== 仿真结果API ====================


@simulation_bp.route("/api/versions/<version_id>/results", methods=["GET"])
@token_required
def get_simulation_results(version_id):
    """获取版本的所有仿真结果"""
    user = request.current_user

    version = ProjectVersion.query.get(version_id)
    if not version:
        return error_response("版本不存在", 404)

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    pagination = (
        SimulationResult.query.filter_by(version_id=version_id)
        .order_by(SimulationResult.executed_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return paginated_response(
        items=[r.to_dict() for r in pagination.items],
        page=pagination.page,
        page_size=pagination.per_page,
        total=pagination.total,
    )


@simulation_bp.route("/api/versions/<version_id>/results", methods=["POST"])
@token_required
def create_simulation_result(version_id):
    """保存仿真结果"""
    data = request.get_json()

    user = request.current_user
    if not user:
        return error_response("用户不存在", 404)

    try:
        result, err = create_simulation_result_service(db, Project, ProjectVersion, SimulationResult, data, version_id, user)
        if err:
            status_code = 403 if err == "权限不足" else 404
            return error_response(err, status_code)
        return success_response(data=result, message="仿真结果保存成功", status_code=201)
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"保存仿真结果失败: {e}", exc_info=True)
        return error_response("保存失败，请重试", 500)


@simulation_bp.route("/api/results/<result_id>", methods=["GET"])
@token_required
def get_simulation_result(result_id):
    """获取单条仿真结果详情"""
    result = SimulationResult.query.get(result_id)
    if not result:
        return error_response("仿真结果不存在", 404)

    return success_response(data=result.to_dict())


@simulation_bp.route("/api/results/<result_id>", methods=["DELETE"])
@token_required
@role_required("engineer", "admin")
def delete_simulation_result(result_id):
    """删除仿真结果"""
    result = SimulationResult.query.get(result_id)
    if not result:
        return error_response("仿真结果不存在", 404)

    try:
        db.session.delete(result)
        db.session.commit()
        return success_response(message="删除成功")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"删除仿真结果失败: {e}", exc_info=True)
        return error_response("删除失败，请重试", 500)


# ==================== 校正因子模板API ====================


@simulation_bp.route("/api/correction-templates", methods=["GET"])
@token_required
def get_correction_templates():
    """获取校正因子模板列表"""
    user = request.current_user

    query = CorrectionTemplate.query.filter_by(status="active")

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    if user.tenant_id:
        query = query.filter(
            (CorrectionTemplate.tenant_id == user.tenant_id) | (CorrectionTemplate.tenant_id.is_(None))
        )

    pagination = query.order_by(CorrectionTemplate.is_default.desc(), CorrectionTemplate.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return paginated_response(
        items=[t.to_dict() for t in pagination.items],
        page=pagination.page,
        page_size=pagination.per_page,
        total=pagination.total,
    )


@simulation_bp.route("/api/correction-templates", methods=["POST"])
@token_required
def create_correction_template():
    """创建校正因子模板"""
    data = request.get_json()

    user = request.current_user
    if not user:
        return error_response("用户不存在", 404)

    try:
        result, err = create_template_service(db, CorrectionTemplate, data, user)
        if err:
            status_code = 403 if err == "权限不足" else 400
            return error_response(err, status_code)
        return success_response(data=result, message="模板创建成功", status_code=201)
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"创建模板失败: {e}", exc_info=True)
        return error_response("创建失败，请重试", 500)


@simulation_bp.route("/api/correction-templates/<template_id>", methods=["GET"])
@token_required
def get_correction_template(template_id):
    """获取校正因子模板详情"""
    template = CorrectionTemplate.query.get(template_id)
    if not template:
        return error_response("模板不存在", 404)

    return success_response(data=template.to_dict())


@simulation_bp.route("/api/correction-templates/<template_id>", methods=["PUT"])
@token_required
def update_correction_template(template_id):
    """更新校正因子模板"""
    data = request.get_json()

    user = request.current_user
    if not user:
        return error_response("用户不存在", 404)

    try:
        template, err = update_template_service(db, CorrectionTemplate, template_id, data, user)
        if err:
            status_code = 403 if err == "权限不足" else 404
            return error_response(err, status_code)
        return success_response(message="模板更新成功")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"更新模板失败: {e}", exc_info=True)
        return error_response("更新失败，请重试", 500)


@simulation_bp.route("/api/correction-templates/<template_id>", methods=["DELETE"])
@token_required
@role_required("engineer", "admin")
def delete_correction_template(template_id):
    """删除校正因子模板"""
    template = CorrectionTemplate.query.get(template_id)
    if not template:
        return error_response("模板不存在", 404)

    if template.is_default:
        return error_response("不能删除默认模板", 400)

    try:
        db.session.delete(template)
        db.session.commit()
        return success_response(message="删除成功")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"删除模板失败: {e}", exc_info=True)
        return error_response("删除失败，请重试", 500)


@simulation_bp.route("/api/correction-templates/seed", methods=["POST"])
@token_required
def seed_correction_templates():
    """初始化默认校正因子模板"""
    user = request.current_user
    if not user:
        return error_response("用户不存在", 404)

    try:
        result, err = seed_templates_service(db, CorrectionTemplate, user)
        if err:
            return error_response(err, 400)
        return success_response(message="默认模板初始化成功")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"初始化模板失败: {e}", exc_info=True)
        return error_response("初始化失败，请重试", 500)
