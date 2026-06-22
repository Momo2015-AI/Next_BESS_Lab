<template>
  <div class="flex-1 min-h-0 overflow-hidden flex flex-col">
    <div class="flex flex-wrap gap-2 mb-3 flex-shrink-0">
      <button v-for="c in chartDefs" :key="c.id" @click="switchChart(c.id)"
        :class="['px-3 py-1 text-[11px] rounded font-semibold transition-all', activeChart === c.id ? 'text-white' : '']"
        :style="activeChart === c.id ? { background: 'var(--color-accent)' } : { background: 'var(--color-bg-secondary)', color: 'var(--color-text-secondary)' }">
        {{ c.label }}
      </button>
    </div>

    <template v-if="activeChart === 'combined'">
      <div class="flex-1 min-h-0 grid grid-cols-1 md:grid-cols-2 gap-3">
        <div ref="sohChartRef" style="background: var(--color-card); border: 1px solid var(--color-border); border-radius: var(--radius-md); width: 100%; height: 100%; min-height: 200px;"></div>
        <div ref="rteChartRef" style="background: var(--color-card); border: 1px solid var(--color-border); border-radius: var(--radius-md); width: 100%; height: 100%; min-height: 200px;"></div>
      </div>
    </template>

    <template v-if="activeChart === 'soh'">
      <div ref="sohChartRef" class="flex-1 min-h-0 bg-slate-900/80 rounded-xl border border-slate-800/80 w-full" style="min-height:200px"></div>
    </template>

    <template v-if="activeChart === 'rte'">
      <div ref="rteChartRef" class="flex-1 min-h-0 bg-slate-900/80 rounded-xl border border-slate-800/80 w-full" style="min-height:200px"></div>
    </template>

    <template v-if="activeChart === 'acusable'">
      <div ref="acChartRef" class="flex-1 min-h-0 bg-slate-900/80 rounded-xl border border-slate-800/80 w-full" style="min-height:200px"></div>
      <div class="flex gap-4 mt-2 flex-shrink-0 flex-wrap">
        <div class="flex items-center gap-1 text-[10px]"><span class="inline-block w-3 h-3 bg-teal-500 rounded-sm"></span> 存量净可用</div>
        <div class="flex items-center gap-1 text-[10px]"><span class="inline-block w-3 h-3 bg-pink-500 rounded-sm"></span> 补容净可用</div>
        <div class="flex items-center gap-1 text-[10px]"><span class="inline-block w-3 h-3 bg-amber-500 rounded-sm"></span> 承诺底线</div>
        <div class="flex items-center gap-1 text-[10px]"><span class="inline-block w-3 h-3 bg-sky-500 rounded-sm"></span> 总输出</div>
      </div>
    </template>

    <template v-if="activeChart === 'stacked'">
      <div ref="stackedChartRef" class="flex-1 min-h-0 bg-slate-900/80 rounded-xl border border-slate-800/80 w-full" style="min-height:200px"></div>
      <div class="flex gap-4 mt-2 flex-shrink-0 flex-wrap">
        <div class="flex items-center gap-1 text-[10px]"><span class="inline-block w-3 h-3 bg-teal-500 rounded-sm"></span> 存量净可用</div>
        <div class="flex items-center gap-1 text-[10px]"><span class="inline-block w-3 h-3 bg-pink-500 rounded-sm"></span> 补容净可用</div>
        <div class="flex items-center gap-1 text-[10px]"><span class="inline-block w-3 h-3 bg-rose-500 rounded-sm"></span> 存量自辅耗</div>
        <div class="flex items-center gap-1 text-[10px]"><span class="inline-block w-3 h-3 bg-orange-500 rounded-sm"></span> 补容自辅耗</div>
      </div>
    </template>

    <template v-if="activeChart === 'degradation'">
      <div ref="degradationChartRef" class="flex-1 min-h-0 bg-slate-900/80 rounded-xl border border-slate-800/80 w-full" style="min-height:200px"></div>
    </template>

    <template v-if="activeChart === 'dashboard'">
      <div class="flex-1 min-h-0 overflow-auto">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-3">
          <div v-for="m in metrics" :key="m.label" class="bg-slate-900/80 rounded-xl p-3 border border-slate-800/80 text-center">
            <div class="text-[10px] text-slate-400 mb-1">{{ m.label }}</div>
            <div :class="['text-lg font-bold font-mono', m.color]">{{ m.value }}</div>
            <div class="text-[10px] text-slate-500 mt-0.5">{{ m.sub }}</div>
          </div>
        </div>
        <div ref="dashChartRef" class="w-full" style="background: var(--color-card); border: 1px solid var(--color-border); border-radius: var(--radius-md); height:260px"></div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import * as echarts from 'echarts'

const { t } = useI18n()
const props = defineProps({ results: Object, soh: Array, rte: Array, requiredEnergy: Number })

const activeChart = ref('combined')
const chartDefs = computed(() => [
  { id: 'combined', label: t('sohChart.combined') },
  { id: 'soh', label: t('sohChart.sohCurve') },
  { id: 'rte', label: t('sohChart.rteCurve') },
  { id: 'acusable', label: t('sohChart.acUsable') },
  { id: 'stacked', label: t('sohChart.stacked') },
  { id: 'degradation', label: t('sohChart.degradation') },
  { id: 'dashboard', label: t('sohChart.dashboard') },
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

const darkTheme = computed(() => {
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
  return {
    textStyle: { color: isDark ? '#94a3b8' : '#64748b' },
    backgroundColor: 'transparent',
  }
})

const years = Array.from({ length: 26 }, (_, i) => i)

const metrics = computed(() => {
  const s = props.soh || []
  const r = props.results || {}
  const init = r.initAcUsable || []
  const total = r.totalAcUsable || []
  const req = props.requiredEnergy || 240
  const eolYear = years.find(i => s[i] <= 0.7) ?? 26
  const meetCount = (r.meetsReq || []).filter(Boolean).length
  const degradationCagr = s.length > 1 ? ((1 - Math.pow(s[s.length-1] / s[0], 1 / (s.length-1))) * 100).toFixed(2) : '-'
  return [
    { label: t('sohChart.initNetAc'), value: init[0]?.toFixed(1) + ' MWh', color: 'text-teal-400', sub: 'Year 0 AC Usable' },
    { label: t('sohChart.degradation'), value: degradationCagr + '%', color: 'text-yellow-400', sub: 'CAGR 25y' },
    { label: t('matrixTable.meetsReq'), value: meetCount + ' / 26', color: meetCount >= 26 ? 'text-emerald-400' : 'text-amber-400', sub: (meetCount/26*100).toFixed(0) + '%' },
    { label: t('sohChart.sohCurve'), value: 'Y' + eolYear, color: eolYear <= 15 ? 'text-red-400' : eolYear <= 20 ? 'text-amber-400' : 'text-emerald-400', sub: 'SOH ≤ 70%' },
  ]
})

function disposeAll() {
  [sohChart, rteChart, acChart, stackedChart, degradationChart, dashChart].forEach(c => { c?.dispose() })
  sohChart = rteChart = acChart = stackedChart = degradationChart = dashChart = null
}

function createSohChart() {
  if (!sohChartRef.value) return
  if (sohChart) sohChart.dispose()
  sohChart = echarts.init(sohChartRef.value, darkTheme.value)
  const sohPercent = (props.soh || []).map(v => (v * 100).toFixed(2))
  sohChart.setOption({
    title: { text: t('sohChart.sohCurve'), left: 'center', textStyle: { color: '#facc15', fontSize: 12 } },
    tooltip: { trigger: 'axis' },
    grid: { top: 35, right: 20, bottom: 30, left: 55 },
    xAxis: { type: 'category', data: years, name: t('matrixTable.year'), axisLabel: { color: '#64748b', fontSize: 10 } },
    yAxis: { type: 'value', min: 50, max: 105, axisLabel: { color: '#64748b', fontSize: 10, formatter: v => v.toFixed(0) + '%' } },
    series: [{
      type: 'line', data: sohPercent, smooth: true, symbol: 'circle', symbolSize: 5,
      lineStyle: { color: '#facc15', width: 2 }, itemStyle: { color: '#facc15' },
      areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: 'rgba(250,204,21,0.3)' }, { offset: 1, color: 'rgba(250,204,21,0)' }
      ])},
      markLine: { silent: true, symbol: 'none', data: [{ yAxis: 70, label: { formatter: 'EOL=70%', color: '#ef4444', fontSize: 10 }, lineStyle: { color: '#ef4444', type: 'dashed' } }] },
    }],
  })
  sohChart.resize()
}

function createRteChart() {
  if (!rteChartRef.value) return
  if (rteChart) rteChart.dispose()
  rteChart = echarts.init(rteChartRef.value, darkTheme.value)
  const rtePercent = (props.rte || []).map(v => (v * 100).toFixed(2))
  rteChart.setOption({
    title: { text: t('sohChart.rteCurve'), left: 'center', textStyle: { color: '#38bdf8', fontSize: 12 } },
    tooltip: { trigger: 'axis' },
    grid: { top: 35, right: 20, bottom: 30, left: 55 },
    xAxis: { type: 'category', data: years, name: t('matrixTable.year'), axisLabel: { color: '#64748b', fontSize: 10 } },
    yAxis: { type: 'value', axisLabel: { color: '#64748b', fontSize: 10, formatter: v => v.toFixed(1) + '%' } },
    series: [{
      type: 'line', data: rtePercent, smooth: true, symbol: 'circle', symbolSize: 5,
      lineStyle: { color: '#38bdf8', width: 2 }, itemStyle: { color: '#38bdf8' },
      areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: 'rgba(56,189,248,0.3)' }, { offset: 1, color: 'rgba(56,189,248,0)' }
      ])},
    }],
  })
  rteChart.resize()
}

function createAcChart() {
  if (!acChartRef.value) return
  if (acChart) acChart.dispose()
  acChart = echarts.init(acChartRef.value, darkTheme.value)
  const required = new Array(26).fill(props.requiredEnergy || 240)
  acChart.setOption({
    title: { text: t('sohChart.acUsable'), left: 10, textStyle: { color: '#2dd4bf', fontSize: 12 } },
    tooltip: { trigger: 'axis' },
    legend: { data: [t('sohChart.initNetAc'), t('sohChart.augNetAc'), t('sohChart.totalOutput'), t('sohChart.reqThreshold')], top: 2, right: 10, textStyle: { color: '#94a3b8', fontSize: 10 } },
    grid: { top: 40, right: 20, bottom: 30, left: 65 },
    xAxis: { type: 'category', data: years, name: t('matrixTable.year'), axisLabel: { color: '#64748b', fontSize: 10 } },
    yAxis: { type: 'value', axisLabel: { color: '#64748b', fontSize: 10, formatter: v => v.toFixed(0) } },
    series: [
      {
        name: t('sohChart.initNetAc'), type: 'line', data: props.results.initAcUsable, smooth: true,
        symbol: 'circle', symbolSize: 5, lineStyle: { color: '#2dd4bf', width: 2 }, itemStyle: { color: '#2dd4bf' },
        areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(45,212,191,0.25)' }, { offset: 1, color: 'rgba(45,212,191,0)' }
        ])},
      },
      {
        name: t('sohChart.augNetAc'), type: 'line', data: props.results.augAcUsable, smooth: true,
        symbol: 'diamond', symbolSize: 5, lineStyle: { color: '#f472b6', width: 2 }, itemStyle: { color: '#f472b6' },
        areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(244,114,182,0.2)' }, { offset: 1, color: 'rgba(244,114,182,0)' }
        ])},
      },
      {
        name: t('sohChart.totalOutput'), type: 'line', data: props.results.totalAcUsable, smooth: true,
        symbol: 'triangle', symbolSize: 6, lineStyle: { color: '#38bdf8', width: 2.5 }, itemStyle: { color: '#38bdf8' },
      },
      {
        name: t('sohChart.reqThreshold'), type: 'line', data: required, step: 'start',
        symbol: 'none', lineStyle: { color: '#f59e0b', width: 1.5, type: 'dashed' },
      },
    ],
  })
  acChart.resize()
}

function createStackedChart() {
  if (!stackedChartRef.value) return
  if (stackedChart) stackedChart.dispose()
  stackedChart = echarts.init(stackedChartRef.value, darkTheme.value)
  stackedChart.setOption({
    title: { text: t('sohChart.stacked'), left: 10, textStyle: { color: '#c084fc', fontSize: 12 } },
    tooltip: { trigger: 'axis', valueFormatter: v => v?.toFixed(2) + ' MWh' },
    legend: { data: [t('sohChart.initNetAc'), t('sohChart.augNetAc'), t('sohChart.initAux'), t('sohChart.augAux')], top: 2, right: 10, textStyle: { color: '#94a3b8', fontSize: 10 } },
    grid: { top: 40, right: 20, bottom: 30, left: 65 },
    xAxis: { type: 'category', data: years, name: t('matrixTable.year'), axisLabel: { color: '#64748b', fontSize: 10 } },
    yAxis: { type: 'value', axisLabel: { color: '#64748b', fontSize: 10, formatter: v => v.toFixed(0) } },
    series: [
      {
        name: t('sohChart.initAux'), type: 'bar', stack: 'total', data: props.results.initAux,
        itemStyle: { color: '#e11d48', borderRadius: [0, 0, 0, 0] }, barWidth: '60%',
      },
      {
        name: t('sohChart.augAux'), type: 'bar', stack: 'total', data: props.results.augAux,
        itemStyle: { color: '#ea580c', borderRadius: [0, 0, 0, 0] },
      },
      {
        name: t('sohChart.initNetAc'), type: 'bar', stack: 'total', data: props.results.initAcUsable,
        itemStyle: { color: '#14b8a6', borderRadius: [0, 0, 0, 0] },
      },
      {
        name: t('sohChart.augNetAc'), type: 'bar', stack: 'total', data: props.results.augAcUsable,
        itemStyle: { color: '#ec4899', borderRadius: [3, 3, 0, 0] },
      },
    ],
  })
  stackedChart.resize()
}

function createDegradationChart() {
  if (!degradationChartRef.value) return
  if (degradationChart) degradationChart.dispose()
  degradationChart = echarts.init(degradationChartRef.value, darkTheme.value)
  const s = props.soh || []
  const r = props.rte || []
  const sohDelta = s.map((v, i) => i === 0 ? 0 : ((s[i-1] - v) * 100).toFixed(2))
  const rteDelta = r.map((v, i) => i === 0 ? 0 : ((r[i-1] - v) * 100).toFixed(4))
  degradationChart.setOption({
    title: { text: t('sohChart.degradation'), left: 10, textStyle: { color: '#fb923c', fontSize: 12 } },
    tooltip: { trigger: 'axis' },
    legend: { data: [t('matrixTable.soh'), t('matrixTable.rte')], top: 2, right: 10, textStyle: { color: '#94a3b8', fontSize: 10 } },
    grid: { top: 40, right: 20, bottom: 30, left: 55 },
    xAxis: { type: 'category', data: years, name: 'Year', axisLabel: { color: '#64748b', fontSize: 10 } },
    yAxis: [
      { type: 'value', name: 'SOH Δ%', nameTextStyle: { color: '#facc15', fontSize: 10 }, axisLabel: { color: '#64748b', fontSize: 10 } },
      { type: 'value', name: 'RTE Δ%', nameTextStyle: { color: '#38bdf8', fontSize: 10 }, axisLabel: { color: '#64748b', fontSize: 10 } },
    ],
    series: [
      {
        name: t('matrixTable.soh'), type: 'bar', data: sohDelta, yAxisIndex: 0,
        itemStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#facc15' }, { offset: 1, color: '#b45309' }
        ])}, barWidth: '50%',
        markLine: { silent: true, symbol: 'none', data: [{ yAxis: 2, label: { formatter: '2%/yr', color: '#f59e0b' }, lineStyle: { color: '#f59e0b', type: 'dashed' } }] },
      },
      {
        name: t('matrixTable.rte'), type: 'line', data: rteDelta, yAxisIndex: 1, smooth: true,
        symbol: 'circle', symbolSize: 5, lineStyle: { color: '#38bdf8', width: 2 }, itemStyle: { color: '#38bdf8' },
      },
    ],
  })
  degradationChart.resize()
}

function createDashboardChart() {
  if (!dashChartRef.value) return
  if (dashChart) dashChart.dispose()
  dashChart = echarts.init(dashChartRef.value, darkTheme.value)
  const s = (props.soh || []).map(v => v * 100)
  const total = props.results.totalAcUsable || []
  const req = props.requiredEnergy || 240
  const statusData = (props.results.meetsReq || []).map((v, i) => ({
    value: [i, v ? 1 : 0],
    itemStyle: { color: v ? '#10b981' : '#ef4444' }
  }))
  dashChart.setOption({
    title: { text: t('sohChart.dashboard'), left: 10, textStyle: { color: '#c084fc', fontSize: 12 } },
    tooltip: { trigger: 'axis' },
    legend: { data: [t('matrixTable.soh'), t('matrixTable.totalNetAc'), t('matrixTable.meetsReq')], top: 2, right: 10, textStyle: { color: '#94a3b8', fontSize: 10 } },
    grid: { top: 40, right: 20, bottom: 30, left: 55 },
    xAxis: { type: 'category', data: years, name: 'Year', axisLabel: { color: '#64748b', fontSize: 10 } },
    yAxis: [
      { type: 'value', name: 'SOH%', min: 50, max: 105, nameTextStyle: { color: '#facc15', fontSize: 10 }, axisLabel: { color: '#64748b', fontSize: 10 } },
      { type: 'value', name: 'MWh', nameTextStyle: { color: '#38bdf8', fontSize: 10 }, axisLabel: { color: '#64748b', fontSize: 10 } },
    ],
    series: [
      {
        name: t('matrixTable.soh'), type: 'line', data: s, smooth: true, yAxisIndex: 0,
        symbol: 'circle', symbolSize: 4, lineStyle: { color: '#facc15', width: 1.5 }, itemStyle: { color: '#facc15' },
        markLine: { silent: true, symbol: 'none', data: [{ yAxis: 70, label: { formatter: 'EOL', color: '#ef4444', fontSize: 10 }, lineStyle: { color: '#ef4444', type: 'dashed' } }] },
      },
      {
        name: t('matrixTable.totalNetAc'), type: 'line', data: total, smooth: true, yAxisIndex: 1,
        symbol: 'diamond', symbolSize: 5, lineStyle: { color: '#38bdf8', width: 2 }, itemStyle: { color: '#38bdf8' },
        markLine: { silent: true, symbol: 'none', data: [{ yAxis: req, label: { formatter: t('sohChart.reqThreshold') + '=' + req, color: '#f59e0b', fontSize: 10 }, lineStyle: { color: '#f59e0b', type: 'dashed' } }] },
      },
      {
        name: t('matrixTable.meetsReq'), type: 'scatter', data: statusData, yAxisIndex: 1,
        symbolSize: 10,
      },
    ],
  })
  dashChart.resize()
}

function renderAll() {
  nextTick(() => {
    setTimeout(() => {
      const id = activeChart.value
      if (id === 'combined') { createSohChart(); createRteChart() }
      if (id === 'soh') createSohChart()
      if (id === 'rte') createRteChart()
      if (id === 'acusable') createAcChart()
      if (id === 'stacked') createStackedChart()
      if (id === 'degradation') createDegradationChart()
      if (id === 'dashboard') createDashboardChart()
    }, 150)
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
    sohChart?.resize(); rteChart?.resize(); acChart?.resize()
    stackedChart?.resize(); degradationChart?.resize(); dashChart?.resize()
  }
  window.addEventListener('resize', resizeHandler)
  renderAll()
})

onUnmounted(() => {
  window.removeEventListener('resize', resizeHandler)
  disposeAll()
})
</script>
