<template>
  <div class="sensitivity-analysis h-full overflow-auto p-4">
    <div class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border)">
      <h3 class="text-sm font-bold mb-4 flex items-center gap-2" style="color: var(--color-accent)">
        <span class="w-2 h-2 rounded-full" style="background-color: var(--color-accent)" />
        {{ $t('sensitivity.title') }}
      </h3>

      <!-- 敏感性参数设置 -->
      <div class="grid grid-cols-4 gap-4 mb-4">
        <!-- 参数选择 -->
        <div class="rounded-lg p-3" style="background-color: var(--color-card-dark)">
          <div class="text-xs mb-3" style="color: var(--color-text-muted)">{{ $t('sensitivity.selectParam') }}</div>
          <div class="space-y-2">
            <label
              v-for="param in sensitivityParams"
              :key="param.key"
              class="flex items-center gap-2 cursor-pointer text-xs label-text"
            >
              <input v-model="param.enabled" type="checkbox" style="accent-color: var(--color-accent)" />
              <span style="color: var(--color-text-secondary)">{{ $t('sensitivity.paramLabel', { label: param.label }) }}</span>
            </label>
          </div>
        </div>

        <!-- 参数范围设置 -->
        <div class="col-span-3 rounded-lg p-3" style="background-color: var(--color-card-dark)">
          <div class="text-xs mb-3" style="color: var(--color-text-muted)">{{ $t('sensitivity.range') }}</div>

          <div class="grid grid-cols-3 gap-3">
            <div v-for="param in enabledParams" :key="param.key">
              <div class="text-xs mb-1" style="color: var(--color-text-secondary)">
                {{ $t('sensitivity.paramLabel', { label: param.label }) }}
              </div>
              <div class="flex items-center gap-1">
                <input
                  v-model.number="param.min"
                  type="number"
                  step="0.01"
                  class="w-16 rounded text-xs px-2 py-1 form-field-input"
                />
                <span class="text-xs" style="color: var(--color-text-muted)">{{ $t('sensitivity.to') }}</span>
                <input
                  v-model.number="param.max"
                  type="number"
                  step="0.01"
                  class="w-16 rounded text-xs px-2 py-1 form-field-input"
                />
              </div>
              <div class="text-[10px] mt-1" style="color: var(--color-text-muted)">{{ $t('sensitivity.currentValue') }}: {{ param.current }}</div>
            </div>
          </div>

          <div class="mt-3 flex items-center gap-2">
            <span class="text-xs" style="color: var(--color-text-muted)">{{ $t('sensitivity.stepsLabel') }}</span>
            <input
              v-model.number="steps"
              type="number"
              min="3"
              max="10"
              class="w-16 rounded text-xs px-2 py-1 form-field-input"
            />
            <span class="text-xs" style="color: var(--color-text-muted)">({{ $t('sensitivity.stepsRange') }})</span>
            <button
              :disabled="analyzing || enabledParams.length === 0"
              class="ml-auto text-xs px-4 py-1.5 rounded transition-colors"
              :style="
                analyzing || enabledParams.length === 0
                  ? { backgroundColor: 'var(--color-card-dark)', color: 'var(--color-text-muted)' }
                  : { backgroundColor: 'var(--color-warning)', color: 'white' }
              "
              @click="runAnalysis"
            >
              {{ analyzing ? $t('sensitivity.analyzing') : $t('sensitivity.runAnalysis') }}
            </button>
          </div>
        </div>
      </div>

      <!-- 分析结果 -->
      <div v-if="analysisResults.length > 0" class="grid grid-cols-2 gap-4">
        <!-- 龙卷风图 -->
        <div class="rounded-lg p-3" style="background-color: var(--color-card-dark)">
          <div class="text-xs mb-3" style="color: var(--color-text-muted)">{{ $t('sensitivity.tornadoRank') }}</div>
          <div ref="tornadoChart" class="h-64" />
        </div>

        <!-- 蜘蛛图 -->
        <div class="rounded-lg p-3" style="background-color: var(--color-card-dark)">
          <div class="text-xs mb-3" style="color: var(--color-text-muted)">{{ $t('sensitivity.spiderChart') }}</div>
          <div ref="spiderChart" class="h-64" />
        </div>
      </div>

      <!-- 详细数据表 -->
      <div v-if="analysisResults.length > 0" class="mt-4">
        <div class="text-xs mb-2" style="color: var(--color-text-muted)">{{ $t('sensitivity.detailData') }}</div>
        <div class="overflow-x-auto">
          <table class="w-full text-xs">
            <thead>
              <tr style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)">
                <th class="text-left py-2 px-2">{{ $t('sensitivity.parameter') }}</th>
                <th v-for="(result, idx) in analysisResults" :key="idx" class="text-right py-2 px-2">
                  {{ result.param }} ({{ (result.minValue * 100).toFixed(0) }}%~{{
                    (result.maxValue * 100).toFixed(0)
                  }}%)
                </th>
              </tr>
            </thead>
            <tbody>
              <tr style="color: var(--color-text-secondary); border-bottom: 1px solid var(--color-border)">
                <td class="py-2 px-2">{{ $t('sensitivity.npvChange') }}</td>
                <td
                  v-for="(result, idx) in analysisResults"
                  :key="idx"
                  class="text-right py-2 px-2"
                  :style="result.npvImpact > 0 ? { color: 'var(--color-success)' } : { color: 'var(--color-danger)' }"
                >
                  {{ result.npvImpact > 0 ? '+' : '' }}{{ result.npvImpact.toFixed(2) }}%
                </td>
              </tr>
              <tr style="color: var(--color-text-secondary); border-bottom: 1px solid var(--color-border)">
                <td class="py-2 px-2">{{ $t('sensitivity.irrChange') }}</td>
                <td
                  v-for="(result, idx) in analysisResults"
                  :key="idx"
                  class="text-right py-2 px-2"
                  :style="result.irrImpact > 0 ? { color: 'var(--color-success)' } : { color: 'var(--color-danger)' }"
                >
                  {{ result.irrImpact > 0 ? '+' : '' }}{{ result.irrImpact.toFixed(2) }}%
                </td>
              </tr>
              <tr style="color: var(--color-text-secondary); border-bottom: 1px solid var(--color-border)">
                <td class="py-2 px-2">{{ $t('sensitivity.paybackChange') }}</td>
                <td
                  v-for="(result, idx) in analysisResults"
                  :key="idx"
                  class="text-right py-2 px-2"
                  :style="
                    result.paybackImpact < 0 ? { color: 'var(--color-success)' } : { color: 'var(--color-danger)' }
                  "
                >
                  {{ result.paybackImpact > 0 ? '+' : '' }}{{ result.paybackImpact.toFixed(2) }}{{ $t('sensitivity.yearUnit') }}
                </td>
              </tr>
              <tr style="color: var(--color-text-secondary); border-bottom: 1px solid var(--color-border)">
                <td class="py-2 px-2">{{ $t('sensitivity.lcosChange') }}</td>
                <td
                  v-for="(result, idx) in analysisResults"
                  :key="idx"
                  class="text-right py-2 px-2"
                  :style="result.lcosImpact < 0 ? { color: 'var(--color-success)' } : { color: 'var(--color-danger)' }"
                >
                  {{ result.lcosImpact > 0 ? '+' : '' }}{{ result.lcosImpact.toFixed(2) }}%
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 财务指标敏感性说明 -->
      <div class="mt-4 p-3 rounded-lg" style="background-color: var(--color-card-dark)">
        <div class="font-medium mb-2" style="color: var(--color-text-secondary)">{{ $t('sensitivity.explanationTitle') }}</div>
        <ul class="list-disc list-inside space-y-1 text-xs" style="color: var(--color-text-muted)">
          <li>{{ $t('sensitivity.explanationNpv') }}</li>
          <li>{{ $t('sensitivity.explanationIrr') }}</li>
          <li>{{ $t('sensitivity.explanationPayback') }}</li>
          <li>{{ $t('sensitivity.explanationLcos') }}</li>
        </ul>
      </div>
    </div>

    <!-- Toast提示 -->
    <div
      v-if="toast.show"
      class="fixed bottom-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all"
      :style="{
        backgroundColor: toast.type === 'success' ? 'var(--color-success)' : 'var(--color-danger)',
        color: 'white'
      }"
    >
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, RadarChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, GridComponent, LegendComponent, RadarComponent } from 'echarts/components'
import { useDraft, useDraftRef } from '../composables/useDraft'
const { t } = useI18n()
echarts.use([
  CanvasRenderer,
  BarChart,
  RadarChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  RadarComponent
])

const props = defineProps({
  params: { type: Object, default: () => ({}) },
  financial: { type: Object, default: () => ({}) }
})

const emit = defineEmits(['error'])

const { state: sensitivityParams, clearDraft: clearSensitivityDraft } = useDraft('sensitivity-params', [
  { key: 'electricityPrice', labelKey: 'sensitivity.params.electricityPrice', enabled: true, min: 0.3, max: 0.8, current: 0.5, unit: 'sensitivity.params.unitPrice' },
  { key: 'inflationRate', labelKey: 'sensitivity.params.inflationRate', enabled: true, min: 0.01, max: 0.05, current: 0.03, unit: '' },
  { key: 'discountRate', labelKey: 'sensitivity.params.discountRate', enabled: false, min: 0.05, max: 0.12, current: 0.08, unit: '' },
  { key: 'bessCost', labelKey: 'sensitivity.params.bessCost', enabled: true, min: 0.8, max: 1.5, current: 1.0, unit: 'sensitivity.params.unitCost' },
  { key: 'efficiency', labelKey: 'sensitivity.params.efficiency', enabled: false, min: 0.85, max: 0.99, current: 0.92, unit: '' },
  { key: 'subsidy', labelKey: 'sensitivity.params.subsidy', enabled: false, min: 0.5, max: 1.5, current: 1.0, unit: '' }
])

const steps = useDraftRef('sensitivity-steps', 5).state
const analyzing = ref(false)
const analysisResults = ref([])
const tornadoChart = ref(null)
const spiderChart = ref(null)
let tornadoInstance = null
let spiderInstance = null
let _resizeHandler = null

const toast = reactive({
  show: false,
  message: '',
  type: 'success'
})

const enabledParams = computed(() => sensitivityParams.filter((p) => p.enabled))

const paramLabels = computed(() =>
  sensitivityParams.value.map((p) => ({
    key: p.key,
    label: p.labelKey ? t(p.labelKey) : p.label
  }))
)

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
    showToast(t('sensitivity.selectParamMsg'), 'error')
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

    showToast(t('sensitivity.analysisComplete'))
  } catch (error) {
    console.error(t('sensitivity.analysisFailed'), error)
    showToast(t('sensitivity.analysisFailed') + ': ' + error.message, 'error')
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
        body: JSON.stringify(testParams)
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
    param: param.labelKey ? t(param.labelKey) : param.label,
    paramKey: param.labelKey || param.label,
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
    sensitivityScore: (Math.abs(npvImpact) + Math.abs(irrImpact) + Math.abs(lcosImpact)) / 3
  }
}

// 更新龙卷风图
function updateTornadoChart() {
  if (!tornadoChart.value) return

  if (!tornadoInstance) {
    tornadoInstance = echarts.init(tornadoChart.value)
  }

  const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
  const colors = {
    success: 'var(--color-success)',
    danger: 'var(--color-danger)',
    textMuted: isDark ? 'var(--color-text-secondary)' : 'var(--color-text-secondary)',
    legendText: isDark ? 'var(--color-text-secondary)' : 'var(--color-text-secondary)',
    axisLine: isDark ? 'var(--color-border)' : 'var(--color-border-light)',
    splitLine: isDark ? '#1e293b' : '#f1f5f9',
    tooltipBg: isDark ? 'rgba(30, 41, 59, 0.9)' : 'rgba(255, 255, 255, 0.95)',
    tooltipText: isDark ? 'var(--color-border-light)' : '#1e293b'
  }

  const sortedResults = [...analysisResults.value].sort((a, b) => b.sensitivityScore - a.sensitivityScore)

  const categories = sortedResults.map((r) => (r.paramKey ? t(r.paramKey) : r.param))
  const npvData = sortedResults.map((r) => ({
    value: r.npvImpact,
    itemStyle: { color: r.npvImpact > 0 ? colors.success : colors.danger }
  }))

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: colors.tooltipBg,
      textStyle: { color: colors.tooltipText, fontSize: 11 },
      formatter: (params) => {
        const idx = params[0].dataIndex
        const result = sortedResults[idx]
        const paramName = result.paramKey ? t(result.paramKey) : result.param
        return `${paramName}<br/>${t('sensitivity.npvImpact')}: ${result.npvImpact.toFixed(2)}%<br/>${t('sensitivity.irrImpact')}: ${result.irrImpact.toFixed(2)}%<br/>${t('sensitivity.lcosImpact')}: ${result.lcosImpact.toFixed(2)}%`
      }
    },
    grid: {
      left: 100,
      right: 80,
      top: 20,
      bottom: 30
    },
    xAxis: {
      type: 'value',
      name: t('sensitivity.impactDegree'),
      nameTextStyle: { color: colors.textMuted, fontSize: 10 },
      axisLabel: { color: colors.textMuted, fontSize: 10 },
      axisLine: { lineStyle: { color: colors.axisLine } },
      splitLine: { lineStyle: { color: colors.splitLine } }
    },
    yAxis: {
      type: 'category',
      data: categories,
      axisLabel: { color: colors.legendText, fontSize: 11 },
      axisLine: { lineStyle: { color: colors.axisLine } }
    },
    series: [
      {
        type: 'bar',
        data: npvData,
        barWidth: '60%',
        label: {
          show: true,
          position: 'right',
          formatter: '{c}%',
          color: colors.legendText,
          fontSize: 10
        }
      }
    ]
  }

  tornadoInstance.setOption(option, true)
}

// 更新蜘蛛图
function updateSpiderChart() {
  if (!spiderChart.value) return

  if (!spiderInstance) {
    spiderInstance = echarts.init(spiderChart.value)
  }

  const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
  const colors = {
    npvLine: isDark ? '#2dd4bf' : '#14b8a6',
    irrLine: isDark ? '#38bdf8' : '#0ea5e9',
    lcosLine: isDark ? 'var(--color-chart-orange)' : 'var(--color-chart-orange)',
    npvArea: isDark ? 'rgba(45, 212, 191, 0.1)' : 'rgba(20, 184, 166, 0.08)',
    irrArea: isDark ? 'rgba(56, 189, 248, 0.1)' : 'rgba(14, 165, 233, 0.08)',
    lcosArea: isDark ? 'rgba(251, 146, 60, 0.1)' : 'rgba(249, 115, 22, 0.08)',
    legendText: isDark ? 'var(--color-text-secondary)' : 'var(--color-text-secondary)',
    axisLine: isDark ? 'var(--color-border)' : 'var(--color-border-light)',
    splitLine: isDark ? '#1e293b' : '#f1f5f9',
    splitArea: isDark ? 'rgba(30, 41, 59, 0.3)' : 'rgba(241, 245, 249, 0.5)',
    tooltipBg: isDark ? 'rgba(30, 41, 59, 0.9)' : 'rgba(255, 255, 255, 0.95)',
    tooltipText: isDark ? 'var(--color-border-light)' : '#1e293b'
  }

  const topResults = [...analysisResults.value].sort((a, b) => b.sensitivityScore - a.sensitivityScore).slice(0, 3)

  if (topResults.length === 0) return

  const indicators = topResults.map((r) => ({
    name: r.paramKey ? t(r.paramKey) : r.param,
    max: Math.max(Math.abs(r.npvImpact), Math.abs(r.irrImpact), Math.abs(r.lcosImpact)) * 1.2
  }))

  const seriesData = [
    {
      name: t('sensitivity.seriesNpv'),
      value: topResults.map((r) => Math.abs(r.npvImpact)),
      lineStyle: { color: colors.npvLine },
      areaStyle: { color: colors.npvArea },
      itemStyle: { color: colors.npvLine }
    },
    {
      name: t('sensitivity.seriesIrr'),
      value: topResults.map((r) => Math.abs(r.irrImpact)),
      lineStyle: { color: colors.irrLine },
      areaStyle: { color: colors.irrArea },
      itemStyle: { color: colors.irrLine }
    },
    {
      name: t('sensitivity.seriesLcos'),
      value: topResults.map((r) => Math.abs(r.lcosImpact)),
      lineStyle: { color: colors.lcosLine },
      areaStyle: { color: colors.lcosArea },
      itemStyle: { color: colors.lcosLine }
    }
  ]

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      backgroundColor: colors.tooltipBg,
      textStyle: { color: colors.tooltipText, fontSize: 11 }
    },
    legend: {
      data: [t('sensitivity.seriesNpv'), t('sensitivity.seriesIrr'), t('sensitivity.seriesLcos')],
      textStyle: { color: colors.legendText, fontSize: 10 },
      top: 5
    },
    radar: {
      indicator: indicators,
      axisName: { color: colors.legendText, fontSize: 10 },
      splitArea: { areaStyle: { color: [colors.splitArea] } },
      axisLine: { lineStyle: { color: colors.axisLine } },
      splitLine: { lineStyle: { color: colors.splitLine } }
    },
    series: [
      {
        type: 'radar',
        data: seriesData
      }
    ]
  }

  spiderInstance.setOption(option, true)
}

// 窗口调整
onMounted(() => {
  _resizeHandler = () => {
    tornadoInstance?.resize()
    spiderInstance?.resize()
  }
  window.addEventListener('resize', _resizeHandler)
})

onUnmounted(() => {
  if (tornadoInstance) {
    tornadoInstance.dispose()
    tornadoInstance = null
  }
  if (spiderInstance) {
    spiderInstance.dispose()
    spiderInstance = null
  }
  if (_resizeHandler) {
    window.removeEventListener('resize', _resizeHandler)
    _resizeHandler = null
  }
})
</script>

<style scoped>
.sensitivity-analysis {
  height: 100%;
}
input:focus,
select:focus,
textarea:focus {
  border-color: var(--color-input-focus);
  outline: none;
}

button:not(:disabled):hover {
  opacity: 0.9;
}
</style>
