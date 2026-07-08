<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>{{ $t('tools.auxPowerTitle') }}</h1>
      <p>{{ $t('tools.auxPowerDesc') }}</p>
    </div>
    <AuxPowerCalculator @error="(msg) => $emit('error', msg)" />
  </div>
</template>

<script setup>
import AuxPowerCalculator from '../components/AuxPowerCalculator.vue'
</script>

<style scoped></style>
