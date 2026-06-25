# -*- coding: utf-8 -*-
"""
PCS产品库同步脚本
将网上主流厂商PCS规格书数据导入到pcs_library表

数据来源：阳光电源、华为、科华数能、上能电气等厂商官方规格书
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'soh-sim-backend'))

from app import app
from database import db, PCS_LIBRARY
import uuid

# PCS产品数据（基于网上主流厂商规格书）
PCS_PRODUCTS = [
    # ==================== 阳光电源 PCS ====================
    {
        "model": "SG2500UH-MV",
        "mfr": "阳光电源",
        "rated_power_mw": 2.5,
        "efficiency": 99.0,
        "ac_voltage": "690V",
        "dc_voltage_range": "900-1500V",
        "max_dc_current": 3125,
        "frequency_range": "45-55Hz",
        "dimensions": "1200x800x2000mm",
        "weight": 1200,
        "cooling": "智能液冷",
        "aux_run": 4.5,
        "aux_standby": 1.2,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "GB/T 34133", "IEC 62477"]',
        "unit_price": 45.0,
        "remarks": "阳光电源2.5MW储能变流器，液冷散热，构网型"
    },
    {
        "model": "SG3125HV-MV",
        "mfr": "阳光电源",
        "rated_power_mw": 3.125,
        "efficiency": 99.0,
        "ac_voltage": "690V",
        "dc_voltage_range": "900-1500V",
        "max_dc_current": 3906,
        "frequency_range": "45-55Hz",
        "dimensions": "1400x800x2200mm",
        "weight": 1400,
        "cooling": "智能液冷",
        "aux_run": 5.5,
        "aux_standby": 1.5,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "GB/T 34133", "IEC 62477"]',
        "unit_price": 52.0,
        "remarks": "阳光电源3.125MW储能变流器，高功率密度"
    },
    {
        "model": "SG5000HV-MV",
        "mfr": "阳光电源",
        "rated_power_mw": 5.0,
        "efficiency": 99.0,
        "ac_voltage": "690V",
        "dc_voltage_range": "900-1500V",
        "max_dc_current": 6250,
        "frequency_range": "45-55Hz",
        "dimensions": "1800x1000x2400mm",
        "weight": 2200,
        "cooling": "智能液冷",
        "aux_run": 8.0,
        "aux_standby": 2.0,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "GB/T 34133", "IEC 62477"]',
        "unit_price": 80.0,
        "remarks": "阳光电源5MW储能变流器，大型储能系统首选"
    },
    {
        "model": "PowerTitan 2.5MW PCS",
        "mfr": "阳光电源",
        "rated_power_mw": 2.5,
        "efficiency": 99.3,
        "ac_voltage": "690V",
        "dc_voltage_range": "1123-1498V",
        "max_dc_current": 2870,
        "frequency_range": "45-55Hz",
        "dimensions": "1100x800x1900mm",
        "weight": 1100,
        "cooling": "全液冷碳化硅",
        "aux_run": 3.5,
        "aux_standby": 0.8,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "GB/T 34133", "GB/T 36276", "IEC 62477"]',
        "unit_price": 48.0,
        "remarks": "PowerTitan 3.0系统专用PCS，碳化硅技术，效率99.3%"
    },
    # ==================== 华为 PCS ====================
    {
        "model": "SUN2000-330KTL",
        "mfr": "华为",
        "rated_power_mw": 0.33,
        "efficiency": 99.0,
        "ac_voltage": "400V",
        "dc_voltage_range": "600-1500V",
        "max_dc_current": 600,
        "frequency_range": "45-55Hz",
        "dimensions": "1040x700x1600mm",
        "weight": 750,
        "cooling": "智能风冷",
        "aux_run": 2.5,
        "aux_standby": 0.5,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "IEC 62477"]',
        "unit_price": 12.0,
        "remarks": "华为330kW储能变流器，工商业储能适用"
    },
    {
        "model": "SUN2000-500KTL",
        "mfr": "华为",
        "rated_power_mw": 0.5,
        "efficiency": 99.0,
        "ac_voltage": "400V",
        "dc_voltage_range": "600-1500V",
        "max_dc_current": 900,
        "frequency_range": "45-55Hz",
        "dimensions": "1100x750x1650mm",
        "weight": 850,
        "cooling": "智能风冷",
        "aux_run": 3.0,
        "aux_standby": 0.6,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "IEC 62477"]',
        "unit_price": 18.0,
        "remarks": "华为500kW储能变流器"
    },
    {
        "model": "SUN2000-630KTL",
        "mfr": "华为",
        "rated_power_mw": 0.63,
        "efficiency": 99.0,
        "ac_voltage": "400V",
        "dc_voltage_range": "600-1500V",
        "max_dc_current": 1100,
        "frequency_range": "45-55Hz",
        "dimensions": "1150x800x1700mm",
        "weight": 950,
        "cooling": "智能风冷",
        "aux_run": 3.5,
        "aux_standby": 0.8,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "IEC 62477"]',
        "unit_price": 22.0,
        "remarks": "华为630kW储能变流器"
    },
    {
        "model": "SUN2000-1.25MW-MT",
        "mfr": "华为",
        "rated_power_mw": 1.25,
        "efficiency": 99.0,
        "ac_voltage": "690V",
        "dc_voltage_range": "900-1500V",
        "max_dc_current": 1563,
        "frequency_range": "45-55Hz",
        "dimensions": "1200x900x2000mm",
        "weight": 1200,
        "cooling": "智能液冷",
        "aux_run": 5.0,
        "aux_standby": 1.0,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "GB/T 34133", "IEC 62477"]',
        "unit_price": 35.0,
        "remarks": "华为1.25MW储能变流器，组串式设计"
    },
    {
        "model": "SUN2000-1.725MW-MT",
        "mfr": "华为",
        "rated_power_mw": 1.725,
        "efficiency": 99.0,
        "ac_voltage": "690V",
        "dc_voltage_range": "1000-1500V",
        "max_dc_current": 1922,
        "frequency_range": "45-55Hz",
        "dimensions": "1400x1000x2200mm",
        "weight": 1600,
        "cooling": "智能液冷",
        "aux_run": 6.5,
        "aux_standby": 1.5,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "GB/T 34133", "IEC 62477"]',
        "unit_price": 45.0,
        "remarks": "华为1.725MW储能变流器"
    },
    {
        "model": "SUN2000-2.5MW-MT",
        "mfr": "华为",
        "rated_power_mw": 2.5,
        "efficiency": 99.0,
        "ac_voltage": "690V",
        "dc_voltage_range": "1000-1500V",
        "max_dc_current": 2885,
        "frequency_range": "45-55Hz",
        "dimensions": "1600x1100x2400mm",
        "weight": 2000,
        "cooling": "智能液冷",
        "aux_run": 8.0,
        "aux_standby": 2.0,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "GB/T 34133", "IEC 62477"]',
        "unit_price": 65.0,
        "remarks": "华为2.5MW储能变流器"
    },
    # ==================== 科华数能 PCS ====================
    {
        "model": "PCS-75K-HM",
        "mfr": "科华数能",
        "rated_power_mw": 0.075,
        "efficiency": 99.03,
        "ac_voltage": "480V",
        "dc_voltage_range": "700-1500V",
        "max_dc_current": 120,
        "frequency_range": "45-55Hz",
        "dimensions": "700x900x265mm",
        "weight": 95,
        "cooling": "强制风冷",
        "aux_run": 0.5,
        "aux_standby": 0.1,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "GB/T 34133", "IEC 62477"]',
        "unit_price": 3.5,
        "remarks": "科华75kW储能变流器，壁挂式/机架式"
    },
    {
        "model": "PCS-100K-HM",
        "mfr": "科华数能",
        "rated_power_mw": 0.1,
        "efficiency": 99.03,
        "ac_voltage": "400V",
        "dc_voltage_range": "600-1000V",
        "max_dc_current": 186,
        "frequency_range": "45-55Hz",
        "dimensions": "700x900x265mm",
        "weight": 95,
        "cooling": "强制风冷",
        "aux_run": 0.6,
        "aux_standby": 0.1,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "GB/T 34133", "IEC 62477"]',
        "unit_price": 4.5,
        "remarks": "科华100kW储能变流器"
    },
    {
        "model": "PCS-125K-HM",
        "mfr": "科华数能",
        "rated_power_mw": 0.125,
        "efficiency": 99.03,
        "ac_voltage": "690V",
        "dc_voltage_range": "1000-1500V",
        "max_dc_current": 134,
        "frequency_range": "45-55Hz",
        "dimensions": "700x900x265mm",
        "weight": 95,
        "cooling": "强制风冷",
        "aux_run": 0.7,
        "aux_standby": 0.15,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "GB/T 34133", "IEC 62477"]',
        "unit_price": 5.5,
        "remarks": "科华125kW储能变流器"
    },
    {
        "model": "BCS100K-B-HM",
        "mfr": "科华数能",
        "rated_power_mw": 0.1,
        "efficiency": 98.8,
        "ac_voltage": "400V",
        "dc_voltage_range": "600-1000V",
        "max_dc_current": 180,
        "frequency_range": "45-55Hz",
        "dimensions": "600x900x295mm",
        "weight": 96,
        "cooling": "智能风冷",
        "aux_run": 0.6,
        "aux_standby": 0.1,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "IEC 62477"]',
        "unit_price": 4.2,
        "remarks": "科华模块化储能变流器100kW"
    },
    {
        "model": "BCS200K-B-HM",
        "mfr": "科华数能",
        "rated_power_mw": 0.2,
        "efficiency": 99.0,
        "ac_voltage": "690V",
        "dc_voltage_range": "1000-1500V",
        "max_dc_current": 220,
        "frequency_range": "45-55Hz",
        "dimensions": "600x900x295mm",
        "weight": 95,
        "cooling": "智能风冷",
        "aux_run": 1.0,
        "aux_standby": 0.2,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "IEC 62477"]',
        "unit_price": 8.0,
        "remarks": "科华模块化储能变流器200kW"
    },
    {
        "model": "PCS-1250K",
        "mfr": "科华数能",
        "rated_power_mw": 1.25,
        "efficiency": 99.0,
        "ac_voltage": "550V",
        "dc_voltage_range": "800-1500V",
        "max_dc_current": 1754,
        "frequency_range": "45-55Hz",
        "dimensions": "1200x1000x2200mm",
        "weight": 1500,
        "cooling": "智能风冷",
        "aux_run": 4.5,
        "aux_standby": 1.0,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "IEC 62477"]',
        "unit_price": 38.0,
        "remarks": "科华1.25MW储能变流器"
    },
    {
        "model": "PCS-1500K",
        "mfr": "科华数能",
        "rated_power_mw": 1.5,
        "efficiency": 99.0,
        "ac_voltage": "600V",
        "dc_voltage_range": "900-1500V",
        "max_dc_current": 1870,
        "frequency_range": "45-55Hz",
        "dimensions": "1400x1000x2200mm",
        "weight": 1700,
        "cooling": "智能风冷",
        "aux_run": 5.5,
        "aux_standby": 1.2,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "IEC 62477"]',
        "unit_price": 45.0,
        "remarks": "科华1.5MW储能变流器"
    },
    {
        "model": "PCS-1725K",
        "mfr": "科华数能",
        "rated_power_mw": 1.725,
        "efficiency": 99.0,
        "ac_voltage": "690V",
        "dc_voltage_range": "1000-1500V",
        "max_dc_current": 1936,
        "frequency_range": "45-55Hz",
        "dimensions": "1400x1000x2200mm",
        "weight": 1800,
        "cooling": "智能风冷",
        "aux_run": 6.0,
        "aux_standby": 1.5,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "IEC 62477"]',
        "unit_price": 50.0,
        "remarks": "科华1.725MW储能变流器"
    },
    {
        "model": "2.5MW液冷PCS",
        "mfr": "科华数能",
        "rated_power_mw": 2.5,
        "efficiency": 99.0,
        "ac_voltage": "690V",
        "dc_voltage_range": "1000-1500V",
        "max_dc_current": 3000,
        "frequency_range": "45-55Hz",
        "dimensions": "1200x900x2000mm",
        "weight": 1400,
        "cooling": "液冷",
        "aux_run": 5.0,
        "aux_standby": 1.2,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "GB/T 34133", "GB/T 36276", "IEC 62477"]',
        "unit_price": 55.0,
        "remarks": "科华2.5MW液冷储能变流器，S³-EStation 2.0系统专用"
    },
    # ==================== 上能电气 PCS ====================
    {
        "model": "EH-500K-HB-UD",
        "mfr": "上能电气",
        "rated_power_mw": 0.5,
        "efficiency": 99.0,
        "ac_voltage": "400V",
        "dc_voltage_range": "600-1500V",
        "max_dc_current": 900,
        "frequency_range": "45-55Hz",
        "dimensions": "800x800x1800mm",
        "weight": 600,
        "cooling": "强制风冷",
        "aux_run": 2.0,
        "aux_standby": 0.5,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "IEC 62477"]',
        "unit_price": 15.0,
        "remarks": "上能电气500kW储能变流器"
    },
    {
        "model": "EH-630K-HB-UD",
        "mfr": "上能电气",
        "rated_power_mw": 0.63,
        "efficiency": 99.0,
        "ac_voltage": "400V",
        "dc_voltage_range": "600-1500V",
        "max_dc_current": 1100,
        "frequency_range": "45-55Hz",
        "dimensions": "800x800x1800mm",
        "weight": 650,
        "cooling": "强制风冷",
        "aux_run": 2.5,
        "aux_standby": 0.5,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "IEC 62477"]',
        "unit_price": 18.0,
        "remarks": "上能电气630kW储能变流器"
    },
    {
        "model": "EH-1000K-HB-UD",
        "mfr": "上能电气",
        "rated_power_mw": 1.0,
        "efficiency": 99.0,
        "ac_voltage": "690V",
        "dc_voltage_range": "800-1500V",
        "max_dc_current": 1443,
        "frequency_range": "45-55Hz",
        "dimensions": "1000x900x2000mm",
        "weight": 900,
        "cooling": "强制风冷",
        "aux_run": 3.5,
        "aux_standby": 0.8,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "IEC 62477"]',
        "unit_price": 28.0,
        "remarks": "上能电气1MW储能变流器"
    },
    {
        "model": "EH-1250K-HB-UD",
        "mfr": "上能电气",
        "rated_power_mw": 1.25,
        "efficiency": 99.0,
        "ac_voltage": "690V",
        "dc_voltage_range": "800-1500V",
        "max_dc_current": 1667,
        "frequency_range": "45-55Hz",
        "dimensions": "1100x900x2000mm",
        "weight": 1000,
        "cooling": "强制风冷",
        "aux_run": 4.5,
        "aux_standby": 1.0,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "IEC 62477"]',
        "unit_price": 35.0,
        "remarks": "上能电气1.25MW储能变流器"
    },
    {
        "model": "EH-1500K-HB-UD",
        "mfr": "上能电气",
        "rated_power_mw": 1.5,
        "efficiency": 99.0,
        "ac_voltage": "690V",
        "dc_voltage_range": "900-1500V",
        "max_dc_current": 1870,
        "frequency_range": "45-55Hz",
        "dimensions": "1200x1000x2200mm",
        "weight": 1200,
        "cooling": "强制风冷",
        "aux_run": 5.0,
        "aux_standby": 1.2,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "IEC 62477"]',
        "unit_price": 42.0,
        "remarks": "上能电气1.5MW储能变流器"
    },
    {
        "model": "EH-1725K-HB-UD",
        "mfr": "上能电气",
        "rated_power_mw": 1.725,
        "efficiency": 99.0,
        "ac_voltage": "690V",
        "dc_voltage_range": "1000-1500V",
        "max_dc_current": 1936,
        "frequency_range": "45-55Hz",
        "dimensions": "725x2350x2150mm",
        "weight": 1100,
        "cooling": "温控强制风冷",
        "aux_run": 5.5,
        "aux_standby": 1.5,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "IEC 62477"]',
        "unit_price": 48.0,
        "remarks": "上能电气1.725MW储能变流器，三电平拓扑"
    },
    {
        "model": "EH-2000K-HA-UD",
        "mfr": "上能电气",
        "rated_power_mw": 2.0,
        "efficiency": 99.0,
        "ac_voltage": "690V",
        "dc_voltage_range": "1000-1500V",
        "max_dc_current": 2222,
        "frequency_range": "45-55Hz",
        "dimensions": "1200x1100x2400mm",
        "weight": 1400,
        "cooling": "温控强制风冷",
        "aux_run": 6.5,
        "aux_standby": 1.8,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "IEC 62477"]',
        "unit_price": 55.0,
        "remarks": "上能电气2MW储能变流器，IGBT7技术，高功率密度"
    },
    {
        "model": "EH-2500K-HA-UD",
        "mfr": "上能电气",
        "rated_power_mw": 2.5,
        "efficiency": 99.0,
        "ac_voltage": "690V",
        "dc_voltage_range": "1000-1500V",
        "max_dc_current": 2885,
        "frequency_range": "45-55Hz",
        "dimensions": "1400x1200x2500mm",
        "weight": 1800,
        "cooling": "温控强制风冷",
        "aux_run": 8.0,
        "aux_standby": 2.0,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "IEC 62477"]',
        "unit_price": 68.0,
        "remarks": "上能电气2.5MW储能变流器"
    },
    {
        "model": "400kW组串式PCS",
        "mfr": "上能电气",
        "rated_power_mw": 0.4,
        "efficiency": 98.5,
        "ac_voltage": "400V",
        "dc_voltage_range": "600-1500V",
        "max_dc_current": 715,
        "frequency_range": "45-55Hz",
        "dimensions": "900x800x1800mm",
        "weight": 700,
        "cooling": "智能液冷",
        "aux_run": 2.0,
        "aux_standby": 0.5,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "IEC 62477", "UL 1741"]',
        "unit_price": 18.0,
        "remarks": "上能电气400kW组串式储能变流器，适配600+Ah大电芯"
    },
    # ==================== 其他厂商 PCS ====================
    {
        "model": "PowerTitan 5.0MW PCS",
        "mfr": "阳光电源",
        "rated_power_mw": 5.0,
        "efficiency": 99.3,
        "ac_voltage": "690V",
        "dc_voltage_range": "900-1500V",
        "max_dc_current": 6250,
        "frequency_range": "45-55Hz",
        "dimensions": "2000x1200x2600mm",
        "weight": 3000,
        "cooling": "全液冷碳化硅",
        "aux_run": 12.0,
        "aux_standby": 3.0,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "GB/T 34133", "GB/T 36276", "IEC 62477"]',
        "unit_price": 120.0,
        "remarks": "阳光电源5MW储能变流器，PowerTitan3.0系统，碳化硅技术"
    },
    {
        "model": "GridForm-2500K",
        "mfr": "阳光电源",
        "rated_power_mw": 2.5,
        "efficiency": 99.0,
        "ac_voltage": "690V",
        "dc_voltage_range": "1000-1500V",
        "max_dc_current": 3000,
        "frequency_range": "45-55Hz",
        "dimensions": "1200x900x2100mm",
        "weight": 1300,
        "cooling": "智能液冷",
        "aux_run": 5.0,
        "aux_standby": 1.2,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "GB/T 34133", "GB/T 36276"]',
        "unit_price": 52.0,
        "remarks": "阳光电源构网型2.5MW储能变流器"
    },
    {
        "model": "GridForm-5000K",
        "mfr": "阳光电源",
        "rated_power_mw": 5.0,
        "efficiency": 99.0,
        "ac_voltage": "690V",
        "dc_voltage_range": "1000-1500V",
        "max_dc_current": 6250,
        "frequency_range": "45-55Hz",
        "dimensions": "1800x1100x2600mm",
        "weight": 2800,
        "cooling": "智能液冷",
        "aux_run": 10.0,
        "aux_standby": 2.5,
        "status": "mass-production",
        "certifications": '["GB/T 34120", "GB/T 34133", "GB/T 36276"]',
        "unit_price": 95.0,
        "remarks": "阳光电源构网型5MW储能变流器"
    },
]


def sync_pcs_products():
    """同步PCS产品数据到数据库"""
    with app.app_context():
        print("=" * 60)
        print("PCS产品库同步开始")
        print("=" * 60)
        
        # 检查现有数据
        existing_count = PCS_LIBRARY.query.count()
        print(f"当前数据库中PCS产品数量: {existing_count}")
        
        # 统计各厂商数量
        manufacturers = {}
        for p in PCS_PRODUCTS:
            mfr = p['mfr']
            manufacturers[mfr] = manufacturers.get(mfr, 0) + 1
        
        print("\n待导入PCS产品分布:")
        for mfr, count in manufacturers.items():
            print(f"  - {mfr}: {count}款")
        print(f"  - 总计: {len(PCS_PRODUCTS)}款")
        
        # 导入数据
        imported = 0
        updated = 0
        skipped = 0
        
        for product in PCS_PRODUCTS:
            # 生成唯一ID
            product_id = f"{product['mfr']}_{product['model']}".replace("-", "_").replace(" ", "_")
            
            # 检查是否已存在
            existing = PCS_LIBRARY.query.filter_by(model=product['model'], mfr=product['mfr']).first()
            
            if existing:
                # 更新现有记录
                existing.rated_power_mw = product['rated_power_mw']
                existing.efficiency = product['efficiency']
                existing.ac_voltage = product['ac_voltage']
                existing.dc_voltage_range = product['dc_voltage_range']
                existing.max_dc_current = product['max_dc_current']
                existing.frequency_range = product['frequency_range']
                existing.dimensions = product['dimensions']
                existing.weight = product['weight']
                existing.cooling = product['cooling']
                existing.aux_run = product['aux_run']
                existing.aux_standby = product['aux_standby']
                existing.status = product['status']
                existing.certifications = product['certifications']
                existing.unit_price = product['unit_price']
                existing.remarks = product['remarks']
                updated += 1
                print(f"  [更新] {product['mfr']} {product['model']}")
            else:
                # 创建新记录
                new_product = PCS_LIBRARY(
                    id=product_id,
                    model=product['model'],
                    mfr=product['mfr'],
                    rated_power_mw=product['rated_power_mw'],
                    efficiency=product['efficiency'],
                    ac_voltage=product['ac_voltage'],
                    dc_voltage_range=product['dc_voltage_range'],
                    max_dc_current=product['max_dc_current'],
                    frequency_range=product['frequency_range'],
                    dimensions=product['dimensions'],
                    weight=product['weight'],
                    cooling=product['cooling'],
                    aux_run=product['aux_run'],
                    aux_standby=product['aux_standby'],
                    status=product['status'],
                    certifications=product['certifications'],
                    unit_price=product['unit_price'],
                    remarks=product['remarks'],
                )
                db.session.add(new_product)
                imported += 1
                print(f"  [新增] {product['mfr']} {product['model']}")
        
        try:
            db.session.commit()
            print("\n" + "=" * 60)
            print("同步完成!")
            print(f"  - 新增: {imported}款")
            print(f"  - 更新: {updated}款")
            print(f"  - 总计: {PCS_LIBRARY.query.count()}款PCS产品")
            print("=" * 60)
            
            # 按厂商统计
            print("\n数据库PCS产品统计:")
            for mfr in ['阳光电源', '华为', '科华数能', '上能电气']:
                count = PCS_LIBRARY.query.filter_by(mfr=mfr).count()
                print(f"  - {mfr}: {count}款")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n同步失败: {str(e)}")
            raise


if __name__ == "__main__":
    sync_pcs_products()
