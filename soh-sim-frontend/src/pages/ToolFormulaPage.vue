<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>算法与公式</h1>
      <p>查看和调整 SOH 仿真算法参数</p>
    </div>
    <FormulaLab :params="store.systemParams" @update="(key, val) => (store.systemParams[key] = val)" />
  </div>
</template>

<script setup>
import { useBessStore } from '../stores/bess.js'
import FormulaLab from '../components/FormulaLab.vue'
const store = useBessStore()
</script>

<style scoped></style>
