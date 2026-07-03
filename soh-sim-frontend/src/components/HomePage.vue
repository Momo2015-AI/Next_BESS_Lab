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
        <div class="card metric-card">
          <div class="metric-label">
            {{ $t('home.currentSoh') }}
          </div>
          <div class="metric-value text-[var(--accent-green)]">
            {{ sohDisplay }}
            <span class="metric-unit">%</span>
          </div>
          <div class="soh-bar-wrap">
            <div class="soh-bar-fill" :style="{ width: sohPercent + '%' }" />
          </div>
        </div>
        <div class="card metric-card">
          <div class="metric-label">
            {{ $t('home.npv') }}
          </div>
          <div class="metric-value">
            {{ npvDisplay }}
            <span class="metric-unit">{{ $t('home.wan') }}</span>
          </div>
        </div>
        <div class="card metric-card">
          <div class="metric-label">
            {{ $t('home.irr') }}
          </div>
          <div class="metric-value metric-value-muted">
            {{ irrDisplay }}
            <span class="metric-unit">%</span>
          </div>
        </div>
      </div>
    </section>

    <section class="phases-section">
      <div class="section-header">
        <h2 class="phase-section-title">{{ $t('home.sectionPhases') }}</h2>
        <p class="phase-section-desc">{{ $t('home.sectionPhasesDesc') }}</p>
      </div>

      <div class="phases-grid">
        <div
          v-for="phase in phases"
          :key="phase.key"
          class="step-node theme-step cursor-pointer"
          @click="gotoPhase(phase.key)"
        >
          <div class="step-num" :class="'num-' + phase.status">{{ phase.num }}</div>
          <h3 class="step-name">{{ phase.title }}</h3>
          <p class="step-desc">{{ phase.desc }}</p>
          <div class="step-arrow">
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </div>
        </div>
      </div>
    </section>

    <section class="tools-section">
      <div class="section-header">
        <h2 class="phase-section-title">{{ $t('home.sectionTools') }}</h2>
        <p class="phase-section-desc">{{ $t('home.sectionToolsDesc') }}</p>
      </div>

      <div class="tools-grid">
        <router-link v-for="tool in tools" :key="tool.path" :to="tool.path" class="card card-hover tool-card">
          <div class="tool-icon-wrap" :class="tool.gradientClass">
            <span class="tool-icon-text">{{ tool.iconText }}</span>
          </div>
          <div class="tool-info">
            <div class="tool-name">{{ tool.name }}</div>
            <div class="tool-desc">{{ tool.desc }}</div>
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
      status: st.phase1.status
    },
    {
      key: 'phase2',
      num: '02',
      title: t('home.phase2Title'),
      desc: t('home.phase2Desc'),
      path: '/phase2',
      status: st.phase2.status
    },
    {
      key: 'phase3',
      num: '03',
      title: t('home.phase3Title'),
      desc: t('home.phase3Desc'),
      path: '/phase3',
      status: st.phase3.status
    },
    {
      key: 'phase4',
      num: '04',
      title: t('home.phase4Title'),
      desc: t('home.phase4Desc'),
      path: '/phase4',
      status: st.phase4.status
    },
    {
      key: 'phase5',
      num: '05',
      title: t('home.phase5Title'),
      desc: t('home.phase5Desc'),
      path: '/phase5',
      status: st.phase5.status
    }
  ]
})

const tools = computed(() => [
  {
    path: '/tools/formula',
    name: t('sidebar.toolFormula'),
    desc: t('home.toolFormulaDesc'),
    iconText: 'fx',
    gradientClass: 'tool-gradient-formula'
  },
  {
    path: '/tools/params',
    name: t('sidebar.toolParams'),
    desc: t('home.toolParamsDesc'),
    iconText: 'sl',
    gradientClass: 'tool-gradient-params'
  },
  {
    path: '/tools/conditions',
    name: t('sidebar.toolConditions'),
    desc: t('home.toolConditionsDesc'),
    iconText: 'wd',
    gradientClass: 'tool-gradient-conditions'
  },
  {
    path: '/tools/auxpower',
    name: t('sidebar.toolAuxPower'),
    desc: t('home.toolAuxPowerDesc'),
    iconText: 'P',
    gradientClass: 'tool-gradient-auxpower'
  },
  {
    path: '/tools/financial',
    name: t('sidebar.toolFinance'),
    desc: t('home.toolFinanceDesc'),
    iconText: '$',
    gradientClass: 'tool-gradient-financial'
  },
  {
    path: '/tools/engineering',
    name: t('sidebar.toolEngineering'),
    desc: t('home.toolEngineeringDesc'),
    iconText: 'En',
    gradientClass: 'tool-gradient-engineering'
  },
  {
    path: '/tools/datainject',
    name: t('sidebar.toolDataInject'),
    desc: t('home.toolDataInjectDesc'),
    iconText: 'Di',
    gradientClass: 'tool-gradient-datainject'
  },
  {
    path: '/tools/simulation-view',
    name: t('sidebar.toolSimulation'),
    desc: t('home.toolSimulationDesc'),
    iconText: 'Sm',
    gradientClass: 'tool-gradient-simulation'
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
const sohPercent = computed(() => {
  const v = store.degradation.soh?.[0]
  return v != null ? v * 100 : 0
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
  color: var(--accent-blue);
  letter-spacing: 0.02em;
  margin: 0 0 12px;
}

.hero-title {
  font-size: 56px;
  font-weight: 700;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  margin: 0 0 16px;
  line-height: 1.05;
}

.hero-accent {
  color: var(--accent-blue);
}

.hero-subtitle {
  font-size: 19px;
  font-weight: 400;
  color: var(--text-secondary);
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
  border-radius: 16px;
  padding: 24px 32px;
  min-width: 150px;
  text-align: left;
}

.metric-label {
  font-size: 11px;
  font-weight: 700;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
  opacity: 0.8;
  margin-bottom: 6px;
}

.metric-value {
  font-size: 54px;
  font-weight: 300;
  letter-spacing: -0.04em;
  color: var(--text-primary);
}

.metric-value-muted {
  font-weight: 200;
  color: var(--text-secondary);
}

.metric-unit {
  font-size: 16px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-left: 4px;
}

.soh-bar-wrap {
  height: 4px;
  background: rgba(142, 142, 147, 0.1);
  border-radius: 2px;
  overflow: hidden;
  margin-top: 16px;
}

.soh-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent-blue), var(--accent-green));
  border-radius: 2px;
}

.phases-section {
  padding: 60px 48px;
}

.section-header {
  text-align: center;
  margin-bottom: 48px;
}

.phase-section-title {
  font-size: 36px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  margin: 0 0 8px;
}

.phase-section-desc {
  font-size: 17px;
  color: var(--text-secondary);
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

.step-node {
  padding: 24px;
  border-radius: 20px;
}

.step-num {
  font-size: 12px;
  font-weight: 700;
  color: var(--accent-blue);
  margin-bottom: 8px;
  letter-spacing: 0.5px;
}

.step-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 6px;
}

.step-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.4;
  margin: 0;
}

.step-arrow {
  position: absolute;
  bottom: 20px;
  right: 20px;
  color: var(--text-secondary);
  opacity: 0.4;
}

.step-node:hover .step-arrow {
  opacity: 1;
  color: var(--accent-blue);
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
  text-decoration: none;
  cursor: pointer;
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
  color: var(--text-primary);
  margin-bottom: 2px;
}

.tool-desc {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.3;
}

.home-footer {
  text-align: center;
  padding: 32px 48px;
  font-size: 12px;
  color: var(--text-secondary);
  border-top: 1px solid var(--border-color);
}
</style>
