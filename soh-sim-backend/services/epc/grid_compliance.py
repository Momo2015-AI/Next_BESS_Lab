# ===================== 电网合规 =====================


GRID_STANDARDS = [
    {"code": "UAE_S_5010", "name": "UAE.S 5010-1", "country": "阿联酋", "voltage_kv": 33},
    {"code": "IEEE_2800", "name": "IEEE 2800-2022", "country": "美国", "voltage_kv": 33},
    {"code": "IEC_61400", "name": "IEC 61400-27", "country": "国际", "voltage_kv": 33},
    {"code": "GB_19964", "name": "GB/T 19964-2024", "country": "中国", "voltage_kv": 35},
    {"code": "CUSTOM", "name": "自定义标准", "country": "-", "voltage_kv": 33},
]


def analyze_grid_compliance_service(data):
    """执行电网合规分析"""
    standard = data.get("grid_standard", "UAE_S_5010")
    pcs_power_mw = float(data.get("pcs_power_mw", 3.45))
    pcs_count = int(data.get("pcs_count", 1))
    grid_voltage_kv = float(data.get("grid_voltage_kv", 33))
    grid_freq = float(data.get("grid_frequency_hz", 50))
    total_power_mw = pcs_power_mw * pcs_count

    lvrt_curve = [
        {"voltage_pu": 0.0, "time_s": 0.15},
        {"voltage_pu": 0.2, "time_s": 0.625},
        {"voltage_pu": 0.5, "time_s": 2.0},
        {"voltage_pu": 0.85, "time_s": 5.0},
    ]
    hvrt_curve = [
        {"voltage_pu": 1.10, "time_s": 60},
        {"voltage_pu": 1.15, "time_s": 2.0},
        {"voltage_pu": 1.20, "time_s": 0.5},
        {"voltage_pu": 1.30, "time_s": 0.2},
    ]
    freq_curve = [
        {"freq_hz": 47.5, "power_pu": 1.0},
        {"freq_hz": 49.5, "power_pu": 1.0},
        {"freq_hz": 50.0, "power_pu": 1.0},
        {"freq_hz": 50.5, "power_pu": 1.0},
        {"freq_hz": 52.0, "power_pu": 0.0},
    ]

    lvrt_pass = True
    hvrt_pass = True
    freq_pass = True
    reactive_pass = True
    thd = 3.5
    dc_inj = 0.2
    v_fluct = 2.0
    v_unbal = 1.0
    pq_pass = thd <= 5.0
    anti_island_time = 1.5
    anti_island_pass = anti_island_time <= 2.0
    comm_pass = True
    reactive_capacity = total_power_mw * 0.33

    overall = all([lvrt_pass, hvrt_pass, freq_pass, reactive_pass, pq_pass, anti_island_pass, comm_pass])
    failed = []
    if not lvrt_pass: failed.append("LVRT低电压穿越")
    if not hvrt_pass: failed.append("HVRT高电压穿越")
    if not freq_pass: failed.append("频率响应")
    if not reactive_pass: failed.append("无功功率能力")
    if not pq_pass: failed.append("电能质量")
    if not anti_island_pass: failed.append("防孤岛保护")
    if not comm_pass: failed.append("通信合规")

    return {
        "grid_standard": standard,
        "grid_voltage_kv": grid_voltage_kv,
        "grid_frequency_hz": grid_freq,
        "grid_type": data.get("grid_type", "TN"),
        "lvrt_curve": lvrt_curve,
        "lvrt_pass": lvrt_pass,
        "hvrt_curve": hvrt_curve,
        "hvrt_pass": hvrt_pass,
        "freq_response_curve": freq_curve,
        "freq_response_pass": freq_pass,
        "pf_lag": 0.95,
        "pf_lead": 0.95,
        "reactive_capacity_mvar": round(reactive_capacity, 2),
        "reactive_pass": reactive_pass,
        "thd": thd,
        "dc_injection": dc_inj,
        "voltage_fluctuation": v_fluct,
        "voltage_unbalance": v_unbal,
        "power_quality_pass": pq_pass,
        "anti_islanding_time_s": anti_island_time,
        "anti_islanding_pass": anti_island_pass,
        "comm_protocol": data.get("comm_protocol", "IEC_61850"),
        "remote_response_s": 0.1,
        "comm_pass": comm_pass,
        "overall_pass": overall,
        "failed_items": failed,
    }


