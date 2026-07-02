<template>
  <aside class="sidebar-container">
    <div class="sidebar-brand">
      <BrandLogo />
    </div>

    <nav class="sidebar-scroll">
      <div class="sidebar-section">
        <router-link to="/" class="sidebar-menu-item" :class="{ active: $route.path === '/' }">
          <svg viewBox="0 0 24 24">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
            <polyline points="9 22 9 12 15 12 15 22" />
          </svg>
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
          <svg viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" />
            <text x="12" y="16" text-anchor="middle" fill="currentColor" stroke="none" font-size="10" font-weight="700">
              {{ item.num }}
            </text>
          </svg>
          <span>{{ item.label }}</span>
          <span class="phase-badge">{{ String(item.num).padStart(2, '0') }}</span>
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
          <svg viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" />
            <text x="12" y="16" text-anchor="middle" fill="currentColor" stroke="none" font-size="9" font-weight="700">
              {{ item.icon }}
            </text>
          </svg>
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
          <svg viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" />
            <text x="12" y="16" text-anchor="middle" fill="currentColor" stroke="none" font-size="9" font-weight="700">
              {{ item.icon }}
            </text>
          </svg>
          <span>{{ item.label }}</span>
        </router-link>
      </div>

      <div class="sidebar-section">
        <div class="sidebar-section-label">EPC</div>
        <router-link to="/epc" class="sidebar-menu-item" :class="{ active: $route.path === '/epc' }">
          <svg viewBox="0 0 24 24">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
            <polyline points="9 22 9 12 15 12 15 22" />
          </svg>
          <span>EPC</span>
        </router-link>
      </div>
    </nav>

    <div class="sidebar-footer">
      <router-link to="/auth" class="sidebar-menu-item" :class="{ active: $route.path === '/auth' }">
        <svg viewBox="0 0 24 24">
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
import BrandLogo from './BrandLogo.vue'

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

.sidebar-brand {
  padding: 28px 24px 0;
}

.brand-icon-wrap {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, var(--accent-blue), #40a9ff);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.brand-text {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--text-primary);
}

.sidebar-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 32px 12px 12px;
}

.sidebar-section {
  margin-bottom: 4px;
}

.phase-badge {
  margin-left: auto;
  font-size: 10px;
  font-weight: 700;
  background: rgba(142, 142, 147, 0.12);
  padding: 2px 8px;
  border-radius: 6px;
  color: var(--text-secondary);
}

.sidebar-footer {
  padding: 8px 12px;
  border-top: 1px solid var(--border-color);
}
</style>
