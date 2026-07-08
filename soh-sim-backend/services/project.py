"""
项目与版本管理服务层
"""

import json
import uuid
from datetime import datetime, timezone


def create_project_service(db, Project, ProjectVersion, data, user):
    """创建项目并自动生成第一个版本"""
    name = data.get("name", "").strip()
    if not name:
        return None, "项目名称不能为空"

    if user.role == "customer":
        return None, "权限不足，客户不能创建项目"

    project_id = str(uuid.uuid4())
    project = Project(
        id=project_id,
        name=name,
        code=data.get("code"),
        tenant_id=user.tenant_id,
        customer_id=data.get("customer_id"),
        status="active",
        stage="survey",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.session.add(project)

    version = ProjectVersion(
        id=str(uuid.uuid4()),
        project_id=project_id,
        version_num=1,
        name="方案v1",
        description="初始版本",
        is_active=True,
        created_by=user.id,
        status="draft",
        created_at=datetime.now(timezone.utc),
    )
    db.session.add(version)
    db.session.commit()

    return {"id": project_id, "version_id": version.id}, None


def update_project_service(db, Project, project_id, data, user):
    """更新项目字段"""
    if user.role == "customer":
        return None, "权限不足"

    project = Project.query.get(project_id)
    if not project:
        return None, "项目不存在"

    if "name" in data:
        project.name = data["name"]
    if "code" in data:
        project.code = data["code"]
    if "status" in data:
        project.status = data["status"]
    if "stage" in data:
        project.stage = data["stage"]
    if "config" in data:
        project.config = json.dumps(data["config"]) if isinstance(data["config"], dict) else data["config"]

    project.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    return project, None


def create_version_service(db, Project, ProjectVersion, project_id, data, user):
    """创建新版本（另存为）"""
    if user.role == "customer":
        return None, "权限不足"

    project = Project.query.get(project_id)
    if not project:
        return None, "项目不存在"

    latest_version = (
        ProjectVersion.query.filter_by(project_id=project_id).order_by(ProjectVersion.version_num.desc()).first()
    )
    new_version_num = (latest_version.version_num + 1) if latest_version else 1

    version_id = str(uuid.uuid4())
    version = ProjectVersion(
        id=version_id,
        project_id=project_id,
        version_num=new_version_num,
        name=data.get("name", f"方案v{new_version_num}"),
        description=data.get("description", ""),
        config_data=data.get(
            "config_data",
            (latest_version.config_data if latest_version else None),
        ),
        is_active=True,
        created_by=user.id,
        status="draft",
        created_at=datetime.now(timezone.utc),
    )

    ProjectVersion.query.filter_by(project_id=project_id, is_active=True).update({"is_active": False})
    db.session.add(version)
    db.session.commit()

    return {
        "id": version_id,
        "version_num": new_version_num,
    }, None


def update_version_service(db, ProjectVersion, version_id, data, user):
    """更新版本配置"""
    if user.role == "customer":
        return None, "权限不足"

    version = ProjectVersion.query.get(version_id)
    if not version:
        return None, "版本不存在"

    if "name" in data:
        version.name = data["name"]
    if "description" in data:
        version.description = data["description"]
    if "config_data" in data:
        version.config_data = (
            json.dumps(data["config_data"]) if isinstance(data["config_data"], dict) else data["config_data"]
        )
    if "status" in data:
        version.status = data["status"]
    if "is_active" in data:
        if data["is_active"]:
            ProjectVersion.query.filter_by(project_id=version.project_id).filter(
                ProjectVersion.id != version_id
            ).update({"is_active": False})
        version.is_active = data["is_active"]

    version.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    return version, None


def activate_version_service(db, ProjectVersion, version_id, user):
    """激活版本"""
    if user.role == "customer":
        return None, "权限不足"

    version = ProjectVersion.query.get(version_id)
    if not version:
        return None, "版本不存在"

    ProjectVersion.query.filter_by(project_id=version.project_id).update({"is_active": False})
    version.is_active = True
    version.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    return version, None


def sync_params_service(db, Project, SohRteData, data):
    """同步参数到数据库"""
    project_id = data.get("project_id")
    params_data = data.get("params")
    soh_data = data.get("soh")
    rte_data = data.get("rte")
    dod_data = data.get("dod")
    aug_qty_data = data.get("augQty")

    if project_id:
        project = Project.query.get(project_id)
        if project:
            config = json.loads(project.config) if project.config else {}
            config["params"] = params_data
            config["soh"] = soh_data
            config["rte"] = rte_data
            config["dod"] = dod_data
            config["augQty"] = aug_qty_data
            project.config = json.dumps(config)
            project.updated_at = datetime.now(timezone.utc)
            db.session.commit()

    soh_rte_record = SohRteData.query.first()
    if soh_rte_record:
        soh_rte_record.soh_values = json.dumps(soh_data) if soh_data else None
        soh_rte_record.rte_values = json.dumps(rte_data) if rte_data else None
        soh_rte_record.dod_values = json.dumps(dod_data) if dod_data else None
        soh_rte_record.aug_qty_values = json.dumps(aug_qty_data) if aug_qty_data else None
        soh_rte_record.updated_at = datetime.now(timezone.utc)
    else:
        soh_rte_record = SohRteData(
            id=str(uuid.uuid4()),
            soh_values=(json.dumps(soh_data) if soh_data else None),
            rte_values=(json.dumps(rte_data) if rte_data else None),
            dod_values=(json.dumps(dod_data) if dod_data else None),
            aug_qty_values=(json.dumps(aug_qty_data) if aug_qty_data else None),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.session.add(soh_rte_record)

    db.session.commit()
    return True, None
