<script setup>
defineProps({
  number: { type: [String, Number], required: true },
  title: { type: String, required: true },
  subtitle: { type: String, default: '' }
})
</script>

<template>
  <section class="section-card">
    <header class="section-card-header">
      <span class="section-number-badge">{{ number }}</span>
      <span class="section-divider" aria-hidden="true" />
      <h2 class="section-title">{{ title }}</h2>
    </header>
    <p v-if="subtitle" class="section-subtitle">{{ subtitle }}</p>
    <slot />
  </section>
</template>
