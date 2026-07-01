<template>
  <div class="home-root">
    <section class="hero">
      <div class="hero-content">
        <p class="hero-eyebrow">
          {{ $t('home.heroEyebrow') }}
        </p>
        <h1 class="hero-title">
          {{ $t('home.heroTitle') }}
          <span class="hero-accent">.</span>
        </h1>
        <p class="hero-subtitle">
          {{ $t('home.heroSubtitle') }}
        </p>
      </div>
      <div class="hero-metrics">
        <div class="metric-card">
          <div class="metric-label">
            {{ $t('home.currentSoh') }}
          </div>
          <div class="metric-value">
            {{ sohDisplay }}
            <span class="metric-unit">%</span>
          </div>
        </div>
        <div class="metric-card">
          <div class="metric-label">
            {{ $t('home.npv') }}
          </div>
          <div class="metric-value">
            {{ npvDisplay }}
            <span class="metric-unit">{{ $t('home.wan') }}</span>
          </div>
        </div>
        <div class="metric-card">
          <div class="metric-label">
            {{ $t('home.irr') }}
          </div>
          <div class="metric-value">
            {{ irrDisplay }}
            <span class="metric-unit">%</span>
          </div>
        </div>
      </div>
    </section>

    <section class="phases-section">
      <div class="section-header">
        <h2 class="section-title">
          {{ $t('home.sectionPhases') }}
        </h2>
        <p class="section-desc">
          {{ $t('home.sectionPhasesDesc') }}
        </p>
      </div>

      <div class="phases-grid">
        <div v-for="phase in phases" :key="phase.key" class="phase-card" @click="gotoPhase(phase.key)">
          <div class="phase-header-row">
            <span class="phase-num" :class="'num-' + phase.status">{{ phase.num }}</span>
            <span class="phase-badge" :class="'badge-' + phase.status">{{ $t('home.' + phase.statusText) }}</span>
          </div>
          <h3 class="phase-name">
            {{ phase.title }}
          </h3>
          <p class="phase-desc">
            {{ phase.desc }}
          </p>
          <div class="phase-arrow">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </div>
        </div>
      </div>
    </section>

    <section class="tools-section">
      <div class="section-header">
        <h2 class="section-title">
          {{ $t('home.sectionTools') }}
        </h2>
        <p class="section-desc">
          {{ $t('home.sectionToolsDesc') }}
        </p>
      </div>

      <div class="tools-grid">
        <router-link v-for="tool in tools" :key="tool.path" :to="tool.path" class="tool-card">
          <div class="tool-icon-wrap" :style="{ background: tool.gradient }">
            <span class="tool-icon-text">{{ tool.iconText }}</span>
          </div>
          <div class="tool-info">
            <div class="tool-name">
              {{ tool.name }}
            </div>
            <div class="tool-desc">
              {{ tool.desc }}
            </div>
          </div>
        </router-link>
      </div>
    </section>

    <footer class="home-footer">
      <p>SOH-SIM Platform &middot; BESS Design & Evaluation</p>
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useBessStore } from '../stores/bess.js'

const { t } = useI18n()
const router = useRouter()
const store = useBessStore()

const phases = computed(() => {
  const st = store.phases
  return [
    {
      key: 'phase1',
      num: '01',
      title: t('home.phase1Title'),
      desc: t('home.phase1Desc'),
      path: '/phase1',
      status: st.phase1.status,
      statusText: statusKey(st.phase1.status)
    },
    {
      key: 'phase2',
      num: '02',
      title: t('home.phase2Title'),
      desc: t('home.phase2Desc'),
      path: '/phase2',
      status: st.phase2.status,
      statusText: statusKey(st.phase2.status)
    },
    {
      key: 'phase3',
      num: '03',
      title: t('home.phase3Title'),
      desc: t('home.phase3Desc'),
      path: '/phase3',
      status: st.phase3.status,
      statusText: statusKey(st.phase3.status)
    },
    {
      key: 'phase4',
      num: '04',
      title: t('home.phase4Title'),
      desc: t('home.phase4Desc'),
      path: '/phase4',
      status: st.phase4.status,
      statusText: statusKey(st.phase4.status)
    },
    {
      key: 'phase5',
      num: '05',
      title: t('home.phase5Title'),
      desc: t('home.phase5Desc'),
      path: '/phase5',
      status: st.phase5.status,
      statusText: statusKey(st.phase5.status)
    }
  ]
})
function statusKey(s) {
  if (s === 'in_progress') return 'statusInProgress'
  if (s === 'completed') return 'statusComplete'
  return 'statusNotStarted'
}

const tools = computed(() => [
  {
    path: '/tools/formula',
    name: t('sidebar.toolFormula'),
    desc: t('home.toolFormulaDesc'),
    iconText: 'fx',
    gradient: 'linear-gradient(135deg, #0071e3, #40a9ff)'
  },
  {
    path: '/tools/params',
    name: t('sidebar.toolParams'),
    desc: t('home.toolParamsDesc'),
    iconText: 'sl',
    gradient: 'linear-gradient(135deg, #5856d6, #af52de)'
  },
  {
    path: '/tools/conditions',
    name: t('sidebar.toolConditions'),
    desc: t('home.toolConditionsDesc'),
    iconText: 'wd',
    gradient: 'linear-gradient(135deg, #ff9500, #ffac33)'
  },
  {
    path: '/tools/auxpower',
    name: t('sidebar.toolAuxPower'),
    desc: t('home.toolAuxPowerDesc'),
    iconText: 'P',
    gradient: 'linear-gradient(135deg, #ff2d55, #ff6482)'
  },
  {
    path: '/tools/financial',
    name: t('sidebar.toolFinance'),
    desc: t('home.toolFinanceDesc'),
    iconText: '$',
    gradient: 'linear-gradient(135deg, #30d158, #63e68b)'
  },
  {
    path: '/tools/engineering',
    name: t('sidebar.toolEngineering'),
    desc: t('home.toolEngineeringDesc'),
    iconText: 'En',
    gradient: 'linear-gradient(135deg, #5ac8fa, #34aadc)'
  },
  {
    path: '/tools/datainject',
    name: t('sidebar.toolDataInject'),
    desc: t('home.toolDataInjectDesc'),
    iconText: 'Di',
    gradient: 'linear-gradient(135deg, #ff3b30, #ff6259)'
  },
  {
    path: '/tools/simulation-view',
    name: t('sidebar.toolSimulation'),
    desc: t('home.toolSimulationDesc'),
    iconText: 'Sm',
    gradient: 'linear-gradient(135deg, #007aff, #5ac8fa)'
  }
])

function gotoPhase(phase) {
  const p = phases.value.find((x) => x.key === phase)
  if (p) router.push(p.path)
}

const sohDisplay = computed(() => {
  const v = store.degradation.soh?.[0]
  return v != null ? (v * 100).toFixed(1) : '--'
})
const npvDisplay = computed(() => {
  const v = store.financial?.metrics?.npv
  return v != null ? v.toFixed(0) : '--'
})
const irrDisplay = computed(() => {
  const v = store.financial?.metrics?.irr
  return v != null ? (v * 100).toFixed(1) : '--'
})
</script>

<style scoped>
.home-root {
  min-height: 100%;
  background: var(--color-bg);
}

.hero {
  padding: 80px 48px 60px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: -50%;
  left: 50%;
  transform: translateX(-50%);
  width: 120%;
  height: 200%;
  background: radial-gradient(ellipse at center, rgba(0, 113, 227, 0.06) 0%, transparent 70%);
  pointer-events: none;
}

[data-theme='dark'] .hero::before {
  background: radial-gradient(ellipse at center, rgba(0, 113, 227, 0.1) 0%, transparent 70%);
}

.hero-content {
  position: relative;
  z-index: 1;
}

.hero-eyebrow {
  font-size: 14px;
  font-weight: 500;
  color: #0071e3;
  letter-spacing: 0.02em;
  margin: 0 0 12px;
}

.hero-title {
  font-size: 56px;
  font-weight: 700;
  letter-spacing: -0.03em;
  color: #1d1d1f;
  margin: 0 0 16px;
  line-height: 1.05;
}

[data-theme='dark'] .hero-title {
  color: #f5f5f7;
}

.hero-accent {
  color: #0071e3;
}

.hero-subtitle {
  font-size: 19px;
  font-weight: 400;
  color: #86868b;
  line-height: 1.5;
  margin: 0;
  max-width: 520px;
  margin-left: auto;
  margin-right: auto;
  white-space: pre-line;
}

.hero-metrics {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-top: 48px;
  position: relative;
  z-index: 1;
}

.metric-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 20px 32px;
  min-width: 140px;
  border: 0.5px solid rgba(0, 0, 0, 0.06);
}

[data-theme='dark'] .metric-card {
  background: rgba(44, 44, 46, 0.6);
  border-color: rgba(255, 255, 255, 0.06);
}

.metric-label {
  font-size: 12px;
  font-weight: 500;
  color: #86868b;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 6px;
}

.metric-value {
  font-size: 32px;
  font-weight: 700;
  color: #1d1d1f;
  letter-spacing: -0.02em;
}

[data-theme='dark'] .metric-value {
  color: #f5f5f7;
}

.metric-unit {
  font-size: 16px;
  font-weight: 400;
  color: #86868b;
  margin-left: 2px;
}

.phases-section {
  padding: 60px 48px;
}

.section-header {
  text-align: center;
  margin-bottom: 48px;
}

.section-title {
  font-size: 36px;
  font-weight: 700;
  color: #1d1d1f;
  letter-spacing: -0.02em;
  margin: 0 0 8px;
}

[data-theme='dark'] .section-title {
  color: #f5f5f7;
}

.section-desc {
  font-size: 17px;
  color: #86868b;
  margin: 0;
}

.phases-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 1024px) {
  .phases-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
@media (max-width: 640px) {
  .phases-grid {
    grid-template-columns: 1fr;
  }
}

.phase-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 0.5px solid rgba(0, 0, 0, 0.04);
  position: relative;
  overflow: hidden;
}

[data-theme='dark'] .phase-card {
  background: rgba(44, 44, 46, 0.5);
  border-color: rgba(255, 255, 255, 0.04);
}

.phase-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08);
  border-color: rgba(0, 113, 227, 0.2);
}

[data-theme='dark'] .phase-card:hover {
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
  border-color: rgba(0, 113, 227, 0.3);
}

.phase-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.phase-num {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.num-pending {
  color: #d2d2d7;
}
.num-in_progress {
  color: #0071e3;
}
.num-completed {
  color: #30d158;
}

.phase-badge {
  font-size: 11px;
  font-weight: 500;
  padding: 3px 10px;
  border-radius: 12px;
}

.badge-pending {
  background: rgba(0, 0, 0, 0.04);
  color: #86868b;
}
.badge-in_progress {
  background: rgba(0, 113, 227, 0.1);
  color: #0071e3;
}
.badge-completed {
  background: rgba(48, 209, 88, 0.1);
  color: #30d158;
}

[data-theme='dark'] .badge-pending {
  background: rgba(255, 255, 255, 0.06);
  color: #6e6e73;
}
[data-theme='dark'] .badge-in_progress {
  background: rgba(0, 113, 227, 0.15);
  color: #40a9ff;
}
[data-theme='dark'] .badge-completed {
  background: rgba(48, 209, 88, 0.15);
  color: #30d158;
}

.phase-name {
  font-size: 16px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0 0 6px;
}

[data-theme='dark'] .phase-name {
  color: #f5f5f7;
}

.phase-desc {
  font-size: 13px;
  color: #86868b;
  line-height: 1.4;
  margin: 0;
}

.phase-arrow {
  position: absolute;
  bottom: 20px;
  right: 20px;
  color: #d2d2d7;
  transition: all 0.3s;
}

.phase-card:hover .phase-arrow {
  color: #0071e3;
  transform: translateX(3px);
}

.tools-section {
  padding: 0 48px 60px;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 1024px) {
  .tools-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.tool-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(12px);
  border: 0.5px solid rgba(0, 0, 0, 0.04);
  text-decoration: none;
  transition: all 0.2s ease;
  cursor: pointer;
}

[data-theme='dark'] .tool-card {
  background: rgba(44, 44, 46, 0.4);
  border-color: rgba(255, 255, 255, 0.04);
}

.tool-card:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

[data-theme='dark'] .tool-card:hover {
  background: rgba(44, 44, 46, 0.7);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

.tool-icon-wrap {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.tool-icon-text {
  color: white;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.tool-info {
  flex: 1;
  min-width: 0;
}

.tool-name {
  font-size: 14px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 2px;
}

[data-theme='dark'] .tool-name {
  color: #f5f5f7;
}

.tool-desc {
  font-size: 12px;
  color: #86868b;
  line-height: 1.3;
}

.home-footer {
  text-align: center;
  padding: 32px 48px;
  font-size: 12px;
  color: #d2d2d7;
  border-top: 0.5px solid rgba(0, 0, 0, 0.06);
}

[data-theme='dark'] .home-footer {
  border-top-color: rgba(255, 255, 255, 0.06);
  color: #48484a;
}
</style>
