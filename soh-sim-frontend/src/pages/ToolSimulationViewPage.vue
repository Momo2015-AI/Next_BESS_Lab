<template>
  <div class="tool-page">
    <SimulationLab @error="onError" />
  </div>
</template>

<script setup>
import SimulationLab from '../components/SimulationLab.vue'

function onError(err) {
  console.error('SimulationLab error:', err)
}
</script>

<style scoped>
.tool-page {
  padding: 24px;
}
</style>
