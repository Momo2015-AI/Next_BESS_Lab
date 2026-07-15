"""
算法模型管理服务 - 内置算法模型库与CRUD操作
"""


def get_builtin_algorithms():
    """获取内置算法模型列表（4大分类：degradation/financial/engineering/simulation）

    内置 6 种容量衰减模型（degradation），与前端 src/data/builtinAlgorithms.js 同源。
    """
    return [
        # ========== 容量衰减类 (degradation) — 6 种内置模型 ==========
        {
            "id": "builtin-arrhenius",
            "name": "阿伦尼乌斯模型 (Arrhenius)",
            "name_en": "Arrhenius Model",
            "model_type": "arrhenius",
            "applicable_scenarios": ["温度加速老化", "日历寿命预测", "高温/高倍率工况"],
            "mathematical_form": "k = A * e^(-Ea/RT)",
            "formula_expression": "params.A * Math.exp(-params.Ea * 1000 / (R * T)) * Math.pow(t + 0.5, 0.5)",
            "parameters": {
                "A": {"label": "指前因子", "default": 1e12, "min": 1e6, "max": 1e18, "unit": "/年"},
                "Ea": {"label": "活化能", "default": 35, "min": 20, "max": 80, "unit": "kJ/mol"},
                "R": {"label": "气体常数", "default": 8.314, "min": 8.0, "max": 8.5, "unit": "J/(mol·K)"},
                "T_ref": {"label": "参考温度", "default": 298, "min": 273, "max": 350, "unit": "K"},
            },
            "accuracy_level": "medium",
            "accuracy_desc": "R²>0.95",
            "category": "degradation",
            "is_builtin": True,
            "description": "基于阿伦尼乌斯化学动力学方程的温度加速老化模型。核心原理：温度每升高10°C，电化学反应速率约翻倍，老化也随之加速。指前因子（A）描述基础反应速率，活化能（Ea=35 kJ/mol）为LFP电池标准值。",
        },
        {
            "id": "builtin-double-exp",
            "name": "双指数模型 (Double Exponential)",
            "name_en": "Double Exponential Model",
            "model_type": "double_exponential",
            "applicable_scenarios": ["LFP日历衰减", "循环衰减", "综合衰减预测"],
            "mathematical_form": "SOH(t) = A·e^(-k₁t) + B·e^(-k₂t) + C",
            "formula_expression": "A * Math.exp(-k1 * t) + B * Math.exp(-k2 * t) + C",
            "parameters": {
                "A": {"label": "快速衰减幅度", "default": 0.15, "min": 0, "max": 0.5, "unit": ""},
                "B": {"label": "慢速衰减幅度", "default": 0.08, "min": 0, "max": 0.3, "unit": ""},
                "k1": {"label": "快速衰减系数", "default": 0.05, "min": 0, "max": 0.2, "unit": "/年"},
                "k2": {"label": "慢速衰减系数", "default": 0.008, "min": 0, "max": 0.05, "unit": "/年"},
                "C": {"label": "剩余容量", "default": 0.77, "min": 0.5, "max": 0.9, "unit": ""},
            },
            "accuracy_level": "high",
            "accuracy_desc": "R²>0.999",
            "category": "degradation",
            "is_builtin": True,
            "description": "适用于LFP电池的日历衰减和循环衰减。采用双指数形式描述容量衰减过程：快速衰减阶段（A项，k₁系数较大）描述SEI膜形成导致的初期快速容量损失；慢速衰减阶段（B项，k₂系数较小）描述活性物质损失导致的长期缓慢衰减。C为25年末剩余容量。行业标准：快速衰减约占15%，慢速衰减约占8%，25年末剩余约77%。适用于大规模储能电站的长期SOH预测。",
        },
        {
            "name": "线性-对数模型 (Linear-Log)",
            "name_en": "Linear-Log Model",
            "model_type": "linear_log",
            "applicable_scenarios": ["RTE衰减", "效率衰减建模"],
            "mathematical_form": "RTE(t) = RTE₀ - αt - β·ln(1+γt)",
            "formula_expression": "RTE0 - alpha * t - beta * Math.log(1 + gamma * t)",
            "parameters": {
                "RTE0": {"label": "初始RTE", "default": 0.94, "min": 0.8, "max": 0.99, "unit": ""},
                "alpha": {"label": "线性衰减系数", "default": 0.0008, "min": 0, "max": 0.005, "unit": "/年"},
                "beta": {"label": "对数衰减幅度", "default": 0.02, "min": 0, "max": 0.1, "unit": ""},
                "gamma": {"label": "对数衰减速率", "default": 0.5, "min": 0, "max": 5, "unit": "/年"},
            },
            "accuracy_level": "medium",
            "accuracy_desc": "R²>0.95",
            "category": "degradation",
            "is_builtin": True,
            "description": "适用于RTE衰减和效率衰减建模。采用线性-对数形式描述RTE随时间的变化过程：线性部分（αt）描述初期快速衰减；对数部分（β·ln(1+γt)）描述后期缓慢衰减。适用于大规模储能电站的长期RTE预测。",
        },
        {
            "id": "builtin-rainflow",
            "name": "雨流计数模型 (Rainflow)",
            "name_en": "Rainflow Counting Model",
            "model_type": "rainflow",
            "applicable_scenarios": ["不规则循环损伤", "实际运行工况", "多DOD混合工况"],
            "mathematical_form": "D = Σ(nᵢ/Nᵢ)·(DODᵢ/DOD_ref)^m",
            "formula_expression": "Math.pow(N_cycles / cycle_life_ref, damage_exponent) * Math.pow(DOD / 100 / dod_ref, 1.5)",
            "parameters": {
                "damage_exponent": {"label": "损伤指数", "default": 1.5, "min": 1.0, "max": 3.0, "unit": ""},
                "cycle_life_ref": {"label": "参考循环寿命", "default": 6000, "min": 1000, "max": 20000, "unit": "次"},
                "dod_ref": {"label": "参考DOD", "default": 1.0, "min": 0.1, "max": 1.0, "unit": ""},
            },
            "accuracy_level": "high",
            "accuracy_desc": "与实际工况高度吻合",
            "category": "degradation",
            "is_builtin": True,
            "description": "基于Miner线性损伤累积法则和雨流计数法的循环寿命预测模型。将实际运行中不规则、变幅的充放电循环统计为等效标准循环次数，按DOD加权计算累积损伤。参考循环寿命（6000次）为LFP电池在100%DOD、25°C下的行业标准值。",
        },
        {
            "id": "builtin-semi-empirical",
            "name": "半经验综合模型 (Semi-Empirical)",
            "name_en": "Semi-Empirical Comprehensive Model",
            "model_type": "semi_empirical",
            "applicable_scenarios": ["多应力耦合", "综合衰减", "复杂工况预测"],
            "mathematical_form": "SOH = f(T)·f(DOD)·f(C-rate)·f(SOC)",
            "formula_expression": "1 - (1 - temp_factor * dod_factor * c_rate_factor * soc_factor) * t / 25",
            "parameters": {
                "temp_coeff": {"label": "温度系数", "default": 0.002, "min": 0, "max": 0.01, "unit": "/°C"},
                "dod_coeff": {"label": "DOD系数", "default": 0.5, "min": 0, "max": 2.0, "unit": ""},
                "c_rate_coeff": {"label": "倍率系数", "default": 0.1, "min": 0, "max": 1.0, "unit": ""},
                "soc_coeff": {"label": "SOC窗口系数", "default": 0.3, "min": 0, "max": 1.0, "unit": ""},
            },
            "accuracy_level": "medium",
            "accuracy_desc": "R²>0.97",
            "category": "degradation",
            "is_builtin": True,
            "description": "综合考虑温度、DOD、C-rate、SOC窗口四大应力因素的半经验综合衰减模型。温度每偏离25°C 1°C，衰减速率变化0.2%；DOD从50%升至100%时衰减速率翻倍；0.5C充电相比1C充电衰减减半。",
        },
        {
            "id": "builtin-hybrid",
            "name": "默认混合模型 (Default Hybrid)",
            "name_en": "Default Hybrid Model",
            "model_type": "arrhenius_hybrid",
            "applicable_scenarios": ["通用默认", "快速评估", "无详细数据时使用"],
            "mathematical_form": "基于Arrhenius方程的综合混合模型",
            "formula_expression": "A_cal * Math.exp(-Ea_cal * 1000 / (R * T)) * Math.pow(t + 0.5, alpha)",
            "parameters": {
                "A_cal": {"label": "日历老化因子", "default": 0.001, "min": 0.0001, "max": 0.01, "unit": ""},
                "Ea_cal": {"label": "日历活化能", "default": 35, "min": 20, "max": 60, "unit": "kJ/mol"},
                "alpha": {"label": "时间指数", "default": 0.5, "min": 0.3, "max": 0.7, "unit": ""},
                "A_cyc": {"label": "循环老化因子", "default": 0.00001, "min": 1e-7, "max": 1e-4, "unit": ""},
                "Ea_cyc": {"label": "循环活化能", "default": 25, "min": 15, "max": 50, "unit": "kJ/mol"},
                "beta": {"label": "循环指数", "default": 0.7, "min": 0.5, "max": 0.9, "unit": ""},
            },
            "accuracy_level": "medium",
            "accuracy_desc": "通用默认模型，适用广泛",
            "category": "degradation",
            "is_builtin": True,
            "description": "通用默认混合衰减模型，基于Arrhenius框架同时处理日历老化和循环老化。日历老化因子（A_cal=0.001）和循环老化因子（A_cyc=1e-5）分别为两个老化路径的基础速率。参数参考多款主流LFP电芯公开数据平均值。",
        },
    ]


def seed_algorithms():
    """初始化内置算法模型种子数据（由调用方处理DB）"""
    pass
