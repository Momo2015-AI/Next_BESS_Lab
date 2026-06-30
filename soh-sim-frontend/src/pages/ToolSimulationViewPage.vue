<template>
  <div class="tool-page">
    <div class="tool-header"><h1>仿真分析</h1><p>SOH 仿真结果查看与参数调整</p></div>
    <SimulationView />
  </div>
</template>

<script setup>
import SimulationView from '../views/SimulationView.vue'
</script>

<style scoped>
.tool-page { padding: 24px; }
.tool-header { margin-bottom: 24px; }
.tool-header h1 { font-size: 24px; font-weight: 700; margin: 0 0 8px; }
.tool-header p { color: #666; font-size: 14px; margin: 0; }
</style>
