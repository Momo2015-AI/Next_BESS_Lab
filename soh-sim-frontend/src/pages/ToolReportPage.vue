<template>
  <div class="tool-page">
    <div class="tool-header"><h1>报告输出</h1><p>生成仿真报告、导出 PDF/Excel</p></div>
    <ReportView />
  </div>
</template>

<script setup>
import ReportView from '../views/ReportView.vue'
</script>

<style scoped>
.tool-page { padding: 24px; }
.tool-header { margin-bottom: 24px; }
.tool-header h1 { font-size: 24px; font-weight: 700; margin: 0 0 8px; }
.tool-header p { color: #666; font-size: 14px; margin: 0; }
</style>
