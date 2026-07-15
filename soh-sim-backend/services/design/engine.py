"""
方案设计引擎 — 核心入口

约束求解 + 产品匹配 + 拓扑生成 + 多方案生成
"""

import json
import math
import os
import uuid

from services.engine_base import BaseEngine

# 产品数据路径（DB 为空时的 JSON 回退）
_PRODUCTS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
    "products.json",
)

# 多方案生成策略
STRATEGIES = ["economic", "balanced", "flexible", "manufacturer"]

# DB snake_case → camelCase 字段映射（与前端 useProducts.js 对齐）
_FIELD_MAP = {
    "rated_energy_mwh": "ratedEnergyMWh",
    "rated_power_mw": "ratedPowerMW",
    "rated_power_mva": "ratedPowerMVA",
    "unit_price": "unitPrice",
    "cell_model": "cellModel",
    "clusters_per_container": "clustersPerContainer",
    "cycle_life": "cycleLife",
    "calendar_life": "calendarLife",
    "ac_voltage": "acVoltage",
    "dc_voltage_range": "dcVoltageRange",
    "max_dc_current": "maxDcCurrent",
    "aux_run": "auxRun",
    "aux_standby": "auxStandby",
}


def _db_row_to_camel(row_dict: dict) -> dict:
    """将 DB 行 dict(snake_case) 转为 camelCase，保留原键"""
    result = {}
    for key, value in row_dict.items():
        camel = _FIELD_MAP.get(key, key)
        result[camel] = value
        # 同时保留 snake_case 键，兼容两种访问方式
        if camel != key:
            result[key] = value
    # Container 需要 ratedPowerMw（小写 w）兼容旧代码
    if "ratedPowerMW" in result and "ratedPowerMw" not in result:
        result["ratedPowerMw"] = result["ratedPowerMW"]
    # Container 需要 ratedEnergyMwh（小写 w）兼容旧代码
    if "ratedEnergyMWh" in result and "ratedEnergyMwh" not in result:
        result["ratedEnergyMwh"] = result["ratedEnergyMWh"]
    return result


def _load_products_from_db():
    """从数据库加载产品库（优先），返回与 JSON 文件相同结构的 dict"""
    try:
        from database import db as _db
        from models.product import (
            CellProduct,
            ClusterProduct,
            ContainerProduct,
            PackProduct,
            PcsProduct,
            RackProduct,
        )

        # 需要在 app context 内执行
        containers_raw = ContainerProduct.query.filter(ContainerProduct.status == "active").all()
        pcs_raw = PcsProduct.query.filter(PcsProduct.status == "active").all()
        cells_raw = CellProduct.query.filter(CellProduct.status == "active").all()
        packs_raw = PackProduct.query.filter(PackProduct.status == "active").all()
        racks_raw = RackProduct.query.filter(RackProduct.status == "active").all()
        clusters_raw = ClusterProduct.query.filter(ClusterProduct.status == "active").all()

        containers = [_db_row_to_camel(c.to_dict()) for c in containers_raw]
        pcs_list = [_db_row_to_camel(p.to_dict()) for p in pcs_raw]

        if containers or pcs_list:
            return {
                "containers": containers,
                "pcs": pcs_list,
                "cells": [_db_row_to_camel(c.to_dict()) for c in cells_raw],
                "packs": [_db_row_to_camel(p.to_dict()) for p in packs_raw],
                "racks": [_db_row_to_camel(r.to_dict()) for r in racks_raw],
                "clusters": [_db_row_to_camel(c.to_dict()) for c in clusters_raw],
            }
        return None  # DB 为空
    except Exception:
        return None  # DB 不可用时回退 JSON


def _load_products():
    """加载产品库数据 — DB 优先，JSON 兜底"""
    # 优先从 DB 加载
    db_products = _load_products_from_db()
    if db_products and (db_products.get("containers") or db_products.get("pcs")):
        return db_products

    # JSON 文件兜底
    if not os.path.exists(_PRODUCTS_PATH):
        return {"cells": [], "containers": [], "pcs": [], "racks": [], "clusters": [], "packs": []}
    with open(_PRODUCTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class DesignEngine(BaseEngine):
    """方案设计引擎"""

    name = "design"

    def __init__(self):
        super().__init__()
        self._products = None

    @property
    def products(self):
        if self._products is None:
            self._products = _load_products()
        return self._products

    def validate_input(self, data: dict) -> list:
        """验证输入参数"""
        errors = []
        required = ["totalPower", "ratedEnergy", "duration", "temperature", "cyclesPerDay"]
        for field in required:
            val = data.get(field)
            if val is None or (isinstance(val, (int, float)) and val <= 0):
                errors.append({"field": field, "error": f"{field} is required and must be positive"})
        temp = data.get("temperature", 25)
        if temp < -20 or temp > 60:
            errors.append({"field": "temperature", "error": "must be between -20 and 60"})
        return errors

    def run(self, **kwargs):
        """执行设计引擎"""
        survey = kwargs.get("survey_params", kwargs)
        strategy = kwargs.get("strategy", "economic")
        manufacturer = kwargs.get("manufacturer")

        # Step 1: 约束求解 — 确定集装箱组合
        candidates = self._solve_combinations(survey, manufacturer)

        # Step 2: PCS 自动匹配
        candidates = self._match_pcs(candidates, survey)

        # Step 3: 效率链构建
        candidates = self._build_efficiency_chain(candidates, survey)

        # Step 4: 衰减模型选择
        candidates = self._select_degradation_model(candidates, survey)

        # Step 5: 辅耗计算
        candidates = self._calculate_aux_power(candidates, survey)

        # Step 6: CAPEX 预估
        candidates = self._estimate_capex(candidates, survey)

        # Step 7: 按策略排序
        candidates = self._rank_by_strategy(candidates, strategy)

        return {
            "strategy": strategy,
            "solutions": candidates[:5],
            "recommendation": candidates[0] if candidates else None,
        }

    def _solve_combinations(self, survey: dict, manufacturer: str = None) -> list:
        """约束求解：根据 targetEnergy 计算集装箱组合"""
        target_energy = float(survey.get("ratedEnergy", 100))
        target_power = float(survey.get("totalPower", 50))
        duration = float(survey.get("duration", 2))

        containers = self.products.get("containers", [])
        if manufacturer:
            containers = [c for c in containers if manufacturer.lower() in c.get("mfr", "").lower()]

        # 按容量从大到小排序
        containers = sorted(containers, key=lambda c: c.get("ratedEnergyMwh", 0), reverse=True)

        candidates = []
        for strategy_type, container_subset in self._group_by_strategy(containers):
            for container in container_subset:
                energy = container.get("ratedEnergyMwh", 5)
                if energy <= 0:
                    continue
                qty = max(1, math.ceil(target_energy / energy))
                total_energy = qty * energy

                candidates.append(
                    {
                        "id": str(uuid.uuid4())[:8],
                        "strategy_type": strategy_type,
                        "container": {
                            "id": container.get("id"),
                            "model": container.get("model"),
                            "mfr": container.get("mfr"),
                            "ratedEnergyMwh": energy,
                            "ratedPowerMw": container.get("ratedPowerMw", 2.5),
                            "cooling": container.get("cooling", "Liquid Cooling"),
                            "cellModel": container.get("cellModel"),
                            "clustersPerContainer": container.get("clustersPerContainer", 2),
                        },
                        "containerQty": qty,
                        "totalEnergyMwh": round(total_energy, 2),
                        "duration": round(total_energy / target_power, 1) if target_power > 0 else duration,
                    }
                )
        return candidates

    def _group_by_strategy(self, containers: list) -> list:
        """按策略分组容器"""
        if not containers:
            return [("economic", [])]

        sorted_c = sorted(containers, key=lambda c: c.get("ratedEnergyMwh", 0), reverse=True)
        n = len(sorted_c)
        if n <= 3:
            return [("economic", [sorted_c[0]]), ("balanced", sorted_c[:1]), ("flexible", sorted_c[-1:])]

        economic = [sorted_c[0]]  # 最大容量
        balanced = sorted_c[n // 3 : n // 3 + 2] if n >= 3 else sorted_c[:1]  # 中等容量
        flexible = sorted_c[-2:] if n >= 2 else sorted_c[:1]  # 较小容量

        return [("economic", economic), ("balanced", balanced), ("flexible", flexible)]

    def _match_pcs(self, candidates: list, survey: dict) -> list:
        """PCS 自动匹配"""
        target_power = float(survey.get("totalPower", 50))
        pcs_list = self.products.get("pcs", [])

        for c in candidates:
            rated_power = max(1.0, min(p.get("ratedPowerMW", 2.5) for p in pcs_list) if pcs_list else 2.5)
            # 选择额定功率最接近需求功率的 PCS
            best_pcs = None
            best_diff = float("inf")
            for pcs in pcs_list:
                pcs_power = pcs.get("ratedPowerMW", 2.5)
                if target_power > 0:
                    diff = abs(pcs_power - target_power / max(1, math.ceil(target_power / pcs_power)))
                else:
                    diff = abs(pcs_power - 2.5)
                if diff < best_diff:
                    best_diff = diff
                    best_pcs = pcs
                    rated_power = pcs_power

            pcs_qty = max(1, math.ceil(target_power / rated_power)) if rated_power > 0 else 1
            c["pcs"] = {
                "id": best_pcs.get("id") if best_pcs else None,
                "model": best_pcs.get("model") if best_pcs else "Default PCS",
                "mfr": best_pcs.get("mfr") if best_pcs else None,
                "ratedPowerMW": rated_power,
                "efficiency": best_pcs.get("efficiency", 98.0) if best_pcs else 98.0,
                "acVoltage": best_pcs.get("acVoltage") if best_pcs else "690V",
                "dcVoltageRange": best_pcs.get("dcVoltageRange") if best_pcs else "800-1500V",
            }
            c["pcsQty"] = pcs_qty
            c["totalPowerMW"] = round(pcs_qty * rated_power, 2)
        return candidates

    def _build_efficiency_chain(self, candidates: list, survey: dict) -> list:
        """效率链自动构建"""
        for c in candidates:
            pcs_eff = c.get("pcs", {}).get("efficiency", 98.0) / 100.0
            # 默认效率链: cell RTE(97%) × PCS eff × transformer(99%) × cable(99.5%)
            cell_rte = 0.97
            transformer_eff = 0.99
            cable_eff = 0.995

            system_rte = cell_rte * pcs_eff * transformer_eff * cable_eff
            c["efficiencyChain"] = {
                "cellRTE": round(cell_rte * 100, 1),
                "pcsEfficiency": round(pcs_eff * 100, 1),
                "transformerEfficiency": round(transformer_eff * 100, 1),
                "cableEfficiency": round(cable_eff * 100, 1),
                "systemRTE": round(system_rte * 100, 1),
            }
        return candidates

    def _select_degradation_model(self, candidates: list, survey: dict) -> list:
        """衰减模型自动选择"""
        temperature = float(survey.get("temperature", 25))
        cycles_per_day = float(survey.get("cyclesPerDay", 1))
        dod = float(survey.get("dod", 90))

        for c in candidates:
            cell_model = c.get("container", {}).get("cellModel", "")
            manufacturer = c.get("container", {}).get("mfr", "")

            # 尝试从 ai_sim 获取厂家校准参数
            manufacturer_params = self._get_manufacturer_params(manufacturer)

            c["degradationModel"] = {
                "model": "arrhenius",
                "manufacturer": manufacturer,
                "cellModel": cell_model,
                "temperature": temperature,
                "cyclesPerDay": cycles_per_day,
                "dod": dod,
                "params": manufacturer_params
                or {
                    "A_cal": 1.950563,
                    "Ea_cal": 26000,
                    "alpha": 0.8,
                    "A_cyc": 12.556758,
                    "Ea_cyc": 22000,
                    "beta": 0.5,
                    "gamma": 1.5,
                    "delta": 0.2,
                },
            }
        return candidates

    def _get_manufacturer_params(self, manufacturer: str) -> dict:
        """获取厂家校准的 Arrhenius 参数"""
        if not manufacturer:
            return None
        try:
            from services.ai_sim import MANUFACTURERS

            for m in MANUFACTURERS:
                if m.get("name", "").lower() in manufacturer.lower():
                    return m.get("calibrated_params", m.get("params"))
        except ImportError:
            pass
        return None

    def _calculate_aux_power(self, candidates: list, survey: dict) -> list:
        """辅耗自动计算"""
        duration = float(survey.get("duration", 2))
        cycles_per_day = float(survey.get("cyclesPerDay", 1))

        for c in candidates:
            container_qty = c.get("containerQty", 10)
            run_hours = duration * cycles_per_day
            standby_hours = max(0, 24 - run_hours)

            # 默认辅耗参数（kW）
            bess_aux_run = 18.124  # 集装箱运行辅耗
            bess_aux_standby = 3.5  # 集装箱待机辅耗
            pcs_aux_run = 6.5  # PCS 运行辅耗
            pcs_aux_standby = 1.0  # PCS 待机辅耗

            daily_bess_aux = container_qty * (bess_aux_run * run_hours + bess_aux_standby * standby_hours) / 1000
            daily_pcs_aux = c.get("pcsQty", 10) * (pcs_aux_run * run_hours + pcs_aux_standby * standby_hours) / 1000

            c["auxPower"] = {
                "bessAuxRun": bess_aux_run,
                "bessAuxStandby": bess_aux_standby,
                "pcsAuxRun": pcs_aux_run,
                "pcsAuxStandby": pcs_aux_standby,
                "dailyBessAuxMWh": round(daily_bess_aux, 4),
                "dailyPcsAuxMWh": round(daily_pcs_aux, 4),
                "dailyTotalAuxMWh": round(daily_bess_aux + daily_pcs_aux, 4),
            }
        return candidates

    def _estimate_capex(self, candidates: list, survey: dict) -> list:
        """CAPEX 预估"""
        for c in candidates:
            container_qty = c.get("containerQty", 10)
            pcs_qty = c.get("pcsQty", 10)
            total_energy = c.get("totalEnergyMwh", 100)

            # 从产品库获取单价（如有）
            container_unit_price = self._get_unit_price("containers", c.get("container", {}).get("id"))
            pcs_unit_price = self._get_unit_price("pcs", c.get("pcs", {}).get("id"))

            # 默认单价（$/unit）
            if container_unit_price is None:
                container_unit_price = total_energy * 200000  # $200k/MWh
            if pcs_unit_price is None:
                pcs_unit_price = c.get("pcs", {}).get("ratedPowerMW", 2.5) * 80000  # $80k/MW

            container_cost = container_qty * container_unit_price
            pcs_cost = pcs_qty * pcs_unit_price
            equipment_cost = container_cost + pcs_cost
            bop_cost = equipment_cost * 0.18  # 18% BOP
            epc_cost = equipment_cost * 0.08  # 8% EPC fee
            development_cost = equipment_cost * 0.05  # 5% development
            total_capex = equipment_cost + bop_cost + epc_cost + development_cost

            c["estimatedCapex"] = {
                "containerCost": round(container_cost, 2),
                "pcsCost": round(pcs_cost, 2),
                "equipmentCost": round(equipment_cost, 2),
                "bopCost": round(bop_cost, 2),
                "epcCost": round(epc_cost, 2),
                "developmentCost": round(development_cost, 2),
                "totalCapex": round(total_capex, 2),
                "capexPerMWh": round(total_capex / total_energy, 2) if total_energy > 0 else 0,
                "currency": "USD",
            }
        return candidates

    def _get_unit_price(self, category: str, product_id: str) -> float:
        """从产品库获取单价"""
        if not product_id:
            return None
        items = self.products.get(category, [])
        for item in items:
            if item.get("id") == product_id:
                price = item.get("unitPrice") or item.get("unit_price")
                if price is not None:
                    return float(price)
                break
        return None

    def _rank_by_strategy(self, candidates: list, strategy: str) -> list:
        """按策略排序"""
        if strategy == "economic":
            # 经济优先：总 CAPEX 最低
            candidates.sort(key=lambda c: c.get("estimatedCapex", {}).get("totalCapex", float("inf")))
        elif strategy == "balanced":
            # 均衡：CAPEX/MWh 最低
            candidates.sort(key=lambda c: c.get("estimatedCapex", {}).get("capexPerMWh", float("inf")))
        elif strategy == "flexible":
            # 灵活：容器数量最多（便于分期扩容）
            candidates.sort(key=lambda c: -c.get("containerQty", 0))
        elif strategy == "manufacturer":
            # 指定厂家：保持原序
            pass

        # 给每个方案打分
        for i, c in enumerate(candidates):
            capex = c.get("estimatedCapex", {}).get("totalCapex", 0)
            rte = c.get("efficiencyChain", {}).get("systemRTE", 85)
            c["rank"] = i + 1
            c["score"] = round(rte * 1000000 / max(capex, 1), 2)  # 综合评分

        return candidates


# 便捷函数
def auto_design(survey_params: dict, strategy: str = "economic", manufacturer: str = None) -> dict:
    """自动生成设计方案（便捷入口）"""
    engine = DesignEngine()
    return engine.run(survey_params=survey_params, strategy=strategy, manufacturer=manufacturer)
