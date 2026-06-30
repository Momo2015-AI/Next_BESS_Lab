<template>
  <div class="tool-page">
    <div class="tool-header"><h1>运行工况</h1><p>配置运行条件和电网参数</p></div>
    <RunningConditions @applyParams="onApply" @error="msg => store.calculationError = msg" />
  </div>
</template>

<script setup>
import { useBessStore } from '../stores/bess.js'
import RunningConditions from '../components/RunningConditions.vue'
const store = useBessStore()

function onApply(mapped) {
  if (mapped.duration != null) store.systemParams.duration = mapped.duration
  if (mapped.cyclesPerDay != null) store.systemParams.cyclesPerDay = mapped.cyclesPerDay
  if (mapped.requiredEnergy != null) store.systemParams.requiredEnergy = mapped.requiredEnergy
}
</script>

<style scoped>
.tool-page { padding: 24px; }
.tool-header { margin-bottom: 24px; }
.tool-header h1 { font-size: 24px; font-weight: 700; margin: 0 0 8px; }
.tool-header p { color: var(--text-secondary, #666); font-size: 14px; margin: 0; }
</style>
