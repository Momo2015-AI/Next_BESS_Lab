from . import _utcnow, db


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
            "started_at": (self.started_at.isoformat() if self.started_at else None),
            "completed_at": (self.completed_at.isoformat() if self.completed_at else None),
            "created_at": (self.created_at.isoformat() if self.created_at else None),
            "updated_at": (self.updated_at.isoformat() if self.updated_at else None),
        }


class SimulationResult(db.Model):
    """仿真结果模型 - 完整存储每次仿真结果，带日期戳便于对比"""

    __tablename__ = "simulation_results"

    __table_args__ = (
        db.Index("idx_simulation_results_version_id", "version_id"),
        db.Index(
            "idx_simulation_results_algorithm_model_id",
            "algorithm_model_id",
        ),
        db.Index(
            "idx_simulation_results_correction_template_id",
            "correction_template_id",
        ),
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
            "executed_at": (self.executed_at.isoformat() if self.executed_at else None),
            "execution_time_ms": self.execution_time_ms,
            "created_by": self.created_by,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
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
            "created_at": (self.created_at.isoformat() if self.created_at else None),
            "updated_at": (self.updated_at.isoformat() if self.updated_at else None),
        }
