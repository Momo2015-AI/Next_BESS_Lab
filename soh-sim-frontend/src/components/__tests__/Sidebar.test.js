import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import Sidebar from '../Sidebar.vue'

// Mock vue-router: useRoute returns a reactive-like object
const mockRoute = { path: '/', query: {} }
vi.mock('vue-router', () => ({
  useRoute: () => mockRoute
}))

// Mock vue-i18n so useI18n() works without installing the plugin
vi.mock('vue-i18n', () => ({
  useI18n: () => ({
    t: (key) => key,
    locale: { value: 'zh' }
  })
}))

// Mock usePermission composable
vi.mock('../../composables/usePermission.js', () => ({
  usePermission: () => ({
    canView: () => true,
    isAdmin: { value: false }
  })
}))

describe('Sidebar.vue', () => {
  let wrapper

  function createWrapper(routeOverrides = {}) {
    Object.assign(mockRoute, { path: '/', query: {} }, routeOverrides)
    return mount(Sidebar, {
      global: {
        plugins: [
          createTestingPinia({
            createSpy: vi.fn,
            initialState: {
              bess: {
                phases: {
                  phase1: { status: 'completed' },
                  phase2: { status: 'active' },
                  phase3: { status: 'pending' },
                  phase4: { status: 'pending' },
                  phase5: { status: 'pending' }
                }
              }
            }
          })
        ],
        stubs: {
          'router-link': {
            template: '<a :class="$attrs.class"><slot /></a>',
            props: ['to']
          },
          AppIcon: { template: '<span class="icon" />' }
        }
      }
    })
  }

  beforeEach(() => {
    wrapper = createWrapper()
  })

  it('renders phase navigation items', () => {
    const items = wrapper.findAll('a')
    // Should have at least: home, 5 phases, auth footer = 7
    expect(items.length).toBeGreaterThanOrEqual(7)
  })

  it('renders home link', () => {
    expect(wrapper.html()).toContain('sidebar.home')
  })

  it('renders phase items with labels', () => {
    const html = wrapper.html()
    expect(html).toContain('sidebar.phaseSetup')
    expect(html).toContain('sidebar.phaseDesign')
    expect(html).toContain('sidebar.phasePerformance')
    expect(html).toContain('sidebar.phaseFinancial')
    expect(html).toContain('sidebar.phaseDeliverables')
  })

  it('renders core tool items', () => {
    const html = wrapper.html()
    expect(html).toContain('sidebar.toolFormula')
  })

  it('highlights active phase based on route path', () => {
    // Re-mount with route pointing to /phase1
    wrapper = createWrapper({ path: '/phase1' })
    const links = wrapper.findAll('a')
    // Find the link that has "active" class and contains phaseSetup text
    const activeLinks = links.filter((link) => link.classes().includes('active'))
    expect(activeLinks.length).toBeGreaterThan(0)
  })

  it('uses useRoute instead of $route', () => {
    // Verify the component is defined (no $route reference crashes)
    expect(wrapper.vm).toBeDefined()
  })

  it('renders auth link in footer', () => {
    expect(wrapper.html()).toContain('sidebar.auth')
  })

  it('renders section labels', () => {
    const html = wrapper.html()
    expect(html).toContain('sidebar.sectionPhases')
    expect(html).toContain('sidebar.sectionCoreTools')
    expect(html).toContain('sidebar.sectionAdvanced')
  })
})
