<template>
  <div class="phase-page phase5-page">
    <div class="phase-header">
      <h1>{{ $t('phase5.title') }}</h1>
      <p class="phase-desc">{{ $t('phase5.desc') }}</p>
    </div>
    <div class="phase-body">
      <div class="steps-nav">
        <button v-for="(s, i) in steps" :key="i" :class="{ active: activeStep === i }" @click="activeStep = i">
          {{ s.label }}
        </button>
      </div>
      <div class="step-content">
        <div v-if="activeStep === 0" class="card">
          <h3>{{ $t('phase5.reportTitle') }}</h3>
          <p>{{ $t('phase5.reportDesc') }}</p>
          <button :disabled="generating" @click="generateReport">{{ $t('phase5.reportBtn') }}</button>
          <p v-if="reportMsg" class="msg">
            {{ reportMsg }}
          </p>
        </div>
        <div v-if="activeStep === 1" class="card">
          <h3>{{ $t('phase5.bomTitle') }}</h3>
          <p>{{ $t('phase5.bomDesc') }}</p>
          <button :disabled="generatingBom" @click="generateBom">{{ $t('phase5.bomBtn') }}</button>
          <p v-if="bomMsg" class="msg">
            {{ bomMsg }}
          </p>
        </div>
        <DataExport
          v-if="activeStep === 2"
          :params="store.systemParams"
          :results="store.results"
          :soh="store.degradation.soh"
          :rte="store.degradation.rte"
          :dod="store.degradation.dod"
          :aug-qty="store.degradation.augQty"
          :financial="store.financial.metrics"
          :project-id="store.project.id"
        />
        <div v-if="activeStep === 3" class="card">
          <h3>{{ $t('phase5.archiveTitle') }}</h3>
          <p>{{ $t('phase5.archiveDesc') }}</p>
          <button @click="saveProject">{{ $t('phase5.archiveBtn') }}</button>
          <p v-if="saveMsg" class="msg">
            {{ saveMsg }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useBessStore } from '../stores/bess.js'
import DataExport from '../components/DataExport.vue'
import api from '../services/api.js'

const store = useBessStore()
const { t } = useI18n()
const activeStep = ref(0)
const steps = computed(() => [
  { label: t('phase5.step1') },
  { label: t('phase5.step2') },
  { label: t('phase5.step3') },
  { label: t('phase5.step4') }
])

const generating = ref(false)
const reportMsg = ref('')
const generatingBom = ref(false)
const bomMsg = ref('')
const saveMsg = ref('')

async function generateReport() {
  generating.value = true
  reportMsg.value = ''
  try {
    const blob = await api.download('/api/report/technical', {
      projectId: store.project.id,
      results: store.results,
      systemParams: store.systemParams,
      financial: store.financial.metrics
    })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'technical-report.pdf'
    a.click()
    URL.revokeObjectURL(url)
    store.exports.reportGenerated = true
    reportMsg.value = '报告已生成并下载'
  } catch (e) {
    reportMsg.value = '错误: ' + e.message
  } finally {
    generating.value = false
  }
}

async function generateBom() {
  generatingBom.value = true
  bomMsg.value = ''
  try {
    const blob = await api.download('/api/report/bom', {
      projectId: store.project.id,
      products: store.selectedProducts
    })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'bom-list.pdf'
    a.click()
    URL.revokeObjectURL(url)
    store.exports.bomGenerated = true
    bomMsg.value = 'BOM 清单已生成并下载'
  } catch (e) {
    bomMsg.value = '错误: ' + e.message
  } finally {
    generatingBom.value = false
  }
}

async function saveProject() {
  saveMsg.value = ''
  try {
    await api.post('/api/project/sync-params', {
      params: store.systemParams,
      soh: store.degradation.soh,
      rte: store.degradation.rte,
      dod: store.degradation.dod,
      augQty: store.degradation.augQty
    })
    saveMsg.value = '项目已保存'
  } catch (e) {
    saveMsg.value = '保存失败: ' + e.message
  }
}
</script>

<style scoped>
.card {
  background: var(--section-card-bg);
  padding: 24px 28px;
  border-radius: var(--section-card-radius);
  border: 1px solid var(--section-card-border);
  box-shadow: var(--section-card-shadow);
}
.card h3 {
  margin: 0 0 8px;
  font-size: var(--section-title-size);
  font-weight: var(--section-title-weight);
  color: var(--section-title-color);
}
.card p {
  margin: 0 0 16px;
  color: var(--color-text-muted);
  font-size: 14px;
}
.card button {
  padding: 10px 24px;
  background: var(--color-accent);
  color: var(--color-text-on-accent);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: opacity 0.2s ease;
}
.card button:hover {
  opacity: 0.88;
}
.card button:disabled {
  background: var(--color-text-muted);
  opacity: 0.5;
  cursor: not-allowed;
}
.msg {
  margin-top: 12px;
  font-size: 13px;
  color: var(--color-success);
}
</style>
