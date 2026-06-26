<template>
  <aside class="sidebar w-64 flex-shrink-0 overflow-hidden flex flex-col" style="background-color: #FFFFFF; border-right: 1px solid #E0E0E0;">
    <nav class="flex-1 overflow-y-auto p-3">
      <div class="mb-6">
        <div class="text-xs font-semibold uppercase tracking-wider mb-2 px-2" style="color: #999999;">{{ $t('sidebar.home') }}</div>
        <button 
          @click="$emit('navigate', 'home')"
          class="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all"
          :class="activeTab === 'home' ? 'sidebar-active' : 'sidebar-item'">
          <span>🏠</span>
          <span>{{ $t('sidebar.home') }}</span>
        </button>
      </div>

      <div class="mb-6">
        <div class="text-xs font-semibold uppercase tracking-wider mb-2 px-2" style="color: #999999;">{{ $t('sidebar.foundation') }}</div>
        <div v-for="item in foundationItems" :key="item.id">
          <button 
            @click="$emit('navigate', item.id)"
            class="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all"
            :class="activeTab === item.id ? 'sidebar-active' : 'sidebar-item'">
            <span>{{ item.icon }}</span>
            <span>{{ item.label }}</span>
          </button>
        </div>
      </div>

      <div class="mb-6">
        <div class="text-xs font-semibold uppercase tracking-wider mb-2 px-2" style="color: #999999;">{{ $t('sidebar.solution') }}</div>
        <div v-for="item in solutionItems" :key="item.id">
          <button 
            @click="$emit('navigate', item.id)"
            class="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all"
            :class="activeTab === item.id ? 'sidebar-active' : 'sidebar-item'">
            <span>{{ item.icon }}</span>
            <span>{{ item.label }}</span>
          </button>
        </div>
      </div>

      <div class="mb-6">
        <div class="text-xs font-semibold uppercase tracking-wider mb-2 px-2" style="color: #999999;">{{ $t('sidebar.tools') }}</div>
        <div v-for="item in toolItems" :key="item.id">
          <button 
            @click="$emit('navigate', item.id)"
            class="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all"
            :class="activeTab === item.id ? 'sidebar-active' : 'sidebar-item'">
            <span>{{ item.icon }}</span>
            <span>{{ item.label }}</span>
          </button>
        </div>
      </div>
    </nav>

    <div class="p-4 border-t" style="border-color: #E0E0E0;">
      <button
        @click="$emit('navigate', 'auth')"
        class="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all"
        :class="activeTab === 'auth' ? 'sidebar-active' : 'sidebar-item'">
        <span>🔐</span>
        <span>{{ $t('sidebar.auth') }}</span>
      </button>
      <button
        @click="onClearDrafts"
        class="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all sidebar-item">
        <span>🧹</span>
        <span>清除草稿缓存</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { ref } from 'vue'
import { clearAllDrafts, listDrafts } from '../composables/useDraft'

defineProps({
  activeTab: {
    type: String,
    default: 'home'
  }
})

const emit = defineEmits(['navigate'])

function onClearDrafts() {
  const keys = listDrafts()
  if (keys.length === 0) {
    alert('当前没有草稿缓存')
    return
  }
  if (confirm(`确定清除 ${keys.length} 项草稿缓存？此操作不可恢复，已提交到数据库的数据不受影响。`)) {
    clearAllDrafts()
    alert('草稿缓存已清除，页面将刷新以应用默认值')
    location.reload()
  }
}

const foundationItems = ref([
  { id: 'survey', label: '项目调研表', icon: '📋' },
  { id: 'param', label: '参数配置面板', icon: '⚙️' },
  { id: 'conditions', label: '运行工况', icon: '📊' },
  { id: 'products', label: '产品与方案配置', icon: '📦' },
  { id: 'batteryPCS', label: '电池与PCS配对', icon: '🔌' },
  { id: 'formula', label: '算法与公式', icon: '📐' },
])

const solutionItems = ref([
  { id: 'dc-design', label: '直流侧设计', icon: '🔋' },
  { id: 'ac-design', label: '交流侧设计', icon: '⚡' },
  { id: 'simulationLab', label: '仿真实验室', icon: '🧪' },
  { id: 'financial', label: '财务看板', icon: '💰' },
  { id: 'matrix', label: '生命周期矩阵', icon: '📈' },
  { id: 'inject', label: '数据注入', icon: '💉' },
  { id: 'chart', label: '可视化图表', icon: '📉' },
  { id: 'scenario', label: '多场景对比', icon: '🔄' },
  { id: 'sensitivity', label: '敏感性分析', icon: '🎯' },
  { id: 'engineering', label: '工程计算', icon: '📐' },
  { id: 'auxPower', label: '辅助功耗计算', icon: '⚙️' },
  { id: 'export', label: '数据导出', icon: '📥' },
])

const toolItems = ref([
  { id: 'auxPower', label: '辅助功耗计算', icon: '⚙️' },
])
</script>

<style scoped>
.sidebar-item {
  color: #666666;
  cursor: pointer;
}

.sidebar-item:hover {
  background-color: #F5F7FA;
  color: #2F5496;
}

.sidebar-active {
  background-color: #E8EEF5;
  color: #2F5496;
  font-weight: 600;
}
</style>
