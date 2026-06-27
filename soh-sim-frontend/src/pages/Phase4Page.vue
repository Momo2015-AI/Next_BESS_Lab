<template>
  <div class="phase-page phase4-page">
    <div class="phase-header">
      <h1>Phase 4: 经济评估</h1>
      <p class="phase-desc">CAPEX 估算、OPEX/收入模型、财务指标、敏感性分析</p>
    </div>
    <div class="phase-body">
      <div class="steps-nav">
        <button v-for="(s, i) in steps" :key="i" @click="activeStep = i" :class="{ active: activeStep === i }">{{ s.label }}</button>
      </div>
      <div class="step-content">
        <div v-if="activeStep === 0" class="form-card">
          <h3>投资估算 (CAPEX)</h3>
          <label>设备采购成本 (万元) <input v-model.number="store.financial.capex.equipment" type="number" /></label>
          <label>EPC 费用 (万元) <input v-model.number="store.financial.capex.epc" type="number" /></label>
          <label>前期开发费 (万元) <input v-model.number="store.financial.capex.development" type="number" /></label>
        </div>
        <div v-if="activeStep === 1" class="form-card">
          <h3>运营模型 (OPEX)</h3>
          <label>年运维成本 (万元) <input v-model.number="store.financial.opex.maintenance" type="number" /></label>
          <label>年保险费用 (万元) <input v-model.number="store.financial.opex.insurance" type="number" /></label>
          <label>年电网费用 (万元) <input v-model.number="store.financial.opex.grid" type="number" /></label>
        </div>
        <div v-if="activeStep === 2" class="form-card">
          <h3>收入模型</h3>
          <label>峰谷套利电价 (元/kWh) <input v-model.number="store.financial.revenue.arbitragePrice" type="number" step="0.01" /></label>
        </div>
        <div v-if="activeStep === 3" class="metrics-card">
          <h3>财务指标</h3>
          <table>
            <tr><td>NPV (万元)</td><td :class="metricClass(store.financial.metrics.npv, 0)">{{ store.financial.metrics.npv }}</td></tr>
            <tr><td>IRR (%)</td><td :class="metricClass(store.financial.metrics.irr, 8)">{{ store.financial.metrics.irr }}</td></tr>
            <tr><td>LCOS</td><td>{{ store.financial.metrics.lcos }}</td></tr>
            <tr><td>ROI (%)</td><td>{{ store.financial.metrics.roi }}</td></tr>
            <tr><td>DSCR</td><td :class="metricClass(store.financial.metrics.dscr, 1.2)">{{ store.financial.metrics.dscr }}</td></tr>
            <tr><td>投资回收期 (年)</td><td>{{ store.financial.metrics.payback > 0 ? store.financial.metrics.payback : '未回收' }}</td></tr>
          </table>
        </div>
        <SensitivityAnalysis v-if="activeStep === 4" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useBessStore } from '../stores/bess.js'
import SensitivityAnalysis from '../components/SensitivityAnalysis.vue'

const store = useBessStore()
const activeStep = ref(0)
const steps = [
  { label: '4.1 投资估算' },
  { label: '4.2 运营模型' },
  { label: '4.3 收入模型' },
  { label: '4.4 财务指标' },
  { label: '4.5 敏感性分析' },
]

function metricClass(value, threshold) {
  if (value >= threshold) return 'status-good'
  return 'status-bad'
}
</script>

<style scoped>
.phase-page { padding: 24px; }
.phase-header { margin-bottom: 24px; }
.phase-header h1 { font-size: 24px; font-weight: 700; margin: 0 0 8px; }
.phase-desc { color: var(--text-secondary, #666); font-size: 14px; margin: 0; }
.steps-nav { display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
.steps-nav button {
  padding: 8px 16px; border: 1px solid var(--border, #ddd); border-radius: 6px;
  background: var(--bg, #fff); cursor: pointer; font-size: 13px; transition: all 0.2s;
}
.steps-nav button.active { background: #409eff; color: #fff; border-color: #409eff; }
.step-content { min-height: 400px; }
.form-card { background: var(--bg-card, #fff); padding: 20px; border-radius: 8px; border: 1px solid var(--border, #eee); }
.form-card h3 { margin: 0 0 16px; font-size: 18px; }
.form-card label { display: block; margin-bottom: 12px; font-size: 14px; }
.form-card input { margin-left: 8px; padding: 6px 10px; border: 1px solid var(--border, #ddd); border-radius: 4px; width: 160px; }
.metrics-card { background: var(--bg-card, #fff); padding: 20px; border-radius: 8px; border: 1px solid var(--border, #eee); }
.metrics-card h3 { margin: 0 0 16px; font-size: 18px; }
.metrics-card table { width: 100%; border-collapse: collapse; }
.metrics-card td { padding: 8px 12px; border-bottom: 1px solid var(--border, #eee); font-size: 14px; }
.status-good { color: #67c23a; font-weight: 600; }
.status-bad { color: #f56c6c; font-weight: 600; }
</style>
