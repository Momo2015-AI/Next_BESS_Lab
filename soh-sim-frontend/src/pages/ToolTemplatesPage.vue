<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>校正因子模板</h1>
      <p>管理 Arrhenius 等模型的校正因子模板</p>
    </div>

    <div class="toolbar">
      <button class="btn-primary" @click="loadTemplates">刷新列表</button>
      <button class="btn-secondary" @click="seedTemplates">初始化默认模板</button>
    </div>

    <div v-if="loading" class="empty-state">加载中...</div>

    <div v-else-if="templates.length === 0" class="empty-state">
      <p>暂无校正因子模板</p>
      <button class="btn-primary" @click="seedTemplates">初始化默认模板</button>
    </div>

    <div v-else class="template-grid">
      <div v-for="t in templates" :key="t.id" class="template-card">
        <div class="card-header">
          <h3 class="card-title">
            {{ t.name }}
          </h3>
          <span v-if="t.is_default" class="badge-default">默认</span>
          <span class="badge-type">{{ t.template_type }}</span>
        </div>
        <p class="card-desc">
          {{ t.description }}
        </p>

        <div class="card-metrics">
          <div class="metric">
            <span class="metric-label">SOH 因子</span>
            <span class="metric-value">{{ t.global_soh_factor }}</span>
          </div>
          <div class="metric">
            <span class="metric-label">RTE 因子</span>
            <span class="metric-value">{{ t.global_rte_factor }}</span>
          </div>
        </div>

        <div v-if="t.annual_corrections" class="card-corrections">
          <div class="corrections-title">年度校正曲线</div>
          <div class="corrections-grid">
            <div v-for="(val, year) in t.annual_corrections" :key="year" class="correction-item">
              <span class="year-label">第{{ year }}年</span>
              <span class="year-value">{{ val }}</span>
            </div>
          </div>
        </div>

        <div class="card-footer">
          <span class="card-meta">{{ formatDate(t.created_at) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const templates = ref([])
const loading = ref(false)

async function loadTemplates() {
  loading.value = true
  try {
    const resp = await fetch('/api/correction-templates')
    const data = await resp.json()
    if (data.success) {
      templates.value = data.data
    }
  } catch (e) {
    console.error('加载模板失败:', e)
  } finally {
    loading.value = false
  }
}

async function seedTemplates() {
  loading.value = true
  try {
    const resp = await fetch('/api/correction-templates/seed', { method: 'POST' })
    const data = await resp.json()
    if (data.success) {
      loadTemplates()
    }
  } catch (e) {
    console.error('初始化模板失败:', e)
  } finally {
    loading.value = false
  }
}

function formatDate(iso) {
  if (!iso) return '-'
  const d = new Date(iso)
  return d.toLocaleDateString('zh-CN')
}

onMounted(() => {
  loadTemplates()
})
</script>

<style scoped>
.tool-page {
  padding: 24px;
}

.tool-header {
  margin-bottom: 24px;
}
.tool-header h1 {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 8px;
}
.tool-header p {
  color: var(--text-secondary, #666);
  font-size: 14px;
  margin: 0;
}

.toolbar {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

.btn-primary {
  padding: 8px 16px;
  border-radius: 6px;
  background: #0071e3;
  color: white;
  border: none;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.btn-primary:hover {
  background: var(--color-accent-secondary);
}
.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  padding: 8px 16px;
  border-radius: 6px;
  background: var(--color-card);
  color: var(--color-accent);
  border: 1px solid var(--color-accent);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.btn-secondary:hover {
  background: var(--color-accent-glow);
}

.empty-state {
  text-align: center;
  padding: 48px 24px;
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e0e0e0;
}
.empty-state p {
  color: #999;
  margin-bottom: 16px;
}

.template-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 16px;
}

.template-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e0e0e0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.card-title {
  font-size: 16px;
  font-weight: 700;
  margin: 0;
  color: #333;
}

.badge-default {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  background: #d1fae5;
  color: #065f46;
}

.badge-type {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
  background: #f3f4f6;
  color: #6b7280;
  margin-left: auto;
}

.card-desc {
  font-size: 13px;
  color: #666;
  margin: 0 0 12px;
}

.card-metrics {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.metric {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.metric-label {
  font-size: 11px;
  color: #999;
}

.metric-value {
  font-size: 18px;
  font-weight: 700;
  color: #0071e3;
}

.card-corrections {
  background: #f9fafb;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 12px;
  flex: 1;
}

.corrections-title {
  font-size: 12px;
  font-weight: 600;
  color: #666;
  margin-bottom: 8px;
}

.corrections-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
}

.correction-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 4px;
  background: #fff;
  border-radius: 4px;
  border: 1px solid #e5e7eb;
}

.year-label {
  font-size: 10px;
  color: #999;
}

.year-value {
  font-size: 14px;
  font-weight: 700;
  color: #333;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 8px;
  border-top: 1px solid #f0f0f0;
}

.card-meta {
  font-size: 11px;
  color: #999;
}
</style>
