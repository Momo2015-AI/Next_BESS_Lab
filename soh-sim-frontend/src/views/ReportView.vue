<template>
  <div class="h-full flex flex-col gap-4">
    <!-- 页面标题 -->
    <div class="flex items-center justify-between">
      <h2 class="text-lg font-bold text-teal-400">报告输出</h2>
      <div class="flex items-center gap-2">
        <button 
          @click="exportReport('pdf')"
          class="bg-red-600 hover:bg-red-700 text-white text-xs px-3 py-1.5 rounded-md transition-colors">
          导出PDF
        </button>
        <button 
          @click="exportReport('excel')"
          class="bg-emerald-600 hover:bg-emerald-700 text-white text-xs px-3 py-1.5 rounded-md transition-colors">
          导出Excel
        </button>
      </div>
    </div>

    <!-- 仿真结果摘要 -->
    <div class="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
      <h3 class="text-sm font-medium text-slate-300 mb-3">仿真结果摘要</h3>
      <div class="grid grid-cols-4 gap-4">
        <div class="bg-slate-700/50 rounded-lg p-3 text-center">
          <div class="text-xs text-slate-500 mb-1">最终SOH</div>
          <div class="text-xl font-bold text-teal-400">{{ summary.finalSOH || 0 }}%</div>
        </div>
        <div class="bg-slate-700/50 rounded-lg p-3 text-center">
          <div class="text-xs text-slate-500 mb-1">最终RTE</div>
          <div class="text-xl font-bold text-sky-400">{{ summary.finalRTE || 0 }}%</div>
        </div>
        <div class="bg-slate-700/50 rounded-lg p-3 text-center">
          <div class="text-xs text-slate-500 mb-1">总循环次数</div>
          <div class="text-xl font-bold text-slate-200">{{ summary.totalCycles || 0 }}</div>
        </div>
        <div class="bg-slate-700/50 rounded-lg p-3 text-center">
          <div class="text-xs text-slate-500 mb-1">平均DOD</div>
          <div class="text-xl font-bold text-slate-200">{{ summary.avgDOD || 0 }}%</div>
        </div>
      </div>
    </div>

    <!-- SOH趋势图 -->
    <div class="flex-1 bg-slate-800/50 rounded-lg p-4 border border-slate-700 min-h-0">
      <h3 class="text-sm font-medium text-slate-300 mb-3">SOH 25年衰减趋势</h3>
      <div ref="sohChart" class="h-64 bg-slate-900/50 rounded"></div>
    </div>

    <!-- RTE趋势图 -->
    <div class="flex-1 bg-slate-800/50 rounded-lg p-4 border border-slate-700 min-h-0">
      <h3 class="text-sm font-medium text-slate-300 mb-3">RTE 25年效率趋势</h3>
      <div ref="rteChart" class="h-64 bg-slate-900/50 rounded"></div>
    </div>

    <!-- 历史对比 -->
    <div v-if="historicalResults.length > 1" class="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
      <h3 class="text-sm font-medium text-slate-300 mb-3">历史结果对比</h3>
      <div class="overflow-x-auto">
        <table class="w-full text-xs">
          <thead>
            <tr class="text-slate-500 border-b border-slate-700">
              <th class="text-left py-2 px-2">版本</th>
              <th class="text-right py-2 px-2">最终SOH</th>
              <th class="text-right py-2 px-2">最终RTE</th>
              <th class="text-right py-2 px-2">仿真日期</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="result in historicalResults" :key="result.id" class="border-b border-slate-700/50 hover:bg-slate-700/30">
              <td class="py-2 px-2 text-slate-300">{{ result.name }}</td>
              <td class="text-right py-2 px-2 text-teal-400">{{ getSummary(result).finalSOH || '-' }}%</td>
              <td class="text-right py-2 px-2 text-sky-400">{{ getSummary(result).finalRTE || '-' }}%</td>
              <td class="text-right py-2 px-2 text-slate-500">{{ formatDate(result.created_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  projectId: String,
  versionId: String,
  results: Object,
})

const sohChart = ref(null)
const rteChart = ref(null)
const historicalResults = ref([])

const summary = reactive({
  finalSOH: 0,
  finalRTE: 0,
  totalCycles: 0,
  avgDOD: 0,
})

// 初始化
onMounted(() => {
  loadHistoricalResults()
  initCharts()
})

// 卸载时清理图表
onUnmounted(() => {
  // 清理操作
})

// 加载历史结果
async function loadHistoricalResults() {
  if (!props.versionId) return
  
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`/api/versions/${props.versionId}/results`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await response.json()
    if (data.success && data.data.length > 0) {
      historicalResults.value = data.data
      
      // 使用最新结果作为当前显示
      const latest = data.data[0]
      const resultSummary = getSummary(latest)
      Object.assign(summary, resultSummary)
    }
  } catch (error) {
    console.error('加载历史结果失败:', error)
  }
}

// 获取结果摘要
function getSummary(result) {
  try {
    if (result.summary) {
      return typeof result.summary === 'string' ? JSON.parse(result.summary) : result.summary
    }
    return {}
  } catch {
    return {}
  }
}

// 初始化图表
function initCharts() {
  // 简单的图表实现
  if (sohChart.value) {
    sohChart.value.innerHTML = '<div class="flex items-center justify-center h-full text-slate-500 text-sm">SOH趋势图</div>'
  }
  if (rteChart.value) {
    rteChart.value.innerHTML = '<div class="flex items-center justify-center h-full text-slate-500 text-sm">RTE趋势图</div>'
  }
}

// 导出报告
async function exportReport(format) {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`/api/export/${props.versionId}?format=${format}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    if (response.ok) {
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `储能方案报告_${new Date().toISOString().split('T')[0]}.${format}`
      a.click()
      window.URL.revokeObjectURL(url)
    }
  } catch (error) {
    console.error('导出失败:', error)
    alert('导出失败')
  }
}

// 格式化日期
function formatDate(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}
</script>
