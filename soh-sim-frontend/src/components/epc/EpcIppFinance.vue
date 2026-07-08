<template>
  <div class="epc-panel space-y-4">
    <div class="panel-card">
      <h3 class="panel-title">IPP财务模型</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <div>
          <label class="block text-xs mb-1 field-label">项目寿命 (年)</label>
          <input v-model.number="ippForm.project_life_years" type="number" class="form-field-input" placeholder="25" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">总CAPEX (USD)</label>
          <input
            v-model.number="ippForm.total_capex_usd"
            type="number"
            class="form-field-input"
            placeholder="500000000"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">容量 (MW)</label>
          <input v-model.number="ippForm.capacity_mw" type="number" class="form-field-input" placeholder="100" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">能量 (MWh)</label>
          <input v-model.number="ippForm.energy_mwh" type="number" class="form-field-input" placeholder="200" />
        </div>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <div>
          <label class="block text-xs mb-1 field-label">容量价格 ($/kW/月)</label>
          <input
            v-model.number="ippForm.capacity_price_usd_kw_month"
            type="number"
            step="0.1"
            class="form-field-input"
            placeholder="8.0"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">电量价格 ($/kWh)</label>
          <input
            v-model.number="ippForm.energy_price_usd_kwh"
            type="number"
            step="0.01"
            class="form-field-input"
            placeholder="0.05"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">PPA递增率</label>
          <input
            v-model.number="ippForm.ppa_escalation_rate"
            type="number"
            step="0.01"
            class="form-field-input"
            placeholder="0.02"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">贷款比例</label>
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
          <label class="block text-xs mb-1 field-label">贷款利率</label>
          <input
            v-model.number="ippForm.debt_interest_rate"
            type="number"
            step="0.01"
            class="form-field-input"
            placeholder="0.05"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">贷款期限 (年)</label>
          <input v-model.number="ippForm.debt_tenor_years" type="number" class="form-field-input" placeholder="15" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">年OPEX (USD)</label>
          <input
            v-model.number="ippForm.annual_opex_usd"
            type="number"
            class="form-field-input"
            placeholder="5000000"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">可用率保证</label>
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
        {{ loading ? '计算中...' : '执行财务计算' }}
      </button>

      <div v-if="ippResult" class="mt-6 space-y-4">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div class="metric-card">
            <div class="metric-value primary-text">${{ formatNum(ippResult.npv_usd) }}</div>
            <div class="metric-label">NPV</div>
          </div>
          <div class="metric-card">
            <div class="metric-value primary-text">{{ ippResult.irr }}%</div>
            <div class="metric-label">项目IRR</div>
          </div>
          <div class="metric-card">
            <div class="metric-value primary-text">{{ ippResult.equity_irr }}%</div>
            <div class="metric-label">股权IRR</div>
          </div>
          <div class="metric-card">
            <div class="metric-value primary-text">${{ ippResult.lcoe_usd_kwh }}/kWh</div>
            <div class="metric-label">LCOE</div>
          </div>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
          <div class="metric-card">
            <div class="metric-value">{{ ippResult.dscr_avg }}</div>
            <div class="metric-label">平均DSCR</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ ippResult.dscr_min }}</div>
            <div class="metric-label">最小DSCR</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ ippResult.payback_years }}年</div>
            <div class="metric-label">回收期</div>
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
