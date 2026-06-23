<template>
  <div class="survey-form-container">
    <div class="form-header">
      <h1>BESS项目调研表</h1>
      <p class="subtitle">请填写以下信息，提交后将自动生成项目</p>
    </div>

    <form @submit.prevent="submitForm" class="survey-form">
      <!-- 基本信息 -->
      <section class="form-section">
        <h2>基本信息</h2>
        <div class="form-grid">
          <div class="form-group required">
            <label>项目名称</label>
            <input v-model="form.project_name" type="text" placeholder="请输入项目名称" required />
          </div>
          <div class="form-group">
            <label>项目地点</label>
            <input v-model="form.location" type="text" placeholder="请输入项目地点" />
          </div>
          <div class="form-group">
            <label>联系人</label>
            <input v-model="form.contact_person" type="text" placeholder="请输入联系人姓名" />
          </div>
          <div class="form-group">
            <label>联系电话</label>
            <input v-model="form.contact_phone" type="tel" placeholder="请输入联系电话" />
          </div>
          <div class="form-group">
            <label>联系邮箱</label>
            <input v-model="form.contact_email" type="email" placeholder="请输入联系邮箱" />
          </div>
        </div>
      </section>

      <!-- 项目规模 -->
      <section class="form-section">
        <h2>项目规模</h2>
        <div class="form-grid">
          <div class="form-group">
            <label>总功率 (MW)</label>
            <input v-model.number="form.total_mw" type="number" step="0.1" min="0" placeholder="如：100" />
          </div>
          <div class="form-group">
            <label>总容量 (MWh)</label>
            <input v-model.number="form.total_mwh" type="number" step="0.1" min="0" placeholder="如：200" />
          </div>
          <div class="form-group">
            <label>储能时长 (h)</label>
            <input v-model.number="form.duration" type="number" step="0.5" min="0.5" max="8" placeholder="如：2" />
          </div>
          <div class="form-group">
            <label>每日循环次数</label>
            <input v-model.number="form.cycles_per_day" type="number" step="0.5" min="0.5" max="4" placeholder="如：1" />
          </div>
        </div>
      </section>

      <!-- 环境条件 -->
      <section class="form-section">
        <h2>环境条件</h2>
        <div class="form-grid">
          <div class="form-group">
            <label>海拔高度 (m)</label>
            <input v-model.number="form.altitude" type="number" min="0" placeholder="如：1500" />
          </div>
          <div class="form-group">
            <label>最高温度 (°C)</label>
            <input v-model.number="form.temp_max" type="number" placeholder="如：45" />
          </div>
          <div class="form-group">
            <label>最低温度 (°C)</label>
            <input v-model.number="form.temp_min" type="number" placeholder="如：-20" />
          </div>
          <div class="form-group">
            <label>平均温度 (°C)</label>
            <input v-model.number="form.temp_avg" type="number" placeholder="如：15" />
          </div>
          <div class="form-group">
            <label>相对湿度 (%)</label>
            <input v-model.number="form.humidity" type="number" min="0" max="100" placeholder="如：65" />
          </div>
        </div>
      </section>

      <!-- 电网参数 -->
      <section class="form-section">
        <h2>电网参数</h2>
        <div class="form-grid">
          <div class="form-group">
            <label>并网电压 (kV)</label>
            <input v-model.number="form.grid_voltage" type="number" step="0.1" placeholder="如：35" />
          </div>
          <div class="form-group">
            <label>电网频率 (Hz)</label>
            <input v-model.number="form.grid_frequency" type="number" step="0.1" placeholder="如：50" />
          </div>
        </div>
      </section>

      <!-- 性能要求 -->
      <section class="form-section">
        <h2>性能要求</h2>
        <div class="form-grid">
          <div class="form-group">
            <label>电芯型号</label>
            <select v-model="form.cell_model" class="input-field">
              <option value="">请选择电芯型号</option>
              <option v-for="cell in cells" :key="cell.id" :value="cell.model">
                {{ cell.mfr }} - {{ cell.model }} ({{ cell.capacityAh }}Ah)
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>RTE目标 (%)</label>
            <input v-model.number="form.rte_target" type="number" min="0" max="100" placeholder="如：90" />
          </div>
          <div class="form-group">
            <label>SOH第一年 (%)</label>
            <input v-model.number="form.soh_year1" type="number" min="0" max="100" placeholder="如：98" />
          </div>
          <div class="form-group">
            <label>SOH第25年 (%)</label>
            <input v-model.number="form.soh_year25" type="number" min="0" max="100" placeholder="如：70" />
          </div>
          <div class="form-group">
            <label>日历寿命 (年)</label>
            <input v-model.number="form.calendar_life" type="number" min="1" max="30" placeholder="如：20" />
          </div>
          <div class="form-group">
            <label>循环寿命 (次)</label>
            <input v-model.number="form.cycle_life" type="number" min="0" placeholder="如：6000" />
          </div>
          <div class="form-group">
            <label>可用率目标 (%)</label>
            <input v-model.number="form.availability_target" type="number" min="0" max="100" placeholder="如：95" />
          </div>
        </div>
      </section>

      <!-- 其他参数 -->
      <section class="form-section">
        <h2>其他参数</h2>
        <div class="form-grid">
          <div class="form-group">
            <label>辅助功耗 (%)</label>
            <input v-model.number="form.aux_consumption" type="number" step="0.1" min="0" placeholder="如：1.5" />
          </div>
          <div class="form-group">
            <label>响应时间 (ms)</label>
            <input v-model.number="form.response_time" type="number" min="0" placeholder="如：100" />
          </div>
          <div class="form-group">
            <label>直流电压范围</label>
            <input v-model="form.dc_voltage_range" type="text" placeholder="如：600-1000V" />
          </div>
          <div class="form-group">
            <label>交流电压 (V)</label>
            <input v-model.number="form.ac_voltage" type="number" placeholder="如：380" />
          </div>
          <div class="form-group">
            <label>谐波畸变THDI (%)</label>
            <input v-model.number="form.thdi" type="number" step="0.1" min="0" max="100" placeholder="如：5" />
          </div>
        </div>
      </section>

      <!-- 备注 -->
      <section class="form-section">
        <h2>备注信息</h2>
        <div class="form-group full-width">
          <label>其他说明</label>
          <textarea v-model="form.remarks" rows="4" placeholder="请输入其他需要说明的信息..."></textarea>
        </div>
      </section>

      <!-- 提交按钮 -->
      <div class="form-actions">
        <button type="button" class="btn-secondary" @click="resetForm">重置</button>
        <button type="button" class="btn-secondary" @click="fillTestData">填充测试数据</button>
        <button type="submit" class="btn-primary" :disabled="submitting">
          {{ submitting ? '提交中...' : '提交调研表' }}
        </button>
      </div>
    </form>

    <!-- 提交成功弹窗 -->
    <div v-if="showSuccess" class="success-modal">
      <div class="modal-content">
        <div class="success-icon">✓</div>
        <h3>提交成功！</h3>
        <p>调研表已成功提交，项目已自动创建</p>
        <div class="info-box">
          <p><strong>调研表ID:</strong> {{ submittedData.survey_id }}</p>
          <p><strong>项目编号:</strong> {{ submittedData.project_code }}</p>
        </div>
        <button class="btn-primary" @click="closeSuccess">确定</button>
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
    emit('error', '提交失败，请检查网络连接或稍后重试', 'error')
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
    remarks: '项目位于沙漠气候区，要求集装箱具备C4以上防腐等级。PCS需满足Masdar级液冷碳化硅方案，支持构网型Grid-Forming功能。预期2027年Q1并网投运。'
  })
}
</script>

<style scoped>
.survey-form-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px;
  background: var(--color-bg);
  color: var(--color-text);
  min-height: 100vh;
}

.form-header {
  text-align: center;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 2px solid var(--color-border);
}

.form-header h1 {
  font-size: 28px;
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 8px 0;
}

.subtitle {
  color: var(--color-text-muted);
  font-size: 14px;
  margin: 0;
}

.survey-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-section {
  background: var(--color-bg-secondary);
  border-radius: 12px;
  padding: 24px;
}

.form-section h2 {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 16px 0;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--color-border);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group.required label::after {
  content: ' *';
  color: #ef4444;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
}

.form-group input,
.form-group textarea {
  padding: 10px 14px;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-size: 14px;
  background: var(--color-bg);
  color: var(--color-text);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: #9ca3af;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  padding-top: 24px;
}

.btn-primary,
.btn-secondary {
  padding: 12px 32px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #3b82f6;
  color: white;
  border: none;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn-primary:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.btn-secondary {
  background: white;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn-secondary:hover {
  background: #f3f4f6;
}

.success-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 32px;
  border-radius: 16px;
  text-align: center;
  max-width: 400px;
  width: 90%;
}

.success-icon {
  width: 64px;
  height: 64px;
  background: #10b981;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  margin: 0 auto 16px;
}

.modal-content h3 {
  font-size: 20px;
  color: #1f2937;
  margin: 0 0 8px;
}

.modal-content p {
  color: #6b7280;
  margin: 0 0 16px;
}

.info-box {
  background: #f3f4f6;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 20px;
  text-align: left;
}

.info-box p {
  margin: 4px 0;
  font-size: 13px;
  color: #374151;
}

.info-box strong {
  color: #1f2937;
}
</style>