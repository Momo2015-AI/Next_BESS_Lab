import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPersistedstate from 'pinia-plugin-persistedstate'
import App from './App.vue'
import router from './router'
import i18n from './i18n/index.js'
import './style.css'
import './assets/styles/shared.css'
import './assets/styles/app-shell.css'
import './assets/styles/admin-panel.css'

const pinia = createPinia()
pinia.use(piniaPersistedstate)

const app = createApp(App)
app.use(pinia)
app.use(router)
app.use(i18n)

app.config.errorHandler = (err, instance, info) => {
  console.error('[Vue Error]', err, '\nStack:', err?.stack, '\nInstance:', instance?.$options?.name || instance?.type?.name, '\nInfo:', info)
  const el = document.getElementById('app')
  if (el) {
    const banner = document.createElement('div')
    banner.style.cssText =
      'position:fixed;top:0;left:0;right:0;background:var(--color-danger);color:white;padding:12px 16px;font-size:13px;z-index:99999;font-family:monospace;white-space:pre-wrap;word-break:break-all;'
    const compName = instance?.$options?.name || instance?.type?.name || ''
    banner.textContent = '[Runtime Error] ' + (err.message || err) + (compName ? ' (in ' + compName + ')' : '') + (info ? '\n' + info : '')
    el.prepend(banner)
  }
}

const savedTheme = localStorage.getItem('app-theme') || 'light'
document.documentElement.setAttribute('data-theme', savedTheme)

const savedLocale = localStorage.getItem('app-locale') || 'zh'
const savedDir = savedLocale === 'ar' ? 'rtl' : 'ltr'
document.documentElement.setAttribute('dir', savedDir)
document.documentElement.setAttribute('lang', savedLocale)

window.addEventListener('error', (evt) => {
  const el = document.getElementById('app')
  if (el) {
    const banner = document.createElement('div')
    banner.style.cssText =
      'position:fixed;top:0;left:0;right:0;background:var(--color-danger);color:white;padding:12px 16px;font-size:11px;z-index:99999;font-family:monospace;white-space:pre-wrap;word-break:break-all;'
    banner.textContent = '[JS Error] ' + evt.message + ' | ' + (evt.filename || '').split('/').pop() + ':' + evt.lineno
    el.prepend(banner)
  }
})

app.mount('#app')
