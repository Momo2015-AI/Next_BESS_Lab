"""导出功能业务逻辑服务层

提供 CSV 生成、仿真结果保存等核心业务，
供 routes/export.py 调用。
"""

import csv
import io
import json
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import selectinload

from database import Project, Simulation, db

MAX_ROWS = 500


def _safe_float(value, default=None):
    """安全转换为浮点数"""
    try:
        return round(float(value), 2)
    except (ValueError, TypeError):
        return value if default is None else default


def build_csv_output(data):
    """构建计算结果 CSV 内容（StringIO）。

    Args:
        data: 请求体 dict（type, results, params, soh, rte, dod, augQty）

    Returns:
        io.StringIO 输出流（已写入内容，位置在末尾）
    """
    export_type = data.get("type", "matrix")
    results = data.get("results") or {}
    params = data.get("params") or {}
    soh = data.get("soh", [])
    rte = data.get("rte", [])
    dod = data.get("dod", [])
    aug_qty = data.get("augQty", [])

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["储能电站SOH仿真计算结果导出"])
    writer.writerow(["导出时间", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    writer.writerow([])

    if export_type in ("matrix", "all"):
        N = 26
        writer.writerow(["25年生命周期矩阵"])
        writer.writerow(
            [
                "年份",
                "初始Gross(MWh)",
                "初始Aux(MWh)",
                "初始净可用(MWh)",
                "扩容Gross(MWh)",
                "扩容Aux(MWh)",
                "扩容净可用(MWh)",
                "总净可用(MWh)",
                "累计扩容数量",
                "是否满足需求",
            ]
        )

        init_gross = results.get("initGross", [])
        init_aux = results.get("initAux", [])
        init_usable = results.get("initAcUsable", [])
        aug_gross = results.get("augGross", [])
        aug_aux = results.get("augAux", [])
        aug_usable = results.get("augAcUsable", [])
        total_usable = results.get("totalAcUsable", [])
        accum_qty = results.get("augAccumQty", [])
        meets_req = results.get("meetsReq", [])

        for i in range(min(N, MAX_ROWS)):
            writer.writerow(
                [
                    i,
                    round(init_gross[i], 4) if i < len(init_gross) else 0,
                    round(init_aux[i], 4) if i < len(init_aux) else 0,
                    round(init_usable[i], 4) if i < len(init_usable) else 0,
                    round(aug_gross[i], 4) if i < len(aug_gross) else 0,
                    round(aug_aux[i], 4) if i < len(aug_aux) else 0,
                    round(aug_usable[i], 4) if i < len(aug_usable) else 0,
                    round(total_usable[i], 4) if i < len(total_usable) else 0,
                    int(accum_qty[i]) if i < len(accum_qty) else 0,
                    "是" if i < len(meets_req) and meets_req[i] else ("否" if i < len(meets_req) else ""),
                ]
            )

    if export_type in ("soh", "all"):
        writer.writerow([])
        writer.writerow(["SOH/RTE数据序列"])
        writer.writerow(["年份", "SOH(%)", "RTE(%)", "DOD(%)", "扩容数量"])

        N = min(
            max(
                len(soh) if soh else 0,
                len(rte) if rte else 0,
                len(dod) if dod else 0,
                len(aug_qty) if aug_qty else 0,
                26,
            ),
            MAX_ROWS,
        )
        if N == 0:
            N = 26

        for i in range(N):
            writer.writerow(
                [
                    i,
                    round(float(soh[i]) * 100, 2) if i < len(soh) else "",
                    round(float(rte[i]) * 100, 2) if i < len(rte) else "",
                    _safe_float(dod[i], "") if i < len(dod) else "",
                    int(aug_qty[i]) if i < len(aug_qty) else 0,
                ]
            )

    if export_type in ("params", "all"):
        writer.writerow([])
        writer.writerow(["参数配置"])
        writer.writerow(["参数名称", "参数值", "单位"])

        param_mapping = {
            "ratedEnergy": ("额定能量", "MWh"),
            "initContainerQty": ("初始集装箱数量", "个"),
            "initPcsQty": ("初始PCS数量", "个"),
            "duration": ("储能时长", "h"),
            "cyclesPerDay": ("每日循环次数", "次"),
            "acEfficiency": ("交流效率", "%"),
            "bessAuxRun": ("BESS运行辅助功耗", "kW"),
            "bessAuxStandby": ("BESS待机辅助功耗", "kW"),
            "pcsAuxRun": ("PCS运行辅助功耗", "kW"),
            "pcsAuxStandby": ("PCS待机辅助功耗", "kW"),
            "requiredEnergy": ("需求能量", "MWh"),
        }

        for key, (label, unit) in param_mapping.items():
            value = params.get(key, "")
            if value != "":
                writer.writerow([label, value, unit])

    return output


def build_financial_csv_output(data):
    """构建财务分析 CSV 内容（StringIO）。

    Args:
        data: 请求体 dict（cashflow, metrics, params）

    Returns:
        io.StringIO 输出流（已写入内容，位置在末尾）
    """
    cashflow = data.get("cashflow") or []
    metrics = data.get("metrics") or {}
    params = data.get("params") or {}

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["储能电站财务分析结果"])
    writer.writerow(["导出时间", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    writer.writerow([])

    writer.writerow(["财务指标汇总"])
    writer.writerow(["指标名称", "数值", "单位"])

    metrics_mapping = {
        "totalRevenue": ("25年总收入", "$"),
        "totalCost": ("25年总成本", "$"),
        "netCashflow": ("25年净现金流", "$"),
        "npv": ("净现值(NPV)", "$"),
        "irr": ("内部收益率(IRR)", "%"),
        "paybackYears": ("投资回收期", "年"),
        "lcos": ("储能度电成本(LCOS)", "$/MWh"),
    }

    for key, (label, unit) in metrics_mapping.items():
        value = metrics.get(key, "")
        if value != "":
            display = _safe_float(value)
            writer.writerow([label, display, unit])

    if cashflow:
        writer.writerow([])
        writer.writerow(["25年现金流明细"])
        writer.writerow(["年份", "收入", "成本", "净现金流", "累计现金流"])

        for i, cf in enumerate(cashflow):
            if i >= MAX_ROWS:
                break
            writer.writerow(
                [
                    i,
                    _safe_float(cf.get("revenue", 0), 0),
                    _safe_float(cf.get("cost", 0), 0),
                    _safe_float(cf.get("net", 0), 0),
                    _safe_float(cf.get("cumulative", 0), 0),
                ]
            )

    return output


def make_csv_response(output, filename_prefix, make_response_fn):
    """生成 CSV 下载响应。

    Args:
        output: StringIO 输出流
        filename_prefix: 文件名前缀
        make_response_fn: flask.make_response 函数

    Returns:
        Flask response object
    """
    output.seek(0)
    response = make_response_fn(output.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8-sig"
    response.headers["Content-Disposition"] = (
        f'attachment; filename={filename_prefix}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )
    return response


def save_simulation(data, current_user):
    """保存完整仿真结果到数据库（含租户隔离校验）。

    Args:
        data: 请求体 dict
        current_user: 当前登录用户（含 tenant_id）

    Returns:
        (result_dict, error_str, status_code)
    """
    project_id = data.get("project_id")
    simulation_id = data.get("simulation_id")
    user_id = data.get("user_id") or (current_user.id if current_user else None)

    # 租户隔离：验证 project_id 属于当前租户
    if project_id:
        project = Project.query.get(project_id)
        if not project:
            return None, "项目不存在", 404
        if current_user and project.tenant_id != current_user.tenant_id:
            return None, "无权访问该项目", 403

    simulation_data = {
        "params": data.get("params") or {},
        "results": data.get("results") or {},
        "soh": data.get("soh", []),
        "rte": data.get("rte", []),
        "dod": data.get("dod", []),
        "aug_qty": data.get("augQty", []),
        "financial": data.get("financial") or {},
    }

    if simulation_id:
        simulation = Simulation.query.options(selectinload(Simulation.project)).get(simulation_id)
        if simulation:
            if simulation.project_id and current_user:
                if simulation.project and simulation.project.tenant_id != current_user.tenant_id:
                    return None, "无权访问该仿真", 403
            simulation.results = json.dumps(simulation_data)
            simulation.status = "completed"
            simulation.completed_at = datetime.now(timezone.utc)
            db.session.commit()
            return {"simulation_id": simulation_id, "message": "仿真结果已更新"}, None, 200

    new_simulation_id = str(uuid.uuid4())

    simulation = Simulation(
        id=new_simulation_id,
        project_id=project_id,
        user_id=user_id,
        name=data.get("name", f'仿真_{datetime.now().strftime("%Y%m%d_%H%M%S")}'),
        algorithm_type=data.get("algorithm_type", "arrhenius"),
        duration_years=data.get("duration_years", 25),
        correction_factor=data.get("correction_factor", 1.0),
        input_params=json.dumps(data.get("params") or {}),
        results=json.dumps(simulation_data),
        status="completed",
        completed_at=datetime.now(timezone.utc),
    )

    db.session.add(simulation)

    try:
        db.session.commit()
        return {"simulation_id": new_simulation_id, "message": "仿真结果已保存"}, None, 201
    except Exception:
        db.session.rollback()
        return None, "保存失败，请稍后重试", 500


def list_simulations(page, per_page, project_id, current_user):
    """获取仿真列表（含租户隔离过滤）。

    Args:
        page: 页码
        per_page: 每页数量
        project_id: 可选项目ID过滤
        current_user: 当前登录用户

    Returns:
        (items, page, per_page, total)
    """
    query = Simulation.query.join(Project).filter(Project.tenant_id == current_user.tenant_id)
    if project_id:
        query = query.filter(Simulation.project_id == project_id)

    pagination = query.order_by(Simulation.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    items = [
        {
            "id": s.id,
            "name": s.name,
            "algorithm_type": s.algorithm_type,
            "status": s.status,
            "created_at": s.created_at.isoformat() if s.created_at else None,
            "completed_at": s.completed_at.isoformat() if s.completed_at else None,
        }
        for s in pagination.items
    ]
    return items, pagination.page, pagination.per_page, pagination.total


def get_simulation_detail(simulation_id, current_user):
    """获取仿真详情（含租户隔离校验）。

    Args:
        simulation_id: 仿真ID
        current_user: 当前登录用户

    Returns:
        (result_dict, error_str, status_code)
    """
    simulation = Simulation.query.options(selectinload(Simulation.project)).get(simulation_id)
    if not simulation:
        return None, "仿真不存在", 404

    if simulation.project_id:
        if simulation.project and current_user and simulation.project.tenant_id != current_user.tenant_id:
            return None, "无权访问", 403

    result = {
        "id": simulation.id,
        "name": simulation.name,
        "description": simulation.description,
        "algorithm_type": simulation.algorithm_type,
        "duration_years": simulation.duration_years,
        "correction_factor": simulation.correction_factor,
        "status": simulation.status,
        "created_at": simulation.created_at.isoformat() if simulation.created_at else None,
        "completed_at": simulation.completed_at.isoformat() if simulation.completed_at else None,
    }

    if simulation.input_params:
        try:
            result["params"] = json.loads(simulation.input_params)
        except json.JSONDecodeError:
            pass

    if simulation.results:
        try:
            result["results"] = json.loads(simulation.results)
        except json.JSONDecodeError:
            pass

    return result, None, 200
