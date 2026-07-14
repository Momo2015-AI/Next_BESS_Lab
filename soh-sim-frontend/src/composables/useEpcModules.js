/**
 * EPC 模块状态与行为组合式
 *
 * 集中管理 9 个 EPC 子模块的：
 * - reactive 表单（archForm / gcForm / sfForm / ippForm / matrixForm / tmForm / seForm / hvForm / bidForm）
 * - result ref（archResult ... bidResult）
 * - apiCall（统一走 services/api.js 的 post，去掉裸 fetch）
 * - 9 个 action 函数
 * - 图表预览状态与 previewChart
 * - loadStandards / formatNum / statusLabel / statusClass / getDeratingColor 工具
 *
 * 设计要点：
 * - apiCall 内部捕获 ApiError 并通过 onError 回调上抛，保持与原 emit('error') 契约一致
 * - services/api.js 的 post 内部仍调用 fetch，因此表征测试对 global.fetch 的 mock 仍然有效
 * - 所有请求经 services/api.js，自动注入 Authorization token、超时、401 跳登录
 */
import { ref, reactive, nextTick } from 'vue'
import { post as apiPost, get as apiGet, ApiError } from '../services/api.js'
import { renderPlotly, purgePlotly } from './usePlotly.js'

/**
 * @param {(msg: string) => void} [onError] 错误回调（用于向上层 emit error）
 * @param {function} [t] i18n translate 函数
 */
export function useEpcModules(onError, t) {
  const loading = ref(false)

  // ---------- 9 个 reactive 表单 ----------
  const archForm = reactive({
    total_power_mw: 100,
    total_energy_mwh: 200,
    architecture_type: 'central',
    coupling_type: 'AC',
    cell_voltage: 3.2,
    cell_capacity: 280,
    pcs_power_mw: 3.45,
    pcs_max_dc_voltage: 1500
  })
  const gcForm = reactive({
    grid_standard: 'UAE_S_5010',
    grid_voltage_kv: 33,
    grid_frequency_hz: 50,
    pcs_count: 10,
    pcs_power_mw: 3.45
  })
  const sfForm = reactive({
    system_capacity_mwh: 100,
    container_count: 20,
    chemistry_type: 'LFP',
    suppression_type: 'Novec1230'
  })
  const ippForm = reactive({
    project_life_years: 25,
    total_capex_usd: 500000000,
    capacity_mw: 100,
    energy_mwh: 200,
    capacity_price_usd_kw_month: 8.0,
    energy_price_usd_kwh: 0.05,
    ppa_escalation_rate: 0.02,
    debt_ratio: 0.7,
    debt_interest_rate: 0.05,
    debt_tenor_years: 15,
    annual_opex_usd: 5000000,
    availability_guarantee: 0.98
  })
  const matrixForm = reactive({ template: 'UAE_DEWA_VII_BESS' })
  const tmForm = reactive({ ambient_max_c: 45, cell_capacity_ah: 280, c_rate: 0.5, cooling_type: 'liquid' })
  const seForm = reactive({
    container_count: 20,
    pcs_count: 10,
    communication_protocol: 'IEC_61850',
    dispatch_strategy: 'peak_shaving'
  })
  const hvForm = reactive({
    total_power_mw: 100,
    poc_voltage_kv: 33,
    short_circuit_capacity_mva: 500,
    poc_type: 'substation'
  })
  const bidForm = reactive({ template: 'technical_proposal' })

  // ---------- 9 个 result ref ----------
  const archResult = ref(null)
  const gcResult = ref(null)
  const sfResult = ref(null)
  const ippResult = ref(null)
  const matrixResult = ref(null)
  const tmResult = ref(null)
  const seResult = ref(null)
  const hvResult = ref(null)
  const bidResult = ref(null)

  // ---------- gridStandards ----------
  const gridStandards = ref([])

  // ---------- 统一 apiCall（走 services/api.js） ----------
  /**
   * 统一 POST 调用：成功返回 data，失败/异常通过 onError 上报并返回 null
   * @param {string} url
   * @param {object} body
   * @returns {Promise<object|null>}
   */
  async function apiCall(url, body) {
    loading.value = true
    try {
      const resp = await apiPost(url, body)
      // services/api.js 在 !ok 或 success===false 时已 throw ApiError，
      // 能走到这里说明 resp.success !== false。保持与原逻辑一致：返回 resp.data
      return resp.data
    } catch (e) {
      const msg =
        e instanceof ApiError
          ? e.message
          : t
            ? t('epc.netError', { message: e?.message || '' })
            : 'Network error: ' + (e?.message || '')
      if (onError) onError(msg)
      return null
    } finally {
      loading.value = false
    }
  }

  // ---------- 9 个 action 函数 ----------
  async function designArchitecture() {
    const data = await apiCall('/api/system-architecture/design', archForm)
    if (data) archResult.value = data
  }

  async function loadStandards() {
    try {
      const resp = await apiGet('/api/grid-compliance/standards')
      gridStandards.value = Array.isArray(resp) ? resp : resp.data || []
    } catch (e) {
      /* ignore */
    }
  }

  async function analyzeGridCompliance() {
    const data = await apiCall('/api/grid-compliance/analyze', gcForm)
    if (data) gcResult.value = data
  }

  async function analyzeSafety() {
    const data = await apiCall('/api/safety-design/analyze', sfForm)
    if (data) sfResult.value = data
  }

  async function calculateIPP() {
    const data = await apiCall('/api/ipp-financial/calculate', ippForm)
    if (data) ippResult.value = data
  }

  async function generateMatrix() {
    const data = await apiCall('/api/compliance-matrix/generate', matrixForm)
    if (data) matrixResult.value = data
  }

  async function calculateThermal() {
    const data = await apiCall('/api/thermal-management/calculate', { ...tmForm, cells_per_container: 5000 })
    if (data) tmResult.value = data
  }

  async function designScada() {
    const data = await apiCall('/api/scada-ems/design', seForm)
    if (data) seResult.value = data
  }

  async function designHV() {
    const data = await apiCall('/api/hv-interconnection/design', hvForm)
    if (data) hvResult.value = data
  }

  async function generateBidDoc() {
    const data = await apiCall('/api/bid-document/generate', bidForm)
    if (data) bidResult.value = data
  }

  // ---------- 图表预览 ----------
  const chartTypes = [
    { id: 'soh_rte_curve', label: 'epc.chartSohRteCurve' },
    { id: 'capacity_matrix', label: 'epc.chartCapacityMatrix' },
    { id: 'grid_compliance', label: 'epc.chartLvrtHvrt' },
    { id: 'ipp_cashflow', label: 'epc.chartIppCashflow' }
  ]
  const chartReady = ref(false)
  const chartLoading = ref('')
  const chartError = ref('')
  const activeChart = ref('')
  const chartContainer = ref(null)

  async function previewChart(chartType) {
    chartLoading.value = chartType
    chartError.value = ''
    chartReady.value = false
    if (chartContainer.value) {
      purgePlotly(chartContainer.value)
    }
    try {
      const body = { ...bidForm, chart_type: chartType }
      if (bidResult.value) {
        body.bid_data = bidResult.value
      }
      // 图表接口同样走 services/api.js（POST）
      const result = await apiPost(`/api/report/charts/${chartType}`, body)
      if (result.success !== false && result.chart) {
        activeChart.value = chartType
        chartReady.value = true
        await nextTick()
        await renderPlotly(chartContainer.value, result.chart, result.div_id)
      } else {
        chartError.value = result.error || (t ? t('epc.chartGenFailed') : 'Chart generation failed')
      }
    } catch (e) {
      chartError.value =
        e instanceof ApiError
          ? e.message
          : t
            ? t('epc.netError', { message: e?.message || '' })
            : 'Network error: ' + (e?.message || '')
    } finally {
      chartLoading.value = ''
    }
  }

  function purgeChart() {
    if (chartContainer.value) {
      purgePlotly(chartContainer.value)
    }
  }

  // ---------- 工具函数 ----------
  function formatNum(n) {
    if (!n) return '0'
    if (Math.abs(n) >= 1e9) return (n / 1e9).toFixed(2) + 'B'
    if (Math.abs(n) >= 1e6) return (n / 1e6).toFixed(1) + 'M'
    if (Math.abs(n) >= 1e3) return (n / 1e3).toFixed(1) + 'K'
    return n.toFixed(0)
  }

  function statusLabel(status) {
    const map = {
      compliant: 'epc.statusCompliant',
      non_compliant: 'epc.statusNonCompliant',
      partial: 'epc.statusPartial',
      'N/A': 'epc.statusNA'
    }
    return map[status] || status
  }

  function statusClass(status) {
    const map = { compliant: 'pass', non_compliant: 'fail', partial: 'warn', 'N/A': 'neutral' }
    return map[status] || 'neutral'
  }

  function getDeratingColor(pct) {
    if (pct > 80) return 'var(--color-success)'
    if (pct > 50) return 'var(--color-warning)'
    return 'var(--color-danger)'
  }

  return {
    // state
    loading,
    archForm,
    gcForm,
    sfForm,
    ippForm,
    matrixForm,
    tmForm,
    seForm,
    hvForm,
    bidForm,
    archResult,
    gcResult,
    sfResult,
    ippResult,
    matrixResult,
    tmResult,
    seResult,
    hvResult,
    bidResult,
    gridStandards,
    // chart
    chartTypes,
    chartReady,
    chartLoading,
    chartError,
    activeChart,
    chartContainer,
    // actions
    designArchitecture,
    loadStandards,
    analyzeGridCompliance,
    analyzeSafety,
    calculateIPP,
    generateMatrix,
    calculateThermal,
    designScada,
    designHV,
    generateBidDoc,
    previewChart,
    purgeChart,
    // utils
    formatNum,
    statusLabel,
    statusClass,
    getDeratingColor
  }
}
