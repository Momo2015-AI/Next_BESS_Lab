<template>
  <div class="tool-page">
    <div class="tool-header"><h1>历史项目</h1><p>查看和管理历史项目记录</p></div>
    <ProjectHistory />
  </div>
</template>

<script setup>
import ProjectHistory from '../views/ProjectHistory.vue'
</script>

<style scoped>
.tool-page { padding: 24px; }
.tool-header { margin-bottom: 24px; }
.tool-header h1 { font-size: 24px; font-weight: 700; margin: 0 0 8px; }
.tool-header p { color: #666; font-size: 14px; margin: 0; }
</style>
