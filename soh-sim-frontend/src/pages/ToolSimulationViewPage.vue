<template>
  <AppPage>
    <SimulationLab @error="onError" />
  </AppPage>
</template>

<script setup>
import AppPage from '../components/AppPage.vue'
import SimulationLab from '../components/SimulationLab.vue'

function onError(err) {
  console.error('SimulationLab error:', err)
}
</script>
