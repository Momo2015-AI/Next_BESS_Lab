<template>
  <aside class="sidebar-container">
    <nav class="sidebar-scroll">
      <div class="sidebar-section">
        <router-link to="/" class="sidebar-link" :class="{ active: $route.path === '/' }">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
          </svg>
          <span>{{ $t('sidebar.home') }}</span>
        </router-link>
      </div>

      <div class="sidebar-section">
        <div class="section-label">
          {{ $t('sidebar.sectionPhases') }}
        </div>
        <router-link
          v-for="item in phaseItems"
          :key="item.id"
          :to="item.path"
          class="sidebar-link"
          :class="{ active: $route.path === item.path }"
        >
          <span class="phase-dot" :class="'dot-' + item.status">{{ item.num }}</span>
          <span>{{ item.label }}</span>
        </router-link>
      </div>

      <div class="sidebar-section">
        <div class="section-label">
          {{ $t('sidebar.sectionCoreTools') }}
        </div>
        <router-link
          v-for="item in coreToolItems"
          :key="item.id"
          :to="item.path"
          class="sidebar-link"
          :class="{ active: $route.path === item.path }"
        >
          <span class="tool-icon">{{ item.icon }}</span>
          <span>{{ item.label }}</span>
        </router-link>
      </div>

      <div class="sidebar-section">
        <div class="section-label">
          {{ $t('sidebar.sectionAdvanced') }}
        </div>
        <router-link
          v-for="item in advToolItems"
          :key="item.id"
          :to="item.path"
          class="sidebar-link"
          :class="{ active: $route.path === item.path }"
        >
          <span class="tool-icon">{{ item.icon }}</span>
          <span>{{ item.label }}</span>
        </router-link>
      </div>

      <div class="sidebar-section">
        <div class="section-label">EPC</div>
        <router-link to="/epc" class="sidebar-link" :class="{ active: $route.path === '/epc' }">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
            <polyline points="9 22 9 12 15 12 15 22" />
          </svg>
          <span>EPC 工程化</span>
        </router-link>
      </div>
    </nav>

    <div class="sidebar-footer">
      <router-link to="/auth" class="sidebar-link" :class="{ active: $route.path === '/auth' }">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
          <path d="M7 11V7a5 5 0 0 1 10 0v4" />
        </svg>
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
  { id: 'phase5', num: 5, path: '/phase5', label: t('sidebar.phaseDeliverables'), status: store.phases.phase5.status }
])

const coreToolItems = computed(() => [
  { id: 'formula', path: '/tools/formula', label: t('sidebar.toolFormula'), icon: 'fx' },
  { id: 'params', path: '/tools/params', label: t('sidebar.toolParams'), icon: 'sl' },
  { id: 'conditions', path: '/tools/conditions', label: t('sidebar.toolConditions'), icon: 'wd' },
  { id: 'auxpower', path: '/tools/auxpower', label: t('sidebar.toolAuxPower'), icon: 'P' },
  { id: 'financial', path: '/tools/financial', label: t('sidebar.toolFinance'), icon: '$' },
  { id: 'engineering', path: '/tools/engineering', label: t('sidebar.toolEngineering'), icon: 'En' },
  { id: 'datainject', path: '/tools/datainject', label: t('sidebar.toolDataInject'), icon: 'Di' }
])

const advToolItems = computed(() => [
  { id: 'config', path: '/tools/config', label: t('sidebar.toolConfig'), icon: 'Cf' },
  { id: 'survey-view', path: '/tools/survey-view', label: t('sidebar.toolSurveyView'), icon: 'Sv' },
  { id: 'simulation-view', path: '/tools/simulation-view', label: t('sidebar.toolSimulation'), icon: 'Sm' },
  { id: 'report', path: '/tools/report', label: t('sidebar.toolReport'), icon: 'Rp' },
  { id: 'projects', path: '/tools/projects', label: t('sidebar.toolProjects'), icon: 'Pj' },
  { id: 'templates', path: '/tools/templates', label: t('sidebar.toolTemplates'), icon: 'Tp' },
  { id: 'rules', path: '/tools/rules', label: t('sidebar.toolRules'), icon: 'Ru' }
])
</script>

<style scoped>
.sidebar-container {
  width: 220px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  background: var(--bg-sidebar);
  backdrop-filter: var(--backdrop-filter);
  -webkit-backdrop-filter: var(--backdrop-filter);
  border-right: 1px solid var(--border-color, rgba(0, 0, 0, 0.08));
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
  border-right-color: rgba(47, 128, 237, 0.45);
  box-shadow: var(--shadow-sidebar-dynamic);
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
  font-size: 10px;
  font-weight: 700;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 1.5px;
  padding: 0 10px;
  margin-bottom: 6px;
  opacity: 0.8;
}

.sidebar-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 7px 10px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 400;
  color: var(--text-secondary);
  text-decoration: none;
  transition:
    background 0.5s cubic-bezier(0.16, 1, 0.3, 1),
    color 0.5s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
}

.sidebar-link:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
}

.sidebar-link.active {
  background: var(--bg-card, rgba(0, 113, 227, 0.08));
  color: var(--icon-active, var(--accent-blue));
  font-weight: 600;
  border: 1px solid var(--border-color, rgba(0, 0, 0, 0.04));
  box-shadow: var(--shadow-card-glow);
}

.sidebar-link svg {
  flex-shrink: 0;
  opacity: 0.6;
  stroke: var(--icon-color, #929297);
}
.sidebar-link:hover svg {
  stroke: var(--icon-color, #929297);
}
.sidebar-link.active svg {
  opacity: 1;
  stroke: var(--icon-active, var(--accent-blue));
}

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

.dot-pending {
  background: rgba(142, 142, 147, 0.12);
  color: var(--text-secondary);
}
.dot-in_progress {
  background: var(--accent-blue);
  color: white;
}
.dot-completed {
  background: #30d158;
  color: white;
}

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
  background: rgba(142, 142, 147, 0.12);
  color: var(--text-secondary);
}

[data-theme='dark'] .tool-icon {
  background: rgba(255, 255, 255, 0.08);
}

.sidebar-footer {
  padding: 10px;
  border-top: 1px solid var(--border-color, rgba(0, 0, 0, 0.08));
}
</style>
