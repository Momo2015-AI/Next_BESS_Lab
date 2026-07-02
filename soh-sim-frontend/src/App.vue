<template>
  <div class="app-shell">
    <div v-if="toast.show" class="toast-notification" :class="'toast-' + toast.type">
      {{ toast.message }}
    </div>

    <header class="app-header">
      <div class="header-inner">
        <router-link to="/" class="brand">
          <NexBessLogo compact />
        </router-link>

        <div class="header-actions">
          <router-link to="/auth" class="auth-btn" :class="{ active: $route.path === '/auth' }">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
              <path d="M7 11V7a5 5 0 0 1 10 0v4" />
            </svg>
            <span>{{ $t('sidebar.auth') }}</span>
          </router-link>
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
import { reactive, provide } from 'vue'
import Sidebar from './components/Sidebar.vue'
import ThemeSwitcher from './components/ThemeSwitcher.vue'
import NexBessLogo from './components/NexBessLogo.vue'
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
  background: var(--bg-global);
  background-attachment: scroll;
  overflow: hidden;
}

.app-header {
  height: 52px;
  flex-shrink: 0;
  background: var(--bg-card);
  backdrop-filter: var(--backdrop-filter);
  -webkit-backdrop-filter: var(--backdrop-filter);
  border-bottom: 1px solid var(--border-color);
  z-index: 100;
  position: relative;
  transition:
    background 0.5s cubic-bezier(0.16, 1, 0.3, 1),
    border-color 0.5s cubic-bezier(0.16, 1, 0.3, 1);
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
  text-decoration: none;
}

.header-actions {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 12px;
}

.auth-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: 14px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  border: 1px solid var(--border-color);
  background: var(--bg-card);
  transition:
    background 0.25s cubic-bezier(0.16, 1, 0.3, 1),
    color 0.25s cubic-bezier(0.16, 1, 0.3, 1),
    border-color 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
}

.auth-btn:hover {
  color: var(--text-primary);
  border-color: var(--border-color-hover);
  box-shadow: var(--shadow-card-glow);
}

.auth-btn.active {
  color: var(--accent-blue);
  border-color: var(--accent-blue);
  box-shadow: var(--shadow-card-glow);
}

.auth-btn svg {
  width: 14px;
  height: 14px;
  stroke: currentColor;
  flex-shrink: 0;
}

.icon-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition:
    background 0.5s cubic-bezier(0.16, 1, 0.3, 1),
    color 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

.icon-btn:hover {
  background: var(--bg-card);
  color: var(--text-primary);
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
  position: relative;
  z-index: 1;
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
  transition: opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
