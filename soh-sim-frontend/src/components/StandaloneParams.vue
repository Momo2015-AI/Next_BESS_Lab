<template>
  <div class="card standalone-params">
    <h3 class="font-bold text-xs mb-3 flex items-center gap-2">
      <span class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold standalone-badge">S</span>
      {{ $t('financial.standaloneSection') }}
    </h3>

    <div class="grid grid-cols-3 gap-3">
      <!-- 系统规模 -->
      <div class="param-group">
        <label class="param-label">{{ $t('financial.labelTotalCapMWh') }}</label>
        <input
          v-model.number="local.totalCapMWh"
          type="number"
          step="1"
          min="1"
          class="param-input"
        />
        <span class="param-unit">MWh</span>
      </div>
      <div class="param-group">
        <label class="param-label">{{ $t('financial.labelTotalCapMW') }}</label>
        <input
          v-model.number="local.totalCapMW"
          type="number"
          step="0.1"
          min="0.1"
          class="param-input"
        />
        <span class="param-unit">MW</span>
      </div>
      <div class="param-group">
        <label class="param-label">{{ $t('financial.labelCyclesPerDay') }}</label>
        <input
          v-model.number="local.cyclesPerDay"
          type="number"
          step="0.1"
          min="0.1"
          class="param-input"
        />
        <span class="param-unit">{{ $t('financial.cyclesUnit') }}</span>
      </div>

      <!-- 运行参数 -->
      <div class="param-group">
        <label class="param-label">{{ $t('financial.labelOperatingDays') }}</label>
        <input
          v-model.number="local.operatingDays"
          type="number"
          step="1"
          min="1"
          max="365"
          class="param-input"
        />
        <span class="param-unit">{{ $t('financial.daysUnit') }}</span>
      </div>
      <div class="param-group">
        <label class="param-label">{{ $t('financial.labelEfficiencyLoss') }}</label>
        <input
          v-model.number="local.efficiencyLossPct"
          type="number"
          step="0.1"
          min="0"
          max="100"
          class="param-input"
        />
        <span class="param-unit">%</span>
      </div>
      <div class="param-group">
        <label class="param-label">{{ $t('financial.labelSohStart') }}</label>
        <input
          v-model.number="local.sohStart"
          type="number"
          step="0.1"
          min="1"
          max="100"
          class="param-input"
        />
        <span class="param-unit">%</span>
      </div>

      <!-- 衰减参数 -->
      <div class="param-group param-group-wide">
        <label class="param-label">{{ $t('financial.labelSohDecline') }}</label>
        <input
          v-model.number="local.sohAnnualDecline"
          type="number"
          step="0.1"
          min="0"
          max="20"
          class="param-input"
        />
        <span class="param-unit">% / {{ $t('financial.yearUnit') }}</span>
      </div>
    </div>

    <!-- 生成的 SOH 曲线预览 -->
    <div class="soh-preview mt-3">
      <span class="soh-preview-label">{{ $t('financial.sohCurvePreview') }}</span>
      <div class="soh-preview-bars">
        <div
          v-for="(v, i) in sohPreview"
          :key="i"
          class="soh-bar"
          :style="{ height: v + '%' }"
          :title="`${$t('financial.year')} ${i}: ${v.toFixed(1)}%`"
        ></div>
      </div>
      <span class="soh-preview-end">{{ $t('financial.sohEnd') }}: {{ sohEnd }}%</span>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed, watch } from 'vue'

const props = defineProps({
  modelValue: { type: Object, required: true }
})

const emit = defineEmits(['update:modelValue', 'change'])

const local = reactive({ ...props.modelValue })

watch(local, (val) => {
  emit('update:modelValue', { ...val })
  emit('change')
}, { deep: true })

// 生成26年SOH曲线预览 (year 0-25)
const sohPreview = computed(() => {
  const result = []
  for (let i = 0; i <= 25; i++) {
    const soh = Math.max(0, local.sohStart - local.sohAnnualDecline * i)
    result.push(soh)
  }
  return result
})

const sohEnd = computed(() => sohPreview.value[25].toFixed(1))
</script>

<style scoped>
.standalone-params {
  padding: 14px 18px;
}

.standalone-badge {
  background: var(--btn-accent-bg);
  color: var(--btn-accent-text);
  border: var(--btn-accent-border);
}

.param-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
  position: relative;
}

.param-group-wide {
  grid-column: span 2;
}

.param-label {
  font-size: 10px;
  font-weight: 600;
  color: var(--text-secondary);
  letter-spacing: 0.3px;
}

.param-input {
  width: 100%;
  height: 30px;
  padding: 0 8px;
  background: var(--form-field-bg);
  border: 1px solid var(--form-field-border);
  border-radius: var(--radius-sm);
  color: var(--form-field-text);
  font-size: 13px;
  font-weight: 500;
  transition: border-color 0.3s var(--ease-precision);
}
.param-input:focus {
  border-color: var(--form-field-border-focus);
  outline: none;
  box-shadow: 0 0 0 2px rgba(22, 119, 255, 0.1);
}

.param-unit {
  font-size: 10px;
  color: var(--color-text-muted);
  position: absolute;
  right: 8px;
  bottom: 8px;
  pointer-events: none;
}

.soh-preview {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  background: var(--panel-sub-bg);
  border: var(--panel-sub-border);
  border-radius: var(--radius-sm);
}

.soh-preview-label {
  font-size: 10px;
  font-weight: 600;
  color: var(--text-muted, var(--color-text-muted));
  white-space: nowrap;
  min-width: 50px;
}

.soh-preview-bars {
  display: flex;
  align-items: flex-end;
  gap: 2px;
  height: 32px;
  flex: 1;
}

.soh-bar {
  flex: 1;
  min-width: 2px;
  background: var(--btn-accent-bg);
  border-radius: 1px 1px 0 0;
  transition: height 0.3s var(--ease-precision);
}

.soh-preview-end {
  font-size: 10px;
  font-weight: 600;
  color: var(--color-warning);
  white-space: nowrap;
}
</style>
