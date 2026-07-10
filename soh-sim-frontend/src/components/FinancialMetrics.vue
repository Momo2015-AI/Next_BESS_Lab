<template>
  <div class="grid grid-cols-4 md:grid-cols-8 gap-2 mb-3">
    <div
      v-for="(m, idx) in metrics"
      :key="m.label"
      class="rounded-lg p-3 text-center transition-all hover:shadow-md"
      :style="{
        backgroundColor: 'var(--color-card)',
        border: '1px solid var(--color-border)',
        borderTop: '3px solid ' + (metrics[idx]?.borderColor || m.textColor || 'var(--color-accent)')
      }"
    >
      <div class="text-[9px] uppercase tracking-wider truncate ins-1">
        {{ m.label }}
      </div>
      <div class="text-base md:text-lg font-bold font-mono mt-1" :style="{ color: m.textColor }">
        {{ m.value }}
      </div>
      <div class="text-[8px] mt-0.5 ins-1">
        {{ m.unit }}
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  metrics: { type: Array, required: true }
})
</script>

<style scoped>
.ins-1 { color: var(--color-text-muted) }
</style>
