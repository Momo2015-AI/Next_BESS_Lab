<template>
  <div class="home-page h-full overflow-auto p-8">
    <div class="max-w-5xl mx-auto">
      <div class="mb-8">
        <h1 class="text-2xl font-bold" style="color: #2F5496;">BESS 储能项目设计评估平台</h1>
        <p class="text-sm mt-2" style="color: #666;">按照实际储能项目流程，从立项到交付逐步完成设计评估</p>
      </div>

      <div class="flow-dashboard">
        <div v-for="(phase, key) in phases" :key="key" class="phase-row" @click="gotoPhase(key)">
          <div class="phase-indicator" :class="'status-' + getPhaseStatus(key)">
            <span class="phase-number">{{ phase.num }}</span>
            <span v-if="getPhaseStatus(key) === 'completed'" class="check">&#10003;</span>
          </div>
          <div class="phase-info">
            <div class="phase-title">{{ phase.title }}</div>
            <div class="phase-desc">{{ phase.desc }}</div>
          </div>
          <div class="phase-status-badge">
            <span :class="'badge badge-' + getPhaseStatus(key)">{{ statusText(getPhaseStatus(key)) }}</span>
          </div>
        </div>
      </div>

      <div class="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="summary-card">
          <div class="summary-label">当前 SOH</div>
          <div class="summary-value">{{ store.degradation.soh[0].toFixed(2) }}%</div>
        </div>
        <div class="summary-card">
          <div class="summary-label">NPV</div>
          <div class="summary-value">{{ store.financial.metrics.npv.toFixed(0) }} 万元</div>
        </div>
        <div class="summary-card">
          <div class="summary-label">IRR</div>
          <div class="summary-value">{{ store.financial.metrics.irr.toFixed(2) }}%</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useBessStore } from '../stores/bess.js'

const router = useRouter()
const store = useBessStore()

const phases = {
  phase1: { num: 1, title: '项目立项', desc: '调研填表、选址评估、需求确认', path: '/phase1' },
  phase2: { num: 2, title: '系统设计', desc: '技术选型、直流/交流侧设计、系统集成配置', path: '/phase2' },
  phase3: { num: 3, title: '性能分析', desc: 'SOH/RTE 衰减预测、25年容量对账、可视化分析', path: '/phase3' },
  phase4: { num: 4, title: '经济评估', desc: 'CAPEX/OPEX估算、财务指标、敏感性分析', path: '/phase4' },
  phase5: { num: 5, title: '成果输出', desc: '技术报告、设备清单、数据导出、项目存档', path: '/phase5' },
}

function getPhaseStatus(phase) {
  return store.phases[phase]?.status || 'pending'
}

function statusText(status) {
  const map = { pending: '未开始', in_progress: '进行中', completed: '已完成' }
  return map[status] || '未开始'
}

function gotoPhase(phase) {
  router.push(phases[phase].path)
}
</script>

<style scoped>
.flow-dashboard {
  background: #fff; border-radius: 12px; border: 1px solid #E0E0E0; padding: 8px 0;
}
.phase-row {
  display: flex; align-items: center; padding: 16px 24px; cursor: pointer;
  transition: background 0.15s; gap: 16px;
}
.phase-row:hover { background: #F5F7FA; }
.phase-row:not(:last-child) { border-bottom: 1px solid #F0F0F0; }
.phase-indicator {
  width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center;
  justify-content: center; flex-shrink: 0; position: relative; font-size: 14px; font-weight: 700;
}
.status-pending { background: #f0f0f0; color: #999; }
.status-in_progress { background: #E8EEF5; color: #2F5496; }
.status-completed { background: #e6f7e6; color: #2e7d32; }
.check { font-size: 18px; }
.phase-info { flex: 1; min-width: 0; }
.phase-title { font-size: 16px; font-weight: 600; color: #2F5496; }
.phase-desc { font-size: 13px; color: #666; margin-top: 2px; }
.phase-status-badge { flex-shrink: 0; }
.badge { padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; }
.badge-pending { background: #f0f0f0; color: #999; }
.badge-in_progress { background: #E8EEF5; color: #2F5496; }
.badge-completed { background: #e6f7e6; color: #2e7d32; }
.summary-card {
  background: #fff; border: 1px solid #E0E0E0; border-radius: 8px; padding: 20px; text-align: center;
}
.summary-label { font-size: 13px; color: #666; margin-bottom: 8px; }
.summary-value { font-size: 24px; font-weight: 700; color: #2F5496; }
</style>
