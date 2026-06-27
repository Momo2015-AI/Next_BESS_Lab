<template>
  <div class="tool-page">
    <div class="tool-header"><h1>辅助功耗计算</h1><p>精细计算直流侧和交流侧辅助功耗</p></div>
    <AuxPowerCalculator @error="msg => $emit('error', msg)" />
  </div>
</template>

<script setup>
import AuxPowerCalculator from '../components/AuxPowerCalculator.vue'
</script>

<style scoped>
.tool-page { padding: 24px; }
.tool-header { margin-bottom: 24px; }
.tool-header h1 { font-size: 24px; font-weight: 700; margin: 0 0 8px; }
.tool-header p { color: var(--text-secondary, #666); font-size: 14px; margin: 0; }
</style>
