"""
仿真结果与校正因子模板API路由
仿真结果完整存储带日期戳，支持多模板管理
"""

import json
import uuid
from datetime import datetime

from flask import Blueprint, jsonify, request

from routes.auth import role_required, token_required

simulation_bp = Blueprint("simulation", __name__)


# ==================== 仿真结果API ====================


@simulation_bp.route("/api/versions/<version_id>/results", methods=["GET"])
@token_required
def get_simulation_results(version_id):
    """获取版本的所有仿真结果"""
    user = request.current_user

    from database import AlgorithmModel, CorrectionTemplate, ProjectVersion, SimulationResult, db

    version = ProjectVersion.query.get(version_id)
    if not version:
        return jsonify({"error": "版本不存在"}), 404

    results = (
        SimulationResult.query.filter_by(version_id=version_id).order_by(SimulationResult.executed_at.desc()).all()
    )

    return jsonify(
        {
            "success": True,
            "data": [
                {
                    "id": r.id,
                    "name": r.name,
                    "description": r.description,
                    "simulation_type": r.simulation_type,
                    "correction_template_id": r.correction_template_id,
                    "params": json.loads(r.params) if r.params else None,
                    "summary": json.loads(r.summary) if r.summary else None,
                    "status": r.status,
                    "executed_at": r.executed_at.isoformat() if r.executed_at else None,
                    "execution_time_ms": r.execution_time_ms,
                    "created_by": r.created_by,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                }
                for r in results
            ],
        }
    )


@simulation_bp.route("/api/versions/<version_id>/results", methods=["POST"])
@token_required
def create_simulation_result(version_id):
    """保存仿真结果"""
    user_id = request.user_id
    data = request.get_json()

    from database import Project, ProjectVersion, SimulationResult, User, db

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "用户不存在"}), 404

    # 检查权限（客户不能保存仿真结果）
    if user.role == "customer":
        return jsonify({"error": "权限不足"}), 403

    # 支持默认版本路径
    actual_version_id = version_id
    if version_id == "default":
        # 查找用户的第一个项目的活跃版本
        project = Project.query.filter_by(tenant_id=user.tenant_id).first()
        if project:
            version = ProjectVersion.query.filter_by(project_id=project.id, is_active=True).first()
            if version:
                actual_version_id = version.id
            else:
                # 创建默认版本
                actual_version_id = str(uuid.uuid4())
                version = ProjectVersion(
                    id=actual_version_id,
                    project_id=project.id,
                    version_num=1,
                    name="默认版本",
                    is_active=True,
                    config_data="{}",
                    created_by=user_id,
                    status="in-use",
                    created_at=datetime.utcnow(),
                )
                db.session.add(version)
        else:
            # 创建默认项目和版本
            project_id = str(uuid.uuid4())
            project = Project(
                id=project_id,
                tenant_id=user.tenant_id,
                name="默认项目",
                code=f"DEF-{user_id[:8]}",
                status="draft",
                stage="survey",
                created_at=datetime.utcnow(),
            )
            db.session.add(project)

            actual_version_id = str(uuid.uuid4())
            version = ProjectVersion(
                id=actual_version_id,
                project_id=project_id,
                version_num=1,
                name="默认版本",
                is_active=True,
                config_data="{}",
                created_by=user_id,
                status="in-use",
                created_at=datetime.utcnow(),
            )
            db.session.add(version)
    else:
        version = ProjectVersion.query.get(version_id)
        if not version:
            return jsonify({"error": "版本不存在"}), 404

    # 生成名称（项目名称+时间戳）
    project = Project.query.get(version.project_id)
    project_name = project.name if project else "未命名项目"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_name = f"{project_name}_{timestamp}"

    result_id = str(uuid.uuid4())
    result = SimulationResult(
        id=result_id,
        version_id=actual_version_id,
        name=data.get("name", default_name),
        description=data.get("description"),
        simulation_type=data.get("simulation_type", "comprehensive"),
        algorithm_model_id=data.get("algorithm_model_id"),
        correction_template_id=data.get("correction_template_id"),
        params=json.dumps(data.get("params", {})) if isinstance(data.get("params"), dict) else data.get("params"),
        results=json.dumps(data.get("results", {})) if isinstance(data.get("results"), dict) else data.get("results"),
        summary=json.dumps(data.get("summary", {})) if isinstance(data.get("summary"), dict) else data.get("summary"),
        status=data.get("status", "completed"),
        executed_at=data.get("executed_at", datetime.utcnow()),
        execution_time_ms=data.get("execution_time_ms"),
        created_by=user_id,
        created_at=datetime.utcnow(),
    )

    db.session.add(result)

    try:
        db.session.commit()
        return jsonify({"success": True, "id": result_id, "name": result.name, "message": "仿真结果保存成功"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"保存失败: {str(e)}"}), 500


@simulation_bp.route("/api/results/<result_id>", methods=["GET"])
@token_required
def get_simulation_result(result_id):
    """获取单条仿真结果详情"""
    user = request.current_user

    from database import CorrectionTemplate, db

    result = SimulationResult.query.get(result_id)
    if not result:
        return jsonify({"error": "仿真结果不存在"}), 404

    return jsonify(
        {
            "success": True,
            "data": {
                "id": result.id,
                "version_id": result.version_id,
                "name": result.name,
                "description": result.description,
                "simulation_type": result.simulation_type,
                "correction_template_id": result.correction_template_id,
                "params": json.loads(result.params) if result.params else None,
                "results": json.loads(result.results) if result.results else None,
                "summary": json.loads(result.summary) if result.summary else None,
                "status": result.status,
                "executed_at": result.executed_at.isoformat() if result.executed_at else None,
                "execution_time_ms": result.execution_time_ms,
                "created_by": result.created_by,
                "created_at": result.created_at.isoformat() if result.created_at else None,
            },
        }
    )


@simulation_bp.route("/api/results/<result_id>", methods=["DELETE"])
@token_required
@role_required("engineer", "admin")
def delete_simulation_result(result_id):
    """删除仿真结果"""
    from database import SimulationResult, db

    result = SimulationResult.query.get(result_id)
    if not result:
        return jsonify({"error": "仿真结果不存在"}), 404

    try:
        db.session.delete(result)
        db.session.commit()
        return jsonify({"success": True, "message": "删除成功"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"删除失败: {str(e)}"}), 500


# ==================== 校正因子模板API ====================


@simulation_bp.route("/api/correction-templates", methods=["GET"])
@token_required
def get_correction_templates():
    """获取校正因子模板列表"""
    user = request.current_user

    from database import CorrectionTemplate, db

    query = CorrectionTemplate.query.filter_by(status="active")

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    # 如果有租户筛选
    if user.tenant_id:
        query = query.filter((CorrectionTemplate.tenant_id == user.tenant_id) | (CorrectionTemplate.tenant_id == None))

    pagination = query.order_by(CorrectionTemplate.is_default.desc(), CorrectionTemplate.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify(
        {
            "success": True,
            "data": [
                {
                    "id": t.id,
                    "name": t.name,
                    "description": t.description,
                    "template_type": t.template_type,
                    "global_soh_factor": t.global_soh_factor,
                    "global_rte_factor": t.global_rte_factor,
                    "annual_corrections": json.loads(t.annual_corrections) if t.annual_corrections else {},
                    "is_default": t.is_default,
                    "status": t.status,
                    "created_by": t.created_by,
                    "created_at": t.created_at.isoformat() if t.created_at else None,
                    "updated_at": t.updated_at.isoformat() if t.updated_at else None,
                }
                for t in pagination.items
            ],
            "total": pagination.total,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "pages": pagination.pages,
        }
    )


@simulation_bp.route("/api/correction-templates", methods=["POST"])
@token_required
def create_correction_template():
    """创建校正因子模板"""
    user_id = request.user_id
    data = request.get_json()

    from database import CorrectionTemplate, User, db

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "用户不存在"}), 404

    # 检查权限（客户不能创建模板）
    if user.role == "customer":
        return jsonify({"error": "权限不足"}), 403

    name = data.get("name", "").strip()
    if not name:
        return jsonify({"error": "模板名称不能为空"}), 400

    template_id = str(uuid.uuid4())
    template = CorrectionTemplate(
        id=template_id,
        tenant_id=user.tenant_id,
        name=name,
        description=data.get("description"),
        template_type=data.get("template_type", "comprehensive"),
        global_soh_factor=data.get("global_soh_factor", 1.0),
        global_rte_factor=data.get("global_rte_factor", 1.0),
        annual_corrections=(
            json.dumps(data.get("annual_corrections", {}))
            if isinstance(data.get("annual_corrections"), dict)
            else json.dumps({})
        ),
        is_default=data.get("is_default", False),
        status="active",
        created_by=user_id,
        created_at=datetime.utcnow(),
    )

    # 如果设为默认，取消其他默认
    if template.is_default:
        CorrectionTemplate.query.filter_by(tenant_id=user.tenant_id).update({"is_default": False})

    db.session.add(template)

    try:
        db.session.commit()
        return jsonify({"success": True, "id": template_id, "message": "模板创建成功"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"创建失败: {str(e)}"}), 500


@simulation_bp.route("/api/correction-templates/<template_id>", methods=["GET"])
@token_required
def get_correction_template(template_id):
    """获取校正因子模板详情"""
    from database import CorrectionTemplate, db

    template = CorrectionTemplate.query.get(template_id)
    if not template:
        return jsonify({"error": "模板不存在"}), 404

    return jsonify(
        {
            "success": True,
            "data": {
                "id": template.id,
                "name": template.name,
                "description": template.description,
                "template_type": template.template_type,
                "global_soh_factor": template.global_soh_factor,
                "global_rte_factor": template.global_rte_factor,
                "annual_corrections": json.loads(template.annual_corrections) if template.annual_corrections else {},
                "is_default": template.is_default,
                "status": template.status,
                "created_by": template.created_by,
                "created_at": template.created_at.isoformat() if template.created_at else None,
                "updated_at": template.updated_at.isoformat() if template.updated_at else None,
            },
        }
    )


@simulation_bp.route("/api/correction-templates/<template_id>", methods=["PUT"])
@token_required
def update_correction_template(template_id):
    """更新校正因子模板"""
    user_id = request.user_id
    data = request.get_json()

    from database import CorrectionTemplate, User, db

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "用户不存在"}), 404

    # 检查权限（客户不能更新模板）
    if user.role == "customer":
        return jsonify({"error": "权限不足"}), 403

    template = CorrectionTemplate.query.get(template_id)
    if not template:
        return jsonify({"error": "模板不存在"}), 404

    # 更新字段
    if "name" in data:
        template.name = data["name"]
    if "description" in data:
        template.description = data["description"]
    if "template_type" in data:
        template.template_type = data["template_type"]
    if "global_soh_factor" in data:
        template.global_soh_factor = data["global_soh_factor"]
    if "global_rte_factor" in data:
        template.global_rte_factor = data["global_rte_factor"]
    if "annual_corrections" in data:
        template.annual_corrections = (
            json.dumps(data["annual_corrections"])
            if isinstance(data["annual_corrections"], dict)
            else data["annual_corrections"]
        )
    if "is_default" in data:
        if data["is_default"]:
            CorrectionTemplate.query.filter_by(tenant_id=user.tenant_id).update({"is_default": False})
        template.is_default = data["is_default"]
    if "status" in data:
        template.status = data["status"]

    template.updated_at = datetime.utcnow()

    try:
        db.session.commit()
        return jsonify({"success": True, "message": "模板更新成功"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"更新失败: {str(e)}"}), 500


@simulation_bp.route("/api/correction-templates/<template_id>", methods=["DELETE"])
@token_required
@role_required("engineer", "admin")
def delete_correction_template(template_id):
    """删除校正因子模板"""
    from database import CorrectionTemplate, db

    template = CorrectionTemplate.query.get(template_id)
    if not template:
        return jsonify({"error": "模板不存在"}), 404

    # 不能删除默认模板
    if template.is_default:
        return jsonify({"error": "不能删除默认模板"}), 400

    try:
        db.session.delete(template)
        db.session.commit()
        return jsonify({"success": True, "message": "删除成功"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"删除失败: {str(e)}"}), 500


@simulation_bp.route("/api/correction-templates/seed", methods=["POST"])
@token_required
def seed_correction_templates():
    """初始化默认校正因子模板"""
    user_id = request.user_id

    from database import CorrectionTemplate, User, db

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "用户不存在"}), 404

    # 检查是否已有模板
    if CorrectionTemplate.query.first():
        return jsonify({"error": "模板已存在，请勿重复初始化"}), 400

    # 创建默认模板
    default_templates = [
        {
            "name": "标准校正",
            "description": "标准校正因子，适用于常规项目",
            "template_type": "comprehensive",
            "global_soh_factor": 1.0,
            "global_rte_factor": 1.0,
            "annual_corrections": {1: 0.98, 5: 0.95, 10: 0.88, 15: 0.80, 20: 0.72, 25: 0.65},
            "is_default": True,
        },
        {
            "name": "乐观校正",
            "description": "乐观场景校正因子，适用于实验室条件",
            "template_type": "comprehensive",
            "global_soh_factor": 1.02,
            "global_rte_factor": 1.01,
            "annual_corrections": {1: 0.99, 5: 0.97, 10: 0.92, 15: 0.85, 20: 0.78, 25: 0.70},
            "is_default": False,
        },
        {
            "name": "保守校正",
            "description": "保守场景校正因子，适用于极端环境",
            "template_type": "comprehensive",
            "global_soh_factor": 0.98,
            "global_rte_factor": 0.99,
            "annual_corrections": {1: 0.96, 5: 0.92, 10: 0.82, 15: 0.72, 20: 0.62, 25: 0.55},
            "is_default": False,
        },
    ]

    try:
        for t_data in default_templates:
            template = CorrectionTemplate(
                id=str(uuid.uuid4()),
                tenant_id=user.tenant_id,
                name=t_data["name"],
                description=t_data["description"],
                template_type=t_data["template_type"],
                global_soh_factor=t_data["global_soh_factor"],
                global_rte_factor=t_data["global_rte_factor"],
                annual_corrections=json.dumps(t_data["annual_corrections"]),
                is_default=t_data["is_default"],
                status="active",
                created_by=user_id,
                created_at=datetime.utcnow(),
            )
            db.session.add(template)

        db.session.commit()
        return jsonify({"success": True, "message": "默认模板初始化成功"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"初始化失败: {str(e)}"}), 500
