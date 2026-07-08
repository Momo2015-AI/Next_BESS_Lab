/**
 * usePlotly composable unit tests
 *
 * Tests: loadPlotly (lazy CDN injection, singleton reuse),
 * renderPlotly (calls Plotly.newPlot), purgePlotly (cleanup without error).
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { loadPlotly, renderPlotly, purgePlotly } from '../usePlotly.js'

// ---------- mocks ----------

let mockNewPlot, mockPurge
let scriptElement = null

beforeEach(() => {
  // Reset Plotly on window
  delete window.Plotly

  // Mock Plotly methods
  mockNewPlot = vi.fn().mockResolvedValue(undefined)
  mockPurge = vi.fn()

  // Spy on document.createElement for script injection
  vi.spyOn(document.head, 'appendChild').mockImplementation((el) => {
    scriptElement = el
  })
})

afterEach(() => {
  vi.restoreAllMocks()
  scriptElement = null
})

// ---------- loadPlotly ----------

describe('loadPlotly', () => {
  it('returns existing window.Plotly immediately', async () => {
    window.Plotly = { newPlot: mockNewPlot }
    const plotly = await loadPlotly()
    expect(plotly).toBe(window.Plotly)
    // Should not create a script tag
    expect(document.head.appendChild).not.toHaveBeenCalled()
  })

  it('injects CDN script and resolves on load', async () => {
    const result = loadPlotly()
    expect(scriptElement).not.toBeNull()
    expect(scriptElement.src).toContain('plotly')

    // Simulate script onload
    window.Plotly = { newPlot: mockNewPlot }
    scriptElement.onload()

    const plotly = await result
    expect(plotly).toBe(window.Plotly)
  })

  it('rejects when script fails to load', async () => {
    const result = loadPlotly()
    scriptElement.onerror(new Error('CDN failed'))
    await expect(result).rejects.toThrow('Plotly CDN 加载失败')
  })

  it('reuses the same promise for concurrent calls', async () => {
    const r1 = loadPlotly()
    const r2 = loadPlotly()
    expect(scriptElement).not.toBeNull()
    // Only one script should exist
    expect(document.head.appendChild).toHaveBeenCalledTimes(1)
  })
})

// ---------- renderPlotly ----------

describe('renderPlotly', () => {
  it('does nothing when container is null', async () => {
    await renderPlotly(null, { data: [], layout: {} }, 'chart1')
    expect(mockNewPlot).not.toHaveBeenCalled()
  })

  it('does nothing when chart is null', async () => {
    const el = document.createElement('div')
    await renderPlotly(el, null, 'chart1')
    expect(mockNewPlot).not.toHaveBeenCalled()
  })

  it('calls Plotly.newPlot with container, data, layout, config', async () => {
    window.Plotly = { newPlot: mockNewPlot }
    const el = document.createElement('div')
    const chart = {
      data: [{ x: [1, 2], y: [3, 4] }],
      layout: { title: 'Test' },
      config: { responsive: true }
    }
    await renderPlotly(el, chart, 'chart-42')
    expect(el.id).toBe('chart-42')
    expect(mockNewPlot).toHaveBeenCalledWith(el, chart.data, chart.layout, chart.config)
  })
})

// ---------- purgePlotly ----------

describe('purgePlotly', () => {
  it('does nothing when container is null', () => {
    expect(() => purgePlotly(null)).not.toThrow()
  })

  it('calls Plotly.purge when available', () => {
    window.Plotly = { purge: mockPurge }
    const el = document.createElement('div')
    purgePlotly(el)
    expect(mockPurge).toHaveBeenCalledWith(el)
  })

  it('does not throw when Plotly is not loaded', () => {
    const el = document.createElement('div')
    expect(() => purgePlotly(el)).not.toThrow()
  })
})
