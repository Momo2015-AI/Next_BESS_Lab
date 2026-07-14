<template>
  <div class="flex-1 min-h-0 overflow-hidden flex flex-col">
    <div class="flex flex-wrap gap-2 mb-3 flex-shrink-0">
      <button
        v-for="c in chartDefs"
        :key="c.id"
        :class="[
          'px-3 py-1 text-[11px] rounded font-semibold transition-all',
          activeChart === c.id ? 'chart-btn-active text-white' : 'chart-btn-inactive'
        ]"
        @click="switchChart(c.id)"
      >
        {{ c.label }}
      </button>
    </div>

    <template v-if="activeChart === 'combined'">
      <div class="flex-1 min-h-0 grid grid-cols-1 md:grid-cols-2 gap-3">
        <div
          ref="sohChartRef"
          class="w-full min-h-0 u-background-var-color-card-border-1px-solid-var-color-border-border-radius-var-radius-md-min-height-250px"
        />
        <div
          ref="rteChartRef"
          class="w-full min-h-0 u-background-var-color-card-border-1px-solid-var-color-border-border-radius-var-radius-md-min-height-250px"
        />
      </div>
    </template>

    <template v-if="activeChart === 'soh'">
      <div ref="sohChartRef" class="flex-1 min-h-0 w-full rounded-xl min-h-300 card-bordered" />
    </template>

    <template v-if="activeChart === 'rte'">
      <div ref="rteChartRef" class="flex-1 min-h-0 w-full rounded-xl min-h-300 card-bordered" />
    </template>

    <template v-if="activeChart === 'acusable'">
      <div ref="acChartRef" class="flex-1 min-h-0 w-full rounded-xl min-h-300 card-bordered" />
      <div class="flex gap-4 mt-2 flex-shrink-0 flex-wrap">
        <div class="flex items-center gap-1 text-[10px] text-secondary">
          <span class="inline-block w-3 h-3 rounded-sm bg-accent" />
          {{ $t('sohChart.initNetAc') }}
        </div>
        <div class="flex items-center gap-1 text-[10px] text-secondary">
          <span class="inline-block w-3 h-3 rounded-sm u-background-color-var-color-chart-pink" />
          {{ $t('sohChart.augNetAc') }}
        </div>
        <div class="flex items-center gap-1 text-[10px] text-secondary">
          <span class="inline-block w-3 h-3 rounded-sm bg-warning" />
          {{ $t('sohChart.reqThreshold') }}
        </div>
        <div class="flex items-center gap-1 text-[10px] text-secondary">
          <span class="inline-block w-3 h-3 rounded-sm bg-accent-2" />
          {{ $t('sohChart.totalOutput') }}
        </div>
      </div>
    </template>

    <template v-if="activeChart === 'stacked'">
      <div ref="stackedChartRef" class="flex-1 min-h-0 w-full rounded-xl min-h-300 card-bordered" />
      <div class="flex gap-4 mt-2 flex-shrink-0 flex-wrap">
        <div class="flex items-center gap-1 text-[10px] text-secondary">
          <span class="inline-block w-3 h-3 rounded-sm bg-accent" />
          {{ $t('sohChart.initNetAc') }}
        </div>
        <div class="flex items-center gap-1 text-[10px] text-secondary">
          <span class="inline-block w-3 h-3 rounded-sm u-background-color-var-color-chart-pink" />
          {{ $t('sohChart.augNetAc') }}
        </div>
        <div class="flex items-center gap-1 text-[10px] text-secondary">
          <span class="inline-block w-3 h-3 rounded-sm bg-danger" />
          {{ $t('sohChart.initAux') }}
        </div>
        <div class="flex items-center gap-1 text-[10px] text-secondary">
          <span class="inline-block w-3 h-3 rounded-sm u-background-color-var-color-chart-orange" />
          {{ $t('sohChart.augAux') }}
        </div>
      </div>
    </template>

    <template v-if="activeChart === 'degradation'">
      <div ref="degradationChartRef" class="flex-1 min-h-0 w-full rounded-xl min-h-300 card-bordered" />
    </template>

    <template v-if="activeChart === 'dashboard'">
      <div class="flex-1 min-h-0 overflow-auto">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-3">
          <div v-for="m in metrics" :key="m.label" class="rounded-xl p-3 text-center card-bordered">
            <div class="text-[10px] mb-1 text-muted">
              {{ m.label }}
            </div>
            <div :class="['text-lg font-bold font-mono', m.color]">
              {{ m.value }}
            </div>
            <div class="text-[10px] mt-0.5 text-muted">
              {{ m.sub }}
            </div>
          </div>
        </div>
        <div
          ref="dashChartRef"
          class="w-full u-background-var-color-card-border-1px-solid-var-color-border-border-radius-var-radius-md-height-300px"
        />
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useChartTheme } from '../composables/useChartTheme.js'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart, ScatterChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, GridComponent, LegendComponent, GraphicComponent } from 'echarts/components'
const { t } = useI18n()
echarts.use([
  CanvasRenderer,
  LineChart,
  BarChart,
  ScatterChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  GraphicComponent
])
const props = defineProps({ results: Object, soh: Array, rte: Array, requiredEnergy: Number })

const activeChart = ref('combined')
const chartDefs = computed(() => [
  { id: 'combined', label: t('sohChart.combined') },
  { id: 'soh', label: t('sohChart.sohCurve') },
  { id: 'rte', label: t('sohChart.rteCurve') },
  { id: 'acusable', label: t('sohChart.acUsable') },
  { id: 'stacked', label: t('sohChart.stacked') },
  { id: 'degradation', label: t('sohChart.degradation') },
  { id: 'dashboard', label: t('sohChart.dashboard') }
])

const sohChartRef = ref(null)
const rteChartRef = ref(null)
const acChartRef = ref(null)
const stackedChartRef = ref(null)
const degradationChartRef = ref(null)
const dashChartRef = ref(null)
let sohChart = null
let rteChart = null
let acChart = null
let stackedChart = null
let degradationChart = null
let dashChart = null

const { themeObject } = useChartTheme()

watch(themeObject, () => {
  nextTick(() => {
    renderAll()
  })
})

const chartColors = computed(() => ({
  ...themeObject.value,
  titleText: themeObject.value.warning,
  sohLine: themeObject.value.warning,
  rteLine: themeObject.value.info,
  augLine: themeObject.value.info,
  totalLine: themeObject.value.info,
  reqLine: themeObject.value.warning,
  initAux: themeObject.value.danger,
  augAux: themeObject.value.orange,
  initAc: themeObject.value.acLine,
  augAc: themeObject.value.cyan,
  degradation: themeObject.value.orange,
  dashboard: themeObject.value.purple
}))

const years = Array.from({ length: 26 }, (_, i) => i)

const metrics = computed(() => {
  const s = props.soh || []
  const r = props.results || {}
  const init = r.initAcUsable || []
  const total = r.totalAcUsable || []
  const req = props.requiredEnergy || 240
  const eolYear = years.find((i) => s[i] <= 0.7) ?? 26
  const meetCount = (r.meetsReq || []).filter(Boolean).length
  const degradationCagr =
    s.length > 1 ? ((1 - Math.pow(s[s.length - 1] / s[0], 1 / (s.length - 1))) * 100).toFixed(2) : '-'
  return [
    {
      label: t('sohChart.initNetAc'),
      value: init[0]?.toFixed(1) + ' MWh',
      color: 'text-teal-400',
      sub: 'Year 0 AC Usable'
    },
    { label: t('sohChart.degradation'), value: degradationCagr + '%', color: 'text-yellow-400', sub: 'CAGR 25y' },
    {
      label: t('matrixTable.meetsReq'),
      value: meetCount + ' / 26',
      color: meetCount >= 26 ? 'text-emerald-400' : 'text-amber-400',
      sub: ((meetCount / 26) * 100).toFixed(0) + '%'
    },
    {
      label: t('sohChart.sohCurve'),
      value: 'Y' + eolYear,
      color: eolYear <= 15 ? 'text-red-400' : eolYear <= 20 ? 'text-amber-400' : 'text-emerald-400',
      sub: 'SOH ≤ 70%'
    }
  ]
})

function disposeAll() {
  ;[sohChart, rteChart, acChart, stackedChart, degradationChart, dashChart].forEach((c) => {
    c?.dispose()
  })
  sohChart = rteChart = acChart = stackedChart = degradationChart = dashChart = null
}

function createSohChart() {
  if (!sohChartRef.value) return
  if (sohChart) sohChart.dispose()
  const colors = chartColors.value
  sohChart = echarts.init(sohChartRef.value, colors)
  const sohPercent = (props.soh || []).map((v) => (v * 100).toFixed(2))
  sohChart.setOption({
    title: { text: t('sohChart.sohCurve'), left: 'center', textStyle: { color: colors.titleText, fontSize: 12 } },
    tooltip: { trigger: 'axis' },
    grid: { top: 35, right: 20, bottom: 30, left: 55 },
    xAxis: {
      type: 'category',
      data: years,
      name: t('matrixTable.year'),
      axisLabel: { color: colors.axisLabel, fontSize: 10 }
    },
    yAxis: {
      type: 'value',
      min: 50,
      max: 105,
      axisLabel: { color: colors.axisLabel, fontSize: 10, formatter: (v) => v.toFixed(0) + '%' }
    },
    series: [
      {
        type: 'line',
        data: sohPercent,
        smooth: true,
        symbol: 'circle',
        symbolSize: 5,
        lineStyle: { color: colors.sohLine, width: 2 },
        itemStyle: { color: colors.sohLine },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color:
                document.documentElement.getAttribute('data-theme') === 'dark'
                  ? 'rgba(250,204,21,0.3)'
                  : 'rgba(245,158,11,0.2)'
            },
            { offset: 1, color: 'transparent' }
          ])
        },
        markLine: {
          silent: true,
          symbol: 'none',
          data: [
            {
              yAxis: 70,
              label: { formatter: 'EOL=70%', color: colors.danger, fontSize: 10 },
              lineStyle: { color: colors.danger, type: 'dashed' }
            }
          ]
        }
      }
    ]
  })
  sohChart.resize()
}

function createRteChart() {
  if (!rteChartRef.value) return
  if (rteChart) rteChart.dispose()
  const colors = chartColors.value
  rteChart = echarts.init(rteChartRef.value, colors)
  const rtePercent = (props.rte || []).map((v) => (v * 100).toFixed(2))
  rteChart.setOption({
    title: { text: t('sohChart.rteCurve'), left: 'center', textStyle: { color: colors.rteLine, fontSize: 12 } },
    tooltip: { trigger: 'axis' },
    grid: { top: 35, right: 20, bottom: 30, left: 55 },
    xAxis: {
      type: 'category',
      data: years,
      name: t('matrixTable.year'),
      axisLabel: { color: colors.axisLabel, fontSize: 10 }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: colors.axisLabel, fontSize: 10, formatter: (v) => v.toFixed(1) + '%' }
    },
    series: [
      {
        type: 'line',
        data: rtePercent,
        smooth: true,
        symbol: 'circle',
        symbolSize: 5,
        lineStyle: { color: colors.rteLine, width: 2 },
        itemStyle: { color: colors.rteLine },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color:
                document.documentElement.getAttribute('data-theme') === 'dark'
                  ? 'rgba(56,189,248,0.3)'
                  : 'rgba(14,165,233,0.2)'
            },
            { offset: 1, color: 'transparent' }
          ])
        }
      }
    ]
  })
  rteChart.resize()
}

function createAcChart() {
  if (!acChartRef.value) return
  if (acChart) acChart.dispose()
  const colors = chartColors.value
  acChart = echarts.init(acChartRef.value, colors)
  const required = new Array(26).fill(props.requiredEnergy || 240)
  acChart.setOption({
    title: { text: t('sohChart.acUsable'), left: 10, textStyle: { color: colors.acLine, fontSize: 12 } },
    tooltip: { trigger: 'axis' },
    legend: {
      data: [t('sohChart.initNetAc'), t('sohChart.augNetAc'), t('sohChart.totalOutput'), t('sohChart.reqThreshold')],
      top: 2,
      right: 10,
      textStyle: { color: colors.legendText, fontSize: 10 }
    },
    grid: { top: 40, right: 20, bottom: 30, left: 65 },
    xAxis: {
      type: 'category',
      data: years,
      name: t('matrixTable.year'),
      axisLabel: { color: colors.axisLabel, fontSize: 10 }
    },
    yAxis: { type: 'value', axisLabel: { color: colors.axisLabel, fontSize: 10, formatter: (v) => v.toFixed(0) } },
    series: [
      {
        name: t('sohChart.initNetAc'),
        type: 'line',
        data: props.results.initAcUsable,
        smooth: true,
        symbol: 'circle',
        symbolSize: 5,
        lineStyle: { color: colors.acLine, width: 2 },
        itemStyle: { color: colors.acLine },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color:
                document.documentElement.getAttribute('data-theme') === 'dark'
                  ? 'rgba(45,212,191,0.25)'
                  : 'rgba(20,184,166,0.2)'
            },
            { offset: 1, color: 'transparent' }
          ])
        }
      },
      {
        name: t('sohChart.augNetAc'),
        type: 'line',
        data: props.results.augAcUsable,
        smooth: true,
        symbol: 'diamond',
        symbolSize: 5,
        lineStyle: { color: colors.augLine, width: 2 },
        itemStyle: { color: colors.augLine },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color:
                document.documentElement.getAttribute('data-theme') === 'dark'
                  ? 'rgba(244,114,182,0.2)'
                  : 'rgba(236,72,153,0.15)'
            },
            { offset: 1, color: 'transparent' }
          ])
        }
      },
      {
        name: t('sohChart.totalOutput'),
        type: 'line',
        data: props.results.totalAcUsable,
        smooth: true,
        symbol: 'triangle',
        symbolSize: 6,
        lineStyle: { color: colors.totalLine, width: 2.5 },
        itemStyle: { color: colors.totalLine }
      },
      {
        name: t('sohChart.reqThreshold'),
        type: 'line',
        data: required,
        step: 'start',
        symbol: 'none',
        lineStyle: { color: colors.reqLine, width: 1.5, type: 'dashed' }
      }
    ]
  })
  acChart.resize()
}

function createStackedChart() {
  if (!stackedChartRef.value) return
  if (stackedChart) stackedChart.dispose()
  const colors = chartColors.value
  stackedChart = echarts.init(stackedChartRef.value, colors)
  stackedChart.setOption({
    title: { text: t('sohChart.stacked'), left: 10, textStyle: { color: colors.dashboard, fontSize: 12 } },
    tooltip: { trigger: 'axis', valueFormatter: (v) => v?.toFixed(2) + ' MWh' },
    legend: {
      data: [t('sohChart.initNetAc'), t('sohChart.augNetAc'), t('sohChart.initAux'), t('sohChart.augAux')],
      top: 2,
      right: 10,
      textStyle: { color: colors.legendText, fontSize: 10 }
    },
    grid: { top: 40, right: 20, bottom: 30, left: 65 },
    xAxis: {
      type: 'category',
      data: years,
      name: t('matrixTable.year'),
      axisLabel: { color: colors.axisLabel, fontSize: 10 }
    },
    yAxis: { type: 'value', axisLabel: { color: colors.axisLabel, fontSize: 10, formatter: (v) => v.toFixed(0) } },
    series: [
      {
        name: t('sohChart.initAux'),
        type: 'bar',
        stack: 'total',
        data: props.results.initAux,
        itemStyle: { color: colors.initAux, borderRadius: [0, 0, 0, 0] },
        barWidth: '60%'
      },
      {
        name: t('sohChart.augAux'),
        type: 'bar',
        stack: 'total',
        data: props.results.augAux,
        itemStyle: { color: colors.augAux, borderRadius: [0, 0, 0, 0] }
      },
      {
        name: t('sohChart.initNetAc'),
        type: 'bar',
        stack: 'total',
        data: props.results.initAcUsable,
        itemStyle: { color: colors.initAc, borderRadius: [0, 0, 0, 0] }
      },
      {
        name: t('sohChart.augNetAc'),
        type: 'bar',
        stack: 'total',
        data: props.results.augAcUsable,
        itemStyle: { color: colors.augAc, borderRadius: [3, 3, 0, 0] }
      }
    ]
  })
  stackedChart.resize()
}

function createDegradationChart() {
  if (!degradationChartRef.value) return
  if (degradationChart) degradationChart.dispose()
  const colors = chartColors.value
  degradationChart = echarts.init(degradationChartRef.value, colors)
  const s = props.soh || []
  const r = props.rte || []
  const sohDelta = s.map((v, i) => (i === 0 ? 0 : ((s[i - 1] - v) * 100).toFixed(2)))
  const rteDelta = r.map((v, i) => (i === 0 ? 0 : ((r[i - 1] - v) * 100).toFixed(4)))
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
  degradationChart.setOption({
    title: { text: t('sohChart.degradation'), left: 10, textStyle: { color: colors.degradation, fontSize: 12 } },
    tooltip: { trigger: 'axis' },
    legend: {
      data: [t('matrixTable.soh'), t('matrixTable.rte')],
      top: 2,
      right: 10,
      textStyle: { color: colors.legendText, fontSize: 10 }
    },
    grid: { top: 40, right: 20, bottom: 30, left: 55 },
    xAxis: { type: 'category', data: years, name: 'Year', axisLabel: { color: colors.axisLabel, fontSize: 10 } },
    yAxis: [
      {
        type: 'value',
        name: 'SOH Δ%',
        nameTextStyle: { color: colors.sohLine, fontSize: 10 },
        axisLabel: { color: colors.axisLabel, fontSize: 10 }
      },
      {
        type: 'value',
        name: 'RTE Δ%',
        nameTextStyle: { color: colors.rteLine, fontSize: 10 },
        axisLabel: { color: colors.axisLabel, fontSize: 10 }
      }
    ],
    series: [
      {
        name: t('matrixTable.soh'),
        type: 'bar',
        data: sohDelta,
        yAxisIndex: 0,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: colors.sohLine },
            { offset: 1, color: isDark ? '#b45309' : '#d97706' }
          ])
        },
        barWidth: '50%',
        markLine: {
          silent: true,
          symbol: 'none',
          data: [
            {
              yAxis: 2,
              label: { formatter: '2%/yr', color: colors.warning },
              lineStyle: { color: colors.warning, type: 'dashed' }
            }
          ]
        }
      },
      {
        name: t('matrixTable.rte'),
        type: 'line',
        data: rteDelta,
        yAxisIndex: 1,
        smooth: true,
        symbol: 'circle',
        symbolSize: 5,
        lineStyle: { color: colors.rteLine, width: 2 },
        itemStyle: { color: colors.rteLine }
      }
    ]
  })
  degradationChart.resize()
}

function createDashboardChart() {
  if (!dashChartRef.value) return
  if (dashChart) dashChart.dispose()
  const colors = chartColors.value
  dashChart = echarts.init(dashChartRef.value, colors)
  const s = (props.soh || []).map((v) => v * 100)
  const total = props.results.totalAcUsable || []
  const req = props.requiredEnergy || 240
  const statusData = (props.results.meetsReq || []).map((v, i) => ({
    value: [i, v ? 1 : 0],
    itemStyle: { color: v ? colors.success : colors.danger }
  }))
  dashChart.setOption({
    title: { text: t('sohChart.dashboard'), left: 10, textStyle: { color: colors.dashboard, fontSize: 12 } },
    tooltip: { trigger: 'axis' },
    legend: {
      data: [t('matrixTable.soh'), t('matrixTable.totalNetAc'), t('matrixTable.meetsReq')],
      top: 2,
      right: 10,
      textStyle: { color: colors.legendText, fontSize: 10 }
    },
    grid: { top: 40, right: 20, bottom: 30, left: 55 },
    xAxis: { type: 'category', data: years, name: 'Year', axisLabel: { color: colors.axisLabel, fontSize: 10 } },
    yAxis: [
      {
        type: 'value',
        name: 'SOH%',
        min: 50,
        max: 105,
        nameTextStyle: { color: colors.sohLine, fontSize: 10 },
        axisLabel: { color: colors.axisLabel, fontSize: 10 }
      },
      {
        type: 'value',
        name: 'MWh',
        nameTextStyle: { color: colors.rteLine, fontSize: 10 },
        axisLabel: { color: colors.axisLabel, fontSize: 10 }
      }
    ],
    series: [
      {
        name: t('matrixTable.soh'),
        type: 'line',
        data: s,
        smooth: true,
        yAxisIndex: 0,
        symbol: 'circle',
        symbolSize: 4,
        lineStyle: { color: colors.sohLine, width: 1.5 },
        itemStyle: { color: colors.sohLine },
        markLine: {
          silent: true,
          symbol: 'none',
          data: [
            {
              yAxis: 70,
              label: { formatter: 'EOL', color: colors.danger, fontSize: 10 },
              lineStyle: { color: colors.danger, type: 'dashed' }
            }
          ]
        }
      },
      {
        name: t('matrixTable.totalNetAc'),
        type: 'line',
        data: total,
        smooth: true,
        yAxisIndex: 1,
        symbol: 'diamond',
        symbolSize: 5,
        lineStyle: { color: colors.rteLine, width: 2 },
        itemStyle: { color: colors.rteLine },
        markLine: {
          silent: true,
          symbol: 'none',
          data: [
            {
              yAxis: req,
              label: { formatter: t('sohChart.reqThreshold') + '=' + req, color: colors.warning, fontSize: 10 },
              lineStyle: { color: colors.warning, type: 'dashed' }
            }
          ]
        }
      },
      {
        name: t('matrixTable.meetsReq'),
        type: 'scatter',
        data: statusData,
        yAxisIndex: 1,
        symbolSize: 10
      }
    ]
  })
  dashChart.resize()
}

function renderAll() {
  nextTick(() => {
    setTimeout(() => {
      const id = activeChart.value
      if (id === 'combined') {
        createSohChart()
        createRteChart()
      }
      if (id === 'soh') createSohChart()
      if (id === 'rte') createRteChart()
      if (id === 'acusable') createAcChart()
      if (id === 'stacked') createStackedChart()
      if (id === 'degradation') createDegradationChart()
      if (id === 'dashboard') createDashboardChart()
    }, 300)
  })
}

function switchChart(id) {
  if (id !== activeChart.value) {
    disposeAll()
    activeChart.value = id
    renderAll()
  }
}

let resizeHandler = null

onMounted(() => {
  resizeHandler = () => {
    sohChart?.resize()
    rteChart?.resize()
    acChart?.resize()
    stackedChart?.resize()
    degradationChart?.resize()
    dashChart?.resize()
  }
  window.addEventListener('resize', resizeHandler)
  renderAll()
})

onUnmounted(() => {
  window.removeEventListener('resize', resizeHandler)
  disposeAll()
})
</script>
