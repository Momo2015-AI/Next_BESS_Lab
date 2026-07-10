<template>
  <AppPage title-key="tools.conditionsTitle" desc-key="tools.conditionsDesc">
    <RunningConditions @apply-params="onApply" @error="(msg) => (store.calculationError = msg)" />
  </AppPage>
</template>

<script setup>
import { useBessStore } from '../stores/bess.js'
import AppPage from '../components/AppPage.vue'
import RunningConditions from '../components/RunningConditions.vue'
const store = useBessStore()

function onApply(mapped) {
  if (mapped.duration != null) store.systemParams.duration = mapped.duration
  if (mapped.cyclesPerDay != null) store.systemParams.cyclesPerDay = mapped.cyclesPerDay
  if (mapped.requiredEnergy != null) store.systemParams.requiredEnergy = mapped.requiredEnergy
}
</script>
