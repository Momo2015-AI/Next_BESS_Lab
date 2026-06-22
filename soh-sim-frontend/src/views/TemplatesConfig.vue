<template>
  <div class="h-full flex flex-col gap-4">
    <!-- 页面标题 -->
    <div class="flex items-center justify-between">
      <h2 class="text-lg font-bold text-teal-400">校正因子模板管理</h2>
      <button 
        v-if="userRole !== 'customer'"
        @click="showCreateDialog = true"
        class="bg-teal-600 hover:bg-teal-700 text-white text-xs px-3 py-1.5 rounded-md transition-colors">
        新建模板
      </button>
    </div>

    <!-- 模板列表 -->
    <div class="flex-1 bg-slate-800/50 rounded-lg p-4 border border-slate-700 overflow-y-auto">
      <div v-if="templates.length === 0" class="flex flex-col items-center justify-center h-full text-slate-500">
        <span class="text-4xl mb-2">📑</span>
        <span class="text-sm">暂无模板</span>
      </div>
      
      <div v-else class="space-y-3">
        <div 
          v-for="template in templates" 
          :key="template.id"
          :class="['bg-slate-700/50 rounded-lg p-4 border transition-colors',
            selectedTemplate?.id === template.id ? 'border-teal-500' : 'border-slate-600 hover:border-slate-500']">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center gap-2 mb-1">
                <h3 class="text-sm font-medium text-slate-200">{{ template.name }}</h3>
                <span v-if="template.is_default" class="text-[10px] bg-teal-500/20 text-teal-400 px-2 py-0.5 rounded">默认</span>
              </div>
              <p class="text-xs text-slate-500 mb-3">{{ template.description || '无描述' }}</p>
              
              <div class="grid grid-cols-2 gap-x-4 gap-y-1 text-xs">
                <div class="flex items-center gap-2">
                  <span class="text-slate-500">SOH全局系数:</span>
                  <span class="text-slate-300">{{ template.global_soh_factor || 1.0 }}</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-slate-500">RTE全局系数:</span>
                  <span class="text-slate-300">{{ template.global_rte_factor || 1.0 }}</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-slate-500">模板类型:</span>
                  <span class="text-slate-300">{{ template.template_type || 'custom' }}</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-slate-500">状态:</span>
                  <span :class="template.status === 'active' ? 'text-emerald-400' : 'text-slate-500'">
                    {{ template.status === 'active' ? '激活' : '已归档' }}
                  </span>
                </div>
              </div>
              
              <!-- 年度校正详情 -->
              <div v-if="template.annual_corrections" class="mt-2 text-xs">
                <span class="text-slate-500">年度校正:</span>
                <div class="flex flex-wrap gap-1 mt-1">
                  <span 
                    v-for="(value, year) in parseAnnualCorrections(template.annual_corrections)" 
                    :key="year"
                    class="bg-slate-600/50 px-2 py-0.5 rounded text-slate-400">
                    {{ year }}: {{ value }}
                  </span>
                </div>
              </div>
            </div>
            
            <div v-if="userRole !== 'customer'" class="flex items-center gap-2 ml-4">
              <button @click="selectTemplate(template)" class="text-xs text-teal-400 hover:text-teal-300">编辑</button>
              <button 
                v-if="!template.is_default"
                @click="setDefault(template)" 
                class="text-xs text-sky-400 hover:text-sky-300">设为默认</button>
              <button @click="deleteTemplate(template.id)" class="text-xs text-red-400 hover:text-red-300">删除</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 新建/编辑模板弹窗 -->
    <div v-if="showCreateDialog || editingTemplate" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center">
      <div class="bg-slate-800 border border-slate-700 rounded-lg p-4 w-[450px] max-h-[80vh] overflow-y-auto">
        <h3 class="text-sm font-medium text-slate-200 mb-4">
          {{ editingTemplate ? '编辑模板' : '新建校正因子模板' }}
        </h3>
        
        <div class="space-y-3">
          <div>
            <label class="block text-xs text-slate-400 mb-1">模板名称 *</label>
            <input v-model="formData.name" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" placeholder="输入模板名称" />
          </div>
          
          <div>
            <label class="block text-xs text-slate-400 mb-1">描述</label>
            <textarea v-model="formData.description" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200 h-20" placeholder="模板描述（可选）"></textarea>
          </div>
          
          <div>
            <label class="block text-xs text-slate-400 mb-1">模板类型</label>
            <select v-model="formData.template_type" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200">
              <option value="soh">SOH专项</option>
              <option value="rte">RTE专项</option>
              <option value="comprehensive">综合</option>
              <option value="custom">自定义</option>
            </select>
          </div>
          
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs text-slate-400 mb-1">SOH全局系数</label>
              <input v-model.number="formData.global_soh_factor" type="number" step="0.001" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
            </div>
            <div>
              <label class="block text-xs text-slate-400 mb-1">RTE全局系数</label>
              <input v-model.number="formData.global_rte_factor" type="number" step="0.001" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" />
            </div>
          </div>
          
          <div>
            <label class="flex items-center gap-2 text-xs text-slate-400 mb-1">
              <input type="checkbox" v-model="formData.is_default" class="rounded border-slate-600" />
              设为默认模板
            </label>
          </div>
          
          <!-- 年度校正表 -->
          <div>
            <div class="flex items-center justify-between mb-1">
              <label class="text-xs text-slate-400">年度校正系数</label>
              <button @click="addAnnualCorrection" class="text-xs text-teal-400 hover:text-teal-300">+ 添加年度</button>
            </div>
            <div class="space-y-2">
              <div v-for="(item, index) in formData.annualCorrections" :key="index" class="flex items-center gap-2">
                <input v-model="item.year" type="text" placeholder="年份" class="bg-slate-700 border border-slate-600 rounded px-2 py-1 text-xs text-slate-200 w-20" />
                <span class="text-slate-500">年</span>
                <input v-model.number="item.value" type="number" step="0.001" placeholder="系数" class="bg-slate-700 border border-slate-600 rounded px-2 py-1 text-xs text-slate-200 w-24" />
                <button @click="removeAnnualCorrection(index)" class="text-red-400 hover:text-red-300 text-xs">删除</button>
              </div>
            </div>
          </div>
        </div>
        
        <div class="flex justify-end gap-2 mt-4 pt-4 border-t border-slate-700">
          <button @click="closeDialog" class="px-3 py-1.5 text-xs text-slate-400 hover:text-slate-300">取消</button>
          <button @click="saveTemplate" class="px-3 py-1.5 text-xs bg-teal-600 text-white rounded hover:bg-teal-700">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

const userRole = ref('customer')
const templates = ref([])
const showCreateDialog = ref(false)
const editingTemplate = ref(null)
const selectedTemplate = ref(null)

const formData = reactive({
  name: '',
  description: '',
  template_type: 'custom',
  global_soh_factor: 1.0,
  global_rte_factor: 1.0,
  is_default: false,
  annualCorrections: [],
})

// 初始化
onMounted(() => {
  loadUserInfo()
  loadTemplates()
})

function loadUserInfo() {
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  userRole.value = user.role || 'customer'
}

// 加载模板列表
async function loadTemplates() {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('/api/correction-templates', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await response.json()
    if (data.success) {
      templates.value = data.data || []
    }
  } catch (error) {
    console.error('加载模板失败:', error)
  }
}

// 解析年度校正数据
function parseAnnualCorrections(data) {
  try {
    if (typeof data === 'string') {
      return JSON.parse(data)
    }
    return data || {}
  } catch {
    return {}
  }
}

// 选择模板
function selectTemplate(template) {
  editingTemplate.value = template
  selectedTemplate.value = template
  formData.name = template.name
  formData.description = template.description || ''
  formData.template_type = template.template_type || 'custom'
  formData.global_soh_factor = template.global_soh_factor || 1.0
  formData.global_rte_factor = template.global_rte_factor || 1.0
  formData.is_default = template.is_default || false
  
  // 解析年度校正
  const annual = parseAnnualCorrections(template.annual_corrections)
  formData.annualCorrections = Object.entries(annual).map(([year, value]) => ({ year, value }))
}

// 添加年度校正
function addAnnualCorrection() {
  formData.annualCorrections.push({ year: '', value: 1.0 })
}

// 删除年度校正
function removeAnnualCorrection(index) {
  formData.annualCorrections.splice(index, 1)
}

// 关闭弹窗
function closeDialog() {
  showCreateDialog.value = false
  editingTemplate.value = null
  selectedTemplate.value = null
  resetForm()
}

// 重置表单
function resetForm() {
  formData.name = ''
  formData.description = ''
  formData.template_type = 'custom'
  formData.global_soh_factor = 1.0
  formData.global_rte_factor = 1.0
  formData.is_default = false
  formData.annualCorrections = []
}

// 保存模板
async function saveTemplate() {
  if (!formData.name.trim()) {
    alert('请输入模板名称')
    return
  }
  
  try {
    const token = localStorage.getItem('token')
    
    // 转换年度校正为对象
    const annualCorrections = {}
    formData.annualCorrections.forEach(item => {
      if (item.year && item.value !== '') {
        annualCorrections[`year_${item.year}`] = item.value
      }
    })
    
    const payload = {
      name: formData.name,
      description: formData.description,
      template_type: formData.template_type,
      global_soh_factor: formData.global_soh_factor,
      global_rte_factor: formData.global_rte_factor,
      annual_corrections: annualCorrections,
      is_default: formData.is_default,
    }
    
    let url = '/api/correction-templates'
    let method = 'POST'
    
    if (editingTemplate.value) {
      url = `/api/correction-templates/${editingTemplate.value.id}`
      method = 'PUT'
    }
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    })
    
    const data = await response.json()
    if (data.success) {
      alert(editingTemplate.value ? '模板更新成功' : '模板创建成功')
      closeDialog()
      loadTemplates()
    } else {
      alert('保存失败: ' + data.error)
    }
  } catch (error) {
    console.error('保存模板失败:', error)
    alert('保存失败')
  }
}

// 设为默认
async function setDefault(template) {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`/api/correction-templates/${template.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ is_default: true }),
    })
    const data = await response.json()
    if (data.success) {
      alert('已设为默认模板')
      loadTemplates()
    }
  } catch (error) {
    console.error('设置默认失败:', error)
  }
}

// 删除模板
async function deleteTemplate(templateId) {
  if (!confirm('确定要删除这个模板吗？')) return
  
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`/api/correction-templates/${templateId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await response.json()
    if (data.success) {
      alert('删除成功')
      loadTemplates()
    }
  } catch (error) {
    console.error('删除失败:', error)
  }
}
</script>
