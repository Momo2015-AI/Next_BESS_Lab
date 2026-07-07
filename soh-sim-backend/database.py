"""
数据库配置与模型定义
使用SQLite作为数据库，支持跨平台运行
完整支持所有功能模块的数据存储
"""

import json
import os
from datetime import datetime, timezone

# 统一使用 timezone-aware UTC 时间，替代已弃用的 _utcnow
_utcnow = lambda: datetime.now(timezone.utc)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index, event, inspect, text
from sqlalchemy.orm import Session as _OrmSession

db = SQLAlchemy()

# 租户隔离模型：flush 前自动从父项目继承 tenant_id
_TENANT_PROJECT_MODELS = {
    "SystemArchitecture", "GridComplianceAnalysis", "SafetyFireDesign",
    "IPPFinancialModel", "ComplianceMatrix", "ThermalManagement",
    "ScadaEmsDesign", "HVInterconnection", "BidDocument",
}


@event.listens_for(_OrmSession, "before_flush")
def _inherit_tenant_from_project(session, flush_context, instances):
    """新建 EPC 对象若未显式设置 tenant_id，则从所属项目继承，确保租户隔离。"""
    for obj in session.new:
        if type(obj).__name__ in _TENANT_PROJECT_MODELS:
            if getattr(obj, "tenant_id", None) is None and getattr(obj, "project_id", None):
                with session.no_autoflush:
                    proj = session.get(Project, obj.project_id)
                if proj is not None:
                    obj.tenant_id = proj.tenant_id

# 这些列存储 JSON 字符串，序列化时需要解析回对象
_JSON_COLUMNS = {
    "Survey": {"attachments"},
    "Project": {"config"},
    "ProjectVersion": {"config_data"},
    "Simulation": {"input_params", "results", "manual_corrections"},
    "SimulationResult": {"params", "results", "summary"},
    "CorrectionTemplate": {"annual_corrections"},
    "BatteryPCSConfig": {"connection_diagram", "single_line_diagram"},
    "SohRteData": {"soh_values", "rte_values", "dod_values", "aug_qty_values"},
    "FinancialData": {"cashflow_data"},
    "ProductConfig": {"certifications"},
    "CellProduct": {"certifications"},
    "ContainerProduct": {"certifications"},
    "PcsProduct": {"certifications"},
    "FormulaConfig": {"parameters"},
    "AlgorithmModel": {"parameters", "applicable_scenarios"},
    "BatteryManufacturer": {"calibrated_params"},
    "SystemArchitecture": {"data"},
    "GridComplianceAnalysis": {"data"},
    "SafetyFireDesign": {"data"},
    "IPPFinancialModel": {"data"},
    "ComplianceMatrix": {"data"},
    "ThermalManagement": {"data"},
    "ScadaEmsDesign": {"data"},
    "HVInterconnection": {"data"},
    "BidDocument": {"data"},
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

    __tablename__ = "tenants"

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True)
    status = db.Column(db.String(20), default="active")
    created_at = db.Column(db.DateTime, default=_utcnow)

    # 关联
    users = db.relationship("User", back_populates="tenant")
    projects = db.relationship("Project", back_populates="tenant")


class User(db.Model):
    """用户模型"""

    __tablename__ = "users"

    __table_args__ = (db.Index("idx_users_tenant_id", "tenant_id"),)

    id = db.Column(db.String(36), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey("tenants.id"))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(256))

    # 角色: customer(客户) / engineer(工程师) / admin(管理员)
    role = db.Column(db.String(20), default="customer")

    status = db.Column(db.String(20), default="active")
    is_active = db.Column(db.Boolean, default=True)
    login_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)
    last_login = db.Column(db.DateTime)

    # 关联
    tenant = db.relationship("Tenant", back_populates="users")
    simulations = db.relationship("Simulation", back_populates="user")
    formula_configs = db.relationship("FormulaConfig", back_populates="user")
    project_versions = db.relationship("ProjectVersion", back_populates="created_by_user")

    def to_dict(self):
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "status": self.status,
            "is_active": self.is_active,
            "login_count": self.login_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }


class Survey(db.Model):
    """调研表模型 - 存储客户填写的调研信息"""

    __tablename__ = "surveys"

    __table_args__ = (db.Index("idx_surveys_project_id", "project_id"),)

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
    pcc_voltage = db.Column(db.Float)
    pcc_short_circuit_mva = db.Column(db.Float)
    grid_code = db.Column(db.String(50))

    # 环境条件
    sand_protection = db.Column(db.String(10))
    humidity_cycle = db.Column(db.String(20))

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
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    # 关联
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"))
    project = db.relationship("Project", back_populates="surveys")

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "project_name": self.project_name,
            "contact_person": self.contact_person,
            "contact_phone": self.contact_phone,
            "contact_email": self.contact_email,
            "location": self.location,
            "altitude": self.altitude,
            "total_mw": self.total_mw,
            "total_mwh": self.total_mwh,
            "duration": self.duration,
            "cycles_per_day": self.cycles_per_day,
            "temp_max": self.temp_max,
            "temp_min": self.temp_min,
            "temp_avg": self.temp_avg,
            "humidity": self.humidity,
            "grid_voltage": self.grid_voltage,
            "grid_frequency": self.grid_frequency,
            "pcc_voltage": self.pcc_voltage,
            "pcc_short_circuit_mva": self.pcc_short_circuit_mva,
            "grid_code": self.grid_code,
            "sand_protection": self.sand_protection,
            "humidity_cycle": self.humidity_cycle,
            "rte_target": self.rte_target,
            "soh_year1": self.soh_year1,
            "soh_year25": self.soh_year25,
            "calendar_life": self.calendar_life,
            "cycle_life": self.cycle_life,
            "availability_target": self.availability_target,
            "aux_consumption": self.aux_consumption,
            "response_time": self.response_time,
            "dc_voltage_range": self.dc_voltage_range,
            "ac_voltage": self.ac_voltage,
            "thdi": self.thdi,
            "remarks": self.remarks,
            "attachments": self.attachments,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Project(db.Model):
    """项目模型 - 由调研表自动生成"""

    __tablename__ = "projects"

    __table_args__ = (
        db.Index("idx_projects_tenant_id", "tenant_id"),
        db.Index("idx_projects_customer_id", "customer_id"),
    )

    id = db.Column(db.String(36), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey("tenants.id"))
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(50), unique=True)

    # 项目状态
    status = db.Column(db.String(20), default="draft")
    stage = db.Column(db.String(50), default="survey")

    # 客户ID（关联到用户）
    customer_id = db.Column(db.String(36), db.ForeignKey("users.id"))

    # 项目配置
    config = db.Column(db.Text)

    # 时间信息
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    # 关联
    tenant = db.relationship("Tenant", back_populates="projects")
    surveys = db.relationship("Survey", back_populates="project")
    simulations = db.relationship("Simulation", back_populates="project")
    battery_configs = db.relationship("BatteryPCSConfig", back_populates="project")
    soh_rte_data = db.relationship("SohRteData", back_populates="project")
    financial_data = db.relationship("FinancialData", back_populates="project")
    product_configs = db.relationship("ProductConfig", back_populates="project")
    versions = db.relationship("ProjectVersion", back_populates="project", order_by="desc(ProjectVersion.version_num)")

    def to_dict(self):
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "code": self.code,
            "status": self.status,
            "stage": self.stage,
            "customer_id": self.customer_id,
            "config": self.config,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class ProjectVersion(db.Model):
    """项目版本模型 - 支持同一项目多个方案版本"""

    __tablename__ = "project_versions"

    __table_args__ = (
        db.Index("idx_project_versions_project_id", "project_id"),
        db.Index("idx_project_versions_created_by", "created_by"),
    )

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"))

    # 版本信息
    version_num = db.Column(db.Integer, default=1)  # 版本号
    name = db.Column(db.String(200))  # 版本名称，如"方案v1"
    description = db.Column(db.Text)  # 版本描述

    # 是否当前活跃版本
    is_active = db.Column(db.Boolean, default=True)

    # 版本配置数据（JSON格式存储完整的方案配置）
    config_data = db.Column(db.Text)  # 完整的方案配置

    # 创建者
    created_by = db.Column(db.String(36), db.ForeignKey("users.id"))

    # 状态
    status = db.Column(db.String(20), default="draft")  # draft/in-use/archived

    # 时间信息
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    # 关联
    project = db.relationship("Project", back_populates="versions")
    created_by_user = db.relationship("User", back_populates="project_versions")
    simulation_results = db.relationship("SimulationResult", back_populates="version")

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "version_num": self.version_num,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "config_data": self.config_data,
            "created_by": self.created_by,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Simulation(db.Model):
    """仿真配置与结果模型"""

    __tablename__ = "simulations"

    __table_args__ = (
        db.Index("idx_simulations_project_id", "project_id"),
        db.Index("idx_simulations_user_id", "user_id"),
    )

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"))

    # 仿真名称与描述
    name = db.Column(db.String(200))
    description = db.Column(db.Text)

    # 仿真参数
    algorithm_type = db.Column(db.String(50), default="arrhenius")  # arrhenius/custom
    duration_years = db.Column(db.Integer, default=25)
    correction_factor = db.Column(db.Float, default=1.0)

    # 输入参数
    input_params = db.Column(db.Text)  # JSON格式存储所有输入参数

    # 仿真结果（25年矩阵数据）
    results = db.Column(db.Text)  # JSON格式存储结果矩阵

    # 手工校正因子
    manual_corrections = db.Column(db.Text)  # JSON格式

    # 状态
    status = db.Column(db.String(20), default="pending")  # pending/running/completed/failed
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)

    # 时间
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    # 关联
    project = db.relationship("Project", back_populates="simulations")
    user = db.relationship("User", back_populates="simulations")

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "algorithm_type": self.algorithm_type,
            "duration_years": self.duration_years,
            "correction_factor": self.correction_factor,
            "input_params": self.input_params,
            "results": self.results,
            "manual_corrections": self.manual_corrections,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class SimulationResult(db.Model):
    """仿真结果模型 - 完整存储每次仿真结果，带日期戳便于对比"""

    __tablename__ = "simulation_results"

    __table_args__ = (
        db.Index("idx_simulation_results_version_id", "version_id"),
        db.Index("idx_simulation_results_algorithm_model_id", "algorithm_model_id"),
        db.Index("idx_simulation_results_correction_template_id", "correction_template_id"),
        db.Index("idx_simulation_results_created_by", "created_by"),
    )

    id = db.Column(db.String(36), primary_key=True)
    version_id = db.Column(db.String(36), db.ForeignKey("project_versions.id"))

    # 结果名称（项目名称+时间戳）
    name = db.Column(db.String(200))
    description = db.Column(db.Text)

    # 仿真类型
    simulation_type = db.Column(db.String(50))  # soh/rte/comprehensive/financial

    # 使用的算法模型ID
    algorithm_model_id = db.Column(db.String(36), db.ForeignKey("algorithm_models.id"))

    # 使用的校正因子模板ID
    correction_template_id = db.Column(db.String(36), db.ForeignKey("correction_templates.id"))

    # 仿真参数（输入参数快照）
    params = db.Column(db.Text)  # JSON格式

    # 仿真结果数据（完整存储）
    results = db.Column(db.Text)  # JSON格式，包含25年所有数据点

    # 关键指标摘要
    summary = db.Column(db.Text)  # JSON格式，关键指标摘要

    # 状态
    status = db.Column(db.String(20), default="completed")  # pending/completed/failed

    # 执行时间
    executed_at = db.Column(db.DateTime, default=_utcnow)  # 实际执行时间戳
    execution_time_ms = db.Column(db.Integer)  # 执行耗时

    # 创建者
    created_by = db.Column(db.String(36), db.ForeignKey("users.id"))

    # 时间信息
    created_at = db.Column(db.DateTime, default=_utcnow)

    # 关联
    version = db.relationship("ProjectVersion", back_populates="simulation_results")
    algorithm_model = db.relationship("AlgorithmModel", back_populates="simulation_results")
    correction_template = db.relationship("CorrectionTemplate", back_populates="simulation_results")

    def to_dict(self):
        return {
            "id": self.id,
            "version_id": self.version_id,
            "name": self.name,
            "description": self.description,
            "simulation_type": self.simulation_type,
            "algorithm_model_id": self.algorithm_model_id,
            "correction_template_id": self.correction_template_id,
            "params": self.params,
            "results": self.results,
            "summary": self.summary,
            "status": self.status,
            "executed_at": self.executed_at.isoformat() if self.executed_at else None,
            "execution_time_ms": self.execution_time_ms,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class CorrectionTemplate(db.Model):
    """校正因子模板模型 - 支持保存多个校正因子模板"""

    __tablename__ = "correction_templates"

    __table_args__ = (
        db.Index("idx_correction_templates_tenant_id", "tenant_id"),
        db.Index("idx_correction_templates_created_by", "created_by"),
    )

    id = db.Column(db.String(36), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey("tenants.id"))

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
    status = db.Column(db.String(20), default="active")  # active/archived

    # 创建者
    created_by = db.Column(db.String(36), db.ForeignKey("users.id"))

    # 时间信息
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    # 关联
    tenant = db.relationship("Tenant", back_populates="correction_templates")
    created_by_user = db.relationship("User", back_populates="correction_templates")
    simulation_results = db.relationship("SimulationResult", back_populates="correction_template")

    def to_dict(self):
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "description": self.description,
            "template_type": self.template_type,
            "global_soh_factor": self.global_soh_factor,
            "global_rte_factor": self.global_rte_factor,
            "annual_corrections": self.annual_corrections,
            "is_default": self.is_default,
            "status": self.status,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class BatteryPCSConfig(db.Model):
    """电池与PCS配置模型"""

    __tablename__ = "battery_pcs_configs"

    __table_args__ = (db.Index("idx_battery_pcs_configs_project_id", "project_id"),)

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"))

    # 配置名称
    name = db.Column(db.String(200))

    # 电池集装箱配置
    container_model = db.Column(db.String(100))
    container_qty = db.Column(db.Integer)
    container_energy = db.Column(db.Float)  # 单个集装箱能量 MWh
    container_power = db.Column(db.Float)  # 单个集装箱功率 MW

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
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    # 关联
    project = db.relationship("Project", back_populates="battery_configs")

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "container_model": self.container_model,
            "container_qty": self.container_qty,
            "container_energy": self.container_energy,
            "container_power": self.container_power,
            "pcs_model": self.pcs_model,
            "pcs_qty": self.pcs_qty,
            "pcs_power": self.pcs_power,
            "pcs_voltage": self.pcs_voltage,
            "total_energy": self.total_energy,
            "total_power": self.total_power,
            "pcs_ratio": self.pcs_ratio,
            "connection_type": self.connection_type,
            "connection_diagram": self.connection_diagram,
            "single_line_diagram": self.single_line_diagram,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class SohRteData(db.Model):
    """SOH/RTE数据模型 - 25年生命周期数据"""

    __tablename__ = "soh_rte_data"

    __table_args__ = (
        db.Index("idx_soh_rte_data_project_id", "project_id"),
        db.Index("idx_soh_rte_data_simulation_id", "simulation_id"),
    )

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"))
    simulation_id = db.Column(db.String(36), db.ForeignKey("simulations.id"))

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
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    # 关联
    project = db.relationship("Project", back_populates="soh_rte_data")

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "simulation_id": self.simulation_id,
            "name": self.name,
            "soh_values": self.soh_values,
            "rte_values": self.rte_values,
            "dod_values": self.dod_values,
            "aug_qty_values": self.aug_qty_values,
            "source": self.source,
            "import_file": self.import_file,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class FinancialData(db.Model):
    """财务数据模型"""

    __tablename__ = "financial_data"

    __table_args__ = (db.Index("idx_financial_data_project_id", "project_id"),)

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"))

    # 配置名称
    name = db.Column(db.String(200))

    # 收入模型参数
    off_peak_price = db.Column(db.Float)  # 低谷购电价 $/MWh
    peak_price = db.Column(db.Float)  # 高峰售电价 $/MWh
    spread_capture = db.Column(db.Float)  # 价差捕获率 %
    operating_days = db.Column(db.Integer)  # 运行天数
    capacity_price = db.Column(db.Float)  # 容量市场单价 $/MW-yr
    ancillary_price = db.Column(db.Float)  # 辅助服务单价 $/MW-yr
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

    # 单位体系
    currency = db.Column(db.String(3), default="USD")
    unit_system = db.Column(db.String(10), default="metric")

    # 详细结果（25年现金流）
    cashflow_data = db.Column(db.Text)  # JSON格式

    # 时间
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    # 关联
    project = db.relationship("Project", back_populates="financial_data")

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "off_peak_price": self.off_peak_price,
            "peak_price": self.peak_price,
            "spread_capture": self.spread_capture,
            "operating_days": self.operating_days,
            "capacity_price": self.capacity_price,
            "ancillary_price": self.ancillary_price,
            "price_escalation": self.price_escalation,
            "capex": self.capex,
            "capex_per_mwh": self.capex_per_mwh,
            "opex_per_year": self.opex_per_year,
            "opex_per_mwh": self.opex_per_mwh,
            "augmentation_cost": self.augmentation_cost,
            "debt_ratio": self.debt_ratio,
            "interest_rate": self.interest_rate,
            "loan_term": self.loan_term,
            "discount_rate": self.discount_rate,
            "npv": self.npv,
            "irr": self.irr,
            "payback_years": self.payback_years,
            "lcos": self.lcos,
            "currency": self.currency,
            "unit_system": self.unit_system,
            "cashflow_data": self.cashflow_data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class ProductConfig(db.Model):
    """产品与方案配置模型"""

    __tablename__ = "product_configs"

    __table_args__ = (db.Index("idx_product_configs_project_id", "project_id"),)

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"))

    # 配置名称
    name = db.Column(db.String(200))

    # 电池产品配置
    cell_model = db.Column(db.String(100))
    cell_capacity = db.Column(db.Float)  # Ah
    cell_voltage = db.Column(db.Float)  # V
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
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    # 关联
    project = db.relationship("Project", back_populates="product_configs")

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "cell_model": self.cell_model,
            "cell_capacity": self.cell_capacity,
            "cell_voltage": self.cell_voltage,
            "cell_supplier": self.cell_supplier,
            "container_model": self.container_model,
            "container_supplier": self.container_supplier,
            "pcs_model": self.pcs_model,
            "pcs_supplier": self.pcs_supplier,
            "certifications": self.certifications,
            "epc_company": self.epc_company,
            "epc_contract_type": self.epc_contract_type,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class CellProduct(db.Model):
    """电芯产品库"""

    __tablename__ = "cell_products"

    __table_args__ = (db.Index("idx_cell_products_tenant_id", "tenant_id"),)

    id = db.Column(db.String(100), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey("tenants.id"))  # 企业隔离
    is_builtin = db.Column(db.Boolean, default=False)  # 是否系统内置（对所有企业可见）
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
    status = db.Column(db.String(50), default="mass-production")
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    def to_dict(self):
        return _model_to_dict(self)


class PackProduct(db.Model):
    """电池包产品库"""

    __tablename__ = "pack_products"

    __table_args__ = (db.Index("idx_pack_products_tenant_id", "tenant_id"),)

    id = db.Column(db.String(100), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey("tenants.id"))
    is_builtin = db.Column(db.Boolean, default=False)
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
    status = db.Column(db.String(50), default="mass-production")

    def to_dict(self):
        return _model_to_dict(self)


class RackProduct(db.Model):
    """电池架产品库"""

    __tablename__ = "rack_products"

    __table_args__ = (db.Index("idx_rack_products_tenant_id", "tenant_id"),)

    id = db.Column(db.String(100), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey("tenants.id"))
    is_builtin = db.Column(db.Boolean, default=False)
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
    status = db.Column(db.String(50), default="mass-production")

    def to_dict(self):
        return _model_to_dict(self)


class ClusterProduct(db.Model):
    """电池簇产品库"""

    __tablename__ = "cluster_products"

    __table_args__ = (db.Index("idx_cluster_products_tenant_id", "tenant_id"),)

    id = db.Column(db.String(100), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey("tenants.id"))
    is_builtin = db.Column(db.Boolean, default=False)
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
    status = db.Column(db.String(50), default="mass-production")

    def to_dict(self):
        return _model_to_dict(self)


class ContainerProduct(db.Model):
    """集装箱产品库（统一入口，合并原 container_library）"""

    __tablename__ = "container_products"

    __table_args__ = (db.Index("idx_container_products_tenant_id", "tenant_id"),)

    id = db.Column(db.String(100), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey("tenants.id"))
    is_builtin = db.Column(db.Boolean, default=False)
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
    status = db.Column(db.String(50), default="mass-production")
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    def to_dict(self):
        return _model_to_dict(self)


class PcsProduct(db.Model):
    """PCS变流器产品库（统一入口，合并原 pcs_library）"""

    __tablename__ = "pcs_products"

    __table_args__ = (db.Index("idx_pcs_products_tenant_id", "tenant_id"),)

    id = db.Column(db.String(100), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey("tenants.id"))
    is_builtin = db.Column(db.Boolean, default=False)
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
    status = db.Column(db.String(50), default="mass-production")
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    def to_dict(self):
        return _model_to_dict(self)


class BatteryConfigRule(db.Model):
    """电池层级配置规则模型"""

    __tablename__ = "battery_config_rules"

    __table_args__ = (db.Index("idx_battery_config_rules_tenant_id", "tenant_id"),)

    id = db.Column(db.String(36), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey("tenants.id"))
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
    status = db.Column(db.String(50), default="active")
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    def to_dict(self):
        return _model_to_dict(self)


class FormulaConfig(db.Model):
    """算法公式配置模型 - 支持自定义公式"""

    __tablename__ = "formula_configs"

    __table_args__ = (db.Index("idx_formula_configs_user_id", "user_id"),)

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"))

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
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    # 关联
    user = db.relationship("User", back_populates="formula_configs")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "formula_type": self.formula_type,
            "expression": self.expression,
            "parameters": self.parameters,
            "description": self.description,
            "is_public": self.is_public,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class AlgorithmModel(db.Model):
    """算法模型库 - 支持添加和管理多种衰减模型"""

    __tablename__ = "algorithm_models"

    __table_args__ = (
        db.Index("idx_algorithm_models_tenant_id", "tenant_id"),
        db.Index("idx_algorithm_models_created_by", "created_by"),
    )

    id = db.Column(db.String(36), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey("tenants.id"))

    # 模型基本信息
    name = db.Column(db.String(200), nullable=False)  # 模型名称
    name_en = db.Column(db.String(200))  # 英文名称
    model_type = db.Column(
        db.String(50)
    )  # 模型类型: double_exponential/linear_log/arrhenius/rainflow/semi_empirical/custom

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
    created_by = db.Column(db.String(36), db.ForeignKey("users.id"))

    # 时间
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    # 关联
    tenant = db.relationship("Tenant", back_populates="algorithm_models")
    created_by_user = db.relationship("User", back_populates="algorithm_models")
    simulation_results = db.relationship("SimulationResult", back_populates="algorithm_model")

    def to_dict(self):
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "name_en": self.name_en,
            "model_type": self.model_type,
            "applicable_scenarios": self.applicable_scenarios,
            "mathematical_form": self.mathematical_form,
            "formula_expression": self.formula_expression,
            "parameters": self.parameters,
            "accuracy_level": self.accuracy_level,
            "accuracy_desc": self.accuracy_desc,
            "category": self.category,
            "is_builtin": self.is_builtin,
            "is_active": self.is_active,
            "sort_order": self.sort_order,
            "description": self.description,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class BoqSection(db.Model):
    """BOQ 分类——固定7级模板"""

    __tablename__ = "boq_sections"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(100))
    name_zh = db.Column(db.String(100))
    default_unit = db.Column(db.String(20))
    sort_order = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "name_zh": self.name_zh,
            "default_unit": self.default_unit,
            "sort_order": self.sort_order,
        }


class BoqItem(db.Model):
    """BOQ 条目"""

    __tablename__ = "boq_items"
    __table_args__ = (db.Index("idx_boq_items_project_id", "project_id"),)
    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"), nullable=False)
    section_code = db.Column(db.String(10))
    seq = db.Column(db.Integer)
    name = db.Column(db.String(300))
    spec = db.Column(db.String(500))
    unit = db.Column(db.String(20))
    quantity = db.Column(db.Float)
    unit_price = db.Column(db.Float)
    total_price = db.Column(db.Float)
    note = db.Column(db.String(500))
    is_alternative = db.Column(db.Boolean, default=False)
    version = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "section_code": self.section_code,
            "seq": self.seq,
            "name": self.name,
            "spec": self.spec,
            "unit": self.unit,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_price": self.total_price,
            "note": self.note,
            "is_alternative": self.is_alternative,
            "version": self.version,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


# 添加租户关联
Tenant.correction_templates = db.relationship("CorrectionTemplate", back_populates="tenant")
Tenant.algorithm_models = db.relationship("AlgorithmModel", back_populates="tenant")

# 添加用户关联
User.correction_templates = db.relationship("CorrectionTemplate", back_populates="created_by_user")
User.algorithm_models = db.relationship("AlgorithmModel", back_populates="created_by_user")


class BatteryManufacturer(db.Model):
    """电池厂家数据模型（含校准后的退化参数）"""

    __tablename__ = "battery_manufacturers"

    id = db.Column(db.String(50), primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    name_en = db.Column(db.String(255))
    country = db.Column(db.String(100))
    chemistry_type = db.Column(db.String(50))
    calibrated_params = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    def __repr__(self):
        return f"<BatteryManufacturer {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_en": self.name_en,
            "country": self.country,
            "chemistry_type": self.chemistry_type,
            "calibrated_params": self.calibrated_params,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class SystemArchitecture(db.Model):
    """系统架构评估模型 (EPC: system-architecture)"""

    __tablename__ = "system_architectures"

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"), nullable=False)
    tenant_id = db.Column(db.String(36), nullable=True, index=True)
    data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    __table_args__ = (db.Index("idx_sa_project_id", "project_id"),)

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "tenant_id": self.tenant_id,
            "data": self.data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class GridComplianceAnalysis(db.Model):
    """电网合规分析模型 (EPC: grid-compliance)"""

    __tablename__ = "grid_compliance_analyses"

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"), nullable=False)
    tenant_id = db.Column(db.String(36), nullable=True, index=True)
    data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    __table_args__ = (db.Index("idx_gca_project_id", "project_id"),)

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "tenant_id": self.tenant_id,
            "data": self.data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class SafetyFireDesign(db.Model):
    """安全消防设计模型 (EPC: safety-fire)"""

    __tablename__ = "safety_fire_designs"

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"), nullable=False)
    tenant_id = db.Column(db.String(36), nullable=True, index=True)
    data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    __table_args__ = (db.Index("idx_sfd_project_id", "project_id"),)

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "tenant_id": self.tenant_id,
            "data": self.data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class IPPFinancialModel(db.Model):
    """IPP 财务模型 (EPC: ipp-financial)"""

    __tablename__ = "ipp_financial_models"

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"), nullable=False)
    tenant_id = db.Column(db.String(36), nullable=True, index=True)
    data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    __table_args__ = (db.Index("idx_ifm_project_id", "project_id"),)

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "tenant_id": self.tenant_id,
            "data": self.data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class ComplianceMatrix(db.Model):
    """合规矩阵模型 (EPC: compliance-matrix)"""

    __tablename__ = "compliance_matrices"

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"), nullable=False)
    tenant_id = db.Column(db.String(36), nullable=True, index=True)
    data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    __table_args__ = (db.Index("idx_cm_project_id", "project_id"),)

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "tenant_id": self.tenant_id,
            "data": self.data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class ThermalManagement(db.Model):
    """热管理设计模型 (EPC: thermal-management)"""

    __tablename__ = "thermal_managements"

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"), nullable=False)
    tenant_id = db.Column(db.String(36), nullable=True, index=True)
    data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    __table_args__ = (db.Index("idx_tm_project_id", "project_id"),)

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "tenant_id": self.tenant_id,
            "data": self.data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class ScadaEmsDesign(db.Model):
    """SCADA/EMS 设计模型 (EPC: scada-ems)"""

    __tablename__ = "scada_ems_designs"

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"), nullable=False)
    tenant_id = db.Column(db.String(36), nullable=True, index=True)
    data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    __table_args__ = (db.Index("idx_sed_project_id", "project_id"),)

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "tenant_id": self.tenant_id,
            "data": self.data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class HVInterconnection(db.Model):
    """高压接入设计模型 (EPC: hv-interconnection)"""

    __tablename__ = "hv_interconnections"

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"), nullable=False)
    tenant_id = db.Column(db.String(36), nullable=True, index=True)
    data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    __table_args__ = (db.Index("idx_hvi_project_id", "project_id"),)

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "tenant_id": self.tenant_id,
            "data": self.data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class BidDocument(db.Model):
    """投标文档模型 (EPC: bid-document)"""

    __tablename__ = "bid_documents"

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"), nullable=False)
    tenant_id = db.Column(db.String(36), nullable=True, index=True)
    data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    __table_args__ = (db.Index("idx_bd_project_id", "project_id"),)

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "tenant_id": self.tenant_id,
            "data": self.data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class PinnModelWeights(db.Model):
    """PINN 神经网络权重存储模型"""

    __tablename__ = "pinn_model_weights"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(255), nullable=False)
    weights = db.Column(db.LargeBinary, nullable=False)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    def __repr__(self):
        return f"<PinnModelWeights {self.model_name}>"


# ==================== to_dict 显式声明（替代运行时动态注入） ====================
Tenant.to_dict = _model_to_dict
User.to_dict = _model_to_dict
Survey.to_dict = _model_to_dict
Project.to_dict = _model_to_dict
ProjectVersion.to_dict = _model_to_dict
Simulation.to_dict = _model_to_dict
SimulationResult.to_dict = _model_to_dict
CorrectionTemplate.to_dict = _model_to_dict
BatteryPCSConfig.to_dict = _model_to_dict
SohRteData.to_dict = _model_to_dict
FinancialData.to_dict = _model_to_dict
ProductConfig.to_dict = _model_to_dict
FormulaConfig.to_dict = _model_to_dict
AlgorithmModel.to_dict = _model_to_dict
BoqSection.to_dict = _model_to_dict
BoqItem.to_dict = _model_to_dict
BatteryManufacturer.to_dict = _model_to_dict
PinnModelWeights.to_dict = _model_to_dict
SystemArchitecture.to_dict = _model_to_dict
GridComplianceAnalysis.to_dict = _model_to_dict
SafetyFireDesign.to_dict = _model_to_dict
IPPFinancialModel.to_dict = _model_to_dict
ComplianceMatrix.to_dict = _model_to_dict
ThermalManagement.to_dict = _model_to_dict
ScadaEmsDesign.to_dict = _model_to_dict
HVInterconnection.to_dict = _model_to_dict
BidDocument.to_dict = _model_to_dict


def init_db(app):
    """初始化数据库，同时种子默认租户"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        # 兼容旧库：为已存在的 EPC 表补充 tenant_id 列
        inspector = inspect(db.engine)
        with db.engine.begin() as conn:
            for table in (
                "system_architectures", "grid_compliance_analyses",
                "safety_fire_designs", "ipp_financial_models",
                "compliance_matrices", "thermal_managements",
                "scada_ems_designs", "hv_interconnections", "bid_documents",
            ):
                if table in inspector.get_table_names():
                    cols = {c["name"] for c in inspector.get_columns(table)}
                    if "tenant_id" not in cols:
                        conn.execute(text(f"ALTER TABLE {table} ADD COLUMN tenant_id VARCHAR(36)"))
        # 种子默认租户
        import uuid as _uuid
        default_tenant_id = "00000000-0000-0000-0000-000000000001"
        existing = db.session.get(Tenant, default_tenant_id)
        if not existing:
            db.session.add(Tenant(
                id=default_tenant_id,
                name="Default Tenant",
                code="default",
                status="active",
            ))
            db.session.commit()
    return db


def get_db_path():
    """获取数据库文件路径"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "soh_sim.db")
