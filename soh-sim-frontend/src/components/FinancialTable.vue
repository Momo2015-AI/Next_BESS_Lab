<template>
  <div class="rounded-lg p-3" style="background-color: var(--color-card); border: 1px solid var(--color-border)">
    <div class="flex justify-between items-center mb-2">
      <h3 class="font-bold text-xs" style="color: var(--color-text)">{{ $t('financial.tableCashFlowTitle') }}</h3>
      <button
        class="text-[10px] px-3 py-1 rounded transition-colors"
        style="background-color: var(--color-accent); color: white"
        @click="$emit('recalc')"
      >
        {{ $t('financial.btnRecalculate') }}
      </button>
    </div>
    <div class="overflow-x-auto custom-scrollbar max-h-[300px]">
      <table class="w-full text-[10px] border-collapse">
        <thead>
          <tr class="sticky top-0 z-10" style="background-color: var(--color-card)">
            <th
              class="text-left py-1 px-2 sticky left-0 z-20"
              style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)"
            >
              {{ $t('financial.colYear') }}
            </th>
            <th
              class="text-right py-1 px-2"
              style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)"
            >
              {{ $t('financial.colGeneration') }}
            </th>
            <th
              class="text-right py-1 px-2"
              style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)"
            >
              {{ $t('financial.colArbitrage') }}
            </th>
            <th
              class="text-right py-1 px-2"
              style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)"
            >
              {{ $t('financial.colCapacity') }}
            </th>
            <th
              class="text-right py-1 px-2"
              style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)"
            >
              {{ $t('financial.colAncillary') }}
            </th>
            <th
              class="text-right py-1 px-2"
              style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)"
            >
              {{ $t('financial.colTotalRevenue') }}
            </th>
            <th
              class="text-right py-1 px-2"
              style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)"
            >
              {{ $t('financial.colOpex') }}
            </th>
            <th
              class="text-right py-1 px-2"
              style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)"
            >
              {{ $t('financial.colEbitda') }}
            </th>
            <th
              class="text-right py-1 px-2"
              style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)"
            >
              {{ $t('financial.colNetCashFlow') }}
            </th>
            <th
              class="text-right py-1 px-2"
              style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)"
            >
              {{ $t('financial.colCumCashFlow') }}
            </th>
            <th
              v-if="f.debtRatio > 0"
              class="text-right py-1 px-2"
              style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)"
            >
              {{ $t('financial.colDscr') }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in cashFlowTable" :key="'yr' + row.year" style="border-bottom: 1px solid var(--color-border)">
            <td
              class="py-1 px-2 sticky left-0 font-bold"
              :style="
                row.year === 0
                  ? { backgroundColor: 'var(--color-card)', color: 'var(--color-warning)' }
                  : { backgroundColor: 'var(--color-card)', color: 'var(--color-text-secondary)' }
              "
            >
              {{ row.year === 0 ? $t('financial.labelConstruction') : row.year }}
            </td>
            <td class="text-right py-1 px-2 font-mono" style="color: var(--color-text-secondary)">
              {{ fmtNum(row.energy) }}
            </td>
            <td class="text-right py-1 px-2 font-mono" style="color: var(--color-text-secondary)">
              {{ fmtNum(row.arbitrage) }}
            </td>
            <td class="text-right py-1 px-2 font-mono" style="color: var(--color-text-secondary)">
              {{ fmtNum(row.capacity) }}
            </td>
            <td class="text-right py-1 px-2 font-mono" style="color: var(--color-text-secondary)">
              {{ fmtNum(row.ancillary) }}
            </td>
            <td class="text-right py-1 px-2 font-mono" style="color: var(--color-text-secondary)">
              {{ fmtNum(row.revenue) }}
            </td>
            <td class="text-right py-1 px-2 font-mono" style="color: var(--color-text-secondary)">
              {{ fmtNum(row.opex) }}
            </td>
            <td
              class="text-right py-1 px-2 font-mono"
              :style="row.ebitda < 0 ? { color: 'var(--color-danger)' } : { color: 'var(--color-text-secondary)' }"
            >
              {{ fmtNum(row.ebitda) }}
            </td>
            <td
              class="text-right py-1 px-2 font-mono font-bold"
              :style="row.cashFlow < 0 ? { color: 'var(--color-danger)' } : { color: 'var(--color-success)' }"
            >
              {{ fmtNum(row.cashFlow) }}
            </td>
            <td
              class="text-right py-1 px-2 font-mono"
              :style="row.cumCashFlow < 0 ? { color: 'var(--color-danger)' } : { color: 'var(--color-text-secondary)' }"
            >
              {{ fmtNum(row.cumCashFlow) }}
            </td>
            <td
              v-if="f.debtRatio > 0"
              class="text-right py-1 px-2 font-mono"
              style="color: var(--color-text-secondary)"
            >
              {{ row.dscr ? row.dscr.toFixed(2) : '-' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { inject } from 'vue'

defineProps({ cashFlowTable: { type: Array, required: true } })
defineEmits(['recalc'])

const f = inject('financialParams')

function fmtNum(v) {
  if (v == null || isNaN(v)) return '-'
  if (Math.abs(v) >= 100) return v.toFixed(1)
  return v.toFixed(2)
}
</script>
