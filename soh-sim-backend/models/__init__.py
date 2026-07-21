"""
数据库配置与模型定义
使用SQLite作为数据库，支持跨平台运行
完整支持所有功能模块的数据存储

此文件为 models/ 包的入口，保持与原有 database.py 的向后兼容。
"""

import json
import os
from datetime import datetime, timezone

# 统一使用 timezone-aware UTC 时间，替代已弃用的 datetime.utcnow
_utcnow = lambda: datetime.now(timezone.utc)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index, event, inspect, text
from sqlalchemy.orm import Session as _OrmSession

db = SQLAlchemy()

# 租户隔离模型：flush 前自动从父项目继承 tenant_id
_TENANT_PROJECT_MODELS = {
    "SystemArchitecture",
    "GridComplianceAnalysis",
    "SafetyFireDesign",
    "IPPFinancialModel",
    "ComplianceMatrix",
    "ThermalManagement",
    "ScadaEmsDesign",
    "HVInterconnection",
    "BidDocument",
}

# 这些列存储 JSON 字符串，序列化时需要解析回对象
_JSON_COLUMNS = {
    "Survey": {"attachments"},
    "Project": {"config"},
    "ProjectVersion": {"config_data"},
    "Simulation": {"input_params", "results", "manual_corrections"},
    "SimulationResult": {"params", "results", "summary"},
    "CorrectionTemplate": {"annual_corrections"},
    "BatteryPCSConfig": {"connection_diagram", "single_line_diagram"},
    "SohRteData": {
        "soh_values",
        "rte_values",
        "dod_values",
        "aug_qty_values",
    },
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


from .algorithm import AlgorithmModel, FormulaConfig

# 导入所有模型类（必须在 db 和辅助函数定义之后）
from .auth import Tenant, User
from .boq import BoqItem, BoqSection
from .config_data import BatteryPCSConfig, FinancialData, SohRteData
from .epc import (
    BidDocument,
    ComplianceMatrix,
    GridComplianceAnalysis,
    HVInterconnection,
    IPPFinancialModel,
    SafetyFireDesign,
    ScadaEmsDesign,
    SystemArchitecture,
    ThermalManagement,
)
from .pinn import PinnModelWeights
from .product import (
    BatteryConfigRule,
    BatteryManufacturer,
    CellProduct,
    ClusterProduct,
    ContainerProduct,
    PackProduct,
    PcsProduct,
    ProductConfig,
    RackProduct,
)
from .project import Project, ProjectVersion
from .rbac import (
    DEFAULT_ROLE,
    DEFAULT_ROLE_PERMISSIONS,
    PERMISSION_KEYS,
    ROLES,
    RolePermission,
    UserPermissionOverride,
    get_effective_permissions,
    get_user_effective_role,
)
from .simulation import CorrectionTemplate, Simulation, SimulationResult
from .survey import Survey

# 所有公共导出（确保 from database import * 兼容）
__all__ = [
    "db",
    "init_db",
    "_model_to_dict",
    "_serialize_value",
    "Tenant",
    "User",
    "Survey",
    "Project",
    "ProjectVersion",
    "Simulation",
    "SimulationResult",
    "CorrectionTemplate",
    "BatteryPCSConfig",
    "SohRteData",
    "FinancialData",
    "ProductConfig",
    "CellProduct",
    "PackProduct",
    "RackProduct",
    "ClusterProduct",
    "ContainerProduct",
    "PcsProduct",
    "BatteryConfigRule",
    "BatteryManufacturer",
    "FormulaConfig",
    "AlgorithmModel",
    "BoqSection",
    "BoqItem",
    "SystemArchitecture",
    "GridComplianceAnalysis",
    "SafetyFireDesign",
    "IPPFinancialModel",
    "ComplianceMatrix",
    "ThermalManagement",
    "ScadaEmsDesign",
    "HVInterconnection",
    "BidDocument",
    "PinnModelWeights",
    "RolePermission",
    "UserPermissionOverride",
    "ROLES",
    "PERMISSION_KEYS",
    "DEFAULT_ROLE",
    "DEFAULT_ROLE_PERMISSIONS",
    "get_effective_permissions",
    "get_user_effective_role",
]


# ==================== to_dict 显式声明 ====================
# 仅对未在各自模型文件中定义 to_dict() 的模型统一赋值
RolePermission.to_dict = _model_to_dict
UserPermissionOverride.to_dict = _model_to_dict
PinnModelWeights.to_dict = _model_to_dict


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


def init_db(app):
    """初始化数据库，同时种子默认租户"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        # 兼容旧库：为已存在的 EPC 表补充 tenant_id 列
        inspector = inspect(db.engine)
        with db.engine.begin() as conn:
            for table in (
                "system_architectures",
                "grid_compliance_analyses",
                "safety_fire_designs",
                "ipp_financial_models",
                "compliance_matrices",
                "thermal_managements",
                "scada_ems_designs",
                "hv_interconnections",
                "bid_documents",
            ):
                if table in inspector.get_table_names():
                    cols = {c["name"] for c in inspector.get_columns(table)}
                    if "tenant_id" not in cols:
                        conn.execute(text(f"ALTER TABLE {table} " "ADD COLUMN tenant_id VARCHAR(36)"))
        # 种子默认租户
        import uuid as _uuid

        default_tenant_id = "00000000-0000-0000-0000-000000000001"
        existing = db.session.get(Tenant, default_tenant_id)
        if not existing:
            db.session.add(
                Tenant(
                    id=default_tenant_id,
                    name="Default Tenant",
                    code="default",
                    status="active",
                )
            )
            db.session.commit()
    return db
