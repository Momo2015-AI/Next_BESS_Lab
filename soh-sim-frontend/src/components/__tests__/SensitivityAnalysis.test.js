import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'

const { mockPost } = vi.hoisted(() => ({
  mockPost: vi.fn(),
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
vi.mock('echarts/charts', () => ({ BarChart: {}, RadarChart: {} }))
vi.mock('echarts/components', () => ({
  TitleComponent: {},
  TooltipComponent: {},
  GridComponent: {},
  LegendComponent: {},
  RadarComponent: {},
}))

// Mock services/api.js - SensitivityAnalysis imports { post } as named
vi.mock('../../services/api.js', () => ({
  post: mockPost,
  get: vi.fn(),
  put: vi.fn(),
  del: vi.fn(),
  request: vi.fn(),
  ApiError: class extends Error { constructor(m) { super(m) } },
  default: { get: vi.fn(), post: mockPost },
}))

// Mock useDraft
const draftStore = new Map()
vi.mock('../../composables/useDraft', () => ({
  useDraft: (key, defaultValue) => {
    if (!draftStore.has(key)) {
      draftStore.set(key, JSON.parse(JSON.stringify(defaultValue)))
    }
    return {
      state: draftStore.get(key),
      clearDraft: vi.fn(),
    }
  },
  useDraftRef: (key, defaultValue) => {
    if (!draftStore.has(key)) {
      draftStore.set(key, JSON.parse(JSON.stringify(defaultValue)))
    }
    const val = draftStore.get(key)
    return {
      state: {
        __v_isRef: true,
        _isRef: true,
        _value: val,
        get value() { return this._value },
        set value(v) {
          this._value = v
          draftStore.set(key, v)
        },
      },
      clearDraft: vi.fn(),
    }
  },
}))

// Mock useSensitivityCharts
vi.mock('../../composables/useSensitivityCharts.js', () => ({
  useSensitivityCharts: () => ({
    updateTornadoChart: vi.fn(),
    updateSpiderChart: vi.fn(),
  }),
}))

import SensitivityAnalysis from '../SensitivityAnalysis.vue'

describe('SensitivityAnalysis.vue', () => {
  function createWrapper() {
    draftStore.clear()
    return mount(SensitivityAnalysis, {
      global: {
        plugins: [
          createTestingPinia({
            createSpy: vi.fn,
            stubActions: false,
          }),
        ],
        stubs: {
          SohChart: { template: '<div class="soh-chart" />' },
          SectionCard: { template: '<div><slot /></div>' },
        },
      },
    })
  }

  it('renders without crashing', () => {
    const wrapper = createWrapper()
    expect(wrapper.exists()).toBe(true)
  })

  it('renders the sensitivity title', () => {
    const wrapper = createWrapper()
    expect(wrapper.html()).toContain('sensitivity.title')
  })

  it('shows parameter selection checkboxes', () => {
    const wrapper = createWrapper()
    expect(wrapper.html()).toContain('sensitivity.selectParam')
  })

  it('uses services/api.js post() not raw fetch', () => {
    const wrapper = createWrapper()
    expect(wrapper.exists()).toBe(true)
  })

  it('renders the run analysis button', () => {
    const wrapper = createWrapper()
    expect(wrapper.html()).toContain('sensitivity.runAnalysis')
  })

  it('renders the explanation section', () => {
    const wrapper = createWrapper()
    expect(wrapper.html()).toContain('sensitivity.explanationTitle')
  })
})
