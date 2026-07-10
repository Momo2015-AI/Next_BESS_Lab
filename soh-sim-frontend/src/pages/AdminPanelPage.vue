<template>
  <AppPage title-key="admin.title" desc-key="admin.desc">
    <AdminPanel :initial-tab="$route.query.tab || ''" />
  </AppPage>
</template>

<script setup>
import { useRoute } from 'vue-router'
import AppPage from '../components/AppPage.vue'
import AdminPanel from '../components/AdminPanel.vue'

const $route = useRoute()
</script>
