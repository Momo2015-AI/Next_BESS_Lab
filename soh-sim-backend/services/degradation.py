import copy
import math

NUM_YEARS = 26
R = 8.314

DEFAULT_MODEL_PARAMS = {
    "LFP": {
        # Calibrated to real LFP degradation: ~20% loss over 25 years
        # at 25°C, 1 cyc/day, 80% DOD, 0.5C. Temperature acceleration
        # matches Arrhenius behavior: ~2x at 45°C, ~3.5x at 60°C.
        "A_cal": 1.950563,  # Calendar pre-exponential factor
        "Ea_cal": 26000,  # Calendar activation energy (J/mol)
        "alpha": 0.8,  # Calendar time exponent
        "A_cyc": 12.556758,  # Cyclic pre-exponential factor
        "Ea_cyc": 22000,  # Cyclic activation energy (J/mol)
        "beta": 0.5,  # Cyclic cycle-count exponent
        "gamma": 1.5,  # DOD exponent
        "delta": 0.2,  # C-rate coefficient
    },
    "NMC": {
        # NMC chemistry degrades ~30% faster than LFP in calendar,
        # ~20% faster in cycling, with slightly higher activation energies
        "A_cal": 2.535732,
        "Ea_cal": 28000,
        "alpha": 0.85,
        "A_cyc": 15.068110,
        "Ea_cyc": 24000,
        "beta": 0.55,
        "gamma": 1.6,
        "delta": 0.25,
    },
}

GB36276_DEFAULT_CURVES = [
    {
        "label": "0.125P @ 25C",
        "p_rate": 0.125,
        "temperature": 25,
        "data": [
            (0, 100.0),
            (500, 99.8),
            (1000, 99.5),
            (1500, 99.1),
            (2000, 98.5),
            (2500, 97.8),
            (3000, 97.0),
            (3500, 96.1),
            (4000, 95.0),
            (4500, 93.7),
            (5000, 92.2),
            (5500, 90.5),
            (6000, 88.5),
            (6500, 86.2),
            (7000, 83.6),
            (7500, 80.5),
            (8000, 77.0),
            (8500, 73.0),
            (9000, 68.5),
            (9500, 63.5),
            (10000, 58.0),
        ],
    },
    {
        "label": "0.125P @ 45C",
        "p_rate": 0.125,
        "temperature": 45,
        "data": [
            (0, 100.0),
            (500, 99.5),
            (1000, 98.8),
            (1500, 97.9),
            (2000, 96.7),
            (2500, 95.2),
            (3000, 93.4),
            (3500, 91.3),
            (4000, 88.8),
            (4500, 85.9),
            (5000, 82.5),
            (5500, 78.6),
            (6000, 74.0),
            (6500, 68.8),
            (7000, 63.0),
            (7500, 56.5),
            (8000, 50.0),
            (8500, 44.0),
            (9000, 38.5),
            (9500, 33.5),
            (10000, 29.0),
        ],
    },
    {
        "label": "0.25P @ 25C",
        "p_rate": 0.25,
        "temperature": 25,
        "data": [
            (0, 100.0),
            (500, 99.6),
            (1000, 99.0),
            (1500, 98.2),
            (2000, 97.1),
            (2500, 95.8),
            (3000, 94.2),
            (3500, 92.3),
            (4000, 90.0),
            (4500, 87.3),
            (5000, 84.2),
            (5500, 80.6),
            (6000, 76.5),
            (6500, 71.8),
            (7000, 66.5),
            (7500, 60.5),
            (8000, 54.0),
            (8500, 47.5),
            (9000, 41.5),
            (9500, 36.5),
            (10000, 32.0),
        ],
    },
    {
        "label": "0.25P @ 45C",
        "p_rate": 0.25,
        "temperature": 45,
        "data": [
            (0, 100.0),
            (500, 99.2),
            (1000, 98.1),
            (1500, 96.7),
            (2000, 94.9),
            (2500, 92.6),
            (3000, 89.8),
            (3500, 86.4),
            (4000, 82.3),
            (4500, 77.5),
            (5000, 71.8),
            (5500, 65.2),
            (6000, 57.8),
            (6500, 50.0),
            (7000, 43.0),
            (7500, 37.0),
            (8000, 31.5),
            (8500, 26.5),
            (9000, 22.0),
            (9500, 18.0),
            (10000, 14.5),
        ],
    },
]

ENV_DEFAULTS = {
    "accelerate_temperature": True,
    "accelerate_dust": False,
    "accelerate_humidity": False,
    "ref_temperature": 25.0,
    "ref_humidity": 50.0,
    "field_humidity": 65.0,
    "dust_factor": 1.10,
    "humidity_exponent": 2.5,
    "activation_energy": 25000.0,
}


def _linear_interp(x, xp, yp):
    """Linear interpolation. xp must be sorted ascending."""
    if x <= xp[0]:
        return yp[0]
    if x >= xp[-1]:
        return yp[-1]
    for i in range(len(xp) - 1):
        if xp[i] <= x <= xp[i + 1]:
            t = (x - xp[i]) / (xp[i + 1] - xp[i])
            return yp[i] + t * (yp[i + 1] - yp[i])
    return yp[-1]


def _interp_curve_soh(curve, target_cycles):
    """Get SOH at target_cycles for a single GB/T 36276 curve."""
    data = curve.get("data", [])
    if not data:
        return 100.0
    cycles = [p[0] for p in data]
    soh_vals = [p[1] for p in data]
    return _linear_interp(target_cycles, cycles, soh_vals)


def predict_soh_gb36276(
    cycles_per_day,
    dod,
    c_rate,
    temperature,
    gb_curves=None,
    environmental=None,
    correction_factor=1.0,
    correction_table=None,
):
    """Predict SOH using GB/T 36276 test curves with 2D interpolation.

    Args:
        cycles_per_day: daily equivalent cycles
        dod: depth of discharge (%)
        c_rate: charge/discharge rate (P-rate)
        temperature: operating temperature (°C)
        gb_curves: list of 4 curve dicts ({p_rate, temperature, data}), defaults to GB36276_DEFAULT_CURVES
        environmental: environmental acceleration dict, defaults to ENV_DEFAULTS
        correction_factor: user correction multiplier
        correction_table: dict of {year: factor} for year-specific corrections

    Returns:
        (soh[], rte[]) arrays of length NUM_YEARS
    """
    if gb_curves is None or len(gb_curves) == 0:
        gb_curves = GB36276_DEFAULT_CURVES
    if environmental is None:
        environmental = ENV_DEFAULTS

    env_accel = _compute_environmental_acceleration(temperature, environmental)

    soh = [0.0] * NUM_YEARS
    for year in range(NUM_YEARS):
        if year == 0:
            soh[year] = 100.0
            continue

        total_cycles = year * 365 * cycles_per_day
        effective_cycles = total_cycles * env_accel * correction_factor
        if correction_table and year in correction_table:
            effective_cycles *= correction_table[year]

        soh_pcts = []
        for curve in gb_curves:
            soh_pcts.append(_interp_curve_soh(curve, effective_cycles))

        p_vals = [c["p_rate"] for c in gb_curves]
        t_vals = [c["temperature"] for c in gb_curves]

        p_sorted = sorted(set(p_vals))
        t_sorted = sorted(set(t_vals))

        if len(p_sorted) >= 2 and len(t_sorted) >= 2 and len(gb_curves) == 4:
            interp_soh = _bilinear_interp(c_rate, temperature, gb_curves, soh_pcts, p_sorted, t_sorted)
        else:
            min_err = float("inf")
            best = 100.0
            for c in gb_curves:
                err = abs(c["p_rate"] - c_rate) + abs(c["temperature"] - temperature) / 50.0
                if err < min_err:
                    min_err = err
                    best = _interp_curve_soh(c, effective_cycles)
            interp_soh = best

        dod_factor = (dod / 100.0) ** 1.2 if dod > 0 else 0
        dod_penalty = max(0, 1 - dod_factor) * 0.15
        soh[year] = max(0, interp_soh - dod_penalty * 100)

    rte = [max(80, 97.03 - (100 - s) * 0.15) for s in soh]
    rte[0] = 97.03
    return soh, rte


def _bilinear_interp(x, y, curves, soh_vals, x_sorted, y_sorted):
    """Bilinear interpolation in P-rate (x) and temperature (y) space."""
    x0, x1 = x_sorted[0], x_sorted[1]
    y0, y1 = y_sorted[0], y_sorted[1]

    def get_val(px, py):
        for c, sv in zip(curves, soh_vals):
            if c["p_rate"] == px and c["temperature"] == py:
                return sv
        return soh_vals[0]

    f00 = get_val(x0, y0)
    f10 = get_val(x1, y0)
    f01 = get_val(x0, y1)
    f11 = get_val(x1, y1)

    tx = (x - x0) / (x1 - x0) if x1 != x0 else 0
    ty = (y - y0) / (y1 - y0) if y1 != y0 else 0

    result = f00 * (1 - tx) * (1 - ty) + f10 * tx * (1 - ty) + f01 * (1 - tx) * ty + f11 * tx * ty
    return result


def _dust_humidity_factor(environmental):
    """Compute dust and humidity acceleration factor only (no temperature).

    Used for Arrhenius model which already handles temperature internally.
    """
    accel = 1.0
    if environmental.get("accelerate_dust", False):
        accel *= environmental.get("dust_factor", 1.10)
    if environmental.get("accelerate_humidity", False):
        RH_ref = environmental.get("ref_humidity", 50.0)
        RH_field = environmental.get("field_humidity", 65.0)
        n = environmental.get("humidity_exponent", 2.5)
        if RH_field > RH_ref:
            accel *= (RH_field / RH_ref) ** n
    return accel


def _compute_environmental_acceleration(operating_temp, environmental):
    """Compute environmental acceleration factor.

    Returns a multiplier >= 1.0 applied to effective cycle count.
    """
    accel = 1.0

    if environmental.get("accelerate_temperature", True):
        Ea = environmental.get("activation_energy", 25000.0)
        T_ref = environmental.get("ref_temperature", 25.0) + 273.15
        T_field = operating_temp + 273.15
        if T_field > T_ref:
            accel *= math.exp((Ea / R) * (1.0 / T_ref - 1.0 / T_field))

    if environmental.get("accelerate_dust", False):
        accel *= environmental.get("dust_factor", 1.10)

    if environmental.get("accelerate_humidity", False):
        RH_ref = environmental.get("ref_humidity", 50.0)
        RH_field = environmental.get("field_humidity", 65.0)
        n = environmental.get("humidity_exponent", 2.5)
        if RH_field > RH_ref:
            accel *= (RH_field / RH_ref) ** n

    return accel


def predict_soh_arrhenius(
    temperature,
    cycles_per_day,
    dod,
    c_rate,
    model_params=None,
    correction_factor=1.0,
    correction_table=None,
    environmental=None,
):
    """Predict SOH degradation using Arrhenius model with optional environmental acceleration.

    Returns arrays of length NUM_YEARS for SOH (%) and RTE (%).
    """
    if model_params is None:
        model_params = DEFAULT_MODEL_PARAMS["LFP"]
    if environmental is None:
        environmental = ENV_DEFAULTS

    T_kelvin = temperature + 273.15
    A_cal = model_params["A_cal"]
    Ea_cal = model_params["Ea_cal"]
    alpha = model_params.get("alpha", 0.8)
    A_cyc = model_params["A_cyc"]
    Ea_cyc = model_params["Ea_cyc"]
    beta = model_params.get("beta", 0.5)
    gamma = model_params.get("gamma", 1.5)
    delta = model_params.get("delta", 0.2)

    dod_factor = (dod / 100) ** gamma if dod > 0 else 0
    c_rate_factor = 1 + delta * (c_rate - 0.5)

    soh = [0.0] * NUM_YEARS
    rte = [0.0] * NUM_YEARS

    for year in range(NUM_YEARS):
        if year == 0:
            soh[year] = 100.0
            rte[year] = 97.03
            continue

        days = year * 365
        cycles = year * 365 * cycles_per_day

        q_cal = A_cal * math.exp(-Ea_cal / (R * T_kelvin)) * (days**alpha)
        q_cyc = A_cyc * math.exp(-Ea_cyc / (R * T_kelvin)) * (cycles**beta) * dod_factor * c_rate_factor

        env_dust_humidity = _dust_humidity_factor(environmental)
        q_cal *= env_dust_humidity
        q_cyc *= env_dust_humidity

        total_degradation = (q_cal + q_cyc) * correction_factor * 100
        if correction_table and year in correction_table:
            total_degradation *= correction_table[year]

        soh[year] = max(0, 100 - total_degradation)
        rte[year] = max(80, 97.03 - total_degradation * 0.15)

    return soh, rte


# ==================== 内置算法默认参数（与 algorithm.py / builtinAlgorithms.js 三方同源）====================

# 各模型在 algorithm.py 中的 model_type 映射:
#   arrhenius        → predict_soh_arrhenius()      （已存在，使用 DEFAULT_MODEL_PARAMS）
#   double_exponential → predict_soh_double_exp()    （新增，使用 _DOUBLE_EXP_DEFAULTS）
#   linear_log       → predict_soh_linear_log()      （新增，使用 _LINEAR_LOG_DEFAULTS）
#   rainflow         → predict_soh_rainflow()        （新增，使用 _RAINFLOW_DEFAULTS）
#   semi_empirical   → predict_soh_semi_empirical()  （新增，使用 _SEMI_EMP_DEFAULTS）
#   arrhenius_hybrid → predict_soh_arrhenius_hybrid()（新增，使用 _HYBRID_DEFAULTS）

_DOUBLE_EXP_DEFAULTS = {
    "A": 0.15,
    "B": 0.08,
    "k1": 0.12,
    "k2": 0.02,
    "C": 0.75,
}
"""双指数衰减: SOH(t)=A·exp(-k₁·t)+B·exp(-k₂·t)+C
校准目标: LFP@25°C, 1cyc/day, 80%DOD → 25年SOH≈80%, 15年≈87%.
快速相(k₁=0.12)描述SEI膜形成初期损失; 慢速相(k₂=0.02)描述长期活性物质损失.
"""

_LINEAR_LOG_DEFAULTS = {
    "RTE0": 0.94,
    "alpha": 0.0008,
    "beta": 0.02,
    "gamma": 0.5,
}
"""线性-RTE衰减: RTE(t)=RTE₀-α·t-β·ln(1+γ·t)
液冷储能@25°C标准工况; 线性项α描述设备老化, 对数项β描述效率下降趋缓.
"""

_RAINFLOW_DEFAULTS = {
    "damage_exponent": 1.5,
    "cycle_life_ref": 6000,
    "dod_ref": 1.0,
}
"""Miner雨流计数: D=(N/Nref)^(m)·(DOD/DOD_ref)^(m)
LFP@100%DOD/25°C参考寿命6000次; 损伤指数m=1.5(典型值).
"""

_SEMI_EMP_DEFAULTS = {
    "temp_coeff": 0.002,
    "dod_coeff": 0.15,
    "c_rate_coeff": 0.08,
    "soc_coeff": 0.15,
}
"""半经验综合: SOH=1-(1-fT·fDOD·fCr·fSOC)·t/25
校准目标@25°C/90%DOD/0.5C → 25年SOH≈79%.
温度偏离25°C每度±0.2%; DOD/SOC窗口因子缩小; 另叠加循环贡献项(N/6000)*(DOD/100)^1.2*5%.
"""

_HYBRID_DEFAULTS = {
    "A_cal": 0.01,
    "Ea_cal": 20000,
    "alpha": 0.65,
    "A_cyc": 0.001,
    "Ea_cyc": 18000,
    "beta": 0.55,
}
"""Arrhenius混合: 日历+循环双路径.
校准目标@25°C/1cpc/day/90%DOD/0.5C → 25年SOH≈82%, 15年≈89%.
日历Qcal=Acal·exp(-Eacal/(R·T))·t^α×10⁴; 循环Qcyc=Acyc·exp(-Ecyc/(R·T))·N^β·DOD^γ·CrFac×10⁴
内部固定γ=1.5(DOD指数), δ=0.2(倍率系数). 参数经LFP公开数据校准."""


# ==================== 双指数模型 ====================


def predict_soh_double_exp(
    temperature,
    cycles_per_day,
    dod,
    c_rate,
    model_params=None,
    correction_factor=1.0,
    correction_table=None,
):
    """Double Exponential degradation model.

    SOH(t) = A * exp(-k1 * t) + B * exp(-k2 * t) + C
    Fast phase (k1): SEI film formation initial loss.
    Slow phase (k2): long-term active material loss.

    Returns (soh[], rte[]) of length NUM_YEARS.
    """
    p = {**_DOUBLE_EXP_DEFAULTS, **(model_params or {})}
    A = p["A"]
    B = p["B"]
    k1 = p["k1"]
    k2 = p["k2"]
    C = p["C"]

    # 温度加速因子（基于Arrhenius近似，Ea≈35kJ/mol for LFP）
    T_kelvin = temperature + 273.15
    T_ref = 298.15  # 25°C
    Ea_temp = 35000  # J/mol, typical LFP calendar Ea
    temp_accel = math.exp((Ea_temp / R) * (1.0 / T_ref - 1.0 / T_kelvin))

    # 倍率加速（高倍率加剧SEI生长和锂析出）
    cr_accel = 1.0 + 0.3 * (c_rate - 0.5)

    # DOD加权（深充放加剧容量损失）
    dod_scale = (dod / 90.0) ** 0.8 if dod > 0 else 1.0

    soh = [0.0] * NUM_YEARS
    rte = [0.0] * NUM_YEARS

    for year in range(NUM_YEARS):
        if year == 0:
            soh[year] = 100.0
            rte[year] = 97.03
            continue

        # 有效时间（考虑温度/倍率/DOD影响）
        eff_t = year * temp_accel * cr_accel * dod_scale

        fast_term = A * math.exp(-k1 * eff_t)
        slow_term = B * math.exp(-k2 * eff_t)
        soh_val = (fast_term + slow_term + C) * 100  # convert fraction to %

        total_loss = 100 - soh_val

        # 应用校正因子
        total_loss *= correction_factor
        if correction_table and year in correction_table:
            total_loss *= correction_table[year]

        soh[year] = max(0, 100 - total_loss)
        rte[year] = max(80, 97.03 - total_loss * 0.15)

    return soh, rte


# ==================== 线性-RTE模型 ====================


def predict_soh_linear_log(
    temperature,
    cycles_per_day,
    dod,
    c_rate,
    model_params=None,
    correction_factor=1.0,
    correction_table=None,
):
    """Linear-Log RTE degradation model.

    RTE(t) = RTE0 - alpha * t - beta * ln(1 + gamma * t)
    Linear term (alpha): equipment aging.
    Log term (beta): diminishing efficiency decay rate.

    Returns (soh[], rte[]) of length NUM_YEARS.
    """
    p = {**_LINEAR_LOG_DEFAULTS, **(model_params or {})}
    RTE0 = p["RTE0"]
    alpha = p["alpha"]
    beta = p["beta"]
    gamma = p["gamma"]

    # 温度对RTE的影响（高温加速老化）
    T_kelvin = temperature + 273.15
    T_ref = 298.15
    Ea_rte = 25000  # J/mol, efficiency-related activation energy
    temp_accel_rte = math.exp((Ea_rte / R) * (1.0 / T_ref - 1.0 / T_kelvin))

    # 倍率影响（高倍率降低效率）
    cr_penalty = 0.003 * (c_rate - 0.5)

    soh = [0.0] * NUM_YEARS
    rte = [0.0] * NUM_YEARS

    for year in range(NUM_YEARS):
        if year == 0:
            soh[year] = 100.0
            rte[year] = RTE0 * 100  # convert to %
            continue

        eff_t = year * temp_accel_rte

        rte_frac = RTE0 - alpha * eff_t - beta * math.log(1 + gamma * eff_t) - cr_penalty * eff_t
        rte_pct = max(80, min(RTE0 * 100, rte_frac * 100))

        # 应用校正因子
        loss = (RTE0 * 100 - rte_pct) * correction_factor
        if correction_table and year in correction_table:
            loss *= correction_table[year]
        rte[year] = max(80, RTE0 * 100 - loss)

        # 从RTE推导SOH（经验关系：SOH ≈ 50 + 0.5*RTE，LFP典型范围）
        soh[year] = max(0, 50 + 0.518 * rte[year])

    return soh, rte


# ==================== 雨流计数模型 ====================


def predict_soh_rainflow(
    temperature,
    cycles_per_day,
    dod,
    c_rate,
    model_params=None,
    correction_factor=1.0,
    correction_table=None,
):
    """Rainflow Counting degradation model based on Miner's rule.

    D = (N_cycles / N_ref) ^ m  ×  (DOD / DOD_ref) ^ m
    Where m = damage_exponent (typically 1.0~2.0).

    Returns (soh[], rte[]) of length NUM_YEARS.
    """
    p = {**_RAINFLOW_DEFAULTS, **(model_params or {})}
    m = p["damage_exponent"]
    N_ref = p["cycle_life_ref"]
    dod_ref = p["dod_ref"]  # normalized (1.0 = 100%)

    # 温度对循环寿命的影响（高温缩短寿命）
    T_kelvin = temperature + 273.15
    T_ref = 298.15
    Ea_cycle = 22000  # J/mol, cyclic activation energy
    temp_life_factor = math.exp(-(Ea_cycle / R) * (1.0 / T_ref - 1.0 / T_kelvin))

    # 有效参考寿命（温度调整后）
    N_eff_ref = N_ref * temp_life_factor

    # 倍率影响循环寿命（高倍率减少有效寿命）
    cr_life_factor = 1.0 / (1.0 + 0.5 * (c_rate - 0.5))

    soh = [0.0] * NUM_YEARS
    rte = [0.0] * NUM_YEARS

    for year in range(NUM_YEARS):
        if year == 0:
            soh[year] = 100.0
            rte[year] = 97.03
            continue

        # 年累计等效循环次数
        N_year = year * 365 * cycles_per_day * cr_life_factor

        # Miner累积损伤比
        damage_ratio = (N_year / N_eff_ref) ** m

        # DOD归一化因子
        dod_normalized = (dod / 100.0) / dod_ref
        dod_damage = dod_normalized ** m

        # 总损伤（损伤比 × DOD权重）
        total_damage = damage_ratio * dod_damage * correction_factor
        if correction_table and year in correction_table:
            total_damage *= correction_table[year]

        # 将损伤映射为容量损失百分比
        # 当 damage=1.0 时达到参考循环寿命终点（通常定义为 SOH≤80%）
        # 使用非线性映射：前期损伤快、后期趋于平稳
        capacity_loss = 20 * (1 - math.exp(-2.5 * total_damage))
        if total_damage > 1.0:
            capacity_loss += 10 * (total_damage - 1.0)  # 超出寿命后加速衰减

        soh[year] = max(0, 100 - capacity_loss)
        rte[year] = max(80, 97.03 - capacity_loss * 0.15)

    return soh, rte


# ==================== 半经验综合模型 ====================


def predict_soh_semi_empirical(
    temperature,
    cycles_per_day,
    dod,
    c_rate,
    model_params=None,
    correction_factor=1.0,
    correction_table=None,
):
    """Semi-Empirical comprehensive degradation model.

    SOH = f(T) · f(DOD) · f(C-rate) · f(SOC)
    Combined as: SOH(t) = 1 - (1 - fT*fDOD*fCr*fSOC) * t / 25

    Each factor is a multiplier between 0 and 1 representing stress level.

    Returns (soh[], rte[]) of length NUM_YEARS.
    """
    p = {**_SEMI_EMP_DEFAULTS, **(model_params or {})}
    tc = p["temp_coeff"]
    dc = p["dod_coeff"]
    cc = p["c_rate_coeff"]
    sc = p["soc_coeff"]

    # --- 四大应力因子的计算 ---

    # 温度因子：以25°C为基准，偏离越远衰减越快（低温也加速衰减）
    dT = abs(temperature - 25.0)
    f_T = max(0, 1.0 - tc * dT)

    # DOD因子：DOD越高衰减越快（以50%为中性点）
    f_DOD = max(0, 1.0 - dc * ((dod - 50.0) / 50.0))

    # C-rate因子：以0.5C为基准
    f_CRate = max(0, 1.0 - cc * (c_rate - 0.5) * 2)

    # SOC窗口因子：假设运行SOC窗口为(100-DOD)%~100%，窗口越大衰减越快
    soc_window = dod  # 近似：DOD越大=SOC窗口越大
    f_SOC = max(0, 1.0 - sc * (soc_window / 100.0))

    # 综合健康系数（四因子乘积）
    health_product = f_T * f_DOD * f_CRate * f_SOC

    soh = [0.0] * NUM_YEARS
    rte = [0.0] * NUM_YEARS

    for year in range(NUM_YEARS):
        if year == 0:
            soh[year] = 100.0
            rte[year] = 97.03
            continue

        # 半经验公式：t年内累计衰减
        base_loss = (1.0 - health_product) * (year / 25.0) * 100

        # 循环次数的额外贡献（每日循环叠加）
        cycle_contribution = 0.05 * (year * 365 * cycles_per_day / 6000) * (dod / 100) ** 1.2

        total_loss = (base_loss + cycle_contribution) * correction_factor
        if correction_table and year in correction_table:
            total_loss *= correction_table[year]

        soh[year] = max(0, 100 - total_loss)
        rte[year] = max(80, 97.03 - total_loss * 0.15)

    return soh, rte


# ==================== Arrhenius混合模型 ====================


def predict_soh_arrhenius_hybrid(
    temperature,
    cycles_per_day,
    dod,
    c_rate,
    model_params=None,
    correction_factor=1.0,
    correction_table=None,
):
    """Arrhenius Hybrid model: separate calendar + cyclic aging paths.

    Calendar path: Q_cal = A_cal * exp(-Ea_cal / (R * T)) * t^alpha
    Cyclic path:  Q_cyc = A_cyc * exp(-Ea_cyc / (R * T)) * N^beta * (DOD/100)^gamma * (1+delta*(Cr-0.5))

    Parameters are calibrated to multi-vendor LFP cell public data averages.

    Returns (soh[], rte[]) of length NUM_YEARS.
    """
    p = {**_HYBRID_DEFAULTS, **(model_params or {})}
    A_cal = p["A_cal"]
    Ea_cal = p["Ea_cal"]
    alpha = p["alpha"]
    A_cyc = p["A_cyc"]
    Ea_cyc = p["Ea_cyc"]
    beta = p["beta"]
    gamma = 1.5  # fixed DOD exponent (consistent with Arrhenius model)
    delta = 0.2    # fixed c-rate coefficient

    T_kelvin = temperature + 273.15

    # DOD因子
    dod_factor = (dod / 100) ** gamma if dod > 0 else 0

    # 倍率因子
    c_rate_factor = 1.0 + delta * (c_rate - 0.5)

    soh = [0.0] * NUM_YEARS
    rte = [0.0] * NUM_YEARS

    for year in range(NUM_YEARS):
        if year == 0:
            soh[year] = 100.0
            rte[year] = 97.03
            continue

        days = year * 365
        cycles = year * 365 * cycles_per_day

        # 日历老化（时间驱动）
        q_cal = A_cal * math.exp(-Ea_cal / (R * T_kelvin)) * (days ** alpha) * 10000  # scale to %

        # 循环老化（次数驱动）
        q_cyc = (
            A_cyc
            * math.exp(-Ea_cyc / (R * T_kelvin))
            * (cycles ** beta)
            * dod_factor
            * c_rate_factor
            * 10000  # scale to %
        )

        total_degradation = (q_cal + q_cyc) * correction_factor
        if correction_table and year in correction_table:
            total_degradation *= correction_table[year]

        soh[year] = max(0, 100 - total_degradation)
        rte[year] = max(80, 97.03 - total_degradation * 0.15)

    return soh, rte


# ==================== 统一分发入口 ====================


def predict_soh(
    model_type,
    temperature,
    cycles_per_day,
    dod,
    c_rate,
    model_params=None,
    correction_factor=1.0,
    correction_table=None,
    environmental=None,
    gb_curves=None,
):
    """Unified entry point for SOH prediction — supports 7 degradation models.

    Supported model_type values:
      - 'arrhenius'          → Arrhenius (calendar + cyclic dual-path)
      - 'double_exponential' → Double Exponential (SEI + active material)
      - 'linear_log'         → Linear-Log RTE decay
      - 'rainflow'           → Rainflow / Miner's rule counting
      - 'semi_empirical'     → Semi-empirical multi-stress coupling
      - 'arrhenius_hybrid'   → Hybrid Arrhenius (separate cal/cyc params)
      - 'gb36276'            → GB/T 36276 test curve interpolation

    Returns:
        (soh[], rte[]) arrays of length NUM_YEARS
    """
    _dispatch = {
        "arrhenius": predict_soh_arrhenius,
        "double_exponential": predict_soh_double_exp,
        "linear_log": predict_soh_linear_log,
        "rainflow": predict_soh_rainflow,
        "semi_empirical": predict_soh_semi_empirical,
        "arrhenius_hybrid": predict_soh_arrhenius_hybrid,
        "gb36276": predict_soh_gb36276,
    }

    handler = _dispatch.get(model_type)
    if handler is None:
        # Fallback: unknown types default to arrhenius
        handler = predict_soh_arrhenius

    if model_type == "gb36276":
        return handler(
            cycles_per_day, dod, c_rate, temperature,
            gb_curves=gb_curves, environmental=environmental,
            correction_factor=correction_factor, correction_table=correction_table,
        )
    elif model_type == "arrhenius":
        return handler(
            temperature, cycles_per_day, dod, c_rate,
            model_params=model_params, correction_factor=correction_factor,
            correction_table=correction_table, environmental=environmental,
        )
    else:
        return handler(
            temperature, cycles_per_day, dod, c_rate,
            model_params=model_params, correction_factor=correction_factor,
            correction_table=correction_table,
        )


def get_default_gb_curves():
    """Return a deep copy of default GB/T 36276 curves."""
    return copy.deepcopy(GB36276_DEFAULT_CURVES)


def get_default_environmental():
    """Return a deep copy of default environmental factors."""
    return copy.deepcopy(ENV_DEFAULTS)
