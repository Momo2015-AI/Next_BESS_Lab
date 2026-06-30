"""
数据库配置与模型定义
使用SQLite作为数据库，支持跨平台运行
完整支持所有功能模块的数据存储
"""
import os
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

# 这些列存储 JSON 字符串，序列化时需要解析回对象
_JSON_COLUMNS = {
    'Survey': {'attachments'},
    'Project': {'config'},
    'Simulation': {'input_params', 'results', 'manual_corrections'},
    'BatteryPCSConfig': {'connection_diagram', 'single_line_diagram'},
    'SohRteData': {'soh_values', 'rte_values', 'dod_values', 'aug_qty_values'},
    'FinancialData': {'cashflow_data'},
    'ProductConfig': {'certifications'},
    'FormulaConfig': {'parameters'},
    'SystemArchitecture': {'stages', 'topology_data'},
    'GridComplianceAnalysis': {'lvrt_curve', 'hvrt_curve', 'freq_response_curve', 'failed_items', 'report_data'},
    'SafetyFireDesign': {'design_data', 'compliance_report'},
    'IPPFinancialModel': {'cashflow_data'},
    'ComplianceMatrix': {'matrix_data'},
    'ThermalManagement': {'derating_curve'},
    'ScadaEmsDesign': {'ems_functions', 'firewall_config', 'architecture_diagram'},
    'HVInterconnection': {'protection_scheme', 'single_line_diagram'},
    'BidDocument': {'content', 'data_sources'},
}

def _serialize_value(model_name, column_name, value):
    """序列化单个字段值：datetime→ISO 字符串，JSON 列→解析回对象"""
    if value is None:
        return None
    if model_name in _JSON_COLUMNS and column_name in _JSON_COLUMNS[model_name]:
        if isinstance(value, str):
            try:
                return json.loads(value)
            except (json.JSONDecodeError, ValueError):
                return value
        return value
    if isinstance(value, datetime):
        return value.isoformat()
    return value

def _model_to_dict(self):
    """通用 to_dict：遍历所有列，按需序列化"""
    model_name = type(self).__name__
    return {
        column.name: _serialize_value(model_name, column.name, getattr(self, column.name))
        for column in self.__table__.columns
    }

class PinnModelWeights(db.Model):
    __tablename__ = 'pinn_model_weights'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(255), nullable=False)
    weights = db.Column(db.LargeBinary, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    def __repr__(self):
        return f'<PinnModelWeights {self.model_name}>'

# ===================== P0/P1 新增模块模型 =====================

class SystemArchitecture(db.Model):
    """超大规模系统架构模型"""
    __tablename__ = 'system_architectures'

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))

    # 系统规模
    total_power_mw = db.Column(db.Float)
    total_energy_mwh = db.Column(db.Float)
    duration_hours = db.Column(db.Float)

    # 架构类型
    architecture_type = db.Column(db.String(30))  # central/string/hybrid
    coupling_type = db.Column(db.String(20))       # AC/DC/hybrid

    # 分层结构
    cell_to_module = db.Column(db.Integer)
    module_to_pack = db.Column(db.Integer)
    pack_to_rack = db.Column(db.Integer)
    rack_to_cluster = db.Column(db.Integer)
    cluster_to_container = db.Column(db.Integer)
    container_to_section = db.Column(db.Integer)
    section_to_stage = db.Column(db.Integer)

    # 分期建设
    stage_count = db.Column(db.Integer)
    stages = db.Column(db.Text)  # JSON

    # PCS配置
    pcs_count = db.Column(db.Integer)
    pcs_power_mw = db.Column(db.Float)
    pcs_topology = db.Column(db.String(30))

    # DC侧配置
    dc_bus_voltage = db.Column(db.Float)
    dc_breaker_count = db.Column(db.Integer)
    dc_fuse_count = db.Column(db.Integer)

    # 拓扑图数据
    topology_data = db.Column(db.Text)  # JSON

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class GridComplianceAnalysis(db.Model):
    """电网合规分析模型"""
    __tablename__ = 'grid_compliance_analyses'

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))

    # 目标电网标准
    grid_standard = db.Column(db.String(50))
    grid_voltage_kv = db.Column(db.Float)
    grid_frequency_hz = db.Column(db.Float)
    grid_type = db.Column(db.String(20))

    # LVRT
    lvrt_curve = db.Column(db.Text)  # JSON
    lvrt_pass = db.Column(db.Boolean)

    # HVRT
    hvrt_curve = db.Column(db.Text)
    hvrt_pass = db.Column(db.Boolean)

    # 频率响应
    freq_response_curve = db.Column(db.Text)
    freq_response_pass = db.Column(db.Boolean)

    # 无功功率
    pf_lag = db.Column(db.Float)
    pf_lead = db.Column(db.Float)
    reactive_capacity_mvar = db.Column(db.Float)
    reactive_pass = db.Column(db.Boolean)

    # 电能质量
    thd = db.Column(db.Float)
    dc_injection = db.Column(db.Float)
    voltage_fluctuation = db.Column(db.Float)
    voltage_unbalance = db.Column(db.Float)
    power_quality_pass = db.Column(db.Boolean)

    # 防孤岛
    anti_islanding_time_s = db.Column(db.Float)
    anti_islanding_pass = db.Column(db.Boolean)

    # 通信
    comm_protocol = db.Column(db.String(50))
    remote_response_s = db.Column(db.Float)
    comm_pass = db.Column(db.Boolean)

    # 总结
    overall_pass = db.Column(db.Boolean)
    failed_items = db.Column(db.Text)  # JSON
    report_data = db.Column(db.Text)   # JSON

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SafetyFireDesign(db.Model):
    """安全与消防设计模型"""
    __tablename__ = 'safety_fire_designs'

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))

    # 系统信息
    system_capacity_mwh = db.Column(db.Float)
    container_count = db.Column(db.Integer)
    chemistry_type = db.Column(db.String(50))

    # 火灾分区
    zone_count = db.Column(db.Integer)
    zone_separation_material = db.Column(db.String(50))
    fire_resistance_rating_min = db.Column(db.Integer)

    # 可燃气体检测
    gas_detection_type = db.Column(db.String(50))
    gas_detectors_per_zone = db.Column(db.Integer)
    gas_threshold_ppm = db.Column(db.Float)

    # 热失控
    thermal_runaway_temp_c = db.Column(db.Float)
    propagation_time_min = db.Column(db.Float)
    propagation_blocked = db.Column(db.Boolean)

    # 灭火系统
    suppression_type = db.Column(db.String(50))
    suppression_capacity_kg = db.Column(db.Float)
    suppression_duration_s = db.Column(db.Float)

    # 安全间距
    container_spacing_m = db.Column(db.Float)
    wall_distance_m = db.Column(db.Float)
    access_road_width_m = db.Column(db.Float)

    # 合规
    ul_9540a_pass = db.Column(db.Boolean)
    nfpa_855_pass = db.Column(db.Boolean)
    iec_62619_pass = db.Column(db.Boolean)

    # 报告
    design_data = db.Column(db.Text)
    compliance_report = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class IPPFinancialModel(db.Model):
    """IPP项目财务模型"""
    __tablename__ = 'ipp_financial_models'

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))

    # 项目参数
    project_name = db.Column(db.String(200))
    project_life_years = db.Column(db.Integer, default=25)
    capacity_mw = db.Column(db.Float)
    energy_mwh = db.Column(db.Float)
    duration_hours = db.Column(db.Float)

    # PPA参数
    ppa_type = db.Column(db.String(30))
    capacity_price_usd_kw_month = db.Column(db.Float)
    energy_price_usd_kwh = db.Column(db.Float)
    ppa_escalation_rate = db.Column(db.Float, default=0.02)
    availability_guarantee = db.Column(db.Float, default=0.98)
    availability_penalty_usd_kw = db.Column(db.Float)

    # 性能保证
    rte_guarantee = db.Column(db.Float, default=90.0)
    soh_guarantee_year10 = db.Column(db.Float, default=70.0)
    soh_guarantee_year20 = db.Column(db.Float, default=60.0)
    performance_penalty_rate = db.Column(db.Float)

    # 投资结构
    total_capex_usd = db.Column(db.Float)
    debt_ratio = db.Column(db.Float, default=0.7)
    debt_interest_rate = db.Column(db.Float, default=0.05)
    debt_tenor_years = db.Column(db.Integer, default=15)
    equity_irr_target = db.Column(db.Float, default=0.12)

    # 运营成本
    annual_opex_usd = db.Column(db.Float)
    insurance_rate = db.Column(db.Float, default=0.005)
    land_lease_usd_year = db.Column(db.Float)

    # 计算结果
    npv_usd = db.Column(db.Float)
    irr = db.Column(db.Float)
    equity_irr = db.Column(db.Float)
    dscr_avg = db.Column(db.Float)
    dscr_min = db.Column(db.Float)
    lcoe_usd_kwh = db.Column(db.Float)
    payback_years = db.Column(db.Float)

    # 现金流
    cashflow_data = db.Column(db.Text)  # JSON

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ComplianceMatrix(db.Model):
    """合规矩阵模型"""
    __tablename__ = 'compliance_matrices'

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))

    rfp_name = db.Column(db.String(200))
    rfp_version = db.Column(db.String(50))
    rfp_standard = db.Column(db.String(50))

    matrix_data = db.Column(db.Text)  # JSON

    total_items = db.Column(db.Integer)
    compliant_count = db.Column(db.Integer)
    non_compliant_count = db.Column(db.Integer)
    partial_count = db.Column(db.Integer)

    generated_report_path = db.Column(db.String(500))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ThermalManagement(db.Model):
    """热管理设计模型"""
    __tablename__ = 'thermal_management'

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))

    # 环境条件
    ambient_max_c = db.Column(db.Float)
    ambient_min_c = db.Column(db.Float)
    ambient_avg_c = db.Column(db.Float)
    dust_level = db.Column(db.String(20))

    # 冷却方案
    cooling_type = db.Column(db.String(20))
    coolant_type = db.Column(db.String(30))
    coolant_flow_rate_lpm = db.Column(db.Float)

    # HVAC
    hvac_capacity_kw = db.Column(db.Float)
    hvac_cop = db.Column(db.Float)
    hvac_redundancy = db.Column(db.Integer)

    # 电池热参数
    cell_heat_generation_w = db.Column(db.Float)
    thermal_resistance_ckw = db.Column(db.Float)
    target_cell_temp_c = db.Column(db.Float)

    # 计算结果
    max_cell_temp_c = db.Column(db.Float)
    temp_gradient_c = db.Column(db.Float)
    cooling_power_kw = db.Column(db.Float)
    annual_cooling_energy_kwh = db.Column(db.Float)
    derating_curve = db.Column(db.Text)  # JSON

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ScadaEmsDesign(db.Model):
    """SCADA/EMS设计模型"""
    __tablename__ = 'scada_ems_designs'

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))

    # SCADA架构
    scada_architecture = db.Column(db.String(30))
    communication_protocol = db.Column(db.String(50))
    network_topology = db.Column(db.String(30))
    redundancy_level = db.Column(db.String(20))

    # 数据点
    total_data_points = db.Column(db.Integer)
    analog_points = db.Column(db.Integer)
    digital_points = db.Column(db.Integer)
    control_points = db.Column(db.Integer)

    # EMS
    ems_functions = db.Column(db.Text)  # JSON
    dispatch_strategy = db.Column(db.String(50))
    forecasting_type = db.Column(db.String(50))

    # 网络安全
    firewall_config = db.Column(db.Text)
    encryption_type = db.Column(db.String(50))
    nerc_cip_compliant = db.Column(db.Boolean)
    iec_62443_compliant = db.Column(db.Boolean)

    # 架构图
    architecture_diagram = db.Column(db.Text)  # JSON

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class HVInterconnection(db.Model):
    """高压接入设计模型"""
    __tablename__ = 'hv_interconnection'

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))

    # 并网点
    poc_voltage_kv = db.Column(db.Float)
    poc_type = db.Column(db.String(20))
    short_circuit_capacity_mva = db.Column(db.Float)
    x_r_ratio = db.Column(db.Float)

    # 变压器
    transformer_count = db.Column(db.Integer)
    transformer_capacity_mva = db.Column(db.Float)
    transformer_ratio = db.Column(db.String(50))
    transformer_vector_group = db.Column(db.String(10))
    transformer_impedance = db.Column(db.Float)

    # 开关柜
    mv_switchgear_count = db.Column(db.Integer)
    mv_switchgear_type = db.Column(db.String(30))
    mv_breaker_rating_ka = db.Column(db.Float)

    # 保护
    protection_scheme = db.Column(db.Text)  # JSON
    relay_count = db.Column(db.Integer)
    relay_type = db.Column(db.String(50))

    # 单线图
    single_line_diagram = db.Column(db.Text)  # JSON

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BidDocument(db.Model):
    """投标文档模型"""
    __tablename__ = 'bid_documents'

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))

    document_type = db.Column(db.String(50))
    title = db.Column(db.String(200))
    version = db.Column(db.String(20))

    content = db.Column(db.Text)  # JSON
    data_sources = db.Column(db.Text)  # JSON
    generated_file_path = db.Column(db.String(500))

    status = db.Column(db.String(20), default='draft')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# 添加租户关联
Tenant.correction_templates = db.relationship('CorrectionTemplate', back_populates='tenant')
Tenant.algorithm_models = db.relationship('AlgorithmModel', back_populates='tenant')

# 添加用户关联
User.correction_templates = db.relationship('CorrectionTemplate', back_populates='created_by_user')
User.algorithm_models = db.relationship('AlgorithmModel', back_populates='created_by_user')

def init_db(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()
    for model_cls in [Tenant, User, Survey, Project, Simulation,
                      BatteryPCSConfig, SohRteData, FinancialData,
                      ProductConfig, FormulaConfig,
                      SystemArchitecture, GridComplianceAnalysis,
                      SafetyFireDesign, IPPFinancialModel, ComplianceMatrix,
                      ThermalManagement, ScadaEmsDesign, HVInterconnection,
                      BidDocument, BatteryManufacturer]:
        model_cls.to_dict = _model_to_dict

    return db


def get_db_path():
    """获取数据库文件路径"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'soh_sim.db')
