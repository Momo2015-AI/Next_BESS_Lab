<template>
  <div class="form-field">
    <label v-if="label" :for="inputId" class="form-field-label">
      <span>{{ label }}</span>
      <span v-if="required" class="required">*</span>
      <span v-else-if="optional" class="optional">(optional)</span>
    </label>

    <select
      v-if="type === 'select'"
      :id="inputId"
      class="form-field-select"
      :value="modelValue ?? ''"
      :disabled="disabled"
      @change="onInput"
      @blur="emit('blur', $event)"
      @focus="emit('focus', $event)"
    >
      <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
      <option v-for="opt in normalizedOptions" :key="opt.value" :value="opt.value">
        {{ opt.label }}
      </option>
    </select>

    <textarea
      v-else-if="type === 'textarea'"
      :id="inputId"
      class="form-field-textarea"
      :value="modelValue ?? ''"
      :placeholder="placeholder"
      :disabled="disabled"
      :readonly="readonly"
      @input="onInput"
      @blur="emit('blur', $event)"
      @focus="emit('focus', $event)"
    />

    <input
      v-else
      :id="inputId"
      class="form-field-input"
      :type="type"
      :value="modelValue ?? ''"
      :placeholder="placeholder"
      :min="min"
      :max="max"
      :step="step"
      :disabled="disabled"
      :readonly="readonly"
      @input="onInput"
      @blur="emit('blur', $event)"
      @focus="emit('focus', $event)"
    />

    <div v-if="error" class="form-field-error">{{ error }}</div>
    <div v-else-if="hint" class="form-field-hint">{{ hint }}</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: { type: String, default: '' },
  required: { type: Boolean, default: false },
  optional: { type: Boolean, default: false },
  type: { type: String, default: 'text' }, // text | number | email | select | textarea
  modelValue: { type: [String, Number, null], default: null },
  placeholder: { type: String, default: '' },
  options: { type: Array, default: () => [] }, // [{label, value}] or [string]
  error: { type: String, default: '' },
  hint: { type: String, default: '' },
  min: { type: [String, Number], default: undefined },
  max: { type: [String, Number], default: undefined },
  step: { type: [String, Number], default: undefined },
  disabled: { type: Boolean, default: false },
  readonly: { type: Boolean, default: false }
})

const emit = defineEmits(['update:modelValue', 'change', 'blur', 'focus'])

const inputId = computed(() => `ff-${Math.random().toString(36).slice(2, 9)}`)

function onInput(e) {
  let v = e.target.value
  if (props.type === 'number') {
    v = v === '' ? null : Number(v)
  }
  emit('update:modelValue', v)
  emit('change', e)
}

const normalizedOptions = computed(() => {
  return props.options.map((opt) => {
    if (typeof opt === 'object' && opt !== null) {
      return { label: opt.label, value: opt.value }
    }
    return { label: String(opt), value: opt }
  })
})
</script>
