import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPersistedstate from 'pinia-plugin-persistedstate'
import App from './App.vue'
import router from './router'
import i18n from './i18n/index.js'
import './style.css'

const pinia = createPinia()
pinia.use(piniaPersistedstate)

const app = createApp(App)
app.use(pinia)
app.use(router)
app.use(i18n)

app.config.errorHandler = (err, instance, info) => {
  console.error('[Vue Error]', err)
  const el = document.getElementById('app')
  if (el) {
    const banner = document.createElement('div')
    banner.style.cssText = 'position:fixed;top:0;left:0;right:0;background:#ef4444;color:white;padding:12px 16px;font-size:13px;z-index:99999;font-family:monospace;white-space:pre-wrap;word-break:break-all;'
    banner.textContent = '[Runtime Error] ' + (err.message || err)
    el.prepend(banner)
  }
}

const savedTheme = localStorage.getItem('app-theme') || 'light'
document.documentElement.setAttribute('data-theme', savedTheme)

const savedLocale = localStorage.getItem('app-locale') || 'zh'
const savedDir = savedLocale === 'ar' ? 'rtl' : 'ltr'
document.documentElement.setAttribute('dir', savedDir)
document.documentElement.setAttribute('lang', savedLocale)

app.mount('#app')
