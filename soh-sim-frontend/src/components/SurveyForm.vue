<template>
  <div class="h-full overflow-y-auto custom-scrollbar">
    <div class="max-w-5xl mx-auto space-y-4 py-2">
      <!-- 01: 基本信息 -->
      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold bg-accent-glow text-accent">
            01
          </span>
          <div>
            <h3 class="section-title text-accent border-accent">
              {{ $t('surveyForm.section01') }}
            </h3>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-3">
          <div class="col-span-2">
            <label class="label-text">{{ $t('surveyForm.projectName') }} *</label>
            <input v-model="form.project_name" class="form-field-input" :placeholder="$t('surveyForm.projectNamePh')" />
          </div>
          <div>
            <label class="label-text">{{ $t('surveyForm.location') }}</label>
            <input v-model="form.location" class="form-field-input" :placeholder="$t('surveyForm.locationPh')" />
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
      </div>

      <!-- 02: 项目规模 -->
      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold bg-accent-glow text-accent">
            02
          </span>
          <div>
            <h3 class="section-title text-accent border-accent">
              {{ $t('surveyForm.section02') }}
            </h3>
          </div>
        </div>
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
      </div>

      <!-- 03: 环境条件 -->
      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold bg-accent-glow text-accent">
            03
          </span>
          <div>
            <h3 class="section-title text-accent border-accent">
              {{ $t('surveyForm.section03') }}
            </h3>
          </div>
        </div>
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
            <label class="label-text">{{ $t('surveyForm.tempAvg') }}</label>
            <input
              v-model.number="form.temp_avg"
              type="number"
              class="form-field-input"
              :placeholder="$t('surveyForm.tempAvgPh')"
            />
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
      </div>

      <!-- 04: 电网参数 -->
      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold bg-accent-glow text-accent">
            04
          </span>
          <div>
            <h3 class="section-title text-accent border-accent">
              {{ $t('surveyForm.section04') }}
            </h3>
          </div>
        </div>
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
      </div>

      <!-- 05: 性能要求 -->
      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold bg-accent-glow text-accent">
            05
          </span>
          <div>
            <h3 class="section-title text-accent border-accent">
              {{ $t('surveyForm.section05') }}
            </h3>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="label-text">{{ $t('surveyForm.cellModel') }}</label>
            <select v-model="form.cell_model" class="form-field-select">
              <option value="">{{ $t('surveyForm.cellModelPh') }}</option>
              <option v-for="cell in cells" :key="cell.id" :value="cell.model">
                {{ cell.mfr }} - {{ cell.model }} ({{ cell.capacityAh }}Ah)
              </option>
            </select>
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
      </div>

      <!-- 06: 其他参数 -->
      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold bg-accent-glow text-accent">
            06
          </span>
          <div>
            <h3 class="section-title text-accent border-accent">
              {{ $t('surveyForm.section06') }}
            </h3>
          </div>
        </div>
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
      </div>

      <!-- 07: 备注信息 -->
      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold bg-accent-glow text-accent">
            07
          </span>
          <div>
            <h3 class="section-title text-accent border-accent">
              {{ $t('surveyForm.section07') }}
            </h3>
          </div>
        </div>
        <div>
          <label class="label-text">{{ $t('surveyForm.remarks') }}</label>
          <textarea
            v-model="form.remarks"
            rows="4"
            class="form-field-textarea"
            :placeholder="$t('surveyForm.remarksPh')"
          />
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="flex justify-end gap-3 pt-2">
        <button type="button" class="btn-secondary" @click="resetForm">
          {{ $t('surveyForm.reset') }}
        </button>
        <button type="button" class="btn-secondary" @click="fillTestData">
          {{ $t('surveyForm.fillTestData') }}
        </button>
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
          <h3 class="text-xl font-semibold mb-2 text-default">
            {{ $t('surveyForm.successTitle') }}
          </h3>
          <p class="mb-4 text-secondary">
            {{ $t('surveyForm.successDesc') }}
          </p>
          <div class="p-4 rounded-lg mb-5 text-left u-background-var-color-card-dark">
            <p class="text-sm mb-1 text-default">
              <strong>{{ $t('surveyForm.surveyId') }}:</strong>
              {{ submittedData.survey_id }}
            </p>
            <p class="text-sm text-default">
              <strong>{{ $t('surveyForm.projectCode') }}:</strong>
              {{ submittedData.project_code }}
            </p>
          </div>
          <button class="btn-primary w-full" @click="closeSuccess">
            {{ $t('surveyForm.confirm') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useProducts } from '../composables/useProducts'
import { useBessStore } from '../stores/bess.js'
import { useDraft } from '../composables/useDraft'
import api from '../services/api.js'

const { t } = useI18n()
const emit = defineEmits(['error'])
const store = useBessStore()

const { cells, loadAll } = useProducts()

const { state: form, clearDraft } = useDraft('survey-form', {
  project_name: '',
  contact_person: '',
  contact_phone: '',
  contact_email: '',
  location: '',
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
})

// 储能时长自动计算
const isDurationAuto = ref(true)

function autoCalcDuration() {
  if (form.total_mwh > 0 && form.total_mw > 0) {
    form.duration = +(form.total_mwh / form.total_mw).toFixed(2)
  }
}

watch(
  () => [form.total_mwh, form.total_mw],
  () => {
    if (isDurationAuto.value) autoCalcDuration()
  }
)

const submitting = ref(false)
const showSuccess = ref(false)
const submittedData = ref({})

onMounted(() => {
  loadAll()
})

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
      // 同步到 Pinia store，确保 Phase2/3/4 能读取调研数据
      if (form.total_mwh) store.survey.ratedEnergy = form.total_mwh
      if (form.total_mw) store.survey.totalPower = form.total_mw
      if (form.duration) store.survey.duration = form.duration
      if (form.temp_avg != null) store.survey.temperature = form.temp_avg
      if (form.cycles_per_day) store.survey.cyclesPerDay = form.cycles_per_day
      if (form.total_mwh && form.duration) {
        store.survey.requiredEnergy = +(form.total_mwh * 0.9).toFixed(1)
      }
      if (form.location) store.survey.location = form.location
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
  const testProjectName = t('surveyForm.testData.projectName')
  const testContactPerson = t('surveyForm.testData.contactPerson')
  const testLocation = t('surveyForm.testData.location')
  const testRemarks = t('surveyForm.testData.remarks')

  Object.assign(form, {
    project_name: testProjectName,
    contact_person: testContactPerson,
    contact_phone: '+86 138-0000-1234',
    contact_email: 'zhangwei@energypro.com',
    location: testLocation,
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
    remarks: testRemarks
  })
}
</script>

<style scoped>
/* 储能时长自动计算样式 */
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
