"""
项目与版本管理API路由
支持项目CRUD、版本管理（另存为）、方案配置
"""

from flask import Blueprint, current_app, request
from sqlalchemy.orm import selectinload

from database import Project, ProjectVersion, SohRteData, db
from routes.auth import role_required, token_required
from services.project import (
    activate_version_service,
    create_project_service,
    create_version_service,
    sync_params_service,
    update_project_service,
    update_version_service,
)
from utils.api_response import error_response, paginated_response, success_response

project_bp = Blueprint("project", __name__)


# ==================== 项目API ====================


@project_bp.route("/api/projects", methods=["GET"])
@token_required
def get_projects():
    """获取项目列表"""
    user = request.current_user

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    query = Project.query

    if user.role == "customer":
        query = query.filter(Project.customer_id == user.id)

    pagination = query.order_by(Project.updated_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return paginated_response(
        items=[p.to_dict() for p in pagination.items],
        page=pagination.page,
        page_size=pagination.per_page,
        total=pagination.total,
    )


@project_bp.route("/api/projects", methods=["POST"])
@token_required
def create_project():
    """创建项目"""
    data = request.get_json()

    if not data:
        return error_response("无效的请求数据", 400)

    name = data.get("name", "").strip()
    if not name:
        return error_response("项目名称不能为空", 400)

    user = request.current_user
    if not user:
        return error_response("用户不存在", 404)

    try:
        result, err = create_project_service(db, Project, ProjectVersion, data, user)
        if err:
            return error_response(err, 403)
        return success_response(data=result, message="项目创建成功", status_code=201)
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"创建项目失败: {e}", exc_info=True)
        return error_response("创建失败，请重试", 500)


@project_bp.route("/api/projects/<project_id>", methods=["GET"])
@token_required
def get_project(project_id):
    """获取项目详情"""
    user = request.current_user
    if not user:
        return error_response("用户不存在", 404)

    project = Project.query.get(project_id)
    if not project:
        return error_response("项目不存在", 404)

    if user.role == "customer" and project.customer_id != user.id:
        return error_response("权限不足", 403)

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    pagination = (
        ProjectVersion.query.filter_by(project_id=project_id)
        .order_by(ProjectVersion.version_num.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    versions = pagination.items

    project_data = project.to_dict()
    project_data["versions"] = [v.to_dict() for v in versions]
    project_data["versions_total"] = pagination.total
    project_data["versions_page"] = pagination.page
    project_data["versions_per_page"] = pagination.per_page
    project_data["versions_pages"] = pagination.pages

    return success_response(data=project_data)


@project_bp.route("/api/projects/<project_id>", methods=["PUT"])
@token_required
def update_project(project_id):
    """更新项目"""
    data = request.get_json()

    user = request.current_user
    if not user:
        return error_response("用户不存在", 404)

    try:
        project, err = update_project_service(db, Project, project_id, data, user)
        if err:
            status_code = 403 if err == "权限不足" else 404
            return error_response(err, status_code)
        return success_response(message="项目更新成功")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"更新项目失败: {e}", exc_info=True)
        return error_response("更新失败，请重试", 500)


@project_bp.route("/api/projects/<project_id>", methods=["DELETE"])
@token_required
@role_required("admin")
def delete_project(project_id):
    """删除项目（仅管理员）"""
    project = Project.query.get(project_id)
    if not project:
        return error_response("项目不存在", 404)

    try:
        db.session.delete(project)
        db.session.commit()
        return success_response(message="项目删除成功")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"删除项目失败: {e}", exc_info=True)
        return error_response("删除失败，请重试", 500)


# ==================== 版本API ====================


@project_bp.route("/api/projects/<project_id>/versions", methods=["GET"])
@token_required
def get_versions(project_id):
    """获取项目版本列表"""
    user = request.current_user

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    project = Project.query.get(project_id)
    if not project:
        return error_response("项目不存在", 404)

    if user.role == "customer" and project.customer_id != user.id:
        return error_response("权限不足", 403)

    pagination = (
        ProjectVersion.query.filter_by(project_id=project_id)
        .order_by(ProjectVersion.version_num.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return paginated_response(
        items=[v.to_dict() for v in pagination.items],
        page=pagination.page,
        page_size=pagination.per_page,
        total=pagination.total,
    )


@project_bp.route("/api/projects/<project_id>/versions", methods=["POST"])
@token_required
def create_version(project_id):
    """创建新版本（另存为）"""
    data = request.get_json()

    user = request.current_user
    if not user:
        return error_response("用户不存在", 404)

    try:
        result, err = create_version_service(db, Project, ProjectVersion, project_id, data, user)
        if err:
            status_code = 403 if err == "权限不足" else 404
            return error_response(err, status_code)
        return success_response(data=result, message="版本创建成功", status_code=201)
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"创建版本失败: {e}", exc_info=True)
        return error_response("创建失败，请重试", 500)


@project_bp.route("/api/versions/<version_id>", methods=["GET"])
@token_required
def get_version(version_id):
    """获取版本详情"""
    user = request.current_user
    if not user:
        return error_response("用户不存在", 404)

    version = ProjectVersion.query.options(selectinload(ProjectVersion.project)).get(version_id)
    if not version:
        return error_response("版本不存在", 404)

    # 租户隔离：admin 可跨租户，其余用户仅可访问同租户版本
    if getattr(user, "role", None) != "admin" and version.project and version.project.tenant_id != user.tenant_id:
        return error_response("版本不存在", 404)

    return success_response(data=version.to_dict())


@project_bp.route("/api/versions/<version_id>", methods=["PUT"])
@token_required
def update_version(version_id):
    """更新版本配置"""
    data = request.get_json()

    user = request.current_user
    if not user:
        return error_response("用户不存在", 404)

    # 租户隔离：先校验版本归属
    version = ProjectVersion.query.options(selectinload(ProjectVersion.project)).get(version_id)
    if not version:
        return error_response("版本不存在", 404)
    if getattr(user, "role", None) != "admin" and version.project and version.project.tenant_id != user.tenant_id:
        return error_response("版本不存在", 404)

    try:
        version, err = update_version_service(db, ProjectVersion, version_id, data, user)
        if err:
            status_code = 403 if err == "权限不足" else 404
            return error_response(err, status_code)
        return success_response(message="版本更新成功")
    except Exception as e:
        db.session.rollback()
        return error_response("更新失败，请重试", 500)


@project_bp.route("/api/versions/<version_id>/activate", methods=["POST"])
@token_required
def activate_version(version_id):
    """激活版本"""
    user = request.current_user
    if not user:
        return error_response("用户不存在", 404)

    # 租户隔离：先校验版本归属
    version = ProjectVersion.query.options(selectinload(ProjectVersion.project)).get(version_id)
    if not version:
        return error_response("版本不存在", 404)
    if getattr(user, "role", None) != "admin" and version.project and version.project.tenant_id != user.tenant_id:
        return error_response("版本不存在", 404)

    try:
        version, err = activate_version_service(db, ProjectVersion, version_id, user)
        if err:
            status_code = 403 if err == "权限不足" else 404
            return error_response(err, status_code)
        return success_response(message="版本激活成功")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"激活版本失败: {e}", exc_info=True)
        return error_response("激活失败，请重试", 500)


# ==================== 参数同步API ====================


@project_bp.route("/api/project/sync-params", methods=["POST"])
@token_required
def sync_params():
    """同步参数到数据库"""
    data = request.get_json()

    if not data:
        return error_response("无效的请求数据", 400)

    try:
        success, err = sync_params_service(db, Project, SohRteData, data)
        return success_response(message="参数同步成功")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"参数同步失败: {e}", exc_info=True)
        return error_response("同步失败，请重试", 500)


# ==================== 版本对比与回溯 API ====================


@project_bp.route("/api/versions/compare", methods=["POST"])
@token_required
def compare_versions():
    """对比两个版本的方案数据

    Request Body:
        { "version_ids": ["id1", "id2"] }

    Returns:
        {
            versions: [{ id, name, design, simulation, financial }, ...],
            delta: { irr: +2.5, npv: -50000, ... }
        }
    """
    import json

    data = request.get_json()
    if not data:
        return error_response("无效的请求数据", 400)

    user = request.current_user
    if not user:
        return error_response("用户不存在", 404)

    version_ids = data.get("version_ids", [])
    if len(version_ids) < 2:
        return error_response("至少需要 2 个版本ID进行对比", 400)

    try:
        versions_data = []
        for vid in version_ids:
            version = ProjectVersion.query.options(selectinload(ProjectVersion.project)).get(vid)
            if not version:
                return error_response(f"版本 {vid} 不存在", 404)

            # 租户隔离：admin 可跨租户，其余用户仅可访问同租户版本
            if (
                getattr(user, "role", None) != "admin"
                and version.project
                and version.project.tenant_id != user.tenant_id
            ):
                return error_response(f"版本 {vid} 不存在", 404)

            config = {}
            if version.config_data:
                try:
                    config = json.loads(version.config_data)
                except (json.JSONDecodeError, TypeError):
                    config = {"raw": version.config_data}

            versions_data.append(
                {
                    "id": version.id,
                    "name": version.name,
                    "version_num": version.version_num,
                    "description": version.description,
                    "created_at": version.created_at.isoformat() if version.created_at else None,
                    "config": config,
                }
            )

        # 计算差异
        delta = _compute_version_delta(versions_data)

        return success_response(
            data={
                "versions": versions_data,
                "delta": delta,
            },
            message="版本对比完成",
        )
    except Exception as e:
        current_app.logger.error(f"版本对比失败: {e}", exc_info=True)
        return error_response("版本对比失败，请重试", 500)


def _compute_version_delta(versions_data: list) -> dict:
    """计算两个版本的关键指标差异"""
    if len(versions_data) < 2:
        return {}

    def extract_metrics(config):
        """从 config 中提取关键指标"""
        fin = config.get("financial", {}) or {}
        m = fin.get("metrics", {}) or {}
        design = config.get("design", {}) or {}
        return {
            "irr": m.get("projectIrr") or m.get("irr"),
            "npv": m.get("npv"),
            "lcos": m.get("lcos") or m.get("lcoe"),
            "payback": m.get("payback"),
            "roi": m.get("roi"),
            "containerQty": design.get("containerQty"),
            "totalEnergy": design.get("totalEnergyMWh"),
            "totalPower": design.get("totalPowerMW"),
            "totalCapex": (design.get("estimatedCapex") or {}).get("totalCapex"),
        }

    m1 = extract_metrics(versions_data[0].get("config", {}))
    m2 = extract_metrics(versions_data[1].get("config", {}))

    delta = {}
    for key in m1:
        v1 = m1[key]
        v2 = m2[key]
        if v1 is None and v2 is None:
            continue
        v1 = float(v1) if v1 is not None else 0
        v2 = float(v2) if v2 is not None else 0
        diff = round(v2 - v1, 4)
        pct = round((diff / abs(v1)) * 100, 2) if v1 != 0 else 0
        delta[key] = {
            "v1": v1,
            "v2": v2,
            "diff": diff,
            "pct": pct,
        }

    return delta


@project_bp.route("/api/versions/<version_id>/restore", methods=["POST"])
@token_required
def restore_version(version_id):
    """回溯版本 — 返回版本的完整方案数据

    将指定版本的 config_data 解析为 design + simulation + financial 返回，
    前端可将其恢复到 store 中。
    """
    import json

    user = request.current_user
    if not user:
        return error_response("用户不存在", 404)

    version = ProjectVersion.query.options(selectinload(ProjectVersion.project)).get(version_id)
    if not version:
        return error_response("版本不存在", 404)

    # 租户隔离：admin 可跨租户，其余用户仅可访问同租户版本
    if getattr(user, "role", None) != "admin" and version.project and version.project.tenant_id != user.tenant_id:
        return error_response("版本不存在", 404)

    try:
        config = {}
        if version.config_data:
            try:
                config = json.loads(version.config_data)
            except (json.JSONDecodeError, TypeError):
                return error_response("版本数据格式异常，无法回溯", 500)

        return success_response(
            data={
                "version": {
                    "id": version.id,
                    "name": version.name,
                    "version_num": version.version_num,
                    "description": version.description,
                },
                "design": config.get("design"),
                "simulation": config.get("simulation"),
                "financial": config.get("financial"),
            },
            message=f"已加载方案版本: {version.name}",
        )
    except Exception as e:
        current_app.logger.error(f"版本回溯失败: {e}", exc_info=True)
        return error_response("版本回溯失败，请重试", 500)
