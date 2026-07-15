"""
SOH-SIM 深度测试 — 三大引擎 + 数据流转 + 支撑服务（可独立运行，无需数据库）

覆盖：
  - DesignEngine  （设计引擎）：校验 / 4 策略 / PCS 匹配 / 效率链 / CAPEX / 排序
  - SimulationEngine（仿真引擎）：SOH(Arrenius/GB36276) / 能量核算 / 补容三策略 / 经济性对比
  - FinancialEngine （财务引擎）：CAPEX/OPEX / 5 收入流 / 融资税务 / 敏感性 / 指标公式
  - 数据流转 E2E： Design → Simulation → Financial 端到端 + 输出即输入一致性
  - 支撑服务：predict_soh / efficiency_chain / aux_power / pipeline

运行：
    cd soh-sim-backend
    python -m pytest tests/test_engines_deep.py -v --tb=short
"""

import math

import pytest

from services.aux_power import calculate_aux_power
from services.degradation import NUM_YEARS, predict_soh
from services.design.engine import DesignEngine, _load_products
from services.efficiency import FACTOR_DEFAULTS, calculate_efficiency_chain
from services.financial.engine import FinancialEngine
from services.orchestrator import run_full_workflow
from services.simulation.engine import SimulationEngine

# ==================== 公共 Fixtures ====================


@pytest.fixture
def fake_products(monkeypatch):
    """用内存产品库替代缺失的 data/products.json，使 DesignEngine 可确定性测试。"""
    products = {
        "cells": [{"id": "c1", "model": "LFP-280", "mfr": "CATL"}],
        "containers": [
            {
                "id": "ct1",
                "model": "C5-MWh",
                "mfr": "CATL",
                "ratedEnergyMWh": 5.0,
                "ratedPowerMw": 2.5,
                "cooling": "Liquid Cooling",
                "cellModel": "LFP-280",
                "clustersPerContainer": 2,
                "unitPrice": 1000000,
            },
            {
                "id": "ct2",
                "model": "C2.5-MWh",
                "mfr": "BYD",
                "ratedEnergyMWh": 2.5,
                "ratedPowerMw": 1.25,
                "cooling": "Liquid Cooling",
                "cellModel": "LFP-280",
                "clustersPerContainer": 2,
                "unitPrice": 500000,
            },
        ],
        "pcs": [
            {
                "id": "p1",
                "model": "PCS-2.5",
                "mfr": "Sungrow",
                "ratedPowerMW": 2.5,
                "efficiency": 98.5,
                "acVoltage": "690V",
                "dcVoltageRange": "800-1500V",
                "unitPrice": 200000,
            },
            {
                "id": "p2",
                "model": "PCS-1.25",
                "mfr": "Sungrow",
                "ratedPowerMW": 1.25,
                "efficiency": 98.0,
                "unitPrice": 100000,
            },
        ],
        "racks": [],
        "clusters": [],
        "packs": [],
    }
    monkeypatch.setattr("services.design.engine._load_products", lambda: products)
    return products


@pytest.fixture
def survey():
    return {
        "ratedEnergy": 100,  # 目标储能容量 MWh
        "totalPower": 50,  # 目标功率 MW
        "duration": 2,
        "temperature": 25,
        "cyclesPerDay": 1,
        "dod": 90,
        "cRate": 0.5,
        "location": "china",
        "requiredEnergy": 240,
    }


# ==================== 1. DesignEngine ====================


class TestDesignEngine:
    def test_validate_missing_required(self):
        eng = DesignEngine()
        errs = eng.validate_input({})
        fields = {e["field"] for e in errs}
        assert {"totalPower", "ratedEnergy", "duration", "temperature", "cyclesPerDay"} <= fields

    def test_validate_negative_power_rejected(self):
        eng = DesignEngine()
        errs = eng.validate_input(
            {"totalPower": -5, "ratedEnergy": 100, "duration": 2, "temperature": 25, "cyclesPerDay": 1}
        )
        assert any(e["field"] == "totalPower" for e in errs)

    def test_validate_temperature_bounds(self):
        eng = DesignEngine()
        assert any(e["field"] == "temperature" for e in eng.validate_input({**survey_default(), "temperature": 80}))
        assert any(e["field"] == "temperature" for e in eng.validate_input({**survey_default(), "temperature": -30}))

    @pytest.mark.parametrize("strategy", ["economic", "balanced", "flexible", "manufacturer"])
    def test_four_strategies_produce_solutions(self, fake_products, survey, strategy):
        res = DesignEngine().run(survey_params=survey, strategy=strategy)
        assert res["strategy"] == strategy
        assert len(res["solutions"]) > 0, "应至少生成一个候选方案"
        assert res["recommendation"] is not None

    def test_manufacturer_filter(self, fake_products, survey):
        res = DesignEngine().run(survey_params=survey, strategy="manufacturer", manufacturer="BYD")
        for s in res["solutions"]:
            assert s["container"]["mfr"] == "BYD"

    def test_pcs_matched(self, fake_products, survey):
        res = DesignEngine().run(survey_params=survey)
        c = res["solutions"][0]
        assert c["pcs"]["ratedPowerMW"] > 0
        assert c["pcsQty"] >= 1
        # 总功率应覆盖目标功率
        assert c["totalPowerMW"] >= survey["totalPower"] - 1e-6

    def test_efficiency_chain_product(self, fake_products, survey):
        res = DesignEngine().run(survey_params=survey)
        chain = res["solutions"][0]["efficiencyChain"]
        pcs = chain["pcsEfficiency"] / 100
        cell = chain["cellRTE"] / 100
        tf = chain["transformerEfficiency"] / 100
        cable = chain["cableEfficiency"] / 100
        expected = round(cell * pcs * tf * cable * 100, 1)
        assert chain["systemRTE"] == expected, "systemRTE 必须等于各段乘积"

    def test_capex_breakdown_sums(self, fake_products, survey):
        res = DesignEngine().run(survey_params=survey)
        cap = res["solutions"][0]["estimatedCapex"]
        total = cap["containerCost"] + cap["pcsCost"] + cap["bopCost"] + cap["epcCost"] + cap["developmentCost"]
        assert abs(total - cap["totalCapex"]) < 1.0
        assert cap["currency"] == "USD"

    def test_ranking_present(self, fake_products, survey):
        res = DesignEngine().run(survey_params=survey, strategy="economic")
        sols = res["solutions"]
        ranks = [s["rank"] for s in sols]
        assert ranks == list(range(1, len(sols) + 1))
        # economic：按 totalCapex 升序
        capexes = [s["estimatedCapex"]["totalCapex"] for s in sols]
        assert capexes == sorted(capexes)


# ==================== 2. SimulationEngine ====================


def _build_design(fake_products, survey):
    return DesignEngine().run(survey_params=survey, strategy="economic")["solutions"][0]


class TestSimulationEngine:
    def test_validate_input_required(self):
        eng = SimulationEngine()
        errs = eng.validate_input({"system_params": {}})
        assert any(e["field"] == "ratedEnergy" for e in errs)

    def test_run_returns_full_contract(self, fake_products, survey):
        design = _build_design(fake_products, survey)
        res = SimulationEngine().run(design_output=design, survey_params=survey)
        for k in [
            "years",
            "soh",
            "rte",
            "dod",
            "augQty",
            "efficiencyCurves",
            "efficiencyDetail",
            "totalAcUsable",
            "meetsReq",
            "augmentationStrategy",
            "augmentationComparison",
        ]:
            assert k in res, f"缺少输出字段 {k}"
        assert len(res["soh"]) == NUM_YEARS
        assert res["soh"][0] == 100.0  # 第 0 年 SOH=100%

    def test_soh_monotonic_decreasing(self, fake_products, survey):
        design = _build_design(fake_products, survey)
        res = SimulationEngine().run(design_output=design, survey_params=survey)
        soh = res["soh"]
        for i in range(1, len(soh)):
            assert soh[i] <= soh[i - 1] + 1e-9, "SOH 应随时间单调不增"

    def test_gb36276_model_runs(self, fake_products, survey):
        design = _build_design(fake_products, survey)
        res = SimulationEngine().run(
            design_output=design,
            survey_params=survey,
            algorithm={"model": "gb36276"},
        )
        assert len(res["soh"]) == NUM_YEARS
        assert all(0 <= s <= 100 for s in res["soh"])

    def test_meets_req_logic(self, fake_products, survey):
        design = _build_design(fake_products, survey)
        res = SimulationEngine().run(design_output=design, survey_params=survey)
        for i, meets in enumerate(res["meetsReq"]):
            assert meets == (res["totalAcUsable"][i] >= survey["requiredEnergy"] - 1e-6)

    def test_augmentation_three_strategies(self, fake_products, survey):
        design = _build_design(fake_products, survey)
        res = SimulationEngine().run(design_output=design, survey_params=survey)
        strat = res["augmentationStrategy"]["strategies"]
        assert set(strat.keys()) == {"fixed_periodic", "on_demand", "overbuild"}
        assert res["augmentationStrategy"]["recommended"] == "on_demand"

    def test_augmentation_comparison_recommends_best_npv(self, fake_products, survey):
        design = _build_design(fake_products, survey)
        res = SimulationEngine().run(design_output=design, survey_params=survey)
        comp = res["augmentationComparison"]
        best = comp["recommended"]
        assert best in comp["strategies"]
        # 推荐策略的 NPV 应 >= 其它策略（除非无度量）
        npvs = {k: (v["metrics"] or {}).get("npv") for k, v in comp["strategies"].items()}
        if all(v is not None for v in npvs.values()):
            assert npvs[best] == max(npvs.values())


# ==================== 3. FinancialEngine ====================


class TestFinancialEngine:
    def test_validate_requires_total_ac(self):
        eng = FinancialEngine()
        assert any(e["field"] == "totalAcUsable" for e in eng.validate_input({"simulation_output": {}}))

    def test_run_returns_metrics(self, fake_products, survey):
        design = _build_design(fake_products, survey)
        sim = SimulationEngine().run(design_output=design, survey_params=survey)
        res = FinancialEngine().run(
            simulation_output={"totalAcUsable": sim["totalAcUsable"]},
            design_output=design,
            survey_params=survey,
        )
        m = res["metrics"]
        for k in ["projectIrr", "npv", "lcos", "dscr", "payback", "roi"]:
            assert k in m
        assert res["cashflowTable"][0]["freeCashflow"] < 0  # 第 0 年为负 CAPEX

    def test_location_selects_revenue_model(self):
        eng = FinancialEngine()
        china = eng._select_revenue_model({"location": "china"})
        assert china["arbitrage"]["enabled"] and china["capacity"]["enabled"]
        assert not china["ppa"]["enabled"]
        me = eng._select_revenue_model({"location": "middle east"})
        assert me["ppa"]["enabled"] and me["capacityAuction"]["enabled"]
        assert not me["arbitrage"]["enabled"]

    def test_sensitivity_four_scenarios(self, fake_products, survey):
        design = _build_design(fake_products, survey)
        sim = SimulationEngine().run(design_output=design, survey_params=survey)
        res = FinancialEngine().run(
            simulation_output={"totalAcUsable": sim["totalAcUsable"]},
            design_output=design,
            survey_params=survey,
        )
        sens = res["sensitivity"]
        assert set(sens.keys()) == {"capex_plus_15", "capex_minus_15", "price_plus_20", "price_minus_20"}
        # 电价上涨 20% 应提升 NPV
        base = res["metrics"]["npv"]
        assert sens["price_plus_20"]["npv"] >= base
        assert sens["price_minus_20"]["npv"] <= base

    def test_dscr_satisfied_flag(self, fake_products, survey):
        design = _build_design(fake_products, survey)
        sim = SimulationEngine().run(design_output=design, survey_params=survey)
        res = FinancialEngine().run(
            simulation_output={"totalAcUsable": sim["totalAcUsable"]},
            design_output=design,
            survey_params=survey,
        )
        dscr = res["metrics"]["dscr"]
        assert "min" in dscr and "avg" in dscr
        assert dscr["min"] >= 0


# ==================== 4. 数据流转 E2E ====================


class TestDataFlow:
    def test_design_to_simulation_to_financial(self, fake_products, survey):
        """核心数据流转：设计输出 → 仿真输入 → 财务输入（输出即输入）"""
        design = DesignEngine().run(survey_params=survey, strategy="economic")["solutions"][0]
        sim = SimulationEngine().run(design_output=design, survey_params=survey)
        # 仿真输出作为财务输入
        fin = FinancialEngine().run(
            simulation_output={"totalAcUsable": sim["totalAcUsable"]},
            design_output=design,
            survey_params=survey,
        )
        assert len(fin["cashflowTable"]) == NUM_YEARS
        assert fin["metrics"]["npv"] is not None

    def test_orchestrator_full_workflow(self, fake_products, survey):
        """编排层端到端"""
        res = run_full_workflow(survey_params=survey, strategy="economic", target_metric="lcos")
        assert res["pipeline_summary"]["total_solutions"] > 0
        assert res["recommendation"] is not None
        rec = res["recommendation"]
        assert rec["simulation"] is not None
        assert rec["financial"] is not None
        # 推荐方案应含完整 design+sim+fin
        assert rec["financial"]["metrics"]["lcos"] is not None

    def test_output_input_compatibility(self, fake_products, survey):
        """仿真引擎的 totalAcUsable 可直接喂给财务引擎（维度/类型一致）"""
        design = _build_design(fake_products, survey)
        sim = SimulationEngine().run(design_output=design, survey_params=survey)
        ac = sim["totalAcUsable"]
        assert isinstance(ac, list) and len(ac) == NUM_YEARS
        fin = FinancialEngine().run(
            simulation_output={"totalAcUsable": ac},
            design_output=design,
            survey_params=survey,
        )
        # 财务现金表首年 freeCashflow 应为负（CAPEX 支出）
        assert fin["cashflowTable"][0]["freeCashflow"] < 0


# ==================== 5. 支撑服务 ====================


class TestSupportServices:
    def test_predict_soh_arrhenius_monotonic(self):
        soh, rte = predict_soh("arrhenius", 25, 1, 90, 0.5)
        assert soh[0] == 100.0
        for i in range(1, len(soh)):
            assert soh[i] <= soh[i - 1] + 1e-9
        assert all(80 <= r <= 100 for r in rte)

    def test_predict_soh_gb36276_bounds(self):
        soh, rte = predict_soh("gb36276", 25, 1, 90, 0.25)
        assert all(0 <= s <= 100 for s in soh)

    def test_predict_soh_higher_temp_faster_decay(self):
        cold, _ = predict_soh("arrhenius", 25, 1, 90, 0.5)
        hot, _ = predict_soh("arrhenius", 45, 1, 90, 0.5)
        assert hot[10] < cold[10], "温度越高衰减应越快"

    def test_efficiency_chain_value(self):
        chain = calculate_efficiency_chain(FACTOR_DEFAULTS, 100.0)
        assert chain["rte"] > 0
        assert chain["systemRTE"] > 0

    def test_aux_power_calculation(self):
        params = {
            "days": 365,
            "cycles": 1,
            "hours": 2,
            "cap": 5,
            "units": 10,
            "dcRte": 0.941,
            "pcsEff": 0.987,
            "acEff": 0.975,
            "bRun": 18.124,
            "bStd": 3.5,
            "pRun": 6.5,
            "pStd": 1.0,
            "pStation": 7.2,
        }
        res = calculate_aux_power(params)
        # 真实输出字段
        assert res["dcTotalAux"] > 0
        assert res["acTotalAux"] > 0
        assert res["totalSystemAux"] > 0
        # 复算 tRun/tStd：cycles=1, hours=2 → tRun=365*1*2*2=1460
        t_run = 365 * 1 * 2 * 2
        t_std = 365 * 24 - t_run
        exp_dc = ((t_run * 18.124) + (t_std * 3.5)) * 10 / 1000
        assert abs(res["dcTotalAux"] - exp_dc) < 1e-2
        # 净放电 = 年毛放电 - 系统自耗，应 < 毛放电
        assert res["annualNetDischarge"] < res["annualGrossDischarge"]


def survey_default():
    return {"ratedEnergy": 100, "totalPower": 50, "duration": 2, "temperature": 25, "cyclesPerDay": 1}
