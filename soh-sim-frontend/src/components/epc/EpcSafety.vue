<template>
  <div class="epc-panel space-y-4">
    <div class="panel-card">
      <h3 class="panel-title">{{ $t('epcSafety.title') }}</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcSafety.systemCapacity') }}</label>
          <input v-model.number="sfForm.system_capacity_mwh" type="number" class="form-field-input" placeholder="100" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcSafety.containerCount') }}</label>
          <input v-model.number="sfForm.container_count" type="number" class="form-field-input" placeholder="20" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcSafety.chemistryType') }}</label>
          <select v-model="sfForm.chemistry_type" class="form-field-select">
            <option value="LFP">LFP (磷酸铁锂)</option>
            <option value="NCM">NCM (三元)</option>
            <option value="NCA">NCA</option>
            <option value="LTO">LTO (钛酸锂)</option>
          </select>
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcSafety.suppressionType') }}</label>
          <select v-model="sfForm.suppression_type" class="form-field-select">
            <option value="Novec1230">Novec 1230</option>
            <option value="Aerosol">气溶胶</option>
            <option value="Water-mist">细水雾</option>
          </select>
        </div>
      </div>
      <button :disabled="loading" class="btn-primary" @click="analyzeSafety">
        {{ loading ? $t('epcSafety.analyzing') : $t('epcSafety.runAnalysis') }}
      </button>

      <div v-if="sfResult" class="mt-6 space-y-4">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div class="metric-card">
            <div class="metric-value">{{ sfResult.zone_count }}</div>
            <div class="metric-label">防火分区数</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ sfResult.container_spacing_m }}m</div>
            <div class="metric-label">集装箱间距</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ sfResult.thermal_runaway_temp_c }}°C</div>
            <div class="metric-label">热失控温度</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ sfResult.propagation_time_min }}min</div>
            <div class="metric-label">蔓延时间</div>
          </div>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div class="metric-card">
            <div class="metric-value" :class="sfResult.ul_9540a_pass ? 'pass-text' : 'fail-text'">
              {{ sfResult.ul_9540a_pass ? 'PASS' : 'FAIL' }}
            </div>
            <div class="metric-label">UL 9540A</div>
          </div>
          <div class="metric-card">
            <div class="metric-value" :class="sfResult.nfpa_855_pass ? 'pass-text' : 'fail-text'">
              {{ sfResult.nfpa_855_pass ? 'PASS' : 'FAIL' }}
            </div>
            <div class="metric-label">NFPA 855</div>
          </div>
          <div class="metric-card">
            <div class="metric-value" :class="sfResult.iec_62619_pass ? 'pass-text' : 'fail-text'">
              {{ sfResult.iec_62619_pass ? 'PASS' : 'FAIL' }}
            </div>
            <div class="metric-label">IEC 62619</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ sfResult.suppression_capacity_kg }}kg</div>
            <div class="metric-label">{{ $t('epcSafety.suppressantCapacity') }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useEpcModules } from '../../composables/useEpcModules.js'

const { loading, sfForm, sfResult, analyzeSafety } = useEpcModules()
</script>
