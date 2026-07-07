<template>
  <div class="epc-panel space-y-4">
    <div class="panel-card">
      <h3 class="panel-title">投标文档生成</h3>
      <div class="flex gap-4 mb-4">
        <select v-model="bidForm.template" class="form-field-select max-w-sm">
          <option value="technical_proposal">技术方案</option>
        </select>
        <button :disabled="loading" class="btn-primary" @click="generateBidDoc">
          {{ loading ? '生成中...' : '生成投标文档' }}
        </button>
      </div>

      <div v-if="bidResult" class="mt-4">
        <div v-for="chapter in bidResult.chapters" :key="chapter.num" class="mb-4">
          <div class="chapter-title">{{ chapter.num }}. {{ chapter.title }}</div>
          <div v-for="sec in chapter.sections" :key="sec.num" class="section-item">
            <div class="font-medium text-sm">{{ sec.num }} {{ sec.title }}</div>
            <div class="text-xs mt-1 whitespace-pre-line tx-muted-dark">{{ sec.content }}</div>
            <div class="text-xs mt-1 tx-muted">数据来源: {{ sec.data_source }}</div>
          </div>
        </div>
      </div>

      <!-- 交互式图表预览 -->
      <div class="mt-6 pt-4 border-top">
        <div class="flex items-center justify-between mb-3">
          <h4 class="text-base font-bold section-title">交互式图表预览</h4>
          <span class="text-xs tx-muted">基于 Plotly，支持缩放/悬停/导出</span>
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
            {{ chartLoading === c.id ? '加载中...' : c.label }}
          </button>
        </div>
        <div v-if="chartError" class="text-xs p-2 rounded mb-3 error-box">{{ chartError }}</div>
        <div v-if="chartReady" ref="chartContainer" class="border rounded-lg p-2 chart-container" />
        <div v-else-if="!chartLoading" class="text-xs text-center py-8 empty-state">
          点击上方按钮选择图表类型，预览投标方案交互式可视化
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useEpcModules } from '../../composables/useEpcModules.js'

const {
  loading, bidForm, bidResult, generateBidDoc,
  chartTypes, chartReady, chartLoading, chartError, activeChart, chartContainer,
  previewChart
} = useEpcModules()
</script>
