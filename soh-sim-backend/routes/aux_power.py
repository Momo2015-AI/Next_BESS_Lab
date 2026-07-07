"""
BESS辅助功耗计算API
支持储能系统直流侧、交流侧辅助功耗的精确计算
"""

from flask import Blueprint, request

from routes.auth import token_required
from services.aux_power import AUX_DEFAULTS, calculate_aux_power, validate_aux_power_params
from utils.api_response import error_response, success_response

aux_power_bp = Blueprint("aux_power", __name__)


@aux_power_bp.route("/api/aux-power/calculate", methods=["POST"])
@token_required
def calculate_aux_power_api():
    """计算辅助功耗"""
    try:
        data = request.get_json()

        is_valid, err_msg = validate_aux_power_params(data)
        if not is_valid:
            return error_response(err_msg, 400)

        result = calculate_aux_power(data)
        return success_response(data=result)
    except Exception as e:
        return error_response("计算失败，请重试", 500)


@aux_power_bp.route("/api/aux-power/defaults", methods=["GET"])
@token_required
def get_defaults():
    """获取默认参数"""
    return success_response(data=AUX_DEFAULTS)
