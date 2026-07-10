<template>
  <div class="rounded-lg p-3 card-bordered">
    <h3 class="font-bold text-xs mb-2 flex items-center gap-2 text-default">
      <span
        class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold u-background-color-rgba-16-185-129-0-2-color-var-color-success"
      >
        VIII
      </span>
      {{ $t('energyFlow.title') }}
    </h3>

    <div class="mb-2 flex items-center gap-2 text-[10px] text-secondary">
      <div class="flex items-center gap-1">
        <div class="w-3 h-3 rounded bg-accent" />
        <span>{{ $t('energyFlow.charging') }}</span>
      </div>
      <div class="flex items-center gap-1">
        <div class="w-3 h-3 rounded bg-danger" />
        <span>{{ $t('energyFlow.loss') }}</span>
      </div>
      <div class="flex items-center gap-1">
        <div class="w-3 h-3 rounded bg-success" />
        <span>{{ $t('energyFlow.discharging') }}</span>
      </div>
      <div class="flex items-center gap-1">
        <div class="w-3 h-3 rounded bg-warning" />
        <span>{{ $t('energyFlow.aux') }}</span>
      </div>
    </div>

    <div ref="sankeyChartRef" class="chart-container" />

    <!-- 参数控制 -->
    <div class="mt-3 grid grid-cols-2 gap-2 text-[10px] text-secondary">
      <div>
        <label class="block mb-0.5 text-muted">{{ $t('energyFlow.cyclesPerDay') }}</label>
        <input
          v-model.number="cyclesPerDay"
          type="number"
          step="0.1"
          min="0.1"
          max="10"
          class="w-full rounded px-2 py-1 text-xs u-background-color-var-color-input-bg-dark-border-1px-solid-var-color-input-border-color-var-color-text"
          @input="updateChart"
        />
      </div>
      <div>
        <label class="block mb-0.5 text-muted">{{ $t('energyFlow.operatingDays') }}</label>
        <input
          v-model.number="operatingDays"
          type="number"
          step="1"
          min="1"
          max="365"
          class="w-full rounded px-2 py-1 text-xs u-background-color-var-color-input-bg-dark-border-1px-solid-var-color-input-border-color-var-color-text"
          @input="updateChart"
        />
      </div>
      <div>
        <label class="block mb-0.5 text-muted">{{ $t('energyFlow.chargingEff') }}</label>
        <input
          v-model.number="chargingEfficiency"
          type="number"
          step="1"
          min="50"
          max="100"
          class="w-full rounded px-2 py-1 text-xs u-background-color-var-color-input-bg-dark-border-1px-solid-var-color-input-border-color-var-color-text"
          @input="updateChart"
        />
      </div>
      <div>
        <label class="block mb-0.5 text-muted">{{ $t('energyFlow.dischargingEff') }}</label>
        <input
          v-model.number="dischargingEfficiency"
          type="number"
          step="1"
          min="50"
          max="100"
          class="w-full rounded px-2 py-1 text-xs u-background-color-var-color-input-bg-dark-border-1px-solid-var-color-input-border-color-var-color-text"
          @input="updateChart"
        />
      </div>
    </div>

    <!-- 能量摘要 -->
    <div class="mt-3 border-t pt-2 border-default">
      <div class="grid grid-cols-2 gap-2 text-[10px]">
        <div class="rounded p-2 bg-card-dark">
          <div>{{ $t('energyFlow.totalCharging') }}</div>
          class="text-muted"
          <div class="font-mono mt-0.5 text-accent">
            {{ formatEnergy(totalCharging) }}
          </div>
        </div>
        <div class="rounded p-2 bg-card-dark">
          <div>{{ $t('energyFlow.totalDischarging') }}</div>
          class="text-muted"
          <div class="font-mono mt-0.5 text-success">
            {{ formatEnergy(totalDischarging) }}
          </div>
        </div>
        <div class="rounded p-2 bg-card-dark">
          <div>{{ $t('energyFlow.energyLoss') }}</div>
          class="text-muted"
          <div class="font-mono mt-0.5 text-danger">
            {{ formatEnergy(totalLoss) }}
          </div>
        </div>
        <div class="rounded p-2 bg-card-dark">
          <div>{{ $t('energyFlow.systemEff') }}</div>
          class="text-muted"
          <div class="font-mono mt-0.5 text-warning">{{ systemEfficiency.toFixed(1) }}%</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, computed, watch, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { debounce } from 'lodash-es'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { SankeyChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, GridComponent, LegendComponent } from 'echarts/components'
import { useDraft } from '../composables/useDraft'
import { useChartTheme } from '../composables/useChartTheme.js'

const { t } = useI18n()
const { themeObject } = useChartTheme()

watch(themeObject, () => {
  nextTick(initChart)
})
echarts.use([CanvasRenderer, SankeyChart, TitleComponent, TooltipComponent, GridComponent, LegendComponent])

const props = defineProps({
  params: Object,
  soh: Array
})

const sankeyChartRef = ref(null)
let sankeyChart = null
let themeObserver = null
let _resizeHandler = null

// 参数
const cyclesPerDay = ref(1)
const operatingDays = ref(330)
const chargingEfficiency = ref(95)
const dischargingEfficiency = ref(95)

// 计算属性
const ratedEnergy = computed(() => props.params?.ratedEnergy || 5)
const totalCapacityMWh = computed(() => ratedEnergy.value * (props.params?.initContainerQty || 62))

// 能量计算
const totalCharging = computed(() => {
  const baseEnergy = totalCapacityMWh.value * cyclesPerDay.value * operatingDays.value
  return baseEnergy // 充电量 = 总能量需求
})

const totalLoss = computed(() => {
  const chargingLoss = totalCharging.value * (1 - chargingEfficiency.value / 100)
  const dischargingLoss = totalCharging.value * (1 - dischargingEfficiency.value / 100)
  return chargingLoss + dischargingLoss
})

const totalDischarging = computed(() => {
  const netEnergy = totalCharging.value - totalLoss.value
  return Math.max(0, netEnergy)
})

const systemEfficiency = computed(() => {
  return totalCharging.value > 0 ? (totalDischarging.value / totalCharging.value) * 100 : 0
})

// 格式化能量
const formatEnergy = (energy) => {
  if (!energy || isNaN(energy)) return '0 MWh'
  if (energy >= 1000) {
    return `${(energy / 1000).toFixed(1)} GWh`
  }
  return `${energy.toFixed(1)} MWh`
}

// 生成桑基图数据
const generateSankeyData = () => {
  const nodes = [
    { name: t('energyFlow.nodeChargingInput'), itemStyle: { color: themeObject.value.primary } },
    { name: t('energyFlow.nodeChargingLoss'), itemStyle: { color: themeObject.value.danger } },
    { name: t('energyFlow.nodeBatteryStorage'), itemStyle: { color: themeObject.value.purple } },
    { name: t('energyFlow.nodeDischargingLoss'), itemStyle: { color: themeObject.value.warning } },
    { name: t('energyFlow.nodeDischargingOutput'), itemStyle: { color: themeObject.value.success } },
    { name: t('energyFlow.nodeAux'), itemStyle: { color: themeObject.value.warning } }
  ]

  const links = [
    {
      source: 0,
      target: 1,
      value: totalCharging.value * (1 - chargingEfficiency.value / 100),
      itemStyle: { color: themeObject.value.danger }
    },
    {
      source: 0,
      target: 2,
      value: (totalCharging.value * chargingEfficiency.value) / 100,
      itemStyle: { color: themeObject.value.primary }
    },
    {
      source: 2,
      target: 3,
      value: totalDischarging.value * (1 - dischargingEfficiency.value / 100),
      itemStyle: { color: themeObject.value.warning }
    },
    {
      source: 2,
      target: 4,
      value: (totalDischarging.value * dischargingEfficiency.value) / 100,
      itemStyle: { color: themeObject.value.success }
    },
    {
      source: 2,
      target: 5,
      value: totalCapacityMWh.value * 0.02 * operatingDays.value,
      itemStyle: { color: themeObject.value.warning }
    }
  ]

  return { nodes, links }
}

// 更新图表
const updateChart = () => {
  if (!sankeyChart) return

  const { nodes, links } = generateSankeyData()

  sankeyChart.setOption({
    title: {
      text: '能量流分析 Energy Flow Analysis',
      left: 'center',
      textStyle: {
        color:
          getComputedStyle(document.documentElement).getPropertyValue('--color-text') || 'var(--color-text-secondary)',
        fontSize: 12,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        if (params.dataType === 'node') {
          return `${params.name}<br/>${t('energyFlow.energy')}: ${formatEnergy(params.value)}`
        } else {
          return `${params.data.source} → ${params.data.target}<br/>${t('energyFlow.flow')}: ${formatEnergy(params.value)}<br/>${t('energyFlow.ratio')}: ${((params.value / totalCharging.value) * 100).toFixed(1)}%`
        }
      }
    },
    series: [
      {
        type: 'sankey',
        data: nodes,
        links: links,
        emphasis: {
          focus: 'adjacency'
        },
        lineStyle: {
          color: 'source',
          curveness: 0.5
        },
        label: {
          show: true,
          position: 'right',
          fontSize: 10,
          color:
            getComputedStyle(document.documentElement).getPropertyValue('--color-text-secondary') ||
            'var(--color-text-secondary)'
        },
        levels: [
          {
            depth: 0,
            itemStyle: {
              borderWidth: 2
            },
            lineStyle: {
              color: 'source',
              width: 4
            }
          },
          {
            depth: 1,
            lineStyle: {
              width: 3
            }
          },
          {
            depth: 2,
            lineStyle: {
              width: 2
            }
          }
        ]
      }
    ]
  })
}

// 初始化图表
const initChart = () => {
  if (sankeyChart) {
    sankeyChart.dispose()
  }

  sankeyChart = echarts.init(sankeyChartRef.value, themeObject.value)
  updateChart()
}

// 监听主题变化
const watchTheme = () => {
  const observer = new MutationObserver(() => {
    updateChart()
  })

  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['data-theme']
  })

  return observer
}

// 组件挂载
onMounted(() => {
  initChart()
  themeObserver = watchTheme()

  watch(
    [() => props.params, () => props.soh],
    debounce(() => {
      updateChart()
    }, 300),
    { deep: true }
  )

  watch([cyclesPerDay, operatingDays, chargingEfficiency, dischargingEfficiency], () => {
    updateChart()
  })

  _resizeHandler = () => {
    sankeyChart?.resize()
  }
  window.addEventListener('resize', _resizeHandler)
})

// 组件卸载
onUnmounted(() => {
  if (sankeyChart) {
    sankeyChart.dispose()
    sankeyChart = null
  }
  if (themeObserver) {
    themeObserver.disconnect()
    themeObserver = null
  }
  if (_resizeHandler) {
    window.removeEventListener('resize', _resizeHandler)
    _resizeHandler = null
  }
})
</script>
