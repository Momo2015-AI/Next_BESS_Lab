<template>
  <div class="pcs-ac-design h-full overflow-auto p-4">
    <div class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border)">
      <h3 class="text-sm font-bold mb-4 flex items-center gap-2" style="color: var(--color-accent)">
        <span class="w-2 h-2 rounded-full" style="background-color: var(--color-accent)" />
        {{ $t('pcsAC.title') }}
      </h3>

      <!-- PCS选型 -->
      <div class="grid grid-cols-2 gap-4 mb-4">
        <div
          class="rounded-lg p-4"
          style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
        >
          <h4 class="text-xs mb-3 font-medium" style="color: var(--color-text-secondary)">
            {{ $t('pcsAC.pcsPowerSelection') }}
          </h4>

          <div class="space-y-3">
            <div>
              <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
                {{ $t('pcsAC.pcsModel') }}
              </label>
              <select
                v-model="selectedPcsId"
                class="w-full rounded px-2 py-1.5 text-xs form-field-select"
                @change="onPcsChange"
              >
                <option value="">{{ $t('pcsAC.selectPcs') }}</option>
                <option v-for="p in pcs" :key="p.id" :value="p.id">
                  {{ p.mfr }} - {{ p.model }} ({{ p.ratedPowerMW }}MW)
                </option>
              </select>
            </div>

            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
                  {{ $t('pcsAC.dcVoltageRange') }}
                </label>
                <input
                  v-model="pcsConfig.dcVoltageRange"
                  type="text"
                  readonly
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
                  {{ $t('pcsAC.maxDcCurrent') }}
                </label>
                <input
                  v-model.number="pcsConfig.maxDcCurrent"
                  type="number"
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
                  {{ $t('pcsAC.acRatedPower') }}
                </label>
                <input
                  v-model.number="pcsConfig.acRatedPower"
                  type="number"
                  readonly
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
                  {{ $t('pcsAC.acRatedCurrent') }}
                </label>
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
          style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
        >
          <h4 class="text-xs mb-3 font-medium" style="color: var(--color-text-secondary)">
            {{ $t('pcsAC.pcsQtyConfig') }}
          </h4>

          <div class="space-y-3">
            <div>
              <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
                {{ $t('pcsAC.calcMode') }}
              </label>
              <select v-model="pcsConfig.calcMode" class="w-full rounded px-2 py-1.5 text-xs form-field-select">
                <option value="ratio">{{ $t('pcsAC.calcModeRatio') }}</option>
                <option value="fixed">{{ $t('pcsAC.calcModeFixed') }}</option>
                <option value="energy">{{ $t('pcsAC.calcModeEnergy') }}</option>
              </select>
            </div>

            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
                  {{ $t('pcsAC.pcsQty') }}
                </label>
                <input
                  v-model.number="pcsConfig.pcsQty"
                  type="number"
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
                  {{ $t('pcsAC.parallelCount') }}
                </label>
                <input
                  v-model.number="pcsConfig.parallelCount"
                  type="number"
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
                  {{ $t('pcsAC.totalPcsPower') }}
                </label>
                <input
                  v-model.number="pcsConfig.totalPcsPower"
                  type="number"
                  readonly
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
                  {{ $t('pcsAC.powerRatio') }}
                </label>
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
        style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
      >
        <h4 class="text-xs mb-3 font-medium" style="color: var(--color-text-secondary)">
          {{ $t('pcsAC.transformerAndGrid') }}
        </h4>

        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
              {{ $t('pcsAC.transformerType') }}
            </label>
            <select v-model="pcsConfig.transformerType" class="w-full rounded px-2 py-1 text-xs form-field-select">
              <option value="2w">{{ $t('pcsAC.transformer2w') }}</option>
              <option value="3w">{{ $t('pcsAC.transformer3w') }}</option>
              <option value="一体化">{{ $t('pcsAC.transformerIntegrated') }}</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
              {{ $t('pcsAC.transformerCapacity') }}
            </label>
            <input
              v-model.number="pcsConfig.transformerCapacity"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">
              {{ $t('pcsAC.transformerQty') }}
            </label>
            <input
              v-model.number="pcsConfig.transformerQty"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">高压侧电压 (kV)</label>
            <input
              v-model.number="pcsConfig.hvVoltage"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
        </div>

        <div class="grid grid-cols-4 gap-3 mt-3">
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">低压侧电压 (V)</label>
            <input
              v-model.number="pcsConfig.lvVoltage"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">短路阻抗 (%)</label>
            <input
              v-model.number="pcsConfig.impedance"
              type="number"
              step="0.1"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">接线方式</label>
            <select v-model="pcsConfig.connection" class="w-full rounded px-2 py-1 text-xs form-field-select">
              <option value="Dynd11">Dyn11</option>
              <option value="Ynd11">Ynd11</option>
              <option value="Yyn0">Yyn0</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">接地方式</label>
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
        style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
      >
        <h4 class="text-xs mb-3 font-medium" style="color: var(--color-text-secondary)">PCS运行参数</h4>

        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">PCS效率 (%)</label>
            <input
              v-model.number="pcsConfig.pcsEfficiency"
              type="number"
              step="0.1"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">运行辅耗 (kW)</label>
            <input
              v-model.number="pcsConfig.auxConsumption"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">待机辅耗 (kW)</label>
            <input
              v-model.number="pcsConfig.standbyConsumption"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted)">功率因数</label>
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
        style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
      >
        <h4 class="text-xs mb-3 font-medium" style="color: var(--color-warning)">⚡ PCS与电池配置规则</h4>

        <div class="grid grid-cols-2 gap-4">
          <div class="rounded p-3" style="background-color: var(--color-input-bg-dark)">
            <div class="text-xs mb-2" style="color: var(--color-text-secondary)">常用配置规则（基于0.5C放电）</div>
            <div class="space-y-1 text-[10px]">
              <div class="flex justify-between">
                <span style="color: var(--color-text-muted)">5MWh集装箱</span>
                <span style="color: var(--color-accent)">→ 2台 2.5MW PCS</span>
              </div>
              <div class="flex justify-between">
                <span style="color: var(--color-text-muted)">10MWh集装箱</span>
                <span style="color: var(--color-accent)">→ 2台 5MW PCS</span>
              </div>
              <div class="flex justify-between">
                <span style="color: var(--color-text-muted)">20MWh集装箱</span>
                <span style="color: var(--color-accent)">→ 4台 5MW PCS</span>
              </div>
            </div>
          </div>
          <div class="rounded p-3" style="background-color: var(--color-input-bg-dark)">
            <div class="text-xs mb-2" style="color: var(--color-text-secondary)">功率配比计算</div>
            <div class="text-[10px]" style="color: var(--color-text-muted)">
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
          style="background-color: var(--color-warning); color: white"
          @click="applyConfigRules"
        >
          根据电池配置自动计算PCS
        </button>
      </div>

      <!-- 配置结果 -->
      <div
        class="rounded-lg p-4"
        style="background-color: var(--color-card-dark); border: 1px solid var(--color-border)"
      >
        <div class="flex items-center justify-between mb-3">
          <h4 class="text-xs font-medium" style="color: var(--color-text-secondary)">PCS系统配置结果</h4>
          <button
            class="text-xs px-3 py-1 rounded transition-colors"
            style="background-color: var(--color-accent); color: white"
            @click="calculatePcsConfig"
          >
            计算配置
          </button>
        </div>

        <div class="grid grid-cols-6 gap-3">
          <div class="text-center rounded p-2" style="background-color: var(--color-input-bg)">
            <div class="text-lg font-bold" style="color: var(--color-accent)">
              {{ pcsConfig.pcsQty }}
            </div>
            <div class="text-[10px]" style="color: var(--color-text-muted)">PCS数量</div>
          </div>
          <div class="text-center rounded p-2" style="background-color: var(--color-input-bg)">
            <div class="text-lg font-bold" style="color: var(--color-accent-secondary)">
              {{ pcsConfig.totalPcsPower.toFixed(1) }}
            </div>
            <div class="text-[10px]" style="color: var(--color-text-muted)">总PCS功率 (MW)</div>
          </div>
          <div class="text-center rounded p-2" style="background-color: var(--color-input-bg)">
            <div class="text-lg font-bold" style="color: var(--color-success)">
              {{ pcsConfig.powerRatio.toFixed(1) }}:1
            </div>
            <div class="text-[10px]" style="color: var(--color-text-muted)">功率配比</div>
          </div>
          <div class="text-center rounded p-2" style="background-color: var(--color-input-bg)">
            <div class="text-lg font-bold" style="color: var(--color-warning)">
              {{ pcsConfig.transformerQty }}
            </div>
            <div class="text-[10px]" style="color: var(--color-text-muted)">变压器数量</div>
          </div>
          <div class="text-center rounded p-2" style="background-color: var(--color-input-bg)">
            <div class="text-lg font-bold" style="color: var(--color-accent-secondary)">
              {{ pcsConfig.transformerCapacity }}MVA
            </div>
            <div class="text-[10px]" style="color: var(--color-text-muted)">单台变压器容量</div>
          </div>
          <div class="text-center rounded p-2" style="background-color: var(--color-input-bg)">
            <div class="text-lg font-bold" style="color: var(--color-danger)">{{ pcsConfig.pcsEfficiency }}%</div>
            <div class="text-[10px]" style="color: var(--color-text-muted)">PCS效率</div>
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
            @click="resetPcsConfig"
          >
            重置
          </button>
          <button
            class="text-xs px-4 py-1.5 rounded transition-colors"
            style="background-color: var(--color-accent); color: white"
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
import { useI18n } from 'vue-i18n'
import { useProducts } from '../composables/useProducts'
import { useDraft, useDraftRef } from '../composables/useDraft'

const { t } = useI18n()

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
