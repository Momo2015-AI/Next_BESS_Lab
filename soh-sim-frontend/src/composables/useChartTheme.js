import { computed } from 'vue'

/**
 * 统一 ECharts 主题 composable
 * 替代各组件独立的 chartColors computed，自动适配 light/dark 模式
 */
export function useChartTheme() {
  const isDark = computed(() => document.documentElement.getAttribute('data-theme') === 'dark')

  const palette = computed(() =>
    isDark.value
      ? ['#3a8bff', '#30d158', '#facc15', '#f87171', '#a78bfa', '#38bdf8', '#2dd4bf', '#fb923c']
      : ['#0066cc', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#0ea5e9', '#14b8a6', '#ea580c']
  )

  const textSecondary = computed(() => (isDark.value ? 'var(--color-text-secondary)' : 'var(--color-text-secondary)'))
  const gridLine = computed(() => (isDark.value ? '#1e293b' : 'var(--color-border-light)'))

  /**
   * 基础主题对象 — 用于 echarts.init(ref, theme)
   */
  const theme = computed(() => ({
    backgroundColor: 'transparent',
    textStyle: { color: textSecondary.value, fontSize: 12 },
    title: {
      textStyle: { color: isDark.value ? '#f5f7fa' : '#1d1d1f', fontSize: 14 },
      subtextStyle: { color: textSecondary.value }
    },
    legend: { textStyle: { color: textSecondary.value } },
    tooltip: {
      backgroundColor: isDark.value ? 'rgba(15, 23, 42, 0.95)' : 'rgba(255, 255, 255, 0.98)',
      borderColor: isDark.value ? '#1e293b' : '#e2e8f0',
      textStyle: { color: isDark.value ? '#cbd5e1' : '#334155' },
      axisPointer: { lineStyle: { color: palette.value[0] }, crossStyle: { color: palette.value[0] } }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      axisLine: { lineStyle: { color: gridLine.value } },
      axisLabel: { color: textSecondary.value },
      splitLine: { lineStyle: { color: gridLine.value, type: 'dashed' } }
    },
    yAxis: {
      axisLine: { lineStyle: { color: gridLine.value } },
      axisLabel: { color: textSecondary.value },
      splitLine: { lineStyle: { color: gridLine.value, type: 'dashed' } }
    },
    color: palette.value
  }))

  /**
   * 快速色值映射 — 兼容原有 chartColors 用法
   */
  const colors = computed(() => ({
    backgroundColor: 'transparent',
    textSecondary: textSecondary.value,
    gridLine: gridLine.value,
    success: 'var(--color-success)',
    danger: 'var(--color-danger)',
    warning: 'var(--color-warning)',
    info: 'var(--color-info)',
    accent: 'var(--color-accent)',
    chartOrange: 'var(--color-chart-orange)',
    chartPink: 'var(--color-chart-pink)',
    chartCyan: 'var(--color-chart-cyan)'
  }))

  return { theme, colors, palette, isDark }
}
