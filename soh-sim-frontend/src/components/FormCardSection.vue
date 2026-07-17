<template>
  <div class="card p-4" :style="{ position: 'relative', zIndex: zIndex }">
    <div class="flex items-center gap-2 mb-3">
      <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold bg-accent-glow text-accent">
        {{ number }}
      </span>
      <div>
        <h3 class="section-title text-accent border-accent">{{ title }}</h3>
      </div>
      <div v-if="$slots.extra" class="ml-auto">
        <slot name="extra" />
      </div>
    </div>
    <slot />
  </div>
</template>

<script setup>
defineProps({
  number: { type: String, default: '' },
  title: { type: String, required: true },
  zIndex: { type: Number, default: 1 }
})
</script>
