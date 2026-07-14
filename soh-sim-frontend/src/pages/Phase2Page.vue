<template>
  <AppPage title-key="phase2.title" desc-key="phase2.desc">
    <div class="steps-nav">
      <button
        v-for="(s, i) in steps"
        :key="i"
        :class="{ active: activeStep === i, done: i < activeStep }"
        @click="activeStep = i"
      >
        <span class="step-num">{{ i + 1 }}</span>
        {{ s.label }}
      </button>
    </div>

    <div class="step-content">
      <!-- 步骤1: 方案模板选择 -->
      <DesignTemplateSelector v-if="activeStep === 0" @confirm="onTemplateConfirm" @skip="activeStep = 1" />

      <!-- 步骤2: 设计参数确认 -->
      <DesignParamsConfirm v-if="activeStep === 1" @back="activeStep = 0" @result="onDesignResult" />

      <!-- 步骤3: 方案结果预览 -->
      <DesignResultPreview
        v-if="activeStep === 2"
        :solutions="designSolutions"
        :strategy="designStrategy"
        @back="activeStep = 1"
        @confirm="onSolutionConfirm"
      />
    </div>
  </AppPage>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useBessStore } from '../stores/bess.js'
import AppPage from '../components/AppPage.vue'
import DesignTemplateSelector from '../components/DesignTemplateSelector.vue'
import DesignParamsConfirm from '../components/DesignParamsConfirm.vue'
import DesignResultPreview from '../components/DesignResultPreview.vue'

const { t } = useI18n()
const router = useRouter()
const store = useBessStore()

const activeStep = ref(0)

const steps = computed(() => [{ label: t('phase2.step1') }, { label: t('phase2.step2') }, { label: t('phase2.step3') }])

// 设计结果 — 优先从 store 恢复（解决返回时数据丢失）
const designSolutions = ref(store.designResults.solutions || [])
const designStrategy = ref(store.designResults.strategy || 'balanced')

// 如果 store 中有已确认的方案且 solutions 非空，直接跳到步骤 3
if (store.designResults.confirmedSolution && store.designResults.solutions.length > 0) {
  activeStep.value = 2
}

function onTemplateConfirm(tmpl) {
  // 模板已确认，直接跳到参数确认
  activeStep.value = 1
}

function onDesignResult(data) {
  designSolutions.value = data?.solutions || []
  designStrategy.value = data?.strategy || 'balanced'
  // 持久化到 store，防止返回时丢失
  store.designResults = {
    solutions: designSolutions.value,
    strategy: designStrategy.value,
    confirmedSolution: null
  }
  activeStep.value = 2
}

function onSolutionConfirm(sol) {
  // 持久化确认的方案
  store.designResults.confirmedSolution = sol
  // 同步写入 survey 数据，确保仿真页面能读取
  store.survey.ratedEnergy = sol.totalEnergyMwh || store.survey.ratedEnergy
  store.survey.totalPower = sol.totalPowerMw || sol.totalEnergyMwh / (sol.duration || 2)
  store.survey.duration = sol.duration || sol.totalEnergyMwh / (sol.totalPowerMw || 50)
  store.survey.dod = sol.dod || store.survey.dod
  store.survey.cRate = sol.cRate || store.survey.cRate
  // systemParams 和 selectedProducts 已由 DesignResultPreview.confirmSolution() 写入
  // 标记 Phase2 完成
  store.phases.phase2 = { status: 'completed' }
  // 跳转到 Phase3 仿真
  router.push('/phase3')
}
</script>

<style scoped>
.steps-nav {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid var(--color-border);
  padding-bottom: 0.75rem;
  flex-wrap: wrap;
}

.steps-nav button {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-card);
  color: var(--color-text-secondary);
  cursor: pointer;
  font-size: 0.8125rem;
  transition: all 0.2s;
}

.steps-nav button:hover {
  border-color: var(--color-accent);
  color: var(--color-text);
}

.steps-nav button.active {
  background: var(--color-accent);
  color: var(--color-text-on-accent);
  border-color: var(--color-accent);
}

.steps-nav button.done {
  border-color: var(--color-success);
  color: var(--color-success);
}

.step-num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  font-size: 0.6875rem;
  font-weight: 700;
  background: rgba(0, 0, 0, 0.08);
}

.steps-nav button.active .step-num {
  background: rgba(255, 255, 255, 0.25);
}

.steps-nav button.done .step-num {
  background: rgba(22, 163, 74, 0.15);
}

.step-content {
  min-height: 300px;
}
</style>
