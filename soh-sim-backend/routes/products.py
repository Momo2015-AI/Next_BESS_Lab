"""
产品库 API 路由
支持电芯、集装箱、PCS 的 CRUD 操作和种子数据初始化
"""
import json
import os
from flask import Blueprint, request, jsonify, current_app
from database import db, CellProduct, ContainerProduct, PcsProduct

products_bp = Blueprint('products', __name__)

PRODUCTS_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'products.json')

_MODELS = {
    'cells': CellProduct,
    'containers': ContainerProduct,
    'pcs': PcsProduct,
}

_FIELD_MAP = {
    'cells': {
        'capacityAh': 'capacity_ah',
        'voltageNominal': 'voltage_nominal',
        'voltageRange': 'voltage_range',
        'energyWh': 'energy_wh',
        'cycleLife': 'cycle_life',
        'sohCurve': 'soh_curve',
    },
    'containers': {
        'ratedEnergyMWh': 'rated_energy_mwh',
        'ratedPowerMW': 'rated_power_mw',
        'cellModel': 'cell_model',
        'cellConfig': 'cell_config',
        'cycleLife': 'cycle_life',
    },
    'pcs': {
        'ratedPowerMW': 'rated_power_mw',
        'ratedPowerKVA': 'rated_power_kva',
        'acVoltage': 'ac_voltage',
        'dcVoltageRange': 'dc_voltage_range',
    },
}


def _camel_to_snake(name, category):
    return _FIELD_MAP.get(category, {}).get(name, name)


def _json_to_model(item, category):
    model_cls = _MODELS[category]
    kwargs = {}
    for k, v in item.items():
        key = _camel_to_snake(k, category)
        if hasattr(model_cls, key):
            kwargs[key] = v
    return model_cls(**kwargs)


def seed_products():
    """从 products.json 种子数据初始化产品库"""
    if not os.path.exists(PRODUCTS_DATA_PATH):
        return

    if CellProduct.query.first() is not None:
        return

    with open(PRODUCTS_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for category, items in data.items():
        if category not in _MODELS:
            continue
        for item in items:
            obj = _json_to_model(item, category)
            db.session.add(obj)

    db.session.commit()


@products_bp.route('/api/products/seed', methods=['POST'])
def seed_api():
    """手动触发种子数据初始化"""
    try:
        seed_products()
        return jsonify({'success': True, 'message': '种子数据已初始化'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'初始化失败: {str(e)}'}), 500


@products_bp.route('/api/products/<category>', methods=['GET'])
def list_products(category):
    """获取产品列表"""
    if category not in _MODELS:
        return jsonify({'error': f'未知产品类别: {category}'}), 400

    model_cls = _MODELS[category]
    mfr = request.args.get('mfr')

    query = model_cls.query
    if mfr:
        query = query.filter(model_cls.mfr == mfr)

    items = query.all()
    return jsonify({
        'items': [item.to_dict() for item in items],
        'total': len(items),
    })


@products_bp.route('/api/products/<category>/<item_id>', methods=['GET'])
def get_product(category, item_id):
    """获取单个产品详情"""
    if category not in _MODELS:
        return jsonify({'error': f'未知产品类别: {category}'}), 400

    model_cls = _MODELS[category]
    item = model_cls.query.get(item_id)
    if not item:
        return jsonify({'error': '产品不存在'}), 404
    return jsonify(item.to_dict())


@products_bp.route('/api/products/<category>', methods=['POST'])
def create_product(category):
    """新增产品"""
    if category not in _MODELS:
        return jsonify({'error': f'未知产品类别: {category}'}), 400

    data = request.get_json()
    if not data:
        return jsonify({'error': '无效请求数据'}), 400

    obj = _json_to_model(data, category)
    db.session.add(obj)

    try:
        db.session.commit()
        return jsonify({'success': True, 'id': obj.id}), 201
    except Exception:
        db.session.rollback()
        return jsonify({'error': '创建失败，ID可能已存在'}), 500


@products_bp.route('/api/products/<category>/<item_id>', methods=['PUT'])
def update_product(category, item_id):
    """更新产品"""
    if category not in _MODELS:
        return jsonify({'error': f'未知产品类别: {category}'}), 400

    model_cls = _MODELS[category]
    item = model_cls.query.get(item_id)
    if not item:
        return jsonify({'error': '产品不存在'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': '无效请求数据'}), 400

    for k, v in data.items():
        key = _camel_to_snake(k, category)
        if hasattr(item, key) and key != 'id':
            setattr(item, key, v)

    try:
        db.session.commit()
        return jsonify({'success': True})
    except Exception:
        db.session.rollback()
        return jsonify({'error': '更新失败'}), 500


@products_bp.route('/api/products/<category>/<item_id>', methods=['DELETE'])
def delete_product(category, item_id):
    """删除产品"""
    if category not in _MODELS:
        return jsonify({'error': f'未知产品类别: {category}'}), 400

    model_cls = _MODELS[category]
    item = model_cls.query.get(item_id)
    if not item:
        return jsonify({'error': '产品不存在'}), 404

    db.session.delete(item)
    try:
        db.session.commit()
        return jsonify({'success': True})
    except Exception:
        db.session.rollback()
        return jsonify({'error': '删除失败'}), 500


@products_bp.route('/api/products/mfrs/<category>', methods=['GET'])
def list_manufacturers(category):
    """获取某类产品的厂商列表"""
    if category not in _MODELS:
        return jsonify({'error': f'未知产品类别: {category}'}), 400

    model_cls = _MODELS[category]
    mfrs = db.session.query(model_cls.mfr).distinct().all()
    return jsonify({'mfrs': [m[0] for m in mfrs if m[0]]})
