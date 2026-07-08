from . import _utcnow, db


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
            "created_at": (self.created_at.isoformat() if self.created_at else None),
            "updated_at": (self.updated_at.isoformat() if self.updated_at else None),
        }


# 添加租户关联
Tenant.correction_templates = db.relationship("CorrectionTemplate", back_populates="tenant")
Tenant.algorithm_models = db.relationship("AlgorithmModel", back_populates="tenant")

# 添加用户关联
User.correction_templates = db.relationship("CorrectionTemplate", back_populates="created_by_user")
User.algorithm_models = db.relationship("AlgorithmModel", back_populates="created_by_user")
