from flask import Blueprint, jsonify, request

from routes.auth import token_required
from services.degradation import (
    ENV_DEFAULTS,
    _compute_environmental_acceleration,
    get_default_environmental,
    get_default_gb_curves,
    predict_soh,
)

degradation_bp = Blueprint("degradation", __name__)

_in_memory_gb_curves = get_default_gb_curves()
_in_memory_env = get_default_environmental()


@degradation_bp.route("/api/degradation/gb36276-curves", methods=["GET"])
@token_required
def get_curves():
    return jsonify({"curves": _in_memory_gb_curves})


@degradation_bp.route("/api/degradation/gb36276-curves", methods=["PUT"])
@token_required
def update_curves():
    data = request.get_json()
    if not data or "curves" not in data:
        return jsonify({"error": "Missing 'curves' in request body"}), 400

    curves = data["curves"]
    for c in curves:
        for key in ("label", "p_rate", "temperature", "data"):
            if key not in c:
                return jsonify({"error": f"Each curve must have '{key}'"}), 400

    global _in_memory_gb_curves
    _in_memory_gb_curves = curves
    return jsonify({"curves": _in_memory_gb_curves})


@degradation_bp.route("/api/degradation/gb36276-curves/reset", methods=["POST"])
@token_required
def reset_curves():
    global _in_memory_gb_curves
    _in_memory_gb_curves = get_default_gb_curves()
    return jsonify({"curves": _in_memory_gb_curves})


@degradation_bp.route("/api/degradation/environmental", methods=["GET"])
@token_required
def get_environmental():
    return jsonify({"environmental": _in_memory_env})


@degradation_bp.route("/api/degradation/environmental", methods=["PUT"])
@token_required
def update_environmental():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    global _in_memory_env
    _in_memory_env = {
        "accelerate_temperature": bool(data.get("accelerate_temperature", ENV_DEFAULTS["accelerate_temperature"])),
        "accelerate_dust": bool(data.get("accelerate_dust", ENV_DEFAULTS["accelerate_dust"])),
        "accelerate_humidity": bool(data.get("accelerate_humidity", ENV_DEFAULTS["accelerate_humidity"])),
        "ref_temperature": float(data.get("ref_temperature", ENV_DEFAULTS["ref_temperature"])),
        "ref_humidity": float(data.get("ref_humidity", ENV_DEFAULTS["ref_humidity"])),
        "field_humidity": float(data.get("field_humidity", ENV_DEFAULTS["field_humidity"])),
        "dust_factor": float(data.get("dust_factor", ENV_DEFAULTS["dust_factor"])),
        "humidity_exponent": float(data.get("humidity_exponent", ENV_DEFAULTS["humidity_exponent"])),
        "activation_energy": float(data.get("activation_energy", ENV_DEFAULTS["activation_energy"])),
    }
    return jsonify({"environmental": _in_memory_env})


@degradation_bp.route("/api/degradation/environmental/reset", methods=["POST"])
@token_required
def reset_environmental():
    global _in_memory_env
    _in_memory_env = get_default_environmental()
    return jsonify({"environmental": _in_memory_env})


@degradation_bp.route("/api/degradation/environmental/preview", methods=["POST"])
@token_required
def preview_acceleration():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    temperature = float(data.get("temperature", 25))
    env = data.get("environmental", _in_memory_env)

    accel = _compute_environmental_acceleration(temperature, env)
    return jsonify(
        {
            "accelerationFactor": round(accel, 4),
            "temperature": temperature,
            "details": {
                "temperature_enabled": env.get("accelerate_temperature", True),
                "dust_enabled": env.get("accelerate_dust", False),
                "humidity_enabled": env.get("accelerate_humidity", False),
            },
        }
    )


@degradation_bp.route("/api/degradation/preview", methods=["POST"])
@token_required
def preview_degradation():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    model_type = data.get("model", "arrhenius")
    temperature = float(data.get("temperature", 25))
    cycles_per_day = float(data.get("cyclesPerDay", 1))
    dod = float(data.get("dod", 80))
    c_rate = float(data.get("cRate", 0.5))
    correction_factor = float(data.get("correctionFactor", 1.0))
    correction_table = data.get("correctionTable")
    model_params = data.get("modelParams")
    environmental = data.get("environmental", _in_memory_env)
    gb_curves = data.get("gb36276Curves", _in_memory_gb_curves)

    soh, rte = predict_soh(
        model_type,
        temperature,
        cycles_per_day,
        dod,
        c_rate,
        model_params,
        correction_factor,
        correction_table,
        environmental,
        gb_curves,
    )

    return jsonify(
        {
            "model": model_type,
            "soh": soh,
            "rte": rte,
            "parameters": {
                "temperature": temperature,
                "cyclesPerDay": cycles_per_day,
                "dod": dod,
                "cRate": c_rate,
            },
        }
    )
