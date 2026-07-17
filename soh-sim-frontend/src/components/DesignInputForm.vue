<template>
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
          @input="$emit('field-edited', 'ratedEnergy')"
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
          @input="$emit('field-edited', 'totalPower')"
        />
      </div>
      <div class="form-group">
        <label>
          {{ $t('design.duration') }} (h)
          <span v-if="isDurationAuto" class="auto-badge">{{ $t('design.auto') }}</span>
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
            @input="$emit('field-edited', 'duration')"
          />
          <button
            v-if="isDurationAuto"
            class="unlock-btn"
            :title="$t('design.unlockDuration')"
            @click="$emit('unlock-duration')"
          >
            🔓
          </button>
          <button v-else class="lock-btn" :title="$t('design.lockDuration')" @click="$emit('lock-duration')">🔒</button>
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
          @input="$emit('field-edited', 'temperature')"
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
          @input="$emit('field-edited', 'cyclesPerDay')"
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
          @input="$emit('field-edited', 'dod')"
        />
      </div>
      <div class="form-group">
        <label>
          {{ $t('design.requiredEnergy') }} (MWh/天)
          <span v-if="isReqEnergyAuto" class="auto-badge">{{ $t('design.auto') }}</span>
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
            @input="$emit('field-edited', 'requiredEnergy')"
          />
          <button
            v-if="isReqEnergyAuto"
            class="unlock-btn"
            :title="$t('design.unlockRequiredEnergy')"
            @click="$emit('unlock-req-energy')"
          >
            🔓
          </button>
          <button v-else class="lock-btn" :title="$t('design.lockRequiredEnergy')" @click="$emit('lock-req-energy')">
            🔒
          </button>
        </div>
      </div>
      <div class="form-group">
        <label>{{ $t('design.country') }}</label>
        <ComboboxInput
          v-model="countryInput"
          :options="countryOptions"
          :placeholder="$t('design.country')"
          :empty-text="$t('common.noMatch')"
          @select="onCountrySelect"
        />
      </div>
      <div class="form-group">
        <label>{{ $t('design.city') }}</label>
        <input
          v-model="form.city"
          type="text"
          class="form-input"
          :placeholder="$t('design.city')"
          @input="$emit('field-edited', 'city')"
        />
      </div>
      <div class="form-group">
        <label>{{ $t('design.site') }}</label>
        <input
          v-model="form.site"
          type="text"
          class="form-input"
          :placeholder="$t('design.site')"
          @input="$emit('field-edited', 'site')"
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
          @input="$emit('field-edited', 'lat')"
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
          @input="$emit('field-edited', 'lng')"
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
      <button class="btn btn-primary" :disabled="loading" @click="$emit('run-design')">
        <span v-if="loading" class="spinner" />
        {{ loading ? $t('design.generating') : $t('design.generateBtn') }}
      </button>
      <button class="btn btn-secondary" :disabled="loading" @click="$emit('run-workflow')">
        <span v-if="workflowLoading" class="spinner" />
        {{ workflowLoading ? $t('design.running') : $t('design.oneClickBtn') }}
      </button>
    </div>
    <div v-if="error" class="error-message">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import AppIcon from './AppIcon.vue'
import ComboboxInput from './ComboboxInput.vue'
import { useCountryList } from '../composables/useCountryList'

const form = defineModel('form', { type: Object, required: true })

defineProps({
  isDurationAuto: { type: Boolean, default: true },
  isReqEnergyAuto: { type: Boolean, default: true },
  loading: { type: Boolean, default: false },
  workflowLoading: { type: Boolean, default: false },
  error: { type: String, default: null }
})

defineEmits([
  'field-edited',
  'unlock-duration',
  'lock-duration',
  'unlock-req-energy',
  'lock-req-energy',
  'run-design',
  'run-workflow'
])

const { filterCountries } = useCountryList()

const countryInput = ref(form.value.country || '')
const countryOptions = computed(() => filterCountries(countryInput.value).map((c) => ({ label: c, value: c })))

function onCountrySelect(opt) {
  form.value.country = opt.label
}

watch(
  () => form.value.country,
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
</script>
