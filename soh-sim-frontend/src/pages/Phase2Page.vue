<template>
  <div class="phase-page phase2-page">
    <div class="phase-header">
      <h1>{{ $t('phase2.title') }}</h1>
      <p class="phase-desc">{{ $t('phase2.desc') }}</p>
    </div>
    <div class="phase-body">
      <div class="steps-nav">
        <button v-for="(s, i) in steps" :key="i" :class="{ active: activeStep === i }" @click="activeStep = i">
          {{ s.label }}
        </button>
      </div>
      <div class="step-content">
        <ProductConfig v-if="activeStep === 0" />
        <ProductCAPEXLink v-if="activeStep === 1" />
        <BatteryDCDesign v-if="activeStep === 2" />
        <PcsACDesign v-if="activeStep === 3" />
        <BatteryPCSConfig v-if="activeStep === 4" />
        <EfficiencyChain v-if="activeStep === 5" />
        <EnergyFlowSankey v-if="activeStep === 6" />
        <DegradationConfig v-if="activeStep === 7" />
        <BatteryHealthHeatmap v-if="activeStep === 8" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import ProductConfig from '../components/ProductConfig.vue'
import ProductCAPEXLink from '../components/ProductCAPEXLink.vue'
import BatteryDCDesign from '../components/BatteryDCDesign.vue'
import PcsACDesign from '../components/PcsACDesign.vue'
import BatteryPCSConfig from '../components/BatteryPCSConfig.vue'
import EfficiencyChain from '../components/EfficiencyChain.vue'
import EnergyFlowSankey from '../components/EnergyFlowSankey.vue'
import DegradationConfig from '../components/DegradationConfig.vue'
import BatteryHealthHeatmap from '../components/BatteryHealthHeatmap.vue'

const { t } = useI18n()
const activeStep = ref(0)
const steps = computed(() => [
  { label: t('phase2.step1') },
  { label: t('phase2.step2') },
  { label: t('phase2.step3') },
  { label: t('phase2.step4') },
  { label: t('phase2.step5') },
  { label: t('phase2.step6') },
  { label: t('phase2.step7') },
  { label: t('phase2.step8') },
  { label: t('phase2.step9') }
])
</script>

<style scoped></style>
