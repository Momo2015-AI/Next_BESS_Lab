<template>
  <div class="h-full overflow-y-auto custom-scrollbar">
    <div class="max-w-5xl mx-auto space-y-4 py-2">
      <!-- 4.2 成本汇总 -->
      <div v-if="activeStep === 1" class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="phase4-badge">
            02
          </span>
          <div>
            <h3 class="section-title phase4-section-title">
              {{ $t('phase4.costSummary') }}
            </h3>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <h4 class="phase4-subtitle">{{ $t('phase4.capex') }}</h4>
            <div class="space-y-3">
              <div>
                <label class="label-text">{{ $t('phase4.equipment') }}</label>
                <input v-model.number="store.financial.capex.equipment" type="number" class="form-field-input" />
              </div>
              <div>
                <label class="label-text">{{ $t('phase4.epc') }}</label>
                <input v-model.number="store.financial.capex.epc" type="number" class="form-field-input" />
              </div>
              <div>
                <label class="label-text">{{ $t('phase4.development') }}</label>
                <input v-model.number="store.financial.capex.development" type="number" class="form-field-input" />
              </div>
              <div class="phase4-total-row">
                {{ $t('phase4.totalCapex') }}: ${{ totalCapex.toLocaleString() }}
              </div>
            </div>
          </div>
          <div>
            <h4 class="phase4-subtitle">{{ $t('phase4.opex') }}</h4>
            <div class="space-y-3">
              <div>
                <label class="label-text">{{ $t('phase4.fixedOpex') }}</label>
                <input
                  v-model.number="store.financial.opex.fixedOpexPerMw"
                  type="number"
                  step="100"
                  class="form-field-input"
                />
              </div>
              <div>
                <label class="label-text">{{ $t('phase4.variableOpex') }}</label>
                <input
                  v-model.number="store.financial.opex.variableOpexPerMwh"
                  type="number"
                  step="0.1"
                  class="form-field-input"
                />
              </div>
              <div>
                <label class="label-text">{{ $t('phase4.insuranceRate') }}</label>
                <input
                  v-model.number="store.financial.opex.insuranceRate"
                  type="number"
                  step="0.1"
                  class="form-field-input"
                />
              </div>
              <div>
                <label class="label-text">{{ $t('phase4.landLease') }}</label>
                <input
                  v-model.number="store.financial.opex.landLease"
                  type="number"
                  step="1000"
                  class="form-field-input"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 4.3 收入模型与融资 -->
      <div v-if="activeStep === 2" class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="phase4-badge">
            03
          </span>
          <div>
            <h3 class="section-title phase4-section-title">
              {{ $t('phase4.revenueFinancing') }}
            </h3>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <h4 class="phase4-subtitle">{{ $t('phase4.financingParams') }}</h4>
            <div class="space-y-3">
              <div>
                <label class="label-text">{{ $t('phase4.debtRatio') }}</label>
                <input
                  v-model.number="store.financial.financing.debtRatio"
                  type="number"
                  step="1"
                  class="form-field-input"
                />
              </div>
              <div>
                <label class="label-text">{{ $t('phase4.interestRate') }}</label>
                <input
                  v-model.number="store.financial.financing.interestRate"
                  type="number"
                  step="0.1"
                  class="form-field-input"
                />
              </div>
              <div>
                <label class="label-text">{{ $t('phase4.loanTerm') }}</label>
                <input
                  v-model.number="store.financial.financing.loanTerm"
                  type="number"
                  step="1"
                  class="form-field-input"
                />
              </div>
            </div>
          </div>
          <div>
            <h4 class="phase4-subtitle">{{ $t('phase4.taxDepreciation') }}</h4>
            <div class="space-y-3">
              <div>
                <label class="label-text">{{ $t('phase4.corporateTaxRate') }}</label>
                <input
                  v-model.number="store.financial.tax.corporateTaxRate"
                  type="number"
                  step="0.5"
                  class="form-field-input"
                />
              </div>
              <div>
                <label class="label-text">{{ $t('phase4.taxHolidayYears') }}</label>
                <input
                  v-model.number="store.financial.tax.taxHolidayYears"
                  type="number"
                  step="1"
                  class="form-field-input"
                />
              </div>
              <div>
                <label class="label-text">{{ $t('phase4.discountRate') }}</label>
                <input
                  v-model.number="store.financial.discountRate"
                  type="number"
                  step="0.1"
                  class="form-field-input"
                />
              </div>
              <div>
                <label class="label-text">{{ $t('phase4.depreciationYears') }}</label>
                <input
                  v-model.number="store.financial.depreciationYears"
                  type="number"
                  step="1"
                  class="form-field-input"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 其他步骤：BOQ 报价 / 财务指标 / 敏感性分析 -->
      <div v-if="activeStep === 0">
        <BoqEditor />
      </div>
      <div v-if="activeStep === 3">
        <FinancialDashboard />
      </div>
      <div v-if="activeStep === 4">
        <SensitivityAnalysis :params="store.systemParams" :financial="store.financial.metrics" @error="onError" />
      </div>
    </div>

    <!-- 步骤导航 -->
    <div class="phase4-sticky-nav">
      <button
        v-for="(s, i) in steps"
        :key="i"
        class="tab-btn"
        :class="{ active: activeStep === i }"
        @click="activeStep = i"
      >
        {{ s.label }}
      </button>
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
  { label: '4.1 BOQ' },
  { label: '4.2 CAPEX/OPEX' },
  { label: '4.3 收入融资' },
  { label: '4.4 财务指标' },
  { label: '4.5 敏感性' }
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
.phase4-badge {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  background: var(--color-accent-glow);
  color: var(--color-accent);
}
.phase4-section-title {
  color: var(--color-accent);
  border-color: var(--color-accent);
}
.phase4-subtitle {
  font-size: 0.875rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: var(--color-text);
}
.phase4-total-row {
  font-weight: 700;
  padding-top: 0.5rem;
  margin-top: 0.5rem;
  border-top: 1px solid var(--color-border);
  color: var(--color-accent);
}
.phase4-sticky-nav {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 0;
  position: sticky;
  top: 0;
  z-index: 10;
  background: var(--color-bg);
}
</style>
