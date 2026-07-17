<template>
  <div class="design-engine-panel">
    <DesignInputForm
      v-model:form="form"
      :is-duration-auto="isDurationAuto"
      :is-req-energy-auto="isReqEnergyAuto"
      :loading="loading"
      :workflow-loading="workflowLoading"
      :error="error"
      @field-edited="markEdited"
      @unlock-duration="isDurationAuto = false"
      @lock-duration="unlockAndCalcDuration"
      @unlock-req-energy="isReqEnergyAuto = false"
      @lock-req-energy="unlockAndCalcReqEnergy"
      @run-design="runDesign"
      @run-workflow="runFullWorkflow"
    />

    <DesignSolutionsList :solutions="solutions" @select="(sol) => $emit('select', sol)" />

    <DesignWorkflowResult :result="workflowResult" />
  </div>
</template>

<script setup>
import { ref, reactive, watch, computed } from 'vue'
import { post } from '../services/api.js'
import { useBessStore } from '../stores/bess.js'
import DesignInputForm from './DesignInputForm.vue'
import DesignSolutionsList from './DesignSolutionsList.vue'
import DesignWorkflowResult from './DesignWorkflowResult.vue'

const store = useBessStore()
const emit = defineEmits(['select', 'workflow-complete'])

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

const userEdited = reactive({})
function markEdited(field) {
  userEdited[field] = true
}

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

const formLocation = computed(() => {
  const parts = [form.country, form.city, form.site].filter(Boolean)
  return parts.join(', ')
})

// Auto-calc duration
const isDurationAuto = ref(true)
function autoCalcDuration() {
  if (
    form.ratedEnergy > 0 &&
    form.totalPower > 0 &&
    typeof form.ratedEnergy === 'number' &&
    typeof form.totalPower === 'number'
  ) {
    form.duration = +(form.ratedEnergy / form.totalPower).toFixed(2)
  }
}
function unlockAndCalcDuration() {
  isDurationAuto.value = true
  autoCalcDuration()
}
watch(
  () => [form.ratedEnergy, form.totalPower],
  () => {
    if (isDurationAuto.value) autoCalcDuration()
  }
)
autoCalcDuration()

// Auto-calc required energy
const isReqEnergyAuto = ref(true)
function autoCalcReqEnergy() {
  if (form.ratedEnergy > 0 && form.dod > 0 && typeof form.ratedEnergy === 'number' && typeof form.dod === 'number') {
    form.requiredEnergy = +(form.ratedEnergy * (form.dod / 100)).toFixed(2)
  }
}
function unlockAndCalcReqEnergy() {
  isReqEnergyAuto.value = true
  autoCalcReqEnergy()
}
watch(
  () => [form.ratedEnergy, form.dod],
  () => {
    if (isReqEnergyAuto.value) autoCalcReqEnergy()
  }
)
autoCalcReqEnergy()

const loading = ref(false)
const workflowLoading = ref(false)
const error = ref(null)
const solutions = ref([])
const workflowResult = ref(null)

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
      if (resp.data.solutions?.length > 0) emit('select', resp.data.solutions[0])
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
      if (resp.data.recommendation) emit('select', resp.data.recommendation.design)
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
</style>
