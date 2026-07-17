<template>
  <div class="rounded p-3 card-panel-bordered">
    <h4 class="text-xs mb-2 font-medium">{{ $t('simLab.titleSohCurve') }}</h4>
    <div ref="chartRef" class="chart-container-sm" />
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, GridComponent, LegendComponent } from 'echarts/components'
import { useChartTheme } from '../composables/useChartTheme.js'

echarts.use([CanvasRenderer, LineChart, TitleComponent, TooltipComponent, GridComponent, LegendComponent])

const { t } = useI18n()
const { themeObject } = useChartTheme()

const props = defineProps({
  sohCurve: { type: Array, default: () => [] },
  rteCurve: { type: Array, default: () => [] },
  guaranteeSoh: { type: Number, default: 70 }
})

const chartRef = ref(null)
let chartInstance = null
let _resizeHandler = null

function renderChart() {
  if (!chartRef.value || !props.sohCurve.length) return
  if (chartInstance) chartInstance.dispose()

  chartInstance = echarts.init(chartRef.value, themeObject.value)
  const years = Array.from({ length: props.sohCurve.length }, (_, i) => i)
  const colors = themeObject.value

  chartInstance.setOption({
    tooltip: { trigger: 'axis' },
    legend: {
      data: [t('simLab.chartSoh'), t('simLab.chartRte'), t('simLab.chartGuaranteeLine')],
      top: 0,
      textStyle: { color: colors.legendText, fontSize: 10 }
    },
    grid: { left: 40, right: 20, top: 30, bottom: 20 },
    xAxis: { type: 'category', data: years, axisLabel: { color: colors.axisLabel, fontSize: 10 } },
    yAxis: { type: 'value', min: 50, max: 100, axisLabel: { color: colors.axisLabel, fontSize: 10 } },
    series: [
      {
        name: t('simLab.chartSoh'),
        type: 'line',
        data: props.sohCurve,
        smooth: true,
        lineStyle: { color: colors.primary },
        itemStyle: { color: colors.primary }
      },
      {
        name: t('simLab.chartRte'),
        type: 'line',
        data: props.rteCurve,
        smooth: true,
        lineStyle: { color: colors.cyan },
        itemStyle: { color: colors.cyan }
      },
      {
        name: t('simLab.chartGuaranteeLine'),
        type: 'line',
        data: Array.from({ length: years.length }, () => props.guaranteeSoh),
        lineStyle: { color: colors.warning, type: 'dashed' },
        itemStyle: { color: colors.warning }
      }
    ]
  })
  chartInstance.resize()
}

function handleResize() {
  chartInstance?.resize()
}

watch(
  () => props.sohCurve,
  () => nextTick(renderChart)
)
watch(themeObject, () => nextTick(renderChart))

onMounted(() => {
  nextTick(renderChart)
  _resizeHandler = handleResize
  window.addEventListener('resize', _resizeHandler)
})

onUnmounted(() => {
  chartInstance?.dispose()
  chartInstance = null
  if (_resizeHandler) {
    window.removeEventListener('resize', _resizeHandler)
    _resizeHandler = null
  }
})

defineExpose({ renderChart })
</script>
