"""旧版财务 API — 仅保留 CAPEX 汇总端点

注：POST /api/financial/calculate 已迁移至 routes/financial_engine.py
"""

from flask import Blueprint, request

from routes.auth import token_required
from services.financial.calculator import _aggregate_boq_to_capex
from utils.api_response import error_response, success_response

financial_bp = Blueprint("financial", __name__)


@financial_bp.route("/api/financial/capex-from-boq", methods=["POST"])
@token_required
def financial_capex_from_boq():
    data = request.get_json()
    if not data:
        return error_response("invalid request body", 400)

    boq_items = data.get("boqItems", [])
    result = _aggregate_boq_to_capex(boq_items)
    return success_response(data=result)
