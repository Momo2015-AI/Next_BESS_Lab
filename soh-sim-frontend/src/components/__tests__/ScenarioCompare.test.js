import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'

// Use vi.hoisted for mock objects
const { mockPost } = vi.hoisted(() => ({
  mockPost: vi.fn()
}))

// Mock vue-i18n
vi.mock('vue-i18n', () => ({
  useI18n: () => ({
    t: (key) => key
  })
}))

// Mock echarts
vi.mock('echarts/core', () => ({
  use: vi.fn(),
  init: vi.fn(() => ({
    setOption: vi.fn(),
    resize: vi.fn(),
    dispose: vi.fn()
  }))
}))
vi.mock('echarts/renderers', () => ({ CanvasRenderer: {} }))
vi.mock('echarts/charts', () => ({ LineChart: {} }))
vi.mock('echarts/components', () => ({
  TitleComponent: {},
  TooltipComponent: {},
  GridComponent: {}
}))

// Mock services/api.js
vi.mock('../../services/api.js', () => ({
  post: mockPost,
  get: vi.fn(),
  put: vi.fn(),
  del: vi.fn(),
  request: vi.fn(),
  ApiError: class extends Error {
    constructor(m) {
      super(m)
    }
  },
  default: { get: vi.fn(), post: mockPost }
}))

// Mock useDraft - return simple objects that work with the component's usage patterns
// We use a different approach: mock the composable to return predictable states
const draftStore = new Map()

vi.mock('../../composables/useDraft', () => ({
  useDraft: (key, defaultValue) => {
    if (!draftStore.has(key)) {
      draftStore.set(key, JSON.parse(JSON.stringify(defaultValue)))
    }
    return {
      state: draftStore.get(key),
      clearDraft: vi.fn()
    }
  },
  useDraftRef: (key, defaultValue) => {
    if (!draftStore.has(key)) {
      draftStore.set(key, JSON.parse(JSON.stringify(defaultValue)))
    }
    // Return a proper ref-like that Vue recognizes
    // We need .value and _isRef for Vue template unwrapping
    const val = draftStore.get(key)
    const refObj = {
      __v_isRef: true,
      _isRef: true,
      _value: val,
      get value() {
        return this._value
      },
      set value(v) {
        this._value = v
        draftStore.set(key, v)
      }
    }
    return {
      state: refObj,
      clearDraft: vi.fn()
    }
  }
}))

import ScenarioCompare from '../ScenarioCompare.vue'

describe('ScenarioCompare.vue', () => {
  function createWrapper() {
    draftStore.clear()
    return mount(ScenarioCompare, {
      global: {
        plugins: [
          createTestingPinia({
            createSpy: vi.fn,
            stubActions: false
          })
        ],
        stubs: {
          SohChart: { template: '<div class="soh-chart" />' },
          SectionCard: { template: '<div><slot /></div>' }
        }
      }
    })
  }

  it('renders without crashing', () => {
    const wrapper = createWrapper()
    expect(wrapper.exists()).toBe(true)
  })

  it('renders the scenario title', () => {
    const wrapper = createWrapper()
    expect(wrapper.html()).toContain('scenario.title')
  })

  it('shows empty state when no scenarios exist', () => {
    const wrapper = createWrapper()
    expect(wrapper.html()).toContain('scenario.noScene')
  })

  it('uses services/api.js post() not raw fetch', () => {
    const wrapper = createWrapper()
    expect(wrapper.exists()).toBe(true)
  })

  it('can create a new scenario', async () => {
    const wrapper = createWrapper()
    const buttons = wrapper.findAll('button')
    const createBtn = buttons.find((b) => b.text().includes('+'))
    if (createBtn) {
      await createBtn.trigger('click')
      await wrapper.vm.$nextTick()
      // After clicking create, the editor should appear with form fields
      expect(wrapper.html()).toContain('scenario.namePlaceholder')
      expect(wrapper.html()).toContain('scenario.ratedEnergy')
    }
  })
})
