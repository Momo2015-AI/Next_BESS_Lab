<template>
  <div class="phase-page phase4-page">
    <div class="phase-header">
      <h1>Phase 4: 经济评估</h1>
      <p class="phase-desc">BOQ 报价、成本汇总、收入模型、财务指标、敏感性分析</p>
    </div>
    <div class="phase-body">
      <div class="steps-nav">
        <button v-for="(s, i) in steps" :key="i" :class="{ active: activeStep === i }" @click="activeStep = i">
          {{ s.label }}
        </button>
      </div>
      <div class="step-content">
        <div v-if="activeStep === 0" class="step-panel">
          <BoqEditor />
        </div>
        <div v-if="activeStep === 1" class="form-card">
          <h3>成本汇总 (CAPEX + OPEX)</h3>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <h4 class="text-sm font-bold mb-2 section-title">CAPEX</h4>
              <label>
                设备采购 (USD)
                <input v-model.number="store.financial.capex.equipment" type="number" />
              </label>
              <label>
                EPC 费用 (USD)
                <input v-model.number="store.financial.capex.epc" type="number" />
              </label>
              <label>
                前期开发 (USD)
                <input v-model.number="store.financial.capex.development" type="number" />
              </label>
              <div class="total-capex">总 CAPEX: ${{ totalCapex.toLocaleString() }}</div>
            </div>
            <div>
              <h4 class="text-sm font-bold mb-2 section-title">OPEX</h4>
              <label>
                固定 O&M ($/MW-yr)
                <input v-model.number="store.financial.opex.fixedOpexPerMw" type="number" step="100" />
              </label>
              <label>
                可变 O&M ($/MWh)
                <input v-model.number="store.financial.opex.variableOpexPerMwh" type="number" step="0.1" />
              </label>
              <label>
                保险率 (% CAPEX)
                <input v-model.number="store.financial.opex.insuranceRate" type="number" step="0.1" />
              </label>
              <label>
                土地租赁 ($/yr)
                <input v-model.number="store.financial.opex.landLease" type="number" step="1000" />
              </label>
            </div>
          </div>
        </div>
        <div v-if="activeStep === 2" class="form-card">
          <h3>收入模型与融资</h3>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <h4 class="text-sm font-bold mb-2 section-title">融资参数</h4>
              <label>
                贷款比例 (%)
                <input v-model.number="store.financial.financing.debtRatio" type="number" step="1" />
              </label>
              <label>
                贷款利率 (%)
                <input v-model.number="store.financial.financing.interestRate" type="number" step="0.1" />
              </label>
              <label>
                贷款期限 (年)
                <input v-model.number="store.financial.financing.loanTerm" type="number" step="1" />
              </label>
            </div>
            <div>
              <h4 class="text-sm font-bold mb-2 section-title">税收与折旧</h4>
              <label>
                所得税率 (%)
                <input v-model.number="store.financial.tax.corporateTaxRate" type="number" step="0.5" />
              </label>
              <label>
                免税期 (年)
                <input v-model.number="store.financial.tax.taxHolidayYears" type="number" step="1" />
              </label>
              <label>
                折现率 (%)
                <input v-model.number="store.financial.discountRate" type="number" step="0.1" />
              </label>
              <label>
                折旧年限
                <input v-model.number="store.financial.depreciationYears" type="number" step="1" />
              </label>
            </div>
          </div>
        </div>
        <div v-if="activeStep === 3" class="step-panel">
          <FinancialDashboard />
        </div>
        <SensitivityAnalysis
          v-if="activeStep === 4"
          :params="store.systemParams"
          :financial="store.financial.metrics"
          @error="onError"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useBessStore } from '../stores/bess.js'
import SensitivityAnalysis from '../components/SensitivityAnalysis.vue'
import BoqEditor from '../components/BoqEditor.vue'
import FinancialDashboard from '../components/FinancialDashboard.vue'

const store = useBessStore()
const activeStep = ref(0)
const steps = [
  { label: '4.1 BOQ 报价' },
  { label: '4.2 成本汇总' },
  { label: '4.3 收入与融资' },
  { label: '4.4 财务指标' },
  { label: '4.5 敏感性分析' }
]

const totalCapex = computed(() => {
  const c = store.financial.capex
  return (c.equipment || 0) + (c.epc || 0) + (c.development || 0)
})

function onError(msg) {
  store.calculationError = msg
}
</script>

<style scoped>
.form-card {
  background: var(--section-card-bg);
  padding: 24px 28px;
  border-radius: var(--section-card-radius);
  border: 1px solid var(--section-card-border);
  box-shadow: var(--section-card-shadow);
}

.form-card h3 {
  margin: 0 0 16px;
  font-size: var(--section-title-size);
  font-weight: var(--section-title-weight);
  color: var(--section-title-color);
  letter-spacing: -0.01em;
}

.form-card h4 {
  color: var(--section-title-color);
}

.form-card label {
  display: block;
  margin-bottom: 12px;
  font-size: 13px;
  color: var(--form-label-color);
}

.form-card input {
  margin-left: 10px;
  padding: 6px 12px;
  height: var(--form-field-height);
  background-color: var(--form-field-bg);
  border: 1px solid var(--form-field-border);
  border-radius: var(--form-field-radius);
  color: var(--form-field-text);
  font-size: 13px;
  font-weight: 500;
  width: 180px;
  outline: none;
  transition: all 0.18s ease;
}

.form-card input:hover {
  background-color: var(--form-field-bg-hover);
}

.form-card input:focus-visible {
  border-color: var(--form-field-border-focus);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.total-capex {
  color: var(--color-accent) !important;
  font-size: 15px;
  font-weight: 700;
  margin: 8px 0 0;
  padding-top: 8px;
  border-top: 1px solid var(--color-border);
}
</style>
