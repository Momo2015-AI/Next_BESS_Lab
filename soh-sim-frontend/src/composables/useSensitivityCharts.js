import { onMounted, onUnmounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, RadarChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, GridComponent, LegendComponent, RadarComponent } from 'echarts/components'
import { useChartTheme } from './useChartTheme.js'

echarts.use([
  CanvasRenderer,
  BarChart,
  RadarChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  RadarComponent
])

export function useSensitivityCharts(analysisResults, tornadoChartRef, spiderChartRef) {
  const { t } = useI18n()
  const { themeObject } = useChartTheme()

  watch(themeObject, () => {
    updateTornadoChart()
    updateSpiderChart()
  })
  let tornadoInstance = null
  let spiderInstance = null
  let _resizeHandler = null

  function updateTornadoChart() {
    if (!tornadoChartRef.value) return

    if (!tornadoInstance) {
      tornadoInstance = echarts.init(tornadoChartRef.value, themeObject.value)
    }

    const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
    const tObj = themeObject.value
    const colors = {
      success: tObj.success,
      danger: tObj.danger,
      textMuted: tObj.axisLabel,
      legendText: tObj.legendText,
      axisLine: tObj.gridLine,
      splitLine: tObj.splitLine,
      tooltipBg: tObj.tooltipBg,
      tooltipText: tObj.tooltipText
    }

    const sortedResults = [...analysisResults.value].sort((a, b) => b.sensitivityScore - a.sensitivityScore)

    const categories = sortedResults.map((r) => (r.paramKey ? t(r.paramKey) : r.param))
    const npvData = sortedResults.map((r) => ({
      value: r.npvImpact,
      itemStyle: { color: r.npvImpact > 0 ? colors.success : colors.danger }
    }))

    const option = {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        backgroundColor: colors.tooltipBg,
        textStyle: { color: colors.tooltipText, fontSize: 11 },
        formatter: (params) => {
          const idx = params[0].dataIndex
          const result = sortedResults[idx]
          const paramName = result.paramKey ? t(result.paramKey) : result.param
          return `${paramName}<br/>${t('sensitivity.npvImpact')}: ${result.npvImpact.toFixed(2)}%<br/>${t('sensitivity.irrImpact')}: ${result.irrImpact.toFixed(2)}%<br/>${t('sensitivity.lcosImpact')}: ${result.lcosImpact.toFixed(2)}%`
        }
      },
      grid: {
        left: 100,
        right: 80,
        top: 20,
        bottom: 30
      },
      xAxis: {
        type: 'value',
        name: t('sensitivity.impactDegree'),
        nameTextStyle: { color: colors.textMuted, fontSize: 10 },
        axisLabel: { color: colors.textMuted, fontSize: 10 },
        axisLine: { lineStyle: { color: colors.axisLine } },
        splitLine: { lineStyle: { color: colors.splitLine } }
      },
      yAxis: {
        type: 'category',
        data: categories,
        axisLabel: { color: colors.legendText, fontSize: 11 },
        axisLine: { lineStyle: { color: colors.axisLine } }
      },
      series: [
        {
          type: 'bar',
          data: npvData,
          barWidth: '60%',
          label: {
            show: true,
            position: 'right',
            formatter: '{c}%',
            color: colors.legendText,
            fontSize: 10
          }
        }
      ]
    }

    tornadoInstance.setOption(option, true)
  }

  function updateSpiderChart() {
    if (!spiderChartRef.value) return

    if (!spiderInstance) {
      spiderInstance = echarts.init(spiderChartRef.value, themeObject.value)
    }

    const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
    const tObj = themeObject.value
    const colors = {
      npvLine: tObj.acLine,
      irrLine: tObj.info,
      lcosLine: tObj.orange,
      npvArea: isDark ? 'rgba(45, 212, 191, 0.1)' : 'rgba(20, 184, 166, 0.08)',
      irrArea: isDark ? 'rgba(56, 189, 248, 0.1)' : 'rgba(14, 165, 233, 0.08)',
      lcosArea: isDark ? 'rgba(251, 146, 60, 0.1)' : 'rgba(249, 115, 22, 0.08)',
      legendText: tObj.legendText,
      axisLine: tObj.gridLine,
      splitLine: tObj.splitLine,
      splitArea: isDark ? 'rgba(30, 41, 59, 0.3)' : 'rgba(241, 245, 249, 0.5)',
      tooltipBg: tObj.tooltipBg,
      tooltipText: tObj.tooltipText
    }

    const topResults = [...analysisResults.value].sort((a, b) => b.sensitivityScore - a.sensitivityScore).slice(0, 3)

    if (topResults.length === 0) return

    const indicators = topResults.map((r) => ({
      name: r.paramKey ? t(r.paramKey) : r.param,
      max: Math.max(Math.abs(r.npvImpact), Math.abs(r.irrImpact), Math.abs(r.lcosImpact)) * 1.2
    }))

    const seriesData = [
      {
        name: t('sensitivity.seriesNpv'),
        value: topResults.map((r) => Math.abs(r.npvImpact)),
        lineStyle: { color: colors.npvLine },
        areaStyle: { color: colors.npvArea },
        itemStyle: { color: colors.npvLine }
      },
      {
        name: t('sensitivity.seriesIrr'),
        value: topResults.map((r) => Math.abs(r.irrImpact)),
        lineStyle: { color: colors.irrLine },
        areaStyle: { color: colors.irrArea },
        itemStyle: { color: colors.irrLine }
      },
      {
        name: t('sensitivity.seriesLcos'),
        value: topResults.map((r) => Math.abs(r.lcosImpact)),
        lineStyle: { color: colors.lcosLine },
        areaStyle: { color: colors.lcosArea },
        itemStyle: { color: colors.lcosLine }
      }
    ]

    const option = {
      backgroundColor: 'transparent',
      tooltip: {
        backgroundColor: colors.tooltipBg,
        textStyle: { color: colors.tooltipText, fontSize: 11 }
      },
      legend: {
        data: [t('sensitivity.seriesNpv'), t('sensitivity.seriesIrr'), t('sensitivity.seriesLcos')],
        textStyle: { color: colors.legendText, fontSize: 10 },
        top: 5
      },
      radar: {
        indicator: indicators,
        axisName: { color: colors.legendText, fontSize: 10 },
        splitArea: { areaStyle: { color: [colors.splitArea] } },
        axisLine: { lineStyle: { color: colors.axisLine } },
        splitLine: { lineStyle: { color: colors.splitLine } }
      },
      series: [
        {
          type: 'radar',
          data: seriesData
        }
      ]
    }

    spiderInstance.setOption(option, true)
  }

  onMounted(() => {
    _resizeHandler = () => {
      tornadoInstance?.resize()
      spiderInstance?.resize()
    }
    window.addEventListener('resize', _resizeHandler)
  })

  onUnmounted(() => {
    if (tornadoInstance) {
      tornadoInstance.dispose()
      tornadoInstance = null
    }
    if (spiderInstance) {
      spiderInstance.dispose()
      spiderInstance = null
    }
    if (_resizeHandler) {
      window.removeEventListener('resize', _resizeHandler)
      _resizeHandler = null
    }
  })

  return { updateTornadoChart, updateSpiderChart }
}
