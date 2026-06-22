<template>
  <div class="flex flex-col gap-4 h-full overflow-auto p-4">
    <!-- 配置面板 -->
    <div class="bg-slate-900/40 rounded-lg border border-slate-800 p-4">
      <h3 class="text-sm font-bold text-teal-400 mb-3 flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-teal-400"></span>
        电池集装箱配置
      </h3>

      <div class="grid grid-cols-4 gap-4">
        <!-- 集装箱选择 -->
        <div class="bg-slate-800/30 rounded p-3 border border-slate-700">
          <label class="text-xs text-slate-400 block mb-2">储能集装箱型号</label>
          <select v-model="selectedContainer" @change="calculatePCS"
            class="w-full bg-slate-900 border border-slate-600 rounded px-3 py-2 text-xs focus:border-teal-500 focus:outline-none">
            <option value="">请选择集装箱型号</option>
            <option v-for="container in containers" :key="container.id" :value="container.id">
              {{ container.name }} - {{ container.energy }}MWh / {{ container.power }}MW
            </option>
          </select>
        </div>

        <!-- 集装箱数量 -->
        <div class="bg-slate-800/30 rounded p-3 border border-slate-700">
          <label class="text-xs text-slate-400 block mb-2">集装箱数量</label>
          <input v-model.number="containerQty" @change="calculatePCS" type="number" min="1" max="100"
            class="w-full bg-slate-900 border border-slate-600 rounded px-3 py-2 text-xs focus:border-teal-500 focus:outline-none">
        </div>

        <!-- 运行时长 -->
        <div class="bg-slate-800/30 rounded p-3 border border-slate-700">
          <label class="text-xs text-slate-400 block mb-2">运行时长 (h)</label>
          <input v-model.number="durationHours" @change="calculatePCS" type="number" min="0.5" max="8" step="0.5"
            class="w-full bg-slate-900 border border-slate-600 rounded px-3 py-2 text-xs focus:border-teal-500 focus:outline-none">
          <p class="text-[10px] text-slate-500 mt-1">C-rate = 1/时长, PCS功率 = 能量/时长</p>
        </div>

        <!-- PCS型号选择 -->
        <div class="bg-slate-800/30 rounded p-3 border border-slate-700">
          <label class="text-xs text-slate-400 block mb-2">PCS型号</label>
          <select v-model="selectedPCS" @change="calculatePCS"
            class="w-full bg-slate-900 border border-slate-600 rounded px-3 py-2 text-xs focus:border-teal-500 focus:outline-none">
            <option value="">请选择PCS型号</option>
            <option v-for="pcs in pcsList" :key="pcs.id" :value="pcs.id">
              {{ pcs.name }} - {{ pcs.power }}MW / {{ pcs.voltage }}V
            </option>
          </select>
        </div>
      </div>

      <!-- 自动计算结果 -->
      <div class="mt-4 bg-teal-500/10 rounded-lg border border-teal-500/30 p-4">
        <h4 class="text-xs font-bold text-teal-400 mb-3">自动计算结果</h4>
        <div class="grid grid-cols-4 gap-3">
          <div class="text-center">
            <p class="text-[10px] text-slate-500">总能量</p>
            <p class="text-lg font-bold text-teal-400">{{ totalEnergy.toFixed(1) }} MWh</p>
          </div>
          <div class="text-center">
            <p class="text-[10px] text-slate-500">总功率</p>
            <p class="text-lg font-bold text-sky-400">{{ totalPower.toFixed(1) }} MW</p>
          </div>
          <div class="text-center">
            <p class="text-[10px] text-slate-500">PCS数量</p>
            <p class="text-lg font-bold text-emerald-400">{{ pcsQty }} 台</p>
          </div>
          <div class="text-center">
            <p class="text-[10px] text-slate-500">配比方式</p>
            <p class="text-lg font-bold text-amber-400">{{ pairingMode }}</p>
          </div>
        </div>

        <!-- 配比详情 -->
        <div class="mt-3 text-[10px] text-slate-400">
          <p><strong class="text-slate-300">配比说明：</strong>{{ pairingDescription }}</p>
        </div>
      </div>
    </div>

    <!-- 连接图展示 -->
    <div class="bg-slate-900/40 rounded-lg border border-slate-800 p-4">
      <h3 class="text-sm font-bold text-teal-400 mb-3 flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-teal-400"></span>
        系统连接图
      </h3>

      <div ref="connectionDiagram" class="h-64 bg-slate-800/30 rounded border border-slate-700"></div>

      <!-- 图例说明 -->
      <div class="mt-3 flex gap-4 text-[10px]">
        <div class="flex items-center gap-1">
          <span class="w-3 h-3 rounded bg-teal-500"></span>
          <span class="text-slate-400">电池集装箱</span>
        </div>
        <div class="flex items-center gap-1">
          <span class="w-3 h-3 rounded bg-sky-500"></span>
          <span class="text-slate-400">PCS</span>
        </div>
        <div class="flex items-center gap-1">
          <span class="w-3 h-3 rounded bg-amber-500"></span>
          <span class="text-slate-400">变压器</span>
        </div>
        <div class="flex items-center gap-1">
          <span class="w-3 h-3 rounded bg-emerald-500"></span>
          <span class="text-slate-400">电网</span>
        </div>
        <div class="flex items-center gap-1">
          <span class="w-2 h-0.5 bg-slate-400"></span>
          <span class="text-slate-400">DC连接</span>
        </div>
        <div class="flex items-center gap-1">
          <span class="w-2 h-0.5 bg-amber-400"></span>
          <span class="text-slate-400">AC连接</span>
        </div>
      </div>
    </div>

    <!-- 单线图展示 -->
    <div class="bg-slate-900/40 rounded-lg border border-slate-800 p-4">
      <h3 class="text-sm font-bold text-teal-400 mb-3 flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-teal-400"></span>
        电气单线图
      </h3>

      <div ref="singleLineDiagram" class="h-80 bg-slate-800/30 rounded border border-slate-700"></div>

      <!-- 电气参数 -->
      <div class="mt-3 grid grid-cols-5 gap-2 text-[10px]">
        <div class="bg-slate-800/50 rounded p-2 border border-slate-700">
          <p class="text-slate-500">DC电压范围</p>
          <p class="text-teal-400 font-bold">{{ dcVoltageRange }}</p>
        </div>
        <div class="bg-slate-800/50 rounded p-2 border border-slate-700">
          <p class="text-slate-500">AC输出电压</p>
          <p class="text-sky-400 font-bold">{{ acVoltage }}</p>
        </div>
        <div class="bg-slate-800/50 rounded p-2 border border-slate-700">
          <p class="text-slate-500">额定频率</p>
          <p class="text-amber-400 font-bold">50 Hz</p>
        </div>
        <div class="bg-slate-800/50 rounded p-2 border border-slate-700">
          <p class="text-slate-500">短路容量</p>
          <p class="text-emerald-400 font-bold">{{ shortCircuitCapacity }}</p>
        </div>
        <div class="bg-slate-800/50 rounded p-2 border border-slate-700">
          <p class="text-slate-500">接地方式</p>
          <p class="text-purple-400 font-bold">TN-S</p>
        </div>
      </div>
    </div>

    <!-- 配对方案列表 -->
    <div class="bg-slate-900/40 rounded-lg border border-slate-800 p-4">
      <h3 class="text-sm font-bold text-teal-400 mb-3 flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-teal-400"></span>
        推荐配对方案
      </h3>

      <div class="overflow-auto">
        <table class="w-full text-xs">
          <thead class="text-slate-500 border-b border-slate-700">
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
              class="border-b border-slate-700 hover:bg-slate-800/50">
              <td class="py-2 px-3 text-slate-400">{{ scheme.id }}</td>
              <td class="py-2 px-3 text-teal-400">{{ scheme.containerConfig }}</td>
              <td class="py-2 px-3 text-sky-400">{{ scheme.pcsConfig }}</td>
              <td class="py-2 px-3 text-amber-400">{{ scheme.pairingMode }}</td>
              <td class="py-2 px-3 text-emerald-400">{{ scheme.energyPowerRatio }}</td>
              <td class="py-2 px-3 text-purple-400">{{ scheme.efficiency }}%</td>
              <td class="py-2 px-3">
                <button @click="applyScheme(scheme)"
                  class="bg-teal-500/20 hover:bg-teal-500/30 text-teal-400 px-2 py-1 rounded text-[10px] transition-all">
                  应用
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 应用配置按钮 -->
    <div class="flex justify-end gap-3">
      <button @click="resetConfig"
        class="bg-slate-700 hover:bg-slate-600 text-slate-300 text-xs px-4 py-2 rounded transition-all">
        重置配置
      </button>
      <button @click="applyConfig"
        class="bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 hover:to-emerald-600 text-white text-xs px-6 py-2 rounded font-bold transition-all shadow-md">
        应用到仿真参数
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick, watch } from 'vue'
import * as echarts from 'echarts'

const emit = defineEmits(['applyConfig', 'error'])

// 集装箱列表 - 从API加载
const containers = ref([])
const pcsList = ref([])

// 加载产品库数据
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
    
    // 如果数据为空，初始化默认数据
    if (containers.value.length === 0 || pcsList.value.length === 0) {
      await seedLibrary()
    }
  } catch (error) {
    console.error('加载产品库失败:', error)
    // 降级使用硬编码数据
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

// 初始化产品库
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

// 组件挂载时加载数据
onMounted(() => {
  loadLibraryData()
})

// 配置状态
const selectedContainer = ref('')
const containerQty = ref(1)
const selectedPCS = ref('')
const durationHours = ref(2) // 运行时长(h)，默认2h

// 计算结果
const totalEnergy = computed(() => {
  const container = containers.value.find(c => c.id === selectedContainer.value)
  return container ? container.energy * containerQty.value : 0
})

// 所需总功率 = max(集装箱额定功率之和, 总能量/运行时长)
// 即同时满足：①PCS覆盖集装箱额定功率  ②PCS满足运行倍率要求
const totalPower = computed(() => {
  const container = containers.value.find(c => c.id === selectedContainer.value)
  if (!container) return 0
  const powerFromRating = container.power * containerQty.value  // 额定功率之和
  const powerFromDuration = totalEnergy.value / durationHours.value  // 运行倍率要求
  return Math.max(powerFromRating, powerFromDuration)
})
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

// 电气参数
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

// 推荐方案
const recommendedSchemes = computed(() => {
  if (!selectedContainer.value) return []
  
  const schemes = []
  const container = containers.value.find(c => c.id === selectedContainer.value)
  
  // 生成推荐方案
  for (let qty = 1; qty <= Math.min(containerQty.value + 2, 10); qty++) {
    const energy = container.energy * qty
    const power = container.power * qty
    
    // 找最佳PCS配对
    for (const pcs of pcsList.value) {
      const pcsCount = Math.ceil(power / pcs.power)
      if (pcsCount <= 10 && pcsCount >= 1) {
        const ratio = power / (pcsCount * pcs.power)
        const efficiency = pcs.efficiency - Math.abs(ratio - 1) * 0.5 // 偏离1:1时效率下降
        
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
  
  // 按效率排序，取前5
  return schemes.sort((a, b) => b.efficiency - a.efficiency).slice(0, 5)
})

// 图表实例
const connectionDiagram = ref(null)
const singleLineDiagram = ref(null)
let connectionChart = null
let singleLineChart = null

// 计算PCS配对
const calculatePCS = () => {
  nextTick(() => {
    renderConnectionDiagram()
    renderSingleLineDiagram()
  })
}

// 渲染连接图
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
      title: { text: '请选择集装箱和PCS型号', left: 'center', top: 'center', textStyle: { color: '#64748b', fontSize: 14 } },
    })
    return
  }
  
  // 构建节点和连接数据
  const nodes = []
  const links = []
  
  // 电网节点
  nodes.push({ name: '电网', x: 500, y: 50, symbolSize: 40, category: 0, itemStyle: { color: '#10b981' } })
  
  // 变压器节点
  nodes.push({ name: '变压器', x: 500, y: 120, symbolSize: 30, category: 3, itemStyle: { color: '#f59e0b' } })
  links.push({ source: '电网', target: '变压器', lineStyle: { color: '#f59e0b', width: 3 } })
  
  // PCS节点
  for (let i = 0; i < pcsQty.value; i++) {
    const pcsName = `PCS${i + 1}`
    const pcsX = 100 + (i * 400 / Math.max(pcsQty.value - 1, 1))
    nodes.push({ name: pcsName, x: pcsX, y: 180, symbolSize: 25, category: 1, itemStyle: { color: '#0ea5e9' }, label: { show: true, position: 'inside', formatter: pcsName, fontSize: 10 } })
    links.push({ source: '变压器', target: pcsName, lineStyle: { color: '#f59e0b', width: 2 } })
  }
  
  // 集装箱节点
  for (let i = 0; i < containerQty.value; i++) {
    const containerName = `电池舱${i + 1}`
    const containerX = 100 + (i * 400 / Math.max(containerQty.value - 1, 1))
    nodes.push({ name: containerName, x: containerX, y: 260, symbolSize: 35, category: 2, itemStyle: { color: '#14b8a6' }, label: { show: true, position: 'inside', formatter: `${i + 1}`, fontSize: 12 } })
    
    // 连接到PCS（根据配比方式）
    const ratio = container.power / pcs.power
    if (ratio <= 1) {
      // 多舱并联到单PCS
      const pcsIndex = Math.floor(i * pcsQty.value / containerQty.value)
      const pcsName = `PCS${Math.min(pcsIndex + 1, pcsQty.value)}`
      links.push({ source: containerName, target: pcsName, lineStyle: { color: '#64748b', width: 2 } })
    } else {
      // 单舱多PCS
      const pcsPerContainer = Math.ceil(ratio)
      for (let j = 0; j < pcsPerContainer; j++) {
        const pcsIndex = i * pcsPerContainer + j
        if (pcsIndex < pcsQty.value) {
          const pcsName = `PCS${pcsIndex + 1}`
          links.push({ source: containerName, target: pcsName, lineStyle: { color: '#64748b', width: 2 } })
        }
      }
    }
  }
  
  connectionChart.setOption({
    tooltip: {},
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

// 渲染单线图
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
      title: { text: '请选择集装箱和PCS型号', left: 'center', top: 'center', textStyle: { color: '#64748b', fontSize: 14 } },
    })
    return
  }
  
  // 构建单线图数据
  const graphicElements = []
  
  // 电网侧
  graphicElements.push({
    type: 'rect',
    shape: { x: 450, y: 20, width: 100, height: 40 },
    style: { fill: '#10b981', stroke: '#059669', lineWidth: 2 },
  })
  graphicElements.push({
    type: 'text',
    style: { text: '电网 10kV', x: 500, y: 45, fill: '#fff', fontSize: 12, textAlign: 'center' },
  })
  
  // 主母线
  graphicElements.push({
    type: 'line',
    shape: { x1: 500, y1: 60, x2: 500, y2: 100 },
    style: { stroke: '#f59e0b', lineWidth: 4 },
  })
  
  // 变压器
  graphicElements.push({
    type: 'circle',
    shape: { cx: 500, cy: 120, r: 20 },
    style: { fill: '#f59e0b', stroke: '#d97706', lineWidth: 2 },
  })
  graphicElements.push({
    type: 'text',
    style: { text: 'T', x: 500, y: 125, fill: '#fff', fontSize: 14, textAlign: 'center' },
  })
  
  // AC母线
  graphicElements.push({
    type: 'line',
    shape: { x1: 500, y1: 140, x2: 500, y2: 180 },
    style: { stroke: '#f59e0b', lineWidth: 4 },
  })
  graphicElements.push({
    type: 'line',
    shape: { x1: 100, y1: 180, x2: 900, y2: 180 },
    style: { stroke: '#f59e0b', lineWidth: 3 },
  })
  graphicElements.push({
    type: 'text',
    style: { text: `AC母线 ${pcs.voltage}V`, x: 500, y: 170, fill: '#f59e0b', fontSize: 10, textAlign: 'center' },
  })
  
  // PCS单元
  for (let i = 0; i < pcsQty.value; i++) {
    const x = 100 + (i * 800 / Math.max(pcsQty.value - 1, 1))
    
    // AC连接线
    graphicElements.push({
      type: 'line',
      shape: { x1: x, y1: 180, x2: x, y2: 220 },
      style: { stroke: '#f59e0b', lineWidth: 2 },
    })
    
    // PCS矩形
    graphicElements.push({
      type: 'rect',
      shape: { x: x - 30, y: 220, width: 60, height: 40 },
      style: { fill: '#0ea5e9', stroke: '#0284c7', lineWidth: 2 },
    })
    graphicElements.push({
      type: 'text',
      style: { text: `PCS${i + 1}\n${pcs.power}MW`, x: x, y: 245, fill: '#fff', fontSize: 10, textAlign: 'center' },
    })
    
    // DC连接线
    graphicElements.push({
      type: 'line',
      shape: { x1: x, y1: 260, x2: x, y2: 300 },
      style: { stroke: '#64748b', lineWidth: 2 },
    })
  }
  
  // DC母线
  graphicElements.push({
    type: 'line',
    shape: { x1: 100, y1: 300, x2: 900, y2: 300 },
    style: { stroke: '#64748b', lineWidth: 3 },
  })
  graphicElements.push({
    type: 'text',
    style: { text: `DC母线 ${pcs.dcVoltage}`, x: 500, y: 290, fill: '#64748b', fontSize: 10, textAlign: 'center' },
  })
  
  // 电池集装箱
  for (let i = 0; i < containerQty.value; i++) {
    const x = 100 + (i * 800 / Math.max(containerQty.value - 1, 1))
    
    // DC连接线
    graphicElements.push({
      type: 'line',
      shape: { x1: x, y1: 300, x2: x, y2: 340 },
      style: { stroke: '#64748b', lineWidth: 2 },
    })
    
    // 集装箱矩形
    graphicElements.push({
      type: 'rect',
      shape: { x: x - 40, y: 340, width: 80, height: 60 },
      style: { fill: '#14b8a6', stroke: '#0d9488', lineWidth: 2 },
    })
    graphicElements.push({
      type: 'text',
      style: { text: `电池舱${i + 1}\n${container.energy}MWh`, x: x, y: 375, fill: '#fff', fontSize: 10, textAlign: 'center' },
    })
  }
  
  singleLineChart.setOption({
    graphic: { elements: graphicElements },
  })
}

// 应用方案
const applyScheme = (scheme) => {
  selectedContainer.value = scheme.containerId
  containerQty.value = scheme.containerQty
  selectedPCS.value = scheme.pcsId
  calculatePCS()
}

// 重置配置
const resetConfig = () => {
  selectedContainer.value = ''
  containerQty.value = 1
  selectedPCS.value = ''
  calculatePCS()
}

// 应用到仿真参数
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
    duration: container.energy / container.power, // 时长 = 能量/功率
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