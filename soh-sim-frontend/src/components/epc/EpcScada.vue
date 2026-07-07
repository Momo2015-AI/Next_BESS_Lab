<template>
  <div class="epc-panel space-y-4">
    <div class="panel-card">
      <h3 class="panel-title">SCADA/EMS设计</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <div>
          <label class="block text-xs mb-1 field-label">集装箱数量</label>
          <input v-model.number="seForm.container_count" type="number" class="form-field-input" placeholder="20" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">PCS数量</label>
          <input v-model.number="seForm.pcs_count" type="number" class="form-field-input" placeholder="10" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">通信协议</label>
          <select v-model="seForm.communication_protocol" class="form-field-select">
            <option value="IEC_61850">IEC 61850</option>
            <option value="Modbus_TCP">Modbus TCP</option>
            <option value="DNP3">DNP3</option>
          </select>
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">调度策略</label>
          <select v-model="seForm.dispatch_strategy" class="form-field-select">
            <option value="peak_shaving">削峰填谷</option>
            <option value="arbitrage">套利</option>
            <option value="frequency_regulation">调频</option>
          </select>
        </div>
      </div>
      <button :disabled="loading" class="btn-primary" @click="designScada">
        {{ loading ? '设计中...' : '执行SCADA设计' }}
      </button>

      <div v-if="seResult" class="mt-6 space-y-4">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div class="metric-card">
            <div class="metric-value">{{ seResult.total_data_points }}</div>
            <div class="metric-label">总数据点</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ seResult.analog_points }}</div>
            <div class="metric-label">模拟量</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ seResult.digital_points }}</div>
            <div class="metric-label">数字量</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ seResult.control_points }}</div>
            <div class="metric-label">控制点</div>
          </div>
        </div>
        <div class="info-box">
          <div class="text-sm font-bold mb-2 section-title">系统架构</div>
          <div class="text-sm space-y-1 info-list">
            <div>架构类型: {{ seResult.scada_architecture }}</div>
            <div>网络拓扑: {{ seResult.network_topology }}</div>
            <div>冗余等级: {{ seResult.redundancy_level }}</div>
            <div>加密方式: {{ seResult.encryption_type }}</div>
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
