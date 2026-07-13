# ===================== 热管理 =====================

# COP (Coefficient of Performance) 按冷却方式
COP_MAP = {
    "forced-air": 2.0,    # 风冷效率较低
    "liquid": 3.5,         # 液冷标准
    "SiC-liquid": 5.0,     # 全液冷碳化硅，最高效
}

# 容器热参数默认值
CONTAINER_U_VALUE = 0.5      # W/(m²·K) 传热系数
CONTAINER_AREA_M2 = 60       # m² 集装箱表面积
TARGET_CELL_TEMP_C = 25      # ℃ 目标电芯温度
FIXED_AUX_KW = 3.0           # kW BMS/消防/照明固定功耗
SAFETY_FACTOR = 1.2          # 20% 安全裕度


def calculate_cooling_power(ambient_temp_c, cooling_type, container_params=None):
    """根据环境温度和冷却方式计算冷却功耗。

    用于仿真管线中动态推导 bessAuxRun，替代固定常量。

    Args:
        ambient_temp_c: 环境温度 (℃)
        cooling_type: 冷却方式 ("forced-air" | "liquid" | "SiC-liquid")
        container_params: 可选容器参数 dict:
            - cell_capacity_ah (默认 280)
            - cell_resistance_ohm (默认 0.00025)
            - c_rate (默认 0.5)
            - cells_per_container (默认 5000)

    Returns:
        dict: {
            cooling_power_kw: 运行冷却功耗 (kW),
            standby_power_kw: 待机冷却功耗 (kW),
            cop: 实际使用的 COP 值,
            heat_load_kw: 总热负荷 (kW),
            cell_heat_kw: 电芯发热 (kW),
            infiltration_kw: 热渗透 (kW),
            ambient_temp_c: 输入环境温度,
            cooling_type: 输入冷却方式,
        }
    """
    cp = container_params or {}
    cell_ah = float(cp.get("cell_capacity_ah", 280))
    cell_resistance = float(cp.get("cell_resistance_ohm", 0.00025))
    c_rate = float(cp.get("c_rate", 0.5))
    cells_per_container = int(cp.get("cells_per_container", 5000))

    # 电芯发热: I²R × N
    current = cell_ah * c_rate
    heat_per_cell_w = current ** 2 * cell_resistance
    cell_heat_kw = (heat_per_cell_w * cells_per_container) / 1000

    # 容器壁热渗透: U × A × (T_ambient - T_target)
    # 仅当环境温度高于目标温度时产生正向热渗透（需要制冷）
    delta_t = max(0, ambient_temp_c - TARGET_CELL_TEMP_C)
    infiltration_w = CONTAINER_U_VALUE * CONTAINER_AREA_M2 * delta_t
    infiltration_kw = infiltration_w / 1000

    # 总热负荷（含安全系数）
    total_heat_kw = (cell_heat_kw + infiltration_kw) * SAFETY_FACTOR

    # COP 折算为电功耗
    cop = COP_MAP.get(cooling_type, COP_MAP["liquid"])
    cooling_power_kw = total_heat_kw / cop if cop > 0 else total_heat_kw

    # 待机功耗约为运行功耗的 15%
    standby_power_kw = round(cooling_power_kw * 0.15, 2)

    return {
        "cooling_power_kw": round(cooling_power_kw, 2),
        "standby_power_kw": standby_power_kw,
        "cop": cop,
        "heat_load_kw": round(total_heat_kw, 2),
        "cell_heat_kw": round(cell_heat_kw, 2),
        "infiltration_kw": round(infiltration_kw, 2),
        "ambient_temp_c": ambient_temp_c,
        "cooling_type": cooling_type,
    }


def calculate_thermal_service(data):
    """热管理设计计算"""
    env_temp = float(data.get("ambient_max_c", 45))
    cell_ah = float(data.get("cell_capacity_ah", 280))
    cell_resistance = float(data.get("cell_resistance_ohm", 0.00025))
    c_rate = float(data.get("c_rate", 0.5))
    cells_per_container = int(data.get("cells_per_container", 5000))
    cooling_type = data.get("cooling_type", "liquid")

    current = cell_ah * c_rate
    heat_per_cell = current**2 * cell_resistance
    total_heat_w = heat_per_cell * cells_per_container
    total_heat_kw = total_heat_w / 1000

    target_temp = 25
    container_area = 60
    u_value = 0.5
    heat_infiltration = container_area * u_value * (env_temp - target_temp)
    total_cooling_kw = (total_heat_kw + heat_infiltration / 1000) * 1.2

    coolant_dt = 5
    coolant_cp = 3.5
    coolant_density = 1050
    coolant_flow_lpm = (
        total_cooling_kw / (coolant_cp * coolant_dt * coolant_density) * 60 * 1000 if total_cooling_kw > 0 else 0
    )

    derating = []
    for temp in range(20, 60, 5):
        if temp <= 35:
            pct = 100
        elif temp <= 45:
            pct = 100 - (temp - 35) * 5
        else:
            pct = max(20, 50 - (temp - 45) * 3)
        derating.append({"temp": temp, "power_pct": pct})

    annual_cooling = total_cooling_kw * 8760 * 0.7

    return {
        "ambient_max_c": env_temp,
        "cooling_type": cooling_type,
        "coolant_type": ("乙二醇水溶液(50%)" if cooling_type == "liquid" else "制冷剂"),
        "coolant_flow_rate_lpm": round(coolant_flow_lpm, 1),
        "hvac_capacity_kw": round(total_cooling_kw, 2),
        "hvac_cop": 2.5,
        "hvac_redundancy": 1,
        "cell_heat_generation_w": round(heat_per_cell, 3),
        "thermal_resistance_ckw": 0.15,
        "target_cell_temp_c": target_temp,
        "max_cell_temp_c": target_temp + 3,
        "temp_gradient_c": 3.0,
        "cooling_power_kw": round(total_cooling_kw, 2),
        "annual_cooling_energy_kwh": round(annual_cooling, 0),
        "derating_curve": derating,
    }
