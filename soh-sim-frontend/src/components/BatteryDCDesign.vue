<template>
  <div class="battery-dc-design h-full overflow-auto p-4">
    <div class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
      <h3 class="text-sm font-bold mb-4 flex items-center gap-2" style="color: var(--color-accent-secondary);">
        <span class="w-2 h-2 rounded-full" style="background-color: var(--color-accent-secondary);"></span>
        直流侧设计（电池系统）
      </h3>

      <!-- 电池系统配置 -->
      <div class="grid grid-cols-2 gap-4 mb-4">
        <!-- 电芯选型 -->
        <div class="rounded-lg p-4" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <h4 class="text-xs mb-3 font-medium" style="color: var(--color-text-secondary);">电芯选型</h4>
          
          <div class="space-y-3">
            <div>
              <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">电芯类型</label>
              <select v-model="selectedCellId" @change="onCellChange" 
                class="w-full rounded px-2 py-1.5 text-xs"
                style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
                onfocus="this.style.borderColor='var(--color-accent-secondary)'; this.style.outline='none';"
                onblur="this.style.borderColor='var(--color-input-border)';">
                <option value="">-- 请选择电芯 --</option>
                <option v-for="c in products.cells" :key="c.id" :value="c.id">{{ c.mfr }} {{ c.model }} ({{ c.capacityAh }}Ah)</option>
              </select>
            </div>
            
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">额定容量 (Ah)</label>
                <input v-model.number="batteryConfig.cellCapacity" type="number"
                  class="w-full rounded px-2 py-1 text-xs"
                  style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
                  onfocus="this.style.borderColor='var(--color-accent-secondary)'; this.style.outline='none';"
                  onblur="this.style.borderColor='var(--color-input-border)';">
              </div>
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">额定电压 (V)</label>
                <input v-model.number="batteryConfig.cellVoltage" type="number"
                  class="w-full rounded px-2 py-1 text-xs"
                  style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
                  onfocus="this.style.borderColor='var(--color-accent-secondary)'; this.style.outline='none';"
                  onblur="this.style.borderColor='var(--color-input-border)';">
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">能量密度 (Wh/kg)</label>
                <input v-model.number="batteryConfig.energyDensity" type="number"
                  class="w-full rounded px-2 py-1 text-xs"
                  style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
                  onfocus="this.style.borderColor='var(--color-accent-secondary)'; this.style.outline='none';"
                  onblur="this.style.borderColor='var(--color-input-border)';">
              </div>
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">循环寿命 (次)</label>
                <input v-model.number="batteryConfig.cycleLife" type="number"
                  class="w-full rounded px-2 py-1 text-xs"
                  style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
                  onfocus="this.style.borderColor='var(--color-accent-secondary)'; this.style.outline='none';"
                  onblur="this.style.borderColor='var(--color-input-border)';">
              </div>
            </div>
          </div>
        </div>

        <!-- 电池簇配置 -->
        <div class="rounded-lg p-4" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <h4 class="text-xs mb-3 font-medium" style="color: var(--color-text-secondary);">电池簇配置</h4>
          
          <div class="space-y-3">
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">串联数量 (S)</label>
                <input v-model.number="batteryConfig.seriesCount" type="number"
                  class="w-full rounded px-2 py-1 text-xs"
                  style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
                  onfocus="this.style.borderColor='var(--color-accent-secondary)'; this.style.outline='none';"
                  onblur="this.style.borderColor='var(--color-input-border)';">
              </div>
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">并联数量 (P)</label>
                <input v-model.number="batteryConfig.parallelCount" type="number"
                  class="w-full rounded px-2 py-1 text-xs"
                  style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
                  onfocus="this.style.borderColor='var(--color-accent-secondary)'; this.style.outline='none';"
                  onblur="this.style.borderColor='var(--color-input-border)';">
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">簇电压 (V)</label>
                <input v-model.number="batteryConfig.stringVoltage" type="number" readonly
                  class="w-full rounded px-2 py-1 text-xs"
                  style="background-color: var(--color-card-dark); border: 1px solid var(--color-border); color: var(--color-accent-secondary);">
              </div>
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">簇容量 (Ah)</label>
                <input v-model.number="batteryConfig.stringCapacity" type="number" readonly
                  class="w-full rounded px-2 py-1 text-xs"
                  style="background-color: var(--color-card-dark); border: 1px solid var(--color-border); color: var(--color-accent-secondary);">
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">簇能量 (kWh)</label>
                <input v-model.number="batteryConfig.stringEnergy" type="number" readonly
                  class="w-full rounded px-2 py-1 text-xs"
                  style="background-color: var(--color-card-dark); border: 1px solid var(--color-border); color: var(--color-accent-secondary);">
              </div>
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">簇数量</label>
                <input v-model.number="batteryConfig.stringQty" type="number"
                  class="w-full rounded px-2 py-1 text-xs"
                  style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
                  onfocus="this.style.borderColor='var(--color-accent-secondary)'; this.style.outline='none';"
                  onblur="this.style.borderColor='var(--color-input-border)';">
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 集装箱配置 -->
      <div class="rounded-lg p-4 mb-4" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
        <h4 class="text-xs mb-3 font-medium" style="color: var(--color-text-secondary);">集装箱配置</h4>
        
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">集装箱规格</label>
            <select v-model="batteryConfig.containerSpec" 
              class="w-full rounded px-2 py-1 text-xs"
              style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
              onfocus="this.style.borderColor='var(--color-accent-secondary)'; this.style.outline='none';"
              onblur="this.style.borderColor='var(--color-input-border)';">
              <option value="20ft">20ft 标准集装箱</option>
              <option value="40ft">40ft 标准集装箱</option>
              <option value="20ft-H">20ft 高柜集装箱</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">集装箱内簇数</label>
            <input v-model.number="batteryConfig.clustersPerContainer" type="number"
              class="w-full rounded px-2 py-1 text-xs"
              style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
              onfocus="this.style.borderColor='var(--color-accent-secondary)'; this.style.outline='none';"
              onblur="this.style.borderColor='var(--color-input-border)';">
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">单个集装箱能量 (MWh)</label>
            <input v-model.number="batteryConfig.containerEnergy" type="number" step="0.1"
              class="w-full rounded px-2 py-1 text-xs"
              style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
              onfocus="this.style.borderColor='var(--color-accent-secondary)'; this.style.outline='none';"
              onblur="this.style.borderColor='var(--color-input-border)';">
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">集装箱数量</label>
            <input v-model.number="batteryConfig.containerQty" type="number"
              class="w-full rounded px-2 py-1 text-xs"
              style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
              onfocus="this.style.borderColor='var(--color-accent-secondary)'; this.style.outline='none';"
              onblur="this.style.borderColor='var(--color-input-border)';">
          </div>
        </div>
        
        <div class="grid grid-cols-4 gap-3 mt-3">
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">总直流能量 (MWh)</label>
            <input v-model.number="batteryConfig.totalDcEnergy" type="number" readonly
              class="w-full rounded px-2 py-1 text-xs"
              style="background-color: var(--color-card-dark); border: 1px solid var(--color-border); color: var(--color-accent-secondary);">
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">直流电压范围 (V)</label>
            <input v-model="batteryConfig.dcVoltageRange" type="text"
              class="w-full rounded px-2 py-1 text-xs"
              style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
              onfocus="this.style.borderColor='var(--color-accent-secondary)'; this.style.outline='none';"
              onblur="this.style.borderColor='var(--color-input-border)';">
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">最大直流电流 (A)</label>
            <input v-model.number="batteryConfig.maxDcCurrent" type="number"
              class="w-full rounded px-2 py-1 text-xs"
              style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
              onfocus="this.style.borderColor='var(--color-accent-secondary)'; this.style.outline='none';"
              onblur="this.style.borderColor='var(--color-input-border)';">
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">直流断路器 (A)</label>
            <input v-model.number="batteryConfig.dcBreaker" type="number"
              class="w-full rounded px-2 py-1 text-xs"
              style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
              onfocus="this.style.borderColor='var(--color-accent-secondary)'; this.style.outline='none';"
              onblur="this.style.borderColor='var(--color-input-border)';">
          </div>
        </div>
      </div>

      <!-- 运行参数 -->
      <div class="rounded-lg p-4 mb-4" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
        <h4 class="text-xs mb-3 font-medium" style="color: var(--color-text-secondary);">运行参数（从调研表获取）</h4>
        
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">运行温度 (°C)</label>
            <input v-model.number="batteryConfig.operatingTemp" type="number"
              class="w-full rounded px-2 py-1 text-xs"
              style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
              onfocus="this.style.borderColor='var(--color-accent-secondary)'; this.style.outline='none';"
              onblur="this.style.borderColor='var(--color-input-border)';">
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">DOD设置 (%)</label>
            <input v-model.number="batteryConfig.dodSet" type="number" min="0" max="100"
              class="w-full rounded px-2 py-1 text-xs"
              style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
              onfocus="this.style.borderColor='var(--color-accent-secondary)'; this.style.outline='none';"
              onblur="this.style.borderColor='var(--color-input-border)';">
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">设计循环次数/天</label>
            <input v-model.number="batteryConfig.cyclesPerDay" type="number"
              class="w-full rounded px-2 py-1 text-xs"
              style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
              onfocus="this.style.borderColor='var(--color-accent-secondary)'; this.style.outline='none';"
              onblur="this.style.borderColor='var(--color-input-border)';">
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">放电深度实际 (%)</label>
            <input v-model.number="batteryConfig.actualDod" type="number"
              class="w-full rounded px-2 py-1 text-xs"
              style="background-color: var(--color-card-dark); border: 1px solid var(--color-border); color: var(--color-accent-secondary);" readonly>
          </div>
        </div>
      </div>

      <!-- 计算结果 -->
      <div class="rounded-lg p-4" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
        <div class="flex items-center justify-between mb-3">
          <h4 class="text-xs font-medium" style="color: var(--color-text-secondary);">电池系统配置结果</h4>
          <button @click="calculateBatteryConfig" 
            class="text-xs px-3 py-1 rounded transition-colors"
            style="background-color: var(--color-accent-secondary); color: white;"
            onmouseover="this.style.opacity='0.9';"
            onmouseout="this.style.opacity='1';">
            计算配置
          </button>
        </div>
        
        <div class="grid grid-cols-6 gap-3">
          <div class="text-center rounded p-2" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
            <div class="text-lg font-bold" style="color: var(--color-accent-secondary);">{{ batteryConfig.totalDcEnergy.toFixed(1) }}</div>
            <div class="text-[10px]" style="color: var(--color-text-muted);">总直流能量 (MWh)</div>
          </div>
          <div class="text-center rounded p-2" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
            <div class="text-lg font-bold" style="color: var(--color-accent);">{{ batteryConfig.containerQty }}</div>
            <div class="text-[10px]" style="color: var(--color-text-muted);">集装箱数量</div>
          </div>
          <div class="text-center rounded p-2" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
            <div class="text-lg font-bold" style="color: var(--color-success);">{{ totalStrings }}</div>
            <div class="text-[10px]" style="color: var(--color-text-muted);">电池簇总数</div>
          </div>
          <div class="text-center rounded p-2" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
            <div class="text-lg font-bold" style="color: var(--color-warning);">{{ batteryConfig.dcVoltageRange }}</div>
            <div class="text-[10px]" style="color: var(--color-text-muted);">电压范围</div>
          </div>
          <div class="text-center rounded p-2" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
            <div class="text-lg font-bold" style="color: var(--color-danger);">{{ batteryConfig.maxDcCurrent }}</div>
            <div class="text-[10px]" style="color: var(--color-text-muted);">最大电流 (A)</div>
          </div>
          <div class="text-center rounded p-2" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
            <div class="text-lg font-bold" style="color: var(--color-accent);">{{ (batteryConfig.totalDcEnergy * 1000 / batteryConfig.containerEnergy).toFixed(0) }}</div>
            <div class="text-[10px]" style="color: var(--color-text-muted);">簇/集装箱</div>
          </div>
        </div>
        
        <div class="mt-4 flex justify-end gap-2">
          <button @click="resetBatteryConfig" 
            class="text-xs px-3 py-1.5 rounded transition-colors"
            style="background-color: var(--color-card); border: 1px solid var(--color-border); color: var(--color-text-secondary);"
            onmouseover="this.style.borderColor='var(--color-accent)';"
            onmouseout="this.style.borderColor='var(--color-border)';">
            重置
          </button>
          <button @click="applyBatteryConfig" 
            class="text-xs px-4 py-1.5 rounded font-bold transition-colors"
            style="background-color: var(--color-accent-secondary); color: white;"
            onmouseover="this.style.opacity='0.9';"
            onmouseout="this.style.opacity='1';">
            应用配置
          </button>
        </div>
      </div>
    </div>

    <!-- Toast -->
    <div v-if="toast.show" class="fixed bottom-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all"
      :style="toast.type === 'success' ? { backgroundColor: 'var(--color-success)', color: 'white' } : { backgroundColor: 'var(--color-danger)', color: 'white' }">
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, computed, onMounted } from 'vue'
import { useProducts } from '../composables/useProducts'

const emit = defineEmits(['apply-config', 'error'])

const products = useProducts()
const selectedCellId = ref('eve-lf280k')

// 根据电芯ID查找映射规则，自动带出 pack/cluster/container 配置
function getCellMapping(cellId) {
  const mappings = products.cellPackMappings?.value || []
  return mappings.find(m => m.cellId === cellId) || null
}

// 根据映射规则和选中的集装箱规格，自动填充所有配置
function applyCellMapping(mapping) {
  if (!mapping) return

  const pack = mapping.packConfig
  const cluster = mapping.clusterConfig

  // 电芯参数
  batteryConfig.cellType = mapping.cellId
  batteryConfig.cellCapacity = mapping.cellAh
  batteryConfig.cellVoltage = mapping.cellV
  const cell = products.getCellById(mapping.cellId)
  batteryConfig.energyDensity = cell ? Math.round((cell.energyWh || mapping.cellAh * mapping.cellV) / (parseFloat(cell.weight) || 5.4)) : 160
  batteryConfig.cycleLife = cell?.cycleLife || 6000

  // Pack 参数
  batteryConfig.seriesPerPack = pack.seriesPerPack
  batteryConfig.parallelPerPack = pack.parallelPerPack

  // 簇参数
  batteryConfig.seriesCount = pack.seriesPerPack * (pack.packsPerCluster || 1)
  batteryConfig.parallelCount = pack.parallelPerPack
  batteryConfig.stringVoltage = cluster.clusterVoltage
  batteryConfig.stringCapacity = cluster.clusterCapacityAh
  batteryConfig.stringEnergy = cluster.clusterEnergyKWh

  // 集装箱：默认选第一个 containerConfig
  const containerCfg = mapping.containerConfigs?.[0]
  if (containerCfg) {
    batteryConfig.containerSpec = containerCfg.containerType === '20ft-H' ? '20ft-H' : containerCfg.containerType === '20ft' ? '20ft' : '20ft'
    batteryConfig.clustersPerContainer = containerCfg.clustersPerContainer
    batteryConfig.containerEnergy = containerCfg.containerEnergyMWh
    // 根据映射的集装箱能量和当前集装箱数量计算总能量
    batteryConfig.totalDcEnergy = batteryConfig.containerQty * containerCfg.containerEnergyMWh

    // 自动匹配兼容的集装箱产品
    if (containerCfg.compatibleContainerIds?.length > 0) {
      batteryConfig.matchedContainerId = containerCfg.compatibleContainerIds[0]
    } else {
      batteryConfig.matchedContainerId = ''
    }
  }

  // 计算电压范围
  const minV = batteryConfig.seriesCount * 3.0
  const maxV = batteryConfig.seriesCount * 3.65
  batteryConfig.dcVoltageRange = `${minV.toFixed(0)}-${maxV.toFixed(0)}V`

  showToast(`已自动配置: ${mapping.cellAh}Ah × ${batteryConfig.seriesCount}S = ${batteryConfig.stringVoltage}V / ${batteryConfig.stringEnergy.toFixed(1)}kWh/簇`)
}

function onCellChange() {
  const cell = products.getCellById(selectedCellId.value)
  if (!cell) return

  // 优先从映射表自动配置
  const mapping = getCellMapping(selectedCellId.value)
  if (mapping) {
    applyCellMapping(mapping)
  } else {
    // 回退：手动填入基础参数
    batteryConfig.cellType = cell.id
    batteryConfig.cellCapacity = cell.capacityAh || 280
    batteryConfig.cellVoltage = cell.voltageNominal || 3.2
    batteryConfig.energyDensity = Math.round((cell.energyWh || 896) / (parseFloat(cell.weight) || 5.4))
    batteryConfig.cycleLife = cell.cycleLife || 6000
  }
}

onMounted(() => {
  products.loadAll().then(() => {
    if (products.cells.value.length > 0 && !selectedCellId.value) {
      selectedCellId.value = products.cells.value[0].id
      onCellChange()
    } else if (selectedCellId.value) {
      onCellChange()
    }
  })
})

// Toast
const toast = reactive({ show: false, message: '', type: 'success' })
const showToast = (message, type = 'success') => {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => { toast.show = false }, 3000)
}

// 电池配置
const batteryConfig = reactive({
  // 电芯
  cellType: 'LFP280',
  cellCapacity: 280,
  cellVoltage: 3.2,
  energyDensity: 160,
  cycleLife: 6000,

  // Pack
  seriesPerPack: 52,
  parallelPerPack: 1,

  // 电池簇
  seriesCount: 240,
  parallelCount: 1,
  stringVoltage: 768,
  stringCapacity: 280,
  stringEnergy: 215,
  stringQty: 24,

  // 集装箱
  containerSpec: '20ft-H',
  clustersPerContainer: 4,
  containerEnergy: 5,
  containerQty: 10,
  matchedContainerId: '',

  // 总计
  totalDcEnergy: 50,
  dcVoltageRange: '672-864V',
  maxDcCurrent: 1500,
  dcBreaker: 2000,

  // 运行参数
  operatingTemp: 25,
  dodSet: 90,
  cyclesPerDay: 1,
  actualDod: 90,
})

// 计算簇参数
watch(() => [batteryConfig.seriesCount, batteryConfig.parallelCount, batteryConfig.cellVoltage, batteryConfig.cellCapacity], () => {
  batteryConfig.stringVoltage = batteryConfig.seriesCount * batteryConfig.cellVoltage
  batteryConfig.stringCapacity = batteryConfig.parallelCount * batteryConfig.cellCapacity
  batteryConfig.stringEnergy = (batteryConfig.stringVoltage * batteryConfig.stringCapacity) / 1000
})

// 计算总直流能量
watch(() => [batteryConfig.containerQty, batteryConfig.containerEnergy], () => {
  batteryConfig.totalDcEnergy = batteryConfig.containerQty * batteryConfig.containerEnergy
})

// 计算电池簇总数
const totalStrings = computed(() => {
  return Math.ceil(batteryConfig.containerQty * batteryConfig.clustersPerContainer)
})

// 计算配置
function calculateBatteryConfig() {
  // 验证输入
  if (batteryConfig.containerEnergy <= 0 || batteryConfig.containerQty <= 0) {
    showToast('请检查集装箱配置', 'error')
    return
  }
  
  // 计算簇数量（根据集装箱能量和簇能量）
  const clustersNeeded = Math.ceil((batteryConfig.containerEnergy * 1000) / batteryConfig.stringEnergy)
  batteryConfig.clustersPerContainer = clustersNeeded
  
  // 计算总簇数
  const total = batteryConfig.containerQty * clustersNeeded
  batteryConfig.stringQty = total
  
  // 计算电压范围 (假设单体3.2V, 240串)
  const minVoltage = 240 * 3.0  // SOC低时
  const maxVoltage = 240 * 3.65 // SOC高时
  batteryConfig.dcVoltageRange = `${minVoltage.toFixed(0)}-${maxVoltage.toFixed(0)}V`
  
  // 计算最大直流电流 (假设0.5C放电)
  const maxDischargeCurrent = (batteryConfig.containerEnergy * 1000) / (batteryConfig.dcVoltageRange.split('-')[0] / 2) * 0.5
  batteryConfig.maxDcCurrent = Math.round(maxDischargeCurrent)
  
  // DC断路器选择 (1.2倍过载)
  batteryConfig.dcBreaker = Math.ceil(maxDischargeCurrent * 1.2 / 100) * 100
  
  // 实际DOD
  batteryConfig.actualDod = Math.min(batteryConfig.dodSet, 95)
  
  showToast('电池配置计算完成')
}

// 重置
function resetBatteryConfig() {
  Object.assign(batteryConfig, {
    cellType: 'LFP280',
    cellCapacity: 280,
    cellVoltage: 3.2,
    seriesCount: 240,
    parallelCount: 1,
    clustersPerContainer: 4,
    containerEnergy: 5,
    containerQty: 10,
    totalDcEnergy: 50,
    dodSet: 90,
    cyclesPerDay: 1,
    actualDod: 90,
  })
  showToast('配置已重置')
}

// 应用配置
function applyBatteryConfig() {
  emit('apply-config', {
    ratedEnergy: batteryConfig.containerEnergy,
    containerQty: batteryConfig.containerQty,
    dod: batteryConfig.actualDod,
    cyclesPerDay: batteryConfig.cyclesPerDay,
    temperature: batteryConfig.operatingTemp,
  })
  showToast('电池配置已应用')
}

// 从调研表加载数据
function loadFromSurvey(surveyData) {
  if (surveyData.totalMwh) batteryConfig.containerEnergy = surveyData.totalMwh / surveyData.containerQty || 5
  if (surveyData.tempAvg) batteryConfig.operatingTemp = surveyData.tempAvg
  if (surveyData.cyclesPerDay) batteryConfig.cyclesPerDay = surveyData.cyclesPerDay
  if (surveyData.dod) batteryConfig.dodSet = surveyData.dod * 100
}

// 导出方法
defineExpose({ loadFromSurvey })
</script>

<style scoped>
.battery-dc-design {
  height: 100%;
}
</style>