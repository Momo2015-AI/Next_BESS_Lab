"""AI 仿真算法业务逻辑服务层

提供厂家数据查询、Arrhenius 模型预测、参数校准等核心业务，
供 routes/ai_sim.py 调用。
"""

import json
import math

from flask import current_app

from database import BatteryManufacturer, db

# ==================== 预设电池厂家数据 ====================

MANUFACTURERS_DB = [
    {
        "id": "catl",
        "name": "宁德时代 CATL",
        "name_en": "CATL",
        "country": "中国",
        "chemistry_type": "LFP",
        "calibrated_params": {
            "A_cal": 1.170338,
            "Ea_cal": 26000,
            "alpha": 0.75,
            "A_cyc": 7.534055,
            "Ea_cyc": 22000,
            "beta": 0.55,
            "gamma": 1.4,
            "delta": 0.18,
            "degradation_rate": 0.12,
        },
        "rmse_soh": 1.8,
        "rmse_rte": 0.8,
        "data_points": 156,
        "applicable_scenarios": ["LFP日历衰减", "循环衰减", "综合衰减预测", "大规模储能"],
        "description": "宁德时代（CATL）LFP电芯，适用于大规模储能电站。首年衰减约2.2%，25年末SOH约85%。",
        "is_builtin": True,
        "sort_order": 1,
    },
    {
        "id": "byd",
        "name": "比亚迪 BYD",
        "name_en": "BYD",
        "country": "中国",
        "chemistry_type": "LFP",
        "calibrated_params": {
            "A_cal": 1.267866,
            "Ea_cal": 26000,
            "alpha": 0.78,
            "A_cyc": 8.161893,
            "Ea_cyc": 22000,
            "beta": 0.58,
            "gamma": 1.35,
            "delta": 0.20,
            "degradation_rate": 0.13,
        },
        "rmse_soh": 1.9,
        "rmse_rte": 0.9,
        "data_points": 148,
        "applicable_scenarios": ["LFP日历衰减", "循环衰减", "综合衰减预测", "大规模储能"],
        "description": "比亚迪（BYD）LFP电芯，适用于大规模储能电站。首年衰减约2.9%，25年末SOH约79%。",
        "is_builtin": True,
        "sort_order": 2,
    },
    {
        "id": "fluence",
        "name": "Fluence Energy",
        "name_en": "Fluence",
        "country": "美国",
        "chemistry_type": "LFP",
        "calibrated_params": {
            "A_cal": 1.072810,
            "Ea_cal": 26000,
            "alpha": 0.72,
            "A_cyc": 6.906217,
            "Ea_cyc": 22000,
            "beta": 0.52,
            "gamma": 1.45,
            "delta": 0.16,
            "degradation_rate": 0.11,
        },
        "rmse_soh": 1.5,
        "rmse_rte": 0.7,
        "data_points": 200,
        "applicable_scenarios": ["LFP日历衰减", "循环衰减", "综合衰减预测", "电网级储能"],
        "description": "Fluence（原Siemens Energy）LFP系统，适用于电网级储能。首年衰减约1.7%，25年末SOH约90%。",
        "is_builtin": True,
        "sort_order": 3,
    },
    {
        "id": "tesla",
        "name": "Tesla Megapack",
        "name_en": "Tesla",
        "country": "美国",
        "chemistry_type": "LFP",
        "calibrated_params": {
            "A_cal": 0.975282,
            "Ea_cal": 26000,
            "alpha": 0.70,
            "A_cyc": 6.278379,
            "Ea_cyc": 22000,
            "beta": 0.50,
            "gamma": 1.50,
            "delta": 0.15,
            "degradation_rate": 0.10,
        },
        "rmse_soh": 1.4,
        "rmse_rte": 0.6,
        "data_points": 220,
        "applicable_scenarios": ["LFP日历衰减", "循环衰减", "综合衰减预测", "电网级储能"],
        "description": "Tesla Megapack LFP系统，适用于电网级储能。首年衰减约1.4%，25年末SOH约92%。",
        "is_builtin": True,
        "sort_order": 4,
    },
    {
        "id": "lg_es",
        "name": "LG Energy Solution",
        "name_en": "LGES",
        "country": "韩国",
        "chemistry_type": "LFP",
        "calibrated_params": {
            "A_cal": 1.365394,
            "Ea_cal": 26000,
            "alpha": 0.80,
            "A_cyc": 8.789731,
            "Ea_cyc": 22000,
            "beta": 0.60,
            "gamma": 1.30,
            "delta": 0.22,
            "degradation_rate": 0.14,
        },
        "rmse_soh": 2.0,
        "rmse_rte": 1.0,
        "data_points": 130,
        "applicable_scenarios": ["LFP日历衰减", "循环衰减", "综合衰减预测"],
        "description": "LG新能源（LGES）LFP电芯，适用于大规模储能。首年衰减约3.6%，25年末SOH约73%。",
        "is_builtin": True,
        "sort_order": 5,
    },
    {
        "id": "panasonic",
        "name": "Panasonic",
        "name_en": "Panasonic",
        "country": "日本",
        "chemistry_type": "NMC",
        "calibrated_params": {
            "A_cal": 1.647877,
            "Ea_cal": 28000,
            "alpha": 0.82,
            "A_cyc": 9.041866,
            "Ea_cyc": 24000,
            "beta": 0.62,
            "gamma": 1.55,
            "delta": 0.24,
            "degradation_rate": 0.15,
        },
        "rmse_soh": 2.2,
        "rmse_rte": 1.1,
        "data_points": 110,
        "applicable_scenarios": ["NMC日历衰减", "循环衰减", "综合衰减预测"],
        "description": "松下（Panasonic）NMC电芯，适用于高能量密度场景。首年衰减约3.8%，25年末SOH约68%。",
        "is_builtin": True,
        "sort_order": 6,
    },
]

NUM_YEARS = 26
R = 8.314


def _get_manufacturer_by_id(manufacturer_id):
    """根据ID查找厂家数据。"""
    if not manufacturer_id:
        return MANUFACTURERS_DB[0]  # 默认 CATL
    for mfr in MANUFACTURERS_DB:
        if mfr["id"] == manufacturer_id:
            return mfr
    return MANUFACTURERS_DB[0]


def _predict_with_arrhenius(params, temp, cycles_per_day, dod, c_rate, model_params):
    """使用 Arrhenius 模型预测 SOH/RTE。"""
    T_kelvin = temp + 273.15
    T_ref = 298.15  # 25°C
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
    soh[0] = 100.0
    rte[0] = 97.03

    for year in range(1, NUM_YEARS):
        days = year * 365
        cycles = year * 365 * cycles_per_day

        # 日历老化
        q_cal = A_cal * math.exp(-Ea_cal / (R * T_kelvin)) * (days**alpha)
        # 循环老化
        q_cyc = A_cyc * math.exp(-Ea_cyc / (R * T_kelvin)) * (cycles**beta) * dod_factor * c_rate_factor

        total_degradation = (q_cal + q_cyc) * 100
        soh[year] = max(0, 100 - total_degradation)
        rte[year] = max(80, 97.03 - total_degradation * 0.15)

    return soh, rte


def run_simulation(data):
    """执行 AI 仿真计算。

    Args:
        data: dict with manufacturer_id, simulation_years, temperature,
              cycles_per_day, dod, c_rate, rte_initial

    Returns:
        dict with soh_curve, rte_curve, manufacturer, model_type, rmse
    """
    manufacturer_id = data.get("manufacturer_id")
    simulation_years = data.get("simulation_years", 25)
    temperature = data.get("temperature", 25)
    cycles_per_day = data.get("cycles_per_day", 1)
    dod = data.get("dod", 0.8)
    c_rate = data.get("c_rate", 0.5)
    rte_initial = data.get("rte_initial", 94.1)

    mfr = _get_manufacturer_by_id(manufacturer_id)
    model_params = mfr["calibrated_params"]

    soh, rte = _predict_with_arrhenius(data, temperature, cycles_per_day, dod, c_rate, model_params)

    # Trim to simulation_years
    soh = soh[: simulation_years + 1]
    rte = rte[: simulation_years + 1]

    return {
        "soh_curve": soh,
        "rte_curve": rte,
        "manufacturer": mfr["name"],
        "chemistry_type": mfr["chemistry_type"],
        "model_type": "arrhenius",
        "rmse_soh": mfr.get("rmse_soh", 2.0),
        "rmse_rte": mfr.get("rmse_rte", 1.0),
        "params": {
            "temperature": temperature,
            "cycles_per_day": cycles_per_day,
            "dod": dod * 100,
            "c_rate": c_rate,
        },
    }


def list_manufacturers():
    """构建厂家列表（供 API 返回）。"""
    manufacturers = []
    for mfr in MANUFACTURERS_DB:
        manufacturers.append(
            {
                "id": mfr["id"],
                "name": mfr["name"],
                "name_en": mfr["name_en"],
                "country": mfr["country"],
                "chemistry_type": mfr["chemistry_type"],
                "calibrated_params": mfr["calibrated_params"],
                "rmse_soh": mfr["rmse_soh"],
                "rmse_rte": mfr["rmse_rte"],
                "data_points": mfr["data_points"],
                "applicable_scenarios": mfr["applicable_scenarios"],
                "description": mfr["description"],
                "is_builtin": mfr["is_builtin"],
                "sort_order": mfr["sort_order"],
            }
        )
    return manufacturers


def calibrate_params(data):
    """参数校准 - 根据实测数据校准 Arrhenius 参数。

    Args:
        data: dict with manufacturer_id, measured_soh (optional)

    Returns:
        dict with calibrated_params, manufacturer
    """
    manufacturer_id = data.get("manufacturer_id")
    mfr = _get_manufacturer_by_id(manufacturer_id)
    calibrated_params = dict(mfr["calibrated_params"])

    # 如果提供了实测 SOH 数据，进行简单最小二乘校准
    measured_soh = data.get("measured_soh")
    if measured_soh and isinstance(measured_soh, list) and len(measured_soh) > 0:
        # 根据实测数据的平均衰减率微调参数
        avg_degradation = sum(100 - s for s in measured_soh if s > 0) / len(measured_soh)
        calibration_factor = 1.0 + (avg_degradation - 28) / 100.0  # 基准28%衰减
        calibrated_params["A_cal"] *= calibration_factor
        calibrated_params["A_cyc"] *= calibration_factor

    return {"calibrated_params": calibrated_params, "manufacturer": mfr["name"]}


def seed_manufacturers():
    """初始化电池厂家种子数据到数据库。"""
    existing_ids = {m.id for m in BatteryManufacturer.query.with_entities(BatteryManufacturer.id).all()}
    for mfr_data in MANUFACTURERS_DB:
        if mfr_data["id"] in existing_ids:
            continue
        mfr = BatteryManufacturer(
            id=mfr_data["id"],
            name=mfr_data["name"],
            name_en=mfr_data["name_en"],
            country=mfr_data["country"],
            chemistry_type=mfr_data["chemistry_type"],
            calibrated_params=json.dumps(mfr_data["calibrated_params"]),
        )
        db.session.add(mfr)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"种子厂家数据失败: {e}", exc_info=True)
