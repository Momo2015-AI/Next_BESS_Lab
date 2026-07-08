<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>{{ $t('tools.conditionsTitle') }}</h1>
      <p>{{ $t('tools.conditionsDesc') }}</p>
    </div>
    <RunningConditions @apply-params="onApply" @error="(msg) => (store.calculationError = msg)" />
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

<style scoped></style>
