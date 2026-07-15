<template>
  <div class="design-params-confirm">
    <h3 class="dpc-title">{{ $t('designTemplate.paramsTitle') }}</h3>
    <p class="dpc-desc">{{ $t('designTemplate.paramsDesc') }}</p>

    <div v-if="!surveyCompleted" class="dpc-survey-warn">
      <span>{{ $t('designTemplate.surveyNotCompleted') }}</span>
      <button class="dpc-survey-link" @click="goToSurvey">{{ $t('designTemplate.goToSurvey') }}</button>
    </div>

    <div class="dpc-form">
      <div class="dpc-row">
        <div class="dpc-field">
          <label>
            {{ $t('designTemplate.fieldTotalPower') }} (MW)
            <span v-if="surveyCompleted" class="dpc-source-badge">{{ $t('designTemplate.fromSurvey') }}</span>
          </label>
          <input v-model.number="form.totalPower" type="number" step="0.1" min="1" />
        </div>
        <div class="dpc-field">
          <label>
            {{ $t('designTemplate.fieldRatedEnergy') }} (MWh)
            <span v-if="surveyCompleted" class="dpc-source-badge">{{ $t('designTemplate.fromSurvey') }}</span>
          </label>
          <input v-model.number="form.ratedEnergy" type="number" step="1" min="1" />
        </div>
        <div class="dpc-field">
          <label>
            {{ $t('designTemplate.fieldDuration') }} (h)
            <span v-if="isDurationAuto" class="auto-badge">{{ $t('design.auto') }}</span>
          </label>
          <div class="duration-input-row">
            <input
              v-model.number="form.duration"
              type="number"
              step="0.5"
              min="0.5"
              :class="{ 'auto-disabled': isDurationAuto }"
              :disabled="isDurationAuto"
            />
            <button
              v-if="isDurationAuto"
              class="lock-btn"
              :title="$t('design.unlockDuration')"
              @click="isDurationAuto = false"
            >
              🔒
            </button>
            <button v-else class="lock-btn unlocked" :title="$t('design.lockDuration')" @click="unlockAndCalcDuration">
              🔓
            </button>
          </div>
        </div>
      </div>
      <div class="dpc-row">
        <div class="dpc-field">
          <label>{{ $t('designTemplate.fieldTemperature') }} (°C)</label>
          <input v-model.number="form.temperature" type="number" step="1" min="-20" max="60" />
        </div>
        <div class="dpc-field">
          <label>{{ $t('designTemplate.fieldCyclesPerDay') }}</label>
          <input v-model.number="form.cyclesPerDay" type="number" step="0.1" min="0" />
        </div>
        <div class="dpc-field">
          <label>{{ $t('designTemplate.fieldDod') }} (%)</label>
          <input v-model.number="form.dod" type="number" step="1" min="10" max="100" />
        </div>
      </div>
      <div class="dpc-row">
        <div class="dpc-field">
          <label>{{ $t('designTemplate.fieldStrategy') }}</label>
          <select v-model="form.strategy">
            <option value="economic">{{ $t('designTemplate.strategyEconomic') }}</option>
            <option value="balanced">{{ $t('designTemplate.strategyBalanced') }}</option>
            <option value="flexible">{{ $t('designTemplate.strategyFlexible') }}</option>
            <option value="manufacturer">{{ $t('designTemplate.strategyManufacturer') }}</option>
          </select>
        </div>
        <div class="dpc-field">
          <label>{{ $t('designTemplate.fieldManufacturer') }}</label>
          <input v-model="form.manufacturer" type="text" :placeholder="$t('designTemplate.mfrPlaceholder')" />
        </div>
      </div>
    </div>

    <div class="dpc-actions">
      <button class="dpc-btn dpc-btn-secondary" @click="$emit('back')">
        {{ $t('designTemplate.back') }}
      </button>
      <button class="dpc-btn dpc-btn-primary" :disabled="generating" @click="runDesign">
        <span v-if="generating" class="dpc-spinner"></span>
        {{ generating ? $t('designTemplate.generating') : $t('designTemplate.generateDesign') }}
      </button>
    </div>

    <div v-if="error" class="dpc-error">{{ error }}</div>
  </div>
</template>

<script setup>
import { reactive, ref, watch, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useBessStore } from '../stores/bess.js'
import api from '../services/api.js'

const { t } = useI18n()
const router = useRouter()
const store = useBessStore()

const emit = defineEmits(['back', 'result'])

const form = reactive({
  totalPower: 50,
  ratedEnergy: 5,
  duration: 2,
  temperature: 25,
  cyclesPerDay: 1,
  dod: 90,
  strategy: 'balanced',
  manufacturer: ''
})

const generating = ref(false)
const error = ref('')

const surveyCompleted = computed(() => {
  return !!(store.survey?.projectName && store.survey?.ratedEnergy)
})

function goToSurvey() {
  router.push('/phase1')
}

onMounted(() => {
  // 从 survey store 预填
  const s = store.survey || {}
  if (s.totalPower) form.totalPower = Number(s.totalPower)
  if (s.ratedEnergy) form.ratedEnergy = Number(s.ratedEnergy)
  if (s.duration) form.duration = Number(s.duration)
  if (s.temperature != null) form.temperature = Number(s.temperature)
  if (s.cyclesPerDay != null) form.cyclesPerDay = Number(s.cyclesPerDay)
  if (s.dod != null) form.dod = Number(s.dod)
  if (store.systemParams?.strategy) form.strategy = store.systemParams.strategy
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

watch(
  () => [form.ratedEnergy, form.totalPower],
  () => {
    if (isDurationAuto.value) autoCalcDuration()
  }
)

async function runDesign() {
  generating.value = true
  error.value = ''

  try {
    const res = await api.post('/api/design/auto', {
      totalPower: form.totalPower,
      ratedEnergy: form.ratedEnergy,
      duration: form.duration,
      temperature: form.temperature,
      cyclesPerDay: form.cyclesPerDay,
      dod: form.dod,
      strategy: form.strategy,
      manufacturer: form.manufacturer || undefined
    })

    const data = res?.data || res
    // 保存到 store
    store.systemParams.strategy = form.strategy
    store.survey.totalPower = form.totalPower
    store.survey.ratedEnergy = form.ratedEnergy
    store.survey.duration = form.duration
    store.survey.temperature = form.temperature
    store.survey.cyclesPerDay = form.cyclesPerDay
    store.survey.dod = form.dod

    emit('result', data)
  } catch (e) {
    error.value = e?.message || t('designTemplate.generateFailed')
  } finally {
    generating.value = false
  }
}
</script>

<style scoped>
.design-params-confirm {
  padding: 1rem 0;
}

.dpc-title {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.dpc-desc {
  color: var(--color-text-secondary);
  font-size: 0.875rem;
  margin-bottom: 1.25rem;
}

.dpc-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.dpc-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
}

.dpc-field {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.dpc-field label {
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--color-text-secondary);
}

.dpc-field input,
.dpc-field select {
  padding: 0.5rem 0.625rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-card);
  color: var(--color-text);
  font-size: 0.875rem;
}

.dpc-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.dpc-btn {
  padding: 0.5rem 1.25rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: opacity 0.2s;
}

.dpc-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.dpc-btn-secondary {
  background: var(--color-bg-secondary, #f3f4f6);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

.dpc-btn-primary {
  background: var(--color-accent);
  color: var(--color-text-on-accent);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.dpc-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: dpc-spin 0.6s linear infinite;
}

@keyframes dpc-spin {
  to {
    transform: rotate(360deg);
  }
}

.dpc-error {
  margin-top: 0.75rem;
  padding: 0.625rem 0.75rem;
  background: var(--color-danger-glow-soft, rgba(239, 68, 68, 0.1));
  color: var(--color-danger);
  border-radius: 6px;
  font-size: 0.8125rem;
}

.auto-badge {
  font-size: 0.65rem;
  background: var(--color-accent);
  color: #fff;
  padding: 0 4px;
  border-radius: 3px;
  margin-left: 4px;
  vertical-align: middle;
}

.dpc-source-badge {
  font-size: 0.625rem;
  background: var(--color-success, #10b981);
  color: #fff;
  padding: 1px 5px;
  border-radius: 3px;
  margin-left: 4px;
  vertical-align: middle;
  font-weight: 400;
}

.dpc-survey-warn {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0.625rem 0.875rem;
  margin-bottom: 1rem;
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.3);
  border-radius: 6px;
  font-size: 0.8125rem;
  color: var(--color-text-secondary);
}

.dpc-survey-link {
  flex-shrink: 0;
  background: var(--color-accent);
  color: var(--color-text-on-accent);
  border: none;
  border-radius: 4px;
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.2s;
}

.dpc-survey-link:hover {
  opacity: 0.85;
}

.duration-input-row {
  display: flex;
  align-items: center;
  gap: 4px;
}

.duration-input-row input {
  flex: 1;
}

.duration-input-row input.auto-disabled {
  opacity: 0.6;
  background: var(--color-bg-muted, #f0f0f0);
}

.unlock-btn,
.lock-btn {
  background: none;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  cursor: pointer;
  padding: 2px 6px;
  font-size: 0.85rem;
  line-height: 1;
  transition: all 0.2s;
}

.unlock-btn:hover,
.lock-btn:hover {
  border-color: var(--color-accent);
  background: var(--color-accent-light, #e8f4fd);
}
</style>
