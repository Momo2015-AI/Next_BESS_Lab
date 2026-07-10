<template>
  <AppPage title-key="tools.dataInjectTitle" desc-key="tools.dataInjectDesc">
    <DataInjection
      :soh="store.degradation.soh"
      :rte="store.degradation.rte"
      @update:soh="store.degradation.soh = $event"
      @update:rte="store.degradation.rte = $event"
    />
  </AppPage>
</template>

<script setup>
import { useBessStore } from '../stores/bess.js'
import AppPage from '../components/AppPage.vue'
import DataInjection from '../components/DataInjection.vue'
const store = useBessStore()
</script>
