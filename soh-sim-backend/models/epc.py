from . import db, _utcnow
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


