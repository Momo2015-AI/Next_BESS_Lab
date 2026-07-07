# ===================== 高压接入 =====================


def design_hv_interconnection_service(data):
    """高压接入设计"""
    total_power_mw = float(data.get("total_power_mw", 100))
    poc_voltage = float(data.get("poc_voltage_kv", 33))
    s_sc = float(data.get("short_circuit_capacity_mva", 500))

    trans_capacity = total_power_mw * 1.1
    trans_count = max(1, math.ceil(trans_capacity / 100))
    capacity_each = trans_capacity / trans_count

    if poc_voltage <= 33:
        ratio = f"{int(poc_voltage)}/0.69"
    elif poc_voltage <= 132:
        ratio = f"{int(poc_voltage)}/33/0.69"
    else:
        ratio = f"{int(poc_voltage)}/132/33/0.69"

    i_sc = s_sc / (1.732 * poc_voltage)
    breaker_rating = math.ceil(i_sc * 1.2 / 5) * 5
    i_rated = trans_capacity * 1000 / (1.732 * poc_voltage)
    cable_section = math.ceil(i_rated / 1.5 / 50) * 50

    protections = [
        {"name": "过流保护", "type": "50/51"},
        {"name": "距离保护", "type": "21"},
        {"name": "差动保护", "type": "87"},
        {"name": "频率保护", "type": "81"},
        {"name": "电压保护", "type": "27/59"},
    ]

    return {
        "poc_voltage_kv": poc_voltage,
        "poc_type": data.get("poc_type", "substation"),
        "short_circuit_capacity_mva": s_sc,
        "x_r_ratio": 10.0,
        "transformer_count": trans_count,
        "transformer_capacity_mva": round(capacity_each, 1),
        "transformer_ratio": ratio,
        "transformer_vector_group": "Dyn11",
        "transformer_impedance": 10.5,
        "mv_switchgear_count": trans_count * 2,
        "mv_switchgear_type": "GIS",
        "mv_breaker_rating_ka": float(breaker_rating),
        "protection_scheme": protections,
        "relay_count": len(protections) * trans_count,
        "relay_type": "微机保护",
        "single_line_diagram": {
            "voltage_levels": ratio.split("/"),
            "transformer_count": trans_count,
            "breaker_rating_ka": breaker_rating,
            "cable_cross_section_mm2": cable_section,
        },
    }


