"""
BESS辅助功耗计算API
支持储能系统直流侧、交流侧辅助功耗的精确计算
"""

import math

from flask import Blueprint, jsonify, request

aux_power_bp = Blueprint("aux_power", __name__)


@aux_power_bp.route("/api/aux-power/calculate", methods=["POST"])
def calculate_aux_power():
    """
    计算辅助功耗
    POST参数:
    {
        "days": 365,           // 计算天数
        "cycles": 2,           // 每天充放电循环次数
        "hours": 2,            // 单次放电时长(h)
        "cap": 5,              // 单舱标称铭牌容量(MWh)
        "units": 62,           // 当前运行总台数
        "dcRte": 0.941,        // DC-RTE(直流往返效率)
        "pcsEff": 0.987,       // PCS充/放电效率
        "acEff": 0.975,        // 交流侧综合效率(变损/线损)
        "bRun": 20,            // 电池舱运行温控功率(kW)
        "bStd": 4,             // 电池舱待机温控功率(kW)
        "pRun": 5,             // PCS变流器运行损耗(kW)
        "pStd": 1.5,           // PCS变流器待机损耗(kW)
        "pStation": 7.2        // 站宇及主变固定自耗(kW)
    }
    """
    try:
        data = request.get_json()

        days = float(data.get("days", 365))
        cycles = float(data.get("cycles", 2))
        hours = float(data.get("hours", 2))
        cap = float(data.get("cap", 5))
        units = float(data.get("units", 62))
        dcRte = float(data.get("dcRte", 0.941))
        pcsEff = float(data.get("pcsEff", 0.987))
        acEff = float(data.get("acEff", 0.975))
        bRun = float(data.get("bRun", 20))
        bStd = float(data.get("bStd", 4))
        pRun = float(data.get("pRun", 5))
        pStd = float(data.get("pStd", 1.5))
        pStation = float(data.get("pStation", 7.2))

        # 输入参数校验
        if days < 0 or cycles < 0 or hours < 0:
            return jsonify({"success": False, "error": "天数、循环次数、时长不能为负值"}), 400
        if cap < 0 or units < 0:
            return jsonify({"success": False, "error": "容量和台数不能为负值"}), 400
        if not (0 < dcRte <= 1) or not (0 < pcsEff <= 1) or not (0 < acEff <= 1):
            return jsonify({"success": False, "error": "效率值必须在 (0, 1] 范围内"}), 400
        if bRun < 0 or bStd < 0 or pRun < 0 or pStd < 0 or pStation < 0:
            return jsonify({"success": False, "error": "功率参数不能为负值"}), 400

        sqrtRte = math.sqrt(dcRte)
        tRun = days * cycles * hours * 2
        tStd = (days * 24) - tRun

        dcTotalAux = ((tRun * bRun) + (tStd * bStd)) * units / 1000

        acTotalAux = ((tRun * pRun) + (tStd * pStd) + (days * 24 * pStation)) / 1000

        totalSystemAux = dcTotalAux + acTotalAux

        annualGrossDischarge = cap * units * sqrtRte * cycles * days * acEff * pcsEff
        annualNetDischarge = annualGrossDischarge - totalSystemAux

        singleUnitDailyKwh = (dcTotalAux * 1000) / max(units, 1) / max(days, 1)

        return jsonify(
            {
                "success": True,
                "data": {
                    "tRun": round(tRun, 1),
                    "tStd": round(tStd, 1),
                    "sqrtRte": round(sqrtRte, 4),
                    "dcTotalAux": round(dcTotalAux, 2),
                    "acTotalAux": round(acTotalAux, 2),
                    "totalSystemAux": round(totalSystemAux, 2),
                    "annualGrossDischarge": round(annualGrossDischarge, 2),
                    "annualNetDischarge": round(annualNetDischarge, 2),
                    "singleUnitDailyKwh": round(singleUnitDailyKwh, 2),
                },
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@aux_power_bp.route("/api/aux-power/defaults", methods=["GET"])
def get_defaults():
    """获取默认参数"""
    return jsonify(
        {
            "success": True,
            "data": {
                "days": 365,
                "cycles": 2,
                "hours": 2,
                "cap": 5,
                "units": 62,
                "dcRte": 0.941,
                "pcsEff": 0.987,
                "acEff": 0.975,
                "bRun": 20,
                "bStd": 4,
                "pRun": 5,
                "pStd": 1.5,
                "pStation": 7.2,
            },
        }
    )
