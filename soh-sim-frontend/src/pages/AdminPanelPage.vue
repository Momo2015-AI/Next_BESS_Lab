<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>{{ $t('admin.title') }}</h1>
      <p>{{ $t('admin.desc') }}</p>
    </div>
    <AdminPanel />
  </div>
</template>

<script setup>
import AdminPanel from '../components/AdminPanel.vue'
</script>
