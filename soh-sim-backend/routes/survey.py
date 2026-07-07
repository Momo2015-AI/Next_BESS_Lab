"""
调研表相关API路由
"""

import json
from datetime import datetime, timezone

from flask import Blueprint, current_app, request

from database import Project, Survey, db
from routes.auth import token_required
from services.survey import (
    delete_project_cascade_service,
    submit_survey_service,
    update_survey_service,
)
from utils.api_response import error_response, paginated_response, success_response

survey_bp = Blueprint("survey", __name__)


@survey_bp.route("/api/survey/submit", methods=["POST"])
@token_required
def submit_survey():
    """提交调研表，自动生成UUID，并创建关联项目"""
    data = request.get_json()
    if not data:
        return error_response("无效的请求数据", 400)

    try:
        result, err = submit_survey_service(db, Project, Survey, data)
        return success_response(data=result, message="调研表提交成功，项目已自动创建", status_code=201)
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"提交调研表失败: {e}", exc_info=True)
        return error_response("提交失败，请重试", 500)


@survey_bp.route("/api/survey/<survey_id>", methods=["GET"])
@token_required
def get_survey(survey_id):
    """获取调研表详情"""
    survey = Survey.query.get(survey_id)
    if not survey:
        return error_response("调研表不存在", 404)

    result = survey.to_dict()
    if survey.project:
        result["project"] = survey.project.to_dict()

    return success_response(data=result)


@survey_bp.route("/api/survey/list", methods=["GET"])
@token_required
def list_surveys():
    """获取调研表列表"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    status = request.args.get("status")
    keyword = request.args.get("keyword")

    query = Survey.query
    if status:
        query = query.filter(Survey.status == status)
    if keyword:
        query = query.filter(Survey.project_name.ilike(f"%{keyword}%"))

    pagination = query.order_by(Survey.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return paginated_response(
        items=[s.to_dict() for s in pagination.items],
        page=pagination.page,
        page_size=pagination.per_page,
        total=pagination.total,
    )


@survey_bp.route("/api/survey/search", methods=["GET"])
@token_required
def search_survey():
    """通过项目名称搜索调研表"""
    keyword = request.args.get("keyword", "")

    if not keyword:
        return error_response("请输入搜索关键词", 400)

    surveys = Survey.query.filter(Survey.project_name.ilike(f"%{keyword}%")).limit(10).all()

    return success_response(data={"surveys": [s.to_dict() for s in surveys]})


@survey_bp.route("/api/survey/<survey_id>", methods=["PUT"])
@token_required
def update_survey(survey_id):
    """更新调研表"""
    data = request.get_json()
    if not data:
        return error_response("无效的请求数据", 400)

    try:
        survey, err = update_survey_service(db, Survey, survey_id, data)
        if err:
            return error_response(err, 404)
        return success_response(data={"survey": survey.to_dict()}, message="调研表更新成功")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"更新调研表失败: {e}", exc_info=True)
        return error_response("更新失败，请重试", 500)


@survey_bp.route("/api/survey/<survey_id>", methods=["DELETE"])
@token_required
def delete_survey(survey_id):
    """删除调研表"""
    survey = Survey.query.get(survey_id)
    if not survey:
        return error_response("调研表不存在", 404)

    try:
        db.session.delete(survey)
        db.session.commit()
        return success_response(message="调研表已删除")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"删除调研表失败: {e}", exc_info=True)
        return error_response("删除失败，请重试", 500)


@survey_bp.route("/api/project/<project_id>", methods=["GET"])
@token_required
def get_project(project_id):
    """获取项目详情"""
    project = Project.query.get(project_id)
    if not project:
        return error_response("项目不存在", 404)

    result = project.to_dict()
    result["surveys"] = [s.to_dict() for s in project.surveys]

    return success_response(data=result)


@survey_bp.route("/api/project/list", methods=["GET"])
@token_required
def list_projects():
    """获取项目列表"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    status = request.args.get("status")
    stage = request.args.get("stage")

    query = Project.query
    if status:
        query = query.filter(Project.status == status)
    if stage:
        query = query.filter(Project.stage == stage)

    pagination = query.order_by(Project.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return paginated_response(
        items=[p.to_dict() for p in pagination.items],
        page=pagination.page,
        page_size=pagination.per_page,
        total=pagination.total,
    )


@survey_bp.route("/api/project/<project_id>", methods=["PUT"])
@token_required
def update_project(project_id):
    """更新项目"""
    project = Project.query.get(project_id)
    if not project:
        return error_response("项目不存在", 404)

    data = request.get_json()
    if not data:
        return error_response("无效的请求数据", 400)

    if "name" in data:
        project.name = data["name"]
    if "status" in data:
        project.status = data["status"]
    if "stage" in data:
        project.stage = data["stage"]
    if "config" in data:
        project.config = json.dumps(data["config"])

    project.updated_at = datetime.now(timezone.utc)

    try:
        db.session.commit()
        return success_response(data={"project": project.to_dict()}, message="项目更新成功")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"更新项目失败: {e}", exc_info=True)
        return error_response("更新失败，请重试", 500)


@survey_bp.route("/api/project/<project_id>", methods=["DELETE"])
@token_required
def delete_project(project_id):
    """删除项目（级联删除关联调研表）"""
    try:
        project, err = delete_project_cascade_service(db, Project, Survey, project_id)
        if err:
            return error_response(err, 404)
        return success_response(message="项目及关联调研表已删除")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"删除项目失败: {e}", exc_info=True)
        return error_response("删除失败，请重试", 500)
