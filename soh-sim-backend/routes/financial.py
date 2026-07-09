from flask import Blueprint, current_app, request

from routes.auth import token_required
from services.financial.calculator import _aggregate_boq_to_capex, calculate_full_financial
from utils.api_response import error_response, success_response

financial_bp = Blueprint("financial", __name__)


@financial_bp.route("/api/financial/calculate", methods=["POST"])
@token_required
def financial_calculate():
    data = request.get_json()
    if not data:
        return error_response("invalid request body", 400)

    total_ac_usable = data.get("totalAcUsable")
    if not total_ac_usable or len(total_ac_usable) == 0:
        return error_response("totalAcUsable is required", 400)

    financial_params = data.get("financialParams", {})
    boq_data = data.get("boqData")

    try:
        result = calculate_full_financial(total_ac_usable, financial_params, boq_data)
        return success_response(data=result)
    except Exception as e:
        current_app.logger.error(f"财务计算失败: {e}", exc_info=True)
        return error_response("计算失败，请重试", 500)


@financial_bp.route("/api/financial/capex-from-boq", methods=["POST"])
@token_required
def financial_capex_from_boq():
    data = request.get_json()
    if not data:
        return error_response("invalid request body", 400)

    boq_items = data.get("boqItems", [])
    result = _aggregate_boq_to_capex(boq_items)
    return success_response(data=result)
