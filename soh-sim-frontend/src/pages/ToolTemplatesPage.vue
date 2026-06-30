<template>
  <div class="tool-page">
    <div class="tool-header"><h1>校正因子模板</h1><p>管理 Arrhenius 等模型的校正因子模板</p></div>
    <TemplatesConfig />
  </div>
</template>

<script setup>
import TemplatesConfig from '../views/TemplatesConfig.vue'
</script>

<style scoped>
.tool-page { padding: 24px; }
.tool-header { margin-bottom: 24px; }
.tool-header h1 { font-size: 24px; font-weight: 700; margin: 0 0 8px; }
.tool-header p { color: #666; font-size: 14px; margin: 0; }
</style>
