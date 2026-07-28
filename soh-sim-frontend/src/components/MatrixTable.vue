<template>
  <div class="flex-1 min-h-0 flex flex-col">
    <div
      class="rounded-xl p-3 flex-shrink-0 mb-3 u-background-color-var-color-bg-secondary-border-1px-solid-var-color-border"
    >
      <div class="grid grid-cols-3 md:grid-cols-6 gap-2 mb-2">
        <div
          class="rounded-lg p-2 text-center u-background-color-var-color-card-border-1px-solid-var-color-border-border-top-2px-solid-var-color-accent"
        >
          <div class="text-[9px] uppercase text-muted">{{ $t('matrixTable.acRteNoAux') }}</div>
          <div class="text-sm font-bold font-mono mt-0.5 text-accent">
            {{ dashboardMetrics.acRteNoAux }}
          </div>
          <div class="text-[8px] text-muted">%</div>
        </div>
        <div
          class="rounded-lg p-2 text-center u-background-color-var-color-card-border-1px-solid-var-color-border-border-top-2px-solid-var-color-success"
        >
          <div class="text-[9px] uppercase text-muted">{{ $t('matrixTable.acRteWithAux') }}</div>
          <div class="text-sm font-bold font-mono mt-0.5 text-success">
            {{ dashboardMetrics.acRteWithAux }}
          </div>
          <div class="text-[8px] text-muted">%</div>
        </div>
        <div
          class="rounded-lg p-2 text-center u-background-color-var-color-card-border-1px-solid-var-color-border-border-top-2px-solid-var-color-accent-secondary"
        >
          <div class="text-[9px] uppercase text-muted">{{ $t('matrixTable.totalCapacity') }}</div>
          <div class="text-sm font-bold font-mono mt-0.5 text-accent-2">
            {{ dashboardMetrics.totalCapacity }}
          </div>
          <div class="text-[8px] text-muted">MWh</div>
        </div>
        <div
          class="rounded-lg p-2 text-center u-background-color-var-color-card-border-1px-solid-var-color-border-border-top-2px-solid-var-color-info"
        >
          <div class="text-[9px] uppercase text-muted">{{ $t('matrixTable.totalPower') }}</div>
          <div class="text-sm font-bold font-mono mt-0.5 u-color-var-color-info">
            {{ dashboardMetrics.totalPower }}
          </div>
          <div class="text-[8px] text-muted">MW</div>
        </div>
        <div
          class="rounded-lg p-2 text-center u-background-color-var-color-card-border-1px-solid-var-color-border-border-top-2px-solid-var-color-warning"
        >
          <div class="text-[9px] uppercase text-muted">{{ $t('matrixTable.annualThroughput') }}</div>
          <div class="text-sm font-bold font-mono mt-0.5 text-warning">
            {{ dashboardMetrics.annualThroughput }}
          </div>
          <div class="text-[8px] text-muted">MWh/yr</div>
        </div>
        <div
          class="rounded-lg p-2 text-center u-background-color-var-color-card-border-1px-solid-var-color-border-border-top-2px-solid-var-color-danger"
        >
          <div class="text-[9px] uppercase text-muted">{{ $t('matrixTable.epRatio') }}</div>
          <div class="text-sm font-bold font-mono mt-0.5 text-danger">
            {{ dashboardMetrics.epRatio }}
          </div>
          <div class="text-[8px] text-muted">h</div>
        </div>
        <div
          v-if="auxPowerMode === 'phase'"
          class="rounded-lg p-2 text-center u-background-color-var-color-card-border-1px-solid-var-color-border-border-top-2px-solid-var-color-info"
        >
          <div class="text-[9px] uppercase text-muted">{{ $t('matrixTable.tDischarge') }}</div>
          <div class="text-sm font-bold font-mono mt-0.5 u-color-var-color-info">
            {{ dashboardMetrics.tDischarge0 }}
          </div>
          <div class="text-[8px] text-muted">Yr0</div>
        </div>
        <div
          v-if="auxPowerMode === 'phase'"
          class="rounded-lg p-2 text-center u-background-color-var-color-card-border-1px-solid-var-color-border-border-top-2px-solid-var-color-info"
        >
          <div class="text-[9px] uppercase text-muted">{{ $t('matrixTable.tCharge') }}</div>
          <div class="text-sm font-bold font-mono mt-0.5 u-color-var-color-info">
            {{ dashboardMetrics.tCharge0 }}
          </div>
          <div class="text-[8px] text-muted">Yr0</div>
        </div>
      </div>
      <div
        v-if="auxPowerMode === 'phase' && dashboardMetrics.acRteFormula"
        class="text-[9px] text-muted mt-1 px-1 font-mono"
      >
        GB/T 36549: AC-RTE = (M - P_dis * t_dis) / (N + E_cycle - P_dis * t_dis) = {{ dashboardMetrics.acRteFormula }}
      </div>
    </div>

    <div class="rounded-xl p-3 flex-shrink-0 mb-3 card">
      <div class="grid grid-cols-3 md:grid-cols-6 gap-3 mb-3">
        <div>
          <label class="label-text">{{ $t('paramPanel.ratedEnergy') }}</label>
          <input
            type="number"
            :value="params.ratedEnergy"
            step="0.1"
            class="form-field-input w-full rounded px-2 py-1 text-xs"
            @input="$emit('update:param', 'ratedEnergy', Number($event.target.value))"
          />
        </div>
        <div>
          <label class="label-text">{{ $t('matrixTable.initContainerCount') }}</label>
          <input
            type="number"
            :value="params.initContainerQty"
            step="1"
            class="form-field-input w-full rounded px-2 py-1 text-xs"
            @input="$emit('update:param', 'initContainerQty', Number($event.target.value))"
          />
        </div>
        <div>
          <label class="label-text">{{ $t('paramPanel.initPcsQty') }}</label>
          <input
            type="number"
            :value="params.initPcsQty"
            step="1"
            class="form-field-input w-full rounded px-2 py-1 text-xs"
            @input="$emit('update:param', 'initPcsQty', Number($event.target.value))"
          />
        </div>
        <div>
          <label class="label-text">{{ $t('paramPanel.duration') }}</label>
          <input
            type="number"
            :value="params.duration"
            step="0.5"
            class="form-field-input w-full rounded px-2 py-1 text-xs"
            @input="$emit('update:param', 'duration', Number($event.target.value))"
          />
        </div>
        <div>
          <label class="label-text">{{ $t('paramPanel.cyclesPerDay') }}</label>
          <input
            type="number"
            :value="params.cyclesPerDay"
            step="1"
            class="form-field-input w-full rounded px-2 py-1 text-xs"
            @input="$emit('update:param', 'cyclesPerDay', Number($event.target.value))"
          />
        </div>
        <div>
          <label class="label-text">{{ $t('paramPanel.acEfficiency') }}</label>
          <input
            type="number"
            :value="params.acEfficiency"
            step="0.01"
            class="form-field-input w-full rounded px-2 py-1 text-xs"
            @input="$emit('update:param', 'acEfficiency', Number($event.target.value))"
          />
        </div>
      </div>
      <div class="flex justify-end">
        <button class="oracle-btn-primary text-sm" :disabled="isCalculating" @click="$emit('recalculate')">
          {{ isCalculating ? $t('matrixTable.calculating') : $t('matrixTable.recalculate') }}
        </button>
      </div>
    </div>

    <div
      class="flex-1 min-h-0 overflow-auto rounded-xl u-border-1px-solid-var-color-border-background-var-color-bg-secondary"
    >
      <table class="w-full text-left border-collapse min-w-[1500px]">
        <thead>
          <tr
            class="text-center border-b text-[10px] font-bold sticky top-0 z-30 u-background-var-color-bg-color-var-color-text-secondary-border-color-var-color-border"
          >
            <th class="py-1.5 u-border-right-1px-solid-var-color-border" colspan="1">
              {{ $t('matrixTable.time') }}
            </th>
            <th class="py-1.5 u-border-right-1px-solid-var-color-border-color-var-color-accent" colspan="8">
              {{ $t('matrixTable.initialStock') }}
            </th>
            <th class="py-1.5 u-border-right-1px-solid-var-color-border-color-var-color-chart-pink" colspan="6">
              {{ $t('matrixTable.augStream') }}
            </th>
            <th class="py-1.5 text-success" :colspan="auxPowerMode === 'phase' ? 5 : 3">
              {{ $t('matrixTable.totalAccounting') }}
            </th>
          </tr>
          <tr
            class="text-[10px] font-semibold text-center border-b sticky top-[31px] z-30 u-background-var-color-bg-color-var-color-text-secondary-border-color-var-color-border"
          >
            <th class="p-1.5 u-border-right-1px-solid-var-color-border-background-var-color-bg">
              {{ $t('matrixTable.year') }}
            </th>
            <th class="p-1.5">
              {{ $t('matrixTable.nominalCapacity') }}
            </th>
            <th class="p-1.5 text-warning">
              {{ $t('matrixTable.dod') }}
            </th>
            <th class="p-1.5 text-accent-2">
              {{ $t('matrixTable.rte') }}
            </th>
            <th class="p-1.5 text-warning">
              {{ $t('matrixTable.soh') }}
            </th>
            <th class="p-1.5">
              {{ $t('matrixTable.initContainerCount') }}
            </th>
            <th class="p-1.5">
              {{ $t('matrixTable.grossDischarge') }}
            </th>
            <th class="p-1.5 text-danger">
              {{ $t('matrixTable.cycleAux') }}
            </th>
            <th class="p-1.5 font-bold u-border-right-1px-solid-var-color-border-color-var-color-accent">
              {{ $t('matrixTable.initNetAc') }}
            </th>
            <th class="p-1.5">
              {{ $t('matrixTable.augNominal') }}
            </th>
            <th class="p-1.5 font-bold u-color-var-color-chart-pink">
              {{ $t('matrixTable.augQty') }}
            </th>
            <th class="p-1.5">
              {{ $t('matrixTable.augAccum') }}
            </th>
            <th class="p-1.5 text-danger">
              {{ $t('matrixTable.augAux') }}
            </th>
            <th class="p-1.5 u-color-var-color-chart-pink">
              {{ $t('matrixTable.augGross') }}
            </th>
            <th class="p-1.5 font-bold u-border-right-1px-solid-var-color-border-color-var-color-chart-pink">
              {{ $t('matrixTable.augNetAc') }}
            </th>
            <th class="p-1.5 font-bold text-success">
              {{ $t('matrixTable.totalNetAc') }}
            </th>
            <th class="p-1.5">
              {{ $t('matrixTable.meetsReq') }}
            </th>
            <th class="p-1.5">
              {{ $t('matrixTable.reqThreshold') }}
            </th>
            <th v-if="auxPowerMode === 'phase'" class="p-1.5 text-info">
              {{ $t('matrixTable.tDischarge') }}
            </th>
            <th v-if="auxPowerMode === 'phase'" class="p-1.5 text-info">
              {{ $t('matrixTable.tCharge') }}
            </th>
          </tr>
        </thead>
        <tbody class="divide-y text-[11px] font-mono border-default">
          <tr
            v-for="i in 26"
            :key="i - 1"
            class="hover:opacity-80 transition-all text-center u-background-var-color-card"
          >
            <td
              class="p-1 font-bold sticky left-0 z-10 u-color-var-color-text-muted-border-right-1px-solid-var-color-border-background-var-color-bg"
            >
              {{ i - 1 }}
            </td>

            <!-- Initial Stock -->
            <td class="p-1 text-secondary">
              {{ params.ratedEnergy != null ? params.ratedEnergy.toFixed(1) : '--' }}
            </td>
            <td class="p-0.5 bg-input">
              <input
                type="number"
                :value="dod[i - 1]"
                step="0.1"
                class="form-field-input w-12 rounded text-center font-mono text-[11px]"
                @input="updateDod(i - 1, $event.target.value)"
              />
            </td>
            <td class="p-0.5 bg-input">
              <input
                type="number"
                :value="rte[i - 1] != null ? (rte[i - 1] * 100).toFixed(2) : ''"
                step="0.01"
                class="form-field-input w-14 rounded text-center font-mono text-[11px]"
                @input="updateRte(i - 1, $event.target.value)"
              />
            </td>
            <td class="p-0.5 bg-input">
              <input
                type="number"
                :value="soh[i - 1] != null ? (soh[i - 1] * 100).toFixed(2) : ''"
                step="0.01"
                class="form-field-input w-14 rounded text-center font-bold font-mono text-[11px]"
                @input="updateSoh(i - 1, $event.target.value)"
              />
            </td>
            <td class="p-1 text-secondary">
              {{ params.initContainerQty }}
            </td>
            <td class="p-1 text-default">
              {{ results.initGross[i - 1]?.toFixed(2) }}
            </td>
            <td class="p-1 font-semibold text-danger">
              {{ results.initAux[i - 1]?.toFixed(2) }}
            </td>
            <td
              class="p-1 font-bold u-border-right-1px-solid-var-color-border-color-var-color-accent-background-var-color-accent-glow"
            >
              {{ results.initAcUsable[i - 1]?.toFixed(2) }}
            </td>

            <!-- Augmentation Stream -->
            <td class="p-1 text-muted">
              {{ params.ratedEnergy != null ? params.ratedEnergy.toFixed(1) : '--' }}
            </td>
            <td class="p-0.5 bg-input">
              <input
                type="number"
                :value="augQty[i - 1]"
                step="1"
                min="0"
                class="form-field-input w-10 rounded text-center font-bold text-[11px]"
                @input="updateAugQty(i - 1, $event.target.value)"
              />
            </td>
            <td class="p-1 text-muted">
              {{ results.augAccumQty[i - 1] }}
            </td>
            <td class="p-1 font-semibold text-danger">
              {{ results.augAux[i - 1]?.toFixed(2) }}
            </td>
            <td class="p-1 text-secondary">
              {{ results.augGross[i - 1]?.toFixed(2) }}
            </td>
            <td
              class="p-1 font-bold u-border-right-1px-solid-var-color-border-color-var-color-chart-pink-background-rgba-236-72-153-0-05"
            >
              {{ results.augAcUsable[i - 1]?.toFixed(2) }}
            </td>

            <!-- Total Accounting -->
            <td class="p-1 font-bold text-xs" :class="results.meetsReq[i - 1] ? 'matrix-pass' : 'matrix-fail'">
              {{ results.totalAcUsable[i - 1]?.toFixed(2) }}
            </td>
            <td
              class="p-1 font-bold"
              :class="results.meetsReq[i - 1] ? 'text-success bg-success-10' : 'text-danger bg-danger-10'"
            >
              {{ results.meetsReq[i - 1] ? $t('matrixTable.meetsYes') : $t('matrixTable.meetsNo') }}
            </td>
            <td class="p-1 font-semibold text-warning">
              {{ params.requiredEnergy != null ? params.requiredEnergy.toFixed(2) : '--' }}
            </td>
            <td v-if="auxPowerMode === 'phase'" class="p-1 text-info">
              {{ results.tDischarge?.[i - 1] != null ? results.tDischarge[i - 1].toFixed(2) : '--' }}
            </td>
            <td v-if="auxPowerMode === 'phase'" class="p-1 text-info">
              {{ results.tCharge?.[i - 1] != null ? results.tCharge[i - 1].toFixed(2) : '--' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { DEFAULT_SURVEY } from '../stores/bess.js'

const props = defineProps({
  params: Object,
  results: Object,
  soh: Array,
  rte: Array,
  dod: Array,
  augQty: Array,
  auxPowerMode: { type: String, default: 'manual' }
})
const emit = defineEmits(['update:soh', 'update:rte', 'update:dod', 'update:augQty', 'update:param', 'recalculate'])

const isCalculating = ref(false)

const dashboardMetrics = computed(() => {
  const p = props.params || {}
  const r = props.rte || []
  const res = props.results || {}
  const ratedEnergy = p.ratedEnergy || 0
  const initContainerQty = p.initContainerQty || 0
  const duration = p.duration || DEFAULT_SURVEY.duration
  const cyclesPerDay = p.cyclesPerDay || 1
  const acEff = (p.acEfficiency || 97) / 100

  const totalCapacity = ratedEnergy * initContainerQty
  const totalPower = totalCapacity / duration
  const rte0 = r[0] || 0.94
  const annualThroughput = totalCapacity * cyclesPerDay * 365 * rte0 * acEff

  const acRteNoAux = res.acRteNoAux != null ? Number(res.acRteNoAux).toFixed(2) : (rte0 * acEff * 100).toFixed(2)
  const initGross0 = res.initGross?.[0] || 0
  const initAux0 = res.initAux?.[0] || 0
  const auxRatio = initGross0 > 0 ? initAux0 / initGross0 : 0.05
  const acRteWithAux =
    res.acRteWithAux != null ? Number(res.acRteWithAux).toFixed(2) : (rte0 * acEff * (1 - auxRatio) * 100).toFixed(2)
  const epRatio = duration.toFixed(1)

  // GB/T 36549 formula breakdown for phase mode
  let acRteFormula = null
  if (res.acRteWithAux != null && res.tDischarge?.[0] != null) {
    const initGross0_val = res.initGross?.[0] || 0
    const initAux0_val = res.initAux?.[0] || 0
    const tDis0 = res.tDischarge[0]
    const pDisSys = initAux0_val > 0 && tDis0 > 0 ? (initAux0_val / tDis0).toFixed(3) : '--'
    const eCycle = initAux0_val > 0 ? initAux0_val.toFixed(2) : '--'
    acRteFormula = `(${initGross0_val.toFixed(1)} - ${pDisSys}*${tDis0.toFixed(2)}) / (${initGross0_val.toFixed(1)} + ${eCycle} - ${pDisSys}*${tDis0.toFixed(2)})`
  }

  return {
    acRteNoAux: acRteNoAux + '%',
    acRteWithAux: acRteWithAux + '%',
    totalCapacity: totalCapacity.toFixed(1),
    totalPower: totalPower.toFixed(1),
    annualThroughput: annualThroughput.toFixed(0),
    epRatio: epRatio + 'h',
    tDischarge0: res.tDischarge?.[0] != null ? res.tDischarge[0].toFixed(2) + 'h' : '--',
    tCharge0: res.tCharge?.[0] != null ? res.tCharge[0].toFixed(2) + 'h' : '--',
    acRteFormula
  }
})

function updateDod(idx, val) {
  const newArr = [...props.dod]
  newArr[idx] = Number(val) || 0
  emit('update:dod', newArr)
}
function updateRte(idx, val) {
  const newArr = [...props.rte]
  newArr[idx] = (Number(val) || 0) / 100
  emit('update:rte', newArr)
}
function updateSoh(idx, val) {
  const newArr = [...props.soh]
  newArr[idx] = (Number(val) || 0) / 100
  emit('update:soh', newArr)
}
function updateAugQty(idx, val) {
  const newArr = [...props.augQty]
  newArr[idx] = parseInt(val) || 0
  emit('update:augQty', newArr)
}
</script>
