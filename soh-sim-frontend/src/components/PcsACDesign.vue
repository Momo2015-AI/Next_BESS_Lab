<template>
  <div class="pcs-ac-design h-full overflow-auto p-4">
    <div class="rounded-lg p-4 card-bordered">
      <h3 class="text-sm font-bold mb-4 flex items-center gap-2 text-accent">
        <span class="w-2 h-2 rounded-full bg-accent" />
        交流侧设计（PCS系统）
      </h3>

      <!-- PCS选型 -->
      <div class="grid grid-cols-2 gap-4 mb-4">
        <div
          class="rounded-lg p-4"
 class="bg-card-dark border-card"
        >
          <h4 class="text-xs mb-3 font-medium text-secondary">PCS功率选型</h4>

          <div class="space-y-3">
            <div>
              <label class="text-[10px] block mb-1 text-muted">PCS型号</label>
              <select
                v-model="selectedPcsId"
                class="w-full rounded px-2 py-1.5 text-xs form-field-select"
                @change="onPcsChange"
              >
                <option value="">-- 请选择PCS --</option>
                <option v-for="p in pcs" :key="p.id" :value="p.id">
                  {{ p.mfr }} - {{ p.model }} ({{ p.ratedPowerMW }}MW)
                </option>
              </select>
            </div>

            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] block mb-1 text-muted">直流电压范围 (V)</label>
                <input
                  v-model="pcsConfig.dcVoltageRange"
                  type="text"
                  readonly
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1 text-muted">直流最大电流 (A)</label>
                <input
                  v-model.number="pcsConfig.maxDcCurrent"
                  type="number"
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] block mb-1 text-muted">交流额定功率 (kW)</label>
                <input
                  v-model.number="pcsConfig.acRatedPower"
                  type="number"
                  readonly
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1 text-muted">额定交流电流 (A)</label>
                <input
                  v-model.number="pcsConfig.acRatedCurrent"
                  type="number"
                  readonly
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
            </div>
          </div>
        </div>

        <div
          class="rounded-lg p-4"
 class="bg-card-dark border-card"
        >
          <h4 class="text-xs mb-3 font-medium text-secondary">PCS数量配置</h4>

          <div class="space-y-3">
            <div>
              <label class="text-[10px] block mb-1 text-muted">PCS数量计算方式</label>
              <select v-model="pcsConfig.calcMode" class="w-full rounded px-2 py-1.5 text-xs form-field-select">
                <option value="ratio">按功率配比计算</option>
                <option value="fixed">固定数量</option>
                <option value="energy">按能量需求</option>
              </select>
            </div>

            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] block mb-1 text-muted">PCS数量</label>
                <input
                  v-model.number="pcsConfig.pcsQty"
                  type="number"
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1 text-muted">并机数量</label>
                <input
                  v-model.number="pcsConfig.parallelCount"
                  type="number"
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] block mb-1 text-muted">总PCS功率 (MW)</label>
                <input
                  v-model.number="pcsConfig.totalPcsPower"
                  type="number"
                  readonly
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1 text-muted">功率配比</label>
                <input
                  v-model.number="pcsConfig.powerRatio"
                  type="number"
                  step="0.1"
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 变压器配置 -->
      <div
        class="rounded-lg p-4 mb-4"
 class="bg-card-dark border-card"
      >
        <h4 class="text-xs mb-3 font-medium text-secondary">变压器与电网连接</h4>

        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] block mb-1 text-muted">变压器类型</label>
            <select v-model="pcsConfig.transformerType" class="w-full rounded px-2 py-1 text-xs form-field-select">
              <option value="2w">两绕组变压器</option>
              <option value="3w">三绕组变压器</option>
              <option value="一体化">一体化升压装置</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] block mb-1 text-muted">变压器容量 (MVA)</label>
            <input
              v-model.number="pcsConfig.transformerCapacity"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1 text-muted">变压器数量</label>
            <input
              v-model.number="pcsConfig.transformerQty"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1 text-muted">高压侧电压 (kV)</label>
            <input
              v-model.number="pcsConfig.hvVoltage"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
        </div>

        <div class="grid grid-cols-4 gap-3 mt-3">
          <div>
            <label class="text-[10px] block mb-1 text-muted">低压侧电压 (V)</label>
            <input
              v-model.number="pcsConfig.lvVoltage"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1 text-muted">短路阻抗 (%)</label>
            <input
              v-model.number="pcsConfig.impedance"
              type="number"
              step="0.1"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1 text-muted">接线方式</label>
            <select v-model="pcsConfig.connection" class="w-full rounded px-2 py-1 text-xs form-field-select">
              <option value="Dynd11">Dyn11</option>
              <option value="Ynd11">Ynd11</option>
              <option value="Yyn0">Yyn0</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] block mb-1 text-muted">接地方式</label>
            <select v-model="pcsConfig.grounding" class="w-full rounded px-2 py-1 text-xs form-field-select">
              <option value="直接接地">直接接地</option>
              <option value="消弧线圈">消弧线圈</option>
              <option value="电阻接地">电阻接地</option>
            </select>
          </div>
        </div>
      </div>

      <!-- 运行参数 -->
      <div
        class="rounded-lg p-4 mb-4"
 class="bg-card-dark border-card"
      >
        <h4 class="text-xs mb-3 font-medium text-secondary">PCS运行参数</h4>

        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] block mb-1 text-muted">PCS效率 (%)</label>
            <input
              v-model.number="pcsConfig.pcsEfficiency"
              type="number"
              step="0.1"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1 text-muted">运行辅耗 (kW)</label>
            <input
              v-model.number="pcsConfig.auxConsumption"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1 text-muted">待机辅耗 (kW)</label>
            <input
              v-model.number="pcsConfig.standbyConsumption"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1 text-muted">功率因数</label>
            <input
              v-model.number="pcsConfig.powerFactor"
              type="number"
              step="0.01"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
        </div>
      </div>

      <!-- 配置规则 -->
      <div
        class="rounded-lg p-4 mb-4"
 class="bg-card-dark border-card"
      >
        <h4 class="text-xs mb-3 font-medium text-warning">⚡ PCS与电池配置规则</h4>

        <div class="grid grid-cols-2 gap-4">
          <div class="rounded p-3 bg-input-dark">
            <div class="text-xs mb-2 text-secondary">常用配置规则（基于0.5C放电）</div>
            <div class="space-y-1 text-[10px]">
              <div class="flex justify-between">
                <span>5MWh集装箱</span>class="text-muted"
                <span>→ 2台 2.5MW PCS</span>class="text-accent"
              </div>
              <div class="flex justify-between">
                <span>10MWh集装箱</span>class="text-muted"
                <span>→ 2台 5MW PCS</span>class="text-accent"
              </div>
              <div class="flex justify-between">
                <span>20MWh集装箱</span>class="text-muted"
                <span>→ 4台 5MW PCS</span>class="text-accent"
              </div>
            </div>
          </div>
          <div class="rounded p-3 bg-input-dark">
            <div class="text-xs mb-2 text-secondary">功率配比计算</div>
            <div class="text-[10px] text-muted">
              PCS总功率 = 电池总能量 ÷ 放电时长
              <br />
              例：100MWh ÷ 2h = 50MW PCS
              <br />
              配比：1:2 (能量:功率)
            </div>
          </div>
        </div>

        <button
          class="mt-3 text-xs px-3 py-1.5 rounded transition-colors"
 class="u-background-color-var-color-warning-color-white"
          @click="applyConfigRules"
        >
          根据电池配置自动计算PCS
        </button>
      </div>

      <!-- 配置结果 -->
      <div
        class="rounded-lg p-4"
 class="bg-card-dark border-card"
      >
        <div class="flex items-center justify-between mb-3">
          <h4 class="text-xs font-medium text-secondary">PCS系统配置结果</h4>
          <button
            class="text-xs px-3 py-1 rounded transition-colors"
 class="bg-accent text-white"
            @click="calculatePcsConfig"
          >
            计算配置
          </button>
        </div>

        <div class="grid grid-cols-6 gap-3">
          <div class="text-center rounded p-2 bg-input">
            <div class="text-lg font-bold text-accent">
              {{ pcsConfig.pcsQty }}
            </div>
            <div class="text-[10px] text-muted">PCS数量</div>
          </div>
          <div class="text-center rounded p-2 bg-input">
            <div class="text-lg font-bold text-accent-2">
              {{ pcsConfig.totalPcsPower.toFixed(1) }}
            </div>
            <div class="text-[10px] text-muted">总PCS功率 (MW)</div>
          </div>
          <div class="text-center rounded p-2 bg-input">
            <div class="text-lg font-bold text-success">
              {{ pcsConfig.powerRatio.toFixed(1) }}:1
            </div>
            <div class="text-[10px] text-muted">功率配比</div>
          </div>
          <div class="text-center rounded p-2 bg-input">
            <div class="text-lg font-bold text-warning">
              {{ pcsConfig.transformerQty }}
            </div>
            <div class="text-[10px] text-muted">变压器数量</div>
          </div>
          <div class="text-center rounded p-2 bg-input">
            <div class="text-lg font-bold text-accent-2">
              {{ pcsConfig.transformerCapacity }}MVA
            </div>
            <div class="text-[10px] text-muted">单台变压器容量</div>
          </div>
          <div class="text-center rounded p-2 bg-input">
            <div class="text-lg font-bold text-danger">{{ pcsConfig.pcsEfficiency }}%</div>
            <div class="text-[10px] text-muted">PCS效率</div>
          </div>
        </div>

        <div class="mt-4 flex justify-end gap-2">
          <button
            class="text-xs px-3 py-1.5 rounded transition-colors"
            class="u-background-color-var-color-card-border-1px-solid-var-color-border-color-var-color-text-secondary"
            @click="resetPcsConfig"
          >
            重置
          </button>
          <button
            class="text-xs px-4 py-1.5 rounded transition-colors"
 class="bg-accent text-white"
            @click="applyPcsConfig"
          >
            应用配置
          </button>
        </div>
      </div>
    </div>

    <!-- Toast -->
    <div
      v-if="toast.show"
      class="fixed bottom-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all"
      :style="{
        backgroundColor: toast.type === 'success' ? 'var(--color-success)' : 'var(--color-danger)',
        color: 'white'
      }"
    >
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, computed, onMounted } from 'vue'
import { useProducts } from '../composables/useProducts'
import { useDraft, useDraftRef } from '../composables/useDraft'

const emit = defineEmits(['apply-config', 'error'])

const { pcs, loadAll } = useProducts()

// PCS库数据源（从统一产品库获取）
const selectedPcsId = useDraftRef('pcs-ac-selected-pcs-id', '').state

async function loadPcsLibrary() {
  await loadAll()
  // 默认选中第一个
  if (pcs.value.length > 0 && !selectedPcsId.value) {
    selectedPcsId.value = pcs.value[0].id
    onPcsChange()
  }
}

function onPcsChange() {
  const pcsItem = pcs.value.find((p) => p.id === selectedPcsId.value)
  if (pcsItem) {
    pcsConfig.pcsPower = pcsItem.ratedPowerMW || 2.5
    pcsConfig.dcVoltageRange = pcsItem.dcVoltageRange || '800-1500V'
    pcsConfig.maxDcCurrent = pcsItem.maxDcCurrent || 1500
    pcsConfig.acRatedPower = (pcsItem.ratedPowerMW || 2.5) * 1000
    pcsConfig.acVoltage = pcsItem.acVoltage || 800
    pcsConfig.efficiency = pcsItem.efficiency || 98.5
    pcsConfig.cooling = pcsItem.cooling || '风冷'
    pcsConfig.frequencyRange = pcsItem.frequencyRange || '47-63Hz'
    pcsConfig.weight = pcsItem.weight || 1200
    pcsConfig.auxRun = pcsItem.auxRun || 4.5
    pcsConfig.auxStandby = pcsItem.auxStandby || 1.2
  }
}

onMounted(() => {
  loadPcsLibrary()
})

const toast = reactive({ show: false, message: '', type: 'success' })
const showToast = (message, type = 'success') => {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => {
    toast.show = false
  }, 3000)
}

const { state: pcsConfig, clearDraft: clearPcsConfigDraft } = useDraft('pcs-ac-config', {
  pcsPower: 5,
  dcVoltageRange: '672-864V',
  maxDcCurrent: 1500,
  acRatedPower: 5000,
  acRatedCurrent: 5774,

  calcMode: 'ratio',
  pcsQty: 10,
  parallelCount: 1,
  totalPcsPower: 50,
  powerRatio: 1.0,

  transformerType: '一体化',
  transformerCapacity: 6.3,
  transformerQty: 5,
  hvVoltage: 35,
  lvVoltage: 690,
  impedance: 10.5,
  connection: 'Dyn11',
  grounding: '电阻接地',

  pcsEfficiency: 99,
  auxConsumption: 6.5,
  standbyConsumption: 1.0,
  powerFactor: 0.95
})

const externalBatteryConfig = reactive({
  totalEnergy: 50,
  containerQty: 10,
  containerEnergy: 5
})

watch(
  () => [pcsConfig.pcsQty, pcsConfig.pcsPower],
  () => {
    pcsConfig.totalPcsPower = pcsConfig.pcsQty * pcsConfig.pcsPower
  }
)

watch(
  () => pcsConfig.totalPcsPower,
  () => {
    pcsConfig.transformerQty = Math.ceil(pcsConfig.totalPcsPower / 5)
    pcsConfig.transformerCapacity = 6.3
  }
)

function applyConfigRules() {
  const batteryEnergy = externalBatteryConfig.totalEnergy
  const dischargeHours = 2

  const requiredPower = batteryEnergy / dischargeHours

  pcsConfig.powerRatio = Number((batteryEnergy / requiredPower).toFixed(1))

  pcsConfig.pcsQty = Math.ceil(requiredPower / pcsConfig.pcsPower)
  pcsConfig.totalPcsPower = pcsConfig.pcsQty * pcsConfig.pcsPower

  pcsConfig.transformerQty = Math.ceil(pcsConfig.totalPcsPower / 5)

  showToast('PCS配置已根据电池参数自动计算')
}

function calculatePcsConfig() {
  if (pcsConfig.totalPcsPower <= 0) {
    showToast('请检查PCS配置', 'error')
    return
  }

  pcsConfig.acRatedCurrent = Math.round((pcsConfig.totalPcsPower * 1000) / (1.732 * 0.69 * pcsConfig.powerFactor))

  pcsConfig.transformerCapacity = Math.ceil((pcsConfig.totalPcsPower / pcsConfig.transformerQty) * 1.1 * 10) / 10

  showToast('PCS配置计算完成')
}

function resetPcsConfig() {
  Object.assign(pcsConfig, {
    pcsPower: 5,
    pcsQty: 10,
    totalPcsPower: 50,
    powerRatio: 1.0,
    transformerType: '一体化',
    transformerCapacity: 6.3,
    transformerQty: 5,
    pcsEfficiency: 99,
    auxConsumption: 6.5,
    standbyConsumption: 1.0
  })
  showToast('配置已重置')
}

function applyPcsConfig() {
  emit('apply-config', {
    pcsPower: pcsConfig.pcsPower,
    pcsQty: pcsConfig.pcsQty,
    totalPcsPower: pcsConfig.totalPcsPower,
    powerRatio: pcsConfig.powerRatio,
    acEfficiency: pcsConfig.pcsEfficiency,
    pcsAuxRun: pcsConfig.auxConsumption,
    pcsAuxStandby: pcsConfig.standbyConsumption
  })
  showToast('PCS配置已应用')
}

function setBatteryConfig(config) {
  externalBatteryConfig.totalEnergy = config.totalEnergy || 50
  externalBatteryConfig.containerQty = config.containerQty || 10
  externalBatteryConfig.containerEnergy = config.containerEnergy || 5
}

defineExpose({ setBatteryConfig, applyConfigRules })
</script>

<style scoped>
.pcs-ac-design {
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
