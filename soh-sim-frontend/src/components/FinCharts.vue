<!-- FinCharts.vue -->
<template>
  <div class="grid grid-cols-2 gap-3">
    <div class="rounded-lg p-3 min-h-300 card-bordered">
      <h3 class="font-bold text-xs mb-2 text-default">{{ t('financialDashboard.chartCashFlow') }}</h3>
      <div ref="cashFlowChartRef" class="w-full h-280" />
    </div>
    <div class="rounded-lg p-3 min-h-300 card-bordered">
      <h3 class="font-bold text-xs mb-2 text-default">{{ t('financialDashboard.chartRevenue') }}</h3>
      <div ref="revenueChartRef" class="w-full h-280" />
    </div>
    <div class="rounded-lg p-3 min-h-300 card-bordered">
      <h3 class="font-bold text-xs mb-2 text-default">{{ t('financialDashboard.chartDscr') }}</h3>
      <div ref="dscrChartRef" class="w-full h-280" />
    </div>
    <div class="rounded-lg p-3 min-h-300 card-bordered">
      <h3 class="font-bold text-xs mb-2 text-default">{{ t('financialDashboard.chartCapex') }}</h3>
      <div ref="capexChartRef" class="w-full h-280" />
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { debounce } from 'lodash-es'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, PieChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, GridComponent, LegendComponent, GraphicComponent } from 'echarts/components'
import { useChartOptions } from '../composables/useChartOptions.js'

echarts.use([
  CanvasRenderer,
  BarChart,
  LineChart,
  PieChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  GraphicComponent
])

const props = defineProps({ model: { type: Object, required: true } })
const { t } = useI18n()
const { chartColors, metrics, cachedRows, cachedCapexData, fmtNum } = props.model
const { getCashFlowOption, getRevenueOption, getDscrOption, getCapexOption } = useChartOptions()

const cashFlowChartRef = ref(null)
const revenueChartRef = ref(null)
const dscrChartRef = ref(null)
const capexChartRef = ref(null)

let cashFlowChart = null
let revenueChart = null
let dscrChart = null
let capexChart = null
let resizeHandler = null

function disposeAll() {
  ;[cashFlowChart, revenueChart, dscrChart, capexChart].forEach((c) => c?.dispose())
  cashFlowChart = revenueChart = dscrChart = capexChart = null
}

function renderCashFlowChart() {
  if (!cashFlowChartRef.value) return
  if (cashFlowChart) cashFlowChart.dispose()
  const colors = chartColors.value
  cashFlowChart = echarts.init(cashFlowChartRef.value, colors)
  const rows = cachedRows()
  const paybackYear = parseFloat(metrics.value[5].value)
  cashFlowChart.setOption(getCashFlowOption(rows, colors, paybackYear))
  cashFlowChart.resize()
}

function renderRevenueChart() {
  if (!revenueChartRef.value) return
  if (revenueChart) revenueChart.dispose()
  const colors = chartColors.value
  revenueChart = echarts.init(revenueChartRef.value, colors)
  const rows = cachedRows().filter((r) => r.year > 0)
  revenueChart.setOption(getRevenueOption(rows, colors, fmtNum))
  revenueChart.resize()
}

function renderDscrChart() {
  if (!dscrChartRef.value) return
  if (dscrChart) dscrChart.dispose()
  const colors = chartColors.value
  dscrChart = echarts.init(dscrChartRef.value, colors)
  const rows = cachedRows().filter((r) => r.year > 0)
  dscrChart.setOption(getDscrOption(rows, colors, fmtNum))
  dscrChart.resize()
}

function renderCapexChart() {
  if (!capexChartRef.value) return
  if (capexChart) capexChart.dispose()
  const colors = chartColors.value
  capexChart = echarts.init(capexChartRef.value, colors)
  const capexData = cachedCapexData()
  if (!capexData) return
  capexChart.setOption(getCapexOption(capexData, colors))
  capexChart.resize()
}

function renderCharts() {
  renderCashFlowChart()
  renderRevenueChart()
  renderDscrChart()
  renderCapexChart()
}

function render() {
  renderCharts()
}

watch(
  () => cachedRows(),
  debounce(() => renderCharts(), 300),
  { deep: true }
)

resizeHandler = () => {
  cashFlowChart?.resize()
  revenueChart?.resize()
  dscrChart?.resize()
  capexChart?.resize()
}
window.addEventListener('resize', resizeHandler)

onUnmounted(() => {
  disposeAll()
  if (resizeHandler) {
    window.removeEventListener('resize', resizeHandler)
    resizeHandler = null
  }
})

defineExpose({ render })
</script>
