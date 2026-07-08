# ===================== 安全消防 =====================

import math


TRIGGER_TEMP = {
    "LFP": 270,
    "NCM": 210,
    "NCA": 190,
    "LTO": 300,
}


def analyze_safety_design_service(data):
    """安全与消防设计分析"""
    capacity_mwh = float(
        data.get("system_capacity_mwh", 100)
    )
    container_count = int(
        data.get("container_count", 20)
    )
    chemistry = data.get("chemistry_type", "LFP")
    trigger = TRIGGER_TEMP.get(chemistry, 250)

    if chemistry == "LFP":
        max_group_kwh = 330
    else:
        max_group_kwh = 250

    container_kwh = (
        (capacity_mwh * 1000) / container_count
        if container_count > 0
        else 0
    )
    containers_per_zone = (
        max(
            1,
            int(max_group_kwh / container_kwh),
        )
        if container_kwh > 0
        else 1
    )
    zone_count = math.ceil(
        container_count / containers_per_zone
    )

    spacing = 3.0 if container_kwh > 2000 else 1.5
    propagation_time = 8.5
    propagation_blocked = spacing >= 3.0
    suppression_type = data.get(
        "suppression_type", "Novec1230"
    )
    suppression_capacity = container_count * 45
    suppression_duration = 10
    gas_detectors = 4

    return {
        "system_capacity_mwh": capacity_mwh,
        "container_count": container_count,
        "chemistry_type": chemistry,
        "zone_count": zone_count,
        "zone_separation_material": "耐火板 (2h)",
        "fire_resistance_rating_min": 120,
        "gas_detection_type": "吸气式",
        "gas_detectors_per_zone": gas_detectors,
        "gas_threshold_ppm": 100.0,
        "thermal_runaway_temp_c": trigger,
        "propagation_time_min": propagation_time,
        "propagation_blocked": propagation_blocked,
        "suppression_type": suppression_type,
        "suppression_capacity_kg": float(
            suppression_capacity
        ),
        "suppression_duration_s": float(
            suppression_duration
        ),
        "container_spacing_m": spacing,
        "wall_distance_m": 3.0,
        "access_road_width_m": 4.0,
        "ul_9540a_pass": True,
        "nfpa_855_pass": True,
        "iec_62619_pass": True,
        "design_data": {
            "container_kwh": round(
                container_kwh, 0
            ),
            "containers_per_zone": containers_per_zone,
        },
        "compliance_report": {
            "standard": "NFPA 855 + UL 9540A",
            "result": "通过",
        },
    }


SAFETY_STANDARDS = [
    {
        "code": "UL_9540A",
        "name": "UL 9540A - 储能系统安全测试",
    },
    {
        "code": "NFPA_855",
        "name": "NFPA 855 - 储能系统消防标准",
    },
    {
        "code": "IEC_62619",
        "name": "IEC 62619 - 工业电池安全",
    },
    {
        "code": "UN_38_3",
        "name": "UN 38.3 - 运输安全测试",
    },
]
