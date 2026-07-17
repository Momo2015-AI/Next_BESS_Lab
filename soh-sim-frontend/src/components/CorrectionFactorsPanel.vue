<template>
  <div>
    <h3 class="text-sm font-bold mb-3 flex items-center gap-2 text-accent">
      <span class="w-2 h-2 rounded-full bg-accent" />
      {{ $t('simLab.titleCorrection') }}
    </h3>

    <div class="grid grid-cols-2 gap-4">
      <div class="rounded p-3 card-panel-bordered">
        <h4 class="text-xs mb-2 font-medium">{{ $t('simLab.sectionGlobalCorrection') }}</h4>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelSohFactor') }}</label>
            <input
              :value="factors.sohFactor"
              type="number"
              step="0.01"
              min="0.9"
              max="1.1"
              class="w-full rounded px-2 py-1 text-xs card-input"
              @input="$emit('update:sohFactor', Number($event.target.value))"
            />
            <p class="text-[10px] mt-1 text-muted">{{ $t('simLab.rangeDefault1') }}</p>
          </div>
          <div>
            <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelRteFactor') }}</label>
            <input
              :value="factors.rteFactor"
              type="number"
              step="0.01"
              min="0.9"
              max="1.1"
              class="w-full rounded px-2 py-1 text-xs card-input"
              @input="$emit('update:rteFactor', Number($event.target.value))"
            />
            <p class="text-[10px] mt-1 text-muted">{{ $t('simLab.rangeDefault1') }}</p>
          </div>
          <div>
            <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelCapacityFactor') }}</label>
            <input
              :value="factors.capacityFactor"
              type="number"
              step="0.01"
              min="0.9"
              max="1.1"
              class="w-full rounded px-2 py-1 text-xs card-input"
              @input="$emit('update:capacityFactor', Number($event.target.value))"
            />
            <p class="text-[10px] mt-1 text-muted">{{ $t('simLab.rangeDefault1') }}</p>
          </div>
          <div>
            <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelAgingFactor') }}</label>
            <input
              :value="factors.agingFactor"
              type="number"
              step="0.01"
              min="1.0"
              max="1.5"
              class="w-full rounded px-2 py-1 text-xs card-input"
              @input="$emit('update:agingFactor', Number($event.target.value))"
            />
            <p class="text-[10px] mt-1 text-muted">{{ $t('simLab.rangeDefault1_5') }}</p>
          </div>
        </div>
      </div>

      <div class="rounded p-3 card-panel-bordered">
        <h4 class="text-xs mb-2 font-medium">{{ $t('simLab.annualCorrection') }}</h4>
        <div class="overflow-auto max-h-40">
          <table class="w-full text-[10px]">
            <thead>
              <tr class="text-muted">
                <th class="py-1 px-2 text-left">{{ $t('simLab.colYear') }}</th>
                <th class="py-1 px-2 text-left">{{ $t('simLab.colSohCorrection') }}</th>
                <th class="py-1 px-2 text-left">{{ $t('simLab.colRteCorrection') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, idx) in yearlyData" :key="idx" class="border-t">
                <td class="py-1 px-2 text-secondary">{{ row.year }}</td>
                <td class="py-1 px-2">
                  <input
                    :value="row.sohCorrection"
                    type="number"
                    step="0.001"
                    class="w-16 rounded px-1 py-0.5 text-xs card-input"
                    @input="$emit('update:yearly', { idx, field: 'sohCorrection', value: Number($event.target.value) })"
                  />
                </td>
                <td class="py-1 px-2">
                  <input
                    :value="row.rteCorrection"
                    type="number"
                    step="0.001"
                    class="w-16 rounded px-1 py-0.5 text-xs card-input"
                    @input="$emit('update:yearly', { idx, field: 'rteCorrection', value: Number($event.target.value) })"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="mt-3 rounded p-2 card-panel-bordered">
      <p class="text-secondary">
        <strong>{{ $t('simLab.correctionNotes') }}</strong>
      </p>
      <ul class="list-disc list-inside mt-1 space-y-0.5 text-secondary">
        <li>{{ $t('simLab.correctionNoteFactorGt') }}</li>
        <li>{{ $t('simLab.correctionNoteFactorLt') }}</li>
        <li>{{ $t('simLab.correctionNoteAnnual') }}</li>
        <li>{{ $t('simLab.correctionNoteApplied') }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
defineProps({
  factors: { type: Object, required: true },
  yearlyData: { type: Array, default: () => [] }
})

defineEmits(['update:sohFactor', 'update:rteFactor', 'update:capacityFactor', 'update:agingFactor', 'update:yearly'])
</script>
