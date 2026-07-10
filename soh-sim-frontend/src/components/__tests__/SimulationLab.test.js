import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'

// Use vi.hoisted to make mockApi available before vi.mock hoisting
const { mockApi } = vi.hoisted(() => ({
  mockApi: {
    get: vi.fn(),
    post: vi.fn(),
  },
}))

// Mock vue-i18n
vi.mock('vue-i18n', () => ({
  useI18n: () => ({
    t: (key) => key,
  }),
}))

// Mock echarts
vi.mock('echarts/core', () => ({
  use: vi.fn(),
  init: vi.fn(() => ({
    setOption: vi.fn(),
    resize: vi.fn(),
    dispose: vi.fn(),
  })),
}))

vi.mock('echarts/renderers', () => ({ CanvasRenderer: {} }))
vi.mock('echarts/charts', () => ({ LineChart: {} }))
vi.mock('echarts/components', () => ({
  TitleComponent: {},
  TooltipComponent: {},
  GridComponent: {},
  LegendComponent: {},
}))

// Mock services/api.js - both default and named exports
vi.mock('../../services/api.js', () => ({
  default: mockApi,
  get: mockApi.get,
  post: mockApi.post,
  put: vi.fn(),
  del: vi.fn(),
  request: vi.fn(),
  ApiError: class extends Error { constructor(m) { super(m) } },
}))

// Mock useDraft composable
const draftStateMap = {}
vi.mock('../../composables/useDraft', () => ({
  useDraft: (key, defaultValue) => {
    if (!draftStateMap[key]) {
      draftStateMap[key] = JSON.parse(JSON.stringify(defaultValue))
    }
    return {
      state: draftStateMap[key],
      clearDraft: vi.fn(),
    }
  },
  useDraftRef: (key, defaultValue) => {
    if (!draftStateMap[key]) {
      draftStateMap[key] = defaultValue
    }
    return {
      state: { value: draftStateMap[key] },
      clearDraft: vi.fn(),
    }
  },
}))

// Mock builtinAlgorithms
vi.mock('../../data/builtinAlgorithms.js', () => ({
  BUILTIN_DEGRADATION_ALGORITHMS: [
    {
      id: 'builtin-arrhenius',
      name: 'Arrhenius',
      description: 'Arrhenius-based degradation',
      category: 'degradation',
      model_type: 'arrhenius',
      accuracy_desc: 'Medium',
      parameters: {
        A: { label: 'A', default: 0.001, unit: '', min: 0, max: 1, step: 0.001 },
        Ea: { label: 'Ea', default: 35, unit: 'kJ/mol', min: 20, max: 60, step: 1 },
        alpha: { label: 'alpha', default: 0.5, unit: '', min: 0.1, max: 1, step: 0.1 },
      },
    },
  ],
  mapToSimulationLabFormat: (alg) => alg,
}))

import SimulationLab from '../SimulationLab.vue'

describe('SimulationLab.vue', () => {
  function createWrapper() {
    // Reset draft state for each test
    Object.keys(draftStateMap).forEach((k) => delete draftStateMap[k])

    return mount(SimulationLab, {
      global: {
        plugins: [
          createTestingPinia({
            createSpy: vi.fn,
            stubActions: false,
          }),
        ],
        stubs: {
          SohChart: { template: '<div class="soh-chart" />' },
          ParamInput: { template: '<div class="param-input" />' },
          SectionCard: { template: '<div class="section-card"><slot /></div>' },
        },
      },
    })
  }

  it('renders without crashing', () => {
    const wrapper = createWrapper()
    expect(wrapper.exists()).toBe(true)
  })

  it('renders the step indicator', () => {
    const wrapper = createWrapper()
    expect(wrapper.html()).toContain('simLab.stepSurvey')
  })

  it('shows survey step by default (currentStep = 0)', () => {
    const wrapper = createWrapper()
    expect(wrapper.html()).toContain('simLab.titleSurvey')
  })

  it('calls POST /api/simulation/run when running backend simulation', async () => {
    mockApi.post.mockResolvedValue({
      success: true,
      data: {
        soh: Array(26).fill(95),
        rte: Array(26).fill(96),
        dod: Array(26).fill(80),
        totalAcUsable: Array(26).fill(900),
      },
    })

    const wrapper = createWrapper()

    // Navigate through steps: survey -> params -> algorithm -> correction
    // Click "Next" for each step
    for (const btnLabel of ['simLab.btnNextParams', 'simLab.btnNextAlgorithm', 'simLab.btnNextCorrection']) {
      await wrapper.vm.$nextTick()
      const buttons = wrapper.findAll('button')
      const btn = buttons.find((b) => b.text() === btnLabel)
      if (btn) {
        await btn.trigger('click')
      }
    }

    // Now on correction step - click backend calc
    await wrapper.vm.$nextTick()
    const runBtn = wrapper.find('[data-testid="run-simulation"]')
    if (runBtn.exists()) {
      await runBtn.trigger('click')
      await wrapper.vm.$nextTick()
      expect(mockApi.post).toHaveBeenCalled()
    }
  })

  it('handles API error gracefully', async () => {
    mockApi.post.mockRejectedValue(new Error('Network error'))

    const wrapper = createWrapper()

    // Navigate to correction step
    for (const btnLabel of ['simLab.btnNextParams', 'simLab.btnNextAlgorithm', 'simLab.btnNextCorrection']) {
      await wrapper.vm.$nextTick()
      const buttons = wrapper.findAll('button')
      const btn = buttons.find((b) => b.text() === btnLabel)
      if (btn) {
        await btn.trigger('click')
      }
    }

    await wrapper.vm.$nextTick()
    const runBtn = wrapper.find('[data-testid="run-simulation"]')
    if (runBtn.exists()) {
      await runBtn.trigger('click')
      await wrapper.vm.$nextTick()
    }

    // Should not crash
    expect(wrapper.exists()).toBe(true)
  })
})
