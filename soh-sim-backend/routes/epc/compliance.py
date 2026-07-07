"""EPC - 合规矩阵 路由"""
import json
import uuid

from flask import Blueprint, request

from database import ComplianceMatrix, db
from routes.auth import token_required
from routes.epc._common import check_project_access, get_or_404
from services.epc.compliance import COMPLIANCE_TEMPLATES, generate_compliance_matrix_service
from utils.api_response import error_response, success_response

compliance_bp = Blueprint("epc_compliance", __name__)


@compliance_bp.route("/api/compliance-matrix/templates", methods=["GET"])
@token_required
def list_compliance_templates():
    return success_response(data=[{"code": k, "name": v["name"]} for k, v in COMPLIANCE_TEMPLATES.items()])


@compliance_bp.route("/api/compliance-matrix/generate", methods=["POST"])
@token_required
def generate_compliance_matrix():
    """生成合规矩阵"""
    data = request.get_json()
    project_id = data.get("project_id")
    user = request.current_user
    if project_id and not check_project_access(project_id, user):
        return error_response("无权访问该项目", 403)

    result, err = generate_compliance_matrix_service(data)
    if err:
        return error_response(err, 400)

    cm = ComplianceMatrix(
        id=str(uuid.uuid4()),
        project_id=data.get("project_id"),
        rfp_name=result["template_name"],
        rfp_version="Rev01",
        rfp_standard=result["template_code"],
        total_items=result["total"],
        compliant_count=result["compliant"],
        non_compliant_count=result["non_compliant"],
        partial_count=result["partial"],
    )
    cm.matrix_data = json.dumps(result["matrix"])
    db.session.add(cm)
    db.session.commit()

    return success_response(data={
        "matrix": result["matrix"],
        "total": result["total"],
        "compliant": result["compliant"],
        "non_compliant": result["non_compliant"],
        "partial": result["partial"],
    }, message={"id": cm.id})


@compliance_bp.route("/api/compliance-matrix/<cm_id>", methods=["GET"])
@token_required
def get_compliance_matrix(cm_id):
    user = request.current_user
    obj = get_or_404(ComplianceMatrix, cm_id)
    if not obj:
        return error_response("未找到", 404)
    if getattr(user, "role", None) != "admin" and getattr(obj, "tenant_id", None) != user.tenant_id:
        return error_response("无权访问该项目", 403)
    return success_response(data=obj.to_dict())


@compliance_bp.route("/api/compliance-matrix/<cm_id>", methods=["PUT"])
@token_required
def update_compliance_matrix_item(cm_id):
    """更新合规矩阵中的单项"""
    user = request.current_user
    obj = get_or_404(ComplianceMatrix, cm_id)
    if not obj:
        return error_response("未找到", 404)
    if getattr(user, "role", None) != "admin" and getattr(obj, "tenant_id", None) != user.tenant_id:
        return error_response("无权访问该项目", 403)

    data = request.get_json()
    matrix = json.loads(obj.matrix_data) if obj.matrix_data else []

    for item in matrix:
        if item["section"] == data.get("section"):
            item["compliance_status"] = data.get("compliance_status", item["compliance_status"])
            item["response"] = data.get("response", item["response"])
            item["evidence"] = data.get("evidence", item.get("evidence", ""))
            item["reference_doc"] = data.get("reference_doc", item.get("reference_doc", ""))
            item["verified"] = data.get("verified", item.get("verified", False))
            break

    obj.matrix_data = json.dumps(matrix)
    obj.compliant_count = sum(1 for m in matrix if m["compliance_status"] == "compliant")
    obj.non_compliant_count = sum(1 for m in matrix if m["compliance_status"] == "non_compliant")
    obj.partial_count = sum(1 for m in matrix if m["compliance_status"] == "partial")
    db.session.commit()

    return success_response(data=matrix)
