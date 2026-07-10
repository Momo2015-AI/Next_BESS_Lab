<template>
  <div class="pcs-ac-design h-full overflow-auto p-4">
    <div class="rounded-lg p-4 ins-1">
      <h3 class="text-sm font-bold mb-4 flex items-center gap-2 ins-2">
        <span class="w-2 h-2 rounded-full ins-3" />
        {{ $t('pcsAC.title') }}
      </h3>

      <!-- PCS选型 -->
      <div class="grid grid-cols-2 gap-4 mb-4">
        <div
          class="rounded-lg p-4 ins-4"
         
        >
          <h4 class="text-xs mb-3 font-medium ins-5">
            {{ $t('pcsAC.pcsPowerSelection') }}
          </h4>

          <div class="space-y-3">
            <div>
              <label class="text-[10px] block mb-1 ins-6">
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
                <label class="text-[10px] block mb-1 ins-6">
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
                <label class="text-[10px] block mb-1 ins-6">
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
                <label class="text-[10px] block mb-1 ins-6">
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
                <label class="text-[10px] block mb-1 ins-6">
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
          class="rounded-lg p-4 ins-4"
         
        >
          <h4 class="text-xs mb-3 font-medium ins-5">
            {{ $t('pcsAC.pcsQtyConfig') }}
          </h4>

          <div class="space-y-3">
            <div>
              <label class="text-[10px] block mb-1 ins-6">
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
                <label class="text-[10px] block mb-1 ins-6">
                  {{ $t('pcsAC.pcsQty') }}
                </label>
                <input
                  v-model.number="pcsConfig.pcsQty"
                  type="number"
                  class="w-full rounded px-2 py-1 text-xs form-field-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1 ins-6">
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
                <label class="text-[10px] block mb-1 ins-6">
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
                <label class="text-[10px] block mb-1 ins-6">
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
        class="rounded-lg p-4 mb-4 ins-4"
       
      >
        <h4 class="text-xs mb-3 font-medium ins-5">
          {{ $t('pcsAC.transformerAndGrid') }}
        </h4>

        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] block mb-1 ins-6">
              {{ $t('pcsAC.transformerType') }}
            </label>
            <select v-model="pcsConfig.transformerType" class="w-full rounded px-2 py-1 text-xs form-field-select">
              <option value="2w">{{ $t('pcsAC.transformer2w') }}</option>
              <option value="3w">{{ $t('pcsAC.transformer3w') }}</option>
              <option value="integrated">{{ $t('pcsAC.transformerIntegrated') }}</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] block mb-1 ins-6">
              {{ $t('pcsAC.transformerCapacity') }}
            </label>
            <input
              v-model.number="pcsConfig.transformerCapacity"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1 ins-6">
              {{ $t('pcsAC.transformerQty') }}
            </label>
            <input
              v-model.number="pcsConfig.transformerQty"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1 ins-6">{{ $t('acDesign.hvSideVoltage') }}</label>
            <input
              v-model.number="pcsConfig.hvVoltage"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
        </div>

        <div class="grid grid-cols-4 gap-3 mt-3">
          <div>
            <label class="text-[10px] block mb-1 ins-6">{{ $t('acDesign.lvSideVoltage') }}</label>
            <input
              v-model.number="pcsConfig.lvVoltage"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1 ins-6">{{ $t('acDesign.shortCircuitImpedance') }}</label>
            <input
              v-model.number="pcsConfig.impedance"
              type="number"
              step="0.1"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1 ins-6">{{ $t('acDesign.wiringMethod') }}</label>
            <select v-model="pcsConfig.connection" class="w-full rounded px-2 py-1 text-xs form-field-select">
              <option value="Dynd11">Dyn11</option>
              <option value="Ynd11">Ynd11</option>
              <option value="Yyn0">Yyn0</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] block mb-1 ins-6">{{ $t('acDesign.groundingMethod') }}</label>
            <select v-model="pcsConfig.grounding" class="w-full rounded px-2 py-1 text-xs form-field-select">
              <option value="direct">{{ $t('acDesign.groundingDirect') }}</option>
              <option value="arc">{{ $t('acDesign.groundingArc') }}</option>
              <option value="resistance">{{ $t('acDesign.groundingResistance') }}</option>
            </select>
          </div>
        </div>
      </div>

      <!-- 运行参数 -->
      <div
        class="rounded-lg p-4 mb-4 ins-4"
       
      >
        <h4 class="text-xs mb-3 font-medium ins-5">{{ $t('acDesign.operatingParams') }}</h4>

        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] block mb-1 ins-6">{{ $t('acDesign.pcsEfficiency') }}</label>
            <input
              v-model.number="pcsConfig.pcsEfficiency"
              type="number"
              step="0.1"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1 ins-6">{{ $t('acDesign.runAux') }}</label>
            <input
              v-model.number="pcsConfig.auxConsumption"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1 ins-6">{{ $t('acDesign.standbyAux') }}</label>
            <input
              v-model.number="pcsConfig.standbyConsumption"
              type="number"
              class="w-full rounded px-2 py-1 text-xs form-field-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1 ins-6">{{ $t('acDesign.powerFactor') }}</label>
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
        class="rounded-lg p-4 mb-4 ins-4"
       
      >
        <h4 class="text-xs mb-3 font-medium ins-7">⚡ {{ $t('acDesign.configRules') }}</h4>

        <div class="grid grid-cols-2 gap-4">
          <div class="rounded p-3 ins-8">
            <div class="text-xs mb-2 ins-5">{{ $t('acDesign.commonRules') }}</div>
            <div class="space-y-1 text-[10px]">
              <div class="flex justify-between">
                <span class="ins-6">{{ $t('acDesign.container5mwh') }}</span>
                <span class="ins-2">→ 2台 2.5MW PCS</span>
              </div>
              <div class="flex justify-between">
                <span class="ins-6">{{ $t('acDesign.container10mwh') }}</span>
                <span class="ins-2">→ 2台 5MW PCS</span>
              </div>
              <div class="flex justify-between">
                <span class="ins-6">{{ $t('acDesign.container20mwh') }}</span>
                <span class="ins-2">→ 4台 5MW PCS</span>
              </div>
            </div>
          </div>
          <div class="rounded p-3 ins-8">
            <div class="text-xs mb-2 ins-5">{{ $t('acDesign.powerRatioCalc') }}</div>
            <div class="text-[10px] ins-6">
              {{ $t('acDesign.pcsTotalPower') }}
              <br />
              {{ $t('acDesign.example') }}
              <br />
              {{ $t('acDesign.ratio') }}
            </div>
          </div>
        </div>

        <button
          class="mt-3 text-xs px-3 py-1.5 rounded transition-colors ins-9"
         
          @click="applyConfigRules"
        >
          {{ $t('acDesign.autoCalcFromBattery') }}
        </button>
      </div>

      <!-- 配置结果 -->
      <div
        class="rounded-lg p-4 ins-4"
       
      >
        <div class="flex items-center justify-between mb-3">
          <h4 class="text-xs font-medium ins-5">{{ $t('acDesign.result') }}</h4>
          <button
            class="text-xs px-3 py-1 rounded transition-colors ins-10"
           
            @click="calculatePcsConfig"
          >
            {{ $t('acDesign.checkConfig') }}
          </button>
        </div>

        <div class="grid grid-cols-6 gap-3">
          <div class="text-center rounded p-2 ins-11">
            <div class="text-lg font-bold ins-2">
              {{ pcsConfig.pcsQty }}
            </div>
            <div class="text-[10px] ins-6">{{ $t('acDesign.pcsQty') }}</div>
          </div>
          <div class="text-center rounded p-2 ins-11">
            <div class="text-lg font-bold ins-12">
              {{ pcsConfig.totalPcsPower.toFixed(1) }}
            </div>
            <div class="text-[10px] ins-6">{{ $t('acDesign.totalPcsPower') }}</div>
          </div>
          <div class="text-center rounded p-2 ins-11">
            <div class="text-lg font-bold ins-13">
              {{ pcsConfig.powerRatio.toFixed(1) }}:1
            </div>
            <div class="text-[10px] ins-6">{{ $t('acDesign.powerRatio') }}</div>
          </div>
          <div class="text-center rounded p-2 ins-11">
            <div class="text-lg font-bold ins-7">
              {{ pcsConfig.transformerQty }}
            </div>
            <div class="text-[10px] ins-6">{{ $t('acDesign.transformerQty') }}</div>
          </div>
          <div class="text-center rounded p-2 ins-11">
            <div class="text-lg font-bold ins-12">
              {{ pcsConfig.transformerCapacity }}MVA
            </div>
            <div class="text-[10px] ins-6">{{ $t('acDesign.singleTransformerCapacity') }}</div>
          </div>
          <div class="text-center rounded p-2 ins-11">
            <div class="text-lg font-bold ins-14">{{ pcsConfig.pcsEfficiency }}%</div>
            <div class="text-[10px] ins-6">{{ $t('acDesign.pcsEfficiencyLabel') }}</div>
          </div>
        </div>

        <div class="mt-4 flex justify-end gap-2">
          <button
            class="text-xs px-3 py-1.5 rounded transition-colors ins-15"
           
            @click="resetPcsConfig"
          >
            {{ $t('acDesign.reset') }}
          </button>
          <button
            class="text-xs px-4 py-1.5 rounded transition-colors ins-10"
           
            @click="applyPcsConfig"
          >
            {{ $t('acDesign.applyConfig') }}
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

  transformerType: 'integrated',
  transformerCapacity: 6.3,
  transformerQty: 5,
  hvVoltage: 35,
  lvVoltage: 690,
  impedance: 10.5,
  connection: 'Dyn11',
  grounding: 'resistance',

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

  showToast(t('acDesign.configAutoCalculated'))
}

function calculatePcsConfig() {
  if (pcsConfig.totalPcsPower <= 0) {
    showToast(t('acDesign.checkConfig'), 'error')
    return
  }

  pcsConfig.acRatedCurrent = Math.round((pcsConfig.totalPcsPower * 1000) / (1.732 * 0.69 * pcsConfig.powerFactor))

  pcsConfig.transformerCapacity = Math.ceil((pcsConfig.totalPcsPower / pcsConfig.transformerQty) * 1.1 * 10) / 10

  showToast(t('acDesign.calcComplete'))
}

function resetPcsConfig() {
  Object.assign(pcsConfig, {
    pcsPower: 5,
    pcsQty: 10,
    totalPcsPower: 50,
    powerRatio: 1.0,
    transformerType: 'integrated',
    transformerCapacity: 6.3,
    transformerQty: 5,
    pcsEfficiency: 99,
    auxConsumption: 6.5,
    standbyConsumption: 1.0
  })
  showToast(t('acDesign.configReset'))
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
  showToast(t('acDesign.configApplied'))
}

function setBatteryConfig(config) {
  externalBatteryConfig.totalEnergy = config.totalEnergy || 50
  externalBatteryConfig.containerQty = config.containerQty || 10
  externalBatteryConfig.containerEnergy = config.containerEnergy || 5
}

defineExpose({ setBatteryConfig, applyConfigRules })
</script>

<style scoped>
.ins-1 { background-color: var(--color-card); border: 1px solid var(--color-border) }
.ins-2 { color: var(--color-accent) }
.ins-3 { background-color: var(--color-accent) }
.ins-4 { background-color: var(--color-card-dark); border: 1px solid var(--color-border) }
.ins-5 { color: var(--color-text-secondary) }
.ins-6 { color: var(--color-text-muted) }
.ins-7 { color: var(--color-warning) }
.ins-8 { background-color: var(--color-input-bg-dark) }
.ins-9 { background-color: var(--color-warning); color: white }
.ins-10 { background-color: var(--color-accent); color: white }
.ins-11 { background-color: var(--color-input-bg) }
.ins-12 { color: var(--color-accent-secondary) }
.ins-13 { color: var(--color-success) }
.ins-14 { color: var(--color-danger) }
.ins-15 { 
              background-color: var(--color-card);
              border: 1px solid var(--color-border);
              color: var(--color-text-secondary);
             }

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