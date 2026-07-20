<template>
  <FormCardSection number="10" :title="$t('runningConditions.section09')" :z-index="1">
    <p class="label-text mb-3">
      {{ $t('runningConditions.uploadHint') }}
    </p>
    <div
      class="border-2 border-dashed rounded-lg p-6 text-center transition-colors cursor-pointer"
      :class="uploadHover ? 'upload-zone-active' : 'upload-zone-idle'"
      @dragover.prevent="uploadHover = true"
      @dragleave.prevent="uploadHover = false"
      @drop.prevent="onDrop"
      @click="triggerUpload"
    >
      <input
        ref="fileInput"
        type="file"
        accept=".pdf,.doc,.docx,.xls,.xlsx,.csv"
        class="hidden"
        @change="onFileChange"
      />
      <div v-if="uploading" class="ins-5 text-xs">
        <div class="animate-spin w-4 h-4 border-2 border-t-transparent rounded-full mx-auto mb-2 ins-7" />
        {{ $t('runningConditions.uploading') }}
      </div>
      <div v-else-if="uploadResult" class="text-xs">
        <span class="ins-8 font-bold">{{ $t('common.done') }}</span>
        <span class="ins-9 ml-2">{{ uploadResult.fieldsExtracted }} {{ $t('runningConditions.uploadDone') }}</span>
        <button class="ml-3 underline text-xs ins-5" @click.stop="applyExtracted">
          {{ $t('runningConditions.applyForm') }}
        </button>
        <button class="ml-3 underline text-xs ins-9" @click.stop="uploadResult = null">
          {{ $t('runningConditions.clearForm') }}
        </button>
      </div>
      <div v-else>
        <div class="text-2xl mb-1 opacity-40">📄</div>
        <p class="text-xs ins-3">
          {{ $t('runningConditions.dragDrop') }}
          <span class="ins-5 underline">
            {{ $t('runningConditions.clickSelect') }}
          </span>
        </p>
        <p class="text-[10px] mt-1 ins-9">
          {{ $t('runningConditions.uploadSupport') }}
        </p>
      </div>
    </div>
  </FormCardSection>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import FormCardSection from './FormCardSection.vue'

const { t } = useI18n()

const form = defineModel('form', { type: Object, required: true })

const fileInput = ref(null)
const uploadHover = ref(false)
const uploading = ref(false)
const uploadResult = ref(null)

function triggerUpload() {
  fileInput.value?.click()
}

function onFileChange(e) {
  const file = e.target.files?.[0]
  if (file) parseFile(file)
}

function onDrop(e) {
  uploadHover.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file) parseFile(file)
}

async function parseFile(file) {
  uploading.value = true
  uploadResult.value = null
  try {
    const formData = new FormData()
    formData.append('file', file)
    const resp = await fetch('/api/upload/extract', { method: 'POST', body: formData })
    const contentType = resp.headers.get('content-type') || ''
    if (!contentType.includes('application/json')) {
      throw new Error(t('runningConditions.parseUnavailable'))
    }
    const data = await resp.json()
    if (data.extracted) {
      uploadResult.value = { extracted: data.extracted, fieldsExtracted: Object.keys(data.extracted).length }
    } else {
      uploadResult.value = {
        extracted: {},
        fieldsExtracted: 0,
        error: data.error || t('runningConditions.extractFailed')
      }
    }
  } catch {
    uploadResult.value = { extracted: {}, fieldsExtracted: 0, error: t('runningConditions.parseUnavailable') }
  }
  uploading.value = false
}

function applyExtracted() {
  if (!uploadResult.value?.extracted) return
  const ext = uploadResult.value.extracted
  const mapping = {
    project_name: 'projectName',
    project_type: 'projectType',
    country: 'country',
    city: 'city',
    site: 'site',
    total_mw: 'totalMW',
    total_mwh: 'totalMWh',
    duration_h: 'durationHours',
    cycles_per_day: 'cyclesPerDay',
    altitude_m: 'altitude',
    temp_max_c: 'tempMax',
    temp_min_c: 'tempMin',
    temp_avg_c: 'tempAvg',
    humidity_pct: 'humidity',
    seismic_zone: 'seismicZone',
    corrosion_class: 'corrosionClass',
    installation_type: 'installationType',
    grid_voltage_kv: 'gridVoltage',
    grid_freq_hz: 'gridFreq',
    sc_capacity_mva: 'scCapacity',
    neutral_grounding: 'neutralGrounding',
    dc_voltage_range: 'dcVoltageRange',
    ac_voltage_v: 'acVoltage',
    pf_range: 'pfRange',
    thdi_pct: 'thdiLimit',
    rte_target_pct: 'rteTarget',
    availability_target_pct: 'availabilityTarget',
    soh_year1_pct: 'sohYear1',
    soh_year25_pct: 'sohYear25',
    calendar_life_y: 'calendarLife',
    cycle_life: 'cycleLife',
    aux_consumption_pct: 'auxConsumption',
    response_time_ms: 'responseTime'
  }
  for (const [k, v] of Object.entries(ext)) {
    const target = mapping[k]
    if (target && v !== null && v !== undefined) {
      const f = form.value[target]
      if (typeof f === 'number' || f === null) form.value[target] = Number(v)
      else form.value[target] = String(v)
    }
  }
}

defineExpose({
  reset() {
    uploadResult.value = null
  }
})
</script>

<style scoped>
.ins-3 {
  color: var(--color-text-secondary);
}
.ins-5 {
  color: var(--color-accent);
}
.ins-7 {
  border-color: var(--color-accent);
  border-top-color: transparent;
}
.ins-8 {
  color: var(--color-success);
}
.ins-9 {
  color: var(--color-text-muted);
}

.upload-zone-active {
  border-color: var(--color-accent);
  background: var(--color-accent-glow);
}

.upload-zone-idle {
  border-color: var(--color-input-border);
}
</style>
