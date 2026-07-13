<template>
  <AppPage :title-key="titleKey" :desc-key="descKey">
    <!-- 模式切换条 -->
    <div class="mode-switch-bar">
      <span class="mode-label">{{ $t('financial.dataSource') }}：</span>
      <button
        :class="['mode-btn', { active: mode === 'project' }]"
        @click="mode = 'project'"
      >
        📋 {{ $t('financial.modeProject') }}
      </button>
      <button
        :class="['mode-btn', { active: mode === 'standalone' }]"
        @click="mode = 'standalone'"
      >
        ✏️ {{ $t('financial.modeStandalone') }}
      </button>
      <span v-if="mode === 'project' && hasProjectData" class="mode-hint">
        {{ $t('financial.dataFromProject', { name: projectName }) }}
      </span>
      <span v-else-if="mode === 'project' && !hasProjectData" class="mode-hint-warn">
        {{ $t('financial.noProjectData') }}
      </span>
      <span v-else class="mode-hint">
        {{ $t('financial.standaloneHint') }}
      </span>
    </div>

    <FinancialDashboard
      :mode="mode"
      :params="store.systemParams"
      :results="store.results"
      :soh="store.degradation.soh"
      :rte="store.degradation.rte"
      :aug-qty="store.degradation.augQty"
    />
  </AppPage>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useBessStore } from '../stores/bess.js'
import AppPage from '../components/AppPage.vue'
import FinancialDashboard from '../components/FinancialDashboard.vue'

const store = useBessStore()

// 默认模式：项目数据带入
const mode = ref('project')

// 判断是否有项目数据（survey 完成即有）
const hasProjectData = computed(() => {
  const p = store.systemParams || {}
  return !!(p.ratedEnergy || p.initContainerQty || p.totalPower)
})

const projectName = computed(() => {
  const p = store.systemParams || {}
  if (p.projectName) return p.projectName
  if (p.ratedEnergy) return `${p.ratedEnergy}MWh × ${p.initContainerQty || '?'}台`
  return '-'
})

const titleKey = computed(() => mode.value === 'standalone' ? 'financial.standaloneTitle' : 'tools.financialTitle')
const descKey = computed(() => mode.value === 'standalone' ? 'financial.standaloneDesc' : 'tools.financialDesc')

// 没有项目数据时自动切到独立模式
watch(hasProjectData, (val) => {
  if (!val && mode.value === 'project') {
    mode.value = 'standalone'
  }
}, { immediate: true })
</script>

<style scoped>
.mode-switch-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  margin: 0 4px 4px 4px;
  background: var(--panel-sub-bg);
  border: var(--panel-sub-border);
  border-radius: var(--radius-md);
}

.mode-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
}

.mode-btn {
  padding: 4px 14px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border);
  background: var(--item-bg);
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition:
    background 0.3s var(--ease-precision),
    border-color 0.3s var(--ease-precision),
    color 0.3s var(--ease-precision),
    box-shadow 0.3s var(--ease-precision);
}

.mode-btn:hover {
  background: var(--bg-card);
  border-color: var(--border-color-hover);
  color: var(--text-primary);
}

.mode-btn.active {
  background: var(--btn-accent-bg);
  border: var(--btn-accent-border);
  color: var(--btn-accent-text);
  font-weight: 600;
  box-shadow: var(--shadow-card-active);
}

.mode-hint {
  font-size: 11px;
  color: var(--color-text-muted);
  margin-left: 8px;
}

.mode-hint-warn {
  font-size: 11px;
  color: var(--color-warning);
  margin-left: 8px;
}
</style>
