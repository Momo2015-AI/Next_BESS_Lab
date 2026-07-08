<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>{{ $t('auth.pageTitle') }}</h1>
      <p>{{ $t('auth.pageSubtitle') }}</p>
    </div>
    <AuthPanel :default-mode="defaultMode" @auth-success="onAuthSuccess" @error="onError" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AuthPanel from '../components/AuthPanel.vue'

const route = useRoute()
const router = useRouter()

const defaultMode = computed(() => (route.query.mode === 'register' ? 'register' : 'login'))

function onAuthSuccess(user) {
  // 登录/注册成功后回首页
  router.push('/')
}

function onError(msg) {
  // AuthPanel 自带错误提示，此处保留事件以备扩展
}
</script>

<style scoped></style>
