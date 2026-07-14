/**
 * BESS Store 数据传递完整性测试
 *
 * 验证:
 * - API 调用参数包含所有必需字段 (auxPowerMode, ambientTemp, coolingType)
 * - API 响应正确映射到 store state
 * - 错误处理路径正常工作
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useBessStore } from '../bess'

// Mock API service
const mockPost = vi.fn()
const mockGet = vi.fn()
const mockPut = vi.fn()
const mockDel = vi.fn()

vi.mock('../../services/api.js', () => ({
  post: (...args) => mockPost(...args),
  get: (...args) => mockGet(...args),
  put: (...args) => mockPut(...args),
  del: (...args) => mockDel(...args)
}))

// Helpers
const arr26 = (val) => Array(26).fill(val)
const simResponse = (overrides = {}) => ({
  success: true,
  data: {
    soh: arr26(100),
    rte: arr26(86.5),
    dod: arr26(90),
    augQty: arr26(0),
    initGross: arr26(389),
    initAux: arr26(6.8),
    initAcUsable: arr26(382),
    augGross: arr26(0),
    augAux: arr26(0),
    augAcUsable: arr26(0),
    augAccumQty: arr26(0),
    totalAcUsable: arr26(382),
    meetsReq: arr26(true),
    efficiencyCurves: null,
    efficiencyDetail: null,
    augmentationStrategy: { strategies: {}, recommended: 'on_demand' },
    augmentationComparison: { strategies: {}, recommended: 'on_demand', comparison_summary: {} },
    ...overrides
  }
})

const finResponse = (overrides = {}) => ({
  success: true,
  data: {
    metrics: {
      projectIrr: 34.85,
      equityIrr: 145.31,
      npv: 142000000,
      lcos: 0.032,
      dscr: { min: 0.98, avg: 3.26 },
      payback: 3.0,
      roi: 251.79
    },
    cashflowTable: [],
    capexBreakdown: { equipment: 100000000, epc: 12500000, development: 2000000 },
    ...overrides
  }
})

const workflowResponse = () => ({
  success: true,
  data: {
    strategy: 'economic',
    target_metric: 'lcos',
    solutions: [],
    recommendation: {
      design: {
        container: { model: 'TEST-5MWh', ratedEnergyMwh: 5, cellModel: 'LFP-280' },
        pcs: { model: 'TEST-PCS', ratedPowerMW: 5 },
        containerQty: 100,
        pcsQty: 50,
        duration: 2,
        estimatedCapex: { equipmentCost: 100000000, epcCost: 12500000, developmentCost: 2000000 }
      },
      simulation: {
        soh: arr26(100),
        rte: arr26(86.5),
        dod: arr26(90),
        augQty: arr26(0),
        initGross: arr26(389),
        initAux: arr26(6.8),
        initAcUsable: arr26(382),
        augGross: arr26(0),
        augAux: arr26(0),
        augAcUsable: arr26(0),
        augAccumQty: arr26(0),
        totalAcUsable: arr26(382),
        meetsReq: arr26(true),
        efficiencyCurves: null,
        efficiencyDetail: null
      },
      financial: {
        metrics: {
          projectIrr: 34.85,
          equityIrr: 145.31,
          npv: 142000000,
          lcos: 0.032,
          dscr: { min: 0.98, avg: 3.26 },
          payback: 3.0,
          roi: 251.79
        },
        cashflowTable: [],
        capexBreakdown: { equipment: 100000000, epc: 12500000, development: 2000000 },
        revenueModel: { arbitrage: { enabled: true } },
        sensitivity: {}
      }
    },
    pipeline_summary: { total_solutions: 3, successful: 3, failed: 0 }
  }
})

describe('BESS Store — Data Flow', () => {
  let store

  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    store = useBessStore()
  })

  describe('runSimulationEngine — 参数传递', () => {
    it('应传递 auxPowerMode/ambientTemp/coolingType 到后端', async () => {
      mockPost.mockResolvedValueOnce(simResponse())
      mockPost.mockResolvedValueOnce(finResponse())

      // 设置 thermal 模式参数
      store.systemParams.auxPowerMode = 'thermal'
      store.systemParams.ambientTemp = 32
      store.systemParams.coolingType = 'liquid'

      await store.runSimulationEngine()

      // 验证 POST /api/simulation/run 的参数
      const simCall = mockPost.mock.calls.find((c) => c[0] === '/api/simulation/run')
      expect(simCall).toBeTruthy()
      const simBody = simCall[1]
      expect(simBody.survey_params.auxPowerMode).toBe('thermal')
      expect(simBody.survey_params.ambientTemp).toBe(32)
      expect(simBody.survey_params.coolingType).toBe('liquid')
    })

    it('应正确映射仿真响应到 store state', async () => {
      mockPost.mockResolvedValueOnce(simResponse())
      mockPost.mockResolvedValueOnce(finResponse())

      await store.runSimulationEngine()

      expect(store.degradation.soh).toHaveLength(26)
      expect(store.degradation.rte).toHaveLength(26)
      expect(store.results.totalAcUsable).toHaveLength(26)
      expect(store.results.meetsReq).toHaveLength(26)
      expect(store.results.initGross[0]).toBe(389)
    })

    it('应正确映射财务响应到 store state', async () => {
      mockPost.mockResolvedValueOnce(simResponse())
      mockPost.mockResolvedValueOnce(
        finResponse({
          metrics: {
            projectIrr: 34.85,
            equityIrr: 145.31,
            npv: 142000000,
            lcos: 0.032,
            dscr: { min: 0.98, avg: 3.26 },
            payback: 3.0,
            roi: 251.79
          }
        })
      )

      await store.runSimulationEngine()

      expect(store.financial.metrics.projectIrr).toBe(34.85)
      expect(store.financial.metrics.npv).toBe(142000000)
      expect(store.financial.metrics.dscr.avg).toBe(3.26)
      expect(store.financial.metrics.payback).toBe(3.0)
    })

    it('skipFinancial=true 时应跳过财务计算', async () => {
      mockPost.mockResolvedValueOnce(simResponse())

      await store.runSimulationEngine(null, null, { skipFinancial: true })

      // 只应调用 simulation API，不应调用 financial API
      const finCall = mockPost.mock.calls.find((c) => c[0] === '/api/financial/calculate')
      expect(finCall).toBeFalsy()
    })

    it('仿真失败时应设置 calculationError', async () => {
      mockPost.mockRejectedValueOnce(new Error('Simulation failed'))

      await expect(store.runSimulationEngine()).rejects.toThrow('Simulation failed')
      expect(store.calculationError).toBe('Simulation failed')
      expect(store.calculating).toBe(false)
    })

    it('仿真成功但财务失败时应保留仿真结果', async () => {
      mockPost.mockResolvedValueOnce(simResponse())
      mockPost.mockRejectedValueOnce(new Error('Financial failed'))

      await expect(store.runSimulationEngine()).rejects.toThrow('Financial failed')
      // 仿真结果应该已写入
      expect(store.results.totalAcUsable[0]).toBe(382)
      expect(store.calculating).toBe(false)
    })
  })

  describe('runFullWorkflow — 参数传递与响应映射', () => {
    it('应传递完整的 survey_params 到编排器', async () => {
      mockPost.mockResolvedValueOnce(workflowResponse())

      const surveyParams = {
        ratedEnergy: 100,
        totalPower: 50,
        temperature: 32,
        cyclesPerDay: 1,
        dod: 90,
        requiredEnergy: 382,
        location: 'cambodia',
        auxPowerMode: 'thermal',
        ambientTemp: 32,
        coolingType: 'liquid',
        efficiencyFactors: null
      }

      await store.runFullWorkflow(surveyParams, 'economic', 'lcos')

      const call = mockPost.mock.calls.find((c) => c[0] === '/api/workflow/full')
      expect(call).toBeTruthy()
      const body = call[1]
      expect(body.survey_params.auxPowerMode).toBe('thermal')
      expect(body.survey_params.ambientTemp).toBe(32)
      expect(body.survey_params.coolingType).toBe('liquid')
      expect(body.strategy).toBe('economic')
      expect(body.target_metric).toBe('lcos')
    })

    it('应正确展开 recommendation 到 store state', async () => {
      mockPost.mockResolvedValueOnce(workflowResponse())

      await store.runFullWorkflow({ ratedEnergy: 100, totalPower: 50 }, 'economic', 'lcos')

      // design → systemParams
      expect(store.systemParams.initContainerQty).toBe(100)
      expect(store.systemParams.initPcsQty).toBe(50)
      expect(store.systemParams.pcsPower).toBe(5)

      // simulation → results
      expect(store.results.totalAcUsable[0]).toBe(382)

      // financial → financial.metrics
      expect(store.financial.metrics.projectIrr).toBe(34.85)
      expect(store.financial.capexBreakdown.equipment).toBe(100000000)
    })
  })

  describe('runDesignEngine — 参数传递', () => {
    it('应传递 survey_params 到设计引擎', async () => {
      mockPost.mockResolvedValueOnce({
        success: true,
        data: { solutions: [], recommendation: {} }
      })

      await store.runDesignEngine({ ratedEnergy: 100, totalPower: 50 }, 'economic')

      const call = mockPost.mock.calls.find((c) => c[0] === '/api/design/auto')
      expect(call).toBeTruthy()
      expect(call[1].survey_params.ratedEnergy).toBe(100)
      expect(call[1].strategy).toBe('economic')
    })
  })
})
