<template>
  <div class="rounded-lg p-3 card-bordered">
    <h3 class="font-bold text-xs mb-2 flex items-center gap-2 text-default">
      <span
        class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold u-background-color-rgba-139-92-246-0-2-color-var-color-accent"
      >
        BH
      </span>
      {{ $t('heatmap.title') }}
    </h3>

    <div class="mb-3 flex justify-between text-[10px] text-secondary">
      <div>{{ $t('heatmap.legend') }}</div>
      <div>{{ $t('heatmap.clickDetail') }}</div>
    </div>

    <div ref="heatmapRef" class="chart-container" />

    <div class="mt-3 grid grid-cols-5 gap-2 text-[10px]">
      <div class="flex items-center">
        <div class="w-3 h-3 rounded mr-1 bg-success" />
        <span>>90%</span>
        class="text-success"
      </div>
      <div class="flex items-center">
        <div class="w-3 h-3 rounded mr-1 bg-success" />
        <span>80-90%</span>
        class="text-success"
      </div>
      <div class="flex items-center">
        <div class="w-3 h-3 rounded mr-1 bg-warning" />
        <span>70-80%</span>
        class="text-warning"
      </div>
      <div class="flex items-center">
        <div class="w-3 h-3 rounded mr-1 u-background-color-var-color-chart-orange" />
        <span>60-70%</span>
        class="text-warning"
      </div>
      <div class="flex items-center">
        <div class="w-3 h-3 rounded mr-1 bg-danger" />
        <span>&lt;60%</span>
        class="text-danger"
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { debounce } from 'lodash-es'

const { t } = useI18n()
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { HeatmapChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  VisualMapComponent
} from 'echarts/components'
import { useChartTheme } from '../composables/useChartTheme.js'
echarts.use([
  CanvasRenderer,
  HeatmapChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  VisualMapComponent
])

const { themeObject } = useChartTheme()

watch(themeObject, () => {
  nextTick(renderHeatmap)
})

const props = defineProps({
  params: Object,
  soh: Array,
  cellData: Array // 假设有电池单元数据
})

const heatmapRef = ref(null)
let heatmap = null

// 生成模拟电池单元健康数据
const generateHeatmapData = () => {
  const data = []
  const rows = 10 // 电池组行数
  const cols = 12 // 电池组列数

  for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) {
      // 基于SOH数据和随机因素生成健康值
      const baseHealth = props.soh && props.soh.length > 0 ? props.soh[0] * 100 : 95
      const variation = Math.random() * 10 - 5 // ±5% 变化
      const health = Math.max(50, Math.min(100, baseHealth + variation))

      data.push([j, i, health]) // [x, y, value]
    }
  }

  return {
    data,
    rows,
    cols
  }
}

const renderHeatmap = () => {
  if (!heatmapRef.value) return

  if (heatmap) {
    heatmap.dispose()
  }

  const colors = {
    success: themeObject.value.success,
    warning: themeObject.value.warning,
    danger: themeObject.value.danger,
    info: themeObject.value.primary,
    purple: themeObject.value.purple,
    muted: themeObject.value.muted
  }

  const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
  const bgColor = isDark ? '#0f172a' : 'var(--color-text-on-accent)' // bg色
  const textColor = isDark ? 'var(--color-border-light)' : 'var(--color-border)' // text色
  const borderColor = isDark ? 'var(--color-border)' : '#cbd5e1' // border色

  heatmap = echarts.init(heatmapRef.value, themeObject.value, {
    renderer: 'canvas'
  })

  const handleResize = () => {
    heatmap?.resize()
  }

  onMounted(() => {
    nextTick(() => {
      renderHeatmap()
    })
    window.addEventListener('resize', handleResize)
  })

  onUnmounted(() => {
    if (heatmap) {
      heatmap.dispose()
      heatmap = null
    }
    window.removeEventListener('resize', handleResize)
  })

  const { data, rows, cols } = generateHeatmapData()

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      position: 'top',
      formatter: function (params) {
        const x = params.data[0]
        const y = params.data[1]
        const value = params.data[2]
        return t('heatmap.cellHealth', { col: String.fromCharCode(65 + y), row: x + 1, value: value.toFixed(1) })
      }
    },
    grid: {
      height: '85%',
      top: '5%'
    },
    xAxis: {
      type: 'category',
      data: Array.from({ length: cols }, (_, i) => i + 1),
      splitArea: {
        show: true
      },
      axisLabel: {
        color: textColor,
        fontSize: 9
      },
      axisLine: {
        lineStyle: {
          color: borderColor
        }
      }
    },
    yAxis: {
      type: 'category',
      data: Array.from({ length: rows }, (_, i) => String.fromCharCode(65 + i)),
      splitArea: {
        show: true
      },
      axisLabel: {
        color: textColor,
        fontSize: 9
      },
      axisLine: {
        lineStyle: {
          color: borderColor
        }
      }
    },
    visualMap: {
      min: 50,
      max: 100,
      calculable: true,
      orient: 'vertical',
      left: 'right',
      top: 'center',
      inRange: {
        color: [
          themeObject.value.danger,
          themeObject.value.orange,
          themeObject.value.warning,
          themeObject.value.success,
          themeObject.value.success
        ]
      },
      textStyle: {
        color: textColor
      }
    },
    series: [
      {
        name: t('heatmap.healthStatus'),
        type: 'heatmap',
        data: data,
        label: {
          show: true,
          formatter: (params) => {
            return params.value[2].toFixed(0) + '%'
          },
          fontSize: 8,
          color: 'var(--color-text-on-accent)'
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }

  heatmap.setOption(option)

  // 添加点击事件
  heatmap.on('click', function (params) {
    if (params.componentType === 'series') {
      // 点击单元格可扩展详细信息
      // 这里可以触发显示详细信息的逻辑
    }
  })
}

// 监听props变化重新渲染
watch(
  () => [props.soh, props.cellData],
  debounce(() => {
    nextTick(() => {
      renderHeatmap()
    })
  }, 300),
  { deep: true }
)

// 监听主题变化
watch(
  () => document.documentElement.getAttribute('data-theme'),
  () => {
    nextTick(() => {
      if (heatmap) {
        heatmap.dispose()
        renderHeatmap()
      }
    })
  }
)
</script>
