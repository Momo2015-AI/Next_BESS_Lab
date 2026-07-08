from . import _utcnow, db


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
            "created_at": (self.created_at.isoformat() if self.created_at else None),
            "updated_at": (self.updated_at.isoformat() if self.updated_at else None),
            "last_login": (self.last_login.isoformat() if self.last_login else None),
        }
