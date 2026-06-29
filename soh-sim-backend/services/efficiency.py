FACTOR_DEFAULTS = [
    {"id": 1,  "name": "HV Cable (PoC - MV/HV Transformer)",   "eta_c": 0.998, "eta_d": 0.998, "degrade": False, "degrade_rate": 0.0},
    {"id": 2,  "name": "MV/HV Transformer",                    "eta_c": 0.992, "eta_d": 0.992, "degrade": False, "degrade_rate": 0.0},
    {"id": 3,  "name": "MV Cable (Transformer - LV/MV)",       "eta_c": 0.998, "eta_d": 0.998, "degrade": False, "degrade_rate": 0.0},
    {"id": 4,  "name": "LV/MV Transformer",                    "eta_c": 0.992, "eta_d": 0.992, "degrade": False, "degrade_rate": 0.0},
    {"id": 5,  "name": "LV Cable (Transformer - PCS)",         "eta_c": 0.998, "eta_d": 0.998, "degrade": False, "degrade_rate": 0.0},
    {"id": 6,  "name": "PCS",                                  "eta_c": 0.986, "eta_d": 0.986, "degrade": False, "degrade_rate": 0.0},
    {"id": 7,  "name": "DC Cable (PCS - DC Panel)",            "eta_c": 0.998, "eta_d": 0.998, "degrade": False, "degrade_rate": 0.0},
    {"id": 8,  "name": "DC Cable (DC Panel - Battery Pack)",   "eta_c": 0.998, "eta_d": 0.998, "degrade": False, "degrade_rate": 0.0},
    {"id": 9,  "name": "DC/DC Converter",                      "eta_c": 0.990, "eta_d": 0.990, "degrade": False, "degrade_rate": 0.0},
    {"id": 10, "name": "Cell",                                 "eta_c": 0.970, "eta_d": 0.980, "degrade": True,  "degrade_rate": 0.05},
]


def calculate_efficiency_chain(factors, soh_pct):
    """Calculate charge/discharge total efficiency and RTE for a given SOH.

    Args:
        factors: list of dicts with eta_c, eta_d, degrade, degrade_rate
        soh_pct: SOH as percentage (0-100)

    Returns:
        dict with eta_charge, eta_discharge, rte, and per-factor breakdown
    """
    eta_c_total = 1.0
    eta_d_total = 1.0
    c_breakdown = []
    d_breakdown = []

    soh_ratio = soh_pct / 100.0

    for f in factors:
        if f["degrade"]:
            degradation = 1 - f["degrade_rate"] * (1 - soh_ratio)
            eta_c = max(0.0, min(1.0, f["eta_c"] * degradation))
            eta_d = max(0.0, min(1.0, f["eta_d"] * degradation))
        else:
            eta_c = f["eta_c"]
            eta_d = f["eta_d"]

        eta_c_total *= eta_c
        eta_d_total *= eta_d
        c_breakdown.append({"id": f["id"], "name": f["name"], "eta": round(eta_c, 6)})
        d_breakdown.append({"id": f["id"], "name": f["name"], "eta": round(eta_d, 6)})

    rte = eta_c_total * eta_d_total

    return {
        "etaCharge": round(eta_c_total, 6),
        "etaDischarge": round(eta_d_total, 6),
        "rte": round(rte, 6),
        "chargeBreakdown": c_breakdown,
        "dischargeBreakdown": d_breakdown,
    }


def calculate_efficiency_curves(factors, soh_curve, num_years=26):
    """Calculate efficiency curves for a full SOH time series.

    Args:
        factors: efficiency factor configurations
        soh_curve: list of SOH values (percentage, length num_years)
        num_years: number of years

    Returns:
        dict with eta_charge[], eta_discharge[], rte[], and soh[] arrays
    """
    n = min(num_years, len(soh_curve))
    eta_c_curve = [0.0] * n
    eta_d_curve = [0.0] * n
    rte_curve = [0.0] * n

    for i in range(n):
        result = calculate_efficiency_chain(factors, soh_curve[i])
        eta_c_curve[i] = result["etaCharge"]
        eta_d_curve[i] = result["etaDischarge"]
        rte_curve[i] = result["rte"]

    return {
        "etaCharge": eta_c_curve,
        "etaDischarge": eta_d_curve,
        "rte": rte_curve,
        "soh": list(soh_curve[:n]),
    }
