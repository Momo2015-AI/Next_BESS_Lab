"""统一单位与汇率工具模块"""

EXCHANGE_RATES = {
    "USD": 1.0,
    "SAR": 3.75,
    "AED": 3.6725,
    "CNY": 7.24,
}

POWER_UNITS = {
    "W": 1e-6,
    "kW": 1e-3,
    "MW": 1.0,
    "GW": 1e3,
}

ENERGY_UNITS = {
    "Wh": 1e-6,
    "kWh": 1e-3,
    "MWh": 1.0,
    "GWh": 1e3,
}

AREA_UNITS = {
    "sqm": 1.0,
    "sqft": 10.7639,
}


def to_internal(value, unit_category, unit):
    """将外部单位转换为内部标准单位 (MW / MWh / USD / m²)"""
    if unit_category == "power":
        factor = POWER_UNITS.get(unit, 1.0)
        return value * factor
    elif unit_category == "energy":
        factor = ENERGY_UNITS.get(unit, 1.0)
        return value * factor
    elif unit_category == "area":
        factor = AREA_UNITS.get(unit, 1.0)
        return value / factor if unit == "sqft" else value
    elif unit_category == "currency":
        rate = EXCHANGE_RATES.get(unit, 1.0)
        return value / rate
    return value


def to_display(value, unit_category, unit):
    """将内部标准单位转换为显示单位"""
    if unit_category == "power":
        factor = POWER_UNITS.get(unit, 1.0)
        return value / factor if factor != 0 else value
    elif unit_category == "energy":
        factor = ENERGY_UNITS.get(unit, 1.0)
        return value / factor if factor != 0 else value
    elif unit_category == "area":
        factor = AREA_UNITS.get(unit, 1.0)
        return value * factor
    elif unit_category == "currency":
        rate = EXCHANGE_RATES.get(unit, 1.0)
        return value * rate
    return value


def convert_currency(value, from_currency, to_currency):
    """货币转换"""
    usd_value = value / EXCHANGE_RATES.get(from_currency, 1.0)
    return usd_value * EXCHANGE_RATES.get(to_currency, 1.0)
