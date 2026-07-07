from . import db, _utcnow
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


