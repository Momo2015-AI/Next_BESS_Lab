"""
编排层 API 路由

端到端一键方案：调研表 → 设计引擎 → 仿真引擎 → 财务引擎
支持 What-If 假设分析
"""

from flask import Blueprint, request

from routes.auth import token_required
from services.orchestrator import run_full_workflow, run_what_if, save_workflow_to_versions
from utils.api_response import error_response, success_response

orchestrator_bp = Blueprint("orchestrator", __name__)


@orchestrator_bp.route("/api/workflow/full", methods=["POST"])
@token_required
def full_workflow():
    """端到端一键方案

    Request Body:
        {
            "survey_params": {
                "ratedEnergy": 100,     // 目标储能容量 (MWh)
                "totalPower": 50,       // 目标功率 (MW)
                "duration": 2,          // 持续时长 (h)
                "temperature": 25,      // 运行温度 (°C)
                "cyclesPerDay": 1,      // 每日循环次数
                "dod": 90,              // 放电深度 (%)
                "cRate": 0.5,           // 充放电倍率
                "location": "china",    // 项目地点（用于收入模型选择）
                "requiredEnergy": 240   // 每日需满足能量 (MWh)
            },
            "strategy": "economic",         // economic|balanced|flexible|manufacturer
            "target_metric": "lcos",        // lcos|irr|npv|capex|payback
            "manufacturer": null            // 指定厂家（可选）
        }

    Returns:
        {
            strategy, target_metric,
            solutions: [{ design, simulation, financial, score }, ...],
            recommendation: {...},
            pipeline_summary: { total_solutions, successful, failed }
        }
    """
    data = request.get_json()
    if not data:
        return error_response("无效的请求数据", 400)

    survey_params = data.get("survey_params", {})
    if not survey_params:
        return error_response("缺少 survey_params 参数", 400)

    strategy = data.get("strategy", "economic")
    target_metric = data.get("target_metric", "lcos")
    project_id = data.get("project_id")
    user = request.current_user
    user_id = user.id if user else None

    try:
        result = run_full_workflow(
            survey_params=survey_params,
            strategy=strategy,
            target_metric=target_metric,
        )

        # 如果指定了 project_id，自动保存方案版本
        saved_versions = None
        if project_id:
            saved_versions = save_workflow_to_versions(
                project_id=project_id,
                workflow_result=result,
                user_id=user_id,
            )
            result["saved_versions"] = saved_versions

        return success_response(
            data=result,
            message=f"编排完成: {result.get('pipeline_summary', {}).get('successful', 0)}/{result.get('pipeline_summary', {}).get('total_solutions', 0)} 方案成功",
        )
    except Exception as e:
        return error_response(f"编排执行失败: {str(e)}", 500)


@orchestrator_bp.route("/api/workflow/what-if", methods=["POST"])
@token_required
def what_if_analysis():
    """What-If 假设分析

    Request Body:
        {
            "base_design": { container, pcs, containerQty, ... },
            "adjustments": { "temperature": 45, "dod": 85, ... },
            "survey_params": { ratedEnergy, totalPower, ... }
        }

    Returns:
        {
            adjustments,
            base: { design, simulation, financial },
            adjusted: { design, simulation, financial },
            delta: { irr: +2.5%, npv: -50000, ... }
        }
    """
    data = request.get_json()
    if not data:
        return error_response("无效的请求数据", 400)

    base_design = data.get("base_design")
    if not base_design:
        return error_response("缺少 base_design 参数", 400)

    adjustments = data.get("adjustments", {})
    if not adjustments:
        return error_response("缺少 adjustments 参数", 400)

    survey_params = data.get("survey_params", {})

    try:
        result = run_what_if(
            base_design=base_design,
            adjustments=adjustments,
            survey_params=survey_params,
        )
        return success_response(data=result, message="What-If 分析完成")
    except Exception as e:
        return error_response(f"What-If 分析失败: {str(e)}", 500)


@orchestrator_bp.route("/api/workflow/metrics", methods=["GET"])
@token_required
def list_target_metrics():
    """获取可用的排序指标"""
    return success_response(
        data={
            "metrics": [
                {"key": "lcos", "label": "LCOS", "description": "平准化储能成本（越低越好）"},
                {"key": "irr", "label": "IRR", "description": "内部收益率（越高越好）"},
                {"key": "npv", "label": "NPV", "description": "净现值（越高越好）"},
                {"key": "capex", "label": "CAPEX", "description": "总投资成本（越低越好）"},
                {"key": "payback", "label": "Payback", "description": "投资回收期（越短越好）"},
            ]
        }
    )
