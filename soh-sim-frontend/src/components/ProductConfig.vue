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
              <option v-for="m in localMfrList('cells')" :key="m" :value="m">{{ m }}</option>
            </select>
            <button @click="openAddModal('cell')" class="text-[10px] bg-teal-600/30 hover:bg-teal-600/60 text-teal-300 border border-teal-500/30 px-2 py-1 rounded transition-colors">+ 新增电芯</button>
          </div>
        </div>
        <div class="grid grid-cols-3 gap-2">
          <div v-for="cell in localFiltered('cells', cellFilter)" :key="cell.id"
            @click="selectedCell = cell.id"
            :class="['border rounded-lg p-3 cursor-pointer transition-all group relative', selectedCell === cell.id ? 'border-teal-500 bg-teal-500/10 shadow-lg shadow-teal-500/10' : 'border-slate-800 hover:border-slate-600 bg-slate-800/40']">
            <button @click.stop="deleteItem('cells', cell.id)" class="absolute top-1 right-1 text-slate-600 hover:text-red-400 text-xs opacity-0 group-hover:opacity-100 transition-opacity">&times;</button>
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
              <option v-for="m in localMfrList('containers')" :key="m" :value="m">{{ m }}</option>
            </select>
            <button @click="openAddModal('container')" class="text-[10px] bg-amber-600/30 hover:bg-amber-600/60 text-amber-300 border border-amber-500/30 px-2 py-1 rounded transition-colors">+ 新增集装箱</button>
          </div>
        </div>
        <div class="grid grid-cols-3 gap-2">
          <div v-for="c in localFiltered('containers', containerFilter)" :key="c.id"
            @click="selectedContainer = c.id"
            :class="['border rounded-lg p-3 cursor-pointer transition-all group relative', selectedContainer === c.id ? 'border-amber-500 bg-amber-500/10 shadow-lg shadow-amber-500/10' : 'border-slate-800 hover:border-slate-600 bg-slate-800/40']">
            <button @click.stop="deleteItem('containers', c.id)" class="absolute top-1 right-1 text-slate-600 hover:text-red-400 text-xs opacity-0 group-hover:opacity-100 transition-opacity">&times;</button>
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
              <option v-for="m in localMfrList('pcs')" :key="m" :value="m">{{ m }}</option>
            </select>
            <select v-model="pcsPowerFilter" class="text-xs bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-300 focus:border-teal-500 focus:outline-none">
              <option value="0">全部功率</option>
              <option value="1.25">1.25 MW</option>
              <option value="1.725">1.725 MW</option>
              <option value="2.5">2.5 MW</option>
              <option value="3.45">3.45 MW</option>
            </select>
            <button @click="openAddModal('pcs')" class="text-[10px] bg-blue-600/30 hover:bg-blue-600/60 text-blue-300 border border-blue-500/30 px-2 py-1 rounded transition-colors">+ 新增 PCS</button>
          </div>
        </div>
        <div class="grid grid-cols-3 gap-2">
          <div v-for="p in localFiltered('pcs', pcsFilter, pcsPowerFilter)" :key="p.id"
            @click="selectedPcs = p.id"
            :class="['border rounded-lg p-3 cursor-pointer transition-all group relative', selectedPcs === p.id ? 'border-blue-500 bg-blue-500/10 shadow-lg shadow-blue-500/10' : 'border-slate-800 hover:border-slate-600 bg-slate-800/40']">
            <button @click.stop="deleteItem('pcs', p.id)" class="absolute top-1 right-1 text-slate-600 hover:text-red-400 text-xs opacity-0 group-hover:opacity-100 transition-opacity">&times;</button>
            <div class="flex justify-between items-start mb-1">
              <span class="text-xs font-bold text-slate-200">{{ p.model }}</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-green-500/20 text-green-400">量产</span>
            </div>
            <div class="text-[10px] text-slate-500 mb-2">{{ p.mfr }}</div>
            <div class="grid grid-cols-2 gap-x-2 gap-y-0.5 text-[10px]">
              <div class="text-slate-500">功率</div><div class="text-slate-300 text-right">{{ p.ratedPowerMW }} MW</div>
              <div class="text-slate-500">效率</div><div class="text-slate-300 text-right">{{ p.efficiency }}%</div>
              <div class="text-slate-500">AC电压</div><div class="text-slate-300 text-right">{{ p.acVoltage }}</div>
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

      <div v-if="showModal" class="fixed inset-0 bg-black/60 z-50 flex items-center justify-center" @click.self="showModal = false">
        <div class="bg-slate-900 border border-slate-700 rounded-xl p-5 w-[480px] max-h-[80vh] overflow-y-auto shadow-2xl">
          <h3 class="font-bold text-sm text-slate-200 mb-4">{{ modalTitle }}</h3>
          <div class="space-y-3">
            <template v-if="modalType === 'cell'">
              <div class="grid grid-cols-2 gap-2 text-[10px]">
                <div><label class="text-slate-500 block mb-0.5">厂商</label><input v-model="modalForm.mfr" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
                <div><label class="text-slate-500 block mb-0.5">型号</label><input v-model="modalForm.model" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
                <div><label class="text-slate-500 block mb-0.5">化学体系</label><input v-model="modalForm.chemistry" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
                <div><label class="text-slate-500 block mb-0.5">容量 Ah</label><input v-model.number="modalForm.capacityAh" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
                <div><label class="text-slate-500 block mb-0.5">标称电压 V</label><input v-model.number="modalForm.voltageNominal" type="number" step="0.1" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
                <div><label class="text-slate-500 block mb-0.5">循环寿命</label><input v-model.number="modalForm.cycleLife" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
                <div><label class="text-slate-500 block mb-0.5">尺寸</label><input v-model="modalForm.dimensions" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
                <div><label class="text-slate-500 block mb-0.5">重量 kg</label><input v-model="modalForm.weight" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
              </div>
            </template>
            <template v-else-if="modalType === 'container'">
              <div class="grid grid-cols-2 gap-2 text-[10px]">
                <div><label class="text-slate-500 block mb-0.5">厂商</label><input v-model="modalForm.mfr" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
                <div><label class="text-slate-500 block mb-0.5">型号</label><input v-model="modalForm.model" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
                <div><label class="text-slate-500 block mb-0.5">额定能量 MWh</label><input v-model.number="modalForm.ratedEnergyMWh" type="number" step="0.001" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
                <div><label class="text-slate-500 block mb-0.5">额定功率 MW</label><input v-model.number="modalForm.ratedPowerMW" type="number" step="0.001" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
                <div><label class="text-slate-500 block mb-0.5">电芯型号</label><input v-model="modalForm.cellModel" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
                <div><label class="text-slate-500 block mb-0.5">散热方式</label><input v-model="modalForm.cooling" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
                <div><label class="text-slate-500 block mb-0.5">尺寸</label><input v-model="modalForm.dimensions" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
                <div><label class="text-slate-500 block mb-0.5">重量 t</label><input v-model="modalForm.weight" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
              </div>
            </template>
            <template v-else-if="modalType === 'pcs'">
              <div class="grid grid-cols-2 gap-2 text-[10px]">
                <div><label class="text-slate-500 block mb-0.5">厂商</label><input v-model="modalForm.mfr" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
                <div><label class="text-slate-500 block mb-0.5">型号</label><input v-model="modalForm.model" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
                <div><label class="text-slate-500 block mb-0.5">额定功率 MW</label><input v-model.number="modalForm.ratedPowerMW" type="number" step="0.001" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
                <div><label class="text-slate-500 block mb-0.5">效率 %</label><input v-model.number="modalForm.efficiency" type="number" step="0.1" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
                <div><label class="text-slate-500 block mb-0.5">AC电压</label><input v-model="modalForm.acVoltage" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
                <div><label class="text-slate-500 block mb-0.5">DC范围</label><input v-model="modalForm.dcVoltageRange" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
                <div><label class="text-slate-500 block mb-0.5">散热</label><input v-model="modalForm.cooling" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-slate-200 text-xs focus:border-teal-500 focus:outline-none"></div>
              </div>
            </template>

            <div class="border-t border-slate-800 pt-3">
              <p class="text-[10px] text-slate-500 mb-2">或上传规格书自动提取 (支持 PDF/CSV)</p>
              <div class="flex gap-2 text-[10px]">
                <input ref="specInput" type="file" accept=".pdf,.csv,.xlsx,.xls" class="hidden" @change="onSpecUpload">
                <button @click="$refs.specInput.click()" class="bg-slate-800 border border-slate-700 hover:border-slate-500 text-slate-300 px-3 py-1.5 rounded transition-colors">
                  上传规格书
                </button>
                <span v-if="specUploading" class="text-teal-400 self-center">解析中...</span>
                <span v-if="specResult" class="text-emerald-400 self-center">{{ specResult }}</span>
              </div>
            </div>
          </div>
          <div class="flex justify-end gap-2 mt-4 pt-3 border-t border-slate-800">
            <button @click="showModal = false" class="text-xs text-slate-500 hover:text-slate-300 px-3 py-1.5">取消</button>
            <button @click="saveProduct" class="text-xs bg-teal-600 hover:bg-teal-700 text-white px-4 py-1.5 rounded transition-colors">保存</button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import baseProducts from '../data/products.json'

const emit = defineEmits(['applyConfig'])

const selectedCell = ref('eve-lf628k')
const selectedContainer = ref('eve-5mwh-lf628k')
const selectedPcs = ref('nari-2500kw')
const selectedScenario = ref(null)

const cellFilter = ref('')
const containerFilter = ref('')
const pcsFilter = ref('')
const pcsPowerFilter = ref('0')

const localData = ref(JSON.parse(JSON.stringify(baseProducts)))

function localMfrList(key) {
  return [...new Set(localData.value[key]?.map(c => c.mfr) || [])]
}

function localFiltered(key, mfrFilter, powerFilter) {
  let list = localData.value[key] || []
  if (mfrFilter) list = list.filter(c => c.mfr === mfrFilter)
  if (key === 'pcs' && powerFilter && powerFilter !== '0') {
    list = list.filter(p => p.ratedPowerMW === Number(powerFilter))
  }
  return list
}

function deleteItem(key, id) {
  localData.value[key] = localData.value[key].filter(item => item.id !== id)
  saveLocal()
}

const showModal = ref(false)
const modalType = ref('cell')
const modalForm = ref({})
const specInput = ref(null)
const specUploading = ref(false)
const specResult = ref('')

function openAddModal(type) {
  modalType.value = type
  showModal.value = true
  specResult.value = ''
  if (type === 'cell') {
    modalForm.value = { mfr: '', model: '', chemistry: 'LFP', capacityAh: '', voltageNominal: 3.2, cycleLife: '', dimensions: '', weight: '', status: 'mass-production' }
  } else if (type === 'container') {
    modalForm.value = { mfr: '', model: '', ratedEnergyMWh: '', ratedPowerMW: '', cellModel: '', cooling: '', dimensions: '', weight: '', status: 'mass-production' }
  } else {
    modalForm.value = { mfr: '', model: '', ratedPowerMW: '', efficiency: '', acVoltage: '', dcVoltageRange: '', cooling: '', status: 'mass-production' }
  }
}

function saveProduct() {
  const type = modalType.value
  const f = modalForm.value
  const id = type + '-' + f.model?.toLowerCase().replace(/\s+/g, '-') + '-' + Date.now().toString(36)
  let item = { id, ...f }

  if (type === 'cell') {
    item.energyWh = (f.capacityAh || 0) * (f.voltageNominal || 3.2)
    item.voltageRange = '2.5-3.65'
    item.sohCurve = 'default'
  } else if (type === 'container') {
    item.type = '20ft Standard'
    item.cycleLife = 8000
  } else if (type === 'pcs') {
    item.ratedPowerKVA = (f.ratedPowerMW || 0) * 1040
    item.topology = '3-Level NPC'
    item.isolation = 'Transformerless'
  }

  if (!localData.value[type + 's']) {
    localData.value[type + 's'] = []
  }
  localData.value[type + 's'].push(item)
  saveLocal()
  showModal.value = false
}

async function onSpecUpload(e) {
  const file = e.target.files?.[0]
  if (!file) return
  specUploading.value = true
  specResult.value = ''
  try {
    const formData = new FormData()
    formData.append('file', file)
    const resp = await fetch('/api/upload/extract', { method: 'POST', body: formData })
    const data = await resp.json()
    if (data.extracted) {
      const ext = data.extracted
      if (modalType.value === 'cell') {
        if (ext.capacity_ah || ext.total_mwh) modalForm.value.capacityAh = ext.capacity_ah || ext.total_mwh
        if (ext.cycle_life) modalForm.value.cycleLife = ext.cycle_life
      }
      specResult.value = '已提取 ' + Object.keys(ext).length + ' 个字段'
    } else {
      specResult.value = '未能自动提取，请手动填写'
    }
  } catch { specResult.value = '上传失败' }
  specUploading.value = false
}

function saveLocal() {
  if (typeof localStorage === 'undefined') return
  try { localStorage.setItem('soh-products', JSON.stringify(localData.value)) } catch(e) {}
}

try {
  if (typeof localStorage !== 'undefined') {
    const saved = localStorage.getItem('soh-products')
    if (saved) {
      const parsed = JSON.parse(saved)
      localData.value = { ...baseProducts, ...parsed }
    }
  }
} catch(e) {}

const mfrList = computed(() => ({
  cells: localMfrList('cells'),
  containers: localMfrList('containers'),
  pcs: localMfrList('pcs'),
}))

const scenarios = baseProducts.scenarios

const filteredCells = computed(() => localFiltered('cells', cellFilter.value))
const filteredContainers = computed(() => localFiltered('containers', containerFilter.value))
const filteredPcs = computed(() => localFiltered('pcs', pcsFilter.value, pcsPowerFilter.value))

const configSummary = computed(() => {
  const cell = localData.value.cells?.find(c => c.id === selectedCell.value)
  const container = localData.value.containers?.find(c => c.id === selectedContainer.value)
  const pcs = localData.value.pcs?.find(p => p.id === selectedPcs.value)
  return {
    cell: cell ? `${cell.mfr} ${cell.model} (${cell.capacityAh}Ah)` : null,
    container: container ? `${container.mfr} ${container.model} (${container.ratedEnergyMWh}MWh)` : null,
    pcs: pcs ? `${pcs.mfr} ${pcs.model} (${pcs.ratedPowerMW}MW)` : null,
  }
})

function applyScenario(s) {
  selectedScenario.value = s.id
  emit('applyConfig', {
    duration: s.duration, requiredEnergy: s.requiredEnergy,
    initContainerQty: s.initContainerQty, initPcsQty: s.initPcsQty,
    ratedEnergy: s.ratedEnergy, scenario: s.name,
  })
}

function applyToSimulation() {
  const cell = localData.value.cells?.find(c => c.id === selectedCell.value)
  const container = localData.value.containers?.find(c => c.id === selectedContainer.value)
  const pcs = localData.value.pcs?.find(p => p.id === selectedPcs.value)
  const payload = { cell, container, pcs }
  if (container) {
    payload.ratedEnergy = container.ratedEnergyMWh
    payload.acEfficiency = pcs ? pcs.efficiency : 97.03
  }
  emit('applyConfig', payload)
}
</script>
