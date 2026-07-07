<template>
  <div class="h-full overflow-y-auto custom-scrollbar">
    <div class="max-w-5xl mx-auto space-y-4 py-2">
      <!-- 01: 基本信息 -->
      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span
            class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold bg-accent-glow text-accent"
          >
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
          <span
            class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold bg-accent-glow text-accent"
          >
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
            <label class="label-text">{{ $t('surveyForm.durationH') }}</label>
            <input
              v-model.number="form.duration"
              type="number"
              step="0.5"
              min="0.5"
              max="8"
              class="form-field-input"
              :placeholder="$t('surveyForm.durationHPh')"
            />
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
          <span
            class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold bg-accent-glow text-accent"
          >
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
          <span
            class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold bg-accent-glow text-accent"
          >
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
          <span
            class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold bg-accent-glow text-accent"
          >
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
          <span
            class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold bg-accent-glow text-accent"
          >
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
          <span
            class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold bg-accent-glow text-accent"
          >
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
      <div
        v-if="showSuccess"
        class="fixed inset-0 z-50 flex items-center justify-center u-background-rgba-0-0-0-0-5"
      >
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
import { ref, reactive, onMounted } from 'vue'
import { useProducts } from '../composables/useProducts'

const emit = defineEmits(['error'])

const { cells, loadAll } = useProducts()

const form = reactive({
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

const submitting = ref(false)
const showSuccess = ref(false)
const submittedData = ref({})

onMounted(() => {
  loadAll()
})

async function submitForm() {
  if (!form.project_name) {
    emit('error', '请填写项目名称', 'warning')
    return
  }

  submitting.value = true

  try {
    const response = await fetch('/api/survey/submit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(form)
    })

    const result = await response.json()

    if (result.success) {
      submittedData.value = result
      showSuccess.value = true
      resetForm()
    } else {
      emit('error', '提交失败: ' + (result.error || '未知错误'), 'error')
    }
  } catch (error) {
    console.error('提交失败:', error)
    emit('error', '提交失败, 请检查网络连接或稍后重试', 'error')
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
}

function closeSuccess() {
  showSuccess.value = false
}

function fillTestData() {
  Object.assign(form, {
    project_name: '阿布扎比 200MW/400MWh 独立储能电站',
    contact_person: '张伟',
    contact_phone: '+86 138-0000-1234',
    contact_email: 'zhangwei@energypro.com',
    location: '阿联酋 阿布扎比 Al Dhafra 工业区',
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
    remarks:
      '项目位于沙漠气候区，要求集装箱具备C4以上防腐等级。PCS需满足Masdar级液冷碳化硅方案，支持构网型Grid-Forming功能。预期2027年Q1并网投运。'
  })
}
</script>
