<template>
  <div class="design-template-selector">
    <h3 class="dts-title">{{ $t('designTemplate.selectTitle') }}</h3>
    <p class="dts-desc">{{ $t('designTemplate.selectDesc') }}</p>

    <div v-if="loading" class="dts-loading">{{ $t('admin.loading') }}</div>

    <div v-else class="dts-grid">
      <div
        v-for="tmpl in templates"
        :key="tmpl.id"
        :class="['dts-card', { selected: selectedId === tmpl.id }]"
        @click="selectTemplate(tmpl)"
      >
        <div class="dts-card-header">
          <span class="dts-strategy-badge">{{ strategyLabel(tmpl.strategy) }}</span>
          <span v-if="tmpl.isDefault" class="dts-default-badge">{{ $t('designTemplate.default') }}</span>
        </div>
        <h4 class="dts-card-name">{{ tmpl.name }}</h4>
        <p class="dts-card-desc">{{ tmpl.description }}</p>
        <div v-if="tmpl.containerModel || tmpl.pcsModel" class="dts-card-products">
          <span v-if="tmpl.containerModel" class="dts-product-tag">
            <AppIcon name="briefcase" size="12" />
            {{ tmpl.containerModel }}
          </span>
          <span v-if="tmpl.pcsModel" class="dts-product-tag">
            <AppIcon name="lightning" size="12" />
            {{ tmpl.pcsModel }}
          </span>
        </div>
      </div>
    </div>

    <div class="dts-actions">
      <button class="dts-btn dts-btn-secondary" @click="$emit('skip')">
        {{ $t('designTemplate.skipTemplate') }}
      </button>
      <button class="dts-btn dts-btn-primary" :disabled="!selectedId" @click="confirmSelection">
        {{ $t('designTemplate.confirmTemplate') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useBessStore } from '../stores/bess.js'
import api from '../services/api.js'
import AppIcon from './AppIcon.vue'

const { t } = useI18n()
const store = useBessStore()

const emit = defineEmits(['confirm', 'skip'])

const templates = ref([])
const selectedId = ref(null)
const selectedTemplate = ref(null)
const loading = ref(false)

const strategyLabels = {
  economic: t('designTemplate.strategyEconomic'),
  balanced: t('designTemplate.strategyBalanced'),
  flexible: t('designTemplate.strategyFlexible'),
  manufacturer: t('designTemplate.strategyManufacturer')
}

function strategyLabel(key) {
  return strategyLabels[key] || key
}

async function loadTemplates() {
  loading.value = true
  try {
    const res = await api.get('/api/admin/design-templates')
    templates.value = res?.data || res?.items || []
    // 自动选中默认模板
    const def = templates.value.find((t) => t.isDefault)
    if (def) {
      selectedId.value = def.id
      selectedTemplate.value = def
    }
  } catch (e) {
    console.error('Failed to load design templates:', e)
  } finally {
    loading.value = false
  }
}

function selectTemplate(tmpl) {
  selectedId.value = tmpl.id
  selectedTemplate.value = tmpl
}

function confirmSelection() {
  if (!selectedTemplate.value) return
  const tmpl = selectedTemplate.value

  // 将模板参数填入 store
  if (tmpl.strategy) {
    store.systemParams.strategy = tmpl.strategy
  }
  if (tmpl.cellModel) {
    store.selectedProducts.cell = { model: tmpl.cellModel }
  }
  if (tmpl.containerModel) {
    store.selectedProducts.container = { model: tmpl.containerModel }
  }
  if (tmpl.pcsModel) {
    store.selectedProducts.pcs = { model: tmpl.pcsModel }
  }
  if (tmpl.defaultDuration) {
    store.survey.duration = tmpl.defaultDuration
  }
  if (tmpl.defaultDod) {
    store.survey.dod = tmpl.defaultDod
  }

  emit('confirm', selectedTemplate.value)
}

onMounted(() => {
  loadTemplates()
})
</script>

<style scoped>
.design-template-selector {
  padding: 1rem 0;
}

.dts-title {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.dts-desc {
  color: var(--color-text-secondary);
  font-size: 0.875rem;
  margin-bottom: 1.25rem;
}

.dts-loading {
  text-align: center;
  padding: 2rem;
  color: var(--color-text-secondary);
}

.dts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.dts-card {
  border: 2px solid var(--color-border);
  border-radius: 10px;
  padding: 1.125rem;
  cursor: pointer;
  transition:
    border-color 0.2s,
    box-shadow 0.2s;
  background: var(--color-card);
}

.dts-card:hover {
  border-color: var(--color-accent);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.dts-card.selected {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 2px rgba(var(--color-accent-rgb, 59, 130, 246), 0.3);
}

.dts-card-header {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.dts-strategy-badge {
  font-size: 0.75rem;
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  background: var(--color-accent-glow);
  color: var(--color-accent);
  font-weight: 500;
}

.dts-default-badge {
  font-size: 0.7rem;
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  background: var(--color-success-glow);
  color: var(--color-success);
}

.dts-card-name {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.375rem;
}

.dts-card-desc {
  font-size: 0.8125rem;
  color: var(--color-text-secondary);
  line-height: 1.4;
  margin-bottom: 0.5rem;
}

.dts-card-products {
  display: flex;
  flex-wrap: wrap;
  gap: 0.375rem;
}

.dts-product-tag {
  font-size: 0.75rem;
  padding: 0.125rem 0.5rem;
  background: var(--color-bg-secondary, #f3f4f6);
  border-radius: 4px;
  color: var(--color-text-secondary);
}

.dts-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.dts-btn {
  padding: 0.5rem 1.25rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: opacity 0.2s;
}

.dts-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.dts-btn-secondary {
  background: var(--color-bg-secondary, #f3f4f6);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

.dts-btn-primary {
  background: var(--color-accent);
  color: var(--color-text-on-accent);
}
</style>
