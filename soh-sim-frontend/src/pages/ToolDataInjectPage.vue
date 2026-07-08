<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>{{ $t('tools.dataInjectTitle') }}</h1>
      <p>{{ $t('tools.dataInjectDesc') }}</p>
    </div>
    <DataInjection
      :soh="store.degradation.soh"
      :rte="store.degradation.rte"
      @update:soh="store.degradation.soh = $event"
      @update:rte="store.degradation.rte = $event"
    />
  </div>
</template>

<script setup>
import { useBessStore } from '../stores/bess.js'
import DataInjection from '../components/DataInjection.vue'
const store = useBessStore()
</script>

<style scoped></style>
