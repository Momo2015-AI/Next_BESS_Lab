<template>
  <div class="hierarchy-builder space-y-4">
    <!-- ===== 左：RFP 需求输入 → DC 容量推导 ===== -->
    <div class="card p-4">
      <h3 class="section-title mb-3">{{ $t('hierarchy.dcSizing') }}</h3>
      <p class="text-xs text-muted mb-3">{{ $t('hierarchy.dcSizingDesc') }}</p>

      <div class="grid grid-cols-2 gap-4 mb-4">
        <div>
          <label class="label-text">{{ $t('hierarchy.targetPower') }} (MW)</label>
          <input v-model.number="h.targetPowerMW" type="number" step="1" class="form-field-input" />
        </div>
        <div>
          <label class="label-text">{{ $t('hierarchy.targetEnergy') }} (MWh)</label>
          <input v-model.number="h.targetEnergyMWh" type="number" step="1" class="form-field-input" />
        </div>
        <div>
          <label class="label-text">{{ $t('hierarchy.pRate') }}</label>
          <input v-model.number="h.pRate" type="number" step="0.001" class="form-field-input" />
        </div>
        <div>
          <label class="label-text">{{ $t('hierarchy.dodPercent') }} (%)</label>
          <input v-model.number="h.dodPercent" type="number" step="1" class="form-field-input" />
        </div>
        <div>
          <label class="label-text">{{ $t('hierarchy.voltageMismatchLoss') }} (%)</label>
          <input v-model.number="h.voltageMismatchLoss" type="number" step="0.1" class="form-field-input" />
        </div>
        <div>
          <label class="label-text">{{ $t('hierarchy.oemDesignMargin') }} (%)</label>
          <input v-model.number="h.oemDesignMargin" type="number" step="0.1" class="form-field-input" />
        </div>
        <div>
          <label class="label-text">{{ $t('hierarchy.sohInitial') }} (%)</label>
          <input v-model.number="h.sohInitial" type="number" step="0.1" class="form-field-input" />
        </div>
      </div>

      <!-- 推导结果 -->
      <div class="dc-result-panel">
        <div class="grid grid-cols-4 gap-3">
          <div class="metric-card">
            <div class="metric-value">{{ dcSizing.deltaPercent.toFixed(2) }}%</div>
            <div class="metric-label">Δ% ({{ $t('hierarchy.deltaPercent') }})</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ dcSizing.dcFunctionalMWh.toFixed(1) }}</div>
            <div class="metric-label">{{ $t('hierarchy.dcFunctional') }} (MWh)</div>
          </div>
          <div class="metric-card">
            <div class="metric-value accent">{{ dcSizing.dcInstalledMWh.toFixed(1) }}</div>
            <div class="metric-label">{{ $t('hierarchy.dcInstalled') }} (MWh)</div>
          </div>
          <div class="metric-card">
            <div class="metric-value accent">{{ dcSizing.requiredContainers }}</div>
            <div class="metric-label">{{ $t('hierarchy.requiredContainers') }}</div>
          </div>
        </div>
        <div class="formula-hint">
          <code>DC_Installed = DC_Functional / ((1 - Δ%) × SOH_initial)</code>
          <br />
          <code>Δ% = (100 - DoD%) + voltage_mismatch + oem_margin</code>
        </div>
      </div>
    </div>

    <!-- ===== 右：层级链自动推导 ===== -->
    <div class="card p-4">
      <h3 class="section-title mb-3">{{ $t('hierarchy.chainBuilder') }}</h3>

      <!-- 电芯选择 -->
      <div class="mb-4">
        <label class="label-text">{{ $t('hierarchy.selectCell') }}</label>
        <select v-model="selectedCellId" class="form-field-select max-w-sm" @change="onCellChange">
          <option value="">{{ $t('hierarchy.selectCellPlaceholder') }}</option>
          <option v-for="c in cells" :key="c.id" :value="c.id">
            {{ c.mfr }} {{ c.model }} ({{ c.capacityAh }}Ah, {{ c.voltageNominal }}V)
          </option>
        </select>
      </div>

      <!-- 层级链展示 -->
      <div v-if="selectedCellId && mapping" class="hierarchy-chain">
        <!-- Cell -->
        <div class="chain-level">
          <div class="chain-badge cell-badge">🔋 {{ $t('hierarchy.levelCell') }}</div>
          <div class="chain-detail">
            {{ selectedCell?.mfr }} {{ selectedCell?.model }} | {{ selectedCell?.capacityAh }}Ah |
            {{ selectedCell?.voltageNominal }}V
          </div>
        </div>
        <div class="chain-arrow">
          ↓ {{ mapping.packConfig.seriesPerPack }}S{{ mapping.packConfig.parallelPerPack }}P
        </div>

        <!-- Pack -->
        <div class="chain-level">
          <div class="chain-badge pack-badge">📦 {{ $t('hierarchy.levelPack') }}</div>
          <div class="chain-detail">
            <div class="grid grid-cols-3 gap-2">
              <div>
                <span class="text-muted">{{ $t('hierarchy.seriesPerPack') }}:</span>
                {{ mapping.packConfig.seriesPerPack }}
              </div>
              <div>
                <span class="text-muted">{{ $t('hierarchy.parallelPerPack') }}:</span>
                {{ mapping.packConfig.parallelPerPack }}
              </div>
              <div>
                <span class="text-muted">{{ $t('hierarchy.packVoltage') }}:</span>
                {{ packVoltage.toFixed(1) }}V
              </div>
              <div class="col-span-2">
                <span class="text-muted">{{ $t('hierarchy.packEnergy') }}:</span>
                {{ packEnergykWh.toFixed(2) }} kWh
              </div>
            </div>
          </div>
        </div>
        <div class="chain-arrow">↓ {{ h.packsPerRack }} {{ $t('hierarchy.packsPerRack') }}</div>

        <!-- Rack -->
        <div class="chain-level">
          <div class="chain-badge rack-badge">🗄️ {{ $t('hierarchy.levelRack') }}</div>
          <div class="chain-detail">
            <div class="grid grid-cols-3 gap-2">
              <div>
                <span class="text-muted">{{ $t('hierarchy.packsPerRack') }}:</span>
                <input
                  v-model.number="h.packsPerRack"
                  type="number"
                  min="1"
                  max="20"
                  class="chain-input"
                  @input="recalcChain"
                />
              </div>
              <div>
                <span class="text-muted">{{ $t('hierarchy.rackVoltage') }}:</span>
                {{ rackVoltage.toFixed(1) }}V
              </div>
              <div>
                <span class="text-muted">{{ $t('hierarchy.rackEnergy') }}:</span>
                {{ rackEnergykWh.toFixed(2) }} kWh
              </div>
            </div>
          </div>
        </div>
        <div class="chain-arrow">↓ {{ h.racksPerCluster }} {{ $t('hierarchy.racksPerCluster') }}</div>

        <!-- Cluster -->
        <div class="chain-level">
          <div class="chain-badge cluster-badge">⚡ {{ $t('hierarchy.levelCluster') }}</div>
          <div class="chain-detail">
            <div class="grid grid-cols-3 gap-2">
              <div>
                <span class="text-muted">{{ $t('hierarchy.clusterVoltage') }}:</span>
                {{ clusterVoltage.toFixed(1) }}V
              </div>
              <div>
                <span class="text-muted">{{ $t('hierarchy.clusterEnergy') }}:</span>
                {{ clusterEnergykWh.toFixed(2) }} kWh
              </div>
              <div>
                <span class="text-muted">{{ $t('hierarchy.racksPerCluster') }}:</span>
                {{ h.racksPerCluster }}
              </div>
            </div>
          </div>
        </div>
        <div class="chain-arrow">↓ {{ h.clustersPerContainer }} {{ $t('hierarchy.clustersPerContainer') }}</div>

        <!-- Container -->
        <div class="chain-level">
          <div class="chain-badge container-badge">📐 {{ $t('hierarchy.levelContainer') }}</div>
          <div class="chain-detail">
            <div class="grid grid-cols-3 gap-2">
              <div>
                <span class="text-muted">{{ $t('hierarchy.containerEnergy') }}:</span>
                {{ containerEnergyMWh.toFixed(3) }} MWh
              </div>
              <div>
                <span class="text-muted">{{ $t('hierarchy.clustersPerContainer') }}:</span>
                <input
                  v-model.number="h.clustersPerContainer"
                  type="number"
                  min="1"
                  max="20"
                  class="chain-input"
                  @input="recalcChain"
                />
              </div>
            </div>
            <!-- 兼容容器匹配 -->
            <div v-if="matchedContainers.length" class="mt-1 text-xs">
              <span class="text-success">{{ $t('hierarchy.matchedContainers') }}:</span>
              <span v-for="c in matchedContainers" :key="c.id" class="badge badge-sm">{{ c.mfr }} {{ c.model }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 容器数量验证 -->
      <div
        v-if="selectedCellId && mapping"
        class="mt-4 p-3 rounded"
        :class="containerValidation.valid ? 'bg-success/10' : 'bg-danger/10'"
      >
        <div class="flex items-center gap-2">
          <span :class="containerValidation.valid ? 'text-success' : 'text-danger'">
            {{ containerValidation.valid ? '✓' : '✗' }}
          </span>
          <span class="text-sm">
            {{ $t('hierarchy.containerValidation') }}: {{ dcSizing.requiredContainers }}
            {{ $t('hierarchy.containersNeeded') }} ({{ dcSizing.dcInstalledMWh.toFixed(1) }} MWh ÷
            {{ containerEnergyMWh.toFixed(3) }} MWh)
            {{ containerValidation.valid ? '≥ ' + dcSizing.requiredContainers : '< ' + dcSizing.requiredContainers }}
          </span>
        </div>
        <div v-if="containerValidation.valid" class="text-xs text-muted mt-1">
          {{ $t('hierarchy.totalInstalled') }}: {{ (dcSizing.requiredContainers * containerEnergyMWh).toFixed(1) }} MWh
          ({{ $t('hierarchy.oversizeRate') }}: {{ oversizeRate.toFixed(1) }}%)
        </div>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="flex gap-3">
      <button class="btn-primary" :disabled="!selectedCellId" @click="applyToDesign">
        {{ $t('hierarchy.applyToDesign') }}
      </button>
      <button class="btn-secondary" @click="resetAll">
        {{ $t('hierarchy.reset') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, reactive } from 'vue'
import { useBessStore } from '../stores/bess.js'
import { useProducts } from '../composables/useProducts.js'
import localProducts from '../data/products.json'

const store = useBessStore()
const { cells } = useProducts()

const h = reactive({ ...store.batteryHierarchy })
const selectedCellId = ref('')

// 选中的电芯
const selectedCell = computed(() => {
  const allCells = cells.value.length ? cells.value : localProducts.cells
  return allCells.find((c) => c.id === selectedCellId.value) || null
})

// 查找 cellPackMappings
const mapping = computed(() => {
  if (!selectedCellId.value) return null
  return localProducts.cellPackMappings.find((m) => m.cellId === selectedCellId.value) || null
})

// Pack 计算
const packVoltage = computed(() => {
  if (!mapping.value) return 0
  return mapping.value.packConfig.seriesPerPack * (selectedCell.value?.voltageNominal || 3.2)
})

const packEnergykWh = computed(() => {
  if (!mapping.value) return 0
  return (packVoltage.value * mapping.value.cellAh * mapping.value.packConfig.parallelPerPack) / 1000
})

// Rack 计算
const rackVoltage = computed(() => packVoltage.value * h.packsPerRack)

const rackEnergykWh = computed(() => packEnergykWh.value * h.packsPerRack)

// Cluster 计算
const clusterVoltage = computed(() => rackVoltage.value * h.racksPerCluster)

const clusterEnergykWh = computed(() => rackEnergykWh.value * h.racksPerCluster)

// Container 计算
const containerEnergyMWh = computed(() => (clusterEnergykWh.value * h.clustersPerContainer) / 1000)

// 匹配兼容容器
const matchedContainers = computed(() => {
  if (!mapping.value) return []
  const allContainers = localProducts.containers || []
  // 查找当前 mapping 中 containerConfigs 里 compatibleContainerIds
  for (const cc of mapping.value.containerConfigs) {
    if (cc.clustersPerContainer === h.clustersPerContainer) {
      return allContainers.filter((c) => cc.compatibleContainerIds.includes(c.id))
    }
  }
  return []
})

// DC 容量推导 (DEWA §6.2)
const dcSizing = computed(() => {
  const dodLoss = 100 - h.dodPercent
  const deltaPercent = dodLoss + h.voltageMismatchLoss + h.oemDesignMargin
  const dcFunctionalMWh = h.targetEnergyMWh
  const dcInstalledMWh = dcFunctionalMWh / ((1 - deltaPercent / 100) * (h.sohInitial / 100))
  const requiredContainers = Math.ceil(dcInstalledMWh / (containerEnergyMWh.value || 5.0))

  return {
    deltaPercent,
    dcFunctionalMWh,
    dcInstalledMWh,
    requiredContainers
  }
})

// 容器数量验证
const containerValidation = computed(() => {
  return {
    valid: dcSizing.value.requiredContainers * containerEnergyMWh.value >= dcSizing.value.dcInstalledMWh
  }
})

const oversizeRate = computed(() => {
  if (!dcSizing.value.dcInstalledMWh) return 0
  return (
    ((dcSizing.value.requiredContainers * containerEnergyMWh.value - dcSizing.value.dcInstalledMWh) /
      dcSizing.value.dcInstalledMWh) *
    100
  )
})

// 双向同步 reactive → store
watch(
  h,
  (val) => {
    Object.assign(store.batteryHierarchy, val)
  },
  { deep: true }
)

// 电芯变更 → 自动填充层级参数
function onCellChange() {
  if (!mapping.value) return
  h.cellModel = selectedCell.value?.model || ''
  h.cellVoltage = selectedCell.value?.voltageNominal || 3.2
  h.cellCapacityAh = selectedCell.value?.capacityAh || 280
  h.seriesPerPack = mapping.value.packConfig.seriesPerPack
  h.parallelPerPack = mapping.value.packConfig.parallelPerPack

  // 尝试从 containerConfigs 匹配 clustersPerContainer
  if (mapping.value.containerConfigs.length > 0) {
    const cfg = mapping.value.containerConfigs[0]
    h.clustersPerContainer = cfg.clustersPerContainer
    h.containerEnergyMWh = cfg.containerEnergyMWh
  }
  recalcChain()
}

function recalcChain() {
  // 更新 store
  Object.assign(store.batteryHierarchy, {
    packVoltage: packVoltage.value,
    packEnergykWh: packEnergykWh.value,
    rackVoltage: rackVoltage.value,
    rackEnergykWh: rackEnergykWh.value,
    clusterVoltage: clusterVoltage.value,
    clusterEnergykWh: clusterEnergykWh.value,
    containerEnergyMWh: containerEnergyMWh.value,
    deltaPercent: dcSizing.value.deltaPercent,
    dcFunctionalMWh: dcSizing.value.dcFunctionalMWh,
    dcInstalledMWh: dcSizing.value.dcInstalledMWh,
    requiredContainers: dcSizing.value.requiredContainers,
    source: 'hierarchy'
  })
}

function applyToDesign() {
  recalcChain()
  store.batteryHierarchy.source = 'hierarchy'
  // 同步到 systemParams
  store.systemParams.ratedEnergy = containerEnergyMWh.value
  store.systemParams.initContainerQty = dcSizing.value.requiredContainers
  store.systemParams.requiredEnergy = h.targetEnergyMWh
  store.systemParams.duration = 1 / h.pRate
}

function resetAll() {
  selectedCellId.value = ''
  Object.assign(h, {
    cellModel: '',
    packModel: '',
    rackModel: '',
    clusterModel: '',
    containerModel: '',
    cellVoltage: 3.2,
    cellCapacityAh: 280,
    seriesPerPack: 52,
    parallelPerPack: 1,
    packVoltage: 0,
    packEnergykWh: 0,
    packsPerRack: 8,
    rackVoltage: 0,
    rackEnergykWh: 0,
    racksPerCluster: 1,
    clusterVoltage: 0,
    clusterEnergykWh: 0,
    clustersPerContainer: 12,
    containerEnergyMWh: 5.0,
    targetPowerMW: 260,
    targetEnergyMWh: 1560,
    pRate: 0.167,
    dodPercent: 90,
    voltageMismatchLoss: 1,
    oemDesignMargin: 3,
    sohInitial: 100,
    deltaPercent: 0,
    dcFunctionalMWh: 0,
    dcInstalledMWh: 0,
    requiredContainers: 0,
    source: 'manual'
  })
}
</script>

<style scoped>
.hierarchy-builder {
  max-width: 100%;
}

.dc-result-panel {
  background: var(--color-bg-muted, rgba(0, 0, 0, 0.03));
  border-radius: var(--radius-md);
  padding: 16px;
  margin-top: 12px;
}

.formula-hint {
  margin-top: 10px;
  padding: 8px 12px;
  background: var(--color-accent-glow, rgba(0, 102, 204, 0.06));
  border-radius: 6px;
  font-size: 0.75rem;
  color: var(--color-text-muted);
  line-height: 1.6;
}
.formula-hint code {
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 0.7rem;
  color: var(--color-accent);
}

.hierarchy-chain {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.chain-level {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px solid var(--color-border);
  background: var(--color-card);
}

.chain-badge {
  font-size: 0.75rem;
  font-weight: 700;
  white-space: nowrap;
  min-width: 80px;
  padding: 4px 8px;
  border-radius: 4px;
  text-align: center;
}

.cell-badge {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}
.pack-badge {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}
.rack-badge {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}
.cluster-badge {
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
}
.container-badge {
  background: rgba(236, 72, 153, 0.1);
  color: #ec4899;
}

.chain-detail {
  flex: 1;
  font-size: 0.8125rem;
  color: var(--color-text);
}

.chain-arrow {
  text-align: center;
  font-size: 0.75rem;
  color: var(--color-text-muted);
  padding: 2px 0;
}

.chain-input {
  width: 48px;
  padding: 2px 4px;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  font-size: 0.75rem;
  text-align: center;
  background: var(--color-card);
  color: var(--color-text);
}

.accent {
  color: var(--color-accent);
}

.badge-sm {
  display: inline-block;
  padding: 1px 6px;
  border-radius: 3px;
  font-size: 0.65rem;
  margin-left: 4px;
  background: var(--color-success-glow, rgba(5, 150, 105, 0.1));
  color: var(--color-success);
}

.bg-success\\/10 {
  background: rgba(5, 150, 105, 0.08);
}
.bg-danger\\/10 {
  background: rgba(220, 38, 38, 0.08);
}
.text-success {
  color: var(--color-success);
}
.text-danger {
  color: var(--color-danger);
}
</style>
