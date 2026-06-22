<template>
  <div class="flex flex-col gap-4 h-full overflow-auto p-4">
    <div class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
      <h3 class="text-sm font-bold mb-3 flex items-center gap-2" style="color: var(--color-accent-secondary);">
        <span class="w-2 h-2 rounded-full" style="background-color: var(--color-accent-secondary);"></span>
        电池集装箱配置
      </h3>

      <div class="grid grid-cols-4 gap-4">
        <div class="rounded p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <label class="text-xs block mb-2" style="color: var(--color-text-muted);">储能集装箱型号</label>
          <select v-model="selectedContainer" @change="calculatePCS"
            class="w-full rounded px-3 py-2 text-xs"
            style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
            onfocus="this.style.borderColor='var(--color-accent-secondary)'; this.style.outline='none';"
            onblur="this.style.borderColor='var(--color-input-border)';">
            <option value="">请选择集装箱型号</option>
            <option v-for="container in containers" :key="container.id" :value="container.id">
              {{ container.name }} - {{ container.energy }}MWh / {{ container.power }}MW
            </option>
          </select>
        </div>

        <div class="rounded p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <label class="text-xs block mb-2" style="color: var(--color-text-muted);">集装箱数量</label>
          <input v-model.number="containerQty" @change="calculatePCS" type="number" min="1" max="100"
            class="w-full rounded px-3 py-2 text-xs"
            style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
            onfocus="this.style.borderColor='var(--color-accent-secondary)'; this.style.outline='none';"
            onblur="this.style.borderColor='var(--color-input-border)';">
        </div>

        <div class="rounded p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <label class="text-xs block mb-2" style="color: var(--color-text-muted);">运行时长 (h)</label>
          <input v-model.number="durationHours" @change="calculatePCS" type="number" min="0.5" max="8" step="0.5"
            class="w-full rounded px-3 py-2 text-xs"
            style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
            onfocus="this.style.borderColor='var(--color-accent-secondary)'; this.style.outline='none';"
            onblur="this.style.borderColor='var(--color-input-border)';">
          <p class="text-[10px] mt-1" style="color: var(--color-text-muted);">C-rate = 1/时长, PCS功率 = 能量/时长</p>
        </div>

        <div class="rounded p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <label class="text-xs block mb-2" style="color: var(--color-text-muted);">PCS型号</label>
          <select v-model="selectedPCS" @change="calculatePCS"
            class="w-full rounded px-3 py-2 text-xs"
            style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
            onfocus="this.style.borderColor='var(--color-accent-secondary)'; this.style.outline='none';"
            onblur="this.style.borderColor='var(--color-input-border)';">
            <option value="">请选择PCS型号</option>
            <option v-for="pcs in pcsList" :key="pcs.id" :value="pcs.id">
              {{ pcs.name }} - {{ pcs.power }}MW / {{ pcs.voltage }}V
            </option>
          </select>
        </div>
      </div>

      <div class="mt-4 p-4 rounded-lg" style="background-color: var(--color-accent-glow); border: 1px solid var(--color-accent-dark);">
        <h4 class="text-xs font-bold mb-3" style="color: var(--color-accent-secondary);">自动计算结果</h4>
        <div class="grid grid-cols-4 gap-3">
          <div class="text-center">
            <p class="text-[10px]" style="color: var(--color-text-muted);">总能量</p>
            <p class="text-lg font-bold" style="color: var(--color-accent-secondary);">{{ totalEnergy.toFixed(1) }} MWh</p>
          </div>
          <div class="text-center">
            <p class="text-[10px]" style="color: var(--color-text-muted);">总功率</p>
            <p class="text-lg font-bold" style="color: var(--color-accent);">{{ totalPower.toFixed(1) }} MW</p>
          </div>
          <div class="text-center">
            <p class="text-[10px]" style="color: var(--color-text-muted);">PCS数量</p>
            <p class="text-lg font-bold" style="color: var(--color-success);">{{ pcsQty }} 台</p>
          </div>
          <div class="text-center">
            <p class="text-[10px]" style="color: var(--color-text-muted);">配比方式</p>
            <p class="text-lg font-bold" style="color: var(--color-warning);">{{ pairingMode }}</p>
          </div>
        </div>

        <div class="mt-3 text-[10px]" style="color: var(--color-text-muted);">
          <p><strong style="color: var(--color-text-secondary);">配比说明：</strong>{{ pairingDescription }}</p>
        </div>
      </div>
    </div>

    <div class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
      <h3 class="text-sm font-bold mb-3 flex items-center gap-2" style="color: var(--color-accent-secondary);">
        <span class="w-2 h-2 rounded-full" style="background-color: var(--color-accent-secondary);"></span>
        系统连接图
      </h3>

      <div ref="connectionDiagram" class="h-64 rounded" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);"></div>

      <div class="mt-3 flex gap-4 text-[10px]">
        <div class="flex items-center gap-1">
          <span class="w-3 h-3 rounded" style="background-color: var(--color-accent-secondary);"></span>
          <span style="color: var(--color-text-muted);">电池集装箱</span>
        </div>
        <div class="flex items-center gap-1">
          <span class="w-3 h-3 rounded" style="background-color: var(--color-accent);"></span>
          <span style="color: var(--color-text-muted);">PCS</span>
        </div>
        <div class="flex items-center gap-1">
          <span class="w-3 h-3 rounded" style="background-color: var(--color-warning);"></span>
          <span style="color: var(--color-text-muted);">变压器</span>
        </div>
        <div class="flex items-center gap-1">
          <span class="w-3 h-3 rounded" style="background-color: var(--color-success);"></span>
          <span style="color: var(--color-text-muted);">电网</span>
        </div>
        <div class="flex items-center gap-1">
          <span class="w-2 h-0.5" style="background-color: var(--color-text-muted);"></span>
          <span style="color: var(--color-text-muted);">DC连接</span>
        </div>
        <div class="flex items-center gap-1">
          <span class="w-2 h-0.5" style="background-color: var(--color-warning);"></span>
          <span style="color: var(--color-text-muted);">AC连接</span>
        </div>
      </div>
    </div>

    <div class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
      <h3 class="text-sm font-bold mb-3 flex items-center gap-2" style="color: var(--color-accent-secondary);">
        <span class="w-2 h-2 rounded-full" style="background-color: var(--color-accent-secondary);"></span>
        电气单线图
      </h3>

      <div ref="singleLineDiagram" class="h-80 rounded" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);"></div>

      <div class="mt-3 grid grid-cols-5 gap-2 text-[10px]">
        <div class="rounded p-2" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <p style="color: var(--color-text-muted);">DC电压范围</p>
          <p class="font-bold" style="color: var(--color-accent-secondary);">{{ dcVoltageRange }}</p>
        </div>
        <div class="rounded p-2" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <p style="color: var(--color-text-muted);">AC输出电压</p>
          <p class="font-bold" style="color: var(--color-accent);">{{ acVoltage }}</p>
        </div>
        <div class="rounded p-2" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <p style="color: var(--color-text-muted);">额定频率</p>
          <p class="font-bold" style="color: var(--color-warning);">50 Hz</p>
        </div>
        <div class="rounded p-2" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <p style="color: var(--color-text-muted);">短路容量</p>
          <p class="font-bold" style="color: var(--color-success);">{{ shortCircuitCapacity }}</p>
        </div>
        <div class="rounded p-2" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <p style="color: var(--color-text-muted);">接地方式</p>
          <p class="font-bold" style="color: var(--color-accent-secondary);">TN-S</p>
        </div>
      </div>
    </div>

    <div class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
      <h3 class="text-sm font-bold mb-3 flex items-center gap-2" style="color: var(--color-accent-secondary);">
        <span class="w-2 h-2 rounded-full" style="background-color: var(--color-accent-secondary);"></span>
        推荐配对方案
      </h3>

      <div class="overflow-auto">
        <table class="w-full text-xs">
          <thead style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border);">
            <tr>
              <th class="py-2 px-3 text-left">方案编号</th>
              <th class="py-2 px-3 text-left">集装箱配置</th>
              <th class="py-2 px-3 text-left">PCS配置</th>
              <th class="py-2 px-3 text-left">配比方式</th>
              <th class="py-2 px-3 text-left">能量/功率比</th>
              <th class="py-2 px-3 text-left">效率预估</th>
              <th class="py-2 px-3 text-left">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(scheme, idx) in recommendedSchemes" :key="idx" 
              style="border-bottom: 1px solid var(--color-border);"
              onmouseover="this.style.backgroundColor='var(--color-card-dark)';"
              onmouseout="this.style.backgroundColor='transparent';">
              <td class="py-2 px-3" style="color: var(--color-text-muted);">{{ scheme.id }}</td>
              <td class="py-2 px-3" style="color: var(--color-accent-secondary);">{{ scheme.containerConfig }}</td>
              <td class="py-2 px-3" style="color: var(--color-accent);">{{ scheme.pcsConfig }}</td>
              <td class="py-2 px-3" style="color: var(--color-warning);">{{ scheme.pairingMode }}</td>
              <td class="py-2 px-3" style="color: var(--color-success);">{{ scheme.energyPowerRatio }}</td>
              <td class="py-2 px-3" style="color: var(--color-accent-secondary);">{{ scheme.efficiency }}%</td>
              <td class="py-2 px-3">
                <button @click="applyScheme(scheme)"
                  class="text-[10px] px-2 py-1 rounded transition-all"
                  style="background-color: var(--color-accent-glow); color: var(--color-accent-secondary);"
                  onmouseover="this.style.backgroundColor='var(--color-accent-dark)';"
                  onmouseout="this.style.backgroundColor='var(--color-accent-glow)';">
                  应用
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="flex justify-end gap-3">
      <button @click="resetConfig" class="text-xs px-4 py-2 rounded transition-colors"
        style="background-color: var(--color-card-dark); border: 1px solid var(--color-border); color: var(--color-text-secondary);"
        onmouseover="this.style.borderColor='var(--color-accent)';"
        onmouseout="this.style.borderColor='var(--color-border)';">
        重置配置
      </button>
      <button @click="applyConfig" class="text-xs px-6 py-2 rounded font-bold transition-colors"
        style="background-color: var(--color-accent-secondary); color: white;"
        onmouseover="this.style.opacity='0.9';"
        onmouseout="this.style.opacity='1';">
        应用到仿真参数
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick, watch } from 'vue'
import * as echarts from 'echarts'

const emit = defineEmits(['applyConfig', 'error'])

const containers = ref([])
const pcsList = ref([])

async function loadLibraryData() {
  try {
    const [containersRes, pcsRes] = await Promise.all([
      fetch('/api/library/containers'),
      fetch('/api/library/pcs')
    ])
    
    const [containersData, pcsData] = await Promise.all([
      containersRes.json(),
      pcsRes.json()
    ])
    
    if (containersData.success) {
      containers.value = containersData.data.map(c => ({
        id: c.id,
        name: c.model,
        energy: c.ratedEnergyMWh,
        power: c.ratedPowerMW,
        voltage: 600,
        cells: c.seriesCount * c.parallelCount || 120,
        ...c
      }))
    }
    
    if (pcsData.success) {
      pcsList.value = pcsData.data.map(p => ({
        id: p.id,
        name: p.model,
        power: p.ratedPowerMW,
        voltage: 380,
        dcVoltage: p.dcVoltageRange,
        efficiency: p.efficiency,
        ...p
      }))
    }
    
    if (containers.value.length === 0 || pcsList.value.length === 0) {
      await seedLibrary()
    }
  } catch (error) {
    console.error('加载产品库失败:', error)
    containers.value = [
      { id: 'container-5mwh', name: '5MWh标准舱', energy: 5, power: 2.5, voltage: 600, cells: 120 },
      { id: 'container-3mwh', name: '3MWh紧凑舱', energy: 3, power: 1.5, voltage: 600, cells: 72 },
      { id: 'container-10mwh', name: '10MWh大容量舱', energy: 10, power: 5, voltage: 800, cells: 240 },
      { id: 'container-2mwh', name: '2MWh小型舱', energy: 2, power: 1, voltage: 400, cells: 48 },
    ]
    pcsList.value = [
      { id: 'pcs-2mw', name: '2MW PCS', power: 2, voltage: 380, dcVoltage: '600-900V', efficiency: 98 },
      { id: 'pcs-1mw', name: '1MW PCS', power: 1, voltage: 380, dcVoltage: '400-600V', efficiency: 97 },
      { id: 'pcs-5mw', name: '5MW PCS', power: 5, voltage: 380, dcVoltage: '800-1200V', efficiency: 98.5 },
      { id: 'pcs-500kw', name: '500kW PCS', power: 0.5, voltage: 380, dcVoltage: '300-500V', efficiency: 96 },
    ]
  }
}

async function seedLibrary() {
  try {
    const response = await fetch('/api/library/seed', { method: 'POST' })
    const data = await response.json()
    if (data.success) {
      await loadLibraryData()
    }
  } catch (error) {
    console.error('初始化产品库失败:', error)
  }
}

onMounted(() => {
  loadLibraryData()
})

const selectedContainer = ref('')
const containerQty = ref(1)
const selectedPCS = ref('')
const durationHours = ref(2)

const totalEnergy = computed(() => {
  const container = containers.value.find(c => c.id === selectedContainer.value)
  return container ? container.energy * containerQty.value : 0
})

const totalPower = computed(() => {
  const container = containers.value.find(c => c.id === selectedContainer.value)
  if (!container) return 0
  const powerFromRating = container.power * containerQty.value
  const powerFromDuration = totalEnergy.value / durationHours.value
  return Math.max(powerFromRating, powerFromDuration)
})

const pcsQty = computed(() => {
  const pcs = pcsList.value.find(p => p.id === selectedPCS.value)
  if (!pcs || totalPower.value === 0) return 0
  return Math.ceil(totalPower.value / pcs.power)
})

const pairingMode = computed(() => {
  if (!selectedContainer.value || !selectedPCS.value) return '--'
  const container = containers.value.find(c => c.id === selectedContainer.value)
  const pcs = pcsList.value.find(p => p.id === selectedPCS.value)
  
  if (container.power === pcs.power) return '1:1配对'
  if (container.power < pcs.power) return '多舱并联'
  if (container.power > pcs.power) return '单舱多PCS'
  return '混合配对'
})

const pairingDescription = computed(() => {
  if (!selectedContainer.value || !selectedPCS.value) return '请选择集装箱和PCS型号'
  const container = containers.value.find(c => c.id === selectedContainer.value)
  const pcs = pcsList.value.find(p => p.id === selectedPCS.value)
  
  const ratio = container.power / pcs.power
  if (ratio === 1) {
    return `每个${container.name}配置1台${pcs.name}，共${containerQty.value}台PCS，独立运行。`
  } else if (ratio < 1) {
    const containersPerPCS = Math.ceil(1 / ratio)
    return `每${containersPerPCS}个${container.name}并联后接入1台${pcs.name}，共${pcsQty.value}台PCS。`
  } else {
    const pcsPerContainer = Math.ceil(ratio)
    return `每个${container.name}配置${pcsPerContainer}台${pcs.name}，共${pcsQty.value}台PCS，并联输出。`
  }
})

const dcVoltageRange = computed(() => {
  const pcs = pcsList.value.find(p => p.id === selectedPCS.value)
  return pcs ? pcs.dcVoltage : '--'
})

const acVoltage = computed(() => {
  const pcs = pcsList.value.find(p => p.id === selectedPCS.value)
  return pcs ? `${pcs.voltage}V` : '--'
})

const shortCircuitCapacity = computed(() => {
  const pcs = pcsList.value.find(p => p.id === selectedPCS.value)
  if (!pcs) return '--'
  return `${pcs.power * 10} MVA`
})

const recommendedSchemes = computed(() => {
  if (!selectedContainer.value) return []
  
  const schemes = []
  const container = containers.value.find(c => c.id === selectedContainer.value)
  
  for (let qty = 1; qty <= Math.min(containerQty.value + 2, 10); qty++) {
    const energy = container.energy * qty
    const power = container.power * qty
    
    for (const pcs of pcsList.value) {
      const pcsCount = Math.ceil(power / pcs.power)
      if (pcsCount <= 10 && pcsCount >= 1) {
        const ratio = power / (pcsCount * pcs.power)
        const efficiency = pcs.efficiency - Math.abs(ratio - 1) * 0.5
        
        schemes.push({
          id: `方案${schemes.length + 1}`,
          containerConfig: `${qty}×${container.name}`,
          pcsConfig: `${pcsCount}×${pcs.name}`,
          pairingMode: ratio === 1 ? '1:1' : ratio < 1 ? '多舱并联' : '单舱多PCS',
          energyPowerRatio: `${energy}/${pcsCount * pcs.power}`,
          efficiency: efficiency.toFixed(1),
          containerQty: qty,
          pcsQty: pcsCount,
          containerId: container.id,
          pcsId: pcs.id,
        })
      }
    }
  }
  
  return schemes.sort((a, b) => b.efficiency - a.efficiency).slice(0, 5)
})

const connectionDiagram = ref(null)
const singleLineDiagram = ref(null)
let connectionChart = null
let singleLineChart = null

const calculatePCS = () => {
  nextTick(() => {
    renderConnectionDiagram()
    renderSingleLineDiagram()
  })
}

const renderConnectionDiagram = () => {
  if (!connectionDiagram.value) return
  
  if (connectionChart) {
    connectionChart.dispose()
  }
  
  connectionChart = echarts.init(connectionDiagram.value)
  
  const container = containers.value.find(c => c.id === selectedContainer.value)
  const pcs = pcsList.value.find(p => p.id === selectedPCS.value)
  
  if (!container || !pcs) {
    connectionChart.setOption({
      title: { text: '请选择集装箱和PCS型号', left: 'center', top: 'center', textStyle: { color: 'var(--color-text-muted)', fontSize: 14 } },
    })
    return
  }
  
  const nodes = []
  const links = []
  
  const style = getComputedStyle(document.documentElement)
  const colors = {
    grid: style.getPropertyValue('--color-border').trim(),
    teal: style.getPropertyValue('--color-accent-secondary').trim(),
    sky: style.getPropertyValue('--color-accent').trim(),
    amber: style.getPropertyValue('--color-warning').trim(),
    emerald: style.getPropertyValue('--color-success').trim(),
    slate: style.getPropertyValue('--color-text-muted').trim(),
    text: style.getPropertyValue('--color-text').trim(),
  }
  
  nodes.push({ name: '电网', x: 500, y: 50, symbolSize: 40, category: 0, itemStyle: { color: colors.emerald } })
  
  nodes.push({ name: '变压器', x: 500, y: 120, symbolSize: 30, category: 3, itemStyle: { color: colors.amber } })
  links.push({ source: '电网', target: '变压器', lineStyle: { color: colors.amber, width: 3 } })
  
  for (let i = 0; i < pcsQty.value; i++) {
    const pcsName = `PCS${i + 1}`
    const pcsX = 100 + (i * 400 / Math.max(pcsQty.value - 1, 1))
    nodes.push({ name: pcsName, x: pcsX, y: 180, symbolSize: 25, category: 1, itemStyle: { color: colors.sky }, label: { show: true, position: 'inside', formatter: pcsName, fontSize: 10, color: '#fff' } })
    links.push({ source: '变压器', target: pcsName, lineStyle: { color: colors.amber, width: 2 } })
  }
  
  for (let i = 0; i < containerQty.value; i++) {
    const containerName = `电池舱${i + 1}`
    const containerX = 100 + (i * 400 / Math.max(containerQty.value - 1, 1))
    nodes.push({ name: containerName, x: containerX, y: 260, symbolSize: 35, category: 2, itemStyle: { color: colors.teal }, label: { show: true, position: 'inside', formatter: `${i + 1}`, fontSize: 12, color: '#fff' } })
    
    const ratio = container.power / pcs.power
    if (ratio <= 1) {
      const pcsIndex = Math.floor(i * pcsQty.value / containerQty.value)
      const pcsName = `PCS${Math.min(pcsIndex + 1, pcsQty.value)}`
      links.push({ source: containerName, target: pcsName, lineStyle: { color: colors.slate, width: 2 } })
    } else {
      const pcsPerContainer = Math.ceil(ratio)
      for (let j = 0; j < pcsPerContainer; j++) {
        const pcsIndex = i * pcsPerContainer + j
        if (pcsIndex < pcsQty.value) {
          const pcsName = `PCS${pcsIndex + 1}`
          links.push({ source: containerName, target: pcsName, lineStyle: { color: colors.slate, width: 2 } })
        }
      }
    }
  }
  
  connectionChart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      backgroundColor: isDark ? 'rgba(30, 41, 59, 0.9)' : 'rgba(255, 255, 255, 0.95)',
      borderColor: isDark ? 'rgba(100, 116, 139, 0.3)' : 'rgba(226, 232, 240, 0.5)',
      textStyle: { color: isDark ? '#e2e8f0' : '#1e293b', fontSize: 11 },
    },
    series: [{
      type: 'graph',
      layout: 'none',
      symbolSize: 30,
      roam: true,
      label: { show: true, fontSize: 10, color: '#fff' },
      edgeSymbol: ['circle', 'arrow'],
      edgeSymbolSize: [4, 8],
      data: nodes,
      links: links,
      categories: [
        { name: '电网' },
        { name: 'PCS' },
        { name: '电池舱' },
        { name: '变压器' },
      ],
      lineStyle: { opacity: 0.9, curveness: 0 },
    }],
  })
}

const renderSingleLineDiagram = () => {
  if (!singleLineDiagram.value) return
  
  if (singleLineChart) {
    singleLineChart.dispose()
  }
  
  singleLineChart = echarts.init(singleLineDiagram.value)
  
  const container = containers.value.find(c => c.id === selectedContainer.value)
  const pcs = pcsList.value.find(p => p.id === selectedPCS.value)
  
  if (!container || !pcs) {
    singleLineChart.setOption({
      title: { text: '请选择集装箱和PCS型号', left: 'center', top: 'center', textStyle: { color: 'var(--color-text-muted)', fontSize: 14 } },
    })
    return
  }
  
  const style = getComputedStyle(document.documentElement)
  const colors = {
    emerald: style.getPropertyValue('--color-success').trim(),
    amber: style.getPropertyValue('--color-warning').trim(),
    sky: style.getPropertyValue('--color-accent').trim(),
    teal: style.getPropertyValue('--color-accent-secondary').trim(),
    slate: style.getPropertyValue('--color-text-muted').trim(),
    text: style.getPropertyValue('--color-text').trim(),
  }
  
  const graphicElements = []
  
  graphicElements.push({
    type: 'rect',
    shape: { x: 450, y: 20, width: 100, height: 40 },
    style: { fill: colors.emerald, stroke: colors.emerald, lineWidth: 2 },
  })
  graphicElements.push({
    type: 'text',
    style: { text: '电网 10kV', x: 500, y: 45, fill: '#fff', fontSize: 12, textAlign: 'center' },
  })
  
  graphicElements.push({
    type: 'line',
    shape: { x1: 500, y1: 60, x2: 500, y2: 100 },
    style: { stroke: colors.amber, lineWidth: 4 },
  })
  
  graphicElements.push({
    type: 'circle',
    shape: { cx: 500, cy: 120, r: 20 },
    style: { fill: colors.amber, stroke: colors.amber, lineWidth: 2 },
  })
  graphicElements.push({
    type: 'text',
    style: { text: 'T', x: 500, y: 125, fill: '#fff', fontSize: 14, textAlign: 'center' },
  })
  
  graphicElements.push({
    type: 'line',
    shape: { x1: 500, y1: 140, x2: 500, y2: 180 },
    style: { stroke: colors.amber, lineWidth: 4 },
  })
  graphicElements.push({
    type: 'line',
    shape: { x1: 100, y1: 180, x2: 900, y2: 180 },
    style: { stroke: colors.amber, lineWidth: 3 },
  })
  graphicElements.push({
    type: 'text',
    style: { text: `AC母线 ${pcs.voltage}V`, x: 500, y: 170, fill: colors.amber, fontSize: 10, textAlign: 'center' },
  })
  
  for (let i = 0; i < pcsQty.value; i++) {
    const x = 100 + (i * 800 / Math.max(pcsQty.value - 1, 1))
    
    graphicElements.push({
      type: 'line',
      shape: { x1: x, y1: 180, x2: x, y2: 220 },
      style: { stroke: colors.amber, lineWidth: 2 },
    })
    
    graphicElements.push({
      type: 'rect',
      shape: { x: x - 30, y: 220, width: 60, height: 40 },
      style: { fill: colors.sky, stroke: colors.sky, lineWidth: 2 },
    })
    graphicElements.push({
      type: 'text',
      style: { text: `PCS${i + 1}\n${pcs.power}MW`, x: x, y: 245, fill: '#fff', fontSize: 10, textAlign: 'center' },
    })
    
    graphicElements.push({
      type: 'line',
      shape: { x1: x, y1: 260, x2: x, y2: 300 },
      style: { stroke: colors.slate, lineWidth: 2 },
    })
  }
  
  graphicElements.push({
    type: 'line',
    shape: { x1: 100, y1: 300, x2: 900, y2: 300 },
    style: { stroke: colors.slate, lineWidth: 3 },
  })
  graphicElements.push({
    type: 'text',
    style: { text: `DC母线 ${pcs.dcVoltage}`, x: 500, y: 290, fill: colors.slate, fontSize: 10, textAlign: 'center' },
  })
  
  for (let i = 0; i < containerQty.value; i++) {
    const x = 100 + (i * 800 / Math.max(containerQty.value - 1, 1))
    
    graphicElements.push({
      type: 'line',
      shape: { x1: x, y1: 300, x2: x, y2: 340 },
      style: { stroke: colors.slate, lineWidth: 2 },
    })
    
    graphicElements.push({
      type: 'rect',
      shape: { x: x - 40, y: 340, width: 80, height: 60 },
      style: { fill: colors.teal, stroke: colors.teal, lineWidth: 2 },
    })
    graphicElements.push({
      type: 'text',
      style: { text: `电池舱${i + 1}\n${container.energy}MWh`, x: x, y: 375, fill: '#fff', fontSize: 10, textAlign: 'center' },
    })
  }
  
  singleLineChart.setOption({
    backgroundColor: 'transparent',
    graphic: { elements: graphicElements },
  })
}

const applyScheme = (scheme) => {
  selectedContainer.value = scheme.containerId
  containerQty.value = scheme.containerQty
  selectedPCS.value = scheme.pcsId
  calculatePCS()
}

const resetConfig = () => {
  selectedContainer.value = ''
  containerQty.value = 1
  selectedPCS.value = ''
  calculatePCS()
}

const applyConfig = () => {
  const container = containers.value.find(c => c.id === selectedContainer.value)
  const pcs = pcsList.value.find(p => p.id === selectedPCS.value)
  
  if (!container || !pcs) {
    emit('error', '请先选择集装箱和PCS型号', 'warning')
    return
  }
  
  emit('applyConfig', {
    ratedEnergy: container.energy,
    initContainerQty: containerQty.value,
    initPcsQty: pcsQty.value,
    duration: container.energy / container.power,
    acEfficiency: pcs.efficiency,
  })
}

onMounted(() => {
  calculatePCS()
})

watch([selectedContainer, containerQty, selectedPCS], () => {
  calculatePCS()
})
</script>