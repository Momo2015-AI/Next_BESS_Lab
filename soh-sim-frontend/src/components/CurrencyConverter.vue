<template>
  <div class="rounded-lg p-3" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
    <h3 class="font-bold text-xs mb-2 flex items-center gap-2" style="color: var(--color-text);">
      <span class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold" style="background-color: rgba(239, 68, 68, 0.2); color: var(--color-danger);">VI</span>
      货币转换 Currency Converter
    </h3>
    
    <div class="space-y-2 text-[10px]" style="color: var(--color-text-secondary);">
      <!-- 快速转换 -->
      <div class="grid grid-cols-2 gap-2">
        <div>
          <label class="block mb-0.5" style="color: var(--color-text-muted);">基础货币 Base</label>
          <select v-model="baseCurrency" class="w-full rounded px-2 py-1 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" @change="updateRates">
            <option v-for="code in Object.keys(supportedCurrencies)" :key="code" :value="code">{{ code }} - {{ supportedCurrencies[code] }}</option>
          </select>
        </div>
        <div>
          <label class="block mb-0.5" style="color: var(--color-text-muted);">目标货币 Target</label>
          <select v-model="targetCurrency" class="w-full rounded px-2 py-1 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" @change="updateRates">
            <option v-for="code in Object.keys(supportedCurrencies)" :key="code" :value="code">{{ code }} - {{ supportedCurrencies[code] }}</option>
          </select>
        </div>
      </div>
      
      <!-- 转换输入 -->
      <div class="grid grid-cols-3 gap-2">
        <div class="col-span-2">
          <label class="block mb-0.5" style="color: var(--color-text-muted);">金额 Amount</label>
          <input v-model.number="amount" type="number" step="0.01" class="w-full rounded px-2 py-1 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" @input="convert" />
        </div>
        <div>
          <label class="block mb-0.5" style="color: var(--color-text-muted);">汇率 Rate</label>
          <div class="px-2 py-1 text-xs font-mono" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text-secondary);">
            {{ rate ? rate.toFixed(6) : '---' }}
          </div>
        </div>
      </div>
      
      <!-- 转换结果 -->
      <div class="flex justify-between items-center p-2 rounded" style="background-color: var(--color-input-bg-dark);">
        <span style="color: var(--color-text-secondary);">{{ amount }} {{ baseCurrency }}</span>
        <span class="text-xs" style="color: var(--color-muted);">→</span>
        <span class="font-bold" style="color: var(--color-accent);">{{ result }} {{ targetCurrency }}</span>
      </div>
      
      <!-- 项目货币设置 -->
      <div class="border-t pt-2 mt-2">
        <div class="flex justify-between items-center mb-1">
          <span class="text-xs" style="color: var(--color-text-muted);">项目货币 Project Currency</span>
          <button @click="refreshRates" class="text-[9px] px-2 py-1 rounded transition-colors" style="background-color: var(--color-accent); color: white;" onmouseover="this.style.opacity='0.9';" onmouseout="this.style.opacity='1';">刷新 Refresh</button>
        </div>
        <div class="grid grid-cols-2 gap-2">
          <div>
            <label class="block mb-0.5" style="color: var(--color-text-muted);">显示货币 Display</label>
            <select v-model="displayCurrency" class="w-full rounded px-2 py-1 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" @change="updateDisplayCurrency">
              <option v-for="code in Object.keys(supportedCurrencies)" :key="code" :value="code">{{ code }} - {{ supportedCurrencies[code] }}</option>
            </select>
          </div>
          <div>
            <label class="block mb-0.5" style="color: var(--color-text-muted);">汇率来源 Source</label>
            <div class="px-2 py-1 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text-secondary);">
              {{ rateSource || '---' }}
            </div>
          </div>
        </div>
      </div>
      
      <!-- 汇率信息 -->
      <div class="text-[9px] space-y-1" style="color: var(--color-text-muted);">
        <div class="flex justify-between">
          <span>更新时间</span>
          <span>{{ lastUpdated || '---' }}</span>
        </div>
        <div class="flex justify-between">
          <span>状态</span>
          <span :style="rateStatus === 'online' ? { color: 'var(--color-success)' } : { color: 'var(--color-warning)' }">{{ rateStatus === 'online' ? '在线 Online' : '缓存 Cached' }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, watch } from 'vue'

// 支持的货币
const supportedCurrencies = reactive({
  'USD': '美元',
  'CNY': '人民币',
  'EUR': '欧元',
  'GBP': '英镑',
  'AED': '迪拉姆(阿联酋)',
  'SAR': '里亚尔(沙特)',
  'QAR': '里亚尔(卡塔尔)',
  'KWD': '第纳尔(科威特)',
  'OMR': '里亚尔(阿曼)',
  'BHD': '第纳尔(巴林)',
  'JPY': '日元',
  'KRW': '韩元',
  'AUD': '澳元',
  'INR': '卢比(印度)',
  'TND': '第纳尔(突尼斯)',
  'EGP': '镑(埃及)',
})

// 状态
const baseCurrency = ref('USD')
const targetCurrency = ref('CNY')
const amount = ref(100)
const rate = ref(null)
const result = ref(0)
const rateSource = ref('')
const lastUpdated = ref('')
const rateStatus = ref('cached')

// 项目设置
const displayCurrency = ref('CNY')

let rateIntervalId = null

// 从localStorage读取用户偏好
const loadPreferences = () => {
  try {
    const prefs = localStorage.getItem('currencyPreferences')
    if (prefs) {
      const parsed = JSON.parse(prefs)
      baseCurrency.value = parsed.baseCurrency || 'USD'
      targetCurrency.value = parsed.targetCurrency || 'CNY'
      displayCurrency.value = parsed.displayCurrency || 'CNY'
    }
  } catch (e) {
    console.warn('Failed to load currency preferences:', e)
  }
}

// 保存用户偏好
const savePreferences = () => {
  try {
    const prefs = {
      baseCurrency: baseCurrency.value,
      targetCurrency: targetCurrency.value,
      displayCurrency: displayCurrency.value
    }
    localStorage.setItem('currencyPreferences', JSON.stringify(prefs))
  } catch (e) {
    console.warn('Failed to save currency preferences:', e)
  }
}

// 获取汇率
const fetchRate = async () => {
  try {
    const response = await fetch(`/api/exchange-rates/latest?currency=${targetCurrency.value}`)
    const data = await response.json()
    
    if (data.success) {
      rate.value = data.rate
      rateSource.value = data.source
      lastUpdated.value = data.date
      rateStatus.value = data.cached ? 'cached' : 'online'
      
      // 自动转换
      convert()
    } else {
      console.error('Failed to fetch exchange rate:', data.error)
    }
  } catch (e) {
    console.error('Error fetching exchange rate:', e)
  }
}

// 转换货币
const convert = () => {
  if (rate.value && amount.value) {
    result.value = (amount.value * rate.value).toFixed(2)
  } else {
    result.value = '0.00'
  }
}

// 刷新汇率
const refreshRates = async () => {
  try {
    const response = await fetch('/api/exchange-rates/refresh', { method: 'POST' })
    const data = await response.json()
    
    if (data.success) {
      await fetchRate() // 重新获取最新汇率
    } else {
      console.error('Failed to refresh rates:', data.error)
    }
  } catch (e) {
    console.error('Error refreshing rates:', e)
  }
}

// 更新汇率
const updateRates = () => {
  savePreferences()
  fetchRate()
}

// 更新显示货币
const updateDisplayCurrency = () => {
  savePreferences()
}

// 初始化
onMounted(() => {
  loadPreferences()
  fetchRate()

  rateIntervalId = setInterval(() => {
    fetchRate()
  }, 5 * 60 * 1000)
})

onUnmounted(() => {
  if (rateIntervalId) {
    clearInterval(rateIntervalId)
    rateIntervalId = null
  }
})

// 监听货币变化
watch([baseCurrency, targetCurrency], updateRates)
</script>