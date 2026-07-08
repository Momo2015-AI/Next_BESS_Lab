import { ref, reactive, onMounted, onUnmounted, watch } from 'vue'
import api from '../services/api.js'

/**
 * 汇率管理 Composable
 * 提供货币转换、汇率获取、货币偏好管理等功能
 */
export function useExchangeRate() {
  // 支持的货币列表
  const supportedCurrencies = reactive({
    USD: '美元',
    CNY: '人民币',
    EUR: '欧元',
    GBP: '英镑',
    AED: '迪拉姆(阿联酋)',
    SAR: '里亚尔(沙特)',
    QAR: '里亚尔(卡塔尔)',
    KWD: '第纳尔(科威特)',
    OMR: '里亚尔(阿曼)',
    BHD: '第纳尔(巴林)',
    JPY: '日元',
    KRW: '韩元',
    AUD: '澳元',
    INR: '卢比(印度)',
    TND: '第纳尔(突尼斯)',
    EGP: '镑(埃及)'
  })

  // 状态
  const baseCurrency = ref('USD')
  const displayCurrency = ref('CNY')
  const exchangeRates = ref({})
  const loading = ref(false)
  const lastUpdated = ref('')
  const rateSource = ref('')

  let rateIntervalId = null

  // 从localStorage加载用户偏好
  const loadPreferences = () => {
    try {
      const prefs = localStorage.getItem('currencyPreferences')
      if (prefs) {
        const parsed = JSON.parse(prefs)
        baseCurrency.value = parsed.baseCurrency || 'USD'
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
        displayCurrency: displayCurrency.value
      }
      localStorage.setItem('currencyPreferences', JSON.stringify(prefs))
    } catch (e) {
      console.warn('Failed to save currency preferences:', e)
    }
  }

  // 获取所有汇率
  const fetchAllRates = async () => {
    loading.value = true
    try {
      const data = await api.get('/api/exchange-rates/all')

      exchangeRates.value = data.rates
      lastUpdated.value = data.date
      rateSource.value = data.rates[Object.keys(data.rates)[0]]?.source || ''
    } catch (e) {
      console.error('Error fetching exchange rates:', e)
    } finally {
      loading.value = false
    }
  }

  // 获取特定汇率
  const fetchRate = async (currency) => {
    loading.value = true
    try {
      const data = await api.get(`/api/exchange-rates/latest?currency=${currency}`)

      exchangeRates.value[currency] = {
        rate: data.rate,
        source: data.source,
        date: data.date,
        name: supportedCurrencies[currency]
      }
      lastUpdated.value = data.date
      rateSource.value = data.source
      return data.rate
    } catch (e) {
      console.error('Error fetching exchange rate:', e)
      return null
    } finally {
      loading.value = false
    }
  }

  // 货币转换
  const convert = (amount, fromCurrency, toCurrency) => {
    if (!amount || isNaN(amount)) return 0

    // 如果相同货币，直接返回
    if (fromCurrency === toCurrency) return amount

    // 获取汇率
    const fromRate = exchangeRates.value[fromCurrency]?.rate
    const toRate = exchangeRates.value[toCurrency]?.rate

    if (fromRate && toRate) {
      // 通过USD转换：amount * (toRate / fromRate)
      return amount * (toRate / fromRate)
    }

    // 如果没有汇率数据，返回0
    return 0
  }

  // 格式化金额
  const formatAmount = (amount, currency = displayCurrency.value) => {
    if (!amount || isNaN(amount)) return '0'

    const converted = convert(amount, 'USD', currency)
    const rate = exchangeRates.value[currency]?.rate

    if (rate) {
      return `${converted.toFixed(2)} ${currency}`
    }

    return `${amount.toFixed(2)} ${currency}`
  }

  // 获取汇率信息
  const getRateInfo = (currency) => {
    return exchangeRates.value[currency] || null
  }

  // 刷新所有汇率
  const refreshRates = async () => {
    try {
      await api.post('/api/exchange-rates/refresh')

      await fetchAllRates()
      return true
    } catch (e) {
      console.error('Error refreshing rates:', e)
      return false
    }
  }

  // 设置基础货币
  const setBaseCurrency = (currency) => {
    if (supportedCurrencies[currency]) {
      baseCurrency.value = currency
      savePreferences()
    }
  }

  // 设置显示货币
  const setDisplayCurrency = (currency) => {
    if (supportedCurrencies[currency]) {
      displayCurrency.value = currency
      savePreferences()
    }
  }

  // 初始化
  onMounted(() => {
    loadPreferences()
    fetchAllRates()

    rateIntervalId = setInterval(
      () => {
        fetchAllRates()
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

  return {
    // 数据
    supportedCurrencies,
    baseCurrency,
    displayCurrency,
    exchangeRates,
    loading,
    lastUpdated,
    rateSource,

    // 方法
    loadPreferences,
    savePreferences,
    fetchAllRates,
    fetchRate,
    convert,
    formatAmount,
    getRateInfo,
    refreshRates,
    setBaseCurrency,
    setDisplayCurrency
  }
}
