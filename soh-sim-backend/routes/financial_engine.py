"""
财务引擎 API 路由

执行 CAPEX/OPEX 估算 + 多收益流叠加 + 敏感性分析 + 财务指标计算
"""

from flask import Blueprint, request

from routes.auth import token_required
from services.financial.engine import FinancialEngine, run_financial
from utils.api_response import error_response, success_response

fin_engine_bp = Blueprint("fin_engine", __name__)


@fin_engine_bp.route("/api/financial/calculate", methods=["POST"])
@token_required
def calculate_financial():
    """执行完整财务计算

    Request Body:
        {
            "simulation_output": { totalAcUsable, soh, rte, ... },
            "design_output": { containerQty, pcsQty, estimatedCapex, ... },
            "survey_params": { location, ratedEnergy, ... },
            "financial_params": { discountRate, ... }  // 可选
        }

    Returns:
        {
            metrics: { projectIrr, npv, lcos, dscr, payback, roi },
            cashflowTable: [...],
            capexBreakdown: { equipment, epc, development },
            opexBreakdown: { maintenance, insurance, ... },
            revenueModel: { arbitrage, capacity, ... },
            sensitivity: { capex_plus_15: {...}, ... }
        }
    """
    data = request.get_json()
    if not data:
        return error_response("无效的请求数据", 400)

    simulation_output = data.get("simulation_output", {})
    design_output = data.get("design_output", {})

    if not simulation_output.get("totalAcUsable"):
        return error_response("缺少 simulation_output.totalAcUsable 参数", 400)

    engine = FinancialEngine()

    try:
        result = engine.run(
            simulation_output=simulation_output,
            design_output=design_output,
            survey_params=data.get("survey_params", {}),
            financial_params=data.get("financial_params", {}),
        )
        return success_response(data=result, message="财务计算完成")
    except Exception as e:
        return error_response(f"财务计算失败: {str(e)}", 500)


@fin_engine_bp.route("/api/financial/sensitivity", methods=["POST"])
@token_required
def run_sensitivity_analysis():
    """单独运行敏感性分析

    Request Body:
        {
            "total_ac_usable": [...],
            "financial_params": { revenue, opex, financing, tax, ... }
        }

    Returns:
        {
            capex_plus_15: { irr, npv, lcos, payback },
            capex_minus_15: {...},
            price_plus_20: {...},
            price_minus_20: {...}
        }
    """
    data = request.get_json()
    if not data:
        return error_response("无效的请求数据", 400)

    total_ac = data.get("total_ac_usable", [])
    if not total_ac:
        return error_response("缺少 total_ac_usable 参数", 400)

    engine = FinancialEngine()

    try:
        result = engine._run_sensitivity(total_ac, data.get("financial_params", {}))
        return success_response(data=result, message="敏感性分析完成")
    except Exception as e:
        return error_response(f"敏感性分析失败: {str(e)}", 500)


@fin_engine_bp.route("/api/financial/revenue-models", methods=["GET"])
@token_required
def list_revenue_models():
    """获取收入模型选项"""
    return success_response(
        data={
            "models": [
                {
                    "region": "china",
                    "label": "中国 (CN)",
                    "streams": ["arbitrage", "capacity"],
                    "description": "峰谷套利 + 容量市场",
                },
                {
                    "region": "europe",
                    "label": "欧洲 (EU)",
                    "streams": ["arbitrage", "ancillary"],
                    "description": "套利 + 辅助服务（含负电价套利）",
                },
                {
                    "region": "middle_east",
                    "label": "中东 (ME)",
                    "streams": ["ppa", "capacityAuction"],
                    "description": "PPA 购电协议 + 容量拍卖",
                },
                {
                    "region": "default",
                    "label": "全模型",
                    "streams": ["arbitrage", "capacity", "ancillary", "ppa", "capacityAuction"],
                    "description": "全部收入流叠加",
                },
            ]
        }
    )
