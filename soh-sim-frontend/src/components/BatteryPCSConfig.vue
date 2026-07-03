<template>
  <div class="flex flex-col gap-4 h-full overflow-auto p-4">
    <div class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border)">
      <h3 class="text-sm font-bold mb-3 flex items-center gap-2" style="color: var(--color-accent-secondary)">
        <span class="w-2 h-2 rounded-full" style="background-color: var(--color-accent-secondary)" />
        电池集装箱配置
      </h3>

      <div class="grid grid-cols-3 gap-4">
        <div
          class="rounded p-3"
          style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
        >
          <label class="text-xs block mb-2" style="color: var(--color-text-muted)">储能集装箱型号</label>
          <select
            v-model="selectedContainer"
            class="w-full rounded px-3 py-2 text-xs"
            style="
              background-color: var(--color-input-bg-dark);
              border: 1px solid var(--color-input-border);
              color: var(--color-text);
            "
            @change="onContainerChange"
          >
            <option value="">请选择集装箱型号</option>
            <option v-for="container in containers" :key="container.id" :value="container.id">
              {{ container.name }} - {{ container.energy }}MWh / {{ container.power }}MW
            </option>
          </select>
        </div>

        <div
          class="rounded p-3"
          style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
        >
          <label class="text-xs block mb-2" style="color: var(--color-text-muted)">目标总能量 (MWh)</label>
          <input
            v-model.number="targetEnergy"
            type="number"
            min="1"
            step="1"
            class="w-full rounded px-3 py-2 text-xs"
            style="
              background-color: var(--color-input-bg-dark);
              border: 1px solid var(--color-input-border);
              color: var(--color-text);
            "
            placeholder="输入目标总能量"
            @change="autoCalcQty"
          />
        </div>

        <div
          class="rounded p-3"
          style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
        >
          <label class="text-xs block mb-2" style="color: var(--color-text-muted)">集装箱数量 (自动计算)</label>
          <p class="text-lg font-bold" style="color: var(--color-accent-secondary)">{{ containerQty }} 台</p>
        </div>
      </div>

      <div class="grid grid-cols-3 gap-4 mt-4">
        <div
          class="rounded p-3"
          style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
        >
          <label class="text-xs block mb-2" style="color: var(--color-text-muted)">PCS型号</label>
          <select
            v-model="selectedPCS"
            class="w-full rounded px-3 py-2 text-xs"
            style="
              background-color: var(--color-input-bg-dark);
              border: 1px solid var(--color-input-border);
              color: var(--color-text);
            "
            @change="onPCSChange"
          >
            <option value="">请选择PCS型号</option>
            <option v-for="pcs in pcsList" :key="pcs.id" :value="pcs.id">
              {{ pcs.name }} - {{ pcs.power }}MW / {{ pcs.voltage }}V
            </option>
          </select>
        </div>

        <div
          class="rounded p-3"
          style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
        >
          <label class="text-xs block mb-2" style="color: var(--color-text-muted)">目标总功率 (MW)</label>
          <input
            v-model.number="targetPower"
            type="number"
            min="0.1"
            step="0.1"
            class="w-full rounded px-3 py-2 text-xs"
            style="
              background-color: var(--color-input-bg-dark);
              border: 1px solid var(--color-input-border);
              color: var(--color-text);
            "
            placeholder="输入目标总功率"
            @change="autoCalcQty"
          />
        </div>

        <div
          class="rounded p-3"
          style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
        >
          <label class="text-xs block mb-2" style="color: var(--color-text-muted)">PCS 数量 (自动)</label>
          <p class="text-lg font-bold" style="color: var(--color-success)">{{ pcsQty }} 台</p>
        </div>
      </div>

      <div
        class="mt-4 p-4 rounded-lg"
        style="background-color: var(--color-accent-glow); border: 1px solid var(--color-accent-dark)"
      >
        <h4 class="text-xs font-bold mb-3" style="color: var(--color-accent-secondary)">自动计算结果</h4>
        <div class="grid grid-cols-6 gap-3">
          <div class="text-center">
            <p class="text-[10px]" style="color: var(--color-text-muted)">集装箱数</p>
            <p class="text-lg font-bold" style="color: var(--color-accent-secondary)">{{ containerQty }} 台</p>
          </div>
          <div class="text-center">
            <p class="text-[10px]" style="color: var(--color-text-muted)">总能量</p>
            <p class="text-lg font-bold" style="color: var(--color-accent-secondary)">
              {{ totalEnergy.toFixed(1) }} MWh
            </p>
          </div>
          <div class="text-center">
            <p class="text-[10px]" style="color: var(--color-text-muted)">PCS数</p>
            <p class="text-lg font-bold" style="color: var(--color-success)">{{ pcsQty }} 台</p>
          </div>
          <div class="text-center">
            <p class="text-[10px]" style="color: var(--color-text-muted)">总功率</p>
            <p class="text-lg font-bold" style="color: var(--color-accent)">{{ totalPower.toFixed(1) }} MW</p>
          </div>
          <div class="text-center">
            <p class="text-[10px]" style="color: var(--color-text-muted)">运行时长</p>
            <p class="text-lg font-bold" style="color: var(--color-accent-secondary)">
              {{ energyPowerRatio }}
            </p>
          </div>
          <div class="text-center">
            <p class="text-[10px]" style="color: var(--color-text-muted)">配比方式</p>
            <p class="text-lg font-bold" style="color: var(--color-warning)">
              {{ pairingMode }}
            </p>
          </div>
        </div>

        <div class="mt-3 text-[10px]" style="color: var(--color-text-muted)">
          <p>
            <strong style="color: var(--color-text-secondary)">配比说明：</strong>
            {{ pairingDescription }}
          </p>
        </div>
      </div>
    </div>

    <div class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border)">
      <h3 class="text-sm font-bold mb-3 flex items-center gap-2" style="color: var(--color-accent-secondary)">
        <span class="w-2 h-2 rounded-full" style="background-color: var(--color-accent-secondary)" />
        系统连接图
      </h3>

      <div
        ref="connectionDiagram"
        class="h-96 rounded"
        style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
      />

      <div class="mt-3 flex gap-4 text-[10px]">
        <div class="flex items-center gap-1">
          <span class="w-3 h-3 rounded" style="background-color: var(--color-accent-secondary)" />
          <span style="color: var(--color-text-muted)">电池集装箱</span>
        </div>
        <div class="flex items-center gap-1">
          <span class="w-3 h-3 rounded" style="background-color: var(--color-accent)" />
          <span style="color: var(--color-text-muted)">PCS</span>
        </div>
        <div class="flex items-center gap-1">
          <span class="w-3 h-3 rounded" style="background-color: var(--color-warning)" />
          <span style="color: var(--color-text-muted)">变压器</span>
        </div>
        <div class="flex items-center gap-1">
          <span class="w-3 h-3 rounded" style="background-color: var(--color-success)" />
          <span style="color: var(--color-text-muted)">电网</span>
        </div>
        <div class="flex items-center gap-1">
          <span class="w-2 h-0.5" style="background-color: var(--color-text-muted)" />
          <span style="color: var(--color-text-muted)">DC连接</span>
        </div>
        <div class="flex items-center gap-1">
          <span class="w-2 h-0.5" style="background-color: var(--color-warning)" />
          <span style="color: var(--color-text-muted)">AC连接</span>
        </div>
      </div>
    </div>

    <div class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border)">
      <h3 class="text-sm font-bold mb-3 flex items-center gap-2" style="color: var(--color-accent-secondary)">
        <span class="w-2 h-2 rounded-full" style="background-color: var(--color-accent-secondary)" />
        电气单线图
      </h3>

      <div
        ref="singleLineDiagram"
        class="h-[500px] rounded"
        style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
      />

      <div class="mt-3 grid grid-cols-5 gap-2 text-[10px]">
        <div
          class="rounded p-2"
          style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
        >
          <p style="color: var(--color-text-muted)">DC电压范围</p>
          <p class="font-bold" style="color: var(--color-accent-secondary)">
            {{ dcVoltageRange }}
          </p>
        </div>
        <div
          class="rounded p-2"
          style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
        >
          <p style="color: var(--color-text-muted)">AC输出电压</p>
          <p class="font-bold" style="color: var(--color-accent)">
            {{ acVoltage }}
          </p>
        </div>
        <div
          class="rounded p-2"
          style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
        >
          <p style="color: var(--color-text-muted)">额定频率</p>
          <p class="font-bold" style="color: var(--color-warning)">50 Hz</p>
        </div>
        <div
          class="rounded p-2"
          style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
        >
          <p style="color: var(--color-text-muted)">短路容量</p>
          <p class="font-bold" style="color: var(--color-success)">
            {{ shortCircuitCapacity }}
          </p>
        </div>
        <div
          class="rounded p-2"
          style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
        >
          <p style="color: var(--color-text-muted)">接地方式</p>
          <p class="font-bold" style="color: var(--color-accent-secondary)">TN-S</p>
        </div>
      </div>
    </div>

    <div class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border)">
      <h3 class="text-sm font-bold mb-3 flex items-center gap-2" style="color: var(--color-accent-secondary)">
        <span class="w-2 h-2 rounded-full" style="background-color: var(--color-accent-secondary)" />
        推荐配对方案
      </h3>

      <div class="overflow-auto">
        <table class="w-full text-xs">
          <thead style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)">
            <tr>
              <th class="py-2 px-3 text-left">方案编号</th>
              <th class="py-2 px-3 text-left">集装箱配置</th>
              <th class="py-2 px-3 text-left">PCS配置</th>
              <th class="py-2 px-3 text-left">配比方式</th>
              <th class="py-2 px-3 text-left">能量/功率比</th>
              <th class="py-2 px-3 text-left">效率预估</th>
              <th class="py-2 px-3 text-left">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(scheme, idx) in recommendedSchemes"
              :key="idx"
              style="border-bottom: 1px solid var(--color-border)"
            >
              <td class="py-2 px-3" style="color: var(--color-text-muted)">
                {{ scheme.id }}
              </td>
              <td class="py-2 px-3" style="color: var(--color-accent-secondary)">
                {{ scheme.containerConfig }}
              </td>
              <td class="py-2 px-3" style="color: var(--color-accent)">
                {{ scheme.pcsConfig }}
              </td>
              <td class="py-2 px-3" style="color: var(--color-warning)">
                {{ scheme.pairingMode }}
              </td>
              <td class="py-2 px-3" style="color: var(--color-success)">
                {{ scheme.energyPowerRatio }}
              </td>
              <td class="py-2 px-3" style="color: var(--color-accent-secondary)">{{ scheme.efficiency }}%</td>
              <td class="py-2 px-3">
                <button
                  class="text-[10px] px-2 py-1 rounded transition-all"
                  style="background-color: var(--color-accent-glow); color: var(--color-accent-secondary)"
                  @click="applyScheme(scheme)"
                >
                  应用
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="flex justify-end gap-3">
      <button
        class="text-xs px-4 py-2 rounded transition-colors"
        style="
          background-color: var(--color-card-dark);
          border: 1px solid var(--color-border);
          color: var(--color-text-secondary);
        "
        @click="resetConfig"
      >
        重置配置
      </button>
      <button
        class="text-xs px-6 py-2 rounded font-bold transition-colors"
        style="background-color: var(--color-accent-secondary); color: white"
        @click="applyConfig"
      >
        应用到仿真参数
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, GridComponent, LegendComponent, GraphicComponent } from 'echarts/components'
import { useProducts } from '../composables/useProducts'
import { useDraftRef } from '../composables/useDraft'
echarts.use([
  CanvasRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  GraphicComponent
])

const props = defineProps({ active: Boolean, params: Object })
const emit = defineEmits(['applyConfig', 'error'])

const { containers: containersFromProducts, pcs: pcsFromProducts, loadAll } = useProducts()

const containers = ref([])
const pcsList = ref([])

async function loadLibraryData() {
  try {
    await loadAll()

    // 转换数据格式以匹配组件需求
    containers.value = containersFromProducts.value.map((c) => {
      const mapped = { ...c }
      mapped.id = c.id
      mapped.name = c.model
      mapped.energy = c.ratedEnergyMWh ?? c.ratedEnergyMwh ?? 0
      mapped.power = c.ratedPowerMW ?? c.ratedPowerMw ?? 0
      mapped.voltage = 600
      mapped.cells = (c.seriesCount || 0) * (c.parallelCount || 0) || 120
      return mapped
    })

    pcsList.value = pcsFromProducts.value.map((p) => {
      const mapped = { ...p }
      mapped.id = p.id
      mapped.name = p.model
      mapped.power = p.ratedPowerMW ?? p.ratedPowerMw ?? 0
      mapped.voltage = p.acVoltage || 380
      mapped.dcVoltage = p.dcVoltageRange || '--'
      mapped.efficiency = p.efficiency || 97
      return mapped
    })

    // 如果没有数据，使用默认值
    if (containers.value.length === 0 || pcsList.value.length === 0) {
      containers.value = [
        { id: 'container-5mwh', name: '5MWh标准舱', energy: 5, power: 2.5, voltage: 600, cells: 120 },
        { id: 'container-3mwh', name: '3MWh紧凑舱', energy: 3, power: 1.5, voltage: 600, cells: 72 },
        { id: 'container-10mwh', name: '10MWh大容量舱', energy: 10, power: 5, voltage: 800, cells: 240 },
        { id: 'container-2mwh', name: '2MWh小型舱', energy: 2, power: 1, voltage: 400, cells: 48 }
      ]
      pcsList.value = [
        { id: 'pcs-2mw', name: '2MW PCS', power: 2, voltage: 380, dcVoltage: '600-900V', efficiency: 98 },
        { id: 'pcs-1mw', name: '1MW PCS', power: 1, voltage: 380, dcVoltage: '400-600V', efficiency: 97 },
        { id: 'pcs-5mw', name: '5MW PCS', power: 5, voltage: 380, dcVoltage: '800-1200V', efficiency: 98.5 },
        { id: 'pcs-500kw', name: '500kW PCS', power: 0.5, voltage: 380, dcVoltage: '300-500V', efficiency: 96 }
      ]
    }
  } catch (error) {
    console.error('加载产品库失败:', error)
    containers.value = [
      { id: 'container-5mwh', name: '5MWh标准舱', energy: 5, power: 2.5, voltage: 600, cells: 120 },
      { id: 'container-3mwh', name: '3MWh紧凑舱', energy: 3, power: 1.5, voltage: 600, cells: 72 },
      { id: 'container-10mwh', name: '10MWh大容量舱', energy: 10, power: 5, voltage: 800, cells: 240 },
      { id: 'container-2mwh', name: '2MWh小型舱', energy: 2, power: 1, voltage: 400, cells: 48 }
    ]
    pcsList.value = [
      { id: 'pcs-2mw', name: '2MW PCS', power: 2, voltage: 380, dcVoltage: '600-900V', efficiency: 98 },
      { id: 'pcs-1mw', name: '1MW PCS', power: 1, voltage: 380, dcVoltage: '400-600V', efficiency: 97 },
      { id: 'pcs-5mw', name: '5MW PCS', power: 5, voltage: 380, dcVoltage: '800-1200V', efficiency: 98.5 },
      { id: 'pcs-500kw', name: '500kW PCS', power: 0.5, voltage: 380, dcVoltage: '300-500V', efficiency: 96 }
    ]
  }
}

// Watch for tab activation - re-render charts when tab becomes visible
watch(
  () => props.active,
  (isActive) => {
    if (isActive) {
      nextTick(() => {
        if (connectionChart) {
          try {
            connectionChart.resize()
          } catch (e) {
            // resize failed silently
          }
          // eslint-disable-next-line vue/no-parsing-error
        }
        if (singleLineChart) {
          try {
            singleLineChart.resize()
          } catch (e) {
            // resize failed silently
          }
        }
        calculatePCS()
      })
    }
  }
)

const selectedContainer = useDraftRef('battery-pcs-selected-container', '').state
const containerQty = useDraftRef('battery-pcs-container-qty', 1).state
const selectedPCS = useDraftRef('battery-pcs-selected-pcs', '').state
const targetEnergy = useDraftRef('battery-pcs-target-energy', null).state
const targetPower = useDraftRef('battery-pcs-target-power', null).state

const energyPowerRatio = computed(() => {
  const e = totalEnergy.value
  const tp =
    targetPower.value != null && targetPower.value > 0 && !isNaN(targetPower.value)
      ? targetPower.value
      : totalPower.value
  if (tp === 0 || e === 0) return '--'
  return (e / tp).toFixed(1) + 'h'
})

const autoCalcQty = () => {
  const container = containers.value.find((c) => c.id === selectedContainer.value)
  if (!container || !(container.energy > 0 && container.power > 0)) return

  const te =
    targetEnergy.value != null && targetEnergy.value > 0 && !isNaN(targetEnergy.value) ? targetEnergy.value : null
  const tp = targetPower.value != null && targetPower.value > 0 && !isNaN(targetPower.value) ? targetPower.value : null

  if (!te && !tp) return

  let qty = 1
  if (te) qty = Math.max(qty, Math.ceil(te / container.energy))
  if (tp) qty = Math.max(qty, Math.ceil(tp / container.power))
  containerQty.value = qty
}

const onContainerChange = () => {
  autoCalcQty()
}

const onPCSChange = () => {
  autoCalcQty()
}

const totalEnergy = computed(() => {
  const container = containers.value.find((c) => c.id === selectedContainer.value)
  return container ? container.energy * containerQty.value : 0
})

const effectiveTargetPower = computed(() => {
  return targetPower.value != null && targetPower.value > 0 && !isNaN(targetPower.value) ? targetPower.value : null
})

const totalPower = computed(() => {
  const container = containers.value.find((c) => c.id === selectedContainer.value)
  if (!container) return 0
  const ratedPower = container.power * containerQty.value
  if (effectiveTargetPower.value != null) {
    return Math.max(ratedPower, effectiveTargetPower.value)
  }
  return ratedPower
})

const pcsQty = computed(() => {
  const pcs = pcsList.value.find((p) => p.id === selectedPCS.value)
  if (!pcs || !pcs.power || pcs.power <= 0) return 0
  if (effectiveTargetPower.value != null) {
    return Math.ceil(effectiveTargetPower.value / pcs.power)
  }
  if (totalPower.value === 0) return 0
  return Math.ceil(totalPower.value / pcs.power)
})
const pairingMode = computed(() => {
  if (!selectedContainer.value || !selectedPCS.value) return '--'
  const ctn = containerQty.value
  const pn = pcsQty.value
  if (ctn === 0 || pn === 0) return '--'
  if (ctn === pn) return '1:1 配对'
  if (ctn > pn) return '多舱并联'
  return '单舱多PCS'
})

const containersPerPCS = computed(() => {
  const ctn = containerQty.value
  const pn = pcsQty.value
  if (pn === 0) return 0
  return Math.ceil(ctn / pn)
})

const pairingDescription = computed(() => {
  if (!selectedContainer.value || !selectedPCS.value) return '请选择集装箱和PCS型号'
  const ctn = containerQty.value
  const pn = pcsQty.value
  if (ctn === 0 || pn === 0) return '请选择集装箱和PCS型号'
  const container = containers.value.find((c) => c.id === selectedContainer.value)
  const pcs = pcsList.value.find((p) => p.id === selectedPCS.value)
  if (!container || !pcs) return '请选择集装箱和PCS型号'

  if (ctn === pn) {
    return `每个${container.name}配置1台${pcs.name}，共${pn}台PCS，独立运行。`
  } else if (ctn > pn) {
    return `每${containersPerPCS.value}个${container.name}并联后接入1台${pcs.name}，共${pn}台PCS。`
  } else {
    const pcsPerContainer = Math.ceil(pn / ctn)
    return `每个${container.name}配置${pcsPerContainer}台${pcs.name}，共${pn}台PCS，并联输出。`
  }
})

const dcVoltageRange = computed(() => {
  const pcs = pcsList.value.find((p) => p.id === selectedPCS.value)
  return pcs ? pcs.dcVoltage : '--'
})

const acVoltage = computed(() => {
  const pcs = pcsList.value.find((p) => p.id === selectedPCS.value)
  return pcs ? `${pcs.voltage}V` : '--'
})

const shortCircuitCapacity = computed(() => {
  const pcs = pcsList.value.find((p) => p.id === selectedPCS.value)
  if (!pcs) return '--'
  return `${pcs.power * 10} MVA`
})

const recommendedSchemes = computed(() => {
  if (!selectedContainer.value) return []
  const container = containers.value.find((c) => c.id === selectedContainer.value)
  if (!container || !container.energy || !container.power) return []

  const schemes = []

  for (let qty = 1; qty <= Math.min(containerQty.value + 2, 10); qty++) {
    const energy = container.energy * qty
    const power = container.power * qty

    for (const pcs of pcsList.value) {
      if (!pcs.power || pcs.power <= 0) continue
      const pcsCount = Math.ceil(power / pcs.power)
      if (pcsCount <= 10 && pcsCount >= 1) {
        const ratio = power / (pcsCount * pcs.power)
        const eff = (pcs.efficiency || 97) - Math.abs(ratio - 1) * 0.5

        schemes.push({
          id: `方案${schemes.length + 1}`,
          containerConfig: `${qty}×${container.name}`,
          pcsConfig: `${pcsCount}×${pcs.name}`,
          pairingMode: qty === pcsCount ? '1:1' : qty > pcsCount ? '多舱并联' : '单舱多PCS',
          energyPowerRatio: `${energy}/${(pcsCount * pcs.power).toFixed(1)}`,
          efficiency: eff.toFixed(1),
          containerQty: qty,
          pcsQty: pcsCount,
          containerId: container.id,
          pcsId: pcs.id
        })
      }
    }
  }

  return schemes.sort((a, b) => b.efficiency - a.efficiency).slice(0, 5)
})

const connectionDiagram = ref(null)
const singleLineDiagram = ref(null)
let connectionChart = null
let singleLineChart = null

const calculatePCS = () => {
  nextTick(() => {
    try {
      renderConnectionDiagram()
    } catch (e) {
      console.error('连接图渲染失败:', e)
    }
    try {
      renderSingleLineDiagram()
    } catch (e) {
      console.error('单线图渲染失败:', e)
    }
  })
}

const renderConnectionDiagram = () => {
  if (!connectionDiagram.value) return

  if (connectionChart) {
    try {
      connectionChart.dispose()
    } catch (e) {
      // resize failed silently
    }
    connectionChart = null
  }

  try {
    connectionChart = echarts.init(connectionDiagram.value)
  } catch (e) {
    console.error('初始化连接图echarts失败:', e)
    return
  }
  if (!connectionChart) return

  const container = containers.value.find((c) => c.id === selectedContainer.value)
  const pcs = pcsList.value.find((p) => p.id === selectedPCS.value)

  if (!container || !pcs) {
    connectionChart.setOption({
      title: {
        text: '请选择集装箱和PCS型号',
        left: 'center',
        top: 'center',
        textStyle: { color: 'var(--color-text-muted)', fontSize: 14 }
      }
    })
    return
  }

  const ctn = containerQty.value
  const pn = pcsQty.value
  if (ctn <= 0 || pn <= 0) {
    connectionChart.setOption({
      title: {
        text: '请设置集装箱数量和PCS数量',
        left: 'center',
        top: 'center',
        textStyle: { color: 'var(--color-text-muted)', fontSize: 14 }
      }
    })
    return
  }

  const nodes = []
  const links = []

  const style = getComputedStyle(document.documentElement)
  const colors = {
    emerald: style.getPropertyValue('--color-success').trim(),
    amber: style.getPropertyValue('--color-warning').trim(),
    sky: style.getPropertyValue('--color-accent').trim(),
    teal: style.getPropertyValue('--color-accent-secondary').trim(),
    slate: style.getPropertyValue('--color-text-muted').trim(),
    text: style.getPropertyValue('--color-text').trim()
  }

  const maxItems = Math.max(ctn, pn, 4)
  const span = Math.min(800, maxItems * 100)
  const startX = (1000 - span) / 2

  nodes.push({
    name: '电网',
    x: 500,
    y: 30,
    symbol: 'circle',
    symbolSize: 42,
    category: 0,
    itemStyle: { color: colors.emerald, shadowBlur: 4, shadowColor: 'rgba(0,0,0,0.3)' },
    label: { show: true, position: 'inside', formatter: '电网', fontSize: 10, color: '#fff' }
  })

  nodes.push({
    name: '变压器',
    x: 500,
    y: 110,
    symbol: 'diamond',
    symbolSize: 34,
    category: 3,
    itemStyle: {
      color: colors.amber,
      shadowBlur: 3,
      shadowOffsetX: 2,
      shadowOffsetY: 2,
      shadowColor: 'rgba(0,0,0,0.25)'
    },
    label: { show: true, position: 'inside', formatter: 'T', fontSize: 12, color: '#fff', fontWeight: 'bold' }
  })
  links.push({ source: '电网', target: '变压器', lineStyle: { color: colors.amber, width: 3, type: 'solid' } })

  const pcsUnitWidth = Math.min(80, span / Math.max(pn, 1))
  for (let i = 0; i < pn; i++) {
    const pcsName = `PCS${i + 1}`
    const pcsX = startX + (i * span) / Math.max(pn - 1, 1) + pcsUnitWidth / 2
    const pcsHalfSpan = pn > 1 ? span / Math.max(pn - 1, 1) / 2 : span / 2
    nodes.push({
      name: pcsName,
      x: pcsX,
      y: 200,
      symbol: 'rect',
      symbolSize: [pcsUnitWidth - 8, 44],
      category: 1,
      itemStyle: {
        color: colors.sky,
        shadowBlur: 4,
        shadowOffsetX: 2,
        shadowOffsetY: 2,
        shadowColor: 'rgba(0,0,0,0.25)',
        borderColor: style.getPropertyValue('--color-accent').trim() + '99',
        borderWidth: 1
      },
      label: { show: true, position: 'inside', formatter: `PCS${i + 1}\n${pcs.power}MW`, fontSize: 9, color: '#fff' }
    })
    links.push({ source: '变压器', target: pcsName, lineStyle: { color: colors.amber, width: 2, type: 'solid' } })
  }

  const containersPerPCSVal = Math.ceil(ctn / Math.max(pn, 1))
  const containerUnitWidth = Math.min(80, (span / Math.max(containersPerPCSVal, 1) / Math.max(pn, 1)) * 0.9)
  for (let i = 0; i < ctn; i++) {
    const containerName = `电池舱${i + 1}`
    const pcsGroupIdx = Math.min(Math.floor(i / Math.max(containersPerPCSVal, 1)), pn - 1)
    const pcsX = startX + (pcsGroupIdx * span) / Math.max(pn - 1, 1) + pcsUnitWidth / 2
    const containerInGroup = i % containersPerPCSVal
    const groupWidth = pn > 1 ? span / Math.max(pn - 1, 1) : span
    const containerOffset = (containerInGroup - (containersPerPCSVal - 1) / 2) * (containerUnitWidth + 4)
    const containerX = pcsX + containerOffset
    nodes.push({
      name: containerName,
      x: containerX,
      y: 290,
      symbol: 'rect',
      symbolSize: [containerUnitWidth - 10, 56],
      category: 2,
      itemStyle: {
        color: colors.teal,
        shadowBlur: 8,
        shadowOffsetX: 4,
        shadowOffsetY: 4,
        shadowColor: 'rgba(0,0,0,0.35)',
        borderColor: style.getPropertyValue('--color-accent-secondary').trim() + '99',
        borderWidth: 2
      },
      label: {
        show: true,
        position: 'inside',
        formatter: `舱${i + 1}\n${container.energy}MWh`,
        fontSize: 9,
        color: '#fff'
      }
    })

    const targetPcs = `PCS${pcsGroupIdx + 1}`
    links.push({
      source: targetPcs,
      target: containerName,
      lineStyle: { color: colors.slate, width: 2, type: 'solid' }
    })
  }

  connectionChart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(30, 41, 59, 0.9)',
      borderColor: 'rgba(100, 116, 139, 0.3)',
      textStyle: { color: '#e2e8f0', fontSize: 11 },
      formatter: (p) => {
        if (!p.data || !p.data.name) return ''
        const name = p.data.name
        const info = nodes.find((n) => n.name === name)
        if (!info) return name
        return `<b>${name}</b><br/>类型: ${['电网', 'PCS', '电池舱', '变压器'][info.category || 0]}`
      }
    },
    series: [
      {
        type: 'graph',
        layout: 'none',
        roam: true,
        label: { show: true, fontSize: 10, color: '#fff' },
        edgeSymbol: ['none', 'none'],
        edgeSymbolSize: [6, 8],
        data: nodes,
        links: links,
        categories: [{ name: '电网' }, { name: 'PCS' }, { name: '电池舱' }, { name: '变压器' }],
        lineStyle: { opacity: 0.9, curveness: 0, width: 2 }
      }
    ]
  })
}

const renderSingleLineDiagram = () => {
  if (!singleLineDiagram.value) return

  if (singleLineChart) {
    try {
      singleLineChart.dispose()
    } catch (e) {
      // resize failed silently
    }
    singleLineChart = null
  }

  try {
    singleLineChart = echarts.init(singleLineDiagram.value)
  } catch (e) {
    console.error('初始化单线图echarts失败:', e)
    return
  }
  if (!singleLineChart) return

  const container = containers.value.find((c) => c.id === selectedContainer.value)
  const pcs = pcsList.value.find((p) => p.id === selectedPCS.value)

  if (!container || !pcs) {
    singleLineChart.setOption({
      title: {
        text: '请选择集装箱和PCS型号',
        left: 'center',
        top: 'center',
        textStyle: { color: 'var(--color-text-muted)', fontSize: 14 }
      }
    })
    return
  }

  const ctn = containerQty.value
  const pn = pcsQty.value
  if (ctn <= 0 || pn <= 0) {
    singleLineChart.setOption({
      title: {
        text: '请设置集装箱数量和PCS数量',
        left: 'center',
        top: 'center',
        textStyle: { color: 'var(--color-text-muted)', fontSize: 14 }
      }
    })
    return
  }

  const style = getComputedStyle(document.documentElement)
  const colors = {
    emerald: style.getPropertyValue('--color-success').trim(),
    amber: style.getPropertyValue('--color-warning').trim(),
    sky: style.getPropertyValue('--color-accent').trim(),
    teal: style.getPropertyValue('--color-accent-secondary').trim(),
    slate: style.getPropertyValue('--color-text-muted').trim(),
    text: style.getPropertyValue('--color-text').trim()
  }

  const maxItems = Math.max(ctn, pn, 4)
  const span = Math.min(880, maxItems * 110)
  const startX = (1000 - span) / 2

  const graphicElements = []

  graphicElements.push({
    type: 'rect',
    shape: { x: 450, y: 10, width: 100, height: 38 },
    style: { fill: colors.emerald, stroke: colors.emerald, lineWidth: 2, shadowBlur: 4, shadowColor: 'rgba(0,0,0,0.3)' }
  })
  graphicElements.push({
    type: 'text',
    style: { text: '电网 10kV', x: 500, y: 34, fill: '#fff', fontSize: 12, textAlign: 'center', fontWeight: 'bold' }
  })

  graphicElements.push({
    type: 'line',
    shape: { x1: 500, y1: 48, x2: 500, y2: 85 },
    style: { stroke: colors.amber, lineWidth: 3 }
  })

  graphicElements.push({
    type: 'circle',
    shape: { cx: 500, cy: 105, r: 20 },
    style: {
      fill: colors.amber,
      stroke: colors.amber,
      lineWidth: 2,
      shadowBlur: 4,
      shadowOffsetX: 2,
      shadowOffsetY: 2,
      shadowColor: 'rgba(0,0,0,0.25)'
    }
  })
  graphicElements.push({
    type: 'text',
    style: { text: 'T', x: 500, y: 110, fill: '#fff', fontSize: 14, textAlign: 'center', fontWeight: 'bold' }
  })

  graphicElements.push({
    type: 'line',
    shape: { x1: 500, y1: 125, x2: 500, y2: 165 },
    style: { stroke: colors.amber, lineWidth: 3 }
  })

  graphicElements.push({
    type: 'line',
    shape: { x1: startX, y1: 165, x2: startX + span, y2: 165 },
    style: { stroke: colors.amber, lineWidth: 3 }
  })
  graphicElements.push({
    type: 'text',
    style: {
      text: `AC母线 ${pcs.voltage}V`,
      x: 500,
      y: 155,
      fill: colors.amber,
      fontSize: 10,
      textAlign: 'center',
      fontWeight: 'bold'
    }
  })

  const pcsUnitWidth = Math.min(74, span / Math.max(pn, 1))
  const pcsPositions = []
  for (let i = 0; i < pn; i++) {
    const x = startX + (i * span) / Math.max(pn - 1, 1) + pcsUnitWidth / 2
    pcsPositions.push(x)

    graphicElements.push({
      type: 'line',
      shape: { x1: x, y1: 165, x2: x, y2: 205 },
      style: { stroke: colors.amber, lineWidth: 2 }
    })

    graphicElements.push({
      type: 'rect',
      shape: { x: x - pcsUnitWidth / 2 + 4, y: 205, width: pcsUnitWidth - 8, height: 44 },
      style: {
        fill: colors.sky,
        stroke: colors.sky,
        lineWidth: 2,
        shadowBlur: 4,
        shadowOffsetX: 2,
        shadowOffsetY: 2,
        shadowColor: 'rgba(0,0,0,0.2)'
      }
    })
    graphicElements.push({
      type: 'text',
      style: { text: `PCS${i + 1}\n${pcs.power}MW`, x: x, y: 230, fill: '#fff', fontSize: 9, textAlign: 'center' }
    })

    graphicElements.push({
      type: 'line',
      shape: { x1: x, y1: 249, x2: x, y2: 285 },
      style: { stroke: colors.slate, lineWidth: 2 }
    })
  }

  // DC侧 — 每个PCS独立连接其集装箱，无公共DC母线
  const containersPerPCSVal = Math.ceil(ctn / Math.max(pn, 1))
  const containerUnitWidth = Math.min(76, (span / Math.max(containersPerPCSVal, 1) / Math.max(pn, 1)) * 0.85)
  const containerHeight = 50
  const depth = 12
  const dcJunctionY = 285
  const dcBranchY = 300
  const containerTop = 335

  // 存放每个PCS组内的集装箱
  const groupContainers = new Array(pn).fill(null).map(() => [])
  for (let i = 0; i < ctn; i++) {
    const gi = Math.min(Math.floor(i / Math.max(containersPerPCSVal, 1)), pn - 1)
    groupContainers[gi].push(i)
  }

  // 为每个PCS画DC垂直线 → DC汇流点
  for (let i = 0; i < pn; i++) {
    const pcsX = pcsPositions[i]
    graphicElements.push({
      type: 'line',
      shape: { x1: pcsX, y1: 249, x2: pcsX, y2: dcJunctionY },
      style: { stroke: colors.slate, lineWidth: 2 }
    })
    graphicElements.push({
      type: 'circle',
      shape: { cx: pcsX, cy: dcJunctionY, r: 4 },
      style: { fill: colors.slate }
    })
    graphicElements.push({
      type: 'text',
      style: { text: 'DC', x: pcsX, y: dcJunctionY - 12, fill: colors.slate, fontSize: 8, textAlign: 'center' }
    })

    const group = groupContainers[i]
    if (group.length === 0) continue

    // 计算此组集装箱的水平范围
    const firstIdx = group[0]
    const lastIdx = group[group.length - 1]
    const containerInGroup0 = firstIdx % containersPerPCSVal
    const containerInGroup1 = lastIdx % containersPerPCSVal
    const groupCount = group.length
    const offset0 = (containerInGroup0 - (groupCount - 1) / 2) * (containerUnitWidth + 4)
    const offset1 = (containerInGroup1 - (groupCount - 1) / 2) * (containerUnitWidth + 4)
    const firstX = pcsX + offset0
    const lastX = pcsX + offset1
    const leftX = Math.min(firstX, lastX)
    const rightX = Math.max(firstX, lastX)

    if (groupCount === 1) {
      // 单集装箱：汇流点直接下垂到集装箱
      graphicElements.push({
        type: 'line',
        shape: { x1: pcsX, y1: dcJunctionY, x2: pcsX, y2: containerTop },
        style: { stroke: colors.slate, lineWidth: 2 }
      })
    } else {
      // 多集装箱：汇流点 → 水平短线 → 分支下到各集装箱
      graphicElements.push({
        type: 'line',
        shape: { x1: pcsX, y1: dcJunctionY, x2: pcsX, y2: dcBranchY },
        style: { stroke: colors.slate, lineWidth: 2 }
      })
      graphicElements.push({
        type: 'line',
        shape: { x1: leftX, y1: dcBranchY, x2: rightX, y2: dcBranchY },
        style: { stroke: colors.slate, lineWidth: 2 }
      })
      for (const ci of group) {
        const containerInGroup = ci % containersPerPCSVal
        const offset = (containerInGroup - (groupCount - 1) / 2) * (containerUnitWidth + 4)
        const cx = pcsX + offset
        graphicElements.push({
          type: 'line',
          shape: { x1: cx, y1: dcBranchY, x2: cx, y2: containerTop },
          style: { stroke: colors.slate, lineWidth: 2 }
        })
      }
    }
  }

  // 绘制集装箱3D图形
  for (let i = 0; i < ctn; i++) {
    const pcsGroupIdx = Math.min(Math.floor(i / Math.max(containersPerPCSVal, 1)), pn - 1)
    const pcsX = pcsPositions[pcsGroupIdx] || 500
    const containerInGroup = i % containersPerPCSVal
    const groupCount = groupContainers[pcsGroupIdx].length
    const offset = (containerInGroup - (groupCount - 1) / 2) * (containerUnitWidth + 4)
    const x = pcsX + offset
    const boxX = x - containerUnitWidth / 2 + 4
    const boxY = containerTop
    graphicElements.push({
      type: 'polygon',
      shape: {
        points: [
          [boxX + containerUnitWidth - 8, boxY],
          [boxX + containerUnitWidth - 8 + depth, boxY - depth],
          [boxX + containerUnitWidth - 8 + depth, boxY - depth + containerHeight],
          [boxX + containerUnitWidth - 8, boxY + containerHeight]
        ]
      },
      style: {
        fill: colors.teal,
        stroke: colors.teal,
        lineWidth: 1,
        opacity: 0.7
      }
    })

    // 3D集装箱 - 顶面（平行四边形）
    graphicElements.push({
      type: 'polygon',
      shape: {
        points: [
          [boxX, boxY],
          [boxX + depth, boxY - depth],
          [boxX + containerUnitWidth - 8 + depth, boxY - depth],
          [boxX + containerUnitWidth - 8, boxY]
        ]
      },
      style: {
        fill: colors.teal,
        stroke: colors.teal,
        lineWidth: 1,
        opacity: 0.85
      }
    })

    // 3D集装箱 - 正面（矩形）
    graphicElements.push({
      type: 'rect',
      shape: { x: boxX, y: boxY, width: containerUnitWidth - 8, height: containerHeight },
      style: {
        fill: colors.teal,
        stroke: style.getPropertyValue('--color-accent-secondary').trim() + '99',
        lineWidth: 2,
        shadowBlur: 6,
        shadowOffsetX: 3,
        shadowOffsetY: 3,
        shadowColor: 'rgba(0,0,0,0.3)'
      }
    })

    graphicElements.push({
      type: 'text',
      style: {
        text: `舱${i + 1}`,
        x: x,
        y: boxY + 20,
        fill: '#fff',
        fontSize: 10,
        textAlign: 'center',
        fontWeight: 'bold'
      }
    })
    graphicElements.push({
      type: 'text',
      style: { text: `${container.energy}MWh`, x: x, y: boxY + 36, fill: '#fff', fontSize: 9, textAlign: 'center' }
    })
  }

  singleLineChart.setOption({
    backgroundColor: 'transparent',
    graphic: { elements: graphicElements }
  })
}

const applyScheme = (scheme) => {
  selectedContainer.value = scheme.containerId
  containerQty.value = scheme.containerQty
  selectedPCS.value = scheme.pcsId
  calculatePCS()
}

const resetConfig = () => {
  selectedContainer.value = ''
  containerQty.value = 1
  selectedPCS.value = ''
  calculatePCS()
}

watch([selectedContainer, containerQty, selectedPCS], () => {
  calculatePCS()
})

const applyConfig = () => {
  const container = containers.value.find((c) => c.id === selectedContainer.value)
  const pcs = pcsList.value.find((p) => p.id === selectedPCS.value)

  if (!container || !pcs) {
    emit('error', '请先选择集装箱和PCS型号', 'warning')
    return
  }

  emit('applyConfig', {
    ratedEnergy: container.energy,
    initContainerQty: containerQty.value,
    initPcsQty: pcsQty.value,
    duration:
      totalEnergy.value > 0 && totalPower.value > 0
        ? totalEnergy.value / totalPower.value
        : container.energy / Math.max(container.power, 0.01),
    acEfficiency: (pcs.efficiency || 97) / 100
  })
}

onMounted(() => {
  loadLibraryData().then(() => {
    const p = props.params || {}
    if (p.ratedEnergy && p.initContainerQty) {
      targetEnergy.value = p.ratedEnergy * p.initContainerQty
    }
    if (p.ratedEnergy && p.initContainerQty && p.duration) {
      targetPower.value = (p.ratedEnergy * p.initContainerQty) / p.duration
    }
    if (p.initContainerQty) {
      containerQty.value = p.initContainerQty
    }
    autoCalcQty()
    calculatePCS()
  })
})

onUnmounted(() => {
  if (connectionChart) {
    connectionChart.dispose()
    connectionChart = null
  }
  if (singleLineChart) {
    singleLineChart.dispose()
    singleLineChart = null
  }
})
</script>

<style scoped>
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
