<template>
  <div class="compare-panel">
    <div v-if="!selected.length" class="empty-state">
      <span class="empty-icon">📊</span>
      <p>{{ $t('compare.selectHint') }}</p>
    </div>

    <div v-else>
      <!-- 对比表格 -->
      <div class="panel-section">
        <h3 class="section-title">
          <span class="icon">📋</span>
          {{ $t('compare.title') }} ({{ selected.length }})
        </h3>
        <div class="table-wrapper">
          <table class="compare-table">
            <thead>
              <tr>
                <th>{{ $t('compare.field') }}</th>
                <th v-for="(sol, idx) in selected" :key="sol.id || idx">
                  <span class="col-header">
                    <span class="rank-badge" :class="'rank-' + (idx + 1)">#{{ idx + 1 }}</span>
                    {{ sol.container?.model || '方案 ' + (idx + 1) }}
                  </span>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in compareRows" :key="row.key">
                <td class="row-label">{{ row.label }}</td>
                <td
                  v-for="(sol, idx) in selected"
                  :key="(sol.id || '') + '-' + idx"
                  :class="['row-value', { best: row.bestIdx === idx }]"
                >
                  {{ row.format(sol, idx) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 雷达图对比 -->
      <div v-if="selected.length >= 2" class="panel-section">
        <h3 class="section-title">
          <span class="icon">🎯</span>
          {{ $t('compare.radarChart') }}
        </h3>
        <div ref="radarChartRef" class="chart-container"></div>
      </div>

      <!-- 柱状图对比 -->
      <div v-if="selected.length >= 2" class="panel-section">
        <h3 class="section-title">
          <span class="icon">📊</span>
          {{ $t('compare.barChart') }}
        </h3>
        <div ref="barChartRef" class="chart-container"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, RadarChart } from 'echarts/charts'
import { TooltipComponent, LegendComponent, RadarComponent, GridComponent } from 'echarts/components'
import { useChartTheme } from '../composables/useChartTheme.js'

echarts.use([CanvasRenderer, BarChart, RadarChart, TooltipComponent, LegendComponent, RadarComponent, GridComponent])

const { themeObject } = useChartTheme()

watch(themeObject, () => {
  nextTick(() => {
    renderRadarChart()
    renderBarChart()
  })
})

function debounce(fn, delay = 300) {
  let timer = null
  return (...args) => {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => fn(...args), delay)
  }
}

const props = defineProps({
  solutions: { type: Array, default: () => [] }
})

const selected = ref([])
const radarChartRef = ref(null)
const barChartRef = ref(null)
let radarChart = null
let barChart = null

const compareRows = computed(() => {
  if (!selected.value.length) return []

  // Find best value for each metric
  function findBest(getter, lowerBetter = true) {
    let bestIdx = -1
    let bestVal = lowerBetter ? Infinity : -Infinity
    selected.value.forEach((sol, idx) => {
      const val = getter(sol)
      if (val == null) return
      const num = Number(val)
      if (lowerBetter ? num < bestVal : num > bestVal) {
        bestVal = num
        bestIdx = idx
      }
    })
    return bestIdx
  }

  function fmt(val, unit = '', decimals = 0) {
    if (val == null || val === '') return '—'
    const num = Number(val)
    if (isNaN(num)) return String(val)
    return num.toFixed(decimals) + unit
  }

  function fmtCurrency(val) {
    if (val == null) return '—'
    const num = Number(val)
    if (num >= 1e8) return '$' + (num / 1e8).toFixed(2) + ' 亿'
    if (num >= 1e6) return '$' + (num / 1e6).toFixed(2) + 'M'
    if (num >= 1e3) return '$' + (num / 1e3).toFixed(0) + 'K'
    return '$' + num.toFixed(0)
  }

  const rows = [
    {
      key: 'container',
      label: '集装箱型号',
      bestIdx: -1,
      format: (sol) => sol.container?.model || '—'
    },
    {
      key: 'manufacturer',
      label: '厂家',
      bestIdx: -1,
      format: (sol) => sol.container?.mfr || '—'
    },
    {
      key: 'containerQty',
      label: '集装箱数量',
      bestIdx: findBest((s) => s.containerQty, true),
      format: (sol) => fmt(sol.containerQty, ' 台')
    },
    {
      key: 'totalEnergy',
      label: '总容量',
      bestIdx: findBest((s) => s.totalEnergyMwh, false),
      format: (sol) => fmt(sol.totalEnergyMwh, ' MWh', 1)
    },
    {
      key: 'totalPower',
      label: '总功率',
      bestIdx: findBest((s) => s.totalPowerMW, false),
      format: (sol) => fmt(sol.totalPowerMW, ' MW', 1)
    },
    {
      key: 'pcsModel',
      label: 'PCS 型号',
      bestIdx: -1,
      format: (sol) => sol.pcs?.model || '—'
    },
    {
      key: 'systemRTE',
      label: '系统效率',
      bestIdx: findBest((s) => s.efficiencyChain?.systemRTE, false),
      format: (sol) => fmt(sol.efficiencyChain?.systemRTE, '%', 1)
    },
    {
      key: 'totalCapex',
      label: '总 CAPEX',
      bestIdx: findBest((s) => s.estimatedCapex?.totalCapex, true),
      format: (sol) => fmtCurrency(sol.estimatedCapex?.totalCapex)
    },
    {
      key: 'capexPerMWh',
      label: 'CAPEX/MWh',
      bestIdx: findBest((s) => s.estimatedCapex?.capexPerMWh, true),
      format: (sol) => fmtCurrency(sol.estimatedCapex?.capexPerMWh)
    },
    {
      key: 'dailyAux',
      label: '日辅耗',
      bestIdx: findBest((s) => s.auxPower?.dailyTotalAuxMWh, true),
      format: (sol) => fmt(sol.auxPower?.dailyTotalAuxMWh, ' MWh', 3)
    },
    {
      key: 'score',
      label: '综合评分',
      bestIdx: findBest((s) => s.score, false),
      format: (sol) => fmt(sol.score, '', 2)
    }
  ]

  return rows
})

function renderRadarChart() {
  if (!radarChartRef.value || selected.value.length < 2) return

  if (!radarChart) {
    radarChart = echarts.init(radarChartRef.value, themeObject.value)
  }

  const indicators = [
    { name: '总容量', max: 1 },
    { name: '总功率', max: 1 },
    { name: '系统效率', max: 1 },
    { name: '经济性', max: 1 },
    { name: '辅耗', max: 1 }
  ]

  // Normalize values to 0-1
  const allSols = selected.value
  const maxVals = {
    totalEnergy: Math.max(...allSols.map((s) => s.totalEnergyMwh || 0)),
    totalPower: Math.max(...allSols.map((s) => s.totalPowerMW || 0)),
    systemRTE: Math.max(...allSols.map((s) => s.efficiencyChain?.systemRTE || 0)),
    capexPerMWh: Math.max(...allSols.map((s) => s.estimatedCapex?.capexPerMWh || 0)),
    dailyAux: Math.max(...allSols.map((s) => s.auxPower?.dailyTotalAuxMWh || 0))
  }

  // Update indicator max values
  indicators[0].max = maxVals.totalEnergy || 100
  indicators[1].max = maxVals.totalPower || 100
  indicators[2].max = 100
  indicators[3].max = maxVals.capexPerMWh || 1000
  indicators[4].max = maxVals.dailyAux || 1

  const seriesData = allSols.map((sol, idx) => ({
    name: sol.container?.model || '方案 ' + (idx + 1),
    value: [
      sol.totalEnergyMwh || 0,
      sol.totalPowerMW || 0,
      sol.efficiencyChain?.systemRTE || 0,
      // Invert capex: lower is better
      maxVals.capexPerMWh - (sol.estimatedCapex?.capexPerMWh || 0),
      // Invert aux: lower is better
      maxVals.dailyAux - (sol.auxPower?.dailyTotalAuxMWh || 0)
    ]
  }))

  radarChart.setOption(
    {
      tooltip: { trigger: 'item' },
      legend: {
        data: seriesData.map((s) => s.name),
        bottom: 0
      },
      radar: { indicators },
      series: [
        {
          type: 'radar',
          data: seriesData
        }
      ]
    },
    true
  )
}

function renderBarChart() {
  if (!barChartRef.value || selected.value.length < 2) return

  if (!barChart) {
    barChart = echarts.init(barChartRef.value, themeObject.value)
  }

  const names = selected.value.map((s, i) => s.container?.model || '方案 ' + (i + 1))
  const capexData = selected.value.map((s) => s.estimatedCapex?.totalCapex || 0)
  const energyData = selected.value.map((s) => s.totalEnergyMwh || 0)

  barChart.setOption(
    {
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' }
      },
      legend: {
        data: ['总 CAPEX ($)', '总容量 (MWh)'],
        bottom: 0
      },
      xAxis: { type: 'category', data: names },
      yAxis: [
        { type: 'value', name: 'CAPEX ($)' },
        { type: 'value', name: '容量 (MWh)' }
      ],
      series: [
        {
          name: '总 CAPEX ($)',
          type: 'bar',
          data: capexData,
          itemStyle: { color: themeObject.value.primary }
        },
        {
          name: '总容量 (MWh)',
          type: 'bar',
          yAxisIndex: 1,
          data: energyData,
          itemStyle: { color: themeObject.value.success }
        }
      ]
    },
    true
  )
}

function handleResize() {
  radarChart?.resize()
  barChart?.resize()
}

watch(
  () => props.solutions,
  (val) => {
    selected.value = (val || []).slice(0, 5)
    nextTick(() => {
      renderRadarChart()
      renderBarChart()
    })
  },
  { immediate: true, deep: true }
)

watch(
  selected,
  debounce(() => {
    nextTick(() => {
      renderRadarChart()
      renderBarChart()
    })
  }),
  { deep: true }
)

onMounted(() => {
  window.addEventListener('resize', handleResize)
  nextTick(() => {
    renderRadarChart()
    renderBarChart()
  })
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  radarChart?.dispose()
  barChart?.dispose()
})
</script>

<style scoped>
.compare-panel {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  background: var(--card-bg, #fff);
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.empty-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: var(--text-secondary, #888);
  font-size: 0.9rem;
}

.panel-section {
  background: var(--card-bg, #fff);
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  margin: 0 0 1rem 0;
  color: var(--text-primary, #1a1a1a);
}

.table-wrapper {
  overflow-x: auto;
}

.compare-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}

.compare-table th,
.compare-table td {
  padding: 0.5rem 0.75rem;
  text-align: left;
  border-bottom: 1px solid var(--border-light, #f3f4f6);
}

.compare-table th {
  background: var(--table-header-bg, #f8fafc);
  font-weight: 600;
  color: var(--text-primary, #333);
  white-space: nowrap;
}

.col-header {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.rank-badge {
  width: 20px;
  height: 20px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 0.65rem;
  font-weight: 700;
  color: var(--color-text-on-accent);
}

.rank-1 {
  background: var(--color-warning);
}
.rank-2 {
  background: var(--color-text-secondary);
}
.rank-3 {
  background: var(--color-text-muted);
}
.rank-4,
.rank-5 {
  background: var(--color-border-light);
}

.row-label {
  font-weight: 500;
  color: var(--text-secondary, #666);
  white-space: nowrap;
}

.row-value {
  font-weight: 500;
  color: var(--text-primary, #333);
  text-align: center;
}

.row-value.best {
  color: var(--color-success);
  font-weight: 700;
}

.chart-container {
  width: 100%;
  height: 350px;
}
</style>
