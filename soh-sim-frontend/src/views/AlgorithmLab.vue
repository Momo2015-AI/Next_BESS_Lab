<template>
  <div class="h-full overflow-y-auto p-4">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg font-bold text-teal-400">算法试验场</h2>
      <button @click="showAddModal = true"
        class="bg-teal-600 hover:bg-teal-700 text-white text-xs px-4 py-2 rounded-lg transition-colors flex items-center gap-2">
        <span>+</span> 添加算法模型
      </button>
    </div>

    <div class="flex gap-2 mb-4 flex-wrap">
      <button v-for="cat in categories" :key="cat.key"
        @click="activeCategory = cat.key"
        :class="['text-xs px-3 py-1.5 rounded-lg transition-all border',
          activeCategory === cat.key
            ? 'bg-teal-500/20 text-teal-400 border-teal-500/40'
            : 'bg-slate-800 text-slate-400 border-slate-700 hover:border-slate-500']">
        {{ cat.label }}
        <span class="ml-1 text-[10px] opacity-50">({{ catCount(cat.key) }})</span>
      </button>
    </div>

    <div v-if="filteredAlgorithms.length === 0" class="text-center py-16 text-slate-500">
      <div class="text-4xl mb-3">&#9312;</div>
      <div>暂无算法模型</div>
      <button @click="initializeBuiltin" class="mt-4 text-teal-400 hover:text-teal-300 text-sm underline">初始化内置算法</button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div v-for="alg in filteredAlgorithms" :key="alg.id"
        class="bg-slate-900/70 border rounded-xl overflow-hidden transition-all duration-200"
        :class="getCardBorderClass(alg.category)">
        <div class="p-4">
          <div class="flex justify-between items-start mb-3">
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 mb-1">
                <h3 class="font-bold text-slate-200 text-sm truncate">{{ alg.name }}</h3>
                <span v-if="alg.is_builtin" class="text-[10px] bg-amber-500/20 text-amber-400 px-1.5 py-0.5 rounded shrink-0">内置</span>
              </div>
              <span :class="['text-[10px] px-1.5 py-0.5 rounded', getCategoryBadgeClass(alg.category)]">
                {{ getCategoryLabel(alg.category) }}
              </span>
            </div>
            <button v-if="!alg.is_builtin" @click="deleteAlgorithm(alg.id)"
              class="text-slate-500 hover:text-red-400 text-xs ml-2 shrink-0">&#10005;</button>
          </div>
          
          <p class="text-xs text-slate-400 leading-relaxed mb-3 line-clamp-3">{{ alg.description || '暂无描述' }}</p>
          
          <div class="grid grid-cols-2 gap-x-3 gap-y-1.5 mb-3 text-[11px]">
            <div>
              <span class="text-slate-500">精度: </span>
              <span :class="getAccuracyClass(alg.accuracy_level)">{{ alg.accuracy_desc || getAccuracyLabel(alg.accuracy_level) }}</span>
            </div>
            <div>
              <span class="text-slate-500">类型: </span>
              <span class="text-slate-300">{{ getModelTypeLabel(alg.model_type) }}</span>
            </div>
            <div v-if="alg.name_en && alg.name_en !== alg.name">
              <span class="text-slate-500">英文: </span>
              <span class="text-slate-300 text-[10px]">{{ alg.name_en }}</span>
            </div>
            <div v-if="alg.mathematical_form">
              <span class="text-slate-500">形式: </span>
              <span class="text-slate-300 font-mono text-[10px]">{{ alg.mathematical_form }}</span>
            </div>
          </div>
          
          <div class="border-t border-slate-800/50 pt-2.5">
            <div class="text-[10px] text-slate-500 mb-1.5">参数 ({{ paramCount(alg.parameters) }}):</div>
            <div class="flex flex-wrap gap-1">
              <span v-for="(param, key) in alg.parameters" :key="key"
                class="text-[10px] bg-slate-800/80 text-slate-300 px-1.5 py-0.5 rounded border border-slate-700/50">
                {{ param.label || key }}={{ param.default }}{{ param.unit }}
              </span>
            </div>
          </div>
          
          <div v-if="alg.applicable_scenarios && alg.applicable_scenarios.length > 0" class="flex flex-wrap gap-1 mt-2">
            <span v-for="scenario in alg.applicable_scenarios" :key="scenario"
              class="text-[10px] bg-teal-500/10 text-teal-400/80 px-1.5 py-0.5 rounded border border-teal-500/20">
              {{ scenario }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div class="text-center text-[10px] text-slate-600 mt-6 mb-4" v-if="filteredAlgorithms.length > 0">
      共 {{ filteredAlgorithms.length }} 个算法模型 | 双击切换分类查看
    </div>

    <!-- 添加算法模型弹窗 -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
      <div class="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center p-4 border-b border-slate-700">
          <h3 class="font-bold text-teal-400">添加算法模型</h3>
          <button @click="showAddModal = false" class="text-slate-500 hover:text-slate-300">&#10005;</button>
        </div>
        
        <div class="p-4 space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="text-xs text-slate-400 block mb-1">模型名称 *</label>
              <input v-model="newAlg.name" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none" placeholder="如: 自定义衰减模型">
            </div>
            <div>
              <label class="text-xs text-slate-400 block mb-1">英文名称</label>
              <input v-model="newAlg.name_en" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none" placeholder="如: Custom Degradation Model">
            </div>
          </div>
          
          <div class="grid grid-cols-3 gap-4">
            <div>
              <label class="text-xs text-slate-400 block mb-1">模型类型</label>
              <select v-model="newAlg.model_type" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none">
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
              <select v-model="newAlg.category" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none">
                <option value="degradation">容量衰减</option>
                <option value="financial">财务模型</option>
                <option value="engineering">工程计算</option>
                <option value="simulation">仿真配置</option>
              </select>
            </div>
            <div>
              <label class="text-xs text-slate-400 block mb-1">精度等级</label>
              <select v-model="newAlg.accuracy_level" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none">
                <option value="high">高</option>
                <option value="medium">中</option>
                <option value="low">低</option>
              </select>
            </div>
          </div>
          
          <div>
            <label class="text-xs text-slate-400 block mb-1">数学形式</label>
            <input v-model="newAlg.mathematical_form" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none font-mono" placeholder="如: SOH(t) = A*e^(-kt) + B">
          </div>
          
          <div>
            <label class="text-xs text-slate-400 block mb-1">公式表达式 (JavaScript)</label>
            <textarea v-model="newAlg.formula_expression" rows="2" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none font-mono" placeholder="如: A * Math.exp(-k * t) + B"></textarea>
          </div>
          
          <div>
            <label class="text-xs text-slate-400 block mb-1">精度描述</label>
            <input v-model="newAlg.accuracy_desc" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none" placeholder="如: R^2>0.99">
          </div>
          
          <div>
            <label class="text-xs text-slate-400 block mb-1">适用场景</label>
            <div class="flex flex-wrap gap-2">
              <button v-for="scenario in availableScenarios" :key="scenario"
                @click="toggleScenario(scenario)"
                :class="['text-xs px-3 py-1 rounded transition-colors',
                  newAlg.applicable_scenarios.includes(scenario) 
                    ? 'bg-teal-600 text-white' 
                    : 'bg-slate-800 text-slate-400 hover:bg-slate-700']">
                {{ scenario }}
              </button>
            </div>
          </div>
          
          <div>
            <div class="flex justify-between items-center mb-2">
              <label class="text-xs text-slate-400">参数定义</label>
              <button @click="addParameter" class="text-teal-400 hover:text-teal-300 text-xs">+ 添加参数</button>
            </div>
            <div v-if="Object.keys(newAlg.parameters).length > 0" class="space-y-2">
              <div v-for="(param, key) in newAlg.parameters" :key="key" class="flex gap-2 items-center">
                <input v-model="param.label" class="bg-slate-800 border border-slate-700 rounded px-2 py-1 text-xs w-28" placeholder="参数名">
                <input v-model.number="param.default" type="number" class="bg-slate-800 border border-slate-700 rounded px-2 py-1 text-xs w-20" placeholder="默认值">
                <input v-model.number="param.min" type="number" class="bg-slate-800 border border-slate-700 rounded px-2 py-1 text-xs w-16" placeholder="最小值">
                <input v-model.number="param.max" type="number" class="bg-slate-800 border border-slate-700 rounded px-2 py-1 text-xs w-16" placeholder="最大值">
                <input v-model="param.unit" class="bg-slate-800 border border-slate-700 rounded px-2 py-1 text-xs w-16" placeholder="单位">
                <button @click="removeParameter(key)" class="text-red-400 hover:text-red-300">&#10005;</button>
              </div>
            </div>
            <div v-else class="text-slate-500 text-xs text-center py-4">-- 点击上方按钮添加参数 --</div>
          </div>
          
          <div>
            <label class="text-xs text-slate-400 block mb-1">描述（支持中文说明）</label>
            <textarea v-model="newAlg.description" rows="3" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none" placeholder="模型描述..."></textarea>
          </div>
        </div>
        
        <div class="flex justify-end gap-3 p-4 border-t border-slate-700">
          <button @click="showAddModal = false" class="text-slate-400 hover:text-slate-200 text-sm px-4 py-2 rounded">取消</button>
          <button @click="createAlgorithm" class="bg-teal-600 hover:bg-teal-700 text-white text-sm px-4 py-2 rounded transition-colors">创建</button>
        </div>
      </div>
    </div>

    <!-- 提示框 -->
    <div v-if="toast.show" 
      :class="['fixed top-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all',
        toast.type === 'success' ? 'bg-emerald-500 text-white' : 'bg-red-500 text-white']">
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'

const algorithms = ref([])
const showAddModal = ref(false)
const activeCategory = ref('degradation')
const toast = reactive({ show: false, message: '', type: 'success' })

const categories = [
  { key: 'degradation', label: '容量衰减' },
  { key: 'financial', label: '财务模型' },
  { key: 'engineering', label: '工程计算' },
  { key: 'simulation', label: '仿真配置' },
]

const filteredAlgorithms = computed(() => {
  if (!activeCategory.value) return algorithms.value
  return algorithms.value.filter(a => a.category === activeCategory.value)
})

function catCount(key) {
  return algorithms.value.filter(a => a.category === key).length
}

const availableScenarios = [
  'LFP日历衰减', '循环衰减', '综合衰减预测', 'RTE衰减', '效率衰减建模',
  '温度加速老化', '日历寿命预测', '不规则循环损伤', '实际运行工况', '多应力耦合',
  '投资决策', '项目评估', '经济性对标', '融资审批', '收益建模',
  '容量配置', '能耗评估', '扩容策略', '默认配置', '环境适应性评估',
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
  description: '',
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
    custom: '自定义',
  }
  return labels[type] || type
}

function getCategoryLabel(category) {
  const labels = {
    degradation: '容量衰减',
    financial: '财务模型',
    engineering: '工程计算',
    simulation: '仿真配置',
  }
  return labels[category] || category
}

function getCategoryBadgeClass(category) {
  const classes = {
    degradation: 'bg-blue-500/15 text-blue-400 border border-blue-500/30',
    financial: 'bg-amber-500/15 text-amber-400 border border-amber-500/30',
    engineering: 'bg-purple-500/15 text-purple-400 border border-purple-500/30',
    simulation: 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30',
  }
  return classes[category] || 'bg-slate-700 text-slate-400'
}

function getCardBorderClass(category) {
  const classes = {
    degradation: 'border-blue-500/20 hover:border-blue-500/50',
    financial: 'border-amber-500/20 hover:border-amber-500/50',
    engineering: 'border-purple-500/20 hover:border-purple-500/50',
    simulation: 'border-emerald-500/20 hover:border-emerald-500/50',
  }
  return classes[category] || 'border-slate-800 hover:border-slate-600'
}

function getAccuracyClass(level) {
  const classes = {
    high: 'text-emerald-400',
    medium: 'text-amber-400',
    low: 'text-red-400',
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
    unit: '',
  }
}

function removeParameter(key) {
  delete newAlg.parameters[key]
}

function showToast(message, type = 'success') {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => { toast.show = false }, 3000)
}

async function fetchAlgorithms() {
  const token = localStorage.getItem('token')
  if (!token) return
  
  try {
    const res = await fetch('http://localhost:5001/api/algorithms', {
      headers: { Authorization: `Bearer ${token}` },
    })
    const data = await res.json()
    if (data.success) {
      algorithms.value = data.data
    }
  } catch (e) {
    console.error('获取算法列表失败:', e)
  }
}

async function createAlgorithm() {
  if (!newAlg.name.trim()) {
    showToast('请输入模型名称', 'error')
    return
  }
  
  const token = localStorage.getItem('token')
  if (!token) return
  
  try {
    const res = await fetch('http://localhost:5001/api/algorithms', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(newAlg),
    })
    const data = await res.json()
    if (data.success) {
      showToast('算法模型创建成功')
      showAddModal.value = false
      Object.assign(newAlg, {
        name: '', name_en: '', model_type: 'custom', category: 'degradation',
        accuracy_level: 'medium', mathematical_form: '', formula_expression: '',
        accuracy_desc: '', applicable_scenarios: [], parameters: {}, description: '',
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
  
  const token = localStorage.getItem('token')
  if (!token) return
  
  try {
    const res = await fetch(`http://localhost:5001/api/algorithms/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` },
    })
    const data = await res.json()
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
  const token = localStorage.getItem('token')
  if (!token) return
  
  try {
    const res = await fetch('http://localhost:5001/api/algorithms/initialize', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
    })
    const data = await res.json()
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
