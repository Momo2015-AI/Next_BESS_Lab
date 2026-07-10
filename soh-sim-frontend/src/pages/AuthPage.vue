<template>
  <AppPage title-key="auth.pageTitle" desc-key="auth.pageSubtitle">
    <AuthPanel :default-mode="defaultMode" @auth-success="onAuthSuccess" @error="onError" />
  </AppPage>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppPage from '../components/AppPage.vue'
import AuthPanel from '../components/AuthPanel.vue'

const route = useRoute()
const router = useRouter()

const defaultMode = computed(() => (route.query.mode === 'register' ? 'register' : 'login'))

function onAuthSuccess(user) {
  router.push('/')
}

function onError(msg) {
  // AuthPanel 自带错误提示，此处保留事件以备扩展
}
</script>
