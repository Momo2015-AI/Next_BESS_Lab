<template>
  <div class="epc-panel space-y-4">
    <div class="panel-card">
      <h3 class="panel-title">{{ $t('epcScada.title') }}</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcScada.containerCount') }}</label>
          <input v-model.number="seForm.container_count" type="number" class="form-field-input" placeholder="20" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcScada.pcsCount') }}</label>
          <input v-model.number="seForm.pcs_count" type="number" class="form-field-input" placeholder="10" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcScada.commProtocol') }}</label>
          <select v-model="seForm.communication_protocol" class="form-field-select">
            <option value="IEC_61850">IEC 61850</option>
            <option value="Modbus_TCP">Modbus TCP</option>
            <option value="DNP3">DNP3</option>
          </select>
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcScada.dispatchStrategy') }}</label>
          <select v-model="seForm.dispatch_strategy" class="form-field-select">
            <option value="peak_shaving">{{ $t('epcScada.peakShaving') }}</option>
            <option value="arbitrage">{{ $t('epcScada.arbitrage') }}</option>
            <option value="frequency_regulation">{{ $t('epcScada.freqReg') }}</option>
          </select>
        </div>
      </div>
      <button :disabled="loading" class="btn-primary" @click="designScada">
        {{ loading ? $t('epcScada.designing') : $t('epcScada.runDesign') }}
      </button>

      <div v-if="seResult" class="mt-6 space-y-4">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div class="metric-card">
            <div class="metric-value">{{ seResult.total_data_points }}</div>
            <div class="metric-label">{{ $t('epcScada.totalDataPoints') }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ seResult.analog_points }}</div>
            <div class="metric-label">{{ $t('epcScada.analogPoints') }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ seResult.digital_points }}</div>
            <div class="metric-label">{{ $t('epcScada.digitalPoints') }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ seResult.control_points }}</div>
            <div class="metric-label">{{ $t('epcScada.controlPoints') }}</div>
          </div>
        </div>
        <div class="info-box">
          <div class="text-sm font-bold mb-2 section-title">{{ $t('epcScada.sysArch') }}</div>
          <div class="text-sm space-y-1 info-list">
            <div>{{ $t('epcScada.archType') }}: {{ seResult.scada_architecture }}</div>
            <div>{{ $t('epcScada.networkTopology') }}: {{ seResult.network_topology }}</div>
            <div>{{ $t('epcScada.redundancy') }}: {{ seResult.redundancy_level }}</div>
            <div>{{ $t('epcScada.encryption') }}: {{ seResult.encryption_type }}</div>
            <div>NERC-CIP: {{ seResult.nerc_cip_compliant ? 'pass' : 'fail' }}</div>
            <div>IEC 62443: {{ seResult.iec_62443_compliant ? 'pass' : 'fail' }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useEpcModules } from '../../composables/useEpcModules.js'

const { loading, seForm, seResult, designScada } = useEpcModules()
</script>
