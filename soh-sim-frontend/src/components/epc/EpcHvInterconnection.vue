<template>
  <div class="epc-panel space-y-4">
    <div class="panel-card">
      <h3 class="panel-title">{{ $t('epcHv.title') }}</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcHv.totalPower') }}</label>
          <input v-model.number="hvForm.total_power_mw" type="number" class="form-field-input" placeholder="100" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcHv.pocVoltage') }}</label>
          <input v-model.number="hvForm.poc_voltage_kv" type="number" class="form-field-input" placeholder="33" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcHv.shortCircuit') }}</label>
          <input
            v-model.number="hvForm.short_circuit_capacity_mva"
            type="number"
            class="form-field-input"
            placeholder="500"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcHv.pocType') }}</label>
          <select v-model="hvForm.poc_type" class="form-field-select">
            <option value="substation">{{ $t('epcHv.substation') }}</option>
            <option value="overhead_line">{{ $t('epcHv.overheadLine') }}</option>
            <option value="cable">{{ $t('epcHv.cable') }}</option>
          </select>
        </div>
      </div>
      <button :disabled="loading" class="btn-primary" @click="designHV">
        {{ loading ? $t('epcHv.designing') : $t('epcHv.runDesign') }}
      </button>

      <div v-if="hvResult" class="mt-6 space-y-4">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div class="metric-card">
            <div class="metric-value">{{ hvResult.transformer_count }}</div>
	            <div class="metric-label">{{ $t('epcHv.transformerCount') }}</div>
	          </div>
	          <div class="metric-card">
	            <div class="metric-value">{{ hvResult.transformer_capacity_mva }}MVA</div>
	            <div class="metric-label">{{ $t('epcHv.transformerCapacity') }}</div>
	          </div>
	          <div class="metric-card">
	            <div class="metric-value">{{ hvResult.transformer_ratio }}</div>
	            <div class="metric-label">{{ $t('epcHv.ratio') }}</div>
	          </div>
	          <div class="metric-card">
	            <div class="metric-value">{{ hvResult.mv_breaker_rating_ka }}kA</div>
	            <div class="metric-label">{{ $t('epcHv.breakerRating') }}</div>
          </div>
        </div>
        <div v-if="hvResult.protection_scheme" class="info-box">
          <div class="text-sm font-bold mb-2 section-title">{{ $t('epcHv.protectionScheme') }}</div>
          <div class="grid grid-cols-2 md:grid-cols-5 gap-2">
            <div v-for="prot in hvResult.protection_scheme" :key="prot.name" class="protection-item">
              <div class="font-bold">{{ prot.name }}</div>
              <div class="tx-muted">{{ prot.type }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useEpcModules } from '../../composables/useEpcModules.js'

const { loading, hvForm, hvResult, designHV } = useEpcModules()
</script>
