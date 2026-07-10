<template>
  <div class="rounded-lg p-3 card-bordered">
    <h3 class="font-bold text-xs mb-2 flex items-center gap-2 text-default">
      <span
        class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold ins-1"
       
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
              class="text-[9px] px-1 py-0.5 rounded transition-colors ins-2"
             
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
        <span class="text-xs ins-3">&rarr;</span>
        <span class="text-xs font-bold ins-4">{{ result }} {{ targetCurrency }}</span>
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
              class="px-2 py-1 text-xs ins-5"
             
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
.ins-1 { background-color: rgba(239, 68, 68, 0.2); color: var(--color-danger) }
.ins-2 { background-color: var(--color-accent); color: white }
.ins-3 { color: var(--color-text-muted) }
.ins-4 { color: var(--color-accent) }
.ins-5 { 
                background-color: var(--color-input-bg-dark);
                border: 1px solid var(--color-input-border);
                color: var(--color-text-secondary);
               }

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
