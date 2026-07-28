<template>
  <div class="home-root" :class="{ 'is-guest': !isAuthed }">
    <!-- ===== 未登录：营销落地页 ===== -->
    <template v-if="!isAuthed">
      <section class="lp-hero">
        <div class="lp-hero-bg" />
        <div class="lp-hero-content">
          <span class="lp-hero-badge">{{ $t('home.heroBadge') }}</span>
          <h1 class="lp-hero-headline">
            {{ $t('home.heroHeadline') }}
            <span class="lp-hero-accent">{{ $t('home.heroHeadlineAccent') }}</span>
          </h1>
          <p class="lp-hero-lead">{{ $t('home.heroLeadText') }}</p>
          <div class="lp-hero-actions">
            <router-link to="/auth?mode=register" class="lp-btn-primary">
              {{ $t('home.heroCtaPrimary') }}
            </router-link>
            <router-link to="/auth?mode=login" class="lp-btn-secondary">
              {{ $t('home.heroCtaSecondary') }}
            </router-link>
          </div>
          <p class="lp-hero-note">{{ $t('home.heroNoCreditCard') }}</p>
          <div class="lp-pulse-bar" aria-hidden="true">
            <div class="lp-pulse-fill" />
          </div>
        </div>
      </section>

      <section class="lp-section">
        <div class="lp-section-header">
          <h2 class="lp-section-title">{{ $t('home.featureSectionTitle') }}</h2>
          <p class="lp-section-desc">{{ $t('home.featureSectionDesc') }}</p>
        </div>
        <div class="lp-features-grid">
          <div v-for="feat in features" :key="feat.key" class="lp-feature-card">
            <div class="lp-feature-icon" :class="feat.iconClass">
              <AppIcon :name="feat.icon" :size="22" :stroke-width="1.5" />
            </div>
            <h3 class="lp-feature-title">{{ $t(feat.titleKey) }}</h3>
            <p class="lp-feature-desc">{{ $t(feat.descKey) }}</p>
          </div>
        </div>
      </section>

      <section class="lp-section lp-stats-section">
        <div class="lp-section-header">
          <h2 class="lp-section-title">{{ $t('home.statsSectionTitle') }}</h2>
          <p class="lp-section-desc">{{ $t('home.statsSectionDesc') }}</p>
        </div>
        <div class="lp-stats-row">
          <div class="lp-stat-block">
            <div class="lp-stat-value">{{ $t('home.stat1Value') }}</div>
            <div class="lp-stat-label">{{ $t('home.stat1Label') }}</div>
          </div>
          <div class="lp-stat-divider" />
          <div class="lp-stat-block">
            <div class="lp-stat-value">{{ $t('home.stat2Value') }}</div>
            <div class="lp-stat-label">{{ $t('home.stat2Label') }}</div>
          </div>
          <div class="lp-stat-divider" />
          <div class="lp-stat-block">
            <div class="lp-stat-value">{{ $t('home.stat3Value') }}</div>
            <div class="lp-stat-label">{{ $t('home.stat3Label') }}</div>
          </div>
        </div>
      </section>

      <section class="lp-section">
        <div class="lp-section-header">
          <h2 class="lp-section-title">{{ $t('home.workflowSectionTitle') }}</h2>
          <p class="lp-section-desc">{{ $t('home.workflowSectionDesc') }}</p>
        </div>
        <div class="lp-phases-grid">
          <div v-for="phase in phases" :key="phase.key" class="lp-phase-card">
            <div class="lp-phase-num">{{ phase.num }}</div>
            <h3 class="lp-phase-name">{{ phase.title }}</h3>
            <p class="lp-phase-desc">{{ phase.desc }}</p>
          </div>
        </div>
      </section>

      <section class="lp-section">
        <div class="lp-section-header">
          <h2 class="lp-section-title">{{ $t('home.toolsSectionTitle') }}</h2>
          <p class="lp-section-desc">{{ $t('home.toolsSectionDesc') }}</p>
        </div>
        <div class="lp-tools-grid">
          <div v-for="tool in tools" :key="tool.path" class="lp-tool-card">
            <div class="lp-tool-icon" :class="tool.gradientClass">
              <span class="lp-tool-icon-text">{{ tool.iconText }}</span>
            </div>
            <div class="lp-tool-info">
              <div class="lp-tool-name">{{ tool.name }}</div>
              <div class="lp-tool-desc">{{ tool.desc }}</div>
            </div>
          </div>
        </div>
      </section>

      <section class="lp-cta-section">
        <div class="lp-cta-content">
          <h2 class="lp-cta-title">{{ $t('home.ctaSectionTitle') }}</h2>
          <p class="lp-cta-desc">{{ $t('home.ctaSectionDesc') }}</p>
          <router-link to="/auth?mode=register" class="lp-btn-primary lp-btn-lg">
            {{ $t('home.ctaButton') }}
          </router-link>
        </div>
      </section>

      <footer class="lp-footer">
        <p>{{ $t('home.footerText') }}</p>
      </footer>
    </template>

    <!-- ===== 已登录：原有仪表盘 ===== -->
    <template v-else>
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
              <AppIcon name="energy-flow" size="16" />
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
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useBessStore } from '../stores/bess.js'
import AppIcon from './AppIcon.vue'

const { t } = useI18n()
const router = useRouter()
const store = useBessStore()

const isAuthed = computed(() => !!sessionStorage.getItem('auth_token'))

const features = [
  {
    key: 'config',
    icon: 'grid',
    iconClass: 'lp-icon-blue',
    titleKey: 'home.feature1Title',
    descKey: 'home.feature1Desc'
  },
  {
    key: 'soh',
    icon: 'battery',
    iconClass: 'lp-icon-green',
    titleKey: 'home.feature2Title',
    descKey: 'home.feature2Desc'
  },
  {
    key: 'finance',
    icon: 'dollar',
    iconClass: 'lp-icon-amber',
    titleKey: 'home.feature3Title',
    descKey: 'home.feature3Desc'
  },
  {
    key: 'compliance',
    icon: 'shield',
    iconClass: 'lp-icon-purple',
    titleKey: 'home.feature4Title',
    descKey: 'home.feature4Desc'
  }
]

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
  return v != null ? v.toFixed(1) : '--'
})
const sohPercent = computed(() => {
  const v = store.degradation.soh?.[0]
  return v != null ? v : 0
})
const npvDisplay = computed(() => {
  const v = store.financial?.metrics?.npv
  return v != null ? v.toFixed(0) : '--'
})
const irrDisplay = computed(() => {
  const v = store.financial?.metrics?.projectIrr
  return v != null ? (v * 100).toFixed(1) : '--'
})
</script>

<style scoped>
.home-root {
  min-height: 100%;
}

/* ===== 营销落地页（未登录） ===== */
.home-root.is-guest {
  overflow-x: hidden;
}

.lp-hero {
  position: relative;
  padding: 80px 48px 60px;
  text-align: center;
  overflow: hidden;
}

.lp-hero-bg {
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse 80% 60% at 50% 0%,
    var(--color-accent-glow, rgba(0, 102, 204, 0.12)) 0%,
    transparent 70%
  );
  pointer-events: none;
}

.lp-hero-content {
  position: relative;
  z-index: 1;
  max-width: 720px;
  margin: 0 auto;
}

.lp-hero-badge {
  display: inline-block;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-accent);
  background: var(--color-accent-glow, rgba(0, 102, 204, 0.08));
  border: 1px solid var(--color-accent-glow, rgba(0, 102, 204, 0.15));
  border-radius: 100px;
  padding: 6px 16px;
  margin-bottom: 24px;
}

.lp-hero-headline {
  font-size: 52px;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--color-text, var(--text-primary));
  margin: 0 0 20px;
  line-height: 1.08;
}

.lp-hero-accent {
  color: var(--color-accent);
}

.lp-hero-lead {
  font-size: 18px;
  font-weight: 400;
  color: var(--color-text-secondary, var(--text-secondary));
  line-height: 1.6;
  margin: 0 auto 36px;
  max-width: 560px;
}

.lp-hero-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 12px;
}

.lp-btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 28px;
  border-radius: var(--radius-md, 8px);
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-on-accent, #fff);
  background: var(--color-accent);
  text-decoration: none;
  transition: all 0.25s var(--ease-precision, cubic-bezier(0.16, 1, 0.3, 1));
  box-shadow: 0 4px 14px rgba(0, 102, 204, 0.25);
}

.lp-btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(0, 102, 204, 0.35);
  opacity: 0.95;
}

.lp-btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 28px;
  border-radius: var(--radius-md, 8px);
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text, var(--text-primary));
  background: var(--color-card, rgba(255, 255, 255, 0.7));
  border: 1px solid var(--color-border);
  text-decoration: none;
  transition: all 0.25s var(--ease-precision, cubic-bezier(0.16, 1, 0.3, 1));
  backdrop-filter: var(--backdrop-filter, blur(40px));
}

.lp-btn-secondary:hover {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.lp-btn-lg {
  padding: 14px 36px;
  font-size: 16px;
}

.lp-hero-note {
  font-size: 13px;
  color: var(--color-text-muted, var(--text-secondary));
  margin: 0 0 48px;
}

/* 签名元素：电池脉冲条 */
.lp-pulse-bar {
  position: relative;
  height: 4px;
  width: 100%;
  max-width: 480px;
  margin: 0 auto;
  background: var(--color-border);
  border-radius: 2px;
  overflow: hidden;
}

.lp-pulse-fill {
  position: absolute;
  inset: 0;
  width: 100%;
  background: linear-gradient(90deg, var(--color-accent), var(--color-accent-secondary, #4a7bc4));
  border-radius: 2px;
}

/* ===== Section 通用 ===== */
.lp-section {
  padding: 64px 48px;
  max-width: 1200px;
  margin: 0 auto;
}

.lp-section-header {
  text-align: center;
  margin-bottom: 48px;
}

.lp-section-title {
  font-size: 34px;
  font-weight: 700;
  color: var(--color-text, var(--text-primary));
  letter-spacing: -0.02em;
  margin: 0 0 8px;
}

.lp-section-desc {
  font-size: 16px;
  color: var(--color-text-secondary, var(--text-secondary));
  margin: 0;
}

/* ===== 核心亮点 ===== */
.lp-features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

@media (max-width: 1024px) {
  .lp-features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .lp-features-grid {
    grid-template-columns: 1fr;
  }
}

.lp-feature-card {
  padding: 28px 24px;
  border-radius: var(--radius-lg, 12px);
  background: var(--color-card, rgba(255, 255, 255, 0.7));
  border: 1px solid var(--color-border);
  backdrop-filter: var(--backdrop-filter, blur(40px));
  transition: all 0.3s var(--ease-precision, cubic-bezier(0.16, 1, 0.3, 1));
}

.lp-feature-card:hover {
  border-color: var(--color-accent);
  box-shadow: var(--shadow-card-elevated, 0 15px 35px rgba(0, 0, 0, 0.08));
  transform: translateY(-2px);
}

.lp-feature-icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md, 8px);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  color: #fff;
}

.lp-icon-blue {
  background: linear-gradient(135deg, #0066cc, #3a8bff);
}
.lp-icon-green {
  background: linear-gradient(135deg, #10b981, #34d399);
}
.lp-icon-amber {
  background: linear-gradient(135deg, #f59e0b, #fbbf24);
}
.lp-icon-purple {
  background: linear-gradient(135deg, #8b5cf6, #a78bfa);
}

.lp-feature-title {
  font-size: 17px;
  font-weight: 700;
  color: var(--color-text, var(--text-primary));
  margin: 0 0 8px;
}

.lp-feature-desc {
  font-size: 13px;
  color: var(--color-text-secondary, var(--text-secondary));
  line-height: 1.5;
  margin: 0;
}

/* ===== 数据指标 ===== */
.lp-stats-section {
  text-align: center;
}

.lp-stats-row {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 48px;
}

.lp-stat-value {
  font-size: 56px;
  font-weight: 200;
  letter-spacing: -0.04em;
  color: var(--color-accent);
  line-height: 1;
}

.lp-stat-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary, var(--text-secondary));
  margin-top: 8px;
}

.lp-stat-divider {
  width: 1px;
  height: 60px;
  background: var(--color-border);
}

@media (max-width: 640px) {
  .lp-stats-row {
    flex-direction: column;
    gap: 24px;
  }
  .lp-stat-divider {
    width: 60px;
    height: 1px;
  }
}

/* ===== 五阶段 ===== */
.lp-phases-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}

@media (max-width: 1024px) {
  .lp-phases-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 640px) {
  .lp-phases-grid {
    grid-template-columns: 1fr;
  }
}

.lp-phase-card {
  padding: 24px;
  border-radius: var(--radius-lg, 12px);
  background: var(--color-card, rgba(255, 255, 255, 0.7));
  border: 1px solid var(--color-border);
  backdrop-filter: var(--backdrop-filter, blur(40px));
  transition: all 0.3s var(--ease-precision, cubic-bezier(0.16, 1, 0.3, 1));
}

.lp-phase-card:hover {
  border-color: var(--color-accent);
  transform: translateY(-2px);
}

.lp-phase-num {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-accent);
  letter-spacing: 0.5px;
  margin-bottom: 10px;
}

.lp-phase-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text, var(--text-primary));
  margin: 0 0 6px;
}

.lp-phase-desc {
  font-size: 13px;
  color: var(--color-text-secondary, var(--text-secondary));
  line-height: 1.4;
  margin: 0;
}

/* ===== 工具矩阵 ===== */
.lp-tools-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}

@media (max-width: 1024px) {
  .lp-tools-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.lp-tool-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  border-radius: var(--radius-md, 8px);
  background: var(--color-card, rgba(255, 255, 255, 0.7));
  border: 1px solid var(--color-border);
  backdrop-filter: var(--backdrop-filter, blur(40px));
  transition: all 0.25s var(--ease-precision, cubic-bezier(0.16, 1, 0.3, 1));
}

.lp-tool-card:hover {
  border-color: var(--color-accent);
  transform: translateY(-1px);
}

.lp-tool-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.lp-tool-icon-text {
  color: white;
  font-size: 13px;
  font-weight: 700;
}

.lp-tool-info {
  flex: 1;
  min-width: 0;
}

.lp-tool-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text, var(--text-primary));
  margin-bottom: 2px;
}

.lp-tool-desc {
  font-size: 12px;
  color: var(--color-text-secondary, var(--text-secondary));
  line-height: 1.3;
}

/* ===== 底部 CTA ===== */
.lp-cta-section {
  padding: 80px 48px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.lp-cta-section::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse 60% 80% at 50% 50%,
    var(--color-accent-glow, rgba(0, 102, 204, 0.08)) 0%,
    transparent 70%
  );
  pointer-events: none;
}

.lp-cta-content {
  position: relative;
  z-index: 1;
  max-width: 560px;
  margin: 0 auto;
}

.lp-cta-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--color-text, var(--text-primary));
  letter-spacing: -0.02em;
  margin: 0 0 12px;
}

.lp-cta-desc {
  font-size: 16px;
  color: var(--color-text-secondary, var(--text-secondary));
  margin: 0 0 32px;
  line-height: 1.5;
}

.lp-footer {
  text-align: center;
  padding: 32px 48px;
  font-size: 13px;
  color: var(--color-text-muted, var(--text-secondary));
  border-top: 1px solid var(--color-border);
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
