<template>
  <div class="h-full overflow-y-auto custom-scrollbar flex flex-col">
    <div class="flex-1 overflow-y-auto space-y-3 py-2 px-4">
      <FinancialMetrics :metrics="metrics" />

      <!-- 独立模式：系统规模 + 电量参数区 -->
      <StandaloneParams v-if="mode === 'standalone'" v-model="standaloneParams" @change="onStandaloneChange" />

      <!-- Tier 3: 年吞吐电量 & SOH 曲线摘要 -->
      <div v-if="mode === 'standalone'" class="text-xs text-gray-500 dark:text-gray-400 mt-1 px-1 space-y-0.5">
        <div>Annual Energy Throughput: {{ annualEnergyThroughput.toLocaleString() }} MWh</div>
        <div>
          SOH Year 1 → Year 25: {{ projectedSohCurve[0] }}% → {{ projectedSohCurve[projectedSohCurve.length - 1] }}%
        </div>
      </div>

      <FinancialInputs />

      <FinancialCharts
        :params="params"
        :soh="soh"
        :cached-rows="cachedRows"
        :cached-capex-data="cachedCapexData"
        :metrics="metrics"
      />

      <CurrencyConverter />

      <!-- 项目模式才显示产品联动 -->
      <ProductCAPEXLink v-if="mode === 'project'" @apply-config="handleProductConfig" />

      <FinancialTable :cash-flow-table="cashFlowTable" @recalc="recalc" />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, nextTick, onMounted, provide } from 'vue'
import { debounce } from 'lodash-es'
import { useFinancialModel } from '../composables/useFinancialModel'
import CurrencyConverter from './CurrencyConverter.vue'
import ProductCAPEXLink from './ProductCAPEXLink.vue'
import FinancialMetrics from './FinancialMetrics.vue'
import FinancialInputs from './FinancialInputs.vue'
import StandaloneParams from './StandaloneParams.vue'
import FinancialCharts from './FinancialCharts.vue'
import FinancialTable from './FinancialTable.vue'
import { useBessStore, DEFAULT_SURVEY } from '../stores/bess.js'

const props = defineProps({
  mode: { type: String, default: 'project' },
  params: { type: Object, default: () => ({}) },
  results: { type: Object, default: () => ({}) },
  soh: { type: Array, default: () => [] },
  rte: { type: Array, default: () => [] },
  augQty: { type: Array, default: () => [] }
})

const store = useBessStore()

// 独立模式参数
const standaloneParams = reactive({
  totalCapMWh: 100,
  totalCapMW: 50,
  cyclesPerDay: DEFAULT_SURVEY.cyclesPerDay,
  operatingDays: 330,
  efficiencyLossPct: 5,
  sohStart: 100,
  sohAnnualDecline: 2.0
})

// Tier 3: 年吞吐电量 = 容量 * 循环次数 * 运行天数
const annualEnergyThroughput = computed(() => {
  const capMWh = standaloneParams.totalCapMWh || 0
  const cycles = standaloneParams.cyclesPerDay || 1
  const days = standaloneParams.operatingDays || 365
  return +(capMWh * cycles * days).toFixed(1)
})

// Tier 3: 预估 SOH 曲线（年化线性衰减，25 年）
const projectedSohCurve = computed(() => {
  const start = standaloneParams.sohStart || 100
  const decline = standaloneParams.sohAnnualDecline || 0.5
  const years = 25
  const curve = []
  for (let i = 0; i < years; i++) {
    curve.push(+(start - decline * i).toFixed(2))
  }
  return curve
})

// 将 standalone 参数注入到 props 中传给 useFinancialModel
const mergedProps = computed(() => ({
  ...props,
  standalone: props.mode === 'standalone' ? standaloneParams : null
}))

const { f, metrics, cashFlowTable, computeAll, recalc } = useFinancialModel(mergedProps)

provide('financialParams', f)
provide('standaloneParams', null) // 由子组件 provide

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
    store.systemParams.ratedEnergy = config.ratedEnergy
  }
  if (config.acEfficiency) {
    store.systemParams.acEfficiency = config.acEfficiency
  }
  computeAllWithCache()
}

function onStandaloneChange() {
  computeAllWithCache()
}

const debouncedRecalc = debounce(() => computeAllWithCache(), 300)

watch([() => props.params, () => props.soh, () => props.augQty], debouncedRecalc, { deep: true, immediate: true })
watch(f, debouncedRecalc, { deep: true })
watch(standaloneParams, debouncedRecalc, { deep: true })

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
