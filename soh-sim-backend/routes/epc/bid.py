"""EPC - 投标文档 路由"""

import json
import uuid

from flask import Blueprint, request

from database import BidDocument, db
from routes.auth import token_required
from routes.epc._common import check_project_access, get_or_404
from services.epc.bid import (
    BID_DOCUMENT_TEMPLATES,
    generate_bid_document_service,
)
from utils.api_response import error_response, success_response

bid_bp = Blueprint("epc_bid", __name__)


@bid_bp.route("/api/bid-document/templates", methods=["GET"])
@token_required
def list_bid_templates():
    return success_response(data=[{"code": k, "name": v["name"]} for k, v in BID_DOCUMENT_TEMPLATES.items()])


@bid_bp.route("/api/bid-document/generate", methods=["POST"])
@token_required
def generate_bid_document():
    """生成投标文档"""
    data = request.get_json()
    project_id = data.get("project_id")
    user = request.current_user
    if project_id and not check_project_access(project_id, user):
        return error_response("无权访问该项目", 403)

    result, err = generate_bid_document_service(data)
    if err:
        return error_response(err, 400)

    bd = BidDocument(
        id=str(uuid.uuid4()),
        project_id=data.get("project_id"),
        document_type=result["template_code"],
        title=result["template_name"],
        version="1.0",
        status="draft",
    )
    bd.content = json.dumps(result["chapters"])
    bd.data_sources = json.dumps(result["sources"])
    db.session.add(bd)
    db.session.commit()

    return success_response(
        data={
            "chapters": result["chapters"],
            "sources": result["sources"],
        },
        message={"id": bd.id},
    )


@bid_bp.route("/api/bid-document/<bd_id>", methods=["GET"])
@token_required
def get_bid_document(bd_id):
    user = request.current_user
    obj = get_or_404(BidDocument, bd_id)
    if not obj:
        return error_response("未找到", 404)
    if getattr(user, "role", None) != "admin" and getattr(obj, "tenant_id", None) != user.tenant_id:
        return error_response("无权访问该项目", 403)
    return success_response(data=obj.to_dict())


@bid_bp.route("/api/bid-document", methods=["GET"])
@token_required
def list_bid_documents():
    user = request.current_user
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))
    project_id = request.args.get("project_id")
    query = BidDocument.query
    if project_id:
        query = query.filter_by(project_id=project_id)
    if getattr(user, "role", None) != "admin":
        query = query.filter_by(tenant_id=user.tenant_id)
    pagination = query.order_by(BidDocument.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return success_response(
        data={
            "items": [item.to_dict() for item in pagination.items],
            "total": pagination.total,
            "page": page,
            "per_page": per_page,
            "pages": pagination.pages,
        }
    )
