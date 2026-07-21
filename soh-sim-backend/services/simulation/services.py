"""
仿真结果与校正因子模板服务层
"""

import json
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import selectinload


def get_or_create_default_version(db, Project, ProjectVersion, user_id, tenant_id, version_id):
    """获取或创建默认版本，返回 actual_version_id 或错误"""
    if version_id != "default":
        version = ProjectVersion.query.get(version_id)
        if not version:
            return None, "版本不存在"
        return version_id, None

    project = Project.query.filter_by(tenant_id=tenant_id).first()
    if project:
        version = ProjectVersion.query.filter_by(project_id=project.id, is_active=True).first()
        if version:
            return version.id, None
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
            created_at=datetime.now(timezone.utc),
        )
        db.session.add(version)
        return actual_version_id, None

    # 创建默认项目和版本
    project_id = str(uuid.uuid4())
    project = Project(
        id=project_id,
        tenant_id=tenant_id,
        name="默认项目",
        code=f"DEF-{user_id[:8]}",
        status="draft",
        stage="survey",
        created_at=datetime.now(timezone.utc),
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
        created_at=datetime.now(timezone.utc),
    )
    db.session.add(version)
    return actual_version_id, None


def create_simulation_result_service(db, Project, ProjectVersion, SimulationResult, data, version_id, user):
    """保存仿真结果"""
    if user.role == "customer":
        return None, "权限不足"

    actual_version_id, err = get_or_create_default_version(
        db, Project, ProjectVersion, user.id, user.tenant_id, version_id
    )
    if err:
        return None, err

    version = ProjectVersion.query.options(selectinload(ProjectVersion.project)).get(actual_version_id)
    project = version.project if version else None
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
        executed_at=data.get("executed_at", datetime.now(timezone.utc)),
        execution_time_ms=data.get("execution_time_ms"),
        created_by=user.id,
        created_at=datetime.now(timezone.utc),
    )
    db.session.add(result)
    db.session.commit()

    return {"id": result_id, "name": result.name}, None


def create_template_service(db, CorrectionTemplate, data, user):
    """创建校正因子模板"""
    if user.role == "customer":
        return None, "权限不足"

    name = data.get("name", "").strip()
    if not name:
        return None, "模板名称不能为空"

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
        created_by=user.id,
        created_at=datetime.now(timezone.utc),
    )

    if template.is_default:
        CorrectionTemplate.query.filter_by(tenant_id=user.tenant_id).update({"is_default": False})

    db.session.add(template)
    db.session.commit()

    return {"id": template_id}, None


def update_template_service(db, CorrectionTemplate, template_id, data, user):
    """更新校正因子模板"""
    if user.role == "customer":
        return None, "权限不足"

    template = CorrectionTemplate.query.get(template_id)
    if not template:
        return None, "模板不存在"

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

    template.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    return template, None


DEFAULT_TEMPLATES = [
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


def seed_templates_service(db, CorrectionTemplate, user):
    """初始化默认校正因子模板"""
    if CorrectionTemplate.query.first():
        return None, "模板已存在，请勿重复初始化"

    for t_data in DEFAULT_TEMPLATES:
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
            created_by=user.id,
            created_at=datetime.now(timezone.utc),
        )
        db.session.add(template)

    db.session.commit()
    return {"count": len(DEFAULT_TEMPLATES)}, None
