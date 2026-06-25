import { reactive, computed } from 'vue'

const strategyParams = [
  { key: 'days', label: '本次计算总天数 (Days)', min: 1, max: 365, step: 1, hasSlider: true },
  { key: 'cycles', label: '每天充放电循环次数', min: 0.5, max: 3, step: 0.5, hasSlider: true },
  { key: 'hours', label: '单次放电时长 (h)', min: 1, max: 6, step: 0.5, hasSlider: true },
  { key: 'cap', label: '单舱标称铭牌容量 (MWh)', min: 0.1, max: 100, hasSlider: false },
  { key: 'units', label: '当前运行总台数 (台)', min: 1, max: 1000, hasSlider: false },
]

const efficiencyParams = [
  { key: 'dcRte', label: 'DC-RTE (直流往返效率)', min: 0.85, max: 0.98, step: 0.005, hasSlider: true },
  { key: 'pcsEff', label: 'PCS 充/放电效率', min: 0.95, max: 0.995, step: 0.002, hasSlider: true },
  { key: 'acEff', label: '交流侧综合效率 (变损/线损)', min: 0.95, max: 0.995, step: 0.002, hasSlider: true },
]

const auxParams = [
  { key: 'bRun', label: '电池舱【运行】温控功率 (kW)', min: 5, max: 40, step: 1, hasSlider: true },
  { key: 'bStd', label: '电池舱【待机】温控功率 (kW)', min: 1, max: 15, step: 0.5, hasSlider: true },
  { key: 'pRun', label: 'PCS变流器【运行】损耗 (kW)', min: 1, max: 20, step: 0.5, hasSlider: true },
  { key: 'pStd', label: 'PCS变流器【待机】损耗 (kW)', min: 0.5, max: 10, step: 0.5, hasSlider: true },
]

const externalParams = [
  { key: 'pStation', label: '站宇及主变固定自耗 (kW)', min: 1, max: 30, step: 0.5, hasSlider: true },
]

// 工厂函数：每次调用创建独立实例，避免组件间状态共享
export function useAuxPower() {
  const state = reactive({
    days: 365,
    cycles: 2,
    hours: 2,
    cap: 5,
    units: 62,
    dcRte: 0.941,
    pcsEff: 0.987,
    acEff: 0.975,
    bRun: 20,
    bStd: 4,
    pRun: 5,
    pStd: 1.5,
    pStation: 7.2,
  })

  const results = computed(() => {
    const sqrtRte = Math.sqrt(state.dcRte)
    const tRun = state.days * state.cycles * state.hours * 2
    const tStd = state.days * 24 - tRun
    const dcTotalAux = ((tRun * state.bRun) + (tStd * state.bStd)) * state.units / 1000
    const acTotalAux = ((tRun * state.pRun) + (tStd * state.pStd) + (state.days * 24 * state.pStation)) / 1000
    const totalSystemAux = dcTotalAux + acTotalAux
    const annualGrossDischarge = state.cap * state.units * sqrtRte * state.cycles * state.days * state.acEff * state.pcsEff
    const annualNetDischarge = annualGrossDischarge - totalSystemAux
    const singleUnitDailyKwh = (dcTotalAux * 1000) / Math.max(state.units, 1) / Math.max(state.days, 1)

    return {
      tRun: Math.round(tRun * 10) / 10,
      tStd: Math.round(tStd * 10) / 10,
      sqrtRte: Math.round(sqrtRte * 10000) / 10000,
      dcTotalAux: Math.round(dcTotalAux * 100) / 100,
      acTotalAux: Math.round(acTotalAux * 100) / 100,
      totalSystemAux: Math.round(totalSystemAux * 100) / 100,
      annualGrossDischarge: Math.round(annualGrossDischarge * 100) / 100,
      annualNetDischarge: Math.round(annualNetDischarge * 100) / 100,
      singleUnitDailyKwh: Math.round(singleUnitDailyKwh * 100) / 100,
    }
  })

  return {
    state,
    results,
    strategyParams,
    efficiencyParams,
    auxParams,
    externalParams,
  }
}
