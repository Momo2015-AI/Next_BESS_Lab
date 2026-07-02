<template>
  <div class="flex items-center gap-4 flex-shrink-0">
    <div class="flex items-center rounded-lg border border-[var(--color-border)] overflow-hidden">
      <button
        v-for="lang in languages"
        :key="lang.value"
        :class="[
          'px-2.5 py-1 text-[11px] font-mono transition-colors cursor-pointer border-0',
          locale === lang.value
            ? 'bg-[var(--color-accent)] text-white'
            : 'bg-transparent text-[var(--color-text-muted)] hover:bg-[var(--color-bg-secondary)]'
        ]"
        @click="switchLocale(lang.value)"
      >
        {{ lang.label }}
      </button>
    </div>
    <button
      class="theme-toggle-btn w-[42px] h-[42px]"
      :title="theme === 'light' ? $t('common.themeDark') : $t('common.themeLight')"
      @click="toggleTheme"
    >
      <AppIcon v-if="theme === 'dark'" name="sun" :size="16" :stroke-width="2" color="var(--color-amber)" />
      <AppIcon v-else name="moon" :size="16" :stroke-width="2" color="var(--color-sky)" />
    </button>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import AppIcon from './AppIcon.vue'

const { locale, t } = useI18n()
const theme = ref(localStorage.getItem('app-theme') || 'light')

const languages = [
  { value: 'zh', label: t('common.langZH') },
  { value: 'en', label: t('common.langEN') },
  { value: 'ar', label: t('common.langAR') }
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
