<template>
  <div class="aug-compare-panel">
    <div v-if="!hasData" class="empty-state">
      <span class="empty-icon">🔋</span>
      <p>{{ $t('augCompare.emptyHint') }}</p>
    </div>

    <div v-else>
      <div class="panel-section">
        <h3 class="section-title">
          <span class="icon">📊</span> {{ $t('augCompare.title') }}
        </h3>

        <!-- 策略卡片 -->
        <div class="strategies-grid">
          <div
            v-for="(strat, key) in strategies"
            :key="key"
            :class="['strategy-card', { recommended: recommended === key }]"
          >
            <div class="card-header">
              <span class="strategy-name">{{ getLabel(key) }}</span>
              <span v-if="recommended === key" class="recommend-badge">
                ⭐ {{ $t('augCompare.recommended') }}
              </span>
            </div>

            <div class="card-body">
              <p class="strategy-desc">{{ strat.description }}</p>

              <div class="metrics-section">
                <div class="metric-row">
                  <span class="metric-label">IRR</span>
                  <span class="metric-value" :class="getMetricClass(key, 'irr')">
                    {{ fmtMetric(strat.metrics?.irr, '%') }}
                  </span>
                </div>
                <div class="metric-row">
                  <span class="metric-label">NPV</span>
                  <span class="metric-value" :class="getMetricClass(key, 'npv')">
                    {{ fmtCurrency(strat.metrics?.npv) }}
                  </span>
                </div>
                <div class="metric-row">
                  <span class="metric-label">LCOS</span>
                  <span class="metric-value" :class="getMetricClass(key, 'lcos', true)">
                    {{ fmtMetric(strat.metrics?.lcos, '') }}
                  </span>
                </div>
                <div class="metric-row">
                  <span class="metric-label">{{ $t('augCompare.payback') }}</span>
                  <span class="metric-value">
                    {{ fmtMetric(strat.metrics?.payback, ' ' + $t('augCompare.yearUnit')) }}
                  </span>
                </div>
                <div class="metric-row">
                  <span class="metric-label">{{ $t('augCompare.totalAugCapex') }}</span>
                  <span class="metric-value highlight">
                    {{ fmtCurrency(strat.totalAugCapex) }}
                  </span>
                </div>
              </div>

              <!-- 补容计划 -->
              <div v-if="strat.augSchedule?.length" class="aug-schedule">
                <div class="schedule-title">{{ $t('augCompare.augPlan') }}</div>
                <div
                  v-for="item in strat.augSchedule.slice(0, 5)"
                  :key="item.year"
                  class="schedule-item"
                >
                  <span>{{ $t('augCompare.yearPrefix') }}{{ item.year }}:</span>
                  <span>{{ item.quantity }} {{ $t('augCompare.units') }}</span>
                  <span class="cost">{{ fmtCurrency(item.totalCost) }}</span>
                </div>
                <div v-if="strat.augSchedule.length > 5" class="schedule-more">
                  +{{ strat.augSchedule.length - 5 }} {{ $t('augCompare.moreYears') }}
                </div>
              </div>
              <div v-else class="no-aug">
                {{ $t('augCompare.noAugNeeded') }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 柱状图对比 -->
      <div v-if="Object.keys(strategies).length >= 2" class="panel-section">
        <h3 class="section-title">
          <span class="icon">📈</span> {{ $t('augCompare.chartTitle') }}
        </h3>
        <div ref="chartRef" class="chart-container"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  comparison: { type: Object, default: () => ({}) }
})

const chartRef = ref(null)
let chart = null

const strategies = computed(() => props.comparison?.strategies || {})
const recommended = computed(() => props.comparison?.recommended || '')
const hasData = computed(() => Object.keys(strategies.value).length > 0)

const labels = {
  fixed_periodic: '固定周期补容',
  on_demand: '按需补容',
  overbuild: '初始超配'
}

function getLabel(key) {
  return labels[key] || key
}

function fmtMetric(val, suffix) {
  if (val == null) return '—'
  const num = Number(val)
  if (isNaN(num)) return String(val)
  if (Math.abs(num) < 0.01) return num.toFixed(4) + suffix
  return num.toFixed(2) + suffix
}

function fmtCurrency(val) {
  if (val == null) return '—'
  const num = Number(val)
  if (num >= 1e8) return '$' + (num / 1e8).toFixed(2) + ' 亿'
  if (num >= 1e6) return '$' + (num / 1e6).toFixed(2) + 'M'
  if (num >= 1e3) return '$' + (num / 1e3).toFixed(0) + 'K'
  return '$' + num.toFixed(0)
}

function getMetricClass(stratKey, metricKey, lowerBetter) {
  if (Object.keys(strategies.value).length < 2) return ''
  const vals = Object.entries(strategies.value)
    .map(([k, s]) => ({ key: k, val: s.metrics?.[metricKey] }))
    .filter(v => v.val != null)
  if (vals.length < 2) return ''

  const best = lowerBetter
    ? vals.reduce((a, b) => (a.val < b.val ? a : b))
    : vals.reduce((a, b) => (a.val > b.val ? a : b))

  return best.key === stratKey ? 'best' : ''
}

function renderChart() {
  if (!chartRef.value || !hasData.value) return

  if (!chart) {
    chart = echarts.init(chartRef.value)
  }

  const keys = Object.keys(strategies.value)
  const names = keys.map(k => getLabel(k))
  const npvData = keys.map(k => strategies.value[k]?.metrics?.npv || 0)
  const irrData = keys.map(k => strategies.value[k]?.metrics?.irr || 0)
  const lcosData = keys.map(k => strategies.value[k]?.metrics?.lcos || 0)
  const capexData = keys.map(k => strategies.value[k]?.totalAugCapex || 0)

  chart.setOption({
    tooltip: { trigger: 'axis' },
    legend: {
      data: ['NPV ($)', 'IRR (%)', 'LCOS', '补容 CAPEX ($)'],
      bottom: 0
    },
    xAxis: { type: 'category', data: names },
    yAxis: { type: 'value' },
    series: [
      {
        name: 'NPV ($)', type: 'bar', data: npvData,
        itemStyle: { color: '#3b82f6' }
      },
      {
        name: 'IRR (%)', type: 'bar', data: irrData,
        itemStyle: { color: '#10b981' }
      },
      {
        name: 'LCOS', type: 'bar', data: lcosData,
        itemStyle: { color: '#f59e0b' }
      },
      {
        name: '补容 CAPEX ($)', type: 'bar', data: capexData,
        itemStyle: { color: '#ef4444' }
      }
    ]
  }, true)
}

function handleResize() {
  chart?.resize()
}

watch(hasData, (val) => {
  if (val) nextTick(() => renderChart())
})

watch(() => props.comparison, () => {
  nextTick(() => renderChart())
}, { deep: true })

onMounted(() => {
  window.addEventListener('resize', handleResize)
  nextTick(() => renderChart())
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
})
</script>

<style scoped>
.aug-compare-panel {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.empty-state {
  text-align: center;
  padding: 2rem 1rem;
  background: var(--card-bg, #fff);
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.empty-icon { font-size: 2.5rem; display: block; margin-bottom: 0.5rem; }
.empty-state p { color: var(--text-secondary, #888); font-size: 0.9rem; }

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
}

.strategies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
}

.strategy-card {
  border: 1px solid var(--border-color, #e5e7eb);
  border-radius: 8px;
  overflow: hidden;
  transition: box-shadow 0.2s;
}

.strategy-card.recommended {
  border-color: #f59e0b;
  box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.3);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.6rem 0.75rem;
  background: var(--card-header-bg, #f8fafc);
  border-bottom: 1px solid var(--border-color, #e5e7eb);
}

.strategy-name { font-weight: 600; font-size: 0.95rem; }

.recommend-badge {
  font-size: 0.75rem;
  color: #92400e;
  background: #fef3c7;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  font-weight: 600;
}

.card-body { padding: 0.75rem; }

.strategy-desc {
  font-size: 0.8rem;
  color: var(--text-secondary, #888);
  margin: 0 0 0.75rem 0;
}

.metrics-section { margin-bottom: 0.75rem; }

.metric-row {
  display: flex;
  justify-content: space-between;
  padding: 0.2rem 0;
  font-size: 0.85rem;
  border-bottom: 1px solid var(--border-light, #f3f4f6);
}

.metric-row:last-child { border-bottom: none; }
.metric-label { color: var(--text-secondary, #888); }
.metric-value { font-weight: 500; }
.metric-value.best { color: #059669; font-weight: 700; }
.metric-value.highlight { color: var(--primary, #3b82f6); font-weight: 600; }

.aug-schedule {
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid var(--border-light, #f3f4f6);
}

.schedule-title {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-primary, #333);
  margin-bottom: 0.25rem;
}

.schedule-item {
  display: flex;
  gap: 0.5rem;
  font-size: 0.78rem;
  padding: 0.1rem 0;
}

.schedule-item .cost { margin-left: auto; color: var(--primary, #3b82f6); }

.schedule-more {
  font-size: 0.75rem;
  color: var(--text-secondary, #888);
  margin-top: 0.15rem;
}

.no-aug {
  font-size: 0.8rem;
  color: #059669;
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid var(--border-light, #f3f4f6);
}

.chart-container { width: 100%; height: 350px; }
</style>
