<template>
  <div class="flex-1 min-h-0 overflow-hidden flex flex-col">
    <div class="flex flex-wrap gap-2 mb-3 flex-shrink-0">
      <button v-for="c in charts" :key="c.id" @click="switchChart(c.id)"
        :class="['px-3 py-1 text-[11px] rounded font-semibold transition-all', activeChart === c.id ? 'bg-teal-600 text-white' : 'bg-slate-800 text-slate-400 hover:text-slate-200']">
        {{ c.label }}
      </button>
    </div>

    <template v-if="activeChart === 'combined'">
      <div class="flex-1 min-h-0 grid grid-cols-1 md:grid-cols-2 gap-3">
        <div ref="sohChartRef" class="bg-slate-900/80 rounded-xl border border-slate-800/80 w-full h-full" style="min-height:200px"></div>
        <div ref="rteChartRef" class="bg-slate-900/80 rounded-xl border border-slate-800/80 w-full h-full" style="min-height:200px"></div>
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
        <div ref="dashChartRef" class="bg-slate-900/80 rounded-xl border border-slate-800/80 w-full" style="height:260px"></div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({ results: Object, soh: Array, rte: Array, requiredEnergy: Number })

const activeChart = ref('combined')
const charts = [
  { id: 'combined', label: 'SOH + RTE 双曲线' },
  { id: 'soh', label: 'SOH 衰减曲线' },
  { id: 'rte', label: 'RTE 效率曲线' },
  { id: 'acusable', label: '网侧净可用趋势' },
  { id: 'stacked', label: '堆叠能量构成' },
  { id: 'degradation', label: '年度衰减速率' },
  { id: 'dashboard', label: '关键指标仪表盘' },
]

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

const darkTheme = { textStyle: { color: '#94a3b8' }, backgroundColor: 'transparent' }

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
    { label: '初始年净可用', value: init[0]?.toFixed(1) + ' MWh', color: 'text-teal-400', sub: 'Year 0 AC Usable' },
    { label: 'SOH 年均衰减率', value: degradationCagr + '%', color: 'text-yellow-400', sub: 'CAGR over 25 years' },
    { label: '达标年份数', value: meetCount + ' / 26', color: meetCount >= 26 ? 'text-emerald-400' : 'text-amber-400', sub: '达标占比 ' + (meetCount/26*100).toFixed(0) + '%' },
    { label: '预测 EOL 年份', value: 'Y' + eolYear, color: eolYear <= 15 ? 'text-red-400' : eolYear <= 20 ? 'text-amber-400' : 'text-emerald-400', sub: 'SOH ≤ 70% 阈值' },
  ]
})

function disposeAll() {
  [sohChart, rteChart, acChart, stackedChart, degradationChart, dashChart].forEach(c => { c?.dispose() })
  sohChart = rteChart = acChart = stackedChart = degradationChart = dashChart = null
}

function createSohChart() {
  if (!sohChartRef.value) return
  if (sohChart) sohChart.dispose()
  sohChart = echarts.init(sohChartRef.value, darkTheme)
  const sohPercent = (props.soh || []).map(v => (v * 100).toFixed(2))
  sohChart.setOption({
    title: { text: 'SOH 健康状态衰减曲线', left: 'center', textStyle: { color: '#facc15', fontSize: 12 } },
    tooltip: { trigger: 'axis' },
    grid: { top: 35, right: 20, bottom: 30, left: 55 },
    xAxis: { type: 'category', data: years, name: 'Year', axisLabel: { color: '#64748b', fontSize: 10 } },
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
  rteChart = echarts.init(rteChartRef.value, darkTheme)
  const rtePercent = (props.rte || []).map(v => (v * 100).toFixed(2))
  rteChart.setOption({
    title: { text: 'RTE 系统效率衰减曲线', left: 'center', textStyle: { color: '#38bdf8', fontSize: 12 } },
    tooltip: { trigger: 'axis' },
    grid: { top: 35, right: 20, bottom: 30, left: 55 },
    xAxis: { type: 'category', data: years, name: 'Year', axisLabel: { color: '#64748b', fontSize: 10 } },
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
  acChart = echarts.init(acChartRef.value, darkTheme)
  const required = new Array(26).fill(props.requiredEnergy || 240)
  acChart.setOption({
    title: { text: '单次循环网侧净可用能量趋势 (MWh)', left: 10, textStyle: { color: '#2dd4bf', fontSize: 12 } },
    tooltip: { trigger: 'axis' },
    legend: { data: ['存量净可用', '补容净可用', '总输出', '承诺底线'], top: 2, right: 10, textStyle: { color: '#94a3b8', fontSize: 10 } },
    grid: { top: 40, right: 20, bottom: 30, left: 65 },
    xAxis: { type: 'category', data: years, name: 'Year', axisLabel: { color: '#64748b', fontSize: 10 } },
    yAxis: { type: 'value', axisLabel: { color: '#64748b', fontSize: 10, formatter: v => v.toFixed(0) } },
    series: [
      {
        name: '存量净可用', type: 'line', data: props.results.initAcUsable, smooth: true,
        symbol: 'circle', symbolSize: 5, lineStyle: { color: '#2dd4bf', width: 2 }, itemStyle: { color: '#2dd4bf' },
        areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(45,212,191,0.25)' }, { offset: 1, color: 'rgba(45,212,191,0)' }
        ])},
      },
      {
        name: '补容净可用', type: 'line', data: props.results.augAcUsable, smooth: true,
        symbol: 'diamond', symbolSize: 5, lineStyle: { color: '#f472b6', width: 2 }, itemStyle: { color: '#f472b6' },
        areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(244,114,182,0.2)' }, { offset: 1, color: 'rgba(244,114,182,0)' }
        ])},
      },
      {
        name: '总输出', type: 'line', data: props.results.totalAcUsable, smooth: true,
        symbol: 'triangle', symbolSize: 6, lineStyle: { color: '#38bdf8', width: 2.5 }, itemStyle: { color: '#38bdf8' },
      },
      {
        name: '承诺底线', type: 'line', data: required, step: 'start',
        symbol: 'none', lineStyle: { color: '#f59e0b', width: 1.5, type: 'dashed' },
      },
    ],
  })
  acChart.resize()
}

function createStackedChart() {
  if (!stackedChartRef.value) return
  if (stackedChart) stackedChart.dispose()
  stackedChart = echarts.init(stackedChartRef.value, darkTheme)
  stackedChart.setOption({
    title: { text: '单次循环能量构成堆叠图 (MWh)', left: 10, textStyle: { color: '#c084fc', fontSize: 12 } },
    tooltip: { trigger: 'axis', valueFormatter: v => v?.toFixed(2) + ' MWh' },
    legend: { data: ['存量净可用', '补容净可用', '存量自辅耗', '补容自辅耗'], top: 2, right: 10, textStyle: { color: '#94a3b8', fontSize: 10 } },
    grid: { top: 40, right: 20, bottom: 30, left: 65 },
    xAxis: { type: 'category', data: years, name: 'Year', axisLabel: { color: '#64748b', fontSize: 10 } },
    yAxis: { type: 'value', axisLabel: { color: '#64748b', fontSize: 10, formatter: v => v.toFixed(0) } },
    series: [
      {
        name: '存量自辅耗', type: 'bar', stack: 'total', data: props.results.initAux,
        itemStyle: { color: '#e11d48', borderRadius: [0, 0, 0, 0] }, barWidth: '60%',
      },
      {
        name: '补容自辅耗', type: 'bar', stack: 'total', data: props.results.augAux,
        itemStyle: { color: '#ea580c', borderRadius: [0, 0, 0, 0] },
      },
      {
        name: '存量净可用', type: 'bar', stack: 'total', data: props.results.initAcUsable,
        itemStyle: { color: '#14b8a6', borderRadius: [0, 0, 0, 0] },
      },
      {
        name: '补容净可用', type: 'bar', stack: 'total', data: props.results.augAcUsable,
        itemStyle: { color: '#ec4899', borderRadius: [3, 3, 0, 0] },
      },
    ],
  })
  stackedChart.resize()
}

function createDegradationChart() {
  if (!degradationChartRef.value) return
  if (degradationChart) degradationChart.dispose()
  degradationChart = echarts.init(degradationChartRef.value, darkTheme)
  const s = props.soh || []
  const r = props.rte || []
  const sohDelta = s.map((v, i) => i === 0 ? 0 : ((s[i-1] - v) * 100).toFixed(2))
  const rteDelta = r.map((v, i) => i === 0 ? 0 : ((r[i-1] - v) * 100).toFixed(4))
  degradationChart.setOption({
    title: { text: '年度衰减速率 (百分点/年)', left: 10, textStyle: { color: '#fb923c', fontSize: 12 } },
    tooltip: { trigger: 'axis' },
    legend: { data: ['SOH 年衰减', 'RTE 年衰减'], top: 2, right: 10, textStyle: { color: '#94a3b8', fontSize: 10 } },
    grid: { top: 40, right: 20, bottom: 30, left: 55 },
    xAxis: { type: 'category', data: years, name: 'Year', axisLabel: { color: '#64748b', fontSize: 10 } },
    yAxis: [
      { type: 'value', name: 'SOH Δ%', nameTextStyle: { color: '#facc15', fontSize: 10 }, axisLabel: { color: '#64748b', fontSize: 10 } },
      { type: 'value', name: 'RTE Δ%', nameTextStyle: { color: '#38bdf8', fontSize: 10 }, axisLabel: { color: '#64748b', fontSize: 10 } },
    ],
    series: [
      {
        name: 'SOH 年衰减', type: 'bar', data: sohDelta, yAxisIndex: 0,
        itemStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#facc15' }, { offset: 1, color: '#b45309' }
        ])}, barWidth: '50%',
        markLine: { silent: true, symbol: 'none', data: [{ yAxis: 2, label: { formatter: '2%/yr', color: '#f59e0b' }, lineStyle: { color: '#f59e0b', type: 'dashed' } }] },
      },
      {
        name: 'RTE 年衰减', type: 'line', data: rteDelta, yAxisIndex: 1, smooth: true,
        symbol: 'circle', symbolSize: 5, lineStyle: { color: '#38bdf8', width: 2 }, itemStyle: { color: '#38bdf8' },
      },
    ],
  })
  degradationChart.resize()
}

function createDashboardChart() {
  if (!dashChartRef.value) return
  if (dashChart) dashChart.dispose()
  dashChart = echarts.init(dashChartRef.value, darkTheme)
  const s = (props.soh || []).map(v => v * 100)
  const total = props.results.totalAcUsable || []
  const req = props.requiredEnergy || 240
  const statusData = (props.results.meetsReq || []).map((v, i) => ({
    value: [i, v ? 1 : 0],
    itemStyle: { color: v ? '#10b981' : '#ef4444' }
  }))
  dashChart.setOption({
    title: { text: '25年生命周期综合视图', left: 10, textStyle: { color: '#c084fc', fontSize: 12 } },
    tooltip: { trigger: 'axis' },
    legend: { data: ['SOH%', '总净可用(MWh)', '达标状态'], top: 2, right: 10, textStyle: { color: '#94a3b8', fontSize: 10 } },
    grid: { top: 40, right: 20, bottom: 30, left: 55 },
    xAxis: { type: 'category', data: years, name: 'Year', axisLabel: { color: '#64748b', fontSize: 10 } },
    yAxis: [
      { type: 'value', name: 'SOH%', min: 50, max: 105, nameTextStyle: { color: '#facc15', fontSize: 10 }, axisLabel: { color: '#64748b', fontSize: 10 } },
      { type: 'value', name: 'MWh', nameTextStyle: { color: '#38bdf8', fontSize: 10 }, axisLabel: { color: '#64748b', fontSize: 10 } },
    ],
    series: [
      {
        name: 'SOH%', type: 'line', data: s, smooth: true, yAxisIndex: 0,
        symbol: 'circle', symbolSize: 4, lineStyle: { color: '#facc15', width: 1.5 }, itemStyle: { color: '#facc15' },
        markLine: { silent: true, symbol: 'none', data: [{ yAxis: 70, label: { formatter: 'EOL', color: '#ef4444', fontSize: 10 }, lineStyle: { color: '#ef4444', type: 'dashed' } }] },
      },
      {
        name: '总净可用(MWh)', type: 'line', data: total, smooth: true, yAxisIndex: 1,
        symbol: 'diamond', symbolSize: 5, lineStyle: { color: '#38bdf8', width: 2 }, itemStyle: { color: '#38bdf8' },
        markLine: { silent: true, symbol: 'none', data: [{ yAxis: req, label: { formatter: '底线=' + req, color: '#f59e0b', fontSize: 10 }, lineStyle: { color: '#f59e0b', type: 'dashed' } }] },
      },
      {
        name: '达标状态', type: 'scatter', data: statusData, yAxisIndex: 1,
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
