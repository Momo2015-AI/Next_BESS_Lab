<template>
  <div class="scenario-compare h-full overflow-auto p-4">
    <div class="bg-slate-900/60 rounded-lg border border-slate-800 p-4">
      <h3 class="text-sm font-bold text-teal-400 mb-4 flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-teal-400"></span>
        多场景对比分析
      </h3>

      <!-- 场景管理 -->
      <div class="grid grid-cols-3 gap-4 mb-4">
        <!-- 场景列表 -->
        <div class="col-span-1 bg-slate-800/50 rounded-lg p-3">
          <div class="flex items-center justify-between mb-3">
            <span class="text-xs text-slate-400">场景列表</span>
            <button @click="createScenario" class="text-xs bg-teal-500 hover:bg-teal-600 text-white px-2 py-1 rounded">
              + 新建
            </button>
          </div>
          
          <div class="space-y-2 max-h-60 overflow-y-auto">
            <div v-for="(scenario, idx) in scenarios" :key="idx"
              :class="['p-2 rounded cursor-pointer transition-all text-xs',
                selectedScenarioIdx === idx ? 'bg-teal-500/20 border border-teal-500/30' : 'bg-slate-700/50 hover:bg-slate-700']">
              <div class="flex items-center justify-between">
                <span class="text-slate-200" @click="selectScenario(idx)">{{ scenario.name }}</span>
                <div class="flex gap-1">
                  <button @click.stop="editScenario(idx)" class="text-slate-400 hover:text-teal-400">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path>
                    </svg>
                  </button>
                  <button @click.stop="deleteScenario(idx)" class="text-slate-400 hover:text-red-400">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                  </button>
                </div>
              </div>
              <div class="text-slate-500 text-[10px] mt-1">
                {{ scenario.params.ratedEnergy || '-' }} MWh | {{ scenario.params.acEfficiency || '-' }}%
              </div>
            </div>
            
            <div v-if="scenarios.length === 0" class="text-xs text-slate-500 text-center py-4">
              暂无场景，点击"新建"创建
            </div>
          </div>
        </div>

        <!-- 场景编辑器 -->
        <div class="col-span-2 bg-slate-800/50 rounded-lg p-3">
          <div v-if="!editingScenario" class="text-xs text-slate-500 text-center py-8">
            选择或创建一个场景进行编辑
          </div>
          
          <div v-else>
            <div class="flex items-center justify-between mb-3">
              <input v-model="editingScenario.name" 
                class="bg-slate-700 text-xs text-white px-2 py-1 rounded border border-slate-600 focus:border-teal-500 outline-none"
                placeholder="场景名称">
              <div class="flex gap-2">
                <button @click="saveScenario" class="text-xs bg-teal-500 hover:bg-teal-600 text-white px-3 py-1 rounded">
                  保存
                </button>
                <button @click="cancelEdit" class="text-xs bg-slate-600 hover:bg-slate-500 text-white px-3 py-1 rounded">
                  取消
                </button>
              </div>
            </div>
            
            <div class="grid grid-cols-3 gap-2 text-xs">
              <div>
                <label class="text-slate-400 text-[10px]">额定能量 (MWh)</label>
                <input v-model.number="editingScenario.params.ratedEnergy" type="number"
                  class="w-full bg-slate-700 text-white px-2 py-1 rounded border border-slate-600 focus:border-teal-500 outline-none">
              </div>
              <div>
                <label class="text-slate-400 text-[10px]">集装箱数量</label>
                <input v-model.number="editingScenario.params.initContainerQty" type="number"
                  class="w-full bg-slate-700 text-white px-2 py-1 rounded border border-slate-600 focus:border-teal-500 outline-none">
              </div>
              <div>
                <label class="text-slate-400 text-[10px]">PCS数量</label>
                <input v-model.number="editingScenario.params.initPcsQty" type="number"
                  class="w-full bg-slate-700 text-white px-2 py-1 rounded border border-slate-600 focus:border-teal-500 outline-none">
              </div>
              <div>
                <label class="text-slate-400 text-[10px]">储能时长 (h)</label>
                <input v-model.number="editingScenario.params.duration" type="number"
                  class="w-full bg-slate-700 text-white px-2 py-1 rounded border border-slate-600 focus:border-teal-500 outline-none">
              </div>
              <div>
                <label class="text-slate-400 text-[10px]">每日循环</label>
                <input v-model.number="editingScenario.params.cyclesPerDay" type="number"
                  class="w-full bg-slate-700 text-white px-2 py-1 rounded border border-slate-600 focus:border-teal-500 outline-none">
              </div>
              <div>
                <label class="text-slate-400 text-[10px]">交流效率 (%)</label>
                <input v-model.number="editingScenario.params.acEfficiency" type="number"
                  class="w-full bg-slate-700 text-white px-2 py-1 rounded border border-slate-600 focus:border-teal-500 outline-none">
              </div>
              <div>
                <label class="text-slate-400 text-[10px]">BESS运行功耗</label>
                <input v-model.number="editingScenario.params.bessAuxRun" type="number"
                  class="w-full bg-slate-700 text-white px-2 py-1 rounded border border-slate-600 focus:border-teal-500 outline-none">
              </div>
              <div>
                <label class="text-slate-400 text-[10px]">BESS待机功耗</label>
                <input v-model.number="editingScenario.params.bessAuxStandby" type="number"
                  class="w-full bg-slate-700 text-white px-2 py-1 rounded border border-slate-600 focus:border-teal-500 outline-none">
              </div>
              <div>
                <label class="text-slate-400 text-[10px]">需求能量 (MWh)</label>
                <input v-model.number="editingScenario.params.requiredEnergy" type="number"
                  class="w-full bg-slate-700 text-white px-2 py-1 rounded border border-slate-600 focus:border-teal-500 outline-none">
              </div>
            </div>
            
            <div class="mt-3 flex gap-2">
              <button @click="calculateScenario" :disabled="calculating"
                class="flex-1 bg-amber-500 hover:bg-amber-600 disabled:bg-slate-600 text-white text-xs px-3 py-1.5 rounded">
                {{ calculating ? '计算中...' : '计算此场景' }}
              </button>
              <button @click="useAsBase" class="flex-1 bg-sky-500 hover:bg-sky-600 text-white text-xs px-3 py-1.5 rounded">
                设为基准
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 对比图表 -->
      <div v-if="scenarios.length > 0" class="mt-4">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs text-slate-400">对比图表</span>
          <div class="flex gap-2">
            <button @click="showChart = 'soh'" :class="['text-xs px-2 py-1 rounded', showChart === 'soh' ? 'bg-teal-500 text-white' : 'bg-slate-700 text-slate-300']">
              SOH曲线
            </button>
            <button @click="showChart = 'energy'" :class="['text-xs px-2 py-1 rounded', showChart === 'energy' ? 'bg-teal-500 text-white' : 'bg-slate-700 text-slate-300']">
              净可用能量
            </button>
            <button @click="showChart = 'cost'" :class="['text-xs px-2 py-1 rounded', showChart === 'cost' ? 'bg-teal-500 text-white' : 'bg-slate-700 text-slate-300']">
              成本对比
            </button>
          </div>
        </div>
        
        <div ref="chartContainer" class="h-64 bg-slate-800/30 rounded-lg"></div>
      </div>

      <!-- 对比表格 -->
      <div v-if="scenarios.length > 0" class="mt-4">
        <div class="text-xs text-slate-400 mb-2">关键指标对比</div>
        <div class="overflow-x-auto">
          <table class="w-full text-xs">
            <thead>
              <tr class="text-slate-400 border-b border-slate-700">
                <th class="text-left py-2 px-2">指标</th>
                <th v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.name }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr class="text-slate-300 border-b border-slate-800">
                <td class="py-2 px-2">额定能量 (MWh)</td>
                <td v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.params.ratedEnergy || '-' }}
                </td>
              </tr>
              <tr class="text-slate-300 border-b border-slate-800">
                <td class="py-2 px-2">交流效率 (%)</td>
                <td v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.params.acEfficiency || '-' }}
                </td>
              </tr>
              <tr class="text-slate-300 border-b border-slate-800">
                <td class="py-2 px-2">初始净可用 (MWh)</td>
                <td v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.results?.initAcUsable?.[0]?.toFixed(2) || '-' }}
                </td>
              </tr>
              <tr class="text-slate-300 border-b border-slate-800">
                <td class="py-2 px-2">第10年净可用 (MWh)</td>
                <td v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.results?.totalAcUsable?.[10]?.toFixed(2) || '-' }}
                </td>
              </tr>
              <tr class="text-slate-300 border-b border-slate-800">
                <td class="py-2 px-2">第25年净可用 (MWh)</td>
                <td v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.results?.totalAcUsable?.[25]?.toFixed(2) || '-' }}
                </td>
              </tr>
              <tr class="text-slate-300 border-b border-slate-800">
                <td class="py-2 px-2">25年累计扩容</td>
                <td v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.results?.augAccumQty?.[25] || '-' }}
                </td>
              </tr>
              <tr class="text-teal-400 font-medium border-b border-slate-800">
                <td class="py-2 px-2">是否满足需求</td>
                <td v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.results?.meetsReq?.[25] ? '✓' : '✗' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Toast提示 -->
    <div v-if="toast.show"
      :class="['fixed bottom-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all',
        toast.type === 'success' ? 'bg-emerald-500 text-white' : 'bg-red-500 text-white']">
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, nextTick, onMounted } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  baseParams: { type: Object, default: () => ({}) },
})

const emit = defineEmits(['error'])

const scenarios = ref([])
const selectedScenarioIdx = ref(-1)
const editingScenario = ref(null)
const calculating = ref(false)
const showChart = ref('soh')
const chartContainer = ref(null)
let chartInstance = null

const toast = reactive({
  show: false,
  message: '',
  type: 'success',
})

const showToast = (message, type = 'success') => {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => {
    toast.show = false
  }, 3000)
}

// 创建新场景
function createScenario() {
  editingScenario.value = {
    name: `场景 ${scenarios.value.length + 1}`,
    params: {
      ratedEnergy: 5,
      initContainerQty: 62,
      initPcsQty: 1,
      duration: 2,
      cyclesPerDay: 1,
      acEfficiency: 97.03,
      bessAuxRun: 18.124,
      bessAuxStandby: 3.5,
      pcsAuxRun: 6.5,
      pcsAuxStandby: 1.0,
      requiredEnergy: 240,
    },
    results: null,
  }
}

// 选择场景
function selectScenario(idx) {
  selectedScenarioIdx.value = idx
  editingScenario.value = JSON.parse(JSON.stringify(scenarios.value[idx]))
}

// 编辑场景
function editScenario(idx) {
  selectScenario(idx)
}

// 保存场景
function saveScenario() {
  if (!editingScenario.value.name) {
    showToast('请输入场景名称', 'error')
    return
  }
  
  const idx = selectedScenarioIdx.value
  if (idx >= 0) {
    scenarios.value[idx] = JSON.parse(JSON.stringify(editingScenario.value))
  } else {
    scenarios.value.push(JSON.parse(JSON.stringify(editingScenario.value)))
    selectedScenarioIdx.value = scenarios.value.length - 1
  }
  
  editingScenario.value = null
  updateChart()
  showToast('场景已保存')
}

// 取消编辑
function cancelEdit() {
  editingScenario.value = null
}

// 删除场景
function deleteScenario(idx) {
  scenarios.value.splice(idx, 1)
  if (selectedScenarioIdx.value === idx) {
    selectedScenarioIdx.value = -1
    editingScenario.value = null
  } else if (selectedScenarioIdx.value > idx) {
    selectedScenarioIdx.value--
  }
  updateChart()
}

// 设为基准
function useAsBase() {
  if (selectedScenarioIdx.value >= 0) {
    scenarios.value[selectedScenarioIdx.value].isBase = true
    scenarios.value.forEach((s, i) => {
      if (i !== selectedScenarioIdx.value) s.isBase = false
    })
    showToast('已设为基准场景')
  }
}

// 计算场景
async function calculateScenario() {
  if (!editingScenario.value) return
  
  calculating.value = true
  
  try {
    const response = await fetch('/api/soh/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editingScenario.value.params),
    })
    
    const result = await response.json()
    
    if (result.success) {
      editingScenario.value.results = result.data
      
      // 更新列表中的场景
      const idx = selectedScenarioIdx.value
      if (idx >= 0) {
        scenarios.value[idx] = JSON.parse(JSON.stringify(editingScenario.value))
      }
      
      updateChart()
      showToast('计算完成')
    } else {
      throw new Error(result.error)
    }
  } catch (error) {
    console.error('计算失败:', error)
    showToast('计算失败: ' + error.message, 'error')
  } finally {
    calculating.value = false
  }
}

// 更新图表
function updateChart() {
  nextTick(() => {
    if (!chartContainer.value) return
    
    if (!chartInstance) {
      chartInstance = echarts.init(chartContainer.value)
    }
    
    const years = Array.from({ length: 26 }, (_, i) => i)
    
    let series = []
    
    if (showChart.value === 'soh') {
      scenarios.value.forEach((scenario, idx) => {
        if (scenario.results?.soh) {
          series.push({
            name: scenario.name,
            type: 'line',
            smooth: true,
            data: scenario.results.soh.map(v => (v * 100).toFixed(2)),
            connectNulls: true,
          })
        }
      })
    } else if (showChart.value === 'energy') {
      scenarios.value.forEach((scenario, idx) => {
        if (scenario.results?.totalAcUsable) {
          series.push({
            name: scenario.name,
            type: 'line',
            smooth: true,
            data: scenario.results.totalAcUsable,
            connectNulls: true,
          })
        }
      })
    }
    
    const option = {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(30, 41, 59, 0.9)',
        borderColor: 'rgba(100, 116, 139, 0.3)',
        textStyle: { color: '#e2e8f0', fontSize: 11 },
      },
      legend: {
        data: scenarios.value.map(s => s.name),
        textStyle: { color: '#94a3b8', fontSize: 11 },
        top: 5,
      },
      grid: {
        left: 50,
        right: 20,
        top: 40,
        bottom: 30,
      },
      xAxis: {
        type: 'category',
        data: years,
        name: '年份',
        nameTextStyle: { color: '#64748b', fontSize: 10 },
        axisLabel: { color: '#64748b', fontSize: 10 },
        axisLine: { lineStyle: { color: '#334155' } },
      },
      yAxis: {
        type: 'value',
        name: showChart.value === 'soh' ? 'SOH (%)' : '净可用 (MWh)',
        nameTextStyle: { color: '#64748b', fontSize: 10 },
        axisLabel: { color: '#64748b', fontSize: 10 },
        axisLine: { lineStyle: { color: '#334155' } },
        splitLine: { lineStyle: { color: '#1e293b' } },
      },
      series,
      color: ['#2dd4bf', '#38bdf8', '#fb923c', '#a78bfa', '#f472b6'],
    }
    
    chartInstance.setOption(option, true)
  })
}

// 监听图表类型变化
watch(showChart, () => {
  updateChart()
})

// 窗口调整
onMounted(() => {
  window.addEventListener('resize', () => {
    chartInstance?.resize()
  })
})
</script>

<style scoped>
.scenario-compare {
  height: 100%;
}
</style>