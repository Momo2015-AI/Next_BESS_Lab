<template>
  <div class="rounded-lg p-3 card-bordered">
    <h3 class="font-bold text-xs mb-2 flex items-center gap-2 text-default">
      <span
        class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold"
        style="background-color: rgba(239, 68, 68, 0.2); color: var(--color-danger)"
      >
        VI
      </span>
      {{ $t('financial.sectionCurrencyConverter') }}
    </h3>

    <div class="space-y-2 text-[10px] text-secondary">
      <div class="grid grid-cols-2 gap-2">
        <div>
          <label class="block mb-0.5 text-muted">{{ $t('financial.labelBaseCurrency') }}</label>
          <select
            v-model="baseCurrency"
            class="w-full rounded px-2 py-1 text-xs form-field-select"
            @change="updateRates"
          >
            <option v-for="code in Object.keys(supportedCurrencies)" :key="code" :value="code">
              {{ code }} - {{ $t(supportedCurrencies[code]) }}
            </option>
          </select>
        </div>
        <div>
          <label class="block mb-0.5 text-muted">{{ $t('financial.labelTargetCurrency') }}</label>
          <select
            v-model="targetCurrency"
            class="w-full rounded px-2 py-1 text-xs form-field-select"
            @change="updateRates"
          >
            <option v-for="code in Object.keys(supportedCurrencies)" :key="code" :value="code">
              {{ code }} - {{ $t(supportedCurrencies[code]) }}
            </option>
          </select>
        </div>
      </div>

      <div class="grid grid-cols-3 gap-2">
        <div>
          <label class="block mb-0.5 text-muted">{{ $t('financial.labelAmount') }}</label>
          <input
            v-model.number="amount"
            type="number"
            step="0.01"
            class="w-full rounded px-2 py-1 text-xs form-field-input"
            @input="convert"
          />
        </div>
        <div>
          <label class="block mb-0.5 text-muted">
            {{ $t('financial.labelRate') }}
            <span v-if="isManualRate" class="text-[8px] text-warning">({{ $t('financial.rateManual') }})</span>
          </label>
          <div class="flex items-center gap-1">
            <input
              v-model.number="manualRate"
              type="number"
              step="0.0001"
              class="flex-1 rounded px-2 py-1 text-xs font-mono form-field-input"
              :style="isManualRate ? { borderColor: 'var(--color-warning)' } : {}"
              @input="onManualRateChange"
            />
            <button
              v-if="isManualRate"
              class="text-[9px] px-1 py-0.5 rounded transition-colors"
              style="background-color: var(--color-accent); color: white"
              @click="resetToApiRate"
            >
              {{ $t('financial.btnReset') }}
            </button>
          </div>
        </div>
        <div class="flex flex-col justify-end">
          <div class="text-[9px] text-muted flex justify-between">
            <span>{{ $t('financial.labelApiRate') }}</span>
            <span class="font-mono">{{ apiRate ? apiRate.toFixed(4) : '---' }}</span>
          </div>
          <div class="text-[9px] text-muted flex justify-between">
            <span>{{ $t('financial.labelEffectiveRate') }}</span>
            <span
              class="font-mono font-bold"
              :style="{ color: isManualRate ? 'var(--color-warning)' : 'var(--color-text-secondary)' }"
            >
              {{ effectiveRate ? effectiveRate.toFixed(4) : '---' }}
            </span>
          </div>
        </div>
      </div>

      <div class="flex justify-between items-center p-2 rounded bg-input-dark">
        <span class="text-xs">{{ amount }} {{ baseCurrency }}</span>
        <span class="text-xs" style="color: var(--color-text-muted)">&rarr;</span>
        <span class="text-xs font-bold" style="color: var(--color-accent)">{{ result }} {{ targetCurrency }}</span>
      </div>

      <div class="border-t pt-2 mt-2">
        <div class="flex justify-between items-center mb-1">
          <span class="text-xs text-muted">{{ $t('financial.labelProjectCurrency') }}</span>
          <div class="flex gap-1">
            <button class="text-[9px] px-2 py-1 rounded transition-colors bg-accent text-white" @click="refreshRates">
              {{ $t('financial.btnRefresh') }}
            </button>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-2">
          <div>
            <label class="block mb-0.5 text-muted">{{ $t('financial.labelDisplayCurrency') }}</label>
            <select
              v-model="displayCurrency"
              class="w-full rounded px-2 py-1 text-xs form-field-select"
              @change="updateDisplayCurrency"
            >
              <option v-for="code in Object.keys(supportedCurrencies)" :key="code" :value="code">
                {{ code }} - {{ $t(supportedCurrencies[code]) }}
              </option>
            </select>
          </div>
          <div>
            <label class="block mb-0.5 text-muted">{{ $t('financial.labelRateSource') }}</label>
            <div
              class="px-2 py-1 text-xs"
              style="
                background-color: var(--color-input-bg-dark);
                border: 1px solid var(--color-input-border);
                color: var(--color-text-secondary);
              "
            >
              {{ rateSource || '---' }}
            </div>
          </div>
        </div>
      </div>

      <div class="text-[9px] space-y-1 text-muted">
        <div class="flex justify-between">
          <span>{{ $t('financial.labelLastUpdated') }}</span>
          <span>{{ lastUpdated || '---' }}</span>
        </div>
        <div class="flex justify-between">
          <span>{{ $t('financial.labelStatus') }}</span>
          <span :style="{ color: rateStatus === 'online' ? 'var(--color-success)' : 'var(--color-warning)' }">
            {{ rateStatus === 'online' ? $t('financial.statusOnline') : $t('financial.statusCached') }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import api from '../services/api.js'

const supportedCurrencies = reactive({
<<<<<<< HEAD
  USD: 'currency.USD',
  CNY: 'currency.CNY',
  EUR: 'currency.EUR',
  GBP: 'currency.GBP',
  AED: 'currency.AED',
  SAR: 'currency.SAR',
  QAR: 'currency.QAR',
  KWD: 'currency.KWD',
  OMR: 'currency.OMR',
  BHD: 'currency.BHD',
  JPY: 'currency.JPY',
  KRW: 'currency.KRW',
  AUD: 'currency.AUD',
  INR: 'currency.INR',
  TND: 'currency.TND',
  EGP: 'currency.EGP'
=======
  USD: '\u7f8e\u5143',
  CNY: '\u4eba\u6c11\u5e01',
  EUR: '\u6b27\u5143',
  GBP: '\u82f1\u9551',
  AED: '\u8fea\u62c9\u59c6(\u963f\u8054\u914b)',
  SAR: '\u91cc\u4e9a\u5c14(\u6c99\u7279)',
  QAR: '\u91cc\u4e9a\u5c14(\u5361\u5854\u5c14)',
  KWD: '\u7b2c\u7eb3\u5c14(\u79d1\u5a01\u7279)',
  OMR: '\u91cc\u4e9a\u5c14(\u963f\u66fc)',
  BHD: '\u7b2c\u7eb3\u5c14(\u5df4\u6797)',
  JPY: '\u65e5\u5143',
  KRW: '\u97e9\u5143',
  AUD: '\u6fb3\u5143',
  INR: '\u5362\u6bd4(\u5370\u5ea6)',
  TND: '\u7b2c\u7eb3\u5c14(\u7a81\u5c3c\u65af)',
  EGP: '\u78c5(\u57c3\u53ca)'
>>>>>>> origin/fix0702
})

const baseCurrency = ref('USD')
const targetCurrency = ref('CNY')
const amount = ref(100)
const apiRate = ref(null)
const manualRate = ref(null)
const isManualRate = ref(false)
const result = ref(0)
const rateSource = ref('')
const lastUpdated = ref('')
const rateStatus = ref('cached')

const displayCurrency = ref('CNY')

let rateIntervalId = null

const effectiveRate = computed(() => {
  if (isManualRate.value && manualRate.value != null) return manualRate.value
  return apiRate.value
})

const loadPreferences = () => {
  try {
    const prefs = localStorage.getItem('currencyPreferences')
    if (prefs) {
      const parsed = JSON.parse(prefs)
      baseCurrency.value = parsed.baseCurrency || 'USD'
      targetCurrency.value = parsed.targetCurrency || 'CNY'
      displayCurrency.value = parsed.displayCurrency || 'CNY'
      if (parsed.manualRate != null) {
        manualRate.value = parsed.manualRate
        isManualRate.value = parsed.isManualRate || false
      }
    }
  } catch (e) {
    console.warn('Failed to load currency preferences:', e)
  }
}

const savePreferences = () => {
  try {
    const prefs = {
      baseCurrency: baseCurrency.value,
      targetCurrency: targetCurrency.value,
      displayCurrency: displayCurrency.value,
      manualRate: manualRate.value,
      isManualRate: isManualRate.value
    }
    localStorage.setItem('currencyPreferences', JSON.stringify(prefs))
  } catch (e) {
    console.warn('Failed to save currency preferences:', e)
  }
}

const fetchRate = async () => {
  try {
    const resp = await api.get(`/api/exchange-rates/latest?currency=${targetCurrency.value}`)

    if (resp.success) {
      const d = resp.data
      apiRate.value = d.rate
      rateSource.value = d.source
      lastUpdated.value = d.date
      rateStatus.value = resp.cached ? 'cached' : 'online'
      if (!isManualRate.value) {
        manualRate.value = d.rate
      }
      convert()
    }
  } catch (e) {
    console.error('Error fetching exchange rate:', e)
  }
}

const convert = () => {
  const r = effectiveRate.value
  if (r && amount.value) {
    result.value = (amount.value * r).toFixed(2)
  } else {
    result.value = '0.00'
  }
}

const onManualRateChange = () => {
  isManualRate.value = true
  savePreferences()
  convert()
}

const resetToApiRate = () => {
  isManualRate.value = false
  manualRate.value = apiRate.value
  savePreferences()
  convert()
}

const refreshRates = async () => {
  try {
    const data = await api.post('/api/exchange-rates/refresh')
    if (data.success) {
      await fetchRate()
    }
  } catch (e) {
    console.error('Error refreshing rates:', e)
  }
}

const updateRates = () => {
  savePreferences()
  fetchRate()
}

const updateDisplayCurrency = () => {
  savePreferences()
}

onMounted(() => {
  loadPreferences()
  fetchRate()
  rateIntervalId = setInterval(
    () => {
      fetchRate()
    },
    5 * 60 * 1000
  )
})

onUnmounted(() => {
  if (rateIntervalId) {
    clearInterval(rateIntervalId)
    rateIntervalId = null
  }
})

watch([baseCurrency, targetCurrency], updateRates)
</script>

<style scoped>
input:focus,
select:focus,
textarea:focus {
  border-color: var(--color-input-focus);
  outline: none;
}

button:not(:disabled):hover {
  opacity: 0.9;
}
</style>
