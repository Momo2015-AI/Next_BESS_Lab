<template>
  <div class="h-screen flex flex-col bg-slate-950 text-slate-100">
    <!-- Toast提示 -->
    <div v-if="toast.show" 
      :class="['fixed top-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all',
        toast.type === 'success' ? 'bg-emerald-500 text-white' : 
        toast.type === 'error' ? 'bg-red-500 text-white' : 
        toast.type === 'warning' ? 'bg-amber-500 text-white' : 'bg-slate-600 text-white']">
      {{ toast.message }}
    </div>

    <!-- 顶部导航栏 -->
    <header class="h-14 flex items-center justify-between px-4 border-b border-slate-800 bg-slate-900/80 flex-shrink-0">
      <div class="flex items-center gap-4">
        <h1 class="text-base font-bold bg-gradient-to-r from-teal-400 to-sky-400 bg-clip-text text-transparent whitespace-nowrap">
          储能解决方案平台
        </h1>
        
        <!-- 项目选择 -->
        <div class="relative">
          <select v-model="currentProjectId" @change="onProjectChange"
            class="bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs focus:border-teal-500 outline-none appearance-none cursor-pointer pr-8">
            <option value="">-- 选择项目 --</option>
            <option v-for="p in projects" :key="p.id" :value="p.id">{{ p.name }}</option>
          </select>
          <span class="absolute right-2 top-1/2 -translate-y-1/2 text-slate-500 pointer-events-none">▼</span>
        </div>
      </div>
      
      <div class="flex items-center gap-3">
        <!-- 快捷操作 -->
        <button v-if="currentProjectId && userRole !== 'customer'"
          @click="executeSimulation"
          class="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white font-bold text-xs px-4 py-1.5 rounded-md shadow-md transition-all active:scale-95 border border-emerald-400/20">
          执行仿真
        </button>
        
        <!-- 用户信息 -->
        <div class="flex items-center gap-2 pl-3 border-l border-slate-700">
          <span class="text-xs text-slate-400">{{ userRoleLabel }}</span>
          <span class="text-xs font-medium text-slate-200">{{ username }}</span>
          <button v-if="isLoggedIn" @click="logout"
            class="text-xs text-slate-500 hover:text-red-400 transition-colors ml-2">
            退出
          </button>
        </div>
      </div>
    </header>

    <!-- 主体内容区 -->
    <div class="flex-1 flex min-h-0">
      <!-- 左侧导航 -->
      <nav class="w-48 border-r border-slate-800 bg-slate-900/40 flex-shrink-0 flex flex-col">
        <!-- 工作流 -->
        <div class="p-3 border-b border-slate-800">
          <h3 class="text-[10px] text-slate-500 uppercase tracking-wider mb-2">工作流 WorkFlow</h3>
          <ul class="space-y-1">
            <li v-for="item in workflowNav" :key="item.id">
              <button @click="navigateTo(item.id)"
                :class="['w-full text-left px-2 py-1.5 rounded text-xs transition-all flex items-center gap-2',
                  currentView === item.id ? 'bg-teal-500/20 text-teal-400' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800']">
                <span>{{ item.icon }}</span>
                <span>{{ item.label }}</span>
              </button>
            </li>
          </ul>
        </div>
        
        <!-- 配置管理 -->
        <div class="p-3 flex-1 overflow-y-auto">
          <h3 class="text-[10px] text-slate-500 uppercase tracking-wider mb-2">配置管理 Config</h3>
          <ul class="space-y-1">
            <li v-for="item in configNav" :key="item.id">
              <button @click="navigateTo(item.id)"
                :class="['w-full text-left px-2 py-1.5 rounded text-xs transition-all flex items-center gap-2',
                  currentView === item.id ? 'bg-teal-500/20 text-teal-400' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800']">
                <span>{{ item.icon }}</span>
                <span>{{ item.label }}</span>
              </button>
            </li>
          </ul>
        </div>
        
        <!-- 版本信息 -->
        <div v-if="currentVersion" class="p-3 border-t border-slate-800">
          <div class="text-[10px] text-slate-500 mb-1">当前版本</div>
          <div class="text-xs text-teal-400 font-medium">{{ currentVersion.name }}</div>
          <div class="text-[10px] text-slate-500 mt-0.5">{{ currentVersion.version_num }}.0</div>
        </div>
      </nav>

      <!-- 右侧工作区 -->
      <main class="flex-1 min-w-0 overflow-hidden flex flex-col">
        <!-- 工作流视图 -->
        <div v-if="isWorkflowView" class="flex-1 overflow-y-auto p-4">
          <!-- 调研输入 -->
          <SurveyView v-if="currentView === 'survey'" 
            :project-id="currentProjectId"
            @apply-params="onApplySurveyParams" />
          
          <!-- 方案配置 -->
          <ConfigView v-if="currentView === 'config'" 
            :project-id="currentProjectId"
            :version-id="currentVersionId"
            @save-config="onSaveConfig" />
          
          <!-- 仿真分析 -->
          <SimulationView v-if="currentView === 'simulation'" 
            :project-id="currentProjectId"
            :version-id="currentVersionId"
            :params="params"
            @update-params="updateParam" />
          
          <!-- 报告输出 -->
          <ReportView v-if="currentView === 'report'" 
            :project-id="currentProjectId"
            :version-id="currentVersionId"
            :results="results" />
        </div>

        <!-- 配置管理视图 -->
        <div v-else class="flex-1 overflow-y-auto p-4">
          <!-- 产品库 -->
          <ProductConfig v-if="currentView === 'products'" />
          
          <!-- 规则配置 -->
          <RulesConfig v-if="currentView === 'rules'" />
          
          <!-- 模板管理 -->
          <TemplatesConfig v-if="currentView === 'templates'" />
          
          <!-- 历史项目 -->
          <ProjectHistory v-if="currentView === 'history'" 
            :projects="projects"
            @select-project="selectProject" />
        </div>
      </main>
    </div>

    <!-- 仿真参数面板（侧边抽屉） -->
    <div v-if="showSimulationParams" 
      class="fixed inset-0 bg-black/50 z-40 flex justify-end"
      @click.self="showSimulationParams = false">
      <div class="w-96 bg-slate-900 border-l border-slate-700 h-full overflow-y-auto p-4">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-sm font-bold text-teal-400">仿真参数</h3>
          <button @click="showSimulationParams = false" class="text-slate-500 hover:text-slate-300">✕</button>
        </div>
        <ParameterPanel :params="params" @update="updateParam" @error="showToast" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import SurveyView from './views/SurveyView.vue'
import ConfigView from './views/ConfigView.vue'
import SimulationView from './views/SimulationView.vue'
import ReportView from './views/ReportView.vue'
import RulesConfig from './views/RulesConfig.vue'
import TemplatesConfig from './views/TemplatesConfig.vue'
import ProjectHistory from './views/ProjectHistory.vue'
import ProductConfig from './components/ProductConfig.vue'
import ParameterPanel from './components/ParameterPanel.vue'

// 用户状态
const isLoggedIn = ref(false)
const username = ref('')
const userRole = ref('customer')
const userRoleLabel = computed(() => {
  const labels = { customer: '客户', engineer: '工程师', admin: '管理员' }
  return labels[userRole.value] || '访客'
})

// 项目状态
const projects = ref([])
const currentProjectId = ref('')
const currentVersionId = ref('')
const currentVersion = ref(null)

// 视图状态
const currentView = ref('survey')
const showSimulationParams = ref(false)

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

// 导航配置
const workflowNav = [
  { id: 'survey', label: '调研输入', icon: '📋' },
  { id: 'config', label: '方案设计', icon: '⚙️' },
  { id: 'simulation', label: '仿真分析', icon: '📊' },
  { id: 'report', label: '报告输出', icon: '📄' },
]

const configNav = [
  { id: 'products', label: '产品库', icon: '📦' },
  { id: 'rules', label: '规则配置', icon: '📐' },
  { id: 'templates', label: '模板管理', icon: '📑' },
  { id: 'history', label: '历史项目', icon: '📁' },
]

const isWorkflowView = computed(() => ['survey', 'config', 'simulation', 'report'].includes(currentView.value))

// 导航
function navigateTo(viewId) {
  currentView.value = viewId
}

// 加载用户信息
function loadUserInfo() {
  const token = localStorage.getItem('token')
  if (token) {
    isLoggedIn.value = true
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    username.value = user.username || '用户'
    userRole.value = user.role || 'customer'
  }
}

// 加载项目列表
async function loadProjects() {
  try {
    const token = localStorage.getItem('token')
    if (!token) return
    
    const response = await fetch('/api/projects', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await response.json()
    if (data.success) {
      projects.value = data.data || []
    }
  } catch (error) {
    console.error('加载项目失败:', error)
  }
}

// 项目变更
async function onProjectChange() {
  if (currentProjectId.value) {
    await loadProjectDetails()
  } else {
    currentVersionId.value = ''
    currentVersion.value = null
  }
}

// 加载项目详情
async function loadProjectDetails() {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`/api/projects/${currentProjectId.value}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await response.json()
    if (data.success && data.data.versions.length > 0) {
      // 找到活跃版本
      const activeVersion = data.data.versions.find(v => v.is_active) || data.data.versions[0]
      currentVersionId.value = activeVersion.id
      currentVersion.value = activeVersion
    }
  } catch (error) {
    console.error('加载项目详情失败:', error)
  }
}

// 选择项目
function selectProject(projectId) {
  currentProjectId.value = projectId
  onProjectChange()
}

// 从调研表应用参数
function onApplySurveyParams(params) {
  Object.assign(simulationParams, params)
  showToast('调研参数已应用')
}

// 保存配置
function onSaveConfig(config) {
  showToast('配置已保存')
  loadProjectDetails()
}

// 更新参数
function updateParam(key, value) {
  simulationParams[key] = value
}

// 执行仿真
function executeSimulation() {
  showSimulationParams.value = true
}

// 登出
function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  isLoggedIn.value = false
  username.value = ''
  userRole.value = 'customer'
}

// 仿真参数
const simulationParams = reactive({
  ratedEnergy: 5,
  initContainerQty: 10,
  initPcsQty: 2,
  pcsPower: 5,
  duration: 2,
  cyclesPerDay: 1,
  temperature: 25,
  acEfficiency: 97.03,
  bessAuxRun: 18.124,
  bessAuxStandby: 3.5,
  pcsAuxRun: 6.5,
  pcsAuxStandby: 1.0,
  requiredEnergy: 240,
})

// 结果数据
const results = reactive({
  initGross: [],
  initAux: [],
  initAcUsable: [],
  augGross: [],
  augAux: [],
  augAcUsable: [],
  augAccumQty: [],
  totalAcUsable: [],
  meetsReq: [],
})

// 生命周期
onMounted(() => {
  loadUserInfo()
  loadProjects()
})
</script>
