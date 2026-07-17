<template>
  <div>
    <h3 class="text-sm font-bold mb-3 flex items-center gap-2 text-accent">
      <span class="w-2 h-2 rounded-full bg-accent" />
      {{ $t('simLab.titleAlgorithm') }}
    </h3>

    <div class="grid grid-cols-3 gap-3">
      <div
        v-for="algo in algorithms"
        :key="algo.id"
        class="rounded-lg p-4 border-2 cursor-pointer transition-all flex flex-col"
        :class="selectedId === algo.id ? 'algo-selected' : 'algo-default'"
        @click="$emit('select', algo)"
      >
        <div class="flex items-center gap-2 mb-2">
          <span
            class="w-4 h-4 rounded-full"
            :class="selectedId === algo.id ? 'algo-dot-selected' : 'algo-dot-default'"
          />
          <h4 class="text-xs font-bold" :class="selectedId === algo.id ? 'algo-name-selected' : 'algo-name-default'">
            {{ algo.name }}
          </h4>
        </div>
        <p v-if="algo.name_en" class="text-[10px] mb-2 text-muted italic">{{ algo.name_en }}</p>
        <p class="text-[10px] mb-2 text-secondary flex-1">{{ algo.description }}</p>
        <div class="text-[10px] text-muted">
          <span class="inline-block rounded px-1.5 py-0.5 mr-1 theme-bg-card">{{ algo.type }}</span>
          <span class="text-secondary">{{ $t('simLab.accuracy') }}: {{ algo.accuracy }}</span>
        </div>
        <div class="mt-2 text-[10px] font-mono truncate text-accent">{{ algo.mathematical_form }}</div>
        <div
          v-if="algo.formula_expression"
          class="mt-1 text-[10px] font-mono truncate text-secondary opacity-75"
          :title="algo.formula_expression"
        >
          = {{ algo.formula_expression }}
        </div>
      </div>
    </div>

    <div v-if="algorithms.length === 0" class="text-center py-8 text-muted">
      <div>{{ $t('simLab.noAlgo') }}</div>
    </div>

    <div v-if="selectedDetail" class="mt-4 rounded p-3 card-panel-bordered">
      <div class="flex justify-between items-center mb-2">
        <h4 class="text-xs font-medium">{{ $t('simLab.algoParams', { name: selectedDetail.name }) }}</h4>
        <button
          class="text-[10px] rounded px-2 py-0.5 transition-colors theme-bg-card text-muted"
          @click="$emit('reset-params')"
        >
          {{ $t('simLab.btnRestoreDefault') }}
        </button>
      </div>
      <div class="grid grid-cols-4 gap-3">
        <div v-for="(param, key) in selectedDetail.parameters" :key="key">
          <label class="text-[10px] block mb-1 text-muted">{{ param.label }} ({{ param.unit || '' }})</label>
          <input
            :value="algoParams[key]"
            type="number"
            :step="param.step || 0.01"
            :min="param.min"
            :max="param.max"
            class="w-full rounded px-2 py-1 text-xs card-input"
            @input="$emit('update-param', { key, value: Number($event.target.value) })"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  algorithms: { type: Array, default: () => [] },
  selectedId: { type: String, default: '' },
  selectedDetail: { type: Object, default: null },
  algoParams: { type: Object, default: () => ({}) }
})

defineEmits(['select', 'reset-params', 'update-param'])
</script>
