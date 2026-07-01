import uuid
from flask import Blueprint, request, jsonify
from database import db, BoqSection, BoqItem

boq_bp = Blueprint("boq", __name__)


@boq_bp.route("/api/boq/sections", methods=["GET"])
def get_boq_sections():
    sections = BoqSection.query.order_by(BoqSection.sort_order).all()
    return jsonify({
        "success": True,
        "data": [s.to_dict() for s in sections],
    })


@boq_bp.route("/api/boq/items", methods=["GET"])
def get_boq_items():
    project_id = request.args.get("project_id")
    is_alternative = request.args.get("is_alternative", "false").lower() == "true"
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    query = BoqItem.query
    if project_id:
        query = query.filter_by(project_id=project_id)
    query = query.filter_by(is_alternative=is_alternative)
    pagination = query.order_by(BoqItem.section_code, BoqItem.seq).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        "success": True,
        "data": [i.to_dict() for i in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages,
    })


@boq_bp.route("/api/boq/items", methods=["POST"])
def save_boq_items():
    data = request.get_json()
    if not data:
        return jsonify({"error": "invalid request body"}), 400

    items_data = data.get("items", [])
    project_id = data.get("projectId")
    is_alternative = data.get("isAlternative", False)

    if not project_id:
        return jsonify({"error": "projectId is required"}), 400

    try:
        # Delete existing items for this project + alternative flag
        BoqItem.query.filter_by(project_id=project_id, is_alternative=is_alternative).delete()

        saved = []
        for item in items_data:
            boq_item = BoqItem(
                id=item.get("id") or str(uuid.uuid4()),
                project_id=project_id,
                section_code=item.get("sectionCode", ""),
                seq=item.get("seq", 0),
                name=item.get("name", ""),
                spec=item.get("spec", ""),
                unit=item.get("unit", ""),
                quantity=float(item.get("quantity", 0) or 0),
                unit_price=float(item.get("unitPrice", 0) or 0),
                total_price=float(item.get("totalPrice", 0) or item.get("quantity", 0) * item.get("unitPrice", 0) or 0),
                note=item.get("note", ""),
                is_alternative=is_alternative,
                version=item.get("version", 1),
            )
            db.session.add(boq_item)
            saved.append(boq_item)

        db.session.commit()

        return jsonify({
            "success": True,
            "data": [i.to_dict() for i in saved],
            "count": len(saved),
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"保存失败: {str(e)}"}), 500


@boq_bp.route("/api/boq/version", methods=["POST"])
def create_boq_version():
    data = request.get_json()
    if not data:
        return jsonify({"error": "invalid request body"}), 400

    project_id = data.get("projectId")
    if not project_id:
        return jsonify({"error": "projectId is required"}), 400

    items = BoqItem.query.filter_by(project_id=project_id, is_alternative=False).all()
    for item in items:
        item.version += 1

    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"Version bumped to {items[0].version if items else 1}",
    })
