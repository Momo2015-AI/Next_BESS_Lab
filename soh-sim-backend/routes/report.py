"""
PDF 报告生成 API 路由
支持技术报告（系统配置 + 25年容量表）和设备清单 BOM 导出

本路由只负责 HTTP 协议、鉴权与租户隔离，PDF/图表构建与数据回填逻辑统一下沉到 services/report.py。
"""

import json
from datetime import datetime

from flask import Blueprint, current_app, make_response, request
from sqlalchemy.orm import selectinload

from database import Project, Simulation
from routes.auth import token_required
from services.report import (
    CHART_BUILDERS,
    build_bom_report,
    build_technical_report,
    register_chinese_font,
    supplement_bom_data,
    supplement_chart_data,
    supplement_technical_data,
)
from utils.api_response import error_response, success_response

report_bp = Blueprint("report", __name__)


def _enforce_project_tenant(project_id, user):
    """校验 project 归属当前租户，返回 (project, error_response)。"""
    if not project_id:
        return None, None
    project = Project.query.get(project_id)
    if project and user and project.tenant_id != user.tenant_id:
        return None, error_response("无权访问该项目", status_code=403)
    return project, None


def _enforce_simulation_tenant(simulation_id, user):
    """校验 simulation 关联 project 归属当前租户，返回 (ok, error_response)。"""
    if not simulation_id:
        return True, None
    simulation = Simulation.query.options(selectinload(Simulation.project)).get(simulation_id)
    if simulation and simulation.project_id:
        if simulation.project and user and simulation.project.tenant_id != user.tenant_id:
            return False, error_response("无权访问该仿真", status_code=403)
    return True, None


@report_bp.route("/api/report/technical", methods=["POST"])
@token_required
def export_technical_report():
    """
    导出技术报告 PDF

    请求体：前端计算数据（params, results, soh, rte 等）
    支持两种模式：
      1. 前端传完整数据（无 project_id）
      2. 从数据库读取（有 project_id + simulation_id）
    """
    register_chinese_font()

    data = request.get_json()
    if not data:
        return error_response("Invalid request data", status_code=400)

    user = request.current_user
    project_id = data.get("project_id")
    simulation_id = data.get("simulation_id")

    # 租户隔离
    _, err = _enforce_project_tenant(project_id, user)
    if err:
        return err
    ok, err = _enforce_simulation_tenant(simulation_id, user)
    if not ok:
        return err

    # 从数据库补充数据（service 层只做数据回填，不做租户校验）
    data = supplement_technical_data(data, user)

    try:
        pdf_buf = build_technical_report(data)
    except Exception:
        current_app.logger.error("技术报告生成失败", exc_info=True)
        return error_response("PDF 生成失败，请重试", status_code=500)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    response = make_response(pdf_buf.getvalue())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"attachment; filename=technical_report_{timestamp}.pdf"

    return response


@report_bp.route("/api/report/bom", methods=["POST"])
@token_required
def export_bom_report():
    """
    导出设备清单 BOM PDF

    请求体：产品选型 + 数量 + 参数
    """
    register_chinese_font()

    data = request.get_json()
    if not data:
        return error_response("Invalid request data", status_code=400)

    user = request.current_user
    project_id = data.get("project_id")

    # 租户隔离
    _, err = _enforce_project_tenant(project_id, user)
    if err:
        return err

    # 从数据库补充选型数据
    data = supplement_bom_data(data, user)

    try:
        pdf_buf = build_bom_report(data)
    except Exception:
        current_app.logger.error("BOM报告生成失败", exc_info=True)
        return error_response("PDF 生成失败，请重试", status_code=500)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    response = make_response(pdf_buf.getvalue())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"attachment; filename=bom_report_{timestamp}.pdf"

    return response


@report_bp.route("/api/report/charts/<chart_type>", methods=["POST"])
@token_required
def export_plotly_chart(chart_type):
    """
    生成 Plotly 交互式图表

    路径参数 chart_type:
      - soh_rte_curve:    25 年 SOH/RTE 衰减曲线
      - capacity_matrix:  容量矩阵热力图
      - grid_compliance:  LVRT/HVRT 电网合规曲线
      - ipp_cashflow:     IPP 现金流瀑布图

    返回: { success, html, div_id } 前端可直接 iframe 或 innerHTML 渲染
    """
    if chart_type not in CHART_BUILDERS:
        return error_response(
            f"不支持的图表类型: {chart_type}",
            message=f"可用类型: {', '.join(CHART_BUILDERS.keys())}",
            status_code=400,
        )

    data = request.get_json() or {}

    user = request.current_user
    project_id = data.get("project_id")
    simulation_id = data.get("simulation_id")

    # 租户隔离
    _, err = _enforce_project_tenant(project_id, user)
    if err:
        return err
    ok, err = _enforce_simulation_tenant(simulation_id, user)
    if not ok:
        return err

    # 从数据库补充图表数据
    data = supplement_chart_data(data)

    try:
        fig = CHART_BUILDERS[chart_type](data)
        if fig is None:
            return error_response(f"数据不足，无法生成 {chart_type} 图表", status_code=422)

        # 返回结构化图表数据（data/layout），由前端 Plotly.newPlot 渲染。
        # 不再返回 to_html() 字符串，避免 v-html 注入与 </script> 提前闭合导致的 XSS。
        plot_json = fig.to_plotly_json()
        div_id = f'plotly-{chart_type}-{datetime.now().strftime("%H%M%S")}'
        return success_response(
            data={
                "chart": {
                    "data": plot_json.get("data", []),
                    "layout": plot_json.get("layout", {}),
                    "config": {"displaylogo": False, "responsive": True},
                },
                "div_id": div_id,
            }
        )

    except Exception:
        current_app.logger.error("图表生成失败", exc_info=True)
        return error_response("图表生成失败，请重试", status_code=500)


@report_bp.route("/api/report/charts", methods=["GET"])
@token_required
def list_chart_types():
    """列出可用的图表类型"""
    return success_response(
        data={
            "chart_types": list(CHART_BUILDERS.keys()),
            "descriptions": {
                "soh_rte_curve": "25 年 SOH/RTE 衰减曲线（双轴折线）",
                "capacity_matrix": "25 年容量矩阵热力图",
                "grid_compliance": "LVRT/HVRT 电网合规曲线",
                "ipp_cashflow": "IPP 现金流瀑布图（累计 NPV）",
            },
        }
    )
