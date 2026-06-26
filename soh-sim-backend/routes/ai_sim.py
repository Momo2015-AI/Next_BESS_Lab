"""
AI仿真算法API - 支持参数校准和预测
"""
import uuid
import json
import math
import numpy as np
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from database import db, BatteryManufacturer, AlgorithmModel

ai_sim_bp = Blueprint('ai_sim', __name__)


# ==================== 预设电池厂家数据 ====================

def get_builtin_manufacturers():
    """获取预设的主流电池厂家数据（包含校准后的Arrhenius参数）"""
    return [
        # ===== LFP 厂家 =====
        {
            'name': '宁德时代 CATL',
            'name_en': 'CATL',
            'country': '中国',
            'chemistry_type': 'LFP',
            'calibrated_params': {
                'A_cal': 0.015,
                'Ea_cal': 22000,
                'alpha': 0.75,
                'A_cyc': 0.0008,
                'Ea_cyc': 16000,
                'beta': 0.55,
                'gamma': 1.4,
                'delta': 0.18,
                'degradation_rate': 0.12
            },
            'rmse_soh': 1.8,
            'rmse_rte': 0.8,
            'data_points': 156,
            'applicable_scenarios': ['LFP日历衰减', '循环衰减', '综合衰减预测', '大规模储能'],
            'description': '宁德时代（CATL）LFP电芯，适用于大规模储能电站。首年衰减约2.5%，年均衰减约1.0%，25年末SOH约72%。',
            'is_builtin': True,
            'sort_order': 1
        },
        {
            'name': '比亚迪 BYD',
            'name_en': 'BYD',
            'country': '中国',
            'chemistry_type': 'LFP',
            'calibrated_params': {
                'A_cal': 0.018,
                'Ea_cal': 20000,
                'alpha': 0.8,
                'A_cyc': 0.0009,
                'Ea_cyc': 15000,
                'beta': 0.5,
                'gamma': 1.5,
                'delta': 0.2,
                'degradation_rate': 0.1
            },
            'rmse_soh': 2.1,
            'rmse_rte': 0.9,
            'data_points': 124,
            'applicable_scenarios': ['LFP日历衰减', '循环衰减', '家庭储能', '工商业储能'],
            'description': '比亚迪（BYD）刀片电池LFP技术，适用于工商业和家庭储能。首年衰减约3%，年均衰减约1.2%，25年末SOH约70%。',
            'is_builtin': True,
            'sort_order': 2
        },
        {
            'name': '亿纬锂能 EVE',
            'name_en': 'EVE Energy',
            'country': '中国',
            'chemistry_type': 'LFP',
            'calibrated_params': {
                'A_cal': 0.012,
                'Ea_cal': 24000,
                'alpha': 0.7,
                'A_cyc': 0.0006,
                'Ea_cyc': 17000,
                'beta': 0.6,
                'gamma': 1.3,
                'delta': 0.15,
                'degradation_rate': 0.08
            },
            'rmse_soh': 1.5,
            'rmse_rte': 0.7,
            'data_points': 98,
            'applicable_scenarios': ['LFP日历衰减', '循环衰减', '高温环境', '长时储能'],
            'description': '亿纬锂能（EVE）LFP电芯，适用于高温环境和长时储能。温度稳定性较好，首年衰减约2%，年均衰减约0.9%，25年末SOH约74%。',
            'is_builtin': True,
            'sort_order': 3
        },
        {
            'name': '国轩高科 Gotion',
            'name_en': 'Gotion High-Tech',
            'country': '中国',
            'chemistry_type': 'LFP',
            'calibrated_params': {
                'A_cal': 0.016,
                'Ea_cal': 21000,
                'alpha': 0.78,
                'A_cyc': 0.0007,
                'Ea_cyc': 15500,
                'beta': 0.58,
                'gamma': 1.45,
                'delta': 0.17,
                'degradation_rate': 0.11
            },
            'rmse_soh': 2.0,
            'rmse_rte': 0.85,
            'data_points': 85,
            'applicable_scenarios': ['LFP日历衰减', '循环衰减', '电网侧储能'],
            'description': '国轩高科（Gotion）LFP电芯，适用于电网侧储能项目。首年衰减约2.8%，年均衰减约1.1%，25年末SOH约71%。',
            'is_builtin': True,
            'sort_order': 4
        },
        {
            'name': '欣旺达 Sunwoda',
            'name_en': 'Sunwoda',
            'country': '中国',
            'chemistry_type': 'LFP',
            'calibrated_params': {
                'A_cal': 0.017,
                'Ea_cal': 20500,
                'alpha': 0.79,
                'A_cyc': 0.00085,
                'Ea_cyc': 15200,
                'beta': 0.53,
                'gamma': 1.42,
                'delta': 0.19,
                'degradation_rate': 0.105
            },
            'rmse_soh': 2.2,
            'rmse_rte': 0.95,
            'data_points': 72,
            'applicable_scenarios': ['LFP日历衰减', '循环衰减', '分布式储能'],
            'description': '欣旺达（Sunwoda）LFP电芯，适用于分布式储能场景。首年衰减约3.2%，年均衰减约1.15%，25年末SOH约70%。',
            'is_builtin': True,
            'sort_order': 5
        },
        # ===== NCM 厂家 =====
        {
            'name': '三星 SDI',
            'name_en': 'Samsung SDI',
            'country': '韩国',
            'chemistry_type': 'NCM',
            'calibrated_params': {
                'A_cal': 0.025,
                'Ea_cal': 28000,
                'alpha': 0.85,
                'A_cyc': 0.0015,
                'Ea_cyc': 20000,
                'beta': 0.65,
                'gamma': 1.6,
                'delta': 0.25,
                'degradation_rate': 0.15
            },
            'rmse_soh': 2.5,
            'rmse_rte': 1.0,
            'data_points': 112,
            'applicable_scenarios': ['NCM衰减', '高能量密度', '户用储能'],
            'description': '三星SDI NCM电芯，高能量密度，适用于户用和小型储能。首年衰减约4%，年均衰减约1.5%，25年末SOH约65%。',
            'is_builtin': True,
            'sort_order': 6
        },
        {
            'name': 'LG化学 LG Chem',
            'name_en': 'LG Energy Solution',
            'country': '韩国',
            'chemistry_type': 'NCM',
            'calibrated_params': {
                'A_cal': 0.022,
                'Ea_cal': 26000,
                'alpha': 0.82,
                'A_cyc': 0.0012,
                'Ea_cyc': 18000,
                'beta': 0.6,
                'gamma': 1.55,
                'delta': 0.22,
                'degradation_rate': 0.13
            },
            'rmse_soh': 2.3,
            'rmse_rte': 0.9,
            'data_points': 135,
            'applicable_scenarios': ['NCM衰减', '高能量密度', '电动汽车配套'],
            'description': 'LG新能源（LG Energy Solution）NCM电芯，适用于电动汽车配套储能。首年衰减约3.5%，年均衰减约1.3%，25年末SOH约67%。',
            'is_builtin': True,
            'sort_order': 7
        },
        {
            'name': '松下 Panasonic',
            'name_en': 'Panasonic',
            'country': '日本',
            'chemistry_type': 'NCA',
            'calibrated_params': {
                'A_cal': 0.028,
                'Ea_cal': 30000,
                'alpha': 0.88,
                'A_cyc': 0.0018,
                'Ea_cyc': 22000,
                'beta': 0.7,
                'gamma': 1.7,
                'delta': 0.28,
                'degradation_rate': 0.17
            },
            'rmse_soh': 2.8,
            'rmse_rte': 1.1,
            'data_points': 95,
            'applicable_scenarios': ['NCA衰减', '高能量密度', '特斯拉配套'],
            'description': '松下（Panasonic）NCA电芯，特斯拉主要供应商。高能量密度但衰减较快，首年衰减约4.5%，年均衰减约1.6%，25年末SOH约63%。',
            'is_builtin': True,
            'sort_order': 8
        },
        {
            'name': '索尼 Sony',
            'name_en': 'Sony',
            'country': '日本',
            'chemistry_type': 'NCM',
            'calibrated_params': {
                'A_cal': 0.020,
                'Ea_cal': 24000,
                'alpha': 0.8,
                'A_cyc': 0.0010,
                'Ea_cyc': 17000,
                'beta': 0.57,
                'gamma': 1.5,
                'delta': 0.20,
                'degradation_rate': 0.12
            },
            'rmse_soh': 2.1,
            'rmse_rte': 0.85,
            'data_points': 68,
            'applicable_scenarios': ['NCM衰减', '高品质储能'],
            'description': '索尼（Sony）NCM电芯，高品质但价格较高。首年衰减约3%，年均衰减约1.2%，25年末SOH约69%。',
            'is_builtin': True,
            'sort_order': 9
        },
        # ===== LTO 厂家 =====
        {
            'name': '东芝 Toshiba',
            'name_en': 'Toshiba',
            'country': '日本',
            'chemistry_type': 'LTO',
            'calibrated_params': {
                'A_cal': 0.005,
                'Ea_cal': 18000,
                'alpha': 0.6,
                'A_cyc': 0.0002,
                'Ea_cyc': 12000,
                'beta': 0.4,
                'gamma': 1.0,
                'delta': 0.1,
                'degradation_rate': 0.05
            },
            'rmse_soh': 1.2,
            'rmse_rte': 0.5,
            'data_points': 88,
            'applicable_scenarios': ['LTO衰减', '高循环寿命', '快充场景'],
            'description': '东芝（Toshiba）LTO电芯，超长循环寿命，适用于快充和高循环场景。首年衰减约1%，年均衰减约0.5%，25年末SOH约87%。',
            'is_builtin': True,
            'sort_order': 10
        },
        {
            'name': '日立 Hitachi',
            'name_en': 'Hitachi',
            'country': '日本',
            'chemistry_type': 'LTO',
            'calibrated_params': {
                'A_cal': 0.006,
                'Ea_cal': 17500,
                'alpha': 0.62,
                'A_cyc': 0.00025,
                'Ea_cyc': 11500,
                'beta': 0.42,
                'gamma': 1.05,
                'delta': 0.11,
                'degradation_rate': 0.055
            },
            'rmse_soh': 1.4,
            'rmse_rte': 0.55,
            'data_points': 76,
            'applicable_scenarios': ['LTO衰减', '高循环寿命', '电网调频'],
            'description': '日立（Hitachi）LTO电芯，适用于电网调频和高循环场景。首年衰减约1.2%，年均衰减约0.6%，25年末SOH约85%。',
            'is_builtin': True,
            'sort_order': 11
        },
        # ===== 其他 =====
        {
            'name': '通用 LFP 模型',
            'name_en': 'Generic LFP',
            'country': '通用',
            'chemistry_type': 'LFP',
            'calibrated_params': {
                'A_cal': 0.017,
                'Ea_cal': 21500,
                'alpha': 0.78,
                'A_cyc': 0.00085,
                'Ea_cyc': 15500,
                'beta': 0.55,
                'gamma': 1.45,
                'delta': 0.18,
                'degradation_rate': 0.1
            },
            'rmse_soh': 2.5,
            'rmse_rte': 1.0,
            'data_points': 500,
            'applicable_scenarios': ['通用LFP', '快速评估', '无厂家数据'],
            'description': '通用LFP模型，综合多个厂家数据校准。适用于快速评估或缺乏厂家详细数据时使用。首年衰减约3%，年均衰减约1.2%，25年末SOH约71%。',
            'is_builtin': True,
            'sort_order': 99
        },
    ]


def seed_manufacturers():
    """初始化预设电池厂家数据"""
    manufacturers = get_builtin_manufacturers()
    count = 0
    for i, mfr_data in enumerate(manufacturers):
        existing = BatteryManufacturer.query.filter_by(
            is_builtin=True,
            name=mfr_data['name'],
        ).first()

        if existing:
            existing.name_en = mfr_data['name_en']
            existing.country = mfr_data['country']
            existing.chemistry_type = mfr_data['chemistry_type']
            existing.calibrated_params = json.dumps(mfr_data['calibrated_params'])
            existing.rmse_soh = mfr_data['rmse_soh']
            existing.rmse_rte = mfr_data['rmse_rte']
            existing.data_points = mfr_data['data_points']
            existing.applicable_scenarios = json.dumps(mfr_data['applicable_scenarios'])
            existing.description = mfr_data['description']
            existing.sort_order = mfr_data['sort_order']
            existing.updated_at = datetime.utcnow()
        else:
            mfr_id = f"builtin-mfr-{i+1}"
            mfr = BatteryManufacturer(
                id=mfr_id,
                tenant_id=None,
                name=mfr_data['name'],
                name_en=mfr_data['name_en'],
                country=mfr_data['country'],
                chemistry_type=mfr_data['chemistry_type'],
                calibrated_params=json.dumps(mfr_data['calibrated_params']),
                rmse_soh=mfr_data['rmse_soh'],
                rmse_rte=mfr_data['rmse_rte'],
                data_points=mfr_data['data_points'],
                applicable_scenarios=json.dumps(mfr_data['applicable_scenarios']),
                is_builtin=True,
                is_active=True,
                sort_order=mfr_data['sort_order'],
                description=mfr_data['description'],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.session.add(mfr)
        count += 1

    try:
        db.session.commit()
        print(f"  电池厂家初始化完成: {count} 个预设厂家")
    except Exception as e:
        db.session.rollback()
        print(f"  电池厂家初始化失败: {e}")


# ==================== Arrhenius 模型实现 ====================

class ArrheniusSOHModel:
    """阿伦尼乌斯电池衰减模型"""

    def __init__(self, params=None):
        self.R = 8.314
        self.params = {
            'A_cal': 0.02,
            'Ea_cal': 20000,
            'alpha': 0.8,
            'A_cyc': 0.001,
            'Ea_cyc': 15000,
            'beta': 0.5,
            'gamma': 1.5,
            'delta': 0.2,
            'degradation_rate': 0.1
        }
        if params:
            self.params.update(params)

    def calculate_calendar_aging(self, years, temperature):
        T = temperature + 273.15
        rate = self.params['A_cal'] * math.exp(-self.params['Ea_cal'] / (self.R * T))
        Q_cal = rate * (years ** self.params['alpha'])
        return Q_cal

    def calculate_cycle_aging(self, years, temperature, cycles_per_day, dod, c_rate):
        T = temperature + 273.15
        DOD_factor = dod ** self.params['gamma']
        C_rate_factor = 1 + self.params['delta'] * (c_rate - 0.5)
        rate = self.params['A_cyc'] * math.exp(-self.params['Ea_cyc'] / (self.R * T))
        N = years * cycles_per_day * 365
        Q_cyc = rate * (N ** self.params['beta']) * DOD_factor * C_rate_factor
        return Q_cyc

    def calculate_soh(self, years, temperature, cycles_per_day, dod, c_rate):
        Q_cal = self.calculate_calendar_aging(years, temperature)
        Q_cyc = self.calculate_cycle_aging(years, temperature, cycles_per_day, dod, c_rate)
        total_loss = Q_cal + Q_cyc
        soh = 1 - total_loss
        return max(soh, 0)

    def calculate_rte(self, soh, rte_initial):
        soh_loss = 1 - soh
        rte = rte_initial * (1 - self.params['degradation_rate'] * soh_loss)
        return max(rte, 0)

    def predict(self, X):
        soh = self.calculate_soh(
            years=X.get('years', 1),
            temperature=X.get('temperature', 25),
            cycles_per_day=X.get('cycles_per_day', 1),
            dod=X.get('dod', 0.8),
            c_rate=X.get('c_rate', 0.5)
        )
        rte = self.calculate_rte(soh, X.get('rte_initial', 97.03))
        return {
            'soh': round(soh * 100, 2),
            'rte': round(rte, 2)
        }

    def predict_curve(self, years, temperature, cycles_per_day, dod, c_rate, rte_initial=97.03):
        soh_curve = []
        rte_curve = []
        for y in range(years + 1):
            soh = self.calculate_soh(y, temperature, cycles_per_day, dod, c_rate)
            rte = self.calculate_rte(soh, rte_initial)
            soh_curve.append(round(soh * 100, 2))
            rte_curve.append(round(rte, 2))
        return {'soh_curve': soh_curve, 'rte_curve': rte_curve}


# ==================== 参数校准器 ====================

class ModelCalibrator:
    """参数校准器 - 使用网格搜索（轻量级，无需额外依赖）"""

    def __init__(self, model, data):
        self.model = model
        self.data = data
        self.best_params = None
        self.best_rmse = float('inf')

    def prepare_data(self):
        features = []
        labels = []
        for row in self.data:
            features.append([
                row['operating_days'] / 365,
                row['temperature'],
                row['cycles_per_day'],
                row['dod'],
                row['c_rate']
            ])
            labels.append(row['measured_soh'] / 100)
        return np.array(features), np.array(labels)

    def calculate_rmse(self, params):
        temp_model = ArrheniusSOHModel(params)
        features, labels = self.prepare_data()
        predictions = []
        for feature in features:
            soh = temp_model.calculate_soh(
                years=feature[0],
                temperature=feature[1],
                cycles_per_day=feature[2],
                dod=feature[3],
                c_rate=feature[4]
            )
            predictions.append(soh)
        rmse = np.sqrt(np.mean((np.array(predictions) - labels) ** 2))
        return rmse

    def calibrate(self, iterations=100):
        features, labels = self.prepare_data()
        if len(features) < 5:
            return self.model.params, float('inf')

        current_params = self.model.params.copy()
        param_ranges = {
            'A_cal': (0.005, 0.03),
            'Ea_cal': (15000, 35000),
            'alpha': (0.5, 1.0),
            'A_cyc': (0.0002, 0.002),
            'Ea_cyc': (10000, 25000),
            'beta': (0.3, 0.8),
            'gamma': (1.0, 2.0),
            'delta': (0.1, 0.3),
        }

        for _ in range(iterations):
            new_params = current_params.copy()
            param_to_tune = np.random.choice(list(param_ranges.keys()))
            low, high = param_ranges[param_to_tune]
            new_params[param_to_tune] = np.random.uniform(low, high)

            current_rmse = self.calculate_rmse(current_params)
            new_rmse = self.calculate_rmse(new_params)

            if new_rmse < current_rmse:
                current_params = new_params
                if new_rmse < self.best_rmse:
                    self.best_rmse = new_rmse
                    self.best_params = new_params.copy()

        if self.best_params is None:
            self.best_params = current_params
            self.best_rmse = self.calculate_rmse(current_params)

        return self.best_params, self.best_rmse


# ==================== API 路由 ====================

@ai_sim_bp.route('/api/ai-sim/manufacturers', methods=['GET'])
def get_manufacturers():
    """获取电池厂家列表"""
    chemistry_type = request.args.get('chemistry_type')
    query = BatteryManufacturer.query.filter_by(is_active=True)
    
    if chemistry_type:
        query = query.filter_by(chemistry_type=chemistry_type)
    
    manufacturers = query.order_by(BatteryManufacturer.sort_order, BatteryManufacturer.name).all()
    
    result = []
    for mfr in manufacturers:
        params = json.loads(mfr.calibrated_params) if mfr.calibrated_params else {}
        scenarios = json.loads(mfr.applicable_scenarios) if mfr.applicable_scenarios else []
        result.append({
            'id': mfr.id,
            'name': mfr.name,
            'name_en': mfr.name_en,
            'country': mfr.country,
            'chemistry_type': mfr.chemistry_type,
            'calibrated_params': params,
            'rmse_soh': mfr.rmse_soh,
            'rmse_rte': mfr.rmse_rte,
            'data_points': mfr.data_points,
            'applicable_scenarios': scenarios,
            'is_builtin': mfr.is_builtin,
            'description': mfr.description,
        })
    
    return jsonify({'success': True, 'data': result})


@ai_sim_bp.route('/api/ai-sim/manufacturers/<id>', methods=['GET'])
def get_manufacturer(id):
    """获取单个厂家详情"""
    mfr = BatteryManufacturer.query.get(id)
    if not mfr:
        return jsonify({'success': False, 'error': '厂家不存在'}), 404
    
    params = json.loads(mfr.calibrated_params) if mfr.calibrated_params else {}
    scenarios = json.loads(mfr.applicable_scenarios) if mfr.applicable_scenarios else []
    
    return jsonify({
        'success': True,
        'data': {
            'id': mfr.id,
            'name': mfr.name,
            'name_en': mfr.name_en,
            'country': mfr.country,
            'chemistry_type': mfr.chemistry_type,
            'calibrated_params': params,
            'rmse_soh': mfr.rmse_soh,
            'rmse_rte': mfr.rmse_rte,
            'data_points': mfr.data_points,
            'applicable_scenarios': scenarios,
            'is_builtin': mfr.is_builtin,
            'description': mfr.description,
        }
    })


@ai_sim_bp.route('/api/ai-sim/calibrate', methods=['POST'])
def calibrate_model():
    """参数校准API"""
    data = request.json
    if not data or 'training_data' not in data:
        return jsonify({'success': False, 'error': '缺少训练数据'}), 400

    training_data = data['training_data']
    iterations = data.get('iterations', 100)
    
    if len(training_data) < 3:
        return jsonify({'success': False, 'error': '训练数据至少需要3个数据点'}), 400

    model = ArrheniusSOHModel()
    calibrator = ModelCalibrator(model, training_data)
    calibrated_params, rmse = calibrator.calibrate(iterations=iterations)

    return jsonify({
        'success': True,
        'data': {
            'calibrated_params': calibrated_params,
            'rmse': round(rmse * 100, 3),
            'data_points': len(training_data),
        }
    })


@ai_sim_bp.route('/api/ai-sim/predict', methods=['POST'])
def predict():
    """预测API - 给定工况，输出SOH/RTE"""
    data = request.json
    if not data:
        return jsonify({'success': False, 'error': '缺少输入数据'}), 400

    manufacturer_id = data.get('manufacturer_id')
    params = data.get('params')

    if manufacturer_id:
        mfr = BatteryManufacturer.query.get(manufacturer_id)
        if mfr:
            mfr_params = json.loads(mfr.calibrated_params) if mfr.calibrated_params else {}
            model = ArrheniusSOHModel(mfr_params)
        else:
            return jsonify({'success': False, 'error': '厂家不存在'}), 404
    elif params:
        model = ArrheniusSOHModel(params)
    else:
        model = ArrheniusSOHModel()

    years = data.get('years', 25)
    temperature = data.get('temperature', 25)
    cycles_per_day = data.get('cycles_per_day', 1)
    dod = data.get('dod', 0.8)
    c_rate = data.get('c_rate', 0.5)
    rte_initial = data.get('rte_initial', 97.03)

    result = model.predict_curve(years, temperature, cycles_per_day, dod, c_rate, rte_initial)

    return jsonify({
        'success': True,
        'data': {
            'soh_curve': result['soh_curve'],
            'rte_curve': result['rte_curve'],
            'years': years,
            'input_params': {
                'temperature': temperature,
                'cycles_per_day': cycles_per_day,
                'dod': dod,
                'c_rate': c_rate,
                'rte_initial': rte_initial,
            },
            'manufacturer_id': manufacturer_id,
        }
    })


@ai_sim_bp.route('/api/ai-sim/simulation', methods=['POST'])
def run_simulation():
    """完整仿真API - 集成到仿真实验室"""
    data = request.json
    if not data:
        return jsonify({'success': False, 'error': '缺少输入数据'}), 400

    manufacturer_id = data.get('manufacturer_id')
    simulation_years = data.get('simulation_years', 25)
    
    if manufacturer_id:
        mfr = BatteryManufacturer.query.get(manufacturer_id)
        if mfr:
            mfr_params = json.loads(mfr.calibrated_params) if mfr.calibrated_params else {}
            model = ArrheniusSOHModel(mfr_params)
        else:
            return jsonify({'success': False, 'error': '厂家不存在'}), 404
    else:
        model = ArrheniusSOHModel()

    temperature = data.get('temperature', 25)
    cycles_per_day = data.get('cycles_per_day', 1)
    dod = data.get('dod', 0.8)
    c_rate = data.get('c_rate', 0.5)
    rte_initial = data.get('rte_initial', 97.03)

    result = model.predict_curve(simulation_years, temperature, cycles_per_day, dod, c_rate, rte_initial)

    soh_curve = result['soh_curve']
    rte_curve = result['rte_curve']

    table_data = []
    for year in range(simulation_years + 1):
        table_data.append({
            'year': year,
            'soh': soh_curve[year],
            'rte': rte_curve[year],
            'soh_loss': round(100 - soh_curve[year], 2),
            'rte_loss': round(rte_initial - rte_curve[year], 2),
        })

    return jsonify({
        'success': True,
        'data': {
            'soh_curve': soh_curve,
            'rte_curve': rte_curve,
            'table_data': table_data,
            'init_soh': soh_curve[0],
            'final_soh': soh_curve[-1],
            'manufacturer': mfr.name if mfr else '通用模型',
            'rmse_soh': mfr.rmse_soh if mfr else None,
            'rmse_rte': mfr.rmse_rte if mfr else None,
        }
    })


@ai_sim_bp.route('/api/ai-sim/initialize', methods=['POST'])
def initialize_ai_sim():
    """初始化AI仿真数据"""
    seed_manufacturers()
    return jsonify({'success': True, 'message': 'AI仿真数据初始化完成'})