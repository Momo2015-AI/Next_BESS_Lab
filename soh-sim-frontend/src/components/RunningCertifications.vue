<template>
  <FormCardSection number="08" :title="$t('runningConditions.section07')" :z-index="1">
    <div class="grid grid-cols-3 gap-3 text-[10px]">
      <div>
        <span class="label-text">{{ $t('runningConditions.certifications.cell') }}</span>
        <div class="rounded p-2 space-y-1.5 ins-6">
          <label
            v-for="(opt, idx) in certOptionsI18n.cell"
            :key="certKeys.cell[idx]"
            class="flex items-center gap-1.5 cursor-pointer ins-3"
          >
            <input v-model="certCell" type="checkbox" :value="certKeys.cell[idx]" class="accent-teal-500" />
            {{ opt }}
          </label>
        </div>
      </div>
      <div>
        <span class="label-text">{{ $t('runningConditions.certifications.system') }}</span>
        <div class="rounded p-2 space-y-1.5 ins-6">
          <label
            v-for="(opt, idx) in certOptionsI18n.system"
            :key="certKeys.system[idx]"
            class="flex items-center gap-1.5 cursor-pointer ins-3"
          >
            <input v-model="certSystem" type="checkbox" :value="certKeys.system[idx]" class="accent-amber-500" />
            {{ opt }}
          </label>
        </div>
      </div>
      <div>
        <span class="label-text">{{ $t('runningConditions.certifications.grid') }}</span>
        <div class="rounded p-2 space-y-1.5 ins-6">
          <label
            v-for="(opt, idx) in certOptionsI18n.grid"
            :key="certKeys.grid[idx]"
            class="flex items-center gap-1.5 cursor-pointer ins-3"
          >
            <input v-model="certGrid" type="checkbox" :value="certKeys.grid[idx]" class="accent-blue-500" />
            {{ opt }}
          </label>
        </div>
      </div>
    </div>
    <div class="mt-2 grid grid-cols-2 gap-3 text-[10px]">
      <div>
        <span class="label-text">{{ $t('runningConditions.certifications.extra') }}</span>
        <div class="rounded p-2 space-y-1.5 ins-6">
          <label
            v-for="(opt, idx) in certOptionsI18n.extra"
            :key="certKeys.extra[idx]"
            class="flex items-center gap-1.5 cursor-pointer ins-3"
          >
            <input v-model="certExtra" type="checkbox" :value="certKeys.extra[idx]" class="accent-purple-500" />
            {{ opt }}
          </label>
        </div>
      </div>
      <div>
        <span class="label-text">{{ $t('runningConditions.certifications.gridCode') }}</span>
        <div class="rounded p-2 space-y-1.5 ins-6">
          <label
            v-for="(opt, idx) in certOptionsI18n.gridCode"
            :key="certKeys.gridCode[idx]"
            class="flex items-center gap-1.5 cursor-pointer ins-3"
          >
            <input v-model="certGridCode" type="checkbox" :value="certKeys.gridCode[idx]" class="accent-emerald-500" />
            {{ opt }}
          </label>
        </div>
      </div>
    </div>
  </FormCardSection>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import FormCardSection from './FormCardSection.vue'

const { t } = useI18n()

const certCell = defineModel('certCell', { type: Array, default: () => [] })
const certSystem = defineModel('certSystem', { type: Array, default: () => [] })
const certGrid = defineModel('certGrid', { type: Array, default: () => [] })
const certExtra = defineModel('certExtra', { type: Array, default: () => [] })
const certGridCode = defineModel('certGridCode', { type: Array, default: () => [] })

const certKeys = {
  cell: ['IEC 62619', 'IEC 62620', 'UL 1642', 'UN 38.3', 'GB/T 36276'],
  system: ['UL 9540', 'UL 9540A', 'UL 1973', 'IEC 62933-5-2', 'NFPA 855', 'IEC 62477-1'],
  grid: ['IEEE 1547', 'IEC 61000-6-2/4', 'UL 1741', 'IEC 62933-4-2', 'IEC 60730'],
  extra: ['ISO 14001', 'ISO 45001', 'ISO 9001', 'CE Marking', 'UKCA', 'RCM'],
  gridCode: ['UK G99', 'VDE-AR-N 4110', 'EN 50549-1', 'IEEE 2800', 'AEMO Grid Code', 'SASO/IEC']
}

const certOptionsI18n = computed(() => ({
  cell: certKeys.cell.map((c) => t(`runningConditions.certificates.${c}`)),
  system: certKeys.system.map((s) => t(`runningConditions.certificates.${s}`)),
  grid: certKeys.grid.map((g) => t(`runningConditions.certificates.${g}`)),
  extra: certKeys.extra.map((e) => t(`runningConditions.certificates.${e}`)),
  gridCode: certKeys.gridCode.map((gc) => t(`runningConditions.certificates.${gc}`))
}))
</script>

<style scoped>
.ins-3 {
  color: var(--color-text-secondary);
}
.ins-6 {
  background: var(--color-input-bg);
}
</style>
