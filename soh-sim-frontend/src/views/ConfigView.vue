<template>
  <div class="h-full flex flex-col gap-4">
    <!-- 页面标题 -->
    <div class="flex items-center justify-between">
      <h2 class="text-lg font-bold text-teal-400">方案设计</h2>
      <div class="flex items-center gap-2">
        <button 
          v-if="userRole !== 'customer'"
          @click="saveAsNewVersion"
          class="bg-sky-600 hover:bg-sky-700 text-white text-xs px-3 py-1.5 rounded-md transition-colors">
          另存为新版本
        </button>
        <button 
          v-if="userRole !== 'customer'"
          @click="saveConfig"
          class="bg-teal-600 hover:bg-teal-700 text-white text-xs px-3 py-1.5 rounded-md transition-colors">
          保存配置
        </button>
      </div>
    </div>

    <!-- 版本信息 -->
    <div v-if="currentVersion" class="bg-slate-800/50 rounded-lg p-3 border border-slate-700 flex items-center justify-between">
      <div class="flex items-center gap-4">
        <span class="text-xs text-slate-400">版本:</span>
        <span class="text-sm font-medium text-teal-400">{{ currentVersion.name }}</span>
        <span class="text-xs text-slate-500">v{{ currentVersion.version_num }}.0</span>
      </div>
      <div class="flex items-center gap-2">
        <span class="text-xs text-slate-500">状态:</span>
        <span :class="['text-xs', currentVersion.status === 'active' ? 'text-emerald-400' : 'text-slate-500']">
          {{ currentVersion.status === 'active' ? '使用中' : '已归档' }}
        </span>
      </div>
    </div>

    <!-- 直流侧设计 -->
    <div class="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
      <h3 class="text-sm font-medium text-slate-300 mb-4 flex items-center gap-2">
        <span class="w-1 h-4 bg-teal-500 rounded"></span>
        直流侧设计（电池系统）
      </h3>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <!-- 左侧：电芯选型 -->
        <div class="space-y-4">
          <!-- 电芯选型 -->
          <div class="bg-slate-700/30 rounded-lg p-4">
            <h4 class="text-xs font-medium text-slate-300 mb-3">电芯型号</h4>
            <select v-model="config.dc.cellId" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200 mb-4">
              <option value="">-- 选择电芯型号 --</option>
              <option v-for="cell in cellLibrary" :key="cell.id" :value="cell.id">
                {{ cell.mfr }} - {{ cell.model }}
              </option>
            </select>
            
            <!-- 电芯参数表单（支持手动修改） -->
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs text-slate-400 mb-1">额定容量 (Ah)</label>
                <input v-model.number="config.dc.cellCapacity" type="number" step="0.1" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
              </div>
              <div>
                <label class="block text-xs text-slate-400 mb-1">额定电压 (V)</label>
                <input v-model.number="config.dc.cellVoltage" type="number" step="0.1" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
              </div>
              <div>
                <label class="block text-xs text-slate-400 mb-1">能量密度 (Wh/kg)</label>
                <input v-model.number="config.dc.cellEnergyDensity" type="number" step="0.1" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
              </div>
              <div>
                <label class="block text-xs text-slate-400 mb-1">循环寿命 (次)</label>
                <input v-model.number="config.dc.cellCycleLife" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
              </div>
              <div>
                <label class="block text-xs text-slate-400 mb-1">标称能量 (Wh)</label>
                <input v-model.number="config.dc.cellEnergyWh" type="number" step="0.1" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
              </div>
              <div>
                <label class="block text-xs text-slate-400 mb-1">重量 (kg)</label>
                <input v-model.number="config.dc.cellWeight" type="number" step="0.1" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
              </div>
              <div>
                <label class="block text-xs text-slate-400 mb-1">最小电压 (V)</label>
                <input v-model.number="config.dc.cellVoltageMin" type="number" step="0.1" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
              </div>
              <div>
                <label class="block text-xs text-slate-400 mb-1">最大电压 (V)</label>
                <input v-model.number="config.dc.cellVoltageMax" type="number" step="0.1" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
              </div>
            </div>
          </div>

          <!-- Pack配置 -->
          <div class="bg-slate-700/30 rounded-lg p-4">
            <h4 class="text-xs font-medium text-slate-300 mb-3">Pack配置</h4>
            <div class="grid grid-cols-2 gap-3 mb-4">
              <div>
                <label class="block text-xs text-slate-400 mb-1">串联数量 (S)</label>
                <input v-model.number="config.dc.packSeries" type="number" min="1" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
              </div>
              <div>
                <label class="block text-xs text-slate-400 mb-1">并联数量 (P)</label>
                <input v-model.number="config.dc.packParallel" type="number" min="1" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
              </div>
            </div>
            
            <!-- Pack参数计算结果 -->
            <div class="grid grid-cols-2 gap-3 text-xs">
              <div class="bg-slate-600/30 rounded p-2">
                <span class="text-slate-400">Pack电压</span>
                <p class="text-teal-400 font-medium">{{ packParams.voltage }} V</p>
              </div>
              <div class="bg-slate-600/30 rounded p-2">
                <span class="text-slate-400">Pack容量</span>
                <p class="text-teal-400 font-medium">{{ packParams.capacity }} Ah</p>
              </div>
              <div class="bg-slate-600/30 rounded p-2 col-span-2">
                <span class="text-slate-400">Pack能量</span>
                <p class="text-teal-400 font-medium">{{ packParams.energy }} kWh</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：电池簇配置 -->
        <div class="space-y-4">
          <!-- 电池簇配置 -->
          <div class="bg-slate-700/30 rounded-lg p-4">
            <h4 class="text-xs font-medium text-slate-300 mb-3">电池簇配置</h4>
            <div class="grid grid-cols-2 gap-3 mb-4">
              <div>
                <label class="block text-xs text-slate-400 mb-1">Pack串联数量 (S)</label>
                <input v-model.number="config.dc.clusterSeries" type="number" min="1" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
              </div>
              <div>
                <label class="block text-xs text-slate-400 mb-1">Pack并联数量 (P)</label>
                <input v-model.number="config.dc.clusterParallel" type="number" min="1" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
              </div>
            </div>
            
            <!-- 簇参数计算结果 -->
            <div class="grid grid-cols-2 gap-3 text-xs">
              <div class="bg-slate-600/30 rounded p-2">
                <span class="text-slate-400">簇电压</span>
                <p class="text-teal-400 font-medium">{{ clusterParams.voltage }} V</p>
              </div>
              <div class="bg-slate-600/30 rounded p-2">
                <span class="text-slate-400">簇容量</span>
                <p class="text-teal-400 font-medium">{{ clusterParams.capacity }} Ah</p>
              </div>
              <div class="bg-slate-600/30 rounded p-2">
                <span class="text-slate-400">簇能量</span>
                <p class="text-teal-400 font-medium">{{ clusterParams.energy }} kWh</p>
              </div>
              <div class="bg-slate-600/30 rounded p-2">
                <span class="text-slate-400">簇数量</span>
                <p class="text-teal-400 font-medium">{{ config.dc.clusterCount }}</p>
              </div>
            </div>
          </div>

          <!-- 集装箱配置 -->
          <div class="bg-slate-700/30 rounded-lg p-4">
            <h4 class="text-xs font-medium text-slate-300 mb-3">集装箱配置</h4>
            <div class="grid grid-cols-2 gap-3 mb-4">
              <div>
                <label class="block text-xs text-slate-400 mb-1">集装箱型号</label>
                <select v-model="config.dc.containerId" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200">
                  <option value="">-- 选择集装箱 --</option>
                  <option v-for="c in containerLibrary" :key="c.id" :value="c.id">
                    {{ c.mfr }} - {{ c.model }}
                  </option>
                </select>
              </div>
              <div>
                <label class="block text-xs text-slate-400 mb-1">集装箱数量</label>
                <input v-model.number="config.dc.containerQty" type="number" min="1" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
              </div>
            </div>
            
            <!-- 集装箱参数计算结果 -->
            <div class="grid grid-cols-2 gap-3 text-xs">
              <div class="bg-slate-600/30 rounded p-2">
                <span class="text-slate-400">单箱能量</span>
                <p class="text-teal-400 font-medium">{{ containerParams.singleEnergy }} kWh</p>
              </div>
              <div class="bg-slate-600/30 rounded p-2">
                <span class="text-slate-400">总能量</span>
                <p class="text-teal-400 font-medium">{{ containerParams.totalEnergy }} MWh</p>
              </div>
              <div class="bg-slate-600/30 rounded p-2">
                <span class="text-slate-400">总电压</span>
                <p class="text-teal-400 font-medium">{{ containerParams.totalVoltage }} V</p>
              </div>
              <div class="bg-slate-600/30 rounded p-2">
                <span class="text-slate-400">总容量</span>
                <p class="text-teal-400 font-medium">{{ containerParams.totalCapacity }} kAh</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 交流侧设计 -->
    <div class="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
      <h3 class="text-sm font-medium text-slate-300 mb-3 flex items-center gap-2">
        <span class="w-1 h-4 bg-sky-500 rounded"></span>
        交流侧设计
      </h3>
      
      <div class="space-y-4">
        <!-- PCS选型 -->
        <div>
          <label class="block text-xs text-slate-400 mb-1">PCS选型</label>
          <select v-model="config.ac.pcsId" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200">
            <option value="">-- 从PCS库选择 --</option>
            <option v-for="pcs in pcsLibrary" :key="pcs.id" :value="pcs.id">
              {{ pcs.mfr }} - {{ pcs.model }} ({{ pcs.ratedPowerMW }}MW)
            </option>
          </select>
        </div>
        
        <!-- PCS数量 -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-xs text-slate-400 mb-1">PCS数量</label>
            <input v-model.number="config.ac.pcsQty" type="number" min="1" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
          </div>
          <div>
            <label class="block text-xs text-slate-400 mb-1">PCS总功率 (MW)</label>
            <input v-model.number="config.ac.totalPower" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" readonly />
          </div>
        </div>
        
        <!-- 变压器配置 -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-xs text-slate-400 mb-1">变压器类型</label>
            <select v-model="config.ac.transformerType" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200">
              <option value="dry">干式变压器</option>
              <option value="oil">油浸式变压器</option>
            </select>
          </div>
          <div>
            <label class="block text-xs text-slate-400 mb-1">变压器容量 (MVA)</label>
            <input v-model.number="config.ac.transformerCapacity" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
          </div>
        </div>
      </div>
    </div>

    <!-- 配置规则匹配状态 -->
    <div v-if="ruleMatchStatus" :class="['rounded-lg p-3 border', ruleMatchStatus.isValid ? 'bg-emerald-500/10 border-emerald-500/30' : 'bg-red-500/10 border-red-500/30']">
      <div class="flex items-center gap-2 text-xs">
        <span :class="ruleMatchStatus.isValid ? 'text-emerald-400' : 'text-red-400'">
          {{ ruleMatchStatus.isValid ? '✓ 配置匹配规则' : '✕ 配置不符合规则' }}
        </span>
      </div>
      <p class="text-xs text-slate-400 mt-1">{{ ruleMatchStatus.message }}</p>
    </div>

    <!-- 另存为版本弹窗 -->
    <div v-if="showSaveAsDialog" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center">
      <div class="bg-slate-800 border border-slate-700 rounded-lg p-4 w-80">
        <h3 class="text-sm font-medium text-slate-200 mb-3">另存为新版本</h3>
        <input v-model="newVersionName" placeholder="版本名称，如：方案v2" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200 mb-3" />
        <div class="flex justify-end gap-2">
          <button @click="showSaveAsDialog = false" class="px-3 py-1 text-xs text-slate-400 hover:text-slate-300">取消</button>
          <button @click="confirmSaveAs" class="px-3 py-1 text-xs bg-sky-600 text-white rounded hover:bg-sky-700">创建</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'

const props = defineProps({
  projectId: String,
  versionId: String,
})

const emit = defineEmits(['save-config'])

const userRole = ref('customer')
const cellLibrary = ref([])
const containerLibrary = ref([])
const pcsLibrary = ref([])
const currentVersion = ref(null)
const showSaveAsDialog = ref(false)
const newVersionName = ref('')

// 配置数据
const config = reactive({
  dc: {
    cellId: '',
    cellCapacity: 280,      // 额定容量 (Ah)
    cellVoltage: 3.2,       // 额定电压 (V)
    cellEnergyDensity: 165, // 能量密度 (Wh/kg)
    cellCycleLife: 6000,    // 循环寿命 (次)
    cellEnergyWh: 896,      // 标称能量 (Wh)
    cellWeight: 5.4,        // 重量 (kg)
    cellVoltageMin: 2.5,    // 最小电压 (V)
    cellVoltageMax: 3.65,   // 最大电压 (V)
    packSeries: 12,         // Pack内电芯串联数
    packParallel: 10,       // Pack内电芯并联数
    clusterSeries: 20,      // 簇内Pack串联数
    clusterParallel: 1,     // 簇内Pack并联数
    clusterCount: 24,       // 簇数量
    containerId: '',
    containerQty: 1,
  },
  ac: {
    pcsId: '',
    pcsQty: 2,
    totalPower: 0,
    transformerType: 'dry',
    transformerCapacity: 10,
  },
})

// 当前选中的电芯
const selectedCell = computed(() => {
  return cellLibrary.value.find(cell => cell.id === config.dc.cellId)
})

// 监听电芯选择变化，自动带出参数
watch(() => config.dc.cellId, (newCellId) => {
  const cell = cellLibrary.value.find(c => c.id === newCellId)
  if (cell) {
    config.dc.cellCapacity = cell.capacityAh || 280
    config.dc.cellVoltage = cell.voltageNominal || 3.2
    config.dc.cellEnergyDensity = cell.energyDensity || 165
    config.dc.cellCycleLife = cell.cycleLife || 6000
    config.dc.cellEnergyWh = cell.energyWh || 896
    config.dc.cellWeight = cell.weight || 5.4
    config.dc.cellVoltageMin = cell.voltageMin || 2.5
    config.dc.cellVoltageMax = cell.voltageMax || 3.65
  }
})

// Pack参数计算
const packParams = computed(() => {
  return {
    voltage: (config.dc.cellVoltage * config.dc.packSeries).toFixed(1),
    capacity: (config.dc.cellCapacity * config.dc.packParallel).toFixed(1),
    energy: ((config.dc.cellVoltage * config.dc.packSeries * config.dc.cellCapacity * config.dc.packParallel) / 1000).toFixed(2),
  }
})

// 簇参数计算
const clusterParams = computed(() => {
  const packVoltage = parseFloat(packParams.value.voltage)
  const packCapacity = parseFloat(packParams.value.capacity)
  const packEnergy = parseFloat(packParams.value.energy)
  
  return {
    voltage: (packVoltage * config.dc.clusterSeries).toFixed(1),
    capacity: (packCapacity * config.dc.clusterParallel).toFixed(1),
    energy: (packEnergy * config.dc.clusterSeries * config.dc.clusterParallel).toFixed(2),
  }
})

// 集装箱参数计算
const containerParams = computed(() => {
  const clusterEnergy = parseFloat(clusterParams.value.energy)
  const clusterVoltage = parseFloat(clusterParams.value.voltage)
  const clusterCapacity = parseFloat(clusterParams.value.capacity)
  
  return {
    singleEnergy: (clusterEnergy * config.dc.clusterCount).toFixed(2),
    totalEnergy: ((clusterEnergy * config.dc.clusterCount * config.dc.containerQty) / 1000).toFixed(3),
    totalVoltage: clusterVoltage.toFixed(1),
    totalCapacity: ((clusterCapacity * config.dc.clusterCount * config.dc.containerQty) / 1000).toFixed(3),
  }
})

// 规则匹配状态
const ruleMatchStatus = computed(() => {
  if (!config.dc.containerId || !config.ac.pcsId) return null
  
  const container = containerLibrary.value.find(c => c.id === config.dc.containerId)
  const pcs = pcsLibrary.value.find(p => p.id === config.ac.pcsId)
  
  if (!container || !pcs) return null
  
  const totalCapacity = container.ratedEnergyMWh * config.dc.containerQty
  const expectedPcsPower = totalCapacity * 0.5 // 0.5C 运行
  
  if (Math.abs(pcs.ratedPowerMW * config.ac.pcsQty - expectedPcsPower) < 1) {
    return { isValid: true, message: '配置符合规则' }
  } else {
    return { 
      isValid: false, 
      message: `功率配比异常：期望约${expectedPcsPower.toFixed(1)}MW PCS，实际${(pcs.ratedPowerMW * config.ac.pcsQty).toFixed(1)}MW` 
    }
  }
})

// 初始化
onMounted(() => {
  loadUserInfo()
  loadProductLibrary()
})

function loadUserInfo() {
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  userRole.value = user.role || 'customer'
}

// 加载产品库
async function loadProductLibrary() {
  try {
    const token = localStorage.getItem('token')
    
    // 加载电芯库
    const cellRes = await fetch('/api/library/cells', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const cellData = await cellRes.json()
    if (cellData.success) cellLibrary.value = cellData.data || []
    
    // 加载集装箱库
    const containerRes = await fetch('/api/library/containers', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const containerData = await containerRes.json()
    if (containerData.success) containerLibrary.value = containerData.data || []
    
    // 加载PCS库
    const pcsRes = await fetch('/api/library/pcs', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const pcsData = await pcsRes.json()
    if (pcsData.success) pcsLibrary.value = pcsData.data || []
    
    // 加载当前版本配置
    if (props.versionId) {
      loadVersionConfig()
    }
  } catch (error) {
    console.error('加载产品库失败:', error)
  }
}

// 加载版本配置
async function loadVersionConfig() {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`/api/versions/${props.versionId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await response.json()
    if (data.success) {
      currentVersion.value = data.data
      if (data.data.config_data) {
        try {
          const savedConfig = JSON.parse(data.data.config_data)
          Object.assign(config, savedConfig)
        } catch (e) {
          console.error('解析配置数据失败:', e)
        }
      }
    }
  } catch (error) {
    console.error('加载版本配置失败:', error)
  }
}

// 保存配置
async function saveConfig() {
  if (!props.versionId) {
    alert('请先选择项目')
    return
  }
  
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`/api/versions/${props.versionId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ config_data: JSON.stringify(config) }),
    })
    const data = await response.json()
    if (data.success) {
      emit('save-config', config)
      alert('配置保存成功')
    } else {
      alert('保存失败: ' + data.error)
    }
  } catch (error) {
    console.error('保存配置失败:', error)
  }
}

// 另存为新版本
function saveAsNewVersion() {
  if (!props.versionId) {
    alert('请先选择项目')
    return
  }
  showSaveAsDialog.value = true
}

// 确认另存为
async function confirmSaveAs() {
  if (!newVersionName.value.trim()) {
    alert('请输入版本名称')
    return
  }
  
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`/api/projects/${props.projectId}/versions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        name: newVersionName.value,
        config_data: JSON.stringify(config),
      }),
    })
    const data = await response.json()
    if (data.success) {
      alert('新版本创建成功')
      showSaveAsDialog.value = false
      newVersionName.value = ''
    } else {
      alert('创建失败: ' + data.error)
    }
  } catch (error) {
    console.error('创建版本失败:', error)
  }
}

// 监听PCS数量变化，自动计算总功率
watch(() => config.ac.pcsQty, (newQty) => {
  const pcs = pcsLibrary.value.find(p => p.id === config.ac.pcsId)
  if (pcs) {
    config.ac.totalPower = (pcs.ratedPowerMW * newQty).toFixed(2)
  }
})
</script>
