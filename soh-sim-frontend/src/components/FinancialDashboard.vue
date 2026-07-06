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
        <div class="rounded-lg p-3 card-panel-chart">
          <h3 class="font-bold text-xs mb-2 text-primary">现金流曲线与回收期 Cash Flow & Payback</h3>
          <div ref="cashFlowChartRef" class="chart-container" />
        </div>
        <div class="rounded-lg p-3 card-panel-chart">
          <h3 class="font-bold text-xs mb-2 text-primary">收入结构堆叠 Revenue Breakdown</h3>
          <div ref="revenueChartRef" class="chart-container" />
        </div>
        <div class="rounded-lg p-3 card-panel-chart">
          <h3 class="font-bold text-xs mb-2 text-primary">EBITDA vs 还本付息 & DSCR DSCR Trend</h3>
          <div ref="dscrChartRef" class="chart-container" />
        </div>
        <div class="rounded-lg p-3 card-panel-chart">
          <h3 class="font-bold text-xs mb-2 text-primary">CAPEX 成本结构与敏感性 Tornado</h3>
          <div ref="capexChartRef" class="chart-container" />
        </div>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div class="rounded-lg p-3 card-panel">
          <h3 class="font-bold text-xs mb-2 flex items-center gap-2 text-primary">
            <span class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold tag-glow text-accent">
              I
            </span>
            收入模型 Revenue Stack
          </h3>
          <div class="grid grid-cols-2 gap-2 text-[10px] text-secondary">
            <div>
              <label class="block mb-0.5 text-muted">低谷购电价 $/MWh</label>
              <input
                v-model.number="f.offPeakPrice"
                type="number"
                step="0.1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">高峰售电价 $/MWh</label>
              <input
                v-model.number="f.peakPrice"
                type="number"
                step="0.1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">价差捕获率 %</label>
              <input
                v-model.number="f.spreadCapture"
                type="number"
                step="0.1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">日历日可用天数</label>
              <input
                v-model.number="f.operatingDays"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">容量市场单价 $/MW-yr</label>
              <input
                v-model.number="f.capacityPrice"
                type="number"
                step="100"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">辅助服务单价 $/MW-yr</label>
              <input
                v-model.number="f.ancillaryPrice"
                type="number"
                step="100"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">电价年涨幅 %</label>
              <input
                v-model.number="f.priceEscalation"
                type="number"
                step="0.1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">充放电效率扣减 %</label>
              <input
                v-model.number="f.efficiencyLossPct"
                type="number"
                step="0.01"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
          </div>
        </div>
        <div class="rounded-lg p-3 card-panel">
          <h3 class="font-bold text-xs mb-2 flex items-center gap-2 text-primary">
            <span class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold badge-glow-warning">
              II
            </span>
            CAPEX & OPEX 成本结构
          </h3>
          <div class="grid grid-cols-2 gap-2 text-[10px] text-secondary">
            <div>
              <label class="block mb-0.5 text-muted">集装箱单价 万元/MWh</label>
              <input
                v-model.number="f.containerCostPerMWh"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">PCS 单价 万元/MW</label>
              <input
                v-model.number="f.pcsCostPerMW"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">BOP 配套 万元/MWh</label>
              <input
                v-model.number="f.bopCostPerMWh"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">变电站 万元/MW</label>
              <input
                v-model.number="f.substationCostPerMW"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">输电线路 万元/MW</label>
              <input
                v-model.number="f.transmissionCostPerMW"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">土地成本 万元/MW</label>
              <input
                v-model.number="f.landCostPerMW"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">开发费 万元/MW</label>
              <input
                v-model.number="f.developmentCostPerMW"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">固定 O&M 元/kW-年</label>
              <input
                v-model.number="f.fixedOpexPerKW"
                type="number"
                step="0.5"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">可变 O&M 元/MWh</label>
              <input
                v-model.number="f.varOpexPerMWh"
                type="number"
                step="0.1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">保险费率 % of CAPEX</label>
              <input
                v-model.number="f.insuranceRate"
                type="number"
                step="0.01"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">O&M 年涨幅 %</label>
              <input
                v-model.number="f.opexEscalation"
                type="number"
                step="0.1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">VAT 税率 %</label>
              <input
                v-model.number="f.vatRate"
                type="number"
                step="0.5"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-3 gap-3">
        <div class="rounded-lg p-3 card-panel">
          <h3 class="font-bold text-xs mb-2 flex items-center gap-2 text-primary">
            <span
              class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold badge-glow-info-secondary"
            >
              III
            </span>
            融资与税务 Financing & Tax
          </h3>
          <div class="grid grid-cols-1 gap-2 text-[10px] text-secondary">
            <div>
              <label class="block mb-0.5 text-muted">折现率 %</label>
              <input
                v-model.number="f.discountRate"
                type="number"
                step="0.1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">债务融资比例 %</label>
              <input
                v-model.number="f.debtRatio"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">权益融资比例 %</label>
              <input
                v-model.number="f.equityRatio"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">贷款利率 %</label>
              <input
                v-model.number="f.interestRate"
                type="number"
                step="0.1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">权益成本 %</label>
              <input
                v-model.number="f.costOfEquity"
                type="number"
                step="0.5"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">贷款年限</label>
              <input
                v-model.number="f.loanTenure"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">所得税率 %</label>
              <input
                v-model.number="f.taxRate"
                type="number"
                step="0.5"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">折旧年限</label>
              <input
                v-model.number="f.depreciationYears"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">残值率 %</label>
              <input
                v-model.number="f.residualRate"
                type="number"
                step="0.5"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">折旧方法</label>
              <select v-model="f.depreciationMethod" class="w-full rounded px-2 py-1 text-xs form-field-select">
                <option value="straight-line">直线折旧</option>
                <option value="double-declining">双倍余额递减</option>
              </select>
            </div>
          </div>
        </div>
        <div class="rounded-lg p-3 card-panel">
          <h3 class="font-bold text-xs mb-2 flex items-center gap-2 text-primary">
            <span class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold badge-glow-info">
              IV
            </span>
            增容与设备成本递减
          </h3>
          <div class="grid grid-cols-1 gap-2 text-[10px] text-secondary">
            <div>
              <label class="block mb-0.5 text-muted">增容集装箱单价 万元/MWh</label>
              <input
                v-model.number="f.augContainerCostPerMWh"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">设备成本年降幅 (学习率) %</label>
              <input
                v-model.number="f.costDeclineRate"
                type="number"
                step="0.1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">增容安装费 万元/台</label>
              <input
                v-model.number="f.augInstallCost"
                type="number"
                step="0.5"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">退役成本 万元/MWh</label>
              <input
                v-model.number="f.decommissioningCost"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
          </div>
        </div>
        <div class="rounded-lg p-3 card-panel">
          <h3 class="font-bold text-xs mb-2 flex items-center gap-2 text-primary">
            <span class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold badge-glow-success">
              V
            </span>
            敏感性分析范围
          </h3>
          <div class="text-[10px] space-y-1.5 text-muted">
            <div class="flex justify-between">
              <span>售电价波动范围</span>
              <span class="text-secondary">+/-{{ f.sensPct }}%</span>
            </div>
            <div class="flex justify-between">
              <span>衰减率波动范围</span>
              <span class="text-secondary">+/-{{ f.sensPct }}%</span>
            </div>
            <div class="flex justify-between">
              <span>融资利率波动</span>
              <span class="text-secondary">+/-{{ f.sensPct }}%</span>
            </div>
            <div class="flex justify-between">
              <span>CAPEX 波动</span>
              <span class="text-secondary">+/-{{ f.sensPct }}%</span>
            </div>
            <div>
              <label class="block mb-0.5 text-muted">波动幅度 %</label>
              <input
                v-model.number="f.sensPct"
                type="number"
                step="5"
                class="w-full rounded px-2 py-1 text-xs form-field-input"
              />
            </div>
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

      <div class="rounded-lg p-3 card-panel">
        <div class="flex justify-between items-center mb-2">
          <h3 class="font-bold text-xs text-primary">年度现金流明细表 Annual Cash Flow</h3>
          <button class="text-[10px] px-3 py-1 rounded transition-colors btn-accent-filled" @click="recalc">
            重新计算 Recalculate
          </button>
        </div>
        <div class="overflow-x-auto custom-scrollbar max-h-[300px]">
          <table class="w-full text-[10px] border-collapse">
            <thead>
              <tr class="sticky top-0 z-10 bg-card">
                <th class="text-left py-1 px-2 sticky left-0 z-20 text-muted border-b-border">年份</th>
                <th class="text-right py-1 px-2 text-muted border-b-border">发电量 MWh</th>
                <th class="text-right py-1 px-2 text-muted border-b-border">套利收入</th>
                <th class="text-right py-1 px-2 text-muted border-b-border">容量收入</th>
                <th class="text-right py-1 px-2 text-muted border-b-border">辅助服务</th>
                <th class="text-right py-1 px-2 text-muted border-b-border">总收入</th>
                <th class="text-right py-1 px-2 text-muted border-b-border">OPEX</th>
                <th class="text-right py-1 px-2 text-muted border-b-border">EBITDA</th>
                <th class="text-right py-1 px-2 text-muted border-b-border">净现金流</th>
                <th class="text-right py-1 px-2 text-muted border-b-border">累计现金流</th>
                <th v-if="f.debtRatio > 0" class="text-right py-1 px-2 text-muted border-b-border">DSCR</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in cashFlowTable" :key="'yr' + row.year" class="border-b-border">
                <td
                  class="py-1 px-2 sticky left-0 font-bold"
                  :style="
                    row.year === 0
                      ? { backgroundColor: 'var(--color-card)', color: 'var(--color-warning)' }
                      : { backgroundColor: 'var(--color-card)', color: 'var(--color-text-secondary)' }
                  "
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
                  :style="row.ebitda < 0 ? { color: 'var(--color-danger)' } : { color: 'var(--color-text-secondary)' }"
                >
                  {{ fmtNum(row.ebitda) }}
                </td>
                <td
                  class="text-right py-1 px-2 font-mono font-bold"
                  :style="row.cashFlow < 0 ? { color: 'var(--color-danger)' } : { color: 'var(--color-success)' }"
                >
                  {{ fmtNum(row.cashFlow) }}
                </td>
                <td
                  class="text-right py-1 px-2 font-mono"
                  :style="
                    row.cumCashFlow < 0 ? { color: 'var(--color-danger)' } : { color: 'var(--color-text-secondary)' }
                  "
                >
                  {{ fmtNum(row.cumCashFlow) }}
                </td>
                <td v-if="f.debtRatio > 0" class="text-right py-1 px-2 font-mono text-secondary">
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
import { useDraft } from '../composables/useDraft'
import CurrencyConverter from './CurrencyConverter.vue'
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
import { useChartTheme } from '../composables/useChartTheme.js'

const props = defineProps({ params: Object, results: Object, soh: Array, rte: Array, augQty: Array })

// 使用汇率管理
const { displayCurrency, formatAmount, convert } = useExchangeRate()

const { colors: chartColors } = useChartTheme({
  gridLine: 'var(--color-border-light)',
  info: '#0ea5e9',
  acLine: '#14b8a6',
  purple: 'var(--color-info)',
  orange: 'var(--color-chart-orange)',
  cyan: 'var(--color-chart-cyan)',
  redLight: '#f87171'
})

const { state: f, clearDraft: clearFDraft } = useDraft('financial-params', {
  offPeakPrice: 200,
  peakPrice: 600,
  spreadCapture: 85,
  operatingDays: 330,
  capacityPrice: 50000,
  ancillaryPrice: 30000,
  priceEscalation: 1.5,
  efficiencyLossPct: 5,
  containerCostPerMWh: 100,
  pcsCostPerMW: 25,
  bopCostPerMWh: 30,
  developmentCostPerMW: 20,
  landCostPerMW: 8,
  substationCostPerMW: 15,
  transmissionCostPerMW: 10,
  fixedOpexPerKW: 35,
  varOpexPerMWh: 3,
  insuranceRate: 0.4,
  opexEscalation: 2.0,
  discountRate: 7,
  debtRatio: 70,
  interestRate: 4.5,
  loanTenure: 15,
  costOfEquity: 12,
  equityRatio: 30,
  taxRate: 25,
  depreciationYears: 20,
  residualRate: 5,
  depreciationMethod: 'straight-line',
  vatRate: 5,
  gracePeriod: 2,
  augContainerCostPerMWh: 90,
  costDeclineRate: 5,
  augInstallCost: 5,
  decommissioningCost: 10,
  sensPct: 20
})

// 融资比例校验：确保债务+权益=100%
watch(
  [() => f.debtRatio, () => f.equityRatio],
  () => {
    if (f.debtRatio + f.equityRatio !== 100) {
      f.equityRatio = 100 - f.debtRatio
    }
  },
  { immediate: true }
)

const metrics = ref([
  { label: 'Project IRR', value: '-', unit: '%', textColor: 'var(--color-accent-secondary)' },
  { label: 'Equity IRR', value: '-', unit: '%', textColor: 'var(--color-success)' },
  { label: 'WACC', value: '-', unit: '%', textColor: '#0ea5e9' },
  { label: 'NPV (7%)', value: '-', unit: `万元 (${displayCurrency})`, textColor: 'var(--color-accent)' },
  { label: 'LCOS', value: '-', unit: `元/kWh (${displayCurrency})`, textColor: 'var(--color-info)' },
  { label: 'Payback', value: '-', unit: '年', textColor: 'var(--color-warning)' },
  { label: 'Total CAPEX', value: '-', unit: `万元 (${displayCurrency})`, textColor: 'var(--color-danger)' },
  { label: 'Min DSCR', value: '-', unit: 'x', textColor: 'var(--color-chart-orange)' }
])

const cashFlowTable = ref([])
const cashFlowChartRef = ref(null)
const revenueChartRef = ref(null)
const dscrChartRef = ref(null)
const capexChartRef = ref(null)

let cashFlowChart = null,
  revenueChart = null,
  dscrChart = null,
  capexChart = null
let cachedRows = []
let cachedCapexData = null
let _resizeHandler = null

function disposeAll() {
  ;[cashFlowChart, revenueChart, dscrChart, capexChart].forEach((c) => {
    c?.dispose()
  })
  cashFlowChart = revenueChart = dscrChart = capexChart = null
}

function fmtNum(v) {
  if (v == null || isNaN(v)) return '-'
  if (Math.abs(v) >= 100) return v.toFixed(1)
  return v.toFixed(2)
}

function computeAll() {
  const p = props.params || {}
  const soh = props.soh || []
  const augQty = props.augQty || []
  const ratedEnergy = p.ratedEnergy || 5
  const initContainerQty = p.initContainerQty || 62
  const initPcsQty = p.initPcsQty || 1
  const cyclesPerDay = p.cyclesPerDay || 1
  const duration = p.duration || 2

  const totalCapMWh = ratedEnergy * initContainerQty
  const totalCapMW = totalCapMWh / (duration || 1)

  const containerCost = f.containerCostPerMWh * totalCapMWh
  const pcsCost = f.pcsCostPerMW * totalCapMW
  const bopCost = f.bopCostPerMWh * totalCapMWh
  const devCost = f.developmentCostPerMW * totalCapMW
  const landCost = f.landCostPerMW * totalCapMW
  const substationCost = f.substationCostPerMW * totalCapMW
  const transmissionCost = f.transmissionCostPerMW * totalCapMW
  const baseCapex = containerCost + pcsCost + bopCost + devCost + landCost + substationCost + transmissionCost
  const vatAmount = (baseCapex * f.vatRate) / 100
  const totalCapex = baseCapex + vatAmount

  cachedCapexData = {
    containerCost,
    pcsCost,
    bopCost,
    devCost,
    landCost,
    substationCost,
    transmissionCost,
    totalCapex,
    totalCapMW,
    totalCapMWh
  }

  const wacc = (f.costOfEquity * f.equityRatio) / 100 + (f.interestRate * (1 - f.taxRate / 100) * f.debtRatio) / 100
  const debtAmount = (totalCapex * f.debtRatio) / 100
  const equityAmount = totalCapex - debtAmount
  const annualDebtService =
    f.interestRate > 0 && f.loanTenure > 0
      ? (debtAmount * (f.interestRate / 100) * Math.pow(1 + f.interestRate / 100, f.loanTenure)) /
        (Math.pow(1 + f.interestRate / 100, f.loanTenure) - 1)
      : 0
  const residualValue = (totalCapex * f.residualRate) / 100
  const spread = ((f.peakPrice - f.offPeakPrice) * f.spreadCapture) / 100

  let annualDepreciation = 0
  if (f.depreciationYears > 0) {
    if (f.depreciationMethod === 'straight-line') {
      annualDepreciation = (totalCapex * (1 - f.residualRate / 100)) / f.depreciationYears
    } else if (f.depreciationMethod === 'double-declining') {
      const rate = 2 / f.depreciationYears
      annualDepreciation = totalCapex * rate * (1 - f.residualRate / 100)
    }
  }

  const rows = []
  rows.push({
    year: 0,
    energy: 0,
    arbitrage: 0,
    capacity: 0,
    ancillary: 0,
    revenue: 0,
    opex: 0,
    ebitda: 0,
    depreciation: 0,
    interest: 0,
    taxableIncome: 0,
    tax: 0,
    augCapex: -totalCapex,
    debtService: 0,
    cashFlow: -totalCapex,
    cumCashFlow: -totalCapex,
    dscr: null
  })

  let cumCash = -totalCapex
  let remainingDebt = debtAmount
  let totalDiscountedCost = totalCapex
  let totalDiscountedEnergy = 0
  let minDscr = Infinity

  for (let i = 1; i <= 25; i++) {
    const idx = i
    const cSoh = soh[idx] != null ? soh[idx] : soh.length > 0 ? soh[soh.length - 1] : 1
    const yearEnergy = totalCapMWh * cyclesPerDay * f.operatingDays * cSoh * (1 - f.efficiencyLossPct / 100)
    const priceFactor = Math.pow(1 + f.priceEscalation / 100, i)
    const opexFactor = Math.pow(1 + f.opexEscalation / 100, i)

    const arbitrageRev = ((yearEnergy * spread) / 10000) * priceFactor
    const capacityRev = ((totalCapMW * f.capacityPrice) / 10000) * priceFactor
    const ancillaryRev = ((totalCapMW * f.ancillaryPrice) / 10000) * priceFactor
    const totalRevenue = arbitrageRev + capacityRev + ancillaryRev

    const fixedOpex = ((f.fixedOpexPerKW * totalCapMW * 1000) / 10000) * opexFactor
    const varOpex = ((f.varOpexPerMWh * yearEnergy) / 10000) * opexFactor
    const insurance = (totalCapex * f.insuranceRate) / 100
    const landLease = (totalCapMW * 2) / 10000
    const totalOpex = fixedOpex + varOpex + insurance + landLease
    const ebitda = totalRevenue - totalOpex

    let dep = 0
    if (f.depreciationMethod === 'straight-line') {
      dep = i <= f.depreciationYears ? annualDepreciation : 0
    } else if (f.depreciationMethod === 'double-declining') {
      // 修正：正确的双倍余额递减法，在最后两年切换直线折旧
      const depreciableAmount = totalCapex - residualValue
      if (i <= f.depreciationYears - 2) {
        // 前N-2年使用双倍余额递减
        const rate = 2 / f.depreciationYears
        const bookValueStart = totalCapex - rows.slice(1, i).reduce((s, r) => s + r.depreciation, 0)
        dep = Math.min(bookValueStart * rate, bookValueStart - residualValue)
      } else if (i <= f.depreciationYears) {
        // 最后两年使用直线折旧（将剩余可折旧金额平均分配）
        const bookValueStart = totalCapex - rows.slice(1, i).reduce((s, r) => s + r.depreciation, 0)
        dep = Math.max(0, (bookValueStart - residualValue) / (f.depreciationYears - i + 1))
      }
    }

    let interestPaid = 0,
      principalPaid = 0,
      debtServiceYear = 0
    if (remainingDebt > 0 && i <= f.loanTenure) {
      interestPaid = (remainingDebt * f.interestRate) / 100
      // 修正：添加宽限期处理（中东标准：宽限期内只还利息不还本金）
      if (i <= f.gracePeriod) {
        principalPaid = 0
        debtServiceYear = interestPaid
      } else {
        principalPaid = Math.min(annualDebtService - interestPaid, remainingDebt)
        debtServiceYear = interestPaid + principalPaid
        remainingDebt = Math.max(0, remainingDebt - principalPaid)
      }
    }

    const taxableIncome = ebitda - dep - interestPaid
    const tax = Math.max(0, (taxableIncome * f.taxRate) / 100)

    const augQtyYear = augQty[idx] || 0
    const costDeclineFactor = Math.pow(1 - f.costDeclineRate / 100, i)
    const augContainerPrice = f.augContainerCostPerMWh * costDeclineFactor
    const augCapexYear =
      augQtyYear > 0 ? -(augQtyYear * ratedEnergy * augContainerPrice + augQtyYear * f.augInstallCost) : 0

    const cashFlow = ebitda - tax - debtServiceYear + augCapexYear
    cumCash += cashFlow

    const discFactor = Math.pow(1 + f.discountRate / 100, i)
    totalDiscountedCost += (totalOpex + (augCapexYear < 0 ? -augCapexYear : 0)) / discFactor
    totalDiscountedEnergy += yearEnergy / discFactor

    const dscr = debtServiceYear > 0 ? (ebitda - tax) / debtServiceYear : null
    if (dscr !== null && dscr < minDscr) minDscr = dscr

    rows.push({
      year: i,
      energy: yearEnergy,
      arbitrage: arbitrageRev,
      capacity: capacityRev,
      ancillary: ancillaryRev,
      revenue: totalRevenue,
      opex: totalOpex,
      ebitda,
      depreciation: dep,
      interest: interestPaid,
      taxableIncome,
      tax,
      augCapex: augCapexYear,
      debtService: debtServiceYear,
      cashFlow,
      cumCashFlow: cumCash,
      dscr
    })
  }

  // 修正BUG4：LCOS退役成本应为支出（加到成本而非减去），残值为收入（减去成本）
  totalDiscountedCost -= residualValue / Math.pow(1 + f.discountRate / 100, 25)
  const decommissioningCostAmount = f.decommissioningCost * totalCapMWh
  totalDiscountedCost += decommissioningCostAmount / Math.pow(1 + f.discountRate / 100, 25)
  // 在第25年现金流中添加退役成本支出
  if (rows.length > 25 && f.decommissioningCost > 0) {
    rows[25].cashFlow -= decommissioningCostAmount
    rows[25].cumCashFlow -= decommissioningCostAmount
  }

  const lcos = totalDiscountedEnergy > 0 ? (totalDiscountedCost / totalDiscountedEnergy) * 10000 : 0
  const npv = rows.reduce((s, r) => s + r.cashFlow / (r.year === 0 ? 1 : Math.pow(1 + f.discountRate / 100, r.year)), 0)
  const irr = calcIRR(
    rows.map((r) => r.cashFlow),
    rows.map((r) => r.year)
  )
  // 修正BUG3：Equity IRR应使用权益现金流序列（第0年为权益出资，后续为项目现金流）
  const equityFlows = [-equityAmount, ...rows.slice(1).map((r) => r.cashFlow)]
  const equityYears = [0, ...rows.slice(1).map((r) => r.year)]
  const equityIrr = calcIRR(equityFlows, equityYears)

  // 修正BUG2：Payback回收期公式错误，prevCum应为上一年的累计现金流
  let payback = '-'
  for (let i = 1; i < rows.length; i++) {
    if (rows[i].cumCashFlow >= 0 && rows[i - 1].cumCashFlow < 0) {
      payback = (i - 1 + Math.abs(rows[i - 1].cumCashFlow) / rows[i].cashFlow).toFixed(1)
      break
    }
  }

  // 转换为显示货币
  const convertToDisplay = (usdAmount) => {
    return convert(usdAmount, 'USD', displayCurrency.value)
  }

  metrics.value[0].value = irr + '%'
  metrics.value[1].value = equityIrr + '%'
  metrics.value[0].value = irr + '%'
  metrics.value[1].value = equityIrr + '%'
  metrics.value[2].value = wacc.toFixed(2) + '%'
  metrics.value[3].value = convertToDisplay(npv).toFixed(0)
  metrics.value[4].value = lcos.toFixed(3) // LCOS 保持原单位，因为已经是单位成本
  metrics.value[5].value = payback
  metrics.value[6].value = convertToDisplay(totalCapex).toFixed(0)
  metrics.value[7].value = minDscr !== Infinity ? minDscr.toFixed(2) : '-'

  cashFlowTable.value = rows
  cachedRows = rows

  nextTick(() => {
    setTimeout(() => renderCharts(), 300)
  })
}

function calcIRR(flows, years) {
  let rate = 0.08
  for (let iter = 0; iter < 100; iter++) {
    let npv = 0,
      dnpv = 0
    for (let i = 0; i < flows.length; i++) {
      const t = years[i] - years[0]
      const df = Math.pow(1 + rate, t)
      npv += flows[i] / df
      if (t > 0) dnpv += (-t * flows[i]) / Math.pow(1 + rate, t + 1)
    }
    if (Math.abs(npv) < 1e-6) break
    const newRate = rate - npv / (dnpv || 1e-10)
    if (Math.abs(newRate - rate) < 1e-8) {
      rate = newRate
      break
    }
    rate = newRate
    if (rate < -0.99) rate = -0.5
    if (rate > 100) rate = 10
  }
  return Math.max(-99, Math.min(999, rate * 100)).toFixed(2)
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

  const rows = cachedRows
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
        let html = `<div class="tooltip-section-header">年份 ${year === 0 ? '建设期' : year + '年'}</div>`
        html += `<div>年净现金流: <span class="tooltip-value-bold" style="color:${row.cashFlow >= 0 ? colors.success : colors.danger}">${row.cashFlow >= 0 ? '+' : ''}${row.cashFlow.toFixed(0)} 万元</span></div>`
        html += `<div>累计现金流: <span class="tooltip-value-bold" style="color:${row.cumCashFlow >= 0 ? colors.success : colors.danger}">${row.cumCashFlow >= 0 ? '+' : ''}${row.cumCashFlow.toFixed(0)} 万元</span></div>`
        if (row.year > 0) {
          html += '<div class="tooltip-separator">'
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

  const rows = cachedRows.filter((r) => r.year > 0)
  const years = rows.map((r) => r.year)

  revenueChart.setOption({
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const year = params[0].axisValue
        const row = rows.find((r) => r.year === parseInt(year))
        if (!row) return ''
        let html = `<div class="tooltip-section-header">第 ${year} 年</div>`
        html += `<div>套利收入: <span class="tooltip-value-bold" style="color:${colors.acLine}">${row.arbitrage.toFixed(0)} 万元</span></div>`
        html += `<div>容量收入: <span class="tooltip-value-bold" style="color:${colors.purple}">${row.capacity.toFixed(0)} 万元</span></div>`
        html += `<div>辅助服务: <span class="tooltip-value-bold" style="color:${colors.orange}">${row.ancillary.toFixed(0)} 万元</span></div>`
        html += '<div class="tooltip-separator">'
        html += `<div>总收入: <span class="tooltip-value-bold">${row.revenue.toFixed(0)} 万元</span></div>`
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

  const rows = cachedRows.filter((r) => r.year > 0)
  const years = rows.map((r) => r.year)
  const dscrData = rows.map((r) => r.dscr || 0)

  dscrChart.setOption({
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const year = params[0].axisValue
        const row = rows.find((r) => r.year === parseInt(year))
        if (!row) return ''
        let html = `<div class="tooltip-section-header">第 ${year} 年</div>`
        html += `<div>EBITDA: <span class="tooltip-value-bold" style="color:${colors.cyan}">${row.ebitda.toFixed(0)} 万元</span></div>`
        html += `<div>还本付息: <span class="tooltip-value-bold" style="color:${colors.redLight}">${row.debtService.toFixed(0)} 万元</span></div>`
        if (row.debtService > 0) {
          html += '<div class="tooltip-separator">'
          html += `<div>DSCR: <span class="tooltip-value-bold" style="font-size:16px;color:${row.dscr >= 1.3 ? colors.success : colors.danger}">${row.dscr.toFixed(2)}x</span></div>`
          html += `<div style="color:${row.dscr >= 1.3 ? colors.success : colors.danger};">${row.dscr >= 1.3 ? '✓ 满足银行要求' : '✗ 低于银行底线 1.3x'}</div>`
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

  if (!cachedCapexData) return
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
  } = cachedCapexData

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

function calculateSensitivityData() {
  if (!cachedCapexData) return {}

  const { containerCost, pcsCost, bopCost, devCost } = cachedCapexData
  const sensitivityPct = f.sensPct || 20

  return {
    base: {
      container: containerCost,
      pcs: pcsCost,
      bop: bopCost,
      dev: devCost,
      total: containerCost + pcsCost + bopCost + devCost
    },
    positive: {
      container: containerCost * (1 + sensitivityPct / 100),
      pcs: pcsCost * (1 + sensitivityPct / 100),
      bop: bopCost * (1 + sensitivityPct / 100),
      dev: devCost * (1 + sensitivityPct / 100),
      total: (containerCost + pcsCost + bopCost + devCost) * (1 + sensitivityPct / 100)
    },
    negative: {
      container: containerCost * (1 - sensitivityPct / 100),
      pcs: pcsCost * (1 - sensitivityPct / 100),
      bop: bopCost * (1 - sensitivityPct / 100),
      dev: devCost * (1 - sensitivityPct / 100),
      total: (containerCost + pcsCost + bopCost + devCost) * (1 - sensitivityPct / 100)
    }
  }
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
  computeAll()
}

function recalc() {
  computeAll()
}
const debouncedRecalc = debounce(recalc, 300)

watch([() => props.params, () => props.soh, () => props.augQty], debouncedRecalc, { deep: true, immediate: true })
watch(f, debouncedRecalc, { deep: true })
watch(displayCurrency, () => {
  // 更新货币单位显示
  metrics.value[2].unit = `万元 (${displayCurrency.value})`
  metrics.value[3].unit = `元/kWh (${displayCurrency.value})`
  metrics.value[5].unit = `万元 (${displayCurrency.value})`
  // 重新计算以应用新的货币转换
  computeAll()
})

onMounted(() => {
  nextTick(() => computeAll())
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
