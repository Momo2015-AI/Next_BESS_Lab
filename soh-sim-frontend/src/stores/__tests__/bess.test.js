import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useBessStore } from '../bess.js'

// Mock the api service - the store imports { post, get, put }
vi.mock('../../services/api.js', () => ({
  post: vi.fn(),
  get: vi.fn(),
  put: vi.fn(),
  del: vi.fn(),
}))

import { post, get } from '../../services/api.js'

// Helper: creates an array of length 26 filled with a value
function arr26(val = 0) {
  return Array.from({ length: 26 }, () => val)
}

describe('bess store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  describe('runSimulationEngine()', () => {
    it('calls POST /api/simulation/run and POST /api/financial/calculate, updates store', async () => {
      const store = useBessStore()

      // Mock simulation response (uses {success, data} pattern)
      post.mockResolvedValueOnce({
        success: true,
        data: {
          soh: arr26(95),
          rte: arr26(96),
          dod: arr26(80),
          augQty: arr26(0),
          initGross: arr26(1000),
          initAux: arr26(50),
          initAcUsable: arr26(950),
          augGross: arr26(0),
          augAux: arr26(0),
          augAcUsable: arr26(0),
          augAccumQty: arr26(0),
          totalAcUsable: arr26(950),
          meetsReq: arr26(true),
        },
      })

      // Mock financial response
      post.mockResolvedValueOnce({
        success: true,
        data: {
          metrics: { npv: 1000000, irr: 12.5, lcos: 0.08 },
          cashflowTable: [],
          capexBreakdown: { equipment: 5000000, epc: 2000000, development: 1000000 },
        },
      })

      await store.runSimulationEngine(
        { container: { model: 'B-20FT' }, pcs: { model: 'PCS-500' }, containerQty: 10 },
        { temperature: 25, cyclesPerDay: 1, dod: 0.8 },
        {}
      )

      expect(post).toHaveBeenCalledWith('/api/simulation/run', expect.any(Object))
      expect(post).toHaveBeenCalledWith('/api/financial/calculate', expect.any(Object))
      expect(store.calculating).toBe(false)
      expect(store.degradation.soh).toHaveLength(26)
      expect(store.degradation.soh[0]).toBe(95)
      expect(store.results.initAcUsable[0]).toBe(950)
      expect(store.financial.metrics.npv).toBe(1000000)
    })

    it('sets calculationError when simulation fails', async () => {
      const store = useBessStore()

      post.mockRejectedValueOnce(new Error('仿真引擎内部错误'))

      await expect(
        store.runSimulationEngine(
          { container: {}, pcs: {}, containerQty: 5 },
          { temperature: 25 },
          {}
        )
      ).rejects.toThrow('仿真引擎内部错误')

      expect(store.calculating).toBe(false)
      expect(store.calculationError).toBe('仿真引擎内部错误')
    })

    it('sets calculationError when simulation response is not successful', async () => {
      const store = useBessStore()

      post.mockResolvedValueOnce({
        success: false,
        message: 'Simulation engine failed',
        data: null,
      })

      await expect(
        store.runSimulationEngine(
          { container: {}, pcs: {}, containerQty: 5 },
          { temperature: 25 },
          {}
        )
      ).rejects.toThrow('Simulation engine failed')

      expect(store.calculating).toBe(false)
      expect(store.calculationError).toBe('Simulation engine failed')
    })

    it('skips financial when options.skipFinancial is true', async () => {
      const store = useBessStore()

      post.mockResolvedValueOnce({
        success: true,
        data: {
          soh: arr26(95),
          rte: arr26(96),
          dod: arr26(80),
          augQty: arr26(0),
          initGross: arr26(1000),
          initAux: arr26(50),
          initAcUsable: arr26(950),
          augGross: arr26(0),
          augAux: arr26(0),
          augAcUsable: arr26(0),
          augAccumQty: arr26(0),
          totalAcUsable: arr26(950),
          meetsReq: arr26(true),
        },
      })

      await store.runSimulationEngine(
        { container: {}, pcs: {}, containerQty: 5 },
        { temperature: 25 },
        { skipFinancial: true }
      )

      expect(post).toHaveBeenCalledTimes(1) // Only simulation, not financial
      expect(post).toHaveBeenCalledWith('/api/simulation/run', expect.any(Object))
      expect(store.calculating).toBe(false)
    })

    it('handles financial failure gracefully while keeping simulation results', async () => {
      const store = useBessStore()

      post.mockResolvedValueOnce({
        success: true,
        data: {
          soh: arr26(95),
          rte: arr26(96),
          dod: arr26(80),
          augQty: arr26(0),
          initGross: arr26(1000),
          initAux: arr26(50),
          initAcUsable: arr26(950),
          augGross: arr26(0),
          augAux: arr26(0),
          augAcUsable: arr26(0),
          augAccumQty: arr26(0),
          totalAcUsable: arr26(950),
          meetsReq: arr26(true),
        },
      })

      // Financial call fails
      post.mockRejectedValueOnce(new Error('Financial engine error'))

      await expect(
        store.runSimulationEngine(
          { container: {}, pcs: {}, containerQty: 5 },
          { temperature: 25 },
          {}
        )
      ).rejects.toThrow('Financial engine error')

      expect(post).toHaveBeenCalledTimes(2)
      // Simulation results should still be applied
      expect(store.degradation.soh).toHaveLength(26)
      expect(store.calculating).toBe(false)
      expect(store.calculationError).toBe('Financial engine error')
    })
  })

  describe('runDesignEngine()', () => {
    it('calls POST /api/design/auto and returns data', async () => {
      const store = useBessStore()

      const designData = {
        solutions: [
          { id: 'sol-1', container: { model: 'B-20FT' }, estimatedCapex: 5000000 },
          { id: 'sol-2', container: { model: 'B-40FT' }, estimatedCapex: 4500000 },
        ],
        strategy: 'balanced',
      }

      post.mockResolvedValueOnce({
        success: true,
        data: designData,
      })

      const result = await store.runDesignEngine({ energy: 1000, duration: 2 }, 'balanced')

      expect(post).toHaveBeenCalledWith('/api/design/auto', {
        survey_params: { energy: 1000, duration: 2 },
        strategy: 'balanced',
      })
      expect(result).toEqual(designData)
      expect(store.calculating).toBe(false)
    })

    it('uses default strategy "economic" when not provided', async () => {
      const store = useBessStore()

      post.mockResolvedValueOnce({
        success: true,
        data: { solutions: [] },
      })

      await store.runDesignEngine({ energy: 500 })

      expect(post).toHaveBeenCalledWith('/api/design/auto', {
        survey_params: { energy: 500 },
        strategy: 'economic',
      })
    })

    it('throws and sets calculationError on failure', async () => {
      const store = useBessStore()

      post.mockRejectedValueOnce(new Error('Design engine error'))

      await expect(
        store.runDesignEngine({ energy: 1000 })
      ).rejects.toThrow('Design engine error')

      expect(store.calculating).toBe(false)
      expect(store.calculationError).toBe('Design engine error')
    })
  })

  describe('runFullWorkflow()', () => {
    it('calls POST /api/workflow/full and applies results to store', async () => {
      const store = useBessStore()

      const workflowData = {
        solutions: [],
        recommendation: {
          id: 'rec-1',
          design: {
            container: { model: 'B-20FT', ratedEnergyMwh: 5, cellModel: 'CELL-A' },
            pcs: { model: 'PCS-500', ratedPowerMW: 2.5 },
            containerQty: 10,
            pcsQty: 2,
            duration: 2,
            estimatedCapex: {
              equipmentCost: 5000000,
              epcCost: 2000000,
              developmentCost: 1000000,
            },
          },
          simulation: {
            soh: arr26(95),
            rte: arr26(96),
            dod: arr26(80),
            augQty: arr26(0),
            initGross: arr26(1000),
            initAux: arr26(50),
            initAcUsable: arr26(950),
            augGross: arr26(0),
            augAux: arr26(0),
            augAcUsable: arr26(0),
            augAccumQty: arr26(0),
            totalAcUsable: arr26(950),
            meetsReq: arr26(true),
          },
          financial: {
            metrics: { npv: 1000000, irr: 12.5, lcos: 0.08 },
            cashflowTable: [],
            capexBreakdown: { equipment: 5000000, epc: 2000000, development: 1000000 },
          },
        },
      }

      post.mockResolvedValueOnce({
        success: true,
        data: workflowData,
      })

      const result = await store.runFullWorkflow(
        { energy: 1000, temperature: 25 },
        'economic',
        'lcos'
      )

      expect(post).toHaveBeenCalledWith('/api/workflow/full', {
        survey_params: { energy: 1000, temperature: 25 },
        strategy: 'economic',
        target_metric: 'lcos',
      })
      expect(result).toEqual(workflowData)
      expect(store.calculating).toBe(false)
      expect(store.degradation.soh).toHaveLength(26)
      expect(store.financial.metrics.npv).toBe(1000000)
      expect(store.systemParams.initContainerQty).toBe(10)
      expect(store.selectedProducts.container).toBe('B-20FT')
      expect(store.financial.capex.equipment).toBe(5000000)
    })

    it('uses default strategy and targetMetric when not provided', async () => {
      const store = useBessStore()

      post.mockResolvedValueOnce({
        success: true,
        data: {
          recommendation: {
            design: { container: {}, pcs: {}, containerQty: 5 },
            simulation: { soh: arr26(95) },
            financial: { metrics: { npv: 500000 } },
          },
        },
      })

      await store.runFullWorkflow({ energy: 500 })

      expect(post).toHaveBeenCalledWith('/api/workflow/full', {
        survey_params: { energy: 500 },
        strategy: 'economic',
        target_metric: 'lcos',
      })
    })

    it('handles error when response.success is false', async () => {
      const store = useBessStore()

      post.mockResolvedValueOnce({
        success: false,
        data: null,
      })

      // When success is false, the method returns undefined (no throw)
      const result = await store.runFullWorkflow({ energy: 1000 })

      expect(result).toBeUndefined()
      expect(store.calculating).toBe(false)
    })

    it('throws and sets calculationError on network failure', async () => {
      const store = useBessStore()

      post.mockRejectedValueOnce(new Error('Network error'))

      await expect(
        store.runFullWorkflow({ energy: 1000 })
      ).rejects.toThrow('Network error')

      expect(store.calculating).toBe(false)
      expect(store.calculationError).toBe('Network error')
    })

    it('does not apply results when recommendation is missing', async () => {
      const store = useBessStore()

      post.mockResolvedValueOnce({
        success: true,
        data: { solutions: [] }, // no recommendation
      })

      const result = await store.runFullWorkflow({ energy: 1000 })

      expect(result).toEqual({ solutions: [] })
      // Store state should remain unchanged
      expect(store.systemParams.initContainerQty).toBe(10) // default
    })
  })
})
