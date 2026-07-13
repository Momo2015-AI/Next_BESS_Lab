<template>
  <AppPage :title-key="'tools.templatesTitle'" :desc-key="'tools.templatesDesc'">

    <div class="toolbar">
      <button class="btn-primary" @click="loadTemplates">{{ $t('tools.templatesRefresh') }}</button>
      <button class="btn-secondary" @click="seedTemplates">{{ $t('tools.templatesSeed') }}</button>
    </div>

    <div v-if="loading" class="empty-state">{{ $t('tools.templatesLoading') }}</div>

    <div v-else-if="templates.length === 0" class="empty-state">
      <p>{{ $t('tools.templatesEmpty') }}</p>
      <button class="btn-primary" @click="seedTemplates">{{ $t('tools.templatesSeed') }}</button>
    </div>

    <div v-else class="template-grid">
      <div v-for="t in templates" :key="t.id" class="template-card">
        <div class="card-header">
          <h3 class="card-title">
            {{ t.name }}
          </h3>
          <span v-if="t.is_default" class="badge-default">{{ $t('tools.templatesDefault') }}</span>
          <span class="badge-type">{{ t.template_type }}</span>
        </div>
        <p class="card-desc">
          {{ t.description }}
        </p>

        <div class="card-metrics">
          <div class="metric">
            <span class="metric-label">{{ $t('tools.templatesSohFactor') }}</span>
            <span class="metric-value">{{ t.global_soh_factor }}</span>
          </div>
          <div class="metric">
            <span class="metric-label">{{ $t('tools.templatesRteFactor') }}</span>
            <span class="metric-value">{{ t.global_rte_factor }}</span>
          </div>
        </div>

        <div v-if="t.annual_corrections" class="card-corrections">
          <div class="corrections-title">{{ $t('tools.templatesAnnualCorrection') }}</div>
          <div class="corrections-grid">
            <div v-for="(val, year) in t.annual_corrections" :key="year" class="correction-item">
              <span class="year-label">
                {{ $t('tools.templatesYearPrefix') }}{{ year }}{{ $t('tools.templatesYearSuffix') }}
              </span>
              <span class="year-value">{{ val }}</span>
            </div>
          </div>
        </div>

        <div class="card-footer">
          <span class="card-meta">{{ formatDate(t.created_at) }}</span>
        </div>
      </div>
    </div>
  </AppPage>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api.js'
import AppPage from '../components/AppPage.vue'

const templates = ref([])
const loading = ref(false)

async function loadTemplates() {
  loading.value = true
  try {
    const data = await api.get('/api/correction-templates')
    if (data.success) {
      templates.value = data.data
    }
  } catch (e) {
    console.error('Failed to load templates:', e)
  } finally {
    loading.value = false
  }
}

async function seedTemplates() {
  loading.value = true
  try {
    const data = await api.post('/api/correction-templates/seed')
    if (data.success) {
      loadTemplates()
    }
  } catch (e) {
    console.error('Failed to seed templates:', e)
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

.empty-state {
  text-align: center;
  padding: 48px 24px;
  background: var(--section-card-bg);
  border-radius: var(--section-card-radius);
  border: 1px solid var(--section-card-border);
}
.empty-state p {
  color: var(--color-text-muted);
  margin-bottom: 16px;
}

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
  color: var(--form-label-color);
}

.metric-value {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-accent);
}

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
  background: var(--color-card);
  border-radius: 4px;
  border: 1px solid var(--color-border);
}

.year-label {
  font-size: 10px;
  color: var(--color-text-muted);
}
.year-value {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-text);
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 8px;
  border-top: 1px solid var(--color-border);
}

.card-meta {
  font-size: 11px;
  color: var(--color-text-muted);
}
</style>
