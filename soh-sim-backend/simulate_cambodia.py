"""
柬埔寨 250MW/500MWh 电网调频 BESS 项目 — 完整仿真脚本 V2
基于招标文件 Section 2.8 + Form FUNC 参数
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.epc.thermal import FIXED_AUX_KW, calculate_cooling_power
from services.financial.calculator import calculate_full_financial
from services.pipeline import calculate_full_pipeline

# ============================================================================
# 项目参数
# ============================================================================
AMBIENT_TEMP = 32
COOLING_TYPE = "liquid"
cp = calculate_cooling_power(AMBIENT_TEMP, COOLING_TYPE)
bess_aux_run = cp["cooling_power_kw"] + FIXED_AUX_KW

print("=" * 80)
print("柬埔寨 250MW/500MWh 电网调频 BESS — 投标仿真")
print(f"环境温度 {AMBIENT_TEMP}°C, {COOLING_TYPE} 冷却, 辅耗={bess_aux_run:.2f} kW")
print("=" * 80)

system_params = {
    "ratedEnergy": 5,
    "initContainerQty": 100,  # 100×5MWh=500MWh 铭牌容量
    "initPcsQty": 50,  # 50×5MW=250MW PCS 功率
    "pcsPower": 5,
    "duration": 2,
    "cyclesPerDay": 1,
    "temperature": AMBIENT_TEMP,
    "acEfficiency": 100.0,  # RTE 值已含AC损耗, 不额外打折
    "bessAuxRun": bess_aux_run,
    "bessAuxStandby": cp["standby_power_kw"],
    "pcsAuxRun": 6.5,
    "pcsAuxStandby": 1.0,
    "requiredEnergy": 382,  # 500MWh×90%DoD×85%RTE ≈ 382MWh @ POC
    "auxPowerMode": "thermal",
    "ambientTemp": AMBIENT_TEMP,
    "coolingType": COOLING_TYPE,
    "dod": 90,
    "efficiencyFactors": None,  # 强制使用自定义RTE数组而非10因子链
}

# 使用用户自定义退化数组
# 招标要求: 8,500次后 SoH>76%, RTE≥85% @ AC side (to POC)
# LFP电池典型衰减曲线 — 前几年快，后面慢
years = 26
soh_custom = [
    100.0,
    98.5,
    97.1,
    95.8,
    94.6,
    93.5,
    92.4,
    91.4,
    90.4,
    89.5,
    88.6,
    87.8,
    87.0,
    86.2,
    85.4,
    84.7,
    84.0,
    83.3,
    82.6,
    82.0,
    81.3,
    80.7,
    80.1,
    79.5,
    78.9,
    78.3,
]
# RTE @ AC side (已含AC损耗), 招标≥85%
rte_custom = [
    86.5,
    86.4,
    86.3,
    86.2,
    86.1,
    86.0,
    85.9,
    85.8,
    85.7,
    85.6,
    85.5,
    85.4,
    85.3,
    85.2,
    85.1,
    85.0,
    85.0,
    85.0,
    85.0,
    85.0,
    85.0,
    85.0,
    85.0,
    85.0,
    85.0,
    85.0,
]

degradation = {
    "soh": soh_custom,
    "rte": rte_custom,
    "dod": [90] * years,
    "augQty": [0] * years,
}

# ============================================================================
# 执行
# ============================================================================
result = calculate_full_pipeline(system_params, degradation, {"model": "arrhenius"})
soh = result["soh"]
rte_curve = result["rte"]
total_ac_usable = result["totalAcUsable"]

# RTE 曲线已经是以 % 为单位 (efficiency_curves 返回百分比值)
# 检查实际值的范围
print(f"\nRTE range: {rte_curve[0]:.2f} ~ {rte_curve[-1]:.2f}")
print(f"SoH range: {soh[0]:.2f} ~ {soh[-1]:.2f}")
print(f"Usable Energy range: {total_ac_usable[0]:.2f} ~ {total_ac_usable[-1]:.2f} MWh")

# ============================================================================
# Functional Guarantee 表
# ============================================================================
print()
print("=" * 80)
print("FUNCTIONAL GUARANTEE (Form FUNC)")
print("250MW/500MWh GRID FORMING BESS @ Takeo Substation, Cambodia")
print("=" * 80)
print(
    f"{'Cycle':>6} | {'Year':>4} | {'SoH (%)':>8} | {'RTE (%)':>8} | {'Usable (MWh)':>13} | {'SOH>76%':>8} | {'RTE≥85%':>8}"
)
print("-" * 80)

all_soh_ok = True
all_rte_ok = True

for i in range(24):
    cycle = i * 365
    s = soh[i]
    # RTE 如果 > 1 说明是百分比 (如 85.0), 如果 < 1 说明是小数 (如 0.85)
    r = rte_curve[i]
    if r < 1.0:
        r = r * 100  # 转换为百分比
    u = total_ac_usable[i]
    soh_ok = s >= 76.0
    rte_ok = r >= 85.0
    if not soh_ok:
        all_soh_ok = False
    if not rte_ok:
        all_rte_ok = False
    print(
        f"{cycle:>6} | {i:>4} | {s:>8.2f} | {r:>8.2f} | {u:>13.2f} |  {'✅' if soh_ok else '❌'}   |  {'✅' if rte_ok else '❌'}"
    )

# Extra years
for extra in [(24, 8760), (25, 9125)]:
    i, cycle = extra
    s = soh[i]
    r = rte_curve[i]
    if r < 1.0:
        r = r * 100
    u = total_ac_usable[i]
    soh_ok = s >= 76.0
    rte_ok = r >= 85.0
    print(
        f"{cycle:>6} | {i:>4} | {s:>8.2f} | {r:>8.2f} | {u:>13.2f} |  {'✅' if soh_ok else '❌'}   |  {'✅' if rte_ok else '❌'}"
    )

print()
print(f"  SoH 全部 >76% (Cycle 0~8500): {'✅ PASS' if all_soh_ok else '❌ FAIL'}")
print(f"  RTE 全部 ≥85±0.5%: {'✅ PASS' if all_rte_ok else '❌ FAIL'}")
print(f"  Usable @ POC (Year 0): {total_ac_usable[0]:.2f} MWh  (500MWh × 90%DoD × 86.5%RTE - Aux)")

# ============================================================================
# 财务
# ============================================================================
print()
print("=" * 80)
print("财务指标")
print("=" * 80)

# 计算 CAPEX 汇总
_total_kwh = system_params["ratedEnergy"] * system_params["initContainerQty"] * 1000  # 500,000 kWh
_total_kw = system_params["pcsPower"] * system_params["initPcsQty"] * 1000  # 250,000 kW
_capex_battery = _total_kwh * 180  # $90M
_capex_pcs = _total_kw * 60  # $15M
_capex_bos = _total_kw * 80  # $20M
_capex_epc = _total_kw * 50  # $12.5M
_capex_dev = 2_000_000  # $2M

fin = calculate_full_financial(
    total_ac_usable,
    {
        "_capexInternal": {
            "equipment": _capex_battery + _capex_pcs + _capex_bos,  # $125M
            "epc": _capex_epc,  # $12.5M
            "development": _capex_dev,  # $2M
        },
        "systemParams": {
            "pcsPower": system_params["pcsPower"],
            "initContainerQty": system_params["initContainerQty"],
            "ratedEnergy": system_params["ratedEnergy"],
        },
        "opex": {"fixedOpexPerMW": 5000, "variableOpexPerMWh": 2.5, "insuranceRate": 0.5, "landLease": 150000},
        "revenue": {
            "arbitrage": {
                "enabled": True,
                "offPeakPrice": 30,  # $/MWh 谷时电价
                "peakPrice": 60,  # $/MWh 峰时电价
                "spreadCapture": 85,  # 价差捕获率(%)
                "operatingDays": 330,
            },
            "capacity": {
                "enabled": True,
                "capacityPrice": 30000,  # $/MW/年
            },
            "ancillary": {
                "enabled": True,
                "ancillaryPrice": 15000,  # $/MW/年 调频服务
            },
        },
        "financing": {"debtRatio": 70, "interestRate": 5.0, "loanTerm": 15, "repaymentType": "equal_installment"},
        "tax": {"corporateTaxRate": 20, "taxHolidayYears": 5},
        "discountRate": 7.0,
        "priceEscalation": 2.0,
    },
)
m = fin["metrics"]
for k, label in [
    ("projectIrr", "项目 IRR"),
    ("equityIrr", "权益 IRR"),
    ("npv", "NPV @7%"),
    ("lcos", "LCOS"),
    ("payback", "回收期"),
    ("roi", "ROI"),
]:
    v = m[k]
    if v is None:
        disp = "N/A"
    elif k in ("npv",):
        disp = f"${v:,.0f}"
    elif k in ("lcos",):
        disp = f"${v:.4f}/kWh"
    elif k in ("payback",):
        disp = f"{v:.1f} 年"
    else:
        disp = f"{v:.2f}%"
    print(f"  {label:>12}: {disp}")
print(f"  {'DSCR (平均)':>12}: {m['dscr']['avg']:.2f}")
print(f"  {'DSCR (最低)':>12}: {m['dscr']['min']:.2f}")

# ============================================================================
# 增补分析
# ============================================================================
print()
print("=" * 80)
print("增补分析 (招标要求: SoH<80% 时增补)")
print("=" * 80)
aug_year = next((i for i, s in enumerate(soh) if s < 80.0), None)
if aug_year:
    print(f"  ⚠ SoH 首次跌破 80%: 第 {aug_year} 年 (Cycle {aug_year*365})")
    print(f"    此时 SoH={soh[aug_year]:.2f}%, Usable={total_ac_usable[aug_year]:.2f} MWh")
else:
    print(f"  ✅ 25年内 SoH 未跌破 80%，无需增补")

# ============================================================================
# 冷却对比
# ============================================================================
print()
print("=" * 80)
print("冷却方式对比 (32°C)")
print("=" * 80)
print(f"  {'方式':>14} | {'冷却kW':>8} | {'总辅耗kW':>9} | {'COP':>5} | {'年耗电MWh':>10}")
for ct in ["forced-air", "liquid", "SiC-liquid"]:
    c = calculate_cooling_power(32, ct)
    annual = c["cooling_power_kw"] * 8760 * 0.7 / 1000  # 70% 运行时间
    print(
        f"  {ct:>14} | {c['cooling_power_kw']:>8.2f} | {c['cooling_power_kw']+FIXED_AUX_KW:>9.2f} | {c['cop']:>5.1f} | {annual:>10.0f}"
    )

# 年度能耗对比
print()
print("=" * 80)
print("年度能量核算 (Year 0)")
print("=" * 80)
from services.pipeline import calculate_energy_accounting

ea = calculate_energy_accounting(system_params, soh_custom, rte_custom, [90] * 26, [0] * 26)
print(f"  Gross:        {ea['initGross'][0]:.2f} MWh")
print(f"  Aux:          {ea['initAux'][0]:.2f} MWh")
print(f"  Net AC Usable: {ea['initAcUsable'][0]:.2f} MWh")
print(f"  Meets {system_params['requiredEnergy']} MWh: {'✅' if ea['meetsReq'][0] else '❌'}")

print()
print("=" * 80)
print("仿真完成 ✅")
print("=" * 80)
