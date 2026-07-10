import threading

from flask import Blueprint

from routes.auth import token_required
from utils.api_response import error_response, success_response

pipeline_bp = Blueprint("pipeline", __name__)

# In-memory task store for async calculation
_pending_tasks = {}
_lock = threading.Lock()


@pipeline_bp.route("/api/pipeline/task/<task_id>", methods=["GET"])
@token_required
def pipeline_task_status(task_id):
    with _lock:
        task = _pending_tasks.get(task_id)
    if task is None:
        return error_response("task not found", 404)
    return success_response(data=task)
