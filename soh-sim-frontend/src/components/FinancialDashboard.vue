<template>
  <div class="h-full overflow-y-auto custom-scrollbar flex flex-col">
    <div class="flex-1 overflow-y-auto space-y-3 py-2 px-4">

      <div class="flex items-center justify-between">
        <h3 class="font-bold text-sm" style="color: var(--color-text);">财务指标仪表盘</h3>
        <button @click="recalc" class="text-xs px-3 py-1 rounded" style="background: var(--color-accent); color: #fff;">重新计算</button>
      </div>

      <div class="grid grid-cols-7 gap-2">
        <div v-for="m in metricsCards" :key="m.label" class="border rounded-lg p-2 text-center" style="background-color: var(--color-card); border-color: var(--color-border);">
          <div class="text-[9px] uppercase tracking-wider" style="color: var(--color-text-muted);">{{ m.label }}</div>
          <div class="text-base font-bold font-mono mt-0.5" :style="{ color: m.color }">{{ m.value }}</div>
          <div class="text-[8px] mt-0.5" style="color: var(--color-text-muted);">{{ m.unit }}</div>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div class="rounded-lg p-3" style="min-height:280px; background-color: var(--color-card); border: 1px solid var(--color-border);">
          <h3 class="font-bold text-xs mb-2" style="color: var(--color-text);">现金流曲线与回收期</h3>
          <div ref="cashFlowChartRef" class="w-full" style="height:260px"></div>
        </div>
        <div class="rounded-lg p-3" style="min-height:280px; background-color: var(--color-card); border: 1px solid var(--color-border);">
          <h3 class="font-bold text-xs mb-2" style="color: var(--color-text);">收入结构堆叠</h3>
          <div ref="revenueChartRef" class="w-full" style="height:260px"></div>
        </div>
        <div class="rounded-lg p-3" style="min-height:280px; background-color: var(--color-card); border: 1px solid var(--color-border);">
          <h3 class="font-bold text-xs mb-2" style="color: var(--color-text);">DSCR 趋势</h3>
          <div ref="dscrChartRef" class="w-full" style="height:260px"></div>
        </div>
        <div class="rounded-lg p-3" style="min-height:280px; background-color: var(--color-card); border: 1px solid var(--color-border);">
          <h3 class="font-bold text-xs mb-2" style="color: var(--color-text);">CAPEX 成本结构</h3>
          <div ref="capexChartRef" class="w-full" style="height:260px"></div>
        </div>
      </div>

      <div class="rounded-lg p-3" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
        <h3 class="font-bold text-xs mb-2" style="color: var(--color-text);">收入模型配置</h3>
        <div class="grid grid-cols-5 gap-2 text-[10px]">
          <div v-for="(cfg, key) in revenueConfig" :key="key" class="p-2 rounded" style="border: 1px solid var(--color-border);">
            <label class="flex items-center gap-1 mb-1 cursor-pointer">
              <input type="checkbox" v-model="cfg.enabled" @change="recalc" />
              <span class="font-bold" style="color: var(--color-text);">{{ cfg.label }}</span>
            </label>
            <div v-for="(field, fk) in cfg.fields" :key="fk" class="mt-1">
              <label class="block mb-0.5" style="color: var(--color-text-muted);">{{ field.label }}</label>
              <input v-model.number="field.value" type="number" :step="field.step" class="w-full rounded px-1 py-0.5 text-xs" style="background: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" @change="recalc" />
            </div>
          </div>
        </div>
      </div>

      <div class="rounded-lg p-3" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
        <h3 class="font-bold text-xs mb-2" style="color: var(--color-text);">年度现金流明细表</h3>
        <div class="overflow-x-auto custom-scrollbar" style="max-height:280px;">
          <table class="w-full text-[10px] border-collapse">
            <thead>
              <tr class="sticky top-0 z-10" style="background-color: var(--color-card);">
                <th class="text-left py-1 px-2" style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border);">年份</th>
                <th class="text-right py-1 px-2" style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border);">套利</th>
                <th class="text-right py-1 px-2" style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border);">容量</th>
                <th class="text-right py-1 px-2" style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border);">辅助</th>
                <th class="text-right py-1 px-2" style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border);">PPA</th>
                <th class="text-right py-1 px-2" style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border);">总收入</th>
                <th class="text-right py-1 px-2" style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border);">OPEX</th>
                <th class="text-right py-1 px-2" style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border);">净现金流</th>
                <th class="text-right py-1 px-2" style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border);">累计</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in store.financial.cashflowTable" :key="row.year" style="border-bottom: 1px solid var(--color-border);">
                <td class="py-1 px-2 font-bold" :style="row.year === 0 ? { color: 'var(--color-warning)' } : { color: 'var(--color-text-secondary)' }">{{ row.year === 0 ? '建设期' : row.year }}</td>
                <td class="text-right py-1 px-2 font-mono" style="color: var(--color-text-secondary);">{{ fmtNum(row.revenue?.arbitrage) }}</td>
                <td class="text-right py-1 px-2 font-mono" style="color: var(--color-text-secondary);">{{ fmtNum(row.revenue?.capacity) }}</td>
                <td class="text-right py-1 px-2 font-mono" style="color: var(--color-text-secondary);">{{ fmtNum(row.revenue?.ancillary) }}</td>
                <td class="text-right py-1 px-2 font-mono" style="color: var(--color-text-secondary);">{{ fmtNum(row.revenue?.ppa) }}</td>
                <td class="text-right py-1 px-2 font-mono" style="color: var(--color-text-secondary);">{{ fmtNum(row.totalRevenue) }}</td>
                <td class="text-right py-1 px-2 font-mono" style="color: var(--color-text-secondary);">{{ fmtNum(row.opex) }}</td>
                <td class="text-right py-1 px-2 font-mono font-bold" :style="row.freeCashflow < 0 ? { color: 'var(--color-danger)' } : { color: 'var(--color-success)' }">{{ fmtNum(row.freeCashflow) }}</td>
                <td class="text-right py-1 px-2 font-mono" :style="row.cumulativeCashflow < 0 ? { color: 'var(--color-danger)' } : { color: 'var(--color-text-secondary)' }">{{ fmtNum(row.cumulativeCashflow) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, nextTick, onMounted, onUnmounted, computed } from 'vue'
import * as echarts from 'echarts'
import { useBessStore } from '../stores/bess.js'

const store = useBessStore()

const cashFlowChartRef = ref(null)
const revenueChartRef = ref(null)
const dscrChartRef = ref(null)
const capexChartRef = ref(null)
let cashFlowChart = null, revenueChart = null, dscrChart = null, capexChart = null

const revenueConfig = reactive({
  arbitrage: { label: '峰谷套利', enabled: true, fields: {
    offPeakPrice: { label: '低谷价 $/MWh', value: 30, step: 1 },
    peakPrice: { label: '高峰价 $/MWh', value: 60, step: 1 },
    spreadCapture: { label: '捕获率 %', value: 85, step: 1 },
    operatingDays: { label: '运行天数', value: 330, step: 1 },
  }},
  capacity: { label: '容量市场', enabled: true, fields: {
    capacityPrice: { label: '$/MW-yr', value: 45000, step: 1000 },
  }},
  ancillary: { label: '辅助服务', enabled: true, fields: {
    ancillaryPrice: { label: '$/MW-yr', value: 15000, step: 1000 },
  }},
  ppa: { label: 'PPA 购电', enabled: true, fields: {
    ppaPrice: { label: 'PPA 价 $/MWh', value: 55, step: 1 },
    escalation: { label: '年涨幅 %', value: 2.0, step: 0.1 },
  }},
  capacityAuction: { label: '容量拍卖', enabled: true, fields: {
    auctionPrice: { label: '$/MWh-yr', value: 120000, step: 5000 },
    contractYears: { label: '合同年数', value: 5, step: 1 },
  }},
})

function syncStoreFromConfig() {
  store.financial.revenue.arbitrage.enabled = revenueConfig.arbitrage.enabled
  store.financial.revenue.arbitrage.offPeakPrice = revenueConfig.arbitrage.fields.offPeakPrice.value
  store.financial.revenue.arbitrage.peakPrice = revenueConfig.arbitrage.fields.peakPrice.value
  store.financial.revenue.arbitrage.spreadCapture = revenueConfig.arbitrage.fields.spreadCapture.value
  store.financial.revenue.arbitrage.operatingDays = revenueConfig.arbitrage.fields.operatingDays.value
  store.financial.revenue.capacity.enabled = revenueConfig.capacity.enabled
  store.financial.revenue.capacity.capacityPrice = revenueConfig.capacity.fields.capacityPrice.value
  store.financial.revenue.ancillary.enabled = revenueConfig.ancillary.enabled
  store.financial.revenue.ancillary.ancillaryPrice = revenueConfig.ancillary.fields.ancillaryPrice.value
  store.financial.revenue.ppa.enabled = revenueConfig.ppa.enabled
  store.financial.revenue.ppa.ppaPrice = revenueConfig.ppa.fields.ppaPrice.value
  store.financial.revenue.ppa.escalation = revenueConfig.ppa.fields.escalation.value
  store.financial.revenue.capacityAuction.enabled = revenueConfig.capacityAuction.enabled
  store.financial.revenue.capacityAuction.auctionPrice = revenueConfig.capacityAuction.fields.auctionPrice.value
  store.financial.revenue.capacityAuction.contractYears = revenueConfig.capacityAuction.fields.contractYears.value
}

function irrColor(val) {
  if (val >= 8) return 'var(--color-success)'
  if (val >= 6) return 'var(--color-warning)'
  return 'var(--color-danger)'
}

const metricsCards = computed(() => {
  const m = store.financial.metrics
  return [
    { label: 'Project IRR', value: m.projectIrr ? m.projectIrr.toFixed(1) + '%' : '-', unit: '%', color: irrColor(m.projectIrr) },
    { label: 'Equity IRR', value: m.equityIrr ? m.equityIrr.toFixed(1) + '%' : '-', unit: '%', color: irrColor(m.equityIrr) },
    { label: 'NPV', value: m.npv ? '$' + (m.npv / 1e6).toFixed(1) + 'M' : '-', unit: 'USD', color: m.npv >= 0 ? 'var(--color-success)' : 'var(--color-danger)' },
    { label: 'LCOS', value: m.lcos ? m.lcos.toFixed(3) : '-', unit: '$/MWh', color: 'var(--color-accent-secondary)' },
    { label: 'DSCR (min)', value: m.dscr?.min ? m.dscr.min.toFixed(2) : '-', unit: 'x', color: (m.dscr?.min || 0) >= 1.3 ? 'var(--color-success)' : 'var(--color-danger)' },
    { label: 'Payback', value: m.payback > 0 ? m.payback + '年' : '未回收', unit: '年', color: 'var(--color-warning)' },
    { label: 'ROI', value: m.roi ? m.roi.toFixed(1) + '%' : '-', unit: '%', color: 'var(--color-accent)' },
  ]
})

function fmtNum(v) {
  if (v == null || isNaN(v)) return '-'
  if (Math.abs(v) >= 1e6) return (v / 1e6).toFixed(1) + 'M'
  if (Math.abs(v) >= 1e3) return (v / 1e3).toFixed(1) + 'K'
  if (Math.abs(v) >= 100) return v.toFixed(1)
  return v.toFixed(2)
}

async function recalc() {
  syncStoreFromConfig()
  await store.refreshFinancialResults()
  nextTick(() => setTimeout(() => renderCharts(), 200))
}

function renderCharts() {
  renderCashFlowChart()
  renderRevenueChart()
  renderDscrChart()
  renderCapexChart()
}

function renderCashFlowChart() {
  if (!cashFlowChartRef.value) return
  if (cashFlowChart) cashFlowChart.dispose()
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
  cashFlowChart = echarts.init(cashFlowChartRef.value)
  const table = store.financial.cashflowTable
  if (!table.length) return
  const years = table.map(r => r.year)
  const cumCF = table.map(r => r.cumulativeCashflow)
  const netCF = table.map(r => r.freeCashflow)

  cashFlowChart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { top: 0, textStyle: { color: isDark ? '#94a3b8' : '#64748b', fontSize: 10 }, data: ['累计现金流', '年净现金流'] },
    grid: { top: 30, right: 20, bottom: 25, left: 65 },
    xAxis: { type: 'category', data: years, axisLabel: { color: '#64748b', fontSize: 9 } },
    yAxis: [{ type: 'value', axisLabel: { color: '#64748b', fontSize: 9, formatter: v => (v / 1e6).toFixed(1) + 'M' }, splitLine: { lineStyle: { color: isDark ? '#1e293b' : '#e2e8f0' } } }],
    series: [
      { name: '累计现金流', type: 'line', data: cumCF, smooth: true, symbol: 'none', lineStyle: { color: '#0ea5e9', width: 2.5 }, markLine: { silent: true, symbol: 'none', data: [{ yAxis: 0, lineStyle: { color: '#ef4444', type: 'dashed' } }] } },
      { name: '年净现金流', type: 'bar', data: netCF, itemStyle: { color: p => p.value >= 0 ? '#10b981' : '#ef4444', borderRadius: [2, 2, 0, 0] }, barWidth: 8 },
    ],
  })
  cashFlowChart.resize()
}

function renderRevenueChart() {
  if (!revenueChartRef.value) return
  if (revenueChart) revenueChart.dispose()
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
  revenueChart = echarts.init(revenueChartRef.value)
  const table = store.financial.cashflowTable.filter(r => r.year > 0)
  if (!table.length) return
  const years = table.map(r => r.year)

  revenueChart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { top: 0, textStyle: { color: isDark ? '#94a3b8' : '#64748b', fontSize: 10 }, data: ['套利', '容量', '辅助', 'PPA', '拍卖'] },
    grid: { top: 30, right: 20, bottom: 25, left: 55 },
    xAxis: { type: 'category', data: years, axisLabel: { color: '#64748b', fontSize: 9 } },
    yAxis: { type: 'value', axisLabel: { color: '#64748b', fontSize: 9, formatter: v => fmtNum(v) }, splitLine: { lineStyle: { color: isDark ? '#1e293b' : '#e2e8f0' } } },
    series: [
      { name: '套利', type: 'bar', stack: 'rev', data: table.map(r => r.revenue?.arbitrage || 0), itemStyle: { color: '#14b8a6' }, barWidth: 14 },
      { name: '容量', type: 'bar', stack: 'rev', data: table.map(r => r.revenue?.capacity || 0), itemStyle: { color: '#8b5cf6' } },
      { name: '辅助', type: 'bar', stack: 'rev', data: table.map(r => r.revenue?.ancillary || 0), itemStyle: { color: '#f97316' } },
      { name: 'PPA', type: 'bar', stack: 'rev', data: table.map(r => r.revenue?.ppa || 0), itemStyle: { color: '#0ea5e9' } },
      { name: '拍卖', type: 'bar', stack: 'rev', data: table.map(r => r.revenue?.capacityAuction || 0), itemStyle: { color: '#f59e0b' } },
    ],
  })
  revenueChart.resize()
}

function renderDscrChart() {
  if (!dscrChartRef.value) return
  if (dscrChart) dscrChart.dispose()
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
  dscrChart = echarts.init(dscrChartRef.value)
  const table = store.financial.cashflowTable.filter(r => r.year > 0)
  if (!table.length) return
  const years = table.map(r => r.year)
  const ebitdaData = table.map(r => r.ebitda || 0)
  const debtData = table.map(r => r.debtService || 0)

  dscrChart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { top: 0, textStyle: { color: isDark ? '#94a3b8' : '#64748b', fontSize: 10 }, data: ['EBITDA', '还本付息'] },
    grid: { top: 30, right: 20, bottom: 25, left: 55 },
    xAxis: { type: 'category', data: years, axisLabel: { color: '#64748b', fontSize: 9 } },
    yAxis: { type: 'value', axisLabel: { color: '#64748b', fontSize: 9, formatter: v => fmtNum(v) }, splitLine: { lineStyle: { color: isDark ? '#1e293b' : '#e2e8f0' } } },
    series: [
      { name: 'EBITDA', type: 'bar', data: ebitdaData, itemStyle: { color: '#22d3ee', borderRadius: [2, 2, 0, 0] }, barWidth: 10 },
      { name: '还本付息', type: 'bar', data: debtData, itemStyle: { color: '#f87171', borderRadius: [2, 2, 0, 0] }, barWidth: 10 },
    ],
  })
  dscrChart.resize()
}

function renderCapexChart() {
  if (!capexChartRef.value) return
  if (capexChart) capexChart.dispose()
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
  capexChart = echarts.init(capexChartRef.value)
  const bd = store.financial.capexBreakdown
  if (!bd) return

  capexChart.setOption({
    tooltip: { trigger: 'item', formatter: '{b}: ${c} ({d}%)' },
    legend: { bottom: 0, textStyle: { color: isDark ? '#94a3b8' : '#64748b', fontSize: 9 }, data: ['Equipment', 'EPC', 'Development'] },
    series: [{
      type: 'pie', radius: ['45%', '65%'], center: ['50%', '48%'],
      label: { show: true, position: 'outside', formatter: '{b}\n{d}%', fontSize: 9, color: isDark ? '#94a3b8' : '#64748b' },
      data: [
        { value: bd.equipment || 0, name: 'Equipment', itemStyle: { color: '#0ea5e9' } },
        { value: bd.epc || 0, name: 'EPC', itemStyle: { color: '#f59e0b' } },
        { value: bd.development || 0, name: 'Development', itemStyle: { color: '#94a3b8' } },
      ],
    }],
  })
  capexChart.resize()
}

function disposeAll() {
  [cashFlowChart, revenueChart, dscrChart, capexChart].forEach(c => c?.dispose())
  cashFlowChart = revenueChart = dscrChart = capexChart = null
}

onMounted(async () => {
  await recalc()
})
onUnmounted(() => { disposeAll() })
window.addEventListener('resize', () => { cashFlowChart?.resize(); revenueChart?.resize(); dscrChart?.resize(); capexChart?.resize() })
</script>
