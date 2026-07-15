<template>
  <div class="survey-page">
    <AppPage title-key="surveyForm.pageTitle" desc-key="surveyForm.pageDesc">
      <template #actions>
        <button class="btn-back" @click="goHome">{{ $t('surveyForm.backToSystem') }}</button>
      </template>

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
            <FormField
              v-model="formData.country"
              :label="$t('surveyForm.country')"
              type="text"
              :placeholder="$t('surveyForm.countryPh')"
            />
            <FormField
              v-model="formData.city"
              :label="$t('surveyForm.city')"
              type="text"
              :placeholder="$t('surveyForm.cityPh')"
            />
            <FormField
              v-model="formData.site"
              :label="$t('surveyForm.site')"
              type="text"
              :placeholder="$t('surveyForm.sitePh')"
            />
            <FormField
              v-model.number="formData.lat"
              :label="$t('surveyForm.lat')"
              type="number"
              step="0.0001"
              :placeholder="$t('surveyForm.latPh')"
            />
            <FormField
              v-model.number="formData.lng"
              :label="$t('surveyForm.lng')"
              type="number"
              step="0.0001"
              :placeholder="$t('surveyForm.lngPh')"
            />
            <FormField
              v-model="formData.contact"
              :label="$t('surveyForm.contactPerson')"
              type="text"
              :placeholder="$t('surveyForm.contactPersonPhShort')"
            />
            <FormField
              v-model="formData.phone"
              :label="$t('surveyForm.contactPhone')"
              type="text"
              :placeholder="$t('surveyForm.contactPhonePhShort')"
            />
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
            >
              <template #hint>
                <span v-if="suggestedCyclesPerDay !== null" class="text-xs text-muted">
                  {{ $t('surveyForm.cyclesPerDayHint') }}
                  &bull; {{ $t('surveyForm.suggestedHint') }}: {{ suggestedCyclesPerDay }}
                </span>
                <span v-else>{{ $t('surveyForm.cyclesPerDayHint') }}</span>
              </template>
            </FormField>
            <FormField
              v-model.number="formData.dod"
              :label="$t('surveyForm.dodLabel')"
              type="number"
              step="5"
              min="0"
              max="100"
              :placeholder="$t('surveyForm.dodPh')"
            />
            <FormField
              v-model.number="formData.cRate"
              :label="$t('surveyForm.cRateLabel')"
              type="select"
              :options="cRateOptions"
            />
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
            <FormField
              v-model="formData.batteryType"
              :label="$t('surveyForm.batteryTypeLabel')"
              type="select"
              :options="batteryTypeOptions"
            />
            <FormField
              v-model="formData.cellCapacity"
              :label="$t('surveyForm.cellCapacityLabel')"
              type="select"
              :options="cellCapacityOptions"
            />
            <FormField
              v-model="formData.containerSpec"
              :label="$t('surveyForm.containerSpecLabel')"
              type="select"
              :options="containerOptions"
            />
          </div>
        </SectionCard>

        <SectionCard number="05" :title="$t('surveyForm.section05Special')" :subtitle="$t('surveyForm.optionalFill')">
          <div class="feature-checkboxes">
            <label v-for="feature in featureOptions" :key="feature.value" class="feature-chip">
              <input v-model="formData.features" type="checkbox" :value="feature.value" />
              <span>{{ feature.label }}</span>
            </label>
          </div>
          <FormField
            v-model="formData.remarks"
            :label="$t('surveyForm.otherRequirementLabel')"
            type="textarea"
            :placeholder="$t('surveyForm.otherRequirementPh')"
          />
        </SectionCard>

        <!-- 提交按钮 -->
        <div class="form-actions">
          <button type="button" class="btn-reset" @click="resetForm">{{ $t('surveyForm.reset') }}</button>
          <button type="submit" class="btn-submit">{{ $t('surveyForm.submit') }}</button>
        </div>
      </form>
    </AppPage>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import SectionCard from '../components/SectionCard.vue'
import AppPage from '../components/AppPage.vue'
import FormField from '../components/FormField.vue'
import api from '../services/api.js'
import { useBessStore, DEFAULT_SURVEY, DEFAULT_DOD } from '../stores/bess.js'

const router = useRouter()
const route = useRoute()
const { t } = useI18n()
const store = useBessStore()

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

// Auto-calc ratedPower from ratedEnergy / dischargeHours
const isPowerAuto = ref(true)

// 如果路由带 :id 参数，加载已有调研数据
onMounted(async () => {
  const surveyId = route.params.id
  if (surveyId) {
    try {
      const data = await api.get(`/api/survey/${surveyId}`)
      if (data.success) {
        const s = data.data
        formData.projectName = s.project_name || ''
        formData.contact = s.contact_person || ''
        formData.phone = s.contact_phone || ''
        formData.country = s.country || ''
        formData.city = s.city || ''
        formData.site = s.site || ''
        formData.lat = s.lat || null
        formData.lng = s.lng || null
        // fallback for old data that only has location field
        if (!formData.country && !formData.city && !formData.site && s.location) {
          formData.site = s.location
        }
        formData.ratedEnergy = s.total_mwh || null
        formData.ratedPower = s.total_mw || null
        formData.dischargeHours = s.duration || null
        formData.voltageLevel = s.grid_voltage || null
        formData.cyclesPerDay = s.cycles_per_day || 1
        formData.temperature = s.temp_avg || null
        formData.remarks = s.remarks || ''
        showToast(t('surveyForm.surveyLoaded'), 'success')
      }
    } catch (e) {
      console.error('加载调研数据失败:', e)
    }
  } else {
    // 从 store 恢复数据（无路由参数时）
    const s = store.survey
    if (s.ratedEnergy) formData.ratedEnergy = s.ratedEnergy
    if (s.totalPower) formData.ratedPower = s.totalPower
    if (s.duration) formData.dischargeHours = s.duration
    if (s.temperature) formData.temperature = s.temperature
    if (s.cyclesPerDay) formData.cyclesPerDay = s.cyclesPerDay
    if (s.country) formData.country = s.country
    if (s.city) formData.city = s.city
    if (s.site) formData.site = s.site
    if (s.lat != null) formData.lat = s.lat
    if (s.lng != null) formData.lng = s.lng
    if (s.location && !formData.site) formData.site = s.location
    if (s.projectName) formData.projectName = s.projectName
    if (s.gridVoltage) formData.voltageLevel = s.gridVoltage
  }
})

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

// Suggested cycles per day based on discharge duration
const suggestedCyclesPerDay = computed(() => {
  if (!formData.dischargeHours || formData.dischargeHours <= 0) return null
  return Math.floor(24 / (2 * formData.dischargeHours))
})

// Auto-calc ratedPower from ratedEnergy / dischargeHours
watch(
  () => [formData.ratedEnergy, formData.dischargeHours],
  ([energy, hours]) => {
    if (isPowerAuto.value && energy > 0 && hours > 0) {
      formData.ratedPower = +(energy / hours).toFixed(1)
    }
  }
)

const formData = reactive({
  projectName: '',
  country: '',
  city: '',
  site: '',
  lat: null,
  lng: null,
  contact: '',
  phone: '',
  ratedEnergy: 10,
  ratedPower: 5,
  dischargeHours: 2,
  application: '',
  voltageLevel: 35,
  cyclesPerDay: DEFAULT_SURVEY.cyclesPerDay,
  dod: DEFAULT_DOD,
  cRate: DEFAULT_SURVEY.cRate,
  temperature: DEFAULT_SURVEY.temperature,
  guaranteeYears: 10,
  batteryType: 'LFP',
  cellCapacity: '280',
  containerSpec: '20ft-H',
  features: [],
  remarks: ''
})

const defaults = { ...formData }

const formLocation = computed(() => {
  const parts = [formData.country, formData.city, formData.site].filter(Boolean)
  return parts.join(', ')
})

function resetForm() {
  Object.assign(formData, { ...defaults })
  showToast(t('surveyForm.formReset'))
}

const CONTAINER_CAPACITY_MWH = {
  '20ft': 3.7,
  '20ft-H': 5,
  '40ft': 10
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
      location: formLocation.value || '',
      country: formData.country || '',
      city: formData.city || '',
      site: formData.site || '',
      lat: formData.lat || null,
      lng: formData.lng || null,
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
      containerQty: Math.ceil(formData.ratedEnergy / (CONTAINER_CAPACITY_MWH[formData.containerSpec] || 5)),
      // PCS rated power defaults to 5 MW per unit; can be configured via PCS_RATED_POWER_MW
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

    // 同步到 Pinia store，确保 Phase2/3 能读取调研数据
    store.survey.ratedEnergy = formData.ratedEnergy
    store.survey.totalPower = formData.ratedPower || 50
    store.survey.duration = formData.dischargeHours || 2
    store.survey.temperature = formData.temperature || 25
    store.survey.cyclesPerDay = formData.cyclesPerDay || 1
    if (formData.dod) store.survey.dod = formData.dod
    if (formData.cRate) store.survey.cRate = formData.cRate
    store.survey.requiredEnergy = +(formData.ratedEnergy * ((formData.dod || 90) / 100)).toFixed(1)
    if (formLocation.value) store.survey.location = formLocation.value
    if (formData.country) store.survey.country = formData.country
    if (formData.city) store.survey.city = formData.city
    if (formData.site) store.survey.site = formData.site
    if (formData.lat != null) store.survey.lat = formData.lat
    if (formData.lng != null) store.survey.lng = formData.lng
    if (formData.projectName) store.survey.projectName = formData.projectName
    if (formData.voltageLevel) store.survey.gridVoltage = formData.voltageLevel

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
