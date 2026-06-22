<template>
  <div class="export-panel p-4">
    <div class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
      <h3 class="text-sm font-bold mb-4 flex items-center gap-2" style="color: var(--color-accent-secondary);">
        <span class="w-2 h-2 rounded-full" style="background-color: var(--color-accent-secondary);"></span>
        数据导出
      </h3>

      <div class="grid grid-cols-2 gap-4">
        <!-- 导出类型选择 -->
        <div class="space-y-3">
          <div class="text-xs mb-2" style="color: var(--color-text-muted);">选择导出内容</div>
          
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" v-model="exportOptions.matrix" style="accent-color: var(--color-accent-secondary);">
            <span class="text-xs" style="color: var(--color-text-secondary);">25年生命周期矩阵</span>
          </label>
          
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" v-model="exportOptions.soh" style="accent-color: var(--color-accent-secondary);">
            <span class="text-xs" style="color: var(--color-text-secondary);">SOH/RTE数据序列</span>
          </label>
          
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" v-model="exportOptions.params" style="accent-color: var(--color-accent-secondary);">
            <span class="text-xs" style="color: var(--color-text-secondary);">参数配置</span>
          </label>
          
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" v-model="exportOptions.financial" style="accent-color: var(--color-accent-secondary);">
            <span class="text-xs" style="color: var(--color-text-secondary);">财务分析数据</span>
          </label>
        </div>

        <!-- 导出操作 -->
        <div class="space-y-3">
          <div class="text-xs mb-2" style="color: var(--color-text-muted);">导出格式</div>
          
          <button @click="exportCSV" :disabled="exporting"
            class="w-full text-xs px-4 py-2 rounded-lg transition-all flex items-center justify-center gap-2"
            :style="exporting ? { backgroundColor: 'var(--color-border)', color: 'var(--color-text-muted)' } : { backgroundColor: 'var(--color-accent-secondary)', color: 'white' }"
            onmouseover="if(!this.disabled) this.style.opacity='0.9';"
            onmouseout="if(!this.disabled) this.style.opacity='1';">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            {{ exporting ? '导出中...' : '导出 CSV' }}
          </button>
          
          <button @click="exportPNG" :disabled="exporting"
            class="w-full text-xs px-4 py-2 rounded-lg transition-all flex items-center justify-center gap-2"
            :style="exporting ? { backgroundColor: 'var(--color-border)', color: 'var(--color-text-muted)' } : { backgroundColor: 'var(--color-accent)', color: 'white' }"
            onmouseover="if(!this.disabled) this.style.opacity='0.9';"
            onmouseout="if(!this.disabled) this.style.opacity='1';">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
            导出 PNG 图表
          </button>
          
          <button @click="saveSimulation" :disabled="saving"
            class="w-full text-xs px-4 py-2 rounded-lg transition-all flex items-center justify-center gap-2"
            :style="saving ? { backgroundColor: 'var(--color-border)', color: 'var(--color-text-muted)' } : { backgroundColor: 'var(--color-warning)', color: 'white' }"
            onmouseover="if(!this.disabled) this.style.opacity='0.9';"
            onmouseout="if(!this.disabled) this.style.opacity='1';">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"></path>
            </svg>
            {{ saving ? '保存中...' : '保存仿真结果' }}
          </button>
        </div>
      </div>

      <!-- 历史仿真记录 -->
      <div class="mt-4 pt-4 border-t" style="border-color: var(--color-border);">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs" style="color: var(--color-text-muted);">历史仿真记录</span>
          <button @click="loadSimulations" class="text-xs" style="color: var(--color-accent-secondary);" onmouseover="this.style.color='var(--color-accent)';" onmouseout="this.style.color='var(--color-accent-secondary)';">
            刷新
          </button>
        </div>
        
        <div v-if="simulations.length === 0" class="text-xs text-center py-2" style="color: var(--color-text-muted);">
          暂无保存的仿真记录
        </div>
        
        <div v-else class="space-y-2 max-h-40 overflow-y-auto">
          <div v-for="sim in simulations" :key="sim.id"
            class="flex items-center justify-between rounded px-3 py-2 text-xs" style="background-color: var(--color-card-dark);">
            <div>
              <span style="color: var(--color-text-secondary);">{{ sim.name }}</span>
              <span style="color: var(--color-text-muted);" class="ml-2">{{ sim.created_at }}</span>
            </div>
            <div class="flex gap-2">
              <button @click="loadSimulation(sim.id)" style="color: var(--color-accent-secondary);" onmouseover="this.style.color='var(--color-accent)';" onmouseout="this.style.color='var(--color-accent-secondary)';">加载</button>
              <button @click="exportSimulationCSV(sim.id)" style="color: var(--color-accent);" onmouseover="this.style.color='var(--color-accent-secondary)';" onmouseout="this.style.color='var(--color-accent)';">导出</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast提示 -->
    <div v-if="toast.show" class="fixed bottom-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all"
      :style="toast.type === 'success' ? { backgroundColor: 'var(--color-success)', color: 'white' } : { backgroundColor: 'var(--color-danger)', color: 'white' }">
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const props = defineProps({
  params: { type: Object, default: () => ({}) },
  results: { type: Object, default: () => ({}) },
  soh: { type: Array, default: () => [] },
  rte: { type: Array, default: () => [] },
  dod: { type: Array, default: () => [] },
  augQty: { type: Array, default: () => [] },
  financial: { type: Object, default: () => ({}) },
  projectId: { type: String, default: '' },
})

const emit = defineEmits(['load-simulation', 'show-toast'])

const exportOptions = reactive({
  matrix: true,
  soh: true,
  params: true,
  financial: false,
})

const exporting = ref(false)
const saving = ref(false)
const simulations = ref([])

const toast = reactive({
  show: false,
  message: '',
  type: 'success',
})

const showToast = (message, type = 'success') => {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => {
    toast.show = false
  }, 3000)
}

// 导出CSV
async function exportCSV() {
  if (!exportOptions.matrix && !exportOptions.soh && !exportOptions.params && !exportOptions.financial) {
    showToast('请选择至少一项导出内容', 'error')
    return
  }

  exporting.value = true

  try {
    let endpoint = '/api/export/csv'
    let exportType = 'all'
    
    if (exportOptions.matrix && !exportOptions.soh && !exportOptions.params) {
      exportType = 'matrix'
    } else if (exportOptions.soh && !exportOptions.matrix && !exportOptions.params) {
      exportType = 'soh'
    } else if (exportOptions.params && !exportOptions.matrix && !exportOptions.soh) {
      exportType = 'params'
    }

    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        type: exportType,
        results: props.results,
        params: props.params,
        soh: props.soh,
        rte: props.rte,
        dod: props.dod,
        augQty: props.augQty,
      }),
    })

    if (!response.ok) throw new Error('导出失败')

    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `soh_export_${new Date().toISOString().slice(0, 10)}.csv`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)

    showToast('CSV导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    showToast('导出失败: ' + error.message, 'error')
  } finally {
    exporting.value = false
  }
}

// 导出PNG
function exportPNG() {
  exporting.value = true

  try {
    // 查找所有ECharts图表
    const charts = document.querySelectorAll('.echarts-instance, canvas')
    
    if (charts.length === 0) {
      showToast('未找到可导出的图表', 'error')
      return
    }

    let exportedCount = 0
    charts.forEach((chart, index) => {
      if (chart.tagName === 'CANVAS') {
        const dataUrl = chart.toDataURL('image/png')
        const link = document.createElement('a')
        link.download = `soh_chart_${index + 1}_${new Date().toISOString().slice(0, 10)}.png`
        link.href = dataUrl
        link.click()
        exportedCount++
      }
    })

    // 如果没有canvas，尝试导出整个页面
    if (exportedCount === 0) {
      showToast('请在图表视图中导出', 'error')
      return
    }

    showToast(`成功导出 ${exportedCount} 张图表`)
  } catch (error) {
    console.error('PNG导出失败:', error)
    showToast('PNG导出失败', 'error')
  } finally {
    exporting.value = false
  }
}

// 保存仿真结果
async function saveSimulation() {
  saving.value = true

  try {
    const response = await fetch('/api/export/simulation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        project_id: props.projectId,
        name: `仿真_${new Date().toLocaleString()}`,
        params: props.params,
        results: props.results,
        soh: props.soh,
        rte: props.rte,
        dod: props.dod,
        augQty: props.augQty,
        financial: props.financial,
      }),
    })

    const result = await response.json()
    
    if (result.success) {
      showToast('仿真结果已保存')
      loadSimulations()
    } else {
      throw new Error(result.error)
    }
  } catch (error) {
    console.error('保存失败:', error)
    showToast('保存失败: ' + error.message, 'error')
  } finally {
    saving.value = false
  }
}

// 加载仿真列表
async function loadSimulations() {
  try {
    const response = await fetch('/api/simulation/list')
    const data = await response.json()
    simulations.value = data.simulations || []
  } catch (error) {
    console.error('加载仿真列表失败:', error)
  }
}

// 加载仿真结果
async function loadSimulation(simulationId) {
  try {
    const response = await fetch(`/api/simulation/${simulationId}`)
    const data = await response.json()
    
    emit('load-simulation', data)
    showToast('仿真结果已加载')
  } catch (error) {
    console.error('加载仿真失败:', error)
    showToast('加载失败', 'error')
  }
}

// 导出历史仿真CSV
async function exportSimulationCSV(simulationId) {
  try {
    const response = await fetch(`/api/simulation/${simulationId}`)
    const data = await response.json()
    
    if (data) {
      const csvContent = generateCSV(data)  // 传入完整data对象
      const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.download = `${data.name || 'simulation'}_${new Date().toISOString().slice(0, 10)}.csv`
      link.href = url
      link.click()
      window.URL.revokeObjectURL(url)
      showToast('导出成功')
    }
  } catch (error) {
    console.error('导出失败:', error)
    showToast('导出失败', 'error')
  }
}

// 生成CSV内容
function generateCSV(data) {
  let csv = '储能电站SOH仿真计算结果\n\n'
  
  // 矩阵数据
  if (data.results) {
    csv += '25年生命周期矩阵\n'
    csv += '年份,初始Gross(MWh),初始Aux(MWh),初始净可用(MWh),扩容Gross(MWh),扩容Aux(MWh),扩容净可用(MWh),总净可用(MWh),累计扩容,满足需求\n'
    
    const r = data.results
    for (let i = 0; i < 26; i++) {
      csv += `${i},${r.initGross?.[i]?.toFixed(2) || 0},${r.initAux?.[i]?.toFixed(2) || 0},${r.initAcUsable?.[i]?.toFixed(2) || 0},`
      csv += `${r.augGross?.[i]?.toFixed(2) || 0},${r.augAux?.[i]?.toFixed(2) || 0},${r.augAcUsable?.[i]?.toFixed(2) || 0},`
      csv += `${r.totalAcUsable?.[i]?.toFixed(2) || 0},${r.augAccumQty?.[i] || 0},${r.meetsReq?.[i] ? '是' : '否'}\n`
    }
  }
  
  // SOH数据
  if (data.soh && data.soh.length > 0) {
    csv += '\nSOH/RTE数据\n年份,SOH(%),RTE(%)\n'
    for (let i = 0; i < data.soh.length; i++) {
      csv += `${i},${(data.soh[i] * 100).toFixed(2)},${data.rte?.[i] ? (data.rte[i] * 100).toFixed(2) : ''}\n`
    }
  }
  
  return csv
}

// 初始化加载
loadSimulations()
</script>

<style scoped>
.export-panel {
  height: 100%;
}
</style>