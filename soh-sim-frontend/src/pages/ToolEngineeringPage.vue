<template>
  <AppPage title-key="tools.engineeringTitle" desc-key="tools.engineeringDesc">
    <EngineeringCalc @error="(msg) => $emit('error', msg)" />
  </AppPage>
</template>

<script setup>
import AppPage from '../components/AppPage.vue'
import EngineeringCalc from '../components/EngineeringCalc.vue'
</script>
