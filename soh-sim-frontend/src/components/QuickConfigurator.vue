<template>
  <div class="quick-config">
    <!-- Hero Input Section -->
    <section class="qc-hero">
      <div class="qc-hero-header">
        <AppIcon name="battery" :size="36" class="qc-hero-icon" />
        <h1 class="qc-title">{{ $t('quickConfig.title') }}</h1>
        <p class="qc-subtitle">{{ $t('quickConfig.subtitle') }}</p>
      </div>

      <div class="qc-form-card">
        <div class="qc-form-grid">
          <div class="qc-field">
            <label class="qc-label">{{ $t('quickConfig.totalPower') }}</label>
            <div class="qc-input-wrap">
              <input
                v-model.number="form.totalPower"
                type="number"
                min="1"
                max="5000"
                step="1"
                class="qc-input"
                placeholder="50"
                @keyup.enter="generate"
              />
              <span class="qc-unit">MW</span>
            </div>
          </div>

          <div class="qc-field">
            <label class="qc-label">{{ $t('quickConfig.ratedEnergy') }}</label>
            <div class="qc-input-wrap">
              <input
                v-model.number="form.ratedEnergy"
                type="number"
                min="1"
                max="50000"
                step="1"
                class="qc-input"
                placeholder="100"
                @keyup.enter="generate"
              />
              <span class="qc-unit">MWh</span>
            </div>
          </div>

          <div class="qc-field">
            <label class="qc-label">{{ $t('quickConfig.duration') }}</label>
            <div class="qc-input-wrap">
              <input
                v-model.number="form.duration"
                type="number"
                min="0.5"
                max="24"
                step="0.5"
                class="qc-input"
                placeholder="2"
                @keyup.enter="generate"
              />
              <span class="qc-unit">h</span>
            </div>
          </div>

          <div class="qc-field">
            <label class="qc-label">{{ $t('quickConfig.strategy') }}</label>
            <select v-model="form.strategy" class="qc-select">
              <option value="economic">{{ $t('quickConfig.strategyEconomic') }}</option>
              <option value="balanced">{{ $t('quickConfig.strategyBalanced') }}</option>
              <option value="flexible">{{ $t('quickConfig.strategyFlexible') }}</option>
            </select>
          </div>

          <div class="qc-field">
            <label class="qc-label">{{ $t('quickConfig.temperature') }}</label>
            <div class="qc-input-wrap">
              <input
                v-model.number="form.temperature"
                type="number"
                min="-20"
                max="60"
                step="1"
                class="qc-input"
                placeholder="25"
              />
              <span class="qc-unit">&deg;C</span>
            </div>
          </div>

          <div class="qc-field">
            <label class="qc-label">{{ $t('quickConfig.cyclesPerDay') }}</label>
            <div class="qc-input-wrap">
              <input
                v-model.number="form.cyclesPerDay"
                type="number"
                min="0.5"
                max="10"
                step="0.5"
                class="qc-input"
                placeholder="1"
              />
              <span class="qc-unit">&times;/d</span>
            </div>
          </div>
        </div>

        <button class="qc-btn-generate" :disabled="loading" @click="generate">
          <span v-if="loading" class="qc-spinner"></span>
          <AppIcon v-else name="lightning" :size="18" />
          {{ loading ? $t('quickConfig.generating') : $t('quickConfig.generateBtn') }}
        </button>
      </div>
    </section>

    <!-- Error State -->
    <div v-if="errorMsg" class="qc-error section-card">
      <p>{{ errorMsg }}</p>
    </div>

    <!-- Results Section -->
    <section v-if="result" class="qc-results">
      <!-- System Overview Card -->
      <div class="qc-card qc-card-overview">
        <div class="qc-card-header">
          <h3>{{ $t('quickConfig.systemOverview') }}</h3>
          <span class="qc-badge" :class="'qc-badge-' + result.strategy">
            {{ $t('quickConfig.strategy' + capitalize(result.strategy)) }}
          </span>
        </div>
        <div class="qc-kpi-grid">
          <div class="qc-kpi">
            <span class="qc-kpi-value">{{ fmtNum(result.totalEnergyMWh) }}</span>
            <span class="qc-kpi-label">MWh {{ $t('quickConfig.totalEnergy') }}</span>
          </div>
          <div class="qc-kpi">
            <span class="qc-kpi-value">{{ fmtNum(result.totalPowerMW) }}</span>
            <span class="qc-kpi-label">MW {{ $t('quickConfig.totalPower') }}</span>
          </div>
          <div class="qc-kpi">
            <span class="qc-kpi-value">{{ fmtNum(result.containerQty) }}</span>
            <span class="qc-kpi-label">{{ $t('quickConfig.containerQty') }}</span>
          </div>
          <div class="qc-kpi">
            <span class="qc-kpi-value">{{ fmtNum(result.pcsQty) }}</span>
            <span class="qc-kpi-label">{{ $t('quickConfig.pcsQty') }}</span>
          </div>
        </div>
      </div>

      <div class="qc-card-grid">
        <!-- Container Config -->
        <div class="qc-card">
          <div class="qc-card-header">
            <AppIcon name="package" :size="20" class="qc-card-icon" />
            <h4>{{ $t('quickConfig.containerConfig') }}</h4>
          </div>
          <dl class="qc-dl">
            <div class="qc-dl-row">
              <dt>{{ $t('quickConfig.model') }}</dt>
              <dd>{{ result.container.model || '-' }}</dd>
            </div>
            <div class="qc-dl-row">
              <dt>{{ $t('quickConfig.mfr') }}</dt>
              <dd>{{ result.container.mfr || '-' }}</dd>
            </div>
            <div class="qc-dl-row">
              <dt>{{ $t('quickConfig.ratedEnergyMWh') }}</dt>
              <dd>{{ fmtNum(result.container.ratedEnergyMWh) }} MWh</dd>
            </div>
            <div class="qc-dl-row">
              <dt>{{ $t('quickConfig.ratedPowerMW') }}</dt>
              <dd>{{ fmtNum(result.container.ratedPowerMW) }} MW</dd>
            </div>
            <div class="qc-dl-row">
              <dt>{{ $t('quickConfig.cooling') }}</dt>
              <dd>{{ result.container.cooling || '-' }}</dd>
            </div>
            <div class="qc-dl-row">
              <dt>{{ $t('quickConfig.cellModel') }}</dt>
              <dd class="qc-dd-mono">{{ result.container.cellModel || '-' }}</dd>
            </div>
            <div class="qc-dl-row">
              <dt>{{ $t('quickConfig.clustersPerContainer') }}</dt>
              <dd>{{ result.container.clustersPerContainer || '-' }}</dd>
            </div>
          </dl>
        </div>

        <!-- PCS Config -->
        <div class="qc-card">
          <div class="qc-card-header">
            <AppIcon name="settings" :size="20" class="qc-card-icon" />
            <h4>{{ $t('quickConfig.pcsConfig') }}</h4>
          </div>
          <dl class="qc-dl">
            <div class="qc-dl-row">
              <dt>{{ $t('quickConfig.model') }}</dt>
              <dd>{{ result.pcs.model || '-' }}</dd>
            </div>
            <div class="qc-dl-row">
              <dt>{{ $t('quickConfig.mfr') }}</dt>
              <dd>{{ result.pcs.mfr || '-' }}</dd>
            </div>
            <div class="qc-dl-row">
              <dt>{{ $t('quickConfig.ratedPowerMW') }}</dt>
              <dd>{{ fmtNum(result.pcs.ratedPowerMW) }} MW</dd>
            </div>
            <div class="qc-dl-row">
              <dt>{{ $t('quickConfig.efficiency') }}</dt>
              <dd>{{ fmtPct(result.pcs.efficiency) }}</dd>
            </div>
            <div class="qc-dl-row">
              <dt>{{ $t('quickConfig.acVoltage') }}</dt>
              <dd>{{ result.pcs.acVoltage || '-' }}</dd>
            </div>
            <div class="qc-dl-row">
              <dt>{{ $t('quickConfig.dcVoltageRange') }}</dt>
              <dd class="qc-dd-mono">{{ result.pcs.dcVoltageRange || '-' }}</dd>
            </div>
            <div class="qc-dl-row">
              <dt>{{ $t('quickConfig.topology') }}</dt>
              <dd>{{ result.pcs.topology || '-' }}</dd>
            </div>
          </dl>
        </div>

        <!-- Efficiency Chain -->
        <div class="qc-card">
          <div class="qc-card-header">
            <AppIcon name="lightning" :size="20" class="qc-card-icon" />
            <h4>{{ $t('quickConfig.efficiencyChain') }}</h4>
          </div>
          <dl class="qc-dl">
            <div class="qc-dl-row">
              <dt>{{ $t('quickConfig.cellRTE') }}</dt>
              <dd>{{ fmtPct(result.efficiencyChain.cellRTE) }}</dd>
            </div>
            <div class="qc-dl-row">
              <dt>{{ $t('quickConfig.pcsEfficiency') }}</dt>
              <dd>{{ fmtPct(result.efficiencyChain.pcsEfficiency) }}</dd>
            </div>
            <div class="qc-dl-row">
              <dt>{{ $t('quickConfig.transformerEfficiency') }}</dt>
              <dd>{{ fmtPct(result.efficiencyChain.transformerEfficiency) }}</dd>
            </div>
            <div class="qc-dl-row">
              <dt>{{ $t('quickConfig.cableEfficiency') }}</dt>
              <dd>{{ fmtPct(result.efficiencyChain.cableEfficiency) }}</dd>
            </div>
            <div class="qc-dl-row qc-dl-highlight">
              <dt>{{ $t('quickConfig.systemRTE') }}</dt>
              <dd class="qc-value-accent">{{ fmtPct(result.efficiencyChain.systemRTE) }}</dd>
            </div>
          </dl>
        </div>

        <!-- CAPEX Estimate -->
        <div class="qc-card">
          <div class="qc-card-header">
            <AppIcon name="dollar" :size="20" class="qc-card-icon" />
            <h4>{{ $t('quickConfig.capexEstimate') }}</h4>
          </div>
          <template v-if="result.estimatedCapex">
            <dl class="qc-dl">
              <div class="qc-dl-row">
                <dt>{{ $t('quickConfig.equipmentCost') }}</dt>
                <dd>{{ fmtMoney(result.estimatedCapex.equipmentCost || result.estimatedCapex.containerCost) }}</dd>
              </div>
              <div class="qc-dl-row">
                <dt>{{ $t('quickConfig.bopCost') }}</dt>
                <dd>{{ fmtMoney(result.estimatedCapex.bopCost) }}</dd>
              </div>
              <div class="qc-dl-row">
                <dt>{{ $t('quickConfig.epcCost') }}</dt>
                <dd>{{ fmtMoney(result.estimatedCapex.epcCost) }}</dd>
              </div>
              <div class="qc-dl-row">
                <dt>{{ $t('quickConfig.developmentCost') }}</dt>
                <dd>{{ fmtMoney(result.estimatedCapex.developmentCost) }}</dd>
              </div>
              <div class="qc-dl-row qc-dl-highlight">
                <dt>{{ $t('quickConfig.totalCapex') }}</dt>
                <dd class="qc-value-accent">{{ fmtMoney(result.estimatedCapex.totalCapex) }}</dd>
              </div>
              <div class="qc-dl-row">
                <dt>{{ $t('quickConfig.capexPerKWh') }}</dt>
                <dd>{{ fmtMoneyPerMWh(result.estimatedCapex.capexPerMWh) }}</dd>
              </div>
            </dl>
          </template>
          <p v-else class="qc-na">{{ $t('quickConfig.capexUnavailable') }}</p>
        </div>
      </div>
    </section>

    <!-- Empty State -->
    <div v-if="!result && !loading && !errorMsg" class="qc-empty section-card">
      <AppIcon name="lightbulb" :size="48" class="qc-empty-icon" />
      <p>{{ $t('quickConfig.emptyHint') }}</p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { post } from '../services/api.js'
import AppIcon from './AppIcon.vue'

const { t } = useI18n()

const form = reactive({
  totalPower: 50,
  ratedEnergy: 100,
  duration: 2,
  strategy: 'economic',
  temperature: 25,
  cyclesPerDay: 1
})

const loading = ref(false)
const errorMsg = ref('')
const result = ref(null)

function capitalize(s) {
  return s ? s.charAt(0).toUpperCase() + s.slice(1) : s
}

function fmtNum(v) {
  if (v == null) return '-'
  return typeof v === 'number' ? v.toLocaleString('zh-CN', { maximumFractionDigits: 1 }) : v
}

function fmtPct(v) {
  if (v == null) return '-'
  return (typeof v === 'number' ? v.toFixed(1) : v) + '%'
}

function fmtMoney(v) {
  if (v == null) return '-'
  if (v >= 10000) {
    return (v / 10000).toFixed(2) + ' ' + t('quickConfig.wanYuan')
  }
  return v.toFixed(2) + ' ' + t('quickConfig.wanYuan')
}

function fmtMoneyPerMWh(v) {
  if (v == null) return '-'
  if (v >= 10000) {
    return (v / 10000).toFixed(2) + ' ' + t('quickConfig.wanPerMWh')
  }
  return v.toFixed(2) + ' ' + t('quickConfig.yuanPerMWh')
}

function normalizeResult(data) {
  const sol = data.recommendation || (data.solutions && data.solutions[0]) || data
  return {
    strategy: sol.strategy_type || data.strategy,
    totalEnergyMWh: sol.totalEnergyMWh,
    totalPowerMW: sol.totalPowerMW,
    containerQty: sol.containerQty,
    pcsQty: sol.pcsQty,
    container: sol.container || {},
    pcs: sol.pcs || {},
    efficiencyChain: sol.efficiencyChain || {},
    estimatedCapex: sol.estimatedCapex || null,
    degradationModel: sol.degradationModel || null,
    auxPower: sol.auxPower || null
  }
}

async function generate() {
  errorMsg.value = ''
  result.value = null

  if (!form.totalPower || form.totalPower <= 0) {
    errorMsg.value = t('quickConfig.errorPowerRequired')
    return
  }
  if (!form.ratedEnergy || form.ratedEnergy <= 0) {
    errorMsg.value = t('quickConfig.errorEnergyRequired')
    return
  }

  loading.value = true
  try {
    const resp = await post('/api/design/auto', {
      survey_params: {
        totalPower: form.totalPower,
        ratedEnergy: form.ratedEnergy,
        duration: form.duration,
        temperature: form.temperature,
        cyclesPerDay: form.cyclesPerDay,
        dod: 90
      },
      strategy: form.strategy
    })

    if (resp.success && resp.data) {
      result.value = normalizeResult(resp.data)
    } else {
      errorMsg.value = resp.error || t('quickConfig.errorUnknown')
    }
  } catch (e) {
    errorMsg.value = e.message || t('quickConfig.errorNetwork')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.quick-config {
  max-width: 960px;
  margin: 0 auto;
  padding: 0 16px 48px;
}

/* Hero */
.qc-hero {
  text-align: center;
  padding: 40px 0 32px;
}
.qc-hero-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}
.qc-hero-icon {
  color: var(--color-accent);
  margin-bottom: 4px;
}
.qc-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 8px;
}
.qc-subtitle {
  font-size: 0.95rem;
  color: var(--text-secondary);
  margin: 0;
  max-width: 480px;
  margin-inline: auto;
}

/* Form Card */
.qc-form-card {
  background: var(--color-card);
  border: 1px solid var(--border-color, rgba(255, 255, 255, 0.08));
  border-radius: 16px;
  padding: 28px 32px;
  margin-top: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(12px);
}
.qc-form-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px 24px;
}
.qc-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.qc-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.qc-input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}
.qc-input {
  width: 100%;
  padding: 10px 12px;
  padding-right: 40px;
  border: 1px solid var(--border-color, rgba(255, 255, 255, 0.12));
  border-radius: 10px;
  background: var(--color-bg, rgba(255, 255, 255, 0.04));
  color: var(--text-primary);
  font-size: 0.95rem;
  font-variant-numeric: tabular-nums;
  transition: border-color 0.2s;
}
.qc-input:focus {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}
.qc-select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border-color, rgba(255, 255, 255, 0.12));
  border-radius: 10px;
  background: var(--color-bg, rgba(255, 255, 255, 0.04));
  color: var(--text-primary);
  font-size: 0.95rem;
  cursor: pointer;
  transition: border-color 0.2s;
}
.qc-select:focus {
  outline: none;
  border-color: var(--color-accent);
}
.qc-unit {
  position: absolute;
  right: 12px;
  font-size: 0.8rem;
  color: var(--text-tertiary);
  pointer-events: none;
}

.qc-btn-generate {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 24px;
  padding: 14px 48px;
  border: none;
  border-radius: 12px;
  background: var(--color-accent, #3b82f6);
  color: #fff;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition:
    opacity 0.2s,
    transform 0.15s;
}
.qc-btn-generate:hover:not(:disabled) {
  opacity: 0.9;
  transform: translateY(-1px);
}
.qc-btn-generate:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.qc-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: qc-spin 0.6s linear infinite;
}
@keyframes qc-spin {
  to {
    transform: rotate(360deg);
  }
}

/* Error */
.qc-error {
  text-align: center;
  color: #ef4444;
  padding: 20px;
  margin-top: 16px;
  font-size: 0.9rem;
}

/* Results */
.qc-results {
  margin-top: 32px;
}

.qc-card {
  background: var(--color-card);
  border: 1px solid var(--border-color, rgba(255, 255, 255, 0.08));
  border-radius: 14px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
.qc-card-overview {
  margin-bottom: 20px;
}
.qc-card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 18px;
}
.qc-card-header h3 {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-primary);
}
.qc-card-header h4 {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
}
.qc-badge {
  font-size: 0.72rem;
  padding: 2px 10px;
  border-radius: 20px;
  font-weight: 600;
}
.qc-badge-economic {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}
.qc-badge-balanced {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}
.qc-badge-flexible {
  background: rgba(168, 85, 247, 0.15);
  color: #a855f7;
}

.qc-card-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

/* KPIs */
.qc-kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
.qc-kpi {
  text-align: center;
}
.qc-kpi-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-accent);
  font-variant-numeric: tabular-nums;
}
.qc-kpi-label {
  font-size: 0.78rem;
  color: var(--text-tertiary);
  margin-top: 2px;
}

/* DL */
.qc-dl {
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0;
}
.qc-dl-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding: 7px 0;
  border-bottom: 1px solid var(--border-color, rgba(255, 255, 255, 0.04));
}
.qc-dl-row:last-child {
  border-bottom: none;
}
.qc-dl-row dt {
  font-size: 0.82rem;
  color: var(--text-secondary);
  flex-shrink: 0;
}
.qc-dl-row dd {
  margin: 0;
  font-size: 0.88rem;
  color: var(--text-primary);
  font-weight: 500;
  text-align: right;
  font-variant-numeric: tabular-nums;
}
.qc-dd-mono {
  font-family: 'SF Mono', 'Fira Code', monospace;
  font-size: 0.78rem !important;
}
.qc-dl-highlight {
  border-bottom: none;
  padding: 9px 0;
}
.qc-dl-highlight dt {
  font-weight: 600;
  color: var(--text-primary);
}
.qc-value-accent {
  color: var(--color-accent) !important;
  font-weight: 700 !important;
  font-size: 1rem !important;
}
.qc-na {
  text-align: center;
  color: var(--text-tertiary);
  font-style: italic;
  margin: 8px 0 0;
}

/* Empty */
.qc-empty {
  text-align: center;
  padding: 48px;
  margin-top: 32px;
}
.qc-empty-icon {
  margin-bottom: 12px;
}
.qc-empty p {
  margin: 0;
  color: var(--text-tertiary);
  font-size: 0.95rem;
}

@media (max-width: 768px) {
  .qc-form-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .qc-card-grid {
    grid-template-columns: 1fr;
  }
  .qc-kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .qc-form-card {
    padding: 20px 18px;
  }
  .qc-title {
    font-size: 1.35rem;
  }
}
</style>
