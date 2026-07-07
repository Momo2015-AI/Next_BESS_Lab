<template>
  <div>
    <label class="block mb-0.5 text-muted">{{ label }}</label>
    <select
      v-if="type === 'select'"
      :value="modelValue"
      class="w-full rounded px-2 py-1 text-xs input-dark"
      @change="$emit('update:modelValue', $event.target.value)"
    >
      <option v-for="opt in options" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
    </select>
    <input
      v-else
      :value="modelValue"
      :type="type"
      :step="step"
      class="w-full rounded px-2 py-1 text-xs input-dark"
      @input="$emit('update:modelValue', type === 'number' ? Number($event.target.value) : $event.target.value)"
    />
  </div>
</template>

<script setup>
defineProps({
  label: { type: String, required: true },
  modelValue: { type: [String, Number], default: '' },
  type: { type: String, default: 'number' },
  step: { type: [String, Number], default: '0.1' },
  options: { type: Array, default: () => [] }
})
defineEmits(['update:modelValue'])
</script>
