<template>
  <div class="flex-1 min-h-0 flex flex-col">
    <div
      class="rounded-xl p-3 flex-shrink-0 mb-3"
      style="background-color: var(--color-bg-secondary); border: 1px solid var(--color-border)"
    >
      <div class="grid grid-cols-3 md:grid-cols-6 gap-2 mb-2">
        <div
          class="rounded-lg p-2 text-center"
          style="
            background-color: var(--color-card);
            border: 1px solid var(--color-border);
            border-top: 2px solid var(--color-accent);
          "
        >
          <div class="text-[9px] uppercase" style="color: var(--color-text-muted)">AC-RTE 不带辅耗</div>
          <div class="text-sm font-bold font-mono mt-0.5" style="color: var(--color-accent)">
            {{ dashboardMetrics.acRteNoAux }}
          </div>
          <div class="text-[8px]" style="color: var(--color-text-muted)">%</div>
        </div>
        <div
          class="rounded-lg p-2 text-center"
          style="
            background-color: var(--color-card);
            border: 1px solid var(--color-border);
            border-top: 2px solid var(--color-success);
          "
        >
          <div class="text-[9px] uppercase" style="color: var(--color-text-muted)">AC-RTE 带辅耗</div>
          <div class="text-sm font-bold font-mono mt-0.5" style="color: var(--color-success)">
            {{ dashboardMetrics.acRteWithAux }}
          </div>
          <div class="text-[8px]" style="color: var(--color-text-muted)">%</div>
        </div>
        <div
          class="rounded-lg p-2 text-center"
          style="
            background-color: var(--color-card);
            border: 1px solid var(--color-border);
            border-top: 2px solid var(--color-accent-secondary);
          "
        >
          <div class="text-[9px] uppercase" style="color: var(--color-text-muted)">总装机容量</div>
          <div class="text-sm font-bold font-mono mt-0.5" style="color: var(--color-accent-secondary)">
            {{ dashboardMetrics.totalCapacity }}
          </div>
          <div class="text-[8px]" style="color: var(--color-text-muted)">MWh</div>
        </div>
        <div
          class="rounded-lg p-2 text-center"
          style="
            background-color: var(--color-card);
            border: 1px solid var(--color-border);
            border-top: 2px solid var(--color-info);
          "
        >
          <div class="text-[9px] uppercase" style="color: var(--color-text-muted)">总装机功率</div>
          <div class="text-sm font-bold font-mono mt-0.5" style="color: var(--color-info)">
            {{ dashboardMetrics.totalPower }}
          </div>
          <div class="text-[8px]" style="color: var(--color-text-muted)">MW</div>
        </div>
        <div
          class="rounded-lg p-2 text-center"
          style="
            background-color: var(--color-card);
            border: 1px solid var(--color-border);
            border-top: 2px solid var(--color-warning);
          "
        >
          <div class="text-[9px] uppercase" style="color: var(--color-text-muted)">年吞吐量</div>
          <div class="text-sm font-bold font-mono mt-0.5" style="color: var(--color-warning)">
            {{ dashboardMetrics.annualThroughput }}
          </div>
          <div class="text-[8px]" style="color: var(--color-text-muted)">MWh/yr</div>
        </div>
        <div
          class="rounded-lg p-2 text-center"
          style="
            background-color: var(--color-card);
            border: 1px solid var(--color-border);
            border-top: 2px solid var(--color-danger);
          "
        >
          <div class="text-[9px] uppercase" style="color: var(--color-text-muted)">E/P 配比</div>
          <div class="text-sm font-bold font-mono mt-0.5" style="color: var(--color-danger)">
            {{ dashboardMetrics.epRatio }}
          </div>
          <div class="text-[8px]" style="color: var(--color-text-muted)">h</div>
        </div>
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
            class="w-full rounded px-2 py-1 text-xs"
            style="
              background-color: var(--color-input-bg-dark);
              border: 1px solid var(--color-input-border);
              color: var(--color-text);
            "
            @input="$emit('update:param', 'ratedEnergy', Number($event.target.value))"
          />
        </div>
        <div>
          <label class="label-text">{{ $t('matrixTable.initContainerCount') }}</label>
          <input
            type="number"
            :value="params.initContainerQty"
            step="1"
            class="w-full rounded px-2 py-1 text-xs"
            style="
              background-color: var(--color-input-bg-dark);
              border: 1px solid var(--color-input-border);
              color: var(--color-text);
            "
            @input="$emit('update:param', 'initContainerQty', Number($event.target.value))"
          />
        </div>
        <div>
          <label class="label-text">{{ $t('paramPanel.initPcsQty') }}</label>
          <input
            type="number"
            :value="params.initPcsQty"
            step="1"
            class="w-full rounded px-2 py-1 text-xs"
            style="
              background-color: var(--color-input-bg-dark);
              border: 1px solid var(--color-input-border);
              color: var(--color-text);
            "
            @input="$emit('update:param', 'initPcsQty', Number($event.target.value))"
          />
        </div>
        <div>
          <label class="label-text">{{ $t('paramPanel.duration') }}</label>
          <input
            type="number"
            :value="params.duration"
            step="0.5"
            class="w-full rounded px-2 py-1 text-xs"
            style="
              background-color: var(--color-input-bg-dark);
              border: 1px solid var(--color-input-border);
              color: var(--color-text);
            "
            @input="$emit('update:param', 'duration', Number($event.target.value))"
          />
        </div>
        <div>
          <label class="label-text">{{ $t('paramPanel.cyclesPerDay') }}</label>
          <input
            type="number"
            :value="params.cyclesPerDay"
            step="1"
            class="w-full rounded px-2 py-1 text-xs"
            style="
              background-color: var(--color-input-bg-dark);
              border: 1px solid var(--color-input-border);
              color: var(--color-text);
            "
            @input="$emit('update:param', 'cyclesPerDay', Number($event.target.value))"
          />
        </div>
        <div>
          <label class="label-text">{{ $t('paramPanel.acEfficiency') }}</label>
          <input
            type="number"
            :value="params.acEfficiency"
            step="0.01"
            class="w-full rounded px-2 py-1 text-xs"
            style="
              background-color: var(--color-input-bg-dark);
              border: 1px solid var(--color-input-border);
              color: var(--color-text);
            "
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
      class="flex-1 min-h-0 overflow-auto rounded-xl"
      style="border: 1px solid var(--color-border); background: var(--color-bg-secondary)"
    >
      <table class="w-full text-left border-collapse min-w-[1500px]">
        <thead>
          <tr
            class="text-center border-b text-[10px] font-bold sticky top-0 z-30"
            style="background: var(--color-bg); color: var(--color-text-secondary); border-color: var(--color-border)"
          >
            <th class="py-1.5" style="border-right: 1px solid var(--color-border)" colspan="1">
              {{ $t('matrixTable.time') }}
            </th>
            <th
              class="py-1.5"
              style="border-right: 1px solid var(--color-border); color: var(--color-accent)"
              colspan="8"
            >
              {{ $t('matrixTable.initialStock') }}
            </th>
            <th class="py-1.5" style="border-right: 1px solid var(--color-border); color: #ec4899" colspan="6">
              {{ $t('matrixTable.augStream') }}
            </th>
            <th class="py-1.5" style="color: var(--color-success)" colspan="3">
              {{ $t('matrixTable.totalAccounting') }}
            </th>
          </tr>
          <tr
            class="text-[10px] font-semibold text-center border-b sticky top-[31px] z-30"
            style="background: var(--color-bg); color: var(--color-text-secondary); border-color: var(--color-border)"
          >
            <th class="p-1.5" style="border-right: 1px solid var(--color-border); background: var(--color-bg)">
              {{ $t('matrixTable.year') }}
            </th>
            <th class="p-1.5">
              {{ $t('matrixTable.nominalCapacity') }}
            </th>
            <th class="p-1.5" style="color: #f59e0b">
              {{ $t('matrixTable.dod') }}
            </th>
            <th class="p-1.5" style="color: var(--color-accent-secondary)">
              {{ $t('matrixTable.rte') }}
            </th>
            <th class="p-1.5" style="color: #eab308">
              {{ $t('matrixTable.soh') }}
            </th>
            <th class="p-1.5">
              {{ $t('matrixTable.initContainerCount') }}
            </th>
            <th class="p-1.5">
              {{ $t('matrixTable.grossDischarge') }}
            </th>
            <th class="p-1.5" style="color: var(--color-danger)">
              {{ $t('matrixTable.cycleAux') }}
            </th>
            <th class="p-1.5 font-bold" style="border-right: 1px solid var(--color-border); color: var(--color-accent)">
              {{ $t('matrixTable.initNetAc') }}
            </th>
            <th class="p-1.5">
              {{ $t('matrixTable.augNominal') }}
            </th>
            <th class="p-1.5 font-bold" style="color: #ec4899">
              {{ $t('matrixTable.augQty') }}
            </th>
            <th class="p-1.5">
              {{ $t('matrixTable.augAccum') }}
            </th>
            <th class="p-1.5" style="color: var(--color-danger)">
              {{ $t('matrixTable.augAux') }}
            </th>
            <th class="p-1.5" style="color: #ec4899">
              {{ $t('matrixTable.augGross') }}
            </th>
            <th class="p-1.5 font-bold" style="border-right: 1px solid var(--color-border); color: #ec4899">
              {{ $t('matrixTable.augNetAc') }}
            </th>
            <th class="p-1.5 font-bold" style="color: var(--color-success)">
              {{ $t('matrixTable.totalNetAc') }}
            </th>
            <th class="p-1.5">
              {{ $t('matrixTable.meetsReq') }}
            </th>
            <th class="p-1.5">
              {{ $t('matrixTable.reqThreshold') }}
            </th>
          </tr>
        </thead>
        <tbody class="divide-y text-[11px] font-mono" style="border-color: var(--color-border)">
          <tr
            v-for="i in 26"
            :key="i - 1"
            class="hover:opacity-80 transition-all text-center"
            style="background: var(--color-card)"
          >
            <td
              class="p-1 font-bold sticky left-0 z-10"
              style="
                color: var(--color-text-muted);
                border-right: 1px solid var(--color-border);
                background: var(--color-bg);
              "
            >
              {{ i - 1 }}
            </td>

            <!-- Initial Stock -->
            <td class="p-1" style="color: var(--color-text-secondary)">
              {{ params.ratedEnergy.toFixed(1) }}
            </td>
            <td class="p-0.5" style="background: var(--color-input-bg)">
              <input
                type="number"
                :value="dod[i - 1]"
                step="0.1"
                class="w-12 rounded text-center font-mono text-[11px]"
                style="background: var(--color-bg); border: 1px solid var(--color-border); color: #f59e0b"
                @input="updateDod(i - 1, $event.target.value)"
              />
            </td>
            <td class="p-0.5" style="background: var(--color-input-bg)">
              <input
                type="number"
                :value="(rte[i - 1] * 100).toFixed(2)"
                step="0.01"
                class="w-14 rounded text-center font-mono text-[11px]"
                style="
                  background: var(--color-bg);
                  border: 1px solid var(--color-border);
                  color: var(--color-accent-secondary);
                "
                @input="updateRte(i - 1, $event.target.value)"
              />
            </td>
            <td class="p-0.5" style="background: var(--color-input-bg)">
              <input
                type="number"
                :value="(soh[i - 1] * 100).toFixed(2)"
                step="0.01"
                class="w-14 rounded text-center font-bold font-mono text-[11px]"
                style="background: var(--color-bg); border: 1px solid var(--color-border); color: #eab308"
                @input="updateSoh(i - 1, $event.target.value)"
              />
            </td>
            <td class="p-1" style="color: var(--color-text-secondary)">
              {{ params.initContainerQty }}
            </td>
            <td class="p-1" style="color: var(--color-text)">
              {{ results.initGross[i - 1]?.toFixed(2) }}
            </td>
            <td class="p-1 font-semibold" style="color: var(--color-danger)">
              {{ results.initAux[i - 1]?.toFixed(2) }}
            </td>
            <td
              class="p-1 font-bold"
              style="
                border-right: 1px solid var(--color-border);
                color: var(--color-accent);
                background: var(--color-accent-glow);
              "
            >
              {{ results.initAcUsable[i - 1]?.toFixed(2) }}
            </td>

            <!-- Augmentation Stream -->
            <td class="p-1" style="color: var(--color-text-muted)">
              {{ params.ratedEnergy.toFixed(1) }}
            </td>
            <td class="p-0.5" style="background: var(--color-input-bg)">
              <input
                type="number"
                :value="augQty[i - 1]"
                step="1"
                min="0"
                class="w-10 rounded text-center font-bold text-[11px]"
                style="background: var(--color-bg); border: 1px solid #be185d; color: #ec4899"
                @input="updateAugQty(i - 1, $event.target.value)"
              />
            </td>
            <td class="p-1" style="color: var(--color-text-muted)">
              {{ results.augAccumQty[i - 1] }}
            </td>
            <td class="p-1 font-semibold" style="color: var(--color-danger)">
              {{ results.augAux[i - 1]?.toFixed(2) }}
            </td>
            <td class="p-1" style="color: var(--color-text-secondary)">
              {{ results.augGross[i - 1]?.toFixed(2) }}
            </td>
            <td
              class="p-1 font-bold"
              style="border-right: 1px solid var(--color-border); color: #ec4899; background: rgba(236, 72, 153, 0.05)"
            >
              {{ results.augAcUsable[i - 1]?.toFixed(2) }}
            </td>

            <!-- Total Accounting -->
            <td
              class="p-1 font-bold text-xs"
              :style="{ color: results.meetsReq[i - 1] ? 'var(--color-accent)' : 'var(--color-danger)' }"
            >
              {{ results.totalAcUsable[i - 1]?.toFixed(2) }}
            </td>
            <td
              class="p-1 font-bold"
              :style="{
                color: results.meetsReq[i - 1] ? 'var(--color-success)' : 'var(--color-danger)',
                background: results.meetsReq[i - 1] ? 'rgba(16,185,129,0.1)' : 'rgba(239,68,68,0.1)'
              }"
            >
              {{ results.meetsReq[i - 1] ? $t('matrixTable.meetsYes') : $t('matrixTable.meetsNo') }}
            </td>
            <td class="p-1 font-semibold" style="color: #f59e0b">
              {{ params.requiredEnergy.toFixed(2) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({ params: Object, results: Object, soh: Array, rte: Array, dod: Array, augQty: Array })
const emit = defineEmits(['update:soh', 'update:rte', 'update:dod', 'update:augQty', 'update:param', 'recalculate'])

const isCalculating = ref(false)

const dashboardMetrics = computed(() => {
  const p = props.params || {}
  const r = props.rte || []
  const res = props.results || {}
  const ratedEnergy = p.ratedEnergy || 0
  const initContainerQty = p.initContainerQty || 0
  const duration = p.duration || 1
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

  return {
    acRteNoAux: acRteNoAux + '%',
    acRteWithAux: acRteWithAux + '%',
    totalCapacity: totalCapacity.toFixed(1),
    totalPower: totalPower.toFixed(1),
    annualThroughput: annualThroughput.toFixed(0),
    epRatio: epRatio + 'h'
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
