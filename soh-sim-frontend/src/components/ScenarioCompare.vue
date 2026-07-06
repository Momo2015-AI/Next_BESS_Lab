<template>
  <div class="scenario-compare h-full overflow-auto p-4">
    <div class="card-panel p-4">
      <h3 class="text-sm font-bold mb-4 flex items-center gap-2 text-accent">
        <span class="dot-accent" />
        多场景对比分析
      </h3>

      <!-- 场景管理 -->
      <div class="grid grid-cols-3 gap-4 mb-4">
        <!-- 场景列表 -->
        <div class="col-span-1 card-panel-small">
          <div class="flex items-center justify-between mb-3">
            <span class="text-xs text-muted">场景列表</span>
            <button class="text-xs px-2 py-1 rounded transition-colors btn-accent-filled" @click="createScenario">
              + 新建
            </button>
          </div>

          <div class="space-y-2 max-h-60 overflow-y-auto">
            <div
              v-for="(scenario, idx) in scenarios"
              :key="idx"
              class="p-2 rounded cursor-pointer transition-all text-xs"
              :class="selectedScenarioIdx === idx ? 'btn-selected' : 'btn-default'"
            >
              <div class="flex items-center justify-between">
                <span class="text-secondary" @click="selectScenario(idx)">{{ scenario.name }}</span>
                <div class="flex gap-1">
                  <button class="text-muted" @click.stop="editScenario(idx)">
                    <AppIcon name="edit" size="12" />
                  </button>
                  <button class="text-muted" @click.stop="deleteScenario(idx)">
                    <AppIcon name="trash" size="12" />
                  </button>
                </div>
              </div>
              <div class="text-[10px] mt-1 text-muted">
                {{ scenario.params.ratedEnergy || '-' }} MWh | {{ scenario.params.acEfficiency || '-' }}%
              </div>
            </div>

            <div v-if="scenarios.length === 0" class="text-xs text-center py-4 text-muted">
              暂无场景，点击"新建"创建
            </div>
          </div>
        </div>

        <!-- 场景编辑器 -->
        <div class="col-span-2 card-panel-small">
          <div v-if="!editingScenario" class="text-xs text-center py-8 text-muted">选择或创建一个场景进行编辑</div>

          <div v-else>
            <div class="flex items-center justify-between mb-3">
              <input
                v-model="editingScenario.name"
                class="text-xs px-2 py-1 rounded form-field-input"
                placeholder="场景名称"
              />
              <div class="flex gap-2">
                <button class="text-xs px-3 py-1 rounded transition-colors btn-accent-filled" @click="saveScenario">
                  保存
                </button>
                <button class="text-xs px-3 py-1 rounded transition-colors btn-card-outline" @click="cancelEdit">
                  取消
                </button>
              </div>
            </div>

            <div class="grid grid-cols-3 gap-2 text-xs">
              <div>
                <label class="text-[10px] block mb-1 label-text">额定能量 (MWh)</label>
                <input
                  v-model.number="editingScenario.params.ratedEnergy"
                  type="number"
                  class="w-full rounded px-2 py-1 form-field-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1 label-text">集装箱数量</label>
                <input
                  v-model.number="editingScenario.params.initContainerQty"
                  type="number"
                  class="w-full rounded px-2 py-1 form-field-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1 label-text">PCS数量</label>
                <input
                  v-model.number="editingScenario.params.initPcsQty"
                  type="number"
                  class="w-full rounded px-2 py-1 form-field-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1 label-text">储能时长 (h)</label>
                <input
                  v-model.number="editingScenario.params.duration"
                  type="number"
                  class="w-full rounded px-2 py-1 form-field-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1 label-text">每日循环</label>
                <input
                  v-model.number="editingScenario.params.cyclesPerDay"
                  type="number"
                  class="w-full rounded px-2 py-1 form-field-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1 label-text">交流效率 (%)</label>
                <input
                  v-model.number="editingScenario.params.acEfficiency"
                  type="number"
                  class="w-full rounded px-2 py-1 form-field-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1 label-text">BESS运行功耗</label>
                <input
                  v-model.number="editingScenario.params.bessAuxRun"
                  type="number"
                  class="w-full rounded px-2 py-1 form-field-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1 label-text">BESS待机功耗</label>
                <input
                  v-model.number="editingScenario.params.bessAuxStandby"
                  type="number"
                  class="w-full rounded px-2 py-1 form-field-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1 label-text">需求能量 (MWh)</label>
                <input
                  v-model.number="editingScenario.params.requiredEnergy"
                  type="number"
                  class="w-full rounded px-2 py-1 form-field-input"
                />
              </div>
            </div>

            <div class="mt-3 flex gap-2">
              <button
                :disabled="calculating"
                class="flex-1 text-xs px-3 py-1.5 rounded transition-colors btn-card-outline"
                :class="calculating ? 'opacity-60 cursor-not-allowed' : ''"
                @click="calculateScenario"
              >
                {{ calculating ? '计算中...' : '计算此场景' }}
              </button>
              <button class="flex-1 text-xs px-3 py-1.5 rounded transition-colors btn-accent-filled" @click="useAsBase">
                设为基准
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 对比图表 -->
      <div v-if="scenarios.length > 0" class="mt-4">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs text-muted">对比图表</span>
          <div class="flex gap-2">
            <button
              class="text-xs px-2 py-1 rounded transition-colors"
              :class="showChart === 'soh' ? 'btn-accent-filled' : 'btn-card-outline'"
              @click="showChart = 'soh'"
            >
              SOH曲线
            </button>
            <button
              class="text-xs px-2 py-1 rounded transition-colors"
              :class="showChart === 'energy' ? 'btn-accent-filled' : 'btn-card-outline'"
              @click="showChart = 'energy'"
            >
              能量对比
            </button>
            <button
              class="text-xs px-2 py-1 rounded transition-colors"
              :class="showChart === 'cost' ? 'btn-accent-filled' : 'btn-card-outline'"
              @click="showChart = 'cost'"
            >
              成本对比
            </button>
          </div>
        </div>

        <div ref="chartContainer" class="chart-container-dark" />
      </div>

      <!-- 对比表格 -->
      <div v-if="scenarios.length > 0" class="mt-4">
        <div class="text-xs mb-2 text-muted">关键指标对比</div>
        <div class="overflow-x-auto">
          <table class="w-full text-xs">
            <thead>
              <tr class="text-muted border-b border-[var(--color-border)]">
                <th class="text-left py-2 px-2">指标</th>
                <th v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.name }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr class="text-secondary border-b border-[var(--color-border)]">
                <td class="py-2 px-2">额定能量 (MWh)</td>
                <td v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.params.ratedEnergy || '-' }}
                </td>
              </tr>
              <tr class="text-secondary border-b border-[var(--color-border)]">
                <td class="py-2 px-2">交流效率 (%)</td>
                <td v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.params.acEfficiency || '-' }}
                </td>
              </tr>
              <tr class="text-secondary border-b border-[var(--color-border)]">
                <td class="py-2 px-2">初始净可用 (MWh)</td>
                <td v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.results?.initAcUsable?.[0]?.toFixed(2) || '-' }}
                </td>
              </tr>
              <tr class="text-secondary border-b border-[var(--color-border)]">
                <td class="py-2 px-2">第10年净可用 (MWh)</td>
                <td v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.results?.totalAcUsable?.[10]?.toFixed(2) || '-' }}
                </td>
              </tr>
              <tr class="text-secondary border-b border-[var(--color-border)]">
                <td class="py-2 px-2">第25年净可用 (MWh)</td>
                <td v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.results?.totalAcUsable?.[25]?.toFixed(2) || '-' }}
                </td>
              </tr>
              <tr class="text-secondary border-b border-[var(--color-border)]">
                <td class="py-2 px-2">25年累计扩容</td>
                <td v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.results?.augAccumQty?.[25] || '-' }}
                </td>
              </tr>
              <tr class="text-accent font-medium border-b border-[var(--color-border)]">
                <td class="py-2 px-2">是否满足需求</td>
                <td v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.results?.meetsReq?.[25] ? '✓' : '✗' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Toast提示 -->
    <div
      v-if="toast.show"
      class="fixed bottom-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all"
      :style="{
        backgroundColor: toast.type === 'success' ? 'var(--color-success)' : 'var(--color-danger)',
        color: 'white'
      }"
    >
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, nextTick, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, GridComponent } from 'echarts/components'
import { useDraftRef } from '../composables/useDraft'
import { useChartTheme } from '../composables/useChartTheme'
import AppIcon from './AppIcon.vue'
echarts.use([CanvasRenderer, LineChart, TitleComponent, TooltipComponent, GridComponent])

const props = defineProps({
  baseParams: { type: Object, default: () => ({}) }
})

const emit = defineEmits(['error'])

const scenarios = useDraftRef('scenario-list', []).state
const selectedScenarioIdx = useDraftRef('scenario-selected-idx', -1).state
const editingScenario = ref(null)
const calculating = ref(false)
const showChart = ref('soh')
const chartContainer = ref(null)
let chartInstance = null
let _resizeHandler = null

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

// 创建新场景
function createScenario() {
  editingScenario.value = {
    name: `场景 ${scenarios.value.length + 1}`,
    params: {
      ratedEnergy: 5,
      initContainerQty: 62,
      initPcsQty: 1,
      duration: 2,
      cyclesPerDay: 1,
      acEfficiency: 97.03,
      bessAuxRun: 18.124,
      bessAuxStandby: 3.5,
      pcsAuxRun: 6.5,
      pcsAuxStandby: 1.0,
      requiredEnergy: 240
    },
    results: null
  }
}

// 选择场景
function selectScenario(idx) {
  selectedScenarioIdx.value = idx
  editingScenario.value = JSON.parse(JSON.stringify(scenarios.value[idx]))
}

// 编辑场景
function editScenario(idx) {
  selectScenario(idx)
}

// 保存场景
function saveScenario() {
  if (!editingScenario.value.name) {
    showToast('请输入场景名称', 'error')
    return
  }

  const idx = selectedScenarioIdx.value
  if (idx >= 0) {
    scenarios.value[idx] = JSON.parse(JSON.stringify(editingScenario.value))
  } else {
    scenarios.value.push(JSON.parse(JSON.stringify(editingScenario.value)))
    selectedScenarioIdx.value = scenarios.value.length - 1
  }

  editingScenario.value = null
  updateChart()
  showToast('场景已保存')
}

// 取消编辑
function cancelEdit() {
  editingScenario.value = null
}

// 删除场景
function deleteScenario(idx) {
  scenarios.value.splice(idx, 1)
  if (selectedScenarioIdx.value === idx) {
    selectedScenarioIdx.value = -1
    editingScenario.value = null
  } else if (selectedScenarioIdx.value > idx) {
    selectedScenarioIdx.value--
  }
  updateChart()
}

// 设为基准
function useAsBase() {
  if (selectedScenarioIdx.value >= 0) {
    scenarios.value[selectedScenarioIdx.value].isBase = true
    scenarios.value.forEach((s, i) => {
      if (i !== selectedScenarioIdx.value) s.isBase = false
    })
    showToast('已设为基准场景')
  }
}

// 计算场景
async function calculateScenario() {
  if (!editingScenario.value) return

  calculating.value = true

  try {
    const response = await fetch('/api/soh/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editingScenario.value.params)
    })

    const result = await response.json()

    if (result.success) {
      editingScenario.value.results = result.data

      // 更新列表中的场景
      const idx = selectedScenarioIdx.value
      if (idx >= 0) {
        scenarios.value[idx] = JSON.parse(JSON.stringify(editingScenario.value))
      }

      updateChart()
      showToast('计算完成')
    } else {
      throw new Error(result.error)
    }
  } catch (error) {
    console.error('计算失败:', error)
    showToast('计算失败: ' + error.message, 'error')
  } finally {
    calculating.value = false
  }
}

// 更新图表
function updateChart() {
  nextTick(() => {
    if (!chartContainer.value) return

    if (!chartInstance) {
      chartInstance = echarts.init(chartContainer.value)
    }

    const years = Array.from({ length: 26 }, (_, i) => i)

    const series = []

    if (showChart.value === 'soh') {
      scenarios.value.forEach((scenario, idx) => {
        if (scenario.results?.soh) {
          series.push({
            name: scenario.name,
            type: 'line',
            smooth: true,
            data: scenario.results.soh.map((v) => (v * 100).toFixed(2)),
            connectNulls: true
          })
        }
      })
    } else if (showChart.value === 'energy') {
      scenarios.value.forEach((scenario, idx) => {
        if (scenario.results?.totalAcUsable) {
          series.push({
            name: scenario.name,
            type: 'line',
            smooth: true,
            data: scenario.results.totalAcUsable,
            connectNulls: true
          })
        }
      })
    }

    const { colors: tc } = useChartTheme({
      tooltipBg: 'rgba(255, 255, 255, 0.95)',
      tooltipBorder: 'rgba(226, 232, 240, 0.5)',
      tooltipText: '#1e293b',
      legendText: 'var(--color-text-secondary)',
      axisLabel: 'var(--color-text-secondary)',
      axisLine: 'var(--color-border-light)',
      splitLine: '#f1f5f9',
      colorList: ['#14b8a6', '#0ea5e9', 'var(--color-chart-orange)', 'var(--color-info)', 'var(--color-chart-pink)']
    })

    const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
    const colors = {
      tooltipBg: isDark ? 'rgba(30, 41, 59, 0.9)' : tc.tooltipBg,
      tooltipBorder: isDark ? 'rgba(100, 116, 139, 0.3)' : tc.tooltipBorder,
      tooltipText: isDark ? 'var(--color-border-light)' : tc.tooltipText,
      legendText: isDark ? 'var(--color-text-secondary)' : tc.legendText,
      axisLabel: isDark ? 'var(--color-text-secondary)' : tc.axisLabel,
      axisLine: isDark ? 'var(--color-border)' : tc.axisLine,
      splitLine: isDark ? '#1e293b' : tc.splitLine,
      colorList: isDark
        ? ['#2dd4bf', '#38bdf8', 'var(--color-chart-orange)', '#a78bfa', 'var(--color-chart-pink)']
        : tc.colorList
    }

    const option = {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        backgroundColor: colors.tooltipBg,
        borderColor: colors.tooltipBorder,
        textStyle: { color: colors.tooltipText, fontSize: 11 }
      },
      legend: {
        data: scenarios.value.map((s) => s.name),
        textStyle: { color: colors.legendText, fontSize: 11 },
        top: 5
      },
      grid: {
        left: 50,
        right: 20,
        top: 40,
        bottom: 30
      },
      xAxis: {
        type: 'category',
        data: years,
        name: '年份',
        nameTextStyle: { color: colors.axisLabel, fontSize: 10 },
        axisLabel: { color: colors.axisLabel, fontSize: 10 },
        axisLine: { lineStyle: { color: colors.axisLine } }
      },
      yAxis: {
        type: 'value',
        name: showChart.value === 'soh' ? 'SOH (%)' : '净可用 (MWh)',
        nameTextStyle: { color: colors.axisLabel, fontSize: 10 },
        axisLabel: { color: colors.axisLabel, fontSize: 10 },
        axisLine: { lineStyle: { color: colors.axisLine } },
        splitLine: { lineStyle: { color: colors.splitLine } }
      },
      series,
      color: colors.colorList
    }

    chartInstance.setOption(option, true)
  })
}

// 监听图表类型变化
watch(showChart, () => {
  updateChart()
})

// 窗口调整
onMounted(() => {
  _resizeHandler = () => {
    chartInstance?.resize()
  }
  window.addEventListener('resize', _resizeHandler)
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  if (_resizeHandler) {
    window.removeEventListener('resize', _resizeHandler)
    _resizeHandler = null
  }
})
</script>

<style scoped>
.scenario-compare {
  height: 100%;
}

button:not(:disabled):hover {
  opacity: 0.9;
}
</style>
