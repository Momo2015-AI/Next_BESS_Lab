<template>
  <aside class="sidebar-container">
    <nav class="sidebar-scroll">
      <div class="sidebar-section">
        <router-link to="/" class="sidebar-menu-item" :class="{ active: $route.path === '/' }">
          <AppIcon name="home" class="menu-icon" :size="18" />
          <span>{{ $t('sidebar.home') }}</span>
        </router-link>
      </div>

      <div class="sidebar-section">
        <div class="sidebar-section-label">
          {{ $t('sidebar.sectionPhases') }}
        </div>
        <router-link
          v-for="item in phaseItems"
          :key="item.id"
          :to="item.path"
          class="sidebar-menu-item"
          :class="{ active: $route.path === item.path }"
        >
          <span class="phase-num">{{ String(item.num).padStart(2, '0') }}</span>
          <span>{{ item.label }}</span>
        </router-link>
      </div>

      <div class="sidebar-section">
        <div class="sidebar-section-label">
          {{ $t('sidebar.sectionCoreTools') }}
        </div>
        <router-link
          v-for="item in coreToolItems"
          :key="item.id"
          :to="item.path"
          class="sidebar-menu-item"
          :class="{ active: $route.path === item.path }"
        >
          <AppIcon :name="item.iconName" class="menu-icon" :size="18" />
          <span>{{ item.label }}</span>
        </router-link>
      </div>

      <div class="sidebar-section">
        <div class="sidebar-section-label">
          {{ $t('sidebar.sectionAdvanced') }}
        </div>
        <router-link
          v-for="item in advToolItems"
          :key="item.id"
          :to="item.path"
          class="sidebar-menu-item"
          :class="{ active: $route.path === item.path }"
        >
          <AppIcon :name="item.iconName" class="menu-icon" :size="18" />
          <span>{{ item.label }}</span>
        </router-link>
      </div>

      <div class="sidebar-section">
        <div class="sidebar-section-label">EPC</div>
        <router-link to="/epc" class="sidebar-menu-item" :class="{ active: $route.path === '/epc' }">
          <AppIcon name="dashboard" class="menu-icon" :size="18" />
          <span>EPC</span>
        </router-link>
      </div>
    </nav>

    <div class="sidebar-footer">
      <router-link to="/auth" class="sidebar-menu-item" :class="{ active: $route.path === '/auth' }">
        <AppIcon name="lock" class="menu-icon" :size="18" />
        <span>{{ $t('sidebar.auth') }}</span>
      </router-link>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useBessStore } from '../stores/bess.js'
import AppIcon from './AppIcon.vue'

const { t } = useI18n()
const store = useBessStore()

const phaseItems = computed(() => [
  { id: 'phase1', num: 1, path: '/phase1', label: t('sidebar.phaseSetup'), status: store.phases.phase1.status },
  { id: 'phase2', num: 2, path: '/phase2', label: t('sidebar.phaseDesign'), status: store.phases.phase2.status },
  { id: 'phase3', num: 3, path: '/phase3', label: t('sidebar.phasePerformance'), status: store.phases.phase3.status },
  { id: 'phase4', num: 4, path: '/phase4', label: t('sidebar.phaseFinancial'), status: store.phases.phase4.status },
  { id: 'phase5', num: 5, path: '/phase5', label: t('sidebar.phaseDeliverables'), status: store.phases.phase5.status }
])

const coreToolItems = computed(() => [
  { id: 'formula', path: '/tools/formula', label: t('sidebar.toolFormula'), iconName: 'flask' },
  { id: 'params', path: '/tools/params', label: t('sidebar.toolParams'), iconName: 'sliders' },
  { id: 'conditions', path: '/tools/conditions', label: t('sidebar.toolConditions'), iconName: 'code' },
  { id: 'auxpower', path: '/tools/auxpower', label: t('sidebar.toolAuxPower'), iconName: 'lightning' },
  { id: 'financial', path: '/tools/financial', label: t('sidebar.toolFinance'), iconName: 'dollar' },
  { id: 'engineering', path: '/tools/engineering', label: t('sidebar.toolEngineering'), iconName: 'grid' },
  { id: 'datainject', path: '/tools/datainject', label: t('sidebar.toolDataInject'), iconName: 'upload' }
])

const advToolItems = computed(() => [
  { id: 'config', path: '/tools/config', label: t('sidebar.toolConfig'), iconName: 'settings' },
  { id: 'survey-view', path: '/tools/survey-view', label: t('sidebar.toolSurveyView'), iconName: 'eye' },
  { id: 'simulation-view', path: '/tools/simulation-view', label: t('sidebar.toolSimulation'), iconName: 'bar-chart' },
  { id: 'report', path: '/tools/report', label: t('sidebar.toolReport'), iconName: 'document' },
  { id: 'projects', path: '/tools/projects', label: t('sidebar.toolProjects'), iconName: 'folder' },
  { id: 'templates', path: '/tools/templates', label: t('sidebar.toolTemplates'), iconName: 'save' },
  { id: 'rules', path: '/tools/rules', label: t('sidebar.toolRules'), iconName: 'shield' }
])
</script>

<style scoped>
.sidebar-container {
  width: 260px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  background: var(--bg-sidebar);
  backdrop-filter: var(--backdrop-filter);
  -webkit-backdrop-filter: var(--backdrop-filter);
  border-right: 1px solid var(--border-color);
  overflow: hidden;
  position: relative;
  z-index: 10;
  transition:
    background 0.5s cubic-bezier(0.16, 1, 0.3, 1),
    border-color 0.5s cubic-bezier(0.16, 1, 0.3, 1),
    box-shadow 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

.sidebar-container:hover {
  background: var(--bg-sidebar-hover);
  border-right-color: var(--border-color-hover);
  box-shadow: var(--shadow-sidebar-dynamic);
}

.sidebar-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 32px 12px 12px;
}

.sidebar-section {
  margin-bottom: 4px;
}

.phase-num {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  font-variant-numeric: tabular-nums;
  min-width: 28px;
  text-align: center;
}

.sidebar-footer {
  padding: 8px 12px;
  border-top: 1px solid var(--border-color);
}
</style>
