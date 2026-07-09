<template>
  <div class="h-full overflow-y-auto custom-scrollbar flex flex-col">
    <div class="flex-1 overflow-y-auto space-y-3 py-2 px-4">
      <FinancialMetrics :metrics="metrics" />

      <FinancialInputs />

      <FinancialCharts
        :params="params"
        :soh="soh"
        :cached-rows="cachedRows"
        :cached-capex-data="cachedCapexData"
        :metrics="metrics"
      />

      <CurrencyConverter />

      <ProductCAPEXLink @apply-config="handleProductConfig" />

      <FinancialTable :cash-flow-table="cashFlowTable" @recalc="recalc" />
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, onMounted, provide } from 'vue'
import { debounce } from 'lodash-es'
import { useFinancialModel } from '../composables/useFinancialModel'
import CurrencyConverter from './CurrencyConverter.vue'
import ProductCAPEXLink from './ProductCAPEXLink.vue'
import FinancialMetrics from './FinancialMetrics.vue'
import FinancialInputs from './FinancialInputs.vue'
import FinancialCharts from './FinancialCharts.vue'
import FinancialTable from './FinancialTable.vue'

const props = defineProps({
  params: { type: Object, default: () => ({}) },
  results: { type: Object, default: () => ({}) },
  soh: { type: Array, default: () => [] },
  rte: { type: Array, default: () => [] },
  augQty: { type: Array, default: () => [] }
})

const { f, metrics, cashFlowTable, computeAll, recalc } = useFinancialModel(props)

provide('financialParams', f)

const cachedRows = ref([])
const cachedCapexData = ref(null)

function computeAllWithCache() {
  computeAll(() => {
    cachedRows.value = cashFlowTable.value
  })
}

function handleProductConfig(config) {
  if (config.autoCalculatedCAPEX) {
    f.containerCostPerMWh = config.autoCalculatedCapexPerMWh * 0.6
    f.pcsCostPerMW = config.autoCalculatedCapexPerMWh * config.ratedEnergy * 0.2
    f.bopCostPerMWh = config.autoCalculatedCapexPerMWh * 0.2
  }
  if (config.ratedEnergy) {
    // eslint-disable-next-line vue/no-mutating-props
    props.params.ratedEnergy = config.ratedEnergy
  }
  if (config.acEfficiency) {
    // eslint-disable-next-line vue/no-mutating-props
    props.params.acEfficiency = config.acEfficiency
  }
  computeAllWithCache()
}

const debouncedRecalc = debounce(() => computeAllWithCache(), 300)

watch([() => props.params, () => props.soh, () => props.augQty], debouncedRecalc, { deep: true, immediate: true })
watch(f, debouncedRecalc, { deep: true })

// Sync cached data after computeAll
watch(cashFlowTable, (rows) => {
  if (rows.length) cachedRows.value = rows
})

onMounted(() => {
  nextTick(() => computeAllWithCache())
})
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
