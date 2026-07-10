<template>
  <AppPage title-key="tools.auxPowerTitle" desc-key="tools.auxPowerDesc">
    <AuxPowerCalculator @error="(msg) => $emit('error', msg)" />
  </AppPage>
</template>

<script setup>
import AppPage from '../components/AppPage.vue'
import AuxPowerCalculator from '../components/AuxPowerCalculator.vue'
</script>
