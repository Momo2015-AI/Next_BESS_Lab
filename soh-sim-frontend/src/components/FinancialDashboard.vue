<template>
  <div class="h-full overflow-y-auto custom-scrollbar flex flex-col">
    <div class="flex-1 overflow-y-auto space-y-3 py-2 px-4">
      <div class="grid grid-cols-4 md:grid-cols-8 gap-2 mb-3">
        <div
          v-for="(m, idx) in metrics"
          :key="m.label"
          class="metric-card rounded-lg p-3 text-center transition-all hover:shadow-md"
          :class="`metric-text-${idx}`"
        >
          <div class="text-[9px] uppercase tracking-wider truncate text-muted">
            {{ m.label }}
          </div>
          <div class="text-base md:text-lg font-bold font-mono mt-1">
            {{ m.value }}
          </div>
          <div class="text-[8px] mt-0.5 text-muted">
            {{ m.unit }}
          </div>
        </div>
      </div>

      <FinCharts ref="finChartsRef" :model="model" />

      <div class="grid grid-cols-2 gap-3">
        <div class="rounded-lg p-3 card-bordered">
          <h3 class="font-bold text-xs mb-2 flex items-center gap-2 text-default">
            <span class="badge-i w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold">
              I
            </span>
            {{ t('financialDashboard.revenueStack') }}
          </h3>
          <div class="grid grid-cols-2 gap-2 text-[10px] text-secondary">
            <ParamInput v-model="f.offPeakPrice" :label="t('financialDashboard.offPeakPrice')" :step="0.1" />
            <ParamInput v-model="f.peakPrice" :label="t('financialDashboard.peakPrice')" :step="0.1" />
            <ParamInput v-model="f.spreadCapture" :label="t('financialDashboard.spreadCapture')" :step="0.1" />
            <ParamInput v-model="f.operatingDays" :label="t('financialDashboard.calendarDays')" :step="1" />
            <ParamInput v-model="f.capacityPrice" :label="t('financialDashboard.capacityPrice')" :step="100" />
            <ParamInput v-model="f.ancillaryPrice" :label="t('financialDashboard.ancillaryPrice')" :step="100" />
            <ParamInput v-model="f.priceEscalation" :label="t('financialDashboard.priceEscalation')" :step="0.1" />
            <ParamInput v-model="f.efficiencyLossPct" :label="t('financialDashboard.efficiencyLoss')" :step="0.01" />
          </div>
        </div>
        <div class="rounded-lg p-3 card-bordered">
          <h3 class="font-bold text-xs mb-2 flex items-center gap-2 text-default">
            <span class="badge-ii w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold">
              II
            </span>
            {{ t('financialDashboard.capexOpex') }}
          </h3>
          <div class="grid grid-cols-2 gap-2 text-[10px] text-secondary">
            <ParamInput v-model="f.containerCostPerMWh" :label="t('financialDashboard.containerCost')" :step="1" />
            <ParamInput v-model="f.pcsCostPerMW" :label="t('financialDashboard.pcsCost')" :step="1" />
            <ParamInput v-model="f.bopCostPerMWh" :label="t('financialDashboard.bopCost')" :step="1" />
            <ParamInput v-model="f.substationCostPerMW" :label="t('financialDashboard.substationCost')" :step="1" />
            <ParamInput v-model="f.transmissionCostPerMW" :label="t('financialDashboard.transmissionCost')" :step="1" />
            <ParamInput v-model="f.landCostPerMW" :label="t('financialDashboard.landCost')" :step="1" />
            <ParamInput v-model="f.developmentCostPerMW" :label="t('financialDashboard.devCost')" :step="1" />
            <ParamInput v-model="f.fixedOpexPerKW" :label="t('financialDashboard.fixedOm')" :step="0.5" />
            <ParamInput v-model="f.varOpexPerMWh" :label="t('financialDashboard.varOm')" :step="0.1" />
            <ParamInput v-model="f.insuranceRate" :label="t('financialDashboard.insuranceRate')" :step="0.01" />
            <ParamInput v-model="f.opexEscalation" :label="t('financialDashboard.omEscalation')" :step="0.1" />
            <ParamInput v-model="f.vatRate" :label="t('financialDashboard.vatRate')" :step="0.5" />
          </div>
        </div>
      </div>

      <div class="grid grid-cols-3 gap-3">
        <div class="rounded-lg p-3 card-bordered">
          <h3 class="font-bold text-xs mb-2 flex items-center gap-2 text-default">
            <span class="badge-iii w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold">
              III
            </span>
            {{ t('financialDashboard.financingTax') }}
          </h3>
          <div class="grid grid-cols-1 gap-2 text-[10px] text-secondary">
            <ParamInput v-model="f.discountRate" :label="t('financialDashboard.wacc')" :step="0.1" />
            <ParamInput v-model="f.debtRatio" :label="t('financialDashboard.debtRatio')" :step="1" />
            <ParamInput v-model="f.equityRatio" :label="t('financialDashboard.equityRatio')" :step="1" />
            <ParamInput v-model="f.interestRate" :label="t('financialDashboard.loanRate')" :step="0.1" />
            <ParamInput v-model="f.costOfEquity" :label="t('financialDashboard.costOfEquity')" :step="0.5" />
            <ParamInput v-model="f.loanTenure" :label="t('financialDashboard.loanYears')" :step="1" />
            <ParamInput v-model="f.taxRate" :label="t('financialDashboard.taxRate')" :step="0.5" />
            <ParamInput v-model="f.depreciationYears" :label="t('financialDashboard.depreciationYears')" :step="1" />
            <ParamInput v-model="f.residualRate" :label="t('financialDashboard.residualRate')" :step="0.5" />
            <ParamInput
              v-model="f.depreciationMethod"
              :label="t('financialDashboard.depreciationMethod')"
              type="select"
              :options="depreciationOptions"
            />
          </div>
        </div>
        <div class="rounded-lg p-3 card-bordered">
          <h3 class="font-bold text-xs mb-2 flex items-center gap-2 text-default">
            <span class="badge-iv w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold">
              IV
            </span>
            {{ t('financialDashboard.augmentation') }}
          </h3>
          <div class="grid grid-cols-1 gap-2 text-[10px] text-secondary">
            <ParamInput v-model="f.augContainerCostPerMWh" :label="t('financialDashboard.augContainerCost')" :step="1" />
            <ParamInput v-model="f.costDeclineRate" :label="t('financialDashboard.costDecline')" :step="0.1" />
            <ParamInput v-model="f.augInstallCost" :label="t('financialDashboard.augInstallCost')" :step="0.5" />
            <ParamInput v-model="f.decommissioningCost" :label="t('financialDashboard.decommissionCost')" :step="1" />
          </div>
        </div>
        <div class="rounded-lg p-3 card-bordered">
          <h3 class="font-bold text-xs mb-2 flex items-center gap-2 text-default">
            <span class="badge-v w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold">
              V
            </span>
            {{ t('financialDashboard.sensitivity') }}
          </h3>
          <div class="text-[10px] space-y-1.5 text-muted">
            <div class="flex justify-between">
              <span>{{ t('financialDashboard.priceVolatility') }}</span>
              <span class="text-secondary">+/-{{ f.sensPct }}%</span>
            </div>
            <div class="flex justify-between">
              <span>{{ t('financialDashboard.degradationVolatility') }}</span>
              <span class="text-secondary">+/-{{ f.sensPct }}%</span>
            </div>
            <div class="flex justify-between">
              <span>{{ t('financialDashboard.interestVolatility') }}</span>
              <span class="text-secondary">+/-{{ f.sensPct }}%</span>
            </div>
            <div class="flex justify-between">
              <span>{{ t('financialDashboard.capexVolatility') }}</span>
              <span class="text-secondary">+/-{{ f.sensPct }}%</span>
            </div>
            <ParamInput v-model="f.sensPct" :label="t('financialDashboard.volatilityRange')" :step="5" />
          </div>
        </div>
      </div>

      <CurrencyConverter />

      <ProductCAPEXLink @apply-config="handleProductConfig" />

      <div class="grid grid-cols-2 gap-3">
        <EnergyFlowSankey :params="params" :soh="soh" />
        <CostWaterfallChart :params="params" :cash-flow-table="cashFlowTable" />
      </div>

      <FinCashFlowTable :model="model" @recalc="handleRecalc" />
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { debounce } from 'lodash-es'
import CurrencyConverter from './CurrencyConverter.vue'
import ParamInput from './ParamInput.vue'
import CostWaterfallChart from './CostWaterfallChart.vue'
import EnergyFlowSankey from './EnergyFlowSankey.vue'
import ProductCAPEXLink from './ProductCAPEXLink.vue'
import FinCharts from './FinCharts.vue'
import FinCashFlowTable from './FinCashFlowTable.vue'
import { useExchangeRate } from '../composables/useExchangeRate.js'
import { useFinancialModel } from '../composables/useFinancialModel.js'

const props = defineProps({ params: Object, results: Object, soh: Array, rte: Array, augQty: Array })
const { t } = useI18n()
const { displayCurrency } = useExchangeRate()

const model = useFinancialModel(props)
const { f, metrics, cashFlowTable, computeAll } = model

const finChartsRef = ref(null)

const depreciationOptions = [
  { value: 'straight-line', label: t('financialDashboard.straightLine') },
  { value: 'double-declining', label: t('financialDashboard.doubleDeclining') }
]

function renderCharts() {
  finChartsRef.value?.render()
}

function handleRecalc() {
  computeAll(renderCharts)
}

function handleProductConfig(config) {
  if (config.autoCalculatedCAPEX) {
    f.containerCostPerMWh = config.autoCalculatedCapexPerMWh * 0.6
    f.pcsCostPerMW = config.autoCalculatedCapexPerMWh * config.ratedEnergy * 0.2
    f.bopCostPerMWh = config.autoCalculatedCapexPerMWh * 0.2
  }

  if (config.ratedEnergy && props.params) {
    // eslint-disable-next-line vue/no-mutating-props
    props.params.ratedEnergy = config.ratedEnergy
  }

  if (config.acEfficiency && props.params) {
    // eslint-disable-next-line vue/no-mutating-props
    props.params.acEfficiency = config.acEfficiency
  }

  computeAll(renderCharts)
}

const debouncedRecalc = debounce(() => {
  computeAll(renderCharts)
}, 300)

watch([() => props.params, () => props.soh, () => props.augQty], debouncedRecalc, { deep: true, immediate: true })
watch(f, debouncedRecalc, { deep: true })
watch(displayCurrency, () => {
  metrics.value[3].unit = `${t('financialDashboard.wanUnit')} (${displayCurrency.value})`
  metrics.value[4].unit = `${t('financialDashboard.energyPriceUnit')} (${displayCurrency.value})`
  metrics.value[6].unit = `${t('financialDashboard.wanUnit')} (${displayCurrency.value})`
  computeAll(renderCharts)
})

onMounted(() => {
  nextTick(() => computeAll(renderCharts))
})
</script>

<style scoped>
.metric-card {
  background-color: var(--color-card);
  border: 1px solid var(--color-border);
  border-top: 3px solid var(--color-accent);
}

.metric-text-0 { color: var(--color-accent-secondary); }
.metric-text-1 { color: var(--color-success); }
.metric-text-2 { color: #0ea5e9; }
.metric-text-3 { color: var(--color-accent); }
.metric-text-4 { color: var(--color-info); }
.metric-text-5 { color: var(--color-warning); }
.metric-text-6 { color: var(--color-danger); }
.metric-text-7 { color: var(--color-chart-orange); }

.badge-i {
  background-color: var(--color-accent-glow);
  color: var(--color-accent);
}

.badge-ii {
  background-color: rgba(245, 158, 11, 0.2);
  color: var(--color-warning);
}

.badge-iii {
  background-color: rgba(59, 130, 246, 0.2);
  color: var(--color-accent-secondary);
}

.badge-iv {
  background-color: rgba(168, 85, 247, 0.2);
  color: var(--color-info);
}

.badge-v {
  background-color: rgba(16, 185, 129, 0.2);
  color: var(--color-success);
}

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
