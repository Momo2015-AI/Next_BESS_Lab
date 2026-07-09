"""
设计引擎 API 路由

一键生成设计方案：输入调研参数 → 约束求解 + 产品匹配 + 多方案生成
"""

from flask import Blueprint, request

from routes.auth import token_required
from services.design.engine import DesignEngine, auto_design
from utils.api_response import error_response, success_response

design_engine_bp = Blueprint("design_engine", __name__)


@design_engine_bp.route("/api/design/auto", methods=["POST"])
@token_required
def auto_design_solutions():
    """一键生成设计方案

    Request Body:
        {
            "survey_params": { "ratedEnergy": 100, "totalPower": 50, "duration": 2, ... },
            "strategy": "economic",          // economic|balanced|flexible|manufacturer
            "manufacturer": null             // 指定厂家（可选）
        }

    Returns:
        {
            strategy, solutions: [...], recommendation: {...}
        }
    """
    data = request.get_json()
    if not data:
        return error_response("无效的请求数据", 400)

    survey_params = data.get("survey_params", data)
    strategy = data.get("strategy", "economic")
    manufacturer = data.get("manufacturer")

    # 输入验证
    engine = DesignEngine()
    errors = engine.validate_input(survey_params)
    if errors:
        return error_response({"message": "参数验证失败", "errors": errors}, 400)

    try:
        result = engine.run(
            survey_params=survey_params,
            strategy=strategy,
            manufacturer=manufacturer,
        )
        return success_response(data=result, message=f"已生成 {len(result.get('solutions', []))} 个设计方案")
    except Exception as e:
        return error_response(f"设计方案生成失败: {str(e)}", 500)


@design_engine_bp.route("/api/design/strategies", methods=["GET"])
@token_required
def list_strategies():
    """获取可用策略列表"""
    return success_response(
        data={
            "strategies": [
                {"key": "economic", "label": "经济优先", "description": "最大容量集装箱 → 最少 BOP 成本"},
                {"key": "balanced", "label": "均衡方案", "description": "中等容量 → CAPEX/MWh 最优"},
                {"key": "flexible", "label": "灵活分期", "description": "小型集装箱 → 便于分期扩容"},
                {"key": "manufacturer", "label": "指定厂家", "description": "限定厂家产品匹配"},
            ]
        }
    )


@design_engine_bp.route("/api/design/validate", methods=["POST"])
@token_required
def validate_design_input():
    """验证设计输入参数"""
    data = request.get_json()
    if not data:
        return error_response("无效的请求数据", 400)

    survey_params = data.get("survey_params", data)
    engine = DesignEngine()
    errors = engine.validate_input(survey_params)

    if errors:
        return success_response(
            data={"valid": False, "errors": errors},
            message=f"发现 {len(errors)} 个参数问题",
        )
    return success_response(data={"valid": True, "errors": []}, message="参数验证通过")
