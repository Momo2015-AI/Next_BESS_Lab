<template>
  <div class="epc-panel space-y-4">
    <div class="panel-card">
	      <h3 class="panel-title">{{ $t('epcBid.title') }}</h3>
	      <div class="flex gap-4 mb-4">
	        <select v-model="bidForm.template" class="form-field-select max-w-sm">
	          <option value="technical_proposal">{{ $t('epcBid.template') }}</option>
	        </select>
	        <button :disabled="loading" class="btn-primary" @click="generateBidDoc">
	          {{ loading ? $t('epcBid.generating') : $t('epcBid.generate') }}
	        </button>
      </div>

      <div v-if="bidResult" class="mt-4">
        <div v-for="chapter in bidResult.chapters" :key="chapter.num" class="mb-4">
          <div class="chapter-title">{{ chapter.num }}. {{ chapter.title }}</div>
          <div v-for="sec in chapter.sections" :key="sec.num" class="section-item">
            <div class="font-medium text-sm">{{ sec.num }} {{ sec.title }}</div>
            <div class="text-xs mt-1 whitespace-pre-line tx-muted-dark">{{ sec.content }}</div>
	            <div class="text-xs mt-1 tx-muted">{{ $t('epcBid.dataSource') }} {{ sec.data_source }}</div>
          </div>
        </div>
      </div>

      <!-- 交互式图表预览 -->
      <div class="mt-6 pt-4 border-top">
        <div class="flex items-center justify-between mb-3">
	          <h4 class="text-base font-bold section-title">{{ $t('epcBid.chartPreview') }}</h4>
	          <span class="text-xs tx-muted">{{ $t('epcBid.chartSubtitle') }}</span>
        </div>
        <div class="flex flex-wrap gap-2 mb-3">
          <button
            v-for="c in chartTypes"
            :key="c.id"
            :disabled="chartLoading === c.id"
            class="chart-btn"
            :class="{ active: activeChart === c.id }"
            @click="previewChart(c.id)"
          >
            {{ chartLoading === c.id ? $t('epc.chartLoading') : $t(c.label) }}
          </button>
        </div>
        <div v-if="chartError" class="text-xs p-2 rounded mb-3 error-box">{{ chartError }}</div>
        <div v-if="chartReady" ref="chartContainer" class="border rounded-lg p-2 chart-container" />
        <div v-else-if="!chartLoading" class="text-xs text-center py-8 empty-state">
	          {{ $t('epcBid.chartPlaceholder') }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useEpcModules } from '../../composables/useEpcModules.js'

const {
  loading,
  bidForm,
  bidResult,
  generateBidDoc,
  chartTypes,
  chartReady,
  chartLoading,
  chartError,
  activeChart,
  chartContainer,
  previewChart
} = useEpcModules()
</script>
