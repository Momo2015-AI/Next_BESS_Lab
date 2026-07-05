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
          <!-- 已登录态：显示用户菜单；未登录：显示登录+注册两按钮 -->
          <template v-if="authUser">
            <div ref="userMenuRef" class="user-menu">
              <button class="user-trigger" @click="userMenuOpen = !userMenuOpen">
                <div class="user-avatar">{{ authUser.username?.charAt(0)?.toUpperCase() || 'U' }}</div>
                <span class="user-name">{{ authUser.username }}</span>
                <AppIcon
                  name="chevron-down"
                  :size="12"
                  :stroke-width="1.5"
                  color="var(--text-secondary)"
                  :class="['chev', { open: userMenuOpen }]"
                />
              </button>
              <ul v-if="userMenuOpen" class="user-dropdown">
                <li class="user-info">
                  <div class="user-info-name">{{ authUser.username }}</div>
                  <div class="user-info-role">{{ authUser.role || 'user' }}</div>
                </li>
                <li class="user-divider" />
                <li class="user-item danger" @click="handleLogout">
                  <AppIcon name="log-in" :size="14" :stroke-width="1.5" color="var(--color-danger)" />
                  <span>{{ $t('common.logout') }}</span>
                </li>
              </ul>
            </div>
          </template>
          <template v-else>
            <router-link to="/auth?mode=login" class="auth-btn login">
              <AppIcon name="log-in" :size="14" :stroke-width="1.5" />
              <span>{{ $t('common.login') }}</span>
            </router-link>
            <router-link to="/auth?mode=register" class="auth-btn register">
              <AppIcon name="user-plus" :size="14" :stroke-width="1.5" />
              <span>{{ $t('common.register') }}</span>
            </router-link>
          </template>
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
import { reactive, ref, onMounted, onUnmounted, provide } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
import ThemeSwitcher from './components/ThemeSwitcher.vue'
import NexBessLogo from './components/NexBessLogo.vue'
import AppIcon from './components/AppIcon.vue'

const router = useRouter()
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

// 鉴权状态
const authUser = ref(null)
const userMenuOpen = ref(false)
const userMenuRef = ref(null)

function loadAuthUser() {
  const raw = localStorage.getItem('user_info')
  if (!raw) {
    authUser.value = null
    return
  }
  try {
    authUser.value = JSON.parse(raw)
  } catch {
    authUser.value = null
  }
}

function handleLogout() {
  localStorage.removeItem('auth_token')
  localStorage.removeItem('user_info')
  authUser.value = null
  userMenuOpen.value = false
  showToast('已退出登录', 'info')
  if (router.currentRoute.value.path === '/auth') router.push('/')
}

function onStorage(e) {
  if (e.key === 'user_info' || e.key === 'auth_token') loadAuthUser()
}

function onDocClick(e) {
  if (!userMenuRef.value) return
  if (!userMenuRef.value.contains(e.target)) userMenuOpen.value = false
}

onMounted(() => {
  loadAuthUser()
  window.addEventListener('storage', onStorage)
  document.addEventListener('click', onDocClick)
})

onUnmounted(() => {
  window.removeEventListener('storage', onStorage)
  document.removeEventListener('click', onDocClick)
})
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
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 32px;
  padding: 0 14px;
  border-radius: var(--radius-md);
  font-size: 13px;
  font-weight: 500;
  text-decoration: none;
  border: 1px solid var(--color-border);
  background: var(--bg-card);
  color: var(--text-secondary);
  cursor: pointer;
  transition:
    background 0.2s ease,
    color 0.2s ease,
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.auth-btn:hover {
  color: var(--text-primary);
  border-color: var(--border-color-hover);
  background: var(--bg-card-solid);
  box-shadow: var(--shadow-card-glow);
}

.auth-btn:focus-visible {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px var(--color-accent-glow);
}

.auth-btn.active {
  color: var(--accent-blue);
  border-color: var(--accent-blue);
  box-shadow: var(--shadow-card-glow);
}

.auth-btn.register {
  color: var(--color-text-on-accent);
  background: var(--color-accent);
  border-color: var(--color-accent);
}

.auth-btn.register:hover {
  opacity: 0.92;
  background: var(--color-accent);
  border-color: var(--color-accent);
  color: var(--color-text-on-accent);
  box-shadow: 0 4px 12px var(--color-accent-glow);
}

.auth-btn svg {
  width: 14px;
  height: 14px;
  stroke: currentColor;
  flex-shrink: 0;
}

/* ===== 已登录态：用户菜单 ===== */
.user-menu {
  position: relative;
}

.user-trigger {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 36px;
  padding: 0 12px 0 6px;
  border-radius: 999px;
  background: var(--bg-card);
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

.user-trigger:hover {
  border-color: var(--border-color-hover);
  background: var(--bg-card-solid);
  box-shadow: var(--shadow-card-glow);
}

.user-trigger:focus-visible {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px var(--color-accent-glow);
}

.user-avatar {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-accent) 0%, var(--accent-blue) 100%);
  color: var(--color-text-on-accent);
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.user-name {
  max-width: 120px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1;
}

.chev {
  transition: transform 0.2s ease;
}
.chev.open {
  transform: rotate(180deg);
}

.user-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 200px;
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

.user-info {
  padding: 10px 12px 8px;
}

.user-info-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.2;
}

.user-info-role {
  font-size: 11px;
  color: var(--text-secondary);
  margin-top: 2px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.user-divider {
  height: 1px;
  background: var(--color-border);
  margin: 4px 6px;
}

.user-item {
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

.user-item:hover {
  background: var(--color-card-hover);
}

.user-item.danger {
  color: var(--color-danger);
}

.user-item.danger:hover {
  background: rgba(239, 68, 68, 0.08);
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
