from flask import Blueprint, jsonify, request

from services.efficiency import FACTOR_DEFAULTS, calculate_efficiency_chain, calculate_efficiency_curves

efficiency_bp = Blueprint("efficiency", __name__)

_in_memory_factors = [dict(f) for f in FACTOR_DEFAULTS]


def _reset_factors():
    global _in_memory_factors
    _in_memory_factors = [dict(f) for f in FACTOR_DEFAULTS]


@efficiency_bp.route("/api/efficiency/factors", methods=["GET"])
def get_factors():
    return jsonify({"factors": _in_memory_factors})


@efficiency_bp.route("/api/efficiency/factors", methods=["PUT"])
def update_factors():
    data = request.get_json()
    if not data or "factors" not in data:
        return jsonify({"error": "Missing 'factors' in request body"}), 400

    new_factors = data["factors"]
    if len(new_factors) != len(FACTOR_DEFAULTS):
        return jsonify({"error": f"Expected {len(FACTOR_DEFAULTS)} factors, got {len(new_factors)}"}), 400

    for i, f in enumerate(new_factors):
        _in_memory_factors[i] = {
            "id": FACTOR_DEFAULTS[i]["id"],
            "name": FACTOR_DEFAULTS[i]["name"],
            "eta_c": float(f.get("eta_c", FACTOR_DEFAULTS[i]["eta_c"])),
            "eta_d": float(f.get("eta_d", FACTOR_DEFAULTS[i]["eta_d"])),
            "degrade": bool(f.get("degrade", FACTOR_DEFAULTS[i]["degrade"])),
            "degrade_rate": float(f.get("degrade_rate", FACTOR_DEFAULTS[i]["degrade_rate"])),
        }

    return jsonify({"factors": _in_memory_factors})


@efficiency_bp.route("/api/efficiency/factors/reset", methods=["POST"])
def reset_factors():
    _reset_factors()
    return jsonify({"factors": _in_memory_factors})


@efficiency_bp.route("/api/efficiency/preview", methods=["POST"])
def preview_efficiency():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    factors = data.get("factors", _in_memory_factors)
    soh_pct = float(data.get("soh", 100.0))

    chain = calculate_efficiency_chain(factors, soh_pct)
    return jsonify(chain)


@efficiency_bp.route("/api/efficiency/curves", methods=["POST"])
def get_curves():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    factors = data.get("factors", _in_memory_factors)
    soh_curve = data.get("soh")
    if not soh_curve:
        return jsonify({"error": "soh curve required"}), 400

    curves = calculate_efficiency_curves(factors, soh_curve, len(soh_curve))
    return jsonify(curves)
