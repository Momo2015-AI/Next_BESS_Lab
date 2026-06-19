<template>
  <div class="h-full overflow-y-auto custom-scrollbar">
    <div class="max-w-5xl mx-auto space-y-4 py-2">
      <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded bg-teal-500/20 text-teal-400 text-xs flex items-center justify-center font-bold">01</span>
          <div>
            <h3 class="font-bold text-sm text-slate-200">项目概况 <span class="text-[10px] text-slate-500 font-normal ml-1">Project Overview</span></h3>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-3">
          <div class="col-span-2">
            <label class="text-[10px] text-slate-400 block mb-1">项目名称 Project Name</label>
            <input v-model="form.projectName" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="项目名称">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">项目类型 Project Type</label>
            <select v-model="form.projectType" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- 请选择 -</option>
              <option value="utility">大型独立储能 Utility-Scale</option>
              <option value="cni">工商业储能 C&I</option>
              <option value="residential">户用储能 Residential</option>
              <option value="microgrid">微电网 Microgrid</option>
              <option value="solar-plus-bess">光伏配储 Solar+BESS</option>
              <option value="wind-plus-bess">风电配储 Wind+BESS</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">项目地点 Location</label>
            <input v-model="form.location" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="国家/地区">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">额定总功率 MW</label>
            <input v-model.number="form.totalMW" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="200">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">额定总能量 MWh</label>
            <input v-model.number="form.totalMWh" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="800">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">充放电时长 小时</label>
            <input v-model.number="form.durationHours" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="4">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">日循环次数 次/天</label>
            <input v-model.number="form.cyclesPerDay" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="1">
          </div>
        </div>
      </div>

      <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded bg-amber-500/20 text-amber-400 text-xs flex items-center justify-center font-bold">02</span>
          <div>
            <h3 class="font-bold text-sm text-slate-200">环境选址 <span class="text-[10px] text-slate-500 font-normal ml-1">Site & Environment</span></h3>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">海拔高度 米</label>
            <input v-model.number="form.altitude" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="≤2000">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">极端最高温度 °C</label>
            <input v-model.number="form.tempMax" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="45">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">极端最低温度 °C</label>
            <input v-model.number="form.tempMin" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="-20">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">年平均温度 °C</label>
            <input v-model.number="form.tempAvg" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="25">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">相对湿度 %RH</label>
            <input v-model.number="form.humidity" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="≤95">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">地震等级</label>
            <select v-model="form.seismicZone" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- -</option>
              <option value="zone1">Zone I (低)</option>
              <option value="zone2">Zone II</option>
              <option value="zone3">Zone III (中)</option>
              <option value="zone4">Zone IV (高)</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">防腐等级</label>
            <select v-model="form.corrosionClass" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- -</option>
              <option value="c1">C1 (极低)</option>
              <option value="c2">C2 (低)</option>
              <option value="c3" selected>C3 (中)</option>
              <option value="c4">C4 (高)</option>
              <option value="c5">C5 (极高)</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">安装方式</label>
            <select v-model="form.installationType" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- -</option>
              <option value="outdoor">户外 Outdoor</option>
              <option value="indoor">户内 Indoor</option>
              <option value="semi-outdoor">半户外 Semi</option>
            </select>
          </div>
        </div>
      </div>

      <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded bg-blue-500/20 text-blue-400 text-xs flex items-center justify-center font-bold">03</span>
          <div>
            <h3 class="font-bold text-sm text-slate-200">电网电气 <span class="text-[10px] text-slate-500 font-normal ml-1">Grid & Electrical</span></h3>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">并网电压等级 kV</label>
            <select v-model="form.gridVoltage" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- -</option>
              <option value="10kV">10 kV</option>
              <option value="35kV">35 kV</option>
              <option value="110kV">110 kV</option>
              <option value="220kV">220 kV</option>
              <option value="330kV">330 kV</option>
              <option value="500kV">500 kV</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">电网频率 Hz</label>
            <select v-model="form.gridFreq" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- -</option>
              <option value="50Hz">50 Hz</option>
              <option value="60Hz">60 Hz</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">短路容量 MVA</label>
            <input v-model.number="form.scCapacity" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="5000">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">中性点接地方式</label>
            <select v-model="form.neutralGrounding" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- -</option>
              <option value="solid">直接接地 Solid</option>
              <option value="resistance">经电阻接地 Resistance</option>
              <option value="arc-suppression">经消弧线圈 Arc-Suppression</option>
              <option value="ungrounded">不接地 Ungrounded</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">DC侧额定电压范围 V</label>
            <input v-model="form.dcVoltageRange" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="1000-1500">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">AC侧额定电压 V</label>
            <input v-model="form.acVoltage" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="690">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">功率因数范围</label>
            <input v-model="form.pfRange" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="0.99超前-0.99滞后">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">THDi 要求 %</label>
            <input v-model.number="form.thdiLimit" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="5">
          </div>
        </div>
      </div>

      <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded bg-purple-500/20 text-purple-400 text-xs flex items-center justify-center font-bold">04</span>
          <div>
            <h3 class="font-bold text-sm text-slate-200">系统性能 <span class="text-[10px] text-slate-500 font-normal ml-1">Performance KPIs</span></h3>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">RTE 目标 首年 %</label>
            <input v-model.number="form.rteTarget" type="number" step="0.01" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="85">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">AC可用率 目标 %</label>
            <input v-model.number="form.availabilityTarget" type="number" step="0.01" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="99">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">SOH 第1年末 %</label>
            <input v-model.number="form.sohYear1" type="number" step="0.01" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="93.2">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">SOH 第25年末 %</label>
            <input v-model.number="form.sohYear25" type="number" step="0.01" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="60">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">日历寿命 年</label>
            <input v-model.number="form.calendarLife" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="25">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">循环寿命 次</label>
            <input v-model.number="form.cycleLife" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="6000">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">辅助功耗 自耗电率 %</label>
            <input v-model.number="form.auxConsumption" type="number" step="0.01" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="5">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">响应时间 ms</label>
            <input v-model.number="form.responseTime" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="50">
          </div>
        </div>
      </div>

      <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded bg-green-500/20 text-green-400 text-xs flex items-center justify-center font-bold">05</span>
          <div>
            <h3 class="font-bold text-sm text-slate-200">文档上传 <span class="text-[10px] text-slate-500 font-normal ml-1">Auto Extract Parameters</span></h3>
          </div>
        </div>
        <p class="text-[10px] text-slate-500 mb-3">上传项目技术规范书、SLD、负荷曲线等文档，自动提取工况参数填充上方表单</p>
        <div
          class="border-2 border-dashed rounded-lg p-6 text-center transition-colors cursor-pointer"
          :class="uploadHover ? 'border-teal-500 bg-teal-500/5' : 'border-slate-700 hover:border-slate-500'"
          @dragover.prevent="uploadHover = true"
          @dragleave.prevent="uploadHover = false"
          @drop.prevent="onDrop"
          @click="triggerUpload"
        >
          <input ref="fileInput" type="file" accept=".pdf,.doc,.docx,.xls,.xlsx,.csv" class="hidden" @change="onFileChange">
          <div v-if="uploading" class="text-teal-400 text-xs">
            <div class="animate-spin w-4 h-4 border-2 border-teal-400 border-t-transparent rounded-full mx-auto mb-2"></div>
            正在解析文档...
          </div>
          <div v-else-if="uploadResult" class="text-xs">
            <span class="text-green-400 font-bold">解析完成</span>
            <span class="text-slate-500 ml-2">{{ uploadResult.fieldsExtracted }} 个字段已提取</span>
            <button @click.stop="applyExtracted" class="ml-3 text-teal-400 underline text-xs hover:text-teal-300">应用至表单</button>
            <button @click.stop="uploadResult = null" class="ml-3 text-slate-500 underline text-xs hover:text-slate-400">清除</button>
          </div>
          <div v-else>
            <div class="text-2xl mb-1 opacity-40">📄</div>
            <p class="text-xs text-slate-400">拖拽文件到此处 或 <span class="text-teal-400 underline">点击选择</span></p>
            <p class="text-[10px] text-slate-600 mt-1">支持 PDF, DOCX, XLSX, CSV</p>
          </div>
        </div>
      </div>

      <div class="text-right pb-4">
        <button @click="clearAll" class="text-xs text-slate-500 hover:text-red-400 underline mr-4">清空 Reset</button>
        <button @click="exportCSV" class="text-xs bg-slate-800 border border-slate-700 hover:border-slate-500 text-slate-300 px-4 py-1.5 rounded mr-2 transition-colors">导出 CSV</button>
        <button @click="applyToSimulation"
          class="text-xs bg-gradient-to-r from-teal-500 to-emerald-600 hover:from-teal-600 hover:to-emerald-700 text-white px-6 py-1.5 rounded shadow-md transition-all active:scale-95">
          应用至仿真引擎
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const emit = defineEmits(['applyParams'])

const form = reactive({
  projectName: '',
  projectType: '',
  location: '',
  totalMW: null,
  totalMWh: null,
  durationHours: null,
  cyclesPerDay: 1,
  altitude: null,
  tempMax: null,
  tempMin: null,
  tempAvg: null,
  humidity: null,
  seismicZone: '',
  corrosionClass: 'c3',
  installationType: '',
  gridVoltage: '',
  gridFreq: '',
  scCapacity: null,
  neutralGrounding: '',
  dcVoltageRange: '',
  acVoltage: '',
  pfRange: '',
  thdiLimit: null,
  rteTarget: null,
  availabilityTarget: null,
  sohYear1: null,
  sohYear25: null,
  calendarLife: null,
  cycleLife: null,
  auxConsumption: null,
  responseTime: null,
})

const fileInput = ref(null)
const uploadHover = ref(false)
const uploading = ref(false)
const uploadResult = ref(null)

function triggerUpload() {
  fileInput.value?.click()
}

function onFileChange(e) {
  const file = e.target.files?.[0]
  if (file) parseFile(file)
}

function onDrop(e) {
  uploadHover.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file) parseFile(file)
}

async function parseFile(file) {
  uploading.value = true
  uploadResult.value = null
  try {
    const formData = new FormData()
    formData.append('file', file)
    const resp = await fetch('/api/upload/extract', { method: 'POST', body: formData })
    const data = await resp.json()
    if (data.extracted) {
      uploadResult.value = { extracted: data.extracted, fieldsExtracted: Object.keys(data.extracted).length }
    } else {
      uploadResult.value = { extracted: {}, fieldsExtracted: 0, error: data.error || '未能提取参数' }
    }
  } catch {
    uploadResult.value = { extracted: {}, fieldsExtracted: 0, error: '解析服务不可用' }
  }
  uploading.value = false
}

function applyExtracted() {
  if (!uploadResult.value?.extracted) return
  const ext = uploadResult.value.extracted
  const mapping = {
    project_name: 'projectName', project_type: 'projectType', location: 'location',
    total_mw: 'totalMW', total_mwh: 'totalMWh', duration_h: 'durationHours',
    cycles_per_day: 'cyclesPerDay', altitude_m: 'altitude',
    temp_max_c: 'tempMax', temp_min_c: 'tempMin', temp_avg_c: 'tempAvg',
    humidity_pct: 'humidity', seismic_zone: 'seismicZone', corrosion_class: 'corrosionClass',
    installation_type: 'installationType', grid_voltage_kv: 'gridVoltage', grid_freq_hz: 'gridFreq',
    sc_capacity_mva: 'scCapacity', neutral_grounding: 'neutralGrounding',
    dc_voltage_range: 'dcVoltageRange', ac_voltage_v: 'acVoltage',
    pf_range: 'pfRange', thdi_pct: 'thdiLimit', rte_target_pct: 'rteTarget',
    availability_target_pct: 'availabilityTarget', soh_year1_pct: 'sohYear1',
    soh_year25_pct: 'sohYear25', calendar_life_y: 'calendarLife',
    cycle_life: 'cycleLife', aux_consumption_pct: 'auxConsumption', response_time_ms: 'responseTime',
  }
  for (const [k, v] of Object.entries(ext)) {
    const target = mapping[k]
    if (target && v !== null && v !== undefined) {
      const f = form[target]
      if (typeof f === 'number' || f === null) form[target] = Number(v)
      else form[target] = String(v)
    }
  }
}

function exportCSV() {
  const rows = [['Key', 'Value']]
  for (const [k, v] of Object.entries(form)) {
    rows.push([k, v ?? ''])
  }
  const csv = '\uFEFF' + rows.map(r => r.map(c => `"${String(c).replace(/"/g, '""')}"`).join(',')).join('\n')
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url; a.download = `BESS_Conditions_${form.projectName || 'Export'}.csv`
  document.body.appendChild(a); a.click(); document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

function clearAll() {
  for (const k of Object.keys(form)) {
    form[k] = typeof form[k] === 'number' || form[k] === null ? null : ''
  }
  uploadResult.value = null
}

function applyToSimulation() {
  const mapped = {
    duration: form.durationHours,
    cyclesPerDay: form.cyclesPerDay,
    requiredEnergy: form.totalMWh,
    altitude: form.altitude,
    tempMax: form.tempMax,
    tempMin: form.tempMin,
    tempAvg: form.tempAvg,
    humidity: form.humidity,
    gridVoltage: form.gridVoltage,
    rteTarget: form.rteTarget,
    availabilityTarget: form.availabilityTarget,
    projectName: form.projectName,
    projectType: form.projectType,
    location: form.location,
  }
  emit('applyParams', mapped)
}
</script>
