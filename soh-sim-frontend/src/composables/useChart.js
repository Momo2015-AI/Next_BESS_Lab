import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart, PieChart, RadarChart, GaugeChart, HeatmapChart, SankeyChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent, PolarComponent, DataZoomComponent, VisualMapComponent, ToolboxComponent } from 'echarts/components'

echarts.use([
  CanvasRenderer,
  LineChart,
  BarChart,
  PieChart,
  RadarChart,
  GaugeChart,
  HeatmapChart,
  SankeyChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  PolarComponent,
  DataZoomComponent,
  VisualMapComponent,
  ToolboxComponent,
])

export function useChart(chartRef, options, dependencies = []) {
  const chart = ref(null)

  const init = () => {
    if (!chartRef.value) return
    if (chart.value) {
      chart.value.dispose()
    }
    chart.value = echarts.init(chartRef.value)
    chart.value.setOption(options.value)
  }

  const resize = () => {
    chart.value?.resize()
  }

  const update = (newOptions) => {
    if (chart.value) {
      chart.value.setOption(newOptions, true)
    }
  }

  onMounted(() => {
    init()
    window.addEventListener('resize', resize)
  })

  onUnmounted(() => {
    window.removeEventListener('resize', resize)
    if (chart.value) {
      chart.value.dispose()
      chart.value = null
    }
  })

  watch([options, ...dependencies], () => {
    if (chart.value && options.value) {
      chart.value.setOption(options.value, true)
    }
  }, { deep: true })

  return { chart, init, resize, update }
}

export function useMultiChart(chartRefs, optionsList, dependencies = []) {
  const charts = ref([])

  const initAll = () => {
    charts.value.forEach((c) => {
      if (c) c.dispose()
    })
    charts.value = chartRefs.value
      .filter((ref) => ref)
      .map((ref) => {
        const instance = echarts.init(ref)
        return instance
      })
    charts.value.forEach((chart, index) => {
      if (optionsList.value[index]) {
        chart.setOption(optionsList.value[index])
      }
    })
  }

  const resizeAll = () => {
    charts.value.forEach((c) => c?.resize())
  }

  const updateAll = (newOptionsList) => {
    charts.value.forEach((chart, index) => {
      if (chart && newOptionsList[index]) {
        chart.setOption(newOptionsList[index], true)
      }
    })
  }

  onMounted(() => {
    initAll()
    window.addEventListener('resize', resizeAll)
  })

  onUnmounted(() => {
    window.removeEventListener('resize', resizeAll)
    charts.value.forEach((c) => c?.dispose())
    charts.value = []
  })

  watch([optionsList, ...dependencies], () => {
    charts.value.forEach((chart, index) => {
      if (chart && optionsList.value[index]) {
        chart.setOption(optionsList.value[index], true)
      }
    })
  }, { deep: true })

  return { charts, initAll, resizeAll, updateAll }
}