from flask import Blueprint, current_app, request

from services.exchange_rate import get_all_rates, get_rate, refresh_all_rates
from utils.api_response import error_response, success_response

exchange_rate_bp = Blueprint("exchange_rate", __name__)


@exchange_rate_bp.route("/api/exchange-rates/all", methods=["GET"])
def list_all_rates():
    try:
        items, updated_str = get_all_rates()
        return success_response(data={"rates": items, "date": updated_str})
    except Exception as e:
        current_app.logger.error(f"获取汇率失败: {e}", exc_info=True)
        return error_response("获取汇率失败，请重试", 500)


@exchange_rate_bp.route("/api/exchange-rates/latest", methods=["GET"])
def get_latest_rate():
    currency = request.args.get("currency", "").upper()
    if not currency:
        return error_response("请指定 currency 参数", 400)

    result = get_rate(currency)
    if result is None:
        return error_response(f"不支持的货币: {currency}", 400)

    rate_info, updated_str = result
    return success_response(data={
        "rate": rate_info["rate"],
        "source": rate_info["source"],
        "date": updated_str,
        "currency": currency,
        "base": "USD"
    })


@exchange_rate_bp.route("/api/exchange-rates/refresh", methods=["POST"])
def refresh_rates():
    try:
        items, updated_str = refresh_all_rates()
        return success_response(data={"rates": items, "date": updated_str}, message="汇率已刷新")
    except Exception as e:
        current_app.logger.error(f"刷新汇率失败: {e}", exc_info=True)
        return error_response("刷新汇率失败，请重试", 500)
