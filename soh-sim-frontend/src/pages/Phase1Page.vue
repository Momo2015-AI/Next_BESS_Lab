<template>
  <div class="phase-page phase1-page">
    <div class="phase-header">
      <h1>Phase 1: 项目立项</h1>
      <p class="phase-desc">调研填表、选址评估、需求确认</p>
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
