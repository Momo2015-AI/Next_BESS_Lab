<template>
  <div class="scenario-compare h-full overflow-auto p-4">
    <div class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border)">
      <h3 class="text-sm font-bold mb-4 flex items-center gap-2" style="color: var(--color-accent)">
        <span class="w-2 h-2 rounded-full" style="background-color: var(--color-accent)" />
        {{ $t('scenario.title') }}
      </h3>

      <!-- 场景管理 -->
      <div class="grid grid-cols-3 gap-4 mb-4">
        <!-- 场景列表 -->
        <div class="col-span-1 rounded-lg p-3" style="background-color: var(--color-card-dark)">
          <div class="flex items-center justify-between mb-3">
            <span class="text-xs" style="color: var(--color-text-muted)">{{ $t('scenario.sceneList') }}</span>
            <button
              class="text-xs px-2 py-1 rounded transition-colors"
              style="background-color: var(--color-accent); color: white"
              @click="createScenario"
              >
                + {{ $t('scenario.createNew') }}
            </button>
          </div>

          <div class="space-y-2 max-h-60 overflow-y-auto">
            <div
              v-for="(scenario, idx) in scenarios"
              :key="idx"
              class="p-2 rounded cursor-pointer transition-all text-xs"
              :style="
                selectedScenarioIdx === idx
                  ? { backgroundColor: 'var(--color-accent-glow)', border: '1px solid var(--color-accent)' }
                  : { backgroundColor: 'var(--color-input-bg)', border: '1px solid transparent' }
              "
            >
              <div class="flex items-center justify-between">
                <span style="color: var(--color-text-secondary)" @click="selectScenario(idx)">{{ scenario.name }}</span>
                <div class="flex gap-1">
                  <button style="color: var(--color-text-muted)" @click.stop="editScenario(idx)">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
                      />
                    </svg>
                  </button>
                  <button style="color: var(--color-text-muted)" @click.stop="deleteScenario(idx)">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                      />
                    </svg>
                  </button>
                </div>
              </div>
              <div class="text-[10px] mt-1" style="color: var(--color-text-muted)">
                {{ scenario.params.ratedEnergy || '-' }} MWh | {{ scenario.params.acEfficiency || '-' }}%
              </div>
            </div>

            <div v-if="scenarios.length === 0" class="text-xs text-center py-4" style="color: var(--color-text-muted)">
              {{ $t('scenario.noScene') }}
            </div>
          </div>
        </div>

        <!-- 场景编辑器 -->
        <div class="col-span-2 rounded-lg p-3" style="background-color: var(--color-card-dark)">
          <div v-if="!editingScenario" class="text-xs text-center py-8" style="color: var(--color-text-muted)">
            {{ $t('scenario.selectOrCreate') }}
          </div>

          <div v-else>
            <div class="flex items-center justify-between mb-3">
              <input
                v-model="editingScenario.name"
                class="text-xs px-2 py-1 rounded"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
                :placeholder="$t('scenario.namePlaceholder')"
              />
              <div class="flex gap-2">
                <button
                  class="text-xs px-3 py-1 rounded transition-colors"
                  style="background-color: var(--color-accent); color: white"
                  @click="saveScenario"
                  >
                  {{ $t('common.save') }}
                </button>
                <button
                  class="text-xs px-3 py-1 rounded transition-colors"
                  style="
                    background-color: var(--color-card);
                    border: 1px solid var(--color-border);
                    color: var(--color-text-secondary);
                  "
                  @click="cancelEdit"
                >
                  {{ $t('common.cancel') }}
                </button>
              </div>
            </div>

            <div class="grid grid-cols-3 gap-2 text-xs">
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">{{ $t('scenario.ratedEnergy') }}</label>
                <input
                  v-model.number="editingScenario.params.ratedEnergy"
                  type="number"
                  class="w-full rounded px-2 py-1"
                  style="
                    background-color: var(--color-input-bg-dark);
                    border: 1px solid var(--color-input-border);
                    color: var(--color-text);
                  "
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">{{ $t('scenario.containerQty') }}</label>
                <input
                  v-model.number="editingScenario.params.initContainerQty"
                  type="number"
                  class="w-full rounded px-2 py-1"
                  style="
                    background-color: var(--color-input-bg-dark);
                    border: 1px solid var(--color-input-border);
                    color: var(--color-text);
                  "
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">{{ $t('scenario.pcsQty') }}</label>
                <input
                  v-model.number="editingScenario.params.initPcsQty"
                  type="number"
                  class="w-full rounded px-2 py-1"
                  style="
                    background-color: var(--color-input-bg-dark);
                    border: 1px solid var(--color-input-border);
                    color: var(--color-text);
                  "
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">{{ $t('scenario.duration') }}</label>
                <input
                  v-model.number="editingScenario.params.duration"
                  type="number"
                  class="w-full rounded px-2 py-1"
                  style="
                    background-color: var(--color-input-bg-dark);
                    border: 1px solid var(--color-input-border);
                    color: var(--color-text);
                  "
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">{{ $t('scenario.cyclesPerDay') }}</label>
                <input
                  v-model.number="editingScenario.params.cyclesPerDay"
                  type="number"
                  class="w-full rounded px-2 py-1"
                  style="
                    background-color: var(--color-input-bg-dark);
                    border: 1px solid var(--color-input-border);
                    color: var(--color-text);
                  "
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">{{ $t('scenario.acEfficiency') }}</label>
                <input
                  v-model.number="editingScenario.params.acEfficiency"
                  type="number"
                  class="w-full rounded px-2 py-1"
                  style="
                    background-color: var(--color-input-bg-dark);
                    border: 1px solid var(--color-input-border);
                    color: var(--color-text);
                  "
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">{{ $t('scenario.bessAuxRun') }}</label>
                <input
                  v-model.number="editingScenario.params.bessAuxRun"
                  type="number"
                  class="w-full rounded px-2 py-1"
                  style="
                    background-color: var(--color-input-bg-dark);
                    border: 1px solid var(--color-input-border);
                    color: var(--color-text);
                  "
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">{{ $t('scenario.bessAuxStandby') }}</label>
                <input
                  v-model.number="editingScenario.params.bessAuxStandby"
                  type="number"
                  class="w-full rounded px-2 py-1"
                  style="
                    background-color: var(--color-input-bg-dark);
                    border: 1px solid var(--color-input-border);
                    color: var(--color-text);
                  "
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">{{ $t('scenario.requiredEnergy') }}</label>
                <input
                  v-model.number="editingScenario.params.requiredEnergy"
                  type="number"
                  class="w-full rounded px-2 py-1"
                  style="
                    background-color: var(--color-input-bg-dark);
                    border: 1px solid var(--color-input-border);
                    color: var(--color-text);
                  "
                />
              </div>
            </div>

            <div class="mt-3 flex gap-2">
              <button
                :disabled="calculating"
                class="flex-1 text-xs px-3 py-1.5 rounded transition-colors"
                :style="
                  calculating
                    ? { backgroundColor: 'var(--color-card-dark)', color: 'var(--color-text-muted)' }
                    : { backgroundColor: 'var(--color-warning)', color: 'white' }
                "
                @click="calculateScenario"
              >
                {{ calculating ? $t('scenario.calculating') : $t('scenario.calculateThis') }}
              </button>
              <button
                class="flex-1 text-xs px-3 py-1.5 rounded transition-colors"
                style="background-color: var(--color-accent-secondary); color: white"
                @click="useAsBase"
              >
                {{ $t('scenario.setAsBase') }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 对比图表 -->
      <div v-if="scenarios.length > 0" class="mt-4">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs" style="color: var(--color-text-muted)">{{ $t('scenario.chart') }}</span>
          <div class="flex gap-2">
            <button
              class="text-xs px-2 py-1 rounded transition-colors"
              :style="
                showChart === 'soh'
                  ? { backgroundColor: 'var(--color-accent)', color: 'white' }
                  : { backgroundColor: 'var(--color-card-dark)', color: 'var(--color-text-secondary)' }
              "
              @click="showChart = 'soh'"
            >
              {{ $t('scenario.sohCurve') }}
            </button>
            <button
              class="text-xs px-2 py-1 rounded transition-colors"
              :style="
                showChart === 'energy'
                  ? { backgroundColor: 'var(--color-accent)', color: 'white' }
                  : { backgroundColor: 'var(--color-card-dark)', color: 'var(--color-text-secondary)' }
              "
              @click="showChart = 'energy'"
            >
              {{ $t('scenario.netEnergy') }}
            </button>
            <button
              class="text-xs px-2 py-1 rounded transition-colors"
              :style="
                showChart === 'cost'
                  ? { backgroundColor: 'var(--color-accent)', color: 'white' }
                  : { backgroundColor: 'var(--color-card-dark)', color: 'var(--color-text-secondary)' }
              "
              @click="showChart = 'cost'"
            >
              {{ $t('scenario.costComparison') }}
            </button>
          </div>
        </div>

        <div ref="chartContainer" class="h-64 rounded-lg" style="background-color: var(--color-card-dark)" />
      </div>

      <!-- 对比表格 -->
      <div v-if="scenarios.length > 0" class="mt-4">
        <div class="text-xs mb-2" style="color: var(--color-text-muted)">{{ $t('scenario.keyMetrics') }}</div>
        <div class="overflow-x-auto">
          <table class="w-full text-xs">
            <thead>
              <tr style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)">
                <th class="text-left py-2 px-2">{{ $t('scenario.metric') }}</th>
                <th v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.name }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr style="color: var(--color-text-secondary); border-bottom: 1px solid var(--color-border)">
                <td class="py-2 px-2">{{ $t('scenario.ratedEnergy') }}</td>
                <td v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.params.ratedEnergy || '-' }}
                </td>
              </tr>
              <tr style="color: var(--color-text-secondary); border-bottom: 1px solid var(--color-border)">
                <td class="py-2 px-2">{{ $t('scenario.acEfficiency') }}</td>
                <td v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.params.acEfficiency || '-' }}
                </td>
              </tr>
              <tr style="color: var(--color-text-secondary); border-bottom: 1px solid var(--color-border)">
                <td class="py-2 px-2">{{ $t('scenario.initNetAvailable') }}</td>
                <td v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.results?.initAcUsable?.[0]?.toFixed(2) || '-' }}
                </td>
              </tr>
              <tr style="color: var(--color-text-secondary); border-bottom: 1px solid var(--color-border)">
                <td class="py-2 px-2">{{ $t('scenario.year10NetAvailable') }}</td>
                <td v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.results?.totalAcUsable?.[10]?.toFixed(2) || '-' }}
                </td>
              </tr>
              <tr style="color: var(--color-text-secondary); border-bottom: 1px solid var(--color-border)">
                <td class="py-2 px-2">{{ $t('scenario.year25NetAvailable') }}</td>
                <td v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.results?.totalAcUsable?.[25]?.toFixed(2) || '-' }}
                </td>
              </tr>
              <tr style="color: var(--color-text-secondary); border-bottom: 1px solid var(--color-border)">
                <td class="py-2 px-2">{{ $t('scenario.cumulativeAug25') }}</td>
                <td v-for="(scenario, idx) in scenarios" :key="idx" class="text-right py-2 px-2">
                  {{ scenario.results?.augAccumQty?.[25] || '-' }}
                </td>
              </tr>
              <tr style="color: var(--color-accent); font-weight: 500; border-bottom: 1px solid var(--color-border)">
                <td class="py-2 px-2">{{ $t('scenario.meetsRequirement') }}</td>
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
import { useI18n } from 'vue-i18n'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, GridComponent } from 'echarts/components'
import { useDraftRef } from '../composables/useDraft'
const { t } = useI18n()
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
    name: t('scenario.sceneDefaultName', { count: scenarios.value.length + 1 }),
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
    showToast(t('scenario.enterName'), 'error')
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
  showToast(t('scenario.saved'))
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
    showToast(t('scenario.setAsBaseMsg'))
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
      showToast(t('scenario.calcComplete'))
    } else {
      throw new Error(result.error)
    }
  } catch (error) {
    console.error(t('scenario.calcFailed'), error)
    showToast(t('scenario.calcFailedMsg') + error.message, 'error')
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

    const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
    const colors = {
      tooltipBg: isDark ? 'rgba(30, 41, 59, 0.9)' : 'rgba(255, 255, 255, 0.95)',
      tooltipBorder: isDark ? 'rgba(100, 116, 139, 0.3)' : 'rgba(226, 232, 240, 0.5)',
      tooltipText: isDark ? 'var(--color-border-light)' : '#1e293b',
      legendText: isDark ? 'var(--color-text-secondary)' : 'var(--color-text-secondary)',
      axisLabel: isDark ? 'var(--color-text-secondary)' : 'var(--color-text-secondary)',
      axisLine: isDark ? 'var(--color-border)' : 'var(--color-border-light)',
      splitLine: isDark ? '#1e293b' : '#f1f5f9',
      colorList: isDark
        ? ['#2dd4bf', '#38bdf8', 'var(--color-chart-orange)', '#a78bfa', 'var(--color-chart-pink)']
        : ['#14b8a6', '#0ea5e9', 'var(--color-chart-orange)', 'var(--color-info)', 'var(--color-chart-pink)']
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
        name: t('scenario.year'),
        nameTextStyle: { color: colors.axisLabel, fontSize: 10 },
        axisLabel: { color: colors.axisLabel, fontSize: 10 },
        axisLine: { lineStyle: { color: colors.axisLine } }
      },
      yAxis: {
        type: 'value',
        name: showChart.value === 'soh' ? t('scenario.sohPct') : t('scenario.netAvailableMwh'),
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
input:focus,
select:focus,
textarea:focus {
  border-color: var(--color-input-focus);
  outline: none;
}

button:not(:disabled):hover {
  opacity: 0.9;
}
</style>
