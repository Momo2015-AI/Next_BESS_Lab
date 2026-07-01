import { createI18n } from 'vue-i18n'
import zh from './zh.js'
import en from './en.js'
import ar from './ar.js'

const savedLocale = localStorage.getItem('app-locale') || 'zh'

const i18n = createI18n({
  legacy: false,
  locale: savedLocale,
  fallbackLocale: 'zh',
  messages: { zh, en, ar }
})

export default i18n
