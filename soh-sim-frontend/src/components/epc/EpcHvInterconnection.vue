<template>
  <div class="epc-panel space-y-4">
    <div class="panel-card">
      <h3 class="panel-title">高压接入设计</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <div>
          <label class="block text-xs mb-1 field-label">总功率 (MW)</label>
          <input v-model.number="hvForm.total_power_mw" type="number" class="form-field-input" placeholder="100" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">并网点电压 (kV)</label>
          <input v-model.number="hvForm.poc_voltage_kv" type="number" class="form-field-input" placeholder="33" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">短路容量 (MVA)</label>
          <input
            v-model.number="hvForm.short_circuit_capacity_mva"
            type="number"
            class="form-field-input"
            placeholder="500"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">并网点类型</label>
          <select v-model="hvForm.poc_type" class="form-field-select">
            <option value="substation">变电站</option>
            <option value="overhead_line">架空线</option>
            <option value="cable">电缆</option>
          </select>
        </div>
      </div>
      <button :disabled="loading" class="btn-primary" @click="designHV">
        {{ loading ? '设计中...' : '执行高压接入设计' }}
      </button>

      <div v-if="hvResult" class="mt-6 space-y-4">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div class="metric-card">
            <div class="metric-value">{{ hvResult.transformer_count }}</div>
            <div class="metric-label">变压器数量</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ hvResult.transformer_capacity_mva }}MVA</div>
            <div class="metric-label">变压器容量</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ hvResult.transformer_ratio }}</div>
            <div class="metric-label">变比</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ hvResult.mv_breaker_rating_ka }}kA</div>
            <div class="metric-label">断路器额定值</div>
          </div>
        </div>
        <div v-if="hvResult.protection_scheme" class="info-box">
          <div class="text-sm font-bold mb-2 section-title">保护配置</div>
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
