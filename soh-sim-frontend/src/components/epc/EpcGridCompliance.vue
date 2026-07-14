<template>
  <div class="epc-panel space-y-4">
    <div class="panel-card">
      <h3 class="panel-title">{{ $t('epcGrid.title') }}</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcGrid.gridStandard') }}</label>
          <select v-model="gcForm.grid_standard" class="form-field-select">
            <option v-for="s in gridStandards" :key="s.code" :value="s.code">{{ s.name }}</option>
          </select>
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcGrid.pocVoltage') }}</label>
          <input v-model.number="gcForm.grid_voltage_kv" type="number" class="form-field-input" placeholder="33" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcGrid.gridFreq') }}</label>
          <input
            v-model.number="gcForm.grid_frequency_hz"
            type="number"
            step="0.01"
            class="form-field-input"
            placeholder="50"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">PCS数量</label>
          <input v-model.number="gcForm.pcs_count" type="number" class="form-field-input" placeholder="10" />
        </div>
      </div>
      <button :disabled="loading" class="btn-primary" @click="analyzeGridCompliance">
        {{ loading ? $t('epcGrid.analyzing') : $t('epcGrid.runAnalysis') }}
      </button>

      <div v-if="gcResult" class="mt-6 space-y-4">
        <div
          class="flex items-center gap-4 p-4 rounded-lg"
          :class="gcResult.overall_pass ? 'pass-banner' : 'fail-banner'"
        >
          <span class="status-icon">{{ gcResult.overall_pass ? 'pass' : 'fail' }}</span>
          <div>
            <div class="font-bold" :class="gcResult.overall_pass ? 'pass-text' : 'fail-text'">
              {{ gcResult.overall_pass ? '全部合规' : '存在不合规项' }}
            </div>
            <div v-if="gcResult.failed_items.length" class="text-xs tx-muted-dark">
              {{ $t('epcGrid.nonCompliant') }} {{ gcResult.failed_items.join(', ') }}
            </div>
          </div>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div class="metric-card">
            <div class="metric-value" :class="gcResult.lvrt_pass ? 'pass-text' : 'fail-text'">
              {{ gcResult.lvrt_pass ? 'PASS' : 'FAIL' }}
            </div>
            <div class="metric-label">{{ $t('epcGrid.lvrt') }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-value" :class="gcResult.hvrt_pass ? 'pass-text' : 'fail-text'">
              {{ gcResult.hvrt_pass ? 'PASS' : 'FAIL' }}
            </div>
            <div class="metric-label">{{ $t('epcGrid.hvrt') }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-value" :class="gcResult.freq_response_pass ? 'pass-text' : 'fail-text'">
              {{ gcResult.freq_response_pass ? 'PASS' : 'FAIL' }}
            </div>
            <div class="metric-label">{{ $t('epcGrid.freqResponse') }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-value" :class="gcResult.reactive_pass ? 'pass-text' : 'fail-text'">
              {{ gcResult.reactive_pass ? 'PASS' : 'FAIL' }}
            </div>
            <div class="metric-label">
              {{ $t('epcGrid.reactivePower') }} ({{ gcResult.reactive_capacity_mvar }}MVar)
            </div>
          </div>
          <div class="metric-card">
            <div class="metric-value" :class="gcResult.power_quality_pass ? 'pass-text' : 'fail-text'">
              {{ gcResult.thd }}%
            </div>
            <div class="metric-label">{{ $t('epcGrid.thdLimit') }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-value" :class="gcResult.anti_islanding_pass ? 'pass-text' : 'fail-text'">
              {{ gcResult.anti_islanding_time_s }}s
            </div>
            <div class="metric-label">{{ $t('epcGrid.antiIslanding') }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-value" :class="gcResult.comm_pass ? 'pass-text' : 'fail-text'">
              {{ gcResult.comm_pass ? 'PASS' : 'FAIL' }}
            </div>
            <div class="metric-label">{{ $t('epcGrid.commCompliance') }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useEpcModules } from '../../composables/useEpcModules.js'

const { loading, gcForm, gcResult, gridStandards, analyzeGridCompliance } = useEpcModules()
</script>
