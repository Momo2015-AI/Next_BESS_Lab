<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>调研输入</h1>
      <p>录入或搜索项目调研数据，作为仿真计算的输入参数</p>
    </div>

    <!-- 搜索区域 -->
    <SectionCard number="01" title="查找调研数据">
      <div class="form-grid-2">
        <div class="search-field-row">
          <FormField v-model="surveyId" label="调研表串码ID" type="text" placeholder="输入调研表ID" />
          <button :disabled="loading" class="btn-search-inline" @click="loadSurveyById">
            {{ loading ? '加载中...' : '加载' }}
          </button>
        </div>
        <div class="search-field-row">
          <FormField v-model="searchKeyword" label="项目名称搜索" type="text" placeholder="输入项目名称搜索" />
          <button :disabled="loading" class="btn-search-inline" @click="searchByProjectName">
            {{ loading ? '搜索中...' : '搜索' }}
          </button>
        </div>
      </div>
      <div v-if="searchResults.length > 0" class="search-results mt-4">
        <h4 class="section-title">搜索结果</h4>
        <div class="results-list">
          <div v-for="item in searchResults" :key="item.id" class="result-item" @click="selectSurvey(item)">
            <div class="result-info">
              <p class="result-name">{{ item.project_name }}</p>
              <p class="result-detail">{{ item.location }} | {{ item.total_mw }}MW / {{ item.total_mwh }}MWh</p>
            </div>
            <span class="result-action">选择</span>
          </div>
        </div>
      </div>
    </SectionCard>

    <!-- 项目基本信息 -->
    <SectionCard number="02" title="项目基本信息">
      <div class="form-grid-3">
        <FormField v-model="formData.projectName" label="项目名称" type="text" placeholder="项目名称" />
        <FormField v-model="formData.location" label="项目地点" type="text" placeholder="项目地点" />
        <FormField
          v-model.number="formData.ratedEnergy"
          label="额定能量 (MWh)"
          type="number"
          step="0.1"
          placeholder="5"
        />
        <FormField v-model.number="formData.containerQty" label="集装箱数量" type="number" placeholder="1" />
        <FormField v-model.number="formData.pcsQty" label="PCS数量" type="number" placeholder="1" />
      </div>
    </SectionCard>

    <!-- 运行条件 -->
    <SectionCard number="03" title="运行条件">
      <div class="form-grid-3">
        <FormField
          v-model.number="formData.temperature"
          label="运行温度 (°C)"
          type="number"
          step="0.5"
          placeholder="25"
        />
        <FormField
          v-model.number="formData.cyclesPerDay"
          label="每日循环次数"
          type="number"
          step="0.5"
          placeholder="1"
        />
        <FormField
          v-model.number="formData.dod"
          label="DOD (%)"
          type="number"
          step="1"
          min="0"
          max="100"
          placeholder="80"
        />
        <FormField
          v-model.number="formData.cRate"
          label="充放电倍率 (C)"
          type="number"
          step="0.1"
          min="0.1"
          max="2"
          placeholder="0.5"
        />
        <FormField v-model="formData.batteryType" label="电池类型" type="select" :options="batteryTypeOptions" />
      </div>
    </SectionCard>

    <!-- 仿真参数 -->
    <SectionCard number="04" title="仿真参数">
      <div class="form-grid-4">
        <FormField
          v-model.number="simParams.simulationYears"
          label="仿真年限 (年)"
          type="select"
          :options="simYearOptions"
        />
        <FormField
          v-model.number="simParams.guaranteeYears"
          label="最低保障年限 (年)"
          type="select"
          :options="guaranteeYearOptions"
        />
        <FormField
          v-model.number="simParams.guaranteeSoh"
          label="保障SOH底线 (%)"
          type="number"
          step="1"
          min="60"
          max="90"
          placeholder="70"
        />
        <FormField
          v-model.number="simParams.requiredEnergy"
          label="承诺能量底线 (MWh)"
          type="number"
          step="1"
          placeholder="100"
        />
        <FormField
          v-model.number="simParams.initRte"
          label="初始RTE (%)"
          type="number"
          step="0.1"
          min="85"
          max="95"
          placeholder="92"
        />
        <FormField
          v-model.number="simParams.acEfficiency"
          label="AC效率 (%)"
          type="number"
          step="0.1"
          min="95"
          max="99"
          placeholder="97"
        />
        <FormField
          v-model.number="simParams.dcEfficiency"
          label="DC效率 (%)"
          type="number"
          step="0.1"
          min="95"
          max="99"
          placeholder="97.5"
        />
        <FormField
          v-model.number="simParams.auxPower"
          label="自辅耗功率 (kW)"
          type="number"
          step="0.1"
          placeholder="5"
        />
      </div>
    </SectionCard>

    <!-- 操作 -->
    <div class="actions">
      <button :disabled="loading" class="btn-primary" @click="saveSurvey">
        {{ loading ? '保存中...' : '保存调研数据' }}
      </button>
      <button class="btn-secondary" @click="resetForm">重置</button>
      <button class="btn-accent" @click="goToSimulation">前往仿真分析</button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import SectionCard from '../components/SectionCard.vue'
import FormField from '../components/FormField.vue'

const router = useRouter()
const emit = defineEmits(['error'])

const loading = ref(false)
const surveyId = ref('')
const searchKeyword = ref('')
const searchResults = ref([])

const formData = reactive({
  projectName: '',
  location: '',
  ratedEnergy: 5,
  containerQty: 1,
  pcsQty: 1,
  temperature: 25,
  cyclesPerDay: 1,
  dod: 80,
  cRate: 0.5,
  batteryType: 'LFP'
})

const simParams = reactive({
  simulationYears: 25,
  guaranteeYears: 10,
  guaranteeSoh: 70,
  requiredEnergy: 100,
  initRte: 92,
  acEfficiency: 97,
  dcEfficiency: 97.5,
  auxPower: 5
})

const batteryTypeOptions = [
  { value: 'LFP', label: 'LFP (磷酸铁锂)' },
  { value: 'NCM', label: 'NCM (三元锂)' },
  { value: 'LTO', label: 'LTO (钛酸锂)' }
]

const simYearOptions = [10, 15, 20, 25, 30].map((v) => ({ value: v, label: v + '年' }))
const guaranteeYearOptions = [5, 10, 15, 20].map((v) => ({ value: v, label: v + '年' }))

async function loadSurveyById() {
  if (!surveyId.value) {
    emit('error', '请输入调研表ID', 'warning')
    return
  }
  loading.value = true
  try {
    const resp = await fetch(`/api/survey/${surveyId.value}`)
    const data = await resp.json()
    if (data.success) {
      mapSurveyData(data.data)
    } else {
      emit('error', '调研表ID不存在，请手动填写数据', 'warning')
    }
  } catch (e) {
    emit('error', '网络错误: ' + e.message, 'error')
  } finally {
    loading.value = false
  }
}

async function searchByProjectName() {
  if (!searchKeyword.value.trim()) {
    emit('error', '请输入项目名称', 'warning')
    return
  }
  loading.value = true
  try {
    const resp = await fetch(`/api/survey/search?keyword=${encodeURIComponent(searchKeyword.value)}`)
    const data = await resp.json()
    if (data.success) {
      searchResults.value = data.surveys
      if (data.surveys.length === 0) emit('error', '未找到匹配的项目', 'warning')
    }
  } catch (e) {
    emit('error', '网络错误: ' + e.message, 'error')
  } finally {
    loading.value = false
  }
}

function selectSurvey(survey) {
  searchKeyword.value = survey.project_name
  surveyId.value = survey.id
  searchResults.value = []
  mapSurveyData(survey)
}

function mapSurveyData(data) {
  formData.projectName = data.project_name || ''
  formData.ratedEnergy = data.total_mwh || 5
  formData.containerQty = data.container_qty || 1
  formData.pcsQty = data.pcs_qty || 1
  formData.temperature = data.temp_avg || 25
  formData.cyclesPerDay = data.cycles_per_day || 1
  formData.dod = data.dod || 100
  formData.cRate = data.c_rate || 0.5
  formData.batteryType = data.battery_type || 'LFP'
  formData.location = data.location || ''
}

async function saveSurvey() {
  loading.value = true
  try {
    const payload = {
      project_name: formData.projectName,
      location: formData.location,
      total_mwh: formData.ratedEnergy,
      container_qty: formData.containerQty,
      pcs_qty: formData.pcsQty,
      temp_avg: formData.temperature,
      cycles_per_day: formData.cyclesPerDay,
      dod: formData.dod,
      c_rate: formData.cRate,
      battery_type: formData.batteryType,
      simulation_years: simParams.simulationYears,
      guarantee_years: simParams.guaranteeYears,
      guarantee_soh: simParams.guaranteeSoh,
      required_energy: simParams.requiredEnergy,
      init_rte: simParams.initRte,
      ac_efficiency: simParams.acEfficiency,
      dc_efficiency: simParams.dcEfficiency,
      aux_power: simParams.auxPower
    }
    const resp = await fetch('/api/survey/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    const result = await resp.json()
    if (result.success) {
      emit('error', '调研数据保存成功', 'success')
      surveyId.value = result.data.id
    } else {
      emit('error', result.error || '保存失败', 'error')
    }
  } catch (e) {
    emit('error', '网络错误: ' + e.message, 'error')
  } finally {
    loading.value = false
  }
}

function resetForm() {
  Object.assign(formData, {
    projectName: '',
    location: '',
    ratedEnergy: 5,
    containerQty: 1,
    pcsQty: 1,
    temperature: 25,
    cyclesPerDay: 1,
    dod: 80,
    cRate: 0.5,
    batteryType: 'LFP'
  })
  Object.assign(simParams, {
    simulationYears: 25,
    guaranteeYears: 10,
    guaranteeSoh: 70,
    requiredEnergy: 100,
    initRte: 92,
    acEfficiency: 97,
    dcEfficiency: 97.5,
    auxPower: 5
  })
}

function goToSimulation() {
  router.push('/tools/simulation-view')
}
</script>

<style scoped>
.tool-page {
  padding: 24px;
  max-width: 960px;
}

.tool-header {
  margin-bottom: 24px;
}
.tool-header h1 {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 8px;
  color: var(--section-title-color);
}
.tool-header p {
  color: var(--color-text-muted);
  font-size: 14px;
  margin: 0;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 12px;
  color: var(--section-title-color);
}

.search-field-row {
  display: flex;
  align-items: flex-end;
  gap: 8px;
}
.search-field-row .form-field {
  flex: 1;
}

.btn-search-inline {
  padding: 0 14px;
  height: var(--form-field-height);
  border-radius: var(--form-field-radius);
  border: none;
  background: var(--color-accent);
  color: var(--color-text-on-accent);
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
  flex-shrink: 0;
  transition: opacity 0.2s ease;
}
.btn-search-inline:hover {
  opacity: 0.88;
}
.btn-search-inline:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.search-results {
  margin-top: 16px;
}

.results-list {
  max-height: 200px;
  overflow-y: auto;
}
.result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px solid var(--color-border);
  margin-bottom: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.result-item:hover {
  background: var(--color-accent-glow, rgba(37, 99, 235, 0.08));
  border-color: var(--color-accent);
}
.result-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-accent);
  margin: 0;
}
.result-detail {
  font-size: 11px;
  color: var(--color-text-muted);
  margin: 2px 0 0;
}
.result-action {
  font-size: 11px;
  padding: 3px 10px;
  border-radius: 6px;
  background: var(--color-accent);
  color: var(--color-text-on-accent);
}

.actions {
  display: flex;
  gap: 10px;
  margin-top: 8px;
}

.btn-primary {
  padding: 10px 24px;
  border-radius: 8px;
  border: none;
  background: var(--color-accent);
  color: var(--color-text-on-accent);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.2s;
}
.btn-primary:hover {
  opacity: 0.88;
}
.btn-primary:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.btn-secondary {
  padding: 10px 24px;
  border-radius: 8px;
  border: 1px solid var(--color-border);
  background: var(--color-card);
  color: var(--color-text-secondary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-secondary:hover {
  background: var(--color-accent-glow, rgba(37, 99, 235, 0.08));
  border-color: var(--color-accent);
}

.btn-accent {
  padding: 10px 24px;
  border-radius: 8px;
  border: none;
  background: var(--color-success);
  color: var(--color-text-on-accent);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.2s;
}
.btn-accent:hover {
  opacity: 0.85;
}
</style>
