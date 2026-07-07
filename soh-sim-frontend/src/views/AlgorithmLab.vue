<template>
  <div class="h-full overflow-y-auto p-4">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg font-bold text-teal-400">算法试验场</h2>
      <button
        class="bg-teal-600 hover:bg-teal-700 text-white text-xs px-4 py-2 rounded-lg transition-colors flex items-center gap-2"
        @click="showAddModal = true"
      >
        <span>+</span>
        添加算法模型
      </button>
    </div>

    <div class="flex gap-2 mb-4 flex-wrap">
      <button
        v-for="cat in categories"
        :key="cat.key"
        :class="[
          'text-xs px-3 py-1.5 rounded-lg transition-all border',
          activeCategory === cat.key
            ? 'bg-teal-500/20 text-teal-400 border-teal-500/40'
            : 'bg-slate-800 text-slate-400 border-slate-700 hover:border-slate-500'
        ]"
        @click="activeCategory = cat.key"
      >
        {{ cat.label }}
        <span class="ml-1 text-[10px] opacity-50">({{ catCount(cat.key) }})</span>
      </button>
    </div>

    <div v-if="filteredAlgorithms.length === 0" class="text-center py-16 text-slate-500">
      <div class="text-4xl mb-3">&#9312;</div>
      <div>暂无算法模型</div>
      <button class="mt-4 text-teal-400 hover:text-teal-300 text-sm underline" @click="initializeBuiltin">
        初始化内置算法
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div
        v-for="alg in filteredAlgorithms"
        :key="alg.id"
        class="bg-slate-900/70 border rounded-xl overflow-hidden transition-all duration-200"
        :class="getCardBorderClass(alg.category)"
      >
        <div class="p-4">
          <div class="flex justify-between items-start mb-3">
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 mb-1">
                <h3 class="font-bold text-slate-200 text-sm truncate">
                  {{ alg.name }}
                </h3>
                <span
                  v-if="alg.is_builtin"
                  class="text-[10px] bg-amber-500/20 text-amber-400 px-1.5 py-0.5 rounded shrink-0"
                >
                  内置
                </span>
              </div>
              <span :class="['text-[10px] px-1.5 py-0.5 rounded', getCategoryBadgeClass(alg.category)]">
                {{ getCategoryLabel(alg.category) }}
              </span>
            </div>
            <button
              v-if="!alg.is_builtin"
              class="text-slate-500 hover:text-red-400 text-xs ml-2 shrink-0"
              @click="deleteAlgorithm(alg.id)"
            >
              &#10005;
            </button>
          </div>

          <p class="text-xs text-slate-400 leading-relaxed mb-3 line-clamp-3">
            {{ alg.description || '暂无描述' }}
          </p>

          <div class="grid grid-cols-2 gap-x-3 gap-y-1.5 mb-3 text-[11px]">
            <div>
              <span class="text-slate-500">精度:</span>
              <span :class="getAccuracyClass(alg.accuracy_level)">
                {{ alg.accuracy_desc || getAccuracyLabel(alg.accuracy_level) }}
              </span>
            </div>
            <div>
              <span class="text-slate-500">类型:</span>
              <span class="text-slate-300">{{ getModelTypeLabel(alg.model_type) }}</span>
            </div>
            <div v-if="alg.name_en && alg.name_en !== alg.name">
              <span class="text-slate-500">英文:</span>
              <span class="text-slate-300 text-[10px]">{{ alg.name_en }}</span>
            </div>
            <div v-if="alg.mathematical_form">
              <span class="text-slate-500">形式:</span>
              <span class="text-slate-300 font-mono text-[10px]">{{ alg.mathematical_form }}</span>
            </div>
          </div>

          <div class="border-t border-slate-800/50 pt-2.5">
            <div class="text-[10px] text-slate-500 mb-1.5">参数 ({{ paramCount(alg.parameters) }}):</div>
            <div class="flex flex-wrap gap-1">
              <span
                v-for="(param, key) in alg.parameters"
                :key="key"
                class="text-[10px] bg-slate-800/80 text-slate-300 px-1.5 py-0.5 rounded border border-slate-700/50"
              >
                {{ param.label || key }}={{ param.default }}{{ param.unit }}
              </span>
            </div>
          </div>

          <div v-if="alg.applicable_scenarios && alg.applicable_scenarios.length > 0" class="flex flex-wrap gap-1 mt-2">
            <span
              v-for="scenario in alg.applicable_scenarios"
              :key="scenario"
              class="text-[10px] bg-teal-500/10 text-teal-400/80 px-1.5 py-0.5 rounded border border-teal-500/20"
            >
              {{ scenario }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="filteredAlgorithms.length > 0" class="text-center text-[10px] text-slate-600 mt-6 mb-4">
      共 {{ filteredAlgorithms.length }} 个算法模型 | 双击切换分类查看
    </div>

    <!-- 添加算法模型弹窗 -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
      <div class="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center p-4 border-b border-slate-700">
          <h3 class="font-bold text-teal-400">添加算法模型</h3>
          <button class="text-slate-500 hover:text-slate-300" @click="showAddModal = false">&#10005;</button>
        </div>

        <div class="p-4 space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="text-xs text-slate-400 block mb-1">模型名称 *</label>
              <input
                v-model="newAlg.name"
                class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none"
                placeholder="如: 自定义衰减模型"
              />
            </div>
            <div>
              <label class="text-xs text-slate-400 block mb-1">英文名称</label>
              <input
                v-model="newAlg.name_en"
                class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none"
                placeholder="如: Custom Degradation Model"
              />
            </div>
          </div>

          <div class="grid grid-cols-3 gap-4">
            <div>
              <label class="text-xs text-slate-400 block mb-1">模型类型</label>
              <select
                v-model="newAlg.model_type"
                class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none"
              >
                <option value="custom">自定义 Custom</option>
                <option value="double_exponential">双指数模型</option>
                <option value="linear_log">线性-对数模型</option>
                <option value="arrhenius">Arrhenius模型</option>
                <option value="rainflow">雨流计数法</option>
                <option value="semi_empirical">半经验模型</option>
                <option value="lcos">LCOS模型</option>
                <option value="irr_newton">IRR模型</option>
                <option value="dscr">DSCR模型</option>
                <option value="payback">回收期模型</option>
                <option value="revenue_stack">多收入模型</option>
                <option value="gross_discharge">粗放电量</option>
                <option value="aux_consumption">自辅耗校核</option>
                <option value="aug_aging">增容老化</option>
                <option value="soh_curve_config">SOH曲线配置</option>
                <option value="rte_curve_config">RTE曲线配置</option>
                <option value="temp_factor">温度加速配置</option>
              </select>
            </div>
            <div>
              <label class="text-xs text-slate-400 block mb-1">分类</label>
              <select
                v-model="newAlg.category"
                class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none"
              >
                <option value="degradation">容量衰减</option>
                <option value="financial">财务模型</option>
                <option value="engineering">工程计算</option>
                <option value="simulation">仿真配置</option>
              </select>
            </div>
            <div>
              <label class="text-xs text-slate-400 block mb-1">精度等级</label>
              <select
                v-model="newAlg.accuracy_level"
                class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none"
              >
                <option value="high">高</option>
                <option value="medium">中</option>
                <option value="low">低</option>
              </select>
            </div>
          </div>

          <div>
            <label class="text-xs text-slate-400 block mb-1">数学形式</label>
            <input
              v-model="newAlg.mathematical_form"
              class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none font-mono"
              placeholder="如: SOH(t) = A*e^(-kt) + B"
            />
          </div>

          <div>
            <label class="text-xs text-slate-400 block mb-1">公式表达式 (JavaScript)</label>
            <textarea
              v-model="newAlg.formula_expression"
              rows="2"
              class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none font-mono"
              placeholder="如: A * Math.exp(-k * t) + B"
            />
          </div>

          <div>
            <label class="text-xs text-slate-400 block mb-1">精度描述</label>
            <input
              v-model="newAlg.accuracy_desc"
              class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none"
              placeholder="如: R^2>0.99"
            />
          </div>

          <div>
            <label class="text-xs text-slate-400 block mb-1">适用场景</label>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="scenario in availableScenarios"
                :key="scenario"
                :class="[
                  'text-xs px-3 py-1 rounded transition-colors',
                  newAlg.applicable_scenarios.includes(scenario)
                    ? 'bg-teal-600 text-white'
                    : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                ]"
                @click="toggleScenario(scenario)"
              >
                {{ scenario }}
              </button>
            </div>
          </div>

          <div>
            <div class="flex justify-between items-center mb-2">
              <label class="text-xs text-slate-400">参数定义</label>
              <button class="text-teal-400 hover:text-teal-300 text-xs" @click="addParameter">+ 添加参数</button>
            </div>
            <div v-if="Object.keys(newAlg.parameters).length > 0" class="space-y-2">
              <div v-for="(param, key) in newAlg.parameters" :key="key" class="flex gap-2 items-center">
                <input
                  v-model="param.label"
                  class="bg-slate-800 border border-slate-700 rounded px-2 py-1 text-xs w-28"
                  placeholder="参数名"
                />
                <input
                  v-model.number="param.default"
                  type="number"
                  class="bg-slate-800 border border-slate-700 rounded px-2 py-1 text-xs w-20"
                  placeholder="默认值"
                />
                <input
                  v-model.number="param.min"
                  type="number"
                  class="bg-slate-800 border border-slate-700 rounded px-2 py-1 text-xs w-16"
                  placeholder="最小值"
                />
                <input
                  v-model.number="param.max"
                  type="number"
                  class="bg-slate-800 border border-slate-700 rounded px-2 py-1 text-xs w-16"
                  placeholder="最大值"
                />
                <input
                  v-model="param.unit"
                  class="bg-slate-800 border border-slate-700 rounded px-2 py-1 text-xs w-16"
                  placeholder="单位"
                />
                <button class="text-red-400 hover:text-red-300" @click="removeParameter(key)">&#10005;</button>
              </div>
            </div>
            <div v-else class="text-slate-500 text-xs text-center py-4">-- 点击上方按钮添加参数 --</div>
          </div>

          <div>
            <label class="text-xs text-slate-400 block mb-1">描述（支持中文说明）</label>
            <textarea
              v-model="newAlg.description"
              rows="3"
              class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none"
              placeholder="模型描述..."
            />
          </div>
        </div>

        <div class="flex justify-end gap-3 p-4 border-t border-slate-700">
          <button class="text-slate-400 hover:text-slate-200 text-sm px-4 py-2 rounded" @click="showAddModal = false">
            取消
          </button>
          <button
            class="bg-teal-600 hover:bg-teal-700 text-white text-sm px-4 py-2 rounded transition-colors"
            @click="createAlgorithm"
          >
            创建
          </button>
        </div>
      </div>
    </div>

    <!-- 提示框 -->
    <div
      v-if="toast.show"
      :class="[
        'fixed top-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all',
        toast.type === 'success' ? 'bg-emerald-500 text-white' : 'bg-red-500 text-white'
      ]"
    >
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import api from '../services/api.js'

const algorithms = ref([])
const showAddModal = ref(false)
const activeCategory = ref('degradation')
const toast = reactive({ show: false, message: '', type: 'success' })

const categories = [
  { key: 'degradation', label: '容量衰减' },
  { key: 'financial', label: '财务模型' },
  { key: 'engineering', label: '工程计算' },
  { key: 'simulation', label: '仿真配置' }
]

const filteredAlgorithms = computed(() => {
  if (!activeCategory.value) return algorithms.value
  return algorithms.value.filter((a) => a.category === activeCategory.value)
})

function catCount(key) {
  return algorithms.value.filter((a) => a.category === key).length
}

const availableScenarios = [
  'LFP日历衰减',
  '循环衰减',
  '综合衰减预测',
  'RTE衰减',
  '效率衰减建模',
  '温度加速老化',
  '日历寿命预测',
  '不规则循环损伤',
  '实际运行工况',
  '多应力耦合',
  '投资决策',
  '项目评估',
  '经济性对标',
  '融资审批',
  '收益建模',
  '容量配置',
  '能耗评估',
  '扩容策略',
  '默认配置',
  '环境适应性评估'
]

const newAlg = reactive({
  name: '',
  name_en: '',
  model_type: 'custom',
  category: 'degradation',
  accuracy_level: 'medium',
  mathematical_form: '',
  formula_expression: '',
  accuracy_desc: '',
  applicable_scenarios: [],
  parameters: {},
  description: ''
})

function getModelTypeLabel(type) {
  const labels = {
    double_exponential: '双指数模型',
    linear_log: '线性-对数模型',
    arrhenius: 'Arrhenius模型',
    rainflow: '雨流计数法',
    semi_empirical: '半经验模型',
    lcos: 'LCOS成本模型',
    irr_newton: 'IRR收益率模型',
    dscr: 'DSCR偿债模型',
    payback: '投资回收期',
    revenue_stack: '多收入叠加',
    gross_discharge: '粗放电量',
    aux_consumption: '自辅耗校核',
    aug_aging: '增容老化模型',
    soh_curve_config: 'SOH曲线配置',
    rte_curve_config: 'RTE曲线配置',
    temp_factor: '温度加速配置',
    custom: '自定义'
  }
  return labels[type] || type
}

function getCategoryLabel(category) {
  const labels = {
    degradation: '容量衰减',
    financial: '财务模型',
    engineering: '工程计算',
    simulation: '仿真配置'
  }
  return labels[category] || category
}

function getCategoryBadgeClass(category) {
  const classes = {
    degradation: 'bg-blue-500/15 text-blue-400 border border-blue-500/30',
    financial: 'bg-amber-500/15 text-amber-400 border border-amber-500/30',
    engineering: 'bg-purple-500/15 text-purple-400 border border-purple-500/30',
    simulation: 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30'
  }
  return classes[category] || 'bg-slate-700 text-slate-400'
}

function getCardBorderClass(category) {
  const classes = {
    degradation: 'border-blue-500/20 hover:border-blue-500/50',
    financial: 'border-amber-500/20 hover:border-amber-500/50',
    engineering: 'border-purple-500/20 hover:border-purple-500/50',
    simulation: 'border-emerald-500/20 hover:border-emerald-500/50'
  }
  return classes[category] || 'border-slate-800 hover:border-slate-600'
}

function getAccuracyClass(level) {
  const classes = {
    high: 'text-emerald-400',
    medium: 'text-amber-400',
    low: 'text-red-400'
  }
  return classes[level] || 'text-slate-400'
}

function getAccuracyLabel(level) {
  const labels = { high: '高精度', medium: '中等精度', low: '一般精度' }
  return labels[level] || level
}

function paramCount(params) {
  return params ? Object.keys(params).length : 0
}

function toggleScenario(scenario) {
  const idx = newAlg.applicable_scenarios.indexOf(scenario)
  if (idx >= 0) {
    newAlg.applicable_scenarios.splice(idx, 1)
  } else {
    newAlg.applicable_scenarios.push(scenario)
  }
}

function addParameter() {
  const key = `param_${Date.now()}`
  newAlg.parameters[key] = {
    label: '',
    default: 0.0,
    min: 0,
    max: 100,
    unit: ''
  }
}

function removeParameter(key) {
  delete newAlg.parameters[key]
}

function showToast(message, type = 'success') {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => {
    toast.show = false
  }, 3000)
}

function getBuiltinFallback() {
  return [
    {
      id: 'builtin-arrhenius',
      name: 'Arrhenius 加速老化模型',
      name_en: 'Arrhenius Accelerated Aging',
      model_type: 'arrhenius',
      category: 'degradation',
      accuracy_level: 'high',
      accuracy_desc: 'R^2 > 0.99',
      mathematical_form: 'SOH(t) = A * exp(-Ea/(R*T)) * t^n',
      description: '基于 Arrhenius 方程的电化学老化模型，考虑温度对反应速率的加速效应，适用于 LFP 电池日历衰减预测。',
      is_builtin: true,
      applicable_scenarios: ['LFP日历衰减', '温度加速老化', '日历寿命预测'],
      parameters: {
        A: { label: '前置系数', default: 1.0, min: 0, max: 10, unit: '' },
        Ea: { label: '活化能', default: 25000, min: 0, max: 100000, unit: 'J/mol' },
        n: { label: '时间指数', default: 0.5, min: 0, max: 2, unit: '' }
      }
    },
    {
      id: 'builtin-double-exp',
      name: '双指数衰减模型',
      name_en: 'Double Exponential Decay',
      model_type: 'double_exponential',
      category: 'degradation',
      accuracy_level: 'high',
      accuracy_desc: 'R^2 > 0.98',
      mathematical_form: 'SOH(t) = A1*exp(-k1*t) + A2*exp(-k2*t) + C',
      description: '双指数模型捕获电池早期快速衰减和中长期缓慢衰减两阶段特征，对 LFP 全寿命周期拟合精度高。',
      is_builtin: true,
      applicable_scenarios: ['LFP日历衰减', '综合衰减预测', '循环衰减'],
      parameters: {
        A1: { label: '快衰减幅值', default: 0.03, min: 0, max: 0.2, unit: '' },
        k1: { label: '快衰减速率', default: 0.5, min: 0, max: 5, unit: '1/yr' },
        A2: { label: '慢衰减幅值', default: 0.35, min: 0, max: 0.6, unit: '' },
        k2: { label: '慢衰减速率', default: 0.02, min: 0, max: 0.1, unit: '1/yr' },
        C: { label: '渐近值', default: 0.6, min: 0, max: 1, unit: '' }
      }
    },
    {
      id: 'builtin-linear-log',
      name: '线性-对数衰减模型',
      name_en: 'Linear-Log Degradation',
      model_type: 'linear_log',
      category: 'degradation',
      accuracy_level: 'medium',
      accuracy_desc: 'R^2 > 0.95',
      mathematical_form: 'SOH(t) = a - b*ln(t+1)',
      description: '基于 SEI 膜生长理论的简化模型，适用于日历老化的粗略估算。',
      is_builtin: true,
      applicable_scenarios: ['LFP日历衰减', '日历寿命预测', '默认配置'],
      parameters: {
        a: { label: '初始值', default: 1.0, min: 0.8, max: 1.0, unit: '' },
        b: { label: '衰减系数', default: 0.05, min: 0, max: 0.2, unit: '' }
      }
    },
    {
      id: 'builtin-rainflow',
      name: '雨流计数模型 (Rainflow)',
      name_en: 'Rainflow Counting Model',
      model_type: 'rainflow',
      category: 'degradation',
      accuracy_level: 'high',
      accuracy_desc: '与实际工况高度吻合',
      mathematical_form: 'D = Σ(n_i/N_i) * (DOD_i/DOD_ref)^m',
      description:
        '基于Miner线性损伤累积法则和雨流计数法的循环寿命预测模型。将实际运行中不规则、变幅的充放电循环统计为等效标准循环次数，按DOD加权计算累积损伤。大DOD循环的损伤远高于小DOD循环。参考循环寿命（6000次）为LFP电池在100%DOD、25°C下的行业标准值。',
      is_builtin: true,
      applicable_scenarios: ['不规则循环损伤', '实际运行工况', '多DOD混合工况'],
      parameters: {
        damage_exponent: { label: '损伤指数', default: 1.5, min: 1.0, max: 3.0, unit: '' },
        cycle_life_ref: { label: '参考循环寿命', default: 6000, min: 1000, max: 20000, unit: '次' },
        dod_ref: { label: '参考DOD', default: 1.0, min: 0.1, max: 1.0, unit: '' }
      }
    },
    {
      id: 'builtin-semi-empirical',
      name: '半经验综合模型 (Semi-Empirical)',
      name_en: 'Semi-Empirical Comprehensive Model',
      model_type: 'semi_empirical',
      category: 'degradation',
      accuracy_level: 'medium',
      accuracy_desc: 'R^2 > 0.97',
      mathematical_form: 'SOH = f(T) * f(DOD) * f(C-rate) * f(SOC)',
      description:
        '综合考虑温度、DOD、C-rate、SOC窗口四大应力因素的半经验综合衰减模型。温度每偏离25°C 1°C，衰减速率变化0.2%；DOD从50%升至100%时衰减速率翻倍；0.5C充电相比1C充电衰减减半；宽SOC窗口加速衰减。适用于多应力耦合的复杂运行工况。',
      is_builtin: true,
      applicable_scenarios: ['多应力耦合', '综合衰减', '复杂工况预测'],
      parameters: {
        temp_coeff: { label: '温度系数', default: 0.002, min: 0, max: 0.01, unit: '/°C' },
        dod_coeff: { label: 'DOD系数', default: 0.5, min: 0, max: 2.0, unit: '' },
        c_rate_coeff: { label: '倍率系数', default: 0.1, min: 0, max: 1.0, unit: '' },
        soc_coeff: { label: 'SOC窗口系数', default: 0.3, min: 0, max: 1.0, unit: '' }
      }
    },
    {
      id: 'builtin-hybrid',
      name: '默认混合模型 (Default Hybrid)',
      name_en: 'Default Hybrid Model',
      model_type: 'arrhenius_hybrid',
      category: 'degradation',
      accuracy_level: 'medium',
      accuracy_desc: '通用默认模型，适用广泛',
      mathematical_form: '基于Arrhenius方程的综合混合模型',
      description:
        '通用默认混合衰减模型，基于Arrhenius框架同时处理日历老化和循环老化。日历老化因子（A_cal=0.001）和循环老化因子（A_cyc=1e-5）分别为两个老化路径的基础速率。参数参考多款主流LFP电芯（EVE LF280K、宁德时代 LFP280等）公开数据平均值，可作为快速评估的起点。',
      is_builtin: true,
      applicable_scenarios: ['通用默认', '快速评估', '无详细数据时使用'],
      parameters: {
        A_cal: { label: '日历老化因子', default: 0.001, min: 0.0001, max: 0.01, unit: '' },
        Ea_cal: { label: '日历活化能', default: 35, min: 20, max: 60, unit: 'kJ/mol' },
        alpha: { label: '时间指数', default: 0.5, min: 0.3, max: 0.7, unit: '' },
        A_cyc: { label: '循环老化因子', default: 0.00001, min: 1e-7, max: 1e-4, unit: '' },
        Ea_cyc: { label: '循环活化能', default: 25, min: 15, max: 50, unit: 'kJ/mol' },
        beta: { label: '循环指数', default: 0.7, min: 0.5, max: 0.9, unit: '' }
      }
    },
    {
      id: 'builtin-lcos',
      name: 'LCOS 度电成本模型',
      name_en: 'Levelized Cost of Storage',
      model_type: 'lcos',
      category: 'financial',
      accuracy_level: 'high',
      accuracy_desc: 'NPV 精度 < 1%',
      mathematical_form: 'LCOS = TotalDiscountedCosts / TotalDiscountedEnergy',
      description: '平准化储能成本模型，通过贴现现金流计算全生命周期每 MWh 的综合成本。',
      is_builtin: true,
      applicable_scenarios: ['投资决策', '项目评估', '经济性对标'],
      parameters: {
        discountRate: { label: '贴现率', default: 0.08, min: 0, max: 0.2, unit: '' }
      }
    },
    {
      id: 'builtin-irr',
      name: 'IRR 内部收益率模型',
      name_en: 'Internal Rate of Return',
      model_type: 'irr_newton',
      category: 'financial',
      accuracy_level: 'high',
      accuracy_desc: 'Newton-Raphson 收敛 < 1e-8',
      mathematical_form: 'NPV(r) = 0, Newton: r(k+1) = r(k) - NPV/NPV',
      description: '使用 Newton-Raphson 迭代法求解使净现值为零的贴现率，支持项目 IRR 和股权 IRR。',
      is_builtin: true,
      applicable_scenarios: ['投资决策', '融资审批', '收益建模'],
      parameters: {
        maxIter: { label: '最大迭代', default: 200, min: 50, max: 1000, unit: '次' },
        tol: { label: '收敛阈值', default: 1e-8, min: 1e-12, max: 1e-4, unit: '' }
      }
    },
    {
      id: 'builtin-dscr',
      name: 'DSCR 偿债备付率模型',
      name_en: 'Debt Service Coverage Ratio',
      model_type: 'dscr',
      category: 'financial',
      accuracy_level: 'medium',
      accuracy_desc: '财务合规模型',
      mathematical_form: 'DSCR = (EBITDA - Tax) / DebtService',
      description: '评估项目每年经营现金流对还本付息的覆盖能力，DSCR >= 1.2 为融资安全线。',
      is_builtin: true,
      applicable_scenarios: ['融资审批', '项目评估'],
      parameters: {
        minDscr: { label: '最低DSCR', default: 1.2, min: 1.0, max: 2.0, unit: '' }
      }
    },
    {
      id: 'builtin-payback',
      name: '投资回收期模型',
      name_en: 'Payback Period',
      model_type: 'payback',
      category: 'financial',
      accuracy_level: 'medium',
      accuracy_desc: '静态/动态双模型',
      mathematical_form: 'Static: CumCF >= 0; Dynamic: DiscountedCumCF >= 0',
      description: '计算静态和动态投资回收期，评估资金回笼速度。',
      is_builtin: true,
      applicable_scenarios: ['投资决策', '项目评估'],
      parameters: {}
    },
    {
      id: 'builtin-gross-discharge',
      name: '粗放电量计算模型',
      name_en: 'Gross Discharge Calculation',
      model_type: 'gross_discharge',
      category: 'engineering',
      accuracy_level: 'high',
      accuracy_desc: '解析解',
      mathematical_form: 'E_gross = RatedEnergy * Q * DOD * RTE * SOH * eta_AC',
      description: '计算每个年份的毛放电量，考虑容器数量、DOD、RTE、SOH 和 AC 效率。',
      is_builtin: true,
      applicable_scenarios: ['容量配置', '能耗评估'],
      parameters: {
        acEfficiency: { label: 'AC效率', default: 97.03, min: 90, max: 99, unit: '%' }
      }
    },
    {
      id: 'builtin-aux-consumption',
      name: '自辅耗校核模型',
      name_en: 'Auxiliary Consumption Verification',
      model_type: 'aux_consumption',
      category: 'engineering',
      accuracy_level: 'high',
      accuracy_desc: '解析解',
      mathematical_form: 'Aux = (tRun*P_run + tStd*P_std) / 1000',
      description: '根据运行/待机时长和功耗计算单次循环辅助能耗，用于校核 POI 并网点净可用电量。',
      is_builtin: true,
      applicable_scenarios: ['能耗评估', '扩容策略'],
      parameters: {
        bessAuxRun: { label: 'BESS运行功耗', default: 18.124, min: 0, max: 50, unit: 'kW' },
        bessAuxStandby: { label: 'BESS待机功耗', default: 3.5, min: 0, max: 20, unit: 'kW' }
      }
    },
    {
      id: 'builtin-aug-aging',
      name: '增容老化模型',
      name_en: 'Augmentation Aging Model',
      model_type: 'aug_aging',
      category: 'engineering',
      accuracy_level: 'high',
      accuracy_desc: '解析解',
      mathematical_form:
        'E_aug(i) = SUM(k<=i)[Qty_k * RatedEnergy * SOH(i-k) * RTE * DOD * eta_AC - Qty_k * Aux_per_unit]',
      description: '计算每个年份增容资产的老化贡献，按投运年份追踪各批次 SOH 衰减。',
      is_builtin: true,
      applicable_scenarios: ['扩容策略', '容量配置'],
      parameters: {}
    },
    {
      id: 'builtin-soh-config',
      name: 'SOH 曲线配置模型',
      name_en: 'SOH Curve Configuration',
      model_type: 'soh_curve_config',
      category: 'simulation',
      accuracy_level: 'medium',
      accuracy_desc: '用户自定义',
      mathematical_form: 'SOH(t) = user-defined array[0..N]',
      description: '允许用户手工输入或上传 SOH 曲线数据，覆盖算法计算结果。',
      is_builtin: true,
      applicable_scenarios: ['默认配置', '实际运行工况'],
      parameters: {}
    },
    {
      id: 'builtin-rte-config',
      name: 'RTE 曲线配置模型',
      name_en: 'RTE Curve Configuration',
      model_type: 'rte_curve_config',
      category: 'simulation',
      accuracy_level: 'medium',
      accuracy_desc: '用户自定义',
      mathematical_form: 'RTE(t) = user-defined array[0..N]',
      description: '允许用户手工输入或上传 RTE 曲线数据，覆盖算法计算结果。',
      is_builtin: true,
      applicable_scenarios: ['默认配置', '实际运行工况'],
      parameters: {}
    },
    {
      id: 'builtin-temp-factor',
      name: '温度加速因子模型',
      name_en: 'Temperature Acceleration Factor',
      model_type: 'temp_factor',
      category: 'simulation',
      accuracy_level: 'medium',
      accuracy_desc: 'Arrhenius 近似',
      mathematical_form: 'AF = exp(Ea/R * (1/T_ref - 1/T))',
      description: '基于 Arrhenius 方程计算温度对老化速率的加速因子，用于工况修正。',
      is_builtin: true,
      applicable_scenarios: ['温度加速老化', '环境适应性评估', '实际运行工况'],
      parameters: {
        Ea: { label: '活化能', default: 25000, min: 0, max: 100000, unit: 'J/mol' },
        Tref: { label: '参考温度', default: 298.15, min: 250, max: 350, unit: 'K' }
      }
    },
    {
      id: 'builtin-revenue-stack',
      name: '多收入叠加模型',
      name_en: 'Revenue Stack Model',
      model_type: 'revenue_stack',
      category: 'financial',
      accuracy_level: 'medium',
      accuracy_desc: '线性叠加',
      mathematical_form: 'Revenue = Arbitrage + Capacity + Ancillary',
      description: '将能量套利、容量补偿和辅助服务收入线性叠加为总收益。',
      is_builtin: true,
      applicable_scenarios: ['收益建模', '项目评估'],
      parameters: {}
    }
  ]
}

async function fetchAlgorithms() {
  const allAlgorithms = []

  try {
    const data = await api.get('/api/algorithms/public')
    if (data.success && data.data && data.data.length > 0) {
      allAlgorithms.push(...data.data.map((a) => ({ ...a, is_builtin: true })))
    }
  } catch (e) {
    console.error('获取公开算法列表失败:', e)
  }

  const token = sessionStorage.getItem('auth_token')
  if (token) {
    try {
      const data = await api.get('/api/algorithms')
      if (data.success && data.data) {
        const builtinIds = new Set(allAlgorithms.map((a) => a.id))
        data.data.forEach((a) => {
          if (!builtinIds.has(a.id)) allAlgorithms.push(a)
        })
      }
    } catch (e) {
      console.error('获取自定义算法列表失败:', e)
    }
  }

  if (allAlgorithms.length === 0) {
    allAlgorithms.push(...getBuiltinFallback())
  }

  algorithms.value = allAlgorithms
}

async function createAlgorithm() {
  if (!newAlg.name.trim()) {
    showToast('请输入模型名称', 'error')
    return
  }

  const token = sessionStorage.getItem('auth_token')
  if (!token) return

  try {
    const data = await api.post('/api/algorithms', newAlg)
    if (data.success) {
      showToast('算法模型创建成功')
      showAddModal.value = false
      Object.assign(newAlg, {
        name: '',
        name_en: '',
        model_type: 'custom',
        category: 'degradation',
        accuracy_level: 'medium',
        mathematical_form: '',
        formula_expression: '',
        accuracy_desc: '',
        applicable_scenarios: [],
        parameters: {},
        description: ''
      })
      await fetchAlgorithms()
    } else {
      showToast(data.error || '创建失败', 'error')
    }
  } catch (e) {
    showToast('创建失败: ' + e.message, 'error')
  }
}

async function deleteAlgorithm(id) {
  if (!confirm('确定删除该算法模型吗？')) return

  const token = sessionStorage.getItem('auth_token')
  if (!token) return

  try {
    const data = await api.del(`/api/algorithms/${id}`)
    if (data.success) {
      showToast('删除成功')
      await fetchAlgorithms()
    } else {
      showToast(data.error || '删除失败', 'error')
    }
  } catch (e) {
    showToast('删除失败: ' + e.message, 'error')
  }
}

async function initializeBuiltin() {
  const token = sessionStorage.getItem('auth_token')
  if (!token) return

  try {
    const data = await api.post('/api/algorithms/initialize')
    if (data.success) {
      showToast(`成功初始化${data.count}个内置算法`)
      await fetchAlgorithms()
    } else {
      showToast(data.error || '初始化失败', 'error')
    }
  } catch (e) {
    showToast('初始化失败: ' + e.message, 'error')
  }
}

onMounted(() => {
  fetchAlgorithms()
})
</script>
