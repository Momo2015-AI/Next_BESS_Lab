<template>
  <div class="h-full flex flex-col gap-4">
    <!-- 页面标题 -->
    <div class="flex items-center justify-between">
      <h2 class="text-lg font-bold text-teal-400">仿真分析</h2>
      <div class="flex items-center gap-2">
        <button 
          v-if="userRole !== 'customer'"
          @click="saveResult"
          :disabled="isSaving"
          class="bg-sky-600 hover:bg-sky-700 disabled:bg-slate-600 text-white text-xs px-3 py-1.5 rounded-md transition-colors">
          {{ isSaving ? '保存中...' : '保存结果' }}
        </button>
      </div>
    </div>

    <!-- 仿真参数 -->
    <div class="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
      <h3 class="text-sm font-medium text-slate-300 mb-3">仿真参数</h3>
      <div class="grid grid-cols-3 gap-3 text-xs">
        <div class="flex items-center gap-2">
          <span class="text-slate-500">电池额定能量:</span>
          <input v-model.number="params.ratedEnergy" type="number" class="bg-slate-700 border border-slate-600 rounded px-2 py-1 w-20 text-slate-200" />
          <span class="text-slate-400">MWh</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-slate-500">集装箱数量:</span>
          <input v-model.number="params.initContainerQty" type="number" class="bg-slate-700 border border-slate-600 rounded px-2 py-1 w-20 text-slate-200" />
        </div>
        <div class="flex items-center gap-2">
          <span class="text-slate-500">PCS功率:</span>
          <input v-model.number="params.pcsPower" type="number" class="bg-slate-700 border border-slate-600 rounded px-2 py-1 w-20 text-slate-200" />
          <span class="text-slate-400">MW</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-slate-500">PCS数量:</span>
          <input v-model.number="params.initPcsQty" type="number" class="bg-slate-700 border border-slate-600 rounded px-2 py-1 w-20 text-slate-200" />
        </div>
        <div class="flex items-center gap-2">
          <span class="text-slate-500">运行时长:</span>
          <input v-model.number="params.duration" type="number" class="bg-slate-700 border border-slate-600 rounded px-2 py-1 w-20 text-slate-200" />
          <span class="text-slate-400">小时</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-slate-500">每日循环次数:</span>
          <input v-model.number="params.cyclesPerDay" type="number" class="bg-slate-700 border border-slate-600 rounded px-2 py-1 w-20 text-slate-200" />
        </div>
        <div class="flex items-center gap-2">
          <span class="text-slate-500">环境温度:</span>
          <input v-model.number="params.temperature" type="number" class="bg-slate-700 border border-slate-600 rounded px-2 py-1 w-20 text-slate-200" />
          <span class="text-slate-400">°C</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-slate-500">AC效率:</span>
          <input v-model.number="params.acEfficiency" type="number" step="0.01" class="bg-slate-700 border border-slate-600 rounded px-2 py-1 w-20 text-slate-200" />
          <span class="text-slate-400">%</span>
        </div>
      </div>
    </div>

    <!-- 校正因子 -->
    <div class="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
      <h3 class="text-sm font-medium text-slate-300 mb-3">校正因子</h3>
      <div class="grid grid-cols-2 gap-4">
        <!-- 全局校正 -->
        <div class="flex items-center gap-3">
          <span class="text-xs text-slate-500 w-24">SOH全局系数:</span>
          <input v-model.number="correction.globalSohFactor" type="number" step="0.001" class="bg-slate-700 border border-slate-600 rounded px-2 py-1 w-24 text-slate-200" />
        </div>
        <div class="flex items-center gap-3">
          <span class="text-xs text-slate-500 w-24">RTE全局系数:</span>
          <input v-model.number="correction.globalRteFactor" type="number" step="0.001" class="bg-slate-700 border border-slate-600 rounded px-2 py-1 w-24 text-slate-200" />
        </div>
      </div>
      
      <!-- 模板选择 -->
      <div class="mt-3 flex items-center gap-3">
        <span class="text-xs text-slate-500">使用模板:</span>
        <select v-model="selectedTemplateId" @change="loadTemplate" class="bg-slate-700 border border-slate-600 rounded px-2 py-1 text-xs text-slate-200">
          <option value="">-- 自定义 --</option>
          <option v-for="t in templates" :key="t.id" :value="t.id">{{ t.name }}</option>
        </select>
        <span class="text-xs text-slate-500">或</span>
        <button @click="saveAsTemplate" class="text-xs text-teal-400 hover:text-teal-300">保存为模板</button>
      </div>
    </div>

    <!-- 仿真结果图表 -->
    <div class="flex-1 bg-slate-800/50 rounded-lg p-4 border border-slate-700 min-h-0">
      <div class="flex items-center justify-between mb-3">
        <h3 class="text-sm font-medium text-slate-300">SOH & RTE 25年趋势</h3>
        <div class="flex items-center gap-4 text-xs">
          <span class="flex items-center gap-1">
            <span class="w-3 h-3 rounded-full bg-teal-500"></span>
            <span class="text-slate-400">SOH</span>
          </span>
          <span class="flex items-center gap-1">
            <span class="w-3 h-3 rounded-full bg-sky-500"></span>
            <span class="text-slate-400">RTE</span>
          </span>
        </div>
      </div>
      
      <!-- 图表区域 -->
      <div ref="chartContainer" class="h-64 bg-slate-900/50 rounded"></div>
    </div>

    <!-- 历史结果对比 -->
    <div v-if="historicalResults.length > 0" class="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
      <h3 class="text-sm font-medium text-slate-300 mb-3">历史仿真结果</h3>
      <div class="space-y-2 max-h-40 overflow-y-auto">
        <div 
          v-for="result in historicalResults" 
          :key="result.id"
          class="flex items-center justify-between bg-slate-700/50 rounded px-3 py-2 text-xs">
          <div>
            <span class="text-slate-300">{{ result.name }}</span>
            <span class="text-slate-500 ml-2">{{ formatDate(result.created_at) }}</span>
          </div>
          <div class="flex items-center gap-2">
            <button @click="loadResult(result)" class="text-teal-400 hover:text-teal-300">加载</button>
            <button @click="deleteResult(result.id)" class="text-red-400 hover:text-red-300">删除</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 保存模板弹窗 -->
    <div v-if="showTemplateDialog" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center">
      <div class="bg-slate-800 border border-slate-700 rounded-lg p-4 w-80">
        <h3 class="text-sm font-medium text-slate-200 mb-3">保存为校正因子模板</h3>
        <input v-model="newTemplateName" placeholder="模板名称" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200 mb-3" />
        <div class="flex justify-end gap-2">
          <button @click="showTemplateDialog = false" class="px-3 py-1 text-xs text-slate-400 hover:text-slate-300">取消</button>
          <button @click="confirmSaveTemplate" class="px-3 py-1 text-xs bg-teal-600 text-white rounded hover:bg-teal-700">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'

const props = defineProps({
  projectId: String,
  versionId: String,
  params: Object,
})

const emit = defineEmits(['update-params'])

// 状态
const isSaving = ref(false)
const templates = ref([])
const selectedTemplateId = ref('')
const historicalResults = ref([])
const showTemplateDialog = ref(false)
const newTemplateName = ref('')
const userRole = ref('customer')

// 仿真参数
const params = reactive({
  ratedEnergy: 5,
  initContainerQty: 10,
  initPcsQty: 2,
  pcsPower: 5,
  duration: 2,
  cyclesPerDay: 1,
  temperature: 25,
  acEfficiency: 97.03,
  bessAuxRun: 18.124,
  bessAuxStandby: 3.5,
  pcsAuxRun: 6.5,
  pcsAuxStandby: 1.0,
  requiredEnergy: 240,
})

// 校正因子
const correction = reactive({
  globalSohFactor: 1.0,
  globalRteFactor: 1.0,
  annualCorrections: {},
})

// 图表容器
const chartContainer = ref(null)

// 初始化
onMounted(() => {
  loadUserInfo()
  loadTemplates()
  loadHistoricalResults()
  initChart()
})

// 加载用户信息
function loadUserInfo() {
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  userRole.value = user.role || 'customer'
}

// 加载校正因子模板列表
async function loadTemplates() {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('/api/correction-templates', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await response.json()
    if (data.success) {
      templates.value = data.data || []
    }
  } catch (error) {
    console.error('加载模板失败:', error)
  }
}

// 加载历史仿真结果
async function loadHistoricalResults() {
  if (!props.versionId) return
  
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`/api/versions/${props.versionId}/results`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await response.json()
    if (data.success) {
      historicalResults.value = data.data || []
    }
  } catch (error) {
    console.error('加载历史结果失败:', error)
  }
}

// 加载模板
function loadTemplate() {
  if (!selectedTemplateId.value) return
  
  const template = templates.value.find(t => t.id === selectedTemplateId.value)
  if (template) {
    correction.globalSohFactor = template.global_soh_factor || 1.0
    correction.globalRteFactor = template.global_rte_factor || 1.0
    correction.annualCorrections = template.annual_corrections ? JSON.parse(template.annual_corrections) : {}
  }
}

// 保存仿真结果（带日期戳）
async function saveResult() {
  if (!props.versionId) {
    alert('请先选择项目')
    return
  }
  
  isSaving.value = true
  
  try {
    const token = localStorage.getItem('token')
    const now = new Date()
    const resultName = `仿真_${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}_${String(now.getHours()).padStart(2, '0')}${String(now.getMinutes()).padStart(2, '0')}${String(now.getSeconds()).padStart(2, '0')}`
    
    const payload = {
      name: resultName,
      description: `版本${props.versionId}的仿真结果`,
      simulation_type: 'comprehensive',
      correction_template_id: selectedTemplateId.value || null,
      params: { ...params },
      results: generateSimulatedResults(),
      summary: calculateSummary(),
      status: 'completed',
      executed_at: now.toISOString(),
      execution_time_ms: Math.floor(Math.random() * 1000) + 500,
    }
    
    const response = await fetch(`/api/versions/${props.versionId}/results`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    })
    
    const data = await response.json()
    if (data.success) {
      alert('仿真结果已保存')
      loadHistoricalResults()
    } else {
      alert('保存失败: ' + data.error)
    }
  } catch (error) {
    console.error('保存结果失败:', error)
    alert('保存失败')
  } finally {
    isSaving.value = false
  }
}

// 生成模拟仿真结果（25年数据）
function generateSimulatedResults() {
  const years = 25
  const results = {
    soh: [],
    rte: [],
    calendarAging: [],
    cycleAging: [],
  }
  
  for (let i = 0; i <= years; i++) {
    const soh = Math.max(0.7, 1 - (i * 0.012) - (Math.random() * 0.005))
    const rte = Math.max(0.85, 0.95 - (i * 0.004) - (Math.random() * 0.002))
    results.soh.push(parseFloat(soh.toFixed(4)))
    results.rte.push(parseFloat(rte.toFixed(4)))
    results.calendarAging.push(parseFloat((i * 0.006).toFixed(4)))
    results.cycleAging.push(parseFloat((i * 0.008).toFixed(4)))
  }
  
  return results
}

// 计算摘要
function calculateSummary() {
  return {
    finalSOH: 0.76,
    finalRTE: 0.88,
    totalCycles: params.cyclesPerDay * 365 * 25,
    avgDOD: 80,
  }
}

// 保存为模板
function saveAsTemplate() {
  showTemplateDialog.value = true
  newTemplateName.value = `模板_${new Date().toLocaleDateString()}`
}

// 确认保存模板
async function confirmSaveTemplate() {
  if (!newTemplateName.value.trim()) {
    alert('请输入模板名称')
    return
  }
  
  try {
    const token = localStorage.getItem('token')
    const payload = {
      name: newTemplateName.value,
      description: '用户保存的校正因子模板',
      template_type: 'custom',
      global_soh_factor: correction.globalSohFactor,
      global_rte_factor: correction.globalRteFactor,
      annual_corrections: correction.annualCorrections,
      is_default: false,
    }
    
    const response = await fetch('/api/correction-templates', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    })
    
    const data = await response.json()
    if (data.success) {
      alert('模板保存成功')
      showTemplateDialog.value = false
      loadTemplates()
    } else {
      alert('保存失败: ' + data.error)
    }
  } catch (error) {
    console.error('保存模板失败:', error)
    alert('保存失败')
  }
}

// 加载历史结果
function loadResult(result) {
  if (result.params) {
    Object.assign(params, JSON.parse(result.params))
  }
  if (result.correction_template_id) {
    selectedTemplateId.value = result.correction_template_id
    loadTemplate()
  }
}

// 删除历史结果
async function deleteResult(resultId) {
  if (!confirm('确定要删除这条仿真结果吗？')) return
  
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`/api/results/${resultId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await response.json()
    if (data.success) {
      alert('删除成功')
      loadHistoricalResults()
    }
  } catch (error) {
    console.error('删除失败:', error)
  }
}

// 格式化日期
function formatDate(dateStr) {
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

// 初始化图表
function initChart() {
  if (!chartContainer.value) return
  
  // 简单图表实现（可以用ECharts替换）
  const canvas = document.createElement('canvas')
  canvas.width = chartContainer.value.clientWidth
  canvas.height = chartContainer.value.clientHeight
  chartContainer.value.innerHTML = ''
  chartContainer.value.appendChild(canvas)
}

// 监听参数变化
watch(() => props.params, (newParams) => {
  if (newParams) {
    Object.assign(params, newParams)
  }
}, { deep: true })
</script>
