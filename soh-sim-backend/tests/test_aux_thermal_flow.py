"""
SOH-SIM Aux Thermal Flow Tests

验证热管理冷却功耗计算的完整数据流：
从 calculate_cooling_power 函数调用到仿真管线中的 auxPowerMode 集成。

运行方式:
    cd soh-sim-backend
    python -m pytest tests/test_aux_thermal_flow.py -v --tb=short 2>&1
"""

import pytest

from services.epc.thermal import FIXED_AUX_KW, calculate_cooling_power
from tests.test_integration import (
    SURVEY_PARAMS,
    _assert_success,
    _post,
)

# ==================== TestThermalCoolingFlow ====================


class TestThermalCoolingFlow:
    """验证热管理冷却功耗计算的完整数据流"""

    # ---- 1. 液冷 32C 冷却功耗计算 ----

    def test_calculate_cooling_power_liquid_32c(self):
        """calculate_cooling_power(32, "liquid") → cooling_power_kw ~8.47, COP=3.5"""
        result = calculate_cooling_power(32, "liquid")

        assert result["cop"] == 3.5, f"Expected COP=3.5, got {result['cop']}"
        assert result["ambient_temp_c"] == 32
        assert result["cooling_type"] == "liquid"

        # 验证 cooling_power_kw 约为 8.47（容许小范围浮动）
        cpk = result["cooling_power_kw"]
        assert 7.5 <= cpk <= 10.0, f"Expected cooling_power_kw ~8.47 for liquid at 32C, got {cpk}"

        # 验证 standby_power_kw = cooling_power_kw * 0.15
        expected_standby = round(cpk * 0.15, 2)
        assert (
            result["standby_power_kw"] == expected_standby
        ), f"standby_power_kw should be {expected_standby}, got {result['standby_power_kw']}"

    # ---- 2. 风冷 32C 冷却功耗计算 ----

    def test_calculate_cooling_power_forced_air_32c(self):
        """calculate_cooling_power(32, "forced-air") → cooling_power_kw ~14.83, COP=2.0"""
        result = calculate_cooling_power(32, "forced-air")

        assert result["cop"] == 2.0, f"Expected COP=2.0, got {result['cop']}"
        assert result["ambient_temp_c"] == 32
        assert result["cooling_type"] == "forced-air"

        cpk = result["cooling_power_kw"]
        assert 12.0 <= cpk <= 18.0, f"Expected cooling_power_kw ~14.83 for forced-air at 32C, got {cpk}"

        expected_standby = round(cpk * 0.15, 2)
        assert (
            result["standby_power_kw"] == expected_standby
        ), f"standby_power_kw should be {expected_standby}, got {result['standby_power_kw']}"

    # ---- 3. SiC 液冷 32C 冷却功耗计算 ----

    def test_calculate_cooling_power_sic_liquid_32c(self):
        """calculate_cooling_power(32, "SiC-liquid") → cooling_power_kw ~5.93, COP=5.0"""
        result = calculate_cooling_power(32, "SiC-liquid")

        assert result["cop"] == 5.0, f"Expected COP=5.0, got {result['cop']}"
        assert result["ambient_temp_c"] == 32
        assert result["cooling_type"] == "SiC-liquid"

        cpk = result["cooling_power_kw"]
        assert 4.5 <= cpk <= 7.5, f"Expected cooling_power_kw ~5.93 for SiC-liquid at 32C, got {cpk}"

        expected_standby = round(cpk * 0.15, 2)
        assert (
            result["standby_power_kw"] == expected_standby
        ), f"standby_power_kw should be {expected_standby}, got {result['standby_power_kw']}"

    # ---- 4. 热管理模式 vs 手动模式能量差异 ----

    def test_thermal_mode_vs_manual_mode_energy(self, client, auth_headers):
        """thermal 模式 totalAcUsable 应高于 manual 模式（32C 液冷功耗低于默认 18.124kW）"""
        design_output = {
            "container": {"ratedEnergyMWh": 5},
            "pcs": {"ratedPowerMW": 2.5},
            "containerQty": 10,
            "pcsQty": 10,
            "duration": 2,
        }

        # 热管理模式
        resp_thermal = _post(
            client,
            "/api/simulation/run",
            {
                "design_output": design_output,
                "survey_params": {
                    **SURVEY_PARAMS,
                    "auxPowerMode": "thermal",
                    "ambientTemp": 32,
                    "coolingType": "liquid",
                },
            },
            auth_headers,
        )
        thermal_data = _assert_success(resp_thermal)

        # 手动模式（默认 bessAuxRun=18.124kW）
        resp_manual = _post(
            client,
            "/api/simulation/run",
            {
                "design_output": design_output,
                "survey_params": {
                    **SURVEY_PARAMS,
                    "auxPowerMode": "manual",
                },
            },
            auth_headers,
        )
        manual_data = _assert_success(resp_manual)

        thermal_tac = thermal_data["totalAcUsable"]
        manual_tac = manual_data["totalAcUsable"]

        # 热管理模式在 32C 液冷下功耗约 8.47+3=11.47kW < 18.124kW
        # 所以 usable energy 应更高
        assert thermal_tac[0] != manual_tac[0], "Thermal and manual mode totalAcUsable should differ"
        assert (
            thermal_tac[0] > manual_tac[0]
        ), f"Thermal mode ({thermal_tac[0]}) should have higher usable energy than manual ({manual_tac[0]})"

    # ---- 5. 环境温度影响冷却功耗 ----

    def test_ambient_temp_affects_cooling(self, client, auth_headers):
        """ambientTemp=45 比 ambientTemp=25 产生更低的 totalAcUsable（更多冷却需求）"""
        design_output = {
            "container": {"ratedEnergyMWh": 5},
            "pcs": {"ratedPowerMW": 2.5},
            "containerQty": 10,
            "pcsQty": 10,
            "duration": 2,
        }

        # 低温（25C）
        resp_cool = _post(
            client,
            "/api/simulation/run",
            {
                "design_output": design_output,
                "survey_params": {
                    **SURVEY_PARAMS,
                    "auxPowerMode": "thermal",
                    "ambientTemp": 25,
                    "coolingType": "liquid",
                },
            },
            auth_headers,
        )
        cool_data = _assert_success(resp_cool)

        # 高温（45C）
        resp_hot = _post(
            client,
            "/api/simulation/run",
            {
                "design_output": design_output,
                "survey_params": {
                    **SURVEY_PARAMS,
                    "auxPowerMode": "thermal",
                    "ambientTemp": 45,
                    "coolingType": "liquid",
                },
            },
            auth_headers,
        )
        hot_data = _assert_success(resp_hot)

        cool_tac = cool_data["totalAcUsable"]
        hot_tac = hot_data["totalAcUsable"]

        # 高温需要更多冷却 → 更多辅机功耗 → 更低可用能量
        assert (
            cool_tac[0] > hot_tac[0]
        ), f"Cool ({cool_tac[0]}) should have higher usable energy than hot ({hot_tac[0]})"

    # ---- 6. 待机功耗 = 冷却功耗 * 0.15 ----

    def test_standby_power_calculation(self):
        """验证 standby_power_kw = cooling_power_kw * 0.15"""
        result = calculate_cooling_power(32, "liquid")

        cpk = result["cooling_power_kw"]
        expected_standby = round(cpk * 0.15, 2)

        assert (
            result["standby_power_kw"] == expected_standby
        ), f"standby_power_kw should be {expected_standby} (= {cpk} * 0.15), got {result['standby_power_kw']}"

        # 同时验证 FIXED_AUX_KW 常量存在且为合理值
        assert FIXED_AUX_KW == 3.0, f"FIXED_AUX_KW should be 3.0, got {FIXED_AUX_KW}"
