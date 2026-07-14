/**
 * 图表主题管理 Composable
 *
 * 提供：
 * - themeKey: 当前选中的配色方案 (echarts / tailwind / antv)
 * - themeMode: 当前明暗模式 (light / dark)
 * - themeObject: 可直接传入 echarts.init(dom, themeObject) 的主题对象
 * - themeName: 拼接后的主题名，如 "tailwind-dark"
 * - cycleTheme(): 循环切换配色方案
 * - setTheme(key): 设置指定配色方案
 */

import { computed, ref, watch } from 'vue'
import { CHART_THEMES, THEME_KEYS } from '../echarts/themes.js'

const STORAGE_KEY = 'app-chart-theme'

const themeKey = ref(loadThemeKey())

const themeMode = ref(getCurrentMode())

function loadThemeKey() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved && THEME_KEYS.includes(saved)) return saved
  } catch {
    /* ignore */
  }
  return 'tailwind'
}

function getCurrentMode() {
  const attr = document.documentElement.getAttribute('data-theme')
  return attr === 'dark' ? 'dark' : 'light'
}

const themeObject = computed(() => {
  const key = themeKey.value
  const mode = themeMode.value
  return CHART_THEMES[key]?.[mode] || CHART_THEMES.tailwind.light
})

const themeName = computed(() => `${themeKey.value}-${themeMode.value}`)

function setTheme(key) {
  if (!THEME_KEYS.includes(key)) return
  themeKey.value = key
  try {
    localStorage.setItem(STORAGE_KEY, key)
  } catch {
    /* ignore */
  }
}

function cycleTheme() {
  const idx = THEME_KEYS.indexOf(themeKey.value)
  const next = THEME_KEYS[(idx + 1) % THEME_KEYS.length]
  setTheme(next)
}

// 监听系统明暗主题变化 (data-theme 属性)
if (typeof window !== 'undefined' && typeof MutationObserver !== 'undefined') {
  const observer = new MutationObserver(() => {
    themeMode.value = getCurrentMode()
  })
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['data-theme']
  })
}

export function useChartTheme() {
  return {
    themeKey,
    themeMode,
    themeObject,
    themeName,
    setTheme,
    cycleTheme,
    THEME_KEYS
  }
}
