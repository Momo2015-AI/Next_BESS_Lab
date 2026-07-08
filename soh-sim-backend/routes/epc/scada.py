"""EPC - SCADA/EMS 路由"""
import json
import uuid

from flask import Blueprint, request

from database import ScadaEmsDesign, db
from routes.auth import token_required
from routes.epc._common import check_project_access, get_or_404
from services.epc.scada import design_scada_ems_service
from utils.api_response import error_response, success_response

scada_bp = Blueprint("epc_scada", __name__)


@scada_bp.route("/api/scada-ems/design", methods=["POST"])
@token_required
def design_scada_ems():
    """SCADA/EMS设计"""
    data = request.get_json()
    project_id = data.get("project_id")
    user = request.current_user
    if project_id and not check_project_access(project_id, user):
        return error_response("无权访问该项目", 403)

    result = design_scada_ems_service(data)

    ems_functions = result["ems_functions"]
    se = ScadaEmsDesign(
        id=str(uuid.uuid4()),
        project_id=data.get("project_id"),
        **{
            k: v
            for k, v in result.items()
            if hasattr(ScadaEmsDesign, k)
            and k
            not in [
                "ems_functions",
                "firewall_config",
                "architecture_diagram",
            ]
        },
    )
    se.ems_functions = json.dumps(ems_functions)
    se.firewall_config = json.dumps(
        {"config": result["firewall_config"]}
    )
    se.architecture_diagram = json.dumps(
        result["architecture_diagram"]
    )
    db.session.add(se)
    db.session.commit()

    return success_response(data=result, message={"id": se.id})


@scada_bp.route("/api/scada-ems/<se_id>", methods=["GET"])
@token_required
def get_scada_ems(se_id):
    user = request.current_user
    obj = get_or_404(ScadaEmsDesign, se_id)
    if not obj:
        return error_response("未找到", 404)
    if (
        getattr(user, "role", None) != "admin"
        and getattr(obj, "tenant_id", None) != user.tenant_id
    ):
        return error_response("无权访问该项目", 403)
    return success_response(data=obj.to_dict())
