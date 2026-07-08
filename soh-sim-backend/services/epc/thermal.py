# ===================== 热管理 =====================


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
