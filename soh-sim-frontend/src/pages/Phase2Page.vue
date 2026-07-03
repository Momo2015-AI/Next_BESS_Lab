<template>
  <div class="phase-page phase2-page">
    <div class="phase-header">
      <h1>Phase 2: 系统设计</h1>
      <p class="phase-desc">技术选型、直流侧设计、交流侧设计、系统集成配置</p>
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
import { ref } from 'vue'
import ProductConfig from '../components/ProductConfig.vue'
import ProductCAPEXLink from '../components/ProductCAPEXLink.vue'
import BatteryDCDesign from '../components/BatteryDCDesign.vue'
import PcsACDesign from '../components/PcsACDesign.vue'
import BatteryPCSConfig from '../components/BatteryPCSConfig.vue'
import EfficiencyChain from '../components/EfficiencyChain.vue'
import EnergyFlowSankey from '../components/EnergyFlowSankey.vue'
import DegradationConfig from '../components/DegradationConfig.vue'
import BatteryHealthHeatmap from '../components/BatteryHealthHeatmap.vue'

const activeStep = ref(0)
const steps = [
  { label: '2.1 设备选型库' },
  { label: '2.2 CAPEX联动' },
  { label: '2.3 直流侧设计' },
  { label: '2.4 交流侧设计' },
  { label: '2.5 系统集成配置' },
  { label: '2.6 效率链配置' },
  { label: '2.7 能量流向图' },
  { label: '2.8 退化模型配置' },
  { label: '2.9 健康热力图' }
]
</script>

<style scoped></style>
