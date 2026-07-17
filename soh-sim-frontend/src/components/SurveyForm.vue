<template>
  <div class="h-full overflow-y-auto custom-scrollbar">
    <div class="max-w-5xl mx-auto space-y-4 py-2">
      <!-- 01: 基本信息 -->
      <FormCardSection :number="'01'" :title="$t('surveyForm.section01')" :z-index="1">
        <div class="grid grid-cols-4 gap-3">
          <div class="col-span-2">
            <label class="label-text">{{ $t('surveyForm.projectName') }} *</label>
            <input v-model="form.project_name" class="form-field-input" :placeholder="$t('surveyForm.projectNamePh')" />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.country') }}</label>
            <ComboboxInput
              v-model="countryInput"
              :options="countryOptions"
              :placeholder="$t('surveyForm.countryPh')"
              :empty-text="$t('common.noMatch')"
              @select="onCountrySelect"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.city') }}</label>
            <input v-model="form.city" class="form-field-input" :placeholder="$t('surveyForm.cityPh')" />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.site') }}</label>
            <input v-model="form.site" class="form-field-input" :placeholder="$t('surveyForm.sitePh')" />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.lat') }}</label>
            <input
              v-model.number="form.lat"
              type="number"
              step="0.0001"
              class="form-field-input"
              :placeholder="$t('surveyForm.latPh')"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.lng') }}</label>
            <input
              v-model.number="form.lng"
              type="number"
              step="0.0001"
              class="form-field-input"
              :placeholder="$t('surveyForm.lngPh')"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.contactPerson') }}</label>
            <input
              v-model="form.contact_person"
              class="form-field-input"
              :placeholder="$t('surveyForm.contactPersonPh')"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.contactPhone') }}</label>
            <input
              v-model="form.contact_phone"
              class="form-field-input"
              :placeholder="$t('surveyForm.contactPhonePh')"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.contactEmail') }}</label>
            <input
              v-model="form.contact_email"
              class="form-field-input"
              :placeholder="$t('surveyForm.contactEmailPh')"
            />
          </div>
        </div>
      </FormCardSection>

      <!-- 02: 项目规模 -->
      <FormCardSection :number="'02'" :title="$t('surveyForm.section02')">
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="label-text">{{ $t('surveyForm.totalPower') }}</label>
            <input
              v-model.number="form.total_mw"
              type="number"
              step="0.1"
              min="0"
              class="form-field-input"
              :placeholder="$t('surveyForm.totalPowerPh')"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.totalEnergy') }}</label>
            <input
              v-model.number="form.total_mwh"
              type="number"
              step="0.1"
              min="0"
              class="form-field-input"
              :placeholder="$t('surveyForm.totalEnergyPh')"
            />
          </div>
          <div>
            <label class="label-text">
              {{ $t('surveyForm.durationH') }}
              <span v-if="isDurationAuto" class="auto-badge">{{ $t('design.auto') }}</span>
            </label>
            <div class="duration-input-row">
              <input
                v-model.number="form.duration"
                type="number"
                step="0.5"
                min="0.5"
                max="8"
                class="form-field-input"
                :disabled="isDurationAuto"
                :placeholder="$t('surveyForm.durationHPh')"
              />
              <button
                type="button"
                class="lock-toggle-btn"
                :title="isDurationAuto ? $t('design.unlock') : $t('design.lock')"
                @click="isDurationAuto = !isDurationAuto"
              >
                {{ isDurationAuto ? '🔒' : '🔓' }}
              </button>
            </div>
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.cyclesPerDay') }}</label>
            <input
              v-model.number="form.cycles_per_day"
              type="number"
              step="0.5"
              min="0.5"
              max="4"
              class="form-field-input"
              :placeholder="$t('surveyForm.cyclesPerDayPh')"
            />
          </div>
        </div>
      </FormCardSection>

      <!-- 03: 环境条件 -->
      <FormCardSection :number="'03'" :title="$t('surveyForm.section03')">
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="label-text">{{ $t('surveyForm.altitude') }}</label>
            <input
              v-model.number="form.altitude"
              type="number"
              min="0"
              class="form-field-input"
              :placeholder="$t('surveyForm.altitudePh')"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.tempMax') }}</label>
            <input
              v-model.number="form.temp_max"
              type="number"
              class="form-field-input"
              :placeholder="$t('surveyForm.tempMaxPh')"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.tempMin') }}</label>
            <input
              v-model.number="form.temp_min"
              type="number"
              class="form-field-input"
              :placeholder="$t('surveyForm.tempMinPh')"
            />
          </div>
          <div>
            <label class="label-text">
              {{ $t('surveyForm.tempAvg') }}
              <span v-if="isTempAvgAuto" class="auto-badge">{{ $t('design.auto') }}</span>
            </label>
            <div class="duration-input-row">
              <input
                v-model.number="form.temp_avg"
                type="number"
                class="form-field-input"
                :disabled="isTempAvgAuto"
                :placeholder="$t('surveyForm.tempAvgPh')"
              />
              <button
                type="button"
                class="lock-toggle-btn"
                :title="isTempAvgAuto ? $t('design.unlock') : $t('design.lock')"
                @click="isTempAvgAuto = !isTempAvgAuto"
              >
                {{ isTempAvgAuto ? '🔒' : '🔓' }}
              </button>
            </div>
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.humidity') }}</label>
            <input
              v-model.number="form.humidity"
              type="number"
              min="0"
              max="100"
              class="form-field-input"
              :placeholder="$t('surveyForm.humidityPh')"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.sandProtection') }}</label>
            <select v-model="form.sand_protection" class="form-field-select">
              <option value="">{{ $t('common.select') }}</option>
              <option value="IP54">IP54</option>
              <option value="IP55">IP55</option>
              <option value="IP65">IP65</option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.humidityCycle') }}</label>
            <select v-model="form.humidity_cycle" class="form-field-select">
              <option value="">{{ $t('common.select') }}</option>
              <option value="low">{{ $t('common.humidityCycle.low') }}</option>
              <option value="medium">{{ $t('common.humidityCycle.medium') }}</option>
              <option value="high">{{ $t('common.humidityCycle.high') }}</option>
            </select>
          </div>
        </div>
      </FormCardSection>

      <!-- 04: 电网参数 -->
      <FormCardSection :number="'04'" :title="$t('surveyForm.section04')">
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="label-text">{{ $t('surveyForm.gridVoltage') }}</label>
            <input
              v-model.number="form.grid_voltage"
              type="number"
              step="0.1"
              class="form-field-input"
              :placeholder="$t('surveyForm.gridVoltagePh')"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.gridFrequency') }}</label>
            <input
              v-model.number="form.grid_frequency"
              type="number"
              step="0.1"
              class="form-field-input"
              :placeholder="$t('surveyForm.gridFrequencyPh')"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.pccVoltage') }}</label>
            <input
              v-model.number="form.pcc_voltage"
              type="number"
              step="0.1"
              class="form-field-input"
              :placeholder="$t('surveyForm.pccVoltagePh')"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.pccShortCircuit') }}</label>
            <input
              v-model.number="form.pcc_short_circuit_mva"
              type="number"
              step="1"
              class="form-field-input"
              :placeholder="$t('surveyForm.pccShortCircuitPh')"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.gridCode') }}</label>
            <select v-model="form.grid_code" class="form-field-select">
              <option value="">{{ $t('common.select') }}</option>
              <option value="SEC">SEC</option>
              <option value="ESMA">ESMA</option>
              <option value="GSO">GSO</option>
              <option value="IEC">IEC</option>
              <option value="other">{{ $t('common.other') }}</option>
            </select>
          </div>
        </div>
      </FormCardSection>

      <!-- 05: 性能要求 -->
      <FormCardSection :number="'05'" :title="$t('surveyForm.section05')" :z-index="1">
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="label-text">{{ $t('surveyForm.cellModel') }}</label>
            <ComboboxInput
              v-model="cellModelInput"
              :options="cellOptions"
              :placeholder="$t('surveyForm.cellModelPh')"
              :empty-text="$t('common.noMatch')"
              @select="onCellSelect"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.rteTarget') }}</label>
            <input
              v-model.number="form.rte_target"
              type="number"
              min="0"
              max="100"
              class="form-field-input"
              :placeholder="$t('surveyForm.rteTargetPh')"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.sohYear1') }}</label>
            <input
              v-model.number="form.soh_year1"
              type="number"
              min="0"
              max="100"
              class="form-field-input"
              :placeholder="$t('surveyForm.sohYear1Ph')"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.sohYear25') }}</label>
            <input
              v-model.number="form.soh_year25"
              type="number"
              min="0"
              max="100"
              class="form-field-input"
              :placeholder="$t('surveyForm.sohYear25Ph')"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.calendarLife') }}</label>
            <input
              v-model.number="form.calendar_life"
              type="number"
              min="1"
              max="30"
              class="form-field-input"
              :placeholder="$t('surveyForm.calendarLifePh')"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.cycleLife') }}</label>
            <input
              v-model.number="form.cycle_life"
              type="number"
              min="0"
              class="form-field-input"
              :placeholder="$t('surveyForm.cycleLifePh')"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.availabilityTarget') }}</label>
            <input
              v-model.number="form.availability_target"
              type="number"
              min="0"
              max="100"
              class="form-field-input"
              :placeholder="$t('surveyForm.availabilityTargetPh')"
            />
          </div>
        </div>
      </FormCardSection>

      <!-- 06: 其他参数 -->
      <FormCardSection :number="'06'" :title="$t('surveyForm.section06')">
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="label-text">{{ $t('surveyForm.auxConsumption') }}</label>
            <input
              v-model.number="form.aux_consumption"
              type="number"
              step="0.1"
              min="0"
              class="form-field-input"
              :placeholder="$t('surveyForm.auxConsumptionPh')"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.responseTime') }}</label>
            <input
              v-model.number="form.response_time"
              type="number"
              min="0"
              class="form-field-input"
              :placeholder="$t('surveyForm.responseTimePh')"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.dcVoltageRange') }}</label>
            <input
              v-model="form.dc_voltage_range"
              class="form-field-input"
              :placeholder="$t('surveyForm.dcVoltageRangePh')"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.acVoltage') }}</label>
            <input
              v-model.number="form.ac_voltage"
              type="number"
              class="form-field-input"
              :placeholder="$t('surveyForm.acVoltagePh')"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.thdi') }}</label>
            <input
              v-model.number="form.thdi"
              type="number"
              step="0.1"
              min="0"
              max="100"
              class="form-field-input"
              :placeholder="$t('surveyForm.thdiPh')"
            />
          </div>
        </div>
      </FormCardSection>

      <!-- 07: 备注信息 -->
      <FormCardSection :number="'07'" :title="$t('surveyForm.section07')">
        <div>
          <label class="label-text">{{ $t('surveyForm.remarks') }}</label>
          <textarea
            v-model="form.remarks"
            rows="4"
            class="form-field-textarea"
            :placeholder="$t('surveyForm.remarksPh')"
          />
        </div>
      </FormCardSection>

      <!-- 操作按钮 -->
      <div class="flex justify-end gap-3 pt-2">
        <button type="button" class="btn-secondary" @click="resetForm">{{ $t('surveyForm.reset') }}</button>
        <button type="button" class="btn-secondary" @click="fillTestData">{{ $t('surveyForm.fillTestData') }}</button>
        <button type="button" class="btn-primary" :disabled="submitting" @click="submitForm">
          {{ submitting ? $t('surveyForm.submitting') : $t('surveyForm.submit') }}
        </button>
      </div>

      <!-- 提交成功弹窗 -->
      <div v-if="showSuccess" class="fixed inset-0 z-50 flex items-center justify-center u-background-rgba-0-0-0-0-5">
        <div class="card p-8 text-center max-w-sm w-11/12">
          <div
            class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center text-3xl font-bold u-background-var-color-success-color-fff"
          >
            &#10003;
          </div>
          <h3 class="text-xl font-semibold mb-2 text-default">{{ $t('surveyForm.successTitle') }}</h3>
          <p class="mb-4 text-secondary">{{ $t('surveyForm.successDesc') }}</p>
          <div class="p-4 rounded-lg mb-5 text-left u-background-var-color-card-dark">
            <p class="text-sm mb-1 text-default">
              <strong>{{ $t('surveyForm.surveyId') }}:</strong>
              {{ submittedData.data?.survey_id }}
            </p>
            <p class="text-sm text-default">
              <strong>{{ $t('surveyForm.projectCode') }}:</strong>
              {{ submittedData.data?.project_code }}
            </p>
          </div>
          <button class="btn-primary w-full" @click="closeSuccess">{{ $t('surveyForm.confirm') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useProducts } from '../composables/useProducts'
import { useBessStore } from '../stores/bess.js'
import { useDraft } from '../composables/useDraft'
import { useCountryList } from '../composables/useCountryList'
import api from '../services/api.js'
import FormCardSection from './FormCardSection.vue'
import ComboboxInput from './ComboboxInput.vue'

const { t } = useI18n()
const emit = defineEmits(['error'])
const store = useBessStore()
const { cells, loadAll } = useProducts()
const { filterCountries } = useCountryList()

const surveyDefaults = {
  project_name: store.survey.projectName || '',
  contact_person: '',
  contact_phone: '',
  contact_email: '',
  country: store.survey.country || '',
  city: store.survey.city || '',
  site: store.survey.site || '',
  lat: store.survey.lat || null,
  lng: store.survey.lng || null,
  altitude: store.survey.altitude || null,
  total_mw: store.survey.totalPower || null,
  total_mwh: store.survey.ratedEnergy || null,
  duration: store.survey.duration || null,
  cycles_per_day: store.survey.cyclesPerDay || 1,
  temp_max: null,
  temp_min: null,
  temp_avg: store.survey.temperature || null,
  humidity: null,
  grid_voltage: store.survey.gridVoltage || null,
  pcc_voltage: null,
  pcc_short_circuit_mva: null,
  grid_code: '',
  sand_protection: '',
  humidity_cycle: '',
  grid_frequency: null,
  cell_model: '',
  rte_target: null,
  soh_year1: null,
  soh_year25: null,
  calendar_life: null,
  cycle_life: null,
  availability_target: null,
  aux_consumption: null,
  response_time: null,
  dc_voltage_range: '',
  ac_voltage: null,
  thdi: null,
  remarks: ''
}

const { state: form, clearDraft } = useDraft('survey-form', surveyDefaults)

// Country combobox via ComboboxInput
const countryInput = ref(form.country || '')
const countryOptions = computed(() => filterCountries(countryInput.value).map((c) => ({ label: c, value: c })))
function onCountrySelect(opt) {
  form.country = opt.label
}
watch(
  () => form.country,
  (val) => {
    if (val && val !== countryInput.value) countryInput.value = val
  }
)

// Cell model combobox via ComboboxInput
const cellModelInput = ref('')
const cellOptions = computed(() =>
  cells.value.map((c) => ({ label: `${c.mfr} - ${c.model}`, value: c.model, sub: `${c.capacityAh}Ah` }))
)
function onCellSelect(opt) {
  form.cell_model = opt.value
  cellModelInput.value = `${opt.label} (${opt.sub})`
}
watch(
  () => form.cell_model,
  (val) => {
    if (val && cells.value.length > 0) {
      const found = cells.value.find((c) => c.model === val)
      if (found) cellModelInput.value = `${found.mfr} - ${found.model} (${found.capacityAh}Ah)`
    }
  }
)
watch(cells, (list) => {
  if (list.length > 0 && form.cell_model) {
    const found = list.find((c) => c.model === form.cell_model)
    if (found) cellModelInput.value = `${found.mfr} - ${found.model} (${found.capacityAh}Ah)`
  }
})

const isDurationAuto = ref(true)
const isTempAvgAuto = ref(true)

function autoCalcDuration() {
  if (
    form.total_mwh > 0 &&
    form.total_mw > 0 &&
    typeof form.total_mwh === 'number' &&
    typeof form.total_mw === 'number'
  ) {
    form.duration = +(form.total_mwh / form.total_mw).toFixed(2)
  }
}
watch(
  () => [form.total_mwh, form.total_mw],
  () => {
    if (isDurationAuto.value) autoCalcDuration()
  }
)

function autoCalcTempAvg() {
  if (
    form.temp_max != null &&
    form.temp_min != null &&
    typeof form.temp_max === 'number' &&
    typeof form.temp_min === 'number'
  ) {
    form.temp_avg = +((form.temp_max + form.temp_min) / 2).toFixed(1)
  }
}
watch(
  () => [form.temp_max, form.temp_min],
  () => {
    if (isTempAvgAuto.value) autoCalcTempAvg()
  }
)

const submitting = ref(false)
const showSuccess = ref(false)
const submittedData = ref({})

onMounted(() => {
  loadAll()
})

// Sync to Pinia store
watch(
  () => ({
    ratedEnergy: form.total_mwh,
    totalPower: form.total_mw,
    duration: form.duration,
    temperature: form.temp_avg,
    cyclesPerDay: form.cycles_per_day,
    country: form.country,
    city: form.city,
    site: form.site,
    lat: form.lat,
    lng: form.lng,
    projectName: form.project_name,
    gridVoltage: form.grid_voltage,
    altitude: form.altitude,
    dod: form.dod
  }),
  (vals) => {
    try {
      if (vals.ratedEnergy != null) store.survey.ratedEnergy = vals.ratedEnergy
      if (vals.totalPower != null) store.survey.totalPower = vals.totalPower
      if (vals.duration != null) store.survey.duration = vals.duration
      if (vals.temperature != null) store.survey.temperature = vals.temperature
      if (vals.cyclesPerDay != null) store.survey.cyclesPerDay = vals.cyclesPerDay
      if (vals.country != null) store.survey.country = vals.country
      if (vals.city != null) store.survey.city = vals.city
      if (vals.site != null) store.survey.site = vals.site
      if (vals.lat != null) store.survey.lat = vals.lat
      if (vals.lng != null) store.survey.lng = vals.lng
      if (vals.projectName != null) store.survey.projectName = vals.projectName
      if (vals.gridVoltage != null) store.survey.gridVoltage = vals.gridVoltage
      if (vals.altitude != null) store.survey.altitude = vals.altitude
      if (vals.dod != null) store.survey.dod = vals.dod
      if (vals.ratedEnergy != null && typeof vals.ratedEnergy === 'number' && !isNaN(vals.ratedEnergy)) {
        const dod = vals.dod != null && typeof vals.dod === 'number' ? vals.dod : 90
        store.survey.requiredEnergy = +(vals.ratedEnergy * (dod / 100)).toFixed(1)
      }
    } catch (e) {
      console.warn('[SurveyForm] store sync error:', e)
    }
  },
  { deep: true }
)

async function submitForm() {
  if (!form.project_name) {
    emit('error', t('surveyForm.required'), 'warning')
    return
  }
  submitting.value = true
  try {
    const result = await api.post('/api/survey/submit', form)
    if (result.success) {
      submittedData.value = result
      showSuccess.value = true
      if (form.total_mwh) store.survey.ratedEnergy = form.total_mwh
      if (form.total_mw) store.survey.totalPower = form.total_mw
      if (form.duration) store.survey.duration = form.duration
      if (form.temp_avg != null) store.survey.temperature = form.temp_avg
      if (form.cycles_per_day) store.survey.cyclesPerDay = form.cycles_per_day
      if (form.total_mwh != null && form.duration != null && typeof form.total_mwh === 'number') {
        store.survey.requiredEnergy = +(form.total_mwh * 0.9).toFixed(1)
      }
      if (form.location) store.survey.location = form.location
      if (form.country) store.survey.country = form.country
      if (form.city) store.survey.city = form.city
      if (form.site) store.survey.site = form.site
      if (form.lat != null) store.survey.lat = form.lat
      if (form.lng != null) store.survey.lng = form.lng
      if (form.project_name) store.survey.projectName = form.project_name
      if (form.grid_voltage) store.survey.gridVoltage = form.grid_voltage
      if (form.altitude != null) store.survey.altitude = form.altitude
      clearDraft()
      resetForm()
    } else {
      emit('error', t('surveyForm.submitFailed') + ': ' + (result.error || t('common.other')), 'error')
    }
  } catch (error) {
    console.error(t('surveyForm.submitFailed'), error)
    emit('error', t('surveyForm.submitFailed'), 'error')
  } finally {
    submitting.value = false
  }
}

function resetForm() {
  Object.assign(form, {
    project_name: '',
    contact_person: '',
    contact_phone: '',
    contact_email: '',
    location: '',
    country: '',
    city: '',
    site: '',
    lat: null,
    lng: null,
    altitude: null,
    total_mw: null,
    total_mwh: null,
    duration: null,
    cycles_per_day: 1,
    temp_max: null,
    temp_min: null,
    temp_avg: null,
    humidity: null,
    grid_voltage: null,
    grid_frequency: null,
    pcc_voltage: null,
    pcc_short_circuit_mva: null,
    grid_code: '',
    sand_protection: '',
    humidity_cycle: '',
    cell_model: '',
    rte_target: null,
    soh_year1: null,
    soh_year25: null,
    calendar_life: null,
    cycle_life: null,
    availability_target: null,
    aux_consumption: null,
    response_time: null,
    dc_voltage_range: '',
    ac_voltage: null,
    thdi: null,
    remarks: ''
  })
  clearDraft()
}

function closeSuccess() {
  showSuccess.value = false
}

function fillTestData() {
  Object.assign(form, {
    project_name: t('surveyForm.testData.projectName'),
    contact_person: t('surveyForm.testData.contactPerson'),
    contact_phone: '+86 138-0000-1234',
    contact_email: 'zhangwei@energypro.com',
    country: t('surveyForm.testData.country'),
    city: t('surveyForm.testData.city'),
    site: t('surveyForm.testData.site'),
    lat: 11.55,
    lng: 104.92,
    altitude: 15,
    total_mw: 200,
    total_mwh: 400,
    duration: 2,
    cycles_per_day: 1,
    temp_max: 50,
    temp_min: 5,
    temp_avg: 28,
    humidity: 65,
    grid_voltage: 132,
    grid_frequency: 50,
    pcc_voltage: 33,
    pcc_short_circuit_mva: 500,
    grid_code: 'SEC',
    sand_protection: 'IP55',
    humidity_cycle: 'medium',
    rte_target: 92,
    soh_year1: 97.5,
    soh_year25: 70,
    calendar_life: 25,
    cycle_life: 8000,
    availability_target: 97,
    aux_consumption: 1.8,
    response_time: 100,
    dc_voltage_range: '1000-1500V',
    ac_voltage: 380,
    thdi: 3,
    remarks: t('surveyForm.testData.remarks')
  })
}
</script>

<style scoped>
.auto-badge {
  display: inline-block;
  font-size: 0.65rem;
  font-weight: 600;
  padding: 1px 6px;
  border-radius: 3px;
  background: #e8f5e9;
  color: #2e7d32;
  margin-left: 6px;
  vertical-align: middle;
}
.duration-input-row {
  display: flex;
  align-items: center;
  gap: 4px;
}
.duration-input-row .form-field-input {
  flex: 1;
}
.duration-input-row .form-field-input:disabled {
  background: var(--color-bg, #f5f5f5);
  color: var(--text-secondary, #888);
  cursor: not-allowed;
}
.lock-toggle-btn {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  border: 1px solid var(--color-border, #ddd);
  border-radius: 4px;
  background: var(--color-card, #fff);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  padding: 0;
}
.lock-toggle-btn:hover {
  background: var(--color-accent-glow, rgba(37, 99, 235, 0.08));
}
</style>
