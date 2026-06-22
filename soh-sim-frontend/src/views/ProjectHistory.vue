<template>
  <div class="h-full flex flex-col gap-4">
    <!-- 页面标题 -->
    <div class="flex items-center justify-between">
      <h2 class="text-lg font-bold text-teal-400">历史项目</h2>
    </div>

    <!-- 项目列表 -->
    <div class="flex-1 bg-slate-800/50 rounded-lg p-4 border border-slate-700 overflow-y-auto">
      <div v-if="projects.length === 0" class="flex flex-col items-center justify-center h-full text-slate-500">
        <span class="text-4xl mb-2">📁</span>
        <span class="text-sm">暂无历史项目</span>
      </div>
      
      <div v-else class="space-y-3">
        <div 
          v-for="project in projects" 
          :key="project.id"
          class="bg-slate-700/50 rounded-lg p-4 border border-slate-600 hover:border-slate-500 transition-colors cursor-pointer"
          @click="$emit('select-project', project.id)">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center gap-2 mb-1">
                <h3 class="text-sm font-medium text-slate-200">{{ project.name }}</h3>
                <span :class="['text-[10px] px-2 py-0.5 rounded',
                  project.status === 'active' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-slate-600/50 text-slate-500']">
                  {{ project.status === 'active' ? '进行中' : '已归档' }}
                </span>
              </div>
              
              <div class="grid grid-cols-2 gap-x-4 gap-y-1 text-xs mb-3">
                <div class="flex items-center gap-2">
                  <span class="text-slate-500">客户:</span>
                  <span class="text-slate-400">{{ project.customer_name || '-' }}</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-slate-500">阶段:</span>
                  <span class="text-slate-400">{{ getStageLabel(project.stage) }}</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-slate-500">创建日期:</span>
                  <span class="text-slate-400">{{ formatDate(project.created_at) }}</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-slate-500">版本数:</span>
                  <span class="text-slate-400">{{ project.versions?.length || 0 }}</span>
                </div>
              </div>
              
              <!-- 版本列表 -->
              <div v-if="project.versions && project.versions.length > 0" class="mt-2">
                <div class="text-xs text-slate-500 mb-1">版本历史:</div>
                <div class="flex flex-wrap gap-2">
                  <div 
                    v-for="version in project.versions.slice(0, 5)" 
                    :key="version.id"
                    :class="['px-2 py-1 rounded text-xs cursor-pointer',
                      version.is_active ? 'bg-teal-500/20 text-teal-400' : 'bg-slate-600/50 text-slate-400 hover:bg-slate-600']">
                    {{ version.name }}
                  </div>
                  <span v-if="project.versions.length > 5" class="px-2 py-1 text-xs text-slate-500">
                    +{{ project.versions.length - 5 }} 更多
                  </span>
                </div>
              </div>
            </div>
            
            <div class="flex items-center gap-2 ml-4">
              <button 
                v-if="userRole !== 'customer'"
                @click.stop="viewProjectDetail(project)"
                class="text-xs text-teal-400 hover:text-teal-300">
                查看
              </button>
              <button 
                v-if="userRole !== 'customer'"
                @click.stop="archiveProject(project.id)"
                class="text-xs text-slate-400 hover:text-slate-300">
                归档
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 项目详情弹窗 -->
    <div v-if="selectedProject" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center">
      <div class="bg-slate-800 border border-slate-700 rounded-lg p-4 w-[600px] max-h-[80vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-sm font-medium text-slate-200">{{ selectedProject.name }} - 详情</h3>
          <button @click="selectedProject = null" class="text-slate-500 hover:text-slate-300">✕</button>
        </div>
        
        <div class="space-y-4">
          <!-- 基本信息 -->
          <div class="bg-slate-700/50 rounded-lg p-3">
            <h4 class="text-xs text-slate-400 mb-2">基本信息</h4>
            <div class="grid grid-cols-2 gap-2 text-xs">
              <div><span class="text-slate-500">客户:</span> {{ selectedProject.customer_name || '-' }}</div>
              <div><span class="text-slate-500">地点:</span> {{ selectedProject.location || '-' }}</div>
              <div><span class="text-slate-500">规模:</span> {{ selectedProject.scale || '-' }}MW</div>
              <div><span class="text-slate-500">状态:</span> {{ selectedProject.status }}</div>
            </div>
          </div>
          
          <!-- 版本列表 -->
          <div>
            <h4 class="text-xs text-slate-400 mb-2">版本列表</h4>
            <div class="space-y-2">
              <div 
                v-for="version in selectedProject.versions" 
                :key="version.id"
                class="bg-slate-700/50 rounded p-3 border border-slate-600">
                <div class="flex items-center justify-between">
                  <div>
                    <span class="text-sm text-slate-200">{{ version.name }}</span>
                    <span v-if="version.is_active" class="ml-2 text-[10px] bg-teal-500/20 text-teal-400 px-2 py-0.5 rounded">当前版本</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="text-xs text-slate-500">{{ formatDate(version.created_at) }}</span>
                    <button 
                      v-if="!version.is_active && userRole !== 'customer'"
                      @click="activateVersion(selectedProject.id, version.id)"
                      class="text-xs text-sky-400 hover:text-sky-300">
                      激活
                    </button>
                  </div>
                </div>
                <p v-if="version.description" class="text-xs text-slate-500 mt-1">{{ version.description }}</p>
                
                <!-- 该版本的仿真结果 -->
                <div v-if="version.simulation_results && version.simulation_results.length > 0" class="mt-2">
                  <div class="text-xs text-slate-500">仿真结果:</div>
                  <div class="flex flex-wrap gap-1 mt-1">
                    <span 
                      v-for="result in version.simulation_results" 
                      :key="result.id"
                      class="bg-slate-600/50 px-2 py-0.5 rounded text-xs text-slate-400">
                      {{ result.name }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  projects: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['select-project'])

const userRole = ref('customer')
const selectedProject = ref(null)

onMounted(() => {
  loadUserInfo()
})

function loadUserInfo() {
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  userRole.value = user.role || 'customer'
}

function getStageLabel(stage) {
  const stages = {
    survey: '调研中',
    design: '设计中',
    simulation: '仿真中',
    review: '审核中',
    completed: '已完成',
  }
  return stages[stage] || stage
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

async function viewProjectDetail(project) {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`/api/projects/${project.id}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await response.json()
    if (data.success) {
      selectedProject.value = data.data
    }
  } catch (error) {
    console.error('加载项目详情失败:', error)
  }
}

async function activateVersion(projectId, versionId) {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`/api/versions/${versionId}/activate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    })
    const data = await response.json()
    if (data.success) {
      alert('版本已激活')
      selectedProject.value = null
    }
  } catch (error) {
    console.error('激活版本失败:', error)
  }
}

async function archiveProject(projectId) {
  if (!confirm('确定要归档这个项目吗？')) return
  
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`/api/projects/${projectId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ status: 'archived' }),
    })
    const data = await response.json()
    if (data.success) {
      alert('项目已归档')
    }
  } catch (error) {
    console.error('归档项目失败:', error)
  }
}
</script>
