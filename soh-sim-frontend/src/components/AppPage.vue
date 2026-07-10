<template>
  <div class="app-page">
    <div class="app-page-header">
      <h1 v-if="titleKey">{{ $t(titleKey) }}</h1>
      <h1 v-else-if="title">{{ title }}</h1>
      <p v-if="descKey" class="app-page-desc">{{ $t(descKey) }}</p>
      <p v-else-if="desc" class="app-page-desc">{{ desc }}</p>
      <div v-if="$slots.actions" class="app-page-actions">
        <slot name="actions" />
      </div>
    </div>
    <div class="app-page-body">
      <slot />
    </div>
  </div>
</template>

<script setup>
defineProps({
  titleKey: { type: String, default: '' },
  descKey: { type: String, default: '' },
  title: { type: String, default: '' },
  desc: { type: String, default: '' }
})
</script>

<style scoped>
.app-page {
  padding: 24px;
}

.app-page-header {
  margin-bottom: 28px;
}

.app-page-header h1 {
  font-size: 24px;
  font-weight: 800;
  margin: 0 0 8px;
  color: var(--section-title-color, var(--color-text));
  letter-spacing: -0.02em;
}

.app-page-desc {
  color: var(--color-text-muted);
  font-size: 14px;
  margin: 0;
}

.app-page-actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
  flex-wrap: wrap;
}

.app-page-body {
  min-height: 400px;
}
</style>
