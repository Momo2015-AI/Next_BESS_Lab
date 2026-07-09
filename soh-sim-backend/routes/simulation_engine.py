"""
仿真引擎 API 路由

执行 SOH 退化预测 + 能量核算 + 补容策略
"""

from flask import Blueprint, request

from routes.auth import token_required
from services.simulation.engine import SimulationEngine, run_simulation
from utils.api_response import error_response, success_response

sim_engine_bp = Blueprint("sim_engine", __name__)


@sim_engine_bp.route("/api/simulation/run", methods=["POST"])
@token_required
def run_simulation_endpoint():
    """执行仿真计算

    Request Body:
        {
            "design_output": { container, pcs, containerQty, pcsQty, ... },
            "survey_params": { temperature, cyclesPerDay, dod, ... },
            "degradation": { soh, rte, dod, augQty },    // 可选
            "algorithm": { model, correctionFactor, ... } // 可选
        }

    Returns:
        {
            years, soh, rte, dod, augQty,
            efficiencyCurves, efficiencyDetail,
            totalAcUsable, meetsReq, ...
            augmentationStrategy
        }
    """
    data = request.get_json()
    if not data:
        return error_response("无效的请求数据", 400)

    design_output = data.get("design_output", {})
    survey_params = data.get("survey_params", {})

    if not design_output:
        return error_response("缺少 design_output 参数", 400)

    engine = SimulationEngine()

    # 输入验证
    errors = engine.validate_input(design_output)
    if errors:
        return error_response({"message": "参数验证失败", "errors": errors}, 400)

    try:
        result = engine.run(
            design_output=design_output,
            survey_params=survey_params,
            degradation=data.get("degradation", {}),
            algorithm=data.get("algorithm", {}),
        )
        return success_response(data=result, message="仿真计算完成")
    except Exception as e:
        return error_response(f"仿真计算失败: {str(e)}", 500)


@sim_engine_bp.route("/api/simulation/augmentation-strategies", methods=["GET"])
@token_required
def list_augmentation_strategies():
    """获取可用的补容策略列表"""
    return success_response(
        data={
            "strategies": [
                {
                    "key": "fixed_periodic",
                    "label": "固定周期补容",
                    "description": "每 5 年自动评估，容量不足时补容",
                },
                {
                    "key": "on_demand",
                    "label": "按需补容",
                    "description": "每年检测容量缺口，即时补容（推荐）",
                },
                {
                    "key": "overbuild",
                    "label": "初始超配",
                    "description": "建设时超配 20%，前 3 年无需补容",
                },
            ],
            "default": "on_demand",
        }
    )


@sim_engine_bp.route("/api/simulation/augmentation-compare", methods=["POST"])
@token_required
def compare_augmentation():
    """补容策略经济性对比

    Request Body:
        {
            "design_output": { container, pcs, containerQty, pcsQty, estimatedCapex, ... },
            "survey_params": { temperature, cyclesPerDay, dod, ... }
        }

    Returns:
        {
            strategies: {
                fixed_periodic: { augQty, augSchedule, totalAugCapex, metrics: {irr, npv, lcos, ...} },
                on_demand: { ... },
                overbuild: { ... }
            },
            recommended: "on_demand",
            comparison_summary: { bestNpv, bestIrr, bestLcos, strategy }
        }
    """
    data = request.get_json()
    if not data:
        return error_response("无效的请求数据", 400)

    design_output = data.get("design_output", {})
    survey_params = data.get("survey_params", {})

    if not design_output:
        return error_response("缺少 design_output 参数", 400)

    engine = SimulationEngine()

    try:
        # 先执行一次基础仿真（无补容），获取 soh/rte/dod/energy
        base_result = engine.run(
            design_output=design_output,
            survey_params=survey_params,
            degradation={},
            algorithm={},
        )

        # 从结果中提取补容对比
        comparison = base_result.get("augmentationComparison", {})

        return success_response(data=comparison, message="补容策略对比完成")
    except Exception as e:
        return error_response(f"补容策略对比失败: {str(e)}", 500)
