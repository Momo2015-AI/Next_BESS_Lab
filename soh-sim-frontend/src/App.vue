<template>
  <div class="h-screen flex flex-col bg-slate-950 text-slate-100 p-4 gap-3 text-xs overflow-hidden">
    <!-- Toast提示 -->
    <div v-if="toast.show" 
      :class="['fixed top-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all',
        toast.type === 'success' ? 'bg-emerald-500 text-white' : 
        toast.type === 'error' ? 'bg-red-500 text-white' : 
        toast.type === 'warning' ? 'bg-amber-500 text-white' : 'bg-slate-600 text-white']">
      {{ toast.message }}
    </div>

    <header class="flex justify-between items-center border-b border-slate-800 pb-2 flex-shrink-0">
      <div>
        <h1 class="text-lg font-bold bg-gradient-to-r from-teal-400 to-sky-400 bg-clip-text text-transparent">
          储能电站 SOH 仿真计算与容量配置矩阵
        </h1>
        <p class="text-[10px] text-slate-400 mt-0.5">BESS SOH Simulation, Degradation Matrix & Augmentation Lifecycle Engine</p>
      </div>
      <button @click="fetchCalculation"
        class="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white font-bold text-xs px-4 py-1.5 rounded-md shadow-md transition-all active:scale-95 border border-emerald-400/20">
        执行仿真计算
      </button>
    </header>

    <nav class="flex bg-slate-900/60 p-1 rounded-lg gap-1 border border-slate-800/80 flex-shrink-0 overflow-x-auto">
      <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id"
        :class="['tab-btn whitespace-nowrap', { active: activeTab === tab.id }]">{{ tab.label }}</button>
    </nav>

    <div class="flex-1 min-h-0 overflow-hidden overflow-y-auto">
      <SurveyForm v-if="activeTab === 'survey'" />
      <ParameterPanel v-if="activeTab === 'param'" :params="params" @update="updateParam" @error="showToast" />
      <RunningConditions v-if="activeTab === 'conditions'" @applyParams="onApplyConditions" />
      <BatteryPCSConfig v-if="activeTab === 'batteryPCS'" @applyConfig="onApplyBatteryPCSConfig" />
      <SimulationLab v-if="activeTab === 'simulationLab'" @applyConfig="onApplySimulationConfig" />
      <ProductConfig v-if="activeTab === 'products'" @applyConfig="onApplyConfig" />
      <FinancialDashboard v-if="activeTab === 'financial'" :params="params" :results="results" :soh="soh" :augQty="augQty" />
      <MatrixTable v-if="activeTab === 'matrix'" :results="results" :params="params" :soh="soh" :rte="rte" :dod="dod" :augQty="augQty"
        @update:soh="soh = $event" @update:rte="rte = $event" @update:dod="dod = $event" @update:augQty="augQty = $event" />
      <DataInjection v-if="activeTab === 'inject'" :soh="soh" :rte="rte" @update:soh="soh = $event" @update:rte="rte = $event" />
      <FormulaLab v-if="activeTab === 'formula'" :params="params" @update="updateParam" />
      <SohChart v-if="activeTab === 'chart'" :results="results" :soh="soh" :rte="rte" :required-energy="params.requiredEnergy" />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import ParameterPanel from './components/ParameterPanel.vue'
import MatrixTable from './components/MatrixTable.vue'
import DataInjection from './components/DataInjection.vue'
import FormulaLab from './components/FormulaLab.vue'
import SohChart from './components/SohChart.vue'
import RunningConditions from './components/RunningConditions.vue'
import ProductConfig from './components/ProductConfig.vue'
import FinancialDashboard from './components/FinancialDashboard.vue'
import BatteryPCSConfig from './components/BatteryPCSConfig.vue'
import SimulationLab from './components/SimulationLab.vue'
import SurveyForm from './components/SurveyForm.vue'

// Toast提示
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

const activeTab = ref('survey')
const tabs = [
  { id: 'survey', label: '0. 项目调研表' },
  { id: 'param', label: '1. 参数配置面板' },
  { id: 'conditions', label: '2. 运行工况' },
  { id: 'batteryPCS', label: '3. 电池与PCS配对' },
  { id: 'simulationLab', label: '4. 仿真实验室' },
  { id: 'products', label: '5. 产品与方案配置' },
  { id: 'financial', label: '6. 财务看板' },
  { id: 'matrix', label: '7. 25年生命周期矩阵' },
  { id: 'inject', label: '8. SOH/RTE 数据注入' },
  { id: 'formula', label: '9. 算法公式实验舱' },
  { id: 'chart', label: '10. 可视化图表' },
]

const N = 26

const params = reactive({
  ratedEnergy: 5,
  initContainerQty: 62,
  initPcsQty: 1,
  duration: 2,
  cyclesPerDay: 1,
  acEfficiency: 97.03,
  bessAuxRun: 18.124,
  bessAuxStandby: 3.5,
  pcsAuxRun: 6.5,
  pcsAuxStandby: 1.0,
  requiredEnergy: 240,
})

const soh = ref([
  0.9925, 0.9318, 0.9014, 0.877, 0.856, 0.8371, 0.8197, 0.8036, 0.7885, 0.7742,
  0.7606, 0.7475, 0.735, 0.723, 0.7113, 0.7, 0.689, 0.678, 0.6672, 0.6564,
  0.6458, 0.6354, 0.6252, 0.6152, 0.6074, 0.6008,
])

const rte = ref([
  0.941, 0.9384, 0.9372, 0.9363, 0.9355, 0.9347, 0.934, 0.9333, 0.9326, 0.932,
  0.9314, 0.9308, 0.9302, 0.9296, 0.929, 0.9285, 0.9279, 0.9273, 0.9268, 0.9262,
  0.9256, 0.9251, 0.9245, 0.924, 0.9235, 0.923,
])

const dod = ref(new Array(N).fill(100))
const augQty = ref(new Array(N).fill(0))
augQty.value[6] = 6

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
  const cycleContainerAuxPerUnit = dailyContainerAuxPerUnit / p.cyclesPerDay
  const cyclePcsAuxPerUnit = dailyPcsAuxPerUnit / p.cyclesPerDay
  const acEff = p.acEfficiency / 100

  let accumAugQty = 0
  for (let i = 0; i < N; i++) {
    accumAugQty += Number(augQty.value[i]) || 0
    results.augAccumQty[i] = accumAugQty

    const cDod = (Number(dod.value[i]) || 0) / 100
    const cRte = Number(rte.value[i]) || 0
    const cSoh = Number(soh.value[i]) || 0

    results.initGross[i] = p.ratedEnergy * p.initContainerQty * cDod * cRte * cSoh * acEff
    results.initAux[i] = p.initContainerQty * cycleContainerAuxPerUnit + p.initPcsQty * cyclePcsAuxPerUnit
    results.initAcUsable[i] = Math.max(0, results.initGross[i] - results.initAux[i])

    let totalAugAc = 0
    let totalAugAux = 0
    for (let k = 0; k <= i; k++) {
      const qtyK = Number(augQty.value[k]) || 0
      if (qtyK > 0) {
        const age = i - k
        const assetSoh = Number(soh.value[Math.min(age, N - 1)]) || 0
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
    calculate()
    if (activeTab.value !== 'matrix') activeTab.value = 'matrix'
  }
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
  if (payload.initContainerQty != null) params.initContainerQty = payload.initContainerQty
  if (payload.initPcsQty != null) params.initPcsQty = payload.initPcsQty
  if (payload.duration != null) params.duration = payload.duration
  if (payload.acEfficiency != null) params.acEfficiency = payload.acEfficiency
  showToast('电池与PCS配置已应用', 'success')
  if (activeTab.value !== 'simulationLab') activeTab.value = 'simulationLab'
}

function onApplySimulationConfig(payload) {
  // 仿真实验室的配置应用到主参数
  Object.keys(payload).forEach(key => {
    if (payload[key] != null && params[key] !== undefined) {
      params[key] = payload[key]
    }
  })
  showToast('仿真参数已应用', 'success')
}

calculate()
</script>
