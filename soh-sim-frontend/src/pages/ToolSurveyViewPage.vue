<template>
  <div class="tool-page">
    <div class="tool-header"><h1>调研输入</h1><p>项目调研表数据录入与管理</p></div>
    <SurveyView />
  </div>
</template>

<script setup>
import SurveyView from '../views/SurveyView.vue'
</script>

<style scoped>
.tool-page { padding: 24px; }
.tool-header { margin-bottom: 24px; }
.tool-header h1 { font-size: 24px; font-weight: 700; margin: 0 0 8px; }
.tool-header p { color: #666; font-size: 14px; margin: 0; }
</style>
