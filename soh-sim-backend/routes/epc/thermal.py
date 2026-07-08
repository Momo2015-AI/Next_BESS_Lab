"""EPC - 热管理 路由"""

import json
import uuid

from flask import Blueprint, request

from database import ThermalManagement, db
from routes.auth import token_required
from routes.epc._common import check_project_access, get_or_404
from services.epc.thermal import calculate_thermal_service
from utils.api_response import error_response, success_response

thermal_bp = Blueprint("epc_thermal", __name__)


@thermal_bp.route("/api/thermal-management/calculate", methods=["POST"])
@token_required
def calculate_thermal():
    """热管理设计计算"""
    data = request.get_json()
    project_id = data.get("project_id")
    user = request.current_user
    if project_id and not check_project_access(project_id, user):
        return error_response("无权访问该项目", 403)

    result = calculate_thermal_service(data)

    tm = ThermalManagement(
        id=str(uuid.uuid4()),
        project_id=data.get("project_id"),
        **{k: v for k, v in result.items() if hasattr(ThermalManagement, k) and k != "derating_curve"},
    )
    tm.derating_curve = json.dumps(result["derating_curve"])
    db.session.add(tm)
    db.session.commit()

    return success_response(data=result, message={"id": tm.id})


@thermal_bp.route("/api/thermal-management/<tm_id>", methods=["GET"])
@token_required
def get_thermal(tm_id):
    user = request.current_user
    obj = get_or_404(ThermalManagement, tm_id)
    if not obj:
        return error_response("未找到", 404)
    if getattr(user, "role", None) != "admin" and getattr(obj, "tenant_id", None) != user.tenant_id:
        return error_response("无权访问该项目", 403)
    return success_response(data=obj.to_dict())
