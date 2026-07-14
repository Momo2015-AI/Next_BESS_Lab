<template>
  <div class="epc-panel space-y-4">
    <div class="panel-card">
      <h3 class="panel-title">{{ $t('epcIpp.title') }}</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcIpp.projectLife') }}</label>
          <input v-model.number="ippForm.project_life_years" type="number" class="form-field-input" placeholder="25" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcIpp.totalCapex') }}</label>
          <input
            v-model.number="ippForm.total_capex_usd"
            type="number"
            class="form-field-input"
            placeholder="500000000"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcIpp.capacity') }}</label>
          <input v-model.number="ippForm.capacity_mw" type="number" class="form-field-input" placeholder="100" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcIpp.energy') }}</label>
          <input v-model.number="ippForm.energy_mwh" type="number" class="form-field-input" placeholder="200" />
        </div>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcIpp.capacityPrice') }}</label>
          <input
            v-model.number="ippForm.capacity_price_usd_kw_month"
            type="number"
            step="0.1"
            class="form-field-input"
            placeholder="8.0"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcIpp.energyPrice') }}</label>
          <input
            v-model.number="ippForm.energy_price_usd_kwh"
            type="number"
            step="0.01"
            class="form-field-input"
            placeholder="0.05"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcIpp.ppaEscalation') }}</label>
          <input
            v-model.number="ippForm.ppa_escalation_rate"
            type="number"
            step="0.01"
            class="form-field-input"
            placeholder="0.02"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcIpp.debtRatio') }}</label>
          <input
            v-model.number="ippForm.debt_ratio"
            type="number"
            step="0.05"
            class="form-field-input"
            placeholder="0.7"
          />
        </div>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcIpp.loanRate') }}</label>
          <input
            v-model.number="ippForm.debt_interest_rate"
            type="number"
            step="0.01"
            class="form-field-input"
            placeholder="0.05"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcIpp.loanTenor') }}</label>
          <input v-model.number="ippForm.debt_tenor_years" type="number" class="form-field-input" placeholder="15" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcIpp.annualOpex') }}</label>
          <input
            v-model.number="ippForm.annual_opex_usd"
            type="number"
            class="form-field-input"
            placeholder="5000000"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcIpp.availability') }}</label>
          <input
            v-model.number="ippForm.availability_guarantee"
            type="number"
            step="0.01"
            class="form-field-input"
            placeholder="0.98"
          />
        </div>
      </div>
      <button :disabled="loading" class="btn-primary" @click="calculateIPP">
        {{ loading ? $t('epcIpp.calculating') : $t('epcIpp.runCalc') }}
      </button>

      <div v-if="ippResult" class="mt-6 space-y-4">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div class="metric-card">
            <div class="metric-value primary-text">${{ formatNum(ippResult.npv_usd) }}</div>
            <div class="metric-label">{{ $t('epcIpp.npv') }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-value primary-text">{{ ippResult.irr }}%</div>
            <div class="metric-label">{{ $t('epcIpp.projectIrr') }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-value primary-text">{{ ippResult.equity_irr }}%</div>
            <div class="metric-label">{{ $t('epcIpp.equityIrr') }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-value primary-text">${{ ippResult.lcoe_usd_kwh }}/kWh</div>
            <div class="metric-label">{{ $t('epcIpp.lcoe') }}</div>
          </div>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
          <div class="metric-card">
            <div class="metric-value">{{ ippResult.dscr_avg }}</div>
            <div class="metric-label">{{ $t('epcIpp.avgDscr') }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ ippResult.dscr_min }}</div>
            <div class="metric-label">{{ $t('epcIpp.minDscr') }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ ippResult.payback_years }}{{ $t('epcIpp.yearUnit') }}</div>
            <div class="metric-label">{{ $t('epcIpp.payback') }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useEpcModules } from '../../composables/useEpcModules.js'

const { loading, ippForm, ippResult, calculateIPP, formatNum } = useEpcModules()
</script>
