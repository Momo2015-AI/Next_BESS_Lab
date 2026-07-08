<!-- FinCashFlowTable.vue -->
<template>
  <div class="rounded-lg p-3 card-bordered">
    <div class="flex justify-between items-center mb-2">
      <h3 class="font-bold text-xs text-default">{{ t('financialDashboard.cashFlowTable') }}</h3>
      <button class="text-[10px] px-3 py-1 rounded transition-colors bg-accent text-white" @click="$emit('recalc')">
        {{ t('financialDashboard.recalculate') }}
      </button>
    </div>
    <div class="overflow-x-auto custom-scrollbar max-h-[300px]">
      <table class="w-full text-[10px] border-collapse">
        <thead>
          <tr class="sticky top-0 z-10 table-header-bg">
            <th class="text-left py-1 px-2 sticky left-0 z-20 text-muted border-b">
              {{ t('financialDashboard.year') }}
            </th>
            <th class="text-right py-1 px-2 text-muted border-b">
              {{ t('financialDashboard.generation') }}
            </th>
            <th class="text-right py-1 px-2 text-muted border-b">
              {{ t('financialDashboard.arbitrageIncome') }}
            </th>
            <th class="text-right py-1 px-2 text-muted border-b">
              {{ t('financialDashboard.capacityIncome') }}
            </th>
            <th class="text-right py-1 px-2 text-muted border-b">
              {{ t('financialDashboard.ancillaryIncome') }}
            </th>
            <th class="text-right py-1 px-2 text-muted border-b">
              {{ t('financialDashboard.totalRevenue') }}
            </th>
            <th class="text-right py-1 px-2 text-muted border-b">
              {{ t('financialDashboard.opex') }}
            </th>
            <th class="text-right py-1 px-2 text-muted border-b">
              {{ t('financialDashboard.ebitda') }}
            </th>
            <th class="text-right py-1 px-2 text-muted border-b">
              {{ t('financialDashboard.netCashFlow') }}
            </th>
            <th class="text-right py-1 px-2 text-muted border-b">
              {{ t('financialDashboard.cumCashFlow') }}
            </th>
            <th v-if="f.debtRatio > 0" class="text-right py-1 px-2 text-muted border-b">
              {{ t('financialDashboard.dscr') }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in cashFlowTable" :key="'yr' + row.year" class="border-b">
            <td class="py-1 px-2 sticky left-0 font-bold" :class="row.year === 0 ? 'text-warning' : 'text-secondary'">
              {{ row.year === 0 ? t('financialDashboard.construction') : row.year }}
            </td>
            <td class="text-right py-1 px-2 font-mono text-secondary">
              {{ fmtNum(row.energy) }}
            </td>
            <td class="text-right py-1 px-2 font-mono text-secondary">
              {{ fmtNum(row.arbitrage) }}
            </td>
            <td class="text-right py-1 px-2 font-mono text-secondary">
              {{ fmtNum(row.capacity) }}
            </td>
            <td class="text-right py-1 px-2 font-mono text-secondary">
              {{ fmtNum(row.ancillary) }}
            </td>
            <td class="text-right py-1 px-2 font-mono text-secondary">
              {{ fmtNum(row.revenue) }}
            </td>
            <td class="text-right py-1 px-2 font-mono text-secondary">
              {{ fmtNum(row.opex) }}
            </td>
            <td class="text-right py-1 px-2 font-mono" :class="row.ebitda < 0 ? 'text-danger' : 'text-secondary'">
              {{ fmtNum(row.ebitda) }}
            </td>
            <td
              class="text-right py-1 px-2 font-mono font-bold"
              :class="row.cashFlow < 0 ? 'text-danger' : 'text-success'"
            >
              {{ fmtNum(row.cashFlow) }}
            </td>
            <td class="text-right py-1 px-2 font-mono" :class="row.cumCashFlow < 0 ? 'text-danger' : 'text-secondary'">
              {{ fmtNum(row.cumCashFlow) }}
            </td>
            <td v-if="f.debtRatio > 0" class="text-right py-1 px-2 font-mono text-secondary">
              {{ row.dscr ? row.dscr.toFixed(2) : '-' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const props = defineProps({ model: { type: Object, required: true } })
defineEmits(['recalc'])

const { t } = useI18n()
const { f, cashFlowTable, fmtNum } = props.model
</script>

<style scoped>
.table-header-bg {
  background-color: var(--color-card);
}
</style>
