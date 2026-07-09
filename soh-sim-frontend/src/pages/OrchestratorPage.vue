<template>
  <div class="orchestrator-page">
    <div class="page-header">
      <h1>{{ $t('orchestrator.title') }}</h1>
      <p>{{ $t('orchestrator.desc') }}</p>
    </div>

    <!-- 项目选择栏 -->
    <div class="project-bar">
      <div class="form-group">
        <label>{{ $t('orchestrator.selectProject') }}</label>
        <select v-model="selectedProjectId" class="form-input" @change="onProjectChange">
          <option value="">{{ $t('orchestrator.noProject') }}</option>
          <option v-for="p in projects" :key="p.id" :value="p.id">
            {{ p.name || p.code || p.id }}
          </option>
        </select>
      </div>
      <button
        v-if="workflowResult && selectedProjectId"
        class="btn btn-save"
        :disabled="savingVersion"
        @click="saveAsVersion"
      >
        <span v-if="savingVersion" class="spinner"></span>
        {{ savingVersion ? $t('orchestrator.saving') : $t('orchestrator.saveAsVersion') }}
      </button>
      <span v-if="saveResult" class="save-success">{{ saveResult }}</span>
    </div>

    <div class="page-layout">
      <!-- 左侧：设计引擎面板 -->
      <div class="layout-left">
        <DesignEnginePanel
          @select="onSelectSolution"
          @workflow-complete="onWorkflowComplete"
        />
      </div>

      <!-- 右侧：方案对比 + 补容对比 + What-If -->
      <div class="layout-right">
        <DesignComparePanel :solutions="compareSolutions" />

        <!-- 补容策略对比 -->
        <AugmentationCompare :comparison="augComparison" />

        <!-- What-If 分析 -->
        <div v-if="baseSolution" class="panel-section what-if-section">
          <h3 class="section-title">
            <span class="icon">🔬</span> {{ $t('orchestrator.whatIf') }}
          </h3>
          <div class="what-if-form">
            <div class="form-row">
              <div class="form-group">
                <label>{{ $t('design.temperature') }} (°C)</label>
                <input
                  v-model.number="whatIf.temperature"
                  type="number"
                  min="-20"
                  max="60"
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label>{{ $t('design.dod') }} (%)</label>
                <input
                  v-model.number="whatIf.dod"
                  type="number"
                  min="50"
                  max="100"
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label>{{ $t('design.cyclesPerDay') }}</label>
                <input
                  v-model.number="whatIf.cyclesPerDay"
                  type="number"
                  min="0.5"
                  max="4"
                  step="0.5"
                  class="form-input"
                />
              </div>
            </div>
            <button
              class="btn btn-accent"
              :disabled="whatIfLoading"
              @click="runWhatIf"
            >
              <span v-if="whatIfLoading" class="spinner"></span>
              {{ whatIfLoading ? $t('orchestrator.analyzing') : $t('orchestrator.runWhatIf') }}
            </button>
          </div>

          <div v-if="whatIfResult" class="what-if-results">
            <h4>{{ $t('orchestrator.whatIfResult') }}</h4>
            <div class="delta-grid">
              <div
                v-for="(val, key) in whatIfResult.delta"
                :key="key"
                class="delta-item"
              >
                <span class="delta-label">{{ key }}</span>
                <span :class="['delta-value', val > 0 ? 'positive' : 'negative']">
                  {{ val > 0 ? '+' : '' }}{{ val.toFixed(2) }}%
                </span>
              </div>
            </div>
          </div>
          <div v-if="whatIfError" class="error-message">{{ whatIfError }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { get, post } from '../services/api.js'
import DesignEnginePanel from '../components/DesignEnginePanel.vue'
import DesignComparePanel from '../components/DesignComparePanel.vue'
import AugmentationCompare from '../components/AugmentationCompare.vue'

const compareSolutions = ref([])
const baseSolution = ref(null)
const workflowResult = ref(null)
const augComparison = ref({})

// 项目选择
const projects = ref([])
const selectedProjectId = ref('')
const savingVersion = ref(false)
const saveResult = ref(null)

const whatIf = reactive({
  temperature: 45,
  dod: 85,
  cyclesPerDay: 1
})

const whatIfLoading = ref(false)
const whatIfResult = ref(null)
const whatIfError = ref(null)

onMounted(async () => {
  try {
    const resp = await get('/api/projects')
    if (resp.success) {
      projects.value = resp.data || []
    }
  } catch (e) {
    console.error('加载项目列表失败:', e)
  }
})

function onProjectChange() {
  saveResult.value = null
}

function onSelectSolution(solution) {
  baseSolution.value = solution
  const exists = compareSolutions.value.find(s => s.id === solution.id)
  if (!exists) {
    compareSolutions.value = [...compareSolutions.value, solution]
  }
}

function onWorkflowComplete(data) {
  workflowResult.value = data
  const designs = (data.solutions || []).map(s => s.design).filter(Boolean)
  if (designs.length) {
    compareSolutions.value = designs
    baseSolution.value = designs[0]
  }

  // 提取补容对比数据
  const rec = data.recommendation
  if (rec?.simulation?.augmentationComparison) {
    augComparison.value = rec.simulation.augmentationComparison
  }

  // 如果选了项目，自动保存
  if (selectedProjectId.value) {
    saveResult.value = `已保存 ${data.pipeline_summary?.successful || 0} 个方案版本`
  }
}

async function saveAsVersion() {
  if (!selectedProjectId.value || !workflowResult.value) return
  savingVersion.value = true
  saveResult.value = null
  try {
    // 重新调用工作流并传入 project_id
    const resp = await post('/api/workflow/full', {
      survey_params: workflowResult.value.solutions?.[0]?.design
        ? { ratedEnergy: workflowResult.value.solutions[0].design.totalEnergyMwh }
        : {},
      strategy: workflowResult.value.strategy || 'economic',
      target_metric: workflowResult.value.target_metric || 'lcos',
      project_id: selectedProjectId.value
    })
    if (resp.success) {
      const count = resp.data?.saved_versions?.length || 0
      saveResult.value = `已保存 ${count} 个方案版本`
    }
  } catch (e) {
    saveResult.value = '保存失败: ' + (e.message || '未知错误')
  } finally {
    savingVersion.value = false
  }
}

async function runWhatIf() {
  if (!baseSolution.value) return
  whatIfLoading.value = true
  whatIfError.value = null
  whatIfResult.value = null

  try {
    const resp = await post('/api/workflow/what-if', {
      base_design: baseSolution.value,
      adjustments: { ...whatIf },
      survey_params: {
        ratedEnergy: baseSolution.value.totalEnergyMwh || 100,
        totalPower: baseSolution.value.totalPowerMW || 50,
        duration: baseSolution.value.duration || 2,
        temperature: baseSolution.value.degradationModel?.temperature || 25,
        cyclesPerDay: baseSolution.value.degradationModel?.cyclesPerDay || 1,
        dod: baseSolution.value.degradationModel?.dod || 90
      }
    })
    if (resp.success) {
      whatIfResult.value = resp.data
    }
  } catch (e) {
    whatIfError.value = e.message || 'What-If 分析失败'
  } finally {
    whatIfLoading.value = false
  }
}
</script>

<style scoped>
.orchestrator-page {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1.5rem;
}

.page-header {
  margin-bottom: 1rem;
}

.page-header h1 {
  font-size: 1.5rem;
  margin: 0 0 0.25rem 0;
  color: var(--text-primary, #1a1a1a);
}

.page-header p {
  color: var(--text-secondary, #888);
  font-size: 0.9rem;
  margin: 0;
}

/* Project Bar */
.project-bar {
  display: flex;
  align-items: flex-end;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  padding: 0.75rem 1rem;
  background: var(--card-bg, #fff);
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.form-group label {
  font-size: 0.8rem;
  color: var(--text-secondary, #666);
}

.form-input {
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--border-color, #ddd);
  border-radius: 6px;
  font-size: 0.9rem;
  min-width: 200px;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-save {
  background: var(--primary, #3b82f6);
  color: #fff;
}

.btn-save:hover:not(:disabled) {
  background: var(--primary-dark, #2563eb);
}

.btn-accent {
  background: #8b5cf6;
  color: #fff;
  align-self: flex-start;
}

.btn-accent:hover:not(:disabled) {
  background: #7c3aed;
}

.save-success {
  font-size: 0.85rem;
  color: #059669;
  font-weight: 500;
}

.spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  display: inline-block;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Layout */
.page-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  align-items: start;
}

@media (max-width: 1024px) {
  .page-layout {
    grid-template-columns: 1fr;
  }
}

.layout-left,
.layout-right {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.panel-section {
  background: var(--card-bg, #fff);
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  margin: 0 0 1rem 0;
  color: var(--text-primary, #1a1a1a);
}

.what-if-form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.form-row {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.error-message {
  margin-top: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: #fef2f2;
  color: #dc2626;
  border-radius: 6px;
  font-size: 0.85rem;
}

.what-if-results {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-light, #f3f4f6);
}

.what-if-results h4 {
  margin: 0 0 0.75rem 0;
  font-size: 0.95rem;
}

.delta-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 0.5rem;
}

.delta-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.5rem;
  background: var(--metric-bg, #f8fafc);
  border-radius: 6px;
}

.delta-label {
  font-size: 0.7rem;
  color: var(--text-secondary, #888);
  text-transform: uppercase;
}

.delta-value {
  font-size: 0.95rem;
  font-weight: 600;
}

.delta-value.positive { color: #059669; }
.delta-value.negative { color: #dc2626; }
</style>
