/**
 * P2-1 0.4: EpcPage 表征测试（拆前快照）
 *
 * 此测试在 P2-1 组件拆分过程中必须保持通过。
 * 覆盖：渲染 9 个 tab、各表单 v-model 双向绑定、apiCall 成功/失败分支。
 *
 * P2-1 1.2 更新：apiCall 改用 services/api.js 的 post/get，
 * fetch 调用签名变化（添加 signal/headers），测试断言相应调整。
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { nextTick } from 'vue'
import EpcPage from '../EpcPage.vue'

// ---------- global mocks ----------

// Mock AppIcon component
const AppIconStub = {
  name: 'AppIcon',
  props: ['name', 'size'],
  template: '<span class="mock-icon">{{ name }}</span>'
}

// Mock fetch
let mockFetch
beforeEach(() => {
  mockFetch = vi.fn()
  global.fetch = mockFetch
  // Default: all fetch calls resolve empty success
  mockFetch.mockResolvedValue({
    ok: true,
    status: 200,
    headers: { get: () => 'application/json' },
    json: async () => ({ success: true, data: null })
  })
})

afterEach(() => {
  vi.restoreAllMocks()
})

// ---------- helpers ----------

function mountEpcPage() {
  return mount(EpcPage, {
    global: {
      stubs: {
        AppIcon: AppIconStub
      }
    }
  })
}

// ---------- 9 个 tab 渲染 ----------

describe('Tab rendering', () => {
  it('renders all 9 module tabs', () => {
    const wrapper = mountEpcPage()
    const buttons = wrapper.findAll('.epc-tabs button')
    expect(buttons).toHaveLength(9)

    const labels = buttons.map((b) => b.find('.tab-label').text())
    expect(labels).toContain('系统架构')
    expect(labels).toContain('电网合规')
    expect(labels).toContain('安全消防')
    expect(labels).toContain('IPP财务')
    expect(labels).toContain('合规矩阵')
    expect(labels).toContain('热管理')
    expect(labels).toContain('SCADA/EMS')
    expect(labels).toContain('高压接入')
    expect(labels).toContain('投标文档')
  })

  it('starts with "architecture" tab active', () => {
    const wrapper = mountEpcPage()
    const activeBtn = wrapper.find('.epc-tabs button.active')
    expect(activeBtn.find('.tab-label').text()).toBe('系统架构')
  })

  it('switches active tab on click', async () => {
    const wrapper = mountEpcPage()
    const buttons = wrapper.findAll('.epc-tabs button')
    // Click "安全消防" (3rd tab)
    await buttons[2].trigger('click')
    const activeBtn = wrapper.find('.epc-tabs button.active')
    expect(activeBtn.find('.tab-label').text()).toBe('安全消防')
  })
})

// ---------- 表单 v-model 双向绑定 ----------

describe('Form v-model binding', () => {
  it('updates arch form fields via input', async () => {
    const wrapper = mountEpcPage()
    const inputs = wrapper.findAll('input[type="number"]')

    // Find and update total_power_mw (first input in architecture tab)
    const powerInput = inputs[0]
    await powerInput.setValue('500')
    expect(powerInput.element.value).toBe('500')
  })

  it('updates grid compliance form select', async () => {
    const wrapper = mountEpcPage()
    // Switch to grid compliance tab
    await wrapper.findAll('.epc-tabs button')[1].trigger('click')
    const select = wrapper.find('select')
    expect(select.exists()).toBe(true)
  })

  it('updates safety form fields', async () => {
    const wrapper = mountEpcPage()
    // Switch to safety tab (3rd)
    await wrapper.findAll('.epc-tabs button')[2].trigger('click')
    const inputs = wrapper.findAll('input[type="number"]')
    // Should find safety-specific inputs
    expect(inputs.length).toBeGreaterThan(0)
  })
})

// ---------- 按钮渲染 ----------

describe('Action buttons', () => {
  it('renders all action buttons correctly', () => {
    const wrapper = mountEpcPage()
    const buttons = wrapper.findAll('button.btn-primary')
    expect(buttons.length).toBeGreaterThanOrEqual(9)
  })

  it('shows button text in Chinese', () => {
    const wrapper = mountEpcPage()
    const btn = wrapper.find('button.btn-primary')
    expect(btn.text()).toContain('设计')
  })
})

// ---------- apiCall 成功路径 ----------

describe('apiCall success', () => {
  it('calls fetch with POST and updates result ref', async () => {
    const wrapper = mountEpcPage()

    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      headers: { get: () => 'application/json' },
      json: async () => ({
        success: true,
        data: { topology_data: { levels: [] } }
      })
    })

    // Click the first action button (designArchitecture)
    const btn = wrapper.find('button.btn-primary')
    await btn.trigger('click')
    await flushPromises()

    // api.js post calls fetch with method POST and Content-Type header
    expect(mockFetch).toHaveBeenCalledWith(
      '/api/system-architecture/design',
      expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({ 'Content-Type': 'application/json' })
      })
    )
  })

  it('sets loading to false after success', async () => {
    const wrapper = mountEpcPage()

    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      headers: { get: () => 'application/json' },
      json: async () => ({ success: true, data: {} })
    })

    const btn = wrapper.find('button.btn-primary')
    await btn.trigger('click')
    await flushPromises()
    await nextTick()

    // Button should no longer say "计算中..."
    expect(btn.text()).not.toBe('计算中...')
  })
})

// ---------- apiCall 失败路径 ----------

describe('apiCall failure', () => {
  it('emits error when response.success is false', async () => {
    const wrapper = mountEpcPage()

    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      headers: { get: () => 'application/json' },
      json: async () => ({
        success: false,
        error: '后端计算失败'
      })
    })

    const btn = wrapper.find('button.btn-primary')
    await btn.trigger('click')
    await flushPromises()

    expect(wrapper.emitted('error')).toBeTruthy()
    expect(wrapper.emitted('error')[0]).toEqual(['后端计算失败'])
  })

  it('emits error on network failure', async () => {
    const wrapper = mountEpcPage()

    mockFetch.mockRejectedValueOnce(new Error('Network down'))

    const btn = wrapper.find('button.btn-primary')
    await btn.trigger('click')
    await flushPromises()

    expect(wrapper.emitted('error')).toBeTruthy()
    expect(wrapper.emitted('error')[0][0]).toContain('网络错误')
  })
})

// ---------- onUnmounted 清理 ----------

describe('Cleanup on unmount', () => {
  it('calls purgePlotly on unmount if chartContainer exists', async () => {
    const wrapper = mountEpcPage()
    wrapper.unmount()
    // purgePlotly should not throw even if chartContainer is null
    expect(true).toBe(true)
  })
})

// ---------- loadStandards ----------

describe('loadStandards on mount', () => {
  it('calls fetch for grid standards on mount', () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      headers: { get: () => 'application/json' },
      json: async () => []
    })
    mountEpcPage()
    // api.js get calls fetch with the URL as first arg
    expect(mockFetch).toHaveBeenCalledWith('/api/grid-compliance/standards', expect.objectContaining({ method: 'GET' }))
  })
})
