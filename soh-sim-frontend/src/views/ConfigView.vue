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
      <h3 class="text-sm font-medium text-slate-300 mb-3 flex items-center gap-2">
        <span class="w-1 h-4 bg-teal-500 rounded"></span>
        直流侧设计
      </h3>
      
      <div class="space-y-4">
        <!-- 电芯选型 -->
        <div>
          <label class="block text-xs text-slate-400 mb-1">电芯选型</label>
          <select v-model="config.dc.cellId" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200">
            <option value="">-- 从电芯库选择 --</option>
            <option v-for="cell in cellLibrary" :key="cell.id" :value="cell.id">
              {{ cell.model }} ({{ cell.capacity }}Ah / {{ cell.voltage }}V)
            </option>
          </select>
        </div>
        
        <!-- 集装箱配置 -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-xs text-slate-400 mb-1">集装箱型号</label>
            <select v-model="config.dc.containerId" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200">
              <option value="">-- 从集装箱库选择 --</option>
              <option v-for="c in containerLibrary" :key="c.id" :value="c.id">
                {{ c.model }} ({{ c.capacity }}MWh)
              </option>
            </select>
          </div>
          <div>
            <label class="block text-xs text-slate-400 mb-1">集装箱数量</label>
            <input v-model.number="config.dc.containerQty" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
          </div>
        </div>
        
        <!-- 簇数和模组配置 -->
        <div class="grid grid-cols-3 gap-4">
          <div>
            <label class="block text-xs text-slate-400 mb-1">簇数/集装箱</label>
            <input v-model.number="config.dc.clusterPerContainer" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
          </div>
          <div>
            <label class="block text-xs text-slate-400 mb-1">模组数/簇</label>
            <input v-model.number="config.dc.modulePerCluster" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
          </div>
          <div>
            <label class="block text-xs text-slate-400 mb-1">电芯数/模组</label>
            <input v-model.number="config.dc.cellPerModule" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
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
              {{ pcs.model }} ({{ pcs.power }}MW)
            </option>
          </select>
        </div>
        
        <!-- PCS数量 -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-xs text-slate-400 mb-1">PCS数量</label>
            <input v-model.number="config.ac.pcsQty" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
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

const config = reactive({
  dc: {
    cellId: '',
    containerId: '',
    containerQty: 10,
    clusterPerContainer: 1,
    modulePerCluster: 10,
    cellPerModule: 20,
  },
  ac: {
    pcsId: '',
    pcsQty: 2,
    totalPower: 10,
    transformerType: 'dry',
    transformerCapacity: 10,
  },
})

const ruleMatchStatus = computed(() => {
  if (!config.dc.containerId || !config.ac.pcsId) return null
  
  const container = containerLibrary.value.find(c => c.id === config.dc.containerId)
  const pcs = pcsLibrary.value.find(p => p.id === config.ac.pcsId)
  
  if (!container || !pcs) return null
  
  // 简单规则检查：功率配比
  const totalCapacity = container.capacity * config.dc.containerQty
  const expectedPcsPower = totalCapacity * 0.5 // 0.5C 运行
  
  if (Math.abs(pcs.power * config.ac.pcsQty - expectedPcsPower) < 1) {
    return { isValid: true, message: '配置符合规则' }
  } else {
    return { 
      isValid: false, 
      message: `功率配比异常：期望约${expectedPcsPower}MW PCS，实际${pcs.power * config.ac.pcsQty}MW` 
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
    config.ac.totalPower = pcs.power * newQty
  }
})
</script>
