"""EPC - 系统架构设计 路由"""

import json
import uuid

from flask import Blueprint, request

from database import SystemArchitecture, db
from routes.auth import token_required
from routes.epc._common import check_project_access, get_or_404
from services.epc_modules import design_architecture_service
from utils.api_response import error_response, success_response

architecture_bp = Blueprint("epc_architecture", __name__)


@architecture_bp.route("/api/system-architecture", methods=["GET"])
@token_required
def list_architectures():
    user = request.current_user
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))
    project_id = request.args.get("project_id")
    query = SystemArchitecture.query
    if project_id:
        query = query.filter_by(project_id=project_id)
    if getattr(user, "role", None) != "admin":
        query = query.filter_by(tenant_id=user.tenant_id)
    pagination = query.order_by(SystemArchitecture.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return success_response(
        data={
            "items": [item.to_dict() for item in pagination.items],
            "total": pagination.total,
            "page": page,
            "per_page": per_page,
            "pages": pagination.pages,
        }
    )


@architecture_bp.route("/api/system-architecture/<arch_id>", methods=["GET"])
@token_required
def get_architecture(arch_id):
    user = request.current_user
    obj = get_or_404(SystemArchitecture, arch_id)
    if not obj:
        return error_response("未找到", 404)
    if getattr(user, "role", None) != "admin" and getattr(obj, "tenant_id", None) != user.tenant_id:
        return error_response("无权访问该项目", 403)
    return success_response(data=obj.to_dict())


@architecture_bp.route("/api/system-architecture/design", methods=["POST"])
@token_required
def design_architecture():
    """自动设计系统架构"""
    data = request.get_json()
    project_id = data.get("project_id")
    user = request.current_user
    if project_id and not check_project_access(project_id, user):
        return error_response("无权访问该项目", 403)

    result = design_architecture_service(data)

    arch = SystemArchitecture(
        id=str(uuid.uuid4()),
        project_id=data.get("project_id"),
        **{k: v for k, v in result.items() if hasattr(SystemArchitecture, k) and k not in ["stages", "topology_data"]},
    )
    arch.stages = json.dumps(result["stages"])
    arch.topology_data = json.dumps(result["topology_data"])
    db.session.add(arch)
    db.session.commit()

    return success_response(data=result, message={"id": arch.id})
