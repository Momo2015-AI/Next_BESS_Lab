<template>
  <div class="app-shell">
    <div v-if="toast.show" class="toast-notification" :class="'toast-' + toast.type">
      {{ toast.message }}
    </div>

    <header class="app-header">
      <div class="header-inner">
        <router-link to="/" class="brand">
          <div class="brand-icon">
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
            </svg>
          </div>
          <span class="brand-text">SOH-SIM</span>
        </router-link>

        <nav class="header-nav">
          <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">Overview</router-link>
          <router-link to="/phase1" class="nav-link">Phases</router-link>
          <router-link to="/tools/formula" class="nav-link">Tools</router-link>
        </nav>

        <div class="header-actions">
          <ThemeSwitcher />
        </div>
      </div>
    </header>

    <div class="app-body">
      <Sidebar />
      <main class="app-main">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, provide } from 'vue'
import Sidebar from './components/Sidebar.vue'
import ThemeSwitcher from './components/ThemeSwitcher.vue'
const toast = reactive({ show: false, message: '', type: 'info' })
const showToast = (message, type = 'info') => {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => {
    toast.show = false
  }, 3000)
}
provide('showToast', showToast)
</script>

<style scoped>
.app-shell {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-bg);
  overflow: hidden;
}

.app-header {
  height: 52px;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 0.5px solid rgba(0, 0, 0, 0.1);
  z-index: 100;
  position: relative;
}

[data-theme='dark'] .app-header {
  background: rgba(29, 29, 31, 0.72);
  border-bottom-color: rgba(255, 255, 255, 0.08);
}

.header-inner {
  max-width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  padding: 0 24px;
  gap: 32px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: #1d1d1f;
}

[data-theme='dark'] .brand {
  color: #f5f5f7;
}

.brand-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, #0071e3, #40a9ff);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.brand-text {
  font-size: 15px;
  font-weight: 600;
  letter-spacing: -0.01em;
}

.header-nav {
  display: flex;
  gap: 4px;
}

.nav-link {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  color: #86868b;
  text-decoration: none;
  transition: all 0.2s;
}

.nav-link:hover {
  color: #1d1d1f;
  background: rgba(0, 0, 0, 0.04);
}
.nav-link.active {
  color: #1d1d1f;
  background: rgba(0, 0, 0, 0.06);
}

[data-theme='dark'] .nav-link:hover {
  color: #f5f5f7;
  background: rgba(255, 255, 255, 0.08);
}
[data-theme='dark'] .nav-link.active {
  color: #f5f5f7;
  background: rgba(255, 255, 255, 0.1);
}

.header-actions {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 8px;
}

.icon-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: transparent;
  color: #86868b;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.icon-btn:hover {
  background: rgba(0, 0, 0, 0.06);
  color: #1d1d1f;
}
[data-theme='dark'] .icon-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #f5f5f7;
}

.app-body {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.app-main {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
}

.toast-notification {
  position: fixed;
  top: 64px;
  right: 24px;
  padding: 10px 20px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 500;
  z-index: 9999;
  backdrop-filter: blur(20px);
  animation: slideIn 0.3s ease;
}
.toast-success {
  background: rgba(16, 185, 129, 0.9);
  color: white;
}
.toast-error {
  background: rgba(239, 68, 68, 0.9);
  color: white;
}
.toast-warning {
  background: rgba(245, 158, 11, 0.9);
  color: white;
}
.toast-info {
  background: rgba(0, 113, 227, 0.9);
  color: white;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
