"""
EPC模块路由 - P0/P1新增模块的API
包含: 系统架构、电网合规、安全消防、IPP财务、合规矩阵、
      热管理、SCADA/EMS、高压接入、投标文档
"""

import json
import uuid
from datetime import datetime

from flask import Blueprint, current_app, request

from database import (
    BidDocument,
    ComplianceMatrix,
    GridComplianceAnalysis,
    HVInterconnection,
    IPPFinancialModel,
    Project,
    SafetyFireDesign,
    ScadaEmsDesign,
    SystemArchitecture,
    ThermalManagement,
    db,
)
from routes.auth import _get_user_from_token, token_required
from services.epc_modules import (
    BID_DOCUMENT_TEMPLATES,
    COMPLIANCE_TEMPLATES,
    GRID_STANDARDS,
    SAFETY_STANDARDS,
    analyze_grid_compliance_service,
    analyze_safety_design_service,
    calculate_ipp_service,
    calculate_thermal_service,
    design_architecture_service,
    design_hv_interconnection_service,
    design_scada_ems_service,
    generate_bid_document_service,
    generate_compliance_matrix_service,
)
from utils.api_response import error_response, success_response

epc_bp = Blueprint("epc", __name__)


def _check_project_access(project_id, user):
    """验证用户有权访问该项目（tenant_id 隔离）"""
    if not user:
        return False
    proj = Project.query.get(project_id) if project_id else None
    if not proj:
        return False
    if getattr(user, "role", None) == "admin":
        return True
    return getattr(proj, "tenant_id", None) == getattr(user, "tenant_id", None)


def _get_or_404(model, item_id):
    obj = db.session.get(model, item_id)
    return obj if obj else None


# ===================== 系统架构 =====================


@epc_bp.route("/api/system-architecture", methods=["GET"])
@token_required
def list_architectures():
    user = request.current_user
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))
    project_id = request.args.get("project_id")
    query = SystemArchitecture.query
    if project_id:
        query = query.filter_by(project_id=project_id)
    if getattr(user, "role", None) != "admin":
        query = query.filter_by(tenant_id=user.tenant_id)
    pagination = query.order_by(SystemArchitecture.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return success_response(data={
        "items": [item.to_dict() for item in pagination.items],
        "total": pagination.total,
        "page": page,
        "per_page": per_page,
        "pages": pagination.pages,
    })


@epc_bp.route("/api/system-architecture/<arch_id>", methods=["GET"])
@token_required
def get_architecture(arch_id):
    user = request.current_user
    obj = _get_or_404(SystemArchitecture, arch_id)
    if not obj:
        return error_response("未找到", 404)
    if getattr(user, "role", None) != "admin" and getattr(obj, "tenant_id", None) != user.tenant_id:
        return error_response("无权访问该项目", 403)
    return success_response(data=obj.to_dict())


@epc_bp.route("/api/system-architecture/design", methods=["POST"])
@token_required
def design_architecture():
    """自动设计系统架构"""
    data = request.get_json()
    project_id = data.get("project_id")
    user = request.current_user
    if project_id and not _check_project_access(project_id, user):
        return error_response("无权访问该项目", 403)

    result = design_architecture_service(data)

    arch = SystemArchitecture(
        id=str(uuid.uuid4()),
        project_id=data.get("project_id"),
        **{k: v for k, v in result.items() if hasattr(SystemArchitecture, k) and k not in ["stages", "topology_data"]},
    )
    arch.stages = json.dumps(result["stages"])
    arch.topology_data = json.dumps(result["topology_data"])
    db.session.add(arch)
    db.session.commit()

    return success_response(data=result, message={"id": arch.id})


# ===================== 电网合规 =====================


@epc_bp.route("/api/grid-compliance/standards", methods=["GET"])
@token_required
def list_grid_standards():
    """获取支持的电网标准"""
    return success_response(data=GRID_STANDARDS)


@epc_bp.route("/api/grid-compliance/analyze", methods=["POST"])
@token_required
def analyze_grid_compliance():
    """执行电网合规分析"""
    data = request.get_json()
    project_id = data.get("project_id")
    user = request.current_user
    if project_id and not _check_project_access(project_id, user):
        return error_response("无权访问该项目", 403)

    result = analyze_grid_compliance_service(data)

    gc = GridComplianceAnalysis(
        id=str(uuid.uuid4()),
        project_id=data.get("project_id"),
        **{
            k: v
            for k, v in result.items()
            if hasattr(GridComplianceAnalysis, k)
            and k not in ["lvrt_curve", "hvrt_curve", "freq_response_curve", "failed_items"]
        },
    )
    gc.lvrt_curve = json.dumps(result["lvrt_curve"])
    gc.hvrt_curve = json.dumps(result["hvrt_curve"])
    gc.freq_response_curve = json.dumps(result["freq_response_curve"])
    gc.failed_items = json.dumps(result["failed_items"])
    db.session.add(gc)
    db.session.commit()

    return success_response(data=result, message={"id": gc.id})


@epc_bp.route("/api/grid-compliance/<gc_id>", methods=["GET"])
@token_required
def get_grid_compliance(gc_id):
    user = request.current_user
    obj = _get_or_404(GridComplianceAnalysis, gc_id)
    if not obj:
        return error_response("未找到", 404)
    if getattr(user, "role", None) != "admin" and getattr(obj, "tenant_id", None) != user.tenant_id:
        return error_response("无权访问该项目", 403)
    return success_response(data=obj.to_dict())


# ===================== 安全消防 =====================


@epc_bp.route("/api/safety-design/analyze", methods=["POST"])
@token_required
def analyze_safety_design():
    """安全与消防设计分析"""
    data = request.get_json()
    project_id = data.get("project_id")
    user = request.current_user
    if project_id and not _check_project_access(project_id, user):
        return error_response("无权访问该项目", 403)

    result = analyze_safety_design_service(data)

    sf = SafetyFireDesign(
        id=str(uuid.uuid4()),
        project_id=data.get("project_id"),
        **{
            k: v
            for k, v in result.items()
            if hasattr(SafetyFireDesign, k) and k not in ["design_data", "compliance_report"]
        },
    )
    sf.design_data = json.dumps(result["design_data"])
    sf.compliance_report = json.dumps(result["compliance_report"])
    db.session.add(sf)
    db.session.commit()

    return success_response(data=result, message={"id": sf.id})


@epc_bp.route("/api/safety-design/<sf_id>", methods=["GET"])
@token_required
def get_safety_design(sf_id):
    user = request.current_user
    obj = _get_or_404(SafetyFireDesign, sf_id)
    if not obj:
        return error_response("未找到", 404)
    if getattr(user, "role", None) != "admin" and getattr(obj, "tenant_id", None) != user.tenant_id:
        return error_response("无权访问该项目", 403)
    return success_response(data=obj.to_dict())


@epc_bp.route("/api/safety-design/standards", methods=["GET"])
@token_required
def list_safety_standards():
    return success_response(data=SAFETY_STANDARDS)


# ===================== IPP财务 =====================


@epc_bp.route("/api/ipp-financial/calculate", methods=["POST"])
@token_required
def calculate_ipp():
    """IPP财务模型计算"""
    data = request.get_json()
    project_id = data.get("project_id")
    user = request.current_user
    if project_id and not _check_project_access(project_id, user):
        return error_response("无权访问该项目", 403)

    result = calculate_ipp_service(data)

    years = int(data.get("project_life_years", 25))
    energy_mwh = float(data.get("energy_mwh", 200))
    capacity_mw = float(data.get("capacity_mw", 100))
    cap_price = float(data.get("capacity_price_usd_kw_month", 8.0))
    energy_price = float(data.get("energy_price_usd_kwh", 0.05))
    escalation = float(data.get("ppa_escalation_rate", 0.02))
    avail_guarantee = float(data.get("availability_guarantee", 0.98))
    avail_penalty = float(data.get("availability_penalty_usd_kw", 5.0))
    rte_guarantee = float(data.get("rte_guarantee", 90.0))
    perf_penalty_rate = float(data.get("performance_penalty_rate", 0.1))
    capex = float(data.get("total_capex_usd", 500_000_000))
    debt_ratio = float(data.get("debt_ratio", 0.7))
    debt_rate = float(data.get("debt_interest_rate", 0.05))
    debt_tenor = int(data.get("debt_tenor_years", 15))
    annual_opex = float(data.get("annual_opex_usd", 5_000_000))
    insurance_rate = float(data.get("insurance_rate", 0.005))
    land_lease = float(data.get("land_lease_usd_year", 500_000))

    ipp = IPPFinancialModel(
        id=str(uuid.uuid4()),
        project_id=data.get("project_id"),
        project_name=data.get("project_name", ""),
        project_life_years=years,
        capacity_mw=capacity_mw,
        energy_mwh=energy_mwh,
        duration_hours=energy_mwh / capacity_mw if capacity_mw > 0 else 0,
        ppa_type=data.get("ppa_type", "hybrid"),
        capacity_price_usd_kw_month=cap_price,
        energy_price_usd_kwh=energy_price,
        ppa_escalation_rate=escalation,
        availability_guarantee=avail_guarantee,
        availability_penalty_usd_kw=avail_penalty,
        rte_guarantee=rte_guarantee,
        performance_penalty_rate=perf_penalty_rate,
        total_capex_usd=capex,
        debt_ratio=debt_ratio,
        debt_interest_rate=debt_rate,
        debt_tenor_years=debt_tenor,
        equity_irr_target=float(data.get("equity_irr_target", 0.12)),
        annual_opex_usd=annual_opex,
        insurance_rate=insurance_rate,
        land_lease_usd_year=land_lease,
        npv_usd=result["npv_usd"],
        irr=result["irr"] / 100,
        equity_irr=result["equity_irr"] / 100,
        dscr_avg=result["dscr_avg"],
        dscr_min=result["dscr_min"],
        lcoe_usd_kwh=result["lcoe_usd_kwh"],
        payback_years=result["payback_years"],
    )
    ipp.cashflow_data = json.dumps(result["cashflow_data"])
    db.session.add(ipp)
    db.session.commit()

    return success_response(data=result, message={"id": ipp.id})


@epc_bp.route("/api/ipp-financial/<ipp_id>", methods=["GET"])
@token_required
def get_ipp(ipp_id):
    user = request.current_user
    obj = _get_or_404(IPPFinancialModel, ipp_id)
    if not obj:
        return error_response("未找到", 404)
    if getattr(user, "role", None) != "admin" and getattr(obj, "tenant_id", None) != user.tenant_id:
        return error_response("无权访问该项目", 403)
    return success_response(data=obj.to_dict())


# ===================== 合规矩阵 =====================


@epc_bp.route("/api/compliance-matrix/templates", methods=["GET"])
@token_required
def list_compliance_templates():
    return success_response(data=[{"code": k, "name": v["name"]} for k, v in COMPLIANCE_TEMPLATES.items()])


@epc_bp.route("/api/compliance-matrix/generate", methods=["POST"])
@token_required
def generate_compliance_matrix():
    """生成合规矩阵"""
    data = request.get_json()
    project_id = data.get("project_id")
    user = request.current_user
    if project_id and not _check_project_access(project_id, user):
        return error_response("无权访问该项目", 403)

    result, err = generate_compliance_matrix_service(data)
    if err:
        return error_response(err, 400)

    cm = ComplianceMatrix(
        id=str(uuid.uuid4()),
        project_id=data.get("project_id"),
        rfp_name=result["template_name"],
        rfp_version="Rev01",
        rfp_standard=result["template_code"],
        total_items=result["total"],
        compliant_count=result["compliant"],
        non_compliant_count=result["non_compliant"],
        partial_count=result["partial"],
    )
    cm.matrix_data = json.dumps(result["matrix"])
    db.session.add(cm)
    db.session.commit()

    return success_response(data={
        "matrix": result["matrix"],
        "total": result["total"],
        "compliant": result["compliant"],
        "non_compliant": result["non_compliant"],
        "partial": result["partial"],
    }, message={"id": cm.id})


@epc_bp.route("/api/compliance-matrix/<cm_id>", methods=["GET"])
@token_required
def get_compliance_matrix(cm_id):
    user = request.current_user
    obj = _get_or_404(ComplianceMatrix, cm_id)
    if not obj:
        return error_response("未找到", 404)
    if getattr(user, "role", None) != "admin" and getattr(obj, "tenant_id", None) != user.tenant_id:
        return error_response("无权访问该项目", 403)
    return success_response(data=obj.to_dict())


@epc_bp.route("/api/compliance-matrix/<cm_id>", methods=["PUT"])
@token_required
def update_compliance_matrix_item(cm_id):
    """更新合规矩阵中的单项"""
    user = request.current_user
    obj = _get_or_404(ComplianceMatrix, cm_id)
    if not obj:
        return error_response("未找到", 404)
    if getattr(user, "role", None) != "admin" and getattr(obj, "tenant_id", None) != user.tenant_id:
        return error_response("无权访问该项目", 403)

    data = request.get_json()
    matrix = json.loads(obj.matrix_data) if obj.matrix_data else []

    for item in matrix:
        if item["section"] == data.get("section"):
            item["compliance_status"] = data.get("compliance_status", item["compliance_status"])
            item["response"] = data.get("response", item["response"])
            item["evidence"] = data.get("evidence", item.get("evidence", ""))
            item["reference_doc"] = data.get("reference_doc", item.get("reference_doc", ""))
            item["verified"] = data.get("verified", item.get("verified", False))
            break

    obj.matrix_data = json.dumps(matrix)
    obj.compliant_count = sum(1 for m in matrix if m["compliance_status"] == "compliant")
    obj.non_compliant_count = sum(1 for m in matrix if m["compliance_status"] == "non_compliant")
    obj.partial_count = sum(1 for m in matrix if m["compliance_status"] == "partial")
    db.session.commit()

    return success_response(data=matrix)


# ===================== 热管理 =====================


@epc_bp.route("/api/thermal-management/calculate", methods=["POST"])
@token_required
def calculate_thermal():
    """热管理设计计算"""
    data = request.get_json()
    project_id = data.get("project_id")
    user = request.current_user
    if project_id and not _check_project_access(project_id, user):
        return error_response("无权访问该项目", 403)

    result = calculate_thermal_service(data)

    tm = ThermalManagement(
        id=str(uuid.uuid4()),
        project_id=data.get("project_id"),
        **{k: v for k, v in result.items() if hasattr(ThermalManagement, k) and k != "derating_curve"},
    )
    tm.derating_curve = json.dumps(result["derating_curve"])
    db.session.add(tm)
    db.session.commit()

    return success_response(data=result, message={"id": tm.id})


@epc_bp.route("/api/thermal-management/<tm_id>", methods=["GET"])
@token_required
def get_thermal(tm_id):
    user = request.current_user
    obj = _get_or_404(ThermalManagement, tm_id)
    if not obj:
        return error_response("未找到", 404)
    if getattr(user, "role", None) != "admin" and getattr(obj, "tenant_id", None) != user.tenant_id:
        return error_response("无权访问该项目", 403)
    return success_response(data=obj.to_dict())


# ===================== SCADA/EMS =====================


@epc_bp.route("/api/scada-ems/design", methods=["POST"])
@token_required
def design_scada_ems():
    """SCADA/EMS设计"""
    data = request.get_json()
    project_id = data.get("project_id")
    user = request.current_user
    if project_id and not _check_project_access(project_id, user):
        return error_response("无权访问该项目", 403)

    result = design_scada_ems_service(data)

    ems_functions = result["ems_functions"]
    se = ScadaEmsDesign(
        id=str(uuid.uuid4()),
        project_id=data.get("project_id"),
        **{
            k: v
            for k, v in result.items()
            if hasattr(ScadaEmsDesign, k) and k not in ["ems_functions", "firewall_config", "architecture_diagram"]
        },
    )
    se.ems_functions = json.dumps(ems_functions)
    se.firewall_config = json.dumps({"config": result["firewall_config"]})
    se.architecture_diagram = json.dumps(result["architecture_diagram"])
    db.session.add(se)
    db.session.commit()

    return success_response(data=result, message={"id": se.id})


@epc_bp.route("/api/scada-ems/<se_id>", methods=["GET"])
@token_required
def get_scada_ems(se_id):
    user = request.current_user
    obj = _get_or_404(ScadaEmsDesign, se_id)
    if not obj:
        return error_response("未找到", 404)
    if getattr(user, "role", None) != "admin" and getattr(obj, "tenant_id", None) != user.tenant_id:
        return error_response("无权访问该项目", 403)
    return success_response(data=obj.to_dict())


# ===================== 高压接入 =====================


@epc_bp.route("/api/hv-interconnection/design", methods=["POST"])
@token_required
def design_hv_interconnection():
    """高压接入设计"""
    data = request.get_json()
    project_id = data.get("project_id")
    user = request.current_user
    if project_id and not _check_project_access(project_id, user):
        return error_response("无权访问该项目", 403)

    result = design_hv_interconnection_service(data)

    protections = result["protection_scheme"]
    hv = HVInterconnection(
        id=str(uuid.uuid4()),
        project_id=data.get("project_id"),
        **{
            k: v
            for k, v in result.items()
            if hasattr(HVInterconnection, k) and k not in ["protection_scheme", "single_line_diagram"]
        },
    )
    hv.protection_scheme = json.dumps(protections)
    hv.single_line_diagram = json.dumps(result["single_line_diagram"])
    db.session.add(hv)
    db.session.commit()

    return success_response(data=result, message={"id": hv.id})


@epc_bp.route("/api/hv-interconnection/<hv_id>", methods=["GET"])
@token_required
def get_hv_interconnection(hv_id):
    user = request.current_user
    obj = _get_or_404(HVInterconnection, hv_id)
    if not obj:
        return error_response("未找到", 404)
    if getattr(user, "role", None) != "admin" and getattr(obj, "tenant_id", None) != user.tenant_id:
        return error_response("无权访问该项目", 403)
    return success_response(data=obj.to_dict())


# ===================== 投标文档 =====================


@epc_bp.route("/api/bid-document/templates", methods=["GET"])
@token_required
def list_bid_templates():
    return success_response(data=[{"code": k, "name": v["name"]} for k, v in BID_DOCUMENT_TEMPLATES.items()])


@epc_bp.route("/api/bid-document/generate", methods=["POST"])
@token_required
def generate_bid_document():
    """生成投标文档"""
    data = request.get_json()
    project_id = data.get("project_id")
    user = request.current_user
    if project_id and not _check_project_access(project_id, user):
        return error_response("无权访问该项目", 403)

    result, err = generate_bid_document_service(data)
    if err:
        return error_response(err, 400)

    bd = BidDocument(
        id=str(uuid.uuid4()),
        project_id=data.get("project_id"),
        document_type=result["template_code"],
        title=result["template_name"],
        version="1.0",
        status="draft",
    )
    bd.content = json.dumps(result["chapters"])
    bd.data_sources = json.dumps(result["sources"])
    db.session.add(bd)
    db.session.commit()

    return success_response(data={"chapters": result["chapters"], "sources": result["sources"]}, message={"id": bd.id})


@epc_bp.route("/api/bid-document/<bd_id>", methods=["GET"])
@token_required
def get_bid_document(bd_id):
    user = request.current_user
    obj = _get_or_404(BidDocument, bd_id)
    if not obj:
        return error_response("未找到", 404)
    if getattr(user, "role", None) != "admin" and getattr(obj, "tenant_id", None) != user.tenant_id:
        return error_response("无权访问该项目", 403)
    return success_response(data=obj.to_dict())


@epc_bp.route("/api/bid-document", methods=["GET"])
@token_required
def list_bid_documents():
    user = request.current_user
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))
    project_id = request.args.get("project_id")
    query = BidDocument.query
    if project_id:
        query = query.filter_by(project_id=project_id)
    if getattr(user, "role", None) != "admin":
        query = query.filter_by(tenant_id=user.tenant_id)
    pagination = query.order_by(BidDocument.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return success_response(data={
        "items": [item.to_dict() for item in pagination.items],
        "total": pagination.total,
        "page": page,
        "per_page": per_page,
        "pages": pagination.pages,
    })
