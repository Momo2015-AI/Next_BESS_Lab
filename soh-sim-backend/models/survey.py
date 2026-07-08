from . import db, _utcnow


class Survey(db.Model):
    """调研表模型 - 存储客户填写的调研信息"""

    __tablename__ = "surveys"

    __table_args__ = (db.Index("idx_surveys_project_id", "project_id"),)

    id = db.Column(db.String(36), primary_key=True)
    project_name = db.Column(db.String(200), nullable=False)
    contact_person = db.Column(db.String(100))
    contact_phone = db.Column(db.String(50))
    contact_email = db.Column(db.String(100))

    # 项目基本信息
    location = db.Column(db.String(200))
    altitude = db.Column(db.Float)
    total_mw = db.Column(db.Float)
    total_mwh = db.Column(db.Float)
    duration = db.Column(db.Float)

    # 运行条件
    cycles_per_day = db.Column(db.Float, default=1.0)
    temp_max = db.Column(db.Float)
    temp_min = db.Column(db.Float)
    temp_avg = db.Column(db.Float)
    humidity = db.Column(db.Float)

    # 电网参数
    grid_voltage = db.Column(db.Float)
    grid_frequency = db.Column(db.Float)
    pcc_voltage = db.Column(db.Float)
    pcc_short_circuit_mva = db.Column(db.Float)
    grid_code = db.Column(db.String(50))

    # 环境条件
    sand_protection = db.Column(db.String(10))
    humidity_cycle = db.Column(db.String(20))

    # 性能要求
    rte_target = db.Column(db.Float)
    soh_year1 = db.Column(db.Float)
    soh_year25 = db.Column(db.Float)
    calendar_life = db.Column(db.Integer)
    cycle_life = db.Column(db.Integer)
    availability_target = db.Column(db.Float)

    # 辅助参数
    aux_consumption = db.Column(db.Float)
    response_time = db.Column(db.Float)
    dc_voltage_range = db.Column(db.String(100))
    ac_voltage = db.Column(db.Float)
    thdi = db.Column(db.Float)

    # 其他信息
    remarks = db.Column(db.Text)
    attachments = db.Column(db.Text)

    # 状态与时间
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    # 关联
    project_id = db.Column(db.String(36), db.ForeignKey("projects.id"))
    project = db.relationship("Project", back_populates="surveys")

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "project_name": self.project_name,
            "contact_person": self.contact_person,
            "contact_phone": self.contact_phone,
            "contact_email": self.contact_email,
            "location": self.location,
            "altitude": self.altitude,
            "total_mw": self.total_mw,
            "total_mwh": self.total_mwh,
            "duration": self.duration,
            "cycles_per_day": self.cycles_per_day,
            "temp_max": self.temp_max,
            "temp_min": self.temp_min,
            "temp_avg": self.temp_avg,
            "humidity": self.humidity,
            "grid_voltage": self.grid_voltage,
            "grid_frequency": self.grid_frequency,
            "pcc_voltage": self.pcc_voltage,
            "pcc_short_circuit_mva": self.pcc_short_circuit_mva,
            "grid_code": self.grid_code,
            "sand_protection": self.sand_protection,
            "humidity_cycle": self.humidity_cycle,
            "rte_target": self.rte_target,
            "soh_year1": self.soh_year1,
            "soh_year25": self.soh_year25,
            "calendar_life": self.calendar_life,
            "cycle_life": self.cycle_life,
            "availability_target": self.availability_target,
            "aux_consumption": self.aux_consumption,
            "response_time": self.response_time,
            "dc_voltage_range": self.dc_voltage_range,
            "ac_voltage": self.ac_voltage,
            "thdi": self.thdi,
            "remarks": self.remarks,
            "attachments": self.attachments,
            "status": self.status,
            "created_at": (
                self.created_at.isoformat() if self.created_at else None
            ),
            "updated_at": (
                self.updated_at.isoformat() if self.updated_at else None
            ),
        }
