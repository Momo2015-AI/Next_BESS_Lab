<template>
  <div class="survey-page min-h-screen bg-slate-950 text-slate-100 p-6">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-2xl font-bold bg-gradient-to-r from-teal-400 to-sky-400 bg-clip-text text-transparent mb-2">
            储能电站项目调研表
          </h1>
          <p class="text-sm text-slate-400">
            请填写以下信息，我们将据此为您定制最优的储能系统配置方案
          </p>
        </div>
        <button @click="goHome"
          class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm rounded-lg border border-slate-700 transition-colors">
          ← 返回系统
        </button>
      </div>

      <!-- Toast -->
      <div v-if="toast.show" :class="['fixed top-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all',
        toast.type === 'success' ? 'bg-emerald-500 text-white' : 
        toast.type === 'error' ? 'bg-red-500 text-white' : 'bg-amber-500 text-white']">
        {{ toast.message }}
      </div>

      <!-- 调研表单 -->
      <form @submit.prevent="submitSurvey" class="space-y-6">
        
        <!-- 基本信息 -->
        <div class="bg-slate-900/60 rounded-lg border border-slate-800 p-6">
          <h2 class="text-lg font-bold text-teal-400 mb-4 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-teal-400"></span>
            1. 基本信息
          </h2>
          
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm text-slate-400 mb-1">项目名称 <span class="text-red-400">*</span></label>
              <input v-model="formData.projectName" type="text" required
                placeholder="请输入项目名称"
                class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:border-teal-500 focus:outline-none">
            </div>
            <div>
              <label class="block text-sm text-slate-400 mb-1">项目地址 <span class="text-red-400">*</span></label>
              <input v-model="formData.location" type="text" required
                placeholder="省/市/区"
                class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:border-teal-500 focus:outline-none">
            </div>
            <div>
              <label class="block text-sm text-slate-400 mb-1">联系人</label>
              <input v-model="formData.contact" type="text"
                placeholder="姓名"
                class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:border-teal-500 focus:outline-none">
            </div>
            <div>
              <label class="block text-sm text-slate-400 mb-1">联系电话</label>
              <input v-model="formData.phone" type="tel"
                placeholder="手机号码"
                class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:border-teal-500 focus:outline-none">
            </div>
          </div>
        </div>

        <!-- 储能需求 -->
        <div class="bg-slate-900/60 rounded-lg border border-slate-800 p-6">
          <h2 class="text-lg font-bold text-sky-400 mb-4 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-sky-400"></span>
            2. 储能需求
          </h2>
          
          <div class="grid grid-cols-3 gap-4 mb-4">
            <div>
              <label class="block text-sm text-slate-400 mb-1">额定能量 (MWh) <span class="text-red-400">*</span></label>
              <input v-model.number="formData.ratedEnergy" type="number" step="0.1" required
                placeholder="如：10"
                class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:border-sky-500 focus:outline-none">
              <span class="text-xs text-slate-500 mt-1">电池集装箱总容量</span>
            </div>
            <div>
              <label class="block text-sm text-slate-400 mb-1">额定功率 (MW)</label>
              <input v-model.number="formData.ratedPower" type="number" step="0.1"
                placeholder="如：5"
                class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:border-sky-500 focus:outline-none">
              <span class="text-xs text-slate-500 mt-1">PCS总额定功率</span>
            </div>
            <div>
              <label class="block text-sm text-slate-400 mb-1">放电时长 (h)</label>
              <select v-model.number="formData.dischargeHours" class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:border-sky-500 focus:outline-none">
                <option :value="1">1小时</option>
                <option :value="2">2小时</option>
                <option :value="3">3小时</option>
                <option :value="4">4小时</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm text-slate-400 mb-1">应用场景 <span class="text-red-400">*</span></label>
              <select v-model="formData.application" required class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:border-sky-500 focus:outline-none">
                <option value="">请选择</option>
                <option value="调峰">调峰</option>
                <option value="调频">调频</option>
                <option value="备用电源">备用电源</option>
                <option value="峰谷套利">峰谷套利</option>
                <option value="需求响应">需求响应</option>
                <option value="微电网">微电网</option>
                <option value="其他">其他</option>
              </select>
            </div>
            <div>
              <label class="block text-sm text-slate-400 mb-1">并网电压等级</label>
              <select v-model.number="formData.voltageLevel" class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:border-sky-500 focus:outline-none">
                <option :value="10">10 kV</option>
                <option :value="35">35 kV</option>
                <option :value="110">110 kV</option>
                <option :value="220">220 kV</option>
              </select>
            </div>
          </div>
        </div>

        <!-- 运行参数 -->
        <div class="bg-slate-900/60 rounded-lg border border-slate-800 p-6">
          <h2 class="text-lg font-bold text-emerald-400 mb-4 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
            3. 运行参数
          </h2>
          
          <div class="grid grid-cols-3 gap-4 mb-4">
            <div>
              <label class="block text-sm text-slate-400 mb-1">日均循环次数</label>
              <input v-model.number="formData.cyclesPerDay" type="number" step="0.5" min="0"
                placeholder="如：1"
                class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:border-emerald-500 focus:outline-none">
              <span class="text-xs text-slate-500 mt-1">0.5 = 每2天一次</span>
            </div>
            <div>
              <label class="block text-sm text-slate-400 mb-1">DOD设置 (%)</label>
              <input v-model.number="formData.dod" type="number" step="5" min="0" max="100"
                placeholder="如：90"
                class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:border-emerald-500 focus:outline-none">
            </div>
            <div>
              <label class="block text-sm text-slate-400 mb-1">设计倍率 (C)</label>
              <select v-model.number="formData.cRate" class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:border-emerald-500 focus:outline-none">
                <option :value="0.25">0.25C (低倍率)</option>
                <option :value="0.5">0.5C (标准)</option>
                <option :value="1">1C (高倍率)</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm text-slate-400 mb-1">年平均温度 (°C)</label>
              <input v-model.number="formData.temperature" type="number"
                placeholder="如：25"
                class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:border-emerald-500 focus:outline-none">
            </div>
            <div>
              <label class="block text-sm text-slate-400 mb-1">保障年限 (年)</label>
              <input v-model.number="formData.guaranteeYears" type="number" min="1" max="30"
                placeholder="如：10"
                class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:border-emerald-500 focus:outline-none">
            </div>
          </div>
        </div>

        <!-- 电池选型 -->
        <div class="bg-slate-900/60 rounded-lg border border-slate-800 p-6">
          <h2 class="text-lg font-bold text-amber-400 mb-4 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-amber-400"></span>
            4. 电池选型偏好
          </h2>
          
          <div class="grid grid-cols-3 gap-4">
            <div>
              <label class="block text-sm text-slate-400 mb-1">电池类型</label>
              <select v-model="formData.batteryType" class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:border-amber-500 focus:outline-none">
                <option value="LFP">磷酸铁锂 (LFP)</option>
                <option value="NCM">三元锂 (NCM)</option>
                <option value="无所谓">无所谓</option>
              </select>
            </div>
            <div>
              <label class="block text-sm text-slate-400 mb-1">电芯容量偏好</label>
              <select v-model="formData.cellCapacity" class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:border-amber-500 focus:outline-none">
                <option value="280">280Ah (主流)</option>
                <option value="302">302Ah (新品)</option>
                <option value="314">314Ah (高容量)</option>
                <option value="无所谓">无所谓</option>
              </select>
            </div>
            <div>
              <label class="block text-sm text-slate-400 mb-1">集装箱规格</label>
              <select v-model="formData.containerSpec" class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:border-amber-500 focus:outline-none">
                <option value="20ft">20ft 标准柜</option>
                <option value="20ft-H">20ft 高柜 (5MWh)</option>
                <option value="40ft">40ft 标准柜</option>
              </select>
            </div>
          </div>
        </div>

        <!-- 特殊需求 -->
        <div class="bg-slate-900/60 rounded-lg border border-slate-800 p-6">
          <h2 class="text-lg font-bold text-purple-400 mb-4 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-purple-400"></span>
            5. 特殊需求（可选）
          </h2>
          
          <div class="mb-4">
            <label class="block text-sm text-slate-400 mb-2">功能需求</label>
            <div class="flex flex-wrap gap-3">
              <label v-for="feature in featureOptions" :key="feature.value" 
                class="flex items-center gap-2 bg-slate-800 px-3 py-2 rounded-lg cursor-pointer hover:bg-slate-700 transition-colors">
                <input type="checkbox" v-model="formData.features" :value="feature.value"
                  class="w-4 h-4 accent-teal-500">
                <span class="text-sm">{{ feature.label }}</span>
              </label>
            </div>
          </div>

          <div>
            <label class="block text-sm text-slate-400 mb-1">其他要求</label>
            <textarea v-model="formData.remarks" rows="3"
              placeholder="请描述其他特殊需求..."
              class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:border-purple-500 focus:outline-none resize-none"></textarea>
          </div>
        </div>

        <!-- 提交按钮 -->
        <div class="flex justify-center gap-4 pb-8">
          <button type="button" @click="resetForm"
            class="px-6 py-3 bg-slate-700 hover:bg-slate-600 text-slate-300 rounded-lg transition-colors">
            重置
          </button>
          <button type="submit"
            class="px-8 py-3 bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 hover:to-emerald-600 text-white font-bold rounded-lg transition-all shadow-lg hover:shadow-teal-500/25">
            提交调研表
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Toast
const toast = reactive({ show: false, message: '', type: 'info' })
const showToast = (message, type = 'info') => {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => { toast.show = false }, 3000)
}

// 返回主页
function goHome() {
  router.push('/')
}

// 功能选项
const featureOptions = [
  { value: 'EMS', label: '能量管理系统' },
  { value: '消防', label: '消防系统' },
  { value: '空调', label: '温控系统' },
  { value: '监控', label: '视频监控' },
  { value: '动环', label: '动环监控' },
  { value: '调频', label: '一次调频' },
]

// 表单数据
const formData = reactive({
  // 基本信息
  projectName: '',
  location: '',
  contact: '',
  phone: '',
  
  // 储能需求
  ratedEnergy: 10,
  ratedPower: 5,
  dischargeHours: 2,
  application: '',
  voltageLevel: 35,
  
  // 运行参数
  cyclesPerDay: 1,
  dod: 90,
  cRate: 0.5,
  temperature: 25,
  guaranteeYears: 10,
  
  // 电池选型
  batteryType: 'LFP',
  cellCapacity: '280',
  containerSpec: '20ft-H',
  
  // 特殊需求
  features: [],
  remarks: '',
})

// 重置表单
function resetForm() {
  Object.assign(formData, {
    projectName: '',
    location: '',
    contact: '',
    phone: '',
    ratedEnergy: 10,
    ratedPower: 5,
    dischargeHours: 2,
    application: '',
    voltageLevel: 35,
    cyclesPerDay: 1,
    dod: 90,
    cRate: 0.5,
    temperature: 25,
    guaranteeYears: 10,
    batteryType: 'LFP',
    cellCapacity: '280',
    containerSpec: '20ft-H',
    features: [],
    remarks: '',
  })
  showToast('表单已重置')
}

// 提交表单
async function submitSurvey() {
  // 验证必填项
  if (!formData.projectName) {
    showToast('请填写项目名称', 'error')
    return
  }
  if (!formData.ratedEnergy) {
    showToast('请填写额定能量', 'error')
    return
  }
  
  try {
    // 构建符合后端API的数据结构
    const surveyData = {
      project_name: formData.projectName,  // 后端期望 project_name
      location: formData.location,
      contact: formData.contact,
      phone: formData.phone,
      
      // 储能需求
      rated_energy: formData.ratedEnergy,  // 后端期望 rated_energy
      rated_power: formData.ratedPower,
      discharge_hours: formData.dischargeHours,  // 后端期望 discharge_hours
      application: formData.application,
      voltage_level: formData.voltageLevel,
      
      // 运行参数
      cycles_per_day: formData.cyclesPerDay,
      dod: formData.dod,
      c_rate: formData.cRate,
      temperature: formData.temperature,
      guarantee_years: formData.guaranteeYears,
      
      // 电池选型
      battery_type: formData.batteryType,
      cell_capacity: formData.cellCapacity,
      container_spec: formData.containerSpec,
      
      // 特殊需求
      features: formData.features,
      remarks: formData.remarks,
    }
    
    // 调用后端API
    const response = await fetch('/api/survey/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(surveyData),
    })
    
    const result = await response.json()
    
    if (response.ok) {
      // 保存到localStorage作为备份
      localStorage.setItem('currentSurveyId', result.id || result.survey_id)
      localStorage.setItem('currentSurvey', JSON.stringify({
        id: result.id || result.survey_id,
        ...formData,
        submittedAt: new Date().toISOString(),
      }))
      
      showToast('调研表提交成功！', 'success')
      
      // 跳转到系统主页
      setTimeout(() => {
        router.push('/')
      }, 1500)
    } else {
      showToast(result.error || '提交失败', 'error')
    }
    
  } catch (error) {
    console.error('提交失败:', error)
    // 网络错误时保存到localStorage
    const surveyId = 'SURV' + Date.now()
    localStorage.setItem('currentSurveyId', surveyId)
    localStorage.setItem('currentSurvey', JSON.stringify({
      id: surveyId,
      ...formData,
      submittedAt: new Date().toISOString(),
    }))
    showToast('网络错误，已保存到本地', 'warning')
    
    setTimeout(() => {
      router.push('/')
    }, 1500)
  }
}
</script>

<style scoped>
.survey-page {
  min-height: 100vh;
}
</style>