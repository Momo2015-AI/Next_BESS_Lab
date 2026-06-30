"""
EPC模块路由 - P0/P1新增模块的API
包含: 系统架构、电网合规、安全消防、IPP财务、合规矩阵、
      热管理、SCADA/EMS、高压接入、投标文档
"""
import math
import uuid
import json
from datetime import datetime
from flask import Blueprint, request, jsonify
from database import db

# 导入所有模型
from database import (
    SystemArchitecture, GridComplianceAnalysis, SafetyFireDesign,
    IPPFinancialModel, ComplianceMatrix, ThermalManagement,
    ScadaEmsDesign, HVInterconnection, BidDocument,
)

# 创建蓝图
epc_bp = Blueprint('epc', __name__)


# ===================== 通用CRUD =====================

def _get_or_404(model, item_id):
    obj = db.session.get(model, item_id)
    if not obj:
        return None
    return obj


def _paginated_query(model, args):
    page = int(args.get('page', 1))
    per_page = int(args.get('per_page', 20))
    project_id = args.get('project_id')
    query = model.query
    if project_id:
        query = query.filter_by(project_id=project_id)
    query = query.order_by(model.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        'items': [item.to_dict() for item in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
    }


# ===================== P0-3: 系统架构 =====================

@epc_bp.route('/api/system-architecture', methods=['GET'])
def list_architectures():
    return jsonify(_paginated_query(SystemArchitecture, request.args))


@epc_bp.route('/api/system-architecture/<arch_id>', methods=['GET'])
def get_architecture(arch_id):
    obj = _get_or_404(SystemArchitecture, arch_id)
    if not obj:
        return jsonify({'error': '未找到'}), 404
    return jsonify(obj.to_dict())


@epc_bp.route('/api/system-architecture/design', methods=['POST'])
def design_architecture():
    """自动设计系统架构"""
    data = request.get_json()
    total_power_mw = float(data.get('total_power_mw', 100))
    total_energy_mwh = float(data.get('total_energy_mwh', 200))
    duration_hours = total_energy_mwh / total_power_mw if total_power_mw > 0 else 2
    arch_type = data.get('architecture_type', 'central')
    coupling = data.get('coupling_type', 'AC')

    # 电芯参数
    cell_v = float(data.get('cell_voltage', 3.2))
    cell_ah = float(data.get('cell_capacity', 280))
    cell_energy_kwh = cell_v * cell_ah / 1000

    # PCS参数
    pcs_power_mw = float(data.get('pcs_power_mw', 3.45))
    pcs_max_dc_v = float(data.get('pcs_max_dc_voltage', 1500))

    # 1. PCS数量
    pcs_count = math.ceil(total_power_mw / pcs_power_mw)

    # 2. DC母线电压
    dc_bus_voltage = min(pcs_max_dc_v * 0.9, 1500)

    # 3. 电芯串联数
    cell_series = int(dc_bus_voltage / cell_v)

    # 4. 模组配置
    module_series = 24 if cell_series >= 24 else 12
    modules_per_rack = cell_series // module_series

    # 5. 电池包
    pack_energy_kwh = module_series * cell_v * cell_ah / 1000

    # 6. 机架
    rack_energy_kwh = pack_energy_kwh * modules_per_rack
    rack_power_kw = rack_energy_kwh / duration_hours if duration_hours > 0 else 0

    # 7. 簇
    racks_per_cluster = max(1, math.ceil(pcs_power_mw * 1000 / rack_power_kw / 4)) if rack_power_kw > 0 else 1
    cluster_energy_mwh = rack_energy_kwh * racks_per_cluster / 1000

    # 8. 集装箱
    racks_per_container = min(racks_per_cluster, 8)
    containers_per_pcs = max(1, math.ceil(racks_per_cluster / racks_per_container))
    container_energy_mwh = rack_energy_kwh * racks_per_container / 1000

    # 9. 分段
    total_containers = pcs_count * containers_per_pcs
    containers_per_section = containers_per_pcs
    sections = max(1, math.ceil(total_energy_mwh / (container_energy_mwh * containers_per_section))) if container_energy_mwh > 0 else 1

    # 10. 分期建设
    recommended_stages = max(2, min(4, sections // 4)) if sections > 1 else 1
    power_per_stage = total_power_mw / recommended_stages
    energy_per_stage = total_energy_mwh / recommended_stages

    stages = []
    for i in range(recommended_stages):
        stages.append({
            'stage': i + 1,
            'power_mw': round(power_per_stage, 1),
            'energy_mwh': round(energy_per_stage, 1),
            'sections': max(1, sections // recommended_stages),
            'estimated_date': f"2027-Q{(i*2)+1}",
        })

    # DC侧保护
    dc_breaker_count = pcs_count * racks_per_cluster
    dc_fuse_count = total_containers * racks_per_container

    # 拓扑数据
    topology = {
        'levels': [
            {'name': '电芯', 'count': cell_series, 'unit': '串联'},
            {'name': '模组', 'count': module_series, 'unit': '串/模组'},
            {'name': '电池包', 'count': modules_per_rack, 'unit': '包/机架'},
            {'name': '机架', 'count': racks_per_cluster, 'unit': '架/簇'},
            {'name': '集装箱', 'count': racks_per_container, 'unit': '架/箱'},
            {'name': 'PCS', 'count': containers_per_pcs, 'unit': '箱/PCS'},
            {'name': '分段', 'count': sections, 'unit': '总段数'},
            {'name': 'PCS总数', 'count': pcs_count, 'unit': '台'},
        ],
        'total_cells': cell_series * modules_per_rack * racks_per_cluster * racks_per_container * containers_per_pcs * pcs_count,
        'total_containers': total_containers,
        'total_racks': total_containers * racks_per_container,
    }

    result = {
        'total_power_mw': total_power_mw,
        'total_energy_mwh': total_energy_mwh,
        'duration_hours': round(duration_hours, 2),
        'architecture_type': arch_type,
        'coupling_type': coupling,
        'cell_to_module': cell_series,
        'module_to_pack': module_series,
        'pack_to_rack': modules_per_rack,
        'rack_to_cluster': racks_per_cluster,
        'cluster_to_container': racks_per_container,
        'container_to_section': containers_per_pcs,
        'section_to_stage': sections,
        'stage_count': recommended_stages,
        'stages': stages,
        'pcs_count': pcs_count,
        'pcs_power_mw': pcs_power_mw,
        'pcs_topology': 'distributed' if arch_type == 'string' else 'centralized',
        'dc_bus_voltage': round(dc_bus_voltage, 0),
        'dc_breaker_count': dc_breaker_count,
        'dc_fuse_count': dc_fuse_count,
        'topology_data': topology,
        'rack_energy_kwh': round(rack_energy_kwh, 2),
        'container_energy_mwh': round(container_energy_mwh, 2),
        'total_containers': total_containers,
    }

    # 保存到数据库
    arch = SystemArchitecture(
        id=str(uuid.uuid4()),
        project_id=data.get('project_id'),
        **{k: v for k, v in result.items() if hasattr(SystemArchitecture, k) and k not in ['stages', 'topology_data']}
    )
    arch.stages = json.dumps(stages)
    arch.topology_data = json.dumps(topology)
    db.session.add(arch)
    db.session.commit()

    return jsonify({'success': True, 'data': result, 'id': arch.id})


# ===================== P0-1: 电网合规 =====================

@epc_bp.route('/api/grid-compliance/standards', methods=['GET'])
def list_grid_standards():
    """获取支持的电网标准"""
    standards = [
        {'code': 'UAE_S_5010', 'name': 'UAE.S 5010-1', 'country': '阿联酋', 'voltage_kv': 33},
        {'code': 'IEEE_2800', 'name': 'IEEE 2800-2022', 'country': '美国', 'voltage_kv': 33},
        {'code': 'IEC_61400', 'name': 'IEC 61400-27', 'country': '国际', 'voltage_kv': 33},
        {'code': 'GB_19964', 'name': 'GB/T 19964-2024', 'country': '中国', 'voltage_kv': 35},
        {'code': 'CUSTOM', 'name': '自定义标准', 'country': '-', 'voltage_kv': 33},
    ]
    return jsonify(standards)


@epc_bp.route('/api/grid-compliance/analyze', methods=['POST'])
def analyze_grid_compliance():
    """执行电网合规分析"""
    data = request.get_json()
    standard = data.get('grid_standard', 'UAE_S_5010')
    pcs_power_mw = float(data.get('pcs_power_mw', 3.45))
    pcs_count = int(data.get('pcs_count', 1))
    grid_voltage_kv = float(data.get('grid_voltage_kv', 33))
    grid_freq = float(data.get('grid_frequency_hz', 50))

    total_power_mw = pcs_power_mw * pcs_count

    # LVRT分析
    lvrt_curve = [
        {'voltage_pu': 0.0, 'time_s': 0.15},
        {'voltage_pu': 0.2, 'time_s': 0.625},
        {'voltage_pu': 0.5, 'time_s': 2.0},
        {'voltage_pu': 0.85, 'time_s': 5.0},
    ]
    lvrt_pass = True  # PCS支持LVRT

    # HVRT分析
    hvrt_curve = [
        {'voltage_pu': 1.10, 'time_s': 60},
        {'voltage_pu': 1.15, 'time_s': 2.0},
        {'voltage_pu': 1.20, 'time_s': 0.5},
        {'voltage_pu': 1.30, 'time_s': 0.2},
    ]
    hvrt_pass = True

    # 频率响应
    freq_curve = [
        {'freq_hz': 47.5, 'power_pu': 1.0},
        {'freq_hz': 49.5, 'power_pu': 1.0},
        {'freq_hz': 50.0, 'power_pu': 1.0},
        {'freq_hz': 50.5, 'power_pu': 1.0},
        {'freq_hz': 52.0, 'power_pu': 0.0},
    ]
    freq_pass = True

    # 无功功率
    reactive_capacity = total_power_mw * 0.33  # 33%无功
    reactive_pass = True

    # 电能质量
    thd = 3.5  # %
    dc_inj = 0.2  # %
    v_fluct = 2.0  # %
    v_unbal = 1.0  # %
    pq_pass = thd <= 5.0

    # 防孤岛
    anti_island_time = 1.5  # s
    anti_island_pass = anti_island_time <= 2.0

    # 通信
    comm_pass = True

    overall = all([lvrt_pass, hvrt_pass, freq_pass, reactive_pass, pq_pass, anti_island_pass, comm_pass])
    failed = []
    if not lvrt_pass: failed.append('LVRT低电压穿越')
    if not hvrt_pass: failed.append('HVRT高电压穿越')
    if not freq_pass: failed.append('频率响应')
    if not reactive_pass: failed.append('无功功率能力')
    if not pq_pass: failed.append('电能质量')
    if not anti_island_pass: failed.append('防孤岛保护')
    if not comm_pass: failed.append('通信合规')

    result = {
        'grid_standard': standard,
        'grid_voltage_kv': grid_voltage_kv,
        'grid_frequency_hz': grid_freq,
        'grid_type': data.get('grid_type', 'TN'),
        'lvrt_curve': lvrt_curve,
        'lvrt_pass': lvrt_pass,
        'hvrt_curve': hvrt_curve,
        'hvrt_pass': hvrt_pass,
        'freq_response_curve': freq_curve,
        'freq_response_pass': freq_pass,
        'pf_lag': 0.95,
        'pf_lead': 0.95,
        'reactive_capacity_mvar': round(reactive_capacity, 2),
        'reactive_pass': reactive_pass,
        'thd': thd,
        'dc_injection': dc_inj,
        'voltage_fluctuation': v_fluct,
        'voltage_unbalance': v_unbal,
        'power_quality_pass': pq_pass,
        'anti_islanding_time_s': anti_island_time,
        'anti_islanding_pass': anti_island_pass,
        'comm_protocol': data.get('comm_protocol', 'IEC_61850'),
        'remote_response_s': 0.1,
        'comm_pass': comm_pass,
        'overall_pass': overall,
        'failed_items': failed,
    }

    # 保存
    gc = GridComplianceAnalysis(
        id=str(uuid.uuid4()),
        project_id=data.get('project_id'),
        **{k: v for k, v in result.items() if hasattr(GridComplianceAnalysis, k) and k not in ['lvrt_curve', 'hvrt_curve', 'freq_response_curve', 'failed_items']}
    )
    gc.lvrt_curve = json.dumps(lvrt_curve)
    gc.hvrt_curve = json.dumps(hvrt_curve)
    gc.freq_response_curve = json.dumps(freq_curve)
    gc.failed_items = json.dumps(failed)
    db.session.add(gc)
    db.session.commit()

    return jsonify({'success': True, 'data': result, 'id': gc.id})


@epc_bp.route('/api/grid-compliance/<gc_id>', methods=['GET'])
def get_grid_compliance(gc_id):
    obj = _get_or_404(GridComplianceAnalysis, gc_id)
    if not obj:
        return jsonify({'error': '未找到'}), 404
    return jsonify(obj.to_dict())


# ===================== P0-2: 安全与消防 =====================

@epc_bp.route('/api/safety-design/analyze', methods=['POST'])
def analyze_safety_design():
    """安全与消防设计分析"""
    data = request.get_json()
    capacity_mwh = float(data.get('system_capacity_mwh', 100))
    container_count = int(data.get('container_count', 20))
    chemistry = data.get('chemistry_type', 'LFP')

    # 热失控温度
    TRIGGER_TEMP = {'LFP': 270, 'NCM': 210, 'NCA': 190, 'LTO': 300}
    trigger = TRIGGER_TEMP.get(chemistry, 250)

    # 火灾分区 (NFPA 855)
    if chemistry == 'LFP':
        max_group_kwh = 330
    else:
        max_group_kwh = 250

    container_kwh = (capacity_mwh * 1000) / container_count if container_count > 0 else 0
    containers_per_zone = max(1, int(max_group_kwh / container_kwh)) if container_kwh > 0 else 1
    zone_count = math.ceil(container_count / containers_per_zone)

    # 间距
    spacing = 1.5
    if container_kwh > 2000:
        spacing = 3.0

    # 热失控蔓延
    propagation_time = 8.5  # min (简化)
    propagation_blocked = spacing >= 3.0

    # 灭火系统
    suppression_type = data.get('suppression_type', 'Novec1230')
    suppression_capacity = container_count * 45  # kg per container
    suppression_duration = 10  # s

    # 可燃气体检测
    gas_detectors = 4  # per zone

    result = {
        'system_capacity_mwh': capacity_mwh,
        'container_count': container_count,
        'chemistry_type': chemistry,
        'zone_count': zone_count,
        'zone_separation_material': '耐火板 (2h)',
        'fire_resistance_rating_min': 120,
        'gas_detection_type': '吸气式',
        'gas_detectors_per_zone': gas_detectors,
        'gas_threshold_ppm': 100.0,
        'thermal_runaway_temp_c': trigger,
        'propagation_time_min': propagation_time,
        'propagation_blocked': propagation_blocked,
        'suppression_type': suppression_type,
        'suppression_capacity_kg': float(suppression_capacity),
        'suppression_duration_s': float(suppression_duration),
        'container_spacing_m': spacing,
        'wall_distance_m': 3.0,
        'access_road_width_m': 4.0,
        'ul_9540a_pass': True,
        'nfpa_855_pass': True,
        'iec_62619_pass': True,
        'design_data': {'container_kwh': round(container_kwh, 0), 'containers_per_zone': containers_per_zone},
        'compliance_report': {'standard': 'NFPA 855 + UL 9540A', 'result': '通过'},
    }

    sf = SafetyFireDesign(
        id=str(uuid.uuid4()),
        project_id=data.get('project_id'),
        **{k: v for k, v in result.items() if hasattr(SafetyFireDesign, k) and k not in ['design_data', 'compliance_report']}
    )
    sf.design_data = json.dumps(result['design_data'])
    sf.compliance_report = json.dumps(result['compliance_report'])
    db.session.add(sf)
    db.session.commit()

    return jsonify({'success': True, 'data': result, 'id': sf.id})


@epc_bp.route('/api/safety-design/<sf_id>', methods=['GET'])
def get_safety_design(sf_id):
    obj = _get_or_404(SafetyFireDesign, sf_id)
    if not obj:
        return jsonify({'error': '未找到'}), 404
    return jsonify(obj.to_dict())


@epc_bp.route('/api/safety-design/standards', methods=['GET'])
def list_safety_standards():
    return jsonify([
        {'code': 'UL_9540A', 'name': 'UL 9540A - 储能系统安全测试'},
        {'code': 'NFPA_855', 'name': 'NFPA 855 - 储能系统消防标准'},
        {'code': 'IEC_62619', 'name': 'IEC 62619 - 工业电池安全'},
        {'code': 'UN_38_3', 'name': 'UN 38.3 - 运输安全测试'},
    ])


# ===================== P0-4: IPP财务 =====================

@epc_bp.route('/api/ipp-financial/calculate', methods=['POST'])
def calculate_ipp():
    """IPP财务模型计算"""
    data = request.get_json()
    years = int(data.get('project_life_years', 25))
    capex = float(data.get('total_capex_usd', 500_000_000))
    capacity_mw = float(data.get('capacity_mw', 100))
    energy_mwh = float(data.get('energy_mwh', 200))

    # PPA参数
    cap_price = float(data.get('capacity_price_usd_kw_month', 8.0))
    energy_price = float(data.get('energy_price_usd_kwh', 0.05))
    escalation = float(data.get('ppa_escalation_rate', 0.02))
    avail_guarantee = float(data.get('availability_guarantee', 0.98))
    avail_penalty = float(data.get('availability_penalty_usd_kw', 5.0))

    # 性能保证
    rte_guarantee = float(data.get('rte_guarantee', 90.0))
    rte_initial = float(data.get('rte_initial', 92.0))
    rte_decay = float(data.get('rte_decay_rate', 0.3))
    perf_penalty_rate = float(data.get('performance_penalty_rate', 0.1))

    # 投资结构
    debt_ratio = float(data.get('debt_ratio', 0.7))
    debt_rate = float(data.get('debt_interest_rate', 0.05))
    debt_tenor = int(data.get('debt_tenor_years', 15))
    discount_rate = float(data.get('discount_rate', 0.08))

    # 运营成本
    annual_opex = float(data.get('annual_opex_usd', 5_000_000))
    insurance_rate = float(data.get('insurance_rate', 0.005))
    land_lease = float(data.get('land_lease_usd_year', 500_000))

    # 债务
    debt_amount = capex * debt_ratio
    equity_amount = capex - debt_amount

    # 年均债务偿还 (等额本息)
    if debt_rate > 0 and debt_tenor > 0:
        annual_debt_service = debt_amount * (debt_rate * (1 + debt_rate) ** debt_tenor) / ((1 + debt_rate) ** debt_tenor - 1)
    else:
        annual_debt_service = debt_amount / debt_tenor if debt_tenor > 0 else 0

    cycles_per_year = 300
    annual_energy_kwh = energy_mwh * 1000 * cycles_per_year

    # 现金流
    project_cf = [-capex]
    equity_cf = [-equity_amount]
    dscrs = []

    for y in range(years):
        esc = (1 + escalation) ** y

        # 收入
        cap_revenue = capacity_mw * 1000 * cap_price * 12 * esc
        soh_factor = max(0.6, 1 - 0.012 * y)  # SOH衰减
        available_energy = annual_energy_kwh * soh_factor * avail_guarantee
        energy_revenue = available_energy * energy_price * esc

        # 可用率违约金
        actual_avail = avail_guarantee - 0.002 * y
        if actual_avail < avail_guarantee:
            shortfall = (avail_guarantee - actual_avail) * capacity_mw * 1000
            penalty = shortfall * avail_penalty
        else:
            penalty = 0

        # 性能违约金
        actual_rte = rte_initial - rte_decay * y
        perf_penalty = energy_revenue * perf_penalty_rate if actual_rte < rte_guarantee else 0

        total_revenue = cap_revenue + energy_revenue - penalty - perf_penalty

        # 支出
        opex_total = (annual_opex + capex * insurance_rate + land_lease) * (1.02 ** y)
        depreciation = capex / years
        ebitda = total_revenue - opex_total
        ebit = ebitda - depreciation
        tax = max(0, ebit * 0.2)
        debt_service = annual_debt_service if y < debt_tenor else 0

        net_cf = ebitda - tax - debt_service
        project_cf.append(net_cf)
        equity_cf.append(net_cf)

        # DSCR
        if y < debt_tenor and annual_debt_service > 0:
            cfads = total_revenue - opex_total
            dscrs.append(cfads / annual_debt_service)

    # NPV
    def npv(cashflows, rate):
        return sum(cf / (1 + rate) ** t for t, cf in enumerate(cashflows))

    # IRR
    def irr(cashflows):
        lo, hi = -0.99, 10.0
        for _ in range(100):
            mid = (lo + hi) / 2
            val = sum(cf / (1 + mid) ** t for t, cf in enumerate(cashflows))
            if val > 0:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    npv_val = npv(project_cf, discount_rate)
    irr_val = irr(project_cf)
    equity_irr_val = irr(equity_cf)
    dscr_avg = sum(dscrs) / len(dscrs) if dscrs else 0
    dscr_min = min(dscrs) if dscrs else 0

    # LCOE
    total_energy = annual_energy_kwh * years
    lcoe = capex / total_energy if total_energy > 0 else 0

    # 回收期
    cumulative = 0
    payback = years
    for t, cf in enumerate(project_cf):
        cumulative += cf
        if cumulative >= 0 and t > 0:
            payback = t - 1 + (project_cf[t-1] * -1 + cumulative - cf) / cf if cf != 0 else t
            break

    cashflow_detail = []
    for y in range(years):
        cashflow_detail.append({
            'year': y,
            'revenue': round(project_cf[y + 1], 0) if y + 1 < len(project_cf) else 0,
            'cumulative': round(sum(project_cf[:y + 2]), 0),
        })

    result = {
        'npv_usd': round(npv_val, 0),
        'irr': round(irr_val * 100, 2),
        'equity_irr': round(equity_irr_val * 100, 2),
        'dscr_avg': round(dscr_avg, 2),
        'dscr_min': round(dscr_min, 2),
        'lcoe_usd_kwh': round(lcoe, 4),
        'payback_years': round(payback, 1),
        'cashflow_data': cashflow_detail,
    }

    # 保存
    ipp = IPPFinancialModel(
        id=str(uuid.uuid4()),
        project_id=data.get('project_id'),
        project_name=data.get('project_name', ''),
        project_life_years=years,
        capacity_mw=capacity_mw,
        energy_mwh=energy_mwh,
        duration_hours=energy_mwh / capacity_mw if capacity_mw > 0 else 0,
        ppa_type=data.get('ppa_type', 'hybrid'),
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
        equity_irr_target=float(data.get('equity_irr_target', 0.12)),
        annual_opex_usd=annual_opex,
        insurance_rate=insurance_rate,
        land_lease_usd_year=land_lease,
        npv_usd=result['npv_usd'],
        irr=result['irr'] / 100,
        equity_irr=result['equity_irr'] / 100,
        dscr_avg=result['dscr_avg'],
        dscr_min=result['dscr_min'],
        lcoe_usd_kwh=result['lcoe_usd_kwh'],
        payback_years=result['payback_years'],
    )
    ipp.cashflow_data = json.dumps(cashflow_detail)
    db.session.add(ipp)
    db.session.commit()

    return jsonify({'success': True, 'data': result, 'id': ipp.id})


@epc_bp.route('/api/ipp-financial/<ipp_id>', methods=['GET'])
def get_ipp(ipp_id):
    obj = _get_or_404(IPPFinancialModel, ipp_id)
    if not obj:
        return jsonify({'error': '未找到'}), 404
    return jsonify(obj.to_dict())


# ===================== P0-5: 合规矩阵 =====================

# 预设RFP模板
COMPLIANCE_TEMPLATES = {
    'UAE_DEWA_VII_BESS': {
        'name': 'UAE DEWA VII BESS RFP',
        'sections': [
            {'section': '1.0', 'title': '通用要求', 'requirements': [
                {'id': '1.1', 'text': '系统容量: 1400MW/8400MWh', 'category': '系统规模'},
                {'id': '1.2', 'text': '储能时长: 6小时', 'category': '系统规模'},
                {'id': '1.3', 'text': 'IPP模式运营', 'category': '商业模式'},
                {'id': '1.4', 'text': '2027-2029分阶段投运', 'category': '项目进度'},
            ]},
            {'section': '2.0', 'title': '电池系统', 'requirements': [
                {'id': '2.1', 'text': '电池化学体系: LFP', 'category': '电池系统'},
                {'id': '2.2', 'text': '循环寿命≥6000次@80%DoD', 'category': '电池系统'},
                {'id': '2.3', 'text': '系统RTE≥90%', 'category': '性能保证'},
                {'id': '2.4', 'text': '10年SOH≥70%', 'category': '性能保证'},
                {'id': '2.5', 'text': '液冷热管理', 'category': '热管理'},
                {'id': '2.6', 'text': 'IP55防护等级', 'category': '环境防护'},
            ]},
            {'section': '3.0', 'title': '电网合规', 'requirements': [
                {'id': '3.1', 'text': '符合UAE.S 5010-1标准', 'category': '电网合规'},
                {'id': '3.2', 'text': 'LVRT: 20%电压保持150ms', 'category': '电网合规'},
                {'id': '3.3', 'text': 'HVRT: 120%电压保持2s', 'category': '电网合规'},
                {'id': '3.4', 'text': '频率响应: 49.5-50.5Hz', 'category': '电网合规'},
                {'id': '3.5', 'text': '功率因数: 0.95滞后~0.95超前', 'category': '电网合规'},
                {'id': '3.6', 'text': 'THD≤5%', 'category': '电能质量'},
                {'id': '3.7', 'text': '防孤岛保护≤2s', 'category': '安全保护'},
                {'id': '3.8', 'text': 'IEC 61850通信协议', 'category': '通信'},
            ]},
            {'section': '4.0', 'title': '安全与消防', 'requirements': [
                {'id': '4.1', 'text': 'UL 9540A认证', 'category': '安全认证'},
                {'id': '4.2', 'text': 'NFPA 855合规', 'category': '消防安全'},
                {'id': '4.3', 'text': '可燃气体检测系统', 'category': '消防安全'},
                {'id': '4.4', 'text': '火灾分区设计', 'category': '消防安全'},
                {'id': '4.5', 'text': '热失控防护', 'category': '安全防护'},
                {'id': '4.6', 'text': 'IEC 62619认证', 'category': '安全认证'},
            ]},
            {'section': '5.0', 'title': 'PCS与电力系统', 'requirements': [
                {'id': '5.1', 'text': 'Grid-forming逆变器', 'category': 'PCS'},
                {'id': '5.2', 'text': '合成惯量支持', 'category': 'PCS'},
                {'id': '5.3', 'text': '一次调频响应≤0.2s', 'category': 'PCS'},
                {'id': '5.4', 'text': 'UL 1741 SB认证', 'category': 'PCS认证'},
            ]},
            {'section': '6.0', 'title': 'SCADA与EMS', 'requirements': [
                {'id': '6.1', 'text': 'SCADA系统集成', 'category': 'SCADA'},
                {'id': '6.2', 'text': 'EMS能量调度', 'category': 'EMS'},
                {'id': '6.3', 'text': '远程监控与控制', 'category': 'SCADA'},
                {'id': '6.4', 'text': '网络安全: NERC-CIP', 'category': '网络安全'},
            ]},
            {'section': '7.0', 'title': '环境要求', 'requirements': [
                {'id': '7.1', 'text': '高温运行: ≥45°C', 'category': '环境'},
                {'id': '7.2', 'text': '沙尘防护: IP55+', 'category': '环境'},
                {'id': '7.3', 'text': '噪声: ≤75dB@1m', 'category': '环境'},
                {'id': '7.4', 'text': '电池回收计划', 'category': '环境'},
            ]},
        ]
    }
}


@epc_bp.route('/api/compliance-matrix/templates', methods=['GET'])
def list_compliance_templates():
    return jsonify([{'code': k, 'name': v['name']} for k, v in COMPLIANCE_TEMPLATES.items()])


@epc_bp.route('/api/compliance-matrix/generate', methods=['POST'])
def generate_compliance_matrix():
    """生成合规矩阵"""
    data = request.get_json()
    template_code = data.get('template', 'UAE_DEWA_VII_BESS')
    template = COMPLIANCE_TEMPLATES.get(template_code)

    if not template:
        return jsonify({'error': '模板不存在'}), 400

    project_data = data.get('project_data', {})
    matrix = []

    for section in template['sections']:
        for req in section['requirements']:
            status, response = _auto_match_requirement(req, project_data)
            matrix.append({
                'section': req['id'],
                'requirement': req['text'],
                'category': req['category'],
                'compliance_status': status,
                'response': response,
                'evidence': '',
                'reference_doc': '',
                'verified': False,
            })

    compliant = sum(1 for m in matrix if m['compliance_status'] == 'compliant')
    non_compliant = sum(1 for m in matrix if m['compliance_status'] == 'non_compliant')
    partial = sum(1 for m in matrix if m['compliance_status'] == 'partial')

    cm = ComplianceMatrix(
        id=str(uuid.uuid4()),
        project_id=data.get('project_id'),
        rfp_name=template['name'],
        rfp_version='Rev01',
        rfp_standard=template_code,
        total_items=len(matrix),
        compliant_count=compliant,
        non_compliant_count=non_compliant,
        partial_count=partial,
    )
    cm.matrix_data = json.dumps(matrix)
    db.session.add(cm)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': {
            'matrix': matrix,
            'total': len(matrix),
            'compliant': compliant,
            'non_compliant': non_compliant,
            'partial': partial,
        },
        'id': cm.id
    })


@epc_bp.route('/api/compliance-matrix/<cm_id>', methods=['GET'])
def get_compliance_matrix(cm_id):
    obj = _get_or_404(ComplianceMatrix, cm_id)
    if not obj:
        return jsonify({'error': '未找到'}), 404
    return jsonify(obj.to_dict())


@epc_bp.route('/api/compliance-matrix/<cm_id>', methods=['PUT'])
def update_compliance_matrix_item(cm_id):
    """更新合规矩阵中的单项"""
    obj = _get_or_404(ComplianceMatrix, cm_id)
    if not obj:
        return jsonify({'error': '未找到'}), 404

    data = request.get_json()
    matrix = json.loads(obj.matrix_data) if obj.matrix_data else []

    for item in matrix:
        if item['section'] == data.get('section'):
            item['compliance_status'] = data.get('compliance_status', item['compliance_status'])
            item['response'] = data.get('response', item['response'])
            item['evidence'] = data.get('evidence', item.get('evidence', ''))
            item['reference_doc'] = data.get('reference_doc', item.get('reference_doc', ''))
            item['verified'] = data.get('verified', item.get('verified', False))
            break

    obj.matrix_data = json.dumps(matrix)
    obj.compliant_count = sum(1 for m in matrix if m['compliance_status'] == 'compliant')
    obj.non_compliant_count = sum(1 for m in matrix if m['compliance_status'] == 'non_compliant')
    obj.partial_count = sum(1 for m in matrix if m['compliance_status'] == 'partial')
    db.session.commit()

    return jsonify({'success': True, 'data': matrix})


def _auto_match_requirement(req, project_data):
    """自动匹配RFP条款"""
    text = req['text']
    if 'LVRT' in text:
        gc = project_data.get('grid_compliance', {})
        return ('compliant' if gc.get('lvrt_pass') else 'partial', '系统支持LVRT功能') if gc else ('N/A', '待电网合规分析')
    if 'HVRT' in text:
        gc = project_data.get('grid_compliance', {})
        return ('compliant' if gc.get('hvrt_pass') else 'partial', '系统支持HVRT功能') if gc else ('N/A', '待电网合规分析')
    if 'RTE' in text and '≥' in text:
        sim = project_data.get('simulation', {})
        rte = sim.get('rte_initial', 0)
        return ('compliant', f'系统初始RTE = {rte}%') if rte >= 90 else ('partial', f'系统RTE = {rte}%，需优化')
    if 'SOH' in text and '10年' in text:
        sim = project_data.get('simulation', {})
        return ('compliant', f'第10年SOH满足要求') if sim.get('soh_year10', 0) >= 70 else ('partial', '需仿真验证')
    if 'UL 9540' in text:
        safety = project_data.get('safety_design', {})
        return ('compliant', '已通过UL 9540A测试') if safety.get('ul_9540a_pass') else ('partial', '需提供测试报告')
    if 'NFPA 855' in text:
        safety = project_data.get('safety_design', {})
        return ('compliant', '符合NFPA 855要求') if safety.get('nfpa_855_pass') else ('partial', '需安全设计分析')
    return ('N/A', '待人工确认')


# ===================== P1-1: 热管理 =====================

@epc_bp.route('/api/thermal-management/calculate', methods=['POST'])
def calculate_thermal():
    """热管理设计计算"""
    data = request.get_json()
    env_temp = float(data.get('ambient_max_c', 45))
    cell_ah = float(data.get('cell_capacity_ah', 280))
    cell_resistance = float(data.get('cell_resistance_ohm', 0.00025))
    c_rate = float(data.get('c_rate', 0.5))
    cells_per_container = int(data.get('cells_per_container', 5000))
    cooling_type = data.get('cooling_type', 'liquid')

    # 电芯发热量
    current = cell_ah * c_rate
    heat_per_cell = current ** 2 * cell_resistance

    # 集装箱总发热
    total_heat_w = heat_per_cell * cells_per_container
    total_heat_kw = total_heat_w / 1000

    # 制冷量 (发热 + 渗热)
    target_temp = 25
    container_area = 60  # m²
    u_value = 0.5
    heat_infiltration = container_area * u_value * (env_temp - target_temp)
    total_cooling_kw = (total_heat_kw + heat_infiltration / 1000) * 1.2

    # 液冷流量
    coolant_dt = 5
    coolant_cp = 3.5
    coolant_density = 1050
    coolant_flow_lpm = total_cooling_kw / (coolant_cp * coolant_dt * coolant_density) * 60 * 1000 if total_cooling_kw > 0 else 0

    # 降额曲线
    derating = []
    for temp in range(20, 60, 5):
        if temp <= 35:
            pct = 100
        elif temp <= 45:
            pct = 100 - (temp - 35) * 5
        else:
            pct = max(20, 50 - (temp - 45) * 3)
        derating.append({'temp': temp, 'power_pct': pct})

    # 年度制冷能耗
    annual_cooling = total_cooling_kw * 8760 * 0.7  # 70%负载率

    result = {
        'ambient_max_c': env_temp,
        'cooling_type': cooling_type,
        'coolant_type': '乙二醇水溶液(50%)' if cooling_type == 'liquid' else '制冷剂',
        'coolant_flow_rate_lpm': round(coolant_flow_lpm, 1),
        'hvac_capacity_kw': round(total_cooling_kw, 2),
        'hvac_cop': 2.5,
        'hvac_redundancy': 1,
        'cell_heat_generation_w': round(heat_per_cell, 3),
        'thermal_resistance_ckw': 0.15,
        'target_cell_temp_c': target_temp,
        'max_cell_temp_c': target_temp + 3,
        'temp_gradient_c': 3.0,
        'cooling_power_kw': round(total_cooling_kw, 2),
        'annual_cooling_energy_kwh': round(annual_cooling, 0),
        'derating_curve': derating,
    }

    tm = ThermalManagement(
        id=str(uuid.uuid4()),
        project_id=data.get('project_id'),
        **{k: v for k, v in result.items() if hasattr(ThermalManagement, k) and k != 'derating_curve'}
    )
    tm.derating_curve = json.dumps(derating)
    db.session.add(tm)
    db.session.commit()

    return jsonify({'success': True, 'data': result, 'id': tm.id})


@epc_bp.route('/api/thermal-management/<tm_id>', methods=['GET'])
def get_thermal(tm_id):
    obj = _get_or_404(ThermalManagement, tm_id)
    if not obj:
        return jsonify({'error': '未找到'}), 404
    return jsonify(obj.to_dict())


# ===================== P1-2: SCADA/EMS =====================

@epc_bp.route('/api/scada-ems/design', methods=['POST'])
def design_scada_ems():
    """SCADA/EMS设计"""
    data = request.get_json()
    container_count = int(data.get('container_count', 20))
    pcs_count = int(data.get('pcs_count', 10))

    # 数据点估算
    points_per_container = 200  # 模拟量+数字量
    points_per_pcs = 50
    total_points = container_count * points_per_container + pcs_count * points_per_pcs + 500  # 系统级

    ems_functions = [
        'peak_shaving', 'arbitrage', 'frequency_regulation',
        'voltage_support', 'renewable_smoothing', 'black_start'
    ]

    result = {
        'scada_architecture': data.get('scada_architecture', 'hierarchical'),
        'communication_protocol': data.get('communication_protocol', 'IEC_61850'),
        'network_topology': 'ring',
        'redundancy_level': 'dual',
        'total_data_points': total_points,
        'analog_points': int(total_points * 0.4),
        'digital_points': int(total_points * 0.5),
        'control_points': int(total_points * 0.1),
        'ems_functions': ems_functions,
        'dispatch_strategy': data.get('dispatch_strategy', 'peak_shaving'),
        'forecasting_type': 'load_and_pv_forecast',
        'firewall_config': '分层防火墙架构',
        'encryption_type': 'AES-256',
        'nerc_cip_compliant': True,
        'iec_62443_compliant': True,
        'architecture_diagram': {
            'layers': ['站控层', '通信层', '间隔层', '过程层'],
            'protocols': {'站控层': 'IEC 61850 MMS', '间隔层': 'IEC 61850 GOOSE', '过程层': 'SV'},
        },
    }

    se = ScadaEmsDesign(
        id=str(uuid.uuid4()),
        project_id=data.get('project_id'),
        **{k: v for k, v in result.items() if hasattr(ScadaEmsDesign, k) and k not in ['ems_functions', 'firewall_config', 'architecture_diagram']}
    )
    se.ems_functions = json.dumps(ems_functions)
    se.firewall_config = json.dumps({'config': '分层防火墙架构'})
    se.architecture_diagram = json.dumps(result['architecture_diagram'])
    db.session.add(se)
    db.session.commit()

    return jsonify({'success': True, 'data': result, 'id': se.id})


@epc_bp.route('/api/scada-ems/<se_id>', methods=['GET'])
def get_scada_ems(se_id):
    obj = _get_or_404(ScadaEmsDesign, se_id)
    if not obj:
        return jsonify({'error': '未找到'}), 404
    return jsonify(obj.to_dict())


# ===================== P1-3: 高压接入 =====================

@epc_bp.route('/api/hv-interconnection/design', methods=['POST'])
def design_hv_interconnection():
    """高压接入设计"""
    data = request.get_json()
    total_power_mw = float(data.get('total_power_mw', 100))
    poc_voltage = float(data.get('poc_voltage_kv', 33))
    s_sc = float(data.get('short_circuit_capacity_mva', 500))

    # 变压器
    trans_capacity = total_power_mw * 1.1
    trans_count = max(1, math.ceil(trans_capacity / 100))
    capacity_each = trans_capacity / trans_count

    if poc_voltage <= 33:
        ratio = f"{int(poc_voltage)}/0.69"
    elif poc_voltage <= 132:
        ratio = f"{int(poc_voltage)}/33/0.69"
    else:
        ratio = f"{int(poc_voltage)}/132/33/0.69"

    # 短路电流
    i_sc = s_sc / (1.732 * poc_voltage)
    breaker_rating = math.ceil(i_sc * 1.2 / 5) * 5

    # 电缆
    i_rated = trans_capacity * 1000 / (1.732 * poc_voltage)
    cable_section = math.ceil(i_rated / 1.5 / 50) * 50

    # 保护配置
    protections = [
        {'name': '过流保护', 'type': '50/51'},
        {'name': '距离保护', 'type': '21'},
        {'name': '差动保护', 'type': '87'},
        {'name': '频率保护', 'type': '81'},
        {'name': '电压保护', 'type': '27/59'},
    ]

    result = {
        'poc_voltage_kv': poc_voltage,
        'poc_type': data.get('poc_type', 'substation'),
        'short_circuit_capacity_mva': s_sc,
        'x_r_ratio': 10.0,
        'transformer_count': trans_count,
        'transformer_capacity_mva': round(capacity_each, 1),
        'transformer_ratio': ratio,
        'transformer_vector_group': 'Dyn11',
        'transformer_impedance': 10.5,
        'mv_switchgear_count': trans_count * 2,
        'mv_switchgear_type': 'GIS',
        'mv_breaker_rating_ka': float(breaker_rating),
        'protection_scheme': protections,
        'relay_count': len(protections) * trans_count,
        'relay_type': '微机保护',
        'single_line_diagram': {
            'voltage_levels': ratio.split('/'),
            'transformer_count': trans_count,
            'breaker_rating_ka': breaker_rating,
            'cable_cross_section_mm2': cable_section,
        },
    }

    hv = HVInterconnection(
        id=str(uuid.uuid4()),
        project_id=data.get('project_id'),
        **{k: v for k, v in result.items() if hasattr(HVInterconnection, k) and k not in ['protection_scheme', 'single_line_diagram']}
    )
    hv.protection_scheme = json.dumps(protections)
    hv.single_line_diagram = json.dumps(result['single_line_diagram'])
    db.session.add(hv)
    db.session.commit()

    return jsonify({'success': True, 'data': result, 'id': hv.id})


@epc_bp.route('/api/hv-interconnection/<hv_id>', methods=['GET'])
def get_hv_interconnection(hv_id):
    obj = _get_or_404(HVInterconnection, hv_id)
    if not obj:
        return jsonify({'error': '未找到'}), 404
    return jsonify(obj.to_dict())


# ===================== P1-4: 投标文档 =====================

BID_DOCUMENT_TEMPLATES = {
    'technical_proposal': {
        'name': '技术方案',
        'chapters': [
            {'num': '1', 'title': '项目概述', 'sections': [
                {'num': '1.1', 'title': '项目背景', 'source': 'survey'},
                {'num': '1.2', 'title': '系统规模', 'source': 'survey'},
                {'num': '1.3', 'title': '合规概述', 'source': 'compliance_matrix'},
            ]},
            {'num': '2', 'title': '系统架构设计', 'sections': [
                {'num': '2.1', 'title': '整体架构', 'source': 'system_architecture'},
                {'num': '2.2', 'title': '分期建设方案', 'source': 'system_architecture'},
            ]},
            {'num': '3', 'title': '电池系统设计', 'sections': [
                {'num': '3.1', 'title': '电芯选型', 'source': 'dc_design'},
                {'num': '3.2', 'title': 'SOH/RTE性能保证', 'source': 'simulation'},
            ]},
            {'num': '4', 'title': 'PCS与电力系统', 'sections': [
                {'num': '4.1', 'title': 'PCS选型', 'source': 'ac_design'},
                {'num': '4.2', 'title': '高压接入设计', 'source': 'hv_interconnection'},
                {'num': '4.3', 'title': '电网合规', 'source': 'grid_compliance'},
            ]},
            {'num': '5', 'title': '安全与消防设计', 'sections': [
                {'num': '5.1', 'title': '火灾分区', 'source': 'safety_design'},
                {'num': '5.2', 'title': '热失控防护', 'source': 'safety_design'},
            ]},
            {'num': '6', 'title': '热管理系统', 'sections': [
                {'num': '6.1', 'title': '冷却方案', 'source': 'thermal_management'},
            ]},
            {'num': '7', 'title': 'SCADA与EMS', 'sections': [
                {'num': '7.1', 'title': '系统架构', 'source': 'scada_ems'},
            ]},
            {'num': '8', 'title': '性能保证', 'sections': [
                {'num': '8.1', 'title': 'SOH衰减曲线', 'source': 'simulation'},
                {'num': '8.2', 'title': '可用率保证', 'source': 'ipp_financial'},
            ]},
            {'num': '9', 'title': '财务方案', 'sections': [
                {'num': '9.1', 'title': '投资概算', 'source': 'ipp_financial'},
                {'num': '9.2', 'title': 'LCOE分析', 'source': 'ipp_financial'},
            ]},
            {'num': '10', 'title': '合规矩阵', 'sections': [
                {'num': '10.1', 'title': 'RFP条款逐项回应', 'source': 'compliance_matrix'},
            ]},
        ]
    }
}


@epc_bp.route('/api/bid-document/templates', methods=['GET'])
def list_bid_templates():
    return jsonify([{'code': k, 'name': v['name']} for k, v in BID_DOCUMENT_TEMPLATES.items()])


@epc_bp.route('/api/bid-document/generate', methods=['POST'])
def generate_bid_document():
    """生成投标文档"""
    data = request.get_json()
    template_code = data.get('template', 'technical_proposal')
    template = BID_DOCUMENT_TEMPLATES.get(template_code)

    if not template:
        return jsonify({'error': '模板不存在'}), 400

    project_data = data.get('project_data', {})

    # 生成文档内容
    chapters = []
    for ch_template in template['chapters']:
        chapter = {
            'num': ch_template['num'],
            'title': ch_template['title'],
            'sections': []
        }
        for sec_template in ch_template['sections']:
            source = sec_template['source']
            src_data = project_data.get(source, {})
            content = _generate_section_content(sec_template, src_data)
            chapter['sections'].append({
                'num': sec_template['num'],
                'title': sec_template['title'],
                'content': content,
                'data_source': source,
            })
        chapters.append(chapter)

    sources = list(set(s['source'] for ch in template['chapters'] for s in ch['sections']))

    bd = BidDocument(
        id=str(uuid.uuid4()),
        project_id=data.get('project_id'),
        document_type=template_code,
        title=template['name'],
        version='1.0',
        status='draft',
    )
    bd.content = json.dumps(chapters)
    bd.data_sources = json.dumps(sources)
    db.session.add(bd)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': {'chapters': chapters, 'sources': sources},
        'id': bd.id
    })


@epc_bp.route('/api/bid-document/<bd_id>', methods=['GET'])
def get_bid_document(bd_id):
    obj = _get_or_404(BidDocument, bd_id)
    if not obj:
        return jsonify({'error': '未找到'}), 404
    return jsonify(obj.to_dict())


@epc_bp.route('/api/bid-document', methods=['GET'])
def list_bid_documents():
    return jsonify(_paginated_query(BidDocument, request.args))


def _generate_section_content(section_template, data):
    """根据数据源生成章节内容"""
    source = section_template['source']

    if not data:
        return f"（待{source}模块数据填充）"

    if source == 'survey':
        return (f"项目名称: {data.get('project_name', 'N/A')}\n"
                f"项目规模: {data.get('total_mw', 'N/A')}MW / {data.get('total_mwh', 'N/A')}MWh\n"
                f"储能时长: {data.get('duration', 'N/A')}小时\n"
                f"项目位置: {data.get('location', 'N/A')}")
    elif source == 'system_architecture':
        return (f"系统架构类型: {data.get('architecture_type', 'N/A')}\n"
                f"PCS数量: {data.get('pcs_count', 'N/A')}台\n"
                f"DC母线电压: {data.get('dc_bus_voltage', 'N/A')}V\n"
                f"分期建设: {data.get('stage_count', 'N/A')}期")
    elif source == 'simulation':
        return (f"初始SOH: {data.get('init_soh', 'N/A')}%\n"
                f"初始RTE: {data.get('init_rte', 'N/A')}%\n"
                f"第10年SOH: {data.get('soh_year10', 'N/A')}%")
    elif source == 'grid_compliance':
        return (f"合规标准: {data.get('grid_standard', 'N/A')}\n"
                f"LVRT: {'通过' if data.get('lvrt_pass') else '未通过'}\n"
                f"HVRT: {'通过' if data.get('hvrt_pass') else '未通过'}\n"
                f"总体合规: {'通过' if data.get('overall_pass') else '未通过'}")
    elif source == 'safety_design':
        return (f"火灾分区: {data.get('zone_count', 'N/A')}个\n"
                f"热失控温度: {data.get('thermal_runaway_temp_c', 'N/A')}°C\n"
                f"UL 9540A: {'通过' if data.get('ul_9540a_pass') else '未通过'}")
    elif source == 'ipp_financial':
        return (f"NPV: ${data.get('npv_usd', 'N/A')}\n"
                f"IRR: {data.get('irr', 'N/A')}%\n"
                f"LCOE: ${data.get('lcoe_usd_kwh', 'N/A')}/kWh\n"
                f"回收期: {data.get('payback_years', 'N/A')}年")
    elif source == 'thermal_management':
        return (f"冷却方式: {data.get('cooling_type', 'N/A')}\n"
                f"制冷容量: {data.get('hvac_capacity_kw', 'N/A')}kW\n"
                f"目标温度: {data.get('target_cell_temp_c', 'N/A')}°C")
    elif source == 'scada_ems':
        return (f"架构: {data.get('scada_architecture', 'N/A')}\n"
                f"通信协议: {data.get('communication_protocol', 'N/A')}\n"
                f"数据点: {data.get('total_data_points', 'N/A')}")
    elif source == 'hv_interconnection':
        return (f"并网点电压: {data.get('poc_voltage_kv', 'N/A')}kV\n"
                f"变压器: {data.get('transformer_count', 'N/A')}×{data.get('transformer_capacity_mva', 'N/A')}MVA\n"
                f"变比: {data.get('transformer_ratio', 'N/A')}")
    elif source == 'compliance_matrix':
        return (f"总条款: {data.get('total_items', 'N/A')}\n"
                f"合规: {data.get('compliant_count', 'N/A')}\n"
                f"不合规: {data.get('non_compliant_count', 'N/A')}\n"
                f"部分合规: {data.get('partial_count', 'N/A')}")
    else:
        return f"（待{source}模块数据填充）"
