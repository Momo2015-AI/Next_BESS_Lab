<template>
  <div class="flex-1 overflow-auto rounded-xl p-4 space-y-4 card">
    <div>
      <h2 class="section-title" style="color: var(--color-accent); border-color: var(--color-accent);">{{ $t('paramPanel.systemParams') }}</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
        <div>
          <label class="label-text">{{ $t('paramPanel.ratedEnergy') }}</label>
          <input type="number" :value="params.ratedEnergy" step="0.1"
            :class="['input-field',
              errors.ratedEnergy ? 'border-red-500 focus:border-red-500' : '']"
            @input="validateAndUpdate('ratedEnergy', Number($event.target.value), validationRules.ratedEnergy)">
          <p v-if="errors.ratedEnergy" class="text-[10px] text-red-400 mt-0.5">{{ errors.ratedEnergy }}</p>
        </div>
        <div>
          <label class="label-text">{{ $t('paramPanel.initContainerQty') }}</label>
          <input type="number" :value="params.initContainerQty" step="1"
            :class="['input-field',
              errors.initContainerQty ? 'border-red-500 focus:border-red-500' : '']"
            @input="validateAndUpdate('initContainerQty', Number($event.target.value), validationRules.initContainerQty)">
          <p v-if="errors.initContainerQty" class="text-[10px] text-red-400 mt-0.5">{{ errors.initContainerQty }}</p>
        </div>
        <div>
          <label class="label-text">{{ $t('paramPanel.initPcsQty') }}</label>
          <input type="number" :value="params.initPcsQty" step="1"
            :class="['input-field',
              errors.initPcsQty ? 'border-red-500 focus:border-red-500' : '']"
            @input="validateAndUpdate('initPcsQty', Number($event.target.value), validationRules.initPcsQty)">
          <p v-if="errors.initPcsQty" class="text-[10px] text-red-400 mt-0.5">{{ errors.initPcsQty }}</p>
        </div>
        <div>
          <label class="label-text">{{ $t('paramPanel.duration') }}</label>
          <input type="number" :value="params.duration" step="0.5"
            :class="['input-field',
              errors.duration ? 'border-red-500 focus:border-red-500' : '']"
            @input="validateAndUpdate('duration', Number($event.target.value), validationRules.duration)">
          <p v-if="errors.duration" class="text-[10px] text-red-400 mt-0.5">{{ errors.duration }}</p>
        </div>
        <div>
          <label class="label-text">{{ $t('paramPanel.cyclesPerDay') }}</label>
          <input type="number" :value="params.cyclesPerDay" step="1"
            :class="['input-field',
              errors.cyclesPerDay ? 'border-red-500 focus:border-red-500' : '']"
            @input="validateAndUpdate('cyclesPerDay', Number($event.target.value), validationRules.cyclesPerDay)">
          <p v-if="errors.cyclesPerDay" class="text-[10px] text-red-400 mt-0.5">{{ errors.cyclesPerDay }}</p>
        </div>
        <div>
          <label class="label-text">{{ $t('paramPanel.acEfficiency') }}</label>
          <input type="number" :value="params.acEfficiency" step="0.01"
            :class="['input-field',
              errors.acEfficiency ? 'border-red-500 focus:border-red-500' : '']"
            @input="validateAndUpdate('acEfficiency', Number($event.target.value), validationRules.acEfficiency)">
          <p v-if="errors.acEfficiency" class="text-[10px] text-red-400 mt-0.5">{{ errors.acEfficiency }}</p>
        </div>
      </div>
    </div>

    <div>
      <h2 class="section-title" style="color: #f59e0b; border-color: #f59e0b;">{{ $t('paramPanel.auxPower') }}</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div>
          <label class="label-text">{{ $t('paramPanel.bessAuxRun') }}</label>
          <input type="number" :value="params.bessAuxRun" step="0.001"
            :class="['input-field', inputAuxStyle,
              errors.bessAuxRun ? 'border-red-500 focus:border-red-500' : '']"
            @input="validateAndUpdate('bessAuxRun', Number($event.target.value), validationRules.bessAuxRun)">
          <p v-if="errors.bessAuxRun" class="text-[10px] text-red-400 mt-0.5">{{ errors.bessAuxRun }}</p>
        </div>
        <div>
          <label class="label-text">{{ $t('paramPanel.bessAuxStandby') }}</label>
          <input type="number" :value="params.bessAuxStandby" step="0.1"
            :class="['input-field', inputAuxStyle,
              errors.bessAuxStandby ? 'border-red-500 focus:border-red-500' : '']"
            @input="validateAndUpdate('bessAuxStandby', Number($event.target.value), validationRules.bessAuxStandby)">
          <p v-if="errors.bessAuxStandby" class="text-[10px] text-red-400 mt-0.5">{{ errors.bessAuxStandby }}</p>
        </div>
        <div>
          <label class="label-text">{{ $t('paramPanel.pcsAuxRun') }}</label>
          <input type="number" :value="params.pcsAuxRun" step="0.1"
            :class="['input-field', inputAuxStyle,
              errors.pcsAuxRun ? 'border-red-500 focus:border-red-500' : '']"
            @input="validateAndUpdate('pcsAuxRun', Number($event.target.value), validationRules.pcsAuxRun)">
          <p v-if="errors.pcsAuxRun" class="text-[10px] text-red-400 mt-0.5">{{ errors.pcsAuxRun }}</p>
        </div>
        <div>
          <label class="label-text">{{ $t('paramPanel.pcsAuxStandby') }}</label>
          <input type="number" :value="params.pcsAuxStandby" step="0.1"
            :class="['input-field', inputAuxStyle,
              errors.pcsAuxStandby ? 'border-red-500 focus:border-red-500' : '']"
            @input="validateAndUpdate('pcsAuxStandby', Number($event.target.value), validationRules.pcsAuxStandby)">
          <p v-if="errors.pcsAuxStandby" class="text-[10px] text-red-400 mt-0.5">{{ errors.pcsAuxStandby }}</p>
        </div>
      </div>

      <div class="mt-3 p-3 rounded-lg font-mono text-[11px] space-y-1" style="background: var(--color-bg-secondary); border: 1px solid var(--color-border); color: var(--color-text-secondary);">
        <div class="font-bold text-[10px]" style="color: #f59e0b;">{{ $t('paramPanel.auxDerivation') }}</div>
        <div>
          {{ $t('paramPanel.dailyRunTotal') }} = {{ params.duration }}h x {{ params.cyclesPerDay }}{{ $t('paramPanel.times') }} = <span style="color: var(--color-accent-secondary); font-weight: bold;">{{ (params.duration * params.cyclesPerDay).toFixed(1) }}h</span>
          &nbsp;{{ $t('paramPanel.dailyStandby') }} = Max(0, 24 - {{ (params.duration * params.cyclesPerDay).toFixed(1) }}) = <span style="color: var(--color-accent-secondary); font-weight: bold;">{{ Math.max(0, 24 - params.duration * params.cyclesPerDay).toFixed(1) }}h</span>
        </div>
        <div>
          {{ $t('paramPanel.singleContainerDaily') }} = ({{ params.bessAuxRun }}kW x {{ (params.duration * params.cyclesPerDay).toFixed(1) }}h + {{ params.bessAuxStandby }}kW x {{ Math.max(0, 24 - params.duration * params.cyclesPerDay).toFixed(1) }}h) / 1000
          = <span style="color: #f59e0b; font-weight: bold;">{{ ((params.bessAuxRun * params.duration * params.cyclesPerDay + params.bessAuxStandby * Math.max(0, 24 - params.duration * params.cyclesPerDay)) / 1000).toFixed(3) }} {{ $t('paramPanel.mwhPerDay') }}</span>
        </div>
        <div>
          {{ $t('paramPanel.singlePcsDaily') }} = ({{ params.pcsAuxRun }}kW x {{ (params.duration * params.cyclesPerDay).toFixed(1) }}h + {{ params.pcsAuxStandby }}kW x {{ Math.max(0, 24 - params.duration * params.cyclesPerDay).toFixed(1) }}h) / 1000
          = <span style="color: #f59e0b; font-weight: bold;">{{ ((params.pcsAuxRun * params.duration * params.cyclesPerDay + params.pcsAuxStandby * Math.max(0, 24 - params.duration * params.cyclesPerDay)) / 1000).toFixed(3) }} {{ $t('paramPanel.mwhPerDay') }}</span>
        </div>
        <div class="pt-1" style="border-top: 1px solid var(--color-border);">
          {{ $t('paramPanel.singleCycleAux') }} = <span style="color: var(--color-success); font-weight: bold;">
            ({{ params.initContainerQty }}{{ $t('paramPanel.units') }} x {{ $t('paramPanel.singleContainerDaily') }} + {{ params.initPcsQty }}{{ $t('paramPanel.units') }} x {{ $t('paramPanel.singlePcsDaily') }}) / {{ params.cyclesPerDay }}{{ $t('paramPanel.times') }}
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
      <h2 class="section-title" style="color: #ec4899; border-color: #ec4899;">{{ $t('paramPanel.boundaryConditions') }}</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div>
          <label class="label-text">{{ $t('paramPanel.avgTemp') }}</label>
          <input type="number" value="25" step="1" disabled class="input-field" style="opacity: 0.5; cursor: not-allowed;">
        </div>
        <div>
          <label class="label-text">{{ $t('paramPanel.avgDischargeRate') }}</label>
          <input type="number" value="0.5" step="0.1" disabled class="input-field" style="opacity: 0.5; cursor: not-allowed;">
        </div>
        <div>
          <label class="label-text">{{ $t('paramPanel.sohStartYear') }}</label>
          <input type="text" value="FOB + 6个月" disabled class="input-field" style="opacity: 0.5; cursor: not-allowed;">
        </div>
        <div>
          <label class="label-text">{{ $t('paramPanel.requiredEnergy') }}</label>
          <input type="number" :value="params.requiredEnergy" step="1"
            :class="['input-field',
              errors.requiredEnergy ? 'border-red-500 focus:border-red-500' : '']"
            @input="validateAndUpdate('requiredEnergy', Number($event.target.value), validationRules.requiredEnergy)">
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
  ratedEnergy: { min: 0.1, max: 20 },
  initContainerQty: { min: 1, max: 200 },
  initPcsQty: { min: 1, max: 50 },
  duration: { min: 0.5, max: 12 },
  cyclesPerDay: { min: 0.5, max: 4 },
  acEfficiency: { min: 90, max: 99 },
  bessAuxRun: { min: 0, max: 50 },
  bessAuxStandby: { min: 0, max: 20 },
  pcsAuxRun: { min: 0, max: 30 },
  pcsAuxStandby: { min: 0, max: 10 },
  requiredEnergy: { min: 50, max: 500 },
}

const validateAndUpdate = (key, value, rule) => {
  if (value === '' || value === null || value === undefined) {
    errors[key] = `该字段不能为空`
    emit('error', errors[key], 'error')
    return
  }
  
  if (value < rule.min) {
    errors[key] = `该值不能小于 ${rule.min}`
    emit('error', errors[key], 'error')
    return
  }
  
  if (value > rule.max) {
    errors[key] = `该值不能大于 ${rule.max}`
    emit('error', errors[key], 'error')
    return
  }
  
  errors[key] = ''

  // 更新参数
  emit('update', key, value)
}

const inputAuxStyle = 'text-amber-300 border-amber-900/60 focus:border-amber-500'

// 自动匹配PCS
const autoMatchPCS = () => {
  const totalEnergy = props.params.initContainerQty * props.params.ratedEnergy
  const pcsQty = Math.ceil(totalEnergy / (props.params.duration * 5))
  emit('update', 'initPcsQty', pcsQty)
}
</script>
