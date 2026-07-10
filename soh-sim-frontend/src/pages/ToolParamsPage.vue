<template>
  <AppPage title-key="tools.paramsTitle" desc-key="tools.paramsDesc">
    <ParameterPanel
      :params="store.systemParams"
      @update="(key, val) => (store.systemParams[key] = val)"
      @error="(msg) => (store.calculationError = msg)"
    />
  </AppPage>
</template>

<script setup>
import { useBessStore } from '../stores/bess.js'
import AppPage from '../components/AppPage.vue'
import ParameterPanel from '../components/ParameterPanel.vue'
const store = useBessStore()
</script>
