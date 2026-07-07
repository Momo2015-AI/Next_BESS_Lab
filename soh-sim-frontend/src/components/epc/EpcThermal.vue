<template>
  <div class="epc-panel space-y-4">
    <div class="panel-card">
      <h3 class="panel-title">热管理设计</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <div>
          <label class="block text-xs mb-1 field-label">最高环境温度 (°C)</label>
          <input v-model.number="tmForm.ambient_max_c" type="number" class="form-field-input" placeholder="45" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">电芯容量 (Ah)</label>
          <input v-model.number="tmForm.cell_capacity_ah" type="number" class="form-field-input" placeholder="280" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">充放电倍率 (C)</label>
          <input v-model.number="tmForm.c_rate" type="number" step="0.1" class="form-field-input" placeholder="0.5" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">冷却方式</label>
          <select v-model="tmForm.cooling_type" class="form-field-select">
            <option value="liquid">液冷</option>
            <option value="air">风冷</option>
          </select>
        </div>
      </div>
      <button :disabled="loading" class="btn-primary" @click="calculateThermal">
        {{ loading ? '计算中...' : '执行热管理计算' }}
      </button>

      <div v-if="tmResult" class="mt-6 space-y-4">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div class="metric-card">
            <div class="metric-value">{{ tmResult.cooling_power_kw }}kW</div>
            <div class="metric-label">制冷功率</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ tmResult.coolant_flow_rate_lpm }}L/min</div>
            <div class="metric-label">冷却液流量</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ tmResult.max_cell_temp_c }}°C</div>
            <div class="metric-label">最高电芯温度</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ formatNum(tmResult.annual_cooling_energy_kwh) }}kWh</div>
            <div class="metric-label">年制冷能耗</div>
          </div>
        </div>
        <div v-if="tmResult.derating_curve" class="mt-4">
          <h4 class="text-sm font-bold mb-2 section-title">高温降额曲线</h4>
          <div class="flex gap-1 items-end h-32 derating-chart">
            <div v-for="point in tmResult.derating_curve" :key="point.temp" class="flex-1 flex flex-col items-center">
              <div class="w-full rounded-t derating-bar" :class="deratingClass(point.power_pct)" :style="{ height: point.power_pct + '%' }" />
              <div class="text-xs mt-1 tx-muted">{{ point.temp }}°C</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useEpcModules } from '../../composables/useEpcModules.js'

const { loading, tmForm, tmResult, calculateThermal, formatNum } = useEpcModules()

function deratingClass(pct) {
  if (pct > 80) return 'bar-success'
  if (pct > 50) return 'bar-warning'
  return 'bar-danger'
}
</script>
