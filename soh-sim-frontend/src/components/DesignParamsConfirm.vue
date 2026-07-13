<template>
  <div class="design-params-confirm">
    <h3 class="dpc-title">{{ $t('designTemplate.paramsTitle') }}</h3>
    <p class="dpc-desc">{{ $t('designTemplate.paramsDesc') }}</p>

    <div class="dpc-form">
      <div class="dpc-row">
        <div class="dpc-field">
          <label>{{ $t('designTemplate.fieldTotalPower') }} (MW)</label>
          <input v-model.number="form.totalPower" type="number" step="0.1" min="1" />
        </div>
        <div class="dpc-field">
          <label>{{ $t('designTemplate.fieldRatedEnergy') }} (MWh)</label>
          <input v-model.number="form.ratedEnergy" type="number" step="1" min="1" />
        </div>
        <div class="dpc-field">
          <label>{{ $t('designTemplate.fieldDuration') }} (h)</label>
          <input v-model.number="form.duration" type="number" step="0.5" min="0.5" />
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
import { reactive, ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useBessStore } from '../stores/bess.js'
import api from '../services/api.js'

const { t } = useI18n()
const store = useBessStore()

const emit = defineEmits(['back', 'result'])

const form = reactive({
  totalPower: 50,
  ratedEnergy: 100,
  duration: 2,
  temperature: 25,
  cyclesPerDay: 1,
  dod: 80,
  strategy: 'balanced',
  manufacturer: '',
})

const generating = ref(false)
const error = ref('')

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
      manufacturer: form.manufacturer || undefined,
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
  to { transform: rotate(360deg); }
}

.dpc-error {
  margin-top: 0.75rem;
  padding: 0.625rem 0.75rem;
  background: var(--color-danger-glow-soft, rgba(239, 68, 68, 0.1));
  color: var(--color-danger);
  border-radius: 6px;
  font-size: 0.8125rem;
}
</style>
