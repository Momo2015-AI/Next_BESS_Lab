<template>
  <AppPage title-key="tools.reportTitle" desc-key="tools.reportDesc">
    <p class="report-intro">{{ $t('tools.reportIntro') }}</p>

    <div class="report-options">
      <SectionCard number="01" :title="$t('tools.reportTechnical')">
        <div class="report-card">
          <AppIcon name="document" :size="36" class="report-icon" />
          <p class="report-desc">{{ $t('tools.reportTechnicalDesc') }}</p>
          <button
            class="btn-generate"
            :disabled="generating === 'technical'"
            @click="generateReport('technical', '/api/report/technical')"
          >
            {{ generating === 'technical' ? $t('common.generating') : $t('common.generate') }}
          </button>
        </div>
      </SectionCard>

      <SectionCard number="02" :title="$t('tools.reportFinancial')">
        <div class="report-card">
          <AppIcon name="dollar" :size="36" class="report-icon" />
          <p class="report-desc">{{ $t('tools.reportFinancialDesc') }}</p>
          <button
            class="btn-generate"
            :disabled="generating === 'financial'"
            @click="generateReport('financial', '/api/report/financial')"
          >
            {{ generating === 'financial' ? $t('common.generating') : $t('common.generate') }}
          </button>
        </div>
      </SectionCard>

      <SectionCard number="03" :title="$t('tools.reportExecutive')">
        <div class="report-card">
          <AppIcon name="briefcase" :size="36" class="report-icon" />
          <p class="report-desc">{{ $t('tools.reportExecutiveDesc') }}</p>
          <button
            class="btn-generate"
            :disabled="generating === 'executive'"
            @click="generateReport('executive', '/api/report/executive')"
          >
            {{ generating === 'executive' ? $t('common.generating') : $t('common.generate') }}
          </button>
        </div>
      </SectionCard>
    </div>

    <div v-if="downloadUrl" class="download-section">
      <p class="download-message">{{ $t('tools.reportReady') }}</p>
      <a :href="downloadUrl" class="btn-download" download>
        <AppIcon name="download" :size="16" class="download-icon" />
        {{ $t('tools.downloadReport') }}
      </a>
    </div>

    <div v-if="errorMsg" class="error-message">{{ errorMsg }}</div>
  </AppPage>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppPage from '../components/AppPage.vue'
import SectionCard from '../components/SectionCard.vue'
import AppIcon from '../components/AppIcon.vue'
import { post } from '../services/api.js'
import { useBessStore } from '../stores/bess.js'

const store = useBessStore()
const generating = ref(null)
const downloadUrl = ref(store.exports.reportDownloadUrl || '')
const errorMsg = ref('')

onMounted(() => {
  if (store.exports.reportDownloadUrl) {
    downloadUrl.value = store.exports.reportDownloadUrl
  }
})

async function generateReport(type, url) {
  generating.value = type
  downloadUrl.value = ''
  errorMsg.value = ''

  try {
    const projectId = store.project.id || localStorage.getItem('current_project_id')
    const { data } = await post(url, projectId ? { project_id: projectId } : {})
    if (data && data.url) {
      downloadUrl.value = data.url
      store.exports.reportDownloadUrl = data.url
    } else if (data && data.download_url) {
      downloadUrl.value = data.download_url
      store.exports.reportDownloadUrl = data.download_url
    }
  } catch (err) {
    errorMsg.value = err.message || 'Report generation failed'
  } finally {
    generating.value = null
  }
}
</script>

<style scoped>
.report-intro {
  color: var(--color-text-secondary);
  font-size: 14px;
  margin-bottom: 24px;
  text-align: center;
}

.report-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.report-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 16px 0;
}

.report-icon {
  color: var(--color-accent);
  margin-bottom: 12px;
}

.report-desc {
  color: var(--color-text-muted);
  font-size: 13px;
  line-height: 1.5;
  margin-bottom: 16px;
  min-height: 40px;
}

.btn-generate {
  padding: 8px 24px;
  border: 1px solid var(--color-accent);
  border-radius: 6px;
  background: transparent;
  color: var(--color-accent);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-generate:hover:not(:disabled) {
  background: var(--color-accent);
  color: var(--color-text-on-accent);
}

.btn-generate:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.download-section {
  margin-top: 28px;
  text-align: center;
}

.download-message {
  color: var(--color-text-secondary);
  font-size: 14px;
  margin-bottom: 12px;
}

.btn-download {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 28px;
  background: var(--color-accent);
  color: var(--color-text-on-accent);
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  transition: opacity 0.2s ease;
}

.btn-download:hover {
  opacity: 0.85;
}

.download-icon {
  flex-shrink: 0;
}

.error-message {
  margin-top: 16px;
  text-align: center;
  color: var(--color-danger, #ef4444);
  font-size: 13px;
}

@media (max-width: 768px) {
  .report-options {
    grid-template-columns: 1fr;
  }
}
</style>
