"""
算法模型管理API - 支持算法模型库的CRUD操作
"""
import uuid
import json
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from database import db, AlgorithmModel, User
from routes.auth import token_required

algorithm_bp = Blueprint('algorithm', __name__)


def get_builtin_algorithms():
    """获取内置算法模型列表"""
    return [
        {
            'name': '双指数模型',
            'name_en': 'Double Exponential Model',
            'model_type': 'double_exponential',
            'applicable_scenarios': ['LFP日历衰减', '循环衰减', '综合衰减'],
            'mathematical_form': 'SOH(t) = A·e^(-k₁t) + B·e^(-k₂t) + C',
            'formula_expression': 'A * Math.exp(-k1 * t) + B * Math.exp(-k2 * t) + C',
            'parameters': {
                'A': {'label': '快速衰减幅度', 'default': 0.15, 'min': 0, 'max': 0.5, 'unit': ''},
                'B': {'label': '慢速衰减幅度', 'default': 0.08, 'min': 0, 'max': 0.3, 'unit': ''},
                'k1': {'label': '快速衰减系数', 'default': 0.05, 'min': 0, 'max': 0.2, 'unit': '1/年'},
                'k2': {'label': '慢速衰减系数', 'default': 0.008, 'min': 0, 'max': 0.05, 'unit': '1/年'},
                'C': {'label': '剩余容量', 'default': 0.77, 'min': 0.5, 'max': 0.9, 'unit': ''},
            },
            'accuracy_level': 'high',
            'accuracy_desc': 'R²>0.999',
            'category': 'soh',
            'is_builtin': True,
            'description': '适用于LFP电池的日历衰减和循环衰减，采用双指数形式描述容量衰减过程，快速衰减阶段描述SEI膜形成，慢速衰减阶段描述活性物质损失。',
        },
        {
            'name': '线性-对数模型',
            'name_en': 'Linear-Log Model',
            'model_type': 'linear_log',
            'applicable_scenarios': ['RTE衰减', '效率衰减'],
            'mathematical_form': 'RTE(t) = RTE₀ - αt - β·ln(1+γt)',
            'formula_expression': 'RTE0 - alpha * t - beta * Math.log(1 + gamma * t)',
            'parameters': {
                'RTE0': {'label': '初始RTE', 'default': 0.94, 'min': 0.8, 'max': 0.99, 'unit': ''},
                'alpha': {'label': '线性衰减系数', 'default': 0.0008, 'min': 0, 'max': 0.005, 'unit': '1/年'},
                'beta': {'label': '对数衰减幅度', 'default': 0.02, 'min': 0, 'max': 0.1, 'unit': ''},
                'gamma': {'label': '对数衰减速率', 'default': 0.5, 'min': 0, 'max': 5, 'unit': '1/年'},
            },
            'accuracy_level': 'high',
            'accuracy_desc': 'R²>0.99',
            'category': 'rte',
            'is_builtin': True,
            'description': '适用于储能系统RTE衰减建模，线性项描述设备老化，对数项描述效率下降的减缓趋势。',
        },
        {
            'name': 'Arrhenius模型',
            'name_en': 'Arrhenius Model',
            'model_type': 'arrhenius',
            'applicable_scenarios': ['温度加速衰减', '日历老化'],
            'mathematical_form': 'k = A·e^(-Ea/RT)',
            'formula_expression': 'A * Math.exp(-Ea / (R * T))',
            'parameters': {
                'A': {'label': '指前因子', 'default': 1e12, 'min': 1e6, 'max': 1e18, 'unit': '1/年'},
                'Ea': {'label': '活化能', 'default': 35, 'min': 20, 'max': 80, 'unit': 'kJ/mol'},
                'R': {'label': '气体常数', 'default': 8.314, 'min': 8.0, 'max': 8.5, 'unit': 'J/mol·K'},
                'T_ref': {'label': '参考温度', 'default': 298, 'min': 273, 'max': 350, 'unit': 'K'},
            },
            'accuracy_level': 'medium',
            'accuracy_desc': 'R²>0.95',
            'category': 'soh',
            'is_builtin': True,
            'description': '基于Arrhenius方程的温度加速老化模型，描述温度对衰减速率的影响，适用于日历寿命预测。',
        },
        {
            'name': '雨流计数法',
            'name_en': 'Rainflow Counting Method',
            'model_type': 'rainflow',
            'applicable_scenarios': ['不规则循环损伤', '实际工况'],
            'mathematical_form': '基于实际充放电剖面统计',
            'formula_expression': 'rainflow_count(profile)',
            'parameters': {
                'damage_exponent': {'label': '损伤指数', 'default': 1.5, 'min': 1, 'max': 3, 'unit': ''},
                'cycle_life_ref': {'label': '参考循环寿命', 'default': 6000, 'min': 1000, 'max': 20000, 'unit': '次'},
                'dod_ref': {'label': '参考DOD', 'default': 1.0, 'min': 0.1, 'max': 1.0, 'unit': ''},
            },
            'accuracy_level': 'high',
            'accuracy_desc': '与实际工况高度吻合',
            'category': 'soh',
            'is_builtin': True,
            'description': '基于雨流计数法的循环寿命预测，能够处理不规则的充放电剖面，统计等效循环次数并计算累积损伤。',
        },
        {
            'name': '半经验模型',
            'name_en': 'Semi-Empirical Model',
            'model_type': 'semi_empirical',
            'applicable_scenarios': ['多应力耦合', '综合衰减'],
            'mathematical_form': 'SOH = f(温度×DOD×C-rate×SOC窗口)',
            'formula_expression': '1 - temp_factor * dod_factor * c_rate_factor * soc_factor',
            'parameters': {
                'temp_coeff': {'label': '温度系数', 'default': 0.002, 'min': 0, 'max': 0.01, 'unit': '1/°C'},
                'dod_coeff': {'label': 'DOD系数', 'default': 0.5, 'min': 0, 'max': 2, 'unit': ''},
                'c_rate_coeff': {'label': '倍率系数', 'default': 0.1, 'min': 0, 'max': 1, 'unit': ''},
                'soc_coeff': {'label': 'SOC窗口系数', 'default': 0.3, 'min': 0, 'max': 1, 'unit': ''},
            },
            'accuracy_level': 'medium',
            'accuracy_desc': 'R²>0.97',
            'category': 'comprehensive',
            'is_builtin': True,
            'description': '综合考虑温度、DOD、倍率、SOC窗口等多应力因素的半经验衰减模型，适用于复杂工况下的寿命预测。',
        },
    ]


@algorithm_bp.route('/api/algorithms', methods=['GET'])
@token_required
def get_algorithms():
    """获取算法模型列表"""
    user_id = request.user_id
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    category = request.args.get('category')
    query = AlgorithmModel.query.filter_by(tenant_id=user.tenant_id, is_active=True)
    
    if category:
        query = query.filter_by(category=category)
    
    algorithms = query.order_by(AlgorithmModel.sort_order, AlgorithmModel.name).all()
    
    result = []
    for alg in algorithms:
        params = json.loads(alg.parameters) if alg.parameters else {}
        scenarios = json.loads(alg.applicable_scenarios) if alg.applicable_scenarios else []
        
        result.append({
            'id': alg.id,
            'name': alg.name,
            'name_en': alg.name_en,
            'model_type': alg.model_type,
            'applicable_scenarios': scenarios,
            'mathematical_form': alg.mathematical_form,
            'formula_expression': alg.formula_expression,
            'parameters': params,
            'accuracy_level': alg.accuracy_level,
            'accuracy_desc': alg.accuracy_desc,
            'category': alg.category,
            'is_builtin': alg.is_builtin,
            'description': alg.description,
            'created_at': alg.created_at.isoformat() if alg.created_at else None,
        })
    
    return jsonify({'success': True, 'data': result})


@algorithm_bp.route('/api/algorithms/<alg_id>', methods=['GET'])
@token_required
def get_algorithm(alg_id):
    """获取单个算法模型详情"""
    user_id = request.user_id
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    alg = AlgorithmModel.query.filter_by(id=alg_id, tenant_id=user.tenant_id, is_active=True).first()
    
    if not alg:
        return jsonify({'error': '算法模型不存在'}), 404
    
    params = json.loads(alg.parameters) if alg.parameters else {}
    scenarios = json.loads(alg.applicable_scenarios) if alg.applicable_scenarios else []
    
    return jsonify({
        'success': True,
        'data': {
            'id': alg.id,
            'name': alg.name,
            'name_en': alg.name_en,
            'model_type': alg.model_type,
            'applicable_scenarios': scenarios,
            'mathematical_form': alg.mathematical_form,
            'formula_expression': alg.formula_expression,
            'parameters': params,
            'accuracy_level': alg.accuracy_level,
            'accuracy_desc': alg.accuracy_desc,
            'category': alg.category,
            'is_builtin': alg.is_builtin,
            'description': alg.description,
            'created_at': alg.created_at.isoformat() if alg.created_at else None,
            'updated_at': alg.updated_at.isoformat() if alg.updated_at else None,
        }
    })


@algorithm_bp.route('/api/algorithms', methods=['POST'])
@token_required
def create_algorithm():
    """创建新算法模型"""
    user_id = request.user_id
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    # 检查权限（客户不能创建算法）
    if user.role == 'customer':
        return jsonify({'error': '权限不足'}), 403
    
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'error': '模型名称不能为空'}), 400
    
    model_type = data.get('model_type', 'custom')
    applicable_scenarios = data.get('applicable_scenarios', [])
    parameters = data.get('parameters', {})
    
    alg_id = str(uuid.uuid4())
    
    algorithm = AlgorithmModel(
        id=alg_id,
        tenant_id=user.tenant_id,
        name=name,
        name_en=data.get('name_en'),
        model_type=model_type,
        applicable_scenarios=json.dumps(applicable_scenarios) if isinstance(applicable_scenarios, list) else '[]',
        mathematical_form=data.get('mathematical_form'),
        formula_expression=data.get('formula_expression'),
        parameters=json.dumps(parameters) if isinstance(parameters, dict) else '{}',
        accuracy_level=data.get('accuracy_level', 'medium'),
        accuracy_desc=data.get('accuracy_desc'),
        category=data.get('category', 'custom'),
        is_builtin=False,
        is_active=True,
        sort_order=data.get('sort_order', 100),
        description=data.get('description'),
        created_by=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    
    db.session.add(algorithm)
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'id': alg_id,
            'message': '算法模型创建成功'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'创建失败: {str(e)}'}), 500


@algorithm_bp.route('/api/algorithms/<alg_id>', methods=['PUT'])
@token_required
def update_algorithm(alg_id):
    """更新算法模型"""
    user_id = request.user_id
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    # 检查权限（客户不能更新算法）
    if user.role == 'customer':
        return jsonify({'error': '权限不足'}), 403
    
    alg = AlgorithmModel.query.filter_by(id=alg_id, tenant_id=user.tenant_id).first()
    
    if not alg:
        return jsonify({'error': '算法模型不存在'}), 404
    
    # 内置模型不可修改核心属性
    if alg.is_builtin:
        return jsonify({'error': '内置算法模型不可修改'}), 403
    
    if 'name' in data:
        alg.name = data['name'].strip()
    if 'name_en' in data:
        alg.name_en = data['name_en']
    if 'model_type' in data:
        alg.model_type = data['model_type']
    if 'applicable_scenarios' in data:
        alg.applicable_scenarios = json.dumps(data['applicable_scenarios']) if isinstance(data['applicable_scenarios'], list) else '[]'
    if 'mathematical_form' in data:
        alg.mathematical_form = data['mathematical_form']
    if 'formula_expression' in data:
        alg.formula_expression = data['formula_expression']
    if 'parameters' in data:
        alg.parameters = json.dumps(data['parameters']) if isinstance(data['parameters'], dict) else '{}'
    if 'accuracy_level' in data:
        alg.accuracy_level = data['accuracy_level']
    if 'accuracy_desc' in data:
        alg.accuracy_desc = data['accuracy_desc']
    if 'category' in data:
        alg.category = data['category']
    if 'is_active' in data:
        alg.is_active = data['is_active']
    if 'sort_order' in data:
        alg.sort_order = data['sort_order']
    if 'description' in data:
        alg.description = data['description']
    
    alg.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': '算法模型更新成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新失败: {str(e)}'}), 500


@algorithm_bp.route('/api/algorithms/<alg_id>', methods=['DELETE'])
@token_required
def delete_algorithm(alg_id):
    """删除算法模型"""
    user_id = request.user_id
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    # 检查权限（客户不能删除算法）
    if user.role == 'customer':
        return jsonify({'error': '权限不足'}), 403
    
    alg = AlgorithmModel.query.filter_by(id=alg_id, tenant_id=user.tenant_id).first()
    
    if not alg:
        return jsonify({'error': '算法模型不存在'}), 404
    
    # 内置模型不可删除
    if alg.is_builtin:
        return jsonify({'error': '内置算法模型不可删除'}), 403
    
    alg.is_active = False
    alg.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': '算法模型已删除'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'删除失败: {str(e)}'}), 500


@algorithm_bp.route('/api/algorithms/initialize', methods=['POST'])
@token_required
def initialize_builtin_algorithms():
    """初始化内置算法模型"""
    user_id = request.user_id
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    # 只有管理员可以初始化
    if user.role != 'admin':
        return jsonify({'error': '权限不足，只有管理员可以初始化'}), 403
    
    builtin_algs = get_builtin_algorithms()
    count = 0
    
    for alg_data in builtin_algs:
        # 检查是否已存在
        existing = AlgorithmModel.query.filter_by(
            tenant_id=user.tenant_id,
            model_type=alg_data['model_type']
        ).first()
        
        if existing:
            continue
        
        alg_id = str(uuid.uuid4())
        
        algorithm = AlgorithmModel(
            id=alg_id,
            tenant_id=user.tenant_id,
            name=alg_data['name'],
            name_en=alg_data['name_en'],
            model_type=alg_data['model_type'],
            applicable_scenarios=json.dumps(alg_data['applicable_scenarios']),
            mathematical_form=alg_data['mathematical_form'],
            formula_expression=alg_data['formula_expression'],
            parameters=json.dumps(alg_data['parameters']),
            accuracy_level=alg_data['accuracy_level'],
            accuracy_desc=alg_data['accuracy_desc'],
            category=alg_data['category'],
            is_builtin=True,
            is_active=True,
            sort_order=count,
            description=alg_data['description'],
            created_by=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        
        db.session.add(algorithm)
        count += 1
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'count': count, 'message': f'成功初始化{count}个内置算法模型'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'初始化失败: {str(e)}'}), 500
