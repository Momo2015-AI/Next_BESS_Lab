"""财务计算核心函数

从 services/financial.py 迁移，避免模块/包同名冲突。
包含：5种收入模型、融资建模、税务/折旧、IRR/NPV/LCOS/DSCR/Payback 全量计算。
"""

NUM_YEARS = 26

BOQ_TO_CAPEX_MAP = {
    "100": "equipment",
    "200": "equipment",
    "300": "epc",
    "400": "epc",
    "500": "epc",
    "600": "equipment",
    "700": "development",
}


def _aggregate_boq_to_capex(boq_items):
    """将 BOQ 条目按 7 分类汇总为 equipment / epc / development
    三大 CAPEX 类别
    """
    result = {
        "equipment": 0,
        "epc": 0,
        "development": 0,
        "unmapped": [],
    }
    if not boq_items:
        return result
    for item in boq_items:
        section_code = str(item.get("section_code", ""))
        capex_cat = BOQ_TO_CAPEX_MAP.get(section_code)
        if capex_cat:
            total = float(item.get("total_price", 0) or 0)
            result[capex_cat] += total
        else:
            result["unmapped"].append(
                {
                    "section_code": section_code,
                    "name": item.get("name", ""),
                    "total_price": float(item.get("total_price", 0) or 0),
                }
            )
    return result


def _compute_irr(cash_flows, guess=0.1):
    """Newton-Raphson IRR 求解，含收敛验证与溢出保护"""
    rate = guess
    converged = False
    for i in range(100):
        npv = 0.0
        dnpv = 0.0
        for t, cf in enumerate(cash_flows):
            denom = (1 + rate) ** t
            # 防止分母爆炸（rate 趋近 -1 时）
            if denom == 0 or abs(denom) > 1e15:
                return None
            npv += cf / denom
            if t > 0:
                denom2 = (1 + rate) ** (t + 1)
                if denom2 == 0 or abs(denom2) > 1e15:
                    return None
                dnpv += -t * cf / denom2
        if abs(dnpv) < 1e-12:
            break
        # 防止 Newton 步长发散
        delta = npv / dnpv
        if abs(delta) > 10:
            # 步长过大，缩小步长防止跳入负值区域
            delta = 10 * (1 if delta > 0 else -1)
        new_rate = rate - delta
        # 防止 rate 进入 ≤ -1 的危险区域
        if new_rate <= -0.99:
            return None
        rate = new_rate
        if abs(npv) < 1e-6:
            converged = True
            break
    if not converged:
        return None
    return rate


def _calculate_revenue_arbitrage(params, year, total_ac_usable_for_year):
    """峰谷套利收入"""
    arb = params.get("arbitrage", {})
    if not arb.get("enabled", True):
        return 0
    off_peak = float(arb.get("offPeakPrice", 30))
    peak = float(arb.get("peakPrice", 60))
    spread_capture = float(arb.get("spreadCapture", 85)) / 100
    operating_days = int(arb.get("operatingDays", 330))
    escalation = float(params.get("_escalation", 2.0)) / 100
    efficiency_loss = float(params.get("_efficiencyLossPct", 3)) / 100

    spread = (peak - off_peak) * spread_capture
    year_energy = total_ac_usable_for_year * operating_days
    year_energy_eff = year_energy * (1 - efficiency_loss)
    revenue = year_energy_eff * spread
    revenue *= (1 + escalation) ** year
    return max(0, revenue)


def _calculate_revenue_capacity(params, year, system_power_mw):
    """容量市场收入"""
    cap = params.get("capacity", {})
    if not cap.get("enabled", True):
        return 0
    capacity_price = float(cap.get("capacityPrice", 45000))
    escalation = float(params.get("_escalation", 2.0)) / 100
    revenue = system_power_mw * capacity_price
    revenue *= (1 + escalation) ** year
    return max(0, revenue)


def _calculate_revenue_ancillary(params, year, system_power_mw):
    """辅助服务收入"""
    anc = params.get("ancillary", {})
    if not anc.get("enabled", True):
        return 0
    ancillary_price = float(anc.get("ancillaryPrice", 15000))
    escalation = float(params.get("_escalation", 2.0)) / 100
    revenue = system_power_mw * ancillary_price
    revenue *= (1 + escalation) ** year
    return max(0, revenue)


def _calculate_revenue_ppa(params, year, total_ac_usable_for_year):
    """PPA 购电协议收入"""
    ppa = params.get("ppa", {})
    if not ppa.get("enabled", True):
        return 0
    ppa_price = float(ppa.get("ppaPrice", 55))
    ppa_escalation = float(ppa.get("escalation", 2.0)) / 100
    operating_days = int(params.get("arbitrage", {}).get("operatingDays", 330))
    efficiency_loss = float(params.get("_efficiencyLossPct", 3)) / 100

    year_energy = total_ac_usable_for_year * operating_days
    year_energy_eff = year_energy * (1 - efficiency_loss)
    revenue = year_energy_eff * ppa_price
    revenue *= (1 + ppa_escalation) ** year
    return max(0, revenue)


def _calculate_revenue_capacity_auction(params, year, system_mwh):
    """容量拍卖收入（仅合同期内）"""
    auction = params.get("capacityAuction", {})
    if not auction.get("enabled", True):
        return 0
    auction_price = float(auction.get("auctionPrice", 120000))
    contract_years = int(auction.get("contractYears", 5))
    escalation = float(params.get("_escalation", 2.0)) / 100
    if year < 1 or year > contract_years:
        return 0
    revenue = system_mwh * auction_price
    revenue *= (1 + escalation) ** year
    return max(0, revenue)


def _calculate_debt_schedule(total_capex, financing):
    """生成 26 年等额本息/等额本金还款计划"""
    debt_ratio = float(financing.get("debtRatio", 70)) / 100
    interest_rate = float(financing.get("interestRate", 6.5)) / 100
    loan_term = int(financing.get("loanTerm", 15))
    repayment_type = financing.get("repaymentType", "equal_installment")

    principal = total_capex * debt_ratio
    if principal <= 0 or loan_term <= 0:
        return [
            {
                "year": y,
                "beginningBalance": 0,
                "principalPayment": 0,
                "interestPayment": 0,
                "endingBalance": 0,
            }
            for y in range(NUM_YEARS)
        ]

    schedule = []
    balance = principal

    for y in range(NUM_YEARS):
        if y == 0:
            schedule.append(
                {
                    "year": 0,
                    "beginningBalance": 0,
                    "principalPayment": 0,
                    "interestPayment": 0,
                    "endingBalance": principal,
                }
            )
            continue
        if y > loan_term:
            schedule.append(
                {
                    "year": y,
                    "beginningBalance": 0,
                    "principalPayment": 0,
                    "interestPayment": 0,
                    "endingBalance": 0,
                }
            )
            continue

        interest = balance * interest_rate
        if repayment_type == "equal_installment":
            if loan_term > 0 and interest_rate > 0:
                annual_payment = (
                    principal
                    * interest_rate
                    * (1 + interest_rate) ** loan_term
                    / ((1 + interest_rate) ** loan_term - 1)
                )
            else:
                annual_payment = principal / loan_term
            principal_pmt = annual_payment - interest
        else:
            principal_pmt = principal / loan_term
            annual_payment = principal_pmt + interest

        principal_pmt = min(principal_pmt, balance)
        balance -= principal_pmt

        schedule.append(
            {
                "year": y,
                "beginningBalance": balance + principal_pmt,
                "principalPayment": principal_pmt,
                "interestPayment": interest,
                "endingBalance": max(0, balance),
            }
        )

    return schedule


def _calculate_depreciation(total_capex, years, residual_rate):
    """15 年直线折旧，残值率 5%"""
    depreciable = total_capex * (1 - residual_rate)
    annual_depr = depreciable / years if years > 0 else 0
    result = []
    for y in range(NUM_YEARS):
        if y == 0 or y > years:
            result.append(0)
        else:
            result.append(annual_depr)
    return result


def calculate_full_financial(total_ac_usable, financial_params=None, boq_data=None):
    """完整财务计算主入口

    Args:
        total_ac_usable: list[float] — 26 年可用能量 (MWh)
        financial_params: dict — 收入/成本/融资/税收参数
        boq_data: dict | None — BOQ 汇总数据
                   (可选,优先于手工 CAPEX)

    Returns:
        FullFinancialResponse:
            {metrics, cashflowTable, capexBreakdown}
    """
    if financial_params is None:
        financial_params = {}

    revenue_params = financial_params.get("revenue", {})
    opex_params = financial_params.get("opex", {})
    financing_params = financial_params.get("financing", {})
    tax_params = financial_params.get("tax", {})
    discount_rate = float(financial_params.get("discountRate", 8.0)) / 100
    depreciation_years = int(financial_params.get("depreciationYears", 15))
    residual_rate = float(financial_params.get("residualRate", 5)) / 100
    escalation = float(financial_params.get("priceEscalation", 2.0))

    revenue_params["_escalation"] = escalation
    revenue_params["_cyclesPerDay"] = financial_params.get("cyclesPerDay", 1)
    revenue_params["_efficiencyLossPct"] = financial_params.get("efficiencyLossPct", 3)

    system_params = financial_params.get("systemParams", {})
    system_power_mw = float(system_params.get("pcsPower", 50))
    system_mwh = float(system_params.get("ratedEnergy", 5)) * float(system_params.get("initContainerQty", 10))

    capExInternal = financial_params.get("_capexInternal")
    if capExInternal is None:
        capExInternal = {
            "equipment": 0,
            "epc": 0,
            "development": 0,
        }
    if boq_data:
        boq_capex = _aggregate_boq_to_capex(boq_data)
        if boq_capex["equipment"] > 0 or boq_capex["epc"] > 0 or boq_capex["development"] > 0:
            capExInternal = boq_capex

    capex_equipment = float(capExInternal.get("equipment", 0))
    capex_epc = float(capExInternal.get("epc", 0))
    capex_development = float(capExInternal.get("development", 0))
    total_capex = capex_equipment + capex_epc + capex_development

    fixed_opex_per_mw = float(opex_params.get("fixedOpexPerMW", 5000))
    variable_opex_per_mwh = float(opex_params.get("variableOpexPerMWh", 2.5))
    insurance_rate = float(opex_params.get("insuranceRate", 0.5)) / 100
    land_lease = float(opex_params.get("landLease", 150000))
    annual_opex_base = (system_power_mw * fixed_opex_per_mw) + (total_capex * insurance_rate) + land_lease

    debt_schedule = _calculate_debt_schedule(total_capex, financing_params)
    depreciation = _calculate_depreciation(total_capex, depreciation_years, residual_rate)

    corp_tax_rate = float(tax_params.get("corporateTaxRate", 20)) / 100
    tax_holiday_years = int(tax_params.get("taxHolidayYears", 5))

    cashflow_table = []
    project_cashflows = []
    equity_cashflows = []

    for y in range(NUM_YEARS):
        if y == 0:
            row = {
                "year": 0,
                "revenue": {
                    "arbitrage": 0,
                    "capacity": 0,
                    "ancillary": 0,
                    "ppa": 0,
                    "capacityAuction": 0,
                },
                "totalRevenue": 0,
                "opex": 0,
                "ebitda": 0,
                "depreciation": 0,
                "interest": 0,
                "taxableIncome": 0,
                "tax": 0,
                "netIncome": 0,
                "debtService": 0,
                "freeCashflow": -total_capex,
                "equityCashflow": -(total_capex - (total_capex * float(financing_params.get("debtRatio", 70)) / 100)),
                "cumulativeCashflow": -total_capex,
            }
            cashflow_table.append(row)
            project_cashflows.append(-total_capex)
            equity_outlay = total_capex - (total_capex * float(financing_params.get("debtRatio", 70)) / 100)
            equity_cashflows.append(-equity_outlay)
            continue

        total_ac = float(total_ac_usable[y]) if y < len(total_ac_usable) else float(total_ac_usable[-1])

        rev_arbitrage = _calculate_revenue_arbitrage(revenue_params, y, total_ac)
        rev_capacity = _calculate_revenue_capacity(revenue_params, y, system_power_mw)
        rev_ancillary = _calculate_revenue_ancillary(revenue_params, y, system_power_mw)
        rev_ppa = _calculate_revenue_ppa(revenue_params, y, total_ac)
        rev_auction = _calculate_revenue_capacity_auction(revenue_params, y, system_mwh)

        total_revenue = rev_arbitrage + rev_capacity + rev_ancillary + rev_ppa + rev_auction

        annual_variable_opex = total_ac * 365 * variable_opex_per_mwh
        annual_opex = annual_opex_base + annual_variable_opex

        ebitda = total_revenue - annual_opex

        depr = depreciation[y]
        debt = debt_schedule[y] if y < len(debt_schedule) else {"interestPayment": 0, "principalPayment": 0}
        interest = debt["interestPayment"]

        taxable_income = ebitda - depr - interest
        if taxable_income < 0:
            taxable_income = 0

        tax = 0
        if y > tax_holiday_years:
            tax = taxable_income * corp_tax_rate

        net_income = taxable_income - tax
        principal_pmt = debt["principalPayment"]
        debt_service = interest + principal_pmt

        free_cashflow = ebitda - tax - principal_pmt - interest
        equity_of = financial_params.get("financing", {}).get("equityOutlay", {})
        equity_cf = free_cashflow
        if y == 1 and equity_of and equity_of > 0:
            equity_cf = free_cashflow

        cashflow_table.append(
            {
                "year": y,
                "revenue": {
                    "arbitrage": round(rev_arbitrage, 2),
                    "capacity": round(rev_capacity, 2),
                    "ancillary": round(rev_ancillary, 2),
                    "ppa": round(rev_ppa, 2),
                    "capacityAuction": round(rev_auction, 2),
                },
                "totalRevenue": round(total_revenue, 2),
                "opex": round(annual_opex, 2),
                "ebitda": round(ebitda, 2),
                "depreciation": round(depr, 2),
                "interest": round(interest, 2),
                "taxableIncome": round(taxable_income, 2),
                "tax": round(tax, 2),
                "netIncome": round(net_income, 2),
                "debtService": round(debt_service, 2),
                "freeCashflow": round(free_cashflow, 2),
                "equityCashflow": round(equity_cf, 2),
            }
        )

        project_cashflows.append(free_cashflow)
        equity_cashflows.append(equity_cf)

    cumulative = [0] * NUM_YEARS
    cum = 0
    for i, cf in enumerate(project_cashflows):
        cum += cf
        cumulative[i] = round(cum, 2)
        cashflow_table[i]["cumulativeCashflow"] = cumulative[i]

    npv = 0
    for t, cf in enumerate(project_cashflows):
        npv += cf / ((1 + discount_rate) ** t)

    irr = _compute_irr(project_cashflows)
    project_irr = round(irr * 100, 2) if irr is not None else None

    equity_irr_val = 0
    try:
        eq_irr = _compute_irr(equity_cashflows)
        equity_irr_val = round(eq_irr * 100, 2) if eq_irr is not None else 0
    except Exception:
        equity_irr_val = 0

    total_discounted_energy = 0.0
    total_discounted_cost = total_capex
    for y in range(1, NUM_YEARS):
        total_discounted_energy += (float(total_ac_usable[y]) if y < len(total_ac_usable) else float(total_ac_usable[-1])) * 365 / ((1 + discount_rate) ** y)
        total_discounted_cost += annual_opex_base / ((1 + discount_rate) ** y)
    lcos = total_discounted_cost / total_discounted_energy if total_discounted_energy > 0 else 0

    total_investment = total_capex + annual_opex_base * (NUM_YEARS - 1)
    total_return = sum(cf for i, cf in enumerate(project_cashflows) if i > 0)
    roi = total_return / total_investment * 100 if total_investment > 0 else 0

    dscr_vals = []
    for y in range(1, NUM_YEARS):
        ds = debt_schedule[y] if y < len(debt_schedule) else {"interestPayment": 0, "principalPayment": 0}
        debt_svc = ds["interestPayment"] + ds["principalPayment"]
        if debt_svc > 0:
            ebitda_val = cashflow_table[y]["ebitda"]
            dscr_vals.append(ebitda_val / debt_svc)
    dscr_min = round(min(dscr_vals), 2) if dscr_vals else 0
    dscr_avg = round(sum(dscr_vals) / len(dscr_vals), 2) if dscr_vals else 0

    payback = -1
    cum2 = -total_capex
    for y in range(1, NUM_YEARS):
        cum2 += cashflow_table[y]["freeCashflow"]
        if cum2 >= 0:
            payback = y
            break

    return {
        "metrics": {
            "projectIrr": project_irr,
            "equityIrr": equity_irr_val,
            "npv": round(npv, 2),
            "lcos": round(lcos, 4),
            "dscr": {"min": dscr_min, "avg": dscr_avg},
            "payback": payback,
            "roi": round(roi, 2),
        },
        "cashflowTable": cashflow_table,
        "capexBreakdown": {
            "equipment": round(capex_equipment, 2),
            "epc": round(capex_epc, 2),
            "development": round(capex_development, 2),
        },
    }
