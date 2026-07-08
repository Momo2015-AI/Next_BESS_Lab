<template>
  <div class="h-full overflow-auto p-4">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg font-bold text-accent-2">BESS 辅助功耗计算</h2>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-4 gap-3 mb-4">
      <div class="rounded-xl p-4 card-bordered">
        <div class="text-xs font-bold mb-2 text-muted">选定天数内系统总能耗</div>
        <div class="text-2xl font-bold text-default">
          {{ results.totalSystemAux.toFixed(2) }}
          <span class="text-sm ml-1 text-accent-2">MWh</span>
        </div>
      </div>
      <div class="rounded-xl p-4 card-bordered">
        <div class="text-xs font-bold mb-2 text-muted">单主仓单天平均能耗</div>
        <div class="text-2xl font-bold text-default">
          {{ results.singleUnitDailyKwh.toFixed(2) }}
          <span class="text-sm ml-1 text-accent-2">kWh/台·天</span>
        </div>
      </div>
      <div class="rounded-xl p-4 card-bordered">
        <div class="text-xs font-bold mb-2 text-muted">POI并网点最终净电量</div>
        <div class="text-2xl font-bold text-default">
          {{ results.annualNetDischarge.toFixed(2) }}
          <span class="text-sm ml-1 text-accent-2">MWh</span>
        </div>
      </div>
      <div class="rounded-xl p-4 card-bordered">
        <div class="text-xs font-bold mb-2 text-muted">选定天数内累计运行时间</div>
        <div class="text-2xl font-bold text-default">
          {{ results.tRun.toFixed(1) }}
          <span class="text-sm ml-1 text-accent-2">小时</span>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <AuxParamPanel v-model="state" />

      <div class="space-y-4">
        <div class="rounded-xl p-4 card-bordered">
          <div class="flex justify-between items-center mb-3">
            <h3 class="text-sm font-medium flex items-center gap-2 text-secondary">
              <span class="w-1 h-4 rounded bg-accent-2" />
              公式沙盒与实时账本推导
            </h3>
            <span class="text-xs px-2 py-1 rounded-full font-bold" :class="statusStyle">{{ statusText }}</span>
          </div>

          <div class="rounded-lg p-3 mb-3 bg-card-dark">
            <div class="flex justify-between items-center mb-2">
              <span class="text-xs font-bold text-accent-2">1. 直流侧总能耗 (DC Total Aux)</span>
              <span class="text-xs px-2 py-0.5 rounded font-bold bg-accent-2 text-white">
                {{ results.dcTotalAux.toFixed(2) }} MWh
              </span>
            </div>
            <div class="text-xs font-mono rounded p-2 bg-input-dark text-default">
              DC_Aux = [(
              <input
                v-model.number="state.days"
                type="number"
                class="w-12 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              天 ×
              <input
                v-model.number="state.cycles"
                type="number"
                step="0.5"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              次 ×
              <input
                v-model.number="state.hours"
                type="number"
                step="0.5"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              h ×
              <span>2</span>
              class="text-muted" ×
              <input
                v-model.number="state.bRun"
                type="number"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              kW) + (
              <span>24</span>
              class="text-muted" h -
              <input
                v-model.number="state.cycles"
                type="number"
                step="0.5"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              次 ×
              <input
                v-model.number="state.hours"
                type="number"
                step="0.5"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              h ×
              <span>2</span>
              class="text-muted" ) ×
              <input
                v-model.number="state.days"
                type="number"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              天 ×
              <input
                v-model.number="state.bStd"
                type="number"
                step="0.5"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              kW] ×
              <input
                v-model.number="state.units"
                type="number"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              台 / 1000
            </div>
            <div class="text-[10px] mt-2 text-muted">
              物理解析：运行态能耗按往返次数计算，待机态能耗按总时间减去运行时间计算，两者相加乘以台数折算为MWh。
            </div>
          </div>

          <div class="rounded-lg p-3 mb-3 bg-card-dark">
            <div class="flex justify-between items-center mb-2">
              <span class="text-xs font-bold text-accent-2">2. 交流侧总能耗 (AC Total Aux)</span>
              <span class="text-xs px-2 py-0.5 rounded font-bold bg-accent-2 text-white">
                {{ results.acTotalAux.toFixed(2) }} MWh
              </span>
            </div>
            <div class="text-xs font-mono rounded p-2 bg-input-dark text-default">
              AC_Aux = [(
              <input
                v-model.number="state.days"
                type="number"
                class="w-12 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              天 ×
              <input
                v-model.number="state.cycles"
                type="number"
                step="0.5"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              次 ×
              <input
                v-model.number="state.hours"
                type="number"
                step="0.5"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              h ×
              <span>2</span>
              class="text-muted" ×
              <input
                v-model.number="state.pRun"
                type="number"
                step="0.5"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              kW) + (
              <span>24</span>
              class="text-muted" h -
              <input
                v-model.number="state.cycles"
                type="number"
                step="0.5"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              次 ×
              <input
                v-model.number="state.hours"
                type="number"
                step="0.5"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              h ×
              <span>2</span>
              class="text-muted" ) ×
              <input
                v-model.number="state.days"
                type="number"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              天 ×
              <input
                v-model.number="state.pStd"
                type="number"
                step="0.5"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              kW +
              <input
                v-model.number="state.days"
                type="number"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              天 ×
              <span>24</span>
              class="text-muted" h ×
              <input
                v-model.number="state.pStation"
                type="number"
                step="0.5"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              kW] / 1000
            </div>
            <div class="text-[10px] mt-2 text-muted">
              物理解析：PCS动静态耗电口径与直流侧时间序列对齐，站宇主变自耗全天候固定拉满。
            </div>
          </div>

          <div class="rounded-lg p-3 mb-3 bg-card-dark">
            <div class="flex justify-between items-center mb-2">
              <span class="text-xs font-bold text-accent-2">3. 全系统总辅助能耗 (Total System Aux)</span>
              <span class="text-xs px-2 py-0.5 rounded font-bold bg-accent-2 text-white">
                {{ results.totalSystemAux.toFixed(2) }} MWh
              </span>
            </div>
            <div class="text-xs font-mono rounded p-2 bg-input-dark text-default">
              Total_Aux = {{ results.dcTotalAux.toFixed(2) }} MWh + {{ results.acTotalAux.toFixed(2) }} MWh
            </div>
            <div class="text-[10px] mt-2 text-muted">
              物理解析：合并选定周期内全场所有动静态总耗电，作为电网POI交割结算前的扣除底数。
            </div>
          </div>

          <div class="rounded-lg p-3 bg-card-dark">
            <div class="flex justify-between items-center mb-2">
              <span class="text-xs font-bold text-accent-2">4. POI并网点期末净可用电量 (POI Net Delivery)</span>
              <span class="text-xs px-2 py-0.5 rounded font-bold bg-accent-2 text-white">
                {{ results.annualNetDischarge.toFixed(2) }} MWh
              </span>
            </div>
            <div class="text-xs font-mono rounded p-2 bg-input-dark text-default">
              POI_Net = (
              <input
                v-model.number="state.cap"
                type="number"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              MWh ×
              <input
                v-model.number="state.units"
                type="number"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              台 × {{ results.sqrtRte.toFixed(4) }} ×
              <input
                v-model.number="state.cycles"
                type="number"
                step="0.5"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              次 ×
              <input
                v-model.number="state.days"
                type="number"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              天 ×
              <input
                v-model.number="state.acEff"
                type="number"
                step="0.002"
                class="w-12 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              ×
              <input
                v-model.number="state.pcsEff"
                type="number"
                step="0.002"
                class="w-12 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              ) - {{ results.totalSystemAux.toFixed(2) }} MWh
            </div>
            <div class="text-[10px] mt-2 text-muted">
              物理解析：括号内的放电量随计算天数线性增减，扣除总能耗即为净交割电量。
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuxPower } from '../composables/useAuxPower.js'
import AuxParamPanel from './AuxParamPanel.vue'

const { state, results } = useAuxPower()

const statusStyle = computed(() => {
  if (state.days < 365) {
    return 'toast-success'
  }
  if (results.value.annualNetDischarge >= 210000) {
    return 'toast-success'
  }
  return 'toast-error'
})

const statusText = computed(() => {
  if (state.days < 365) {
    return `阶段交割模式 (${state.days}天)`
  }
  if (results.value.annualNetDischarge >= 210000) {
    return '全年交割电量合规'
  }
  return '跌破年化保底红线！'
})
</script>

<style scoped src="../assets/styles/aux-power.css"></style>
