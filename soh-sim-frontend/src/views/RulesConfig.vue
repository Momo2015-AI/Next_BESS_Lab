<template>
  <div class="h-full flex flex-col gap-4">
    <!-- 页面标题 -->
    <div class="flex items-center justify-between">
      <h2 class="text-lg font-bold text-teal-400">配置规则管理</h2>
      <button 
        v-if="userRole === 'admin'"
        @click="showCreateDialog = true"
        class="bg-teal-600 hover:bg-teal-700 text-white text-xs px-3 py-1.5 rounded-md transition-colors">
        新建规则
      </button>
    </div>

    <!-- 规则列表 -->
    <div class="flex-1 bg-slate-800/50 rounded-lg p-4 border border-slate-700 overflow-y-auto">
      <div v-if="rules.length === 0" class="flex flex-col items-center justify-center h-full text-slate-500">
        <span class="text-4xl mb-2">📐</span>
        <span class="text-sm">暂无配置规则</span>
      </div>
      
      <div v-else class="space-y-3">
        <div 
          v-for="rule in rules" 
          :key="rule.id"
          class="bg-slate-700/50 rounded-lg p-4 border border-slate-600 hover:border-slate-500 transition-colors">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center gap-2 mb-1">
                <h3 class="text-sm font-medium text-slate-200">{{ rule.name }}</h3>
                <span :class="['text-[10px] px-2 py-0.5 rounded', 
                  rule.status === 'active' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-slate-600/50 text-slate-500']">
                  {{ rule.status === 'active' ? '激活' : '已禁用' }}
                </span>
              </div>
              <p class="text-xs text-slate-500 mb-3">{{ rule.description || '无描述' }}</p>
              
              <!-- 规则条件 -->
              <div class="bg-slate-800/50 rounded p-2 mb-2">
                <div class="text-xs text-slate-500 mb-1">匹配条件:</div>
                <div class="text-xs text-slate-300">
                  <span v-if="rule.conditions.containerCapacity">
                    集装箱容量 {{ rule.conditions.containerCapacity }}MWh
                  </span>
                  <span v-if="rule.conditions.dod">
                    , DOD {{ rule.conditions.dod }}%
                  </span>
                  <span v-if="rule.conditions.cyclesPerDay">
                    , 每日循环 {{ rule.conditions.cyclesPerDay }}次
                  </span>
                </div>
              </div>
              
              <!-- 规则结果 -->
              <div class="bg-slate-800/50 rounded p-2">
                <div class="text-xs text-slate-500 mb-1">配置结果:</div>
                <div class="text-xs text-slate-300">
                  建议PCS功率: {{ rule.config.suggestedPcsPower || '-' }}MW
                  <span v-if="rule.config.pcsQty">, 数量: {{ rule.config.pcsQty }}</span>
                  <span v-if="rule.config.ratio">, 配比: 1:{{ rule.config.ratio }}</span>
                </div>
              </div>
            </div>
            
            <div v-if="userRole === 'admin'" class="flex items-center gap-2 ml-4">
              <button @click="editRule(rule)" class="text-xs text-teal-400 hover:text-teal-300">编辑</button>
              <button 
                v-if="rule.status === 'active'"
                @click="toggleRule(rule)" 
                class="text-xs text-slate-400 hover:text-slate-300">禁用</button>
              <button 
                v-else
                @click="toggleRule(rule)" 
                class="text-xs text-emerald-400 hover:text-emerald-300">启用</button>
              <button @click="deleteRule(rule.id)" class="text-xs text-red-400 hover:text-red-300">删除</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 新建/编辑规则弹窗 -->
    <div v-if="showCreateDialog || editingRule" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center">
      <div class="bg-slate-800 border border-slate-700 rounded-lg p-4 w-[450px] max-h-[80vh] overflow-y-auto">
        <h3 class="text-sm font-medium text-slate-200 mb-4">
          {{ editingRule ? '编辑规则' : '新建配置规则' }}
        </h3>
        
        <div class="space-y-3">
          <div>
            <label class="block text-xs text-slate-400 mb-1">规则名称 *</label>
            <input v-model="formData.name" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200" placeholder="输入规则名称" />
          </div>
          
          <div>
            <label class="block text-xs text-slate-400 mb-1">描述</label>
            <textarea v-model="formData.description" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200 h-16" placeholder="规则描述"></textarea>
          </div>
          
          <!-- 匹配条件 -->
          <div>
            <label class="block text-xs text-slate-400 mb-2">匹配条件</label>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs text-slate-500 mb-1">集装箱容量 (MWh)</label>
                <input v-model.number="formData.conditions.containerCapacity" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-2 py-1.5 text-xs text-slate-200" />
              </div>
              <div>
                <label class="block text-xs text-slate-500 mb-1">DOD (%)</label>
                <input v-model.number="formData.conditions.dod" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-2 py-1.5 text-xs text-slate-200" />
              </div>
              <div>
                <label class="block text-xs text-slate-500 mb-1">每日循环次数</label>
                <input v-model.number="formData.conditions.cyclesPerDay" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-2 py-1.5 text-xs text-slate-200" />
              </div>
            </div>
          </div>
          
          <!-- 配置结果 -->
          <div>
            <label class="block text-xs text-slate-400 mb-2">配置结果</label>
            <div class="grid grid-cols-3 gap-3">
              <div>
                <label class="block text-xs text-slate-500 mb-1">建议PCS功率 (MW)</label>
                <input v-model.number="formData.config.suggestedPcsPower" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-2 py-1.5 text-xs text-slate-200" />
              </div>
              <div>
                <label class="block text-xs text-slate-500 mb-1">PCS数量</label>
                <input v-model.number="formData.config.pcsQty" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-2 py-1.5 text-xs text-slate-200" />
              </div>
              <div>
                <label class="block text-xs text-slate-500 mb-1">容量配比</label>
                <input v-model.number="formData.config.ratio" type="number" class="w-full bg-slate-700 border border-slate-600 rounded px-2 py-1.5 text-xs text-slate-200" placeholder="如: 2" />
              </div>
            </div>
          </div>
        </div>
        
        <div class="flex justify-end gap-2 mt-4 pt-4 border-t border-slate-700">
          <button @click="closeDialog" class="px-3 py-1.5 text-xs text-slate-400 hover:text-slate-300">取消</button>
          <button @click="saveRule" class="px-3 py-1.5 text-xs bg-teal-600 text-white rounded hover:bg-teal-700">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

const userRole = ref('customer')
const rules = ref([])
const showCreateDialog = ref(false)
const editingRule = ref(null)

const formData = reactive({
  name: '',
  description: '',
  conditions: {
    containerCapacity: null,
    dod: null,
    cyclesPerDay: null,
  },
  config: {
    suggestedPcsPower: null,
    pcsQty: null,
    ratio: null,
  },
})

// 初始化
onMounted(() => {
  loadUserInfo()
  loadRules()
})

function loadUserInfo() {
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  userRole.value = user.role || 'customer'
}

// 加载规则列表
async function loadRules() {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('/api/rules', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await response.json()
    if (data.success) {
      rules.value = data.data || []
    }
  } catch (error) {
    console.error('加载规则失败:', error)
  }
}

// 编辑规则
function editRule(rule) {
  editingRule.value = rule
  formData.name = rule.name
  formData.description = rule.description || ''
  formData.conditions = { ...rule.conditions }
  formData.config = { ...rule.config }
}

// 关闭弹窗
function closeDialog() {
  showCreateDialog.value = false
  editingRule.value = null
  resetForm()
}

// 重置表单
function resetForm() {
  formData.name = ''
  formData.description = ''
  formData.conditions = { containerCapacity: null, dod: null, cyclesPerDay: null }
  formData.config = { suggestedPcsPower: null, pcsQty: null, ratio: null }
}

// 保存规则
async function saveRule() {
  if (!formData.name.trim()) {
    alert('请输入规则名称')
    return
  }
  
  try {
    const token = localStorage.getItem('token')
    let url = '/api/rules'
    let method = 'POST'
    
    if (editingRule.value) {
      url = `/api/rules/${editingRule.value.id}`
      method = 'PUT'
    }
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(formData),
    })
    
    const data = await response.json()
    if (data.success) {
      alert(editingRule.value ? '规则更新成功' : '规则创建成功')
      closeDialog()
      loadRules()
    } else {
      alert('保存失败: ' + data.error)
    }
  } catch (error) {
    console.error('保存规则失败:', error)
    alert('保存失败')
  }
}

// 切换规则状态
async function toggleRule(rule) {
  try {
    const token = localStorage.getItem('token')
    const newStatus = rule.status === 'active' ? 'disabled' : 'active'
    const response = await fetch(`/api/rules/${rule.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ status: newStatus }),
    })
    const data = await response.json()
    if (data.success) {
      loadRules()
    }
  } catch (error) {
    console.error('切换规则状态失败:', error)
  }
}

// 删除规则
async function deleteRule(ruleId) {
  if (!confirm('确定要删除这个规则吗？')) return
  
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`/api/rules/${ruleId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await response.json()
    if (data.success) {
      loadRules()
    }
  } catch (error) {
    console.error('删除规则失败:', error)
  }
}
</script>
