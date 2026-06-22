<template>
  <div class="sensitivity-analysis h-full overflow-auto p-4">
    <div class="bg-slate-900/60 rounded-lg border border-slate-800 p-4">
      <h3 class="text-sm font-bold text-teal-400 mb-4 flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-teal-400"></span>
        敏感性分析
      </h3>

      <!-- 敏感性参数设置 -->
      <div class="grid grid-cols-4 gap-4 mb-4">
        <!-- 参数选择 -->
        <div class="bg-slate-800/50 rounded-lg p-3">
          <div class="text-xs text-slate-400 mb-3">选择敏感性参数</div>
          <div class="space-y-2">
            <label v-for="param in sensitivityParams" :key="param.key"
              class="flex items-center gap-2 cursor-pointer text-xs">
              <input type="checkbox" v-model="param.enabled" class="accent-teal-500">
              <span class="text-slate-300">{{ param.label }}</span>
            </label>
          </div>
        </div>

        <!-- 参数范围设置 -->
        <div class="col-span-3 bg-slate-800/50 rounded-lg p-3">
          <div class="text-xs text-slate-400 mb-3">参数变化范围</div>
          
          <div class="grid grid-cols-3 gap-3">
            <div v-for="param in enabledParams" :key="param.key">
              <div class="text-xs text-slate-300 mb-1">{{ param.label }}</div>
              <div class="flex items-center gap-1">
                <input v-model.number="param.min" type="number" step="0.01"
                  class="w-16 bg-slate-700 text-white px-2 py-1 rounded text-xs border border-slate-600 focus:border-teal-500 outline-none">
                <span class="text-slate-500 text-xs">至</span>
                <input v-model.number="param.max" type="number" step="0.01"
                  class="w-16 bg-slate-700 text-white px-2 py-1 rounded text-xs border border-slate-600 focus:border-teal-500 outline-none">
              </div>
              <div class="text-[10px] text-slate-500 mt-1">
                当前值: {{ param.current }}
              </div>
            </div>
          </div>
          
          <div class="mt-3 flex items-center gap-2">
            <span class="text-xs text-slate-400">变化步数:</span>
            <input v-model.number="steps" type="number" min="3" max="10"
              class="w-16 bg-slate-700 text-white px-2 py-1 rounded text-xs border border-slate-600 focus:border-teal-500 outline-none">
            <span class="text-xs text-slate-500">(3-10步)</span>
            <button @click="runAnalysis" :disabled="analyzing || enabledParams.length === 0"
              class="ml-auto bg-amber-500 hover:bg-amber-600 disabled:bg-slate-600 text-white text-xs px-4 py-1.5 rounded">
              {{ analyzing ? '分析中...' : '运行分析' }}
            </button>
          </div>
        </div>
      </div>

      <!-- 分析结果 -->
      <div v-if="analysisResults.length > 0" class="grid grid-cols-2 gap-4">
        <!-- 龙卷风图 -->
        <div class="bg-slate-800/50 rounded-lg p-3">
          <div class="text-xs text-slate-400 mb-3">敏感性排名 (龙卷风图)</div>
          <div ref="tornadoChart" class="h-64"></div>
        </div>

        <!-- 蜘蛛图 -->
        <div class="bg-slate-800/50 rounded-lg p-3">
          <div class="text-xs text-slate-400 mb-3">多参数蜘蛛图</div>
          <div ref="spiderChart" class="h-64"></div>
        </div>
      </div>

      <!-- 详细数据表 -->
      <div v-if="analysisResults.length > 0" class="mt-4">
        <div class="text-xs text-slate-400 mb-2">敏感性分析详细数据</div>
        <div class="overflow-x-auto">
          <table class="w-full text-xs">
            <thead>
              <tr class="text-slate-400 border-b border-slate-700">
                <th class="text-left py-2 px-2">参数</th>
                <th v-for="(result, idx) in analysisResults" :key="idx" class="text-right py-2 px-2">
                  {{ result.param }} ({{ (result.minValue * 100).toFixed(0) }}%~{{ (result.maxValue * 100).toFixed(0) }}%)
                </th>
              </tr>
            </thead>
            <tbody>
              <tr class="text-slate-300 border-b border-slate-800">
                <td class="py-2 px-2">NPV变化</td>
                <td v-for="(result, idx) in analysisResults" :key="idx" class="text-right py-2 px-2"
                  :class="result.npvImpact > 0 ? 'text-emerald-400' : 'text-red-400'">
                  {{ result.npvImpact > 0 ? '+' : '' }}{{ result.npvImpact.toFixed(2) }}%
                </td>
              </tr>
              <tr class="text-slate-300 border-b border-slate-800">
                <td class="py-2 px-2">IRR变化</td>
                <td v-for="(result, idx) in analysisResults" :key="idx" class="text-right py-2 px-2"
                  :class="result.irrImpact > 0 ? 'text-emerald-400' : 'text-red-400'">
                  {{ result.irrImpact > 0 ? '+' : '' }}{{ result.irrImpact.toFixed(2) }}%
                </td>
              </tr>
              <tr class="text-slate-300 border-b border-slate-800">
                <td class="py-2 px-2">回收期变化</td>
                <td v-for="(result, idx) in analysisResults" :key="idx" class="text-right py-2 px-2"
                  :class="result.paybackImpact < 0 ? 'text-emerald-400' : 'text-red-400'">
                  {{ result.paybackImpact > 0 ? '+' : '' }}{{ result.paybackImpact.toFixed(2) }}年
                </td>
              </tr>
              <tr class="text-slate-300 border-b border-slate-800">
                <td class="py-2 px-2">LCOS变化</td>
                <td v-for="(result, idx) in analysisResults" :key="idx" class="text-right py-2 px-2"
                  :class="result.lcosImpact < 0 ? 'text-emerald-400' : 'text-red-400'">
                  {{ result.lcosImpact > 0 ? '+' : '' }}{{ result.lcosImpact.toFixed(2) }}%
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 财务指标敏感性说明 -->
      <div class="mt-4 p-3 bg-slate-800/30 rounded-lg text-xs text-slate-400">
        <div class="font-medium text-slate-300 mb-2">敏感性分析说明</div>
        <ul class="list-disc list-inside space-y-1">
          <li>NPV (净现值): 对电价、补贴政策敏感，影响项目投资回报</li>
          <li>IRR (内部收益率): 反映项目盈利能力，对成本和收入变化敏感</li>
          <li>回收期: 投资回收所需时间，影响资金周转</li>
          <li>LCOS (储能度电成本): 核心竞争指标，对电池价格、效率敏感</li>
        </ul>
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
import { ref, reactive, computed, watch, nextTick, onMounted } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  params: { type: Object, default: () => ({}) },
  financial: { type: Object, default: () => ({}) },
})

const emit = defineEmits(['error'])

const sensitivityParams = reactive([
  { key: 'electricityPrice', label: '电价', enabled: true, min: 0.3, max: 0.8, current: 0.5, unit: '元/kWh' },
  { key: 'inflationRate', label: '通货膨胀率', enabled: true, min: 0.01, max: 0.05, current: 0.03, unit: '' },
  { key: 'discountRate', label: '折现率', enabled: false, min: 0.05, max: 0.12, current: 0.08, unit: '' },
  { key: 'bessCost', label: '电池成本', enabled: true, min: 0.8, max: 1.5, current: 1.0, unit: '元/Wh' },
  { key: 'efficiency', label: '系统效率', enabled: false, min: 0.85, max: 0.99, current: 0.92, unit: '' },
  { key: 'subsidy', label: '补贴系数', enabled: false, min: 0.5, max: 1.5, current: 1.0, unit: '' },
])

const steps = ref(5)
const analyzing = ref(false)
const analysisResults = ref([])
const tornadoChart = ref(null)
const spiderChart = ref(null)
let tornadoInstance = null
let spiderInstance = null

const toast = reactive({
  show: false,
  message: '',
  type: 'success',
})

const enabledParams = computed(() => sensitivityParams.filter(p => p.enabled))

const showToast = (message, type = 'success') => {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => {
    toast.show = false
  }, 3000)
}

// 运行敏感性分析
async function runAnalysis() {
  if (enabledParams.value.length === 0) {
    showToast('请选择至少一个敏感性参数', 'error')
    return
  }

  analyzing.value = true
  analysisResults.value = []

  try {
    // 对每个启用的参数进行分析
    for (const param of enabledParams.value) {
      const result = await analyzeSingleParam(param)
      analysisResults.value.push(result)
    }

    // 更新图表
    nextTick(() => {
      updateTornadoChart()
      updateSpiderChart()
    })

    showToast('敏感性分析完成')
  } catch (error) {
    console.error('分析失败:', error)
    showToast('分析失败: ' + error.message, 'error')
  } finally {
    analyzing.value = false
  }
}

// 分析单个参数
async function analyzeSingleParam(param) {
  const baseValue = param.current
  const minValue = param.min
  const maxValue = param.max
  
  const stepSize = (maxValue - minValue) / (steps.value - 1)
  const values = Array.from({ length: steps.value }, (_, i) => minValue + i * stepSize)
  
  const npvValues = []
  const irrValues = []
  const paybackValues = []
  const lcosValues = []
  
  for (const value of values) {
    const testParams = { ...props.params, [param.key]: value }
    
    try {
      const response = await fetch('/api/soh/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(testParams),
      })
      
      const result = await response.json()
      
      if (result.success) {
        const financial = result.data.financial || {}
        npvValues.push(financial.npv || 0)
        irrValues.push(financial.irr || 0)
        paybackValues.push(financial.paybackYears || 0)
        lcosValues.push(financial.lcos || 0)
      } else {
        npvValues.push(0)
        irrValues.push(0)
        paybackValues.push(0)
        lcosValues.push(0)
      }
    } catch (error) {
      npvValues.push(0)
      irrValues.push(0)
      paybackValues.push(0)
      lcosValues.push(0)
    }
  }
  
  // 计算影响（变化百分比）
  const baseFinancial = props.financial || {}
  const baseNpv = baseFinancial.npv || 0
  const baseIrr = baseFinancial.irr || 0
  const basePayback = baseFinancial.paybackYears || 0
  const baseLcos = baseFinancial.lcos || 0
  
  // 使用最大值和最小值的差异作为敏感性指标
  const npvRange = Math.max(...npvValues) - Math.min(...npvValues)
  const irrRange = Math.max(...irrValues) - Math.min(...irrValues)
  const paybackRange = Math.max(...paybackValues) - Math.min(...paybackValues)
  const lcosRange = Math.max(...lcosValues) - Math.min(...lcosValues)
  
  // 计算相对于基准的影响百分比
  const npvImpact = baseNpv !== 0 ? (npvRange / Math.abs(baseNpv)) * 100 : 0
  const irrImpact = baseIrr !== 0 ? (irrRange / Math.abs(baseIrr)) * 100 : 0
  const paybackImpact = paybackRange
  const lcosImpact = baseLcos !== 0 ? (lcosRange / Math.abs(baseLcos)) * 100 : 0
  
  return {
    param: param.label,
    paramKey: param.key,
    minValue,
    maxValue,
    values,
    npvValues,
    irrValues,
    paybackValues,
    lcosValues,
    npvImpact,
    irrImpact,
    paybackImpact,
    lcosImpact,
    // 综合敏感性得分
    sensitivityScore: (Math.abs(npvImpact) + Math.abs(irrImpact) + Math.abs(lcosImpact)) / 3,
  }
}

// 更新龙卷风图
function updateTornadoChart() {
  if (!tornadoChart.value) return
  
  if (!tornadoInstance) {
    tornadoInstance = echarts.init(tornadoChart.value)
  }
  
  // 按敏感性排序
  const sortedResults = [...analysisResults.value].sort((a, b) => 
    b.sensitivityScore - a.sensitivityScore
  )
  
  const categories = sortedResults.map(r => r.param)
  const npvData = sortedResults.map(r => ({
    value: r.npvImpact,
    itemStyle: { color: r.npvImpact > 0 ? '#10b981' : '#ef4444' }
  }))
  
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(30, 41, 59, 0.9)',
      textStyle: { color: '#e2e8f0', fontSize: 11 },
      formatter: (params) => {
        const idx = params[0].dataIndex
        const result = sortedResults[idx]
        return `${result.param}<br/>NPV影响: ${result.npvImpact.toFixed(2)}%<br/>IRR影响: ${result.irrImpact.toFixed(2)}%<br/>LCOS影响: ${result.lcosImpact.toFixed(2)}%`
      }
    },
    grid: {
      left: 100,
      right: 80,
      top: 20,
      bottom: 30,
    },
    xAxis: {
      type: 'value',
      name: '影响程度 (%)',
      nameTextStyle: { color: '#64748b', fontSize: 10 },
      axisLabel: { color: '#64748b', fontSize: 10 },
      axisLine: { lineStyle: { color: '#334155' } },
      splitLine: { lineStyle: { color: '#1e293b' } },
    },
    yAxis: {
      type: 'category',
      data: categories,
      axisLabel: { color: '#94a3b8', fontSize: 11 },
      axisLine: { lineStyle: { color: '#334155' } },
    },
    series: [{
      type: 'bar',
      data: npvData,
      barWidth: '60%',
      label: {
        show: true,
        position: 'right',
        formatter: '{c}%',
        color: '#94a3b8',
        fontSize: 10,
      },
    }],
  }
  
  tornadoInstance.setOption(option, true)
}

// 更新蜘蛛图
function updateSpiderChart() {
  if (!spiderChart.value) return
  
  if (!spiderInstance) {
    spiderInstance = echarts.init(spiderChart.value)
  }
  
  // 选择最敏感的3个参数展示蜘蛛图
  const topResults = [...analysisResults.value]
    .sort((a, b) => b.sensitivityScore - a.sensitivityScore)
    .slice(0, 3)
  
  if (topResults.length === 0) return
  
  const indicators = topResults.map(r => ({
    name: r.param,
    max: Math.max(Math.abs(r.npvImpact), Math.abs(r.irrImpact), Math.abs(r.lcosImpact)) * 1.2,
  }))
  
  const seriesData = [
    {
      name: 'NPV',
      value: topResults.map(r => Math.abs(r.npvImpact)),
      lineStyle: { color: '#2dd4bf' },
      areaStyle: { color: 'rgba(45, 212, 191, 0.1)' },
      itemStyle: { color: '#2dd4bf' },
    },
    {
      name: 'IRR',
      value: topResults.map(r => Math.abs(r.irrImpact)),
      lineStyle: { color: '#38bdf8' },
      areaStyle: { color: 'rgba(56, 189, 248, 0.1)' },
      itemStyle: { color: '#38bdf8' },
    },
    {
      name: 'LCOS',
      value: topResults.map(r => Math.abs(r.lcosImpact)),
      lineStyle: { color: '#fb923c' },
      areaStyle: { color: 'rgba(251, 146, 60, 0.1)' },
      itemStyle: { color: '#fb923c' },
    },
  ]
  
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      backgroundColor: 'rgba(30, 41, 59, 0.9)',
      textStyle: { color: '#e2e8f0', fontSize: 11 },
    },
    legend: {
      data: ['NPV', 'IRR', 'LCOS'],
      textStyle: { color: '#94a3b8', fontSize: 10 },
      top: 5,
    },
    radar: {
      indicator: indicators,
      axisName: { color: '#94a3b8', fontSize: 10 },
      splitArea: { areaStyle: { color: ['rgba(30, 41, 59, 0.3)'] } },
      axisLine: { lineStyle: { color: '#334155' } },
      splitLine: { lineStyle: { color: '#1e293b' } },
    },
    series: [{
      type: 'radar',
      data: seriesData,
    }],
  }
  
  spiderInstance.setOption(option, true)
}

// 窗口调整
onMounted(() => {
  window.addEventListener('resize', () => {
    tornadoInstance?.resize()
    spiderInstance?.resize()
  })
})
</script>

<style scoped>
.sensitivity-analysis {
  height: 100%;
}
</style>