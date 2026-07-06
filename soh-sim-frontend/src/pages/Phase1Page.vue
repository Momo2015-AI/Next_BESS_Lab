<template>
  <div class="phase-page phase1-page">
    <div class="phase-header">
      <h1>{{ $t('phase1.title') }}</h1>
      <p class="phase-desc">{{ $t('phase1.desc') }}</p>
    </div>
    <div class="phase-body">
      <SurveyForm />
    </div>
  </div>
</template>

<script setup>
import SurveyForm from '../components/SurveyForm.vue'
</script>

<style scoped>
.phase-body {
  min-height: 400px;
}
</style>
