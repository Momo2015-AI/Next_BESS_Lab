"""
产品库 API 路由
支持电芯、Pack、Rack、Cluster、集装箱、PCS 的 CRUD 操作和种子数据初始化
支持电池层级配置规则自动匹配
支持企业隔离（多租户）：超级管理员可见全部，普通用户仅可见自己企业
"""
import uuid
import json
import os
from flask import Blueprint, request, jsonify, current_app
from sqlalchemy import or_
from database import (
    db, CellProduct, PackProduct, RackProduct, ClusterProduct,
    ContainerProduct, PcsProduct, BatteryConfigRule, User
)
from routes.auth import _get_user_from_token

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
        'ratedEnergyMwh': 'rated_energy_mwh',
        'ratedEnergyMWh': 'rated_energy_mwh',
        'energyWh': 'rated_energy_mwh',  # 兼容旧字段
        'cycleLife': 'cycle_life',
        'sohCurve': 'soh_curve',
    },
    'packs': {
        'cellsPerPack': 'cells_per_pack',
        'seriesCount': 'series_count',
        'parallelCount': 'parallel_count',
        'nominalVoltage': 'nominal_voltage',
        'nominalCapacityAh': 'nominal_capacity_ah',
        'ratedEnergyMwh': 'rated_energy_mwh',
        'ratedEnergyMWh': 'rated_energy_mwh',
        'nominalEnergyKwh': 'rated_energy_mwh',  # 兼容旧字段
        'nominalEnergyKWh': 'rated_energy_mwh',
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
        'ratedEnergyMwh': 'rated_energy_mwh',
        'ratedEnergyMWh': 'rated_energy_mwh',
        'nominalEnergyKwh': 'rated_energy_mwh',  # 兼容旧字段
        'nominalEnergyKWh': 'rated_energy_mwh',
        'packModel': 'pack_model',
    },
    'clusters': {
        'racksPerCluster': 'racks_per_cluster',
        'seriesCount': 'series_count',
        'parallelCount': 'parallel_count',
        'nominalVoltage': 'nominal_voltage',
        'nominalCapacityAh': 'nominal_capacity_ah',
        'ratedEnergyMwh': 'rated_energy_mwh',
        'ratedEnergyMWh': 'rated_energy_mwh',
        'nominalEnergyMwh': 'rated_energy_mwh',  # 兼容旧字段
        'nominalEnergyMWh': 'rated_energy_mwh',
        'ratedPowerMw': 'rated_power_mw',
        'ratedPowerMW': 'rated_power_mw',
        'nominalPowerMw': 'rated_power_mw',  # 兼容旧字段
        'nominalPowerMW': 'rated_power_mw',
        'rackModel': 'rack_model',
        'bmuType': 'bmu_type',
    },
    'containers': {
        'ratedEnergyMWh': 'rated_energy_mwh',
        'ratedEnergyMwh': 'rated_energy_mwh',
        'ratedPowerMW': 'rated_power_mw',
        'ratedPowerMw': 'rated_power_mw',
        'cellModel': 'cell_model',
        'cellConfig': 'cell_config',
        'cycleLife': 'cycle_life',
        'clusterModel': 'cluster_model',
        'clustersPerContainer': 'clusters_per_container',
        'type': 'spec',  # 兼容旧字段
        'seriesCount': 'series_count',
        'parallelCount': 'parallel_count',
        'dcVoltageRange': 'dc_voltage_range',
        'maxDcCurrent': 'max_dc_current',
        'rte': 'rte',
        'auxRun': 'aux_run',
        'auxStandby': 'aux_standby',
        'certifications': 'certifications',
        'unitPrice': 'unit_price',
        'remarks': 'remarks',
    },
    'pcs': {
        'ratedPowerMW': 'rated_power_mw',
        'ratedPowerMw': 'rated_power_mw',
        'ratedPowerKVA': 'rated_power_kva',
        'ratedPowerKva': 'rated_power_kva',
        'acVoltage': 'ac_voltage',
        'dcVoltageRange': 'dc_voltage_range',
        'maxDcCurrent': 'max_dc_current',
        'frequencyRange': 'frequency_range',
        'topology': 'topology',
        'isolation': 'isolation',
        'dimensions': 'dimensions',
        'weight': 'weight',
        'efficiency': 'efficiency',
        'cooling': 'cooling',
        'auxRun': 'aux_run',
        'auxStandby': 'aux_standby',
        'certifications': 'certifications',
        'unitPrice': 'unit_price',
        'remarks': 'remarks',
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


def _get_current_user():
    """从请求中获取当前用户（如未认证则返回 None）"""
    user, _ = _get_user_from_token()
    return user


def _is_super_admin(user):
    """判断是否为超级管理员：role == 'admin'"""
    return user is not None and getattr(user, 'role', None) == 'admin'


def _apply_tenant_filter(query, model_cls, user, include_builtin=True):
    """
    应用企业隔离过滤：
    - 超级管理员：可见全部数据
    - 普通用户：仅可见自己企业数据 + 系统内置数据
    """
    if _is_super_admin(user):
        return query
    if user is None:
        # 未登录用户仅看系统内置数据
        if include_builtin and hasattr(model_cls, 'is_builtin'):
            return query.filter(model_cls.is_builtin == True)
        return query.filter(False)  # 不可见
    if hasattr(model_cls, 'tenant_id') and hasattr(model_cls, 'is_builtin'):
        if include_builtin:
            return query.filter(or_(model_cls.tenant_id == user.tenant_id, model_cls.is_builtin == True))
        return query.filter(model_cls.tenant_id == user.tenant_id)
    return query


def seed_products():
    """从 products.json 种子数据初始化产品库（标记为系统内置，所有企业可见）
    
    支持 upsert：ID 存在时更新所有字段，不存在时创建。
    避免因 _FIELD_MAP 修复后已有记录无法更新的问题。
    """
    if not os.path.exists(PRODUCTS_DATA_PATH):
        return

    with open(PRODUCTS_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for category, items in data.items():
        if category not in _MODELS:
            continue
        model_cls = _MODELS[category]
        for item in items:
            # 种子数据：标记为系统内置（对所有企业可见）
            if 'is_builtin' not in item:
                item['is_builtin'] = True
            if 'tenant_id' not in item:
                item['tenant_id'] = None

            existing = model_cls.query.get(item.get('id'))
            if existing:
                for k, v in item.items():
                    key = _camel_to_snake(k, category)
                    if hasattr(model_cls, key):
                        setattr(existing, key, v)
            else:
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
            # 仅清空系统内置数据
            if hasattr(model_cls, 'is_builtin'):
                model_cls.query.filter(model_cls.is_builtin == True).delete()
            else:
                model_cls.query.delete()
        db.session.commit()
        seed_products()
        return jsonify({'success': True, 'message': '产品库已刷新'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'刷新失败: {str(e)}'}), 500


@products_bp.route('/api/products/<category>', methods=['GET'])
def list_products(category):
    """获取产品列表（支持企业隔离）"""
    if category not in _MODELS:
        return jsonify({'error': f'未知产品类别: {category}'}), 400

    user = _get_current_user()
    model_cls = _MODELS[category]
    mfr = request.args.get('mfr')
    model_name = request.args.get('model')
    chemistry = request.args.get('chemistry')
    scope = request.args.get('scope', 'all')  # all / mine / builtin

    query = model_cls.query

    # 应用企业隔离
    if scope == 'builtin':
        if hasattr(model_cls, 'is_builtin'):
            query = query.filter(model_cls.is_builtin == True)
    elif scope == 'mine':
        if user and hasattr(model_cls, 'tenant_id'):
            query = query.filter(model_cls.tenant_id == user.tenant_id)
        else:
            query = query.filter(False)
    else:
        query = _apply_tenant_filter(query, model_cls, user)

    if mfr:
        query = query.filter(model_cls.mfr == mfr)
    if model_name:
        query = query.filter(model_cls.model == model_name)
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

    user = _get_current_user()
    model_cls = _MODELS[category]
    item = model_cls.query.get(item_id)
    if not item:
        return jsonify({'error': '产品不存在'}), 404

    # 权限检查
    if not _is_super_admin(user):
        if hasattr(item, 'tenant_id') and hasattr(item, 'is_builtin'):
            if not item.is_builtin and (not user or item.tenant_id != user.tenant_id):
                return jsonify({'error': '无权访问'}), 403

    return jsonify(item.to_dict())


@products_bp.route('/api/products/<category>', methods=['POST'])
def create_product(category):
    """新增产品（自动归属到当前用户的企业）"""
    if category not in _MODELS:
        return jsonify({'error': f'未知产品类别: {category}'}), 400

    user = _get_current_user()
    if not user:
        return jsonify({'error': '请先登录'}), 401

    data = request.get_json()
    if not data:
        return jsonify({'error': '无效请求数据'}), 400

    # 自动设置 tenant_id 与 is_builtin
    data['tenant_id'] = user.tenant_id
    data['is_builtin'] = False  # 用户新增的产品不是系统内置

    # 若未提供 id，自动生成
    if 'id' not in data or not data['id']:
        data['id'] = str(uuid.uuid4())

    obj = _json_to_model(data, category)
    db.session.add(obj)

    try:
        db.session.commit()
        return jsonify({'success': True, 'id': obj.id, 'item': obj.to_dict()}), 201
    except Exception:
        db.session.rollback()
        return jsonify({'error': '创建失败，ID可能已存在'}), 500


@products_bp.route('/api/products/<category>/<item_id>', methods=['PUT'])
def update_product(category, item_id):
    """更新产品（仅能修改自己企业的非系统内置数据）"""
    if category not in _MODELS:
        return jsonify({'error': f'未知产品类别: {category}'}), 400

    user = _get_current_user()
    if not user:
        return jsonify({'error': '请先登录'}), 401

    model_cls = _MODELS[category]
    item = model_cls.query.get(item_id)
    if not item:
        return jsonify({'error': '产品不存在'}), 404

    # 权限检查：仅超级管理员可改系统内置数据；普通用户仅能改自己企业数据
    if not _is_super_admin(user):
        if hasattr(item, 'is_builtin') and item.is_builtin:
            return jsonify({'error': '无权修改系统内置数据'}), 403
        if hasattr(item, 'tenant_id') and item.tenant_id != user.tenant_id:
            return jsonify({'error': '无权修改其他企业的数据'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'error': '无效请求数据'}), 400

    for k, v in data.items():
        key = _camel_to_snake(k, category)
        if hasattr(item, key) and key not in ('id', 'tenant_id', 'is_builtin'):
            setattr(item, key, v)

    try:
        db.session.commit()
        return jsonify({'success': True})
    except Exception:
        db.session.rollback()
        return jsonify({'error': '更新失败'}), 500


@products_bp.route('/api/products/<category>/<item_id>', methods=['DELETE'])
def delete_product(category, item_id):
    """删除产品（仅能删除自己企业的非系统内置数据）"""
    if category not in _MODELS:
        return jsonify({'error': f'未知产品类别: {category}'}), 400

    user = _get_current_user()
    if not user:
        return jsonify({'error': '请先登录'}), 401

    model_cls = _MODELS[category]
    item = model_cls.query.get(item_id)
    if not item:
        return jsonify({'error': '产品不存在'}), 404

    # 权限检查
    if not _is_super_admin(user):
        if hasattr(item, 'is_builtin') and item.is_builtin:
            return jsonify({'error': '无权删除系统内置数据'}), 403
        if hasattr(item, 'tenant_id') and item.tenant_id != user.tenant_id:
            return jsonify({'error': '无权删除其他企业的数据'}), 403

    db.session.delete(item)
    try:
        db.session.commit()
        return jsonify({'success': True})
    except Exception:
        db.session.rollback()
        return jsonify({'error': '删除失败'}), 500


@products_bp.route('/api/products/mfrs/<category>', methods=['GET'])
def list_manufacturers(category):
    """获取某类产品的厂商列表（受企业隔离影响）"""
    if category not in _MODELS:
        return jsonify({'error': f'未知产品类别: {category}'}), 400

    user = _get_current_user()
    model_cls = _MODELS[category]
    query = _apply_tenant_filter(db.session.query(model_cls.mfr), model_cls, user)
    mfrs = query.distinct().all()
    return jsonify({'mfrs': [m[0] for m in mfrs if m[0]]})


@products_bp.route('/api/products/models/<category>', methods=['GET'])
def list_models(category):
    """获取某类产品的型号列表（受企业隔离影响）"""
    if category not in _MODELS:
        return jsonify({'error': f'未知产品类别: {category}'}), 400

    user = _get_current_user()
    model_cls = _MODELS[category]
    mfr = request.args.get('mfr')

    query = _apply_tenant_filter(db.session.query(model_cls.model), model_cls, user)
    if mfr:
        query = query.filter(model_cls.mfr == mfr)

    models = query.distinct().all()
    return jsonify({'models': [m[0] for m in models if m[0]]})


@products_bp.route('/api/products/match-config', methods=['POST'])
def match_config_rule():
    """根据电芯/电池型号自动匹配配置规则（受企业隔离影响）"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '无效请求数据'}), 400

    user = _get_current_user()
    cell_model = data.get('cellModel')
    pack_model = data.get('packModel')
    rack_model = data.get('rackModel')
    cluster_model = data.get('clusterModel')
    container_model = data.get('containerModel')

    query = _apply_tenant_filter(BatteryConfigRule.query.filter(BatteryConfigRule.status == 'active'),
                                 BatteryConfigRule, user)

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
    """获取所有配置规则列表（受企业隔离影响）"""
    status = request.args.get('status', 'active')
    user = _get_current_user()
    query = _apply_tenant_filter(BatteryConfigRule.query, BatteryConfigRule, user)

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
    user = _get_current_user()
    rule = BatteryConfigRule.query.get(rule_id)
    if not rule:
        return jsonify({'error': '配置规则不存在'}), 404

    if not _is_super_admin(user):
        if hasattr(rule, 'is_builtin') and hasattr(rule, 'tenant_id'):
            if not rule.is_builtin and (not user or rule.tenant_id != user.tenant_id):
                return jsonify({'error': '无权访问'}), 403

    return jsonify(rule.to_dict())


@products_bp.route('/api/products/config-rules', methods=['POST'])
def create_config_rule():
    """创建配置规则（归属当前用户企业）"""
    user = _get_current_user()
    if not user:
        return jsonify({'error': '请先登录'}), 401

    data = request.get_json()
    if not data:
        return jsonify({'error': '无效请求数据'}), 400

    if 'id' not in data:
        data['id'] = str(uuid.uuid4())

    data['tenant_id'] = user.tenant_id
    data['is_builtin'] = False

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
    user = _get_current_user()
    if not user:
        return jsonify({'error': '请先登录'}), 401

    rule = BatteryConfigRule.query.get(rule_id)
    if not rule:
        return jsonify({'error': '配置规则不存在'}), 404

    if not _is_super_admin(user):
        if hasattr(rule, 'is_builtin') and rule.is_builtin:
            return jsonify({'error': '无权修改系统内置数据'}), 403
        if hasattr(rule, 'tenant_id') and rule.tenant_id != user.tenant_id:
            return jsonify({'error': '无权修改其他企业的数据'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'error': '无效请求数据'}), 400

    for k, v in data.items():
        key = _camel_to_snake(k, 'config_rules')
        if hasattr(rule, key) and key not in ('id', 'tenant_id', 'is_builtin'):
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
    user = _get_current_user()
    if not user:
        return jsonify({'error': '请先登录'}), 401

    rule = BatteryConfigRule.query.get(rule_id)
    if not rule:
        return jsonify({'error': '配置规则不存在'}), 404

    if not _is_super_admin(user):
        if hasattr(rule, 'is_builtin') and rule.is_builtin:
            return jsonify({'error': '无权删除系统内置数据'}), 403
        if hasattr(rule, 'tenant_id') and rule.tenant_id != user.tenant_id:
            return jsonify({'error': '无权删除其他企业的数据'}), 403

    db.session.delete(rule)
    try:
        db.session.commit()
        return jsonify({'success': True})
    except Exception:
        db.session.rollback()
        return jsonify({'error': '删除失败'}), 500


@products_bp.route('/api/products/hierarchy', methods=['POST'])
def get_hierarchy():
    """获取完整的电池层级配置信息（受企业隔离影响）"""
    user = _get_current_user()
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
        cell_query = _apply_tenant_filter(
            CellProduct.query.filter(CellProduct.model == cell_model), CellProduct, user
        )
        cell = cell_query.first()
        if cell:
            result['cell'] = cell.to_dict()
            packs_query = _apply_tenant_filter(
                PackProduct.query.filter(PackProduct.cell_model == cell_model), PackProduct, user
            )
            packs = packs_query.all()
            if packs:
                result['pack'] = packs[0].to_dict()
                pack_model = packs[0].model
                racks_query = _apply_tenant_filter(
                    RackProduct.query.filter(RackProduct.pack_model == pack_model), RackProduct, user
                )
                racks = racks_query.all()
                if racks:
                    result['rack'] = racks[0].to_dict()
                    rack_model = racks[0].model
                    clusters_query = _apply_tenant_filter(
                        ClusterProduct.query.filter(ClusterProduct.rack_model == rack_model),
                        ClusterProduct, user
                    )
                    clusters = clusters_query.all()
                    if clusters:
                        result['cluster'] = clusters[0].to_dict()
                        cluster_model = clusters[0].model
                        containers_query = _apply_tenant_filter(
                            ContainerProduct.query.filter(
                                or_(
                                    ContainerProduct.cluster_model == cluster_model,
                                    ContainerProduct.cell_model == cell_model,
                                )
                            ),
                            ContainerProduct, user
                        )
                        containers = containers_query.all()
                        if containers:
                            result['container'] = containers[0].to_dict()

    elif pack_model:
        pack_query = _apply_tenant_filter(
            PackProduct.query.filter(PackProduct.model == pack_model), PackProduct, user
        )
        pack = pack_query.first()
        if pack:
            result['pack'] = pack.to_dict()
            racks_query = _apply_tenant_filter(
                RackProduct.query.filter(RackProduct.pack_model == pack_model), RackProduct, user
            )
            racks = racks_query.all()
            if racks:
                result['rack'] = racks[0].to_dict()
                rack_model = racks[0].model
                clusters_query = _apply_tenant_filter(
                    ClusterProduct.query.filter(ClusterProduct.rack_model == rack_model),
                    ClusterProduct, user
                )
                clusters = clusters_query.all()
                if clusters:
                    result['cluster'] = clusters[0].to_dict()
                    cluster_model = clusters[0].model
                    containers_query = _apply_tenant_filter(
                        ContainerProduct.query.filter(ContainerProduct.cluster_model == cluster_model),
                        ContainerProduct, user
                    )
                    containers = containers_query.all()
                    if containers:
                        result['container'] = containers[0].to_dict()

    rule_query = _apply_tenant_filter(
        BatteryConfigRule.query.filter(
            BatteryConfigRule.status == 'active',
        ),
        BatteryConfigRule, user
    )
    if cell_model:
        rule_query = rule_query.filter(BatteryConfigRule.cell_model == cell_model)
    if pack_model:
        rule_query = rule_query.filter(BatteryConfigRule.pack_model == pack_model)

    rule_match = rule_query.first()
    if rule_match:
        result['config_rule'] = rule_match.to_dict()

    return jsonify({
        'success': True,
        'data': result,
    })
