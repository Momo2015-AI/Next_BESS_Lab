"""产品库业务逻辑服务层

提供字段映射、模型转换、租户过滤、种子数据初始化等核心业务，
供 routes/products.py 调用。
"""

import json
import os

from flask import current_app
from sqlalchemy import or_

from database import (
    BatteryConfigRule,
    BatteryManufacturer,
    CellProduct,
    ClusterProduct,
    ContainerProduct,
    PackProduct,
    PcsProduct,
    RackProduct,
    db,
)

PRODUCTS_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "products.json")

_MODELS = {
    "cells": CellProduct,
    "packs": PackProduct,
    "racks": RackProduct,
    "clusters": ClusterProduct,
    "containers": ContainerProduct,
    "pcs": PcsProduct,
    "config_rules": BatteryConfigRule,
}

_FIELD_MAP = {
    "cells": {
        "capacityAh": "capacity_ah",
        "voltageNominal": "voltage_nominal",
        "voltageRange": "voltage_range",
        "ratedEnergyMWh": "rated_energy_mwh",
        "ratedEnergyMwh": "rated_energy_mwh",  # 兼容旧写法
        "energyWh": "rated_energy_mwh",
        "voltageMax": "voltage_max",
        "voltageMin": "voltage_min",
        "calendarLife": "calendar_life",
        "energyDensity": "energy_density",
        "certifications": "certifications",
        "unitPrice": "unit_price",
        "remarks": "remarks",
        "cycleLife": "cycle_life",
        "sohCurve": "soh_curve",
    },
    "packs": {
        "cellsPerPack": "cells_per_pack",
        "seriesCount": "series_count",
        "parallelCount": "parallel_count",
        "nominalVoltage": "nominal_voltage",
        "nominalCapacityAh": "nominal_capacity_ah",
        "ratedEnergyMWh": "rated_energy_mwh",
        "ratedEnergyMwh": "rated_energy_mwh",  # 兼容旧写法
        "nominalEnergykWh": "rated_energy_mwh",
        "nominalEnergyKwh": "rated_energy_mwh",  # 兼容旧写法
        "nominalEnergyKWh": "rated_energy_mwh",  # 兼容旧写法
        "maxChargeCurrent": "max_charge_current",
        "maxDischargeCurrent": "max_discharge_current",
        "cellModel": "cell_model",
        "bmsType": "bms_type",
    },
    "racks": {
        "packsPerRack": "packs_per_rack",
        "seriesCount": "series_count",
        "parallelCount": "parallel_count",
        "nominalVoltage": "nominal_voltage",
        "nominalCapacityAh": "nominal_capacity_ah",
        "ratedEnergyMWh": "rated_energy_mwh",
        "ratedEnergyMwh": "rated_energy_mwh",  # 兼容旧写法
        "nominalEnergykWh": "rated_energy_mwh",
        "nominalEnergyKwh": "rated_energy_mwh",  # 兼容旧写法
        "nominalEnergyKWh": "rated_energy_mwh",  # 兼容旧写法
        "packModel": "pack_model",
    },
    "clusters": {
        "racksPerCluster": "racks_per_cluster",
        "seriesCount": "series_count",
        "parallelCount": "parallel_count",
        "nominalVoltage": "nominal_voltage",
        "nominalCapacityAh": "nominal_capacity_ah",
        "ratedEnergyMWh": "rated_energy_mwh",
        "ratedEnergyMwh": "rated_energy_mwh",  # 兼容旧写法
        "nominalEnergyMWh": "rated_energy_mwh",
        "nominalEnergyMwh": "rated_energy_mwh",  # 兼容旧写法
        "ratedPowerMW": "rated_power_mw",
        "ratedPowerMw": "rated_power_mw",  # 兼容旧写法
        "nominalPowerMW": "rated_power_mw",
        "nominalPowerMw": "rated_power_mw",  # 兼容旧写法
        "rackModel": "rack_model",
        "bmuType": "bmu_type",
    },
    "containers": {
        "ratedEnergyMWh": "rated_energy_mwh",
        "ratedEnergyMwh": "rated_energy_mwh",  # 兼容旧写法
        "ratedPowerMW": "rated_power_mw",
        "ratedPowerMw": "rated_power_mw",  # 兼容旧写法
        "cellModel": "cell_model",
        "cellConfig": "cell_config",
        "cycleLife": "cycle_life",
        "clusterModel": "cluster_model",
        "clustersPerContainer": "clusters_per_container",
        "type": "spec",
        "seriesCount": "series_count",
        "parallelCount": "parallel_count",
        "dcVoltageRange": "dc_voltage_range",
        "maxDcCurrent": "max_dc_current",
        "rte": "rte",
        "auxRun": "aux_run",
        "auxStandby": "aux_standby",
        "certifications": "certifications",
        "unitPrice": "unit_price",
        "remarks": "remarks",
    },
    "pcs": {
        "ratedPowerMW": "rated_power_mw",
        "ratedPowerMw": "rated_power_mw",  # 兼容旧写法
        "ratedPowerKVA": "rated_power_kva",
        "ratedPowerKva": "rated_power_kva",  # 兼容旧写法
        "acVoltage": "ac_voltage",
        "dcVoltageRange": "dc_voltage_range",
        "maxDcCurrent": "max_dc_current",
        "frequencyRange": "frequency_range",
        "topology": "topology",
        "isolation": "isolation",
        "dimensions": "dimensions",
        "weight": "weight",
        "efficiency": "efficiency",
        "cooling": "cooling",
        "auxRun": "aux_run",
        "auxStandby": "aux_standby",
        "certifications": "certifications",
        "unitPrice": "unit_price",
        "remarks": "remarks",
    },
    "config_rules": {
        "cellModel": "cell_model",
        "packModel": "pack_model",
        "rackModel": "rack_model",
        "clusterModel": "cluster_model",
        "containerModel": "container_model",
        "cellsPerPack": "cells_per_pack",
        "packsPerRack": "packs_per_rack",
        "racksPerCluster": "racks_per_cluster",
        "clustersPerContainer": "clusters_per_container",
        "seriesPerPack": "series_per_pack",
        "parallelPerPack": "parallel_per_pack",
        "seriesPerRack": "series_per_rack",
        "parallelPerRack": "parallel_per_rack",
        "seriesPerCluster": "series_per_cluster",
        "parallelPerCluster": "parallel_per_cluster",
        "packNominalVoltage": "pack_nominal_voltage",
        "packNominalCapacityAh": "pack_nominal_capacity_ah",
        "packNominalEnergykWh": "pack_nominal_energy_kwh",
        "packNominalEnergyKwh": "pack_nominal_energy_kwh",  # 兼容旧写法
        "rackNominalVoltage": "rack_nominal_voltage",
        "rackNominalCapacityAh": "rack_nominal_capacity_ah",
        "rackNominalEnergykWh": "rack_nominal_energy_kwh",
        "rackNominalEnergyKwh": "rack_nominal_energy_kwh",  # 兼容旧写法
        "clusterNominalVoltage": "cluster_nominal_voltage",
        "clusterNominalCapacityAh": "cluster_nominal_capacity_ah",
        "clusterNominalEnergyMWh": "cluster_nominal_energy_mwh",
        "clusterNominalEnergyMwh": "cluster_nominal_energy_mwh",  # 兼容旧写法
        "clusterNominalPowerMW": "cluster_nominal_power_mw",
        "clusterNominalPowerMw": "cluster_nominal_power_mw",  # 兼容旧写法
        "containerNominalEnergyMWh": "container_nominal_energy_mwh",
        "containerNominalEnergyMwh": "container_nominal_energy_mwh",  # 兼容旧写法
        "containerNominalPowerMW": "container_nominal_power_mw",
        "containerNominalPowerMw": "container_nominal_power_mw",  # 兼容旧写法
        "isDefault": "is_default",
    },
}

_MFR_NAME_MAP = {
    "EVE (亿纬锂能)": "亿纬锂能 EVE",
    "CATL (宁德时代)": "宁德时代 CATL",
    "BYD (比亚迪)": "比亚迪 BYD",
    "Panasonic (松下)": "松下 Panasonic",
    "LG Energy (LG新能源)": "LG化学 LG Chem",
    "Samsung SDI": "三星 SDI",
    "Sony": "索尼 Sony",
    "Toshiba": "东芝 Toshiba",
    "Hitachi": "日立 Hitachi",
    "国轩高科": "国轩高科 Gotion",
    "欣旺达": "欣旺达 Sunwoda",
}

_MFR_CACHE = {}


def get_models():
    """返回类别 → Model 映射。"""
    return _MODELS


def camel_to_snake(name, category):
    """camelCase → snake_case 字段映射。"""
    return _FIELD_MAP.get(category, {}).get(name, name)


def json_to_model(item, category):
    """将前端 JSON dict 转为 ORM 模型实例。"""
    model_cls = _MODELS[category]
    kwargs = {}
    for k, v in item.items():
        key = camel_to_snake(k, category)
        if hasattr(model_cls, key):
            kwargs[key] = v
    return model_cls(**kwargs)


def is_super_admin(user):
    """判断是否为超级管理员：role == 'admin'"""
    return user is not None and getattr(user, "role", None) == "admin"


def apply_tenant_filter(query, model_cls, user, include_builtin=True):
    """
    应用企业隔离过滤：
    - 超级管理员：可见全部数据
    - 普通用户：仅可见自己企业数据 + 系统内置数据
    """
    if is_super_admin(user):
        return query
    if user is None:
        if include_builtin and hasattr(model_cls, "is_builtin"):
            return query.filter(model_cls.is_builtin.is_(True))
        return query.filter(False)
    if hasattr(model_cls, "tenant_id") and hasattr(model_cls, "is_builtin"):
        if include_builtin:
            return query.filter(or_(model_cls.tenant_id == user.tenant_id, model_cls.is_builtin.is_(True)))
        return query.filter(model_cls.tenant_id == user.tenant_id)
    return query


def _get_manufacturer_id(mfr_name):
    """根据厂商名称匹配电池厂家ID（带缓存）"""
    if not mfr_name:
        return None

    if mfr_name in _MFR_CACHE:
        return _MFR_CACHE[mfr_name]

    normalized_name = _MFR_NAME_MAP.get(mfr_name, mfr_name)

    mfr = BatteryManufacturer.query.filter(
        or_(
            BatteryManufacturer.name == normalized_name,
            BatteryManufacturer.name_en == normalized_name,
            BatteryManufacturer.name.contains(mfr_name.split("(")[0].strip()),
        )
    ).first()

    result = mfr.id if mfr else None
    _MFR_CACHE[mfr_name] = result
    return result


def seed_products():
    """从 products.json 种子数据初始化产品库（标记为系统内置，所有企业可见）

    支持 upsert：ID 存在时更新所有字段，不存在时创建。
    """
    if not os.path.exists(PRODUCTS_DATA_PATH):
        return

    with open(PRODUCTS_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for category, items in data.items():
        if category not in _MODELS:
            continue
        model_cls = _MODELS[category]
        existing_map = {str(o.id): o for o in model_cls.query.all()}
        for item in items:
            if "is_builtin" not in item:
                item["is_builtin"] = True
            if "tenant_id" not in item:
                item["tenant_id"] = None

            mfr_name = item.get("mfr")
            if mfr_name and hasattr(model_cls, "manufacturer_id"):
                item["manufacturer_id"] = _get_manufacturer_id(mfr_name)

            existing = existing_map.get(item.get("id"))
            if existing:
                for k, v in item.items():
                    key = camel_to_snake(k, category)
                    if hasattr(model_cls, key):
                        setattr(existing, key, v)
            else:
                obj = json_to_model(item, category)
                db.session.add(obj)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"种子产品数据失败: {e}", exc_info=True)
