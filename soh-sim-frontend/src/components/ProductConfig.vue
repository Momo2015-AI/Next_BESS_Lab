<template>
  <div class="h-full overflow-y-auto custom-scrollbar">
    <div class="max-w-6xl mx-auto space-y-4 py-2">

      <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded bg-teal-500/20 text-teal-400 text-xs flex items-center justify-center font-bold">A</span>
          <div>
            <h3 class="font-bold text-sm text-slate-200">电芯选型库 <span class="text-[10px] text-slate-500 font-normal ml-1">Battery Cell Library</span></h3>
          </div>
          <div class="ml-auto flex gap-2">
            <select v-model="cellFilter" class="text-xs bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-300 focus:border-teal-500 focus:outline-none">
              <option value="">全部厂商</option>
              <option v-for="m in mfrList.cells" :key="m" :value="m">{{ m }}</option>
            </select>
          </div>
        </div>
        <div class="grid grid-cols-3 gap-2">
          <div v-for="cell in filteredCells" :key="cell.id"
            @click="selectedCell = cell.id"
            :class="['border rounded-lg p-3 cursor-pointer transition-all', selectedCell === cell.id ? 'border-teal-500 bg-teal-500/10 shadow-lg shadow-teal-500/10' : 'border-slate-800 hover:border-slate-600 bg-slate-800/40']">
            <div class="flex justify-between items-start mb-1">
              <span class="text-xs font-bold text-slate-200">{{ cell.model }}</span>
              <span :class="['text-[10px] px-1.5 py-0.5 rounded', cell.status === 'mass-production' ? 'bg-green-500/20 text-green-400' : 'bg-amber-500/20 text-amber-400']">{{ cell.status === 'mass-production' ? '量产' : '预研' }}</span>
            </div>
            <div class="text-[10px] text-slate-500 mb-2">{{ cell.mfr }}</div>
            <div class="grid grid-cols-2 gap-x-2 gap-y-0.5 text-[10px]">
              <div class="text-slate-500">容量</div><div class="text-slate-300 text-right">{{ cell.capacityAh }} Ah</div>
              <div class="text-slate-500">标压</div><div class="text-slate-300 text-right">{{ cell.voltageNominal }} V</div>
              <div class="text-slate-500">能量</div><div class="text-slate-300 text-right">{{ cell.energyWh }} Wh</div>
              <div class="text-slate-500">循环</div><div class="text-slate-300 text-right">{{ cell.cycleLife }}+</div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded bg-amber-500/20 text-amber-400 text-xs flex items-center justify-center font-bold">B</span>
          <div>
            <h3 class="font-bold text-sm text-slate-200">集装箱库 <span class="text-[10px] text-slate-500 font-normal ml-1">Container Library</span></h3>
          </div>
          <div class="ml-auto flex gap-2">
            <select v-model="containerFilter" class="text-xs bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-300 focus:border-teal-500 focus:outline-none">
              <option value="">全部厂商</option>
              <option v-for="m in mfrList.containers" :key="m" :value="m">{{ m }}</option>
            </select>
          </div>
        </div>
        <div class="grid grid-cols-3 gap-2">
          <div v-for="c in filteredContainers" :key="c.id"
            @click="selectedContainer = c.id"
            :class="['border rounded-lg p-3 cursor-pointer transition-all', selectedContainer === c.id ? 'border-amber-500 bg-amber-500/10 shadow-lg shadow-amber-500/10' : 'border-slate-800 hover:border-slate-600 bg-slate-800/40']">
            <div class="flex justify-between items-start mb-1">
              <span class="text-xs font-bold text-slate-200">{{ c.model }}</span>
              <span :class="['text-[10px] px-1.5 py-0.5 rounded', c.status === 'mass-production' ? 'bg-green-500/20 text-green-400' : 'bg-amber-500/20 text-amber-400']">{{ c.status === 'mass-production' ? '量产' : '预研' }}</span>
            </div>
            <div class="text-[10px] text-slate-500 mb-2">{{ c.mfr }}</div>
            <div class="grid grid-cols-2 gap-x-2 gap-y-0.5 text-[10px]">
              <div class="text-slate-500">能量</div><div class="text-slate-300 text-right">{{ c.ratedEnergyMWh }} MWh</div>
              <div class="text-slate-500">功率</div><div class="text-slate-300 text-right">{{ c.ratedPowerMW }} MW</div>
              <div class="text-slate-500">电芯</div><div class="text-slate-300 text-right">{{ c.cellModel }}</div>
              <div class="text-slate-500">散热</div><div class="text-slate-300 text-right">{{ c.cooling }}</div>
              <div class="text-slate-500">规格</div><div class="text-slate-300 text-right">{{ c.type }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded bg-blue-500/20 text-blue-400 text-xs flex items-center justify-center font-bold">C</span>
          <div>
            <h3 class="font-bold text-sm text-slate-200">PCS 变流器库 <span class="text-[10px] text-slate-500 font-normal ml-1">PCS Library</span></h3>
          </div>
          <div class="ml-auto flex gap-2">
            <select v-model="pcsFilter" class="text-xs bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-300 focus:border-teal-500 focus:outline-none">
              <option value="">全部厂商</option>
              <option v-for="m in mfrList.pcs" :key="m" :value="m">{{ m }}</option>
            </select>
            <select v-model="pcsPowerFilter" class="text-xs bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-300 focus:border-teal-500 focus:outline-none">
              <option value="0">全部功率</option>
              <option value="1.25">1.25 MW</option>
              <option value="1.725">1.725 MW</option>
              <option value="2.5">2.5 MW</option>
              <option value="3.45">3.45 MW</option>
            </select>
          </div>
        </div>
        <div class="grid grid-cols-3 gap-2">
          <div v-for="p in filteredPcs" :key="p.id"
            @click="selectedPcs = p.id"
            :class="['border rounded-lg p-3 cursor-pointer transition-all', selectedPcs === p.id ? 'border-blue-500 bg-blue-500/10 shadow-lg shadow-blue-500/10' : 'border-slate-800 hover:border-slate-600 bg-slate-800/40']">
            <div class="flex justify-between items-start mb-1">
              <span class="text-xs font-bold text-slate-200">{{ p.model }}</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-green-500/20 text-green-400">量产</span>
            </div>
            <div class="text-[10px] text-slate-500 mb-2">{{ p.mfr }}</div>
            <div class="grid grid-cols-2 gap-x-2 gap-y-0.5 text-[10px]">
              <div class="text-slate-500">功率</div><div class="text-slate-300 text-right">{{ p.ratedPowerMW }} MW</div>
              <div class="text-slate-500">容量</div><div class="text-slate-300 text-right">{{ p.ratedPowerKVA }} kVA</div>
              <div class="text-slate-500">效率</div><div class="text-slate-300 text-right">{{ p.efficiency }}%</div>
              <div class="text-slate-500">AC电压</div><div class="text-slate-300 text-right">{{ p.acVoltage }}</div>
              <div class="text-slate-500">DC范围</div><div class="text-slate-300 text-right">{{ p.dcVoltageRange }}</div>
              <div class="text-slate-500">散热</div><div class="text-slate-300 text-right">{{ p.cooling }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded bg-purple-500/20 text-purple-400 text-xs flex items-center justify-center font-bold">D</span>
          <div>
            <h3 class="font-bold text-sm text-slate-200">典型场景方案 Template <span class="text-[10px] text-slate-500 font-normal ml-1">Scenario Templates</span></h3>
          </div>
        </div>
        <div class="grid grid-cols-5 gap-2 mb-4">
          <div v-for="s in scenarios" :key="s.id"
            @click="applyScenario(s)"
            :class="['border rounded-lg p-3 cursor-pointer transition-all text-center', selectedScenario === s.id ? 'border-purple-500 bg-purple-500/10' : 'border-slate-800 hover:border-slate-600 bg-slate-800/40']">
            <div class="text-xs font-bold text-slate-200 mb-1">{{ s.name }}</div>
            <div class="text-[10px] text-slate-500 leading-relaxed">{{ s.description }}</div>
          </div>
        </div>

        <div v-if="configSummary" class="border-t border-slate-800 pt-3">
          <h4 class="text-xs font-bold text-slate-300 mb-2">当前方案摘要 Current Selection</h4>
          <div class="grid grid-cols-3 gap-3 text-[10px]">
            <div class="bg-slate-800/60 rounded p-2">
              <span class="text-slate-500">电芯</span>
              <div class="text-slate-200 font-mono mt-0.5">{{ configSummary.cell || '未选择' }}</div>
            </div>
            <div class="bg-slate-800/60 rounded p-2">
              <span class="text-slate-500">集装箱</span>
              <div class="text-slate-200 font-mono mt-0.5">{{ configSummary.container || '未选择' }}</div>
            </div>
            <div class="bg-slate-800/60 rounded p-2">
              <span class="text-slate-500">PCS</span>
              <div class="text-slate-200 font-mono mt-0.5">{{ configSummary.pcs || '未选择' }}</div>
            </div>
          </div>
          <div class="mt-3 flex justify-end">
            <button @click="applyToSimulation"
              class="text-xs bg-gradient-to-r from-teal-500 to-emerald-600 hover:from-teal-600 hover:to-emerald-700 text-white px-6 py-1.5 rounded shadow-md transition-all active:scale-95">
              应用至仿真参数 Apply to Simulation
            </button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import products from '../data/products.json'

const emit = defineEmits(['applyConfig'])

const selectedCell = ref('eve-lf628k')
const selectedContainer = ref('eve-5mwh-lf628k')
const selectedPcs = ref('nari-2500kw')
const selectedScenario = ref(null)

const cellFilter = ref('')
const containerFilter = ref('')
const pcsFilter = ref('')
const pcsPowerFilter = ref('0')

const mfrList = computed(() => ({
  cells: [...new Set(products.cells.map(c => c.mfr))],
  containers: [...new Set(products.containers.map(c => c.mfr))],
  pcs: [...new Set(products.pcs.map(p => p.mfr))],
}))

const scenarios = products.scenarios

const filteredCells = computed(() => {
  let list = products.cells
  if (cellFilter.value) list = list.filter(c => c.mfr === cellFilter.value)
  return list
})

const filteredContainers = computed(() => {
  let list = products.containers
  if (containerFilter.value) list = list.filter(c => c.mfr === containerFilter.value)
  return list
})

const filteredPcs = computed(() => {
  let list = products.pcs
  if (pcsFilter.value) list = list.filter(p => p.mfr === pcsFilter.value)
  if (pcsPowerFilter.value !== '0') list = list.filter(p => p.ratedPowerMW === Number(pcsPowerFilter.value))
  return list
})

const configSummary = computed(() => {
  const cell = products.cells.find(c => c.id === selectedCell.value)
  const container = products.containers.find(c => c.id === selectedContainer.value)
  const pcs = products.pcs.find(p => p.id === selectedPcs.value)
  return {
    cell: cell ? `${cell.mfr} ${cell.model} (${cell.capacityAh}Ah)` : null,
    container: container ? `${container.mfr} ${container.model} (${container.ratedEnergyMWh}MWh)` : null,
    pcs: pcs ? `${pcs.mfr} ${pcs.model} (${pcs.ratedPowerMW}MW)` : null,
  }
})

function applyScenario(s) {
  selectedScenario.value = s.id
  emit('applyConfig', {
    duration: s.duration,
    requiredEnergy: s.requiredEnergy,
    initContainerQty: s.initContainerQty,
    initPcsQty: s.initPcsQty,
    ratedEnergy: s.ratedEnergy,
    scenario: s.name,
  })
}

function applyToSimulation() {
  const cell = products.cells.find(c => c.id === selectedCell.value)
  const container = products.containers.find(c => c.id === selectedContainer.value)
  const pcs = products.pcs.find(p => p.id === selectedPcs.value)
  const payload = { cell, container, pcs }
  if (container) {
    payload.ratedEnergy = container.ratedEnergyMWh
    payload.acEfficiency = pcs ? pcs.efficiency : 97.03
  }
  emit('applyConfig', payload)
}
</script>
