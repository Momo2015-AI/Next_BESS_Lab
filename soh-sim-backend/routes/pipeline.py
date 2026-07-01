import threading
import uuid

from flask import Blueprint, jsonify, request

from services.pipeline import calculate_full_pipeline, validate_pipeline_input

pipeline_bp = Blueprint("pipeline", __name__)

# In-memory task store for async calculation
_pending_tasks = {}
_lock = threading.Lock()


@pipeline_bp.route("/api/pipeline/calculate", methods=["POST"])
def pipeline_calculate():
    data = request.get_json()
    if not data:
        return jsonify({"error": "invalid request body"}), 400

    errors = validate_pipeline_input(data)
    if errors:
        return jsonify({"error": "validation failed", "fields": errors}), 400

    system_params = data.get("systemParams", {})
    degradation = data.get("degradation")
    algorithm = data.get("algorithm")
    financial_params = data.get("financial")

    try:
        result = calculate_full_pipeline(system_params, degradation, algorithm, financial_params)
        return jsonify({"status": "completed", "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@pipeline_bp.route("/api/pipeline/task/<task_id>", methods=["GET"])
def pipeline_task_status(task_id):
    with _lock:
        task = _pending_tasks.get(task_id)
    if task is None:
        return jsonify({"error": "task not found"}), 404
    return jsonify(task)
