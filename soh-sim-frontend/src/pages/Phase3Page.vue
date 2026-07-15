<template>
  <AppPage title-key="phase3.title" desc-key="phase3.desc">
    <template #actions>
      <button class="run-btn" :disabled="store.calculating" @click="runPipeline">
        {{ store.calculating ? $t('phase3.calculating') : $t('phase3.runPipeline') }}
      </button>
      <p v-if="store.calculationError" class="error">
        {{ store.calculationError }}
      </p>
    </template>
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
  </AppPage>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useBessStore } from '../stores/bess.js'
import AppPage from '../components/AppPage.vue'
import SimulationLab from '../components/SimulationLab.vue'
import MatrixTable from '../components/MatrixTable.vue'
import SohChart from '../components/SohChart.vue'
import ScenarioCompare from '../components/ScenarioCompare.vue'

const store = useBessStore()
const { t } = useI18n()
const activeStep = ref(store.phase3ActiveStep || 0)
watch(activeStep, (v) => {
  store.phase3ActiveStep = v
})
const steps = computed(() => [
  { label: t('phase3.step1') },
  { label: t('phase3.step2') },
  { label: t('phase3.step3') },
  { label: t('phase3.step4') }
])

async function runPipeline() {
  const designOutput = {
    container: { ratedEnergyMWh: store.systemParams.ratedEnergy },
    pcs: { ratedPowerMW: store.systemParams.pcsPower },
    containerQty: store.systemParams.initContainerQty,
    pcsQty: store.systemParams.initPcsQty,
    duration: store.systemParams.duration
  }
  const surveyParams = {
    ratedEnergy: store.survey.ratedEnergy,
    temperature: store.survey.temperature,
    cyclesPerDay: store.survey.cyclesPerDay,
    dod: store.survey.dod || 90,
    cRate: store.survey.cRate || 0.5,
    duration: store.survey.duration || store.systemParams.duration,
    requiredEnergy: store.survey.requiredEnergy
  }
  try {
    await store.runSimulationEngine(designOutput, surveyParams)
  } catch (e) {
    store.calculationError = e.message
  }
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
    // SimulationLab 传出百分比(0-100)，统一转为 0-1 小数存储
    store.degradation.soh = sohData[0] <= 1 ? sohData : sohData.map((v) => v / 100)
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
