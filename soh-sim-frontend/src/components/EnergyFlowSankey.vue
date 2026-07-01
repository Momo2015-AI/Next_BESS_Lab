<template>
  <div class="rounded-lg p-3" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
    <h3 class="font-bold text-xs mb-2 flex items-center gap-2" style="color: var(--color-text);">
      <span class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold" style="background-color: rgba(16, 185, 129, 0.2); color: var(--color-success);">VIII</span>
      能量流桑基图 Energy Flow Sankey
    </h3>
    
    <div class="mb-2 flex items-center gap-2 text-[10px]" style="color: var(--color-text-secondary);">
      <div class="flex items-center gap-1">
        <div class="w-3 h-3 rounded" style="background-color: #3b82f6;"></div>
        <span>充电 Charging</span>
      </div>
      <div class="flex items-center gap-1">
        <div class="w-3 h-3 rounded" style="background-color: #ef4444;"></div>
        <span>损失 Loss</span>
      </div>
      <div class="flex items-center gap-1">
        <div class="w-3 h-3 rounded" style="background-color: #10b981;"></div>
        <span>放电 Discharging</span>
      </div>
      <div class="flex items-center gap-1">
        <div class="w-3 h-3 rounded" style="background-color: #f59e0b;"></div>
        <span>辅助 Auxiliary</span>
      </div>
    </div>
    
    <div ref="sankeyChartRef" class="w-full" style="height: 350px;"></div>
    
    <!-- 参数控制 -->
    <div class="mt-3 grid grid-cols-2 gap-2 text-[10px]" style="color: var(--color-text-secondary);">
      <div>
        <label class="block mb-0.5" style="color: var(--color-text-muted);">循环次数/天</label>
        <input v-model.number="cyclesPerDay" type="number" step="0.1" min="0.1" max="10" class="w-full rounded px-2 py-1 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" @input="updateChart" />
      </div>
      <div>
        <label class="block mb-0.5" style="color: var(--color-text-muted);">可用天数/年</label>
        <input v-model.number="operatingDays" type="number" step="1" min="1" max="365" class="w-full rounded px-2 py-1 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" @input="updateChart" />
      </div>
      <div>
        <label class="block mb-0.5" style="color: var(--color-text-muted);">充电效率 %</label>
        <input v-model.number="chargingEfficiency" type="number" step="1" min="50" max="100" class="w-full rounded px-2 py-1 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" @input="updateChart" />
      </div>
      <div>
        <label class="block mb-0.5" style="color: var(--color-text-muted);">放电效率 %</label>
        <input v-model.number="dischargingEfficiency" type="number" step="1" min="50" max="100" class="w-full rounded px-2 py-1 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" @input="updateChart" />
      </div>
    </div>
    
    <!-- 能量摘要 -->
    <div class="mt-3 border-t pt-2" style="border-color: var(--color-border);">
      <div class="grid grid-cols-2 gap-2 text-[10px]">
        <div class="rounded p-2" style="background-color: var(--color-card-dark);">
          <div style="color: var(--color-text-muted);">总充电量</div>
          <div class="font-mono mt-0.5" style="color: var(--color-accent);">{{ formatEnergy(totalCharging) }}</div>
        </div>
        <div class="rounded p-2" style="background-color: var(--color-card-dark);">
          <div style="color: var(--color-text-muted);">总放电量</div>
          <div class="font-mono mt-0.5" style="color: var(--color-success);">{{ formatEnergy(totalDischarging) }}</div>
        </div>
        <div class="rounded p-2" style="background-color: var(--color-card-dark);">
          <div style="color: var(--color-text-muted);">能量损失</div>
          <div class="font-mono mt-0.5" style="color: var(--color-danger);">{{ formatEnergy(totalLoss) }}</div>
        </div>
        <div class="rounded p-2" style="background-color: var(--color-card-dark);">
          <div style="color: var(--color-text-muted);">系统效率</div>
          <div class="font-mono mt-0.5" style="color: var(--color-warning);">{{ systemEfficiency.toFixed(1) }}%</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, computed, watch } from 'vue'
import { debounce } from 'lodash-es'
import * as echarts from 'echarts'

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
    { name: '充电输入', itemStyle: { color: '#3b82f6' } },
    { name: '充电损失', itemStyle: { color: '#ef4444' } },
    { name: '电池储能', itemStyle: { color: '#8b5cf6' } },
    { name: '放电损失', itemStyle: { color: '#f59e0b' } },
    { name: '放电输出', itemStyle: { color: '#10b981' } },
    { name: '辅助消耗', itemStyle: { color: '#f59e0b' } }
  ]
  
  const links = [
    {
      source: 0,
      target: 1,
      value: totalCharging.value * (1 - chargingEfficiency.value / 100),
      itemStyle: { color: '#ef4444' }
    },
    {
      source: 0,
      target: 2,
      value: totalCharging.value * chargingEfficiency.value / 100,
      itemStyle: { color: '#3b82f6' }
    },
    {
      source: 2,
      target: 3,
      value: totalDischarging.value * (1 - dischargingEfficiency.value / 100),
      itemStyle: { color: '#f59e0b' }
    },
    {
      source: 2,
      target: 4,
      value: totalDischarging.value * dischargingEfficiency.value / 100,
      itemStyle: { color: '#10b981' }
    },
    {
      source: 2,
      target: 5,
      value: totalCapacityMWh.value * 0.02 * operatingDays.value, // 2% auxiliary consumption
      itemStyle: { color: '#f59e0b' }
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
        color: getComputedStyle(document.documentElement).getPropertyValue('--color-text') || '#64748b',
        fontSize: 12,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        if (params.dataType === 'node') {
          return `${params.name}<br/>能量: ${formatEnergy(params.value)}`
        } else {
          return `${params.data.source} → ${params.data.target}<br/>流量: ${formatEnergy(params.value)}<br/>占比: ${((params.value / totalCharging.value) * 100).toFixed(1)}%`
        }
      }
    },
    series: [{
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
        color: getComputedStyle(document.documentElement).getPropertyValue('--color-text-secondary') || '#64748b'
      },
      levels: [{
        depth: 0,
        itemStyle: {
          borderWidth: 2
        },
        lineStyle: {
          color: 'source',
          width: 4
        }
      }, {
        depth: 1,
        lineStyle: {
          width: 3
        }
      }, {
        depth: 2,
        lineStyle: {
          width: 2
        }
      }]
    }]
  })
}

// 初始化图表
const initChart = () => {
  if (sankeyChart) {
    sankeyChart.dispose()
  }
  
  sankeyChart = echarts.init(sankeyChartRef.value)
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

  watch([() => props.params, () => props.soh], debounce(() => {
    updateChart()
  }, 300), { deep: true })

  watch([cyclesPerDay, operatingDays, chargingEfficiency, dischargingEfficiency], () => {
    updateChart()
  })

  _resizeHandler = () => { sankeyChart?.resize() }
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