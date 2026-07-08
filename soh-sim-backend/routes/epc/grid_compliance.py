"""EPC - 电网合规 路由"""
import json
import uuid

from flask import Blueprint, request

from database import GridComplianceAnalysis, db
from routes.auth import token_required
from routes.epc._common import check_project_access, get_or_404
from services.epc.grid_compliance import (
    GRID_STANDARDS,
    analyze_grid_compliance_service,
)
from utils.api_response import error_response, success_response

grid_compliance_bp = Blueprint("epc_grid_compliance", __name__)


@grid_compliance_bp.route(
    "/api/grid-compliance/standards", methods=["GET"]
)
@token_required
def list_grid_standards():
    """获取支持的电网标准"""
    return success_response(data=GRID_STANDARDS)


@grid_compliance_bp.route(
    "/api/grid-compliance/analyze", methods=["POST"]
)
@token_required
def analyze_grid_compliance():
    """执行电网合规分析"""
    data = request.get_json()
    project_id = data.get("project_id")
    user = request.current_user
    if project_id and not check_project_access(project_id, user):
        return error_response("无权访问该项目", 403)

    result = analyze_grid_compliance_service(data)

    gc = GridComplianceAnalysis(
        id=str(uuid.uuid4()),
        project_id=data.get("project_id"),
        **{
            k: v
            for k, v in result.items()
            if hasattr(GridComplianceAnalysis, k)
            and k
            not in [
                "lvrt_curve",
                "hvrt_curve",
                "freq_response_curve",
                "failed_items",
            ]
        },
    )
    gc.lvrt_curve = json.dumps(result["lvrt_curve"])
    gc.hvrt_curve = json.dumps(result["hvrt_curve"])
    gc.freq_response_curve = json.dumps(
        result["freq_response_curve"]
    )
    gc.failed_items = json.dumps(result["failed_items"])
    db.session.add(gc)
    db.session.commit()

    return success_response(data=result, message={"id": gc.id})


@grid_compliance_bp.route(
    "/api/grid-compliance/<gc_id>", methods=["GET"]
)
@token_required
def get_grid_compliance(gc_id):
    user = request.current_user
    obj = get_or_404(GridComplianceAnalysis, gc_id)
    if not obj:
        return error_response("未找到", 404)
    if (
        getattr(user, "role", None) != "admin"
        and getattr(obj, "tenant_id", None) != user.tenant_id
    ):
        return error_response("无权访问该项目", 403)
    return success_response(data=obj.to_dict())
