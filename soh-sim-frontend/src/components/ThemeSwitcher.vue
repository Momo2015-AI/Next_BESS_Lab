<template>
  <div class="flex items-center gap-4 flex-shrink-0">
    <div class="flex items-center rounded-lg border border-[var(--color-border)] overflow-hidden">
      <button v-for="lang in languages" :key="lang.value"
        @click="switchLocale(lang.value)"
        :class="['px-2.5 py-1 text-[11px] font-mono transition-colors cursor-pointer border-0',
          locale === lang.value
            ? 'bg-[var(--color-accent)] text-white'
            : 'bg-transparent text-[var(--color-text-muted)] hover:bg-[var(--color-bg-secondary)]']">
        {{ lang.label }}
      </button>
    </div>
    <button @click="toggleTheme"
      class="flex items-center justify-center w-8 h-8 rounded-lg bg-[var(--color-card)] border border-[var(--color-border)]
             text-[var(--color-text)] hover:border-[var(--color-accent)] transition-colors cursor-pointer"
      :title="theme === 'light' ? $t('common.themeDark') : $t('common.themeLight')">
      <svg v-if="theme === 'dark'" class="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
      </svg>
      <svg v-else class="w-4 h-4 text-sky-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'

const { locale, t } = useI18n()
const theme = ref(localStorage.getItem('app-theme') || 'light')

const languages = [
  { value: 'zh', label: t('common.langZH') },
  { value: 'en', label: t('common.langEN') },
  { value: 'ar', label: t('common.langAR') },
]

function switchLocale(val) {
  locale.value = val
  localStorage.setItem('app-locale', val)
  document.documentElement.setAttribute('dir', val === 'ar' ? 'rtl' : 'ltr')
  document.documentElement.setAttribute('lang', val)
}

function toggleTheme() {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
  localStorage.setItem('app-theme', theme.value)
  document.documentElement.setAttribute('data-theme', theme.value)
}
</script>
