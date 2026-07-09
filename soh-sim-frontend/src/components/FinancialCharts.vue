<template>
  <div>
    <div class="grid grid-cols-2 gap-3">
      <div
        class="rounded-lg p-3"
        style="min-height: 300px; background-color: var(--color-card); border: 1px solid var(--color-border)"
      >
        <h3 class="font-bold text-xs mb-2" style="color: var(--color-text)">{{ $t('financial.chartCashFlow') }}</h3>
        <div ref="cashFlowChartRef" class="w-full" style="height: 280px" />
      </div>
      <div
        class="rounded-lg p-3"
        style="min-height: 300px; background-color: var(--color-card); border: 1px solid var(--color-border)"
      >
        <h3 class="font-bold text-xs mb-2" style="color: var(--color-text)">{{ $t('financial.chartRevenue') }}</h3>
        <div ref="revenueChartRef" class="w-full" style="height: 280px" />
      </div>
      <div
        class="rounded-lg p-3"
        style="min-height: 300px; background-color: var(--color-card); border: 1px solid var(--color-border)"
      >
        <h3 class="font-bold text-xs mb-2" style="color: var(--color-text)">{{ $t('financial.chartDscr') }}</h3>
        <div ref="dscrChartRef" class="w-full" style="height: 280px" />
      </div>
      <div
        class="rounded-lg p-3"
        style="min-height: 300px; background-color: var(--color-card); border: 1px solid var(--color-border)"
      >
        <h3 class="font-bold text-xs mb-2" style="color: var(--color-text)">{{ $t('financial.chartCapex') }}</h3>
        <div ref="capexChartRef" class="w-full" style="height: 280px" />
      </div>
    </div>
    <div class="grid grid-cols-2 gap-3 mt-3">
      <EnergyFlowSankey :params="params" :soh="soh" />
      <CostWaterfallChart :params="params" :cash-flow-table="cashFlowTable" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, PieChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, GridComponent, LegendComponent, GraphicComponent } from 'echarts/components'
import CostWaterfallChart from './CostWaterfallChart.vue'
import EnergyFlowSankey from './EnergyFlowSankey.vue'

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

const { t } = useI18n()

const props = defineProps({
  params: { type: Object, default: () => ({}) },
  soh: { type: Array, default: () => [] },
  cachedRows: { type: Array, default: () => [] },
  cachedCapexData: { type: Object, default: null },
  metrics: { type: Array, required: true }
})

const cashFlowChartRef = ref(null)
const revenueChartRef = ref(null)
const dscrChartRef = ref(null)
const capexChartRef = ref(null)
let cashFlowChart = null,
  revenueChart = null,
  dscrChart = null,
  capexChart = null
let _resizeHandler = null

const chartColors = computed(() => {
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
  return {
    textStyle: { color: 'var(--color-text-secondary)', fontSize: 10 },
    axisLabel: 'var(--color-text-secondary)',
    legendText: 'var(--color-text-secondary)',
    gridLine: isDark ? '#1e293b' : 'var(--color-border-light)',
    success: 'var(--color-success)',
    danger: 'var(--color-danger)',
    warning: 'var(--color-warning)',
    info: isDark ? '#0ea5e9' : '#0ea5e9',
    acLine: isDark ? '#14b8a6' : '#14b8a6',
    purple: 'var(--color-info)',
    orange: 'var(--color-chart-orange)',
    cyan: 'var(--color-chart-cyan)',
    redLight: '#f87171',
    muted: 'var(--color-text-secondary)'
  }
})

function fmtNum(v) {
  if (v == null || isNaN(v)) return '-'
  if (Math.abs(v) >= 100) return v.toFixed(1)
  return v.toFixed(2)
}

function disposeAll() {
  ;[cashFlowChart, revenueChart, dscrChart, capexChart].forEach((c) => c?.dispose())
  cashFlowChart = revenueChart = dscrChart = capexChart = null
}

function renderAll() {
  renderCashFlowChart()
  renderRevenueChart()
  renderDscrChart()
  renderCapexChart()
}

function renderCashFlowChart() {
  if (!cashFlowChartRef.value) return
  if (cashFlowChart) cashFlowChart.dispose()
  const colors = chartColors.value
  cashFlowChart = echarts.init(cashFlowChartRef.value, colors)
  const rows = props.cachedRows
  const years = rows.map((r) => r.year)
  const cumCF = rows.map((r) => r.cumCashFlow)
  const netCF = rows.map((r) => r.cashFlow)
  const paybackYear = parseFloat(props.metrics[5]?.value || 0)

  cashFlowChart.setOption({
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const year = params[0].axisValue
        const row = rows.find((r) => r.year === parseInt(year))
        if (!row) return ''
        let html = `<div style="font-weight:bold;margin-bottom:8px;">${t('financial.tooltipYear')} ${year === 0 ? t('financial.tooltipConstruction') : year + t('financial.tooltipYearLabel')}</div>`
        html += `<div>${t('financial.tooltipNetCashFlow')}: <span style="color:${row.cashFlow >= 0 ? colors.success : colors.danger};font-weight:bold;">${row.cashFlow >= 0 ? '+' : ''}${row.cashFlow.toFixed(0)} ${t('financial.wanUnit')}</span></div>`
        html += `<div>${t('financial.tooltipCumCashFlow')}: <span style="color:${row.cumCashFlow >= 0 ? colors.success : colors.danger};font-weight:bold;">${row.cumCashFlow >= 0 ? '+' : ''}${row.cumCashFlow.toFixed(0)} ${t('financial.wanUnit')}</span></div>`
        if (row.year > 0) {
          html += '<div style="border-top:1px solid #eee;margin-top:6px;padding-top:6px;">'
          html += `<div>${t('financial.tooltipTotalRevenue')}: ${row.revenue.toFixed(0)} ${t('financial.wanUnit')}</div>`
          html += `<div>${t('financial.tooltipOpex')}: ${row.opex.toFixed(0)} ${t('financial.wanUnit')}</div>`
          html += `<div>${t('financial.tooltipEbitda')}: ${row.ebitda.toFixed(0)} ${t('financial.wanUnit')}</div>`
          html += `<div>${t('financial.tooltipDepreciation')}: ${row.depreciation.toFixed(0)} ${t('financial.wanUnit')}</div>`
          html += `<div>${t('financial.tooltipInterest')}: ${row.interest.toFixed(0)} ${t('financial.wanUnit')}</div>`
          html += `<div>${t('financial.tooltipTax')}: ${row.tax.toFixed(0)} ${t('financial.wanUnit')}</div>`
          if (row.debtService > 0) {
            html += `<div>${t('financial.tooltipDebtService')}: ${row.debtService.toFixed(0)} ${t('financial.wanUnit')}</div>`
            html += `<div>${t('financial.tooltipDscr')}: ${row.dscr ? row.dscr.toFixed(2) : '-'}x</div>`
          }
          html += '</div>'
        }
        return html
      }
    },
    legend: {
      top: 0,
      textStyle: { color: colors.legendText, fontSize: 10 },
      data: [t('financial.cumCashFlow'), t('financial.annualNetCashFlow')]
    },
    grid: { top: 30, right: 20, bottom: 25, left: 65 },
    xAxis: {
      type: 'category',
      data: years,
      axisLabel: { color: colors.axisLabel, fontSize: 9 },
      name: t('financial.yearAxis'),
      nameTextStyle: { color: colors.axisLabel, fontSize: 9 }
    },
    yAxis: [
      {
        type: 'value',
        axisLabel: {
          color: colors.axisLabel,
          fontSize: 9,
          formatter: (v) => (v / 10000).toFixed(1) + t('financial.millionUnit')
        },
        splitLine: { lineStyle: { color: colors.gridLine } }
      }
    ],
    series: [
      {
        name: t('financial.cumCashFlow'),
        type: 'line',
        data: cumCF,
        smooth: true,
        symbol: 'circle',
        symbolSize: 4,
        lineStyle: { color: colors.info, width: 2.5 },
        itemStyle: { color: colors.info, borderWidth: 1, borderColor: 'var(--color-text-on-accent)' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color:
                document.documentElement.getAttribute('data-theme') === 'dark'
                  ? 'rgba(14,165,233,0.25)'
                  : 'rgba(59,130,246,0.15)'
            },
            { offset: 1, color: 'transparent' }
          ])
        },
        markLine: {
          silent: true,
          symbol: 'none',
          data: [
            {
              yAxis: 0,
              lineStyle: { color: colors.danger, type: 'dashed', width: 1.5 },
              label: { formatter: t('financial.breakevenLine'), color: colors.danger, fontSize: 9 }
            }
          ]
        },
        markPoint:
          paybackYear > 0 && paybackYear < 26
            ? {
                silent: true,
                symbol: 'pin',
                symbolSize: 24,
                data: [
                  {
                    coord: [paybackYear, 0],
                    value: t('financial.paybackPrefix') + paybackYear + t('financial.paybackSuffix'),
                    itemStyle: { color: colors.warning }
                  }
                ]
              }
            : undefined
      },
      {
        name: t('financial.annualNetCashFlow'),
        type: 'bar',
        data: netCF,
        itemStyle: {
          color: (params) => (params.value >= 0 ? colors.success : colors.danger),
          borderRadius: [2, 2, 0, 0]
        },
        barWidth: 8
      }
    ]
  })
  cashFlowChart.resize()
}

function renderRevenueChart() {
  if (!revenueChartRef.value) return
  if (revenueChart) revenueChart.dispose()
  const colors = chartColors.value
  revenueChart = echarts.init(revenueChartRef.value, colors)
  const rows = props.cachedRows.filter((r) => r.year > 0)
  const years = rows.map((r) => r.year)

  revenueChart.setOption({
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const year = params[0].axisValue
        const row = rows.find((r) => r.year === parseInt(year))
        if (!row) return ''
        let html = `<div style="font-weight:bold;margin-bottom:8px;">${t('financial.tooltipYearFormat', { year })}</div>`
        html += `<div>${t('financial.tooltipArbitrage')}: <span style="color:${colors.acLine};font-weight:bold;">${row.arbitrage.toFixed(0)} ${t('financial.wanUnit')}</span></div>`
        html += `<div>${t('financial.tooltipCapacity')}: <span style="color:${colors.purple};font-weight:bold;">${row.capacity.toFixed(0)} ${t('financial.wanUnit')}</span></div>`
        html += `<div>${t('financial.tooltipAncillary')}: <span style="color:${colors.orange};font-weight:bold;">${row.ancillary.toFixed(0)} ${t('financial.wanUnit')}</span></div>`
        html += '<div style="border-top:1px solid #eee;margin-top:6px;padding-top:6px;">'
        html += `<div>${t('financial.tooltipTotalRevenue')}: <span style="font-weight:bold;">${row.revenue.toFixed(0)} ${t('financial.wanUnit')}</span></div>`
        const aPct = row.revenue > 0 ? ((row.arbitrage / row.revenue) * 100).toFixed(1) : 0
        const cPct = row.revenue > 0 ? ((row.capacity / row.revenue) * 100).toFixed(1) : 0
        const nPct = row.revenue > 0 ? ((row.ancillary / row.revenue) * 100).toFixed(1) : 0
        html += `<div>${t('financial.tooltipRevenueStructure')}: ${t('financial.tooltipArbitrage')}${aPct}% + ${t('financial.tooltipCapacity')}${cPct}% + ${t('financial.tooltipAncillary')}${nPct}%</div>`
        html += `<div>${t('financial.tooltipGeneration')}: ${row.energy.toFixed(0)} MWh</div>`
        html += '</div>'
        return html
      }
    },
    legend: {
      top: 0,
      textStyle: { color: colors.legendText, fontSize: 10 },
      data: [t('financial.arbitrageSeries'), t('financial.capacitySeries'), t('financial.ancillarySeries')]
    },
    grid: { top: 30, right: 20, bottom: 25, left: 55 },
    xAxis: { type: 'category', data: years, axisLabel: { color: colors.axisLabel, fontSize: 9 } },
    yAxis: {
      type: 'value',
      axisLabel: { color: colors.axisLabel, fontSize: 9, formatter: (v) => fmtNum(v) },
      splitLine: { lineStyle: { color: colors.gridLine } }
    },
    series: [
      {
        name: t('financial.arbitrageSeries'),
        type: 'bar',
        stack: 'revenue',
        data: rows.map((r) => r.arbitrage),
        itemStyle: { color: colors.acLine },
        barWidth: 18
      },
      {
        name: t('financial.capacitySeries'),
        type: 'bar',
        stack: 'revenue',
        data: rows.map((r) => r.capacity),
        itemStyle: { color: colors.purple },
        barWidth: 18
      },
      {
        name: t('financial.ancillarySeries'),
        type: 'bar',
        stack: 'revenue',
        data: rows.map((r) => r.ancillary),
        itemStyle: { color: colors.orange },
        barWidth: 18
      }
    ]
  })
  revenueChart.resize()
}

function renderDscrChart() {
  if (!dscrChartRef.value) return
  if (dscrChart) dscrChart.dispose()
  const colors = chartColors.value
  dscrChart = echarts.init(dscrChartRef.value, colors)
  const rows = props.cachedRows.filter((r) => r.year > 0)
  const years = rows.map((r) => r.year)
  const dscrData = rows.map((r) => r.dscr || 0)

  dscrChart.setOption({
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const year = params[0].axisValue
        const row = rows.find((r) => r.year === parseInt(year))
        if (!row) return ''
        let html = `${t('financial.tooltipYearFormat', { year })}`
        html += `<div>${t('financial.tooltipEbitda')}: <span style="color:${colors.cyan};font-weight:bold;">${row.ebitda.toFixed(0)} ${t('financial.wanUnit')}</span></div>`
        html += `<div>${t('financial.tooltipDebtService')}: <span style="color:${colors.redLight};font-weight:bold;">${row.debtService.toFixed(0)} ${t('financial.wanUnit')}</span></div>`
        if (row.debtService > 0) {
          html += '<div style="border-top:1px solid #eee;margin-top:6px;padding-top:6px;">'
          html += `<div>DSCR: <span style="font-weight:bold;font-size:16px;color:${row.dscr >= 1.3 ? colors.success : colors.danger};">${row.dscr.toFixed(2)}x</span></div>`
          html += `<div style="color:${row.dscr >= 1.3 ? colors.success : colors.danger};">${row.dscr >= 1.3 ? t('financial.dscrSatisfied') : t('financial.dscrBelowMin')}</div>`
          html += `<div>${t('financial.tooltipInterest')}: ${row.interest.toFixed(0)} ${t('financial.wanUnit')}</div>`
          html += `<div>${t('financial.tooltipPrincipal')}: ${(row.debtService - row.interest).toFixed(0)} ${t('financial.wanUnit')}</div>`
          html += '</div>'
        } else {
          html += `<div>${t('financial.noDebtService')}</div>`
        }
        return html
      }
    },
    legend: {
      top: 0,
      textStyle: { color: colors.legendText, fontSize: 10 },
      data: [t('financial.ebitdaSeries'), t('financial.debtServiceSeries'), 'DSCR']
    },
    grid: { top: 30, right: 45, bottom: 25, left: 55 },
    xAxis: { type: 'category', data: years, axisLabel: { color: colors.axisLabel, fontSize: 9 } },
    yAxis: [
      {
        type: 'value',
        axisLabel: { color: colors.axisLabel, fontSize: 9, formatter: (v) => fmtNum(v) },
        splitLine: { lineStyle: { color: colors.gridLine } },
        name: t('financial.yAxisUnit')
      },
      {
        type: 'value',
        min: 0,
        max: 4,
        axisLabel: { color: colors.axisLabel, fontSize: 9 },
        splitLine: { show: false },
        name: t('financial.yAxisMultiplier')
      }
    ],
    series: [
      {
        name: t('financial.ebitdaSeries'),
        type: 'bar',
        data: rows.map((r) => r.ebitda),
        itemStyle: { color: colors.cyan, borderRadius: [2, 2, 0, 0] },
        barWidth: 10,
        barGap: '30%'
      },
      {
        name: t('financial.debtServiceSeries'),
        type: 'bar',
        data: rows.map((r) => r.debtService),
        itemStyle: { color: colors.redLight, borderRadius: [2, 2, 0, 0] },
        barWidth: 10
      },
      {
        name: 'DSCR',
        type: 'line',
        yAxisIndex: 1,
        data: dscrData,
        smooth: true,
        symbol: 'circle',
        symbolSize: 6,
        lineStyle: { color: colors.warning, width: 2.5 },
        itemStyle: {
          color: (params) => (params.value >= 1.3 ? colors.success : colors.danger),
          borderWidth: 2,
          borderColor: 'var(--color-text-on-accent)'
        },
        markLine: {
          silent: true,
          symbol: 'none',
          yAxisIndex: 1,
          data: [
            {
              yAxis: 1.3,
              lineStyle: { color: colors.danger, type: 'dashed', width: 1.5 },
              label: { formatter: t('financial.bankMinDscr'), color: colors.danger, fontSize: 9 }
            },
            {
              yAxis: 1.5,
              lineStyle: { color: colors.warning, type: 'dashed', width: 1 },
              label: { formatter: t('financial.idealDscr'), color: colors.warning, fontSize: 8 }
            }
          ]
        }
      }
    ]
  })
  dscrChart.resize()
}

function renderCapexChart() {
  if (!capexChartRef.value) return
  if (capexChart) capexChart.dispose()
  const colors = chartColors.value
  capexChart = echarts.init(capexChartRef.value, colors)
  if (!props.cachedCapexData) return
  const {
    containerCost,
    pcsCost,
    bopCost,
    devCost,
    landCost,
    substationCost,
    transmissionCost,
    totalCapMW,
    totalCapMWh
  } = props.cachedCapexData

  const capexItems = [
    { value: containerCost, name: t('financial.capexContainer'), color: colors.info },
    { value: pcsCost, name: t('financial.capexPcs'), color: colors.purple },
    { value: bopCost, name: t('financial.capexBop'), color: colors.warning },
    { value: substationCost, name: t('financial.capexSubstation'), color: 'var(--color-chart-cyan)' },
    { value: transmissionCost, name: t('financial.capexTransmission'), color: 'var(--color-chart-orange)' },
    { value: landCost, name: t('financial.capexLand'), color: 'var(--color-success)' },
    { value: devCost, name: t('financial.capexDev'), color: colors.muted }
  ].filter((item) => item.value > 0)

  capexChart.setOption({
    tooltip: {
      trigger: 'item',
      formatter: (params) =>
        `${params.name}<br/>${t('financial.tooltipAmount')}: ${params.value.toFixed(0)} ${t('financial.wanUnit')} (${params.percent.toFixed(1)}%)<br/>${t('financial.tooltipUnitPrice')}: ${(params.value / totalCapMWh).toFixed(1)} ${t('financial.wanUnit')}/MWh = ${(params.value / totalCapMW).toFixed(1)} ${t('financial.wanUnit')}/MW`
    },
    legend: {
      bottom: 0,
      textStyle: { color: colors.legendText, fontSize: 9 },
      data: capexItems.map((item) => item.name),
      orient: 'horizontal',
      itemWidth: 10,
      itemHeight: 10
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '65%'],
        center: ['50%', '45%'],
        avoidLabelOverlap: false,
        label: {
          show: true,
          position: 'outside',
          formatter: (params) => `${params.name}\n${params.value.toFixed(0)}${t('financial.wanSuffix')}`,
          fontSize: 8,
          color: colors.legendText,
          lineHeight: 12
        },
        labelLine: { show: true, length: 8, length2: 8 },
        emphasis: {
          label: { show: true, fontSize: 10, fontWeight: 'bold' },
          itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.3)' }
        },
        data: capexItems.map((item) => ({ value: item.value, name: item.name, itemStyle: { color: item.color } }))
      }
    ]
  })
  capexChart.resize()
}

watch(
  () => [props.cachedRows, props.cachedCapexData],
  () => {
    nextTick(() => {
      setTimeout(() => renderAll(), 300)
    })
  },
  { deep: true }
)

onMounted(() => {
  nextTick(() => {
    renderAll()
  })
})
onUnmounted(() => {
  disposeAll()
  if (_resizeHandler) {
    window.removeEventListener('resize', _resizeHandler)
    _resizeHandler = null
  }
})

_resizeHandler = () => {
  cashFlowChart?.resize()
  revenueChart?.resize()
  dscrChart?.resize()
  capexChart?.resize()
}
window.addEventListener('resize', _resizeHandler)
</script>
