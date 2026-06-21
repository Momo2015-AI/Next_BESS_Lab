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
    role = db.Column(db.String(20), default='user')  # admin/engineer/user
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # 关联
    tenant = db.relationship('Tenant', back_populates='users')
    simulations = db.relationship('Simulation', back_populates='user')


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


def init_db(app):
    """初始化数据库"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return db


def get_db_path():
    """获取数据库文件路径"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'soh_sim.db')