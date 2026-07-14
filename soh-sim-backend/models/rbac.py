"""角色权限模型

支持管理员对角色和特定用户进行权限覆盖配置，并可设置失效时间。
过期后角色权限自动恢复到默认。
"""

from datetime import datetime, timezone

from . import _utcnow, db

# ==================== 角色与权限常量 ====================

# 系统定义的 6 种角色
ROLES = {
    "developer": {
        "label": "项目开发商",
        "label_en": "Developer",
        "description": "项目立项、经济评估、投资决策",
    },
    "solution_engineer": {
        "label": "方案工程师",
        "label_en": "Solution Engineer",
        "description": "系统设计、产品选型、仿真分析",
    },
    "epc_contractor": {
        "label": "EPC承包商",
        "label_en": "EPC Contractor",
        "description": "工程设计、安全合规、施工交付",
    },
    "financial_analyst": {
        "label": "财务分析师",
        "label_en": "Financial Analyst",
        "description": "财务建模、CAPEX/OPEX、IPP报价",
    },
    "project_manager": {
        "label": "项目经理",
        "label_en": "Project Manager",
        "description": "全流程管理、报告归档、项目协调",
    },
    "admin": {
        "label": "系统管理员",
        "label_en": "Administrator",
        "description": "用户管理、系统配置、跨租户管理",
    },
}

# 默认角色（注册时分配）
DEFAULT_ROLE = "developer"

# 系统定义的所有功能模块 key
PERMISSION_KEYS = [
    # Phase 阶段
    "phase1",  # 项目立项
    "phase2",  # 系统设计
    "phase3",  # 性能分析
    "phase4",  # 经济评估
    "phase5",  # 成果输出
    # 核心工具
    "tool_formula",  # 算法与公式
    "tool_params",  # 参数面板
    "tool_conditions",  # 运行工况
    "tool_auxpower",  # 辅耗计算
    "tool_financial",  # 财务看板
    "tool_engineering",  # 工程计算
    "tool_datainject",  # 数据注入
    # 高级工具
    "tool_config",  # 方案设计
    "tool_survey_view",  # 调研输入
    "tool_simulation_view",  # 仿真查看
    "tool_report",  # 报告输出
    "tool_projects",  # 历史项目
    "tool_templates",  # 校正因子模板
    "tool_rules",  # 配置规则
    # EPC
    "epc",  # EPC 模块
    "epc_ipp",  # IPP 财务模型
    # 引擎
    "orchestrator",  # 一键方案引擎
    # 管理
    "admin_panel",  # 管理面板（仅 admin）
]

# ==================== 默认角色-权限映射 ====================
# "full" = 可编辑, "readonly" = 只读, "hidden" = 不可见

DEFAULT_ROLE_PERMISSIONS = {
    "developer": {
        "phase1": "full",
        "phase2": "readonly",
        "phase3": "readonly",
        "phase4": "full",
        "phase5": "full",
        "tool_formula": "hidden",
        "tool_params": "hidden",
        "tool_conditions": "hidden",
        "tool_auxpower": "hidden",
        "tool_financial": "full",
        "tool_engineering": "hidden",
        "tool_datainject": "hidden",
        "tool_config": "hidden",
        "tool_survey_view": "full",
        "tool_simulation_view": "hidden",
        "tool_report": "full",
        "tool_projects": "full",
        "tool_templates": "hidden",
        "tool_rules": "hidden",
        "epc": "readonly",
        "epc_ipp": "full",
        "orchestrator": "full",
        "admin_panel": "hidden",
    },
    "solution_engineer": {
        "phase1": "full",
        "phase2": "full",
        "phase3": "full",
        "phase4": "readonly",
        "phase5": "full",
        "tool_formula": "full",
        "tool_params": "full",
        "tool_conditions": "full",
        "tool_auxpower": "full",
        "tool_financial": "hidden",
        "tool_engineering": "full",
        "tool_datainject": "full",
        "tool_config": "full",
        "tool_survey_view": "full",
        "tool_simulation_view": "full",
        "tool_report": "full",
        "tool_projects": "readonly",
        "tool_templates": "full",
        "tool_rules": "readonly",
        "epc": "readonly",
        "epc_ipp": "hidden",
        "orchestrator": "full",
        "admin_panel": "hidden",
    },
    "epc_contractor": {
        "phase1": "readonly",
        "phase2": "readonly",
        "phase3": "readonly",
        "phase4": "readonly",
        "phase5": "full",
        "tool_formula": "hidden",
        "tool_params": "hidden",
        "tool_conditions": "hidden",
        "tool_auxpower": "full",
        "tool_financial": "hidden",
        "tool_engineering": "full",
        "tool_datainject": "hidden",
        "tool_config": "hidden",
        "tool_survey_view": "hidden",
        "tool_simulation_view": "hidden",
        "tool_report": "full",
        "tool_projects": "readonly",
        "tool_templates": "hidden",
        "tool_rules": "hidden",
        "epc": "full",
        "epc_ipp": "hidden",
        "orchestrator": "readonly",
        "admin_panel": "hidden",
    },
    "financial_analyst": {
        "phase1": "readonly",
        "phase2": "readonly",
        "phase3": "readonly",
        "phase4": "full",
        "phase5": "full",
        "tool_formula": "hidden",
        "tool_params": "hidden",
        "tool_conditions": "hidden",
        "tool_auxpower": "hidden",
        "tool_financial": "full",
        "tool_engineering": "hidden",
        "tool_datainject": "hidden",
        "tool_config": "hidden",
        "tool_survey_view": "hidden",
        "tool_simulation_view": "hidden",
        "tool_report": "full",
        "tool_projects": "readonly",
        "tool_templates": "hidden",
        "tool_rules": "hidden",
        "epc": "readonly",
        "epc_ipp": "full",
        "orchestrator": "full",
        "admin_panel": "hidden",
    },
    "project_manager": {
        "phase1": "full",
        "phase2": "full",
        "phase3": "full",
        "phase4": "full",
        "phase5": "full",
        "tool_formula": "full",
        "tool_params": "full",
        "tool_conditions": "full",
        "tool_auxpower": "full",
        "tool_financial": "full",
        "tool_engineering": "full",
        "tool_datainject": "full",
        "tool_config": "full",
        "tool_survey_view": "full",
        "tool_simulation_view": "full",
        "tool_report": "full",
        "tool_projects": "full",
        "tool_templates": "full",
        "tool_rules": "readonly",
        "epc": "full",
        "epc_ipp": "full",
        "orchestrator": "full",
        "admin_panel": "hidden",
    },
    "admin": {
        "phase1": "full",
        "phase2": "full",
        "phase3": "full",
        "phase4": "full",
        "phase5": "full",
        "tool_formula": "full",
        "tool_params": "full",
        "tool_conditions": "full",
        "tool_auxpower": "full",
        "tool_financial": "full",
        "tool_engineering": "full",
        "tool_datainject": "full",
        "tool_config": "full",
        "tool_survey_view": "full",
        "tool_simulation_view": "full",
        "tool_report": "full",
        "tool_projects": "full",
        "tool_templates": "full",
        "tool_rules": "full",
        "epc": "full",
        "epc_ipp": "full",
        "orchestrator": "full",
        "admin_panel": "full",
    },
}


class RolePermission(db.Model):
    """角色权限覆盖配置

    管理员可对某个角色整体覆盖其默认权限。
    设置 expires_at 后，过期自动恢复默认。
    """

    __tablename__ = "role_permissions"
    __table_args__ = (db.Index("idx_role_permissions_role", "role"),)

    id = db.Column(db.String(36), primary_key=True)
    role = db.Column(db.String(30), nullable=False, unique=True)
    # JSON 字符串: {"phase1": "full", "phase2": "readonly", ...}
    permissions = db.Column(db.Text, default="{}")
    # 失效时间，过期后该覆盖失效，恢复默认权限
    expires_at = db.Column(db.DateTime, nullable=True)
    # 记录创建/更新信息
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)
    created_by = db.Column(db.String(36), nullable=True)
    note = db.Column(db.String(500), default="")


class UserPermissionOverride(db.Model):
    """特定用户权限覆盖

    管理员可对特定用户单独配置权限，优先级高于角色权限。
    设置 expires_at 后，过期自动恢复到角色默认权限。
    """

    __tablename__ = "user_permission_overrides"
    __table_args__ = (db.Index("idx_user_perm_user_id", "user_id"),)

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False, unique=True)
    # 临时角色（可选）：如果设置，用户在过期前使用此角色
    temporary_role = db.Column(db.String(30), nullable=True)
    # 权限覆盖（可选）：精确到模块级别的权限覆盖
    # JSON 字符串: {"phase1": "full", "tool_formula": "hidden", ...}
    permissions = db.Column(db.Text, default="{}")
    # 失效时间，过期后恢复用户原始角色权限
    expires_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)
    created_by = db.Column(db.String(36), nullable=True)
    note = db.Column(db.String(500), default="")

    # 关联
    user = db.relationship("User", backref=db.backref("permission_override", uselist=False))


def get_effective_permissions(user):
    """计算用户的有效权限。

    优先级: 用户级覆盖 > 角色级覆盖 > 默认角色权限

    Args:
        user: User 模型实例

    Returns:
        dict: { "phase1": "full", "phase2": "readonly", ... }
    """
    import json

    now = datetime.now(timezone.utc)

    # 1. 获取角色默认权限
    role = user.role or DEFAULT_ROLE
    perms = dict(DEFAULT_ROLE_PERMISSIONS.get(role, DEFAULT_ROLE_PERMISSIONS[DEFAULT_ROLE]))

    # 2. 检查角色级覆盖
    role_override = RolePermission.query.filter_by(role=role).first()
    if role_override:
        # 检查是否过期
        if role_override.expires_at is None or role_override.expires_at > now:
            try:
                override_perms = json.loads(role_override.permissions or "{}")
                perms.update(override_perms)
            except (json.JSONDecodeError, ValueError):
                pass

    # 3. 检查用户级覆盖
    user_override = UserPermissionOverride.query.filter_by(user_id=user.id).first()
    if user_override:
        # 检查是否过期
        if user_override.expires_at is None or user_override.expires_at > now:
            # 如果有临时角色，用临时角色的默认权限作为基础
            if user_override.temporary_role:
                temp_role = user_override.temporary_role
                perms = dict(DEFAULT_ROLE_PERMISSIONS.get(temp_role, DEFAULT_ROLE_PERMISSIONS[DEFAULT_ROLE]))
                # 也应用该角色的角色级覆盖
                temp_role_override = RolePermission.query.filter_by(role=temp_role).first()
                if temp_role_override and (
                    temp_role_override.expires_at is None or temp_role_override.expires_at > now
                ):
                    try:
                        temp_override_perms = json.loads(temp_role_override.permissions or "{}")
                        perms.update(temp_override_perms)
                    except (json.JSONDecodeError, ValueError):
                        pass
            # 再叠加用户级精确权限覆盖
            try:
                user_perms = json.loads(user_override.permissions or "{}")
                perms.update(user_perms)
            except (json.JSONDecodeError, ValueError):
                pass

    return perms


def get_user_effective_role(user):
    """获取用户的有效角色（考虑临时角色覆盖）"""
    now = datetime.now(timezone.utc)
    user_override = UserPermissionOverride.query.filter_by(user_id=user.id).first()
    if user_override and user_override.temporary_role:
        if user_override.expires_at is None or user_override.expires_at > now:
            return user_override.temporary_role
    return user.role or DEFAULT_ROLE
