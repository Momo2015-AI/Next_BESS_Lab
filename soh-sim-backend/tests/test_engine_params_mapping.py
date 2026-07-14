"""
SOH-SIM Engine Params Mapping Tests

验证 SimulationEngine._extract_params 和 FinancialEngine._estimate_capex /
_select_revenue_model 正确映射所有参数，包括新的 auxPowerMode / ambientTemp /
coolingType / efficiencyFactors 字段。

运行方式:
    cd soh-sim-backend
    python -m pytest tests/test_engine_params_mapping.py -v --tb=short 2>&1
"""

from services.efficiency import FACTOR_DEFAULTS
from services.financial.engine import FinancialEngine
from services.simulation.engine import SimulationEngine

# ==================== TestSimulationEngineParamsMapping ====================


class TestSimulationEngineParamsMapping:
    """验证 SimulationEngine._extract_params 参数映射"""

    @staticmethod
    def _extract(design_output=None, survey_params=None):
        """便捷方法：直接调用 _extract_params"""
        engine = SimulationEngine()
        return engine._extract_params(design_output or {}, survey_params or {})

    # ---- 1. 热管理模式映射 ----

    def test_aux_power_mode_thermal_mapped(self):
        """auxPowerMode="thermal", ambientTemp=32, coolingType="liquid" 正确映射"""
        params = self._extract(
            design_output={"containerQty": 10, "pcsQty": 10, "duration": 2},
            survey_params={
                "auxPowerMode": "thermal",
                "ambientTemp": 32,
                "coolingType": "liquid",
                "temperature": 25,
                "cyclesPerDay": 1,
                "dod": 90,
            },
        )
        assert params["auxPowerMode"] == "thermal", f"Expected thermal, got {params['auxPowerMode']}"
        assert params["ambientTemp"] == 32, f"Expected 32, got {params['ambientTemp']}"
        assert params["coolingType"] == "liquid", f"Expected liquid, got {params['coolingType']}"

    # ---- 2. auxPowerMode 默认值 ----

    def test_aux_power_mode_manual_default(self):
        """不传 auxPowerMode 时默认为 manual"""
        params = self._extract(
            design_output={"containerQty": 10, "pcsQty": 10, "duration": 2},
            survey_params={"temperature": 25, "cyclesPerDay": 1, "dod": 90},
        )
        assert params["auxPowerMode"] == "manual", f"Expected manual (default), got {params['auxPowerMode']}"

    # ---- 3. ambientTemp 回退到 tempAvg ----

    def test_ambient_temp_fallback_to_tempAvg(self):
        """survey_params 有 tempAvg 但无 ambientTemp 时，ambientTemp 回退到 tempAvg"""
        params = self._extract(
            design_output={"containerQty": 10, "pcsQty": 10, "duration": 2},
            survey_params={
                "tempAvg": 30,
                "temperature": 25,
                "cyclesPerDay": 1,
                "dod": 90,
            },
        )
        assert params["ambientTemp"] == 30, f"Expected 30 (from tempAvg), got {params['ambientTemp']}"

    # ---- 4. ambientTemp 直接使用 ----

    def test_ambient_temp_from_survey_params(self):
        """survey_params 有 ambientTemp 时直接使用，不取 tempAvg"""
        params = self._extract(
            design_output={"containerQty": 10, "pcsQty": 10, "duration": 2},
            survey_params={
                "ambientTemp": 40,
                "tempAvg": 30,
                "temperature": 25,
                "cyclesPerDay": 1,
                "dod": 90,
            },
        )
        assert params["ambientTemp"] == 40, f"Expected 40 (ambientTemp takes priority), got {params['ambientTemp']}"

    # ---- 5. efficiencyFactors=None 穿透 ----

    def test_efficiency_factors_none_passthrough(self):
        """survey_params 中 efficiencyFactors=None 时保留 None"""
        params = self._extract(
            design_output={"containerQty": 10, "pcsQty": 10, "duration": 2},
            survey_params={
                "temperature": 25,
                "cyclesPerDay": 1,
                "dod": 90,
                "efficiencyFactors": None,
            },
        )
        assert params["efficiencyFactors"] is None, f"Expected None, got {params['efficiencyFactors']}"

    # ---- 6. efficiencyFactors 默认值 ----

    def test_efficiency_factors_default(self):
        """不传 efficiencyFactors 时默认为 FACTOR_DEFAULTS"""
        params = self._extract(
            design_output={"containerQty": 10, "pcsQty": 10, "duration": 2},
            survey_params={"temperature": 25, "cyclesPerDay": 1, "dod": 90},
        )
        assert (
            params["efficiencyFactors"] == FACTOR_DEFAULTS
        ), "Expected FACTOR_DEFAULTS when efficiencyFactors not provided"

    # ---- 7. coolingType 默认值 ----

    def test_cooling_type_default(self):
        """不传 coolingType 时默认为 liquid"""
        params = self._extract(
            design_output={"containerQty": 10, "pcsQty": 10, "duration": 2},
            survey_params={"temperature": 25, "cyclesPerDay": 1, "dod": 90},
        )
        assert params["coolingType"] == "liquid", f"Expected liquid (default), got {params['coolingType']}"

    # ---- 8. 完整参数集成 ----

    def test_full_params_integration(self):
        """传入所有新参数，验证每一个都映射正确"""
        params = self._extract(
            design_output={
                "container": {"ratedEnergyMwh": 5},
                "pcs": {"ratedPowerMW": 2.5},
                "containerQty": 20,
                "pcsQty": 20,
                "duration": 4,
                "auxPower": {
                    "bessAuxRun": 10.0,
                    "bessAuxStandby": 2.0,
                    "pcsAuxRun": 5.0,
                    "pcsAuxStandby": 0.5,
                },
                "efficiencyChain": {"systemRTE": 95.0},
            },
            survey_params={
                "temperature": 35,
                "cyclesPerDay": 2,
                "dod": 85,
                "cRate": 1.0,
                "auxPowerMode": "thermal",
                "ambientTemp": 35,
                "coolingType": "SiC-liquid",
                "requiredEnergy": 500,
                "efficiencyFactors": None,
            },
        )

        # 基础参数
        assert params["ratedEnergy"] == 5, f"ratedEnergy: {params['ratedEnergy']}"
        assert params["initContainerQty"] == 20, f"initContainerQty: {params['initContainerQty']}"
        assert params["initPcsQty"] == 20, f"initPcsQty: {params['initPcsQty']}"
        assert params["pcsPower"] == 2.5, f"pcsPower: {params['pcsPower']}"
        assert params["duration"] == 4, f"duration: {params['duration']}"

        # survey 参数
        assert params["cyclesPerDay"] == 2, f"cyclesPerDay: {params['cyclesPerDay']}"
        assert params["temperature"] == 35, f"temperature: {params['temperature']}"
        assert params["dod"] == 85, f"dod: {params['dod']}"
        assert params["cRate"] == 1.0, f"cRate: {params['cRate']}"

        # aux 参数（来自 design_output）
        assert params["bessAuxRun"] == 10.0, f"bessAuxRun: {params['bessAuxRun']}"
        assert params["bessAuxStandby"] == 2.0, f"bessAuxStandby: {params['bessAuxStandby']}"
        assert params["pcsAuxRun"] == 5.0, f"pcsAuxRun: {params['pcsAuxRun']}"
        assert params["pcsAuxStandby"] == 0.5, f"pcsAuxStandby: {params['pcsAuxStandby']}"

        # efficiency
        assert params["acEfficiency"] == 95.0, f"acEfficiency: {params['acEfficiency']}"

        # 新字段
        assert params["auxPowerMode"] == "thermal", f"auxPowerMode: {params['auxPowerMode']}"
        assert params["ambientTemp"] == 35, f"ambientTemp: {params['ambientTemp']}"
        assert params["coolingType"] == "SiC-liquid", f"coolingType: {params['coolingType']}"
        assert params["requiredEnergy"] == 500, f"requiredEnergy: {params['requiredEnergy']}"
        assert params["efficiencyFactors"] is None, f"efficiencyFactors: {params['efficiencyFactors']}"


# ==================== TestFinancialEngineParamsMapping ====================


class TestFinancialEngineParamsMapping:
    """验证 FinancialEngine 参数映射"""

    # ---- 9. CAPEX 从 container 计算 ----

    def test_financial_engine_capex_from_container(self):
        """_estimate_capex 使用 container × containerQty 计算 equipment"""
        engine = FinancialEngine()
        capex = engine._estimate_capex(
            design_output={
                "container": {"ratedEnergyMwh": 5},
                "containerQty": 100,
            },
            survey_params={},
        )
        # total_energy = 5 * 100 = 500
        # equipment = 500 * 200000 = 100,000,000
        assert capex["equipment"] > 0, f"equipment should be > 0, got {capex['equipment']}"
        expected_equipment = 500 * 200000  # 100,000,000
        assert capex["equipment"] == expected_equipment, f"Expected {expected_equipment}, got {capex['equipment']}"
        # 验证不是旧逻辑的 100*200000=20,000,000
        assert (
            capex["equipment"] != 100 * 200000
        ), "equipment should use totalEnergy (container * qty), not just containerQty"

    # ---- 10. CAPEX fallback 使用 totalEnergyMwh ----

    def test_financial_engine_capex_fallback(self):
        """totalEnergyMwh 存在时直接使用"""
        engine = FinancialEngine()
        capex = engine._estimate_capex(
            design_output={"totalEnergyMwh": 200},
            survey_params={},
        )
        expected_equipment = 200 * 200000  # 40,000,000
        assert capex["equipment"] == expected_equipment, f"Expected {expected_equipment}, got {capex['equipment']}"

    # ---- 11. 中国收入模型 ----

    def test_financial_engine_revenue_model_china(self):
        """location="china" → arbitrage enabled, ancillary disabled"""
        engine = FinancialEngine()
        revenue = engine._select_revenue_model({"location": "china"})

        assert revenue["arbitrage"]["enabled"] is True, "China: arbitrage should be enabled"
        assert revenue["ancillary"]["enabled"] is False, "China: ancillary should be disabled"
        assert revenue["capacity"]["enabled"] is True, "China: capacity should be enabled"

    # ---- 12. 默认收入模型（无匹配） ----

    def test_financial_engine_revenue_model_cambodia(self):
        """location="cambodia" (无匹配) → 默认模型，所有收益流启用"""
        engine = FinancialEngine()
        revenue = engine._select_revenue_model({"location": "cambodia"})

        assert revenue["arbitrage"]["enabled"] is True, "Default: arbitrage should be enabled"
        assert revenue["ancillary"]["enabled"] is True, "Default: ancillary should be enabled"
        assert revenue["capacity"]["enabled"] is True, "Default: capacity should be enabled"
        assert revenue["ppa"]["enabled"] is True, "Default: ppa should be enabled"
        assert revenue["capacityAuction"]["enabled"] is True, "Default: capacityAuction should be enabled"
