<template>
  <div class="h-full flex flex-col gap-4">
    <!-- 页面标题 -->
    <div class="flex items-center justify-between">
      <h2 class="text-lg font-bold text-teal-400">调研输入</h2>
      <div class="flex items-center gap-2">
        <button 
          v-if="userRole !== 'customer'"
          @click="loadSurvey"
          class="bg-slate-600 hover:bg-slate-700 text-white text-xs px-3 py-1.5 rounded-md transition-colors">
          加载调研表
        </button>
        <button 
          v-if="userRole !== 'customer' && projectId"
          @click="saveSurvey"
          class="bg-teal-600 hover:bg-teal-700 text-white text-xs px-3 py-1.5 rounded-md transition-colors">
          保存调研表
        </button>
      </div>
    </div>

    <!-- 调研表单 -->
    <div class="flex-1 bg-slate-800/50 rounded-lg p-4 border border-slate-700 overflow-y-auto">
      <div class="space-y-6">
        <!-- 基本信息 -->
        <div>
          <h3 class="text-sm font-medium text-slate-300 mb-3 border-b border-slate-700 pb-2">基本信息</h3>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs text-slate-400 mb-1">客户名称</label>
              <input v-model="formData.customerName" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
            </div>
            <div>
              <label class="block text-xs text-slate-400 mb-1">项目名称</label>
              <input v-model="formData.projectName" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
            </div>
            <div>
              <label class="block text-xs text-slate-400 mb-1">项目地点</label>
              <input v-model="formData.location" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
            </div>
            <div>
              <label class="block text-xs text-slate-400 mb-1">项目规模</label>
              <input v-model="formData.scale" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" placeholder="MW" />
            </div>
          </div>
        </div>

        <!-- 电池系统参数 -->
        <div>
          <h3 class="text-sm font-medium text-slate-300 mb-3 border-b border-slate-700 pb-2">电池系统参数</h3>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs text-slate-400 mb-1">电池类型</label>
              <select v-model="formData.batteryType" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200">
                <option value="">-- 选择 --</option>
                <option value="LFP">磷酸铁锂电池 (LFP)</option>
                <option value="NMC">三元锂电池 (NMC)</option>
              </select>
            </div>
            <div>
              <label class="block text-xs text-slate-400 mb-1">额定能量 (MWh)</label>
              <input v-model.number="formData.ratedEnergy" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
            </div>
            <div>
              <label class="block text-xs text-slate-400 mb-1">集装箱数量</label>
              <input v-model.number="formData.containerQty" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
            </div>
            <div>
              <label class="block text-xs text-slate-400 mb-1">单集装箱容量 (MWh)</label>
              <input v-model.number="formData.containerCapacity" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
            </div>
          </div>
        </div>

        <!-- PCS参数 -->
        <div>
          <h3 class="text-sm font-medium text-slate-300 mb-3 border-b border-slate-700 pb-2">PCS系统参数</h3>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs text-slate-400 mb-1">PCS功率 (MW)</label>
              <input v-model.number="formData.pcsPower" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
            </div>
            <div>
              <label class="block text-xs text-slate-400 mb-1">PCS数量</label>
              <input v-model.number="formData.pcsQty" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
            </div>
            <div>
              <label class="block text-xs text-slate-400 mb-1">AC效率 (%)</label>
              <input v-model.number="formData.acEfficiency" type="number" step="0.01" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
            </div>
          </div>
        </div>

        <!-- 运行参数 -->
        <div>
          <h3 class="text-sm font-medium text-slate-300 mb-3 border-b border-slate-700 pb-2">运行参数</h3>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs text-slate-400 mb-1">每日循环次数</label>
              <input v-model.number="formData.cyclesPerDay" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
            </div>
            <div>
              <label class="block text-xs text-slate-400 mb-1">运行时长 (小时)</label>
              <input v-model.number="formData.duration" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
            </div>
            <div>
              <label class="block text-xs text-slate-400 mb-1">DOD (%)</label>
              <input v-model.number="formData.dod" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
            </div>
            <div>
              <label class="block text-xs text-slate-400 mb-1">环境温度 (°C)</label>
              <input v-model.number="formData.temperature" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
            </div>
          </div>
        </div>

        <!-- 能耗参数 -->
        <div>
          <h3 class="text-sm font-medium text-slate-300 mb-3 border-b border-slate-700 pb-2">辅助能耗参数</h3>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs text-slate-400 mb-1">BESS辅耗-运行 (kW)</label>
              <input v-model.number="formData.bessAuxRun" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
            </div>
            <div>
              <label class="block text-xs text-slate-400 mb-1">BESS辅耗-待机 (kW)</label>
              <input v-model.number="formData.bessAuxStandby" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
            </div>
            <div>
              <label class="block text-xs text-slate-400 mb-1">PCS辅耗-运行 (kW)</label>
              <input v-model.number="formData.pcsAuxRun" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
            </div>
            <div>
              <label class="block text-xs text-slate-400 mb-1">PCS辅耗-待机 (kW)</label>
              <input v-model.number="formData.pcsAuxStandby" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 客户填写提示 -->
    <div v-if="userRole === 'customer'" class="bg-amber-500/10 border border-amber-500/30 rounded-lg p-3">
      <p class="text-xs text-amber-400">
        提示：请填写您的项目需求信息。工程师将根据您提供的信息进行方案设计。
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'

const props = defineProps({
  projectId: String,
})

const emit = defineEmits(['apply-params'])

const userRole = ref('customer')

const formData = reactive({
  customerName: '',
  projectName: '',
  location: '',
  scale: null,
  batteryType: '',
  ratedEnergy: 5,
  containerQty: 10,
  containerCapacity: 5,
  pcsPower: 5,
  pcsQty: 2,
  acEfficiency: 97.03,
  cyclesPerDay: 1,
  duration: 2,
  dod: 80,
  temperature: 25,
  bessAuxRun: 18.124,
  bessAuxStandby: 3.5,
  pcsAuxRun: 6.5,
  pcsAuxStandby: 1.0,
})

import { ref } from 'vue'

// 初始化
onMounted(() => {
  loadUserInfo()
})

function loadUserInfo() {
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  userRole.value = user.role || 'customer'
}

// 加载调研表
async function loadSurvey() {
  if (!props.projectId) return
  
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`/api/projects/${props.projectId}/survey`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await response.json()
    if (data.success && data.data) {
      Object.assign(formData, data.data)
    }
  } catch (error) {
    console.error('加载调研表失败:', error)
  }
}

// 保存调研表
async function saveSurvey() {
  if (!props.projectId) {
    alert('请先选择项目')
    return
  }
  
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`/api/projects/${props.projectId}/survey`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(formData),
    })
    const data = await response.json()
    if (data.success) {
      alert('调研表保存成功')
    } else {
      alert('保存失败: ' + data.error)
    }
  } catch (error) {
    console.error('保存调研表失败:', error)
  }
}
</script>
