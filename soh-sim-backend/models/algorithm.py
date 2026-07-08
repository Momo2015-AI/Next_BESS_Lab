from . import db, _utcnow


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
            "created_at": (
                self.created_at.isoformat() if self.created_at else None
            ),
            "updated_at": (
                self.updated_at.isoformat() if self.updated_at else None
            ),
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
    applicable_scenarios = db.Column(
        db.Text
    )  # JSON数组，如 ["LFP日历衰减", "循环衰减"]

    # 数学形式/公式表达式
    mathematical_form = db.Column(db.Text)  # 数学形式描述
    formula_expression = db.Column(db.Text)  # 可执行的公式表达式

    # 参数定义（JSON格式）
    parameters = db.Column(
        db.Text
    )  # 参数定义 {"param_name": {"label": "", "default": 0.0, "min": 0, "max": 100}}

    # 精度等级
    accuracy_level = db.Column(db.String(20))  # low/medium/high
    accuracy_desc = db.Column(
        db.String(200)
    )  # 精度描述，如 "R²>0.999"

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
    created_by_user = db.relationship(
        "User", back_populates="algorithm_models"
    )
    simulation_results = db.relationship(
        "SimulationResult", back_populates="algorithm_model"
    )

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
            "created_at": (
                self.created_at.isoformat() if self.created_at else None
            ),
            "updated_at": (
                self.updated_at.isoformat() if self.updated_at else None
            ),
        }
