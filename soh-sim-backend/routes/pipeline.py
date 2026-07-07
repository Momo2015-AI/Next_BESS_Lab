import threading
import uuid

from flask import Blueprint, request

from routes.auth import token_required
from services.pipeline import calculate_full_pipeline, validate_pipeline_input
from utils.api_response import error_response, success_response

pipeline_bp = Blueprint("pipeline", __name__)

# In-memory task store for async calculation
_pending_tasks = {}
_lock = threading.Lock()


@pipeline_bp.route("/api/pipeline/calculate", methods=["POST"])
@token_required
def pipeline_calculate():
    data = request.get_json()
    if not data:
        return error_response("invalid request body", 400)

    errors = validate_pipeline_input(data)
    if errors:
        return error_response("validation failed", 400)

    system_params = data.get("systemParams", {})
    degradation = data.get("degradation")
    algorithm = data.get("algorithm")
    financial_params = data.get("financial")

    try:
        result = calculate_full_pipeline(system_params, degradation, algorithm, financial_params)
        return success_response(data={"status": "completed", "result": result})
    except Exception as e:
        return error_response("计算失败，请重试", 500)


@pipeline_bp.route("/api/pipeline/task/<task_id>", methods=["GET"])
@token_required
def pipeline_task_status(task_id):
    with _lock:
        task = _pending_tasks.get(task_id)
    if task is None:
        return error_response("task not found", 404)
    return success_response(data=task)
