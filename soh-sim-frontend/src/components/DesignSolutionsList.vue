<template>
  <div v-if="solutions.length > 0" class="panel-section">
    <h3 class="section-title">
      <span class="icon">📋</span>
      {{ $t('design.solutions') }} ({{ solutions.length }})
    </h3>
    <div class="solutions-grid">
      <div v-for="(sol, idx) in solutions" :key="sol.id || idx" :class="['solution-card', { recommended: idx === 0 }]">
        <div class="card-header">
          <span class="rank-badge" :class="'rank-' + (idx + 1)">#{{ idx + 1 }}</span>
          <span class="strategy-tag">{{ getStrategyLabel(sol.strategy_type) }}</span>
          <span v-if="idx === 0" class="recommend-badge">{{ $t('design.recommended') }}</span>
        </div>
        <div class="card-body">
          <div class="card-row">
            <span class="label">{{ $t('design.containerModel') }}</span>
            <span class="value">{{ sol.container?.model || '—' }}</span>
          </div>
          <div class="card-row">
            <span class="label">{{ $t('design.manufacturer') }}</span>
            <span class="value">{{ sol.container?.mfr || '—' }}</span>
          </div>
          <div class="card-row">
            <span class="label">{{ $t('design.containerQty') }}</span>
            <span class="value">{{ sol.containerQty }} {{ $t('design.units') }}</span>
          </div>
          <div class="card-row">
            <span class="label">{{ $t('design.totalEnergy') }}</span>
            <span class="value highlight">{{ sol.totalEnergyMWh }} MWh</span>
          </div>
          <div class="card-row">
            <span class="label">{{ $t('design.pcsModel') }}</span>
            <span class="value">{{ sol.pcs?.model || '—' }}</span>
          </div>
          <div class="card-row">
            <span class="label">{{ $t('design.totalPower') }}</span>
            <span class="value">{{ sol.totalPowerMW }} MW</span>
          </div>
          <div class="card-row">
            <span class="label">{{ $t('design.systemRTE') }}</span>
            <span class="value">{{ sol.efficiencyChain?.systemRTE || '—' }}%</span>
          </div>
          <div class="card-row">
            <span class="label">{{ $t('design.estimatedCapex') }}</span>
            <span class="value highlight">{{ formatCurrency(sol.estimatedCapex?.totalCapex) }}</span>
          </div>
          <div class="card-row">
            <span class="label">{{ $t('design.capexPerMWh') }}</span>
            <span class="value">{{ formatCurrency(sol.estimatedCapex?.capexPerMWh) }}/MWh</span>
          </div>
          <div v-if="sol.score" class="card-row">
            <span class="label">{{ $t('design.score') }}</span>
            <span class="value">{{ sol.score.toFixed(2) }}</span>
          </div>
        </div>
        <div class="card-footer">
          <button class="btn btn-sm" @click="$emit('select', sol)">{{ $t('design.viewDetail') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  solutions: { type: Array, default: () => [] }
})

defineEmits(['select'])

function getStrategyLabel(type) {
  const map = { economic: '经济优先', balanced: '均衡方案', flexible: '灵活分期', manufacturer: '指定厂家' }
  return map[type] || type || '—'
}

function formatCurrency(val) {
  if (val == null) return '—'
  const num = Number(val)
  if (isNaN(num)) return '—'
  if (num >= 1e8) return '$' + (num / 1e8).toFixed(2) + ' 亿'
  if (num >= 1e6) return '$' + (num / 1e6).toFixed(2) + 'M'
  if (num >= 1e3) return '$' + (num / 1e3).toFixed(0) + 'K'
  return '$' + num.toFixed(0)
}
</script>
