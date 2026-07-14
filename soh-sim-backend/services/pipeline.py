"""
完整计算流水线

新架构：核心已迁移到 services/simulation/engine.py (SimulationEngine)
此文件保留为向后兼容代理，所有原有函数保持不变。
"""

# 向后兼容代理 — 从新引擎模块重导出
from services.simulation.engine import SimulationEngine, run_simulation  # noqa: F401

from services.degradation import NUM_YEARS, predict_soh
from services.efficiency import FACTOR_DEFAULTS, calculate_efficiency_chain, calculate_efficiency_curves


def calculate_energy_accounting(params, soh, rte, dod, aug_qty, efficiency_factors=None):
    """Calculate 25-year energy accounting matrix.

    If efficiency_factors is provided (10-factor chain), RTE is computed from
    the chain at each year based on SOH. Otherwise falls back to the single
    acEfficiency parameter for backward compatibility.

    Returns dict with 26-element arrays for all accounting metrics.
    """
    N = NUM_YEARS
    rated_energy = params.get("ratedEnergy", 5)
    init_container_qty = params.get("initContainerQty", 62)
    init_pcs_qty = params.get("initPcsQty", 1)
    duration = params.get("duration", 2)
    cycles_per_day = params.get("cyclesPerDay", 1)
    ac_efficiency = params.get("acEfficiency", 97.03) / 100
    # 辅耗计算模式: "manual"（默认，向后兼容）或 "thermal"（环境温度驱动）
    aux_mode = params.get("auxPowerMode", "manual")
    if aux_mode == "thermal":
        from services.epc.thermal import calculate_cooling_power, FIXED_AUX_KW

        ambient_temp = params.get("ambientTemp", params.get("temperature", 25))
        cooling_type = params.get("coolingType", "liquid")
        cp = calculate_cooling_power(ambient_temp, cooling_type)
        bess_aux_run = cp["cooling_power_kw"] + FIXED_AUX_KW
        bess_aux_standby = cp["standby_power_kw"]
    else:
        bess_aux_run = params.get("bessAuxRun", 18.124)
        bess_aux_standby = params.get("bessAuxStandby", 3.5)

    pcs_aux_run = params.get("pcsAuxRun", 6.5)
    pcs_aux_standby = params.get("pcsAuxStandby", 1.0)
    required_energy = params.get("requiredEnergy", 240)

    run_hours = duration * cycles_per_day
    standby_hours = max(0, 24 - run_hours)

    daily_container_aux_per_unit = (bess_aux_run * run_hours + bess_aux_standby * standby_hours) / 1000
    daily_pcs_aux_per_unit = (pcs_aux_run * run_hours + pcs_aux_standby * standby_hours) / 1000
    # 防止 cycles_per_day=0 导致除零（0 循环时辅助损耗按 0 处理）
    if cycles_per_day > 0:
        cycle_container_aux_per_unit = daily_container_aux_per_unit / cycles_per_day
        cycle_pcs_aux_per_unit = daily_pcs_aux_per_unit / cycles_per_day
    else:
        cycle_container_aux_per_unit = 0.0
        cycle_pcs_aux_per_unit = 0.0

    init_gross = [0.0] * N
    init_aux = [0.0] * N
    init_ac_usable = [0.0] * N
    aug_gross = [0.0] * N
    aug_aux = [0.0] * N
    aug_ac_usable = [0.0] * N
    aug_accum_qty = [0.0] * N
    total_ac_usable = [0.0] * N
    meets_req = [False] * N

    accum = 0
    for i in range(N):
        accum += int(aug_qty[i]) if (i < len(aug_qty) and aug_qty[i] is not None) else 0
        aug_accum_qty[i] = accum

        if i < len(soh) and soh[i] is not None:
            try:
                raw = float(soh[i])
                c_soh = raw / 100.0 if raw > 1.0 else raw
            except (ValueError, TypeError):
                c_soh = 1.0
        else:
            raw_last = float(soh[-1]) if (soh and soh[-1] is not None) else 100.0
            c_soh = raw_last / 100.0 if raw_last > 1.0 else raw_last

        if i < len(dod) and dod[i] is not None:
            try:
                raw_dod = float(dod[i])
                c_dod = raw_dod / 100.0 if raw_dod > 1.0 else raw_dod
            except (ValueError, TypeError):
                c_dod = 1.0
        else:
            raw_dod_last = float(dod[-1]) if (dod and dod[-1] is not None) else 1.0
            c_dod = raw_dod_last / 100.0 if raw_dod_last > 1.0 else raw_dod_last

        if efficiency_factors is not None:
            soh_pct = c_soh * 100.0
            chain = calculate_efficiency_chain(efficiency_factors, soh_pct)
            cycle_rte = chain["rte"]
        else:
            if i < len(rte) and rte[i] is not None:
                try:
                    raw_rte = float(rte[i])
                    c_rte = raw_rte / 100.0 if raw_rte > 1.0 else raw_rte
                except (ValueError, TypeError):
                    c_rte = 0.9703
            else:
                raw_rte_last = float(rte[-1]) if (rte and rte[-1] is not None) else 97.03
                c_rte = raw_rte_last / 100.0 if raw_rte_last > 1.0 else raw_rte_last
            cycle_rte = c_rte * ac_efficiency

        init_gross[i] = rated_energy * init_container_qty * c_dod * cycle_rte * c_soh
        init_aux[i] = init_container_qty * cycle_container_aux_per_unit + init_pcs_qty * cycle_pcs_aux_per_unit
        init_ac_usable[i] = max(0, init_gross[i] - init_aux[i])

        total_aug_ac = 0.0
        total_aug_aux = 0.0
        for k in range(i + 1):
            qty_k = int(aug_qty[k]) if (k < len(aug_qty) and aug_qty[k] is not None) else 0
            if qty_k > 0:
                age = i - k
                try:
                    raw_asset_soh = float(soh[min(age, N - 1)])
                    asset_soh = raw_asset_soh / 100.0 if raw_asset_soh > 1.0 else raw_asset_soh
                except (ValueError, TypeError, IndexError):
                    asset_soh = 1.0
                if efficiency_factors is not None:
                    asset_soh_pct = asset_soh * 100.0
                    asset_chain = calculate_efficiency_chain(efficiency_factors, asset_soh_pct)
                    asset_cycle_rte = asset_chain["rte"]
                else:
                    asset_cycle_rte = c_rte * ac_efficiency
                asset_gross = rated_energy * qty_k * c_dod * asset_cycle_rte * asset_soh
                asset_aux = qty_k * cycle_container_aux_per_unit
                total_aug_ac += max(0, asset_gross - asset_aux)
                total_aug_aux += asset_aux

        aug_gross[i] = total_aug_ac + total_aug_aux
        aug_aux[i] = total_aug_aux
        aug_ac_usable[i] = total_aug_ac
        total_ac_usable[i] = init_ac_usable[i] + total_aug_ac
        meets_req[i] = total_ac_usable[i] >= required_energy

    return {
        "initGross": init_gross,
        "initAux": init_aux,
        "initAcUsable": init_ac_usable,
        "augGross": aug_gross,
        "augAux": aug_aux,
        "augAcUsable": aug_ac_usable,
        "augAccumQty": aug_accum_qty,
        "totalAcUsable": total_ac_usable,
        "meetsReq": meets_req,
    }


def calculate_financial_metrics(total_ac_usable, financial_params=None):
    """Calculate financial metrics based on energy output.

    Delegates to services/financial.py:calculate_full_financial for full 25-year cashflow.
    Returns backward-compatible metrics dict.
    """
    from services.financial.calculator import calculate_full_financial as _calc_full

    result = _calc_full(total_ac_usable, financial_params)
    metrics = result["metrics"]

    return {
        "npv": metrics["npv"],
        "irr": metrics["projectIrr"],
        "lcoe": metrics["lcos"],
        "lcos": metrics["lcos"],
        "roi": metrics["roi"],
        "dscr": metrics["dscr"]["avg"],
        "payback": metrics["payback"],
    }


def calculate_full_pipeline(system_params, degradation=None, algorithm=None, financial_params=None):
    """Execute the full calculation pipeline.

    Args:
        system_params: dict with ratedEnergy, initContainerQty, etc.
        degradation: optional dict with soh[], rte[], dod[], augQty[]
        algorithm: optional dict with model, correctionFactor, correctionTable
        financial_params: optional dict with capex, opex, revenue

    Returns:
        dict with years, soh, rte, dod, energy accounting fields, financial fields
    """
    if degradation is None:
        degradation = {}

    algorithm = algorithm or {}
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
        soh, rte = predict_soh(
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

    if degradation.get("dod") and len(degradation["dod"]) == NUM_YEARS:
        dod = list(degradation["dod"])
    else:
        dod = [dod_input] * NUM_YEARS

    if degradation.get("augQty") and len(degradation["augQty"]) == NUM_YEARS:
        aug_qty = list(degradation["augQty"])
    else:
        aug_qty = [0] * NUM_YEARS

    efficiency_factors = system_params.get("efficiencyFactors")
    if efficiency_factors is None and "efficiencyFactors" not in system_params:
        efficiency_factors = FACTOR_DEFAULTS

    energy_results = calculate_energy_accounting(system_params, soh, rte, dod, aug_qty, efficiency_factors)
    financial_results = calculate_financial_metrics(energy_results["totalAcUsable"], financial_params)

    if efficiency_factors is not None:
        eff_curves = calculate_efficiency_curves(efficiency_factors, soh, NUM_YEARS)
        rte = eff_curves["rte"]
        efficiency_detail = calculate_efficiency_chain(efficiency_factors, soh[0])
    else:
        eff_curves = None
        efficiency_detail = None

    return {
        "years": list(range(NUM_YEARS)),
        "soh": soh,
        "rte": rte,
        "dod": dod,
        "efficiencyCurves": eff_curves,
        "efficiencyDetail": efficiency_detail,
        **energy_results,
        "financial": financial_results,
    }


def validate_pipeline_input(data):
    """Validate pipeline input parameters. Returns list of field errors."""
    errors = []
    required_fields = ["ratedEnergy", "initContainerQty", "duration", "temperature", "requiredEnergy"]

    system_params = data.get("systemParams", {})
    for field in required_fields:
        if field not in system_params or system_params[field] is None:
            errors.append({"field": field, "error": f"{field} is required"})
            continue

    if system_params.get("ratedEnergy", 0) <= 0:
        errors.append(
            {
                "field": "ratedEnergy",
                "error": "must be positive",
                "value": system_params.get("ratedEnergy"),
                "constraint": "> 0",
            }
        )
    if system_params.get("initContainerQty", 0) <= 0:
        errors.append(
            {
                "field": "initContainerQty",
                "error": "must be positive",
                "value": system_params.get("initContainerQty"),
                "constraint": "> 0",
            }
        )
    if system_params.get("duration", 0) <= 0:
        errors.append(
            {
                "field": "duration",
                "error": "must be positive",
                "value": system_params.get("duration"),
                "constraint": "> 0",
            }
        )
    temp = system_params.get("temperature", 25)
    if temp < -20 or temp > 60:
        errors.append(
            {
                "field": "temperature",
                "error": "must be between -20 and 60",
                "value": temp,
                "constraint": "-20 <= temp <= 60",
            }
        )

    return errors
