<template>
  <div class="rounded-lg p-3" style="background-color: var(--color-card); border: 1px solid var(--color-border)">
    <h3 class="font-bold text-xs mb-2 flex items-center gap-2" style="color: var(--color-text)">
      <span
        class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold"
        style="background-color: rgba(139, 92, 246, 0.2); color: var(--color-accent)"
      >
        BH
      </span>
      电池健康状态热力图 Battery Health Heatmap
    </h3>

    <div class="mb-3 flex justify-between text-[10px]" style="color: var(--color-text-secondary)">
      <div>单元格颜色表示健康状态：绿色(>90%) - 红色(&lt;70%)</div>
      <div>点击单元格查看详细信息</div>
    </div>

    <div ref="heatmapRef" class="chart-container" />

    <div class="mt-3 grid grid-cols-5 gap-2 text-[10px]">
      <div class="flex items-center">
        <div class="w-3 h-3 rounded mr-1" style="background-color: var(--color-success)" />
        <span style="color: var(--color-success)">>90%</span>
      </div>
      <div class="flex items-center">
        <div class="w-3 h-3 rounded mr-1" style="background-color: var(--color-success)" />
        <span style="color: var(--color-success)">80-90%</span>
      </div>
      <div class="flex items-center">
        <div class="w-3 h-3 rounded mr-1" style="background-color: var(--color-warning)" />
        <span style="color: var(--color-warning)">70-80%</span>
      </div>
      <div class="flex items-center">
        <div class="w-3 h-3 rounded mr-1" style="background-color: var(--color-chart-orange)" />
        <span style="color: var(--color-warning)">60-70%</span>
      </div>
      <div class="flex items-center">
        <div class="w-3 h-3 rounded mr-1" style="background-color: var(--color-danger)" />
        <span style="color: var(--color-danger)">&lt;60%</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { debounce } from 'lodash-es'
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
import { useDraft } from '../composables/useDraft'
echarts.use([
  CanvasRenderer,
  HeatmapChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  VisualMapComponent
])

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
    success: 'var(--color-success)', // green-500
    warning: 'var(--color-warning)', // amber-500
    danger: 'var(--color-danger)', // red-500
    info: 'var(--color-accent)', // blue-500
    purple: 'var(--color-info)', // violet-500
    muted: 'var(--color-text-secondary)' // slate-400
  }

  const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
  const bgColor = isDark ? '#0f172a' : 'var(--color-text-on-accent)' // bg色
  const textColor = isDark ? 'var(--color-border-light)' : 'var(--color-border)' // text色
  const borderColor = isDark ? 'var(--color-border)' : '#cbd5e1' // border色

  heatmap = echarts.init(heatmapRef.value, null, {
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
        return `单元格 [${String.fromCharCode(65 + y)},${x + 1}]<br/>健康状态: ${value.toFixed(1)}%`
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
          'var(--color-danger)',
          'var(--color-chart-orange)',
          'var(--color-warning)',
          'var(--color-success)',
          'var(--color-success)'
        ]
      },
      textStyle: {
        color: textColor
      }
    },
    series: [
      {
        name: '健康状态',
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
      console.log(
        `Clicked cell [${String.fromCharCode(65 + params.data[1])},${params.data[0] + 1}] with health: ${params.data[2]}%`
      )
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
