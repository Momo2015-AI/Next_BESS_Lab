<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>{{ $t('tools.engineeringTitle') }}</h1>
      <p>{{ $t('tools.engineeringDesc') }}</p>
    </div>
    <EngineeringCalc @error="(msg) => $emit('error', msg)" />
  </div>
</template>

<script setup>
import EngineeringCalc from '../components/EngineeringCalc.vue'
</script>

<style scoped></style>
