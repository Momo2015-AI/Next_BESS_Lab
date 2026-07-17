<template>
  <div>
    <div class="flex justify-between items-center mb-3">
      <h3 class="text-sm font-bold flex items-center gap-2 text-accent">
        <span class="w-2 h-2 rounded-full bg-accent" />
        {{ $t('simLab.titleResults') }}
      </h3>
      <button class="text-xs px-3 py-1.5 rounded transition-all flex items-center gap-1 bg-info" @click="$emit('save')">
        <span>💾</span>
        {{ $t('simLab.btnSaveResult') }}
      </button>
    </div>

    <div class="grid grid-cols-4 gap-3 mb-4">
      <div class="rounded p-3 text-center card-panel-bordered">
        <p class="text-[10px] text-muted">{{ $t('simLab.labelInitSoh') }}</p>
        <p class="text-lg font-bold text-accent">{{ results.initSoh?.toFixed(2) || '--' }}%</p>
      </div>
      <div class="rounded p-3 text-center card-panel-bordered">
        <p class="text-[10px] text-muted">{{ $t('simLab.labelGuaranteeEndSoh') }}</p>
        <p class="text-lg font-bold" :class="results.guaranteeEndSoh >= guaranteeSoh ? 'text-success' : 'text-danger'">
          {{ results.guaranteeEndSoh?.toFixed(2) || '--' }}%
        </p>
      </div>
      <div class="rounded p-3 text-center card-panel-bordered">
        <p class="text-[10px] text-muted">{{ $t('simLab.labelFinalSoh') }}</p>
        <p class="text-lg font-bold text-accent-secondary">{{ results.finalSoh?.toFixed(2) || '--' }}%</p>
      </div>
      <div class="rounded p-3 text-center card-panel-bordered">
        <p class="text-[10px] text-muted">{{ $t('simLab.labelGuaranteeCheck') }}</p>
        <p class="text-lg font-bold" :class="results.meetsGuarantee ? 'text-success' : 'text-danger'">
          {{ results.meetsGuarantee ? $t('simLab.pass') : $t('simLab.fail') }}
        </p>
      </div>
    </div>

    <SohRteChart
      ref="chartComp"
      :soh-curve="results.sohCurve"
      :rte-curve="results.rteCurve"
      :guarantee-soh="guaranteeSoh"
    />

    <div class="mt-3 rounded p-3 overflow-auto max-h-32 card-panel-bordered">
      <table class="w-full text-[10px]">
        <thead>
          <tr class="text-muted">
            <th class="py-1 px-2 text-left">{{ $t('simLab.colYear') }}</th>
            <th class="py-1 px-2 text-left">{{ $t('simLab.colSoh') }}</th>
            <th class="py-1 px-2 text-left">{{ $t('simLab.colRte') }}</th>
            <th class="py-1 px-2 text-left">{{ $t('simLab.colNetAvail') }}</th>
            <th class="py-1 px-2 text-left">{{ $t('simLab.colGuaranteeLine') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(row, idx) in results.tableData"
            :key="idx"
            :class="['border-t', { 'bg-danger-10': !row.meetsReq }]"
          >
            <td class="py-1 px-2 text-secondary">{{ row.year }}</td>
            <td class="py-1 px-2 text-accent">{{ row.soh != null ? row.soh.toFixed(2) : '--' }}</td>
            <td class="py-1 px-2 text-accent-secondary">{{ row.rte != null ? row.rte.toFixed(2) : '--' }}</td>
            <td class="py-1 px-2 text-success">{{ row.netAvail != null ? row.netAvail.toFixed(1) : '--' }}</td>
            <td class="py-1 px-2" :class="row.meetsReq ? 'sim-row-pass' : 'sim-row-fail'">
              {{ row.meetsReq ? $t('simLab.pass') : $t('simLab.fail') }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="mt-4 flex justify-between">
      <button class="text-xs px-4 py-2 rounded transition-all theme-btn-secondary" @click="$emit('re-simulate')">
        {{ $t('simLab.btnReSimulate') }}
      </button>
      <button class="text-xs px-4 py-2 rounded transition-all btn-accent-filled" @click="$emit('export')">
        {{ $t('simLab.btnExport') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import SohRteChart from './SohRteChart.vue'

defineProps({
  results: { type: Object, required: true },
  guaranteeSoh: { type: Number, default: 70 }
})

defineEmits(['save', 're-simulate', 'export'])

const chartComp = ref(null)
defineExpose({ chartComp })
</script>
