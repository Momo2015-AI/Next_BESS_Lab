<template>
  <div class="export-panel p-4">
    <div class="rounded-lg p-4 card-bordered">
      <h3 class="text-sm font-bold mb-4 flex items-center gap-2 text-accent-2">
        <span class="w-2 h-2 rounded-full bg-accent-2" />
        {{ $t('dataExport.title') }}
      </h3>

      <div class="grid grid-cols-2 gap-4">
        <!-- 导出类型选择 -->
        <div class="space-y-3">
          <div class="text-xs mb-2 text-muted">{{ $t('dataExport.selectContent') }}</div>

          <label class="flex items-center gap-2 cursor-pointer">
            <input v-model="exportOptions.matrix" type="checkbox" />
            class="accent-accent-2"
            <span class="text-xs text-secondary">{{ $t('dataExport.matrix') }}</span>
          </label>

          <label class="flex items-center gap-2 cursor-pointer">
            <input v-model="exportOptions.soh" type="checkbox" />
            class="accent-accent-2"
            <span class="text-xs text-secondary">{{ $t('dataExport.sohRte') }}</span>
          </label>

          <label class="flex items-center gap-2 cursor-pointer">
            <input v-model="exportOptions.params" type="checkbox" />
            class="accent-accent-2"
            <span class="text-xs text-secondary">{{ $t('dataExport.params') }}</span>
          </label>

          <label class="flex items-center gap-2 cursor-pointer">
            <input v-model="exportOptions.financial" type="checkbox" class="accent-accent-2" />
            <span class="text-xs text-secondary">{{ $t('dataExport.financial') }}</span>
          </label>
        </div>

        <!-- 导出操作 -->
        <div class="space-y-3">
          <div class="text-xs mb-2 text-muted">{{ $t('dataExport.exportFormat') }}</div>

          <button
            :disabled="exporting"
            class="export-action-btn w-full text-xs px-4 py-2 rounded-lg transition-all flex items-center justify-center gap-2"
            :class="exporting ? 'btn-disabled' : 'bg-accent-2 text-white'"
            @click="exportCSV"
          >
            <AppIcon name="download" size="16" />
            {{ exporting ? $t('dataExport.exporting') : $t('dataExport.exportCsv') }}
          </button>

          <button
            :disabled="exporting"
            class="export-action-btn w-full text-xs px-4 py-2 rounded-lg transition-all flex items-center justify-center gap-2"
            :class="exporting ? 'btn-disabled' : 'bg-accent text-white'"
            @click="exportPNG"
          >
            <AppIcon name="image" size="16" />
            {{ $t('dataExport.exportPng') }}
          </button>

          <button
            :disabled="saving"
            class="export-action-btn w-full text-xs px-4 py-2 rounded-lg transition-all flex items-center justify-center gap-2"
            :class="saving ? 'btn-disabled' : 'bg-warning text-white'"
            @click="saveSimulation"
          >
            <AppIcon name="save" size="16" />
            {{ saving ? $t('dataExport.saving') : $t('dataExport.saveResult') }}
          </button>
        </div>
      </div>

      <!-- 历史仿真记录 -->
      <div class="mt-4 pt-4 border-t border-default">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs text-muted">{{ $t('dataExport.history') }}</span>
          <button class="link-btn text-xs" @click="loadSimulations">{{ $t('dataExport.refresh') }}</button>
        </div>

        <div v-if="simulations.length === 0" class="text-xs text-center py-2 text-muted">
          {{ $t('dataExport.noHistory') }}
        </div>

        <div v-else class="space-y-2 max-h-40 overflow-y-auto">
          <div
            v-for="sim in simulations"
            :key="sim.id"
            class="flex items-center justify-between rounded px-3 py-2 text-xs bg-card-dark"
          >
            <div>
              <span>{{ sim.name }}</span>
              class="text-secondary"
              <span class="ml-2 text-muted">{{ sim.created_at }}</span>
            </div>
            <div class="flex gap-2">
              <button class="link-btn" @click="loadSimulation(sim.id)">{{ $t('dataExport.load') }}</button>
              <button class="link-btn text-accent" @click="exportSimulationCSV(sim.id)">
                {{ $t('dataExport.export') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast提示 -->
    <div
      v-if="toast.show"
      class="fixed bottom-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all"
      :class="toast.type === 'success' ? 'toast-success' : 'toast-error'"
    >
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useI18n } from 'vue-i18n'
import { useBessStore } from '../stores/bess.js'
import AppIcon from './AppIcon.vue'
import api from '../services/api.js'

const { t } = useI18n()
const store = useBessStore()

const props = defineProps({
  params: { type: Object, default: () => ({}) },
  results: { type: Object, default: () => ({}) },
  soh: { type: Array, default: () => [] },
  rte: { type: Array, default: () => [] },
  dod: { type: Array, default: () => [] },
  augQty: { type: Array, default: () => [] },
  financial: { type: Object, default: () => ({}) },
  projectId: { type: String, default: '' }
})

const emit = defineEmits(['load-simulation', 'show-toast'])

const exportOptions = reactive({
  matrix: true,
  soh: true,
  params: true,
  financial: false
})

const exporting = ref(false)
const saving = ref(false)
const simulations = ref([])

const toast = reactive({
  show: false,
  message: '',
  type: 'success'
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
    showToast(t('dataExport.selectAtLeastOne'), 'error')
    return
  }

  exporting.value = true

  try {
    const endpoint = '/api/export/csv'
    let exportType = 'all'

    if (exportOptions.matrix && !exportOptions.soh && !exportOptions.params) {
      exportType = 'matrix'
    } else if (exportOptions.soh && !exportOptions.matrix && !exportOptions.params) {
      exportType = 'soh'
    } else if (exportOptions.params && !exportOptions.matrix && !exportOptions.soh) {
      exportType = 'params'
    }

    const blob = await api.download(endpoint, {
      type: exportType,
      results: props.results,
      params: props.params,
      soh: props.soh,
      rte: props.rte,
      dod: props.dod,
      augQty: props.augQty
    })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `soh_export_${new Date().toISOString().slice(0, 10)}.csv`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)

    showToast(t('dataExport.csvSuccess'))
  } catch (error) {
    console.error('Export failed:', error)
    showToast(t('dataExport.exportFailedWithError', { message: error.message }), 'error')
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
      showToast(t('dataExport.noChartToExport'), 'error')
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
      showToast(t('dataExport.exportInChartView'), 'error')
      return
    }

    showToast(t('dataExport.pngSuccess', { count: exportedCount }))
  } catch (error) {
    console.error('PNG export failed:', error)
    showToast(t('dataExport.exportFailed'), 'error')
  } finally {
    exporting.value = false
  }
}

// 保存仿真结果
async function saveSimulation() {
  saving.value = true

  try {
    const result = await api.post('/api/export/simulation', {
      project_id: props.projectId,
      name: t('dataExport.simSaveName', { date: new Date().toLocaleString() }),
      params: props.params,
      results: props.results,
      soh: props.soh,
      rte: props.rte,
      dod: props.dod,
      augQty: props.augQty,
      financial: props.financial
    })

    if (result.success) {
      showToast(t('dataExport.resultSaved'))
      loadSimulations()
    } else {
      throw new Error(result.error)
    }
  } catch (error) {
    console.error('Save failed:', error)
    showToast(t('dataExport.saveFailedWithError', { message: error.message }), 'error')
  } finally {
    saving.value = false
  }
}

// 加载仿真列表
async function loadSimulations() {
  try {
    const data = await api.get('/api/simulation/list')
    simulations.value = data.simulations || []
  } catch (error) {
    console.error('加载仿真列表失败:', error)
  }
}

// 加载仿真结果
async function loadSimulation(simulationId) {
  try {
    const data = await api.get(`/api/simulation/${simulationId}`)

    emit('load-simulation', data)
    showToast(t('dataExport.resultLoaded'))
  } catch (error) {
    console.error('Load simulation failed:', error)
    showToast(t('dataExport.loadFailed'), 'error')
  }
}

// 导出历史仿真CSV
async function exportSimulationCSV(simulationId) {
  try {
    const data = await api.get(`/api/simulation/${simulationId}`)

    if (data) {
      const csvContent = generateCSV(data) // 传入完整data对象
      const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.download = `${data.name || 'simulation'}_${new Date().toISOString().slice(0, 10)}.csv`
      link.href = url
      link.click()
      window.URL.revokeObjectURL(url)
      showToast(t('dataExport.csvSuccess'))
    }
  } catch (error) {
    console.error('Export failed:', error)
    showToast(t('dataExport.exportFailed'), 'error')
  }
}

// 生成CSV内容
function generateCSV(data) {
  const eq = t('export.eqHeader')
  const sep = t('export.separator')
  const date = new Date().toISOString().slice(0, 10)
  const projectName = store.survey.projectName || data.name || 'Untitled'

  // 报告标题头
  let csv = eq + '\n'
  csv += '  ' + t('export.reportTitle') + '\n'
  csv += '  ' + t('export.projectName') + ': ' + projectName + '\n'
  csv += '  ' + t('export.generatedDate') + ': ' + date + '\n'
  csv += '  ' + t('export.version') + ': v1.0\n'
  csv += eq + '\n\n'

  // 关键参数摘要
  csv += sep + ' ' + t('export.keyParams') + ' ' + sep + '\n'
  csv += t('export.ratedEnergy') + ',' + (store.systemParams.ratedEnergy || 'N/A') + '\n'
  csv += t('export.totalPower') + ',' + (store.systemParams.pcsPower || 'N/A') + '\n'
  csv += t('export.duration') + ',' + (store.systemParams.duration || 'N/A') + '\n'
  csv += t('export.strategy') + ',' + (store.designResults.strategy || 'N/A') + '\n'
  csv += '\n'

  // 矩阵数据
  if (data.results) {
    csv += sep + ' ' + t('export.lifecycleMatrix') + ' ' + sep + '\n'
    csv += t('dataExport.csvMatrixHeader') + '\n'

    const r = data.results
    for (let i = 0; i < 26; i++) {
      csv += `${i},${r.initGross?.[i]?.toFixed(2) || 0},${r.initAux?.[i]?.toFixed(2) || 0},${r.initAcUsable?.[i]?.toFixed(2) || 0},`
      csv += `${r.augGross?.[i]?.toFixed(2) || 0},${r.augAux?.[i]?.toFixed(2) || 0},${r.augAcUsable?.[i]?.toFixed(2) || 0},`
      csv += `${r.totalAcUsable?.[i]?.toFixed(2) || 0},${r.augAccumQty?.[i] || 0},${r.meetsReq?.[i] ? t('dataExport.csvYes') : t('dataExport.csvNo')}\n`
    }
  }

  // SOH数据
  if (data.soh && data.soh.length > 0) {
    csv += '\n' + sep + ' ' + t('export.sohRteData') + ' ' + sep + '\n'
    csv += t('dataExport.csvSohRteHeader') + '\n'
    for (let i = 0; i < data.soh.length; i++) {
      csv += `${i},${(data.soh[i] * 100).toFixed(2)},${data.rte?.[i] ? (data.rte[i] * 100).toFixed(2) : ''}\n`
    }
  }

  // 免责声明
  csv += '\n' + sep + '\n'
  csv += t('export.disclaimer') + '\n'

  return csv
}

// 初始化加载
loadSimulations()
</script>

<style scoped>
.export-panel {
  height: 100%;
}

.export-action-btn:not(:disabled):hover {
  opacity: 0.9;
}

.link-btn {
  color: var(--color-accent-secondary);
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  transition: color 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.link-btn:hover {
  color: var(--color-accent);
}
</style>
