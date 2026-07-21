"""
管理员配置模型

包含方案模板（DesignTemplate）等管理员可配置的业务对象。
"""

import uuid

from models import _utcnow, db


def _new_uuid():
    return str(uuid.uuid4())


class DesignTemplate(db.Model):
    """方案设计模板 — 管理员预设的产品组合方案"""

    __tablename__ = "design_templates"

    id = db.Column(db.String(36), primary_key=True, default=_new_uuid)
    tenant_id = db.Column(db.String(36), db.ForeignKey("tenants.id"), nullable=True)
    name = db.Column(db.String(100), nullable=False, comment="模板名称")
    name_en = db.Column(db.String(100), nullable=True, comment="英文名称")
    strategy = db.Column(
        db.String(50), nullable=False, default="balanced", comment="策略: economic/balanced/flexible/manufacturer"
    )
    description = db.Column(db.Text, nullable=True, comment="模板描述")

    # 产品引用（存 model 字符串，非 FK，便于跨库迁移）
    cell_model = db.Column(db.String(200), nullable=True, comment="推荐电芯型号")
    container_model = db.Column(db.String(200), nullable=True, comment="推荐集装箱型号")
    pcs_model = db.Column(db.String(200), nullable=True, comment="推荐 PCS 型号")

    # 默认设计参数
    default_duration = db.Column(db.Float, nullable=True, comment="默认时长(h)")
    default_dod = db.Column(db.Float, nullable=True, comment="默认 DOD(%)")
    default_crate = db.Column(db.Float, nullable=True, comment="默认充放电倍率")

    is_default = db.Column(db.Boolean, default=False, comment="是否默认模板")
    is_builtin = db.Column(db.Boolean, default=False, comment="是否内置模板")
    sort_order = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default="active")
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    __table_args__ = (db.Index("idx_design_templates_tenant_id", "tenant_id"),)

    def to_dict(self):
        return {
            "id": self.id,
            "tenantId": self.tenant_id,
            "name": self.name,
            "nameEn": self.name_en,
            "strategy": self.strategy,
            "description": self.description,
            "cellModel": self.cell_model,
            "containerModel": self.container_model,
            "pcsModel": self.pcs_model,
            "defaultDuration": self.default_duration,
            "defaultDod": self.default_dod,
            "defaultCrate": self.default_crate,
            "isDefault": self.is_default,
            "isBuiltin": self.is_builtin,
            "sortOrder": self.sort_order,
            "status": self.status,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
        }
