<template>
  <div
    class="border rounded-lg p-3 cursor-pointer transition-all group relative"
    :class="{ 'border-accent bg-accent-glow': selected }"
    @click="$emit('select', item.id)"
  >
    <button
      v-if="deletable"
      class="absolute top-1 right-1 text-xs opacity-0 group-hover:opacity-100 transition-opacity text-muted"
      @click.stop="$emit('delete', item.id)"
    >
      ×
    </button>
    <div class="flex justify-between items-start mb-1">
      <span class="text-xs font-bold">{{ item.model }}</span>
      <span
        class="text-[10px] px-1.5 py-0.5 rounded"
        :class="item.status === 'mass-production' ? 'tag-success' : 'tag-warning'"
      >
        {{ statusText }}
      </span>
    </div>
    <div class="text-[10px] mb-2 text-muted">
      {{ item.mfr }}
    </div>
    <div class="grid grid-cols-2 gap-x-2 gap-y-0.5 text-[10px]">
      <template v-for="field in displayFields" :key="field.key">
        <div class="text-muted">{{ field.label }}</div>
        <div class="text-secondary text-right">{{ formatValue(item, field) }}</div>
      </template>
    </div>
    <div v-if="item.scenario" class="mt-2">
      <span class="text-[9px] px-1.5 py-0.5 rounded tag-glow text-accent">
        {{ item.scenario }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps({
  item: { type: Object, required: true },
  type: { type: String, required: true }, // 'cell' | 'container' | 'pcs' | 'cabinet'
  selected: { type: Boolean, default: false },
  deletable: { type: Boolean, default: true },
  accentColor: { type: String, default: 'var(--color-accent)' },
  accentGlow: { type: String, default: 'var(--color-accent-glow)' }
})

defineEmits(['select', 'delete'])

const statusText = computed(() => {
  if (props.item.status === 'mass-production') return t('productConfig.massProduction')
  if (props.item.status === 'in-development') return t('productConfig.inDevelopment')
  return t('productConfig.preResearch')
})

const FIELD_DEFS = {
  cell: [
    { key: 'capacityAh', label: 'productConfig.capacity' },
    { key: 'voltageNominal', label: 'productConfig.nominalVoltage' },
    { key: 'voltageRange', label: 'productConfig.voltageRange' },
    { key: 'ratedEnergyMWh', label: 'productConfig.energy' },
    { key: 'energyDensity', label: 'productConfig.energyDensity' },
    { key: 'cycleCalendar', label: 'productConfig.cycleCalendar' }
  ],
  container: [
    { key: 'ratedEnergyMWh', label: 'productConfig.energy' },
    { key: 'ratedPowerMW', label: 'productConfig.power' },
    { key: 'cellModel', label: 'productConfig.cellModel' },
    { key: 'cooling', label: 'productConfig.coolingMethod' }
  ],
  pcs: [
    { key: 'ratedPowerMW', label: 'productConfig.power' },
    { key: 'efficiency', label: 'productConfig.efficiency' },
    { key: 'acVoltage', label: 'productConfig.acVoltage' },
    { key: 'cooling', label: 'productConfig.coolingMethod' }
  ]
}

const FORMATTERS = {
  capacityAh: (v) => v + ' Ah',
  ratedEnergyMWh: (v) => v + ' MWh',
  ratedPowerMW: (v) => v + ' MW',
  ratedEnergykWh: (v) => v + ' kWh',
  ratedPowerkW: (v) => v + ' kW',
  voltageNominal: (v) => v + ' V',
  voltageRange: (v, item) =>
    item.voltageMin && item.voltageMax ? item.voltageMin + '~' + item.voltageMax + 'V' : v || '--',
  energyDensity: (v) => (v != null ? v + ' Wh/kg' : '--'),
  cycleCalendar: (v, item) => (item.cycleLife || '--') + '/' + (item.calendarLife || '--') + 'y',
  efficiency: (v) => v + '%',
  cellModel: (v) => v || '--',
  cooling: (v) => v || '--',
  acVoltage: (v) => v || '--'
}

const displayFields = computed(() => FIELD_DEFS[props.type] || [])

function formatValue(item, field) {
  const val = item[field.key]
  const fmt = FORMATTERS[field.key]
  if (fmt) return fmt(val, item)
  return val ?? '--'
}
</script>

<style scoped>
.border-accent {
  border-color: var(--color-accent);
}

.bg-accent-glow {
  background: var(--color-accent-glow);
}
</style>
