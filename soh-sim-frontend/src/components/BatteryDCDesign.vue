<template>
  <div class="battery-dc-design h-full overflow-auto p-4">
    <div class="bg-slate-900/60 rounded-lg border border-slate-800 p-4">
      <h3 class="text-sm font-bold text-teal-400 mb-4 flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-teal-400"></span>
        直流侧设计（电池系统）
      </h3>

      <!-- 电池系统配置 -->
      <div class="grid grid-cols-2 gap-4 mb-4">
        <!-- 电芯选型 -->
        <div class="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
          <h4 class="text-xs text-slate-300 mb-3 font-medium">电芯选型</h4>
          
          <div class="space-y-3">
            <div>
              <label class="text-[10px] text-slate-500 block mb-1">电芯类型</label>
              <select v-model="batteryConfig.cellType" class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1.5 text-xs focus:border-teal-500 outline-none">
                <option value="LFP280">LFP 280Ah (主流)</option>
                <option value="LFP302">LFP 302Ah (新品)</option>
                <option value="LFP314">LFP 314Ah (高容量)</option>
                <option value="NCM">NCM (三元锂)</option>
              </select>
            </div>
            
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] text-slate-500 block mb-1">额定容量 (Ah)</label>
                <input v-model.number="batteryConfig.cellCapacity" type="number"
                  class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 outline-none">
              </div>
              <div>
                <label class="text-[10px] text-slate-500 block mb-1">额定电压 (V)</label>
                <input v-model.number="batteryConfig.cellVoltage" type="number"
                  class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 outline-none">
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] text-slate-500 block mb-1">能量密度 (Wh/kg)</label>
                <input v-model.number="batteryConfig.energyDensity" type="number"
                  class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 outline-none">
              </div>
              <div>
                <label class="text-[10px] text-slate-500 block mb-1">循环寿命 (次)</label>
                <input v-model.number="batteryConfig.cycleLife" type="number"
                  class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 outline-none">
              </div>
            </div>
          </div>
        </div>

        <!-- 电池簇配置 -->
        <div class="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
          <h4 class="text-xs text-slate-300 mb-3 font-medium">电池簇配置</h4>
          
          <div class="space-y-3">
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] text-slate-500 block mb-1">串联数量 (S)</label>
                <input v-model.number="batteryConfig.seriesCount" type="number"
                  class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 outline-none">
              </div>
              <div>
                <label class="text-[10px] text-slate-500 block mb-1">并联数量 (P)</label>
                <input v-model.number="batteryConfig.parallelCount" type="number"
                  class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 outline-none">
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] text-slate-500 block mb-1">簇电压 (V)</label>
                <input v-model.number="batteryConfig.stringVoltage" type="number" readonly
                  class="w-full bg-slate-700 border border-slate-600 rounded px-2 py-1 text-xs text-teal-400">
              </div>
              <div>
                <label class="text-[10px] text-slate-500 block mb-1">簇容量 (Ah)</label>
                <input v-model.number="batteryConfig.stringCapacity" type="number" readonly
                  class="w-full bg-slate-700 border border-slate-600 rounded px-2 py-1 text-xs text-teal-400">
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] text-slate-500 block mb-1">簇能量 (kWh)</label>
                <input v-model.number="batteryConfig.stringEnergy" type="number" readonly
                  class="w-full bg-slate-700 border border-slate-600 rounded px-2 py-1 text-xs text-teal-400">
              </div>
              <div>
                <label class="text-[10px] text-slate-500 block mb-1">簇数量</label>
                <input v-model.number="batteryConfig.stringQty" type="number"
                  class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 outline-none">
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 集装箱配置 -->
      <div class="bg-slate-800/50 rounded-lg p-4 border border-slate-700 mb-4">
        <h4 class="text-xs text-slate-300 mb-3 font-medium">集装箱配置</h4>
        
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">集装箱规格</label>
            <select v-model="batteryConfig.containerSpec" class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 outline-none">
              <option value="20ft">20ft 标准集装箱</option>
              <option value="40ft">40ft 标准集装箱</option>
              <option value="20ft-H">20ft 高柜集装箱</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">集装箱内簇数</label>
            <input v-model.number="batteryConfig.clustersPerContainer" type="number"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 outline-none">
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">单个集装箱能量 (MWh)</label>
            <input v-model.number="batteryConfig.containerEnergy" type="number" step="0.1"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 outline-none">
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">集装箱数量</label>
            <input v-model.number="batteryConfig.containerQty" type="number"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 outline-none">
          </div>
        </div>
        
        <div class="grid grid-cols-4 gap-3 mt-3">
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">总直流能量 (MWh)</label>
            <input v-model.number="batteryConfig.totalDcEnergy" type="number" readonly
              class="w-full bg-slate-700 border border-slate-600 rounded px-2 py-1 text-xs text-teal-400">
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">直流电压范围 (V)</label>
            <input v-model="batteryConfig.dcVoltageRange" type="text"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 outline-none">
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">最大直流电流 (A)</label>
            <input v-model.number="batteryConfig.maxDcCurrent" type="number"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 outline-none">
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">直流断路器 (A)</label>
            <input v-model.number="batteryConfig.dcBreaker" type="number"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 outline-none">
          </div>
        </div>
      </div>

      <!-- 运行参数 -->
      <div class="bg-slate-800/50 rounded-lg p-4 border border-slate-700 mb-4">
        <h4 class="text-xs text-slate-300 mb-3 font-medium">运行参数（从调研表获取）</h4>
        
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">运行温度 (°C)</label>
            <input v-model.number="batteryConfig.operatingTemp" type="number"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 outline-none">
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">DOD设置 (%)</label>
            <input v-model.number="batteryConfig.dodSet" type="number" min="0" max="100"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 outline-none">
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">设计循环次数/天</label>
            <input v-model.number="batteryConfig.cyclesPerDay" type="number"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 outline-none">
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">放电深度实际 (%)</label>
            <input v-model.number="batteryConfig.actualDod" type="number"
              class="w-full bg-slate-700 border border-slate-600 rounded px-2 py-1 text-xs text-teal-400" readonly>
          </div>
        </div>
      </div>

      <!-- 计算结果 -->
      <div class="bg-slate-800/30 rounded-lg p-4 border border-slate-700">
        <div class="flex items-center justify-between mb-3">
          <h4 class="text-xs text-slate-300 font-medium">电池系统配置结果</h4>
          <button @click="calculateBatteryConfig" class="bg-teal-500 hover:bg-teal-600 text-white text-xs px-3 py-1 rounded">
            计算配置
          </button>
        </div>
        
        <div class="grid grid-cols-6 gap-3">
          <div class="text-center bg-slate-700/50 rounded p-2">
            <div class="text-lg font-bold text-teal-400">{{ batteryConfig.totalDcEnergy.toFixed(1) }}</div>
            <div class="text-[10px] text-slate-500">总直流能量 (MWh)</div>
          </div>
          <div class="text-center bg-slate-700/50 rounded p-2">
            <div class="text-lg font-bold text-sky-400">{{ batteryConfig.containerQty }}</div>
            <div class="text-[10px] text-slate-500">集装箱数量</div>
          </div>
          <div class="text-center bg-slate-700/50 rounded p-2">
            <div class="text-lg font-bold text-emerald-400">{{ totalStrings }}</div>
            <div class="text-[10px] text-slate-500">电池簇总数</div>
          </div>
          <div class="text-center bg-slate-700/50 rounded p-2">
            <div class="text-lg font-bold text-amber-400">{{ batteryConfig.dcVoltageRange }}</div>
            <div class="text-[10px] text-slate-500">电压范围</div>
          </div>
          <div class="text-center bg-slate-700/50 rounded p-2">
            <div class="text-lg font-bold text-rose-400">{{ batteryConfig.maxDcCurrent }}</div>
            <div class="text-[10px] text-slate-500">最大电流 (A)</div>
          </div>
          <div class="text-center bg-slate-700/50 rounded p-2">
            <div class="text-lg font-bold text-purple-400">{{ (batteryConfig.totalDcEnergy * 1000 / batteryConfig.containerEnergy).toFixed(0) }}</div>
            <div class="text-[10px] text-slate-500">簇/集装箱</div>
          </div>
        </div>
        
        <div class="mt-4 flex justify-end gap-2">
          <button @click="resetBatteryConfig" class="bg-slate-700 hover:bg-slate-600 text-slate-300 text-xs px-3 py-1.5 rounded">
            重置
          </button>
          <button @click="applyBatteryConfig" class="bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 hover:to-emerald-600 text-white text-xs px-4 py-1.5 rounded">
            应用配置
          </button>
        </div>
      </div>
    </div>

    <!-- Toast -->
    <div v-if="toast.show" :class="['fixed bottom-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all',
      toast.type === 'success' ? 'bg-emerald-500 text-white' : 'bg-red-500 text-white']">
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, computed } from 'vue'

const emit = defineEmits(['apply-config'])

// Toast
const toast = reactive({ show: false, message: '', type: 'success' })
const showToast = (message, type = 'success') => {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => { toast.show = false }, 3000)
}

// 电池配置
const batteryConfig = reactive({
  // 电芯
  cellType: 'LFP280',
  cellCapacity: 280,
  cellVoltage: 3.2,
  energyDensity: 160,
  cycleLife: 6000,
  
  // 电池簇
  seriesCount: 240,
  parallelCount: 1,
  stringVoltage: 768,
  stringCapacity: 280,
  stringEnergy: 215,
  stringQty: 24,
  
  // 集装箱
  containerSpec: '20ft-H',
  clustersPerContainer: 4,
  containerEnergy: 5,
  containerQty: 10,
  
  // 总计
  totalDcEnergy: 50,
  dcVoltageRange: '672-864V',
  maxDcCurrent: 1500,
  dcBreaker: 2000,
  
  // 运行参数
  operatingTemp: 25,
  dodSet: 90,
  cyclesPerDay: 1,
  actualDod: 90,
})

// 计算簇参数
watch(() => [batteryConfig.seriesCount, batteryConfig.parallelCount, batteryConfig.cellVoltage, batteryConfig.cellCapacity], () => {
  batteryConfig.stringVoltage = batteryConfig.seriesCount * batteryConfig.cellVoltage
  batteryConfig.stringCapacity = batteryConfig.parallelCount * batteryConfig.cellCapacity
  batteryConfig.stringEnergy = (batteryConfig.stringVoltage * batteryConfig.stringCapacity) / 1000
})

// 计算总直流能量
watch(() => [batteryConfig.containerQty, batteryConfig.containerEnergy], () => {
  batteryConfig.totalDcEnergy = batteryConfig.containerQty * batteryConfig.containerEnergy
})

// 计算电池簇总数
const totalStrings = computed(() => {
  return Math.ceil(batteryConfig.containerQty * batteryConfig.clustersPerContainer)
})

// 计算配置
function calculateBatteryConfig() {
  // 验证输入
  if (batteryConfig.containerEnergy <= 0 || batteryConfig.containerQty <= 0) {
    showToast('请检查集装箱配置', 'error')
    return
  }
  
  // 计算簇数量（根据集装箱能量和簇能量）
  const clustersNeeded = Math.ceil((batteryConfig.containerEnergy * 1000) / batteryConfig.stringEnergy)
  batteryConfig.clustersPerContainer = clustersNeeded
  
  // 计算总簇数
  const total = batteryConfig.containerQty * clustersNeeded
  batteryConfig.stringQty = total
  
  // 计算电压范围 (假设单体3.2V, 240串)
  const minVoltage = 240 * 3.0  // SOC低时
  const maxVoltage = 240 * 3.65 // SOC高时
  batteryConfig.dcVoltageRange = `${minVoltage.toFixed(0)}-${maxVoltage.toFixed(0)}V`
  
  // 计算最大直流电流 (假设0.5C放电)
  const maxDischargeCurrent = (batteryConfig.containerEnergy * 1000) / (batteryConfig.dcVoltageRange.split('-')[0] / 2) * 0.5
  batteryConfig.maxDcCurrent = Math.round(maxDischargeCurrent)
  
  // DC断路器选择 (1.2倍过载)
  batteryConfig.dcBreaker = Math.ceil(maxDischargeCurrent * 1.2 / 100) * 100
  
  // 实际DOD
  batteryConfig.actualDod = Math.min(batteryConfig.dodSet, 95)
  
  showToast('电池配置计算完成')
}

// 重置
function resetBatteryConfig() {
  Object.assign(batteryConfig, {
    cellType: 'LFP280',
    cellCapacity: 280,
    cellVoltage: 3.2,
    seriesCount: 240,
    parallelCount: 1,
    clustersPerContainer: 4,
    containerEnergy: 5,
    containerQty: 10,
    totalDcEnergy: 50,
    dodSet: 90,
    cyclesPerDay: 1,
    actualDod: 90,
  })
  showToast('配置已重置')
}

// 应用配置
function applyBatteryConfig() {
  emit('apply-config', {
    ratedEnergy: batteryConfig.containerEnergy,
    containerQty: batteryConfig.containerQty,
    dod: batteryConfig.actualDod,
    cyclesPerDay: batteryConfig.cyclesPerDay,
    temperature: batteryConfig.operatingTemp,
  })
  showToast('电池配置已应用')
}

// 从调研表加载数据
function loadFromSurvey(surveyData) {
  if (surveyData.totalMwh) batteryConfig.containerEnergy = surveyData.totalMwh / surveyData.containerQty || 5
  if (surveyData.tempAvg) batteryConfig.operatingTemp = surveyData.tempAvg
  if (surveyData.cyclesPerDay) batteryConfig.cyclesPerDay = surveyData.cyclesPerDay
  if (surveyData.dod) batteryConfig.dodSet = surveyData.dod * 100
}

// 导出方法
defineExpose({ loadFromSurvey })
</script>

<style scoped>
.battery-dc-design {
  height: 100%;
}
</style>