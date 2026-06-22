<template>
  <div class="h-full overflow-y-auto p-4">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg font-bold text-teal-400">算法公式试验舱</h2>
      <button @click="showAddModal = true"
        class="bg-teal-600 hover:bg-teal-700 text-white text-xs px-4 py-2 rounded-lg transition-colors flex items-center gap-2">
        <span>+</span> 添加算法模型
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="alg in algorithms" :key="alg.id"
        class="bg-slate-900/70 border border-slate-800 rounded-xl p-4 hover:border-teal-500/50 transition-colors">
        <div class="flex justify-between items-start mb-2">
          <div>
            <h3 class="font-bold text-slate-200">{{ alg.name }}</h3>
            <span v-if="alg.is_builtin" class="inline-block text-[10px] bg-amber-500/20 text-amber-400 px-2 py-0.5 rounded mt-1">内置</span>
          </div>
          <button v-if="!alg.is_builtin" @click="deleteAlgorithm(alg.id)"
            class="text-slate-500 hover:text-red-400 text-xs">✕</button>
        </div>
        
        <div class="text-xs space-y-1.5">
          <div><span class="text-slate-500">模型类型:</span> <span class="text-slate-300">{{ getModelTypeLabel(alg.model_type) }}</span></div>
          <div><span class="text-slate-500">精度:</span> <span :class="getAccuracyClass(alg.accuracy_level)">{{ alg.accuracy_desc }}</span></div>
          <div><span class="text-slate-500">适用场景:</span></div>
          <div class="flex flex-wrap gap-1">
            <span v-for="scenario in alg.applicable_scenarios" :key="scenario"
              class="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded">{{ scenario }}</span>
          </div>
          <div class="mt-2 pt-2 border-t border-slate-800">
            <span class="text-slate-500">数学形式:</span>
            <div class="font-mono text-teal-400 mt-1 text-[11px]">{{ alg.mathematical_form }}</div>
          </div>
          <div class="mt-2">
            <span class="text-slate-500">参数:</span>
            <div class="flex flex-wrap gap-1 mt-1">
              <span v-for="(param, key) in alg.parameters" :key="key"
                class="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded">{{ param.label }}={{ param.default }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="algorithms.length === 0" class="text-center py-12 text-slate-500">
      <div class="text-4xl mb-2">📊</div>
      <div>暂无算法模型</div>
      <button @click="initializeBuiltin" class="mt-4 text-teal-400 hover:text-teal-300 text-sm">初始化内置算法</button>
    </div>

    <!-- 添加算法模型弹窗 -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
      <div class="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center p-4 border-b border-slate-700">
          <h3 class="font-bold text-teal-400">添加算法模型</h3>
          <button @click="showAddModal = false" class="text-slate-500 hover:text-slate-300">✕</button>
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
              </select>
            </div>
            <div>
              <label class="text-xs text-slate-400 block mb-1">分类</label>
              <select v-model="newAlg.category" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none">
                <option value="soh">SOH衰减</option>
                <option value="rte">RTE衰减</option>
                <option value="comprehensive">综合模型</option>
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
            <input v-model="newAlg.mathematical_form" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none font-mono" placeholder="如: SOH(t) = A·e^(-kt) + B">
          </div>
          
          <div>
            <label class="text-xs text-slate-400 block mb-1">公式表达式 (JavaScript)</label>
            <textarea v-model="newAlg.formula_expression" rows="3" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none font-mono" placeholder="如: A * Math.exp(-k * t) + B"></textarea>
          </div>
          
          <div>
            <label class="text-xs text-slate-400 block mb-1">精度描述</label>
            <input v-model="newAlg.accuracy_desc" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none" placeholder="如: R²>0.99">
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
                <input v-model="param.unit" class="bg-slate-800 border border-slate-700 rounded px-2 py-1 text-xs w-12" placeholder="单位">
                <button @click="removeParameter(key)" class="text-red-400 hover:text-red-300">✕</button>
              </div>
            </div>
            <div v-else class="text-slate-500 text-xs text-center py-4">点击上方按钮添加参数</div>
          </div>
          
          <div>
            <label class="text-xs text-slate-400 block mb-1">描述</label>
            <textarea v-model="newAlg.description" rows="2" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm focus:border-teal-500 focus:outline-none" placeholder="模型描述..."></textarea>
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
import { ref, reactive, onMounted } from 'vue'

const algorithms = ref([])
const showAddModal = ref(false)
const toast = reactive({ show: false, message: '', type: 'success' })

const availableScenarios = [
  'LFP日历衰减', '循环衰减', '综合衰减', 'RTE衰减', '效率衰减',
  '温度加速衰减', '日历老化', '不规则循环损伤', '实际工况', '多应力耦合'
]

const newAlg = reactive({
  name: '',
  name_en: '',
  model_type: 'custom',
  category: 'soh',
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
    custom: '自定义',
  }
  return labels[type] || type
}

function getAccuracyClass(level) {
  const classes = {
    high: 'text-emerald-400',
    medium: 'text-amber-400',
    low: 'text-red-400',
  }
  return classes[level] || 'text-slate-400'
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
      newAlg.name = ''
      newAlg.name_en = ''
      newAlg.model_type = 'custom'
      newAlg.category = 'soh'
      newAlg.accuracy_level = 'medium'
      newAlg.mathematical_form = ''
      newAlg.formula_expression = ''
      newAlg.accuracy_desc = ''
      newAlg.applicable_scenarios = []
      newAlg.parameters = {}
      newAlg.description = ''
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
