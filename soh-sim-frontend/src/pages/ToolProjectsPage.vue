<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>{{ $t('tools.projectsTitle') }}</h1>
      <p>{{ $t('tools.projectsDesc') }}</p>
    </div>
    <SectionCard number="00" :title="$t('tools.projectsSectionTitle')" :subtitle="$t('tools.projectsSectionSubtitle')">
      <p class="placeholder-text">{{ $t('tools.projectsPlaceholder') }}</p>
    </SectionCard>
  </div>
</template>

<script setup>
import SectionCard from '../components/SectionCard.vue'
</script>

<style scoped>
.placeholder-text {
  color: var(--color-text-muted);
  font-size: 14px;
  text-align: center;
  padding: 16px 0;
}
</style>
