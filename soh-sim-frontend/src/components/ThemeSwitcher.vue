<template>
  <div class="flex items-center gap-3 flex-shrink-0">
    <!-- Theme toggle: icon-only circular button -->
    <button
      class="theme-icon-btn"
      :title="theme === 'light' ? $t('common.themeDark') : $t('common.themeLight')"
      :aria-label="theme === 'light' ? $t('common.themeDark') : $t('common.themeLight')"
      @click="toggleTheme"
    >
      <AppIcon v-if="theme === 'dark'" name="sun" :size="18" :stroke-width="1.5" color="var(--color-warning)" />
      <AppIcon v-else name="moon" :size="18" :stroke-width="1.5" color="var(--text-secondary)" />
    </button>

    <!-- Chart theme switcher: icon button that cycles through palettes -->
    <button
      class="theme-icon-btn"
      :title="`${$t('common.chartTheme')}: ${chartThemeLabel}`"
      :aria-label="`${$t('common.chartTheme')}: ${chartThemeLabel}`"
      @click="cycleTheme"
    >
      <AppIcon name="palette" :size="18" :stroke-width="1.5" color="var(--text-secondary)" />
    </button>

    <!-- Language switcher: pill with globe + current lang + chevron -->
    <div ref="rootRef" class="lang-switcher">
      <button class="lang-trigger" :aria-expanded="open" :title="$t('common.language')" @click="open = !open">
        <AppIcon name="globe" :size="16" :stroke-width="1.5" color="var(--text-secondary)" />
        <span class="lang-label">{{ currentLangLabel }}</span>
        <AppIcon
          name="chevron-down"
          :size="14"
          :stroke-width="1.5"
          color="var(--text-secondary)"
          :class="['chev', { open }]"
        />
      </button>

      <ul v-if="open" class="lang-menu" role="listbox">
        <li
          v-for="lang in languages"
          :key="lang.value"
          :class="['lang-item', { active: locale === lang.value }]"
          role="option"
          :aria-selected="locale === lang.value"
          @click="selectLang(lang.value)"
        >
          <span class="lang-item-dot" />
          <span>{{ lang.label }}</span>
          <AppIcon
            v-if="locale === lang.value"
            name="check"
            :size="14"
            :stroke-width="1.5"
            color="var(--color-accent)"
          />
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useChartTheme } from '../composables/useChartTheme.js'
import AppIcon from './AppIcon.vue'

const { locale, t } = useI18n()
const { themeKey, cycleTheme } = useChartTheme()
const theme = ref(localStorage.getItem('app-theme') || 'light')
const open = ref(false)
const rootRef = ref(null)

const languages = [
  { value: 'zh', label: t('common.langZH') },
  { value: 'en', label: t('common.langEN') },
  { value: 'ar', label: t('common.langAR') }
]

const currentLangLabel = computed(() => {
  const cur = languages.find((l) => l.value === locale.value)
  return cur ? cur.label : ''
})

const chartThemeLabel = computed(() => {
  const map = {
    echarts: t('common.chartThemeEcharts'),
    tailwind: t('common.chartThemeTailwind'),
    antv: t('common.chartThemeAntv'),
  }
  return map[themeKey.value] || themeKey.value
})

function switchLocale(val) {
  locale.value = val
  localStorage.setItem('app-locale', val)
  document.documentElement.setAttribute('dir', val === 'ar' ? 'rtl' : 'ltr')
  document.documentElement.setAttribute('lang', val)
}

function selectLang(val) {
  switchLocale(val)
  open.value = false
}

function toggleTheme() {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
  localStorage.setItem('app-theme', theme.value)
  document.documentElement.setAttribute('data-theme', theme.value)
}

function onDocClick(e) {
  if (!rootRef.value) return
  if (!rootRef.value.contains(e.target)) open.value = false
}

function onKeydown(e) {
  if (e.key === 'Escape') open.value = false
}

onMounted(() => {
  document.addEventListener('click', onDocClick)
  document.addEventListener('keydown', onKeydown)
})

onUnmounted(() => {
  document.removeEventListener('click', onDocClick)
  document.removeEventListener('keydown', onKeydown)
})
</script>

<style scoped>
/* ===== 主题切换：圆形图标按钮 ===== */
.theme-icon-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--color-border);
  border-radius: 50%;
  background: var(--color-card);
  cursor: pointer;
  transition:
    background 0.2s ease,
    border-color 0.2s ease,
    color 0.2s ease;
}

.theme-icon-btn:hover {
  background: var(--color-card-hover);
}

.theme-icon-btn:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

/* ===== 语言切换：胶囊触发器 + 下拉 ===== */
.lang-switcher {
  position: relative;
}

.lang-trigger {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 36px;
  padding: 0 12px 0 14px;
  border-radius: 999px;
  background: var(--color-card);
  border: 1px solid var(--color-border);
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition:
    background 0.2s ease,
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.lang-trigger:hover {
  border-color: var(--border-color-hover);
  background: var(--bg-card-solid);
  box-shadow: var(--shadow-card-glow);
}

.lang-trigger:focus-visible {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px var(--color-accent-glow);
}

.lang-label {
  white-space: nowrap;
  line-height: 1;
}

.chev {
  transition: transform 0.2s ease;
}
.chev.open {
  transform: rotate(180deg);
}

/* ===== 下拉菜单 ===== */
.lang-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 160px;
  list-style: none;
  margin: 0;
  padding: 6px;
  background: var(--color-modal-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  backdrop-filter: var(--backdrop-filter);
  z-index: 200;
  animation: lang-menu-in 0.16s ease;
}

@keyframes lang-menu-in {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.lang-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  color: var(--text-primary);
  cursor: pointer;
  transition: background 0.15s ease;
}

.lang-item:hover {
  background: var(--color-card-hover);
}

.lang-item.active {
  color: var(--color-accent);
  font-weight: 600;
}

.lang-item-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: transparent;
  flex-shrink: 0;
}

.lang-item.active .lang-item-dot {
  background: var(--color-accent);
}
</style>
