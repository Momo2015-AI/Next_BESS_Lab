<template>
  <div class="survey-page">
    <div class="tool-page max-w-4xl mx-auto">
      <!-- Header -->
      <div class="tool-header survey-header">
        <h1 class="survey-title">储能电站项目调研表</h1>
        <p class="survey-desc">请填写以下信息，我们将据此为您定制最优的储能系统配置方案</p>
        <button class="btn-back" @click="goHome">← 返回系统</button>
      </div>

      <!-- Toast -->
      <div v-if="toast.show" class="toast" :class="'toast-' + toast.type">
        {{ toast.message }}
      </div>

      <!-- 调研表单 -->
      <form class="space-y-6" @submit.prevent="submitSurvey">
        <!-- 01. 基本信息 -->
        <SectionCard number="01" title="基本信息">
          <div class="form-grid-2">
            <FormField
              v-model="formData.projectName"
              label="项目名称"
              required
              type="text"
              placeholder="请输入项目名称"
            />
            <FormField v-model="formData.location" label="项目地址" required type="text" placeholder="省/市/区" />
            <FormField v-model="formData.contact" label="联系人" type="text" placeholder="姓名" />
            <FormField v-model="formData.phone" label="联系电话" type="text" placeholder="手机号码" />
          </div>
        </SectionCard>

        <!-- 02. 储能需求 -->
        <SectionCard number="02" title="储能需求">
          <div class="form-grid-3">
            <FormField
              v-model.number="formData.ratedEnergy"
              label="额定能量 (MWh)"
              required
              type="number"
              step="0.1"
              placeholder="如：10"
              hint="电池集装箱总容量"
            />
            <FormField
              v-model.number="formData.ratedPower"
              label="额定功率 (MW)"
              type="number"
              step="0.1"
              placeholder="如：5"
              hint="PCS总额定功率"
            />
            <FormField
              v-model.number="formData.dischargeHours"
              label="放电时长 (h)"
              type="select"
              :options="dischargeHourOptions"
            />
          </div>
          <div class="form-grid-2">
            <FormField
              v-model="formData.application"
              label="应用场景"
              required
              type="select"
              placeholder="请选择"
              :options="applicationOptions"
            />
            <FormField
              v-model.number="formData.voltageLevel"
              label="并网电压等级"
              type="select"
              :options="voltageOptions"
            />
          </div>
        </SectionCard>

        <!-- 03. 运行参数 -->
        <SectionCard number="03" title="运行参数">
          <div class="form-grid-3">
            <FormField
              v-model.number="formData.cyclesPerDay"
              label="日均循环次数"
              type="number"
              step="0.5"
              min="0"
              placeholder="如：1"
              hint="0.5 = 每2天一次"
            />
            <FormField
              v-model.number="formData.dod"
              label="DOD设置 (%)"
              type="number"
              step="5"
              min="0"
              max="100"
              placeholder="如：90"
            />
            <FormField v-model.number="formData.cRate" label="设计倍率 (C)" type="select" :options="cRateOptions" />
          </div>
          <div class="form-grid-2">
            <FormField
              v-model.number="formData.temperature"
              label="年平均温度 (°C)"
              type="number"
              placeholder="如：25"
            />
            <FormField
              v-model.number="formData.guaranteeYears"
              label="保障年限 (年)"
              type="number"
              min="1"
              max="30"
              placeholder="如：10"
            />
          </div>
        </SectionCard>

        <!-- 04. 电池选型偏好 -->
        <SectionCard number="04" title="电池选型偏好">
          <div class="form-grid-3">
            <FormField v-model="formData.batteryType" label="电池类型" type="select" :options="batteryTypeOptions" />
            <FormField
              v-model="formData.cellCapacity"
              label="电芯容量偏好"
              type="select"
              :options="cellCapacityOptions"
            />
            <FormField v-model="formData.containerSpec" label="集装箱规格" type="select" :options="containerOptions" />
          </div>
        </SectionCard>

        <!-- 05. 特殊需求（可选） -->
        <SectionCard number="05" title="特殊需求" subtitle="可选填写">
          <div class="feature-checkboxes">
            <label v-for="feature in featureOptions" :key="feature.value" class="feature-chip">
              <input v-model="formData.features" type="checkbox" :value="feature.value" />
              <span>{{ feature.label }}</span>
            </label>
          </div>
          <FormField v-model="formData.remarks" label="其他要求" type="textarea" placeholder="请描述其他特殊需求..." />
        </SectionCard>

        <!-- 提交按钮 -->
        <div class="form-actions">
          <button type="button" class="btn-reset" @click="resetForm">重置</button>
          <button type="submit" class="btn-submit">提交调研表</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import SectionCard from '../components/SectionCard.vue'
import FormField from '../components/FormField.vue'

const router = useRouter()

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

const featureOptions = [
  { value: 'EMS', label: '能量管理系统' },
  { value: '消防', label: '消防系统' },
  { value: '空调', label: '温控系统' },
  { value: '监控', label: '视频监控' },
  { value: '动环', label: '动环监控' },
  { value: '调频', label: '一次调频' }
]

const applicationOptions = [
  { value: '调峰', label: '调峰' },
  { value: '调频', label: '调频' },
  { value: '备用电源', label: '备用电源' },
  { value: '峰谷套利', label: '峰谷套利' },
  { value: '需求响应', label: '需求响应' },
  { value: '微电网', label: '微电网' },
  { value: '其他', label: '其他' }
]

const voltageOptions = [
  { value: 10, label: '10 kV' },
  { value: 35, label: '35 kV' },
  { value: 110, label: '110 kV' },
  { value: 220, label: '220 kV' }
]

const dischargeHourOptions = [
  { value: 1, label: '1小时' },
  { value: 2, label: '2小时' },
  { value: 3, label: '3小时' },
  { value: 4, label: '4小时' }
]

const cRateOptions = [
  { value: 0.25, label: '0.25C (低倍率)' },
  { value: 0.5, label: '0.5C (标准)' },
  { value: 1, label: '1C (高倍率)' }
]

const batteryTypeOptions = [
  { value: 'LFP', label: '磷酸铁锂 (LFP)' },
  { value: 'NCM', label: '三元锂 (NCM)' },
  { value: '无所谓', label: '无所谓' }
]

const cellCapacityOptions = [
  { value: '280', label: '280Ah (主流)' },
  { value: '302', label: '302Ah (新品)' },
  { value: '314', label: '314Ah (高容量)' },
  { value: '无所谓', label: '无所谓' }
]

const containerOptions = [
  { value: '20ft', label: '20ft 标准柜' },
  { value: '20ft-H', label: '20ft 高柜 (5MWh)' },
  { value: '40ft', label: '40ft 标准柜' }
]

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
  showToast('表单已重置')
}

async function submitSurvey() {
  if (!formData.projectName) {
    showToast('请填写项目名称', 'error')
    return
  }
  if (formData.ratedEnergy == null || formData.ratedEnergy <= 0) {
    showToast('请填写额定能量', 'error')
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
      const response = await fetch('/api/survey/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(mappedData)
      })
      const result = await response.json()
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
    showToast(apiSuccess ? '调研表已提交至服务器！' : '调研表已保存在本地！', 'success')
    setTimeout(() => router.push('/'), 1500)
  } catch (error) {
    console.error('提交失败:', error)
    showToast('提交失败，请重试', 'error')
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
  color: #fff;
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
  background: var(--color-info, #3b82f6);
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
  color: #fff;
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
