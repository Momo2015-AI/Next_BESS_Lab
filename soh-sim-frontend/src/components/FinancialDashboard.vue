<template>
  <div class="h-full overflow-y-auto custom-scrollbar flex flex-col">
    <div class="flex-1 overflow-y-auto space-y-3 py-2 px-4">
      <div class="grid grid-cols-4 md:grid-cols-8 gap-2 mb-3">
        <div
          v-for="(m, idx) in metrics"
          :key="m.label"
          class="rounded-lg p-3 text-center transition-all hover:shadow-md"
          :style="{
            backgroundColor: 'var(--color-card)',
            border: '1px solid var(--color-border)',
            borderTop: '3px solid ' + (metrics[idx]?.borderColor || 'var(--color-accent)')
          }"
        >
          <div class="text-[9px] uppercase tracking-wider truncate text-muted">
            {{ m.label }}
          </div>
          <div class="text-base md:text-lg font-bold font-mono mt-1" :style="{ color: m.textColor }">
            {{ m.value }}
          </div>
          <div class="text-[8px] mt-0.5 text-muted">
            {{ m.unit }}
          </div>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div
          class="rounded-lg p-3 min-h-300 card-bordered"
        >
          <h3 class="font-bold text-xs mb-2 text-default">
            现金流曲线与回收期 Cash Flow & Payback
          </h3>
          <div ref="cashFlowChartRef" class="w-full h-280" />
        </div>
        <div
          class="rounded-lg p-3 min-h-300 card-bordered"
        >
          <h3 class="font-bold text-xs mb-2 text-default">收入结构堆叠 Revenue Breakdown</h3>
          <div ref="revenueChartRef" class="w-full h-280" />
        </div>
        <div
          class="rounded-lg p-3 min-h-300 card-bordered"
        >
          <h3 class="font-bold text-xs mb-2 text-default">EBITDA vs 还本付息 & DSCR DSCR Trend</h3>
          <div ref="dscrChartRef" class="w-full h-280" />
        </div>
        <div
          class="rounded-lg p-3 min-h-300 card-bordered"
        >
          <h3 class="font-bold text-xs mb-2 text-default">CAPEX 成本结构与敏感性 Tornado</h3>
          <div ref="capexChartRef" class="w-full h-280" />
        </div>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div class="rounded-lg p-3 card-bordered">
          <h3 class="font-bold text-xs mb-2 flex items-center gap-2 text-default">
            <span
              class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold u-background-color-var-color-accent-glow-color-var-color-accent"
            >
              I
            </span>
            收入模型 Revenue Stack
          </h3>
          <div class="grid grid-cols-2 gap-2 text-[10px] text-secondary">
            <ParamInput v-model="f.offPeakPrice" :label="'低谷购电价 $/MWh'" :step="0.1" />
            <ParamInput v-model="f.peakPrice" :label="'高峰售电价 $/MWh'" :step="0.1" />
            <ParamInput v-model="f.spreadCapture" :label="'价差捕获率 %'" :step="0.1" />
            <ParamInput v-model="f.operatingDays" :label="'日历日可用天数'" :step="1" />
            <ParamInput v-model="f.capacityPrice" :label="'容量市场单价 $/MW-yr'" :step="100" />
            <ParamInput v-model="f.ancillaryPrice" :label="'辅助服务单价 $/MW-yr'" :step="100" />
            <ParamInput v-model="f.priceEscalation" :label="'电价年涨幅 %'" :step="0.1" />
            <ParamInput v-model="f.efficiencyLossPct" :label="'充放电效率扣减 %'" :step="0.01" />
          </div>
        </div>
        <div class="rounded-lg p-3 card-bordered">
          <h3 class="font-bold text-xs mb-2 flex items-center gap-2 text-default">
            <span
              class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold u-background-color-rgba-245-158-11-0-2-color-var-color-warning"
            >
              II
            </span>
            CAPEX & OPEX 成本结构
          </h3>
          <div class="grid grid-cols-2 gap-2 text-[10px] text-secondary">
            <ParamInput v-model="f.containerCostPerMWh" :label="'集装箱单价 万元/MWh'" :step="1" />
            <ParamInput v-model="f.pcsCostPerMW" :label="'PCS 单价 万元/MW'" :step="1" />
            <ParamInput v-model="f.bopCostPerMWh" :label="'BOP 配套 万元/MWh'" :step="1" />
            <ParamInput v-model="f.substationCostPerMW" :label="'变电站 万元/MW'" :step="1" />
            <ParamInput v-model="f.transmissionCostPerMW" :label="'输电线路 万元/MW'" :step="1" />
            <ParamInput v-model="f.landCostPerMW" :label="'土地成本 万元/MW'" :step="1" />
            <ParamInput v-model="f.developmentCostPerMW" :label="'开发费 万元/MW'" :step="1" />
            <ParamInput v-model="f.fixedOpexPerKW" :label="'固定 O&M 元/kW-年'" :step="0.5" />
            <ParamInput v-model="f.varOpexPerMWh" :label="'可变 O&M 元/MWh'" :step="0.1" />
            <ParamInput v-model="f.insuranceRate" :label="'保险费率 % of CAPEX'" :step="0.01" />
            <ParamInput v-model="f.opexEscalation" :label="'O&M 年涨幅 %'" :step="0.1" />
            <ParamInput v-model="f.vatRate" :label="'VAT 税率 %'" :step="0.5" />
          </div>
        </div>
      </div>

      <div class="grid grid-cols-3 gap-3">
        <div class="rounded-lg p-3 card-bordered">
          <h3 class="font-bold text-xs mb-2 flex items-center gap-2 text-default">
            <span
              class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold u-background-color-rgba-59-130-246-0-2-color-var-color-accent-secondary"
            >
              III
            </span>
            融资与税务 Financing & Tax
          </h3>
          <div class="grid grid-cols-1 gap-2 text-[10px] text-secondary">
            <ParamInput v-model="f.discountRate" :label="'折现率 %'" :step="0.1" />
            <ParamInput v-model="f.debtRatio" :label="'债务融资比例 %'" :step="1" />
            <ParamInput v-model="f.equityRatio" :label="'权益融资比例 %'" :step="1" />
            <ParamInput v-model="f.interestRate" :label="'贷款利率 %'" :step="0.1" />
            <ParamInput v-model="f.costOfEquity" :label="'权益成本 %'" :step="0.5" />
            <ParamInput v-model="f.loanTenure" :label="'贷款年限'" :step="1" />
            <ParamInput v-model="f.taxRate" :label="'所得税率 %'" :step="0.5" />
            <ParamInput v-model="f.depreciationYears" :label="'折旧年限'" :step="1" />
            <ParamInput v-model="f.residualRate" :label="'残值率 %'" :step="0.5" />
            <ParamInput
              v-model="f.depreciationMethod"
              :label="'折旧方法'"
              type="select"
              :options="[{ value: 'straight-line', label: '直线折旧' }, { value: 'double-declining', label: '双倍余额递减' }]"
            />
          </div>
        </div>
        <div class="rounded-lg p-3 card-bordered">
          <h3 class="font-bold text-xs mb-2 flex items-center gap-2 text-default">
            <span
              class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold u-background-color-rgba-168-85-247-0-2-color-var-color-info"
            >
              IV
            </span>
            增容与设备成本递减
          </h3>
          <div class="grid grid-cols-1 gap-2 text-[10px] text-secondary">
            <ParamInput v-model="f.augContainerCostPerMWh" :label="'增容集装箱单价 万元/MWh'" :step="1" />
            <ParamInput v-model="f.costDeclineRate" :label="'设备成本年降幅 (学习率) %'" :step="0.1" />
            <ParamInput v-model="f.augInstallCost" :label="'增容安装费 万元/台'" :step="0.5" />
            <ParamInput v-model="f.decommissioningCost" :label="'退役成本 万元/MWh'" :step="1" />
          </div>
        </div>
        <div class="rounded-lg p-3 card-bordered">
          <h3 class="font-bold text-xs mb-2 flex items-center gap-2 text-default">
            <span
              class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold u-background-color-rgba-16-185-129-0-2-color-var-color-success"
            >
              V
            </span>
            敏感性分析范围
          </h3>
          <div class="text-[10px] space-y-1.5 text-muted">
            <div class="flex justify-between">
              <span>售电价波动范围</span>
              <span>+/-{{ f.sensPct }}%</span>class="text-secondary"
            </div>
            <div class="flex justify-between">
              <span>衰减率波动范围</span>
              <span>+/-{{ f.sensPct }}%</span>class="text-secondary"
            </div>
            <div class="flex justify-between">
              <span>融资利率波动</span>
              <span>+/-{{ f.sensPct }}%</span>class="text-secondary"
            </div>
            <div class="flex justify-between">
              <span>CAPEX 波动</span>
              <span>+/-{{ f.sensPct }}%</span>class="text-secondary"
            </div>
            <ParamInput v-model="f.sensPct" :label="'波动幅度 %'" :step="5" />
          </div>
        </div>
      </div>

      <!-- 货币转换器 -->
      <CurrencyConverter />

      <!-- 产品库→CAPEX 自动联动 -->
      <ProductCAPEXLink @apply-config="handleProductConfig" />

      <div class="grid grid-cols-2 gap-3">
        <EnergyFlowSankey :params="params" :soh="soh" />
        <CostWaterfallChart :params="params" :cash-flow-table="cashFlowTable" />
      </div>

      <div class="rounded-lg p-3 card-bordered">
        <div class="flex justify-between items-center mb-2">
          <h3 class="font-bold text-xs text-default">年度现金流明细表 Annual Cash Flow</h3>
          <button
            class="text-[10px] px-3 py-1 rounded transition-colors bg-accent text-white"
            @click="recalc"
          >
            重新计算 Recalculate
          </button>
        </div>
        <div class="overflow-x-auto custom-scrollbar max-h-[300px]">
          <table class="w-full text-[10px] border-collapse">
            <thead>
              <tr class="sticky top-0 z-10 u-background-color-var-color-card">
                <th
                  class="text-left py-1 px-2 sticky left-0 z-20 text-muted border-b"
                >
                  年份
                </th>
                <th
                  class="text-right py-1 px-2 text-muted border-b"
                >
                  发电量 MWh
                </th>
                <th
                  class="text-right py-1 px-2 text-muted border-b"
                >
                  套利收入
                </th>
                <th
                  class="text-right py-1 px-2 text-muted border-b"
                >
                  容量收入
                </th>
                <th
                  class="text-right py-1 px-2 text-muted border-b"
                >
                  辅助服务
                </th>
                <th
                  class="text-right py-1 px-2 text-muted border-b"
                >
                  总收入
                </th>
                <th
                  class="text-right py-1 px-2 text-muted border-b"
                >
                  OPEX
                </th>
                <th
                  class="text-right py-1 px-2 text-muted border-b"
                >
                  EBITDA
                </th>
                <th
                  class="text-right py-1 px-2 text-muted border-b"
                >
                  净现金流
                </th>
                <th
                  class="text-right py-1 px-2 text-muted border-b"
                >
                  累计现金流
                </th>
                <th
                  v-if="f.debtRatio > 0"
                  class="text-right py-1 px-2 text-muted border-b"
                >
                  DSCR
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="row in cashFlowTable"
                :key="'yr' + row.year"
 class="border-b"
              >
                <td
                  class="py-1 px-2 sticky left-0 font-bold"
                  :class="row.year === 0 ? 'text-warning' : 'text-secondary'"
                >
                  {{ row.year === 0 ? '建设期' : row.year }}
                </td>
                <td class="text-right py-1 px-2 font-mono text-secondary">
                  {{ fmtNum(row.energy) }}
                </td>
                <td class="text-right py-1 px-2 font-mono text-secondary">
                  {{ fmtNum(row.arbitrage) }}
                </td>
                <td class="text-right py-1 px-2 font-mono text-secondary">
                  {{ fmtNum(row.capacity) }}
                </td>
                <td class="text-right py-1 px-2 font-mono text-secondary">
                  {{ fmtNum(row.ancillary) }}
                </td>
                <td class="text-right py-1 px-2 font-mono text-secondary">
                  {{ fmtNum(row.revenue) }}
                </td>
                <td class="text-right py-1 px-2 font-mono text-secondary">
                  {{ fmtNum(row.opex) }}
                </td>
                <td
                  class="text-right py-1 px-2 font-mono"
                  :class="row.ebitda < 0 ? 'text-danger' : 'text-secondary'"
                >
                  {{ fmtNum(row.ebitda) }}
                </td>
                <td
                  class="text-right py-1 px-2 font-mono font-bold"
                  :class="row.cashFlow < 0 ? 'text-danger' : 'text-success'"
                >
                  {{ fmtNum(row.cashFlow) }}
                </td>
                <td
                  class="text-right py-1 px-2 font-mono"
                  :class="row.cumCashFlow < 0 ? 'text-danger' : 'text-secondary'"
                >
                  {{ fmtNum(row.cumCashFlow) }}
                </td>
                <td
                  v-if="f.debtRatio > 0"
                  class="text-right py-1 px-2 font-mono text-secondary"
                >
                  {{ row.dscr ? row.dscr.toFixed(2) : '-' }}
                </td>
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
import { debounce } from 'lodash-es'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, PieChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, GridComponent, LegendComponent, GraphicComponent } from 'echarts/components'
import CurrencyConverter from './CurrencyConverter.vue'
import ParamInput from './ParamInput.vue'
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
import CostWaterfallChart from './CostWaterfallChart.vue'
import EnergyFlowSankey from './EnergyFlowSankey.vue'
import ProductCAPEXLink from './ProductCAPEXLink.vue'
import { useExchangeRate } from '../composables/useExchangeRate.js'
import { useFinancialModel } from '../composables/useFinancialModel.js'

const props = defineProps({ params: Object, results: Object, soh: Array, rte: Array, augQty: Array })

const { displayCurrency } = useExchangeRate()
const model = useFinancialModel(props)
const { f, metrics, cashFlowTable, chartColors, fmtNum, computeAll, calculateSensitivityData, recalc } = model

const cashFlowChartRef = ref(null)
const revenueChartRef = ref(null)
const dscrChartRef = ref(null)
const capexChartRef = ref(null)

let cashFlowChart = null,
  revenueChart = null,
  dscrChart = null,
  capexChart = null
let _resizeHandler = null

function disposeAll() {
  ;[cashFlowChart, revenueChart, dscrChart, capexChart].forEach((c) => {
    c?.dispose()
  })
  cashFlowChart = revenueChart = dscrChart = capexChart = null
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
  const colors = chartColors.value
  cashFlowChart = echarts.init(cashFlowChartRef.value, colors)

  const rows = model.cachedRows()
  const years = rows.map((r) => r.year)
  const cumCF = rows.map((r) => r.cumCashFlow)
  const netCF = rows.map((r) => r.cashFlow)
  const paybackYear = parseFloat(metrics.value[4].value)

  cashFlowChart.setOption({
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const year = params[0].axisValue
        const row = rows.find((r) => r.year === parseInt(year))
        if (!row) return ''
        let html = `<div>年份 ${year === 0 ? '建设期' : year + '年'}</div>` class="font-bold mb-8"
        html += `<div>年净现金流: <span>${row.cashFlow >= 0 ? '+' : ''}${row.cashFlow.toFixed(0)} 万元</span></div>` class="u-color-row-cashFlow--0--colors-success--colors-danger-font-weight-bold"
        html += `<div>累计现金流: <span>${row.cumCashFlow >= 0 ? '+' : ''}${row.cumCashFlow.toFixed(0)} 万元</span></div>` class="u-color-row-cumCashFlow--0--colors-success--colors-danger-font-weight-bold"
        if (row.year > 0) {
          html += '<div>' class="border-t-eee mt-6 pt-6"
          html += `<div>总收入: ${row.revenue.toFixed(0)} 万元</div>`
          html += `<div>OPEX: ${row.opex.toFixed(0)} 万元</div>`
          html += `<div>EBITDA: ${row.ebitda.toFixed(0)} 万元</div>`
          html += `<div>折旧: ${row.depreciation.toFixed(0)} 万元</div>`
          html += `<div>利息: ${row.interest.toFixed(0)} 万元</div>`
          html += `<div>所得税: ${row.tax.toFixed(0)} 万元</div>`
          if (row.debtService > 0) {
            html += `<div>还本付息: ${row.debtService.toFixed(0)} 万元</div>`
            html += `<div>DSCR: ${row.dscr ? row.dscr.toFixed(2) : '-'}x</div>`
          }
          html += '</div>'
        }
        return html
      }
    },
    legend: { top: 0, textStyle: { color: colors.legendText, fontSize: 10 }, data: ['累计现金流', '年净现金流'] },
    grid: { top: 30, right: 20, bottom: 25, left: 65 },
    xAxis: {
      type: 'category',
      data: years,
      axisLabel: { color: colors.axisLabel, fontSize: 9 },
      name: '年份',
      nameTextStyle: { color: colors.axisLabel, fontSize: 9 }
    },
    yAxis: [
      {
        type: 'value',
        axisLabel: { color: colors.axisLabel, fontSize: 9, formatter: (v) => (v / 10000).toFixed(1) + '亿' },
        splitLine: { lineStyle: { color: colors.gridLine } }
      }
    ],
    series: [
      {
        name: '累计现金流',
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
              label: { formatter: '盈亏平衡线', color: colors.danger, fontSize: 9 }
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
                  { coord: [paybackYear, 0], value: '回收 ' + paybackYear + '年', itemStyle: { color: colors.warning } }
                ]
              }
            : undefined
      },
      {
        name: '年净现金流',
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

  const rows = model.cachedRows().filter((r) => r.year > 0)
  const years = rows.map((r) => r.year)

  revenueChart.setOption({
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const year = params[0].axisValue
        const row = rows.find((r) => r.year === parseInt(year))
        if (!row) return ''
        let html = `<div>第 ${year} 年</div>` class="font-bold mb-8"
        html += `<div>套利收入: <span>${row.arbitrage.toFixed(0)} 万元</span></div>` class="u-color-colors-acLine-font-weight-bold"
        html += `<div>容量收入: <span>${row.capacity.toFixed(0)} 万元</span></div>` class="u-color-colors-purple-font-weight-bold"
        html += `<div>辅助服务: <span>${row.ancillary.toFixed(0)} 万元</span></div>` class="u-color-colors-orange-font-weight-bold"
        html += '<div>' class="border-t-eee mt-6 pt-6"
        html += `<div>总收入: <span>${row.revenue.toFixed(0)} 万元</span></div>` class="u-font-weight-bold"
        const arbitragePct = row.revenue > 0 ? ((row.arbitrage / row.revenue) * 100).toFixed(1) : 0
        const capacityPct = row.revenue > 0 ? ((row.capacity / row.revenue) * 100).toFixed(1) : 0
        const ancillaryPct = row.revenue > 0 ? ((row.ancillary / row.revenue) * 100).toFixed(1) : 0
        html += `<div>收入结构: 套利${arbitragePct}% + 容量${capacityPct}% + 辅助${ancillaryPct}%</div>`
        html += `<div>发电量: ${row.energy.toFixed(0)} MWh</div>`
        html += '</div>'
        return html
      }
    },
    legend: {
      top: 0,
      textStyle: { color: colors.legendText, fontSize: 10 },
      data: ['套利收入', '容量收入', '辅助服务']
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
        name: '套利收入',
        type: 'bar',
        stack: 'revenue',
        data: rows.map((r) => r.arbitrage),
        itemStyle: { color: colors.acLine },
        barWidth: 18
      },
      {
        name: '容量收入',
        type: 'bar',
        stack: 'revenue',
        data: rows.map((r) => r.capacity),
        itemStyle: { color: colors.purple },
        barWidth: 18
      },
      {
        name: '辅助服务',
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

  const rows = model.cachedRows().filter((r) => r.year > 0)
  const years = rows.map((r) => r.year)
  const dscrData = rows.map((r) => r.dscr || 0)

  dscrChart.setOption({
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const year = params[0].axisValue
        const row = rows.find((r) => r.year === parseInt(year))
        if (!row) return ''
        let html = `<div>第 ${year} 年</div>` class="font-bold mb-8"
        html += `<div>EBITDA: <span>${row.ebitda.toFixed(0)} 万元</span></div>` class="u-color-colors-cyan-font-weight-bold"
        html += `<div>还本付息: <span>${row.debtService.toFixed(0)} 万元</span></div>` class="u-color-colors-redLight-font-weight-bold"
        if (row.debtService > 0) {
          html += '<div>' class="border-t-eee mt-6 pt-6"
          html += `<div>DSCR: <span>${row.dscr.toFixed(2)}x</span></div>` class="u-font-weight-bold-font-size-16px-color-row-dscr--1-3--colors-success--colors-danger"
          html += `<div>${row.dscr >= 1.3 ? '✓ 满足银行要求' : '✗ 低于银行底线 1.3x'}</div>` class="u-color-row-dscr--1-3--colors-success--colors-danger"
          html += `<div>利息支出: ${row.interest.toFixed(0)} 万元</div>`
          html += `<div>本金偿还: ${(row.debtService - row.interest).toFixed(0)} 万元</div>`
          html += '</div>'
        } else {
          html += '<div>DSCR: 无债务偿还</div>'
        }
        return html
      }
    },
    legend: { top: 0, textStyle: { color: colors.legendText, fontSize: 10 }, data: ['EBITDA', '还本付息', 'DSCR'] },
    grid: { top: 30, right: 45, bottom: 25, left: 55 },
    xAxis: { type: 'category', data: years, axisLabel: { color: colors.axisLabel, fontSize: 9 } },
    yAxis: [
      {
        type: 'value',
        axisLabel: { color: colors.axisLabel, fontSize: 9, formatter: (v) => fmtNum(v) },
        splitLine: { lineStyle: { color: colors.gridLine } },
        name: '万元'
      },
      {
        type: 'value',
        min: 0,
        max: 4,
        axisLabel: { color: colors.axisLabel, fontSize: 9 },
        splitLine: { show: false },
        name: '倍率'
      }
    ],
    series: [
      {
        name: 'EBITDA',
        type: 'bar',
        data: rows.map((r) => r.ebitda),
        itemStyle: { color: colors.cyan, borderRadius: [2, 2, 0, 0] },
        barWidth: 10,
        barGap: '30%'
      },
      {
        name: '还本付息',
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
              label: { formatter: '银行底线 1.3x', color: colors.danger, fontSize: 9 }
            },
            {
              yAxis: 1.5,
              lineStyle: { color: colors.warning, type: 'dashed', width: 1 },
              label: { formatter: '理想值 1.5x', color: colors.warning, fontSize: 8 }
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

  if (!model.cachedCapexData()) return
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
  } = model.cachedCapexData()

  const capexItems = [
    { value: containerCost, name: '集装箱', color: colors.info },
    { value: pcsCost, name: 'PCS', color: colors.purple },
    { value: bopCost, name: 'BOP配套', color: colors.warning },
    { value: substationCost, name: '变电站', color: 'var(--color-chart-cyan)' },
    { value: transmissionCost, name: '输电线路', color: 'var(--color-chart-orange)' },
    { value: landCost, name: '土地', color: 'var(--color-success)' },
    { value: devCost, name: '开发费', color: colors.muted }
  ].filter((item) => item.value > 0)

  const total = capexItems.reduce((sum, item) => sum + item.value, 0)

  // 计算敏感性分析数据
  const sensitivityData = calculateSensitivityData()

  capexChart.setOption({
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        const perMWh = params.value / totalCapMWh
        const perMW = params.value / totalCapMW
        return `${params.name}<br/>金额: ${params.value.toFixed(0)} 万元 (${params.percent.toFixed(1)}%)<br/>单价: ${perMWh.toFixed(1)} 万元/MWh = ${perMW.toFixed(1)} 万元/MW`
      }
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
          formatter: (params) => `${params.name}
${params.value.toFixed(0)}万`,
          fontSize: 8,
          color: colors.legendText,
          lineHeight: 12
        },
        labelLine: { show: true, length: 8, length2: 8 },
        emphasis: {
          label: { show: true, fontSize: 10, fontWeight: 'bold' },
          itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.3)' }
        },
        data: capexItems.map((item) => ({
          value: item.value,
          name: item.name,
          itemStyle: { color: item.color }
        }))
      }
    ]
  })
  capexChart.resize()
}

// 处理产品配置
function handleProductConfig(config) {
  if (config.autoCalculatedCAPEX) {
    // 使用自动计算的CAPEX
    f.containerCostPerMWh = config.autoCalculatedCapexPerMWh * 0.6 // 60% for container
    f.pcsCostPerMW = config.autoCalculatedCapexPerMWh * config.ratedEnergy * 0.2 // 20% for PCS
    f.bopCostPerMWh = config.autoCalculatedCapexPerMWh * 0.2 // 20% for BOP
  }

  if (config.ratedEnergy) {
    // 更新能量参数
    if (props.params) {
      // eslint-disable-next-line vue/no-mutating-props
      props.params.ratedEnergy = config.ratedEnergy
    }
  }

  if (config.acEfficiency) {
    // 更新PCS效率
    if (props.params) {
      // eslint-disable-next-line vue/no-mutating-props
      props.params.acEfficiency = config.acEfficiency
    }
  }

  // 重新计算
  computeAll(renderCharts)
}

function recalc() {
  computeAll(renderCharts)
}
const debouncedRecalc = debounce(recalc, 300)

watch([() => props.params, () => props.soh, () => props.augQty], debouncedRecalc, { deep: true, immediate: true })
watch(f, debouncedRecalc, { deep: true })
watch(displayCurrency, () => {
  // 更新货币单位显示
  metrics.value[3].unit = `万元 (${displayCurrency.value})`
  metrics.value[4].unit = `元/kWh (${displayCurrency.value})`
  metrics.value[6].unit = `万元 (${displayCurrency.value})`
  // 重新计算以应用新的货币转换
  computeAll(renderCharts)
})

onMounted(() => {
  nextTick(() => computeAll(renderCharts))
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

<style scoped>
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
