<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>数据注入</h1>
      <p>手工注入/修正 SOH、RTE 数据序列</p>
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
