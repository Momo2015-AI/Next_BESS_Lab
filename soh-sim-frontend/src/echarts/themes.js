/**
 * ECharts 图表风格主题定义
 *
 * 三套配色方案，每套含亮色/暗色两个变体。
 * 主题对象直接传给 echarts.init(dom, themeObj)，无需 registerTheme。
 */

// ==================== 方案 A：ECharts 5 默认色板 ====================
// 基于 ColorBrewer Set2 + Tableau 10
const ECHARTS_DEFAULT_PALETTE = [
  '#5470C6', '#91CC75', '#FAC858', '#EE6666', '#73C0DE',
  '#3BA272', '#FC8452', '#9A60B4', '#EA7CCC', '#546570'
]

const eChartsDefaultLight = {
  color: ECHARTS_DEFAULT_PALETTE,
  backgroundColor: 'transparent',
  textStyle: { color: '#333' },
  title: { textStyle: { color: '#333' } },
  legend: { textStyle: { color: '#666' } },
  // semantic aliases
  primary: '#5470C6',
  success: '#91CC75',
  warning: '#FAC858',
  danger: '#EE6666',
  info: '#73C0DE',
  purple: '#9A60B4',
  orange: '#FC8452',
  cyan: '#73C0DE',
  muted: '#546570',
  redLight: '#EE6666',
  acLine: '#3BA272',
  gridLine: '#e5e7eb',
  axisLabel: '#86868b',
  legendText: '#86868b',
  tooltipBg: 'rgba(255,255,255,0.95)',
  tooltipText: '#1e293b',
  splitLine: '#f1f5f9',
}

const eChartsDefaultDark = {
  color: ECHARTS_DEFAULT_PALETTE,
  backgroundColor: 'transparent',
  textStyle: { color: '#e5e7eb' },
  title: { textStyle: { color: '#e5e7eb' } },
  legend: { textStyle: { color: '#94a3b8' } },
  primary: '#5470C6',
  success: '#91CC75',
  warning: '#FAC858',
  danger: '#EE6666',
  info: '#73C0DE',
  purple: '#9A60B4',
  orange: '#FC8452',
  cyan: '#73C0DE',
  muted: '#546570',
  redLight: '#EE6666',
  acLine: '#3BA272',
  gridLine: '#1e293b',
  axisLabel: '#64748b',
  legendText: '#94a3b8',
  tooltipBg: 'rgba(30,41,59,0.95)',
  tooltipText: '#e5e7eb',
  splitLine: '#1e293b',
}

// ==================== 方案 B：Tailwind CSS 色板 ====================
const TAILWIND_PALETTE = [
  '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
  '#06b6d4', '#f97316', '#84cc16', '#ec4899', '#6366f1'
]

const tailwindLight = {
  color: TAILWIND_PALETTE,
  backgroundColor: 'transparent',
  textStyle: { color: '#1e293b' },
  title: { textStyle: { color: '#1e293b' } },
  legend: { textStyle: { color: '#64748b' } },
  primary: '#3b82f6',
  success: '#10b981',
  warning: '#f59e0b',
  danger: '#ef4444',
  info: '#3b82f6',
  purple: '#8b5cf6',
  orange: '#f97316',
  cyan: '#06b6d4',
  muted: '#94a3b8',
  redLight: '#f87171',
  acLine: '#10b981',
  gridLine: '#e2e8f0',
  axisLabel: '#94a3b8',
  legendText: '#64748b',
  tooltipBg: 'rgba(255,255,255,0.95)',
  tooltipText: '#1e293b',
  splitLine: '#f1f5f9',
}

const tailwindDark = {
  color: [
    '#60a5fa', '#34d399', '#fbbf24', '#f87171', '#a78bfa',
    '#22d3ee', '#fb923c', '#a3e635', '#f472b6', '#818cf8'
  ],
  backgroundColor: 'transparent',
  textStyle: { color: '#e2e8f0' },
  title: { textStyle: { color: '#e2e8f0' } },
  legend: { textStyle: { color: '#94a3b8' } },
  primary: '#60a5fa',
  success: '#34d399',
  warning: '#fbbf24',
  danger: '#f87171',
  info: '#60a5fa',
  purple: '#a78bfa',
  orange: '#fb923c',
  cyan: '#22d3ee',
  muted: '#64748b',
  redLight: '#f87171',
  acLine: '#34d399',
  gridLine: '#334155',
  axisLabel: '#64748b',
  legendText: '#94a3b8',
  tooltipBg: 'rgba(30,41,59,0.95)',
  tooltipText: '#e2e8f0',
  splitLine: '#1e293b',
}

// ==================== 方案 C：AntV/G2 色板 ====================
const ANTV_PALETTE = [
  '#5B8FF9', '#61DDAA', '#65789B', '#F6BD16', '#7262FD',
  '#78D3F8', '#9661BC', '#F6903D', '#008685', '#F08BB4'
]

const antvLight = {
  color: ANTV_PALETTE,
  backgroundColor: 'transparent',
  textStyle: { color: '#333' },
  title: { textStyle: { color: '#333' } },
  legend: { textStyle: { color: '#666' } },
  primary: '#5B8FF9',
  success: '#61DDAA',
  warning: '#F6BD16',
  danger: '#F6903D',
  info: '#5B8FF9',
  purple: '#7262FD',
  orange: '#F6903D',
  cyan: '#78D3F8',
  muted: '#65789B',
  redLight: '#F08BB4',
  acLine: '#61DDAA',
  gridLine: '#e5e7eb',
  axisLabel: '#86868b',
  legendText: '#86868b',
  tooltipBg: 'rgba(255,255,255,0.95)',
  tooltipText: '#1e293b',
  splitLine: '#f1f5f9',
}

const antvDark = {
  color: [
    '#7BABFF', '#7BE8B8', '#8B95AD', '#FCD34D', '#9B8DFD',
    '#9EDFF8', '#B08BCC', '#F8A86D', '#26A69A', '#F4A8C8'
  ],
  backgroundColor: 'transparent',
  textStyle: { color: '#e5e7eb' },
  title: { textStyle: { color: '#e5e7eb' } },
  legend: { textStyle: { color: '#94a3b8' } },
  primary: '#7BABFF',
  success: '#7BE8B8',
  warning: '#FCD34D',
  danger: '#F8A86D',
  info: '#7BABFF',
  purple: '#9B8DFD',
  orange: '#F8A86D',
  cyan: '#9EDFF8',
  muted: '#8B95AD',
  redLight: '#F4A8C8',
  acLine: '#7BE8B8',
  gridLine: '#1e293b',
  axisLabel: '#64748b',
  legendText: '#94a3b8',
  tooltipBg: 'rgba(30,41,59,0.95)',
  tooltipText: '#e5e7eb',
  splitLine: '#1e293b',
}

// ==================== 主题字典 ====================
export const CHART_THEMES = {
  echarts: { light: eChartsDefaultLight, dark: eChartsDefaultDark },
  tailwind: { light: tailwindLight, dark: tailwindDark },
  antv: { light: antvLight, dark: antvDark },
}

export const THEME_LABELS = {
  echarts: 'ECharts 默认',
  tailwind: 'Tailwind',
  antv: 'AntV',
}

export const THEME_KEYS = Object.keys(CHART_THEMES)
