<template>
  <aside class="sidebar-container">
    <nav class="sidebar-scroll">
      <div class="sidebar-section">
        <router-link to="/" class="sidebar-link" :class="{ active: $route.path === '/' }">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>
          <span>{{ $t('sidebar.home') }}</span>
        </router-link>
      </div>

      <div class="sidebar-section">
        <div class="section-label">{{ $t('sidebar.sectionPhases') }}</div>
        <router-link
          v-for="item in phaseItems" :key="item.id"
          :to="item.path"
          class="sidebar-link"
          :class="{ active: $route.path === item.path }">
          <span class="phase-dot" :class="'dot-' + item.status">{{ item.num }}</span>
          <span>{{ item.label }}</span>
        </router-link>
      </div>

      <div class="sidebar-section">
        <div class="section-label">{{ $t('sidebar.sectionCoreTools') }}</div>
        <router-link
          v-for="item in coreToolItems" :key="item.id"
          :to="item.path"
          class="sidebar-link"
          :class="{ active: $route.path === item.path }">
          <span class="tool-icon">{{ item.icon }}</span>
          <span>{{ item.label }}</span>
        </router-link>
      </div>

      <div class="sidebar-section">
        <div class="section-label">{{ $t('sidebar.sectionAdvanced') }}</div>
        <router-link
          v-for="item in advToolItems" :key="item.id"
          :to="item.path"
          class="sidebar-link"
          :class="{ active: $route.path === item.path }">
          <span class="tool-icon">{{ item.icon }}</span>
          <span>{{ item.label }}</span>
        </router-link>
      </div>
    </nav>

    <div class="sidebar-footer">
      <router-link to="/auth" class="sidebar-link" :class="{ active: $route.path === '/auth' }">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
        <span>{{ $t('sidebar.auth') }}</span>
      </router-link>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useBessStore } from '../stores/bess.js'

const { t } = useI18n()
const store = useBessStore()

const phaseItems = computed(() => [
  { id: 'phase1', num: 1, path: '/phase1', label: t('sidebar.phaseSetup'), status: store.phases.phase1.status },
  { id: 'phase2', num: 2, path: '/phase2', label: t('sidebar.phaseDesign'), status: store.phases.phase2.status },
  { id: 'phase3', num: 3, path: '/phase3', label: t('sidebar.phasePerformance'), status: store.phases.phase3.status },
  { id: 'phase4', num: 4, path: '/phase4', label: t('sidebar.phaseFinancial'), status: store.phases.phase4.status },
  { id: 'phase5', num: 5, path: '/phase5', label: t('sidebar.phaseDeliverables'), status: store.phases.phase5.status },
])

const coreToolItems = [
  { id: 'formula', path: '/tools/formula', label: t('sidebar.toolFormula'), icon: 'fx' },
  { id: 'params', path: '/tools/params', label: t('sidebar.toolParams'), icon: 'sl' },
  { id: 'conditions', path: '/tools/conditions', label: t('sidebar.toolConditions'), icon: 'wd' },
  { id: 'auxpower', path: '/tools/auxpower', label: t('sidebar.toolAuxPower'), icon: 'P' },
  { id: 'financial', path: '/tools/financial', label: t('sidebar.toolFinance'), icon: '$' },
  { id: 'engineering', path: '/tools/engineering', label: t('sidebar.toolEngineering'), icon: 'En' },
  { id: 'datainject', path: '/tools/datainject', label: t('sidebar.toolDataInject'), icon: 'Di' },
]

const advToolItems = [
  { id: 'config', path: '/tools/config', label: t('sidebar.toolConfig'), icon: 'Cf' },
  { id: 'survey-view', path: '/tools/survey-view', label: t('sidebar.toolSurveyView'), icon: 'Sv' },
  { id: 'simulation-view', path: '/tools/simulation-view', label: t('sidebar.toolSimulation'), icon: 'Sm' },
  { id: 'report', path: '/tools/report', label: t('sidebar.toolReport'), icon: 'Rp' },
  { id: 'projects', path: '/tools/projects', label: t('sidebar.toolProjects'), icon: 'Pj' },
  { id: 'templates', path: '/tools/templates', label: t('sidebar.toolTemplates'), icon: 'Tp' },
  { id: 'rules', path: '/tools/rules', label: t('sidebar.toolRules'), icon: 'Ru' },
]
</script>

<style scoped>
.sidebar-container {
  width: 220px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  background: rgba(255,255,255,0.6);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-right: 0.5px solid rgba(0,0,0,0.08);
  overflow: hidden;
}

[data-theme="dark"] .sidebar-container {
  background: rgba(29,29,31,0.6);
  border-right-color: rgba(255,255,255,0.06);
}

.sidebar-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 12px 10px;
}

.sidebar-section {
  margin-bottom: 16px;
}

.section-label {
  font-size: 11px;
  font-weight: 600;
  color: #86868b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0 10px;
  margin-bottom: 4px;
}

[data-theme="dark"] .section-label { color: #6e6e73; }

.sidebar-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 7px 10px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 400;
  color: #424245;
  text-decoration: none;
  transition: all 0.15s ease;
  cursor: pointer;
}

.sidebar-link:hover {
  background: rgba(0,0,0,0.04);
  color: #1d1d1f;
}

.sidebar-link.active {
  background: rgba(0,113,227,0.08);
  color: #0071e3;
  font-weight: 500;
}

[data-theme="dark"] .sidebar-link { color: #a1a1a6; }
[data-theme="dark"] .sidebar-link:hover { background: rgba(255,255,255,0.06); color: #f5f5f7; }
[data-theme="dark"] .sidebar-link.active { background: rgba(0,113,227,0.15); color: #40a9ff; }

.sidebar-link svg { flex-shrink: 0; opacity: 0.6; }
.sidebar-link.active svg { opacity: 1; }

.phase-dot {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 600;
  flex-shrink: 0;
}

.dot-pending { background: #f0f0f0; color: #999; }
.dot-in_progress { background: #0071e3; color: white; }
.dot-completed { background: #30d158; color: white; }

.tool-icon {
  width: 22px;
  height: 22px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 9px;
  font-weight: 700;
  flex-shrink: 0;
  background: rgba(0,0,0,0.04);
  color: #86868b;
}

[data-theme="dark"] .tool-icon { background: rgba(255,255,255,0.08); color: #6e6e73; }

.sidebar-footer {
  padding: 10px;
  border-top: 0.5px solid rgba(0,0,0,0.08);
}

[data-theme="dark"] .sidebar-footer { border-top-color: rgba(255,255,255,0.06); }
</style>
