<template>
  <div class="phase-page phase3-page">
    <div class="phase-header">
      <h1>Phase 3: 性能分析</h1>
      <p class="phase-desc">SOH/RTE 衰减预测、25 年容量对账、可视化分析、多场景对比</p>
      <button class="run-btn" @click="runPipeline" :disabled="store.calculating">
        {{ store.calculating ? '计算中...' : '运行计算管道' }}
      </button>
      <p v-if="store.calculationError" class="error">{{ store.calculationError }}</p>
    </div>
    <div class="phase-body">
      <div class="steps-nav">
        <button v-for="(s, i) in steps" :key="i" @click="activeStep = i" :class="{ active: activeStep === i }">{{ s.label }}</button>
      </div>
      <div class="step-content">
        <SimulationLab v-if="activeStep === 0" />
        <MatrixTable v-if="activeStep === 1" />
        <SohChart v-if="activeStep === 2" />
        <ScenarioCompare v-if="activeStep === 3" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useBessStore } from '../stores/bess.js'
import SimulationLab from '../components/SimulationLab.vue'
import MatrixTable from '../components/MatrixTable.vue'
import SohChart from '../components/SohChart.vue'
import ScenarioCompare from '../components/ScenarioCompare.vue'

const store = useBessStore()
const activeStep = ref(0)
const steps = [
  { label: '3.1 衰减预测' },
  { label: '3.2 容量对账' },
  { label: '3.3 可视化分析' },
  { label: '3.4 多场景对比' },
]

async function runPipeline() {
  await store.runPipeline()
}
</script>

<style scoped>
.phase-page { padding: 24px; }
.phase-header { margin-bottom: 24px; }
.phase-header h1 { font-size: 24px; font-weight: 700; margin: 0 0 8px; }
.phase-desc { color: var(--text-secondary, #666); font-size: 14px; margin: 0 0 12px; }
.run-btn {
  padding: 10px 24px; background: #409eff; color: #fff; border: none;
  border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 600;
}
.run-btn:hover { background: #337ecc; }
.run-btn:disabled { background: #ccc; cursor: not-allowed; }
.error { color: #f56c6c; font-size: 13px; margin: 8px 0 0; }
.steps-nav { display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
.steps-nav button {
  padding: 8px 16px; border: 1px solid var(--border, #ddd); border-radius: 6px;
  background: var(--bg, #fff); cursor: pointer; font-size: 13px; transition: all 0.2s;
}
.steps-nav button.active { background: #409eff; color: #fff; border-color: #409eff; }
.step-content { min-height: 400px; }
</style>
