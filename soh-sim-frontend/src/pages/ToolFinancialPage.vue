<template>
  <AppPage title-key="tools.financialTitle" desc-key="tools.financialDesc">
    <FinancialDashboard
      :params="store.systemParams"
      :results="store.results"
      :soh="store.degradation.soh"
      :rte="store.degradation.rte"
      :aug-qty="store.degradation.augQty"
    />
  </AppPage>
</template>

<script setup>
import { useBessStore } from '../stores/bess.js'
import AppPage from '../components/AppPage.vue'
import FinancialDashboard from '../components/FinancialDashboard.vue'
const store = useBessStore()
</script>
