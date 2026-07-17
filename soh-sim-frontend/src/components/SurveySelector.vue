<template>
  <div class="rounded-lg p-4 card-panel">
    <h3 class="text-sm font-bold mb-3 flex items-center gap-2 text-accent">
      <span class="w-2 h-2 rounded-full bg-accent" />
      {{ $t('simLab.titleSurvey') }}
    </h3>

    <div class="grid grid-cols-2 gap-4">
      <div class="space-y-2">
        <label class="text-xs text-secondary">{{ $t('simLab.labelSurveyId') }}</label>
        <div class="flex gap-2">
          <ComboboxInput
            v-model="surveyIdInput"
            :options="surveyOptions"
            :placeholder="$t('simLab.placeholderSurveyId')"
            :empty-text="$t('simLab.noMatch')"
            class="flex-1"
            @select="onSurveySelect"
          />
          <button class="text-xs px-3 py-1.5 transition-all btn-accent-filled" @click="$emit('load')">
            {{ $t('simLab.btnLoad') }}
          </button>
        </div>
      </div>

      <div class="space-y-2">
        <label class="text-xs text-secondary">{{ $t('simLab.labelProjectSearch') }}</label>
        <div class="flex gap-2">
          <input
            v-model="searchKeyword"
            type="text"
            :placeholder="$t('simLab.placeholderProjectSearch')"
            class="flex-1 rounded px-3 py-1.5 text-xs card-input-dark"
            @keydown.enter="$emit('search', searchKeyword)"
          />
          <button class="text-xs px-3 py-1.5 transition-all btn-card-outline" @click="$emit('search', searchKeyword)">
            {{ $t('simLab.btnSearch') }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="searchResults.length > 0" class="mt-4 rounded-lg p-3 card-panel-bordered">
      <h4 class="text-xs font-medium mb-2">{{ $t('simLab.searchResults') }}</h4>
      <div class="max-h-40 overflow-auto">
        <div
          v-for="item in searchResults"
          :key="item.id"
          class="flex justify-between items-center p-2 rounded cursor-pointer transition-all mb-1 card-panel"
          @click="$emit('select-survey', item)"
        >
          <div>
            <p class="text-xs text-accent">{{ item.project_name }}</p>
            <p class="text-[10px] text-muted">
              {{ item.country || item.city || item.location || '' }} | {{ item.total_mw }}MW / {{ item.total_mwh }}MWh
            </p>
          </div>
          <span class="text-[10px] px-2 py-1 rounded bg-accent">{{ $t('simLab.btnSelect') }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ComboboxInput from './ComboboxInput.vue'

const props = defineProps({
  surveyList: { type: Array, default: () => [] },
  searchResults: { type: Array, default: () => [] }
})

const emit = defineEmits(['load', 'search', 'select-survey'])

const surveyIdInput = ref('')
const searchKeyword = ref('')

const surveyOptions = computed(() =>
  props.surveyList.map((s) => ({
    label: s.project_name || s.id,
    value: s.id,
    sub: (s.id || '').slice(0, 8) + '...'
  }))
)

function onSurveySelect(opt) {
  const survey = props.surveyList.find((s) => s.id === opt.value)
  if (survey) {
    emit('select-survey', survey)
  }
}
</script>
