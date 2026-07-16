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
          <div class="drp-card-title-row">
            <h4 class="drp-card-title">
              {{ strategyLabel(sol.strategy_type) }}
            </h4>
            <span v-if="idx === 0" class="drp-recommend-badge">
              {{ $t('designTemplate.recommended') }}
            </span>
          </div>
          <span class="drp-strategy-en">{{ sol.strategy_type || 'balanced' }}</span>
        </div>

        <p class="drp-card-desc">{{ strategyDesc(sol.strategy_type) }}</p>

        <div class="drp-stats-row">
          <div class="drp-stat-block">
            <span class="drp-stat-label-text">{{ $t('designTemplate.labelSohFactor') }}</span>
            <span class="drp-stat-value-text">{{ sol.efficiencyChain?.systemRTE ?? '97' }}</span>
          </div>
          <div class="drp-stat-block">
            <span class="drp-stat-label-text">{{ $t('designTemplate.labelRteFactor') }}</span>
            <span class="drp-stat-value-text">{{ sol.efficiencyChain?.systemRTE ?? '97' }}</span>
          </div>
        </div>

        <div class="drp-curve-section">
          <div class="drp-section-title">{{ $t('designTemplate.curveTitle') }}</div>
          <div class="drp-curve-grid">
            <div v-for="(p, i) in curvePoints(sol)" :key="i" class="drp-curve-cell">
              <div class="drp-curve-year">{{ p.year }}</div>
              <div class="drp-curve-value">{{ p.value }}</div>
            </div>
          </div>
        </div>

        <div class="drp-card-footer">
          <span class="drp-card-date">{{ formatDate(sol.generatedAt) }}</span>
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
            }}, DOD={{ selectedSolution.degradationModel?.dod || DEFAULT_DOD }}%
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
import { useBessStore, DEFAULT_DOD } from '../stores/bess.js'

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

const strategyDescs = computed(() => ({
  economic: t('designTemplate.strategyDescEconomic'),
  balanced: t('designTemplate.strategyDescBalanced'),
  flexible: t('designTemplate.strategyDescFlexible'),
  manufacturer: t('designTemplate.strategyDescManufacturer')
}))

function strategyLabel(key) {
  return strategyLabels.value[key] || key
}

function strategyDesc(key) {
  return strategyDescs.value[key] || ''
}

// 模拟年度校正曲线 6 个点（基于 SOH 衰减近似）
function curvePoints(sol) {
  const init = sol?.efficiencyChain?.systemRTE ? Math.min(0.99, sol.efficiencyChain.systemRTE / 100) : 0.97
  const target = 0.7
  const years = [1, 5, 10, 15, 20, 25]
  return years.map((y) => {
    // 指数衰减至 target（@ y=25 趋近 target）
    const value = target + (init - target) * Math.exp(-y / 12)
    return { year: `第${y}年`, value: value != null && !isNaN(value) ? value.toFixed(2) : '--' }
  })
}

function formatDate(iso) {
  const d = iso ? new Date(iso) : new Date()
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}/${m}/${day}`
}

function fmtMoney(v) {
  if (v == null) return '-'
  const n = Number(v)
  if (isNaN(n)) return '-'
  if (n >= 1e6) return (n / 1e6).toFixed(2) + 'M'
  if (n >= 1e3) return (n / 1e3).toFixed(1) + 'K'
  return n.toLocaleString()
}

function confirmSolution() {
  try {
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
      ratedEnergy: sol.totalEnergyMWh,
      pcsPower: sol.pcs?.ratedPowerMW || sol.totalPowerMW || store.systemParams.pcsPower,
      duration: sol.duration || store.systemParams.duration,
      strategy: sol.strategy_type || props.strategy
    }

    emit('confirm', sol)
  } catch (e) {
    console.error('[DesignResultPreview] confirmSolution error:', e)
  }
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
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.drp-card {
  background: var(--color-card, #ffffff);
  border: 1px solid var(--color-border, #e5e7eb);
  border-radius: 12px;
  padding: 1rem 1.25rem;
  cursor: pointer;
  transition:
    border-color 0.2s,
    box-shadow 0.2s,
    transform 0.15s;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.drp-card:hover {
  border-color: var(--color-accent);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-1px);
}

.drp-card.selected {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.18);
}

.drp-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 0.375rem;
  gap: 0.5rem;
}

.drp-card-title-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
  min-width: 0;
}

.drp-card-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-text-primary, #111827);
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.drp-recommend-badge {
  font-size: 0.6875rem;
  font-weight: 500;
  padding: 0.125rem 0.5rem;
  border-radius: 6px;
  background: rgba(16, 185, 129, 0.12);
  color: #10b981;
  flex-shrink: 0;
}

.drp-strategy-en {
  font-size: 0.6875rem;
  color: var(--color-text-secondary, #6b7280);
  font-style: italic;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 140px;
}

.drp-card-desc {
  font-size: 0.75rem;
  color: var(--color-text-secondary, #6b7280);
  margin: 0 0 0.875rem 0;
  line-height: 1.4;
}

/* 关键数据行（两列 SOH/RTE 因子） */
.drp-stats-row {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1rem;
}

.drp-stat-block {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.drp-stat-label-text {
  font-size: 0.75rem;
  color: var(--color-text-secondary, #6b7280);
}

.drp-stat-value-text {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-accent, #2563eb);
  line-height: 1;
}

/* 年度校正曲线分组 */
.drp-curve-section {
  margin-bottom: 0.875rem;
}

.drp-section-title {
  font-size: 0.75rem;
  color: var(--color-text-secondary, #6b7280);
  margin-bottom: 0.5rem;
}

.drp-curve-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem;
}

.drp-curve-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 0.25rem;
  border: 1px solid var(--color-border, #e5e7eb);
  border-radius: 6px;
  background: var(--color-card, #ffffff);
}

.drp-curve-year {
  font-size: 0.6875rem;
  color: var(--color-text-secondary, #6b7280);
  margin-bottom: 0.125rem;
}

.drp-curve-value {
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-text-primary, #111827);
}

/* 卡片底部（分隔线 + 日期） */
.drp-card-footer {
  border-top: 1px solid var(--color-border, #e5e7eb);
  padding-top: 0.625rem;
  margin-top: auto;
}

.drp-card-date {
  font-size: 0.75rem;
  color: var(--color-text-secondary, #9ca3af);
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
