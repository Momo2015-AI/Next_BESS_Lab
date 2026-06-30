<template>
  <div class="tool-page">
    <div class="tool-header"><h1>参数配置面板</h1><p>统一管理系统参数</p></div>
    <ParameterPanel :params="store.systemParams" @update="(key, val) => store.systemParams[key] = val" @error="msg => store.calculationError = msg" />
  </div>
</template>

<script setup>
import { useBessStore } from '../stores/bess.js'
import ParameterPanel from '../components/ParameterPanel.vue'
const store = useBessStore()
</script>

<style scoped>
.tool-page { padding: 24px; }
.tool-header { margin-bottom: 24px; }
.tool-header h1 { font-size: 24px; font-weight: 700; margin: 0 0 8px; }
.tool-header p { color: var(--text-secondary, #666); font-size: 14px; margin: 0; }
</style>
