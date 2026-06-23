"""
产品库 API 路由
支持电芯、Pack、Rack、Cluster、集装箱、PCS 的 CRUD 操作和种子数据初始化
支持电池层级配置规则自动匹配
"""
import uuid
import json
import os
from flask import Blueprint, request, jsonify, current_app
from database import db, CellProduct, PackProduct, RackProduct, ClusterProduct, ContainerProduct, PcsProduct, BatteryConfigRule

products_bp = Blueprint('products', __name__)

PRODUCTS_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'products.json')

_MODELS = {
    'cells': CellProduct,
    'packs': PackProduct,
    'racks': RackProduct,
    'clusters': ClusterProduct,
    'containers': ContainerProduct,
    'pcs': PcsProduct,
    'config_rules': BatteryConfigRule,
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
    'packs': {
        'cellsPerPack': 'cells_per_pack',
        'seriesCount': 'series_count',
        'parallelCount': 'parallel_count',
        'nominalVoltage': 'nominal_voltage',
        'nominalCapacityAh': 'nominal_capacity_ah',
        'nominalEnergyKwh': 'nominal_energy_kwh',
        'maxChargeCurrent': 'max_charge_current',
        'maxDischargeCurrent': 'max_discharge_current',
        'cellModel': 'cell_model',
        'bmsType': 'bms_type',
    },
    'racks': {
        'packsPerRack': 'packs_per_rack',
        'seriesCount': 'series_count',
        'parallelCount': 'parallel_count',
        'nominalVoltage': 'nominal_voltage',
        'nominalCapacityAh': 'nominal_capacity_ah',
        'nominalEnergyKwh': 'nominal_energy_kwh',
        'packModel': 'pack_model',
    },
    'clusters': {
        'racksPerCluster': 'racks_per_cluster',
        'seriesCount': 'series_count',
        'parallelCount': 'parallel_count',
        'nominalVoltage': 'nominal_voltage',
        'nominalCapacityAh': 'nominal_capacity_ah',
        'nominalEnergyMwh': 'nominal_energy_mwh',
        'nominalPowerMw': 'nominal_power_mw',
        'rackModel': 'rack_model',
        'bmuType': 'bmu_type',
    },
    'containers': {
        'ratedEnergyMWh': 'rated_energy_mwh',
        'ratedPowerMW': 'rated_power_mw',
        'cellModel': 'cell_model',
        'cellConfig': 'cell_config',
        'cycleLife': 'cycle_life',
        'clusterModel': 'cluster_model',
        'clustersPerContainer': 'clusters_per_container',
    },
    'pcs': {
        'ratedPowerMW': 'rated_power_mw',
        'ratedPowerKVA': 'rated_power_kva',
        'acVoltage': 'ac_voltage',
        'dcVoltageRange': 'dc_voltage_range',
    },
    'config_rules': {
        'cellModel': 'cell_model',
        'packModel': 'pack_model',
        'rackModel': 'rack_model',
        'clusterModel': 'cluster_model',
        'containerModel': 'container_model',
        'cellsPerPack': 'cells_per_pack',
        'packsPerRack': 'packs_per_rack',
        'racksPerCluster': 'racks_per_cluster',
        'clustersPerContainer': 'clusters_per_container',
        'seriesPerPack': 'series_per_pack',
        'parallelPerPack': 'parallel_per_pack',
        'seriesPerRack': 'series_per_rack',
        'parallelPerRack': 'parallel_per_rack',
        'seriesPerCluster': 'series_per_cluster',
        'parallelPerCluster': 'parallel_per_cluster',
        'packNominalVoltage': 'pack_nominal_voltage',
        'packNominalCapacityAh': 'pack_nominal_capacity_ah',
        'packNominalEnergyKwh': 'pack_nominal_energy_kwh',
        'rackNominalVoltage': 'rack_nominal_voltage',
        'rackNominalCapacityAh': 'rack_nominal_capacity_ah',
        'rackNominalEnergyKwh': 'rack_nominal_energy_kwh',
        'clusterNominalVoltage': 'cluster_nominal_voltage',
        'clusterNominalCapacityAh': 'cluster_nominal_capacity_ah',
        'clusterNominalEnergyMwh': 'cluster_nominal_energy_mwh',
        'clusterNominalPowerMw': 'cluster_nominal_power_mw',
        'containerNominalEnergyMwh': 'container_nominal_energy_mwh',
        'containerNominalPowerMw': 'container_nominal_power_mw',
        'isDefault': 'is_default',
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

    with open(PRODUCTS_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for category, items in data.items():
        if category not in _MODELS:
            continue
        model_cls = _MODELS[category]
        for item in items:
            existing = model_cls.query.get(item.get('id'))
            if not existing:
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


@products_bp.route('/api/products/refresh', methods=['POST'])
def refresh_products():
    """刷新产品库：清空现有数据并重新导入种子数据"""
    try:
        for category, model_cls in _MODELS.items():
            model_cls.query.delete()
        db.session.commit()
        seed_products()
        return jsonify({'success': True, 'message': '产品库已刷新'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'刷新失败: {str(e)}'}), 500


@products_bp.route('/api/products/<category>', methods=['GET'])
def list_products(category):
    """获取产品列表"""
    if category not in _MODELS:
        return jsonify({'error': f'未知产品类别: {category}'}), 400

    model_cls = _MODELS[category]
    mfr = request.args.get('mfr')
    model = request.args.get('model')
    chemistry = request.args.get('chemistry')

    query = model_cls.query
    if mfr:
        query = query.filter(model_cls.mfr == mfr)
    if model:
        query = query.filter(model_cls.model == model)
    if chemistry and hasattr(model_cls, 'chemistry'):
        query = query.filter(model_cls.chemistry == chemistry)

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


@products_bp.route('/api/products/models/<category>', methods=['GET'])
def list_models(category):
    """获取某类产品的型号列表"""
    if category not in _MODELS:
        return jsonify({'error': f'未知产品类别: {category}'}), 400

    model_cls = _MODELS[category]
    mfr = request.args.get('mfr')
    
    query = db.session.query(model_cls.model).distinct()
    if mfr:
        query = query.filter(model_cls.mfr == mfr)
    
    models = query.all()
    return jsonify({'models': [m[0] for m in models if m[0]]})


@products_bp.route('/api/products/match-config', methods=['POST'])
def match_config_rule():
    """根据电芯/电池型号自动匹配配置规则"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '无效请求数据'}), 400

    cell_model = data.get('cellModel')
    pack_model = data.get('packModel')
    rack_model = data.get('rackModel')
    cluster_model = data.get('clusterModel')
    container_model = data.get('containerModel')

    query = BatteryConfigRule.query.filter(BatteryConfigRule.status == 'active')

    if cell_model:
        query = query.filter(BatteryConfigRule.cell_model == cell_model)
    if pack_model:
        query = query.filter(BatteryConfigRule.pack_model == pack_model)
    if rack_model:
        query = query.filter(BatteryConfigRule.rack_model == rack_model)
    if cluster_model:
        query = query.filter(BatteryConfigRule.cluster_model == cluster_model)
    if container_model:
        query = query.filter(BatteryConfigRule.container_model == container_model)

    rules = query.all()
    
    if rules:
        default_rule = next((r for r in rules if r.is_default), rules[0])
        return jsonify({
            'success': True,
            'matched': True,
            'rule': default_rule.to_dict(),
            'all_rules': [r.to_dict() for r in rules],
        })
    else:
        return jsonify({
            'success': True,
            'matched': False,
            'rule': None,
            'all_rules': [],
            'message': '未找到匹配的配置规则，请手动配置',
        })


@products_bp.route('/api/products/config-rules', methods=['GET'])
def list_config_rules():
    """获取所有配置规则列表"""
    status = request.args.get('status', 'active')
    query = BatteryConfigRule.query
    
    if status:
        query = query.filter(BatteryConfigRule.status == status)
    
    rules = query.all()
    return jsonify({
        'items': [r.to_dict() for r in rules],
        'total': len(rules),
    })


@products_bp.route('/api/products/config-rules/<rule_id>', methods=['GET'])
def get_config_rule(rule_id):
    """获取单个配置规则详情"""
    rule = BatteryConfigRule.query.get(rule_id)
    if not rule:
        return jsonify({'error': '配置规则不存在'}), 404
    return jsonify(rule.to_dict())


@products_bp.route('/api/products/config-rules', methods=['POST'])
def create_config_rule():
    """创建配置规则"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '无效请求数据'}), 400

    if 'id' not in data:
        data['id'] = str(uuid.uuid4())
    
    rule = _json_to_model(data, 'config_rules')
    db.session.add(rule)

    try:
        db.session.commit()
        return jsonify({'success': True, 'id': rule.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'创建失败: {str(e)}'}), 500


@products_bp.route('/api/products/config-rules/<rule_id>', methods=['PUT'])
def update_config_rule(rule_id):
    """更新配置规则"""
    rule = BatteryConfigRule.query.get(rule_id)
    if not rule:
        return jsonify({'error': '配置规则不存在'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': '无效请求数据'}), 400

    for k, v in data.items():
        key = _camel_to_snake(k, 'config_rules')
        if hasattr(rule, key) and key != 'id':
            setattr(rule, key, v)

    try:
        db.session.commit()
        return jsonify({'success': True})
    except Exception:
        db.session.rollback()
        return jsonify({'error': '更新失败'}), 500


@products_bp.route('/api/products/config-rules/<rule_id>', methods=['DELETE'])
def delete_config_rule(rule_id):
    """删除配置规则"""
    rule = BatteryConfigRule.query.get(rule_id)
    if not rule:
        return jsonify({'error': '配置规则不存在'}), 404

    db.session.delete(rule)
    try:
        db.session.commit()
        return jsonify({'success': True})
    except Exception:
        db.session.rollback()
        return jsonify({'error': '删除失败'}), 500


@products_bp.route('/api/products/hierarchy', methods=['POST'])
def get_hierarchy():
    """获取完整的电池层级配置信息"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '无效请求数据'}), 400

    cell_model = data.get('cellModel')
    pack_model = data.get('packModel')

    result = {
        'cell': None,
        'pack': None,
        'rack': None,
        'cluster': None,
        'container': None,
        'config_rule': None,
    }

    if cell_model:
        cell = CellProduct.query.filter(CellProduct.model == cell_model).first()
        if cell:
            result['cell'] = cell.to_dict()
            packs = PackProduct.query.filter(PackProduct.cell_model == cell_model).all()
            if packs:
                result['pack'] = packs[0].to_dict()
                pack_model = packs[0].model
                racks = RackProduct.query.filter(RackProduct.pack_model == pack_model).all()
                if racks:
                    result['rack'] = racks[0].to_dict()
                    rack_model = racks[0].model
                    clusters = ClusterProduct.query.filter(ClusterProduct.rack_model == rack_model).all()
                    if clusters:
                        result['cluster'] = clusters[0].to_dict()
                        cluster_model = clusters[0].model
                        containers = ContainerProduct.query.filter(
                            (ContainerProduct.cluster_model == cluster_model) |
                            (ContainerProduct.cell_model == cell_model)
                        ).all()
                        if containers:
                            result['container'] = containers[0].to_dict()

    elif pack_model:
        pack = PackProduct.query.filter(PackProduct.model == pack_model).first()
        if pack:
            result['pack'] = pack.to_dict()
            racks = RackProduct.query.filter(RackProduct.pack_model == pack_model).all()
            if racks:
                result['rack'] = racks[0].to_dict()
                rack_model = racks[0].model
                clusters = ClusterProduct.query.filter(ClusterProduct.rack_model == rack_model).all()
                if clusters:
                    result['cluster'] = clusters[0].to_dict()
                    cluster_model = clusters[0].model
                    containers = ContainerProduct.query.filter(
                        ContainerProduct.cluster_model == cluster_model
                    ).all()
                    if containers:
                        result['container'] = containers[0].to_dict()

    rule_match = BatteryConfigRule.query.filter(
        BatteryConfigRule.status == 'active',
        ((BatteryConfigRule.cell_model == cell_model) if cell_model else True),
        ((BatteryConfigRule.pack_model == pack_model) if pack_model else True),
    ).first()

    if rule_match:
        result['config_rule'] = rule_match.to_dict()

    return jsonify({
        'success': True,
        'data': result,
    })