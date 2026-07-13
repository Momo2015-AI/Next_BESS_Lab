<template>
  <div class="design-engine-panel">
    <!-- 输入区域 -->
    <div class="panel-section">
      <h3 class="section-title">
        <AppIcon name="settings" size="16" /> {{ $t('design.surveyInput') }}
      </h3>
      <div class="form-grid">
        <div class="form-group">
          <label>{{ $t('design.ratedEnergy') }} (MWh)</label>
          <input
            v-model.number="form.ratedEnergy"
            type="number"
            min="1"
            step="1"
            class="form-input"
          />
        </div>
        <div class="form-group">
          <label>{{ $t('design.totalPower') }} (MW)</label>
          <input
            v-model.number="form.totalPower"
            type="number"
            min="1"
            step="0.1"
            class="form-input"
          />
        </div>
        <div class="form-group">
          <label>{{ $t('design.duration') }} (h)</label>
          <input
            v-model.number="form.duration"
            type="number"
            min="0.5"
            max="24"
            step="0.5"
            class="form-input"
          />
        </div>
        <div class="form-group">
          <label>{{ $t('design.temperature') }} (°C)</label>
          <input
            v-model.number="form.temperature"
            type="number"
            min="-20"
            max="60"
            step="1"
            class="form-input"
          />
        </div>
        <div class="form-group">
          <label>{{ $t('design.cyclesPerDay') }}</label>
          <input
            v-model.number="form.cyclesPerDay"
            type="number"
            min="0.5"
            max="4"
            step="0.5"
            class="form-input"
          />
        </div>
        <div class="form-group">
          <label>{{ $t('design.dod') }} (%)</label>
          <input
            v-model.number="form.dod"
            type="number"
            min="50"
            max="100"
            step="1"
            class="form-input"
          />
        </div>
        <div class="form-group">
          <label>{{ $t('design.requiredEnergy') }} (MWh/天)</label>
          <input
            v-model.number="form.requiredEnergy"
            type="number"
            min="1"
            step="1"
            class="form-input"
          />
        </div>
        <div class="form-group">
          <label>{{ $t('design.location') }}</label>
          <select v-model="form.location" class="form-input">
            <option value="china">{{ $t('design.locationChina') }}</option>
            <option value="europe">{{ $t('design.locationEurope') }}</option>
            <option value="middle_east">{{ $t('design.locationMiddleEast') }}</option>
            <option value="other">{{ $t('design.locationOther') }}</option>
          </select>
        </div>
      </div>

      <div class="strategy-row">
        <div class="form-group">
          <label>{{ $t('design.strategy') }}</label>
          <div class="strategy-options">
            <button
              v-for="s in strategies"
              :key="s.key"
              :class="['strategy-btn', { active: form.strategy === s.key }]"
              @click="form.strategy = s.key"
              :title="s.description"
            >
              {{ s.label }}
            </button>
          </div>
        </div>
        <div class="form-group">
          <label>{{ $t('design.targetMetric') }}</label>
          <select v-model="form.targetMetric" class="form-input">
            <option value="lcos">LCOS ({{ $t('design.lowerBetter') }})</option>
            <option value="irr">IRR ({{ $t('design.higherBetter') }})</option>
            <option value="npv">NPV ({{ $t('design.higherBetter') }})</option>
            <option value="capex">CAPEX ({{ $t('design.lowerBetter') }})</option>
            <option value="payback">Payback ({{ $t('design.lowerBetter') }})</option>
          </select>
        </div>
      </div>

      <div class="action-row">
        <button
          class="btn btn-primary"
          :disabled="loading"
          @click="runDesign"
        >
          <span v-if="loading" class="spinner"></span>
          {{ loading ? $t('design.generating') : $t('design.generateBtn') }}
        </button>
        <button
          class="btn btn-secondary"
          :disabled="loading"
          @click="runFullWorkflow"
        >
          <span v-if="workflowLoading" class="spinner"></span>
          {{ workflowLoading ? $t('design.running') : $t('design.oneClickBtn') }}
        </button>
      </div>
      <div v-if="error" class="error-message">{{ error }}</div>
    </div>

    <!-- 方案列表 -->
    <div v-if="solutions.length > 0" class="panel-section">
      <h3 class="section-title">
        <span class="icon">📋</span> {{ $t('design.solutions') }} ({{ solutions.length }})
      </h3>
      <div class="solutions-grid">
        <div
          v-for="(sol, idx) in solutions"
          :key="sol.id || idx"
          :class="['solution-card', { recommended: idx === 0 }]"
        >
          <div class="card-header">
            <span class="rank-badge" :class="'rank-' + (idx + 1)">#{{ idx + 1 }}</span>
            <span class="strategy-tag">{{ getStrategyLabel(sol.strategy_type) }}</span>
            <span v-if="idx === 0" class="recommend-badge">{{ $t('design.recommended') }}</span>
          </div>
          <div class="card-body">
            <div class="card-row">
              <span class="label">{{ $t('design.containerModel') }}</span>
              <span class="value">{{ sol.container?.model || '—' }}</span>
            </div>
            <div class="card-row">
              <span class="label">{{ $t('design.manufacturer') }}</span>
              <span class="value">{{ sol.container?.mfr || '—' }}</span>
            </div>
            <div class="card-row">
              <span class="label">{{ $t('design.containerQty') }}</span>
              <span class="value">{{ sol.containerQty }} {{ $t('design.units') }}</span>
            </div>
            <div class="card-row">
              <span class="label">{{ $t('design.totalEnergy') }}</span>
              <span class="value highlight">{{ sol.totalEnergyMwh }} MWh</span>
            </div>
            <div class="card-row">
              <span class="label">{{ $t('design.pcsModel') }}</span>
              <span class="value">{{ sol.pcs?.model || '—' }}</span>
            </div>
            <div class="card-row">
              <span class="label">{{ $t('design.totalPower') }}</span>
              <span class="value">{{ sol.totalPowerMW }} MW</span>
            </div>
            <div class="card-row">
              <span class="label">{{ $t('design.systemRTE') }}</span>
              <span class="value">{{ sol.efficiencyChain?.systemRTE || '—' }}%</span>
            </div>
            <div class="card-row">
              <span class="label">{{ $t('design.estimatedCapex') }}</span>
              <span class="value highlight">
                {{ formatCurrency(sol.estimatedCapex?.totalCapex) }}
              </span>
            </div>
            <div class="card-row">
              <span class="label">{{ $t('design.capexPerMWh') }}</span>
              <span class="value">{{ formatCurrency(sol.estimatedCapex?.capexPerMWh) }}/MWh</span>
            </div>
            <div v-if="sol.score" class="card-row">
              <span class="label">{{ $t('design.score') }}</span>
              <span class="value">{{ sol.score.toFixed(2) }}</span>
            </div>
          </div>
          <div class="card-footer">
            <button class="btn btn-sm" @click="$emit('select', sol)">
              {{ $t('design.viewDetail') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 工作流结果 -->
    <div v-if="workflowResult" class="panel-section">
      <h3 class="section-title">
        <span class="icon">🚀</span> {{ $t('design.workflowResult') }}
      </h3>
      <div class="workflow-summary">
        <div class="summary-item">
          <span class="summary-value">{{ workflowResult.pipeline_summary?.successful || 0 }}</span>
          <span class="summary-label">{{ $t('design.successfulSolutions') }}</span>
        </div>
        <div class="summary-item">
          <span class="summary-value">{{ workflowResult.pipeline_summary?.failed || 0 }}</span>
          <span class="summary-label">{{ $t('design.failedSolutions') }}</span>
        </div>
        <div class="summary-item">
          <span class="summary-value">{{ workflowResult.strategy }}</span>
          <span class="summary-label">{{ $t('design.strategy') }}</span>
        </div>
      </div>
      <div v-if="workflowResult.recommendation" class="recommendation-detail">
        <h4>{{ $t('design.bestSolution') }}</h4>
        <div class="metrics-grid">
          <div
            v-for="(val, key) in workflowResult.recommendation.financial?.metrics || {}"
            :key="key"
            class="metric-item"
          >
            <span class="metric-value">{{ formatMetric(key, val) }}</span>
            <span class="metric-label">{{ key }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { post } from '../services/api.js'
import { useBessStore } from '../stores/bess.js'
import AppIcon from './AppIcon.vue'

const store = useBessStore()
const emit = defineEmits(['select', 'workflow-complete'])

const form = reactive({
  ratedEnergy: store.survey.ratedEnergy || 100,
  totalPower: store.survey.totalPower || 50,
  duration: store.survey.duration || 2,
  temperature: store.survey.temperature || 25,
  cyclesPerDay: store.survey.cyclesPerDay || 1,
  dod: 90,
  requiredEnergy: store.survey.requiredEnergy || 240,
  location: store.survey.location || 'china',
  strategy: 'economic',
  targetMetric: 'lcos'
})

const strategies = [
  { key: 'economic', label: '经济优先', description: '最大容量集装箱 → 最少 BOP 成本' },
  { key: 'balanced', label: '均衡方案', description: '中等容量 → CAPEX/MWh 最优' },
  { key: 'flexible', label: '灵活分期', description: '小型集装箱 → 便于分期扩容' },
  { key: 'manufacturer', label: '指定厂家', description: '限定厂家产品匹配' }
]

const loading = ref(false)
const workflowLoading = ref(false)
const error = ref(null)
const solutions = ref([])
const workflowResult = ref(null)

function getStrategyLabel(type) {
  const map = {
    economic: '经济优先',
    balanced: '均衡方案',
    flexible: '灵活分期',
    manufacturer: '指定厂家'
  }
  return map[type] || type || '—'
}

function formatCurrency(val) {
  if (val == null) return '—'
  const num = Number(val)
  if (num >= 1e8) return '$' + (num / 1e8).toFixed(2) + ' 亿'
  if (num >= 1e6) return '$' + (num / 1e6).toFixed(2) + 'M'
  if (num >= 1e3) return '$' + (num / 1e3).toFixed(0) + 'K'
  return '$' + num.toFixed(0)
}

function formatMetric(key, val) {
  if (val == null) return '—'
  if (key === 'lcos' || key === 'lcoe') return Number(val).toFixed(4)
  if (key === 'projectIrr' || key === 'equityIrr' || key === 'irr' || key === 'roi')
    return Number(val).toFixed(2) + '%'
  if (key === 'npv' || key === 'capex') return formatCurrency(val)
  if (key === 'payback') return Number(val).toFixed(1) + ' 年'
  if (typeof val === 'object') return JSON.stringify(val)
  return Number(val).toFixed(2)
}

async function runDesign() {
  loading.value = true
  error.value = null
  try {
    const resp = await post('/api/design/auto', {
      survey_params: { ...form },
      strategy: form.strategy
    })
    if (resp.success) {
      solutions.value = resp.data.solutions || []
      if (resp.data.solutions?.length > 0) {
        emit('select', resp.data.solutions[0])
      }
    }
  } catch (e) {
    error.value = e.message || '设计引擎执行失败'
  } finally {
    loading.value = false
  }
}

async function runFullWorkflow() {
  workflowLoading.value = true
  error.value = null
  workflowResult.value = null
  try {
    const resp = await post('/api/workflow/full', {
      survey_params: { ...form },
      strategy: form.strategy,
      target_metric: form.targetMetric
    })
    if (resp.success) {
      workflowResult.value = resp.data
      solutions.value = (resp.data.solutions || []).map(s => s.design).filter(Boolean)
      if (resp.data.recommendation) {
        emit('select', resp.data.recommendation.design)
      }
      emit('workflow-complete', resp.data)
    }
  } catch (e) {
    error.value = e.message || '编排执行失败'
  } finally {
    workflowLoading.value = false
  }
}
</script>

<style scoped>
.design-engine-panel {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.panel-section {
  background: var(--card-bg, #fff);
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  margin: 0 0 1rem 0;
  color: var(--text-primary, #1a1a1a);
}

.section-title .icon {
  font-size: 1.2rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 0.75rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.form-group label {
  font-size: 0.8rem;
  color: var(--text-secondary, #666);
  font-weight: 500;
}

.form-input {
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--border-color, #ddd);
  border-radius: 6px;
  font-size: 0.9rem;
  background: var(--input-bg, #f9f9f9);
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary, #3b82f6);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15);
}

.strategy-row {
  display: flex;
  gap: 1.5rem;
  margin-top: 1rem;
  align-items: flex-end;
}

.strategy-options {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.strategy-btn {
  padding: 0.4rem 0.75rem;
  border: 1px solid var(--border-color, #ddd);
  border-radius: 6px;
  background: var(--input-bg, #f9f9f9);
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s;
}

.strategy-btn.active {
  background: var(--color-accent);
  color: var(--color-text-on-accent);
  border-color: var(--color-accent);
}

.strategy-btn:hover:not(.active) {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.action-row {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
}

.btn {
  padding: 0.6rem 1.25rem;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: var(--color-accent);
  color: var(--color-text-on-accent);
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-accent-secondary);
}

.btn-secondary {
  background: var(--color-success);
  color: var(--color-text-on-accent);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--success-dark, #059669);
}

.btn-sm {
  padding: 0.35rem 0.75rem;
  font-size: 0.8rem;
  background: var(--input-bg, #f0f0f0);
  color: var(--text-primary, #333);
}

.error-message {
  margin-top: 0.75rem;
  padding: 0.5rem 0.75rem;
  background: var(--color-danger-glow-soft, rgba(239, 68, 68, 0.1));
  color: var(--color-danger);
  border-radius: 6px;
  font-size: 0.85rem;
}

.spinner {
  width: 14px;
  height: 14px;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  display: inline-block;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Solutions Grid */
.solutions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.solution-card {
  border: 1px solid var(--border-color, #e5e7eb);
  border-radius: 8px;
  overflow: hidden;
  transition: box-shadow 0.2s, transform 0.2s;
}

.solution-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

.solution-card.recommended {
  border-color: var(--primary, #3b82f6);
  box-shadow: 0 0 0 1px var(--primary, #3b82f6);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 0.75rem;
  background: var(--card-header-bg, #f8fafc);
  border-bottom: 1px solid var(--border-color, #e5e7eb);
}

.rank-badge {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--color-text-on-accent);
}

.rank-1 { background: var(--color-warning); }
.rank-2 { background: var(--color-text-secondary); }
.rank-3 { background: var(--color-text-muted); }
.rank-4, .rank-5 { background: var(--color-border-light); }

.strategy-tag {
  font-size: 0.75rem;
  padding: 0.15rem 0.5rem;
  background: var(--tag-bg, #e5e7eb);
  border-radius: 4px;
  color: var(--text-secondary, #666);
}

.recommend-badge {
  font-size: 0.7rem;
  padding: 0.15rem 0.5rem;
  background: var(--color-accent-glow);
  color: var(--color-accent);
  border-radius: 4px;
  margin-left: auto;
  font-weight: 600;
}

.card-body {
  padding: 0.75rem;
}

.card-row {
  display: flex;
  justify-content: space-between;
  padding: 0.25rem 0;
  font-size: 0.85rem;
  border-bottom: 1px solid var(--border-light, #f3f4f6);
}

.card-row:last-child {
  border-bottom: none;
}

.card-row .label {
  color: var(--text-secondary, #888);
}

.card-row .value {
  font-weight: 500;
  color: var(--text-primary, #333);
}

.card-row .value.highlight {
  color: var(--primary, #3b82f6);
  font-weight: 600;
}

.card-footer {
  padding: 0.5rem 0.75rem;
  border-top: 1px solid var(--border-color, #e5e7eb);
  text-align: right;
}

/* Workflow Result */
.workflow-summary {
  display: flex;
  gap: 2rem;
  margin-bottom: 1rem;
}

.summary-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.summary-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary, #3b82f6);
}

.summary-label {
  font-size: 0.8rem;
  color: var(--text-secondary, #888);
}

.recommendation-detail h4 {
  margin: 0 0 0.75rem 0;
  font-size: 0.95rem;
  color: var(--text-primary, #333);
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 0.5rem;
}

.metric-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.5rem;
  background: var(--metric-bg, #f8fafc);
  border-radius: 6px;
}

.metric-value {
  font-size: 1rem;
  font-weight: 600;
  color: var(--primary, #3b82f6);
}

.metric-label {
  font-size: 0.7rem;
  color: var(--text-secondary, #888);
  text-transform: uppercase;
  margin-top: 0.15rem;
}
</style>
