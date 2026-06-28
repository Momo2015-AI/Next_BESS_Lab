"""BOQ 业务逻辑"""

BOQ_CATEGORIES = [
    {"code": "100", "name": "Battery System", "name_zh": "电池系统", "unit": "MWh", "sort_order": 1},
    {"code": "200", "name": "PCS", "name_zh": "PCS 变流系统", "unit": "MW", "sort_order": 2},
    {"code": "300", "name": "BOP", "name_zh": "电站配套 BOP", "unit": "lot", "sort_order": 3},
    {"code": "400", "name": "Civil Works", "name_zh": "土建工程", "unit": "sqm", "sort_order": 4},
    {"code": "500", "name": "Grid Connection", "name_zh": "并网接入", "unit": "lot", "sort_order": 5},
    {"code": "600", "name": "EMS", "name_zh": "能量管理系统 EMS", "unit": "lot", "sort_order": 6},
    {"code": "700", "name": "Commissioning & O&M", "name_zh": "调试与运维", "unit": "lot", "sort_order": 7},
]


def seed_boq_sections(db):
    """初始化 7 级 BOQ 分类模板"""
    for cat in BOQ_CATEGORIES:
        existing = db.session.execute(
            db.select(db.Model.metadata.tables['boq_sections']).where(
                db.Model.metadata.tables['boq_sections'].c.code == cat["code"]
            )
        ).first()
        if not existing:
            from database import BoqSection
            section = BoqSection(
                code=cat["code"],
                name=cat["name"],
                name_zh=cat["name_zh"],
                default_unit=cat["unit"],
                sort_order=cat["sort_order"],
            )
            db.session.add(section)
    db.session.commit()
