"""
导出功能相关API路由
支持CSV格式导出
"""

from flask import Blueprint, make_response, request

from routes.auth import limiter, token_required
from utils.api_response import (
    error_response,
    paginated_response,
    success_response,
)
from services.export import (
    build_csv_output,
    build_financial_csv_output,
    make_csv_response,
    save_simulation,
    list_simulations as svc_list_simulations,
    get_simulation_detail,
)

export_bp = Blueprint("export", __name__)


@export_bp.route("/api/export/csv", methods=["POST"])
@token_required
@limiter.limit("20/minute")
def export_csv():
    """导出计算结果为CSV格式"""
    data = request.get_json()
    if not data:
        return error_response("无效的请求数据", status_code=400)

    output = build_csv_output(data)
    return make_csv_response(output, "soh_export", make_response)


@export_bp.route("/api/export/financial-csv", methods=["POST"])
@token_required
@limiter.limit("20/minute")
def export_financial_csv():
    """导出财务分析结果为CSV格式"""
    data = request.get_json()
    if not data:
        return error_response("无效的请求数据", status_code=400)

    output = build_financial_csv_output(data)
    return make_csv_response(
        output, "financial_export", make_response
    )


@export_bp.route("/api/export/simulation", methods=["POST"])
@token_required
@limiter.limit("20/minute")
def export_simulation():
    """保存完整仿真结果到数据库（含租户隔离校验）"""
    data = request.get_json()
    if not data:
        return error_response("无效的请求数据", status_code=400)

    result, error, status_code = save_simulation(
        data, request.current_user
    )
    if error:
        return error_response(error, status_code=status_code)
    return success_response(
        data={"simulation_id": result["simulation_id"]},
        message=result.get("message", ""),
        status_code=status_code,
    )


@export_bp.route("/api/simulation/list", methods=["GET"])
@token_required
def list_simulations():
    """获取仿真列表（含租户隔离过滤）"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    project_id = request.args.get("project_id")

    items, ret_page, ret_per_page, total = svc_list_simulations(
        page, per_page, project_id, request.current_user
    )
    return paginated_response(
        items=items,
        page=ret_page,
        page_size=ret_per_page,
        total=total,
    )


@export_bp.route("/api/simulation/<simulation_id>", methods=["GET"])
@token_required
def get_simulation(simulation_id):
    """获取仿真详情（含租户隔离校验）"""
    result, error, status_code = get_simulation_detail(
        simulation_id, request.current_user
    )
    if error:
        return error_response(error, status_code=status_code)
    return success_response(data=result)
