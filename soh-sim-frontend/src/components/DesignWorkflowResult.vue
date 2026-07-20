<template>
  <div v-if="result" class="panel-section">
    <h3 class="section-title">
      <span class="icon">🚀</span>
      {{ $t('design.workflowResult') }}
    </h3>
    <div class="workflow-summary">
      <div class="summary-item">
        <span class="summary-value">{{ result.pipeline_summary?.successful || 0 }}</span>
        <span class="summary-label">{{ $t('design.successfulSolutions') }}</span>
      </div>
      <div class="summary-item">
        <span class="summary-value">{{ result.pipeline_summary?.failed || 0 }}</span>
        <span class="summary-label">{{ $t('design.failedSolutions') }}</span>
      </div>
      <div class="summary-item">
        <span class="summary-value">{{ result.strategy }}</span>
        <span class="summary-label">{{ $t('design.strategy') }}</span>
      </div>
    </div>
    <div v-if="result.recommendation" class="recommendation-detail">
      <h4>{{ $t('design.bestSolution') }}</h4>
      <div class="metrics-grid">
        <div v-for="(val, key) in result.recommendation.financial?.metrics || {}" :key="key" class="metric-item">
          <span class="metric-value">{{ formatMetric(key, val) }}</span>
          <span class="metric-label">{{ key }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { formatCurrency } from '../utils/format.js'

const { t } = useI18n()

defineProps({
  result: { type: Object, default: null }
})

function formatMetric(key, val) {
  if (val == null) return '—'
  const num = Number(val)
  if (isNaN(num)) return '—'
  if (key === 'lcos' || key === 'lcoe') return num.toFixed(4)
  if (key === 'projectIrr' || key === 'equityIrr' || key === 'irr' || key === 'roi') return num.toFixed(2) + '%'
  if (key === 'npv' || key === 'capex') return formatCurrency(val)
  if (key === 'payback') return num.toFixed(1) + ' ' + t('common.yearUnit')
  if (typeof val === 'object') return JSON.stringify(val)
  return num.toFixed(2)
}
</script>
