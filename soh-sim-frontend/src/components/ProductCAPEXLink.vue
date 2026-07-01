<template>
  <div class="rounded-lg p-3" style="background-color: var(--color-card); border: 1px solid var(--color-border)">
    <h3 class="font-bold text-xs mb-2 flex items-center gap-2" style="color: var(--color-text)">
      <span
        class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold"
        style="background-color: rgba(245, 158, 11, 0.2); color: var(--color-warning)"
      >
        VII
      </span>
      产品库→CAPEX 自动联动 Product Library → CAPEX Auto-Link
    </h3>

    <div class="space-y-3 text-[10px]" style="color: var(--color-text-secondary)">
      <!-- 产品选择 -->
      <div class="grid grid-cols-3 gap-2">
        <div>
          <label class="block mb-0.5" style="color: var(--color-text-muted)">电芯 Cell</label>
          <select
            v-model="selectedCell"
            class="w-full rounded px-2 py-1 text-xs"
            style="
              background-color: var(--color-input-bg-dark);
              border: 1px solid var(--color-input-border);
              color: var(--color-text);
            "
            @change="updateCAPEX"
          >
            <option value="">选择电芯</option>
            <option v-for="cell in availableCells" :key="cell.id" :value="cell.id">
              {{ cell.mfr }} {{ cell.model }} ({{ cell.capacityAh }}Ah, ¥{{ cell.unitPrice }}/Ah)
            </option>
          </select>
        </div>
        <div>
          <label class="block mb-0.5" style="color: var(--color-text-muted)">集装箱 Container</label>
          <select
            v-model="selectedContainer"
            class="w-full rounded px-2 py-1 text-xs"
            style="
              background-color: var(--color-input-bg-dark);
              border: 1px solid var(--color-input-border);
              color: var(--color-text);
            "
            @change="updateCAPEX"
          >
            <option value="">选择集装箱</option>
            <option v-for="container in availableContainers" :key="container.id" :value="container.id">
              {{ container.mfr }} {{ container.model }} ({{ container.ratedEnergyMWh }}MWh, ¥{{
                container.unitPrice
              }}/MWh)
            </option>
          </select>
        </div>
        <div>
          <label class="block mb-0.5" style="color: var(--color-text-muted)">PCS 变流器</label>
          <select
            v-model="selectedPcs"
            class="w-full rounded px-2 py-1 text-xs"
            style="
              background-color: var(--color-input-bg-dark);
              border: 1px solid var(--color-input-border);
              color: var(--color-text);
            "
            @change="updateCAPEX"
          >
            <option value="">选择PCS</option>
            <option v-for="pcs in availablePcs" :key="pcs.id" :value="pcs.id">
              {{ pcs.mfr }} {{ pcs.model }} ({{ pcs.ratedPowerMW }}MW, ¥{{ pcs.unitPrice }}/MW)
            </option>
          </select>
        </div>
      </div>

      <!-- 配置摘要 -->
      <div
        v-if="hasSelection"
        class="border rounded p-2"
        style="border-color: var(--color-border); background-color: var(--color-card-dark)"
      >
        <h4 class="text-xs font-bold mb-2" style="color: var(--color-text-secondary)">
          当前配置 Current Configuration
        </h4>
        <div class="grid grid-cols-3 gap-2 text-xs">
          <div>
            <div style="color: var(--color-text-muted)">电芯</div>
            <div class="font-mono mt-0.5" style="color: var(--color-text)">
              {{ selectedCellInfo?.mfr }} {{ selectedCellInfo?.model }}
            </div>
            <div class="text-[9px]" style="color: var(--color-text-muted)">
              {{ selectedCellInfo?.capacityAh }}Ah @ ¥{{ selectedCellInfo?.unitPrice }}/Ah
            </div>
          </div>
          <div>
            <div style="color: var(--color-text-muted)">集装箱</div>
            <div class="font-mono mt-0.5" style="color: var(--color-text)">
              {{ selectedContainerInfo?.mfr }} {{ selectedContainerInfo?.model }}
            </div>
            <div class="text-[9px]" style="color: var(--color-text-muted)">
              {{ selectedContainerInfo?.ratedEnergyMWh }}MWh @ ¥{{ selectedContainerInfo?.unitPrice }}/MWh
            </div>
          </div>
          <div>
            <div style="color: var(--color-text-muted)">PCS</div>
            <div class="font-mono mt-0.5" style="color: var(--color-text)">
              {{ selectedPcsInfo?.mfr }} {{ selectedPcsInfo?.model }}
            </div>
            <div class="text-[9px]" style="color: var(--color-text-muted)">
              {{ selectedPcsInfo?.ratedPowerMW }}MW @ ¥{{ selectedPcsInfo?.unitPrice }}/MW
            </div>
          </div>
        </div>
      </div>

      <!-- CAPEX 计算 -->
      <div v-if="hasSelection" class="border-t pt-2">
        <h4 class="text-xs font-bold mb-2" style="color: var(--color-text-secondary)">
          CAPEX 成本计算 CAPEX Cost Calculation
        </h4>
        <div class="space-y-1 text-xs">
          <div class="flex justify-between">
            <span style="color: var(--color-text-muted)">电芯成本</span>
            <span class="font-mono" style="color: var(--color-text-secondary)">{{ formatCurrency(cellCost) }}</span>
          </div>
          <div class="flex justify-between">
            <span style="color: var(--color-text-muted)">集装箱成本</span>
            <span class="font-mono" style="color: var(--color-text-secondary)">
              {{ formatCurrency(containerCost) }}
            </span>
          </div>
          <div class="flex justify-between">
            <span style="color: var(--color-text-muted)">PCS成本</span>
            <span class="font-mono" style="color: var(--color-text-secondary)">{{ formatCurrency(pcsCost) }}</span>
          </div>
          <div class="flex justify-between">
            <span style="color: var(--color-text-muted)">BOP配套</span>
            <span class="font-mono" style="color: var(--color-text-secondary)">{{ formatCurrency(bopCost) }}</span>
          </div>
          <div class="border-t pt-1 mt-1 flex justify-between font-bold">
            <span style="color: var(--color-text)">总CAPEX</span>
            <span class="font-mono" style="color: var(--color-accent)">{{ formatCurrency(totalCAPEX) }}</span>
          </div>
          <div class="flex justify-between text-[9x]">
            <span style="color: var(--color-text-muted)">单价</span>
            <span style="color: var(--color-text-secondary)">{{ capexPerMWh.toFixed(0) }} 万元/MWh</span>
          </div>
        </div>
      </div>

      <!-- 应用到仿真 -->
      <div v-if="hasSelection" class="flex justify-end mt-3">
        <button
          class="text-xs px-4 py-1.5 rounded transition-colors"
          style="background-color: var(--color-accent-secondary); color: white"
          onmouseover="this.style.opacity = '0.9'"
          onmouseout="this.style.opacity = '1'"
          @click="applyToSimulation"
        >
          应用到仿真 Apply to Simulation
        </button>
      </div>

      <!-- 提示信息 -->
      <div v-if="!hasSelection" class="text-[9x] text-center py-2" style="color: var(--color-text-muted)">
        请选择产品以自动计算CAPEX
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useExchangeRate } from '../composables/useExchangeRate.js'

const props = defineProps({
  params: Object,
  onApplyConfig: Function
})

const emit = defineEmits(['applyConfig'])

// 使用汇率管理
const { displayCurrency, formatAmount } = useExchangeRate()

// 产品数据
const selectedCell = ref('')
const selectedContainer = ref('')
const selectedPcs = ref('')

const availableCells = ref([])
const availableContainers = ref([])
const availablePcs = ref([])

// 计算属性
const selectedCellInfo = computed(() => availableCells.value.find((c) => c.id === selectedCell.value))

const selectedContainerInfo = computed(() => availableContainers.value.find((c) => c.id === selectedContainer.value))

const selectedPcsInfo = computed(() => availablePcs.value.find((p) => p.id === selectedPcs.value))

const hasSelection = computed(() => selectedCell.value && selectedContainer.value && selectedPcs.value)

// CAPEX 计算
const cellCost = computed(() => {
  if (!selectedCellInfo.value) return 0
  // 假设每个集装箱需要一定数量的电芯
  const cellsPerContainer = (selectedContainerInfo.value?.ratedEnergyMWh * 1000) / selectedCellInfo.value.energyWh || 0
  return (
    selectedCellInfo.value.unitPrice *
    selectedCellInfo.value.capacityAh *
    cellsPerContainer *
    selectedContainerInfo.value.ratedEnergyMWh
  )
})

const containerCost = computed(() => {
  if (!selectedContainerInfo.value) return 0
  return selectedContainerInfo.value.unitPrice * selectedContainerInfo.value.ratedEnergyMWh
})

const pcsCost = computed(() => {
  if (!selectedPcsInfo.value) return 0
  return selectedPcsInfo.value.unitPrice * selectedPcsInfo.value.ratedPowerMW
})

const bopCost = computed(() => {
  if (!selectedContainerInfo.value) return 0
  // BOP成本按集装箱的30%估算
  return containerCost.value * 0.3
})

const totalCAPEX = computed(() => {
  return cellCost.value + containerCost.value + pcsCost.value + bopCost.value
})

const capexPerMWh = computed(() => {
  if (!selectedContainerInfo.value) return 0
  return totalCAPEX.value / selectedContainerInfo.value.ratedEnergyMWh
})

// 格式化货币
const formatCurrency = (amount) => {
  if (!amount || isNaN(amount)) return '¥0'
  return `¥${amount.toFixed(0)}`
}

// 加载产品数据
const loadProducts = async () => {
  try {
    // 尝试从API加载
    const [cellsRes, containersRes, pcsRes] = await Promise.all([
      fetch('/api/library/cells'),
      fetch('/api/library/containers'),
      fetch('/api/library/pcs')
    ])

    const [cellsData, containersData, pcsData] = await Promise.all([
      cellsRes.json(),
      containersRes.json(),
      pcsRes.json()
    ])

    if (cellsData.success) availableCells.value = cellsData.data || []
    if (containersData.success) availableContainers.value = containersData.data || []
    if (pcsData.success) availablePcs.value = pcsData.data || []

    // 如果API无数据，使用本地数据
    if (availableCells.value.length === 0) {
      const localData = await import('../data/products.json')
      availableCells.value = localData.cells.map((cell) => ({
        ...cell,
        unitPrice: cell.unitPrice || 0.8 // 默认价格
      }))
    }

    if (availableContainers.value.length === 0) {
      const localData = await import('../data/products.json')
      availableContainers.value = localData.containers.map((container) => ({
        ...container,
        unitPrice: container.unitPrice || 800 // 默认价格
      }))
    }

    if (availablePcs.value.length === 0) {
      const localData = await import('../data/products.json')
      availablePcs.value = localData.pcs.map((pcs) => ({
        ...pcs,
        unitPrice: pcs.unitPrice || 25 // 默认价格
      }))
    }
  } catch (error) {
    console.error('加载产品数据失败:', error)
    // 降级到本地数据
    const localData = await import('../data/products.json')
    availableCells.value = localData.cells.map((cell) => ({
      ...cell,
      unitPrice: cell.unitPrice || 0.8
    }))
    availableContainers.value = localData.containers.map((container) => ({
      ...container,
      unitPrice: container.unitPrice || 800
    }))
    availablePcs.value = localData.pcs.map((pcs) => ({
      ...pcs,
      unitPrice: pcs.unitPrice || 25
    }))
  }
}

// 更新CAPEX
const updateCAPEX = () => {
  // 这里可以触发重新计算或更新父组件
  console.log('CAPEX updated:', {
    cellCost: cellCost.value,
    containerCost: containerCost.value,
    pcsCost: pcsCost.value,
    bopCost: bopCost.value,
    totalCAPEX: totalCAPEX.value,
    capexPerMWh: capexPerMWh.value
  })
}

// 应用到仿真
const applyToSimulation = () => {
  if (!hasSelection.value) return

  const config = {
    selectedCell: selectedCellInfo.value,
    selectedContainer: selectedContainerInfo.value,
    selectedPcs: selectedPcsInfo.value,
    autoCalculatedCAPEX: totalCAPEX.value,
    autoCalculatedCapexPerMWh: capexPerMWh.value,
    ratedEnergy: selectedContainerInfo.value.ratedEnergyMWh,
    acEfficiency: selectedPcsInfo.value?.efficiency || 97.03
  }

  emit('applyConfig', config)
}

// 监听货币变化
watch(displayCurrency, () => {
  // 货币变化时重新计算
  updateCAPEX()
})

// 初始化
onMounted(() => {
  loadProducts()
})
</script>
