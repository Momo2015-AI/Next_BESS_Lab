"""
分相位非对称辅耗模型 (Phase-Aware Auxiliary Power Model)

参考 Annex 8 AuxModel: 基于实测 6 步循环数据的分相位辅耗计算。
充电相位辅耗 ≠ 放电相位辅耗（充电侧含 AC/DC 转换+冷却全开，辅耗更大）。

设计工况默认值来自 Annex 8 实测数据（0.5P @ 25℃, 5MWh 集装箱）:
- pChg = 32.5 kW/箱 (充电功率)
- pDis = 27.5 kW/箱 (放电功率)

后续可通过参数覆盖适配不同倍率/温度条件。
"""

import math

# 默认值：0.5P @ 25℃ 单箱实测功率 (kW)
PHASE_AUX_DEFAULTS = {
    "pChg_per_container_kw": 32.5,    # 充电相位单箱辅耗功率
    "pDis_per_container_kw": 27.5,    # 放电相位单箱辅耗功率
    "pTailC_per_container_kw": 28.0,  # 充电冷却尾流单箱功率 (预留)
    "pTailD_per_container_kw": 22.0,  # 放电冷却尾流单箱功率 (预留)
    "tail_duration_h": 1.5,           # 冷却尾流时长 (h) (预留)
}


def calculate_phase_aux_power(
    dc_available_mwh,       # H: 补容后直流可用容量 (MWh)
    rated_power_mw,         # P_dc: 直流侧需求功率 (MW)
    ac_aux_per_skid_mw,     # AC 辅耗每 SKID (MW), 对应 Inputs!D12
    container_count,        # 集装箱数量
    eta_dis,                # 放电单程效率 (如 0.9741)
    eta_chg,                # 充电单程效率 (如 0.9698)
    cable_eff,              # 直流电缆效率 (如 0.998)
    dc_rte,                 # 直流往返效率 K (如 0.941)
    p_chg_per_container_kw=None,   # 单箱充电辅耗 (kW), None 用默认值
    p_dis_per_container_kw=None,   # 单箱放电辅耗 (kW), None 用默认值
):
    """
    计算分相位非对称辅耗。

    返回:
        P_chg_sys: 充电相位系统辅耗 (MW)
        P_dis_sys: 放电相位系统辅耗 (MW)
        E_cycle_sys: 整循环系统辅耗能量 (MWh) — 含充+放+冷尾+待机
        t_dis: 放电工步时长 (h)
        t_chg: 充电工步时长 (h)
    """
    if p_chg_per_container_kw is None:
        p_chg_per_container_kw = PHASE_AUX_DEFAULTS["pChg_per_container_kw"]
    if p_dis_per_container_kw is None:
        p_dis_per_container_kw = PHASE_AUX_DEFAULTS["pDis_per_container_kw"]

    # 系统级分相位辅耗功率 (MW)
    # P_chg_sys = AC_aux + containers × pChg / 1000
    P_chg_sys = ac_aux_per_skid_mw + container_count * p_chg_per_container_kw / 1000.0
    # P_dis_sys = AC_aux + containers × pDis / 1000
    P_dis_sys = ac_aux_per_skid_mw + container_count * p_dis_per_container_kw / 1000.0

    sqrt_k = math.sqrt(dc_rte)

    # 放电时间 (h): J = H / (P_dc / η_dis + P_dis_sys)
    # 分母 = 直流功率需求折算到交流侧 + 放电相位辅耗
    t_dis = dc_available_mwh / (rated_power_mw / eta_dis + P_dis_sys)

    # 充电时间 (h): K = H / ((P_dc × η_chg − P_chg_sys) × √K)
    # 分母 = 净充电功率 (扣除充电辅耗) × 单程效率
    net_charge_power = rated_power_mw * eta_chg - P_chg_sys
    if net_charge_power <= 0:
        # 辅耗超过净充电功率时，设一个很大的充电时间（实际不可行）
        t_chg = float("inf")
    else:
        t_chg = dc_available_mwh / (net_charge_power * sqrt_k)

    # 整循环系统辅耗能量 (MWh): E_cycle_sys
    # 简化版 = P_chg_sys × t_chg + P_dis_sys × t_dis
    # 完整版还需加冷尾+待机，此处先按充放两相计算
    if t_chg == float("inf"):
        E_cycle_sys = float("inf")
    else:
        E_cycle_sys = P_chg_sys * t_chg + P_dis_sys * t_dis

    return {
        "P_chg_sys": round(P_chg_sys, 4),
        "P_dis_sys": round(P_dis_sys, 4),
        "E_cycle_sys": round(E_cycle_sys, 4) if E_cycle_sys != float("inf") else float("inf"),
        "t_dis": round(t_dis, 4),
        "t_chg": round(t_chg, 4) if t_chg != float("inf") else float("inf"),
        "sqrt_k": round(sqrt_k, 6),
    }
