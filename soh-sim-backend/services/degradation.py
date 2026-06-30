import math
import copy

NUM_YEARS = 26
R = 8.314

DEFAULT_MODEL_PARAMS = {
    "LFP": {
        "A_cal": 0.02, "Ea_cal": 20000, "alpha": 0.8,
        "A_cyc": 0.001, "Ea_cyc": 15000, "beta": 0.5, "gamma": 1.5, "delta": 0.2,
    },
    "NMC": {
        "A_cal": 0.03, "Ea_cal": 22000, "alpha": 0.85,
        "A_cyc": 0.0015, "Ea_cyc": 18000, "beta": 0.55, "gamma": 1.6, "delta": 0.25,
    },
}

GB36276_DEFAULT_CURVES = [
    {
        "label": "0.125P @ 25C",
        "p_rate": 0.125,
        "temperature": 25,
        "data": [
            (0, 100.0), (500, 99.8), (1000, 99.5), (1500, 99.1), (2000, 98.5),
            (2500, 97.8), (3000, 97.0), (3500, 96.1), (4000, 95.0), (4500, 93.7),
            (5000, 92.2), (5500, 90.5), (6000, 88.5), (6500, 86.2), (7000, 83.6),
            (7500, 80.5), (8000, 77.0), (8500, 73.0), (9000, 68.5), (9500, 63.5),
            (10000, 58.0),
        ],
    },
    {
        "label": "0.125P @ 45C",
        "p_rate": 0.125,
        "temperature": 45,
        "data": [
            (0, 100.0), (500, 99.5), (1000, 98.8), (1500, 97.9), (2000, 96.7),
            (2500, 95.2), (3000, 93.4), (3500, 91.3), (4000, 88.8), (4500, 85.9),
            (5000, 82.5), (5500, 78.6), (6000, 74.0), (6500, 68.8), (7000, 63.0),
            (7500, 56.5), (8000, 50.0), (8500, 44.0), (9000, 38.5), (9500, 33.5),
            (10000, 29.0),
        ],
    },
    {
        "label": "0.25P @ 25C",
        "p_rate": 0.25,
        "temperature": 25,
        "data": [
            (0, 100.0), (500, 99.6), (1000, 99.0), (1500, 98.2), (2000, 97.1),
            (2500, 95.8), (3000, 94.2), (3500, 92.3), (4000, 90.0), (4500, 87.3),
            (5000, 84.2), (5500, 80.6), (6000, 76.5), (6500, 71.8), (7000, 66.5),
            (7500, 60.5), (8000, 54.0), (8500, 47.5), (9000, 41.5), (9500, 36.5),
            (10000, 32.0),
        ],
    },
    {
        "label": "0.25P @ 45C",
        "p_rate": 0.25,
        "temperature": 45,
        "data": [
            (0, 100.0), (500, 99.2), (1000, 98.1), (1500, 96.7), (2000, 94.9),
            (2500, 92.6), (3000, 89.8), (3500, 86.4), (4000, 82.3), (4500, 77.5),
            (5000, 71.8), (5500, 65.2), (6000, 57.8), (6500, 50.0), (7000, 43.0),
            (7500, 37.0), (8000, 31.5), (8500, 26.5), (9000, 22.0), (9500, 18.0),
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


def predict_soh_gb36276(cycles_per_day, dod, c_rate, temperature, gb_curves=None,
                          environmental=None, correction_factor=1.0, correction_table=None):
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

    result = (f00 * (1 - tx) * (1 - ty)
              + f10 * tx * (1 - ty)
              + f01 * (1 - tx) * ty
              + f11 * tx * ty)
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


def predict_soh_arrhenius(temperature, cycles_per_day, dod, c_rate, model_params=None,
                           correction_factor=1.0, correction_table=None, environmental=None):
    """Predict SOH degradation using Arrhenius model with optional environmental acceleration.

    Returns arrays of length NUM_YEARS for SOH (%) and RTE (%).
    """
    if model_params is None:
        model_params = DEFAULT_MODEL_PARAMS["LFP"]
    if environmental is None:
        environmental = ENV_DEFAULTS

    T_kelvin = temperature + 273.15
    T_ref = environmental.get("ref_temperature", 25.0) + 273.15
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

    env_accel = _compute_environmental_acceleration(temperature, environmental)

    soh = [0.0] * NUM_YEARS
    rte = [0.0] * NUM_YEARS

    for year in range(NUM_YEARS):
        if year == 0:
            soh[year] = 100.0
            rte[year] = 97.03
            continue

        days = year * 365
        cycles = year * 365 * cycles_per_day

        q_cal = A_cal * math.exp(-Ea_cal / (R * T_kelvin)) * (days ** alpha)
        q_cyc = A_cyc * math.exp(-Ea_cyc / (R * T_kelvin)) * (cycles ** beta) * dod_factor * c_rate_factor

        env_dust_humidity = _dust_humidity_factor(environmental)
        q_cal *= env_dust_humidity
        q_cyc *= env_dust_humidity

        total_degradation = (q_cal + q_cyc) * correction_factor * 100
        if correction_table and year in correction_table:
            total_degradation *= correction_table[year]

        soh[year] = max(0, 100 - total_degradation)
        rte[year] = max(80, 97.03 - total_degradation * 0.15)

    return soh, rte


def predict_soh(model_type, temperature, cycles_per_day, dod, c_rate,
                model_params=None, correction_factor=1.0, correction_table=None,
                environmental=None, gb_curves=None):
    """Unified entry point for SOH prediction.

    Args:
        model_type: 'arrhenius' or 'gb36276'
        temperature: operating temperature (°C)
        cycles_per_day: daily equivalent cycles
        dod: depth of discharge (%)
        c_rate: charge/discharge rate (P-rate)
        model_params: Arrhenius params (for arrhenius mode)
        correction_factor: user correction multiplier
        correction_table: year-specific corrections
        environmental: environmental acceleration dict
        gb_curves: GB/T 36276 test curves (for gb36276 mode)

    Returns:
        (soh[], rte[]) arrays of length NUM_YEARS
    """
    if model_type == "gb36276":
        return predict_soh_gb36276(cycles_per_day, dod, c_rate, temperature,
                                    gb_curves, environmental, correction_factor, correction_table)
    else:
        return predict_soh_arrhenius(temperature, cycles_per_day, dod, c_rate,
                                      model_params, correction_factor, correction_table, environmental)


def get_default_gb_curves():
    """Return a deep copy of default GB/T 36276 curves."""
    return copy.deepcopy(GB36276_DEFAULT_CURVES)


def get_default_environmental():
    """Return a deep copy of default environmental factors."""
    return copy.deepcopy(ENV_DEFAULTS)
