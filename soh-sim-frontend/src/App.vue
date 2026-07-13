<template>
  <div class="app-shell">
    <div v-if="toast.show" class="toast-notification" :class="'toast-' + toast.type">
      {{ toast.message }}
    </div>

    <header class="app-header">
      <div class="header-inner">
        <router-link ref="brandRef" to="/" class="brand">
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
                  <div class="user-info-role">{{ getRoleLabel(authUser.effective_role || authUser.role) }}</div>
                </li>
                <li class="user-divider" />
                <li v-if="canAccessAdmin" class="user-item" @click="goToAdmin">
                  <AppIcon name="shield" :size="14" :stroke-width="1.5" color="var(--text-secondary)" />
                  <span>{{ $t('admin.title') }}</span>
                </li>
                <li v-if="canAccessAdmin" class="user-divider" />
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
import { reactive, ref, computed, onMounted, onUnmounted, provide, nextTick } from 'vue'
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

// ===== 侧边栏宽度与 LOGO 宽度同步 =====
const brandRef = ref(null)
const logoWidth = ref(260) // 默认 fallback

function syncSidebarWidth() {
  if (!brandRef.value) return
  const brandRect = brandRef.value.getBoundingClientRect()
  if (brandRect.width <= 0) return

  // 关键：Sidebar width 是 CSS 宽度（相对其 containing block），
  // 而 brandRect.right 是视口坐标。两者坐标系不同会导致偏移。
  // 正确做法：sidebarWidth = Logo右边缘(视口) - Sidebar左边缘(视口)
  const sidebarEl = document.querySelector('.sidebar-container')
  if (!sidebarEl) {
    // fallback: 假设 Sidebar 从视口 x=0 开始（无 body margin 时成立）
    logoWidth.value = Math.ceil(brandRect.right)
  } else {
    const sidebarRect = sidebarEl.getBoundingClientRect()
    logoWidth.value = Math.ceil(brandRect.right - sidebarRect.left)
  }
  document.documentElement.style.setProperty('--sidebar-width', logoWidth.value + 'px')
}

onMounted(() => {
  nextTick(() => {
    syncSidebarWidth()
  })
  // 监听窗口缩放
  window.addEventListener('resize', syncSidebarWidth)
})

onUnmounted(() => {
  window.removeEventListener('resize', syncSidebarWidth)
})

// 鉴权状态
const authUser = ref(null)
const userMenuOpen = ref(false)
const userMenuRef = ref(null)

function loadAuthUser() {
  const raw = sessionStorage.getItem('user_info')
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

// 管理员权限检查
const canAccessAdmin = computed(() => {
  if (!authUser.value) return false
  const role = authUser.value.effective_role || authUser.value.role
  return role === 'admin'
})

function goToAdmin() {
  userMenuOpen.value = false
  router.push('/admin')
}

const ROLE_LABELS = {
  developer: '开发商',
  solution_engineer: '方案工程师',
  epc_contractor: 'EPC承包商',
  financial_analyst: '财务分析师',
  project_manager: '项目经理',
  admin: '管理员'
}

function getRoleLabel(role) {
  return ROLE_LABELS[role] || role || '用户'
}

function handleLogout() {
  sessionStorage.removeItem('auth_token')
  sessionStorage.removeItem('user_info')
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
