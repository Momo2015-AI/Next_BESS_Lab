<template>
  <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-overlay" @click.self="$emit('close')">
    <div class="rounded-xl p-5 w-[480px] max-h-[80vh] overflow-y-auto shadow-2xl card-panel">
      <h3 class="font-bold text-sm mb-4">{{ title }}</h3>
      <div class="space-y-3">
        <!-- Cell fields -->
        <template v-if="type === 'cell'">
          <div class="grid grid-cols-2 gap-2 text-[10px]">
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.vendor') }}</label>
              <input v-model="form.mfr" class="w-full rounded px-2 py-1.5 text-xs form-field-input" />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.model') }}</label>
              <input v-model="form.model" class="w-full rounded px-2 py-1.5 text-xs form-field-input" />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.chemistry') }}</label>
              <input v-model="form.chemistry" class="w-full rounded px-2 py-1.5 text-xs form-field-input" />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.capacityAh') }}</label>
              <input
                v-model.number="form.capacityAh"
                type="number"
                class="w-full rounded px-2 py-1.5 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.nominalVoltageV') }}</label>
              <input
                v-model.number="form.voltageNominal"
                type="number"
                step="0.1"
                class="w-full rounded px-2 py-1.5 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.cycleLife') }}</label>
              <input
                v-model.number="form.cycleLife"
                type="number"
                class="w-full rounded px-2 py-1.5 text-xs form-field-input"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.dimensions') }}</label>
              <input v-model="form.dimensions" class="w-full rounded px-2 py-1.5 text-xs form-field-input" />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.weightKg') }}</label>
              <input v-model="form.weight" class="w-full rounded px-2 py-1.5 text-xs form-field-input" />
            </div>
          </div>
        </template>

        <!-- Container fields -->
        <template v-else-if="type === 'container'">
          <div class="grid grid-cols-2 gap-2 text-[10px]">
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.vendor') }}</label>
              <input v-model="form.mfr" class="w-full rounded px-2 py-1.5 text-xs card-input-dark" />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.model') }}</label>
              <input v-model="form.model" class="w-full rounded px-2 py-1.5 text-xs card-input-dark" />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.capacityAh') }}</label>
              <input
                v-model.number="form.capacityAh"
                type="number"
                class="w-full rounded px-2 py-1.5 text-xs card-input-dark"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.nominalVoltageV') }}</label>
              <input
                v-model.number="form.voltageNominal"
                type="number"
                step="0.1"
                class="w-full rounded px-2 py-1.5 text-xs card-input-dark"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.voltageMaxV') }}</label>
              <input
                v-model.number="form.voltageMax"
                type="number"
                step="0.05"
                class="w-full rounded px-2 py-1.5 text-xs card-input-dark"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.voltageMinV') }}</label>
              <input
                v-model.number="form.voltageMin"
                type="number"
                step="0.05"
                class="w-full rounded px-2 py-1.5 text-xs card-input-dark"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.cycleLife') }}</label>
              <input
                v-model.number="form.cycleLife"
                type="number"
                class="w-full rounded px-2 py-1.5 text-xs card-input-dark"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.calendarLifeY') }}</label>
              <input
                v-model.number="form.calendarLife"
                type="number"
                class="w-full rounded px-2 py-1.5 text-xs card-input-dark"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.dimensions') }}</label>
              <input v-model="form.dimensions" class="w-full rounded px-2 py-1.5 text-xs card-input-dark" />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.weightKg') }}</label>
              <input
                v-model.number="form.weight"
                type="number"
                step="0.01"
                class="w-full rounded px-2 py-1.5 text-xs card-input-dark"
              />
            </div>
          </div>
        </template>

        <!-- PCS fields -->
        <template v-else-if="type === 'pcs'">
          <div class="grid grid-cols-2 gap-2 text-[10px]">
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.vendor') }}</label>
              <input v-model="form.mfr" class="w-full rounded px-2 py-1.5 text-xs card-input-dark" />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.model') }}</label>
              <input v-model="form.model" class="w-full rounded px-2 py-1.5 text-xs card-input-dark" />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.ratedPowerMW') }}</label>
              <input
                v-model.number="form.ratedPowerMW"
                type="number"
                step="0.001"
                class="w-full rounded px-2 py-1.5 text-xs card-input-dark"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.efficiencyPct') }}</label>
              <input
                v-model.number="form.efficiency"
                type="number"
                step="0.1"
                class="w-full rounded px-2 py-1.5 text-xs card-input-dark"
              />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.acVoltage') }}</label>
              <input v-model="form.acVoltage" class="w-full rounded px-2 py-1.5 text-xs card-input-dark" />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.dcRange') }}</label>
              <input v-model="form.dcVoltageRange" class="w-full rounded px-2 py-1.5 text-xs card-input-dark" />
            </div>
            <div>
              <label class="block mb-0.5 text-muted">{{ $t('productConfig.coolingMethod') }}</label>
              <input v-model="form.cooling" class="w-full rounded px-2 py-1.5 text-xs card-input-dark" />
            </div>
          </div>
        </template>

        <!-- Spec upload -->
        <div class="border-t pt-3 border-color-muted">
          <p class="text-[10px] mb-2 text-muted">{{ $t('productConfig.uploadSpec') }}</p>
          <div class="flex gap-2 text-[10px]">
            <input
              ref="specInput"
              type="file"
              accept=".pdf,.csv,.xlsx,.xls"
              class="hidden"
              @change="$emit('spec-upload', $event)"
            />
            <button
              class="px-3 py-1.5 rounded transition-colors bg-card-dark border-color-muted text-secondary"
              @click="$refs.specInput.click()"
            >
              {{ $t('productConfig.uploadSpecBtn') }}
            </button>
            <span v-if="uploading" class="self-center text-accent-secondary">{{ $t('productConfig.parsing') }}</span>
            <span v-if="specResult" class="self-center text-success">{{ specResult }}</span>
          </div>
        </div>
      </div>
      <div class="flex justify-end gap-2 mt-4 pt-3 border-t border-color-muted">
        <button class="text-xs px-3 py-1.5 text-muted" @click="$emit('close')">{{ $t('common.cancel') }}</button>
        <button
          class="text-xs px-4 py-1.5 rounded transition-colors bg-accent-secondary text-white"
          @click="$emit('save', form)"
        >
          {{ $t('common.save') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  show: { type: Boolean, default: false },
  type: { type: String, default: 'cell' },
  title: { type: String, default: '' },
  uploading: { type: Boolean, default: false },
  specResult: { type: String, default: '' }
})

defineEmits(['close', 'save', 'spec-upload'])

const form = reactive({
  mfr: '',
  model: '',
  chemistry: 'LFP',
  capacityAh: '',
  voltageNominal: 3.2,
  voltageMax: '',
  voltageMin: '',
  cycleLife: '',
  calendarLife: 20,
  dimensions: '',
  weight: '',
  status: 'mass-production',
  ratedEnergyMWh: '',
  ratedPowerMW: '',
  cellModel: '',
  cooling: '',
  efficiency: '',
  acVoltage: '',
  dcVoltageRange: ''
})

watch(
  () => props.type,
  (t) => {
    if (t === 'cell') {
      Object.assign(form, {
        mfr: '',
        model: '',
        chemistry: 'LFP',
        capacityAh: '',
        voltageNominal: 3.2,
        voltageMax: '',
        voltageMin: '',
        cycleLife: '',
        calendarLife: 20,
        dimensions: '',
        weight: '',
        status: 'mass-production'
      })
    } else if (t === 'container') {
      Object.assign(form, {
        mfr: '',
        model: '',
        ratedEnergyMWh: '',
        ratedPowerMW: '',
        cellModel: '',
        cooling: '',
        dimensions: '',
        weight: '',
        status: 'mass-production'
      })
    } else {
      Object.assign(form, {
        mfr: '',
        model: '',
        ratedPowerMW: '',
        efficiency: '',
        acVoltage: '',
        dcVoltageRange: '',
        cooling: '',
        status: 'mass-production'
      })
    }
  },
  { immediate: true }
)
</script>
