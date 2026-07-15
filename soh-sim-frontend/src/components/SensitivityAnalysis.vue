<template>
  <div class="sensitivity-analysis h-full overflow-auto p-4">
    <div class="rounded-lg p-4 ins-1">
      <h3 class="text-sm font-bold mb-4 flex items-center gap-2 ins-2">
        <span class="w-2 h-2 rounded-full ins-3" />
        {{ $t('sensitivity.title') }}
      </h3>

      <!-- 敏感性参数设置 -->
      <div class="grid grid-cols-4 gap-4 mb-4">
        <!-- 参数选择 -->
        <div class="rounded-lg p-3 ins-4">
          <div class="text-xs mb-3 ins-5">{{ $t('sensitivity.selectParam') }}</div>
          <div class="space-y-2">
            <label
              v-for="param in sensitivityParams"
              :key="param.key"
              class="flex items-center gap-2 cursor-pointer text-xs label-text"
            >
              <input v-model="param.enabled" type="checkbox" class="ins-6" />
              <span class="ins-7">
                {{ $t('sensitivity.paramLabel', { label: param.label }) }}
              </span>
            </label>
          </div>
        </div>

        <!-- 参数范围设置 -->
        <div class="col-span-3 rounded-lg p-3 ins-4">
          <div class="text-xs mb-3 ins-5">{{ $t('sensitivity.range') }}</div>

          <div class="grid grid-cols-3 gap-3">
            <div v-for="param in enabledParams" :key="param.key">
              <div class="text-xs mb-1 ins-7">
                {{ $t('sensitivity.paramLabel', { label: param.label }) }}
              </div>
              <div class="flex items-center gap-1">
                <input
                  v-model.number="param.min"
                  type="number"
                  step="0.01"
                  class="w-16 rounded text-xs px-2 py-1 form-field-input"
                />
                <span class="text-xs ins-5">{{ $t('sensitivity.to') }}</span>
                <input
                  v-model.number="param.max"
                  type="number"
                  step="0.01"
                  class="w-16 rounded text-xs px-2 py-1 form-field-input"
                />
              </div>
              <div class="text-[10px] mt-1 ins-5">{{ $t('sensitivity.currentValue') }}: {{ param.current }}</div>
            </div>
          </div>

          <div class="mt-3 flex items-center gap-2">
            <span class="text-xs ins-5">{{ $t('sensitivity.stepsLabel') }}</span>
            <input
              v-model.number="steps"
              type="number"
              min="3"
              max="10"
              class="w-16 rounded text-xs px-2 py-1 form-field-input"
            />
            <span class="text-xs ins-5">({{ $t('sensitivity.stepsRange') }})</span>
            <button
              :disabled="analyzing || enabledParams.length === 0"
              class="ml-auto text-xs px-4 py-1.5 rounded transition-colors"
              :style="
                analyzing || enabledParams.length === 0
                  ? { backgroundColor: 'var(--color-card-dark)', color: 'var(--color-text-muted)' }
                  : { backgroundColor: 'var(--color-warning)', color: 'white' }
              "
              @click="runAnalysis"
            >
              {{ analyzing ? $t('sensitivity.analyzing') : $t('sensitivity.runAnalysis') }}
            </button>
          </div>
        </div>
      </div>

      <!-- 分析结果 -->
      <div v-if="analysisResults.length > 0" class="grid grid-cols-2 gap-4">
        <!-- 龙卷风图 -->
        <div class="rounded-lg p-3 ins-4">
          <div class="text-xs mb-3 ins-5">{{ $t('sensitivity.tornadoRank') }}</div>
          <div ref="tornadoChart" class="h-64" />
        </div>

        <!-- 蜘蛛图 -->
        <div class="rounded-lg p-3 ins-4">
          <div class="text-xs mb-3 ins-5">{{ $t('sensitivity.spiderChart') }}</div>
          <div ref="spiderChart" class="h-64" />
        </div>
      </div>

      <!-- 详细数据表 -->
      <div v-if="analysisResults.length > 0" class="mt-4">
        <div class="text-xs mb-2 ins-5">{{ $t('sensitivity.detailData') }}</div>
        <div class="overflow-x-auto">
          <table class="w-full text-xs">
            <thead>
              <tr class="ins-8">
                <th class="text-left py-2 px-2">{{ $t('sensitivity.parameter') }}</th>
                <th v-for="(result, idx) in analysisResults" :key="idx" class="text-right py-2 px-2">
                  {{ result.param }} ({{ (result.minValue * 100).toFixed(0) }}%~{{
                    (result.maxValue * 100).toFixed(0)
                  }}%)
                </th>
              </tr>
            </thead>
            <tbody>
              <tr class="ins-9">
                <td class="py-2 px-2">{{ $t('sensitivity.npvChange') }}</td>
                <td
                  v-for="(result, idx) in analysisResults"
                  :key="idx"
                  class="text-right py-2 px-2"
                  :style="result.npvImpact > 0 ? { color: 'var(--color-success)' } : { color: 'var(--color-danger)' }"
                >
                  {{ result.npvImpact > 0 ? '+' : '' }}{{ result.npvImpact.toFixed(2) }}%
                </td>
              </tr>
              <tr class="ins-9">
                <td class="py-2 px-2">{{ $t('sensitivity.irrChange') }}</td>
                <td
                  v-for="(result, idx) in analysisResults"
                  :key="idx"
                  class="text-right py-2 px-2"
                  :style="result.irrImpact > 0 ? { color: 'var(--color-success)' } : { color: 'var(--color-danger)' }"
                >
                  {{ result.irrImpact > 0 ? '+' : '' }}{{ result.irrImpact.toFixed(2) }}%
                </td>
              </tr>
              <tr class="ins-9">
                <td class="py-2 px-2">{{ $t('sensitivity.paybackChange') }}</td>
                <td
                  v-for="(result, idx) in analysisResults"
                  :key="idx"
                  class="text-right py-2 px-2"
                  :style="
                    result.paybackImpact < 0 ? { color: 'var(--color-success)' } : { color: 'var(--color-danger)' }
                  "
                >
                  {{ result.paybackImpact > 0 ? '+' : '' }}{{ result.paybackImpact.toFixed(2)
                  }}{{ $t('sensitivity.yearUnit') }}
                </td>
              </tr>
              <tr class="ins-9">
                <td class="py-2 px-2">{{ $t('sensitivity.lcosChange') }}</td>
                <td
                  v-for="(result, idx) in analysisResults"
                  :key="idx"
                  class="text-right py-2 px-2"
                  :style="result.lcosImpact < 0 ? { color: 'var(--color-success)' } : { color: 'var(--color-danger)' }"
                >
                  {{ result.lcosImpact > 0 ? '+' : '' }}{{ result.lcosImpact.toFixed(2) }}%
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 财务指标敏感性说明 -->
      <div class="mt-4 p-3 rounded-lg ins-4">
        <div class="font-medium mb-2 ins-7">
          {{ $t('sensitivity.explanationTitle') }}
        </div>
        <ul class="list-disc list-inside space-y-1 text-xs ins-5">
          <li>{{ $t('sensitivity.explanationNpv') }}</li>
          <li>{{ $t('sensitivity.explanationIrr') }}</li>
          <li>{{ $t('sensitivity.explanationPayback') }}</li>
          <li>{{ $t('sensitivity.explanationLcos') }}</li>
        </ul>
      </div>
    </div>

    <!-- Toast提示 -->
    <div
      v-if="toast.show"
      class="fixed bottom-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all"
      :style="{
        backgroundColor: toast.type === 'success' ? 'var(--color-success)' : 'var(--color-danger)',
        color: 'white'
      }"
    >
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { useDraft, useDraftRef } from '../composables/useDraft'
import { useSensitivityCharts } from '../composables/useSensitivityCharts.js'
import { post } from '../services/api.js'
import { DEFAULT_SURVEY, DEFAULT_DOD } from '../stores/bess.js'
const { t } = useI18n()

const props = defineProps({
  params: { type: Object, default: () => ({}) },
  financial: { type: Object, default: () => ({}) }
})

const { state: sensitivityParams } = useDraft('sensitivity-params', [
  {
    key: 'electricityPrice',
    labelKey: 'sensitivity.params.electricityPrice',
    enabled: true,
    min: 0.3,
    max: 0.8,
    current: 0.5,
    unit: 'sensitivity.params.unitPrice'
  },
  {
    key: 'inflationRate',
    labelKey: 'sensitivity.params.inflationRate',
    enabled: true,
    min: 0.01,
    max: 0.05,
    current: 0.03,
    unit: ''
  },
  {
    key: 'discountRate',
    labelKey: 'sensitivity.params.discountRate',
    enabled: false,
    min: 0.05,
    max: 0.12,
    current: 0.08,
    unit: ''
  },
  {
    key: 'bessCost',
    labelKey: 'sensitivity.params.bessCost',
    enabled: true,
    min: 0.8,
    max: 1.5,
    current: 1.0,
    unit: 'sensitivity.params.unitCost'
  },
  {
    key: 'efficiency',
    labelKey: 'sensitivity.params.efficiency',
    enabled: false,
    min: 0.85,
    max: 0.99,
    current: 0.92,
    unit: ''
  },
  { key: 'subsidy', labelKey: 'sensitivity.params.subsidy', enabled: false, min: 0.5, max: 1.5, current: 1.0, unit: '' }
])

const steps = useDraftRef('sensitivity-steps', 5).state
const analyzing = ref(false)
const analysisResults = ref([])
const tornadoChart = ref(null)
const spiderChart = ref(null)
const { updateTornadoChart, updateSpiderChart } = useSensitivityCharts(analysisResults, tornadoChart, spiderChart)

const toast = reactive({
  show: false,
  message: '',
  type: 'success'
})

const enabledParams = computed(() => sensitivityParams.filter((p) => p.enabled))

const showToast = (message, type = 'success') => {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => {
    toast.show = false
  }, 3000)
}

// 运行敏感性分析
async function runAnalysis() {
  if (enabledParams.value.length === 0) {
    showToast(t('sensitivity.selectParamMsg'), 'error')
    return
  }

  analyzing.value = true
  analysisResults.value = []

  try {
    // 对每个启用的参数进行分析
    for (const param of enabledParams.value) {
      const result = await analyzeSingleParam(param)
      analysisResults.value.push(result)
    }

    // 更新图表
    nextTick(() => {
      updateTornadoChart()
      updateSpiderChart()
    })

    showToast(t('sensitivity.analysisComplete'))
  } catch (error) {
    console.error(t('sensitivity.analysisFailed'), error)
    showToast(t('sensitivity.analysisFailed') + ': ' + error.message, 'error')
  } finally {
    analyzing.value = false
  }
}

// 分析单个参数
async function analyzeSingleParam(param) {
  const minValue = param.min
  const maxValue = param.max

  const stepSize = (maxValue - minValue) / (steps.value - 1)
  const values = Array.from({ length: steps.value }, (_, i) => minValue + i * stepSize)

  const npvValues = []
  const irrValues = []
  const paybackValues = []
  const lcosValues = []

  for (const value of values) {
    const testParams = { ...props.params, [param.key]: value }

    try {
      // 构建仿真请求
      const simBody = {
        design_output: {
          container: { ratedEnergyMwh: testParams.ratedEnergy || DEFAULT_SURVEY.ratedEnergy },
          pcs: { ratedPowerMW: testParams.pcsPower || 2.5 },
          containerQty: testParams.initContainerQty || 10,
          pcsQty: testParams.initPcsQty || 2,
          duration: testParams.duration || DEFAULT_SURVEY.duration
        },
        survey_params: {
          ratedEnergy: testParams.ratedEnergy || DEFAULT_SURVEY.ratedEnergy,
          temperature: testParams.temperature || DEFAULT_SURVEY.temperature,
          cyclesPerDay: testParams.cyclesPerDay || DEFAULT_SURVEY.cyclesPerDay,
          dod: DEFAULT_DOD,
          requiredEnergy: testParams.requiredEnergy || DEFAULT_SURVEY.requiredEnergy
        }
      }
      const simResult = await post('/api/simulation/run', simBody)

      if (simResult.success && simResult.data) {
        const totalAcUsable = simResult.data.totalAcUsable || []
        // 调用财务引擎
        const finBody = {
          simulation_output: {
            totalAcUsable: totalAcUsable,
            soh: simResult.data.soh || [],
            rte: simResult.data.rte || [],
            meetsReq: simResult.data.meetsReq || []
          },
          design_output: simBody.design_output,
          survey_params: simBody.survey_params
        }
        const finResult = await post('/api/financial/calculate', finBody)

        if (finResult.success && finResult.data) {
          const financial = finResult.data.metrics || {}
          npvValues.push(financial.npv || 0)
          irrValues.push(financial.irr || financial.projectIrr || 0)
          paybackValues.push(financial.payback || financial.paybackYears || 0)
          lcosValues.push(financial.lcos || financial.lcoe || 0)
        } else {
          npvValues.push(0)
          irrValues.push(0)
          paybackValues.push(0)
          lcosValues.push(0)
        }
      } else {
        npvValues.push(0)
        irrValues.push(0)
        paybackValues.push(0)
        lcosValues.push(0)
      }
    } catch (error) {
      npvValues.push(0)
      irrValues.push(0)
      paybackValues.push(0)
      lcosValues.push(0)
    }
  }

  // 计算影响（变化百分比）
  const baseFinancial = props.financial || {}
  const baseNpv = baseFinancial.npv || 0
  const baseIrr = baseFinancial.irr || 0
  const baseLcos = baseFinancial.lcos || 0

  // 使用最大值和最小值的差异作为敏感性指标
  const npvRange = Math.max(...npvValues) - Math.min(...npvValues)
  const irrRange = Math.max(...irrValues) - Math.min(...irrValues)
  const paybackRange = Math.max(...paybackValues) - Math.min(...paybackValues)
  const lcosRange = Math.max(...lcosValues) - Math.min(...lcosValues)

  // 计算相对于基准的影响百分比
  const npvImpact = baseNpv !== 0 ? (npvRange / Math.abs(baseNpv)) * 100 : 0
  const irrImpact = baseIrr !== 0 ? (irrRange / Math.abs(baseIrr)) * 100 : 0
  const paybackImpact = paybackRange
  const lcosImpact = baseLcos !== 0 ? (lcosRange / Math.abs(baseLcos)) * 100 : 0

  return {
    param: param.labelKey ? t(param.labelKey) : param.label,
    paramKey: param.labelKey || param.label,
    minValue,
    maxValue,
    values,
    npvValues,
    irrValues,
    paybackValues,
    lcosValues,
    npvImpact,
    irrImpact,
    paybackImpact,
    lcosImpact,
    // 综合敏感性得分
    sensitivityScore: (Math.abs(npvImpact) + Math.abs(irrImpact) + Math.abs(lcosImpact)) / 3
  }
}
</script>

<style scoped>
.ins-1 {
  background-color: var(--color-card);
  border: 1px solid var(--color-border);
}
.ins-2 {
  color: var(--color-accent);
}
.ins-3 {
  background-color: var(--color-accent);
}
.ins-4 {
  background-color: var(--color-card-dark);
}
.ins-5 {
  color: var(--color-text-muted);
}
.ins-6 {
  accent-color: var(--color-accent);
}
.ins-7 {
  color: var(--color-text-secondary);
}
.ins-8 {
  color: var(--color-text-muted);
  border-bottom: 1px solid var(--color-border);
}
.ins-9 {
  color: var(--color-text-secondary);
  border-bottom: 1px solid var(--color-border);
}

.sensitivity-analysis {
  height: 100%;
}
input:focus,
select:focus,
textarea:focus {
  border-color: var(--color-input-focus);
  outline: none;
}

button:not(:disabled):hover {
  opacity: 0.9;
}
</style>
