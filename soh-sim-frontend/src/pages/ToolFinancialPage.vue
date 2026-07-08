<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>{{ $t('tools.financialTitle') }}</h1>
      <p>{{ $t('tools.financialDesc') }}</p>
    </div>
    <FinancialDashboard
      :params="store.systemParams"
      :results="store.results"
      :soh="store.degradation.soh"
      :rte="store.degradation.rte"
      :aug-qty="store.degradation.augQty"
    />
  </div>
</template>

<script setup>
import { useBessStore } from '../stores/bess.js'
import FinancialDashboard from '../components/FinancialDashboard.vue'
const store = useBessStore()
</script>

<style scoped></style>
