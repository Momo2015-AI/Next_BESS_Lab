<template>
  <div class="epc-panel space-y-4">
    <div class="panel-card">
	      <h3 class="panel-title">{{ $t('epcMatrix.title') }}</h3>
	      <div class="flex gap-4 mb-4">
	        <select v-model="matrixForm.template" class="form-field-select max-w-sm">
	          <option value="UAE_DEWA_VII_BESS">UAE DEWA VII BESS RFP</option>
	        </select>
	        <button :disabled="loading" class="btn-primary" @click="generateMatrix">
	          {{ loading ? $t('epcMatrix.generating') : $t('epcMatrix.generate') }}
	        </button>
      </div>

      <div v-if="matrixResult" class="mt-4">
        <div class="grid grid-cols-4 gap-3 mb-4">
          <div class="metric-card">
            <div class="metric-value">{{ matrixResult.total }}</div>
	            <div class="metric-label">{{ $t('epcMatrix.totalClauses') }}</div>
	          </div>
	          <div class="metric-card">
	            <div class="metric-value pass-text">{{ matrixResult.compliant }}</div>
	            <div class="metric-label">{{ $t('epcMatrix.compliant') }}</div>
	          </div>
	          <div class="metric-card">
	            <div class="metric-value fail-text">{{ matrixResult.non_compliant }}</div>
	            <div class="metric-label">{{ $t('epcMatrix.nonCompliant') }}</div>
	          </div>
	          <div class="metric-card">
	            <div class="metric-value warn-text">{{ matrixResult.partial }}</div>
	            <div class="metric-label">{{ $t('epcMatrix.partial') }}</div>
          </div>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm data-table">
            <thead>
              <tr>
	                <th class="px-3 py-2 text-left header-cell">{{ $t('epcMatrix.colClause') }}</th>
	                <th class="px-3 py-2 text-left header-cell">{{ $t('epcMatrix.colRequirement') }}</th>
	                <th class="px-3 py-2 text-left header-cell">{{ $t('epcMatrix.colCategory') }}</th>
	                <th class="px-3 py-2 text-left header-cell">{{ $t('epcMatrix.colStatus') }}</th>
	                <th class="px-3 py-2 text-left header-cell">{{ $t('epcMatrix.colResponse') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in matrixResult.matrix" :key="item.section" class="border-row">
                <td class="px-3 py-2 font-mono text-xs">{{ item.section }}</td>
                <td class="px-3 py-2">{{ item.requirement }}</td>
                <td class="px-3 py-2 text-xs tx-muted">{{ item.category }}</td>
                <td class="px-3 py-2">
                  <span class="status-badge" :class="statusClass(item.compliance_status)">
                    {{ $t(statusLabel(item.compliance_status)) }}
                  </span>
                </td>
                <td class="px-3 py-2 text-xs tx-muted-dark">{{ item.response }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useEpcModules } from '../../composables/useEpcModules.js'

const { loading, matrixForm, matrixResult, generateMatrix, statusLabel, statusClass } = useEpcModules()
</script>
