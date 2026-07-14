<template>
  <AppPage :title-key="'sidebar.toolSurveyViewTitle'" :desc-key="'sidebar.toolSurveyViewDesc'">
    <!-- 搜索区域 -->
    <SectionCard number="01" :title="$t('sidebar.toolSurveyView.searchTitle')">
      <div class="form-grid-2">
        <div class="search-field-row">
          <FormField
            v-model="surveyId"
            :label="$t('sidebar.toolSurveyView.idLabel')"
            type="text"
            :placeholder="$t('sidebar.toolSurveyView.idPlaceholder')"
          />
          <button :disabled="loading" class="btn-primary-sm btn-search-inline" @click="loadSurveyById">
            {{ loading ? $t('sidebar.toolSurveyView.loading') : $t('sidebar.toolSurveyView.loadBtn') }}
          </button>
        </div>
        <div class="search-field-row">
          <FormField
            v-model="searchKeyword"
            :label="$t('sidebar.toolSurveyView.nameSearchLabel')"
            type="text"
            :placeholder="$t('sidebar.toolSurveyView.nameSearchPlaceholder')"
          />
          <button :disabled="loading" class="btn-primary-sm btn-search-inline" @click="searchByProjectName">
            {{ loading ? $t('sidebar.toolSurveyView.searching') : $t('sidebar.toolSurveyView.searchBtn') }}
          </button>
        </div>
      </div>
      <div v-if="searchResults.length > 0" class="search-results mt-4">
        <h4 class="section-title">{{ $t('sidebar.toolSurveyView.searchResults') }}</h4>
        <div class="results-list">
          <div v-for="item in searchResults" :key="item.id" class="result-item" @click="selectSurvey(item)">
            <div class="result-info">
              <p class="result-name">{{ item.project_name }}</p>
              <p class="result-detail">{{ item.location }} | {{ item.total_mw }}MW / {{ item.total_mwh }}MWh</p>
            </div>
            <span class="result-action">{{ $t('sidebar.toolSurveyView.select') }}</span>
          </div>
        </div>
      </div>
    </SectionCard>

    <!-- 项目基本信息 -->
    <SectionCard number="02" :title="$t('sidebar.toolSurveyView.basicInfoTitle')">
      <div class="form-grid-3">
        <FormField
          v-model="formData.projectName"
          :label="$t('sidebar.toolSurveyView.projectName')"
          type="text"
          :placeholder="$t('sidebar.toolSurveyView.projectName')"
        />
        <FormField
          v-model="formData.location"
          :label="$t('sidebar.toolSurveyView.projectLocation')"
          type="text"
          :placeholder="$t('sidebar.toolSurveyView.projectLocation')"
        />
        <FormField
          v-model.number="formData.ratedEnergy"
          :label="$t('sidebar.toolSurveyView.ratedEnergy')"
          type="number"
          step="0.1"
          :placeholder="5"
        />
        <FormField
          v-model.number="formData.containerQty"
          :label="$t('sidebar.toolSurveyView.containerQty')"
          type="number"
          :placeholder="1"
        />
        <FormField
          v-model.number="formData.pcsQty"
          :label="$t('sidebar.toolSurveyView.pcsQty')"
          type="number"
          :placeholder="1"
        />
      </div>
    </SectionCard>

    <!-- 运行条件 -->
    <SectionCard number="03" :title="$t('sidebar.toolSurveyView.operatingConditionsTitle')">
      <div class="form-grid-3">
        <FormField
          v-model.number="formData.temperature"
          :label="$t('sidebar.toolSurveyView.temperature')"
          type="number"
          step="0.5"
          :placeholder="25"
        />
        <FormField
          v-model.number="formData.cyclesPerDay"
          :label="$t('sidebar.toolSurveyView.cyclesPerDay')"
          type="number"
          step="0.5"
          :placeholder="1"
        />
        <FormField
          v-model.number="formData.dod"
          :label="$t('sidebar.toolSurveyView.dod')"
          type="number"
          step="1"
          min="0"
          max="100"
          :placeholder="80"
        />
        <FormField
          v-model.number="formData.cRate"
          :label="$t('sidebar.toolSurveyView.cRate')"
          type="number"
          step="0.1"
          min="0.1"
          max="2"
          :placeholder="0.5"
        />
        <FormField
          v-model="formData.batteryType"
          :label="$t('sidebar.toolSurveyView.batteryType')"
          type="select"
          :options="batteryTypeOptions"
        />
      </div>
    </SectionCard>

    <!-- 仿真参数 -->
    <SectionCard number="04" :title="$t('sidebar.toolSurveyView.simulationParamsTitle')">
      <div class="form-grid-4">
        <FormField
          v-model.number="simParams.simulationYears"
          :label="$t('sidebar.toolSurveyView.simYears')"
          type="select"
          :options="simYearOptions"
        />
        <FormField
          v-model.number="simParams.guaranteeYears"
          :label="$t('sidebar.toolSurveyView.guaranteeYears')"
          type="select"
          :options="guaranteeYearOptions"
        />
        <FormField
          v-model.number="simParams.guaranteeSoh"
          :label="$t('sidebar.toolSurveyView.guaranteeSoh')"
          type="number"
          step="1"
          min="60"
          max="90"
          :placeholder="70"
        />
        <FormField
          v-model.number="simParams.requiredEnergy"
          :label="$t('sidebar.toolSurveyView.requiredEnergy')"
          type="number"
          step="1"
          :placeholder="100"
        />
        <FormField
          v-model.number="simParams.initRte"
          :label="$t('sidebar.toolSurveyView.initRte')"
          type="number"
          step="0.1"
          min="85"
          max="95"
          :placeholder="92"
        />
        <FormField
          v-model.number="simParams.acEfficiency"
          :label="$t('sidebar.toolSurveyView.acEfficiency')"
          type="number"
          step="0.1"
          min="95"
          max="99"
          :placeholder="97"
        />
        <FormField
          v-model.number="simParams.dcEfficiency"
          :label="$t('sidebar.toolSurveyView.dcEfficiency')"
          type="number"
          step="0.1"
          min="95"
          max="99"
          :placeholder="97.5"
        />
        <FormField
          v-model.number="simParams.auxPower"
          :label="$t('sidebar.toolSurveyView.auxPower')"
          type="number"
          step="0.1"
          :placeholder="5"
        />
      </div>
    </SectionCard>

    <!-- 操作 -->
    <div class="actions">
      <button :disabled="loading" class="btn-primary" @click="saveSurvey">
        {{ loading ? $t('sidebar.toolSurveyView.saving') : $t('sidebar.toolSurveyView.saveBtn') }}
      </button>
      <button class="btn-secondary" @click="resetForm">{{ $t('sidebar.toolSurveyView.resetBtn') }}</button>
      <button class="btn-accent" @click="goToSimulation">{{ $t('sidebar.toolSurveyView.goSimBtn') }}</button>
    </div>
  </AppPage>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import SectionCard from '../components/SectionCard.vue'
import FormField from '../components/FormField.vue'
import AppPage from '../components/AppPage.vue'
import api from '../services/api.js'

const router = useRouter()
const emit = defineEmits(['error'])
const { t } = useI18n()

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
  { value: 'LFP', label: t('tools.batteryTypeLFP') },
  { value: 'NCM', label: t('tools.batteryTypeNCM') },
  { value: 'LTO', label: t('tools.batteryTypeLTO') }
]

const simYearOptions = [10, 15, 20, 25, 30].map((v) => ({ value: v, label: v + t('tools.simYearUnit') }))
const guaranteeYearOptions = [5, 10, 15, 20].map((v) => ({ value: v, label: v + t('tools.yearUnit') }))

async function loadSurveyById() {
  if (!surveyId.value) {
    emit('error', t('tools.errorIdRequired'), 'warning')
    return
  }
  loading.value = true
  try {
    const data = await api.get(`/api/survey/${surveyId.value}`)
    if (data.success) {
      mapSurveyData(data.data)
    } else {
      emit('error', t('tools.errorIdNotFound'), 'warning')
    }
  } catch (e) {
    emit('error', t('tools.errorNetwork') + ': ' + e.message, 'error')
  } finally {
    loading.value = false
  }
}

async function searchByProjectName() {
  if (!searchKeyword.value.trim()) {
    emit('error', t('tools.errorNameRequired'), 'warning')
    return
  }
  loading.value = true
  try {
    const data = await api.get(`/api/survey/search?keyword=${encodeURIComponent(searchKeyword.value)}`)
    if (data.success) {
      searchResults.value = data.surveys
      if (data.surveys.length === 0) emit('error', t('tools.errorNoMatch'), 'warning')
    }
  } catch (e) {
    emit('error', t('tools.errorNetwork') + ': ' + e.message, 'error')
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
    const result = await api.post('/api/survey/create', payload)
    if (result.success) {
      emit('error', t('tools.saveSuccess'), 'success')
      surveyId.value = result.data.id
    } else {
      emit('error', result.error || t('tools.saveFailed'), 'error')
    }
  } catch (e) {
    emit('error', t('tools.errorNetwork') + ': ' + e.message, 'error')
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
.search-field-row {
  display: flex;
  align-items: flex-end;
  gap: 8px;
}
.search-field-row .form-field {
  flex: 1;
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
</style>
