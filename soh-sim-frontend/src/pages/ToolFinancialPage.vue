<template>
  <div class="tool-page">
    <div class="tool-header"><h1>财务看板</h1><p>CAPEX/OPEX/IRR/LCOS/DSCR 全景财务指标</p></div>
    <FinancialDashboard :params="store.systemParams" :results="store.results" :soh="store.degradation.soh" :rte="store.degradation.rte" :augQty="store.degradation.augQty" />
  </div>
</template>

<script setup>
import { useBessStore } from '../stores/bess.js'
import FinancialDashboard from '../components/FinancialDashboard.vue'
const store = useBessStore()
</script>

<style scoped>
.tool-page { padding: 24px; }
.tool-header { margin-bottom: 24px; }
.tool-header h1 { font-size: 24px; font-weight: 700; margin: 0 0 8px; }
.tool-header p { color: #666; font-size: 14px; margin: 0; }
</style>
