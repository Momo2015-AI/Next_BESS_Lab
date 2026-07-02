<template>
  <aside class="sidebar-container">
    <nav class="sidebar-scroll">
      <div class="sidebar-section">
        <router-link to="/" class="sidebar-menu-item" :class="{ active: $route.path === '/' }">
          <svg
            class="menu-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
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
          <svg
            class="menu-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <!-- formula: 烧瓶 -->
            <path v-if="item.icon === 'fx'" d="M9 3h6v2a4 4 0 01-4 4v5a3 3 0 01-3-3V7a4 4 0 01-4-4z" />
            <line v-if="item.icon === 'fx'" x1="6" y1="21" x2="18" y2="21" />
            <!-- sliders: 滑块 -->
            <path v-else-if="item.icon === 'sl'" d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 14h6M17 14h6" />
            <!-- conditions: 交叉线 -->
            <path v-else-if="item.icon === 'wd'" d="M3 3l18 18M3 21l18-18" />
            <!-- auxpower: 闪电 -->
            <path v-else-if="item.icon === 'P'" d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
            <!-- financial: 美元 -->
            <path v-else-if="item.icon === '$'" d="M12 1v22M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6" />
            <!-- engineering: 网格 -->
            <path v-else-if="item.icon === 'En'" d="M3 3h18v18H3zM9 3v18M15 3v18M3 9h18M3 15h18" />
            <!-- datainject: 上传 -->
            <path v-else-if="item.icon === 'Di'" d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3" />
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
          <svg
            class="menu-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <!-- config: 齿轮 -->
            <path v-if="item.icon === 'Cf'" d="M12 15a3 3 0 100-6 3 3 0 000 6z" />
            <!-- survey: 眼睛 -->
            <path v-else-if="item.icon === 'Sv'" d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
            <!-- simulation: 柱状图 -->
            <path v-else-if="item.icon === 'Sm'" d="M18 20V10M12 20V4M6 20v-6" />
            <!-- report: 文档 -->
            <path v-else-if="item.icon === 'Rp'" d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
            <!-- projects: 文件夹 -->
            <path v-else-if="item.icon === 'Pj'" d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z" />
            <!-- templates: 模板 -->
            <path v-else-if="item.icon === 'Tp'" d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z" />
            <!-- rules: 盾牌 -->
            <path v-else-if="item.icon === 'Ru'" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
          </svg>
          <span>{{ item.label }}</span>
        </router-link>
      </div>

      <div class="sidebar-section">
        <div class="sidebar-section-label">EPC</div>
        <router-link to="/epc" class="sidebar-menu-item" :class="{ active: $route.path === '/epc' }">
          <svg
            class="menu-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
            <polyline points="9 22 9 12 15 12 15 22" />
          </svg>
          <span>EPC</span>
        </router-link>
      </div>
    </nav>

    <div class="sidebar-footer">
      <router-link to="/auth" class="sidebar-menu-item" :class="{ active: $route.path === '/auth' }">
        <svg
          class="menu-icon"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.5"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
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
