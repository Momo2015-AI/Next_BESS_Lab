<template>
  <div class="h-screen flex flex-col overflow-hidden" style="background-color: #F5F7FA;">
    <div v-if="toast.show" class="fixed top-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all"
      :style="toast.type === 'success' ? { backgroundColor: '#10b981', color: 'white' } :
              toast.type === 'error' ? { backgroundColor: '#ef4444', color: 'white' } :
              toast.type === 'warning' ? { backgroundColor: '#f59e0b', color: 'white' } :
              { backgroundColor: '#666666', color: 'white' }">
      {{ toast.message }}
    </div>

    <header class="flex justify-between items-center flex-shrink-0 z-10" 
      style="background-color: #FFFFFF; border-bottom: 1px solid #E0E0E0; padding: 10px 20px;">
      <div class="flex items-center gap-4">
        <button @click="navigateTo('home')" class="flex items-center gap-2 cursor-pointer">
          <div class="w-8 h-8 rounded-lg flex items-center justify-center" style="background-color: #2F5496; color: white;">
            <span class="text-sm font-bold">S</span>
          </div>
          <span class="font-bold text-sm hidden sm:block" style="color: #2F5496;">SOH-SIM</span>
        </button>
        <nav class="hidden md:flex items-center gap-1 ml-4">
          <button 
            @click="navigateTo('foundation')"
            class="px-4 py-2 text-sm font-medium rounded-lg transition-all"
            :class="isFoundationTab ? 'nav-active' : 'nav-item'">
            {{ $t('app.foundation') }}
          </button>
          <button 
            @click="navigateTo('solution')"
            class="px-4 py-2 text-sm font-medium rounded-lg transition-all"
            :class="isSolutionTab ? 'nav-active' : 'nav-item'">
            {{ $t('app.solution') }}
          </button>
        </nav>
      </div>
      <div class="flex items-center gap-3">
      </div>
    </header>

    <div class="flex flex-1 overflow-hidden">
      <Sidebar :active-tab="activeTab" @navigate="navigateTo" />

      <main class="flex-1 overflow-auto">
        <div class="min-h-full p-6">
          <HomePage v-show="activeTab === 'home'" @navigate="navigateTo" />
          <SurveyForm v-show="activeTab === 'survey'" @error="showToast" />
          <ParameterPanel v-show="activeTab === 'param'" :params="params" @update="updateParam" @error="showToast" />
          <RunningConditions v-show="activeTab === 'conditions'" @applyParams="onApplyConditions" @error="showToast" />
          <BatteryDCDesign v-show="activeTab === 'dc-design'" ref="batteryDC" @apply-config="onApplyBatteryConfig" @error="showToast" />
          <PcsACDesign v-show="activeTab === 'ac-design'" ref="pcsAC" @apply-config="onApplyPcsConfig" @error="showToast" />
          <BatteryPCSConfig v-show="activeTab === 'batteryPCS'" :active="activeTab === 'batteryPCS'" :params="params" @applyConfig="onApplyBatteryPCSConfig" @error="showToast" />
          <SimulationLab v-show="activeTab === 'simulationLab'" @applyConfig="onApplySimulationConfig" @error="showToast" />
          <ProductConfig v-show="activeTab === 'products'" @applyConfig="onApplyConfig" @error="showToast" />
          <FinancialDashboard v-show="activeTab === 'financial'" :params="params" :results="results" :soh="soh" :augQty="augQty" />
          <MatrixTable v-show="activeTab === 'matrix'" :results="results" :params="params" :soh="soh" :rte="rte" :dod="dod" :augQty="augQty"
            @update:soh="soh = $event; syncParamsToDb()" @update:rte="rte = $event; syncParamsToDb()" @update:dod="dod = $event; syncParamsToDb()" @update:augQty="augQty = $event; syncParamsToDb()"
            @update:param="handleParamUpdate" @recalculate="fetchCalculation" />
          <DataInjection v-show="activeTab === 'inject'" :soh="soh" :rte="rte" @update:soh="soh = $event" @update:rte="rte = $event" />
          <FormulaLab v-show="activeTab === 'formula'" :params="params" @update="updateParam" />
          <SohChart v-show="activeTab === 'chart'" :results="results" :soh="soh" :rte="rte" :required-energy="params.requiredEnergy" />
          <ScenarioCompare v-show="activeTab === 'scenario'" :base-params="params" @error="showToast" />
          <SensitivityAnalysis v-show="activeTab === 'sensitivity'" :params="params" :financial="financialData" @error="showToast" />
          <EngineeringCalc v-show="activeTab === 'engineering'" @error="showToast" />
          <AuxPowerCalculator v-show="activeTab === 'auxPower'" @error="showToast" />
          <DataExport v-show="activeTab === 'export'" :params="params" :results="results" :soh="soh" :rte="rte" :dod="dod" :aug-qty="augQty" :financial="financialData" :project-id="currentProjectId" />
          <AuthPanel v-show="activeTab === 'auth'" @auth-success="onAuthSuccess" @error="showToast" />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import Sidebar from './components/Sidebar.vue'
import HomePage from './components/HomePage.vue'
import ParameterPanel from './components/ParameterPanel.vue'
import MatrixTable from './components/MatrixTable.vue'
import DataInjection from './components/DataInjection.vue'
import FormulaLab from './components/FormulaLab.vue'
import SohChart from './components/SohChart.vue'
import RunningConditions from './components/RunningConditions.vue'
import ProductConfig from './components/ProductConfig.vue'
import FinancialDashboard from './components/FinancialDashboard.vue'
import BatteryDCDesign from './components/BatteryDCDesign.vue'
import PcsACDesign from './components/PcsACDesign.vue'
import BatteryPCSConfig from './components/BatteryPCSConfig.vue'
import SimulationLab from './components/SimulationLab.vue'
import DataExport from './components/DataExport.vue'
import ScenarioCompare from './components/ScenarioCompare.vue'
import SensitivityAnalysis from './components/SensitivityAnalysis.vue'
import EngineeringCalc from './components/EngineeringCalc.vue'
import AuthPanel from './components/AuthPanel.vue'
import SurveyForm from './components/SurveyForm.vue'
import AuxPowerCalculator from './components/AuxPowerCalculator.vue'
import { useDraft, setupBeforeUnloadGuard } from './composables/useDraft'

const batteryDC = ref(null)
const pcsAC = ref(null)
const router = useRouter()
const { t } = useI18n()

const toast = reactive({
  show: false,
  message: '',
  type: 'info',
})

const showToast = (message, type = 'info') => {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => {
    toast.show = false
  }, 3000)
}

const activeTab = ref('home')

const foundationTabs = ['survey', 'param', 'conditions', 'products', 'batteryPCS', 'formula']
const solutionTabs = ['dc-design', 'ac-design', 'simulationLab', 'financial', 'matrix', 'inject', 'chart', 'scenario', 'sensitivity', 'engineering', 'auxPower', 'export']

const isFoundationTab = computed(() => foundationTabs.includes(activeTab.value))
const isSolutionTab = computed(() => solutionTabs.includes(activeTab.value))

function navigateTo(tab) {
  if (tab === 'foundation') {
    activeTab.value = 'param'
  } else if (tab === 'solution') {
    activeTab.value = 'dc-design'
  } else {
    activeTab.value = tab
  }
}

const N = 26

const params = useDraft('app-params', {
  ratedEnergy: 5,
  initContainerQty: 10,
  initPcsQty: 2,
  pcsPower: 5,
  duration: 2,
  cyclesPerDay: 1,
  temperature: 25,
  acEfficiency: 97.03,
  bessAuxRun: 18.124,
  bessAuxStandby: 3.5,
  pcsAuxRun: 6.5,
  pcsAuxStandby: 1.0,
  requiredEnergy: 240,
}).state

const soh = useDraftRef('app-soh', [
  0.9925, 0.9318, 0.9014, 0.877, 0.856, 0.8371, 0.8197, 0.8036, 0.7885, 0.7742,
  0.7606, 0.7475, 0.735, 0.723, 0.7113, 0.7, 0.689, 0.678, 0.6672, 0.6564,
  0.6458, 0.6354, 0.6252, 0.6152, 0.6074, 0.6008,
]).state

const rte = useDraftRef('app-rte', [
  0.941, 0.9384, 0.9372, 0.9363, 0.9355, 0.9347, 0.934, 0.9333, 0.9326, 0.932,
  0.9314, 0.9308, 0.9302, 0.9296, 0.929, 0.9285, 0.9279, 0.9273, 0.9268, 0.9262,
  0.9256, 0.9251, 0.9245, 0.924, 0.9235, 0.923,
]).state

const dod = useDraftRef('app-dod', new Array(N).fill(100)).state

const augQtyDraft = useDraftRef('app-aug-qty', (function () {
  const arr = new Array(N).fill(0)
  arr[6] = 6
  return arr
})())
const augQty = augQtyDraft.state

const results = reactive({
  initGross: new Array(N).fill(0),
  initAux: new Array(N).fill(0),
  initAcUsable: new Array(N).fill(0),
  augGross: new Array(N).fill(0),
  augAux: new Array(N).fill(0),
  augAcUsable: new Array(N).fill(0),
  augAccumQty: new Array(N).fill(0),
  totalAcUsable: new Array(N).fill(0),
  meetsReq: new Array(N).fill(false),
  acRteNoAux: 0,
  acRteWithAux: 0,
})

function updateParam(key, value) {
  params[key] = value
}

watch(params, () => calculate(), { deep: true })
watch(soh, () => calculate(), { deep: true })
watch(rte, () => calculate(), { deep: true })
watch(dod, () => calculate(), { deep: true })
watch(augQty, () => calculate(), { deep: true })

function calculate() {
  const p = params
  const runHours = p.duration * p.cyclesPerDay
  const standbyHours = Math.max(0, 24 - runHours)
  const dailyContainerAuxPerUnit = (p.bessAuxRun * runHours + p.bessAuxStandby * standbyHours) / 1000
  const dailyPcsAuxPerUnit = (p.pcsAuxRun * runHours + p.pcsAuxStandby * standbyHours) / 1000
  const safeCycles = Math.max(p.cyclesPerDay, 0.001)
  const cycleContainerAuxPerUnit = dailyContainerAuxPerUnit / safeCycles
  const cyclePcsAuxPerUnit = dailyPcsAuxPerUnit / safeCycles
  const acEff = p.acEfficiency / 100

  let accumAugQty = 0
  for (let i = 0; i < N; i++) {
    accumAugQty += Number(augQty.value[i]) || 0
    results.augAccumQty[i] = accumAugQty

    const cDod = ((Number(dod.value[i]) || 0) / 100) || 1.0
    const cRte = Number.isFinite(Number(rte.value[i])) ? Number(rte.value[i]) : 0.94
    const cSoh = Number.isFinite(Number(soh.value[i])) ? Number(soh.value[i]) : 1.0

    results.initGross[i] = p.ratedEnergy * p.initContainerQty * cDod * cRte * cSoh * acEff
    results.initAux[i] = p.initContainerQty * cycleContainerAuxPerUnit + p.initPcsQty * cyclePcsAuxPerUnit
    results.initAcUsable[i] = Math.max(0, results.initGross[i] - results.initAux[i])

    let totalAugAc = 0
    let totalAugAux = 0
    for (let k = 0; k <= i; k++) {
      const qtyK = Number(augQty.value[k]) || 0
      if (qtyK > 0) {
        const age = i - k
        const assetSoh = Number.isFinite(Number(soh.value[Math.min(age, N - 1)])) ? Number(soh.value[Math.min(age, N - 1)]) : 1.0
        const assetGross = p.ratedEnergy * qtyK * cDod * cRte * assetSoh * acEff
        const assetAux = qtyK * cycleContainerAuxPerUnit
        totalAugAc += Math.max(0, assetGross - assetAux)
        totalAugAux += assetAux
      }
    }
    results.augGross[i] = totalAugAc + totalAugAux
    results.augAux[i] = totalAugAux
    results.augAcUsable[i] = totalAugAc
    results.totalAcUsable[i] = results.initAcUsable[i] + totalAugAc
    results.meetsReq[i] = results.totalAcUsable[i] >= p.requiredEnergy
  }

  const rteYear1 = Number.isFinite(Number(rte.value[0])) ? Number(rte.value[0]) : 0.94
  results.acRteNoAux = +(rteYear1 * acEff * 100).toFixed(2)
  const gross0 = results.initGross[0]
  const aux0 = results.initAux[0]
  const auxRatio = gross0 > 0 ? aux0 / gross0 : 0.05
  results.acRteWithAux = +(rteYear1 * acEff * (1 - auxRatio) * 100).toFixed(2)
}

async function fetchCalculation() {
  try {
    const resp = await fetch('/api/soh/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        params: { ...params },
        soh: soh.value,
        rte: rte.value,
        dod: dod.value,
        augQty: augQty.value,
      }),
    })
    const data = await resp.json()
    if (data.results) {
      Object.assign(results, data.results)
    }
    if (activeTab.value !== 'matrix') activeTab.value = 'matrix'
  } catch (error) {
    console.error('API调用失败，使用本地计算:', error)
    showToast('API 调用失败，已使用本地计算', 'warning')
    calculate()
    if (activeTab.value !== 'matrix') activeTab.value = 'matrix'
  }
}

function handleParamUpdate(key, value) {
  params[key] = value
  syncParamsToDb()
}

let syncTimer = null
async function syncParamsToDb() {
  if (syncTimer) clearTimeout(syncTimer)
  syncTimer = setTimeout(async () => {
    try {
      await fetch('/api/project/sync-params', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          params: { ...params },
          soh: soh.value,
          rte: rte.value,
          dod: dod.value,
          augQty: augQty.value,
          project_id: currentProjectId.value,
        }),
      })
    } catch (error) {
      console.error('同步参数到数据库失败:', error)
    }
  }, 500)
}

function onApplyConditions(mapped) {
  if (mapped.duration != null) params.duration = mapped.duration
  if (mapped.cyclesPerDay != null) params.cyclesPerDay = mapped.cyclesPerDay
  if (mapped.requiredEnergy != null) params.requiredEnergy = mapped.requiredEnergy
}

function onApplyConfig(payload) {
  if (payload.duration != null) params.duration = payload.duration
  if (payload.requiredEnergy != null) params.requiredEnergy = payload.requiredEnergy
  if (payload.initContainerQty != null) params.initContainerQty = payload.initContainerQty
  if (payload.initPcsQty != null) params.initPcsQty = payload.initPcsQty
  if (payload.ratedEnergy != null) params.ratedEnergy = payload.ratedEnergy
  if (payload.acEfficiency != null) params.acEfficiency = payload.acEfficiency
  showToast('配置已应用', 'success')
}

function onApplyBatteryPCSConfig(payload) {
  if (payload.ratedEnergy != null) params.ratedEnergy = payload.ratedEnergy
  if (payload.containerQty != null) params.initContainerQty = payload.containerQty
  if (payload.pcsQty != null) params.initPcsQty = payload.pcsQty
  if (payload.duration != null) params.duration = payload.duration
  if (payload.cyclesPerDay != null) params.cyclesPerDay = payload.cyclesPerDay
  showToast('电池PCS配置已应用', 'success')
}

function onApplyBatteryConfig(payload) {
  if (payload.ratedEnergy != null) params.ratedEnergy = payload.ratedEnergy
  if (payload.containerQty != null) params.initContainerQty = payload.containerQty
  if (payload.dod != null) dod.value = new Array(N).fill(payload.dod)
  if (payload.cyclesPerDay != null) params.cyclesPerDay = payload.cyclesPerDay
  if (payload.temperature != null) params.temperature = payload.temperature
  showToast('直流侧配置已应用', 'success')
  if (pcsAC.value) {
    pcsAC.value.setBatteryConfig({
      totalEnergy: params.ratedEnergy,
      containerQty: params.initContainerQty,
    })
  }
}

function onApplyPcsConfig(payload) {
  if (payload.pcsQty != null) params.initPcsQty = payload.pcsQty
  if (payload.totalPcsPower != null) params.pcsPower = payload.totalPcsPower
  if (payload.acEfficiency != null) params.acEfficiency = payload.acEfficiency
  if (payload.pcsAuxRun != null) params.pcsAuxRun = payload.pcsAuxRun
  if (payload.pcsAuxStandby != null) params.pcsAuxStandby = payload.pcsAuxStandby
  showToast('交流侧配置已应用', 'success')
}

function onApplySimulationConfig(payload) {
  Object.keys(payload).forEach(key => {
    if (payload[key] != null && params[key] !== undefined) {
      params[key] = payload[key]
    }
  })
  const sohData = payload.sohCurve || payload.soh
  const rteData = payload.rteCurve || payload.rte
  if (sohData && Array.isArray(sohData)) {
    soh.value = sohData
    if (payload.source === 'simulation' && activeTab.value !== 'inject') {
      activeTab.value = 'inject'
    }
  }
  if (rteData && Array.isArray(rteData)) {
    rte.value = rteData
  }
  showToast(payload.source === 'simulation'
    ? '仿真结果已自动填入数据注入面板'
    : '仿真参数已应用', 'success')
}

const currentProjectId = ref('')

const financialData = reactive({
  totalRevenue: 0,
  totalCost: 0,
  netCashflow: 0,
  npv: 0,
  irr: 0,
  paybackYears: 0,
  lcos: 0,
})

function onAuthSuccess(user) {
  showToast(`欢迎 ${user.username}`, 'success')
}

function loadSurveyData() {
  try {
    const currentSurvey = localStorage.getItem('currentSurvey')
    if (currentSurvey) {
      const survey = JSON.parse(currentSurvey)
      if (survey.ratedEnergy) params.ratedEnergy = survey.ratedEnergy
      if (survey.containerQty) params.initContainerQty = survey.containerQty
      if (survey.pcsQty) params.initPcsQty = survey.pcsQty
      if (survey.dischargeHours) params.duration = survey.dischargeHours
      if (survey.cyclesPerDay) params.cyclesPerDay = survey.cyclesPerDay
      if (survey.dod) dod.value = new Array(N).fill(survey.dod)
      if (survey.temperature) params.temperature = survey.temperature
      if (survey.guaranteeYears) params.guaranteeYears = survey.guaranteeYears
      currentProjectId.value = survey.id || ''
      showToast(`已加载调研表: ${survey.projectName}`, 'info')
    }
  } catch (e) {
    console.error('加载调研表失败:', e)
  }
}

onMounted(() => {
  setupBeforeUnloadGuard()
  loadSurveyData()
  calculate()
})
</script>

<style scoped>
.nav-item {
  color: #666666;
}

.nav-item:hover {
  background-color: #F5F7FA;
  color: #2F5496;
}

.nav-active {
  background-color: #E8EEF5;
  color: #2F5496;
}

.oracle-btn-primary {
  background-color: #2F5496;
  color: white;
  font-weight: 600;
  padding: 6px 14px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.oracle-btn-primary:hover {
  background-color: #4A7BC4;
  box-shadow: 0 2px 8px rgba(47, 84, 150, 0.3);
}
</style>
