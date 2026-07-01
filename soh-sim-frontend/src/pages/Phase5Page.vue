<template>
  <div class="phase-page phase5-page">
    <div class="phase-header">
      <h1>Phase 5: 成果输出</h1>
      <p class="phase-desc">技术报告、设备清单、数据导出、项目存档</p>
    </div>
    <div class="phase-body">
      <div class="steps-nav">
        <button v-for="(s, i) in steps" :key="i" :class="{ active: activeStep === i }" @click="activeStep = i">
          {{ s.label }}
        </button>
      </div>
      <div class="step-content">
        <div v-if="activeStep === 0" class="card">
          <h3>技术报告 (PDF)</h3>
          <p>整合项目概览、系统配置、性能分析、经济指标生成完整技术报告。</p>
          <button :disabled="generating" @click="generateReport">生成技术报告</button>
          <p v-if="reportMsg" class="msg">
            {{ reportMsg }}
          </p>
        </div>
        <div v-if="activeStep === 1" class="card">
          <h3>设备清单 (BOM)</h3>
          <p>生成电芯、集装箱、PCS 等设备的型号和数量清单。</p>
          <button :disabled="generatingBom" @click="generateBom">生成设备清单</button>
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
          <h3>项目存档</h3>
          <p>将当前项目全部数据保存到数据库。</p>
          <button @click="saveProject">保存项目</button>
          <p v-if="saveMsg" class="msg">
            {{ saveMsg }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useBessStore } from '../stores/bess.js'
import DataExport from '../components/DataExport.vue'

const store = useBessStore()
const activeStep = ref(0)
const steps = [
  { label: '5.1 技术报告' },
  { label: '5.2 设备清单' },
  { label: '5.3 数据导出' },
  { label: '5.4 项目存档' }
]

const generating = ref(false)
const reportMsg = ref('')
const generatingBom = ref(false)
const bomMsg = ref('')
const saveMsg = ref('')

async function generateReport() {
  generating.value = true
  reportMsg.value = ''
  try {
    const res = await fetch('/api/report/technical', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        projectId: store.project.id,
        results: store.results,
        systemParams: store.systemParams,
        financial: store.financial.metrics
      })
    })
    if (res.ok) {
      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'technical-report.pdf'
      a.click()
      URL.revokeObjectURL(url)
      store.exports.reportGenerated = true
      reportMsg.value = '报告已生成并下载'
    } else {
      reportMsg.value = '报告生成失败'
    }
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
    const res = await fetch('/api/report/bom', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ projectId: store.project.id, products: store.selectedProducts })
    })
    if (res.ok) {
      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'bom-list.pdf'
      a.click()
      URL.revokeObjectURL(url)
      store.exports.bomGenerated = true
      bomMsg.value = 'BOM 清单已生成并下载'
    } else {
      bomMsg.value = 'BOM 生成失败'
    }
  } catch (e) {
    bomMsg.value = '错误: ' + e.message
  } finally {
    generatingBom.value = false
  }
}

async function saveProject() {
  saveMsg.value = ''
  try {
    await fetch('/api/project/sync-params', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        params: store.systemParams,
        soh: store.degradation.soh,
        rte: store.degradation.rte,
        dod: store.degradation.dod,
        augQty: store.degradation.augQty
      })
    })
    saveMsg.value = '项目已保存'
  } catch (e) {
    saveMsg.value = '保存失败: ' + e.message
  }
}
</script>

<style scoped>
.phase-page {
  padding: 24px;
}
.phase-header {
  margin-bottom: 24px;
}
.phase-header h1 {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 8px;
}
.phase-desc {
  color: var(--text-secondary, #666);
  font-size: 14px;
  margin: 0;
}
.steps-nav {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}
.steps-nav button {
  padding: 8px 16px;
  border: 1px solid var(--border, #ddd);
  border-radius: 6px;
  background: var(--bg, #fff);
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
}
.steps-nav button.active {
  background: #409eff;
  color: #fff;
  border-color: #409eff;
}
.step-content {
  min-height: 400px;
}
.card {
  background: var(--bg-card, #fff);
  padding: 24px;
  border-radius: 8px;
  border: 1px solid var(--border, #eee);
}
.card h3 {
  margin: 0 0 8px;
  font-size: 18px;
}
.card p {
  margin: 0 0 16px;
  color: var(--text-secondary, #666);
  font-size: 14px;
}
.card button {
  padding: 10px 24px;
  background: #409eff;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
}
.card button:hover {
  background: #337ecc;
}
.card button:disabled {
  background: #ccc;
}
.msg {
  margin-top: 12px;
  font-size: 13px;
  color: #67c23a;
}
</style>
