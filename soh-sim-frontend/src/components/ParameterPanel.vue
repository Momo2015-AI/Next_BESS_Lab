<template>
  <div class="flex-1 overflow-auto rounded-xl p-4 space-y-4" style="background-color: var(--color-card);">
    <div>
      <h2 class="section-title" style="color: var(--color-accent); border-color: var(--color-accent);">{{ $t('paramPanel.systemParams') }}</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
        <div>
          <label class="label-text" style="color: var(--color-text-muted);">{{ $t('paramPanel.ratedEnergy') }}</label>
          <input type="number" :value="params.ratedEnergy" step="0.1"
            class="w-full rounded px-2 py-1 text-xs"
            :style="errors.ratedEnergy ? { backgroundColor: 'var(--color-input-bg-dark)', border: '1px solid var(--color-danger)', color: 'var(--color-text)' } : { backgroundColor: 'var(--color-input-bg-dark)', border: '1px solid var(--color-input-border)', color: 'var(--color-text)' }"
            onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';"
            onblur="this.style.borderColor=this.classList.contains('border-red-500') ? 'var(--color-danger)' : 'var(--color-input-border)';"
            @input="validateAndUpdate('ratedEnergy', Number($event.target.value), validationRules.ratedEnergy)">
          <p v-if="errors.ratedEnergy" class="text-[10px] mt-0.5" style="color: var(--color-danger);">{{ errors.ratedEnergy }}</p>
        </div>
        <div>
          <label class="label-text" style="color: var(--color-text-muted);">{{ $t('paramPanel.initContainerQty') }}</label>
          <input type="number" :value="params.initContainerQty" step="1"
            class="w-full rounded px-2 py-1 text-xs"
            :style="errors.initContainerQty ? { backgroundColor: 'var(--color-input-bg-dark)', border: '1px solid var(--color-danger)', color: 'var(--color-text)' } : { backgroundColor: 'var(--color-input-bg-dark)', border: '1px solid var(--color-input-border)', color: 'var(--color-text)' }"
            onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';"
            onblur="this.style.borderColor=this.classList.contains('border-red-500') ? 'var(--color-danger)' : 'var(--color-input-border)';"
            @input="validateAndUpdate('initContainerQty', Number($event.target.value), validationRules.initContainerQty)">
          <p v-if="errors.initContainerQty" class="text-[10px] mt-0.5" style="color: var(--color-danger);">{{ errors.initContainerQty }}</p>
        </div>
        <div>
          <label class="label-text" style="color: var(--color-text-muted);">{{ $t('paramPanel.initPcsQty') }}</label>
          <input type="number" :value="params.initPcsQty" step="1"
            class="w-full rounded px-2 py-1 text-xs"
            :style="errors.initPcsQty ? { backgroundColor: 'var(--color-input-bg-dark)', border: '1px solid var(--color-danger)', color: 'var(--color-text)' } : { backgroundColor: 'var(--color-input-bg-dark)', border: '1px solid var(--color-input-border)', color: 'var(--color-text)' }"
            onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';"
            onblur="this.style.borderColor=this.classList.contains('border-red-500') ? 'var(--color-danger)' : 'var(--color-input-border)';"
            @input="validateAndUpdate('initPcsQty', Number($event.target.value), validationRules.initPcsQty)">
          <p v-if="errors.initPcsQty" class="text-[10px] mt-0.5" style="color: var(--color-danger);">{{ errors.initPcsQty }}</p>
        </div>
        <div>
          <label class="label-text" style="color: var(--color-text-muted);">{{ $t('paramPanel.duration') }}</label>
          <input type="number" :value="params.duration" step="0.5"
            class="w-full rounded px-2 py-1 text-xs"
            :style="errors.duration ? { backgroundColor: 'var(--color-input-bg-dark)', border: '1px solid var(--color-danger)', color: 'var(--color-text)' } : { backgroundColor: 'var(--color-input-bg-dark)', border: '1px solid var(--color-input-border)', color: 'var(--color-text)' }"
            onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';"
            onblur="this.style.borderColor=this.classList.contains('border-red-500') ? 'var(--color-danger)' : 'var(--color-input-border)';"
            @input="validateAndUpdate('duration', Number($event.target.value), validationRules.duration)">
          <p v-if="errors.duration" class="text-[10px] mt-0.5" style="color: var(--color-danger);">{{ errors.duration }}</p>
        </div>
        <div>
          <label class="label-text" style="color: var(--color-text-muted);">{{ $t('paramPanel.cyclesPerDay') }}</label>
          <input type="number" :value="params.cyclesPerDay" step="1"
            class="w-full rounded px-2 py-1 text-xs"
            :style="errors.cyclesPerDay ? { backgroundColor: 'var(--color-input-bg-dark)', border: '1px solid var(--color-danger)', color: 'var(--color-text)' } : { backgroundColor: 'var(--color-input-bg-dark)', border: '1px solid var(--color-input-border)', color: 'var(--color-text)' }"
            onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';"
            onblur="this.style.borderColor=this.classList.contains('border-red-500') ? 'var(--color-danger)' : 'var(--color-input-border)';"
            @input="validateAndUpdate('cyclesPerDay', Number($event.target.value), validationRules.cyclesPerDay)">
          <p v-if="errors.cyclesPerDay" class="text-[10px] mt-0.5" style="color: var(--color-danger);">{{ errors.cyclesPerDay }}</p>
        </div>
        <div>
          <label class="label-text" style="color: var(--color-text-muted);">{{ $t('paramPanel.acEfficiency') }}</label>
          <input type="number" :value="params.acEfficiency" step="0.01"
            class="w-full rounded px-2 py-1 text-xs"
            :style="errors.acEfficiency ? { backgroundColor: 'var(--color-input-bg-dark)', border: '1px solid var(--color-danger)', color: 'var(--color-text)' } : { backgroundColor: 'var(--color-input-bg-dark)', border: '1px solid var(--color-input-border)', color: 'var(--color-text)' }"
            onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';"
            onblur="this.style.borderColor=this.classList.contains('border-red-500') ? 'var(--color-danger)' : 'var(--color-input-border)';"
            @input="validateAndUpdate('acEfficiency', Number($event.target.value), validationRules.acEfficiency)">
          <p v-if="errors.acEfficiency" class="text-[10px] mt-0.5" style="color: var(--color-danger);">{{ errors.acEfficiency }}</p>
        </div>
      </div>
    </div>

    <div>
      <h2 class="section-title" style="color: var(--color-warning); border-color: var(--color-warning);">{{ $t('paramPanel.auxPower') }}</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div>
          <label class="label-text" style="color: var(--color-text-muted);">{{ $t('paramPanel.bessAuxRun') }}</label>
          <input type="number" :value="params.bessAuxRun" step="0.001"
            class="w-full rounded px-2 py-1 text-xs"
            :style="errors.bessAuxRun ? { backgroundColor: 'var(--color-input-bg-dark)', border: '1px solid var(--color-danger)', color: 'var(--color-warning)' } : { backgroundColor: 'var(--color-input-bg-dark)', border: '1px solid var(--color-input-border)', color: 'var(--color-warning)' }"
            onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';"
            onblur="this.style.borderColor=this.classList.contains('border-red-500') ? 'var(--color-danger)' : 'var(--color-input-border)';"
            @input="validateAndUpdate('bessAuxRun', Number($event.target.value), validationRules.bessAuxRun)">
          <p v-if="errors.bessAuxRun" class="text-[10px] mt-0.5" style="color: var(--color-danger);">{{ errors.bessAuxRun }}</p>
        </div>
        <div>
          <label class="label-text" style="color: var(--color-text-muted);">{{ $t('paramPanel.bessAuxStandby') }}</label>
          <input type="number" :value="params.bessAuxStandby" step="0.1"
            class="w-full rounded px-2 py-1 text-xs"
            :style="errors.bessAuxStandby ? { backgroundColor: 'var(--color-input-bg-dark)', border: '1px solid var(--color-danger)', color: 'var(--color-warning)' } : { backgroundColor: 'var(--color-input-bg-dark)', border: '1px solid var(--color-input-border)', color: 'var(--color-warning)' }"
            onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';"
            onblur="this.style.borderColor=this.classList.contains('border-red-500') ? 'var(--color-danger)' : 'var(--color-input-border)';"
            @input="validateAndUpdate('bessAuxStandby', Number($event.target.value), validationRules.bessAuxStandby)">
          <p v-if="errors.bessAuxStandby" class="text-[10px] mt-0.5" style="color: var(--color-danger);">{{ errors.bessAuxStandby }}</p>
        </div>
        <div>
          <label class="label-text" style="color: var(--color-text-muted);">{{ $t('paramPanel.pcsAuxRun') }}</label>
          <input type="number" :value="params.pcsAuxRun" step="0.1"
            class="w-full rounded px-2 py-1 text-xs"
            :style="errors.pcsAuxRun ? { backgroundColor: 'var(--color-input-bg-dark)', border: '1px solid var(--color-danger)', color: 'var(--color-warning)' } : { backgroundColor: 'var(--color-input-bg-dark)', border: '1px solid var(--color-input-border)', color: 'var(--color-warning)' }"
            onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';"
            onblur="this.style.borderColor=this.classList.contains('border-red-500') ? 'var(--color-danger)' : 'var(--color-input-border)';"
            @input="validateAndUpdate('pcsAuxRun', Number($event.target.value), validationRules.pcsAuxRun)">
          <p v-if="errors.pcsAuxRun" class="text-[10px] mt-0.5" style="color: var(--color-danger);">{{ errors.pcsAuxRun }}</p>
        </div>
        <div>
          <label class="label-text" style="color: var(--color-text-muted);">{{ $t('paramPanel.pcsAuxStandby') }}</label>
          <input type="number" :value="params.pcsAuxStandby" step="0.1"
            class="w-full rounded px-2 py-1 text-xs"
            :style="errors.pcsAuxStandby ? { backgroundColor: 'var(--color-input-bg-dark)', border: '1px solid var(--color-danger)', color: 'var(--color-warning)' } : { backgroundColor: 'var(--color-input-bg-dark)', border: '1px solid var(--color-input-border)', color: 'var(--color-warning)' }"
            onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';"
            onblur="this.style.borderColor=this.classList.contains('border-red-500') ? 'var(--color-danger)' : 'var(--color-input-border)';"
            @input="validateAndUpdate('pcsAuxStandby', Number($event.target.value), validationRules.pcsAuxStandby)">
          <p v-if="errors.pcsAuxStandby" class="text-[10px] mt-0.5" style="color: var(--color-danger);">{{ errors.pcsAuxStandby }}</p>
        </div>
      </div>

      <div class="mt-3 p-3 rounded-lg font-mono text-[11px] space-y-1" style="background: var(--color-bg-secondary); border: 1px solid var(--color-border); color: var(--color-text-secondary);">
        <div class="font-bold text-[10px]" style="color: var(--color-warning);">{{ $t('paramPanel.auxDerivation') }}</div>
        <div>
          {{ $t('paramPanel.dailyRunTotal') }} = {{ params.duration }}h x {{ params.cyclesPerDay }}{{ $t('paramPanel.times') }} = <span style="color: var(--color-accent-secondary); font-weight: bold;">{{ (params.duration * params.cyclesPerDay).toFixed(1) }}h</span>
          &nbsp;{{ $t('paramPanel.dailyStandby') }} = Max(0, 24 - {{ (params.duration * params.cyclesPerDay).toFixed(1) }}) = <span style="color: var(--color-accent-secondary); font-weight: bold;">{{ Math.max(0, 24 - params.duration * params.cyclesPerDay).toFixed(1) }}h</span>
        </div>
        <div>
          {{ $t('paramPanel.singleContainerDaily') }} = ({{ params.bessAuxRun }}kW x {{ (params.duration * params.cyclesPerDay).toFixed(1) }}h + {{ params.bessAuxStandby }}kW x {{ Math.max(0, 24 - params.duration * params.cyclesPerDay).toFixed(1) }}h) / 1000
          = <span style="color: var(--color-warning); font-weight: bold;">{{ ((params.bessAuxRun * params.duration * params.cyclesPerDay + params.bessAuxStandby * Math.max(0, 24 - params.duration * params.cyclesPerDay)) / 1000).toFixed(3) }} {{ $t('paramPanel.mwhPerDay') }}</span>
        </div>
        <div>
          {{ $t('paramPanel.singlePcsDaily') }} = ({{ params.pcsAuxRun }}kW x {{ (params.duration * params.cyclesPerDay).toFixed(1) }}h + {{ params.pcsAuxStandby }}kW x {{ Math.max(0, 24 - params.duration * params.cyclesPerDay).toFixed(1) }}h) / 1000
          = <span style="color: var(--color-warning); font-weight: bold;">{{ ((params.pcsAuxRun * params.duration * params.cyclesPerDay + params.pcsAuxStandby * Math.max(0, 24 - params.duration * params.cyclesPerDay)) / 1000).toFixed(3) }} {{ $t('paramPanel.mwhPerDay') }}</span>
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
      <h2 class="text-sm font-bold mb-3 flex items-center gap-2" style="color: var(--color-accent); border-left: 4px solid var(--color-accent); padding-left: 8px;">⚡ 电池与PCS配置规则</h2>
      <div class="rounded-lg p-4" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
        <div class="grid grid-cols-3 gap-4 mb-4">
          <div class="rounded p-3" style="background-color: var(--color-input-bg-dark);">
            <div class="text-xs mb-2 font-medium" style="color: var(--color-accent);">功率配比规则</div>
            <div class="text-[10px] space-y-1" style="color: var(--color-text-muted);">
              <div>• 2h储能: <span style="color: var(--color-accent-secondary);">能量 = 2 × 功率</span></div>
              <div>• 4h储能: <span style="color: var(--color-accent-secondary);">能量 = 4 × 功率</span></div>
              <div>• 常用配比: <span style="color: var(--color-accent-secondary);">1:2 (功率:能量)</span></div>
            </div>
          </div>
          <div class="rounded p-3" style="background-color: var(--color-input-bg-dark);">
            <div class="text-xs mb-2 font-medium" style="color: var(--color-accent-secondary);">集装箱与PCS对应规则</div>
            <div class="text-[10px] space-y-1" style="color: var(--color-text-muted);">
              <div>• 5MWh + 0.5C放电 → <span style="color: var(--color-accent-secondary);">2台 2.5MW PCS</span></div>
              <div>• 10MWh + 0.5C放电 → <span style="color: var(--color-accent-secondary);">2台 5MW PCS</span></div>
              <div>• 20MWh + 0.5C放电 → <span style="color: var(--color-accent-secondary);">4台 5MW PCS</span></div>
            </div>
          </div>
          <div class="rounded p-3" style="background-color: var(--color-input-bg-dark);">
            <div class="text-xs mb-2 font-medium" style="color: var(--color-warning);">计算公式</div>
            <div class="text-[10px] space-y-1" style="color: var(--color-text-muted);">
              <div>PCS数量 = 能量 ÷ (放电时长 × 单台功率)</div>
              <div>变压器 = PCS总量 ÷ 并机数 × 1.1</div>
            </div>
          </div>
        </div>

        <div class="flex items-center gap-4 p-3 rounded" style="background-color: var(--color-accent-glow); border: 1px solid var(--color-accent-dark);">
          <div class="text-xs" style="color: var(--color-accent-secondary);">
            当前: <span style="font-weight: bold; color: var(--color-text);">{{ params.initContainerQty }}</span>台 × <span style="font-weight: bold; color: var(--color-text);">{{ params.ratedEnergy }}</span>MWh = <span style="font-weight: bold; color: var(--color-accent);">{{ (params.initContainerQty * params.ratedEnergy).toFixed(1) }}</span> MWh
          </div>
          <div style="color: var(--color-text-muted);">→</div>
          <div class="text-xs" style="color: var(--color-accent-secondary);">
            建议PCS: <span style="font-weight: bold; color: var(--color-text);">{{ Math.ceil((params.initContainerQty * params.ratedEnergy) / (params.duration * 5)) }}</span> 台 5MW
          </div>
          <div style="color: var(--color-text-muted);">→</div>
          <div class="text-xs" style="color: var(--color-warning);">
            配比: <span style="font-weight: bold; color: var(--color-text);">1:{{ ((params.initContainerQty * params.ratedEnergy) / (Math.ceil((params.initContainerQty * params.ratedEnergy) / (params.duration * 5)) * 5)).toFixed(1) }}</span>
          </div>
        </div>

        <button @click="autoMatchPCS" class="mt-3 text-xs px-4 py-2 rounded transition-colors"
          style="background-color: var(--color-accent); color: white;"
          onmouseover="this.style.opacity='0.9';"
          onmouseout="this.style.opacity='1';">
          根据配置规则自动匹配PCS
        </button>
      </div>
    </div>

    <div>
      <h2 class="section-title" style="color: var(--color-danger); border-color: var(--color-danger);">{{ $t('paramPanel.boundaryConditions') }}</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div>
          <label class="label-text" style="color: var(--color-text-muted);">{{ $t('paramPanel.avgTemp') }}</label>
          <input type="number" value="25" step="1" disabled 
            class="w-full rounded px-2 py-1 text-xs"
            style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border); color: var(--color-text-muted); opacity: 0.5; cursor: not-allowed;">
        </div>
        <div>
          <label class="label-text" style="color: var(--color-text-muted);">{{ $t('paramPanel.avgDischargeRate') }}</label>
          <input type="number" value="0.5" step="0.1" disabled 
            class="w-full rounded px-2 py-1 text-xs"
            style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border); color: var(--color-text-muted); opacity: 0.5; cursor: not-allowed;">
        </div>
        <div>
          <label class="label-text" style="color: var(--color-text-muted);">{{ $t('paramPanel.sohStartYear') }}</label>
          <input type="text" value="FOB + 6个月" disabled 
            class="w-full rounded px-2 py-1 text-xs"
            style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border); color: var(--color-text-muted); opacity: 0.5; cursor: not-allowed;">
        </div>
        <div>
          <label class="label-text" style="color: var(--color-text-muted);">{{ $t('paramPanel.requiredEnergy') }}</label>
          <input type="number" :value="params.requiredEnergy" step="1"
            class="w-full rounded px-2 py-1 text-xs"
            :style="errors.requiredEnergy ? { backgroundColor: 'var(--color-input-bg-dark)', border: '1px solid var(--color-danger)', color: 'var(--color-text)' } : { backgroundColor: 'var(--color-input-bg-dark)', border: '1px solid var(--color-input-border)', color: 'var(--color-text)' }"
            onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';"
            onblur="this.style.borderColor=this.classList.contains('border-red-500') ? 'var(--color-danger)' : 'var(--color-input-border)';"
            @input="validateAndUpdate('requiredEnergy', Number($event.target.value), validationRules.requiredEnergy)">
          <p v-if="errors.requiredEnergy" class="text-[10px] mt-0.5" style="color: var(--color-danger);">{{ errors.requiredEnergy }}</p>
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

  emit('update', key, value)
}

const autoMatchPCS = () => {
  const totalEnergy = props.params.initContainerQty * props.params.ratedEnergy
  const pcsQty = Math.ceil(totalEnergy / (props.params.duration * 5))
  emit('update', 'initPcsQty', pcsQty)
}
</script>