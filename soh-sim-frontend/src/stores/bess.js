import { defineStore } from 'pinia'
import { NUM_YEARS } from '../constants.js'

function create26Array(defaultVal = 0) {
  return Array.from({ length: NUM_YEARS }, () => defaultVal)
}

export const useBessStore = defineStore('bess', {
  state: () => ({
    project: {
      id: null,
      name: '',
      status: 'draft',
    },
    survey: {
      projectName: '',
      location: '',
      temperature: 25,
      duration: 2,
      cyclesPerDay: 1,
      requiredEnergy: 240,
      ratedEnergy: 5,
      totalPower: 50,
      gridVoltage: '110kV',
      altitude: 0,
    },
    systemParams: {
      ratedEnergy: 5,
      initContainerQty: 10,
      initPcsQty: 2,
      pcsPower: 5,
      duration: 2,
      cyclesPerDay: 1,
      temperature: 25,
      acEfficiency: 97.03,
      bessAuxRun: 18.124,
      bessAuxStandby: 3.5,
      pcsAuxRun: 6.5,
      pcsAuxStandby: 1.0,
      requiredEnergy: 240,
    },
    selectedProducts: {
      cell: null,
      container: null,
      pcs: null,
    },
    degradation: {
      soh: create26Array(100),
      rte: create26Array(97.03),
      dod: create26Array(100),
      augQty: create26Array(0),
    },
    results: {
      initGross: create26Array(0),
      initAux: create26Array(0),
      initAcUsable: create26Array(0),
      augGross: create26Array(0),
      augAux: create26Array(0),
      augAcUsable: create26Array(0),
      augAccumQty: create26Array(0),
      totalAcUsable: create26Array(0),
      meetsReq: create26Array(false),
    },
    financial: {
      capex: { equipment: 0, epc: 0, development: 0 },
      opex: { maintenance: 0, insurance: 0, grid: 0 },
      revenue: { arbitragePrice: 0.5 },
      metrics: { npv: 0, irr: 0, lcoe: 0, lcos: 0, roi: 0, dscr: 0, payback: -1 },
    },
    exports: {
      reportGenerated: false,
      bomGenerated: false,
    },
    phases: {
      phase1: { status: 'pending' },
      phase2: { status: 'pending' },
      phase3: { status: 'pending' },
      phase4: { status: 'pending' },
      phase5: { status: 'pending' },
    },
    calculating: false,
    calculationError: null,
  }),

  getters: {
    simulationDefaults: (state) => ({
      duration: state.survey.duration || 2,
      cyclesPerDay: state.survey.cyclesPerDay || 1,
      requiredEnergy: state.survey.requiredEnergy || 240,
      temperature: state.survey.temperature || 25,
    }),
    allPhasesComplete: (state) =>
      Object.values(state.phases).every((p) => p.status === 'completed'),
  },

  actions: {
    updatePhaseParams(phase, params) {
      this.phases[phase].status = 'completed'
      if (phase === 'phase1') {
        Object.assign(this.survey, params)
        this.project.name = params.projectName || ''
      } else if (phase === 'phase2') {
        Object.assign(this.systemParams, params)
      }
    },

    async runPipeline() {
      this.calculating = true
      this.calculationError = null
      try {
        const body = {
          systemParams: { ...this.systemParams },
          degradation: {
            soh: [...this.degradation.soh],
            rte: [...this.degradation.rte],
            dod: [...this.degradation.dod],
            augQty: [...this.degradation.augQty],
          },
          financial: {
            capex: { ...this.financial.capex },
            opex: { ...this.financial.opex },
            revenue: { ...this.financial.revenue },
          },
        }
        const res = await fetch('/api/pipeline/calculate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
        })
        if (!res.ok) {
          const err = await res.json()
          throw new Error(err.error || 'Calculation failed')
        }
        const data = await res.json()
        if (data.result) {
          this.results = {
            initGross: data.result.initGross,
            initAux: data.result.initAux,
            initAcUsable: data.result.initAcUsable,
            augGross: data.result.augGross,
            augAux: data.result.augAux,
            augAcUsable: data.result.augAcUsable,
            augAccumQty: data.result.augAccumQty,
            totalAcUsable: data.result.totalAcUsable,
            meetsReq: data.result.meetsReq,
          }
          this.degradation.soh = data.result.soh
          this.degradation.rte = data.result.rte
          this.degradation.dod = data.result.dod
          if (data.result.financial) {
            this.financial.metrics = { ...data.result.financial }
          }
        }
      } catch (e) {
        this.calculationError = e.message
      } finally {
        this.calculating = false
      }
    },

    async loadProject(id) {
      try {
        const res = await fetch(`/api/projects/${id}`)
        if (res.ok) {
          const data = await res.json()
          this.project = data.project || this.project
        }
      } catch (e) {
        console.error('Failed to load project:', e)
      }
    },

    resetProject() {
      this.project = { id: null, name: '', status: 'draft' }
      this.phases = {
        phase1: { status: 'pending' },
        phase2: { status: 'pending' },
        phase3: { status: 'pending' },
        phase4: { status: 'pending' },
        phase5: { status: 'pending' },
      }
    },
  },
  persist: true,
})
