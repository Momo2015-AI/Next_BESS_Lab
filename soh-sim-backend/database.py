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
    mfr = db.Column(db.String(200))
    model = db.Column(db.String(200))
    chemistry = db.Column(db.String(50))
    capacity_ah = db.Column(db.Float)
    voltage_nominal = db.Column(db.Float)
    voltage_range = db.Column(db.String(100))
    energy_wh = db.Column(db.Float)
    cycle_life = db.Column(db.Integer)
    dimensions = db.Column(db.String(200))
    weight = db.Column(db.String(100))
    soh_curve = db.Column(db.String(100))
    status = db.Column(db.String(50), default='mass-production')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ContainerProduct(db.Model):
    """集装箱产品库"""
    __tablename__ = 'container_products'

    id = db.Column(db.String(100), primary_key=True)
    mfr = db.Column(db.String(200))
    model = db.Column(db.String(200))
    type = db.Column(db.String(100))
    rated_energy_mwh = db.Column(db.Float)
    rated_power_mw = db.Column(db.Float)
    cell_model = db.Column(db.String(200))
    cell_config = db.Column(db.String(200))
    dimensions = db.Column(db.String(200))
    cooling = db.Column(db.String(100))
    weight = db.Column(db.String(100))
    cycle_life = db.Column(db.Integer)
    status = db.Column(db.String(50), default='mass-production')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class PcsProduct(db.Model):
    """PCS变流器产品库"""
    __tablename__ = 'pcs_products'

    id = db.Column(db.String(100), primary_key=True)
    mfr = db.Column(db.String(200))
    model = db.Column(db.String(200))
    rated_power_mw = db.Column(db.Float)
    rated_power_kva = db.Column(db.Float)
    ac_voltage = db.Column(db.String(100))
    dc_voltage_range = db.Column(db.String(100))
    efficiency = db.Column(db.Float)
    cooling = db.Column(db.String(100))
    topology = db.Column(db.String(100))
    isolation = db.Column(db.String(100))
    status = db.Column(db.String(50), default='mass-production')

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


class CellLibrary(db.Model):
    """电芯库模型 - 统一管理电芯产品"""
    __tablename__ = 'cell_library'
    
    id = db.Column(db.String(36), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))
    
    # 基本信息
    model = db.Column(db.String(100), nullable=False)  # 型号
    mfr = db.Column(db.String(100))  # 厂商
    chemistry = db.Column(db.String(50))  # 化学体系 LFP/NCM
    
    # 电性能参数
    capacity_ah = db.Column(db.Float)  # 额定容量 Ah
    voltage_nominal = db.Column(db.Float)  # 标称电压 V
    voltage_max = db.Column(db.Float)  # 最高电压 V
    voltage_min = db.Column(db.Float)  # 最低电压 V
    energy_wh = db.Column(db.Float)  # 能量 Wh
    
    # 寿命参数
    cycle_life = db.Column(db.Integer)  # 循环寿命 次
    calendar_life = db.Column(db.Integer)  # 日历寿命 年
    
    # 物理参数
    dimensions = db.Column(db.String(100))  # 尺寸 L*W*H mm
    weight = db.Column(db.Float)  # 重量 kg
    energy_density = db.Column(db.Float)  # 能量密度 Wh/kg
    
    # 状态与认证
    status = db.Column(db.String(50), default='mass-production')  # mass-production/pre-production
    certifications = db.Column(db.Text)  # JSON数组 认证列表
    
    # 价格信息
    unit_price = db.Column(db.Float)  # 单价 元/Wh
    
    # 备注
    remarks = db.Column(db.Text)
    
    # 时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    tenant = db.relationship('Tenant', back_populates='cell_library')


class ContainerLibrary(db.Model):
    """集装箱库模型 - 统一管理集装箱产品"""
    __tablename__ = 'container_library'
    
    id = db.Column(db.String(36), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))
    
    # 基本信息
    model = db.Column(db.String(100), nullable=False)  # 型号
    mfr = db.Column(db.String(100))  # 厂商
    spec = db.Column(db.String(50))  # 规格 20ft/40ft/20ft-H
    
    # 电气参数
    rated_energy_mwh = db.Column(db.Float)  # 额定能量 MWh
    rated_power_mw = db.Column(db.Float)  # 额定功率 MW
    dc_voltage_range = db.Column(db.String(100))  # DC电压范围
    max_dc_current = db.Column(db.Float)  # 最大直流电流 A
    
    # 电芯配置
    cell_model = db.Column(db.String(100))  # 使用电芯型号
    series_count = db.Column(db.Integer)  # 串联数量
    parallel_count = db.Column(db.Integer)  # 并联数量
    
    # 物理参数
    dimensions = db.Column(db.String(100))  # 尺寸 L*W*H mm
    weight = db.Column(db.Float)  # 重量 t
    cooling = db.Column(db.String(50))  # 散热方式
    
    # 效率参数
    rte = db.Column(db.Float)  # 往返效率 %
    
    # 辅助功耗
    aux_run = db.Column(db.Float)  # 运行功耗 kW
    aux_standby = db.Column(db.Float)  # 待机功耗 kW
    
    # 状态与认证
    status = db.Column(db.String(50), default='mass-production')
    certifications = db.Column(db.Text)  # JSON数组
    
    # 价格信息
    unit_price = db.Column(db.Float)  # 单价 万元/台
    
    # 备注
    remarks = db.Column(db.Text)
    
    # 时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    tenant = db.relationship('Tenant', back_populates='container_library')


class PCS_LIBRARY(db.Model):
    """PCS库模型 - 统一管理PCS产品"""
    __tablename__ = 'pcs_library'
    
    id = db.Column(db.String(36), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey('tenants.id'))
    
    # 基本信息
    model = db.Column(db.String(100), nullable=False)  # 型号
    mfr = db.Column(db.String(100))  # 厂商
    
    # 电气参数
    rated_power_mw = db.Column(db.Float)  # 额定功率 MW
    efficiency = db.Column(db.Float)  # 效率 %
    ac_voltage = db.Column(db.String(50))  # AC电压等级
    dc_voltage_range = db.Column(db.String(100))  # DC电压范围
    max_dc_current = db.Column(db.Float)  # 最大直流电流 A
    
    # 频率参数
    frequency_range = db.Column(db.String(50))  # 频率范围 Hz
    
    # 物理参数
    dimensions = db.Column(db.String(100))  # 尺寸
    weight = db.Column(db.Float)  # 重量 kg
    cooling = db.Column(db.String(50))  # 散热方式
    
    # 辅助功耗
    aux_run = db.Column(db.Float)  # 运行功耗 kW
    aux_standby = db.Column(db.Float)  # 待机功耗 kW
    
    # 状态与认证
    status = db.Column(db.String(50), default='mass-production')
    certifications = db.Column(db.Text)  # JSON数组
    
    # 价格信息
    unit_price = db.Column(db.Float)  # 单价 万元/台
    
    # 备注
    remarks = db.Column(db.Text)
    
    # 时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    tenant = db.relationship('Tenant', back_populates='pcs_library')


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


# 添加租户关联
Tenant.cell_library = db.relationship('CellLibrary', back_populates='tenant')
Tenant.container_library = db.relationship('ContainerLibrary', back_populates='tenant')
Tenant.pcs_library = db.relationship('PCS_LIBRARY', back_populates='tenant')
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
                      ProductConfig, FormulaConfig]:
        model_cls.to_dict = _model_to_dict

    return db


def get_db_path():
    """获取数据库文件路径"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'soh_sim.db')