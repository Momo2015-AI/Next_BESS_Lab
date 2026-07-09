from . import _model_to_dict, _utcnow, db


class ProductConfig(db.Model):
    """产品与方案配置模型"""

    __tablename__ = "product_configs"

    __table_args__ = (db.Index("idx_product_configs_project_id", "project_id"),)

    id = db.Column(db.String(36), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"))

    # 配置名称
    name = db.Column(db.String(200))

    # 电池产品配置
    cell_model = db.Column(db.String(100))
    cell_capacity = db.Column(db.Float)  # Ah
    cell_voltage = db.Column(db.Float)  # V
    cell_supplier = db.Column(db.String(100))

    # 集装箱产品配置
    container_model = db.Column(db.String(100))
    container_supplier = db.Column(db.String(100))

    # PCS产品配置
    pcs_model = db.Column(db.String(100))
    pcs_supplier = db.Column(db.String(100))

    # 认证要求
    certifications = db.Column(db.Text)  # JSON数组 ['UL9540', 'IEC62619', ...]

    # EPC配置
    epc_company = db.Column(db.String(100))
    epc_contract_type = db.Column(db.String(50))  # turnkey/performance

    # 时间
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    # 关联
    project = db.relationship("Project", back_populates="product_configs")

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "cell_model": self.cell_model,
            "cell_capacity": self.cell_capacity,
            "cell_voltage": self.cell_voltage,
            "cell_supplier": self.cell_supplier,
            "container_model": self.container_model,
            "container_supplier": self.container_supplier,
            "pcs_model": self.pcs_model,
            "pcs_supplier": self.pcs_supplier,
            "certifications": self.certifications,
            "epc_company": self.epc_company,
            "epc_contract_type": self.epc_contract_type,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
            "updated_at": (self.updated_at.isoformat() if self.updated_at else None),
        }


class CellProduct(db.Model):
    """电芯产品库"""

    __tablename__ = "cell_products"

    __table_args__ = (db.Index("idx_cell_products_tenant_id", "tenant_id"),)

    id = db.Column(db.String(100), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey("tenants.id"))  # 企业隔离
    is_builtin = db.Column(db.Boolean, default=False)  # 是否系统内置（对所有企业可见）
    mfr = db.Column(db.String(200))
    model = db.Column(db.String(200))
    chemistry = db.Column(db.String(50))
    capacity_ah = db.Column(db.Float)
    voltage_nominal = db.Column(db.Float)
    voltage_max = db.Column(db.Float)
    voltage_min = db.Column(db.Float)
    voltage_range = db.Column(db.String(100))
    rated_energy_mwh = db.Column(db.Float)  # MWh
    cycle_life = db.Column(db.Integer)
    calendar_life = db.Column(db.Integer)  # 日历寿命 年
    energy_density = db.Column(db.Float)  # Wh/kg
    dimensions = db.Column(db.String(200))
    weight = db.Column(db.Float)  # kg
    soh_curve = db.Column(db.String(100))
    certifications = db.Column(db.Text)  # JSON
    unit_price = db.Column(db.Float)  # 元/Wh
    remarks = db.Column(db.Text)
    status = db.Column(db.String(50), default="mass-production")
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    def to_dict(self):
        return _model_to_dict(self)


class PackProduct(db.Model):
    """电池包产品库"""

    __tablename__ = "pack_products"

    __table_args__ = (db.Index("idx_pack_products_tenant_id", "tenant_id"),)

    id = db.Column(db.String(100), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey("tenants.id"))
    is_builtin = db.Column(db.Boolean, default=False)
    mfr = db.Column(db.String(200))
    model = db.Column(db.String(200))
    chemistry = db.Column(db.String(50))
    cell_model = db.Column(db.String(200))
    cells_per_pack = db.Column(db.Integer)
    series_count = db.Column(db.Integer)
    parallel_count = db.Column(db.Integer)
    nominal_voltage = db.Column(db.Float)
    nominal_capacity_ah = db.Column(db.Float)
    rated_energy_mwh = db.Column(db.Float)  # MWh, was nominal_energy_kwh
    max_charge_current = db.Column(db.Float)
    max_discharge_current = db.Column(db.Float)
    dimensions = db.Column(db.String(200))
    weight = db.Column(db.Float)  # kg
    bms_type = db.Column(db.String(100))
    cycle_life = db.Column(db.Integer)
    status = db.Column(db.String(50), default="mass-production")

    def to_dict(self):
        return _model_to_dict(self)


class RackProduct(db.Model):
    """电池架产品库"""

    __tablename__ = "rack_products"

    __table_args__ = (db.Index("idx_rack_products_tenant_id", "tenant_id"),)

    id = db.Column(db.String(100), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey("tenants.id"))
    is_builtin = db.Column(db.Boolean, default=False)
    mfr = db.Column(db.String(200))
    model = db.Column(db.String(200))
    pack_model = db.Column(db.String(200))
    packs_per_rack = db.Column(db.Integer)
    series_count = db.Column(db.Integer)
    parallel_count = db.Column(db.Integer)
    nominal_voltage = db.Column(db.Float)
    nominal_capacity_ah = db.Column(db.Float)
    rated_energy_mwh = db.Column(db.Float)  # MWh, was nominal_energy_kwh
    dimensions = db.Column(db.String(200))
    weight = db.Column(db.Float)  # kg
    cooling = db.Column(db.String(100))
    status = db.Column(db.String(50), default="mass-production")

    def to_dict(self):
        return _model_to_dict(self)


class ClusterProduct(db.Model):
    """电池簇产品库"""

    __tablename__ = "cluster_products"

    __table_args__ = (db.Index("idx_cluster_products_tenant_id", "tenant_id"),)

    id = db.Column(db.String(100), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey("tenants.id"))
    is_builtin = db.Column(db.Boolean, default=False)
    mfr = db.Column(db.String(200))
    model = db.Column(db.String(200))
    rack_model = db.Column(db.String(200))
    racks_per_cluster = db.Column(db.Integer)
    series_count = db.Column(db.Integer)
    parallel_count = db.Column(db.Integer)
    nominal_voltage = db.Column(db.Float)
    nominal_capacity_ah = db.Column(db.Float)
    rated_energy_mwh = db.Column(db.Float)  # MWh, was nominal_energy_mwh (统一命名)
    rated_power_mw = db.Column(db.Float)  # MW, was nominal_power_mw (统一命名)
    dimensions = db.Column(db.String(200))
    weight = db.Column(db.Float)  # kg
    bmu_type = db.Column(db.String(100))
    status = db.Column(db.String(50), default="mass-production")

    def to_dict(self):
        return _model_to_dict(self)


class ContainerProduct(db.Model):
    """集装箱产品库（统一入口，合并原 container_library）"""

    __tablename__ = "container_products"

    __table_args__ = (db.Index("idx_container_products_tenant_id", "tenant_id"),)

    id = db.Column(db.String(100), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey("tenants.id"))
    is_builtin = db.Column(db.Boolean, default=False)
    mfr = db.Column(db.String(200))
    model = db.Column(db.String(200))
    spec = db.Column(db.String(100))  # 规格，was type
    rated_energy_mwh = db.Column(db.Float)  # MWh
    rated_power_mw = db.Column(db.Float)  # MW
    cluster_model = db.Column(db.String(200))
    clusters_per_container = db.Column(db.Integer)
    cell_model = db.Column(db.String(200))
    cell_config = db.Column(db.String(200))
    series_count = db.Column(db.Integer)
    parallel_count = db.Column(db.Integer)
    dc_voltage_range = db.Column(db.String(100))
    max_dc_current = db.Column(db.Float)
    dimensions = db.Column(db.String(200))
    cooling = db.Column(db.String(100))
    weight = db.Column(db.Float)  # t
    cycle_life = db.Column(db.Integer)
    rte = db.Column(db.Float)  # 往返效率 %
    aux_run = db.Column(db.Float)  # kW
    aux_standby = db.Column(db.Float)  # kW
    certifications = db.Column(db.Text)  # JSON
    unit_price = db.Column(db.Float)  # 万元/台
    remarks = db.Column(db.Text)
    status = db.Column(db.String(50), default="mass-production")
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    def to_dict(self):
        return _model_to_dict(self)


class PcsProduct(db.Model):
    """PCS变流器产品库（统一入口，合并原 pcs_library）"""

    __tablename__ = "pcs_products"

    __table_args__ = (db.Index("idx_pcs_products_tenant_id", "tenant_id"),)

    id = db.Column(db.String(100), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey("tenants.id"))
    is_builtin = db.Column(db.Boolean, default=False)
    mfr = db.Column(db.String(200))
    model = db.Column(db.String(200))
    rated_power_mw = db.Column(db.Float)  # MW
    rated_power_kva = db.Column(db.Float)  # KVA
    ac_voltage = db.Column(db.String(100))
    dc_voltage_range = db.Column(db.String(100))
    max_dc_current = db.Column(db.Float)  # A
    frequency_range = db.Column(db.String(50))  # Hz
    efficiency = db.Column(db.Float)  # %
    cooling = db.Column(db.String(100))
    topology = db.Column(db.String(100))
    isolation = db.Column(db.String(100))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.Float)  # kg
    aux_run = db.Column(db.Float)  # kW
    aux_standby = db.Column(db.Float)  # kW
    certifications = db.Column(db.Text)  # JSON
    unit_price = db.Column(db.Float)  # 万元/台
    remarks = db.Column(db.Text)
    status = db.Column(db.String(50), default="mass-production")
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    def to_dict(self):
        return _model_to_dict(self)


class BatteryConfigRule(db.Model):
    """电池层级配置规则模型"""

    __tablename__ = "battery_config_rules"

    __table_args__ = (db.Index("idx_battery_config_rules_tenant_id", "tenant_id"),)

    id = db.Column(db.String(36), primary_key=True)
    tenant_id = db.Column(db.String(36), db.ForeignKey("tenants.id"))
    is_builtin = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    cell_model = db.Column(db.String(100))
    pack_model = db.Column(db.String(100))
    rack_model = db.Column(db.String(100))
    cluster_model = db.Column(db.String(100))
    container_model = db.Column(db.String(100))

    cells_per_pack = db.Column(db.Integer)
    packs_per_rack = db.Column(db.Integer)
    racks_per_cluster = db.Column(db.Integer)
    clusters_per_container = db.Column(db.Integer)

    series_per_pack = db.Column(db.Integer)
    parallel_per_pack = db.Column(db.Integer)
    series_per_rack = db.Column(db.Integer)
    parallel_per_rack = db.Column(db.Integer)
    series_per_cluster = db.Column(db.Integer)
    parallel_per_cluster = db.Column(db.Integer)

    pack_nominal_voltage = db.Column(db.Float)
    pack_nominal_capacity_ah = db.Column(db.Float)
    pack_nominal_energy_kwh = db.Column(db.Float)

    rack_nominal_voltage = db.Column(db.Float)
    rack_nominal_capacity_ah = db.Column(db.Float)
    rack_nominal_energy_kwh = db.Column(db.Float)

    cluster_nominal_voltage = db.Column(db.Float)
    cluster_nominal_capacity_ah = db.Column(db.Float)
    cluster_nominal_energy_mwh = db.Column(db.Float)
    cluster_nominal_power_mw = db.Column(db.Float)

    container_nominal_energy_mwh = db.Column(db.Float)
    container_nominal_power_mw = db.Column(db.Float)

    is_default = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(50), default="active")
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    def to_dict(self):
        return _model_to_dict(self)


class BatteryManufacturer(db.Model):
    """电池厂家数据模型（含校准后的退化参数）"""

    __tablename__ = "battery_manufacturers"

    id = db.Column(db.String(50), primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    name_en = db.Column(db.String(255))
    country = db.Column(db.String(100))
    chemistry_type = db.Column(db.String(50))
    calibrated_params = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    def __repr__(self):
        return f"<BatteryManufacturer {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_en": self.name_en,
            "country": self.country,
            "chemistry_type": self.chemistry_type,
            "calibrated_params": self.calibrated_params,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
            "updated_at": (self.updated_at.isoformat() if self.updated_at else None),
        }
