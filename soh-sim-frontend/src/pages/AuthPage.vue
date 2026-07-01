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
.tool-page {
  padding: 24px;
}
.tool-header {
  margin-bottom: 24px;
}
.tool-header h1 {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 8px;
}
.tool-header p {
  color: #666;
  font-size: 14px;
  margin: 0;
}
</style>
