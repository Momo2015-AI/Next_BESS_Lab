<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>{{ $t('tools.formulaTitle') }}</h1>
      <p>{{ $t('tools.formulaDesc') }}</p>
    </div>
    <FormulaLab :params="store.systemParams" @update="(key, val) => (store.systemParams[key] = val)" />
  </div>
</template>

<script setup>
import { useBessStore } from '../stores/bess.js'
import FormulaLab from '../components/FormulaLab.vue'
const store = useBessStore()
</script>

<style scoped></style>
