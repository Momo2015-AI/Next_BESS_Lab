<template>
  <div class="design-engine-panel">
    <!-- 输入区域 -->
    <div class="panel-section">
      <h3 class="section-title">
        <AppIcon name="settings" size="16" />
        {{ $t('design.surveyInput') }}
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
            @input="markEdited('ratedEnergy')"
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
            @input="markEdited('totalPower')"
          />
        </div>
        <div class="form-group">
          <label>
            {{ $t('design.duration') }} (h)
            <span v-if="isDurationAuto" class="auto-badge">自动</span>
          </label>
          <div class="duration-input-row">
            <input
              v-model.number="form.duration"
              type="number"
              min="0.5"
              max="24"
              step="0.5"
              class="form-input"
              :class="{ 'auto-disabled': isDurationAuto }"
              :disabled="isDurationAuto"
              @input="markEdited('duration')"
            />
            <button
              v-if="isDurationAuto"
              class="unlock-btn"
              :title="$t('design.unlockDuration') || '手动设置'"
              @click="isDurationAuto = false"
            >
              🔓
            </button>
            <button
              v-else
              class="lock-btn"
              :title="$t('design.lockDuration') || '自动计算'"
              @click="unlockAndCalcDuration"
            >
              🔒
            </button>
          </div>
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
            @input="markEdited('temperature')"
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
            @input="markEdited('cyclesPerDay')"
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
            @input="markEdited('dod')"
          />
        </div>
        <div class="form-group">
          <label>
            {{ $t('design.requiredEnergy') }} (MWh/天)
            <span v-if="isReqEnergyAuto" class="auto-badge">自动</span>
          </label>
          <div class="duration-input-row">
            <input
              v-model.number="form.requiredEnergy"
              type="number"
              min="1"
              step="1"
              class="form-input"
              :class="{ 'auto-disabled': isReqEnergyAuto }"
              :disabled="isReqEnergyAuto"
              @input="markEdited('requiredEnergy')"
            />
            <button
              v-if="isReqEnergyAuto"
              class="unlock-btn"
              :title="$t('design.unlockRequiredEnergy') || '手动设置'"
              @click="isReqEnergyAuto = false"
            >
              🔓
            </button>
            <button
              v-else
              class="lock-btn"
              :title="$t('design.lockRequiredEnergy') || '自动计算'"
              @click="unlockAndCalcReqEnergy"
            >
              🔒
            </button>
          </div>
        </div>
        <div class="form-group">
          <label>{{ $t('design.country') }}</label>
          <div class="combobox-wrapper">
            <input
              v-model="countryInput"
              type="text"
              class="form-input"
              :placeholder="$t('design.country')"
              @focus="countryDropdown = true"
              @blur="onCountryBlur"
              @input="onCountryInput"
            />
            <div v-if="countryDropdown && filteredCountries.length > 0" class="combobox-dropdown">
              <div
                v-for="c in filteredCountries"
                :key="c"
                class="combobox-option"
                :class="{ active: c === form.country }"
                @mousedown.prevent="selectCountry(c)"
              >
                <span class="option-name">{{ c }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="form-group">
          <label>{{ $t('design.city') }}</label>
          <input
            v-model="form.city"
            type="text"
            class="form-input"
            :placeholder="$t('design.city')"
            @input="markEdited('city')"
          />
        </div>
        <div class="form-group">
          <label>{{ $t('design.site') }}</label>
          <input
            v-model="form.site"
            type="text"
            class="form-input"
            :placeholder="$t('design.site')"
            @input="markEdited('site')"
          />
        </div>
        <div class="form-group">
          <label>{{ $t('design.lat') }}</label>
          <input
            v-model.number="form.lat"
            type="number"
            step="0.0001"
            class="form-input"
            :placeholder="$t('design.lat')"
            @input="markEdited('lat')"
          />
        </div>
        <div class="form-group">
          <label>{{ $t('design.lng') }}</label>
          <input
            v-model.number="form.lng"
            type="number"
            step="0.0001"
            class="form-input"
            :placeholder="$t('design.lng')"
            @input="markEdited('lng')"
          />
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
              :title="s.description"
              @click="form.strategy = s.key"
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
        <button class="btn btn-primary" :disabled="loading" @click="runDesign">
          <span v-if="loading" class="spinner"></span>
          {{ loading ? $t('design.generating') : $t('design.generateBtn') }}
        </button>
        <button class="btn btn-secondary" :disabled="loading" @click="runFullWorkflow">
          <span v-if="workflowLoading" class="spinner"></span>
          {{ workflowLoading ? $t('design.running') : $t('design.oneClickBtn') }}
        </button>
      </div>
      <div v-if="error" class="error-message">{{ error }}</div>
    </div>

    <!-- 方案列表 -->
    <div v-if="solutions.length > 0" class="panel-section">
      <h3 class="section-title">
        <span class="icon">📋</span>
        {{ $t('design.solutions') }} ({{ solutions.length }})
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
              <span class="value highlight">{{ sol.totalEnergyMWh }} MWh</span>
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
        <span class="icon">🚀</span>
        {{ $t('design.workflowResult') }}
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
import { ref, reactive, watch, computed } from 'vue'
import { post } from '../services/api.js'
import { useBessStore, DEFAULT_DOD } from '../stores/bess.js'
import AppIcon from './AppIcon.vue'
import { useCountryList } from '../composables/useCountryList'

const store = useBessStore()
const emit = defineEmits(['select', 'workflow-complete'])

const { filterCountries } = useCountryList()

// 国家 combobox 状态
const countryInput = ref('')
const countryDropdown = ref(false)
const filteredCountries = computed(() => {
  return filterCountries(countryInput.value)
})
function onCountryInput() {
  form.country = countryInput.value
  markEdited('country')
  countryDropdown.value = true
}
function onCountryBlur() {
  setTimeout(() => {
    countryDropdown.value = false
  }, 150)
}
function selectCountry(c) {
  form.country = c
  countryInput.value = c
  markEdited('country')
  countryDropdown.value = false
}

const form = reactive({
  ratedEnergy: store.survey.ratedEnergy || 100,
  totalPower: store.survey.totalPower || 50,
  duration: store.survey.duration || 2,
  temperature: store.survey.temperature || 25,
  cyclesPerDay: store.survey.cyclesPerDay || 1,
  dod: store.survey.dod || 90,
  requiredEnergy: store.survey.requiredEnergy || 240,
  country: store.survey.country || '',
  city: store.survey.city || '',
  site: store.survey.site || '',
  lat: store.survey.lat || null,
  lng: store.survey.lng || null,
  strategy: 'economic',
  targetMetric: 'lcos'
})

// 跟踪哪些字段被用户手动修改过
const userEdited = reactive({})

// 监听 store.survey 变化，仅在用户未手动修改时更新 form
watch(
  () => ({
    ratedEnergy: store.survey.ratedEnergy,
    totalPower: store.survey.totalPower,
    duration: store.survey.duration,
    temperature: store.survey.temperature,
    cyclesPerDay: store.survey.cyclesPerDay,
    dod: store.survey.dod,
    requiredEnergy: store.survey.requiredEnergy,
    country: store.survey.country,
    city: store.survey.city,
    site: store.survey.site,
    lat: store.survey.lat,
    lng: store.survey.lng
  }),
  (vals) => {
    if (!userEdited.ratedEnergy && vals.ratedEnergy) form.ratedEnergy = vals.ratedEnergy
    if (!userEdited.totalPower && vals.totalPower) form.totalPower = vals.totalPower
    if (!userEdited.duration && vals.duration) form.duration = vals.duration
    if (!userEdited.temperature && vals.temperature != null) form.temperature = vals.temperature
    if (!userEdited.cyclesPerDay && vals.cyclesPerDay) form.cyclesPerDay = vals.cyclesPerDay
    if (!userEdited.dod && vals.dod != null) form.dod = vals.dod
    if (!userEdited.requiredEnergy && vals.requiredEnergy) form.requiredEnergy = vals.requiredEnergy
    if (!userEdited.country && vals.country) form.country = vals.country
    if (!userEdited.city && vals.city) form.city = vals.city
    if (!userEdited.site && vals.site) form.site = vals.site
    if (!userEdited.lat && vals.lat != null) form.lat = vals.lat
    if (!userEdited.lng && vals.lng != null) form.lng = vals.lng
  },
  { immediate: true }
)

// 标记字段被用户手动修改
function markEdited(field) {
  userEdited[field] = true
}

const formLocation = computed(() => {
  const parts = [form.country, form.city, form.site].filter(Boolean)
  return parts.join(', ')
})

// 储能时长自动计算
const isDurationAuto = ref(true)

function autoCalcDuration() {
  if (form.ratedEnergy > 0 && form.totalPower > 0) {
    form.duration = +(form.ratedEnergy / form.totalPower).toFixed(2)
  }
}

function unlockAndCalcDuration() {
  isDurationAuto.value = true
  autoCalcDuration()
}

// 监听功率和容量变化，自动计算时长
watch(
  () => [form.ratedEnergy, form.totalPower],
  () => {
    if (isDurationAuto.value) {
      autoCalcDuration()
    }
  }
)

// 初始化时计算一次
autoCalcDuration()

// 所需能量自动计算
const isReqEnergyAuto = ref(true)

function autoCalcReqEnergy() {
  if (form.ratedEnergy > 0 && form.dod > 0) {
    form.requiredEnergy = +(form.ratedEnergy * (form.dod / 100)).toFixed(2)
  }
}

function unlockAndCalcReqEnergy() {
  isReqEnergyAuto.value = true
  autoCalcReqEnergy()
}

// 监听额定能量和DOD变化，自动计算所需能量
watch(
  () => [form.ratedEnergy, form.dod],
  () => {
    if (isReqEnergyAuto.value) {
      autoCalcReqEnergy()
    }
  }
)

// 初始化时计算一次
autoCalcReqEnergy()

// 国家输入框同步
watch(
  () => form.country,
  (val) => {
    if (val && val !== countryInput.value) countryInput.value = val
  }
)

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
  if (key === 'projectIrr' || key === 'equityIrr' || key === 'irr' || key === 'roi') return Number(val).toFixed(2) + '%'
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
      survey_params: { ...form, location: formLocation.value },
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
      survey_params: { ...form, location: formLocation.value },
      strategy: form.strategy,
      target_metric: form.targetMetric
    })
    if (resp.success) {
      workflowResult.value = resp.data
      solutions.value = (resp.data.solutions || []).map((s) => s.design).filter(Boolean)
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
  to {
    transform: rotate(360deg);
  }
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
  transition:
    box-shadow 0.2s,
    transform 0.2s;
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

.rank-1 {
  background: var(--color-warning);
}
.rank-2 {
  background: var(--color-text-secondary);
}
.rank-3 {
  background: var(--color-text-muted);
}
.rank-4,
.rank-5 {
  background: var(--color-border-light);
}

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

/* 储能时长自动计算样式 */
.auto-badge {
  display: inline-block;
  font-size: 0.65rem;
  font-weight: 600;
  padding: 1px 6px;
  border-radius: 3px;
  background: #e8f5e9;
  color: #2e7d32;
  margin-left: 6px;
  vertical-align: middle;
}

.duration-input-row {
  display: flex;
  align-items: center;
  gap: 4px;
}

.duration-input-row .form-input {
  flex: 1;
}

.duration-input-row .form-input.auto-disabled {
  background: var(--color-bg, #f5f5f5);
  color: var(--text-secondary, #888);
  cursor: not-allowed;
}

.unlock-btn,
.lock-btn {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  border: 1px solid var(--color-border, #ddd);
  border-radius: 4px;
  background: var(--card-bg, #fff);
  cursor: pointer;
  font-size: 13px;
  line-height: 1;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}

.unlock-btn:hover,
.lock-btn:hover {
  border-color: var(--color-accent, #409eff);
  background: var(--color-accent-light, #ecf5ff);
}

/* Combobox 下拉面板 */
.combobox-wrapper {
  position: relative;
}
.combobox-wrapper .form-input {
  width: 100%;
}
.combobox-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 100;
  max-height: 220px;
  overflow-y: auto;
  overflow-x: hidden;
  background: var(--color-card);
  backdrop-filter: var(--backdrop-filter, blur(12px));
  -webkit-backdrop-filter: var(--backdrop-filter, blur(12px));
  border: 1px solid var(--color-border);
  border-radius: 6px;
  margin-top: 2px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}
.combobox-option {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  cursor: pointer;
  transition: background 0.15s ease;
  border-bottom: 1px solid var(--color-border-light);
}
.combobox-option:last-child {
  border-bottom: none;
}
.combobox-option:hover,
.combobox-option.active {
  background: var(--color-accent);
  color: #fff;
}
.combobox-option:hover .option-name,
.combobox-option.active .option-name {
  color: #fff;
}
.option-name {
  flex: 1;
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-align: left;
}
</style>
