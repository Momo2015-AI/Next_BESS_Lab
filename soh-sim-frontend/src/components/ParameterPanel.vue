<template>
  <div class="flex-1 overflow-auto bg-slate-900/80 rounded-xl p-4 border border-slate-800/80 space-y-4">
    <div>
      <h2 class="text-sm font-bold text-teal-400 border-l-4 border-teal-500 pl-2 mb-3">系统参数配置</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">标称单舱能量 (MWh)</label>
          <input type="number" :value="params.ratedEnergy" step="0.1" min="0.1" max="20"
            :class="['w-full bg-slate-950 border rounded px-2 py-1.5 text-teal-300 font-mono focus:outline-none',
              errors.ratedEnergy ? 'border-red-500 focus:border-red-500' : 'border-slate-700 focus:border-teal-500']"
            @input="validateAndUpdate('ratedEnergy', Number($event.target.value), { min: 0.1, max: 20 })">
          <p v-if="errors.ratedEnergy" class="text-[10px] text-red-400 mt-0.5">{{ errors.ratedEnergy }}</p>
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">初始集装箱数量 (台)</label>
          <input type="number" :value="params.initContainerQty" step="1" min="1" max="200"
            :class="['w-full bg-slate-950 border rounded px-2 py-1.5 text-teal-300 font-mono focus:outline-none',
              errors.initContainerQty ? 'border-red-500 focus:border-red-500' : 'border-slate-700 focus:border-teal-500']"
            @input="validateAndUpdate('initContainerQty', Number($event.target.value), { min: 1, max: 200 })">
          <p v-if="errors.initContainerQty" class="text-[10px] text-red-400 mt-0.5">{{ errors.initContainerQty }}</p>
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">PCS变流数量 (台)</label>
          <input type="number" :value="params.initPcsQty" step="1" min="1" max="50"
            :class="['w-full bg-slate-950 border rounded px-2 py-1.5 text-teal-300 font-mono focus:outline-none',
              errors.initPcsQty ? 'border-red-500 focus:border-red-500' : 'border-slate-700 focus:border-teal-500']"
            @input="validateAndUpdate('initPcsQty', Number($event.target.value), { min: 1, max: 50 })">
          <p v-if="errors.initPcsQty" class="text-[10px] text-red-400 mt-0.5">{{ errors.initPcsQty }}</p>
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">单程充电时间 (h)</label>
          <input type="number" :value="params.duration" step="0.5" min="0.5" max="12"
            :class="['w-full bg-slate-950 border rounded px-2 py-1.5 text-teal-300 font-mono focus:outline-none',
              errors.duration ? 'border-red-500 focus:border-red-500' : 'border-slate-700 focus:border-teal-500']"
            @input="validateAndUpdate('duration', Number($event.target.value), { min: 0.5, max: 12 })">
          <p v-if="errors.duration" class="text-[10px] text-red-400 mt-0.5">{{ errors.duration }}</p>
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">单日循环次数 (次)</label>
          <input type="number" :value="params.cyclesPerDay" step="1" min="0.5" max="4"
            :class="['w-full bg-slate-950 border rounded px-2 py-1.5 text-teal-300 font-mono focus:outline-none',
              errors.cyclesPerDay ? 'border-red-500 focus:border-red-500' : 'border-slate-700 focus:border-teal-500']"
            @input="validateAndUpdate('cyclesPerDay', Number($event.target.value), { min: 0.5, max: 4 })">
          <p v-if="errors.cyclesPerDay" class="text-[10px] text-red-400 mt-0.5">{{ errors.cyclesPerDay }}</p>
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">网侧AC效率 (%)</label>
          <input type="number" :value="params.acEfficiency" step="0.01" min="90" max="99"
            :class="['w-full bg-slate-950 border rounded px-2 py-1.5 text-teal-300 font-mono focus:outline-none',
              errors.acEfficiency ? 'border-red-500 focus:border-red-500' : 'border-slate-700 focus:border-teal-500']"
            @input="validateAndUpdate('acEfficiency', Number($event.target.value), { min: 90, max: 99 })">
          <p v-if="errors.acEfficiency" class="text-[10px] text-red-400 mt-0.5">{{ errors.acEfficiency }}</p>
        </div>
      </div>
    </div>

    <div>
      <h2 class="text-sm font-bold text-amber-400 border-l-4 border-amber-500 pl-2 mb-3">自辅耗功率设定</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">集装箱运行功率 (kW)</label>
          <input type="number" :value="params.bessAuxRun" step="0.001" min="0" max="50"
            :class="['w-full bg-slate-950 border rounded px-2 py-1.5 text-amber-300 font-mono focus:outline-none',
              errors.bessAuxRun ? 'border-red-500 focus:border-red-500' : 'border-amber-900/60 focus:border-amber-500']"
            @input="validateAndUpdate('bessAuxRun', Number($event.target.value), { min: 0, max: 50 })">
          <p v-if="errors.bessAuxRun" class="text-[10px] text-red-400 mt-0.5">{{ errors.bessAuxRun }}</p>
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">集装箱待机功率 (kW)</label>
          <input type="number" :value="params.bessAuxStandby" step="0.1" min="0" max="20"
            :class="['w-full bg-slate-950 border rounded px-2 py-1.5 text-amber-300 font-mono focus:outline-none',
              errors.bessAuxStandby ? 'border-red-500 focus:border-red-500' : 'border-amber-900/60 focus:border-amber-500']"
            @input="validateAndUpdate('bessAuxStandby', Number($event.target.value), { min: 0, max: 20 })">
          <p v-if="errors.bessAuxStandby" class="text-[10px] text-red-400 mt-0.5">{{ errors.bessAuxStandby }}</p>
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">PCS运行功率 (kW)</label>
          <input type="number" :value="params.pcsAuxRun" step="0.1" min="0" max="30"
            :class="['w-full bg-slate-950 border rounded px-2 py-1.5 text-amber-300 font-mono focus:outline-none',
              errors.pcsAuxRun ? 'border-red-500 focus:border-red-500' : 'border-amber-900/60 focus:border-amber-500']"
            @input="validateAndUpdate('pcsAuxRun', Number($event.target.value), { min: 0, max: 30 })">
          <p v-if="errors.pcsAuxRun" class="text-[10px] text-red-400 mt-0.5">{{ errors.pcsAuxRun }}</p>
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">PCS待机功率 (kW)</label>
          <input type="number" :value="params.pcsAuxStandby" step="0.1" min="0" max="10"
            :class="['w-full bg-slate-950 border rounded px-2 py-1.5 text-amber-300 font-mono focus:outline-none',
              errors.pcsAuxStandby ? 'border-red-500 focus:border-red-500' : 'border-amber-900/60 focus:border-amber-500']"
            @input="validateAndUpdate('pcsAuxStandby', Number($event.target.value), { min: 0, max: 10 })">
          <p v-if="errors.pcsAuxStandby" class="text-[10px] text-red-400 mt-0.5">{{ errors.pcsAuxStandby }}</p>
        </div>
      </div>

      <div class="mt-3 p-3 bg-slate-950 border border-slate-800 rounded-lg font-mono text-[11px] text-slate-300 space-y-1">
        <div class="text-amber-400 font-bold text-[10px]">自辅耗时轴计算推导：</div>
        <div>
          日运行总时长 = {{ params.duration }}h × {{ params.cyclesPerDay }}次 = <span class="text-sky-300 font-bold">{{ (params.duration * params.cyclesPerDay).toFixed(1) }}h</span>
          &nbsp;日待机时长 = Max(0, 24 - {{ (params.duration * params.cyclesPerDay).toFixed(1) }}) = <span class="text-sky-300 font-bold">{{ Math.max(0, 24 - params.duration * params.cyclesPerDay).toFixed(1) }}h</span>
        </div>
        <div>
          单舱日辅耗 = ({{ params.bessAuxRun }}kW × {{ (params.duration * params.cyclesPerDay).toFixed(1) }}h + {{ params.bessAuxStandby }}kW × {{ Math.max(0, 24 - params.duration * params.cyclesPerDay).toFixed(1) }}h) / 1000
          = <span class="text-amber-300 font-bold">{{ ((params.bessAuxRun * params.duration * params.cyclesPerDay + params.bessAuxStandby * Math.max(0, 24 - params.duration * params.cyclesPerDay)) / 1000).toFixed(3) }} MWh/天</span>
        </div>
        <div>
          单PCS日辅耗 = ({{ params.pcsAuxRun }}kW × {{ (params.duration * params.cyclesPerDay).toFixed(1) }}h + {{ params.pcsAuxStandby }}kW × {{ Math.max(0, 24 - params.duration * params.cyclesPerDay).toFixed(1) }}h) / 1000
          = <span class="text-amber-300 font-bold">{{ ((params.pcsAuxRun * params.duration * params.cyclesPerDay + params.pcsAuxStandby * Math.max(0, 24 - params.duration * params.cyclesPerDay)) / 1000).toFixed(3) }} MWh/天</span>
        </div>
        <div class="pt-1 border-t border-slate-800">
          单次循环总自辅耗 = <span class="text-emerald-300 font-bold">
            ({{ params.initContainerQty }}台 × 单舱日辅耗 + {{ params.initPcsQty }}台 × 单PCS日辅耗) / {{ params.cyclesPerDay }}次
          </span>
        </div>
      </div>
    </div>

    <!-- 配置规则区域 -->
    <div>
      <h2 class="text-sm font-bold text-sky-400 border-l-4 border-sky-500 pl-2 mb-3">⚡ 电池与PCS配置规则</h2>
      <div class="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
        <div class="grid grid-cols-3 gap-4 mb-4">
          <div class="bg-slate-900/50 rounded p-3">
            <div class="text-xs text-sky-400 mb-2 font-medium">功率配比规则</div>
            <div class="text-[10px] text-slate-400 space-y-1">
              <div>• 2h储能: <span class="text-sky-300">能量 = 2 × 功率</span></div>
              <div>• 4h储能: <span class="text-sky-300">能量 = 4 × 功率</span></div>
              <div>• 常用配比: <span class="text-sky-300">1:2 (功率:能量)</span></div>
            </div>
          </div>
          <div class="bg-slate-900/50 rounded p-3">
            <div class="text-xs text-teal-400 mb-2 font-medium">集装箱与PCS对应规则</div>
            <div class="text-[10px] text-slate-400 space-y-1">
              <div>• 5MWh + 0.5C放电 → <span class="text-teal-300">2台 2.5MW PCS</span></div>
              <div>• 10MWh + 0.5C放电 → <span class="text-teal-300">2台 5MW PCS</span></div>
              <div>• 20MWh + 0.5C放电 → <span class="text-teal-300">4台 5MW PCS</span></div>
            </div>
          </div>
          <div class="bg-slate-900/50 rounded p-3">
            <div class="text-xs text-amber-400 mb-2 font-medium">计算公式</div>
            <div class="text-[10px] text-slate-400 space-y-1">
              <div>PCS数量 = 能量 ÷ (放电时长 × 单台功率)</div>
              <div>变压器 = PCS总量 ÷ 并机数 × 1.1</div>
            </div>
          </div>
        </div>

        <div class="flex items-center gap-4 p-3 bg-sky-900/30 rounded border border-sky-800/50">
          <div class="text-xs text-sky-300">
            当前: <span class="font-bold">{{ params.initContainerQty }}</span>台 × <span class="font-bold">{{ params.ratedEnergy }}</span>MWh = <span class="font-bold text-sky-200">{{ (params.initContainerQty * params.ratedEnergy).toFixed(1) }}</span> MWh
          </div>
          <div class="text-slate-500">→</div>
          <div class="text-xs text-teal-300">
            建议PCS: <span class="font-bold">{{ Math.ceil((params.initContainerQty * params.ratedEnergy) / (params.duration * 5)) }}</span> 台 5MW
          </div>
          <div class="text-slate-500">→</div>
          <div class="text-xs text-amber-300">
            配比: <span class="font-bold">1:{{ ((params.initContainerQty * params.ratedEnergy) / (Math.ceil((params.initContainerQty * params.ratedEnergy) / (params.duration * 5)) * 5)).toFixed(1) }}</span>
          </div>
        </div>

        <button @click="autoMatchPCS" class="mt-3 bg-sky-500 hover:bg-sky-600 text-white text-xs px-4 py-2 rounded transition-colors">
          根据配置规则自动匹配PCS
        </button>
      </div>
    </div>

    <div>
      <h2 class="text-sm font-bold text-pink-400 border-l-4 border-pink-500 pl-2 mb-3">仿真条件边界</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">运行平均温度 (°C)</label>
          <input type="number" value="25" step="1" disabled
            class="w-full bg-slate-900 border border-slate-800 rounded px-2 py-1.5 text-slate-500 font-mono cursor-not-allowed">
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">平均放电倍率</label>
          <input type="number" value="0.5" step="0.1" disabled
            class="w-full bg-slate-900 border border-slate-800 rounded px-2 py-1.5 text-slate-500 font-mono cursor-not-allowed">
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">SOH/RTE起始年份</label>
          <input type="text" value="FOB + 6个月" disabled
            class="w-full bg-slate-900 border border-slate-800 rounded px-2 py-1.5 text-slate-500 font-mono cursor-not-allowed">
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">承诺保障线 (MWh/次)</label>
          <input type="number" :value="params.requiredEnergy" step="1" min="50" max="500"
            :class="['w-full bg-slate-950 border rounded px-2 py-1.5 text-emerald-300 font-mono focus:outline-none',
              errors.requiredEnergy ? 'border-red-500 focus:border-red-500' : 'border-emerald-900/60 focus:border-emerald-500']"
            @input="validateAndUpdate('requiredEnergy', Number($event.target.value), { min: 50, max: 500 })">
          <p v-if="errors.requiredEnergy" class="text-[10px] text-red-400 mt-0.5">{{ errors.requiredEnergy }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const props = defineProps({ params: Object })
const emit = defineEmits(['update', 'error'])

const errors = reactive({
  ratedEnergy: '',
  initContainerQty: '',
  initPcsQty: '',
  duration: '',
  cyclesPerDay: '',
  acEfficiency: '',
  bessAuxRun: '',
  bessAuxStandby: '',
  pcsAuxRun: '',
  pcsAuxStandby: '',
  requiredEnergy: '',
})

const validationRules = {
  ratedEnergy: { min: 0.1, max: 20, label: '标称单舱能量' },
  initContainerQty: { min: 1, max: 200, label: '初始集装箱数量' },
  initPcsQty: { min: 1, max: 50, label: 'PCS变流数量' },
  duration: { min: 0.5, max: 12, label: '单程充电时间' },
  cyclesPerDay: { min: 0.5, max: 4, label: '单日循环次数' },
  acEfficiency: { min: 90, max: 99, label: '网侧AC效率' },
  bessAuxRun: { min: 0, max: 50, label: '集装箱运行功率' },
  bessAuxStandby: { min: 0, max: 20, label: '集装箱待机功率' },
  pcsAuxRun: { min: 0, max: 30, label: 'PCS运行功率' },
  pcsAuxStandby: { min: 0, max: 10, label: 'PCS待机功率' },
  requiredEnergy: { min: 50, max: 500, label: '承诺保障线' },
}

const validateAndUpdate = (key, value, rule) => {
  // 验证
  if (value === '' || value === null || value === undefined) {
    errors[key] = `${validationRules[key].label}不能为空`
    emit('error', errors[key], 'error')
    return
  }
  
  if (value < rule.min) {
    errors[key] = `${validationRules[key].label}不能小于${rule.min}`
    emit('error', errors[key], 'error')
    return
  }
  
  if (value > rule.max) {
    errors[key] = `${validationRules[key].label}不能大于${rule.max}`
    emit('error', errors[key], 'error')
    return
  }
  
  // 验证通过，清除错误
  errors[key] = ''

  // 更新参数
  emit('update', key, value)
}

// 自动匹配PCS
const autoMatchPCS = () => {
  const totalEnergy = props.params.initContainerQty * props.params.ratedEnergy
  const pcsQty = Math.ceil(totalEnergy / (props.params.duration * 5))
  emit('update', 'initPcsQty', pcsQty)
}
</script>
