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
.toolbar {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

.btn-primary {
  padding: 8px 20px;
  border-radius: var(--radius-md);
  background: var(--color-accent);
  color: #fff;
  border: none;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s ease;
}
.btn-primary:hover { opacity: 0.88; }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-secondary {
  padding: 8px 20px;
  border-radius: var(--radius-md);
  background: var(--color-card);
  color: var(--color-accent);
  border: 1px solid var(--color-accent);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-secondary:hover { background: var(--color-accent-glow, rgba(37,99,235,0.08)); }

.empty-state {
  text-align: center;
  padding: 48px 24px;
  background: var(--section-card-bg);
  border-radius: var(--section-card-radius);
  border: 1px solid var(--section-card-border);
}
.empty-state p { color: var(--color-text-muted); margin-bottom: 16px; }

.template-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 16px;
}

.template-card {
  background: var(--section-card-bg);
  border-radius: var(--section-card-radius);
  padding: 20px;
  border: 1px solid var(--section-card-border);
  box-shadow: var(--section-card-shadow);
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
  color: var(--section-title-color);
}

.badge-default {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  background: rgba(16, 185, 129, 0.15);
  color: var(--color-success);
}

.badge-type {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
  background: var(--form-field-bg);
  color: var(--color-text-muted);
  margin-left: auto;
}

.card-desc {
  font-size: 13px;
  color: var(--color-text-muted);
  margin: 0 0 12px;
}

.card-metrics { display: flex; gap: 16px; margin-bottom: 12px; }

.metric { display: flex; flex-direction: column; gap: 2px; }

.metric-label { font-size: 11px; color: var(--form-label-color); }

.metric-value { font-size: 18px; font-weight: 700; color: var(--color-accent); }

.card-corrections {
  background: var(--form-field-bg);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 12px;
  flex: 1;
}

.corrections-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-muted);
  margin-bottom: 8px;
}

.corrections-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }

.correction-item {
  display: flex; flex-direction: column; align-items: center;
  padding: 4px; background: var(--color-card); border-radius: 4px;
  border: 1px solid var(--color-border);
}

.year-label { font-size: 10px; color: var(--color-text-muted); }
.year-value { font-size: 14px; font-weight: 700; color: var(--color-text); }

.card-footer {
  display: flex; justify-content: space-between; align-items: center;
  padding-top: 8px; border-top: 1px solid var(--color-border);
}

.card-meta { font-size: 11px; color: var(--color-text-muted); }
</style>
