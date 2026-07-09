/**
 * 权限管理 Composable
 *
 * 从 sessionStorage 中的 user_info 读取用户角色和权限，
 * 提供权限检查方法供路由守卫、侧边栏过滤和页面组件使用。
 */

import { computed, ref } from 'vue'

/** 用户信息（含 role, effective_role, permissions） */
const userInfo = ref(null)

/** 从 sessionStorage 加载用户信息 */
function loadUserInfo() {
  try {
    const raw = sessionStorage.getItem('user_info')
    if (!raw) {
      userInfo.value = null
      return
    }
    userInfo.value = JSON.parse(raw)
  } catch {
    userInfo.value = null
  }
}

/** 当前角色（考虑临时角色覆盖后的有效角色） */
const effectiveRole = computed(() => userInfo.value?.effective_role || userInfo.value?.role || null)

/** 原始角色 */
const originalRole = computed(() => userInfo.value?.role || null)

/** 权限映射表 */
const permissions = computed(() => userInfo.value?.permissions || {})

/** 是否已登录 */
const isLoggedIn = computed(() => !!userInfo.value)

/** 是否是管理员 */
const isAdmin = computed(() => effectiveRole.value === 'admin')

/**
 * 检查对某个功能模块的权限级别
 * @param {string} key - 权限模块 key (如 'phase1', 'tool_formula')
 * @returns {'full'|'readonly'|'hidden'} 权限级别
 */
function getPermission(key) {
  return permissions.value[key] || 'hidden'
}

/**
 * 是否可以查看某个模块（有 full 或 readonly 权限）
 * @param {string} key - 权限模块 key
 * @returns {boolean}
 */
function canView(key) {
  const level = getPermission(key)
  return level === 'full' || level === 'readonly'
}

/**
 * 是否可以编辑某个模块（有 full 权限）
 * @param {string} key - 权限模块 key
 * @returns {boolean}
 */
function canEdit(key) {
  return getPermission(key) === 'full'
}

/**
 * 是否完全无权访问某个模块
 * @param {string} key - 权限模块 key
 * @returns {boolean}
 */
function isHidden(key) {
  return getPermission(key) === 'hidden'
}

// 初始化加载
loadUserInfo()

// 监听 storage 变化（跨标签页同步）
if (typeof window !== 'undefined') {
  window.addEventListener('storage', (e) => {
    if (e.key === 'user_info') {
      loadUserInfo()
    }
  })
}

export function usePermission() {
  return {
    userInfo,
    effectiveRole,
    originalRole,
    permissions,
    isLoggedIn,
    isAdmin,
    getPermission,
    canView,
    canEdit,
    isHidden,
    loadUserInfo,
  }
}
