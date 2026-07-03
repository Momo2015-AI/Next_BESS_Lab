<template>
  <div class="rounded-lg p-3" style="background-color: var(--color-card); border: 1px solid var(--color-border)">
    <h3 class="font-bold text-xs mb-2 flex items-center gap-2" style="color: var(--color-text)">
      <span
        class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold"
        style="background-color: rgba(139, 92, 246, 0.2); color: var(--color-accent)"
      >
        IX
      </span>
      成本构成瀑布图 Cost Structure Waterfall
    </h3>

    <div class="mb-2 flex items-center justify-between text-[10px]" style="color: var(--color-text-secondary)">
      <div>年度成本分析 Annual Cost Breakdown</div>
      <select
        v-model="selectedYear"
        class="rounded px-2 py-1 text-xs"
        style="
          background-color: var(--color-input-bg-dark);
          border: 1px solid var(--color-input-border);
          color: var(--color-text);
        "
      >
        <option v-for="year in availableYears" :key="year" :value="year">Year {{ year }}</option>
      </select>
    </div>

    <div ref="waterfallChartRef" class="w-full" style="height: 300px" />

    <!-- 成本摘要 -->
    <div class="mt-3 border-t pt-2" style="border-color: var(--color-border)">
      <div class="grid grid-cols-2 gap-2 text-[10px]">
        <div class="rounded p-2" style="background-color: var(--color-card-dark)">
          <div style="color: var(--color-text-muted)">总成本</div>
          <div class="font-mono mt-0.5" style="color: var(--color-danger)">
            {{ formatCurrency(totalCost) }}
          </div>
        </div>
        <div class="rounded p-2" style="background-color: var(--color-card-dark)">
          <div style="color: var(--color-text-muted)">单位成本</div>
          <div class="font-mono mt-0.5" style="color: var(--color-warning)">
            {{ formatCostPerMWh(costPerMWh) }}
          </div>
        </div>
      </div>
    </div>

    <!-- 成本明细 -->
    <div class="mt-2 space-y-1 text-[9x]" style="color: var(--color-text-muted)">
      <div class="flex justify-between">
        <span>初始CAPEX</span>
        <span>{{ formatCurrency(initialCapex) }}</span>
      </div>
      <div class="flex justify-between">
        <span>年度OPEX</span>
        <span>{{ formatCurrency(annualOpex) }}</span>
      </div>
      <div class="flex justify-between">
        <span>维护成本</span>
        <span>{{ formatCurrency(maintenanceCost) }}</span>
      </div>
      <div class="flex justify-between">
        <span>保险费用</span>
        <span>{{ formatCurrency(insuranceCost) }}</span>
      </div>
      <div class="flex justify-between">
        <span>土地租金</span>
        <span>{{ formatCurrency(landLeaseCost) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, computed, watch } from 'vue'
import { debounce } from 'lodash-es'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, GridComponent, LegendComponent } from 'echarts/components'
import { useDraft } from '../composables/useDraft'
echarts.use([CanvasRenderer, BarChart, LineChart, TitleComponent, TooltipComponent, GridComponent, LegendComponent])

const props = defineProps({
  params: Object,
  cashFlowTable: Array
})

const waterfallChartRef = ref(null)
let waterfallChart = null
let themeObserver = null
let _resizeHandler = null

// 年份选择
const selectedYear = ref(1)
const availableYears = computed(() => {
  if (!props.cashFlowTable || props.cashFlowTable.length === 0) return []
  return props.cashFlowTable.filter((row) => row.year > 0).map((row) => row.year)
})

// 成本计算
const initialCapex = computed(() => {
  if (!props.cashFlowTable || props.cashFlowTable.length === 0) return 0
  return Math.abs(props.cashFlowTable[0]?.augCapex || 0)
})

const annualOpex = computed(() => {
  if (!props.cashFlowTable || props.cashFlowTable.length === 0) return 0
  const yearData = props.cashFlowTable.find((row) => row.year === selectedYear.value)
  return yearData?.opex || 0
})

const maintenanceCost = computed(() => {
  if (!props.cashFlowTable || props.cashFlowTable.length === 0) return 0
  const yearData = props.cashFlowTable.find((row) => row.year === selectedYear.value)
  return yearData?.opex * 0.6 || 0 // 60% for maintenance
})

const insuranceCost = computed(() => {
  if (!props.cashFlowTable || props.cashFlowTable.length === 0) return 0
  const yearData = props.cashFlowTable.find((row) => row.year === selectedYear.value)
  return yearData?.opex * 0.15 || 0 // 15% for insurance
})

const landLeaseCost = computed(() => {
  if (!props.cashFlowTable || props.cashFlowTable.length === 0) return 0
  const yearData = props.cashFlowTable.find((row) => row.year === selectedYear.value)
  return yearData?.opex * 0.1 || 0 // 10% for land lease
})

const totalCost = computed(() => {
  return initialCapex.value + annualOpex.value + maintenanceCost.value + insuranceCost.value + landLeaseCost.value
})

const costPerMWh = computed(() => {
  if (!props.cashFlowTable || props.cashFlowTable.length === 0) return 0
  const yearData = props.cashFlowTable.find((row) => row.year === selectedYear.value)
  const energy = yearData?.energy || 1
  return totalCost.value / energy
})

// 格式化货币
const formatCurrency = (amount) => {
  if (!amount || isNaN(amount)) return '¥0'
  if (amount >= 10000) {
    return `¥${(amount / 10000).toFixed(1)}万`
  }
  return `¥${amount.toFixed(0)}`
}

const formatCostPerMWh = (cost) => {
  if (!cost || isNaN(cost)) return '¥0/kWh'
  if (cost >= 100) {
    return `¥${(cost / 10000).toFixed(2)}/kWh`
  }
  return `¥${cost.toFixed(0)}/MWh`
}

// 生成瀑布图数据
const generateWaterfallData = () => {
  const baseValue = 0

  // 瀑布图数据：正值为向上，负值为向下
  const data = [
    {
      name: '初始CAPEX',
      value: initialCapex.value,
      itemStyle: { color: 'var(--color-danger)' }
    },
    {
      name: '年度OPEX',
      value: annualOpex.value,
      itemStyle: { color: 'var(--color-warning)' }
    },
    {
      name: '维护成本',
      value: maintenanceCost.value,
      itemStyle: { color: 'var(--color-warning)' }
    },
    {
      name: '保险费用',
      value: insuranceCost.value,
      itemStyle: { color: '#84cc16' }
    },
    {
      name: '土地租金',
      value: landLeaseCost.value,
      itemStyle: { color: 'var(--color-chart-cyan)' }
    }
  ]

  // 计算累计值
  let cumulative = baseValue
  const series = []

  // 第一列：从0到初始值
  series.push({
    name: '初始CAPEX',
    type: 'bar',
    stack: 'total',
    emphasis: { focus: 'series' },
    data: [baseValue],
    itemStyle: { color: 'var(--color-danger)' },
    barWidth: '40%'
  })

  // 中间列：每个成本项
  data.forEach((item, index) => {
    if (index === 0) return // 跳过第一列

    cumulative += item.value
    series.push({
      name: item.name,
      type: 'bar',
      stack: 'total',
      emphasis: { focus: 'series' },
      data: [item.value],
      itemStyle: item.itemStyle,
      barWidth: '40%'
    })
  })

  // 最后一列：累计线
  series.push({
    name: '累计',
    type: 'line',
    yAxisIndex: 1,
    data: [baseValue, cumulative],
    lineStyle: { color: 'var(--color-accent)', width: 2 },
    symbol: 'none',
    silent: true
  })

  return {
    series,
    categories: data.map((item) => item.name)
  }
}

// 更新图表
const updateChart = () => {
  if (!waterfallChart) return

  const { series, categories } = generateWaterfallData()

  waterfallChart.setOption({
    title: {
      text: `Year ${selectedYear.value} Cost Structure`,
      left: 'center',
      textStyle: {
        color:
          getComputedStyle(document.documentElement).getPropertyValue('--color-text') || 'var(--color-text-secondary)',
        fontSize: 12,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: (params) => {
        const param = params[0]
        const value = param.value
        const formatted = formatCurrency(Math.abs(value))
        return `${param.name}<br/>金额: ${formatted}`
      }
    },
    grid: {
      top: 60,
      right: 20,
      bottom: 80,
      left: 60
    },
    xAxis: {
      type: 'category',
      data: categories,
      axisLabel: {
        color:
          getComputedStyle(document.documentElement).getPropertyValue('--color-text-secondary') ||
          'var(--color-text-secondary)',
        fontSize: 9,
        interval: 0,
        rotate: 45
      }
    },
    yAxis: [
      {
        type: 'value',
        name: '金额 (万元)',
        nameTextStyle: {
          color:
            getComputedStyle(document.documentElement).getPropertyValue('--color-text-secondary') ||
            'var(--color-text-secondary)',
          fontSize: 10
        },
        axisLabel: {
          color:
            getComputedStyle(document.documentElement).getPropertyValue('--color-text-secondary') ||
            'var(--color-text-secondary)',
          fontSize: 9,
          formatter: (value) => formatCurrency(value)
        },
        splitLine: {
          lineStyle: {
            color:
              getComputedStyle(document.documentElement).getPropertyValue('--color-border') ||
              'var(--color-border-light)',
            type: 'dashed'
          }
        }
      },
      {
        type: 'value',
        name: '累计线',
        nameTextStyle: {
          color: 'var(--color-accent)',
          fontSize: 10
        },
        axisLine: { show: false },
        axisTick: { show: false },
        axisLabel: { show: false },
        splitLine: { show: false }
      }
    ],
    series: series
  })
}

// 初始化图表
const initChart = () => {
  if (waterfallChart) {
    waterfallChart.dispose()
  }

  waterfallChart = echarts.init(waterfallChartRef.value)
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
    [() => props.cashFlowTable, selectedYear],
    debounce(() => {
      updateChart()
    }, 300),
    { deep: true }
  )

  _resizeHandler = () => {
    waterfallChart?.resize()
  }
  window.addEventListener('resize', _resizeHandler)
})

// 组件卸载
onUnmounted(() => {
  if (waterfallChart) {
    waterfallChart.dispose()
    waterfallChart = null
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
