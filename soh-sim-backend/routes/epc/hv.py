"""EPC - 高压接入 路由"""
import json
import uuid

from flask import Blueprint, request

from database import HVInterconnection, db
from routes.auth import token_required
from routes.epc._common import check_project_access, get_or_404
from services.epc.hv import design_hv_interconnection_service
from utils.api_response import error_response, success_response

hv_bp = Blueprint("epc_hv", __name__)


@hv_bp.route("/api/hv-interconnection/design", methods=["POST"])
@token_required
def design_hv_interconnection():
    """高压接入设计"""
    data = request.get_json()
    project_id = data.get("project_id")
    user = request.current_user
    if project_id and not check_project_access(project_id, user):
        return error_response("无权访问该项目", 403)

    result = design_hv_interconnection_service(data)

    protections = result["protection_scheme"]
    hv = HVInterconnection(
        id=str(uuid.uuid4()),
        project_id=data.get("project_id"),
        **{
            k: v
            for k, v in result.items()
            if hasattr(HVInterconnection, k)
            and k
            not in ["protection_scheme", "single_line_diagram"]
        },
    )
    hv.protection_scheme = json.dumps(protections)
    hv.single_line_diagram = json.dumps(
        result["single_line_diagram"]
    )
    db.session.add(hv)
    db.session.commit()

    return success_response(data=result, message={"id": hv.id})


@hv_bp.route("/api/hv-interconnection/<hv_id>", methods=["GET"])
@token_required
def get_hv_interconnection(hv_id):
    user = request.current_user
    obj = get_or_404(HVInterconnection, hv_id)
    if not obj:
        return error_response("未找到", 404)
    if (
        getattr(user, "role", None) != "admin"
        and getattr(obj, "tenant_id", None) != user.tenant_id
    ):
        return error_response("无权访问该项目", 403)
    return success_response(data=obj.to_dict())
