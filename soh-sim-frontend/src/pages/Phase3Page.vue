<template>
  <div class="phase-page phase3-page">
    <div class="phase-header">
      <h1>{{ $t('phase3.title') }}</h1>
      <p class="phase-desc">{{ $t('phase3.desc') }}</p>
      <button class="run-btn" :disabled="store.calculating" @click="runPipeline">
        {{ store.calculating ? $t('phase3.calculating') : $t('phase3.runPipeline') }}
      </button>
      <p v-if="store.calculationError" class="error">
        {{ store.calculationError }}
      </p>
    </div>
    <div class="phase-body">
      <div class="steps-nav">
        <button v-for="(s, i) in steps" :key="i" :class="{ active: activeStep === i }" @click="activeStep = i">
          {{ s.label }}
        </button>
      </div>
      <div class="step-content">
        <SimulationLab v-if="activeStep === 0" @apply-config="onApplySimulationConfig" @error="onError" />
        <MatrixTable
          v-if="activeStep === 1"
          :params="store.systemParams"
          :results="store.results"
          :soh="store.degradation.soh"
          :rte="store.degradation.rte"
          :dod="store.degradation.dod"
          :aug-qty="store.degradation.augQty"
          @update:param="(key, val) => (store.systemParams[key] = val)"
          @update:soh="store.degradation.soh = $event"
          @update:rte="store.degradation.rte = $event"
          @update:dod="store.degradation.dod = $event"
          @update:aug-qty="store.degradation.augQty = $event"
          @recalculate="runPipeline"
        />
        <SohChart
          v-if="activeStep === 2"
          :results="store.results"
          :soh="store.degradation.soh"
          :rte="store.degradation.rte"
          :required-energy="store.systemParams.requiredEnergy"
        />
        <ScenarioCompare v-if="activeStep === 3" :base-params="store.systemParams" @error="onError" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useBessStore } from '../stores/bess.js'
import SimulationLab from '../components/SimulationLab.vue'
import MatrixTable from '../components/MatrixTable.vue'
import SohChart from '../components/SohChart.vue'
import ScenarioCompare from '../components/ScenarioCompare.vue'

const store = useBessStore()
const { t } = useI18n()
const activeStep = ref(0)
const steps = computed(() => [
  { label: t('phase3.step1') },
  { label: t('phase3.step2') },
  { label: t('phase3.step3') },
  { label: t('phase3.step4') }
])

async function runPipeline() {
  await store.runPipeline()
}

function onError(msg) {
  store.calculationError = msg
}

function onApplySimulationConfig(payload) {
  Object.keys(payload).forEach((key) => {
    if (payload[key] != null && store.systemParams[key] !== undefined) {
      store.systemParams[key] = payload[key]
    }
  })
  const sohData = payload.sohCurve || payload.soh
  const rteData = payload.rteCurve || payload.rte
  if (sohData && Array.isArray(sohData)) {
    store.degradation.soh = sohData
  }
  if (rteData && Array.isArray(rteData)) {
    store.degradation.rte = rteData
  }
}
</script>

<style scoped>
.run-btn {
  padding: 10px 24px;
  background: var(--color-accent);
  color: var(--color-text-on-accent);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: opacity 0.2s ease;
}
.run-btn:hover {
  opacity: 0.88;
}
.run-btn:disabled {
  background: var(--color-text-muted);
  opacity: 0.5;
  cursor: not-allowed;
}
.error {
  color: var(--color-danger);
  font-size: 13px;
  margin: 8px 0 0;
}
</style>
