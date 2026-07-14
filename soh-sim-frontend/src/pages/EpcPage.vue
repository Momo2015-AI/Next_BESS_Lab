<template>
  <AppPage :title-key="'epcPage.title'" :desc-key="'epcPage.desc'">
    <!-- 模块标签页 -->
    <div class="epc-tabs">
      <button v-for="tab in tabs" :key="tab.id" :class="{ active: activeModule === tab.id }" @click="switchTab(tab.id)">
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
  </AppPage>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import AppIcon from '../components/AppIcon.vue'
import { useI18n } from 'vue-i18n'
import { useEpcModules } from '../composables/useEpcModules.js'

const { t } = useI18n()

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

const activeModule = ref(sessionStorage.getItem('epcActiveModule') || 'architecture')

// 持久化当前 tab，防止路由切换后重置
function switchTab(tabId) {
  activeModule.value = tabId
  sessionStorage.setItem('epcActiveModule', tabId)
}

const tabs = computed(() => [
  { id: 'architecture', label: t('epcPage.tabArchitecture'), priority: 'P0-3', iconName: 'home' },
  { id: 'gridCompliance', label: t('epcPage.tabGridCompliance'), priority: 'P0-1', iconName: 'target' },
  { id: 'safety', label: t('epcPage.tabSafety'), priority: 'P0-2', iconName: 'shield' },
  { id: 'ipp', label: t('epcPage.tabIpp'), priority: 'P0-4', iconName: 'dollar' },
  { id: 'matrix', label: t('epcPage.tabMatrix'), priority: 'P0-5', iconName: 'grid' },
  { id: 'thermal', label: t('epcPage.tabThermal'), priority: 'P1-1', iconName: 'thermometer' },
  { id: 'scada', label: t('epcPage.tabScada'), priority: 'P1-2', iconName: 'data-flow' },
  { id: 'hv', label: t('epcPage.tabHv'), priority: 'P1-3', iconName: 'lightning' },
  { id: 'bidDoc', label: t('epcPage.tabBidDoc'), priority: 'P1-4', iconName: 'document' }
])

// 壳组件不直接持有状态，仅负责 tab 导航与生命周期钩子；
// 9 个子组件各自通过 useEpcModules() 共享同一份状态（composable 为模块级单例）。
// loadStandards / purgeChart 由共享 composable 承载，这里仅触发生命周期副作用。
const { loadStandards, purgeChart } = useEpcModules((msg) => emit('error', msg), t)

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
