<template>
  <div class="h-full overflow-y-auto p-4">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg font-bold" style="color: var(--color-accent);">算法公式试验舱</h2>
      <button @click="showAddModal = true"
        class="text-xs px-4 py-2 rounded-lg transition-colors flex items-center gap-2"
        style="background-color: var(--color-accent); color: white;"
        onmouseover="this.style.opacity='0.9';"
        onmouseout="this.style.opacity='1';">
        <span>+</span> 添加算法模型
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="alg in algorithms" :key="alg.id"
        class="rounded-xl p-4 transition-colors"
        style="background-color: var(--color-card); border: 1px solid var(--color-border);"
        onmouseover="this.style.borderColor='var(--color-accent)';"
        onmouseout="this.style.borderColor='var(--color-border)';">
        <div class="flex justify-between items-start mb-2">
          <div>
            <h3 class="font-bold" style="color: var(--color-text);">{{ alg.name }}</h3>
            <span v-if="alg.is_builtin" class="inline-block text-[10px] px-2 py-0.5 rounded mt-1" style="background-color: rgba(245, 158, 11, 0.2); color: #f59e0b;">内置</span>
          </div>
          <button v-if="!alg.is_builtin" @click="deleteAlgorithm(alg.id)"
            class="text-xs" style="color: var(--color-text-muted);"
            onmouseover="this.style.color='var(--color-danger)';"
            onmouseout="this.style.color='var(--color-text-muted)';">✕</button>
        </div>
        
        <div class="text-xs space-y-1.5">
          <div><span style="color: var(--color-text-muted);">模型类型:</span> <span style="color: var(--color-text-secondary);">{{ getModelTypeLabel(alg.model_type) }}</span></div>
          <div><span style="color: var(--color-text-muted);">精度:</span> <span :class="getAccuracyClass(alg.accuracy_level)">{{ alg.accuracy_desc }}</span></div>
          <div><span style="color: var(--color-text-muted);">适用场景:</span></div>
          <div class="flex flex-wrap gap-1">
            <span v-for="scenario in alg.applicable_scenarios" :key="scenario"
              class="text-[10px] px-2 py-0.5 rounded" style="background-color: var(--color-card-dark); color: var(--color-text-secondary);">{{ scenario }}</span>
          </div>
          <div class="mt-2 pt-2" style="border-top: 1px solid var(--color-border);">
            <span style="color: var(--color-text-muted);">数学形式:</span>
            <div class="font-mono mt-1 text-[11px]" style="color: var(--color-accent);">{{ alg.mathematical_form }}</div>
          </div>
          <div class="mt-2">
            <span style="color: var(--color-text-muted);">参数:</span>
            <div class="flex flex-wrap gap-1 mt-1">
              <span v-for="(param, key) in alg.parameters" :key="key"
                class="text-[10px] px-2 py-0.5 rounded" style="background-color: var(--color-card-dark); color: var(--color-text-secondary);">{{ param.label }}={{ param.default }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="algorithms.length === 0" class="text-center py-12" style="color: var(--color-text-muted);">
      <div class="text-4xl mb-2">📊</div>
      <div>暂无算法模型</div>
      <button @click="initializeBuiltin" class="mt-4 text-sm" style="color: var(--color-accent);"
        onmouseover="this.style.opacity='0.8';"
        onmouseout="this.style.opacity='1';">初始化内置算法</button>
    </div>

    <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center p-4" style="background-color: var(--color-modal-overlay);">
      <div class="rounded-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto" style="background-color: var(--color-modal-bg); border: 1px solid var(--color-border);">
        <div class="flex justify-between items-center p-4" style="border-bottom: 1px solid var(--color-border);">
          <h3 class="font-bold" style="color: var(--color-accent);">添加算法模型</h3>
          <button @click="showAddModal = false" class="text-xs" style="color: var(--color-text-muted);"
            onmouseover="this.style.color='var(--color-text)';">✕</button>
        </div>
        
        <div class="p-4 space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="text-xs block mb-1" style="color: var(--color-text-secondary);">模型名称 *</label>
              <input v-model="newAlg.name" class="w-full rounded px-3 py-2 text-sm" 
                style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border);"
                onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                onblur="this.style.borderColor='var(--color-input-border)';"
                placeholder="如: 自定义衰减模型">
            </div>
            <div>
              <label class="text-xs block mb-1" style="color: var(--color-text-secondary);">英文名称</label>
              <input v-model="newAlg.name_en" class="w-full rounded px-3 py-2 text-sm" 
                style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border);"
                onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                onblur="this.style.borderColor='var(--color-input-border)';"
                placeholder="如: Custom Degradation Model">
            </div>
          </div>
          
          <div class="grid grid-cols-3 gap-4">
            <div>
              <label class="text-xs block mb-1" style="color: var(--color-text-secondary);">模型类型</label>
              <select v-model="newAlg.model_type" class="w-full rounded px-3 py-2 text-sm" 
                style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border);"
                onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                onblur="this.style.borderColor='var(--color-input-border)';">
                <option value="custom">自定义 Custom</option>
                <option value="double_exponential">双指数模型</option>
                <option value="linear_log">线性-对数模型</option>
                <option value="arrhenius">Arrhenius模型</option>
                <option value="rainflow">雨流计数法</option>
                <option value="semi_empirical">半经验模型</option>
              </select>
            </div>
            <div>
              <label class="text-xs block mb-1" style="color: var(--color-text-secondary);">分类</label>
              <select v-model="newAlg.category" class="w-full rounded px-3 py-2 text-sm" 
                style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border);"
                onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                onblur="this.style.borderColor='var(--color-input-border)';">
                <option value="soh">SOH衰减</option>
                <option value="rte">RTE衰减</option>
                <option value="comprehensive">综合模型</option>
              </select>
            </div>
            <div>
              <label class="text-xs block mb-1" style="color: var(--color-text-secondary);">精度等级</label>
              <select v-model="newAlg.accuracy_level" class="w-full rounded px-3 py-2 text-sm" 
                style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border);"
                onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                onblur="this.style.borderColor='var(--color-input-border)';">
                <option value="high">高</option>
                <option value="medium">中</option>
                <option value="low">低</option>
              </select>
            </div>
          </div>
          
          <div>
            <label class="text-xs block mb-1" style="color: var(--color-text-secondary);">数学形式</label>
            <input v-model="newAlg.mathematical_form" class="w-full rounded px-3 py-2 text-sm font-mono" 
              style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border);"
              onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
              onblur="this.style.borderColor='var(--color-input-border)';"
              placeholder="如: SOH(t) = A·e^(-kt) + B">
          </div>
          
          <div>
            <label class="text-xs block mb-1" style="color: var(--color-text-secondary);">公式表达式 (JavaScript)</label>
            <textarea v-model="newAlg.formula_expression" rows="3" class="w-full rounded px-3 py-2 text-sm font-mono" 
              style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border);"
              onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
              onblur="this.style.borderColor='var(--color-input-border)';"
              placeholder="如: A * Math.exp(-k * t) + B"></textarea>
          </div>
          
          <div>
            <label class="text-xs block mb-1" style="color: var(--color-text-secondary);">精度描述</label>
            <input v-model="newAlg.accuracy_desc" class="w-full rounded px-3 py-2 text-sm" 
              style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border);"
              onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
              onblur="this.style.borderColor='var(--color-input-border)';"
              placeholder="如: R²>0.99">
          </div>
          
          <div>
            <label class="text-xs block mb-1" style="color: var(--color-text-secondary);">适用场景</label>
            <div class="flex flex-wrap gap-2">
              <button v-for="scenario in availableScenarios" :key="scenario"
                @click="toggleScenario(scenario)"
                class="text-xs px-3 py-1 rounded transition-colors"
                :style="newAlg.applicable_scenarios.includes(scenario) ? { backgroundColor: 'var(--color-accent)', color: 'white' } : { backgroundColor: 'var(--color-card-dark)', color: 'var(--color-text-secondary)' }">
                {{ scenario }}
              </button>
            </div>
          </div>
          
          <div>
            <div class="flex justify-between items-center mb-2">
              <label class="text-xs" style="color: var(--color-text-secondary);">参数定义</label>
              <button @click="addParameter" class="text-xs" style="color: var(--color-accent);"
                onmouseover="this.style.opacity='0.8';"
                onmouseout="this.style.opacity='1';">+ 添加参数</button>
            </div>
            <div v-if="Object.keys(newAlg.parameters).length > 0" class="space-y-2">
              <div v-for="(param, key) in newAlg.parameters" :key="key" class="flex gap-2 items-center">
                <input v-model="param.label" class="rounded px-2 py-1 text-xs w-28" 
                  style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border);"
                  onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                  onblur="this.style.borderColor='var(--color-input-border)';"
                  placeholder="参数名">
                <input v-model.number="param.default" type="number" class="rounded px-2 py-1 text-xs w-20" 
                  style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border);"
                  onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                  onblur="this.style.borderColor='var(--color-input-border)';"
                  placeholder="默认值">
                <input v-model.number="param.min" type="number" class="rounded px-2 py-1 text-xs w-16" 
                  style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border);"
                  onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                  onblur="this.style.borderColor='var(--color-input-border)';"
                  placeholder="最小值">
                <input v-model.number="param.max" type="number" class="rounded px-2 py-1 text-xs w-16" 
                  style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border);"
                  onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                  onblur="this.style.borderColor='var(--color-input-border)';"
                  placeholder="最大值">
                <input v-model="param.unit" class="rounded px-2 py-1 text-xs w-12" 
                  style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border);"
                  onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                  onblur="this.style.borderColor='var(--color-input-border)';"
                  placeholder="单位">
                <button @click="removeParameter(key)" class="text-xs" style="color: var(--color-danger);"
                  onmouseover="this.style.opacity='0.8';"
                  onmouseout="this.style.opacity='1';">✕</button>
              </div>
            </div>
            <div v-else class="text-xs text-center py-4" style="color: var(--color-text-muted);">点击上方按钮添加参数</div>
          </div>
          
          <div>
            <label class="text-xs block mb-1" style="color: var(--color-text-secondary);">描述</label>
            <textarea v-model="newAlg.description" rows="2" class="w-full rounded px-3 py-2 text-sm" 
              style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border);"
              onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
              onblur="this.style.borderColor='var(--color-input-border)';"
              placeholder="模型描述..."></textarea>
          </div>
        </div>
        
        <div class="flex justify-end gap-3 p-4" style="border-top: 1px solid var(--color-border);">
          <button @click="showAddModal = false" class="text-sm px-4 py-2 rounded" style="color: var(--color-text-secondary);"
            onmouseover="this.style.color='var(--color-text)';">取消</button>
          <button @click="createAlgorithm" class="text-sm px-4 py-2 rounded transition-colors"
            style="background-color: var(--color-accent); color: white;"
            onmouseover="this.style.opacity='0.9';"
            onmouseout="this.style.opacity='1';">创建</button>
        </div>
      </div>
    </div>

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
  fetchCalculation()
})
</script>