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

# ==================== 内置算法模型列表 ====================

def get_builtin_algorithms():
    """获取内置算法模型列表（4大分类：degradation/financial/engineering/simulation）"""
    return [
        # ========== 容量衰减类 (degradation) ==========
        {
            'name': '双指数模型 (Double Exponential)',
            'name_en': 'Double Exponential Model',
            'model_type': 'double_exponential',
            'applicable_scenarios': ['LFP日历衰减', '循环衰减', '综合衰减预测'],
            'mathematical_form': 'SOH(t) = A·e^(-k₁t) + B·e^(-k₂t) + C',
            'formula_expression': 'A * Math.exp(-k1 * t) + B * Math.exp(-k2 * t) + C',
            'parameters': {
                'A': {'label': '快速衰减幅度', 'default': 0.15, 'min': 0, 'max': 0.5, 'unit': ''},
                'B': {'label': '慢速衰减幅度', 'default': 0.08, 'min': 0, 'max': 0.3, 'unit': ''},
                'k1': {'label': '快速衰减系数', 'default': 0.05, 'min': 0, 'max': 0.2, 'unit': '/年'},
                'k2': {'label': '慢速衰减系数', 'default': 0.008, 'min': 0, 'max': 0.05, 'unit': '/年'},
                'C': {'label': '剩余容量', 'default': 0.77, 'min': 0.5, 'max': 0.9, 'unit': ''},
            },
            'accuracy_level': 'high',
            'accuracy_desc': 'R²>0.999',
            'category': 'degradation',
            'is_builtin': True,
            'description': '适用于LFP电池的日历衰减和循环衰减。采用双指数形式描述容量衰减过程：快速衰减阶段（A项，k₁系数较大）描述SEI膜形成导致的初期快速容量损失；慢速衰减阶段（B项，k₂系数较小）描述活性物质损失导致的长期缓慢衰减。C为25年末剩余容量。行业标准：快速衰减约占15%，慢速衰减约占8%，25年末剩余约77%。适用于大规模储能电站的长期SOH预测。',
        },
        {
            'name': '线性-对数模型 (Linear-Log)',
            'name_en': 'Linear-Log Model',
            'model_type': 'linear_log',
            'applicable_scenarios': ['RTE衰减', '效率衰减建模'],
            'mathematical_form': 'RTE(t) = RTE₀ - αt - β·ln(1+γt)',
            'formula_expression': 'RTE0 - alpha * t - beta * Math.log(1 + gamma * t)',
            'parameters': {
                'RTE0': {'label': '初始RTE', 'default': 0.94, 'min': 0.8, 'max': 0.99, 'unit': ''},
                'alpha': {'label': '线性衰减系数', 'default': 0.0008, 'min': 0, 'max': 0.005, 'unit': '/年'},
                'beta': {'label': '对数衰减幅度', 'default': 0.02, 'min': 0, 'max': 0.1, 'unit': ''},
                'gamma': {'label': '对数衰减速率', 'default': 0.5, 'min': 0, 'max': 5, 'unit': '/年'},
            },
            'accuracy_level': 'medium',
            'accuracy_desc': 'R²>0.95',
            'category': 'degradation',
            'is_builtin': True,
            'description': '适用于RTE衰减和效率衰减建模。采用线性-对数形式描述RTE随时间的变化过程：线性部分（αt）描述初期快速衰减；对数部分（β·ln(1+γt)）描述后期缓慢衰减。适用于大规模储能电站的长期RTE预测。',
        }
        # 其他算法模型省略
    ]


def seed_algorithms():
    """初始化内置算法模型种子数据"""
    pass


# ==================== API 路由 ====================

@algorithm_bp.route('/api/algorithm/builtin_models', methods=['GET'])
def get_builtin_models_api():
    models = get_builtin_algorithms()
    return jsonify({'success': True, 'data': models})

@algorithm_bp.route('/api/algorithm/register', methods=['POST'])
@token_required
def register_algorithm_api():
    data = request.get_json()
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
    
    new_model = {
        'name': data.get('name'),
        'name_en': data.get('name_en'),
        'model_type': data.get('model_type'),
        'applicable_scenarios': data.get('applicable_scenarios', []),
        'mathematical_form': data.get('mathematical_form'),
        'formula_expression': data.get('formula_expression'),
        'parameters': data.get('parameters', {}),
        'accuracy_level': data.get('accuracy_level', 'unknown'),
        'accuracy_desc': data.get('accuracy_desc', ''),
        'category': data.get('category', 'other'),
        'is_builtin': False,
        'description': data.get('description', '')
    }
    
    # 将新模型保存到数据库
    new_algorithm = AlgorithmModel(**new_model)
    db.session.add(new_algorithm)
    db.session.commit()
    
    return jsonify({'success': True, 'registered_model': new_model}), 201

@algorithm_bp.route('/api/algorithm/update/<model_id>', methods=['PUT'])
@token_required
def update_algorithm_api(model_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
    
    algorithm = AlgorithmModel.query.get(model_id)
    if not algorithm:
        return jsonify({'error': '算法模型不存在'}), 404
    
    for key, value in data.items():
        setattr(algorithm, key, value)
    
    db.session.commit()
    
    return jsonify({'success': True, 'updated_model': algorithm.to_dict()}), 200

@algorithm_bp.route('/api/algorithm/delete/<model_id>', methods=['DELETE'])
@token_required
def delete_algorithm_api(model_id):
    algorithm = AlgorithmModel.query.get(model_id)
    if not algorithm:
        return jsonify({'error': '算法模型不存在'}), 404
    
    db.session.delete(algorithm)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '算法模型已删除'}), 200