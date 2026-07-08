<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>{{ $t('tools.reportTitle') }}</h1>
      <p>{{ $t('tools.reportDesc') }}</p>
    </div>
    <SectionCard number="00" :title="$t('tools.reportSectionTitle')" :subtitle="$t('tools.reportSectionSubtitle')">
      <p class="placeholder-text">
        {{ $t('tools.reportGuidePrefix') }}
        <router-link to="/phase2" class="inline-link">{{ $t('tools.reportGuidePhase2') }}</router-link>
        {{ $t('tools.reportGuideMiddle') }}
        <router-link to="/tools/simulation-view" class="inline-link">{{ $t('tools.reportGuideSim') }}</router-link>
        {{ $t('tools.reportGuideSuffix') }}
      </p>
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
.inline-link {
  color: var(--color-accent);
  text-decoration: none;
  font-weight: 500;
}
.inline-link:hover {
  text-decoration: underline;
}
</style>
