# ===================== IPP财务 =====================


def _npv(cashflows, rate):
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(cashflows))


def _irr(cashflows):
    lo, hi = -0.99, 10.0
    for _ in range(100):
        mid = (lo + hi) / 2
        val = sum(cf / (1 + mid) ** t for t, cf in enumerate(cashflows))
        if val > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def calculate_ipp_service(data):
    """IPP财务模型计算"""
    years = int(data.get("project_life_years", 25))
    capex = float(data.get("total_capex_usd", 500_000_000))
    capacity_mw = float(data.get("capacity_mw", 100))
    energy_mwh = float(data.get("energy_mwh", 200))

    cap_price = float(data.get("capacity_price_usd_kw_month", 8.0))
    energy_price = float(data.get("energy_price_usd_kwh", 0.05))
    escalation = float(data.get("ppa_escalation_rate", 0.02))
    avail_guarantee = float(data.get("availability_guarantee", 0.98))
    avail_penalty = float(data.get("availability_penalty_usd_kw", 5.0))
    rte_guarantee = float(data.get("rte_guarantee", 90.0))
    rte_initial = float(data.get("rte_initial", 92.0))
    rte_decay = float(data.get("rte_decay_rate", 0.3))
    perf_penalty_rate = float(data.get("performance_penalty_rate", 0.1))
    debt_ratio = float(data.get("debt_ratio", 0.7))
    debt_rate = float(data.get("debt_interest_rate", 0.05))
    debt_tenor = int(data.get("debt_tenor_years", 15))
    discount_rate = float(data.get("discount_rate", 0.08))
    annual_opex = float(data.get("annual_opex_usd", 5_000_000))
    insurance_rate = float(data.get("insurance_rate", 0.005))
    land_lease = float(data.get("land_lease_usd_year", 500_000))

    debt_amount = capex * debt_ratio
    equity_amount = capex - debt_amount

    if debt_rate > 0 and debt_tenor > 0:
        annual_debt_service = debt_amount * (debt_rate * (1 + debt_rate) ** debt_tenor) / ((1 + debt_rate) ** debt_tenor - 1)
    else:
        annual_debt_service = debt_amount / debt_tenor if debt_tenor > 0 else 0

    cycles_per_year = 300
    annual_energy_kwh = energy_mwh * 1000 * cycles_per_year

    project_cf = [-capex]
    equity_cf = [-equity_amount]
    dscrs = []

    for y in range(years):
        esc = (1 + escalation) ** y
        cap_revenue = capacity_mw * 1000 * cap_price * 12 * esc
        soh_factor = max(0.6, 1 - 0.012 * y)
        available_energy = annual_energy_kwh * soh_factor * avail_guarantee
        energy_revenue = available_energy * energy_price * esc
        actual_avail = avail_guarantee - 0.002 * y
        if actual_avail < avail_guarantee:
            shortfall = (avail_guarantee - actual_avail) * capacity_mw * 1000
            penalty = shortfall * avail_penalty
        else:
            penalty = 0
        actual_rte = rte_initial - rte_decay * y
        perf_penalty = energy_revenue * perf_penalty_rate if actual_rte < rte_guarantee else 0
        total_revenue = cap_revenue + energy_revenue - penalty - perf_penalty
        opex_total = (annual_opex + capex * insurance_rate + land_lease) * (1.02**y)
        depreciation = capex / years
        ebitda = total_revenue - opex_total
        ebit = ebitda - depreciation
        tax = max(0, ebit * 0.2)
        debt_service = annual_debt_service if y < debt_tenor else 0
        net_cf = ebitda - tax - debt_service
        project_cf.append(net_cf)
        equity_cf.append(net_cf)
        if y < debt_tenor and annual_debt_service > 0:
            cfads = total_revenue - opex_total
            dscrs.append(cfads / annual_debt_service)

    npv_val = _npv(project_cf, discount_rate)
    irr_val = _irr(project_cf)
    equity_irr_val = _irr(equity_cf)
    dscr_avg = sum(dscrs) / len(dscrs) if dscrs else 0
    dscr_min = min(dscrs) if dscrs else 0

    total_energy = annual_energy_kwh * years
    lcoe = capex / total_energy if total_energy > 0 else 0

    cumulative = 0
    payback = years
    for t, cf in enumerate(project_cf):
        cumulative += cf
        if cumulative >= 0 and t > 0:
            payback = t - 1 + (project_cf[t - 1] * -1 + cumulative - cf) / cf if cf != 0 else t
            break

    cashflow_detail = []
    for y in range(years):
        cashflow_detail.append({
            "year": y,
            "revenue": round(project_cf[y + 1], 0) if y + 1 < len(project_cf) else 0,
            "cumulative": round(sum(project_cf[: y + 2]), 0),
        })

    return {
        "npv_usd": round(npv_val, 0),
        "irr": round(irr_val * 100, 2),
        "equity_irr": round(equity_irr_val * 100, 2),
        "dscr_avg": round(dscr_avg, 2),
        "dscr_min": round(dscr_min, 2),
        "lcoe_usd_kwh": round(lcoe, 4),
        "payback_years": round(payback, 1),
        "cashflow_data": cashflow_detail,
    }


