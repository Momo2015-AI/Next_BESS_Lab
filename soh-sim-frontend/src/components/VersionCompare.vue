<template>
  <div class="version-compare-panel">
    <div v-if="!hasResult" class="empty-state">
      <span class="empty-icon">🔄</span>
      <p>{{ $t('versionCompare.selectHint') }}</p>
    </div>

    <div v-else>
      <div class="panel-section">
        <h3 class="section-title">
          <span class="icon">📊</span> {{ $t('versionCompare.title') }}
        </h3>

        <!-- 版本信息 -->
        <div class="version-headers">
          <div v-for="(v, idx) in versions" :key="v.id" class="version-header">
            <span class="version-name">{{ v.name || ('v' + v.version_num) }}</span>
            <span class="version-meta">v{{ v.version_num }}</span>
          </div>
        </div>

        <!-- 差异表格 -->
        <div class="table-wrapper">
          <table class="delta-table">
            <thead>
              <tr>
                <th>{{ $t('versionCompare.metric') }}</th>
                <th v-for="(v, idx) in versions" :key="v.id">
                  {{ v.name || ('v' + v.version_num) }}
                </th>
                <th>{{ $t('versionCompare.diff') }}</th>
                <th>%</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in deltaRows" :key="row.key">
                <td class="row-label">{{ row.label }}</td>
                <td
                  v-for="(v, idx) in versions"
                  :key="v.id"
                  :class="['row-value', { best: row.bestIdx === idx }]"
                >
                  {{ row.formatVal(row.values[idx]) }}
                </td>
                <td :class="['row-diff', row.diff > 0 ? 'positive' : 'negative']">
                  {{ row.diff > 0 ? '+' : '' }}{{ row.formatDiff(row.diff) }}
                </td>
                <td :class="['row-pct', row.pct > 0 ? 'positive' : 'negative']">
                  {{ row.pct > 0 ? '+' : '' }}{{ row.pct.toFixed(1) }}%
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 雷达图 -->
      <div class="panel-section">
        <h3 class="section-title">
          <span class="icon">🎯</span> {{ $t('versionCompare.radarChart') }}
        </h3>
        <div ref="radarRef" class="chart-container"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { RadarChart } from 'echarts/charts'
import { TooltipComponent, LegendComponent, RadarComponent } from 'echarts/components'
import { useChartTheme } from '../composables/useChartTheme.js'

echarts.use([CanvasRenderer, RadarChart, TooltipComponent, LegendComponent, RadarComponent])

const { themeObject } = useChartTheme()

watch(themeObject, () => {
  nextTick(renderRadar)
})

function debounce(fn, delay = 300) {
  let timer = null
  return (...args) => {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => fn(...args), delay)
  }
}

const props = defineProps({
  compareResult: { type: Object, default: null }
})

const radarRef = ref(null)
let radarChart = null

const versions = computed(() => props.compareResult?.versions || [])
const delta = computed(() => props.compareResult?.delta || {})
const hasResult = computed(() => versions.value.length >= 2)

function fmtCurrency(val) {
  if (val == null) return '—'
  const num = Number(val)
  if (num >= 1e8) return '$' + (num / 1e8).toFixed(2) + ' 亿'
  if (num >= 1e6) return '$' + (num / 1e6).toFixed(2) + 'M'
  return '$' + num.toFixed(0)
}

function fmtNum(val, decimals = 2) {
  if (val == null) return '—'
  return Number(val).toFixed(decimals)
}

const deltaRows = computed(() => {
  if (!hasResult.value) return []

  const rowDefs = [
    { key: 'irr', label: 'IRR', format: (v) => fmtNum(v, 2) + '%', lowerBetter: false },
    { key: 'npv', label: 'NPV', format: fmtCurrency, lowerBetter: false },
    { key: 'lcos', label: 'LCOS', format: (v) => fmtNum(v, 4), lowerBetter: true },
    { key: 'payback', label: 'Payback', format: (v) => fmtNum(v, 1) + ' 年', lowerBetter: true },
    { key: 'roi', label: 'ROI', format: (v) => fmtNum(v, 2) + '%', lowerBetter: false },
    { key: 'containerQty', label: '集装箱数量', format: (v) => fmtNum(v, 0) + ' 台', lowerBetter: true },
    { key: 'totalEnergy', label: '总容量', format: (v) => fmtNum(v, 1) + ' MWh', lowerBetter: false },
    { key: 'totalPower', label: '总功率', format: (v) => fmtNum(v, 1) + ' MW', lowerBetter: false },
    { key: 'totalCapex', label: '总 CAPEX', format: fmtCurrency, lowerBetter: true }
  ]

  return rowDefs
    .filter(def => delta.value[def.key])
    .map(def => {
      const d = delta.value[def.key]
      const vals = [d.v1, d.v2]
      const bestIdx = def.lowerBetter
        ? (vals[0] <= vals[1] ? 0 : 1)
        : (vals[0] >= vals[1] ? 0 : 1)
      return {
        ...def,
        values: vals,
        bestIdx,
        diff: d.diff,
        pct: d.pct,
        formatVal: def.format,
        formatDiff: (v) => {
          if (def.key === 'irr' || def.key === 'roi') return fmtNum(v, 2) + '%'
          if (def.key === 'lcos') return fmtNum(v, 4)
          if (def.key === 'containerQty') return fmtNum(v, 0)
          if (def.key === 'totalEnergy' || def.key === 'totalPower' || def.key === 'payback')
            return fmtNum(v, 1)
          return fmtCurrency(v)
        }
      }
    })
})

function renderRadar() {
  if (!radarRef.value || versions.value.length < 2) return
  if (!radarChart) radarChart = echarts.init(radarRef.value, themeObject.value)

  const indicators = [
    { name: 'IRR', max: 20 },
    { name: 'NPV', max: 1 },
    { name: 'LCOS (反)', max: 0.1 },
    { name: 'CAPEX (反)', max: 1 }
  ]

  const v1Config = versions.value[0]?.config || {}
  const v2Config = versions.value[1]?.config || {}

  function getMetric(config, key) {
    const fin = config.financial || {}
    const m = fin.metrics || {}
    const design = config.design || {}
    const vals = {
      irr: m.projectIrr || m.irr || 0,
      npv: m.npv || 0,
      lcos: m.lcos || m.lcoe || 0.1,
      capex: (design.estimatedCapex || {}).totalCapex || 0
    }
    return vals[key] || 0
  }

  const maxNpv = Math.max(getMetric(v1Config, 'npv'), getMetric(v2Config, 'npv'), 1)
  const maxCapex = Math.max(getMetric(v1Config, 'capex'), getMetric(v2Config, 'capex'), 1)
  const maxLcos = Math.max(getMetric(v1Config, 'lcos'), getMetric(v2Config, 'lcos'), 0.01)

  indicators[1].max = maxNpv
  indicators[2].max = maxLcos
  indicators[3].max = maxCapex

  radarChart.setOption({
    tooltip: {},
    legend: {
      data: versions.value.map(v => v.name || ('v' + v.version_num)),
      bottom: 0
    },
    radar: { indicators },
    series: [{
      type: 'radar',
      data: versions.value.map(v => ({
        name: v.name || ('v' + v.version_num),
        value: [
          getMetric(v.config, 'irr'),
          getMetric(v.config, 'npv'),
          maxLcos - getMetric(v.config, 'lcos'),
          maxCapex - getMetric(v.config, 'capex')
        ]
      }))
    }]
  }, true)
}

function handleResize() { radarChart?.resize() }

watch(() => props.compareResult, debounce(() => {
  nextTick(() => renderRadar())
}), { deep: true })

onMounted(() => {
  window.addEventListener('resize', handleResize)
  nextTick(() => renderRadar())
})
onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  radarChart?.dispose()
})
</script>

<style scoped>
.version-compare-panel { display: flex; flex-direction: column; gap: 1.5rem; }

.empty-state {
  text-align: center; padding: 2rem 1rem;
  background: var(--card-bg, #fff); border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.empty-icon { font-size: 2.5rem; display: block; margin-bottom: 0.5rem; }
.empty-state p { color: var(--text-secondary, #888); font-size: 0.9rem; }

.panel-section {
  background: var(--card-bg, #fff); border-radius: 8px; padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.section-title { display: flex; align-items: center; gap: 0.5rem; font-size: 1.1rem; margin: 0 0 1rem 0; }

.version-headers { display: flex; gap: 2rem; margin-bottom: 1rem; }
.version-name { font-weight: 600; font-size: 1rem; }
.version-meta { font-size: 0.8rem; color: var(--text-secondary, #888); margin-left: 0.5rem; }

.table-wrapper { overflow-x: auto; }
.delta-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
.delta-table th, .delta-table td {
  padding: 0.5rem 0.75rem; text-align: center; border-bottom: 1px solid var(--border-light, #f3f4f6);
}
.delta-table th { background: var(--table-header-bg, #f8fafc); font-weight: 600; }
.row-label { text-align: left; font-weight: 500; color: var(--text-secondary, #666); }
.row-value.best { color: #059669; font-weight: 700; }
.row-diff.positive, .row-pct.positive { color: #059669; font-weight: 600; }
.row-diff.negative, .row-pct.negative { color: #dc2626; font-weight: 600; }

.chart-container { width: 100%; height: 350px; }
</style>
