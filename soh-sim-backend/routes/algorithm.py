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
            'accuracy_level': 'high',
            'accuracy_desc': 'R²>0.99',
            'category': 'degradation',
            'is_builtin': True,
            'description': '适用于储能系统RTE（往返效率）衰减建模。线性项（αt）描述设备老化导致的效率线性下降；对数项（β·ln(1+γt)）描述效率下降随时间的减缓趋势——初期衰减快，后期趋于平稳。行业标准：初始RTE约94%，年线性衰减约0.08%，对数衰减幅度约2%。适合液冷系统在25°C标准工况下的效率衰减预测。',
        },
        {
            'name': '阿伦尼乌斯模型 (Arrhenius)',
            'name_en': 'Arrhenius Model',
            'model_type': 'arrhenius',
            'applicable_scenarios': ['温度加速老化', '日历寿命预测', '高温/高倍率工况'],
            'mathematical_form': 'k = A·e^(-Ea/RT)',
            'formula_expression': 'params.A * Math.exp(-params.Ea * 1000 / (R * T)) * Math.pow(t + 0.5, 0.5)',
            'parameters': {
                'A': {'label': '指前因子', 'default': 1e12, 'min': 1e6, 'max': 1e18, 'unit': '/年'},
                'Ea': {'label': '活化能', 'default': 35, 'min': 20, 'max': 80, 'unit': 'kJ/mol'},
                'R': {'label': '气体常数', 'default': 8.314, 'min': 8.0, 'max': 8.5, 'unit': 'J/(mol·K)'},
                'T_ref': {'label': '参考温度', 'default': 298, 'min': 273, 'max': 350, 'unit': 'K'},
            },
            'accuracy_level': 'medium',
            'accuracy_desc': 'R²>0.95',
            'category': 'degradation',
            'is_builtin': True,
            'description': '基于阿伦尼乌斯化学动力学方程的温度加速老化模型。核心原理：温度每升高10°C，电化学反应速率约翻倍，老化也随之加速。指前因子（A）描述基础反应速率，活化能（Ea=35 kJ/mol）为LFP电池标准值。适用场景：高温环境（如中东地区户外50°C+）或高倍率充放电工况下的日历寿命加速预测。注意：该模型不直接处理循环老化，需结合循环项。',
        },
        {
            'name': '雨流计数模型 (Rainflow)',
            'name_en': 'Rainflow Counting Model',
            'model_type': 'rainflow',
            'applicable_scenarios': ['不规则循环损伤', '实际运行工况', '多DOD混合工况'],
            'mathematical_form': 'D = Σ(n_i/N_i) · (DOD_i/DOD_ref)^m',
            'formula_expression': 'Math.pow(N_cycles / cycle_life_ref, damage_exponent) * Math.pow(DOD / 100 / dod_ref, 1.5)',
            'parameters': {
                'damage_exponent': {'label': '损伤指数', 'default': 1.5, 'min': 1.0, 'max': 3.0, 'unit': ''},
                'cycle_life_ref': {'label': '参考循环寿命', 'default': 6000, 'min': 1000, 'max': 20000, 'unit': '次'},
                'dod_ref': {'label': '参考DOD', 'default': 1.0, 'min': 0.1, 'max': 1.0, 'unit': ''},
            },
            'accuracy_level': 'high',
            'accuracy_desc': '与实际工况高度吻合',
            'category': 'degradation',
            'is_builtin': True,
            'description': '基于Miner线性损伤累积法则和雨流计数法的循环寿命预测模型。核心原理：将实际运行中不规则、变幅的充放电循环统计为等效标准循环次数，再按DOD加权计算累积损伤。损伤指数（1.5）描述循环损伤的非线性叠加效应——大DOD循环的损伤远高于小DOD循环。参考循环寿命（6000次）为LFP电池在100%DOD、25°C下的行业标准值。适合存在日间调频+晚间调峰等多DOD混合工况的场景。',
        },
        {
            'name': '半经验综合模型 (Semi-Empirical)',
            'name_en': 'Semi-Empirical Model',
            'model_type': 'semi_empirical',
            'applicable_scenarios': ['多应力耦合', '综合衰减', '复杂工况预测'],
            'mathematical_form': 'SOH = f(T) × f(DOD) × f(C-rate) × f(SOC)',
            'formula_expression': '1 - (1 - temp_factor * dod_factor * c_rate_factor * soc_factor) * t / 25',
            'parameters': {
                'temp_coeff': {'label': '温度系数', 'default': 0.002, 'min': 0, 'max': 0.01, 'unit': '/°C'},
                'dod_coeff': {'label': 'DOD系数', 'default': 0.5, 'min': 0, 'max': 2.0, 'unit': ''},
                'c_rate_coeff': {'label': '倍率系数', 'default': 0.1, 'min': 0, 'max': 1.0, 'unit': ''},
                'soc_coeff': {'label': 'SOC窗口系数', 'default': 0.3, 'min': 0, 'max': 1.0, 'unit': ''},
            },
            'accuracy_level': 'medium',
            'accuracy_desc': 'R²>0.97',
            'category': 'degradation',
            'is_builtin': True,
            'description': '综合考虑温度、DOD、C-rate、SOC窗口四大应力因素的半经验综合衰减模型。温度系数（0.002/°C）：温度每偏离25°C 1°C，衰减速率变化0.2%；DOD系数（0.5）：DOD从50%升至100%时衰减速率翻倍；倍率系数（0.1）：0.5C充电相比1C充电衰减减半；SOC窗口系数（0.3）：宽SOC窗口加速衰减。适用于无法简化为单一主应力因素的复杂运行工况综合评估。',
        },
        {
            'name': '默认混合模型 (Default Hybrid)',
            'name_en': 'Default Hybrid Model',
            'model_type': 'arrhenius_hybrid',
            'applicable_scenarios': ['通用默认', '快速评估', '无详细数据时使用'],
            'mathematical_form': '基于Arrhenius方程的综合混合模型',
            'formula_expression': 'A_cal * Math.exp(-Ea_cal * 1000 / (R * T)) * Math.pow(t + 0.5, alpha)',
            'parameters': {
                'A_cal': {'label': '日历老化因子', 'default': 0.001, 'min': 0.0001, 'max': 0.01, 'unit': ''},
                'Ea_cal': {'label': '日历活化能', 'default': 35, 'min': 20, 'max': 60, 'unit': 'kJ/mol'},
                'alpha': {'label': '时间指数', 'default': 0.5, 'min': 0.3, 'max': 0.7, 'unit': ''},
                'A_cyc': {'label': '循环老化因子', 'default': 0.00001, 'min': 1e-7, 'max': 1e-4, 'unit': ''},
                'Ea_cyc': {'label': '循环活化能', 'default': 25, 'min': 15, 'max': 50, 'unit': 'kJ/mol'},
                'beta': {'label': '循环指数', 'default': 0.7, 'min': 0.5, 'max': 0.9, 'unit': ''},
            },
            'accuracy_level': 'medium',
            'accuracy_desc': '通用默认模型，适用广泛',
            'category': 'degradation',
            'is_builtin': True,
            'description': '通用默认混合衰减模型，基于Arrhenius框架同时处理日历老化和循环老化。日历老化因子（A_cal=0.001）和循环老化因子（A_cyc=1e-5）分别为两个老化路径的基础速率。当项目缺乏详细的电芯衰减测试数据时使用。参数参考了多款主流LFP电芯（EVE LF280K、宁德时代 LFP280等）公开数据的平均值，可作为快速评估的起点。',
        },
        
        # ========== 财务类 (financial) ==========
        {
            'name': 'IRR 内部收益率 (Newton-Raphson)',
            'name_en': 'IRR (Newton-Raphson)',
            'model_type': 'irr_newton',
            'applicable_scenarios': ['投资决策', '项目评估', '敏感性分析'],
            'mathematical_form': 'NPV = Σ CF_t/(1+IRR)^t = 0',
            'formula_expression': 'Newton-Raphson迭代法数值求解',
            'parameters': {
                'wacc': {'label': '折现率 WACC', 'default': 8, 'min': 4, 'max': 15, 'unit': '%'},
                'debt_ratio': {'label': '债务融资比例', 'default': 70, 'min': 0, 'max': 90, 'unit': '%'},
                'loan_rate': {'label': '贷款利率', 'default': 4.5, 'min': 2, 'max': 10, 'unit': '%'},
                'loan_years': {'label': '贷款年限', 'default': 15, 'min': 5, 'max': 25, 'unit': '年'},
                'tax_rate': {'label': '所得税率', 'default': 25, 'min': 0, 'max': 35, 'unit': '%'},
                'depreciation_years': {'label': '折旧年限', 'default': 20, 'min': 10, 'max': 25, 'unit': '年'},
                'residual_rate': {'label': '残值率', 'default': 5, 'min': 0, 'max': 20, 'unit': '%'},
            },
            'accuracy_level': 'high',
            'accuracy_desc': '收敛精度 < 1e-6',
            'category': 'financial',
            'is_builtin': True,
            'description': '内部收益率（IRR）是使项目净现值为零时的折现率，是投资决策的核心指标。采用Newton-Raphson迭代法数值求解f(r)=0的根，收敛精度 < 1e-6。行业标准：全投资IRR（Project IRR）目标6-10%，自有资金IRR（Equity IRR）目标10-15%。WACC=8%为行业典型折现率，债务融资比例70%参考了国内储能项目主流融资结构（70%银行贷款+30%自有资金）。',
        },
        {
            'name': 'LCOS 平准化储能成本',
            'name_en': 'LCOS (Levelized Cost of Storage)',
            'model_type': 'lcos',
            'applicable_scenarios': ['经济性对标', '技术路线比较', '项目可行性'],
            'mathematical_form': 'LCOS = Σ(CAPEX_t + OPEX_t + Aug_t - RV)/(1+r)^t / Σ E_t/(1+r)^t',
            'formula_expression': '全生命周期折现总成本 / 全生命周期折现总放电量',
            'parameters': {
                'container_cost': {'label': '集装箱单价', 'default': 120, 'min': 80, 'max': 200, 'unit': '万元/MWh'},
                'pcs_cost': {'label': 'PCS单价', 'default': 30, 'min': 20, 'max': 60, 'unit': '万元/MW'},
                'bop_cost': {'label': 'BOP配套成本', 'default': 15, 'min': 5, 'max': 30, 'unit': '万元/MWh'},
                'dev_cost': {'label': '开发费', 'default': 5, 'min': 2, 'max': 15, 'unit': '万元/MW'},
                'fixed_om': {'label': '固定O&M', 'default': 45, 'min': 20, 'max': 80, 'unit': '元/kW·年'},
                'var_om': {'label': '可变O&M', 'default': 0.008, 'min': 0.003, 'max': 0.02, 'unit': '元/kWh'},
                'insurance_rate': {'label': '保险费率', 'default': 0.3, 'min': 0.1, 'max': 0.5, 'unit': '% of CAPEX'},
                'om_escalation': {'label': 'O&M年涨幅', 'default': 2, 'min': 0, 'max': 5, 'unit': '%/年'},
            },
            'accuracy_level': 'medium',
            'accuracy_desc': '行业对标标准',
            'category': 'financial',
            'is_builtin': True,
            'description': '平准化储能成本（LCOS）是储能项目经济性的核心对标指标，类比光伏LCOE。计算全生命周期内每放出1kWh电的折现总成本，包含初始投资+运维支出+增容支出，扣除末期残值。行业标准：集装箱120万元/MWh（2024年LFP电芯价格触底后）、PCS 30万元/MW、固定O&M 45元/kW·年。Masdar级项目要求LCOS < 0.06美元/kWh（折合约0.40元/kWh）。',
        },
        {
            'name': 'DSCR 偿债覆盖倍率',
            'name_en': 'DSCR (Debt Service Coverage Ratio)',
            'model_type': 'dscr',
            'applicable_scenarios': ['融资审批', '风险评估', '贷款可行性'],
            'mathematical_form': 'DSCR = (EBITDA - Tax) / (Principal + Interest)',
            'formula_expression': '可偿债现金流 / 年应付本息',
            'parameters': {
                'dscr_min': {'label': '银行最低要求', 'default': 1.3, 'min': 1.0, 'max': 2.0, 'unit': ''},
                'loan_rate': {'label': '贷款利率', 'default': 4.5, 'min': 2, 'max': 10, 'unit': '%'},
                'loan_years': {'label': '贷款年限', 'default': 15, 'min': 5, 'max': 25, 'unit': '年'},
                'repayment_type': {'label': '还款方式', 'default': '等额本息', 'min': '', 'max': '', 'unit': ''},
            },
            'accuracy_level': 'high',
            'accuracy_desc': '逐年度精准计算',
            'category': 'financial',
            'is_builtin': True,
            'description': '偿债覆盖倍率（DSCR）衡量项目每年可用于还本付息的现金是否充足，是银行和金融机构放贷的核心审批指标。分子为EBITDA减所得税后的可偿债现金流，分母为当年应付本息。行业标准：国内银行通常要求DSCR全程 ≥ 1.3倍；若某年DSCR < 1.0则项目无法自行偿债，需股东追加担保。贷款利率4.5%参考了2024年绿色信贷优惠利率。',
        },
        {
            'name': '投资回收期 (Payback Period)',
            'name_en': 'Payback Period',
            'model_type': 'payback',
            'applicable_scenarios': ['投资风险', '快速筛选', '方案比较'],
            'mathematical_form': 'Σ CF_t = 0 时的年份数',
            'formula_expression': '静态回收期 + 动态回收期（WACC折现）',
            'parameters': {
                'discount_rate': {'label': '折现率(动态)', 'default': 8, 'min': 4, 'max': 15, 'unit': '%'},
                'target_years': {'label': '目标回收年限', 'default': 10, 'min': 5, 'max': 20, 'unit': '年'},
            },
            'accuracy_level': 'high',
            'accuracy_desc': '静态+动态双计算',
            'category': 'financial',
            'is_builtin': True,
            'description': '投资回收期是累计净现金流首次由负转正的时间点。静态回收期不考虑资金时间价值，直接累加名义现金流；动态回收期将所有现金流按WACC折现后再累加。行业标准：储能项目静态回收期通常8-12年，动态回收期10-15年。目标回收年限10年为行业投资决策参考线。回收期越短，项目抗政策/电价波动风险能力越强。',
        },
        {
            'name': '多收入叠加模型 (Multi-Stack Revenue)',
            'name_en': 'Multi-Stack Revenue Model',
            'model_type': 'revenue_stack',
            'applicable_scenarios': ['收益建模', '市场分析', '电价场景'],
            'mathematical_form': 'Revenue = Arbitrage + Capacity + Ancillary',
            'formula_expression': '套利收入 + 容量市场 + 辅助服务',
            'parameters': {
                'off_peak_price': {'label': '低谷购电价', 'default': 40, 'min': 20, 'max': 80, 'unit': '$/MWh'},
                'peak_price': {'label': '高峰售电价', 'default': 120, 'min': 60, 'max': 200, 'unit': '$/MWh'},
                'spread_capture': {'label': '价差捕获率', 'default': 85, 'min': 60, 'max': 95, 'unit': '%'},
                'calendar_days': {'label': '日历可用天数', 'default': 350, 'min': 300, 'max': 365, 'unit': '天'},
                'capacity_price': {'label': '容量市场单价', 'default': 50000, 'min': 0, 'max': 150000, 'unit': '$/MW·年'},
                'ancillary_price': {'label': '辅助服务单价', 'default': 5, 'min': 0, 'max': 15, 'unit': '$/MW·h'},
                'price_escalation': {'label': '电价年涨幅', 'default': 2, 'min': 0, 'max': 5, 'unit': '%/年'},
                'efficiency_loss': {'label': '充放电效率扣减', 'default': 5, 'min': 2, 'max': 10, 'unit': '%'},
            },
            'accuracy_level': 'medium',
            'accuracy_desc': '三收入栈叠加',
            'category': 'financial',
            'is_builtin': True,
            'description': '大型储能电站叠加多个收入来源以提升项目IRR。三收入栈：1）电能量套利——低谷购电/高峰售电，价差捕获率85%考虑了充放电效率和辅助损耗；2）容量市场——按可用装机容量获得固定补偿，5万美元/MW·年参考了美国PJM市场价格；3）辅助服务——调频/备用服务的额外收入。不同市场结构下各收入占比差异显著（套利40-70%、容量20-40%、辅助10-20%）。电价年涨幅2%为保守通胀估计。',
        },
        
        # ========== 工程计算类 (engineering) ==========
        {
            'name': '存量资产粗放电量计算',
            'name_en': 'Gross Discharge Energy (Initial Assets)',
            'model_type': 'gross_discharge',
            'applicable_scenarios': ['容量配置', '放电量估算'],
            'mathematical_form': 'E_gross = N_cont × E_rated × DOD × SOH',
            'formula_expression': 'containerQty * ratedEnergy * DOD * SOH',
            'parameters': {
                'rated_energy_mwh': {'label': '单舱额定能量', 'default': 5, 'min': 1, 'max': 15, 'unit': 'MWh'},
                'dod_default': {'label': '默认DOD', 'default': 90, 'min': 50, 'max': 100, 'unit': '%'},
                'rte_default': {'label': '首年RTE', 'default': 94, 'min': 85, 'max': 98, 'unit': '%'},
            },
            'accuracy_level': 'high',
            'accuracy_desc': '精确工程计算',
            'category': 'engineering',
            'is_builtin': True,
            'description': '计算存量资产（初始安装的集装箱）的单次循环粗放电量。公式：E_gross = 舱数 × 单舱额定能量(MWh) × DOD × SOH(t)。这是后续所有净放电量和增容计算的基础。行业标准：5MWh标准舱为当前主流产品（宁德时代C20-5MWh），默认DOD=90%为LFP电池行业推荐运行深度，RTE=94%为液冷系统在25°C下的标准效率。',
        },
        {
            'name': '自辅耗校核模型',
            'name_en': 'Auxiliary Consumption Calibration',
            'model_type': 'aux_consumption',
            'applicable_scenarios': ['能耗评估', '效率分析'],
            'mathematical_form': 'E_aux = P_run × t_run + P_standby × t_standby',
            'formula_expression': '运行辅耗 + 待机辅耗（含集装箱和PCS）',
            'parameters': {
                'bess_aux_run': {'label': '集装箱运行功率', 'default': 15, 'min': 5, 'max': 50, 'unit': 'kW'},
                'bess_aux_standby': {'label': '集装箱待机功率', 'default': 5, 'min': 1, 'max': 15, 'unit': 'kW'},
                'pcs_aux_run': {'label': 'PCS运行功率', 'default': 2, 'min': 1, 'max': 10, 'unit': 'kW'},
                'pcs_aux_standby': {'label': 'PCS待机功率', 'default': 0.5, 'min': 0.1, 'max': 5, 'unit': 'kW'},
                'daily_run_hours': {'label': '日运行时长', 'default': 8, 'min': 2, 'max': 20, 'unit': '小时'},
            },
            'accuracy_level': 'high',
            'accuracy_desc': '基于时轴动态计算',
            'category': 'engineering',
            'is_builtin': True,
            'description': '高精度时轴动静态复合自辅耗平摊校核模型。将辅耗分为运行功耗和待机功耗两部分，分别按日运行时长和日待机时长加权计算。集装箱运行功率15kW（液冷系统，含水泵/风机/BMS）、待机5kW；PCS运行2kW（含控制电路/散热风扇）、待机0.5kW。单日8小时运行（2次完整充放电循环 × 4小时/次）为行业典型运行工况。',
        },
        {
            'name': '增容老化位移模型',
            'name_en': 'Augmentation Aging Displacement',
            'model_type': 'aug_aging',
            'applicable_scenarios': ['扩容策略', '全生命周期规划'],
            'mathematical_form': 'SOH_aug(t) = SOH_base(t - t_aug)',
            'formula_expression': '新增资产以安装年份为t=0的独立SOH曲线',
            'parameters': {
                'aug_strategy': {'label': '增容策略', 'default': '逐年补容', 'min': '', 'max': '', 'unit': ''},
                'target_soh': {'label': '目标维持SOH', 'default': 90, 'min': 70, 'max': 100, 'unit': '%'},
                'aug_threshold': {'label': '增容触发SOH', 'default': 85, 'min': 70, 'max': 95, 'unit': '%'},
                'cost_decline_rate': {'label': '成本年降幅', 'default': 5, 'min': 2, 'max': 10, 'unit': '%/年'},
                'learning_rate': {'label': '学习率', 'default': 18, 'min': 10, 'max': 25, 'unit': '%'},
            },
            'accuracy_level': 'medium',
            'accuracy_desc': 'Wright定律+役龄位移',
            'category': 'engineering',
            'is_builtin': True,
            'description': '动态扩容资产流役龄位移追踪模型。核心原理：每年新增的补容资产作为独立资产流，各自以安装年份为t=0开始独立的SOH衰减曲线。增容策略可选择"逐年补容"或"阈值触发"。目标维持SOH=90%意味着当系统总可用容量降至初始的90%以下时触发增容。成本年降幅5%基于Wright定律（学习率18%），反映锂电池成本随累计出货量翻倍而下降的趋势。',
        },
        
        # ========== 仿真配置类 (simulation) ==========
        {
            'name': 'SOH曲线参数配置',
            'name_en': 'SOH Curve Configuration',
            'model_type': 'soh_curve_config',
            'applicable_scenarios': ['默认SOH序列', '基准衰减配置'],
            'mathematical_form': '26年SOH序列（Year 0-25）',
            'formula_expression': '预定义SOH百分比序列',
            'parameters': {
                'soh_year1': {'label': '第1年末SOH', 'default': 97, 'min': 90, 'max': 100, 'unit': '%'},
                'soh_year25': {'label': '第25年末SOH', 'default': 71, 'min': 50, 'max': 85, 'unit': '%'},
                'soh_start_year': {'label': 'SOH起始年份', 'default': 1, 'min': 0, 'max': 5, 'unit': '年'},
                'degradation_rate_first': {'label': '首年衰减率', 'default': 3, 'min': 1, 'max': 8, 'unit': '%'},
                'degradation_rate_avg': {'label': '年均衰减率', 'default': 1.2, 'min': 0.5, 'max': 3, 'unit': '%'},
            },
            'accuracy_level': 'medium',
            'accuracy_desc': 'LFP标准衰减曲线',
            'category': 'simulation',
            'is_builtin': True,
            'description': 'SOH（健康状态）26年（Year 0-25）衰减序列的默认配置。行业标准：LFP电池首年衰减较快约3%（SEI膜形成和初期不可逆损失），之后年均衰减约1.2%，25年末剩余约71%容量。SOH起始年份设为第1年意味着第0年为出厂100%状态，实际衰减从第1年开始计算。适用于大规模储能电站ELC（能量保证合同）中的容量衰减预测。',
        },
        {
            'name': 'RTE曲线参数配置',
            'name_en': 'RTE Curve Configuration',
            'model_type': 'rte_curve_config',
            'applicable_scenarios': ['效率衰减', '净放电量计算'],
            'mathematical_form': '26年RTE序列（Year 0-25）',
            'formula_expression': '预定义RTE百分比序列',
            'parameters': {
                'rte_initial': {'label': '初始RTE', 'default': 94, 'min': 88, 'max': 98, 'unit': '%'},
                'rte_decline_annual': {'label': '年效率衰减', 'default': 0.1, 'min': 0.05, 'max': 0.3, 'unit': '%/年'},
                'rte_year25': {'label': '第25年末RTE', 'default': 91.5, 'min': 80, 'max': 95, 'unit': '%'},
            },
            'accuracy_level': 'medium',
            'accuracy_desc': '液冷系统标准效率',
            'category': 'simulation',
            'is_builtin': True,
            'description': 'RTE（往返效率）26年衰减序列的默认配置。RTE包括充电损耗（AC→DC）和放电损耗（DC→AC），反映储能系统整体能源转换效率。行业标准：液冷系统初始RTE约94%（含变压器+变流器+电池内阻损耗），年效率衰减约0.1%（主要来自电池内阻增大和冷却系统老化），25年末约91.5%。风冷系统初始RTE略低（约92%），衰减略快（0.15%/年）。',
        },
        {
            'name': '温度加速系数配置',
            'name_en': 'Temperature Acceleration Factor',
            'model_type': 'temp_factor',
            'applicable_scenarios': ['高温环境', '低温环境', '环境适应性评估'],
            'mathematical_form': 'Factor = 2^((T - T_ref)/10)',
            'formula_expression': '温度每升高10°C，老化速率翻倍',
            'parameters': {
                'T_ref': {'label': '参考温度', 'default': 25, 'min': 15, 'max': 35, 'unit': '°C'},
                'T_max': {'label': '最高运行温度', 'default': 50, 'min': 35, 'max': 65, 'unit': '°C'},
                'T_min': {'label': '最低运行温度', 'default': -20, 'min': -40, 'max': 0, 'unit': '°C'},
                'arrhenius_ea': {'label': '活化能', 'default': 35, 'min': 20, 'max': 60, 'unit': 'kJ/mol'},
            },
            'accuracy_level': 'medium',
            'accuracy_desc': 'Arrhenius 温度修正',
            'category': 'simulation',
            'is_builtin': True,
            'description': '基于Arrhenius方程的温度加速因子配置，用于修正不同环境温度下的老化速率。核心规则：温度每偏离参考温度25°C 10°C，化学反应速率（老化速率）约翻倍。最高运行温度50°C参考了中东户外项目典型环境；最低-20°C参考了中国北方冬季户外运行条件。活化能35 kJ/mol为LFP电池SEI膜生长的标准值，低温环境下该值可能略有变化。',
        },
    ]


@algorithm_bp.route('/api/algorithms/public', methods=['GET'])
def get_public_algorithms():
    """公开接口：获取算法模型列表（无需认证，供仿真实验室使用）"""
    category = request.args.get('category')
    query = AlgorithmModel.query.filter_by(is_builtin=True, is_active=True)
    
    if category:
        query = query.filter_by(category=category)
    
    algorithms = query.order_by(AlgorithmModel.sort_order, AlgorithmModel.name).all()
    
    result = []
    for alg in algorithms:
        result.append({
            'id': alg.id,
            'name': alg.name,
            'model_type': alg.model_type,
            'parameters': json.loads(alg.parameters) if alg.parameters else {},
            'category': alg.category,
            'formula_expression': alg.formula_expression,
            'description': alg.description,
        })
    
    return jsonify({'success': True, 'data': result})


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
            is_builtin=True,
        ).filter(AlgorithmModel.name == alg_data['name']).first()
        
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
