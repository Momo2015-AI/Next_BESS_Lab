"""
财务引擎 — 核心入口

整合：CAPEX/OPEX估算 + 多收益流叠加 + 敏感性分析 + 指标计算
"""

from services.engine_base import BaseEngine


class FinancialEngine(BaseEngine):
    """财务引擎"""

    name = "financial"

    def validate_input(self, data: dict) -> list:
        errors = []
        sim_output = data.get("simulation_output", data)
        if not sim_output.get("totalAcUsable"):
            errors.append({"field": "totalAcUsable", "error": "required"})
        return errors

    def run(self, **kwargs):
        """执行财务计算"""
        simulation_output = kwargs.get("simulation_output", {})
        design_output = kwargs.get("design_output", {})
        survey_params = kwargs.get("survey_params", {})
        financial_params = kwargs.get("financial_params", {})

        # Step 1: CAPEX 自动估算（从设计方案）
        capex = self._estimate_capex(design_output, survey_params)

        # Step 2: OPEX 自动估算
        opex = self._estimate_opex(design_output, survey_params)

        # Step 3: 收入模型自动选择（根据项目地点）
        revenue = self._select_revenue_model(survey_params)

        # Step 4: 融资结构
        financing = self._default_financing()

        # Step 5: 税收参数
        tax = self._default_tax(survey_params)

        # 合并参数
        merged_params = {
            "revenue": revenue,
            "opex": opex,
            "financing": financing,
            "tax": tax,
            "discountRate": financial_params.get("discountRate", 8.0),
            "depreciationYears": financial_params.get("depreciationYears", 15),
            "residualRate": financial_params.get("residualRate", 5),
            "priceEscalation": financial_params.get("priceEscalation", 2.0),
            "efficiencyLossPct": financial_params.get("efficiencyLossPct", 3),
            "_capexInternal": capex,
            "systemParams": self._extract_system_params(design_output, survey_params),
        }

        # 执行完整财务计算
        total_ac = simulation_output.get("totalAcUsable", [0] * 26)
        result = self._calculate_full(total_ac, merged_params)

        # 敏感性分析
        sensitivity = self._run_sensitivity(total_ac, merged_params)

        return {
            "metrics": result.get("metrics", {}),
            "cashflowTable": result.get("cashflowTable", []),
            "capexBreakdown": result.get("capexBreakdown", {}),
            "opexBreakdown": opex,
            "revenueModel": revenue,
            "sensitivity": sensitivity,
        }

    def _estimate_capex(self, design_output: dict, survey_params: dict) -> dict:
        """CAPEX 自动估算"""
        estimated = design_output.get("estimatedCapex", {})
        if estimated.get("totalCapex", 0) > 0:
            return {
                "equipment": estimated.get("equipmentCost", 0),
                "epc": estimated.get("epcCost", 0),
                "development": estimated.get("developmentCost", 0),
            }
        # 默认估算
        total_energy = design_output.get("totalEnergyMwh", 100)
        return {
            "equipment": round(total_energy * 200000, 2),
            "epc": round(total_energy * 200000 * 0.08, 2),
            "development": round(total_energy * 200000 * 0.05, 2),
        }

    def _estimate_opex(self, design_output: dict, survey_params: dict) -> dict:
        """OPEX 自动估算"""
        total_power = design_output.get("totalPowerMW", 50)
        return {
            "maintenance": round(total_power * 5000, 2),
            "insurance": round(total_power * 2000, 2),
            "grid": round(total_power * 1000, 2),
            "landLease": 150000,
            "fixedOpexPerMw": 5000,
            "variableOpexPerMwh": 2.5,
            "insuranceRate": 0.5,
        }

    def _select_revenue_model(self, survey_params: dict) -> dict:
        """根据项目地点自动选择收入模型"""
        location = (survey_params.get("location") or "").lower()

        # 欧洲：套利 + 辅助服务 + 负电价
        if any(kw in location for kw in ["europe", "eu", "germany", "uk", "france", "spain"]):
            return {
                "arbitrage": {"enabled": True, "offPeakPrice": 30, "peakPrice": 60, "spreadCapture": 85, "operatingDays": 330},
                "capacity": {"enabled": True, "capacityPrice": 45000},
                "ancillary": {"enabled": True, "ancillaryPrice": 25000},  # 欧洲辅助服务价格更高
                "ppa": {"enabled": False, "ppaPrice": 55, "escalation": 2.0},
                "capacityAuction": {"enabled": False, "auctionPrice": 120000, "contractYears": 5},
            }
        # 中东：PPA + 容量拍卖
        elif any(kw in location for kw in ["middle east", "saudi", "uae", "dubai", "qatar", "kuwait"]):
            return {
                "arbitrage": {"enabled": False, "offPeakPrice": 30, "peakPrice": 60, "spreadCapture": 85, "operatingDays": 330},
                "capacity": {"enabled": False, "capacityPrice": 45000},
                "ancillary": {"enabled": False, "ancillaryPrice": 15000},
                "ppa": {"enabled": True, "ppaPrice": 45, "escalation": 2.0},
                "capacityAuction": {"enabled": True, "auctionPrice": 100000, "contractYears": 10},
            }
        # 中国：峰谷套利 + 容量市场
        elif any(kw in location for kw in ["china", "cn", "beijing", "shanghai"]):
            return {
                "arbitrage": {"enabled": True, "offPeakPrice": 20, "peakPrice": 50, "spreadCapture": 80, "operatingDays": 330},
                "capacity": {"enabled": True, "capacityPrice": 35000},
                "ancillary": {"enabled": False, "ancillaryPrice": 15000},
                "ppa": {"enabled": False, "ppaPrice": 55, "escalation": 2.0},
                "capacityAuction": {"enabled": False, "auctionPrice": 120000, "contractYears": 5},
            }
        # 默认：全部开启
        else:
            return {
                "arbitrage": {"enabled": True, "offPeakPrice": 30, "peakPrice": 60, "spreadCapture": 85, "operatingDays": 330},
                "capacity": {"enabled": True, "capacityPrice": 45000},
                "ancillary": {"enabled": True, "ancillaryPrice": 15000},
                "ppa": {"enabled": True, "ppaPrice": 55, "escalation": 2.0},
                "capacityAuction": {"enabled": True, "auctionPrice": 120000, "contractYears": 5},
            }

    def _default_financing(self) -> dict:
        return {
            "debtRatio": 70,
            "interestRate": 6.5,
            "loanTerm": 15,
            "repaymentType": "equal_installment",
        }

    def _default_tax(self, survey_params: dict) -> dict:
        location = (survey_params.get("location") or "").lower()
        if any(kw in location for kw in ["middle east", "saudi", "uae", "dubai"]):
            return {"corporateTaxRate": 20, "vatRate": 5, "taxHolidayYears": 5}
        elif any(kw in location for kw in ["europe", "eu", "germany"]):
            return {"corporateTaxRate": 25, "vatRate": 19, "taxHolidayYears": 0}
        else:
            return {"corporateTaxRate": 20, "vatRate": 15, "taxHolidayYears": 5}

    def _extract_system_params(self, design_output: dict, survey_params: dict) -> dict:
        return {
            "pcsPower": design_output.get("totalPowerMW", 50),
            "ratedEnergy": design_output.get("container", {}).get("ratedEnergyMwh", 5),
            "initContainerQty": design_output.get("containerQty", 10),
        }

    def _calculate_full(self, total_ac_usable: list, params: dict) -> dict:
        """委托给现有 financial.py 的完整计算"""
        from services.financial.calculator import calculate_full_financial

        return calculate_full_financial(total_ac_usable, params)

    def _run_sensitivity(self, total_ac_usable: list, base_params: dict) -> dict:
        """敏感性分析：CAPEX±15%, 电价±20%"""
        scenarios = {
            "capex_plus_15": {"capex_multiplier": 1.15, "price_multiplier": 1.0},
            "capex_minus_15": {"capex_multiplier": 0.85, "price_multiplier": 1.0},
            "price_plus_20": {"capex_multiplier": 1.0, "price_multiplier": 1.20},
            "price_minus_20": {"capex_multiplier": 1.0, "price_multiplier": 0.80},
        }

        results = {}
        for name, scenario in scenarios.items():
            try:
                adjusted = self._apply_scenario(base_params, scenario)
                result = self._calculate_full(total_ac_usable, adjusted)
                metrics = result.get("metrics", {})
                results[name] = {
                    "irr": metrics.get("projectIrr"),
                    "npv": metrics.get("npv"),
                    "lcos": metrics.get("lcos"),
                    "payback": metrics.get("payback"),
                }
            except Exception:
                results[name] = None

        return results

    def _apply_scenario(self, base_params: dict, scenario: dict) -> dict:
        """应用敏感性场景"""
        import copy
        params = copy.deepcopy(base_params)

        capex_mult = scenario.get("capex_multiplier", 1.0)
        capex = params.get("_capexInternal", {})
        if capex:
            for key in capex:
                capex[key] = round(capex[key] * capex_mult, 2)

        price_mult = scenario.get("price_multiplier", 1.0)
        revenue = params.get("revenue", {})
        for stream in ["arbitrage", "capacity", "ancillary", "ppa"]:
            if stream in revenue:
                for price_key in ["offPeakPrice", "peakPrice", "capacityPrice", "ancillaryPrice", "ppaPrice"]:
                    if price_key in revenue[stream]:
                        revenue[stream][price_key] = round(revenue[stream][price_key] * price_mult, 2)

        return params


def run_financial(simulation_output: dict, design_output: dict = None, survey_params: dict = None, **kwargs) -> dict:
    """便捷入口"""
    engine = FinancialEngine()
    return engine.run(
        simulation_output=simulation_output,
        design_output=design_output or {},
        survey_params=survey_params or {},
        **kwargs,
    )
