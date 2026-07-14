<template>
  <div class="design-result-preview">
    <h3 class="drp-title">{{ $t('designTemplate.resultTitle') }}</h3>
    <p class="drp-desc">{{ $t('designTemplate.resultDesc') }}</p>

    <div v-if="!solutions || solutions.length === 0" class="drp-empty">
      {{ $t('designTemplate.noSolutions') }}
    </div>

    <div v-else class="drp-solutions">
      <div
        v-for="(sol, idx) in solutions"
        :key="sol.id || idx"
        :class="['drp-card', { selected: selectedIdx === idx }]"
        @click="selectedIdx = idx"
      >
        <div class="drp-card-header">
          <span class="drp-rank">#{{ idx + 1 }}</span>
          <span class="drp-strategy-badge">{{ strategyLabel(sol.strategy_type) }}</span>
          <span v-if="idx === 0" class="drp-recommend-badge">{{ $t('designTemplate.recommended') }}</span>
        </div>

        <div class="drp-card-body">
          <div class="drp-topology">
            <div class="drp-topo-item">
              <span class="drp-topo-icon">📦</span>
              <span class="drp-topo-label">{{ sol.container?.model || '-' }}</span>
              <span class="drp-topo-qty">× {{ sol.containerQty }}</span>
            </div>
            <div class="drp-topo-item">
              <AppIcon name="lightning" size="14" class="drp-topo-icon" />
              <span class="drp-topo-label">{{ sol.pcs?.model || '-' }}</span>
              <span class="drp-topo-qty">× {{ sol.pcsQty }}</span>
            </div>
          </div>

          <div class="drp-stats">
            <div class="drp-stat">
              <span class="drp-stat-val">{{ sol.totalEnergyMwh }}</span>
              <span class="drp-stat-label">MWh</span>
            </div>
            <div class="drp-stat">
              <span class="drp-stat-val">{{ sol.efficiencyChain?.systemRTE ?? '-' }}%</span>
              <span class="drp-stat-label">RTE</span>
            </div>
            <div class="drp-stat">
              <span class="drp-stat-val">${{ fmtMoney(sol.estimatedCapex?.totalCapex) }}</span>
              <span class="drp-stat-label">CAPEX</span>
            </div>
            <div class="drp-stat">
              <span class="drp-stat-val">${{ fmtMoney(sol.estimatedCapex?.capexPerMWh) }}</span>
              <span class="drp-stat-label">/MWh</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 选中方案详情 -->
    <div v-if="selectedSolution" class="drp-detail">
      <h4>{{ $t('designTemplate.solutionDetail') }}</h4>
      <div class="drp-detail-grid">
        <div class="drp-detail-section">
          <h5>{{ $t('designTemplate.efficiencyChain') }}</h5>
          <table class="drp-detail-table">
            <tr v-for="(v, k) in selectedSolution.efficiencyChain" :key="k">
              <td>{{ k }}</td>
              <td>{{ v }}{{ typeof v === 'number' ? '%' : '' }}</td>
            </tr>
          </table>
        </div>
        <div class="drp-detail-section">
          <h5>{{ $t('designTemplate.capexBreakdown') }}</h5>
          <table class="drp-detail-table">
            <tr>
              <td>{{ $t('designTemplate.equipment') }}</td>
              <td>${{ fmtMoney(selectedSolution.estimatedCapex?.equipmentCost) }}</td>
            </tr>
            <tr>
              <td>{{ $t('designTemplate.epc') }}</td>
              <td>${{ fmtMoney(selectedSolution.estimatedCapex?.epcCost) }}</td>
            </tr>
            <tr>
              <td>{{ $t('designTemplate.development') }}</td>
              <td>${{ fmtMoney(selectedSolution.estimatedCapex?.developmentCost) }}</td>
            </tr>
            <tr class="drp-total-row">
              <td>{{ $t('designTemplate.total') }}</td>
              <td>${{ fmtMoney(selectedSolution.estimatedCapex?.totalCapex) }}</td>
            </tr>
          </table>
        </div>
        <div class="drp-detail-section">
          <h5>{{ $t('designTemplate.degradationModel') }}</h5>
          <p class="drp-degradation-info">
            {{ selectedSolution.degradationModel?.model || 'Arrhenius' }}
            <template v-if="selectedSolution.degradationModel?.manufacturer">
              — {{ selectedSolution.degradationModel.manufacturer }}
            </template>
          </p>
          <p class="drp-degradation-params">
            T={{ selectedSolution.degradationModel?.temperature || 25 }}°C, CPD={{
              selectedSolution.degradationModel?.cyclesPerDay || 1
            }}, DOD={{ selectedSolution.degradationModel?.dod || 80 }}%
          </p>
        </div>
      </div>
    </div>

    <div class="drp-actions">
      <button class="drp-btn drp-btn-secondary" @click="$emit('back')">
        {{ $t('designTemplate.back') }}
      </button>
      <button class="drp-btn drp-btn-primary" :disabled="selectedIdx === null" @click="confirmSolution">
        {{ $t('designTemplate.confirmSolution') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useBessStore } from '../stores/bess.js'
import AppIcon from './AppIcon.vue'

const { t } = useI18n()
const store = useBessStore()

const props = defineProps({
  solutions: { type: Array, default: () => [] },
  strategy: { type: String, default: 'balanced' }
})

const emit = defineEmits(['back', 'confirm'])

const selectedIdx = ref(0)

const selectedSolution = computed(() => {
  if (selectedIdx.value === null || !props.solutions) return null
  return props.solutions[selectedIdx.value] || null
})

const strategyLabels = computed(() => ({
  economic: t('designTemplate.strategyEconomic'),
  balanced: t('designTemplate.strategyBalanced'),
  flexible: t('designTemplate.strategyFlexible'),
  manufacturer: t('designTemplate.strategyManufacturer')
}))

function strategyLabel(key) {
  return strategyLabels[key] || key
}

function fmtMoney(v) {
  if (v == null) return '-'
  const n = Number(v)
  if (n >= 1e6) return (n / 1e6).toFixed(2) + 'M'
  if (n >= 1e3) return (n / 1e3).toFixed(1) + 'K'
  return n.toLocaleString()
}

function confirmSolution() {
  if (!selectedSolution.value) return

  const sol = selectedSolution.value
  // 将选中方案写入 store
  store.selectedProducts = {
    container: sol.container || {},
    pcs: sol.pcs || {},
    cell: sol.container?.cellModel ? { model: sol.container.cellModel } : {}
  }
  store.systemParams = {
    ...store.systemParams,
    initContainerQty: sol.containerQty,
    initPcsQty: sol.pcsQty,
    ratedEnergy: sol.totalEnergyMwh,
    pcsPower: sol.pcs?.ratedPowerMW || sol.totalPowerMw || store.systemParams.pcsPower,
    duration: sol.duration || store.systemParams.duration,
    strategy: sol.strategy_type || props.strategy
  }

  emit('confirm', sol)
}

onMounted(() => {
  if (props.solutions.length > 0) {
    selectedIdx.value = 0
  }
})
</script>

<style scoped>
.design-result-preview {
  padding: 1rem 0;
}

.drp-title {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.drp-desc {
  color: var(--color-text-secondary);
  font-size: 0.875rem;
  margin-bottom: 1.25rem;
}

.drp-empty {
  text-align: center;
  padding: 2rem;
  color: var(--color-text-secondary);
}

.drp-solutions {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.drp-card {
  border: 2px solid var(--color-border);
  border-radius: 10px;
  padding: 1rem;
  cursor: pointer;
  transition:
    border-color 0.2s,
    box-shadow 0.2s;
  background: var(--color-card);
}

.drp-card:hover {
  border-color: var(--color-accent);
}

.drp-card.selected {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3);
}

.drp-card-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.drp-rank {
  font-weight: 700;
  font-size: 0.875rem;
  color: var(--color-accent);
}

.drp-strategy-badge {
  font-size: 0.7rem;
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  background: var(--color-accent-glow);
  color: var(--color-accent);
}

.drp-recommend-badge {
  font-size: 0.65rem;
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  background: var(--color-success-glow);
  color: var(--color-success);
  margin-left: auto;
}

.drp-card-body {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.drp-topology {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.drp-topo-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.drp-topo-icon {
  font-size: 1rem;
}

.drp-topo-label {
  font-weight: 500;
  flex: 1;
}

.drp-topo-qty {
  font-weight: 600;
  color: var(--color-accent);
}

.drp-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.drp-stat {
  text-align: center;
  padding: 0.375rem;
  background: var(--color-bg-secondary, #f9fafb);
  border-radius: 6px;
}

.drp-stat-val {
  display: block;
  font-weight: 700;
  font-size: 0.9375rem;
}

.drp-stat-label {
  font-size: 0.6875rem;
  color: var(--color-text-secondary);
  text-transform: uppercase;
}

.drp-detail {
  margin-top: 1rem;
  padding: 1rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.drp-detail h4 {
  font-size: 0.9375rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.drp-detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
}

.drp-detail-section h5 {
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--color-text-secondary);
  margin-bottom: 0.5rem;
}

.drp-detail-table {
  width: 100%;
  font-size: 0.8125rem;
}

.drp-detail-table td {
  padding: 0.25rem 0;
}

.drp-detail-table td:last-child {
  text-align: right;
  font-weight: 500;
}

.drp-total-row {
  border-top: 1px solid var(--color-border);
}

.drp-total-row td {
  padding-top: 0.5rem;
  font-weight: 700;
}

.drp-degradation-info {
  font-size: 0.8125rem;
  margin-bottom: 0.25rem;
}

.drp-degradation-params {
  font-size: 0.75rem;
  color: var(--color-text-secondary);
}

.drp-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.drp-btn {
  padding: 0.5rem 1.25rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: opacity 0.2s;
}

.drp-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.drp-btn-secondary {
  background: var(--color-bg-secondary, #f3f4f6);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

.drp-btn-primary {
  background: var(--color-accent);
  color: var(--color-text-on-accent);
}
</style>
