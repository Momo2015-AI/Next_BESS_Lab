"""EPC - IPP财务 路由"""

import json
import uuid

from flask import Blueprint, request

from database import IPPFinancialModel, db
from routes.auth import token_required
from routes.epc._common import check_project_access, get_or_404
from services.epc.ipp import calculate_ipp_service
from utils.api_response import error_response, success_response

ipp_bp = Blueprint("epc_ipp", __name__)


@ipp_bp.route("/api/ipp-financial/calculate", methods=["POST"])
@token_required
def calculate_ipp():
    """IPP财务模型计算"""
    data = request.get_json()
    project_id = data.get("project_id")
    user = request.current_user
    if project_id and not check_project_access(project_id, user):
        return error_response("无权访问该项目", 403)

    result = calculate_ipp_service(data)

    years = int(data.get("project_life_years", 25))
    energy_mwh = float(data.get("energy_mwh", 200))
    capacity_mw = float(data.get("capacity_mw", 100))
    cap_price = float(data.get("capacity_price_usd_kw_month", 8.0))
    energy_price = float(data.get("energy_price_usd_kwh", 0.05))
    escalation = float(data.get("ppa_escalation_rate", 0.02))
    avail_guarantee = float(data.get("availability_guarantee", 0.98))
    avail_penalty = float(data.get("availability_penalty_usd_kw", 5.0))
    rte_guarantee = float(data.get("rte_guarantee", 90.0))
    perf_penalty_rate = float(data.get("performance_penalty_rate", 0.1))
    capex = float(data.get("total_capex_usd", 500_000_000))
    debt_ratio = float(data.get("debt_ratio", 0.7))
    debt_rate = float(data.get("debt_interest_rate", 0.05))
    debt_tenor = int(data.get("debt_tenor_years", 15))
    annual_opex = float(data.get("annual_opex_usd", 5_000_000))
    insurance_rate = float(data.get("insurance_rate", 0.005))
    land_lease = float(data.get("land_lease_usd_year", 500_000))

    ipp = IPPFinancialModel(
        id=str(uuid.uuid4()),
        project_id=data.get("project_id"),
        project_name=data.get("project_name", ""),
        project_life_years=years,
        capacity_mw=capacity_mw,
        energy_mwh=energy_mwh,
        duration_hours=(energy_mwh / capacity_mw if capacity_mw > 0 else 0),
        ppa_type=data.get("ppa_type", "hybrid"),
        capacity_price_usd_kw_month=cap_price,
        energy_price_usd_kwh=energy_price,
        ppa_escalation_rate=escalation,
        availability_guarantee=avail_guarantee,
        availability_penalty_usd_kw=avail_penalty,
        rte_guarantee=rte_guarantee,
        performance_penalty_rate=perf_penalty_rate,
        total_capex_usd=capex,
        debt_ratio=debt_ratio,
        debt_interest_rate=debt_rate,
        debt_tenor_years=debt_tenor,
        equity_irr_target=float(data.get("equity_irr_target", 0.12)),
        annual_opex_usd=annual_opex,
        insurance_rate=insurance_rate,
        land_lease_usd_year=land_lease,
        npv_usd=result["npv_usd"],
        irr=result["irr"] / 100,
        equity_irr=result["equity_irr"] / 100,
        dscr_avg=result["dscr_avg"],
        dscr_min=result["dscr_min"],
        lcoe_usd_kwh=result["lcoe_usd_kwh"],
        payback_years=result["payback_years"],
    )
    ipp.cashflow_data = json.dumps(result["cashflow_data"])
    db.session.add(ipp)
    db.session.commit()

    return success_response(data=result, message={"id": ipp.id})


@ipp_bp.route("/api/ipp-financial/<ipp_id>", methods=["GET"])
@token_required
def get_ipp(ipp_id):
    user = request.current_user
    obj = get_or_404(IPPFinancialModel, ipp_id)
    if not obj:
        return error_response("未找到", 404)
    if getattr(user, "role", None) != "admin" and getattr(obj, "tenant_id", None) != user.tenant_id:
        return error_response("无权访问该项目", 403)
    return success_response(data=obj.to_dict())
