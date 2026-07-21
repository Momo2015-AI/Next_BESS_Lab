"""
编排层 (Orchestrator)

从调研表到完整方案的端到端编排：
  1. DesignEngine.auto_design() → 3-5 个候选方案
  2. 串行: SimulationEngine + FinancialEngine
  3. 按目标函数排序 → 推荐方案
  4. 可选: 自动保存为 ProjectVersion
"""

import json
import logging
import uuid
from datetime import datetime, timezone

from services.design.engine import DesignEngine

logger = logging.getLogger(__name__)


def run_full_workflow(
    survey_params: dict,
    strategy: str = "economic",
    target_metric: str = "lcos",
    project_id: str = None,
    user_id: str = None,
) -> dict:
    """
    从调研表输入到完整方案输出的端到端编排

    Args:
        survey_params: 调研表参数（ratedEnergy, totalPower, duration, temperature, ...）
        strategy: 方案策略 (economic/balanced/flexible/manufacturer)
        target_metric: 排序指标 (lcos/irr/npv/capex)
        project_id: 可选，项目ID（传入时自动保存为 ProjectVersion）
        user_id: 可选，用户ID（版本创建者）

    Returns:
        { strategy, solutions: [...], recommendation: {...}, pipeline_summary: {...},
          saved_versions: [...] }  # 仅当 project_id 传入时有 saved_versions
    """
    logger.info(f"编排层启动: strategy={strategy}, target_metric={target_metric}")

    # 0. 输入验证
    design_engine = DesignEngine()
    validation_errors = design_engine.validate_input(survey_params)
    if validation_errors:
        err_msgs = [f"{e['field']}: {e['error']}" for e in validation_errors]
        return {"error": f"参数验证失败: {'; '.join(err_msgs)}", "solutions": [], "recommendation": None}

    # 1. 设计引擎: 生成 3-5 个候选方案
    design_result = design_engine.run(survey_params=survey_params, strategy=strategy)
    solutions = design_result.get("solutions", [])

    if not solutions:
        return {"error": "无法生成设计方案，请检查产品库数据", "solutions": [], "recommendation": None}

    # 2. 为每个方案执行仿真 + 财务
    results = []
    for design in solutions:
        try:
            # 2a. 仿真引擎
            sim_result = _run_simulation(design, survey_params)

            # 2b. 财务引擎
            fin_result = _run_financial(sim_result, design, survey_params)

            # 2c. 组装
            result = {
                "design": design,
                "simulation": sim_result,
                "financial": fin_result,
                "score": _extract_score(fin_result, target_metric),
            }
            results.append(result)

        except Exception as e:
            logger.warning(f"方案 {design.get('id')} 计算失败: {e}")
            results.append(
                {
                    "design": design,
                    "simulation": None,
                    "financial": None,
                    "score": float("inf"),
                    "error": str(e),
                }
            )

    # 3. 按目标函数排序
    results.sort(key=lambda r: r.get("score", float("inf")))

    return {
        "strategy": strategy,
        "target_metric": target_metric,
        "solutions": results,
        "recommendation": results[0] if results else None,
        "pipeline_summary": {
            "total_solutions": len(results),
            "successful": sum(1 for r in results if r.get("financial") is not None),
            "failed": sum(1 for r in results if r.get("error")),
        },
    }


def save_workflow_to_versions(project_id: str, workflow_result: dict, user_id: str = None) -> list:
    """
    将工作流结果保存为 ProjectVersion 记录

    为每个成功的方案创建一个 ProjectVersion，
    config_data 存储完整的 design + simulation + financial 数据。

    Args:
        project_id: 项目ID
        workflow_result: run_full_workflow() 的返回结果
        user_id: 创建者用户ID

    Returns:
        [{"version_id": "...", "version_num": N, "name": "..."}, ...]
    """
    try:
        from database import ProjectVersion
        from database import db as _db

        # 获取当前最大版本号
        latest = (
            ProjectVersion.query.filter_by(project_id=project_id).order_by(ProjectVersion.version_num.desc()).first()
        )
        next_num = (latest.version_num + 1) if latest else 1

        saved = []
        for solution in workflow_result.get("solutions", []):
            if solution.get("error"):
                continue  # 跳过失败方案

            design = solution.get("design", {})
            strategy_type = design.get("strategy_type", "unknown")
            fin_metrics = (solution.get("financial", {}) or {}).get("metrics", {})
            lcos = fin_metrics.get("lcos", fin_metrics.get("lcoe", "N/A"))
            irr = fin_metrics.get("projectIrr", fin_metrics.get("irr", "N/A"))

            version = ProjectVersion(
                id=str(uuid.uuid4()),
                project_id=project_id,
                version_num=next_num,
                name=f"{strategy_type}_v{next_num}",
                description=(
                    f"{strategy_type}方案 — LCOS: {lcos}, IRR: {irr}%"
                    if lcos != "N/A"
                    else f"{strategy_type}方案 v{next_num}"
                ),
                config_data=json.dumps(solution, default=str),
                is_active=(next_num == 1),  # 第一个版本默认激活
                created_by=user_id,
                status="draft",
                created_at=datetime.now(timezone.utc),
            )
            _db.session.add(version)
            saved.append(
                {
                    "version_id": version.id,
                    "version_num": next_num,
                    "name": version.name,
                }
            )
            next_num += 1

        _db.session.commit()
        logger.info(f"已保存 {len(saved)} 个方案版本到项目 {project_id}")
        return saved

    except ImportError:
        logger.warning("无法导入数据库模块，跳过版本保存")
        return []
    except Exception as e:
        logger.error(f"保存版本失败: {e}")
        try:
            _db.session.rollback()
        except Exception:
            pass
        return []


def _run_simulation(design: dict, survey_params: dict) -> dict:
    """执行仿真引擎"""
    try:
        from services.simulation.engine import SimulationEngine

        engine = SimulationEngine()
        return engine.run(design_output=design, survey_params=survey_params)
    except ImportError:
        # 回退到旧 pipeline
        from services.pipeline import calculate_full_pipeline

        params = _design_to_system_params(design, survey_params)
        return calculate_full_pipeline(params)


def _run_financial(sim_result: dict, design: dict, survey_params: dict) -> dict:
    """执行财务引擎"""
    try:
        from services.financial.engine import FinancialEngine

        engine = FinancialEngine()
        return engine.run(simulation_output=sim_result, design_output=design, survey_params=survey_params)
    except ImportError:
        # 回退到旧 financial
        from services.pipeline import calculate_financial_metrics

        total_ac = sim_result.get("totalAcUsable", [0] * 26) if sim_result else [0] * 26
        return calculate_financial_metrics(total_ac)


def _design_to_system_params(design: dict, survey_params: dict) -> dict:
    """将设计方案转为 systemParams 格式"""
    return {
        "ratedEnergy": design.get("container", {}).get("ratedEnergyMWh", 5),
        "initContainerQty": design.get("containerQty", 10),
        "initPcsQty": design.get("pcsQty", 10),
        "pcsPower": design.get("pcs", {}).get("ratedPowerMW", 2.5),
        "duration": design.get("duration", 2),
        "cyclesPerDay": survey_params.get("cyclesPerDay", 1),
        "temperature": survey_params.get("temperature", 25),
        "dod": survey_params.get("dod", 90),
        "cRate": survey_params.get("cRate", 0.5),
        "acEfficiency": design.get("efficiencyChain", {}).get("systemRTE", 97.03),
        "bessAuxRun": design.get("auxPower", {}).get("bessAuxRun", 18.124),
        "bessAuxStandby": design.get("auxPower", {}).get("bessAuxStandby", 3.5),
        "pcsAuxRun": design.get("auxPower", {}).get("pcsAuxRun", 6.5),
        "pcsAuxStandby": design.get("auxPower", {}).get("pcsAuxStandby", 1.0),
        "auxPowerMode": survey_params.get("auxPowerMode", design.get("auxPowerMode", "manual")),
        "ambientTemp": survey_params.get("ambientTemp", survey_params.get("tempAvg", design.get("ambientTemp", 25))),
        "coolingType": survey_params.get("coolingType", design.get("coolingType", "liquid")),
        "efficiencyFactors": survey_params.get("efficiencyFactors"),
        "requiredEnergy": survey_params.get("requiredEnergy", 240),
    }


def _extract_score(fin_result: dict, metric: str) -> float:
    """提取排序分数"""
    if not fin_result:
        return float("inf")

    metrics = fin_result.get("metrics", fin_result)
    if metric == "lcos":
        return float(metrics.get("lcos", metrics.get("lcoe", float("inf"))))
    elif metric == "irr":
        irr = float(metrics.get("irr", metrics.get("projectIrr", 0)))
        return -irr  # IRR 越高越好，取负以便排序
    elif metric == "npv":
        npv = float(metrics.get("npv", 0))
        return -npv
    elif metric == "capex":
        return float(metrics.get("capex", metrics.get("totalCapex", float("inf"))))
    elif metric == "payback":
        pb = float(metrics.get("payback", float("inf")))
        return pb
    else:
        return float(metrics.get("lcos", metrics.get("lcoe", float("inf"))))


def run_what_if(base_design: dict, adjustments: dict, survey_params: dict) -> dict:
    """
    What-If 假设分析

    Args:
        base_design: 基准设计方案
        adjustments: 调整参数 {"temperature": 45, "dod": 85, ...}
        survey_params: 调研表参数

    Returns:
        { base_result, adjusted_result, delta }
    """
    # 基准方案结果
    base_sim = _run_simulation(base_design, survey_params)
    base_fin = _run_financial(base_sim, base_design, survey_params)

    # 调整后参数
    adjusted_params = {**survey_params, **adjustments}

    # 调整后方案（重新设计）
    adjusted_design_result = DesignEngine().run(survey_params=adjusted_params, strategy="economic")
    adjusted_design = adjusted_design_result.get("recommendation", {})
    if not adjusted_design:
        adjusted_design = base_design

    # 用调整后参数仿真
    adjusted_sim = _run_simulation(adjusted_design, adjusted_params)
    adjusted_fin = _run_financial(adjusted_sim, adjusted_design, adjusted_params)

    return {
        "adjustments": adjustments,
        "base": {
            "design": base_design,
            "simulation": base_sim,
            "financial": base_fin,
        },
        "adjusted": {
            "design": adjusted_design,
            "simulation": adjusted_sim,
            "financial": adjusted_fin,
        },
        "delta": _compute_delta(base_fin, adjusted_fin),
    }


def _compute_delta(base_fin: dict, adjusted_fin: dict) -> dict:
    """计算两个方案的差异"""
    if not base_fin or not adjusted_fin:
        return {}
    bm = base_fin.get("metrics", base_fin)
    am = adjusted_fin.get("metrics", adjusted_fin)
    delta = {}
    for key in ["irr", "projectIrr", "npv", "lcos", "lcoe", "payback"]:
        try:
            bv = float(bm.get(key, 0)) if bm.get(key) is not None else 0
            av = float(am.get(key, 0)) if am.get(key) is not None else 0
        except (ValueError, TypeError):
            delta[key] = None
            continue
        if bv != 0:
            delta[key] = round((av - bv) / abs(bv) * 100, 2)
        else:
            delta[key] = round(av - bv, 2)
    return delta
