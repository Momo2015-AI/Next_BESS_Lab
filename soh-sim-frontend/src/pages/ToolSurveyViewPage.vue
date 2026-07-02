<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>调研输入</h1>
      <p>录入或搜索项目调研数据，作为仿真计算的输入参数</p>
    </div>

    <div class="search-section">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-xs mb-1 field-label">调研表串码ID</label>
          <div class="flex gap-2">
            <input v-model="surveyId" type="text" placeholder="输入调研表ID" class="form-input" />
            <button :disabled="loading" class="btn-primary btn-sm" @click="loadSurveyById">
              {{ loading ? '加载中...' : '加载' }}
            </button>
          </div>
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">项目名称搜索</label>
          <div class="flex gap-2">
            <input v-model="searchKeyword" type="text" placeholder="输入项目名称搜索" class="form-input" />
            <button :disabled="loading" class="btn-primary btn-sm" @click="searchByProjectName">
              {{ loading ? '搜索中...' : '搜索' }}
            </button>
          </div>
        </div>
      </div>

      <div v-if="searchResults.length > 0" class="search-results mt-4">
        <h4 class="text-xs font-medium mb-2 section-title">搜索结果</h4>
        <div class="results-list">
          <div v-for="item in searchResults" :key="item.id" class="result-item" @click="selectSurvey(item)">
            <div class="result-info">
              <p class="result-name">
                {{ item.project_name }}
              </p>
              <p class="result-detail">{{ item.location }} | {{ item.total_mw }}MW / {{ item.total_mwh }}MWh</p>
            </div>
            <span class="result-action">选择</span>
          </div>
        </div>
      </div>
    </div>

    <div class="form-section">
      <h3 class="section-title">项目基本信息</h3>
      <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-xs mb-1 field-label">项目名称</label>
          <input v-model="formData.projectName" type="text" class="form-input" placeholder="项目名称" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">项目地点</label>
          <input v-model="formData.location" type="text" class="form-input" placeholder="项目地点" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">额定能量 (MWh)</label>
          <input v-model.number="formData.ratedEnergy" type="number" step="0.1" class="form-input" placeholder="5" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">集装箱数量</label>
          <input v-model.number="formData.containerQty" type="number" class="form-input" placeholder="1" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">PCS数量</label>
          <input v-model.number="formData.pcsQty" type="number" class="form-input" placeholder="1" />
        </div>
      </div>
    </div>

    <div class="form-section">
      <h3 class="section-title">运行条件</h3>
      <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-xs mb-1 field-label">运行温度 (°C)</label>
          <input v-model.number="formData.temperature" type="number" step="0.5" class="form-input" placeholder="25" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">每日循环次数</label>
          <input v-model.number="formData.cyclesPerDay" type="number" step="0.5" class="form-input" placeholder="1" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">DOD (%)</label>
          <input
            v-model.number="formData.dod"
            type="number"
            step="1"
            min="0"
            max="100"
            class="form-input"
            placeholder="80"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">充放电倍率 (C)</label>
          <input
            v-model.number="formData.cRate"
            type="number"
            step="0.1"
            min="0.1"
            max="2"
            class="form-input"
            placeholder="0.5"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">电池类型</label>
          <select v-model="formData.batteryType" class="form-input">
            <option value="LFP">LFP (磷酸铁锂)</option>
            <option value="NCM">NCM (三元锂)</option>
            <option value="LTO">LTO (钛酸锂)</option>
          </select>
        </div>
      </div>
    </div>

    <div class="form-section">
      <h3 class="section-title">仿真参数</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-xs mb-1 field-label">仿真年限 (年)</label>
          <select v-model.number="simParams.simulationYears" class="form-input">
            <option value="10">10年</option>
            <option value="15">15年</option>
            <option value="20">20年</option>
            <option value="25">25年</option>
            <option value="30">30年</option>
          </select>
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">最低保障年限 (年)</label>
          <select v-model.number="simParams.guaranteeYears" class="form-input">
            <option value="5">5年</option>
            <option value="10">10年</option>
            <option value="15">15年</option>
            <option value="20">20年</option>
          </select>
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">保障SOH底线 (%)</label>
          <input
            v-model.number="simParams.guaranteeSoh"
            type="number"
            step="1"
            min="60"
            max="90"
            class="form-input"
            placeholder="70"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">承诺能量底线 (MWh)</label>
          <input
            v-model.number="simParams.requiredEnergy"
            type="number"
            step="1"
            class="form-input"
            placeholder="100"
          />
        </div>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
        <div>
          <label class="block text-xs mb-1 field-label">初始RTE (%)</label>
          <input
            v-model.number="simParams.initRte"
            type="number"
            step="0.1"
            min="85"
            max="95"
            class="form-input"
            placeholder="92"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">AC效率 (%)</label>
          <input
            v-model.number="simParams.acEfficiency"
            type="number"
            step="0.1"
            min="95"
            max="99"
            class="form-input"
            placeholder="97"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">DC效率 (%)</label>
          <input
            v-model.number="simParams.dcEfficiency"
            type="number"
            step="0.1"
            min="95"
            max="99"
            class="form-input"
            placeholder="97.5"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">自辅耗功率 (kW)</label>
          <input v-model.number="simParams.auxPower" type="number" step="0.1" class="form-input" placeholder="5" />
        </div>
      </div>
    </div>

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
      if (data.surveys.length === 0) {
        emit('error', '未找到匹配的项目', 'warning')
      }
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
}
.tool-header p {
  color: var(--text-secondary, #666);
  font-size: 14px;
  margin: 0;
}

.field-label {
  color: #999;
}

.form-input {
  width: 100%;
  padding: 6px 10px;
  border: 1px solid var(--color-input-border);
  border-radius: 6px;
  font-size: 13px;
  outline: none;
  transition: border-color 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.form-input:focus {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 2px var(--color-accent-glow);
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 12px;
}

.search-section,
.form-section {
  background: var(--color-card);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid var(--color-border);
  margin-bottom: 16px;
}

.results-list {
  max-height: 200px;
  overflow-y: auto;
}

.result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  border-radius: 6px;
  border: 1px solid var(--color-border);
  margin-bottom: 6px;
  cursor: pointer;
  transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.result-item:hover {
  background: var(--color-accent-glow);
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
  padding: 2px 8px;
  border-radius: 4px;
  background: var(--color-accent);
  color: white;
}

.btn-primary {
  padding: 8px 20px;
  border-radius: 6px;
  background: var(--color-accent);
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
  padding: 8px 20px;
  border-radius: 6px;
  background: var(--color-card);
  color: var(--color-text-secondary);
  border: 1px solid var(--color-input-border);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.btn-secondary:hover {
  background: var(--color-accent-glow);
}

.btn-accent {
  padding: 8px 20px;
  border-radius: 6px;
  background: var(--color-success);
  color: white;
  border: none;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.btn-accent:hover {
  background: var(--color-success);
  opacity: 0.85;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
  white-space: nowrap;
}

.actions {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}
</style>
