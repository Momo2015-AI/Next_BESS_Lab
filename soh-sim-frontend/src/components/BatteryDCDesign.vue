<template>
  <div class="battery-dc-design h-full overflow-auto p-4">
    <div class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border)">
      <h3 class="text-sm font-bold mb-4 flex items-center gap-2" style="color: var(--color-accent-secondary)">
        <span class="w-2 h-2 rounded-full" style="background-color: var(--color-accent-secondary)" />
        {{ $t('batteryDC.title') }}
      </h3>

      <!-- 电池系统配置 -->
      <div class="grid grid-cols-2 gap-4 mb-4">
        <!-- 电芯选型 -->
        <div
          class="rounded-lg p-4"
          style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
        >
          <h4 class="text-xs mb-3 font-medium" style="color: var(--color-text-secondary)">
            {{ $t('batteryDC.cellModel') }}
          </h4>

          <div class="space-y-3">
            <div>
              <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
                {{ $t('batteryDC.cellType') }}
              </label>
              <select
                v-model="selectedCellId"
                class="w-full rounded px-2 py-1.5 text-xs form-field-select"
                @change="onCellChange"
              >
                <option value="">{{ $t('batteryDC.selectCell') }}</option>
                <option v-for="c in cells" :key="c.id" :value="c.id">
                  {{ c.mfr }} - {{ c.model }} ({{ c.capacityAh }}Ah)
                </option>
              </select>
            </div>

            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
                  {{ $t('batteryDC.ratedCapacity') }}
                </label>
                <input
                  v-model.number="batteryConfig.cellCapacity"
                  type="number"
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
                  {{ $t('batteryDC.ratedVoltage') }}
                </label>
                <input
                  v-model.number="batteryConfig.cellVoltage"
                  type="number"
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
                  {{ $t('batteryDC.energyDensity') }}
                </label>
                <input
                  v-model.number="batteryConfig.energyDensity"
                  type="number"
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
                  {{ $t('batteryDC.cycleLife') }}
                </label>
                <input
                  v-model.number="batteryConfig.cycleLife"
                  type="number"
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- 电池簇配置 -->
        <div
          class="rounded-lg p-4"
          style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
        >
          <h4 class="text-xs mb-3 font-medium" style="color: var(--color-text-secondary)">
            {{ $t('batteryDC.clusterConfig') }}
          </h4>

          <div class="space-y-3">
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
                  {{ $t('batteryDC.seriesCount') }}
                </label>
                <input
                  v-model.number="batteryConfig.seriesCount"
                  type="number"
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
                  {{ $t('batteryDC.parallelCount') }}
                </label>
                <input
                  v-model.number="batteryConfig.parallelCount"
                  type="number"
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
                  {{ $t('batteryDC.clusterVoltage') }}
                </label>
                <input
                  v-model.number="batteryConfig.stringVoltage"
                  type="number"
                  readonly
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
                  {{ $t('batteryDC.clusterCapacity') }}
                </label>
                <input
                  v-model.number="batteryConfig.stringCapacity"
                  type="number"
                  readonly
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
                  {{ $t('batteryDC.clusterEnergy') }}
                </label>
                <input
                  v-model.number="batteryConfig.stringEnergy"
                  type="number"
                  readonly
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
                  {{ $t('batteryDC.clusterQty') }}
                </label>
                <input
                  v-model.number="batteryConfig.stringQty"
                  type="number"
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 集装箱配置 -->
      <div
        class="rounded-lg p-4 mb-4"
        style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
      >
        <h4 class="text-xs mb-3 font-medium" style="color: var(--color-text-secondary)">
          {{ $t('batteryDC.containerConfig') }}
        </h4>

        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
              {{ $t('batteryDC.containerSpec') }}
            </label>
            <select v-model="batteryConfig.containerSpec" class="w-full rounded px-2 py-1 text-xs form-field-select">
              <option value="20ft">{{ $t('batteryDC.container20ft') }}</option>
              <option value="40ft">{{ $t('batteryDC.container40ft') }}</option>
              <option value="20ft-H">{{ $t('batteryDC.container20ftH') }}</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
              {{ $t('batteryDC.clustersPerContainer') }}
            </label>
            <input
              v-model.number="batteryConfig.clustersPerContainer"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
              {{ $t('batteryDC.containerEnergy') }}
            </label>
            <input
              v-model.number="batteryConfig.containerEnergy"
              type="number"
              step="0.1"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
              {{ $t('batteryDC.containerQty') }}
            </label>
            <input
              v-model.number="batteryConfig.containerQty"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
        </div>

        <div class="grid grid-cols-4 gap-3 mt-3">
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
              {{ $t('batteryDC.totalDcEnergy') }}
            </label>
            <input
              v-model.number="batteryConfig.totalDcEnergy"
              type="number"
              readonly
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
              {{ $t('batteryDC.dcVoltageRange') }}
            </label>
            <input
              v-model="batteryConfig.dcVoltageRange"
              type="text"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
              {{ $t('batteryDC.maxDcCurrent') }}
            </label>
            <input
              v-model.number="batteryConfig.maxDcCurrent"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
              {{ $t('batteryDC.dcBreaker') }}
            </label>
            <input
              v-model.number="batteryConfig.dcBreaker"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
        </div>
      </div>

      <!-- 运行参数 -->
      <div
        class="rounded-lg p-4 mb-4"
        style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
      >
        <h4 class="text-xs mb-3 font-medium" style="color: var(--color-text-secondary)">
          {{ $t('batteryDC.operatingParams') }}
        </h4>

        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
              {{ $t('batteryDC.operatingTemp') }}
            </label>
            <input
              v-model.number="batteryConfig.operatingTemp"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
              {{ $t('batteryDC.dodSetting') }}
            </label>
            <input
              v-model.number="batteryConfig.dodSet"
              type="number"
              min="0"
              max="100"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
              {{ $t('batteryDC.cyclesPerDay') }}
            </label>
            <input
              v-model.number="batteryConfig.cyclesPerDay"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
              {{ $t('batteryDC.actualDod') }}
            </label>
            <input
              v-model.number="batteryConfig.actualDod"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
              readonly
            />
          </div>
        </div>
      </div>

      <!-- 计算结果 -->
      <div
        class="rounded-lg p-4"
        style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
      >
        <div class="flex items-center justify-between mb-3">
          <h4 class="text-xs font-medium" style="color: var(--color-text-secondary)">
            {{ $t('batteryDC.configResult') }}
          </h4>
          <button
            class="text-xs px-3 py-1 rounded transition-colors"
            style="background-color: var(--color-accent-secondary); color: white"
            @click="calculateBatteryConfig"
          >
            {{ $t('batteryDC.calculateConfig') }}
          </button>
        </div>

        <div class="grid grid-cols-6 gap-3">
          <div
            class="text-center rounded p-2"
            style="background-color: var(--color-card); border: 1px solid var(--color-border)"
          >
            <div class="text-lg font-bold" style="color: var(--color-accent-secondary)">
              {{ batteryConfig.totalDcEnergy.toFixed(1) }}
            </div>
            <div class="text-[10px]" style="color: var(--color-text-muted)">
              {{ $t('batteryDC.resultTotalDcEnergy') }}
            </div>
          </div>
          <div
            class="text-center rounded p-2"
            style="background-color: var(--color-card); border: 1px solid var(--color-border)"
          >
            <div class="text-lg font-bold" style="color: var(--color-accent)">
              {{ batteryConfig.containerQty }}
            </div>
            <div class="text-[10px]" style="color: var(--color-text-muted)">
              {{ $t('batteryDC.resultContainerQty') }}
            </div>
          </div>
          <div
            class="text-center rounded p-2"
            style="background-color: var(--color-card); border: 1px solid var(--color-border)"
          >
            <div class="text-lg font-bold" style="color: var(--color-success)">
              {{ totalStrings }}
            </div>
            <div class="text-[10px]" style="color: var(--color-text-muted)">
              {{ $t('batteryDC.resultTotalClusters') }}
            </div>
          </div>
          <div
            class="text-center rounded p-2"
            style="background-color: var(--color-card); border: 1px solid var(--color-border)"
          >
            <div class="text-lg font-bold" style="color: var(--color-warning)">
              {{ batteryConfig.dcVoltageRange }}
            </div>
            <div class="text-[10px]" style="color: var(--color-text-muted)">
              {{ $t('batteryDC.resultVoltageRange') }}
            </div>
          </div>
          <div
            class="text-center rounded p-2"
            style="background-color: var(--color-card); border: 1px solid var(--color-border)"
          >
            <div class="text-lg font-bold" style="color: var(--color-danger)">
              {{ batteryConfig.maxDcCurrent }}
            </div>
            <div class="text-[10px]" style="color: var(--color-text-muted)">{{ $t('batteryDC.resultMaxCurrent') }}</div>
          </div>
          <div
            class="text-center rounded p-2"
            style="background-color: var(--color-card); border: 1px solid var(--color-border)"
          >
            <div class="text-lg font-bold" style="color: var(--color-accent)">
              {{ batteryConfig.clustersPerContainer }}
            </div>
            <div class="text-[10px]" style="color: var(--color-text-muted)">
              {{ $t('batteryDC.resultClustersPerContainer') }}
            </div>
          </div>
        </div>

        <div class="mt-4 flex justify-end gap-2">
          <button
            class="text-xs px-3 py-1.5 rounded transition-colors"
            style="
              background-color: var(--color-card);
              border: 1px solid var(--color-border);
              color: var(--color-text-secondary);
            "
            @click="resetBatteryConfig"
          >
            {{ $t('common.reset') }}
          </button>
          <button
            class="text-xs px-4 py-1.5 rounded font-bold transition-colors"
            style="background-color: var(--color-accent-secondary); color: white"
            @click="applyBatteryConfig"
          >
            {{ $t('batteryDC.applyConfig') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Toast -->
    <div
      v-if="toast.show"
      class="fixed bottom-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all"
      :style="
        toast.type === 'success'
          ? { backgroundColor: 'var(--color-success)', color: 'white' }
          : { backgroundColor: 'var(--color-danger)', color: 'white' }
      "
    >
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useProducts } from '../composables/useProducts'
import { useDraft } from '../composables/useDraft'

const { t } = useI18n()

const emit = defineEmits(['apply-config', 'error'])

const { cells, containers, loadAll } = useProducts()

// 电芯库数据（从统一产品库获取）
const selectedCellId = ref('')

// 加载电芯库数据
async function loadCellLibrary() {
  await loadAll()
  // 如果有数据，默认选择第一个
  if (cells.value.length > 0 && !selectedCellId.value) {
    selectedCellId.value = cells.value[0].id
    onCellChange()
  }
}

// 获取选中的电芯
function getSelectedCell() {
  return cells.value.find((c) => c.id === selectedCellId.value)
}

// 电芯变化时自动带出参数
function onCellChange() {
  const cell = getSelectedCell()
  if (!cell) return

  // 填入基础参数
  batteryConfig.cellType = cell.id
  batteryConfig.cellCapacity = cell.capacityAh || 280
  batteryConfig.cellVoltage = cell.voltageNominal || 3.2
  batteryConfig.energyDensity =
    cell.energyDensity || Math.round(((cell.ratedEnergyMWh || 0.000896) * 1e6) / (parseFloat(cell.weight) || 5.4))
  batteryConfig.cycleLife = cell.cycleLife || 6000
}

onMounted(() => {
  loadCellLibrary()
})

// Toast
const toast = reactive({ show: false, message: '', type: 'success' })
const showToast = (message, type = 'success') => {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => {
    toast.show = false
  }, 3000)
}

// 电池配置
const { state: batteryConfig, clearDraft: clearBatteryConfigDraft } = useDraft('battery-dc-config', {
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
  actualDod: 90
})

// 计算簇参数
watch(
  () => [batteryConfig.seriesCount, batteryConfig.parallelCount, batteryConfig.cellVoltage, batteryConfig.cellCapacity],
  () => {
    batteryConfig.stringVoltage = batteryConfig.seriesCount * batteryConfig.cellVoltage
    batteryConfig.stringCapacity = batteryConfig.parallelCount * batteryConfig.cellCapacity
    batteryConfig.stringEnergy = (batteryConfig.stringVoltage * batteryConfig.stringCapacity) / 1000
  }
)

// 计算总直流能量
watch(
  () => [batteryConfig.containerQty, batteryConfig.containerEnergy],
  () => {
    batteryConfig.totalDcEnergy = batteryConfig.containerQty * batteryConfig.containerEnergy
  }
)

// 计算电池簇总数
const totalStrings = computed(() => {
  return Math.ceil(batteryConfig.containerQty * batteryConfig.clustersPerContainer)
})

// 计算配置
function calculateBatteryConfig() {
  // 验证输入
  if (batteryConfig.containerEnergy <= 0 || batteryConfig.containerQty <= 0) {
    showToast(t('batteryDC.msgCheckContainerConfig'), 'error')
    return
  }

  // 根据用户输入的簇数量和集装箱数量，推算每箱簇数（不覆盖用户的簇数量输入）
  if (batteryConfig.stringQty > 0 && batteryConfig.containerQty > 0) {
    batteryConfig.clustersPerContainer = Math.ceil(batteryConfig.stringQty / batteryConfig.containerQty)
  } else {
    // 回退：使用能量公式估算
    const clustersNeeded = Math.ceil((batteryConfig.containerEnergy * 1000) / batteryConfig.stringEnergy)
    batteryConfig.clustersPerContainer = clustersNeeded
    batteryConfig.stringQty = batteryConfig.containerQty * clustersNeeded
  }

  // 计算总直流能量
  batteryConfig.totalDcEnergy = batteryConfig.containerQty * batteryConfig.containerEnergy

  // 计算电压范围
  const minVoltage = batteryConfig.seriesCount * 3.0 // SOC低时
  const maxVoltage = batteryConfig.seriesCount * 3.65 // SOC高时
  batteryConfig.dcVoltageRange = `${minVoltage.toFixed(0)}-${maxVoltage.toFixed(0)}V`

  // 计算最大直流电流 (假设0.5C放电)
  // 公式: I = (E × 10^6 / V) × 0.5C  (E单位MWh，V单位V，结果A)
  const avgVoltage = (minVoltage + maxVoltage) / 2
  const capacityAh = (batteryConfig.containerEnergy * 1000000) / avgVoltage
  const maxDischargeCurrent = capacityAh * 0.5
  batteryConfig.maxDcCurrent = Math.round(maxDischargeCurrent)

  // DC断路器选择 (1.2倍过载)
  batteryConfig.dcBreaker = Math.ceil((maxDischargeCurrent * 1.2) / 100) * 100

  // 实际DOD
  batteryConfig.actualDod = Math.min(batteryConfig.dodSet, 95)

  showToast(t('batteryDC.msgCalcComplete'))
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
    actualDod: 90
  })
  showToast(t('batteryDC.msgConfigReset'))
}

// 应用配置
function applyBatteryConfig() {
  emit('apply-config', {
    ratedEnergy: batteryConfig.containerEnergy,
    containerQty: batteryConfig.containerQty,
    dod: batteryConfig.actualDod,
    cyclesPerDay: batteryConfig.cyclesPerDay,
    temperature: batteryConfig.operatingTemp
  })
  // 应用配置后，App.vue 会触发数据库持久化（syncParamsToDb），此处保留草稿以便用户回看
  showToast(t('batteryDC.msgConfigApplied'))
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
