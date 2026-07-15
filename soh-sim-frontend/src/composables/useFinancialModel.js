/**
 * 前端财务模型 — 实时预览引擎
 *
 * **双轨设计（Frontend Preview + Backend Precision）：**
 *   - 前端（此文件）：用于拖拽参数时的即时反馈，含 Newton-Raphson IRR 求解器。
 *     计算简化版指标（IRR/NPV/Payback），让用户调整参数时获得 <100ms 的响应。
 *   - 后端（services/financial/engine.py）：确认后调用 POST /api/financial/calculate
 *     执行完整精算（26年逐期现金流 + DSCR + LCOS + 敏感性分析）。
 *
 * 不要废弃此文件 — 它是交互体验的关键。
 */

import { ref, computed, watch, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { useDraft } from './useDraft'
import { useExchangeRate } from './useExchangeRate.js'

export function useFinancialModel(props) {
  const { t } = useI18n()
  const { displayCurrency, convert } = useExchangeRate()

  const chartColors = computed(() => {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
    return {
      backgroundColor: 'transparent',
      textStyle: { color: isDark ? 'var(--color-text-secondary)' : 'var(--color-text-secondary)', fontSize: 10 },
      axisLabel: isDark ? 'var(--color-text-secondary)' : 'var(--color-text-secondary)',
      legendText: isDark ? 'var(--color-text-secondary)' : 'var(--color-text-secondary)',
      gridLine: isDark ? '#1e293b' : 'var(--color-border-light)',
      success: isDark ? 'var(--color-success)' : 'var(--color-success)',
      danger: isDark ? 'var(--color-danger)' : 'var(--color-danger)',
      warning: isDark ? 'var(--color-warning)' : 'var(--color-warning)',
      info: isDark ? '#0ea5e9' : '#0ea5e9',
      acLine: isDark ? '#14b8a6' : '#14b8a6',
      purple: isDark ? 'var(--color-info)' : 'var(--color-info)',
      orange: isDark ? 'var(--color-chart-orange)' : 'var(--color-chart-orange)',
      cyan: isDark ? 'var(--color-chart-cyan)' : 'var(--color-chart-cyan)',
      redLight: isDark ? '#f87171' : '#f87171',
      muted: isDark ? 'var(--color-text-secondary)' : 'var(--color-text-secondary)'
    }
  })

  const { state: f, clearDraft: clearFDraft } = useDraft('financial-params', {
    offPeakPrice: 200,
    peakPrice: 600,
    spreadCapture: 85,
    operatingDays: 330,
    capacityPrice: 50000,
    ancillaryPrice: 30000,
    priceEscalation: 1.5,
    efficiencyLossPct: 5,
    containerCostPerMWh: 100,
    pcsCostPerMW: 25,
    bopCostPerMWh: 30,
    developmentCostPerMW: 20,
    landCostPerMW: 8,
    substationCostPerMW: 15,
    transmissionCostPerMW: 10,
    fixedOpexPerkW: 35,
    varOpexPerMWh: 3,
    insuranceRate: 0.4,
    opexEscalation: 2.0,
    discountRate: 7,
    debtRatio: 70,
    interestRate: 4.5,
    loanTenure: 15,
    costOfEquity: 12,
    equityRatio: 30,
    taxRate: 25,
    depreciationYears: 20,
    residualRate: 5,
    depreciationMethod: 'straight-line',
    vatRate: 5,
    gracePeriod: 2,
    augContainerCostPerMWh: 90,
    costDeclineRate: 5,
    augInstallCost: 5,
    decommissioningCost: 10,
    sensPct: 20
  })

  // 融资比例校验：确保债务+权益=100%
  watch(
    [() => f.debtRatio, () => f.equityRatio],
    () => {
      if (f.debtRatio + f.equityRatio !== 100) {
        f.equityRatio = 100 - f.debtRatio
      }
    },
    { immediate: true }
  )

  const metrics = ref([
    { label: t('financialDashboard.projectIRR'), value: '-', unit: '%', textColor: 'var(--color-accent-secondary)' },
    { label: t('financialDashboard.equityIRR'), value: '-', unit: '%', textColor: 'var(--color-success)' },
    { label: 'WACC', value: '-', unit: '%', textColor: '#0ea5e9' },
    {
      label: t('financialDashboard.npv'),
      value: '-',
      unit: `${t('financialDashboard.wanUnit')} (${displayCurrency})`,
      textColor: 'var(--color-accent)'
    },
    {
      label: t('financialDashboard.lcos'),
      value: '-',
      unit: `${t('financialDashboard.energyPriceUnit')} (${displayCurrency})`,
      textColor: 'var(--color-info)'
    },
    {
      label: t('financialDashboard.payback'),
      value: '-',
      unit: t('financialDashboard.yearUnit'),
      textColor: 'var(--color-warning)'
    },
    {
      label: t('financialDashboard.totalCAPEX'),
      value: '-',
      unit: `${t('financialDashboard.wanUnit')} (${displayCurrency})`,
      textColor: 'var(--color-danger)'
    },
    { label: t('financialDashboard.minDscr'), value: '-', unit: 'x', textColor: 'var(--color-chart-orange)' }
  ])

  const cashFlowTable = ref([])
  let cachedRows = []
  let cachedCapexData = null

  function fmtNum(v) {
    if (v == null || isNaN(v)) return '-'
    if (Math.abs(v) >= 100) return v.toFixed(1)
    return v.toFixed(2)
  }

  function calcIRR(flows, years) {
    let rate = 0.08
    for (let iter = 0; iter < 100; iter++) {
      let npv = 0,
        dnpv = 0
      for (let i = 0; i < flows.length; i++) {
        const t = years[i] - years[0]
        const df = Math.pow(1 + rate, t)
        npv += flows[i] / df
        if (t > 0) dnpv += (-t * flows[i]) / Math.pow(1 + rate, t + 1)
      }
      if (Math.abs(npv) < 1e-6) break
      const newRate = rate - npv / (dnpv || 1e-10)
      if (Math.abs(newRate - rate) < 1e-8) {
        rate = newRate
        break
      }
      rate = newRate
      if (rate < -0.99) rate = -0.5
      if (rate > 100) rate = 10
    }
    return Math.max(-99, Math.min(999, rate * 100)).toFixed(2)
  }

  function computeAll(afterCompute) {
    const p = props.params || {}
    const soh = props.soh || []
    const augQty = props.augQty || []

    // 独立模式 vs 项目模式：数据来源不同
    let totalCapMWh,
      totalCapMW,
      cyclesPerDay,
      duration,
      ratedEnergy = 5
    const isStandalone = props.mode === 'standalone'

    if (isStandalone && props.standalone) {
      const sp = props.standalone
      totalCapMWh = sp.totalCapMWh || 100
      totalCapMW = sp.totalCapMW || 50
      cyclesPerDay = sp.cyclesPerDay || 1
      duration = totalCapMWh / (totalCapMW || 1)
      // 独立模式：operatingDays / efficiencyLossPct 从 standalone 读取
      if (sp.operatingDays != null) f.operatingDays = sp.operatingDays
      if (sp.efficiencyLossPct != null) f.efficiencyLossPct = sp.efficiencyLossPct
    } else {
      ratedEnergy = p.ratedEnergy || 5
      const initContainerQty = p.initContainerQty || 62
      cyclesPerDay = p.cyclesPerDay || 1
      duration = p.duration || 2
      totalCapMWh = ratedEnergy * initContainerQty
      totalCapMW = totalCapMWh / (duration || 1)
    }

    const containerCost = f.containerCostPerMWh * totalCapMWh
    const pcsCost = f.pcsCostPerMW * totalCapMW
    const bopCost = f.bopCostPerMWh * totalCapMWh
    const devCost = f.developmentCostPerMW * totalCapMW
    const landCost = f.landCostPerMW * totalCapMW
    const substationCost = f.substationCostPerMW * totalCapMW
    const transmissionCost = f.transmissionCostPerMW * totalCapMW
    const baseCapex = containerCost + pcsCost + bopCost + devCost + landCost + substationCost + transmissionCost
    const vatAmount = (baseCapex * f.vatRate) / 100
    const totalCapex = baseCapex + vatAmount

    cachedCapexData = {
      containerCost,
      pcsCost,
      bopCost,
      devCost,
      landCost,
      substationCost,
      transmissionCost,
      totalCapex,
      totalCapMW,
      totalCapMWh
    }

    const wacc = (f.costOfEquity * f.equityRatio) / 100 + (f.interestRate * (1 - f.taxRate / 100) * f.debtRatio) / 100
    const debtAmount = (totalCapex * f.debtRatio) / 100
    const equityAmount = totalCapex - debtAmount
    const annualDebtService =
      f.interestRate > 0 && f.loanTenure > 0
        ? (debtAmount * (f.interestRate / 100) * Math.pow(1 + f.interestRate / 100, f.loanTenure)) /
          (Math.pow(1 + f.interestRate / 100, f.loanTenure) - 1)
        : 0
    const residualValue = (totalCapex * f.residualRate) / 100
    const spread = ((f.peakPrice - f.offPeakPrice) * f.spreadCapture) / 100

    let annualDepreciation = 0
    if (f.depreciationYears > 0) {
      if (f.depreciationMethod === 'straight-line') {
        annualDepreciation = (totalCapex * (1 - f.residualRate / 100)) / f.depreciationYears
      } else if (f.depreciationMethod === 'double-declining') {
        const rate = 2 / f.depreciationYears
        annualDepreciation = totalCapex * rate * (1 - f.residualRate / 100)
      }
    }

    const rows = []
    rows.push({
      year: 0,
      energy: 0,
      arbitrage: 0,
      capacity: 0,
      ancillary: 0,
      revenue: 0,
      opex: 0,
      ebitda: 0,
      depreciation: 0,
      interest: 0,
      taxableIncome: 0,
      tax: 0,
      augCapex: -totalCapex,
      debtService: 0,
      cashFlow: -totalCapex,
      cumCashFlow: -totalCapex,
      dscr: null
    })

    let cumCash = -totalCapex
    let remainingDebt = debtAmount
    let totalDiscountedCost = totalCapex
    let totalDiscountedEnergy = 0
    let minDscr = Infinity

    for (let i = 1; i <= 25; i++) {
      const idx = i
      // 独立模式：用线性衰减生成SOH；项目模式：用仿真结果
      let cSoh
      if (isStandalone && props.standalone) {
        const sp = props.standalone
        cSoh = Math.max(0, (sp.sohStart || 100) - (sp.sohAnnualDecline || 2) * i) / 100
      } else {
        cSoh = soh[idx] != null ? soh[idx] : soh.length > 0 ? soh[soh.length - 1] : 1
      }
      const yearEnergy = totalCapMWh * cyclesPerDay * f.operatingDays * cSoh * (1 - f.efficiencyLossPct / 100)
      const priceFactor = Math.pow(1 + f.priceEscalation / 100, i)
      const opexFactor = Math.pow(1 + f.opexEscalation / 100, i)

      const arbitrageRev = ((yearEnergy * spread) / 10000) * priceFactor
      const capacityRev = ((totalCapMW * f.capacityPrice) / 10000) * priceFactor
      const ancillaryRev = ((totalCapMW * f.ancillaryPrice) / 10000) * priceFactor
      const totalRevenue = arbitrageRev + capacityRev + ancillaryRev

      const fixedOpex = ((f.fixedOpexPerkW * totalCapMW * 1000) / 10000) * opexFactor
      const varOpex = ((f.varOpexPerMWh * yearEnergy) / 10000) * opexFactor
      const insurance = (totalCapex * f.insuranceRate) / 100
      const landLease = (totalCapMW * 2) / 10000
      const totalOpex = fixedOpex + varOpex + insurance + landLease
      const ebitda = totalRevenue - totalOpex

      let dep = 0
      if (f.depreciationMethod === 'straight-line') {
        dep = i <= f.depreciationYears ? annualDepreciation : 0
      } else if (f.depreciationMethod === 'double-declining') {
        const depreciableAmount = totalCapex - residualValue
        if (i <= f.depreciationYears - 2) {
          const rate = 2 / f.depreciationYears
          const bookValueStart = totalCapex - rows.slice(1, i).reduce((s, r) => s + r.depreciation, 0)
          dep = Math.min(bookValueStart * rate, bookValueStart - residualValue)
        } else if (i <= f.depreciationYears) {
          const bookValueStart = totalCapex - rows.slice(1, i).reduce((s, r) => s + r.depreciation, 0)
          dep = Math.max(0, (bookValueStart - residualValue) / (f.depreciationYears - i + 1))
        }
      }

      let interestPaid = 0,
        principalPaid = 0,
        debtServiceYear = 0
      if (remainingDebt > 0 && i <= f.loanTenure) {
        interestPaid = (remainingDebt * f.interestRate) / 100
        if (i <= f.gracePeriod) {
          principalPaid = 0
          debtServiceYear = interestPaid
        } else {
          principalPaid = Math.min(annualDebtService - interestPaid, remainingDebt)
          debtServiceYear = interestPaid + principalPaid
          remainingDebt = Math.max(0, remainingDebt - principalPaid)
        }
      }

      const taxableIncome = ebitda - dep - interestPaid
      const tax = Math.max(0, (taxableIncome * f.taxRate) / 100)

      const augQtyYear = augQty[idx] || 0
      const costDeclineFactor = Math.pow(1 - f.costDeclineRate / 100, i)
      const augContainerPrice = f.augContainerCostPerMWh * costDeclineFactor
      const augCapexYear =
        augQtyYear > 0 ? -(augQtyYear * ratedEnergy * augContainerPrice + augQtyYear * f.augInstallCost) : 0

      const cashFlow = ebitda - tax - debtServiceYear + augCapexYear
      cumCash += cashFlow

      const discFactor = Math.pow(1 + f.discountRate / 100, i)
      totalDiscountedCost += (totalOpex + (augCapexYear < 0 ? -augCapexYear : 0)) / discFactor
      totalDiscountedEnergy += yearEnergy / discFactor

      const dscr = debtServiceYear > 0 ? (ebitda - tax) / debtServiceYear : null
      if (dscr !== null && dscr < minDscr) minDscr = dscr

      rows.push({
        year: i,
        energy: yearEnergy,
        arbitrage: arbitrageRev,
        capacity: capacityRev,
        ancillary: ancillaryRev,
        revenue: totalRevenue,
        opex: totalOpex,
        ebitda,
        depreciation: dep,
        interest: interestPaid,
        taxableIncome,
        tax,
        augCapex: augCapexYear,
        debtService: debtServiceYear,
        cashFlow,
        cumCashFlow: cumCash,
        dscr
      })
    }

    totalDiscountedCost -= residualValue / Math.pow(1 + f.discountRate / 100, 25)
    const decommissioningCostAmount = f.decommissioningCost * totalCapMWh
    totalDiscountedCost += decommissioningCostAmount / Math.pow(1 + f.discountRate / 100, 25)
    if (rows.length > 25 && f.decommissioningCost > 0) {
      rows[25].cashFlow -= decommissioningCostAmount
      rows[25].cumCashFlow -= decommissioningCostAmount
    }

    const lcos = totalDiscountedEnergy > 0 ? (totalDiscountedCost / totalDiscountedEnergy) * 10000 : 0
    const npv = rows.reduce(
      (s, r) => s + r.cashFlow / (r.year === 0 ? 1 : Math.pow(1 + f.discountRate / 100, r.year)),
      0
    )
    const irr = calcIRR(
      rows.map((r) => r.cashFlow),
      rows.map((r) => r.year)
    )
    const equityFlows = [-equityAmount, ...rows.slice(1).map((r) => r.cashFlow)]
    const equityYears = [0, ...rows.slice(1).map((r) => r.year)]
    const equityIrr = calcIRR(equityFlows, equityYears)

    let payback = '-'
    for (let i = 1; i < rows.length; i++) {
      if (rows[i].cumCashFlow >= 0 && rows[i - 1].cumCashFlow < 0) {
        payback = (i - 1 + Math.abs(rows[i - 1].cumCashFlow) / rows[i].cashFlow).toFixed(1)
        break
      }
    }

    const convertToDisplay = (usdAmount) => convert(usdAmount, 'USD', displayCurrency.value)

    metrics.value[0].value = irr + '%'
    metrics.value[1].value = equityIrr + '%'
    metrics.value[2].value = wacc.toFixed(2) + '%'
    metrics.value[3].value = convertToDisplay(npv).toFixed(0)
    metrics.value[4].value = lcos.toFixed(3)
    metrics.value[5].value = payback
    metrics.value[6].value = convertToDisplay(totalCapex).toFixed(0)
    metrics.value[7].value = minDscr !== Infinity ? minDscr.toFixed(2) : '-'

    cashFlowTable.value = rows
    cachedRows = rows

    if (typeof afterCompute === 'function') {
      nextTick(() => {
        setTimeout(() => afterCompute(), 300)
      })
    }
  }

  function calculateSensitivityData() {
    if (!cachedCapexData) return {}
    const { containerCost, pcsCost, bopCost, devCost } = cachedCapexData
    const sensitivityPct = f.sensPct || 20
    return {
      base: {
        container: containerCost,
        pcs: pcsCost,
        bop: bopCost,
        dev: devCost,
        total: containerCost + pcsCost + bopCost + devCost
      },
      positive: {
        container: containerCost * (1 + sensitivityPct / 100),
        pcs: pcsCost * (1 + sensitivityPct / 100),
        bop: bopCost * (1 + sensitivityPct / 100),
        dev: devCost * (1 + sensitivityPct / 100),
        total: (containerCost + pcsCost + bopCost + devCost) * (1 + sensitivityPct / 100)
      },
      negative: {
        container: containerCost * (1 - sensitivityPct / 100),
        pcs: pcsCost * (1 - sensitivityPct / 100),
        bop: bopCost * (1 - sensitivityPct / 100),
        dev: devCost * (1 - sensitivityPct / 100),
        total: (containerCost + pcsCost + bopCost + devCost) * (1 - sensitivityPct / 100)
      }
    }
  }

  function recalc() {
    computeAll()
  }

  return {
    f,
    metrics,
    cashFlowTable,
    chartColors,
    cachedRows: () => cachedRows,
    cachedCapexData: () => cachedCapexData,
    fmtNum,
    computeAll,
    calculateSensitivityData,
    recalc
  }
}
