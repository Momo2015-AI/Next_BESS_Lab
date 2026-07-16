import { defineStore } from 'pinia'
import { get, post, put } from '../services/api.js'
import { NUM_YEARS } from '../constants.js'

// 全系统立项 DoD（放电深度）默认百分比。所有模块应从 store.survey.dod 取值，
// 仅在无 survey 数据时回退到本常量，确保"改一处即全局联动"。
export const DEFAULT_DOD = 90

// ---------------------------------------------------------------------------
// 单一数据源（Single Source of Truth）
// 全系统立项/设计默认参数集中定义于此。所有组件的表单初始值与 fallback
// (`|| 25` 之类) 都应引用这里，禁止再在各文件写死字面量，确保"改一处即全局联动"。
// ---------------------------------------------------------------------------

// Phase1 立项调研默认参数
export const DEFAULT_SURVEY = {
  projectName: '',
  location: '',
  country: '',
  city: '',
  site: '',
  lat: null,
  lng: null,
  temperature: 25, // 运行环境温度(℃)
  duration: 2, // 时长(h) = ratedEnergy / totalPower
  cyclesPerDay: 1, // 日循环次数
  dod: DEFAULT_DOD, // 放电深度(%)
  cRate: 0.5, // 倍率(1/h) = totalPower / ratedEnergy
  requiredEnergy: 240, // 需量电量(MWh)
  ratedEnergy: 5, // 单元额定电量(MWh)
  totalPower: 50, // 额定功率(MW)
  gridVoltage: '110kV',
  altitude: 0
}

// Phase2 系统设计默认参数（含仿真/质保/效率级联，均为全系统 canonical 值）
export const DEFAULT_SYSTEM_PARAMS = {
  ratedEnergy: DEFAULT_SURVEY.ratedEnergy,
  initContainerQty: 10,
  initPcsQty: 2,
  pcsPower: 5,
  duration: DEFAULT_SURVEY.duration,
  cyclesPerDay: DEFAULT_SURVEY.cyclesPerDay,
  temperature: DEFAULT_SURVEY.temperature,
  requiredEnergy: DEFAULT_SURVEY.requiredEnergy,
  // 效率级联组
  acEfficiency: 97.03, // 交流侧效率(%)
  dcEfficiency: 98.5, // 直流侧效率(%)
  initRte: 94.1, // 初始往返效率(%)
  selfDischarge: 2, // 自放电(%)
  // 辅助功耗组
  bessAuxRun: 18.124,
  bessAuxStandby: 3.5,
  pcsAuxRun: 6.5,
  pcsAuxStandby: 1.0,
  auxPowerMode: 'manual', // 'manual' | 'thermal'
  coolingType: 'liquid', // 'forced-air' | 'liquid' | 'SiC-liquid'
  ambientTemp: 25, // 环境温度(℃) — thermal 模式使用
  // 退化/质保/投影年限组
  simulationYears: 25, // 投影运行年数(第0年为投产年，时间序列长度为 NUM_YEARS)
  guaranteeYears: 10, // 质保年限
  guaranteeSoh: 70 // 质保末端 SOH(%)
}

// 物理推导助手：能量-功率-时长-倍率-需量本质是同一系统的不同表达，应互推而非各填各的。
export const deriveDuration = (ratedEnergy, totalPower) =>
  totalPower && ratedEnergy != null ? +(ratedEnergy / totalPower).toFixed(3) : DEFAULT_SURVEY.duration
export const deriveCRate = (ratedEnergy, totalPower) =>
  ratedEnergy && totalPower != null ? +(totalPower / ratedEnergy).toFixed(3) : DEFAULT_SURVEY.cRate
export const deriveRequiredEnergy = (ratedEnergy, dod = DEFAULT_DOD) =>
  ratedEnergy != null ? +(ratedEnergy * (dod / 100)).toFixed(1) : DEFAULT_SURVEY.requiredEnergy

function create26Array(defaultVal = 0) {
  return Array.from({ length: NUM_YEARS }, () => defaultVal)
}

export const useBessStore = defineStore('bess', {
  state: () => ({
    project: {
      id: null,
      name: '',
      status: 'draft'
    },
    survey: { ...DEFAULT_SURVEY },
    systemParams: { ...DEFAULT_SYSTEM_PARAMS },
    selectedProducts: {
      cell: null,
      container: null,
      pcs: null
    },
    batteryHierarchy: {
      // 层级配置
      cellModel: '',
      packModel: '',
      rackModel: '',
      clusterModel: '',
      containerModel: '',
      // 电芯参数
      cellVoltage: 3.2,
      cellCapacityAh: 280,
      // Pack 层级
      seriesPerPack: 52,
      parallelPerPack: 1,
      packVoltage: 0,
      packEnergykWh: 0,
      // Rack 层级
      packsPerRack: 8,
      rackVoltage: 0,
      rackEnergykWh: 0,
      // Cluster 层级
      racksPerCluster: 1,
      clusterVoltage: 0,
      clusterEnergykWh: 0,
      // Container 层级
      clustersPerContainer: 12,
      containerEnergyMWh: 5.0,
      // DC 容量推导 (DEWA §6.2)
      targetPowerMW: 260,
      targetEnergyMWh: 1560,
      pRate: 0.167,
      dodPercent: 90,
      voltageMismatchLoss: 1,
      oemDesignMargin: 3,
      sohInitial: 100,
      // 计算结果
      deltaPercent: 0,
      dcFunctionalMWh: 0,
      dcInstalledMWh: 0,
      requiredContainers: 0,
      // 来源标记
      source: 'manual' // 'manual' | 'hierarchy'
    },
    degradation: {
      soh: create26Array(1.0),
      rte: create26Array(97.03),
      dod: create26Array(100),
      augQty: create26Array(0)
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
      meetsReq: create26Array(false)
    },
    financial: {
      capex: { equipment: 0, epc: 0, development: 0 },
      opex: {
        maintenance: 0,
        insurance: 0,
        grid: 0,
        landLease: 0,
        fixedOpexPerMW: 5000,
        variableOpexPerMWh: 2.5,
        insuranceRate: 0.5
      },
      revenue: {
        arbitrage: { enabled: true, offPeakPrice: 30, peakPrice: 60, spreadCapture: 85, operatingDays: 330 },
        capacity: { enabled: true, capacityPrice: 45000 },
        ancillary: { enabled: true, ancillaryPrice: 15000 },
        ppa: { enabled: true, ppaPrice: 55, escalation: 2.0 },
        capacityAuction: { enabled: true, auctionPrice: 120000, contractYears: 5 }
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
      calculating: false
    },
    boq: {
      items: [],
      activeVersion: 'main',
      totalPrice: 0
    },
    exports: {
      reportGenerated: false,
      bomGenerated: false,
      reportDownloadUrl: ''
    },
    phases: {
      phase1: { status: 'pending' },
      phase2: { status: 'pending' },
      phase3: { status: 'pending' },
      phase4: { status: 'pending' },
      phase5: { status: 'pending' }
    },
    calculating: false,
    calculationError: null,
    efficiencyFactors: [],
    efficiencyCurves: null,
    efficiencyDetail: null,
    degradationModel: 'arrhenius',
    gb36276Curves: [],
    // Phase2 设计结果缓存（解决返回设计页面数据丢失问题）
    designResults: {
      solutions: [], // 设计方案列表
      strategy: 'balanced', // 当前策略
      confirmedSolution: null // 用户确认的方案
    },
    // Phase3 当前步骤持久化（解决切换 tab 后步骤重置问题）
    phase3ActiveStep: 0,
    // Phase2/Phase4 当前步骤持久化
    phase2ActiveStep: 0,
    phase4ActiveStep: 0,
    environmental: {
      accelerate_temperature: true,
      accelerate_dust: false,
      accelerate_humidity: false,
      ref_temperature: 25,
      ref_humidity: 50,
      field_humidity: 65,
      dust_factor: 1.1,
      humidity_exponent: 2.5,
      activation_energy: 25000
    }
  }),

  getters: {
    simulationDefaults: (state) => ({
      duration: state.survey.duration || 2,
      cyclesPerDay: state.survey.cyclesPerDay || 1,
      requiredEnergy: state.survey.requiredEnergy || 240,
      temperature: state.survey.temperature || 25
    }),
    allPhasesComplete: (state) => Object.values(state.phases).every((p) => p.status === 'completed')
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
        const data = await get('/api/efficiency/factors')
        this.efficiencyFactors = data.data?.factors || []
      } catch (e) {
        console.error('Failed to load efficiency factors:', e)
      }
    },

    async loadDegradationConfig() {
      try {
        const [curvesData, envData] = await Promise.all([
          get('/api/degradation/gb36276-curves'),
          get('/api/degradation/environmental')
        ])
        this.gb36276Curves = curvesData.data?.curves || []
        this.environmental = envData.data?.environmental || []
      } catch (e) {
        console.error('Failed to load degradation config:', e)
      }
    },

    async updateGb36276Curves(curves) {
      const data = await put('/api/degradation/gb36276-curves', { curves })
      this.gb36276Curves = data.data?.curves || []
    },

    async resetGb36276Curves() {
      const data = await post('/api/degradation/gb36276-curves/reset')
      this.gb36276Curves = data.data?.curves || []
    },

    async updateEnvironmental(env) {
      const data = await put('/api/degradation/environmental', env)
      this.environmental = data.data?.environmental || []
    },

    async resetEnvironmental() {
      const data = await post('/api/degradation/environmental/reset')
      this.environmental = data.data?.environmental || []
    },

    async previewDegradation(params) {
      return await post('/api/degradation/preview', params)
    },

    async previewAcceleration(params) {
      return await post('/api/degradation/environmental/preview', params)
    },

    // ==================== 三引擎工作流 ====================

    /** 运行仿真引擎 → 财务引擎（新 API） */
    async runSimulationEngine(designOutput, surveyParams, options = {}) {
      this.calculating = true
      this.calculationError = null
      try {
        let sim = null
        let simResp = null

        // Step 1: 调用仿真引擎（financialOnly 模式下跳过）
        if (!options.financialOnly) {
          const simBody = {
            design_output: designOutput || {
              container: { ratedEnergyMWh: this.systemParams.ratedEnergy },
              pcs: { ratedPowerMW: this.systemParams.pcsPower },
              containerQty: this.systemParams.initContainerQty,
              pcsQty: this.systemParams.initPcsQty,
              duration: this.systemParams.duration
            },
            survey_params: surveyParams || {
              ratedEnergy: this.survey.ratedEnergy,
              temperature: this.survey.temperature,
              cyclesPerDay: this.survey.cyclesPerDay,
              dod: DEFAULT_DOD,
              requiredEnergy: this.survey.requiredEnergy,
              cRate: this.systemParams.cRate || 0.5,
              auxPowerMode: this.systemParams.auxPowerMode,
              ambientTemp: this.systemParams.ambientTemp,
              coolingType: this.systemParams.coolingType
            },
            degradation: {
              soh: [...this.degradation.soh],
              rte: [...this.degradation.rte],
              dod: [...this.degradation.dod],
              augQty: [...this.degradation.augQty]
            },
            algorithm: {
              model: this.degradationModel,
              correctionFactor: 1.0,
              environmental: { ...this.environmental },
              gb36276Curves: [...this.gb36276Curves]
            }
          }

          simResp = await post('/api/simulation/run', simBody)
          if (!simResp.success || !simResp.data) {
            throw new Error(simResp.message || 'Simulation engine failed')
          }

          sim = simResp.data

          // 写入退化结果
          this.degradation.soh = sim.soh || []
          this.degradation.rte = sim.rte || []
          this.degradation.dod = sim.dod || []
          this.degradation.augQty = sim.augQty || []

          // 写入能量核算结果
          this.results = {
            initGross: sim.initGross || create26Array(0),
            initAux: sim.initAux || create26Array(0),
            initAcUsable: sim.initAcUsable || create26Array(0),
            augGross: sim.augGross || create26Array(0),
            augAux: sim.augAux || create26Array(0),
            augAcUsable: sim.augAcUsable || create26Array(0),
            augAccumQty: sim.augAccumQty || create26Array(0),
            totalAcUsable: sim.totalAcUsable || create26Array(0),
            meetsReq: sim.meetsReq || create26Array(false)
          }

          if (sim && sim.efficiencyCurves) this.efficiencyCurves = sim.efficiencyCurves
          if (sim && sim.efficiencyDetail) this.efficiencyDetail = sim.efficiencyDetail
        } // end Step 1 (if !financialOnly)

        // Step 2: 调用财务引擎
        if (!options.skipFinancial) {
          const simTotalAcUsable = options.financialOnly
            ? this.results.totalAcUsable
            : (sim && sim.totalAcUsable) || create26Array(0)
          const simSoh = options.financialOnly ? this.degradation.soh : (sim && sim.soh) || []
          const simRte = options.financialOnly ? this.degradation.rte : (sim && sim.rte) || []
          const simMeetsReq = options.financialOnly ? this.results.meetsReq : (sim && sim.meetsReq) || []
          const finBody = {
            simulation_output: {
              totalAcUsable: simTotalAcUsable,
              soh: simSoh,
              rte: simRte,
              meetsReq: simMeetsReq
            },
            design_output: designOutput || {
              container: { ratedEnergyMWh: this.systemParams.ratedEnergy },
              pcs: { ratedPowerMW: this.systemParams.pcsPower },
              containerQty: this.systemParams.initContainerQty,
              pcsQty: this.systemParams.initPcsQty,
              duration: this.systemParams.duration
            },
            survey_params: surveyParams || {
              location: this.survey.location,
              country: this.survey.country,
              city: this.survey.city,
              site: this.survey.site,
              lat: this.survey.lat,
              lng: this.survey.lng,
              ratedEnergy: this.survey.ratedEnergy,
              totalPower: this.survey.totalPower
            },
            financial_params: {
              discountRate: this.financial.discountRate,
              depreciationYears: this.financial.depreciationYears,
              residualRate: this.financial.residualRate,
              priceEscalation: this.financial.priceEscalation,
              efficiencyLossPct: this.financial.efficiencyLossPct
            }
          }

          const finResp = await post('/api/financial/calculate', finBody)
          if (finResp.success && finResp.data) {
            const fin = finResp.data
            const m = fin.metrics || {}
            this.financial.metrics = {
              projectIrr: m.projectIrr || m.irr || 0,
              equityIrr: m.equityIrr || 0,
              npv: m.npv || 0,
              lcos: m.lcos || m.lcoe || 0,
              dscr: m.dscr || { min: 0, avg: 0 },
              payback: m.payback || m.paybackYears || -1,
              roi: m.roi || 0
            }
            this.financial.cashflowTable = fin.cashflowTable || []
            this.financial.capexBreakdown = fin.capexBreakdown || { equipment: 0, epc: 0, development: 0 }
          }
        }

        return sim || simResp?.data
      } catch (e) {
        this.calculationError = e.message
        throw e
      } finally {
        this.calculating = false
      }
    },

    async fetchBoqItems(projectId) {
      try {
        const isAlt = this.boq.activeVersion === 'alternative'
        const json = await get(`/api/boq/items?project_id=${projectId}&is_alternative=${isAlt}`)
        if (json.success) {
          this.boq.items = json.data
          this.boq.totalPrice = json.data.reduce((sum, item) => sum + (item.total_price || 0), 0)
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
            version: item.version || 1
          }))
        }
        const json = await post('/api/boq/items', payload)
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
          boqItems: this.boq.items.map((item) => ({
            section_code: item.section_code || item.sectionCode || '',
            total_price:
              item.total_price || item.totalPrice || (item.quantity || 0) * (item.unit_price || item.unitPrice || 0)
          }))
        }
        const json = await post('/api/financial/capex-from-boq', payload)
        if (json.success) {
          this.financial.capex = { ...json.data }
        }
      } catch (e) {
        console.error('Failed to aggregate CAPEX from BOQ:', e)
      }
    },

    async loadProject(id) {
      try {
        const data = await get(`/api/projects/${id}`)
        this.project = data.data?.project || this.project
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
        phase5: { status: 'pending' }
      }
    },

    // ==================== 三引擎工作流 ====================

    /** 一键执行完整工作流（设计 → 仿真 → 财务） */
    async runFullWorkflow(surveyParams, strategy = 'economic', targetMetric = 'lcos') {
      this.calculating = true
      this.calculationError = null
      try {
        const resp = await post('/api/workflow/full', {
          survey_params: surveyParams || {
            ratedEnergy: this.survey.ratedEnergy,
            totalPower: this.survey.totalPower,
            duration: this.survey.duration,
            temperature: this.survey.temperature,
            cyclesPerDay: this.survey.cyclesPerDay,
            dod: DEFAULT_DOD,
            requiredEnergy: this.survey.requiredEnergy,
            location: this.survey.location,
            country: this.survey.country,
            city: this.survey.city,
            site: this.survey.site,
            lat: this.survey.lat,
            lng: this.survey.lng
          },
          strategy,
          target_metric: targetMetric
        })
        if (resp.success && resp.data) {
          this._applyWorkflowResult(resp.data)
          return resp.data
        }
      } catch (e) {
        this.calculationError = e.message
        throw e
      } finally {
        this.calculating = false
      }
    },

    /** 应用工作流结果到 store */
    _applyWorkflowResult(data) {
      const rec = data.recommendation
      if (!rec) return

      // 应用设计方案
      if (rec.design) {
        const d = rec.design
        this.systemParams = {
          ...this.systemParams,
          ratedEnergy: d.container?.ratedEnergyMWh || this.systemParams.ratedEnergy,
          initContainerQty: d.containerQty || this.systemParams.initContainerQty,
          initPcsQty: d.pcsQty || this.systemParams.initPcsQty,
          pcsPower: d.pcs?.ratedPowerMW || this.systemParams.pcsPower,
          duration: d.duration || this.systemParams.duration
        }
        this.selectedProducts = {
          cell: d.container?.cellModel || null,
          container: d.container?.model || null,
          pcs: d.pcs?.model || null
        }
        if (d.estimatedCapex) {
          this.financial.capex = {
            equipment: d.estimatedCapex.equipmentCost || 0,
            epc: d.estimatedCapex.epcCost || 0,
            development: d.estimatedCapex.developmentCost || 0
          }
        }
      }

      // 应用仿真结果
      if (rec.simulation) {
        const sim = rec.simulation
        this.results = {
          initGross: sim.initGross || [],
          initAux: sim.initAux || [],
          initAcUsable: sim.initAcUsable || [],
          augGross: sim.augGross || [],
          augAux: sim.augAux || [],
          augAcUsable: sim.augAcUsable || [],
          augAccumQty: sim.augAccumQty || [],
          totalAcUsable: sim.totalAcUsable || [],
          meetsReq: sim.meetsReq || []
        }
        this.degradation.soh = sim.soh || []
        this.degradation.rte = sim.rte || []
        this.degradation.dod = sim.dod || []
        this.degradation.augQty = sim.augQty || []
        if (sim.efficiencyCurves) this.efficiencyCurves = sim.efficiencyCurves
        if (sim.efficiencyDetail) this.efficiencyDetail = sim.efficiencyDetail
      }

      // 应用财务结果
      if (rec.financial?.metrics) {
        const m = rec.financial.metrics
        this.financial.metrics = {
          projectIrr: m.projectIrr || m.irr || 0,
          equityIrr: m.equityIrr || 0,
          npv: m.npv || 0,
          lcos: m.lcos || m.lcoe || 0,
          dscr: m.dscr || { min: 0, avg: 0 },
          payback: m.payback || -1,
          roi: m.roi || 0
        }
        this.financial.cashflowTable = rec.financial.cashflowTable || []
        this.financial.capexBreakdown = rec.financial.capexBreakdown || { equipment: 0, epc: 0, development: 0 }
        if (rec.financial.revenueModel) {
          this.financial.revenue = { ...this.financial.revenue, ...rec.financial.revenueModel }
        }
        if (rec.financial.sensitivity) {
          this.financial.sensitivity = rec.financial.sensitivity
        }
      }
    },

    /** 运行设计引擎（仅设计） */
    async runDesignEngine(surveyParams, strategy = 'economic') {
      this.calculating = true
      this.calculationError = null
      try {
        const resp = await post('/api/design/auto', {
          survey_params: surveyParams,
          strategy
        })
        if (resp.success && resp.data) {
          return resp.data
        }
      } catch (e) {
        this.calculationError = e.message
        throw e
      } finally {
        this.calculating = false
      }
    },

    /** 运行 What-If 分析 */
    async runWhatIf(baseDesign, adjustments, surveyParams) {
      try {
        const resp = await post('/api/workflow/what-if', {
          base_design: baseDesign,
          adjustments,
          survey_params: surveyParams
        })
        if (resp.success && resp.data) {
          return resp.data
        }
      } catch (e) {
        console.error('What-If analysis failed:', e)
        throw e
      }
    },

    /** 保存工作流结果为版本 */
    async saveWorkflowAsVersion(projectId, surveyParams, strategy, targetMetric) {
      try {
        const resp = await post('/api/workflow/full', {
          survey_params: surveyParams || {
            ratedEnergy: this.survey.ratedEnergy,
            totalPower: this.survey.totalPower,
            duration: this.survey.duration,
            temperature: this.survey.temperature,
            cyclesPerDay: this.survey.cyclesPerDay,
            dod: DEFAULT_DOD,
            requiredEnergy: this.survey.requiredEnergy,
            location: this.survey.location,
            country: this.survey.country,
            city: this.survey.city,
            site: this.survey.site,
            lat: this.survey.lat,
            lng: this.survey.lng
          },
          strategy: strategy || 'economic',
          target_metric: targetMetric || 'lcos',
          project_id: projectId
        })
        if (resp.success) {
          return resp.data
        }
      } catch (e) {
        console.error('保存方案版本失败:', e)
        throw e
      }
    },

    /** 加载版本数据到 store */
    async loadVersion(versionId) {
      try {
        const resp = await post(`/api/versions/${versionId}/restore`)
        if (resp.success) {
          const data = resp.data
          if (data.design) {
            this.selectedProducts = {
              cell: data.design.container?.cellModel || null,
              container: data.design.container?.model || null,
              pcs: data.design.pcs?.model || null
            }
            this.systemParams = {
              ...this.systemParams,
              ratedEnergy: data.design.container?.ratedEnergyMWh || this.systemParams.ratedEnergy,
              initContainerQty: data.design.containerQty || this.systemParams.initContainerQty,
              initPcsQty: data.design.pcsQty || this.systemParams.initPcsQty,
              pcsPower: data.design.pcs?.ratedPowerMW || this.systemParams.pcsPower
            }
          }
          if (data.simulation) {
            this.results = {
              initGross: data.simulation.initGross || [],
              initAux: data.simulation.initAux || [],
              initAcUsable: data.simulation.initAcUsable || [],
              augGross: data.simulation.augGross || [],
              augAux: data.simulation.augAux || [],
              augAcUsable: data.simulation.augAcUsable || [],
              augAccumQty: data.simulation.augAccumQty || [],
              totalAcUsable: data.simulation.totalAcUsable || [],
              meetsReq: data.simulation.meetsReq || []
            }
            this.degradation.soh = data.simulation.soh || []
            this.degradation.rte = data.simulation.rte || []
            this.degradation.dod = data.simulation.dod || []
          }
          if (data.financial?.metrics) {
            const m = data.financial.metrics
            this.financial.metrics = {
              projectIrr: m.projectIrr || m.irr || 0,
              equityIrr: m.equityIrr || 0,
              npv: m.npv || 0,
              lcos: m.lcos || m.lcoe || 0,
              dscr: m.dscr || { min: 0, avg: 0 },
              payback: m.payback || -1,
              roi: m.roi || 0
            }
          }
          return data
        }
      } catch (e) {
        console.error('版本回溯失败:', e)
        throw e
      }
    },

    /** 对比两个版本 */
    async compareVersions(versionIds) {
      try {
        const resp = await post('/api/versions/compare', { version_ids: versionIds })
        if (resp.success) {
          return resp.data
        }
      } catch (e) {
        console.error('版本对比失败:', e)
        throw e
      }
    }
  },
  persist: { storage: localStorage }
})
