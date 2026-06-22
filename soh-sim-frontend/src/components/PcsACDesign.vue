<template>
  <div class="pcs-ac-design h-full overflow-auto p-4">
    <div class="bg-slate-900/60 rounded-lg border border-slate-800 p-4">
      <h3 class="text-sm font-bold text-sky-400 mb-4 flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-sky-400"></span>
        交流侧设计（PCS系统）
      </h3>

      <!-- PCS选型 -->
      <div class="grid grid-cols-2 gap-4 mb-4">
        <div class="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
          <h4 class="text-xs text-slate-300 mb-3 font-medium">PCS功率选型</h4>
          
          <div class="space-y-3">
            <div>
              <label class="text-[10px] text-slate-500 block mb-1">PCS型号</label>
              <select v-model="pcsConfig.pcsModel" @change="onPcsModelChange"
                class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1.5 text-xs focus:border-sky-500 outline-none">
                <option value="">请选择PCS型号</option>
                <option v-for="pcs in pcsLibrary" :key="pcs.id" :value="pcs.model">
                  {{ pcs.model }} - {{ pcs.mfr }} ({{ pcs.ratedPowerMW }}MW)
                </option>
              </select>
            </div>
            
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] text-slate-500 block mb-1">PCS单机功率 (MW)</label>
                <input v-model.number="pcsConfig.pcsPower" type="number" step="0.001"
                  class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-sky-500 outline-none">
              </div>
              <div>
                <label class="text-[10px] text-slate-500 block mb-1">效率 (%)</label>
                <input v-model.number="pcsConfig.efficiency" type="number" step="0.1"
                  class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-sky-500 outline-none">
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] text-slate-500 block mb-1">直流电压范围 (V)</label>
                <input v-model="pcsConfig.dcVoltageRange" type="text" readonly
                  class="w-full bg-slate-700 border border-slate-600 rounded px-2 py-1 text-xs text-sky-400">
              </div>
              <div>
                <label class="text-[10px] text-slate-500 block mb-1">直流最大电流 (A)</label>
                <input v-model.number="pcsConfig.maxDcCurrent" type="number"
                  class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-sky-500 outline-none">
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] text-slate-500 block mb-1">交流额定功率 (kW)</label>
                <input v-model.number="pcsConfig.acRatedPower" type="number" readonly
                  class="w-full bg-slate-700 border border-slate-600 rounded px-2 py-1 text-xs text-sky-400">
              </div>
              <div>
                <label class="text-[10px] text-slate-500 block mb-1">额定交流电流 (A)</label>
                <input v-model.number="pcsConfig.acRatedCurrent" type="number" readonly
                  class="w-full bg-slate-700 border border-slate-600 rounded px-2 py-1 text-xs text-sky-400">
              </div>
            </div>
          </div>
        </div>

        <div class="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
          <h4 class="text-xs text-slate-300 mb-3 font-medium">PCS数量配置</h4>
          
          <div class="space-y-3">
            <div>
              <label class="text-[10px] text-slate-500 block mb-1">PCS数量计算方式</label>
              <select v-model="pcsConfig.calcMode" class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1.5 text-xs focus:border-sky-500 outline-none">
                <option value="ratio">按功率配比计算</option>
                <option value="fixed">固定数量</option>
                <option value="energy">按能量需求</option>
              </select>
            </div>
            
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] text-slate-500 block mb-1">PCS数量</label>
                <input v-model.number="pcsConfig.pcsQty" type="number"
                  class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-sky-500 outline-none">
              </div>
              <div>
                <label class="text-[10px] text-slate-500 block mb-1">并机数量</label>
                <input v-model.number="pcsConfig.parallelCount" type="number"
                  class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-sky-500 outline-none">
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="text-[10px] text-slate-500 block mb-1">总PCS功率 (MW)</label>
                <input v-model.number="pcsConfig.totalPcsPower" type="number" readonly
                  class="w-full bg-slate-700 border border-slate-600 rounded px-2 py-1 text-xs text-sky-400">
              </div>
              <div>
                <label class="text-[10px] text-slate-500 block mb-1">功率配比</label>
                <input v-model.number="pcsConfig.powerRatio" type="number" step="0.1"
                  class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-sky-500 outline-none">
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 变压器配置 -->
      <div class="bg-slate-800/50 rounded-lg p-4 border border-slate-700 mb-4">
        <h4 class="text-xs text-slate-300 mb-3 font-medium">变压器与电网连接</h4>
        
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">变压器类型</label>
            <select v-model="pcsConfig.transformerType" class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-sky-500 outline-none">
              <option value="2w">两绕组变压器</option>
              <option value="3w">三绕组变压器</option>
              <option value="一体化">一体化升压装置</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">变压器容量 (MVA)</label>
            <input v-model.number="pcsConfig.transformerCapacity" type="number"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-sky-500 outline-none">
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">变压器数量</label>
            <input v-model.number="pcsConfig.transformerQty" type="number"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-sky-500 outline-none">
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">高压侧电压 (kV)</label>
            <input v-model.number="pcsConfig.hvVoltage" type="number"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-sky-500 outline-none">
          </div>
        </div>
        
        <div class="grid grid-cols-4 gap-3 mt-3">
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">低压侧电压 (V)</label>
            <input v-model.number="pcsConfig.lvVoltage" type="number"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-sky-500 outline-none">
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">短路阻抗 (%)</label>
            <input v-model.number="pcsConfig.impedance" type="number" step="0.1"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-sky-500 outline-none">
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">接线方式</label>
            <select v-model="pcsConfig.connection" class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-sky-500 outline-none">
              <option value="Dynd11">Dyn11</option>
              <option value="Ynd11">Ynd11</option>
              <option value="Yyn0">Yyn0</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">接地方式</label>
            <select v-model="pcsConfig.grounding" class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-sky-500 outline-none">
              <option value="直接接地">直接接地</option>
              <option value="消弧线圈">消弧线圈</option>
              <option value="电阻接地">电阻接地</option>
            </select>
          </div>
        </div>
      </div>

      <!-- 运行参数 -->
      <div class="bg-slate-800/50 rounded-lg p-4 border border-slate-700 mb-4">
        <h4 class="text-xs text-slate-300 mb-3 font-medium">PCS运行参数</h4>
        
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">PCS效率 (%)</label>
            <input v-model.number="pcsConfig.pcsEfficiency" type="number" step="0.1"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-sky-500 outline-none">
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">运行辅耗 (kW)</label>
            <input v-model.number="pcsConfig.auxConsumption" type="number"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-sky-500 outline-none">
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">待机辅耗 (kW)</label>
            <input v-model.number="pcsConfig.standbyConsumption" type="number"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-sky-500 outline-none">
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">功率因数</label>
            <input v-model.number="pcsConfig.powerFactor" type="number" step="0.01"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-sky-500 outline-none">
          </div>
        </div>
      </div>

      <!-- 配置规则 -->
      <div class="bg-slate-800/50 rounded-lg p-4 border border-slate-700 mb-4">
        <h4 class="text-xs text-amber-400 mb-3 font-medium">⚡ PCS与电池配置规则</h4>
        
        <div class="grid grid-cols-2 gap-4">
          <div class="bg-slate-900/50 rounded p-3">
            <div class="text-xs text-slate-300 mb-2">常用配置规则（基于0.5C放电）</div>
            <div class="space-y-1 text-[10px]">
              <div class="flex justify-between">
                <span class="text-slate-500">5MWh集装箱</span>
                <span class="text-sky-400">→ 2台 2.5MW PCS</span>
              </div>
              <div class="flex justify-between">
                <span class="text-slate-500">10MWh集装箱</span>
                <span class="text-sky-400">→ 2台 5MW PCS</span>
              </div>
              <div class="flex justify-between">
                <span class="text-slate-500">20MWh集装箱</span>
                <span class="text-sky-400">→ 4台 5MW PCS</span>
              </div>
            </div>
          </div>
          <div class="bg-slate-900/50 rounded p-3">
            <div class="text-xs text-slate-300 mb-2">功率配比计算</div>
            <div class="text-[10px] text-slate-400">
              PCS总功率 = 电池总能量 ÷ 放电时长<br>
              例：100MWh ÷ 2h = 50MW PCS<br>
              配比：1:2 (能量:功率)
            </div>
          </div>
        </div>
        
        <button @click="applyConfigRules" class="mt-3 bg-amber-500 hover:bg-amber-600 text-white text-xs px-3 py-1.5 rounded">
          根据电池配置自动计算PCS
        </button>
      </div>

      <!-- 配置结果 -->
      <div class="bg-slate-800/30 rounded-lg p-4 border border-slate-700">
        <div class="flex items-center justify-between mb-3">
          <h4 class="text-xs text-slate-300 font-medium">PCS系统配置结果</h4>
          <button @click="calculatePcsConfig" class="bg-sky-500 hover:bg-sky-600 text-white text-xs px-3 py-1 rounded">
            计算配置
          </button>
        </div>
        
        <div class="grid grid-cols-6 gap-3">
          <div class="text-center bg-slate-700/50 rounded p-2">
            <div class="text-lg font-bold text-sky-400">{{ pcsConfig.pcsQty }}</div>
            <div class="text-[10px] text-slate-500">PCS数量</div>
          </div>
          <div class="text-center bg-slate-700/50 rounded p-2">
            <div class="text-lg font-bold text-teal-400">{{ pcsConfig.totalPcsPower.toFixed(1) }}</div>
            <div class="text-[10px] text-slate-500">总PCS功率 (MW)</div>
          </div>
          <div class="text-center bg-slate-700/50 rounded p-2">
            <div class="text-lg font-bold text-emerald-400">{{ pcsConfig.powerRatio.toFixed(1) }}:1</div>
            <div class="text-[10px] text-slate-500">功率配比</div>
          </div>
          <div class="text-center bg-slate-700/50 rounded p-2">
            <div class="text-lg font-bold text-amber-400">{{ pcsConfig.transformerQty }}</div>
            <div class="text-[10px] text-slate-500">变压器数量</div>
          </div>
          <div class="text-center bg-slate-700/50 rounded p-2">
            <div class="text-lg font-bold text-purple-400">{{ pcsConfig.transformerCapacity }}MVA</div>
            <div class="text-[10px] text-slate-500">单台变压器容量</div>
          </div>
          <div class="text-center bg-slate-700/50 rounded p-2">
            <div class="text-lg font-bold text-rose-400">{{ pcsConfig.pcsEfficiency }}%</div>
            <div class="text-[10px] text-slate-500">PCS效率</div>
          </div>
        </div>
        
        <div class="mt-4 flex justify-end gap-2">
          <button @click="resetPcsConfig" class="bg-slate-700 hover:bg-slate-600 text-slate-300 text-xs px-3 py-1.5 rounded">
            重置
          </button>
          <button @click="applyPcsConfig" class="bg-gradient-to-r from-sky-500 to-blue-500 hover:from-sky-600 hover:to-blue-600 text-white text-xs px-4 py-1.5 rounded">
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
import { ref, reactive, watch, computed, onMounted } from 'vue'

const emit = defineEmits(['apply-config'])

// PCS库数据
const pcsLibrary = ref([])

// Toast
const toast = reactive({ show: false, message: '', type: 'success' })
const showToast = (message, type = 'success') => {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => { toast.show = false }, 3000)
}

// 加载PCS库数据
async function loadPcsLibrary() {
  try {
    const response = await fetch('/api/library/pcs')
    const data = await response.json()
    if (data.success) {
      pcsLibrary.value = data.data || []
      // 如果PCS库为空，尝试初始化
      if (pcsLibrary.value.length === 0) {
        await seedLibrary()
      }
    }
  } catch (error) {
    console.error('加载PCS库失败:', error)
  }
}

// 初始化产品库
async function seedLibrary() {
  try {
    const response = await fetch('/api/library/seed', { method: 'POST' })
    const data = await response.json()
    if (data.success) {
      await loadPcsLibrary()
      showToast('产品库初始化成功')
    }
  } catch (error) {
    console.error('初始化产品库失败:', error)
  }
}

// PCS型号变更时自动填充参数
function onPcsModelChange() {
  const selectedPcs = pcsLibrary.value.find(p => p.model === pcsConfig.pcsModel)
  if (selectedPcs) {
    pcsConfig.pcsPower = selectedPcs.ratedPowerMW
    pcsConfig.efficiency = selectedPcs.efficiency
    pcsConfig.dcVoltageRange = selectedPcs.dcVoltageRange
    pcsConfig.maxDcCurrent = selectedPcs.maxDcCurrent
  }
}

// PCS配置
const pcsConfig = reactive({
  // PCS选型
  pcsModel: '',
  pcsPower: 5,
  efficiency: 99,
  dcVoltageRange: '672-864V',
  maxDcCurrent: 1500,
  acRatedPower: 5000,
  acRatedCurrent: 5774,
  
  // 数量配置
  calcMode: 'ratio',
  pcsQty: 10,
  parallelCount: 1,
  totalPcsPower: 50,
  powerRatio: 1.0, // 能量:功率 = 1:ratio
  
  // 变压器
  transformerType: '一体化',
  transformerCapacity: 6.3,
  transformerQty: 5,
  hvVoltage: 35,
  lvVoltage: 690,
  impedance: 10.5,
  connection: 'Dyn11',
  grounding: '电阻接地',
  
  // 运行参数
  pcsEfficiency: 99,
  auxConsumption: 6.5,
  standbyConsumption: 1.0,
  powerFactor: 0.95,
})

// 接收外部电池参数
let externalBatteryConfig = reactive({
  totalEnergy: 50,
  containerQty: 10,
  containerEnergy: 5,
})

// 计算PCS总额定功率
watch(() => [pcsConfig.pcsQty, pcsConfig.pcsPower], () => {
  pcsConfig.totalPcsPower = pcsConfig.pcsQty * pcsConfig.pcsPower
})

// 计算变压器配置
watch(() => pcsConfig.totalPcsPower, () => {
  // 每5MW配置一台6.3MVA变压器
  pcsConfig.transformerQty = Math.ceil(pcsConfig.totalPcsPower / 5)
  pcsConfig.transformerCapacity = 6.3
})

// 根据电池配置自动计算PCS
function applyConfigRules() {
  const batteryEnergy = externalBatteryConfig.totalEnergy
  const dischargeHours = 2 // 默认2小时放电
  
  // 计算需要的PCS功率
  const requiredPower = batteryEnergy / dischargeHours
  
  // 计算功率配比（保持为数字）
  pcsConfig.powerRatio = parseFloat((batteryEnergy / requiredPower).toFixed(1))
  
  // 计算PCS数量
  pcsConfig.pcsQty = Math.ceil(requiredPower / pcsConfig.pcsPower)
  pcsConfig.totalPcsPower = pcsConfig.pcsQty * pcsConfig.pcsPower
  
  // 计算变压器
  pcsConfig.transformerQty = Math.ceil(pcsConfig.totalPcsPower / 5)
  
  showToast('PCS配置已根据电池参数自动计算')
}

// 计算配置
function calculatePcsConfig() {
  // 验证
  if (pcsConfig.totalPcsPower <= 0) {
    showToast('请检查PCS配置', 'error')
    return
  }
  
  // 交流额定电流计算
  pcsConfig.acRatedCurrent = Math.round((pcsConfig.totalPcsPower * 1000) / (1.732 * 0.69 * pcsConfig.powerFactor))
  
  // 更新变压器容量（考虑过载）
  pcsConfig.transformerCapacity = Math.ceil(pcsConfig.totalPcsPower / pcsConfig.transformerQty * 1.1 * 10) / 10
  
  showToast('PCS配置计算完成')
}

// 重置
function resetPcsConfig() {
  Object.assign(pcsConfig, {
    pcsPower: 5,
    pcsQty: 10,
    totalPcsPower: 50,
    powerRatio: 1.0,
    transformerType: '一体化',
    transformerCapacity: 6.3,
    transformerQty: 5,
    pcsEfficiency: 99,
    auxConsumption: 6.5,
    standbyConsumption: 1.0,
  })
  showToast('配置已重置')
}

// 应用配置
function applyPcsConfig() {
  emit('apply-config', {
    pcsPower: pcsConfig.pcsPower,
    pcsQty: pcsConfig.pcsQty,
    totalPcsPower: pcsConfig.totalPcsPower,
    powerRatio: pcsConfig.powerRatio,
    acEfficiency: pcsConfig.pcsEfficiency,
    pcsAuxRun: pcsConfig.auxConsumption,
    pcsAuxStandby: pcsConfig.standbyConsumption,
  })
  showToast('PCS配置已应用')
}

// 设置外部电池配置（从参数配置面板调用）
function setBatteryConfig(config) {
  externalBatteryConfig.totalEnergy = config.totalEnergy || 50
  externalBatteryConfig.containerQty = config.containerQty || 10
  externalBatteryConfig.containerEnergy = config.containerEnergy || 5
}

// 组件挂载时加载PCS库
onMounted(() => {
  loadPcsLibrary()
})

// 导出方法
defineExpose({ setBatteryConfig, applyConfigRules })
</script>

<style scoped>
.pcs-ac-design {
  height: 100%;
}
</style>