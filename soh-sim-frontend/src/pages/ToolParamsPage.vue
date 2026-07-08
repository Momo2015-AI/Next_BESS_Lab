<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>{{ $t('tools.paramsTitle') }}</h1>
      <p>{{ $t('tools.paramsDesc') }}</p>
    </div>
    <ParameterPanel
      :params="store.systemParams"
      @update="(key, val) => (store.systemParams[key] = val)"
      @error="(msg) => (store.calculationError = msg)"
    />
  </div>
</template>

<script setup>
import { useBessStore } from '../stores/bess.js'
import ParameterPanel from '../components/ParameterPanel.vue'
const store = useBessStore()
</script>

<style scoped></style>
