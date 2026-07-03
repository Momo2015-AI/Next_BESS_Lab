<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>辅助功耗计算</h1>
      <p>精细计算直流侧和交流侧辅助功耗</p>
    </div>
    <AuxPowerCalculator @error="(msg) => $emit('error', msg)" />
  </div>
</template>

<script setup>
import AuxPowerCalculator from '../components/AuxPowerCalculator.vue'
</script>

<style scoped>
</style>
