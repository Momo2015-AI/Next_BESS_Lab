<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>{{ $t('admin.title') }}</h1>
      <p>{{ $t('admin.desc') }}</p>
    </div>
    <AdminPanel :initial-tab="$route.query.tab || ''" />
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import AdminPanel from '../components/AdminPanel.vue'

const $route = useRoute()
</script>
