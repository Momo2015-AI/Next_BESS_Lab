from . import db, _utcnow


class BatteryPCSConfig(db.Model):
    """电池与PCS配置模型"""

    __tablename__ = "battery_pcs_configs"

    __table_args__ = (
        db.Index("idx_battery_pcs_configs_project_id", "project_id"),
    )

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
            "created_at": (
                self.created_at.isoformat() if self.created_at else None
            ),
            "updated_at": (
                self.updated_at.isoformat() if self.updated_at else None
            ),
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
    simulation_id = db.Column(
        db.String(36), db.ForeignKey("simulations.id")
    )

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
            "created_at": (
                self.created_at.isoformat() if self.created_at else None
            ),
            "updated_at": (
                self.updated_at.isoformat() if self.updated_at else None
            ),
        }


class FinancialData(db.Model):
    """财务数据模型"""

    __tablename__ = "financial_data"

    __table_args__ = (
        db.Index("idx_financial_data_project_id", "project_id"),
    )

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
            "created_at": (
                self.created_at.isoformat() if self.created_at else None
            ),
            "updated_at": (
                self.updated_at.isoformat() if self.updated_at else None
            ),
        }
