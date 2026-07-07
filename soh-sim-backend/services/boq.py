"""BOQ 业务逻辑"""

import uuid

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
            db.select(db.Model.metadata.tables["boq_sections"]).where(
                db.Model.metadata.tables["boq_sections"].c.code == cat["code"]
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


def save_boq_items(db, BoqItem, project_id, items_data, is_alternative=False):
    """保存BOQ清单项：先删除已有项，再批量写入"""
    BoqItem.query.filter_by(project_id=project_id, is_alternative=is_alternative).delete()

    saved = []
    for item in items_data:
        boq_item = BoqItem(
            id=item.get("id") or str(uuid.uuid4()),
            project_id=project_id,
            section_code=item.get("sectionCode", ""),
            seq=item.get("seq", 0),
            name=item.get("name", ""),
            spec=item.get("spec", ""),
            unit=item.get("unit", ""),
            quantity=float(item.get("quantity", 0) or 0),
            unit_price=float(item.get("unitPrice", 0) or 0),
            total_price=float(item.get("totalPrice", 0) or item.get("quantity", 0) * item.get("unitPrice", 0) or 0),
            note=item.get("note", ""),
            is_alternative=is_alternative,
            version=item.get("version", 1),
        )
        db.session.add(boq_item)
        saved.append(boq_item)

    db.session.commit()
    return saved


def bump_boq_version(db, BoqItem, project_id):
    """BOQ版本号递增"""
    items = BoqItem.query.filter_by(project_id=project_id, is_alternative=False).all()
    for item in items:
        item.version += 1
    db.session.commit()
    return items[0].version if items else 1
