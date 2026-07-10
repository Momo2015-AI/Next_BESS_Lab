<template>
  <AppPage title-key="tools.formulaTitle" desc-key="tools.formulaDesc">
    <FormulaLab :params="store.systemParams" @update="(key, val) => (store.systemParams[key] = val)" />
  </AppPage>
</template>

<script setup>
import { useBessStore } from '../stores/bess.js'
import AppPage from '../components/AppPage.vue'
import FormulaLab from '../components/FormulaLab.vue'
const store = useBessStore()
</script>
