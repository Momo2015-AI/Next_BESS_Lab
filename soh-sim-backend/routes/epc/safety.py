"""EPC - 安全消防 路由"""
import json
import uuid

from flask import Blueprint, request

from database import SafetyFireDesign, db
from routes.auth import token_required
from routes.epc._common import check_project_access, get_or_404
from services.epc.safety import (
    SAFETY_STANDARDS,
    analyze_safety_design_service,
)
from utils.api_response import error_response, success_response

safety_bp = Blueprint("epc_safety", __name__)


@safety_bp.route("/api/safety-design/analyze", methods=["POST"])
@token_required
def analyze_safety_design():
    """安全与消防设计分析"""
    data = request.get_json()
    project_id = data.get("project_id")
    user = request.current_user
    if project_id and not check_project_access(project_id, user):
        return error_response("无权访问该项目", 403)

    result = analyze_safety_design_service(data)

    sf = SafetyFireDesign(
        id=str(uuid.uuid4()),
        project_id=data.get("project_id"),
        **{
            k: v
            for k, v in result.items()
            if hasattr(SafetyFireDesign, k)
            and k not in ["design_data", "compliance_report"]
        },
    )
    sf.design_data = json.dumps(result["design_data"])
    sf.compliance_report = json.dumps(
        result["compliance_report"]
    )
    db.session.add(sf)
    db.session.commit()

    return success_response(data=result, message={"id": sf.id})


@safety_bp.route("/api/safety-design/<sf_id>", methods=["GET"])
@token_required
def get_safety_design(sf_id):
    user = request.current_user
    obj = get_or_404(SafetyFireDesign, sf_id)
    if not obj:
        return error_response("未找到", 404)
    if (
        getattr(user, "role", None) != "admin"
        and getattr(obj, "tenant_id", None) != user.tenant_id
    ):
        return error_response("无权访问该项目", 403)
    return success_response(data=obj.to_dict())


@safety_bp.route("/api/safety-design/standards", methods=["GET"])
@token_required
def list_safety_standards():
    return success_response(data=SAFETY_STANDARDS)
