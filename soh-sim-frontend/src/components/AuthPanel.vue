<template>
  <div class="auth-panel h-full flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- 登录/注册表单 -->
      <div class="bg-slate-900/80 rounded-xl border border-slate-700 p-6 shadow-2xl">
        <div class="text-center mb-6">
          <h2 class="text-xl font-bold text-teal-400 mb-1">
            {{ isLogin ? '用户登录' : '用户注册' }}
          </h2>
          <p class="text-xs text-slate-400">
            {{ isLogin ? '欢迎回来' : '创建新账号' }}
          </p>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label class="block text-xs text-slate-400 mb-1">用户名 / 邮箱</label>
            <input v-model="form.username" type="text" required
              class="w-full bg-slate-800 text-white px-3 py-2 rounded-lg border border-slate-600 focus:border-teal-500 outline-none text-sm"
              placeholder="输入用户名或邮箱">
          </div>

          <div v-if="!isLogin">
            <label class="block text-xs text-slate-400 mb-1">邮箱</label>
            <input v-model="form.email" type="email" required
              class="w-full bg-slate-800 text-white px-3 py-2 rounded-lg border border-slate-600 focus:border-teal-500 outline-none text-sm"
              placeholder="输入邮箱地址">
          </div>

          <div>
            <label class="block text-xs text-slate-400 mb-1">密码</label>
            <div class="relative">
              <input v-model="form.password" :type="showPassword ? 'text' : 'password'" required
                class="w-full bg-slate-800 text-white px-3 py-2 rounded-lg border border-slate-600 focus:border-teal-500 outline-none text-sm"
                placeholder="输入密码">
              <button type="button" @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-300">
                <svg v-if="showPassword" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"></path>
                </svg>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                </svg>
              </button>
            </div>
          </div>

          <div v-if="!isLogin" class="flex items-start gap-2">
            <input type="checkbox" v-model="agreedToTerms" required class="accent-teal-500 mt-0.5">
            <span class="text-xs text-slate-400">
              我已阅读并同意 <a href="#" class="text-teal-400 hover:underline">服务条款</a> 和 <a href="#" class="text-teal-400 hover:underline">隐私政策</a>
            </span>
          </div>

          <button type="submit" :disabled="loading || (!isLogin && !agreedToTerms)"
            class="w-full bg-gradient-to-r from-teal-500 to-emerald-600 hover:from-teal-600 hover:to-emerald-700 disabled:from-slate-600 disabled:to-slate-600 text-white font-bold text-sm py-2 rounded-lg transition-all shadow-lg">
            {{ loading ? '处理中...' : (isLogin ? '登 录' : '注 册') }}
          </button>

          <div class="text-center">
            <button type="button" @click="isLogin = !isLogin; clearForm()"
              class="text-xs text-teal-400 hover:text-teal-300">
              {{ isLogin ? '还没有账号？立即注册' : '已有账号？立即登录' }}
            </button>
          </div>
        </form>

        <!-- 错误提示 -->
        <div v-if="errorMessage" class="mt-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg">
          <p class="text-xs text-red-400">{{ errorMessage }}</p>
        </div>
      </div>

      <!-- 快捷登录（演示用） -->
      <div class="mt-4 p-3 bg-slate-800/50 rounded-lg border border-slate-700">
        <div class="text-xs text-slate-400 text-center mb-2">快捷体验（无需注册）</div>
        <div class="flex gap-2">
          <button @click="quickLogin('admin')" class="flex-1 bg-slate-700 hover:bg-slate-600 text-slate-300 text-xs py-1.5 rounded">
            管理员
          </button>
          <button @click="quickLogin('engineer')" class="flex-1 bg-slate-700 hover:bg-slate-600 text-slate-300 text-xs py-1.5 rounded">
            仿真工程师
          </button>
          <button @click="quickLogin('guest')" class="flex-1 bg-slate-700 hover:bg-slate-600 text-slate-300 text-xs py-1.5 rounded">
            访客
          </button>
        </div>
      </div>
    </div>

    <!-- Toast提示 -->
    <div v-if="toast.show"
      :class="['fixed bottom-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all',
        toast.type === 'success' ? 'bg-emerald-500 text-white' : 'bg-red-500 text-white']">
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const emit = defineEmits(['auth-success'])

const isLogin = ref(true)
const showPassword = ref(false)
const loading = ref(false)
const agreedToTerms = ref(false)
const errorMessage = ref('')

const form = reactive({
  username: '',
  email: '',
  password: '',
})

const toast = reactive({
  show: false,
  message: '',
  type: 'success',
})

const showToast = (message, type = 'success') => {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => {
    toast.show = false
  }, 3000)
}

function clearForm() {
  form.username = ''
  form.email = ''
  form.password = ''
  errorMessage.value = ''
  agreedToTerms.value = false
}

async function handleSubmit() {
  errorMessage.value = ''
  loading.value = true

  const endpoint = isLogin.value ? '/api/auth/login' : '/api/auth/register'
  const payload = isLogin.value
    ? { username: form.username, password: form.password }
    : { username: form.username, email: form.email, password: form.password }

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })

    const result = await response.json()

    if (result.success) {
      // 保存token和用户信息
      localStorage.setItem('auth_token', result.token)
      localStorage.setItem('user_info', JSON.stringify(result.user))
      
      showToast(isLogin.value ? '登录成功' : '注册成功')
      emit('auth-success', result.user)
    } else {
      errorMessage.value = result.error || '操作失败'
    }
  } catch (error) {
    console.error('认证失败:', error)
    errorMessage.value = '网络错误，请稍后重试'
  } finally {
    loading.value = false
  }
}

// 快捷登录（演示用，实际不会有这个功能）
async function quickLogin(role) {
  loading.value = true
  
  // 模拟快速登录
  const mockUsers = {
    admin: { id: 'admin-001', username: 'admin', email: 'admin@soh-sim.com', role: 'admin' },
    engineer: { id: 'eng-001', username: 'engineer', email: 'engineer@soh-sim.com', role: 'engineer' },
    guest: { id: 'guest-001', username: 'guest', email: 'guest@soh-sim.com', role: 'guest' },
  }
  
  const mockToken = `mock-token-${role}-${Date.now()}`
  
  localStorage.setItem('auth_token', mockToken)
  localStorage.setItem('user_info', JSON.stringify(mockUsers[role]))
  
  showToast(`${role === 'admin' ? '管理员' : role === 'engineer' ? '仿真工程师' : '访客'} 登录成功`)
  emit('auth-success', mockUsers[role])
  
  loading.value = false
}

// 检查是否已登录
function checkAuth() {
  const token = localStorage.getItem('auth_token')
  const userInfo = localStorage.getItem('user_info')
  
  if (token && userInfo) {
    try {
      const user = JSON.parse(userInfo)
      emit('auth-success', user)
      return true
    } catch {
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user_info')
    }
  }
  return false
}

// 获取当前用户
function getCurrentUser() {
  const userInfo = localStorage.getItem('user_info')
  if (userInfo) {
    try {
      return JSON.parse(userInfo)
    } catch {
      return null
    }
  }
  return null
}

// 登出
function logout() {
  localStorage.removeItem('auth_token')
  localStorage.removeItem('user_info')
  showToast('已退出登录')
}

// 获取token
function getToken() {
  return localStorage.getItem('auth_token')
}

// 导出方法
defineExpose({ checkAuth, getCurrentUser, logout, getToken })
</script>

<style scoped>
.auth-panel {
  height: 100%;
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%);
}
</style>