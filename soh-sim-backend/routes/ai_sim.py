"""
AI仿真算法API - 支持参数校准和预测
"""

from flask import Blueprint, current_app, request

from routes.auth import token_required, limiter
from utils.api_response import error_response, success_response
from services.ai_sim import (
    list_manufacturers,
    run_simulation,
    calibrate_params,
    seed_manufacturers,
)

ai_sim_bp = Blueprint("ai_sim", __name__)


@ai_sim_bp.route("/api/ai-sim/manufacturers", methods=["GET"])
@token_required
def get_manufacturers_api():
    """前端 SimulationLab 使用的厂家列表端点。"""
    manufacturers = list_manufacturers()
    return success_response(data=manufacturers)


@ai_sim_bp.route("/api/ai_sim/builtin_manufacturers", methods=["GET"])
@token_required
def get_builtin_manufacturers_api():
    manufacturers = list_manufacturers()
    return success_response(data=manufacturers)


@ai_sim_bp.route("/api/ai_sim/simulation", methods=["POST"])
@token_required
def simulation_api():
    """AI 仿真端点 - 根据厂家模型预测 SOH/RTE 曲线。"""
    data = request.get_json()
    if not data:
        return error_response("无效的请求数据", status_code=400)

    try:
        result = run_simulation(data)
        return success_response(data=result)
    except Exception:
        current_app.logger.error("AI仿真计算失败", exc_info=True)
        return error_response("操作失败，请重试", status_code=500)


@ai_sim_bp.route("/api/ai_sim/calibrate", methods=["POST"])
@token_required
@limiter.limit("10/minute")
def calibrate_params_api():
    """参数校准端点 - 根据实测数据校准 Arrhenius 参数。"""
    data = request.get_json()
    if not data:
        return error_response("无效的请求数据", status_code=400)

    result = calibrate_params(data)
    return success_response(data=result)


@ai_sim_bp.route("/api/ai_sim/predict", methods=["POST"])
@token_required
@limiter.limit("10/minute")
def predict_api():
    """预测端点 - 使用校准后的参数预测 SOH/RTE。"""
    data = request.get_json()
    if not data:
        return error_response("无效的请求数据", status_code=400)

    try:
        result = run_simulation(data)
        return success_response(
            data={
                "soh_curve": result["soh_curve"],
                "rte_curve": result["rte_curve"],
                "manufacturer": result["manufacturer"],
                "model_type": result["model_type"],
            }
        )
    except Exception:
        current_app.logger.error("AI预测失败", exc_info=True)
        return error_response("操作失败，请重试", status_code=500)
