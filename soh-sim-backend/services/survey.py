"""
调研表服务层
"""

import json
import uuid
from datetime import datetime, timezone

SURVEY_UPDATABLE_FIELDS = [
    "project_name",
    "contact_person",
    "contact_phone",
    "contact_email",
    "location",
    "altitude",
    "total_mw",
    "total_mwh",
    "duration",
    "cycles_per_day",
    "temp_max",
    "temp_min",
    "temp_avg",
    "humidity",
    "grid_voltage",
    "grid_frequency",
    "rte_target",
    "soh_year1",
    "soh_year25",
    "calendar_life",
    "cycle_life",
    "availability_target",
    "aux_consumption",
    "response_time",
    "dc_voltage_range",
    "ac_voltage",
    "thdi",
    "remarks",
    "status",
]


def submit_survey_service(db, Project, Survey, data):
    """提交调研表，自动创建关联项目"""
    survey_id = str(uuid.uuid4())
    project_id = str(uuid.uuid4())
    project_code = f"PRJ-{datetime.now().strftime('%Y%m%d')}-{project_id[:8].upper()}"

    project = Project(
        id=project_id,
        name=data.get("project_name", "未命名项目"),
        code=project_code,
        status="draft",
        stage="survey",
        config=json.dumps(
            {
                "survey_id": survey_id,
                "created_from": "survey",
                "basic_params": {
                    "total_mw": data.get("total_mw"),
                    "total_mwh": data.get("total_mwh"),
                    "duration": data.get("duration"),
                    "location": data.get("location"),
                },
            }
        ),
    )
    db.session.add(project)

    survey = Survey(
        id=survey_id,
        project_name=data.get("project_name"),
        contact_person=data.get("contact_person"),
        contact_phone=data.get("contact_phone"),
        contact_email=data.get("contact_email"),
        location=data.get("location"),
        altitude=data.get("altitude"),
        total_mw=data.get("total_mw"),
        total_mwh=data.get("total_mwh"),
        duration=data.get("duration"),
        cycles_per_day=data.get("cycles_per_day", 1.0),
        temp_max=data.get("temp_max"),
        temp_min=data.get("temp_min"),
        temp_avg=data.get("temp_avg"),
        humidity=data.get("humidity"),
        grid_voltage=data.get("grid_voltage"),
        grid_frequency=data.get("grid_frequency"),
        rte_target=data.get("rte_target"),
        soh_year1=data.get("soh_year1"),
        soh_year25=data.get("soh_year25"),
        calendar_life=data.get("calendar_life"),
        cycle_life=data.get("cycle_life"),
        availability_target=data.get("availability_target"),
        aux_consumption=data.get("aux_consumption"),
        response_time=data.get("response_time"),
        dc_voltage_range=data.get("dc_voltage_range"),
        ac_voltage=data.get("ac_voltage"),
        thdi=data.get("thdi"),
        remarks=data.get("remarks"),
        attachments=json.dumps(data.get("attachments", [])),
        status="pending",
        project_id=project_id,
    )
    db.session.add(survey)
    db.session.commit()

    return {
        "survey_id": survey_id,
        "project_id": project_id,
        "project_code": project_code,
    }, None


def update_survey_service(db, Survey, survey_id, data):
    """更新调研表"""
    survey = Survey.query.get(survey_id)
    if not survey:
        return None, "调研表不存在"

    for field in SURVEY_UPDATABLE_FIELDS:
        if field in data:
            setattr(survey, field, data[field])

    if "attachments" in data:
        survey.attachments = json.dumps(data["attachments"])

    survey.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    return survey, None


def delete_project_cascade_service(db, Project, Survey, project_id):
    """删除项目（级联删除关联调研表）"""
    project = Project.query.get(project_id)
    if not project:
        return None, "项目不存在"

    Survey.query.filter_by(project_id=project_id).delete()
    db.session.delete(project)
    db.session.commit()

    return project, None
