<template>
  <div class="h-full overflow-auto p-4">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg font-bold text-accent-2">{{ $t('auxCalc.title') }}</h2>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-4 gap-3 mb-4">
      <div class="rounded-xl p-4 card-bordered">
        <div class="text-xs font-bold mb-2 text-muted">{{ $t('auxCalc.totalAux') }}</div>
        <div class="text-2xl font-bold text-default">
          {{ results.totalSystemAux.toFixed(2) }}
          <span class="text-sm ml-1 text-accent-2">MWh</span>
        </div>
      </div>
      <div class="rounded-xl p-4 card-bordered">
        <div class="text-xs font-bold mb-2 text-muted">{{ $t('auxCalc.singleDaily') }}</div>
        <div class="text-2xl font-bold text-default">
          {{ results.singleUnitDailykWh.toFixed(2) }}
          <span class="text-sm ml-1 text-accent-2">{{ $t('auxCalc.kwhPerUnitDay') }}</span>
        </div>
      </div>
      <div class="rounded-xl p-4 card-bordered">
        <div class="text-xs font-bold mb-2 text-muted">{{ $t('auxCalc.poiNet') }}</div>
        <div class="text-2xl font-bold text-default">
          {{ results.annualNetDischarge.toFixed(2) }}
          <span class="text-sm ml-1 text-accent-2">MWh</span>
        </div>
      </div>
      <div class="rounded-xl p-4 card-bordered">
        <div class="text-xs font-bold mb-2 text-muted">{{ $t('auxCalc.runtime') }}</div>
        <div class="text-2xl font-bold text-default">
          {{ results.tRun.toFixed(1) }}
          <span class="text-sm ml-1 text-accent-2">{{ $t('auxCalc.hours') }}</span>
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
              {{ $t('auxCalc.formulaSandbox') }}
            </h3>
            <span class="text-xs px-2 py-1 rounded-full font-bold" :class="statusStyle">{{ statusText }}</span>
          </div>

          <div class="rounded-lg p-3 mb-3 bg-card-dark">
            <div class="flex justify-between items-center mb-2">
              <span class="text-xs font-bold text-accent-2">{{ $t('auxCalc.dcTotalAux') }}</span>
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
              {{ $t('auxCalc.days') }} ×
              <input
                v-model.number="state.cycles"
                type="number"
                step="0.5"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              {{ $t('auxCalc.times') }} ×
              <input
                v-model.number="state.hours"
                type="number"
                step="0.5"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              h ×
              <span class="text-muted">2</span>
              ×
              <input
                v-model.number="state.bRun"
                type="number"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              kW) + (
              <span class="text-muted">24</span>
              h -
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
              <span class="text-muted">2</span>
              ) ×
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
              {{ $t('auxCalc.dcPhysics') }}
            </div>
          </div>

          <div class="rounded-lg p-3 mb-3 bg-card-dark">
            <div class="flex justify-between items-center mb-2">
              <span class="text-xs font-bold text-accent-2">{{ $t('auxCalc.acTotalAux') }}</span>
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
              <span class="text-muted">2</span>
              ×
              <input
                v-model.number="state.pRun"
                type="number"
                step="0.5"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              kW) + (
              <span class="text-muted">24</span>
              h -
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
              <span class="text-muted">2</span>
              ) ×
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
              <span class="text-muted">24</span>
              h ×
              <input
                v-model.number="state.pStation"
                type="number"
                step="0.5"
                class="w-10 text-center bg-transparent border border-current outline-none rounded px-1"
              />
              kW] / 1000
            </div>
            <div class="text-[10px] mt-2 text-muted">
              {{ $t('auxCalc.acPhysics') }}
            </div>
          </div>

          <div class="rounded-lg p-3 mb-3 bg-card-dark">
            <div class="flex justify-between items-center mb-2">
              <span class="text-xs font-bold text-accent-2">{{ $t('auxCalc.totalSystemAux') }}</span>
              <span class="text-xs px-2 py-0.5 rounded font-bold bg-accent-2 text-white">
                {{ results.totalSystemAux.toFixed(2) }} MWh
              </span>
            </div>
            <div class="text-xs font-mono rounded p-2 bg-input-dark text-default">
              Total_Aux = {{ results.dcTotalAux.toFixed(2) }} MWh + {{ results.acTotalAux.toFixed(2) }} MWh
            </div>
            <div class="text-[10px] mt-2 text-muted">
              {{ $t('auxCalc.totalPhysics') }}
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
              {{ $t('auxCalc.poiPhysics') }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuxPower } from '../composables/useAuxPower.js'
import AuxParamPanel from './AuxParamPanel.vue'

const { t } = useI18n()
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
    return t('auxCalc.stageMode', { days: state.days })
  }
  if (results.value.annualNetDischarge >= 210000) {
    return t('auxCalc.annualPass')
  }
  return t('auxCalc.annualFail')
})
</script>

<style scoped src="../assets/styles/aux-power.css"></style>
