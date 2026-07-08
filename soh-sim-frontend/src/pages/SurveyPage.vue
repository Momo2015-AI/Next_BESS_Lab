<template>
  <div class="survey-page">
    <div class="tool-page max-w-4xl mx-auto">
      <!-- Header -->
      <div class="tool-header survey-header">
        <h1 class="survey-title">{{ $t('surveyForm.pageTitle') }}</h1>
        <p class="survey-desc">{{ $t('surveyForm.pageDesc') }}</p>
        <button class="btn-back" @click="goHome">{{ $t('surveyForm.backToSystem') }}</button>
      </div>

      <!-- Toast -->
      <div v-if="toast.show" class="toast" :class="'toast-' + toast.type">
        {{ toast.message }}
      </div>

      <!-- 调研表单 -->
      <form class="space-y-6" @submit.prevent="submitSurvey">
        <!-- 01. 基本信息 -->
        <SectionCard number="01" :title="$t('surveyForm.section01')">
          <div class="form-grid-2">
            <FormField
              v-model="formData.projectName"
              :label="$t('surveyForm.projectName')"
              required
              type="text"
              :placeholder="$t('surveyForm.projectNamePh')"
            />
            <FormField v-model="formData.location" :label="$t('surveyForm.location')" required type="text" :placeholder="$t('surveyForm.locationPhShort')" />
            <FormField v-model="formData.contact" :label="$t('surveyForm.contactPerson')" type="text" :placeholder="$t('surveyForm.contactPersonPhShort')" />
            <FormField v-model="formData.phone" :label="$t('surveyForm.contactPhone')" type="text" :placeholder="$t('surveyForm.contactPhonePhShort')" />
          </div>
        </SectionCard>

        <!-- 02. 储能需求 -->
        <SectionCard number="02" :title="$t('surveyForm.section02Storage')">
          <div class="form-grid-3">
            <FormField
              v-model.number="formData.ratedEnergy"
              :label="$t('surveyForm.ratedEnergyLabel')"
              required
              type="number"
              step="0.1"
              :placeholder="$t('surveyForm.ratedEnergyPh')"
              :hint="$t('surveyForm.ratedEnergyHint')"
            />
            <FormField
              v-model.number="formData.ratedPower"
              :label="$t('surveyForm.ratedPowerLabel')"
              type="number"
              step="0.1"
              :placeholder="$t('surveyForm.ratedPowerPh')"
              :hint="$t('surveyForm.ratedPowerHint')"
            />
            <FormField
              v-model.number="formData.dischargeHours"
              :label="$t('surveyForm.dischargeHoursLabel')"
              type="select"
              :options="dischargeHourOptions"
            />
          </div>
          <div class="form-grid-2">
            <FormField
              v-model="formData.application"
              :label="$t('surveyForm.applicationLabel')"
              required
              type="select"
              :placeholder="$t('common.select')"
              :options="applicationOptions"
            />
            <FormField
              v-model.number="formData.voltageLevel"
              :label="$t('surveyForm.voltageLevelLabel')"
              type="select"
              :options="voltageOptions"
            />
          </div>
        </SectionCard>

        <!-- 03. 运行参数 -->
        <SectionCard number="03" :title="$t('surveyForm.section03Operation')">
          <div class="form-grid-3">
            <FormField
              v-model.number="formData.cyclesPerDay"
              :label="$t('surveyForm.cyclesPerDayLabel')"
              type="number"
              step="0.5"
              min="0"
              :placeholder="$t('surveyForm.cyclesPerDayPh')"
              :hint="$t('surveyForm.cyclesPerDayHint')"
            />
            <FormField
              v-model.number="formData.dod"
              :label="$t('surveyForm.dodLabel')"
              type="number"
              step="5"
              min="0"
              max="100"
              :placeholder="$t('surveyForm.dodPh')"
            />
            <FormField v-model.number="formData.cRate" :label="$t('surveyForm.cRateLabel')" type="select" :options="cRateOptions" />
          </div>
          <div class="form-grid-2">
            <FormField
              v-model.number="formData.temperature"
              :label="$t('surveyForm.avgTempLabel')"
              type="number"
              :placeholder="$t('surveyForm.avgTempPh')"
            />
            <FormField
              v-model.number="formData.guaranteeYears"
              :label="$t('surveyForm.guaranteeYearsLabel')"
              type="number"
              min="1"
              max="30"
              :placeholder="$t('surveyForm.guaranteeYearsPh')"
            />
          </div>
        </SectionCard>

        <!-- 04. 电池选型偏好 -->
        <SectionCard number="04" :title="$t('surveyForm.section04Battery')">
          <div class="form-grid-3">
            <FormField v-model="formData.batteryType" :label="$t('surveyForm.batteryTypeLabel')" type="select" :options="batteryTypeOptions" />
            <FormField
              v-model="formData.cellCapacity"
              :label="$t('surveyForm.cellCapacityLabel')"
              type="select"
              :options="cellCapacityOptions"
            />
            <FormField v-model="formData.containerSpec" :label="$t('surveyForm.containerSpecLabel')" type="select" :options="containerOptions" />
          </div>
        </SectionCard>

        <SectionCard number="05" :title="$t('surveyForm.section05Special')" :subtitle="$t('surveyForm.optionalFill')">
          <div class="feature-checkboxes">
            <label v-for="feature in featureOptions" :key="feature.value" class="feature-chip">
              <input v-model="formData.features" type="checkbox" :value="feature.value" />
              <span>{{ feature.label }}</span>
            </label>
          </div>
          <FormField v-model="formData.remarks" :label="$t('surveyForm.otherRequirementLabel')" type="textarea" :placeholder="$t('surveyForm.otherRequirementPh')" />
        </SectionCard>

        <!-- 提交按钮 -->
        <div class="form-actions">
          <button type="button" class="btn-reset" @click="resetForm">{{ $t('surveyForm.reset') }}</button>
          <button type="submit" class="btn-submit">{{ $t('surveyForm.submit') }}</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import SectionCard from '../components/SectionCard.vue'
import FormField from '../components/FormField.vue'
import api from '../services/api.js'

const router = useRouter()
const { t } = useI18n()

const toast = reactive({ show: false, message: '', type: 'info' })
const showToast = (message, type = 'info') => {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => {
    toast.show = false
  }, 3000)
}

const submitting = ref(false)

function goHome() {
  router.push('/')
}

const featureOptions = computed(() => [
  { value: 'EMS', label: t('surveyForm.featureEms') },
  { value: '消防', label: t('surveyForm.featureFire') },
  { value: '空调', label: t('surveyForm.featureAc') },
  { value: '监控', label: t('surveyForm.featureMonitor') },
  { value: '动环', label: t('surveyForm.featureEnv') },
  { value: '调频', label: t('surveyForm.featureFreq') }
])

const applicationOptions = computed(() => [
  { value: '调峰', label: t('surveyForm.appPeakShaving') },
  { value: '调频', label: t('surveyForm.appFreqReg') },
  { value: '备用电源', label: t('surveyForm.appBackupPower') },
  { value: '峰谷套利', label: t('surveyForm.appArbitrage') },
  { value: '需求响应', label: t('surveyForm.appDemandResponse') },
  { value: '微电网', label: t('surveyForm.appMicrogrid') },
  { value: '其他', label: t('surveyForm.appOther') }
])

const voltageOptions = [
  { value: 10, label: '10 kV' },
  { value: 35, label: '35 kV' },
  { value: 110, label: '110 kV' },
  { value: 220, label: '220 kV' }
]

const dischargeHourOptions = computed(() => [
  { value: 1, label: t('surveyForm.dischargeHour1') },
  { value: 2, label: t('surveyForm.dischargeHour2') },
  { value: 3, label: t('surveyForm.dischargeHour3') },
  { value: 4, label: t('surveyForm.dischargeHour4') }
])

const cRateOptions = computed(() => [
  { value: 0.25, label: t('surveyForm.cRate025') },
  { value: 0.5, label: t('surveyForm.cRate05') },
  { value: 1, label: t('surveyForm.cRate1') }
])

const batteryTypeOptions = computed(() => [
  { value: 'LFP', label: t('surveyForm.batteryLfp') },
  { value: 'NCM', label: t('surveyForm.batteryNcm') },
  { value: '无所谓', label: t('surveyForm.batteryAny') }
])

const cellCapacityOptions = computed(() => [
  { value: '280', label: t('surveyForm.cell280') },
  { value: '302', label: t('surveyForm.cell302') },
  { value: '314', label: t('surveyForm.cell314') },
  { value: '无所谓', label: t('surveyForm.cellAny') }
])

const containerOptions = computed(() => [
  { value: '20ft', label: t('surveyForm.container20ft') },
  { value: '20ft-H', label: t('surveyForm.container20ftH') },
  { value: '40ft', label: t('surveyForm.container40ft') }
])

const formData = reactive({
  projectName: '',
  location: '',
  contact: '',
  phone: '',
  ratedEnergy: 10,
  ratedPower: 5,
  dischargeHours: 2,
  application: '',
  voltageLevel: 35,
  cyclesPerDay: 1,
  dod: 90,
  cRate: 0.5,
  temperature: 25,
  guaranteeYears: 10,
  batteryType: 'LFP',
  cellCapacity: '280',
  containerSpec: '20ft-H',
  features: [],
  remarks: ''
})

const defaults = { ...formData }

function resetForm() {
  Object.assign(formData, { ...defaults })
  showToast(t('surveyForm.formReset'))
}

async function submitSurvey() {
  if (!formData.projectName) {
    showToast(t('surveyForm.required'), 'error')
    return
  }
  if (formData.ratedEnergy == null || formData.ratedEnergy <= 0) {
    showToast(t('surveyForm.ratedEnergyRequired'), 'error')
    return
  }

  submitting.value = true
  try {
    const mappedData = {
      project_name: formData.projectName,
      contact_person: formData.contact || '',
      contact_phone: formData.phone || '',
      location: formData.location || '',
      total_mwh: formData.ratedEnergy,
      total_mw: formData.ratedPower || null,
      duration: formData.dischargeHours || null,
      grid_voltage: formData.voltageLevel || null,
      cycles_per_day: formData.cyclesPerDay || 1,
      temp_avg: formData.temperature || null,
      remarks: formData.remarks || ''
    }
    const surveyId = 'SURV' + Date.now()
    const surveyData = {
      id: surveyId,
      ...formData,
      submittedAt: new Date().toISOString(),
      status: 'pending',
      containerQty: Math.ceil(formData.ratedEnergy / 5),
      pcsQty: Math.ceil((formData.ratedPower || 5) / 5),
      totalEnergyMwh: formData.ratedEnergy,
      totalPowerMw: formData.ratedPower
    }
    let apiSuccess = false
    try {
      const result = await api.post('/api/survey/submit', mappedData)
      if (result.success) {
        apiSuccess = true
        surveyData.id = result.data?.survey_id || surveyId
      }
    } catch (e) {
      console.error('API 提交失败，使用本地存储:', e)
    }

    const surveys = JSON.parse(localStorage.getItem('surveys') || '[]')
    surveys.push(surveyData)
    localStorage.setItem('surveys', JSON.stringify(surveys))
    localStorage.setItem('currentSurveyId', surveyData.id)
    localStorage.setItem('currentSurvey', JSON.stringify(surveyData))
    showToast(apiSuccess ? t('surveyForm.surveySubmittedServer') : t('surveyForm.surveySubmittedLocal'), 'success')
    setTimeout(() => router.push('/'), 1500)
  } catch (error) {
    console.error('提交失败:', error)
    showToast(t('surveyForm.submitFailed'), 'error')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.survey-page {
  min-height: 100vh;
  padding: 32px 24px;
  background-color: var(--color-bg);
  color: var(--color-text);
}

.survey-header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
}

.survey-title {
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, var(--color-accent), var(--color-accent-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 6px;
}

.survey-desc {
  color: var(--color-text-muted);
  font-size: 14px;
  margin: 0;
}

.btn-back {
  padding: 8px 18px;
  border-radius: 8px;
  border: 1px solid var(--color-border);
  background: var(--color-card);
  color: var(--color-text-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-back:hover {
  background: var(--color-accent-glow, rgba(37, 99, 235, 0.08));
  border-color: var(--color-accent);
  color: var(--color-accent);
}

/* Toast */
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 10px 20px;
  border-radius: 8px;
  color: var(--color-text-on-accent);
  font-size: 14px;
  z-index: 1000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: opacity 0.3s ease;
}
.toast-success {
  background: var(--color-success);
}
.toast-error {
  background: var(--color-danger);
}
.toast-info {
  background: var(--color-info, var(--color-accent));
}
.toast-warning {
  background: var(--color-warning);
}

/* Feature checkboxes */
.feature-checkboxes {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 16px;
}

.feature-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 8px;
  background: var(--form-field-bg);
  font-size: 13px;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: background 0.2s ease;
}
.feature-chip:hover {
  background: var(--form-field-bg-hover);
}
.feature-chip input[type='checkbox'] {
  accent-color: var(--color-accent);
  width: 16px;
  height: 16px;
}

/* Form actions */
.form-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  padding: 24px 0 48px;
}

.btn-reset {
  padding: 12px 32px;
  border-radius: 10px;
  border: 1px solid var(--color-border);
  background: var(--color-card);
  color: var(--color-text-secondary);
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-reset:hover {
  background: var(--color-accent-glow, rgba(37, 99, 235, 0.08));
  border-color: var(--color-accent);
}

.btn-submit {
  padding: 12px 40px;
  border-radius: 10px;
  border: none;
  background: linear-gradient(135deg, var(--color-accent), var(--color-success));
  color: var(--color-text-on-accent);
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.2s ease;
}
.btn-submit:hover {
  opacity: 0.9;
}

@media (max-width: 640px) {
  .survey-page {
    padding: 16px;
  }
  .form-actions {
    flex-direction: column;
    align-items: stretch;
  }
  .form-actions button {
    width: 100%;
  }
}
</style>
