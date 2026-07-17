<template>
  <div class="combobox-wrapper">
    <input
      :value="modelValue"
      type="text"
      :placeholder="placeholder"
      class="w-full rounded px-2 py-1 text-xs card-input text-accent"
      @focus="dropdown = true"
      @blur="onBlur"
      @input="onInput"
    />
    <div v-if="dropdown && filteredOptions.length > 0" class="combobox-dropdown">
      <div
        v-for="opt in filteredOptions"
        :key="opt.value"
        class="combobox-option"
        :class="{ active: opt.value === modelValue }"
        @mousedown.prevent="select(opt)"
      >
        <span class="option-name">{{ opt.label }}</span>
        <span v-if="opt.sub" class="option-code">{{ opt.sub }}</span>
      </div>
    </div>
    <div v-else-if="dropdown && modelValue && filteredOptions.length === 0" class="combobox-dropdown">
      <div class="combobox-empty">{{ emptyText }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  modelValue: { type: String, default: '' },
  options: { type: Array, default: () => [] },
  placeholder: { type: String, default: '' },
  emptyText: { type: String, default: 'No match' }
})

const emit = defineEmits(['update:modelValue', 'select'])

const dropdown = ref(false)

const filteredOptions = computed(() => {
  const q = props.modelValue.trim().toLowerCase()
  if (!q) return props.options.slice(0, 20)
  return props.options
    .filter((o) => o.label.toLowerCase().includes(q) || (o.sub || '').toLowerCase().includes(q))
    .slice(0, 20)
})

function onInput(e) {
  emit('update:modelValue', e.target.value)
  dropdown.value = true
}

function onBlur() {
  setTimeout(() => {
    dropdown.value = false
  }, 150)
}

function select(opt) {
  emit('update:modelValue', opt.label)
  emit('select', opt)
  dropdown.value = false
}
</script>
