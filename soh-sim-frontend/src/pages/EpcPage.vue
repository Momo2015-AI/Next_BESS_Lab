<template>
  <div class="epc-page">
    <div class="epc-header">
      <h1>EPC 工程化模块</h1>
      <p class="epc-desc">
        系统架构设计、电网合规分析、安全消防、IPP财务、合规矩阵、热管理、SCADA/EMS、高压接入、投标文档
      </p>
    </div>

    <!-- 模块标签页 -->
    <div class="epc-tabs">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        :class="{ active: activeModule === tab.id }"
        @click="activeModule = tab.id"
      >
        <AppIcon :name="tab.iconName" :size="18" class="tab-icon" />
        <span class="tab-label">{{ tab.label }}</span>
        <span class="tab-priority" :class="'pri-' + tab.priority">{{ tab.priority }}</span>
      </button>
    </div>

    <!-- P0-3: 系统架构 -->
    <EpcArchitecture v-show="activeModule === 'architecture'" />
    <!-- P0-1: 电网合规 -->
    <EpcGridCompliance v-show="activeModule === 'gridCompliance'" />
    <!-- P0-2: 安全消防 -->
    <EpcSafety v-show="activeModule === 'safety'" />
    <!-- P0-4: IPP财务 -->
    <EpcIppFinance v-show="activeModule === 'ipp'" />
    <!-- P0-5: 合规矩阵 -->
    <EpcComplianceMatrix v-show="activeModule === 'matrix'" />
    <!-- P1-1: 热管理 -->
    <EpcThermal v-show="activeModule === 'thermal'" />
    <!-- P1-2: SCADA/EMS -->
    <EpcScada v-show="activeModule === 'scada'" />
    <!-- P1-3: 高压接入 -->
    <EpcHvInterconnection v-show="activeModule === 'hv'" />
    <!-- P1-4: 投标文档 -->
    <EpcBidDocument v-show="activeModule === 'bidDoc'" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import AppIcon from '../components/AppIcon.vue'
import { useEpcModules } from '../composables/useEpcModules.js'

import EpcArchitecture from '../components/epc/EpcArchitecture.vue'
import EpcGridCompliance from '../components/epc/EpcGridCompliance.vue'
import EpcSafety from '../components/epc/EpcSafety.vue'
import EpcIppFinance from '../components/epc/EpcIppFinance.vue'
import EpcComplianceMatrix from '../components/epc/EpcComplianceMatrix.vue'
import EpcThermal from '../components/epc/EpcThermal.vue'
import EpcScada from '../components/epc/EpcScada.vue'
import EpcHvInterconnection from '../components/epc/EpcHvInterconnection.vue'
import EpcBidDocument from '../components/epc/EpcBidDocument.vue'

const emit = defineEmits(['error'])

const activeModule = ref('architecture')

const tabs = [
  { id: 'architecture', label: '系统架构', priority: 'P0-3', iconName: 'home' },
  { id: 'gridCompliance', label: '电网合规', priority: 'P0-1', iconName: 'target' },
  { id: 'safety', label: '安全消防', priority: 'P0-2', iconName: 'shield' },
  { id: 'ipp', label: 'IPP财务', priority: 'P0-4', iconName: 'dollar' },
  { id: 'matrix', label: '合规矩阵', priority: 'P0-5', iconName: 'grid' },
  { id: 'thermal', label: '热管理', priority: 'P1-1', iconName: 'thermometer' },
  { id: 'scada', label: 'SCADA/EMS', priority: 'P1-2', iconName: 'data-flow' },
  { id: 'hv', label: '高压接入', priority: 'P1-3', iconName: 'lightning' },
  { id: 'bidDoc', label: '投标文档', priority: 'P1-4', iconName: 'document' }
]

// 壳组件不直接持有状态，仅负责 tab 导航与生命周期钩子；
// 9 个子组件各自通过 useEpcModules() 共享同一份状态（composable 为模块级单例）。
// loadStandards / purgeChart 由共享 composable 承载，这里仅触发生命周期副作用。
const { loadStandards, purgeChart } = useEpcModules((msg) => emit('error', msg))

onMounted(() => {
  loadStandards()
})

onUnmounted(() => {
  purgeChart()
})
</script>

<style scoped>
/* 所有 EPC 共享样式已迁移到 src/assets/styles/shared.css（全局导入） */
</style>
