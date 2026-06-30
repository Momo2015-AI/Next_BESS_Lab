<template>
  <div class="tool-page">
    <div class="tool-header"><h1>方案设计</h1><p>配置方案参数、保存版本、对比方案</p></div>
    <ConfigView />
  </div>
</template>

<script setup>
import ConfigView from '../views/ConfigView.vue'
</script>

<style scoped>
.tool-page { padding: 24px; }
.tool-header { margin-bottom: 24px; }
.tool-header h1 { font-size: 24px; font-weight: 700; margin: 0 0 8px; }
.tool-header p { color: #666; font-size: 14px; margin: 0; }
</style>
