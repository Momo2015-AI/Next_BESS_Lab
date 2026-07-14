<template>
  <div class="rules-config">
    <!-- Grid Code Rules -->
    <SectionCard :title="t('tools.rules.gridCode')">
      <div class="rules-grid">
        <div v-for="rule in gridCodeRules" :key="rule.key" class="rule-item">
          <label class="rule-label">{{ t(rule.labelKey) }}</label>
          <div class="rule-input-group">
            <input
              v-model.number="form[rule.key]"
              type="number"
              class="rule-input"
              :min="rule.min"
              :max="rule.max"
              :step="rule.step"
            />
            <span class="rule-unit">{{ rule.unit }}</span>
          </div>
          <p class="rule-desc">{{ t(rule.descKey) }}</p>
        </div>
      </div>
    </SectionCard>

    <!-- Battery Constraints -->
    <SectionCard :title="t('tools.rules.batteryConstraints')">
      <div class="rules-grid">
        <div v-for="rule in batteryRules" :key="rule.key" class="rule-item">
          <label class="rule-label">{{ t(rule.labelKey) }}</label>
          <div class="rule-input-group">
            <input
              v-model.number="form[rule.key]"
              type="number"
              class="rule-input"
              :min="rule.min"
              :max="rule.max"
              :step="rule.step"
            />
            <span class="rule-unit">{{ rule.unit }}</span>
          </div>
          <p class="rule-desc">{{ t(rule.descKey) }}</p>
        </div>
      </div>
    </SectionCard>

    <!-- Financial Rules -->
    <SectionCard :title="t('tools.rules.financialRules')">
      <div class="rules-grid">
        <div v-for="rule in financialRules" :key="rule.key" class="rule-item">
          <label class="rule-label">{{ t(rule.labelKey) }}</label>
          <div class="rule-input-group">
            <input
              v-model.number="form[rule.key]"
              type="number"
              class="rule-input"
              :min="rule.min"
              :max="rule.max"
              :step="rule.step"
            />
            <span class="rule-unit">{{ rule.unit }}</span>
          </div>
          <p class="rule-desc">{{ t(rule.descKey) }}</p>
        </div>
      </div>
    </SectionCard>

    <!-- Action Buttons -->
    <div class="rules-actions">
      <button class="btn-reset" @click="resetDefaults">{{ t('tools.rules.resetDefaults') }}</button>
      <button class="btn-save" @click="saveRules">{{ t('tools.rules.saveRules') }}</button>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import SectionCard from './SectionCard.vue'

const { t } = useI18n()

const STORAGE_KEY = 'soh-sim-rules-config'

const defaults = {
  freqDeviationMax: 0.5,
  voltageDeviationMax: 5,
  responseTimeMax: 100,
  rampRateMin: 10,
  maxContainersPerString: 4,
  minSocOperating: 10,
  maxSocOperating: 90,
  maxDodDaily: 80,
  minIrrThreshold: 6,
  maxPaybackYears: 12,
  discountRateDefault: 7,
  inflationRateDefault: 2
}

function loadFromStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) {
      const parsed = JSON.parse(raw)
      return { ...defaults, ...parsed }
    }
  } catch {
    // ignore parse errors, fall back to defaults
  }
  return { ...defaults }
}

const form = reactive(loadFromStorage())

const gridCodeRules = [
  {
    key: 'freqDeviationMax',
    labelKey: 'tools.rules.freqDeviationMax',
    descKey: 'tools.rules.freqDeviationMaxDesc',
    min: 0.01,
    max: 10,
    step: 0.01,
    unit: 'Hz'
  },
  {
    key: 'voltageDeviationMax',
    labelKey: 'tools.rules.voltageDeviationMax',
    descKey: 'tools.rules.voltageDeviationMaxDesc',
    min: 0.1,
    max: 30,
    step: 0.1,
    unit: '%'
  },
  {
    key: 'responseTimeMax',
    labelKey: 'tools.rules.responseTimeMax',
    descKey: 'tools.rules.responseTimeMaxDesc',
    min: 1,
    max: 10000,
    step: 1,
    unit: 'ms'
  },
  {
    key: 'rampRateMin',
    labelKey: 'tools.rules.rampRateMin',
    descKey: 'tools.rules.rampRateMinDesc',
    min: 0.1,
    max: 100,
    step: 0.1,
    unit: '%/min'
  }
]

const batteryRules = computed(() => [
  {
    key: 'maxContainersPerString',
    labelKey: 'tools.rules.maxContainersPerString',
    descKey: 'tools.rules.maxContainersPerStringDesc',
    min: 1,
    max: 50,
    step: 1,
    unit: t('tools.rules.units')
  },
  {
    key: 'minSocOperating',
    labelKey: 'tools.rules.minSocOperating',
    descKey: 'tools.rules.minSocOperatingDesc',
    min: 0,
    max: 50,
    step: 0.1,
    unit: '%'
  },
  {
    key: 'maxSocOperating',
    labelKey: 'tools.rules.maxSocOperating',
    descKey: 'tools.rules.maxSocOperatingDesc',
    min: 50,
    max: 100,
    step: 0.1,
    unit: '%'
  },
  {
    key: 'maxDodDaily',
    labelKey: 'tools.rules.maxDodDaily',
    descKey: 'tools.rules.maxDodDailyDesc',
    min: 10,
    max: 100,
    step: 0.1,
    unit: '%'
  }
])

const financialRules = computed(() => [
  {
    key: 'minIrrThreshold',
    labelKey: 'tools.rules.minIrrThreshold',
    descKey: 'tools.rules.minIrrThresholdDesc',
    min: 0,
    max: 50,
    step: 0.1,
    unit: '%'
  },
  {
    key: 'maxPaybackYears',
    labelKey: 'tools.rules.maxPaybackYears',
    descKey: 'tools.rules.maxPaybackYearsDesc',
    min: 1,
    max: 30,
    step: 0.1,
    unit: t('tools.rules.years')
  },
  {
    key: 'discountRateDefault',
    labelKey: 'tools.rules.discountRateDefault',
    descKey: 'tools.rules.discountRateDefaultDesc',
    min: 0,
    max: 30,
    step: 0.1,
    unit: '%'
  },
  {
    key: 'inflationRateDefault',
    labelKey: 'tools.rules.inflationRateDefault',
    descKey: 'tools.rules.inflationRateDefaultDesc',
    min: 0,
    max: 20,
    step: 0.1,
    unit: '%'
  }
])

function resetDefaults() {
  Object.assign(form, defaults)
}

function saveRules() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ ...form }))
    alert(t('tools.rules.saved'))
  } catch {
    // ignore storage errors
  }
}
</script>

<style scoped>
.rules-config {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.rules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.rule-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 12px;
  background: var(--color-card-dark);
  border: 1px solid var(--color-border);
  border-radius: 8px;
}

.rule-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text);
}

.rule-input-group {
  display: flex;
  align-items: center;
  gap: 6px;
}

.rule-input {
  width: 100px;
  padding: 6px 8px;
  border: 1px solid var(--color-input-border);
  border-radius: 6px;
  background: var(--color-input-bg-dark);
  color: var(--color-text);
  font-size: 14px;
  font-weight: 600;
  text-align: right;
}

.rule-input:focus-visible {
  outline: none;
  border-color: var(--color-accent);
}

.rule-unit {
  font-size: 12px;
  color: var(--color-text-muted);
  min-width: 40px;
}

.rule-desc {
  font-size: 11px;
  color: var(--color-text-muted);
  margin: 0;
}

.rules-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding-top: 8px;
}

.btn-reset {
  padding: 8px 20px;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-card);
  color: var(--color-text-secondary);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-reset:hover {
  background: var(--color-card-dark);
  color: var(--color-text);
}

.btn-save {
  padding: 8px 20px;
  border: none;
  border-radius: 6px;
  background: var(--color-accent);
  color: white;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.2s ease;
}

.btn-save:hover {
  opacity: 0.9;
}
</style>
