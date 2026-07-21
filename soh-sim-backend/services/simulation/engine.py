"""
仿真引擎 — 核心入口

整合：容量仿真 + 寿命预测 + 补容策略 + 能量核算
"""

import logging

from services.degradation import NUM_YEARS, predict_soh
from services.efficiency import FACTOR_DEFAULTS, calculate_efficiency_chain, calculate_efficiency_curves
from services.engine_base import BaseEngine

logger = logging.getLogger(__name__)


class SimulationEngine(BaseEngine):
    """仿真引擎"""

    name = "simulation"

    def validate_input(self, data: dict) -> list:
        errors = []
        required = ["ratedEnergy", "initContainerQty", "duration", "temperature"]
        # 兼容两种输入格式：直接的 system_params 或嵌套的 design_output + survey_params
        if "design_output" in data:
            params = self._extract_params(data.get("design_output", {}), data.get("survey_params", {}))
        elif "container" in data:
            # design_output 格式
            params = self._extract_params(data, {})
        else:
            params = data.get("system_params", data)
        for field in required:
            if params.get(field) is None:
                errors.append({"field": field, "error": f"{field} is required"})
        return errors

    def run(self, **kwargs):
        """执行仿真"""
        design_output = kwargs.get("design_output", {})
        survey_params = kwargs.get("survey_params", {})
        degradation = kwargs.get("degradation", {})
        algorithm = kwargs.get("algorithm", {})

        # 从设计方案提取参数
        system_params = self._extract_params(design_output, survey_params)

        # 执行退化预测
        soh, rte, dod, aug_qty = self._predict_degradation(system_params, degradation, algorithm)

        # 能量核算 — 允许 efficiencyFactors=None 以使用自定义RTE数组
        efficiency_factors = system_params.get("efficiencyFactors")
        if efficiency_factors is None and "efficiencyFactors" not in system_params:
            efficiency_factors = FACTOR_DEFAULTS
        energy_results = self._calculate_energy(system_params, soh, rte, dod, aug_qty, efficiency_factors)

        # 效率曲线 — 当 efficiency_factors 为 None 时跳过（使用自定义RTE）
        if efficiency_factors is not None:
            eff_curves = calculate_efficiency_curves(efficiency_factors, soh, NUM_YEARS)
            rte = eff_curves["rte"]
            efficiency_detail = calculate_efficiency_chain(efficiency_factors, soh[0])
        else:
            eff_curves = None
            efficiency_detail = None

        # 补容策略
        aug_strategy = self._optimize_augmentation(soh, energy_results, system_params)

        # 补容策略经济性对比
        aug_comparison = self._compare_augmentation_strategies(
            system_params,
            soh,
            rte,
            dod,
            energy_results,
            design_output,
            survey_params,
        )

        return {
            "years": list(range(NUM_YEARS)),
            "soh": soh,
            "rte": rte,
            "dod": dod,
            "augQty": aug_qty,
            "efficiencyCurves": eff_curves,
            "efficiencyDetail": efficiency_detail,
            **energy_results,
            "augmentationStrategy": aug_strategy,
            "augmentationComparison": aug_comparison,
        }

    def _extract_params(self, design_output: dict, survey_params: dict) -> dict:
        """从设计方案提取 systemParams"""
        container = design_output.get("container", {})
        pcs = design_output.get("pcs", {})
        aux = design_output.get("auxPower", {})
        eff = design_output.get("efficiencyChain", {})
        deg = design_output.get("degradationModel", {})

        return {
            "ratedEnergy": container.get("ratedEnergyMWh", survey_params.get("ratedEnergy", 5)),
            "initContainerQty": design_output.get("containerQty", 10),
            "initPcsQty": design_output.get("pcsQty", 10),
            "pcsPower": pcs.get("ratedPowerMW", 2.5),
            "duration": design_output.get("duration", survey_params.get("duration", 2)),
            "cyclesPerDay": survey_params.get("cyclesPerDay", 1),
            "temperature": survey_params.get("temperature", 25),
            "dod": survey_params.get("dod", 90),
            "cRate": survey_params.get("cRate", 0.5),
            "acEfficiency": eff.get("systemRTE", 97.03),
            "bessAuxRun": aux.get("bessAuxRun", 18.124),
            "bessAuxStandby": aux.get("bessAuxStandby", 3.5),
            "pcsAuxRun": aux.get("pcsAuxRun", 6.5),
            "pcsAuxStandby": aux.get("pcsAuxStandby", 1.0),
            "auxPowerMode": survey_params.get("auxPowerMode", design_output.get("auxPowerMode", "manual")),
            "ambientTemp": survey_params.get(
                "ambientTemp", survey_params.get("tempAvg", design_output.get("ambientTemp", 25))
            ),
            "coolingType": survey_params.get("coolingType", design_output.get("coolingType", "liquid")),
            "requiredEnergy": survey_params.get("requiredEnergy", 240),
            "efficiencyFactors": survey_params.get("efficiencyFactors", FACTOR_DEFAULTS),
        }

    def _predict_degradation(self, system_params, degradation, algorithm):
        """退化预测"""
        model_type = algorithm.get("model", "arrhenius")
        correction_factor = algorithm.get("correctionFactor", 1.0)
        correction_table = algorithm.get("correctionTable")
        model_params = algorithm.get("modelParams")
        environmental = algorithm.get("environmental")
        gb_curves = algorithm.get("gb36276Curves")

        temperature = system_params.get("temperature", 25)
        cycles_per_day = system_params.get("cyclesPerDay", 1)
        dod_input = system_params.get("dod", 80)
        c_rate = system_params.get("cRate", 0.5)

        if degradation.get("soh") and len(degradation["soh"]) == NUM_YEARS:
            soh = list(degradation["soh"])
        else:
            soh, rte_out = predict_soh(
                model_type,
                temperature,
                cycles_per_day,
                dod_input,
                c_rate,
                model_params,
                correction_factor,
                correction_table,
                environmental,
                gb_curves,
            )

        if degradation.get("rte") and len(degradation["rte"]) == NUM_YEARS:
            rte = list(degradation["rte"])
        else:
            rte = [max(80, 97.03 - (100 - s) * 0.15) for s in soh]

        dod = (
            list(degradation["dod"])
            if degradation.get("dod") and len(degradation["dod"]) == NUM_YEARS
            else [dod_input] * NUM_YEARS
        )

        aug_qty = (
            list(degradation["augQty"])
            if degradation.get("augQty") and len(degradation["augQty"]) == NUM_YEARS
            else [0] * NUM_YEARS
        )

        return soh, rte, dod, aug_qty

    def _calculate_energy(self, params, soh, rte, dod, aug_qty, efficiency_factors):
        """能量核算"""
        from services.pipeline import calculate_energy_accounting

        return calculate_energy_accounting(params, soh, rte, dod, aug_qty, efficiency_factors)

    def _optimize_augmentation(self, soh, energy_results, system_params):
        """补容策略优化 — 生成三种策略的 augQty 数组"""
        required_energy = system_params.get("requiredEnergy", 240)
        total_ac = energy_results.get("totalAcUsable", [])
        meets_req = energy_results.get("meetsReq", [])

        # 策略A: 固定周期补容（每5年）
        fixed_aug = [0] * NUM_YEARS
        rated_energy = max(system_params.get("ratedEnergy", 5), 0.01)
        for i in range(5, NUM_YEARS, 5):
            if i < len(meets_req) and not meets_req[i]:
                shortfall = required_energy - total_ac[i]
                aug_units = max(0, int(shortfall / (rated_energy * 0.5)))
                fixed_aug[i] = aug_units

        # 策略B: 按需补容
        ondemand_aug = [0] * NUM_YEARS
        for i in range(NUM_YEARS):
            if i < len(meets_req) and not meets_req[i]:
                shortfall = required_energy - total_ac[i]
                aug_units = max(0, int(shortfall / (rated_energy * 0.5)))
                ondemand_aug[i] = aug_units

        # 策略C: 初始超配 20%（初始多装，前几年无需补容）
        overbuild_aug = [0] * NUM_YEARS
        # 超配逻辑体现在初始 containerQty × 1.2，不在 augQty 数组中
        # 但需要在能量核算时使用调整后的 initContainerQty

        return {
            "strategies": {
                "fixed_periodic": {"augQty": fixed_aug, "description": "每5年固定补容"},
                "on_demand": {"augQty": ondemand_aug, "description": "容量不足时补容"},
                "overbuild": {"augQty": overbuild_aug, "description": "初始超配20%，前期无需补容"},
            },
            "recommended": "on_demand",
        }

    def _compare_augmentation_strategies(
        self, system_params, soh, rte, dod, energy_results, design_output, survey_params
    ):
        """对三种补容策略执行完整经济性对比

        对每种策略：
          1. 用该策略的 augQty 重新执行能量核算
          2. 计算补容 CAPEX（增量成本）
          3. 调用 FinancialEngine 计算 NPV/IRR/LCOS
        返回对比结果并推荐 NPV 最高的策略。
        """
        from services.financial.engine import FinancialEngine
        from services.pipeline import calculate_energy_accounting

        aug_result = self._optimize_augmentation(soh, energy_results, system_params)
        strategies = aug_result.get("strategies", {})

        rated_energy = system_params.get("ratedEnergy", 5)
        efficiency_factors = system_params.get("efficiencyFactors")

        # 补容成本参数
        learning_rate = 0.05  # 设备成本年降幅 5%（Wright 定律）
        aug_install_cost_per_unit = 10000  # 补容安装费 $10k/台
        # 初始 container 单价（从设计方案获取，或默认估算）
        init_container_unit_price = design_output.get("estimatedCapex", {}).get(
            "containerCost", rated_energy * 200000
        ) / max(design_output.get("containerQty", 1), 1)

        financial_engine = FinancialEngine()
        comparison = {}

        for strat_name, strat_data in strategies.items():
            aug_qty = strat_data.get("augQty", [0] * NUM_YEARS)

            # 超配策略：初始 containerQty × 1.2，初始 CAPEX 也需增加
            # 额外成本直接融入 equipment，不在输出中暴露独立字段，避免双重计数风险
            if strat_name == "overbuild":
                params = {**system_params}
                extra_containers = int(system_params.get("initContainerQty", 10) * 0.2)
                params["initContainerQty"] = int(system_params.get("initContainerQty", 10)) + extra_containers
                overbuild_extra_cost = extra_containers * init_container_unit_price
            else:
                params = system_params
                overbuild_extra_cost = 0

            # 重新执行能量核算
            energy = calculate_energy_accounting(params, soh, rte, dod, aug_qty, efficiency_factors)
            total_ac = energy.get("totalAcUsable", [0] * NUM_YEARS)

            # 计算补容 CAPEX（仅限实际补容事件，不含 overbuild 溢价）
            total_aug_capex = 0.0
            aug_schedule = []
            for y in range(NUM_YEARS):
                qty = int(aug_qty[y]) if y < len(aug_qty) else 0
                if qty > 0:
                    # 补容年份的 container 单价 = 初始单价 × (1 - 学习率)^年份
                    discounted_price = init_container_unit_price * ((1 - learning_rate) ** y)
                    year_aug_cost = qty * discounted_price + qty * aug_install_cost_per_unit
                    total_aug_capex += year_aug_cost
                    aug_schedule.append(
                        {
                            "year": y,
                            "quantity": qty,
                            "unitPrice": round(discounted_price, 2),
                            "totalCost": round(year_aug_cost, 2),
                        }
                    )

            # 构造财务参数
            # overbuild 策略：equipment CAPEX 已包含额外 20% 容器的成本，
            # 反映更高的初始投资（不单独暴露 overbuildExtraCost 字段以避免双重计数）
            capex_internal = design_output.get("estimatedCapex", {})
            adjusted_capex = {
                "equipment": float(capex_internal.get("equipmentCost", 0)) + overbuild_extra_cost,
                "epc": float(capex_internal.get("epcCost", 0)),
                "development": float(capex_internal.get("developmentCost", 0)),
            }

            # 执行财务计算
            try:
                fin_result = financial_engine.run(
                    simulation_output={"totalAcUsable": total_ac},
                    design_output=design_output,
                    survey_params=survey_params,
                    financial_params={"_capexInternal": adjusted_capex},
                )
                metrics = fin_result.get("metrics", {})
            except Exception as e:
                logger.warning("补容策略 %s 财务计算失败: %s", strat_name, e)
                metrics = {}

            comparison[strat_name] = {
                "augQty": aug_qty,
                "augSchedule": aug_schedule,
                "totalAugCapex": round(total_aug_capex, 2),
                "description": strat_data.get("description", ""),
                "metrics": {
                    "irr": metrics.get("projectIrr"),
                    "npv": metrics.get("npv"),
                    "lcos": metrics.get("lcos"),
                    "payback": metrics.get("payback"),
                    "roi": metrics.get("roi"),
                },
            }

        # 推荐 NPV 最高的策略
        best_strategy = max(
            comparison.keys(),
            key=lambda k: float(comparison[k].get("metrics", {}).get("npv") or -float("inf")),
            default="on_demand",
        )

        return {
            "strategies": comparison,
            "recommended": best_strategy,
            "comparison_summary": {
                "bestNpv": comparison.get(best_strategy, {}).get("metrics", {}).get("npv"),
                "bestIrr": comparison.get(best_strategy, {}).get("metrics", {}).get("irr"),
                "bestLcos": comparison.get(best_strategy, {}).get("metrics", {}).get("lcos"),
                "strategy": best_strategy,
            },
        }


def run_simulation(design_output: dict, survey_params: dict = None, **kwargs) -> dict:
    """便捷入口"""
    engine = SimulationEngine()
    return engine.run(design_output=design_output, survey_params=survey_params or {}, **kwargs)
