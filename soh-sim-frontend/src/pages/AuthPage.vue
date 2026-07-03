<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>系统认证</h1>
      <p>登录与权限管理</p>
    </div>
    <AuthPanel @auth-success="(msg) => {}" @error="(msg) => {}" />
  </div>
</template>

<script setup>
import AuthPanel from '../components/AuthPanel.vue'
</script>

<style scoped>
</style>
