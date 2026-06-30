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
      opex: { maintenance: 0, insurance: 0, grid: 0, landLease: 0, fixedOpexPerMw: 5000, variableOpexPerMwh: 2.5, insuranceRate: 0.5 },
      revenue: {
        arbitrage: { enabled: true, offPeakPrice: 30, peakPrice: 60, spreadCapture: 85, operatingDays: 330 },
        capacity: { enabled: true, capacityPrice: 45000 },
        ancillary: { enabled: true, ancillaryPrice: 15000 },
        ppa: { enabled: true, ppaPrice: 55, escalation: 2.0 },
        capacityAuction: { enabled: true, auctionPrice: 120000, contractYears: 5 },
      },
      financing: { debtRatio: 70, interestRate: 6.5, loanTerm: 15, repaymentType: 'equal_installment' },
      tax: { corporateTaxRate: 20, vatRate: 15, taxHolidayYears: 5 },
      discountRate: 8.0,
      depreciationYears: 15,
      residualRate: 5,
      priceEscalation: 2.0,
      efficiencyLossPct: 3,
      metrics: { projectIrr: 0, equityIrr: 0, npv: 0, lcos: 0, dscr: { min: 0, avg: 0 }, payback: -1, roi: 0 },
      cashflowTable: [],
      capexBreakdown: { equipment: 0, epc: 0, development: 0 },
      currency: 'USD',
      calculating: false,
    },
    boq: {
      items: [],
      activeVersion: 'main',
      totalPrice: 0,
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
    efficiencyFactors: [],
    efficiencyCurves: null,
    efficiencyDetail: null,
    degradationModel: 'arrhenius',
    gb36276Curves: [],
    environmental: {
      accelerate_temperature: true,
      accelerate_dust: false,
      accelerate_humidity: false,
      ref_temperature: 25,
      ref_humidity: 50,
      field_humidity: 65,
      dust_factor: 1.10,
      humidity_exponent: 2.5,
      activation_energy: 25000,
    },
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

    async loadEfficiencyFactors() {
      try {
        const resp = await fetch('/api/efficiency/factors')
        const data = await resp.json()
        this.efficiencyFactors = data.factors
      } catch (e) {
        console.error('Failed to load efficiency factors:', e)
      }
    },

    async loadDegradationConfig() {
      try {
        const [curvesRes, envRes] = await Promise.all([
          fetch('/api/degradation/gb36276-curves'),
          fetch('/api/degradation/environmental'),
        ])
        const curves = await curvesRes.json()
        const env = await envRes.json()
        this.gb36276Curves = curves.curves
        this.environmental = env.environmental
      } catch (e) {
        console.error('Failed to load degradation config:', e)
      }
    },

    async updateGb36276Curves(curves) {
      const res = await fetch('/api/degradation/gb36276-curves', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ curves }),
      })
      const data = await res.json()
      this.gb36276Curves = data.curves
    },

    async resetGb36276Curves() {
      const res = await fetch('/api/degradation/gb36276-curves/reset', { method: 'POST' })
      const data = await res.json()
      this.gb36276Curves = data.curves
    },

    async updateEnvironmental(env) {
      const res = await fetch('/api/degradation/environmental', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(env),
      })
      const data = await res.json()
      this.environmental = data.environmental
    },

    async resetEnvironmental() {
      const res = await fetch('/api/degradation/environmental/reset', { method: 'POST' })
      const data = await res.json()
      this.environmental = data.environmental
    },

    async previewDegradation(params) {
      const res = await fetch('/api/degradation/preview', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params),
      })
      return await res.json()
    },

    async previewAcceleration(params) {
      const res = await fetch('/api/degradation/environmental/preview', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params),
      })
      return await res.json()
    },

    async runPipeline() {
      this.calculating = true
      this.calculationError = null
      try {
        const body = {
          systemParams: { ...this.systemParams, efficiencyFactors: this.efficiencyFactors },
          degradation: {
            soh: [...this.degradation.soh],
            rte: [...this.degradation.rte],
            dod: [...this.degradation.dod],
            augQty: [...this.degradation.augQty],
          },
          algorithm: {
            model: this.degradationModel,
            correctionFactor: 1.0,
            environmental: { ...this.environmental },
            gb36276Curves: [...this.gb36276Curves],
          },
          financial: {
            capex: { ...this.financial.capex },
            opex: { ...this.financial.opex },
            revenue: { ...this.financial.revenue },
            financing: { ...this.financial.financing },
            tax: { ...this.financial.tax },
            discountRate: this.financial.discountRate,
            depreciationYears: this.financial.depreciationYears,
            residualRate: this.financial.residualRate,
            priceEscalation: this.financial.priceEscalation,
            efficiencyLossPct: this.financial.efficiencyLossPct,
            systemParams: { ...this.systemParams },
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
            this.financial.metrics = {
              projectIrr: data.result.financial.irr || 0,
              equityIrr: 0,
              npv: data.result.financial.npv || 0,
              lcos: data.result.financial.lcos || 0,
              dscr: { min: data.result.financial.dscr || 0, avg: data.result.financial.dscr || 0 },
              payback: data.result.financial.payback || -1,
              roi: data.result.financial.roi || 0,
            }
          }
          if (data.result.efficiencyCurves) {
            this.efficiencyCurves = data.result.efficiencyCurves
          }
          if (data.result.efficiencyDetail) {
            this.efficiencyDetail = data.result.efficiencyDetail
          }
        }
      } catch (e) {
        this.calculationError = e.message
      } finally {
        this.calculating = false
      }
    },

    async refreshFinancialResults() {
      this.financial.calculating = true
      try {
        const body = {
          totalAcUsable: [...this.results.totalAcUsable],
          financialParams: {
            capex: { ...this.financial.capex },
            opex: { ...this.financial.opex },
            revenue: { ...this.financial.revenue },
            financing: { ...this.financial.financing },
            tax: { ...this.financial.tax },
            discountRate: this.financial.discountRate,
            depreciationYears: this.financial.depreciationYears,
            residualRate: this.financial.residualRate,
            priceEscalation: this.financial.priceEscalation,
            efficiencyLossPct: this.financial.efficiencyLossPct,
            cyclesPerDay: this.systemParams.cyclesPerDay,
            systemParams: { ...this.systemParams },
          },
        }
        const res = await fetch('/api/financial/calculate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
        })
        if (!res.ok) {
          const err = await res.json()
          throw new Error(err.message || 'Financial calculation failed')
        }
        const json = await res.json()
        if (json.success && json.data) {
          this.financial.metrics = { ...json.data.metrics }
          this.financial.cashflowTable = json.data.cashflowTable || []
          this.financial.capexBreakdown = json.data.capexBreakdown || { equipment: 0, epc: 0, development: 0 }
        }
      } catch (e) {
        console.error('Financial calculation failed:', e)
      } finally {
        this.financial.calculating = false
      }
    },

    async fetchBoqItems(projectId) {
      try {
        const isAlt = this.boq.activeVersion === 'alternative'
        const res = await fetch(`/api/boq/items?project_id=${projectId}&is_alternative=${isAlt}`)
        if (res.ok) {
          const json = await res.json()
          if (json.success) {
            this.boq.items = json.data
            this.boq.totalPrice = json.data.reduce((sum, item) => sum + (item.total_price || 0), 0)
          }
        }
      } catch (e) {
        console.error('Failed to fetch BOQ items:', e)
      }
    },

    async saveBoqItems(projectId) {
      try {
        const payload = {
          projectId,
          isAlternative: this.boq.activeVersion === 'alternative',
          items: this.boq.items.map((item, index) => ({
            id: item.id,
            sectionCode: item.section_code || item.sectionCode || '',
            seq: item.seq || index + 1,
            name: item.name || '',
            spec: item.spec || '',
            unit: item.unit || '',
            quantity: item.quantity || 0,
            unitPrice: item.unit_price || item.unitPrice || 0,
            totalPrice: item.total_price || item.totalPrice || 0,
            note: item.note || '',
            version: item.version || 1,
          })),
        }
        const res = await fetch('/api/boq/items', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        })
        if (!res.ok) throw new Error('Failed to save BOQ items')
        const json = await res.json()
        if (json.success) {
          this.boq.items = json.data
          this.boq.totalPrice = json.data.reduce((sum, item) => sum + (item.total_price || 0), 0)
        }
      } catch (e) {
        console.error('Failed to save BOQ items:', e)
      }
    },

    async aggregateCapexFromBoq() {
      try {
        const payload = {
          boqItems: this.boq.items.map(item => ({
            section_code: item.section_code || item.sectionCode || '',
            total_price: item.total_price || item.totalPrice || (item.quantity || 0) * (item.unit_price || item.unitPrice || 0),
          })),
        }
        const res = await fetch('/api/financial/capex-from-boq', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        })
        if (res.ok) {
          const json = await res.json()
          if (json.success) {
            this.financial.capex = { ...json.data }
          }
        }
      } catch (e) {
        console.error('Failed to aggregate CAPEX from BOQ:', e)
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
