"""${1:Route Description}"""

from flask import Blueprint, request, jsonify

${2:name}_bp = Blueprint("${2:name}", __name__)


@${2:name}_bp.route("/api/${2:name}", methods=["GET"])
def get_${2:name}_list():
    """Get paginated list of ${2:name}."""
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 20, type=int)
    page_size = min(page_size, 100)

    # TODO: Implement query with pagination
    # items = Model.query.paginate(page=page, per_page=page_size)

    return jsonify({
        "success": True,
        "data": [],
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": 0,
            "total_pages": 0,
        },
    })


@${2:name}_bp.route("/api/${2:name}/<int:item_id>", methods=["GET"])
def get_${2:name}_item(item_id):
    """Get single ${2:name} by ID."""
    # TODO: Implement query
    return jsonify({"success": True, "data": {}})
