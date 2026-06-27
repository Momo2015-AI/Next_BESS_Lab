<template>
  <div class="tool-page">
    <div class="tool-header"><h1>配置规则</h1><p>管理系统配置规则与约束</p></div>
    <RulesConfig />
  </div>
</template>

<script setup>
import RulesConfig from '../views/RulesConfig.vue'
</script>

<style scoped>
.tool-page { padding: 24px; }
.tool-header { margin-bottom: 24px; }
.tool-header h1 { font-size: 24px; font-weight: 700; margin: 0 0 8px; }
.tool-header p { color: #666; font-size: 14px; margin: 0; }
</style>
