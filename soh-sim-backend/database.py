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


class Tenant(db.Model):
    """租户模型 - 支持多租户数据隔离"""
    __tablename__ = 'tenants'
    
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联
    users = db.relationship('User', back_populates='tenant')
    projects = db.relationship('Project', back_populates='tenant')


class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(256))
    
    # 角色: customer(客户) / engineer(工程师) / admin(管理员)
    role = db.Column(db.String(20), default='customer')
    
    status = db.Column(db.String(20), default='active')
    is_active = db.Column(db.Boolean, default=True)
    login_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # 关联
    tenant = db.relationship('Tenant', back_populates='users')
    simulations = db.relationship('Simulation', back_populates='user')
    formula_configs = db.relationship('FormulaConfig', back_populates='user')
    project_versions = db.relationship('ProjectVersion', back_populates='created_by_user')


class Survey(db.Model):
    """调研表模型 - 存储客户填写的调研信息"""
    __tablename__ = 'surveys'
    
    id = db.Column(db.String(36), primary_key=True)
    project_name = db.Column(db.String(200), nullable=False)
    contact_person = db.Column(db.String(100))
    contact_phone = db.Column(db.String(50))
    contact_email = db.Column(db.String(100))
    
    # 项目基本信息
    location = db.Column(db.String(200))
    altitude = db.Column(db.Float)
    total_mw = db.Column(db.Float)
    total_mwh = db.Column(db.Float)
    duration = db.Column(db.Float)
    
    # 运行条件
    cycles_per_day = db.Column(db.Float, default=1.0)
    temp_max = db.Column(db.Float)
    temp_min = db.Column(db.Float)
    temp_avg = db.Column(db.Float)
    humidity = db.Column(db.Float)
    
    # 电网参数
    grid_voltage = db.Column(db.Float)
    grid_frequency = db.Column(db.Float)
    
    # 性能要求
    rte_target = db.Column(db.Float)
    soh_year1 = db.Column(db.Float)
    soh_year25 = db.Column(db.Float)
    calendar_life = db.Column(db.Integer)
    cycle_life = db.Column(db.Integer)
    availability_target = db.Column(db.Float)
    
    # 辅助参数
    aux_consumption = db.Column(db.Float)
    response_time = db.Column(db.Float)
    dc_voltage_range = db.Column(db.String(100))
    ac_voltage = db.Column(db.Float)
    thdi = db.Column(db.Float)
    
    # 其他信息
    remarks = db.Column(db.Text)
    attachments = db.Column(db.Text)
    
    # 状态与时间
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    project = db.relationship('Project', back_populates='surveys')


class Project(db.Model):
    """项目模型 - 由调研表自动生成"""
    __tablename__ = 'projects'
    
    id = db.Column(db.String(36), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(50), unique=True)
    
    # 项目状态
    status = db.Column(db.String(20), default='draft')
    stage = db.Column(db.String(50), default='survey')
    
    # 客户ID（关联到用户）
    customer_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    
    # 项目配置
    config = db.Column(db.Text)
    
    # 时间信息
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    tenant = db.relationship('Tenant', back_populates='projects')
    surveys = db.relationship('Survey', back_populates='project')
    simulations = db.relationship('Simulation', back_populates='project')
    battery_configs = db.relationship('BatteryPCSConfig', back_populates='project')
    soh_rte_data = db.relationship('SohRteData', back_populates='project')
    financial_data = db.relationship('FinancialData', back_populates='project')
    product_configs = db.relationship('ProductConfig', back_populates='project')
    versions = db.relationship('ProjectVersion', back_populates='project', order_by='desc(ProjectVersion.version_num)')


class ProjectVersion(db.Model):
    """项目版本模型 - 支持同一项目多个方案版本"""
    __tablename__ = 'project_versions'
    
    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    
    # 版本信息
    version_num = db.Column(db.Integer, default=1)  # 版本号
    name = db.Column(db.String(200))  # 版本名称，如"方案v1"
    description = db.Column(db.Text)  # 版本描述
    
    # 是否当前活跃版本
    is_active = db.Column(db.Boolean, default=True)
    
    # 版本配置数据（JSON格式存储完整的方案配置）
    config_data = db.Column(db.Text)  # 完整的方案配置
    
    # 创建者
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    
    # 状态
    status = db.Column(db.String(20), default='draft')  # draft/in-use/archived
    
    # 时间信息
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    project = db.relationship('Project', back_populates='versions')
    created_by_user = db.relationship('User', back_populates='project_versions')
    simulation_results = db.relationship('SimulationResult', back_populates='version')


class Simulation(db.Model):
    """仿真配置与结果模型"""
    __tablename__ = 'simulations'
    
    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    
    # 仿真名称与描述
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    
    # 仿真参数
    algorithm_type = db.Column(db.String(50), default='arrhenius')  # arrhenius/custom
    duration_years = db.Column(db.Integer, default=25)
    correction_factor = db.Column(db.Float, default=1.0)
    
    # 输入参数
    input_params = db.Column(db.Text)  # JSON格式存储所有输入参数
    
    # 仿真结果（25年矩阵数据）
    results = db.Column(db.Text)  # JSON格式存储结果矩阵
    
    # 手工校正因子
    manual_corrections = db.Column(db.Text)  # JSON格式
    
    # 状态
    status = db.Column(db.String(20), default='pending')  # pending/running/completed/failed
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # 时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    project = db.relationship('Project', back_populates='simulations')
    user = db.relationship('User', back_populates='simulations')


class SimulationResult(db.Model):
    """仿真结果模型 - 完整存储每次仿真结果，带日期戳便于对比"""
    __tablename__ = 'simulation_results'
    
    id = db.Column(db.String(36), primary_key=True)
    version_id = db.Column(db.String(36), db.ForeignKey('project_versions.id'))
    
    # 结果名称（项目名称+时间戳）
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    
    # 仿真类型
    simulation_type = db.Column(db.String(50))  # soh/rte/comprehensive/financial
    
    # 使用的算法模型ID
    algorithm_model_id = db.Column(db.String(36), db.ForeignKey('algorithm_models.id'))
    
    # 使用的校正因子模板ID
    correction_template_id = db.Column(db.String(36), db.ForeignKey('correction_templates.id'))
    
    # 仿真参数（输入参数快照）
    params = db.Column(db.Text)  # JSON格式
    
    # 仿真结果数据（完整存储）
    results = db.Column(db.Text)  # JSON格式，包含25年所有数据点
    
    # 关键指标摘要
    summary = db.Column(db.Text)  # JSON格式，关键指标摘要
    
    # 状态
    status = db.Column(db.String(20), default='completed')  # pending/completed/failed
    
    # 执行时间
    executed_at = db.Column(db.DateTime, default=datetime.utcnow)  # 实际执行时间戳
    execution_time_ms = db.Column(db.Integer)  # 执行耗时
    
    # 创建者
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    
    # 时间信息
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联
    version = db.relationship('ProjectVersion', back_populates='simulation_results')
    algorithm_model = db.relationship('AlgorithmModel', back_populates='simulation_results')
    correction_template = db.relationship('CorrectionTemplate', back_populates='simulation_results')


class CorrectionTemplate(db.Model):
    """校正因子模板模型 - 支持保存多个校正因子模板"""
    __tablename__ = 'correction_templates'
    
    id = db.Column(db.String(36), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))
    
    # 模板名称
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # 模板类型
    template_type = db.Column(db.String(50))  # soh/rte/comprehensive/custom
    
    # 全局校正因子
    global_soh_factor = db.Column(db.Float, default=1.0)  # SOH全局校正系数
    global_rte_factor = db.Column(db.Float, default=1.0)  # RTE全局校正系数
    
    # 年度校正表（JSON格式存储）
    annual_corrections = db.Column(db.Text)  # JSON格式 {"year_1": 0.98, "year_5": 0.95, ...}
    
    # 是否默认模板
    is_default = db.Column(db.Boolean, default=False)
    
    # 状态
    status = db.Column(db.String(20), default='active')  # active/archived
    
    # 创建者
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    
    # 时间信息
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    tenant = db.relationship('Tenant', back_populates='correction_templates')
    created_by_user = db.relationship('User', back_populates='correction_templates')
    simulation_results = db.relationship('SimulationResult', back_populates='correction_template')


class BatteryPCSConfig(db.Model):
    """电池与PCS配置模型"""
    __tablename__ = 'battery_pcs_configs'
    
    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    
    # 配置名称
    name = db.Column(db.String(200))
    
    # 电池集装箱配置
    container_model = db.Column(db.String(100))
    container_qty = db.Column(db.Integer)
    container_energy = db.Column(db.Float)  # 单个集装箱能量 MWh
    container_power = db.Column(db.Float)   # 单个集装箱功率 MW
    
    # PCS配置
    pcs_model = db.Column(db.String(100))
    pcs_qty = db.Column(db.Integer)
    pcs_power = db.Column(db.Float)  # 单个PCS功率 MW
    pcs_voltage = db.Column(db.Float)
    
    # 自动计算结果
    total_energy = db.Column(db.Float)
    total_power = db.Column(db.Float)
    pcs_ratio = db.Column(db.Float)  # PCS配比
    
    # 连接方式
    connection_type = db.Column(db.String(50))  # parallel/series/mixed
    connection_diagram = db.Column(db.Text)  # JSON格式连接图数据
    single_line_diagram = db.Column(db.Text)  # JSON格式单线图数据
    
    # 时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    project = db.relationship('Project', back_populates='battery_configs')


class SohRteData(db.Model):
    """SOH/RTE数据模型 - 25年生命周期数据"""
    __tablename__ = 'soh_rte_data'
    
    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    simulation_id = db.Column(db.String(36), db.ForeignKey('simulations.id'))
    
    # 数据名称
    name = db.Column(db.String(200))
    
    # SOH数据（25年，每年一个值）
    soh_values = db.Column(db.Text)  # JSON数组 [0.99, 0.93, ...]
    
    # RTE数据（25年，每年一个值）
    rte_values = db.Column(db.Text)  # JSON数组 [0.94, 0.93, ...]
    
    # DOD数据
    dod_values = db.Column(db.Text)  # JSON数组
    
    # 扩容数量
    aug_qty_values = db.Column(db.Text)  # JSON数组
    
    # 数据来源
    source = db.Column(db.String(50))  # manual/simulation/imported
    import_file = db.Column(db.String(200))  # 导入文件名
    
    # 时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    project = db.relationship('Project', back_populates='soh_rte_data')


class FinancialData(db.Model):
    """财务数据模型"""
    __tablename__ = 'financial_data'
    
    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    
    # 配置名称
    name = db.Column(db.String(200))
    
    # 收入模型参数
    off_peak_price = db.Column(db.Float)  # 低谷购电价 $/MWh
    peak_price = db.Column(db.Float)      # 高峰售电价 $/MWh
    spread_capture = db.Column(db.Float)  # 价差捕获率 %
    operating_days = db.Column(db.Integer)  # 运行天数
    capacity_price = db.Column(db.Float)    # 容量市场单价 $/MW-yr
    ancillary_price = db.Column(db.Float)   # 辅助服务单价 $/MW-yr
    price_escalation = db.Column(db.Float)  # 电价年涨幅 %
    
    # 成本模型参数
    capex = db.Column(db.Float)  # 初始投资 $
    capex_per_mwh = db.Column(db.Float)  # 单位投资 $/MWh
    opex_per_year = db.Column(db.Float)  # 年运维成本 $
    opex_per_mwh = db.Column(db.Float)  # 单位运维 $/MWh/yr
    augmentation_cost = db.Column(db.Float)  # 扩容成本 $
    
    # 融资参数
    debt_ratio = db.Column(db.Float)  # 贷款比例 %
    interest_rate = db.Column(db.Float)  # 贷款利率 %
    loan_term = db.Column(db.Integer)  # 贷款期限 年
    discount_rate = db.Column(db.Float)  # 折现率 %
    
    # 计算结果
    npv = db.Column(db.Float)  # 净现值
    irr = db.Column(db.Float)  # 内部收益率
    payback_years = db.Column(db.Float)  # 回收期
    lcos = db.Column(db.Float)  # 储能度电成本
    
    # 详细结果（25年现金流）
    cashflow_data = db.Column(db.Text)  # JSON格式
    
    # 时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    project = db.relationship('Project', back_populates='financial_data')


class ProductConfig(db.Model):
    """产品与方案配置模型"""
    __tablename__ = 'product_configs'
    
    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey('projects.id'))
    
    # 配置名称
    name = db.Column(db.String(200))
    
    # 电池产品配置
    cell_model = db.Column(db.String(100))
    cell_capacity = db.Column(db.Float)  # Ah
    cell_voltage = db.Column(db.Float)   # V
    cell_supplier = db.Column(db.String(100))
    
    # 集装箱产品配置
    container_model = db.Column(db.String(100))
    container_supplier = db.Column(db.String(100))
    
    # PCS产品配置
    pcs_model = db.Column(db.String(100))
    pcs_supplier = db.Column(db.String(100))
    
    # 认证要求
    certifications = db.Column(db.Text)  # JSON数组 ['UL9540', 'IEC62619', ...]
    
    # EPC配置
    epc_company = db.Column(db.String(100))
    epc_contract_type = db.Column(db.String(50))  # turnkey/performance
    
    # 时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    project = db.relationship('Project', back_populates='product_configs')


class CellProduct(db.Model):
    """电芯产品库"""
    __tablename__ = 'cell_products'

    id = db.Column(db.String(100), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))  # 企业隔离
    is_builtin = db.Column(db.Boolean, default=False)  # 是否系统内置（对所有企业可见）
    manufacturer_id = db.Column(db.String(36), db.ForeignKey('battery_manufacturers.id'))  # 关联电池厂家
    mfr = db.Column(db.String(200))
    model = db.Column(db.String(200))
    chemistry = db.Column(db.String(50))
    capacity_ah = db.Column(db.Float)
    voltage_nominal = db.Column(db.Float)
    voltage_max = db.Column(db.Float)
    voltage_min = db.Column(db.Float)
    voltage_range = db.Column(db.String(100))
    rated_energy_mwh = db.Column(db.Float)  # MWh
    cycle_life = db.Column(db.Integer)
    calendar_life = db.Column(db.Integer)  # 日历寿命 年
    energy_density = db.Column(db.Float)  # Wh/kg
    dimensions = db.Column(db.String(200))
    weight = db.Column(db.Float)  # kg
    soh_curve = db.Column(db.String(100))
    certifications = db.Column(db.Text)  # JSON
    unit_price = db.Column(db.Float)  # 元/Wh
    remarks = db.Column(db.Text)
    status = db.Column(db.String(50), default='mass-production')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    manufacturer = db.relationship('BatteryManufacturer', back_populates='cells')
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class PackProduct(db.Model):
    """电池包产品库"""
    __tablename__ = 'pack_products'

    id = db.Column(db.String(100), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))
    is_builtin = db.Column(db.Boolean, default=False)
    manufacturer_id = db.Column(db.String(36), db.ForeignKey('battery_manufacturers.id'))  # 关联电池厂家
    mfr = db.Column(db.String(200))
    model = db.Column(db.String(200))
    chemistry = db.Column(db.String(50))
    cell_model = db.Column(db.String(200))
    cells_per_pack = db.Column(db.Integer)
    series_count = db.Column(db.Integer)
    parallel_count = db.Column(db.Integer)
    nominal_voltage = db.Column(db.Float)
    nominal_capacity_ah = db.Column(db.Float)
    rated_energy_mwh = db.Column(db.Float)  # MWh, was nominal_energy_kwh
    max_charge_current = db.Column(db.Float)
    max_discharge_current = db.Column(db.Float)
    dimensions = db.Column(db.String(200))
    weight = db.Column(db.Float)  # kg
    bms_type = db.Column(db.String(100))
    cycle_life = db.Column(db.Integer)
    status = db.Column(db.String(50), default='mass-production')
    
    # 关联
    manufacturer = db.relationship('BatteryManufacturer', back_populates='packs')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class RackProduct(db.Model):
    """电池架产品库"""
    __tablename__ = 'rack_products'

    id = db.Column(db.String(100), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))
    is_builtin = db.Column(db.Boolean, default=False)
    manufacturer_id = db.Column(db.String(36), db.ForeignKey('battery_manufacturers.id'))  # 关联电池厂家
    mfr = db.Column(db.String(200))
    model = db.Column(db.String(200))
    pack_model = db.Column(db.String(200))
    packs_per_rack = db.Column(db.Integer)
    series_count = db.Column(db.Integer)
    parallel_count = db.Column(db.Integer)
    nominal_voltage = db.Column(db.Float)
    nominal_capacity_ah = db.Column(db.Float)
    rated_energy_mwh = db.Column(db.Float)  # MWh, was nominal_energy_kwh
    dimensions = db.Column(db.String(200))
    weight = db.Column(db.Float)  # kg
    cooling = db.Column(db.String(100))
    status = db.Column(db.String(50), default='mass-production')
    
    # 关联
    manufacturer = db.relationship('BatteryManufacturer', back_populates='racks')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ClusterProduct(db.Model):
    """电池簇产品库"""
    __tablename__ = 'cluster_products'

    id = db.Column(db.String(100), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))
    is_builtin = db.Column(db.Boolean, default=False)
    manufacturer_id = db.Column(db.String(36), db.ForeignKey('battery_manufacturers.id'))  # 关联电池厂家
    mfr = db.Column(db.String(200))
    model = db.Column(db.String(200))
    rack_model = db.Column(db.String(200))
    racks_per_cluster = db.Column(db.Integer)
    series_count = db.Column(db.Integer)
    parallel_count = db.Column(db.Integer)
    nominal_voltage = db.Column(db.Float)
    nominal_capacity_ah = db.Column(db.Float)
    rated_energy_mwh = db.Column(db.Float)  # MWh, was nominal_energy_mwh (统一命名)
    rated_power_mw = db.Column(db.Float)  # MW, was nominal_power_mw (统一命名)
    dimensions = db.Column(db.String(200))
    weight = db.Column(db.Float)  # kg
    bmu_type = db.Column(db.String(100))
    status = db.Column(db.String(50), default='mass-production')
    
    # 关联
    manufacturer = db.relationship('BatteryManufacturer', back_populates='clusters')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ContainerProduct(db.Model):
    """集装箱产品库（统一入口，合并原 container_library）"""
    __tablename__ = 'container_products'

    id = db.Column(db.String(100), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))
    is_builtin = db.Column(db.Boolean, default=False)
    manufacturer_id = db.Column(db.String(36), db.ForeignKey('battery_manufacturers.id'))  # 关联电池厂家
    mfr = db.Column(db.String(200))
    model = db.Column(db.String(200))
    spec = db.Column(db.String(100))  # 规格，was type
    rated_energy_mwh = db.Column(db.Float)  # MWh
    rated_power_mw = db.Column(db.Float)  # MW
    cluster_model = db.Column(db.String(200))
    clusters_per_container = db.Column(db.Integer)
    cell_model = db.Column(db.String(200))
    cell_config = db.Column(db.String(200))
    series_count = db.Column(db.Integer)
    parallel_count = db.Column(db.Integer)
    dc_voltage_range = db.Column(db.String(100))
    max_dc_current = db.Column(db.Float)
    dimensions = db.Column(db.String(200))
    cooling = db.Column(db.String(100))
    weight = db.Column(db.Float)  # t
    cycle_life = db.Column(db.Integer)
    rte = db.Column(db.Float)  # 往返效率 %
    aux_run = db.Column(db.Float)  # kW
    aux_standby = db.Column(db.Float)  # kW
    certifications = db.Column(db.Text)  # JSON
    unit_price = db.Column(db.Float)  # 万元/台
    remarks = db.Column(db.Text)
    status = db.Column(db.String(50), default='mass-production')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    manufacturer = db.relationship('BatteryManufacturer', back_populates='containers')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class PcsProduct(db.Model):
    """PCS变流器产品库（统一入口，合并原 pcs_library）"""
    __tablename__ = 'pcs_products'

    id = db.Column(db.String(100), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))
    is_builtin = db.Column(db.Boolean, default=False)
    manufacturer_id = db.Column(db.String(36), db.ForeignKey('battery_manufacturers.id'))  # 关联厂家
    mfr = db.Column(db.String(200))
    model = db.Column(db.String(200))
    rated_power_mw = db.Column(db.Float)  # MW
    rated_power_kva = db.Column(db.Float)  # KVA
    ac_voltage = db.Column(db.String(100))
    dc_voltage_range = db.Column(db.String(100))
    max_dc_current = db.Column(db.Float)  # A
    frequency_range = db.Column(db.String(50))  # Hz
    efficiency = db.Column(db.Float)  # %
    cooling = db.Column(db.String(100))
    topology = db.Column(db.String(100))
    isolation = db.Column(db.String(100))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.Float)  # kg
    aux_run = db.Column(db.Float)  # kW
    aux_standby = db.Column(db.Float)  # kW
    certifications = db.Column(db.Text)  # JSON
    unit_price = db.Column(db.Float)  # 万元/台
    remarks = db.Column(db.Text)
    status = db.Column(db.String(50), default='mass-production')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    manufacturer = db.relationship('BatteryManufacturer', back_populates='pcs')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class BatteryConfigRule(db.Model):
    """电池层级配置规则模型"""
    __tablename__ = 'battery_config_rules'

    id = db.Column(db.String(36), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))
    is_builtin = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    cell_model = db.Column(db.String(100))
    pack_model = db.Column(db.String(100))
    rack_model = db.Column(db.String(100))
    cluster_model = db.Column(db.String(100))
    container_model = db.Column(db.String(100))
    
    cells_per_pack = db.Column(db.Integer)
    packs_per_rack = db.Column(db.Integer)
    racks_per_cluster = db.Column(db.Integer)
    clusters_per_container = db.Column(db.Integer)
    
    series_per_pack = db.Column(db.Integer)
    parallel_per_pack = db.Column(db.Integer)
    series_per_rack = db.Column(db.Integer)
    parallel_per_rack = db.Column(db.Integer)
    series_per_cluster = db.Column(db.Integer)
    parallel_per_cluster = db.Column(db.Integer)
    
    pack_nominal_voltage = db.Column(db.Float)
    pack_nominal_capacity_ah = db.Column(db.Float)
    pack_nominal_energy_kwh = db.Column(db.Float)
    
    rack_nominal_voltage = db.Column(db.Float)
    rack_nominal_capacity_ah = db.Column(db.Float)
    rack_nominal_energy_kwh = db.Column(db.Float)
    
    cluster_nominal_voltage = db.Column(db.Float)
    cluster_nominal_capacity_ah = db.Column(db.Float)
    cluster_nominal_energy_mwh = db.Column(db.Float)
    cluster_nominal_power_mw = db.Column(db.Float)
    
    container_nominal_energy_mwh = db.Column(db.Float)
    container_nominal_power_mw = db.Column(db.Float)
    
    is_default = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(50), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class FormulaConfig(db.Model):
    """算法公式配置模型 - 支持自定义公式"""
    __tablename__ = 'formula_configs'
    
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    
    # 公式名称
    name = db.Column(db.String(200))
    
    # 公式类型
    formula_type = db.Column(db.String(50))  # soh/rte/financial/custom
    
    # 公式表达式
    expression = db.Column(db.Text)  # 数学表达式
    
    # 参数定义
    parameters = db.Column(db.Text)  # JSON格式参数定义
    
    # 公式说明
    description = db.Column(db.Text)
    
    # 是否公开
    is_public = db.Column(db.Boolean, default=False)
    
    # 时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    user = db.relationship('User', back_populates='formula_configs')


class AlgorithmModel(db.Model):
    """算法模型库 - 支持添加和管理多种衰减模型"""
    __tablename__ = 'algorithm_models'
    
    id = db.Column(db.String(36), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))
    
    # 模型基本信息
    name = db.Column(db.String(200), nullable=False)  # 模型名称
    name_en = db.Column(db.String(200))  # 英文名称
    model_type = db.Column(db.String(50))  # 模型类型: double_exponential/linear_log/arrhenius/rainflow/semi_empirical/custom
    
    # 适用场景
    applicable_scenarios = db.Column(db.Text)  # JSON数组，如 ["LFP日历衰减", "循环衰减"]
    
    # 数学形式/公式表达式
    mathematical_form = db.Column(db.Text)  # 数学形式描述
    formula_expression = db.Column(db.Text)  # 可执行的公式表达式
    
    # 参数定义（JSON格式）
    parameters = db.Column(db.Text)  # 参数定义 {"param_name": {"label": "", "default": 0.0, "min": 0, "max": 100}}
    
    # 精度等级
    accuracy_level = db.Column(db.String(20))  # low/medium/high
    accuracy_desc = db.Column(db.String(200))  # 精度描述，如 "R²>0.999"
    
    # 模型分类
    category = db.Column(db.String(50))  # soh/rte/comprehensive
    
    # 是否内置模型（不可删除）
    is_builtin = db.Column(db.Boolean, default=False)
    
    # 是否启用
    is_active = db.Column(db.Boolean, default=True)
    
    # 排序
    sort_order = db.Column(db.Integer, default=0)
    
    # 描述
    description = db.Column(db.Text)
    
    # 创建者
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    
    # 时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    tenant = db.relationship('Tenant', back_populates='algorithm_models')
    created_by_user = db.relationship('User', back_populates='algorithm_models')
    simulation_results = db.relationship('SimulationResult', back_populates='algorithm_model')


class BatteryManufacturer(db.Model):
    """电池厂家模型 - 存储各主流厂家的SOH/RTE校准参数"""
    __tablename__ = 'battery_manufacturers'
    
    id = db.Column(db.String(36), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))
    
    # 厂家基本信息
    name = db.Column(db.String(200), nullable=False)  # 厂家名称
    name_en = db.Column(db.String(200))  # 英文名称
    country = db.Column(db.String(100))  # 国家
    logo_url = db.Column(db.String(500))  # 厂家Logo
    
    # 电池类型
    chemistry_type = db.Column(db.String(50))  # 化学体系: LFP/NCM/NCA/LTO
    
    # 校准后的Arrhenius参数（JSON格式存储）
    calibrated_params = db.Column(db.Text)  # {"A_cal": 0.02, "Ea_cal": 20000, ...}
    
    # 精度指标
    rmse_soh = db.Column(db.Float)  # SOH预测RMSE (%)
    rmse_rte = db.Column(db.Float)  # RTE预测RMSE (%)
    data_points = db.Column(db.Integer)  # 训练数据点数量
    
    # 适用场景
    applicable_scenarios = db.Column(db.Text)  # JSON数组
    
    # 是否内置（预设厂家）
    is_builtin = db.Column(db.Boolean, default=False)
    
    # 是否启用
    is_active = db.Column(db.Boolean, default=True)
    
    # 排序
    sort_order = db.Column(db.Integer, default=0)
    
    # 描述
    description = db.Column(db.Text)
    
    # 时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 反向关联
    cells = db.relationship('CellProduct', back_populates='manufacturer')
    packs = db.relationship('PackProduct', back_populates='manufacturer')
    racks = db.relationship('RackProduct', back_populates='manufacturer')
    clusters = db.relationship('ClusterProduct', back_populates='manufacturer')
    containers = db.relationship('ContainerProduct', back_populates='manufacturer')
    pcs = db.relationship('PcsProduct', back_populates='manufacturer')
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


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
    """初始化数据库"""
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # 给所有模型挂上 to_dict 方法（一次性，避免每类重复定义）
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