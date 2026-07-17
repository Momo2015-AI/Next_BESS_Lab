<template>
  <div class="flex flex-col gap-4 h-full overflow-auto p-4">
    <div class="flex items-center gap-2 p-2 rounded-lg card-step">
      <div
        v-for="(step, idx) in steps"
        :key="idx"
        :class="[
          'flex items-center gap-1 px-3 py-1 rounded text-xs transition-all cursor-pointer hover:opacity-80',
          currentStep >= idx ? 'text-teal-400 step-active' : 'text-slate-500'
        ]"
        @click="currentStep = idx"
      >
        <span
          class="w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold"
          :class="currentStep >= idx ? 'step-num-active' : 'step-num-inactive'"
        >
          {{ idx + 1 }}
        </span>
        {{ $t(step.label) }}
      </div>
    </div>

    <!-- Step 0: Survey Data -->
    <div v-show="currentStep === 0">
      <SurveySelector
        :survey-list="surveyList"
        :search-results="searchResults"
        @load="loadSurveyData"
        @search="searchByProjectName"
        @select-survey="selectSurvey"
      />

      <div class="mt-4 grid grid-cols-3 gap-3">
        <div class="rounded p-3 card-panel-bordered">
          <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelRatedEnergy') }}</label>
          <input
            v-model.number="surveyData.ratedEnergy"
            type="number"
            step="0.1"
            class="w-full rounded px-2 py-1 text-xs card-input text-accent"
          />
        </div>
        <div class="rounded p-3 card-panel-bordered">
          <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelContainerQty') }}</label>
          <input
            v-model.number="surveyData.containerQty"
            type="number"
            class="w-full rounded px-2 py-1 text-xs card-input text-accent"
          />
        </div>
        <div class="rounded p-3 card-panel-bordered">
          <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelPcsQty') }}</label>
          <input
            v-model.number="surveyData.pcsQty"
            type="number"
            class="w-full rounded px-2 py-1 text-xs card-input text-accent"
          />
        </div>
        <div class="rounded p-3 card-panel-bordered">
          <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelTemperature') }}</label>
          <input
            v-model.number="surveyData.temperature"
            type="number"
            step="0.5"
            class="w-full rounded px-2 py-1 text-xs card-input text-accent"
          />
        </div>
        <div class="rounded p-3 card-panel-bordered">
          <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelCyclesPerDay') }}</label>
          <input
            v-model.number="surveyData.cyclesPerDay"
            type="number"
            step="0.5"
            class="w-full rounded px-2 py-1 text-xs card-input text-accent"
          />
        </div>
        <div class="rounded p-3 card-panel-bordered">
          <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelDod') }}</label>
          <input
            v-model.number="surveyData.dod"
            type="number"
            step="1"
            min="0"
            max="100"
            class="w-full rounded px-2 py-1 text-xs card-input text-accent"
          />
        </div>
        <div class="rounded p-3 card-panel-bordered">
          <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelCRate') }}</label>
          <input
            v-model.number="surveyData.cRate"
            type="number"
            step="0.1"
            min="0.1"
            max="2"
            class="w-full rounded px-2 py-1 text-xs card-input text-accent"
          />
        </div>
        <div class="rounded p-3 card-panel-bordered">
          <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelBatteryType') }}</label>
          <select v-model="surveyData.batteryType" class="w-full rounded px-2 py-1 text-xs card-input text-accent">
            <option value="LFP">{{ $t('simLab.batteryLfp') }}</option>
            <option value="NCM">{{ $t('simLab.batteryNcm') }}</option>
            <option value="LTO">{{ $t('simLab.batteryLto') }}</option>
          </select>
        </div>
        <ComboboxInput
          v-model="countryInput"
          :options="countryOptions"
          :placeholder="$t('simLab.labelCountry')"
          :empty-text="$t('simLab.noMatch')"
          wrapper-class="rounded p-3 card-panel-bordered"
          label-class="text-[10px] block mb-1 text-muted"
          :label="$t('simLab.labelCountry')"
          @select="
            (opt) => {
              surveyData.country = opt.label
            }
          "
        />
        <div class="rounded p-3 card-panel-bordered">
          <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelCity') }}</label>
          <input
            v-model="surveyData.city"
            type="text"
            class="w-full rounded px-2 py-1 text-xs card-input text-accent"
          />
        </div>
        <div class="rounded p-3 card-panel-bordered">
          <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelSite') }}</label>
          <input
            v-model="surveyData.site"
            type="text"
            class="w-full rounded px-2 py-1 text-xs card-input text-accent"
          />
        </div>
      </div>

      <div class="mt-3 text-[10px] text-muted">
        {{ $t('simLab.annualThroughput') }}: {{ annualEnergyThroughput }} MWh/yr
      </div>

      <div class="mt-4 flex justify-end">
        <button class="text-xs px-4 py-2 rounded transition-all btn-accent-filled" @click="nextStep">
          {{ $t('simLab.btnNextParams') }}
        </button>
      </div>
    </div>

    <!-- Step 1: Simulation Params -->
    <div v-show="currentStep === 1" class="rounded-lg p-4 card-panel">
      <h3 class="text-sm font-bold mb-3 flex items-center gap-2 text-accent">
        <span class="w-2 h-2 rounded-full bg-accent" />
        {{ $t('simLab.titleParamsComplete') }}
      </h3>

      <div class="grid grid-cols-4 gap-3">
        <div class="col-span-4 rounded p-3 card-panel-bordered">
          <h4 class="text-xs mb-2 font-medium">{{ $t('simLab.sectionBasic') }}</h4>
          <div class="grid grid-cols-4 gap-3">
            <div>
              <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelSimYears') }}</label>
              <select
                v-model.number="simParams.simulationYears"
                class="w-full rounded px-2 py-1 text-xs card-input"
                @change="initYearlyCorrections"
              >
                <option v-for="n in [10, 15, 20, 25, 30]" :key="n" :value="n">{{ $t('simLab.years', { n }) }}</option>
              </select>
            </div>
            <div>
              <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelGuaranteeYears') }}</label>
              <select v-model.number="simParams.guaranteeYears" class="w-full rounded px-2 py-1 text-xs card-input">
                <option v-for="n in [5, 10, 15, 20]" :key="n" :value="n">{{ $t('simLab.years', { n }) }}</option>
              </select>
            </div>
            <div>
              <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelGuaranteeSoh') }}</label>
              <input
                v-model.number="simParams.guaranteeSoh"
                type="number"
                step="1"
                min="60"
                max="90"
                class="w-full rounded px-2 py-1 text-xs card-input"
              />
            </div>
            <div>
              <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelRequiredEnergy') }}</label>
              <input
                v-model.number="simParams.requiredEnergy"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs card-input"
              />
            </div>
          </div>
        </div>

        <div class="col-span-2 rounded p-3 card-panel-bordered">
          <h4 class="text-xs mb-2 font-medium">{{ $t('simLab.sectionEfficiency') }}</h4>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelInitRte') }}</label>
              <input
                v-model.number="simParams.initRte"
                type="number"
                step="0.1"
                min="85"
                max="95"
                class="w-full rounded px-2 py-1 text-xs card-input"
              />
            </div>
            <div>
              <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelAcEfficiency') }}</label>
              <input
                v-model.number="simParams.acEfficiency"
                type="number"
                step="0.1"
                min="95"
                max="99"
                class="w-full rounded px-2 py-1 text-xs card-input"
              />
            </div>
            <div>
              <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelDcEfficiency') }}</label>
              <input
                v-model.number="simParams.dcEfficiency"
                type="number"
                step="0.1"
                min="95"
                max="99"
                class="w-full rounded px-2 py-1 text-xs card-input"
              />
            </div>
            <div>
              <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelSelfDischarge') }}</label>
              <input
                v-model.number="simParams.selfDischarge"
                type="number"
                step="0.1"
                min="0"
                max="5"
                class="w-full rounded px-2 py-1 text-xs card-input"
              />
            </div>
          </div>
          <div class="mt-2 space-y-1">
            <div class="text-[10px] text-muted">{{ $t('simLab.systemRTE') }}: {{ systemRTE }}%</div>
            <div class="text-[10px] text-muted">
              {{ $t('simLab.grossEnergyPreview') }}: {{ grossEnergyPreview }} MWh
            </div>
          </div>
        </div>

        <div class="col-span-2 rounded p-3 card-panel-bordered">
          <div class="flex items-center justify-between mb-2">
            <h4 class="text-xs font-medium">{{ $t('simLab.sectionAux') }}</h4>
            <div class="flex items-center gap-1 text-[10px]">
              <span class="text-muted">{{ $t('simLab.auxModeLabel') }}:</span>
              <button
                :class="[
                  'px-2 py-0.5 rounded transition-all',
                  simParams.auxPowerMode === 'manual' ? 'bg-accent text-white' : 'text-muted hover:text-secondary'
                ]"
                @click="simParams.auxPowerMode = 'manual'"
              >
                {{ $t('simLab.auxModeManual') }}
              </button>
              <button
                :class="[
                  'px-2 py-0.5 rounded transition-all',
                  simParams.auxPowerMode === 'thermal' ? 'bg-accent text-white' : 'text-muted hover:text-secondary'
                ]"
                @click="simParams.auxPowerMode = 'thermal'"
              >
                {{ $t('simLab.auxModeThermal') }}
              </button>
            </div>
          </div>

          <div v-if="simParams.auxPowerMode === 'manual'">
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelBessAuxRun') }}</label>
                <input
                  v-model.number="simParams.bessAuxRun"
                  type="number"
                  step="0.1"
                  class="w-full rounded px-2 py-1 text-xs card-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelBessAuxStandby') }}</label>
                <input
                  v-model.number="simParams.bessAuxStandby"
                  type="number"
                  step="0.1"
                  class="w-full rounded px-2 py-1 text-xs card-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelPcsAuxRun') }}</label>
                <input
                  v-model.number="simParams.pcsAuxRun"
                  type="number"
                  step="0.1"
                  class="w-full rounded px-2 py-1 text-xs card-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelPcsAuxStandby') }}</label>
                <input
                  v-model.number="simParams.pcsAuxStandby"
                  type="number"
                  step="0.1"
                  class="w-full rounded px-2 py-1 text-xs card-input"
                />
              </div>
            </div>
            <div class="mt-2 text-[10px] text-muted space-y-0.5">
              <div class="flex justify-between">
                <span>{{ $t('simLab.totalRunAux') }}:</span>
                <span class="text-accent">{{ totalRunAux }} kW</span>
              </div>
              <div class="flex justify-between">
                <span>{{ $t('simLab.totalStandbyAux') }}:</span>
                <span class="text-accent">{{ totalStandbyAux }} kW</span>
              </div>
            </div>
          </div>

          <div v-else class="space-y-2">
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.ambientTempLabel') }}</label>
                <input
                  v-model.number="simParams.ambientTemp"
                  type="number"
                  step="0.5"
                  class="w-full rounded px-2 py-1 text-xs card-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.coolingTypeLabel') }}</label>
                <select v-model="simParams.coolingType" class="w-full rounded px-2 py-1 text-xs card-input">
                  <option value="forced-air">{{ $t('simLab.coolingTypes.forcedAir') }}</option>
                  <option value="liquid">{{ $t('simLab.coolingTypes.liquid') }}</option>
                  <option value="SiC-liquid">{{ $t('simLab.coolingTypes.SiCLiquid') }}</option>
                </select>
              </div>
            </div>
            <div class="rounded p-2 text-[10px] space-y-0.5" style="background: var(--color-input-bg)">
              <div class="flex justify-between text-muted">
                <span>{{ $t('simLab.coolingPowerEstimate') }}</span>
                <span class="text-secondary">{{ estimatedCoolingPower?.coolingkW ?? '—' }} kW</span>
              </div>
              <div class="flex justify-between text-muted">
                <span>{{ $t('simLab.fixedAuxNote') }}</span>
                <span class="text-secondary">{{ FIXED_AUX }} kW</span>
              </div>
              <div
                class="flex justify-between font-medium"
                style="border-top: 1px solid var(--color-border); padding-top: 2px; margin-top: 2px"
              >
                <span>= {{ $t('simLab.labelBessAuxRun') }}</span>
                <span class="text-accent">{{ estimatedCoolingPower?.totalRunkW ?? '—' }} kW</span>
              </div>
              <div class="flex justify-between text-muted">
                <span>{{ $t('simLab.standbyAuxNote') }}</span>
                <span class="text-secondary">{{ estimatedCoolingPower?.standbykW ?? '—' }} kW</span>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelPcsAuxRun') }}</label>
                <input
                  v-model.number="simParams.pcsAuxRun"
                  type="number"
                  step="0.1"
                  class="w-full rounded px-2 py-1 text-xs card-input"
                />
              </div>
              <div>
                <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelPcsAuxStandby') }}</label>
                <input
                  v-model.number="simParams.pcsAuxStandby"
                  type="number"
                  step="0.1"
                  class="w-full rounded px-2 py-1 text-xs card-input"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-4 flex justify-between">
        <button class="text-xs px-4 py-2 rounded transition-all theme-btn-secondary" @click="prevStep">
          {{ $t('simLab.btnPrev') }}
        </button>
        <button class="text-xs px-4 py-2 rounded transition-all btn-accent-filled" @click="nextStep">
          {{ $t('simLab.btnNextAlgorithm') }}
        </button>
      </div>
    </div>

    <!-- Step 2: Algorithm Selection -->
    <div v-show="currentStep === 2" class="rounded-lg p-4 card-panel">
      <AlgorithmSelector
        :algorithms="algorithms"
        :selected-id="selectedAlgorithm"
        :selected-detail="selectedAlgoDetail"
        :algo-params="algoParams"
        @select="selectAlgorithm"
        @reset-params="resetAlgoParams"
        @update-param="({ key, value }) => (algoParams[key] = value)"
      />

      <div
        v-if="selectedAlgorithm === 'builtin-ai_simulation'"
        class="mt-4 rounded p-4 card-panel-bordered theme-border-accent"
      >
        <h4 class="text-xs font-bold mb-3 flex items-center gap-2 text-accent">
          <span>🤖</span>
          {{ $t('simLab.titleAiConfig') }}
        </h4>
        <div class="grid grid-cols-3 gap-3">
          <div>
            <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelManufacturer') }}</label>
            <ComboboxInput
              v-model="mfrInput"
              :options="manufacturerOptions"
              :placeholder="$t('simLab.manufacturerPlaceholder')"
              :empty-text="$t('simLab.noMatch')"
              @select="onMfrSelect"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelSimYears') }}</label>
            <input
              v-model.number="aiSimParams.simulationYears"
              type="number"
              min="1"
              max="40"
              class="w-full rounded px-2 py-1 text-xs card-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelTemperature') }}</label>
            <input
              v-model.number="aiSimParams.temperature"
              type="number"
              step="0.5"
              min="-20"
              max="60"
              class="w-full rounded px-2 py-1 text-xs card-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelDailyCycles') }}</label>
            <input
              v-model.number="aiSimParams.cyclesPerDay"
              type="number"
              step="0.5"
              min="0.5"
              max="3"
              class="w-full rounded px-2 py-1 text-xs card-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelDischargeDod') }}</label>
            <input
              v-model.number="aiSimParams.dod"
              type="number"
              step="1"
              min="20"
              max="100"
              class="w-full rounded px-2 py-1 text-xs card-input"
            />
          </div>
          <div>
            <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelChargeRate') }}</label>
            <input
              v-model.number="aiSimParams.cRate"
              type="number"
              step="0.1"
              min="0.1"
              max="2"
              class="w-full rounded px-2 py-1 text-xs card-input"
            />
          </div>
        </div>
        <div v-if="selectedManufacturer" class="mt-3 rounded p-2 card-panel">
          <p class="text-[10px] text-muted">
            <strong class="text-accent">{{ selectedManufacturer.name }}</strong>
            - {{ selectedManufacturer.description }}
          </p>
          <div class="flex gap-4 mt-1">
            <span class="text-[10px] text-secondary">
              {{ $t('simLab.rmseSohLabel') }}: {{ selectedManufacturer.rmse_soh }}%
            </span>
            <span class="text-[10px] text-secondary">
              {{ $t('simLab.rmseRteLabel') }}: {{ selectedManufacturer.rmse_rte }}%
            </span>
            <span class="text-[10px] text-secondary">
              {{ $t('simLab.dataPoints') }}: {{ selectedManufacturer.data_points }}
            </span>
          </div>
        </div>
      </div>

      <div class="mt-4 flex justify-between">
        <button class="text-xs px-4 py-2 rounded transition-all theme-btn-secondary" @click="prevStep">
          {{ $t('simLab.btnPrev') }}
        </button>
        <button class="text-xs px-4 py-2 rounded transition-all btn-accent-filled" @click="nextStep">
          {{ $t('simLab.btnNextCorrection') }}
        </button>
      </div>
    </div>

    <!-- Step 3: Correction Factors -->
    <div v-show="currentStep === 3" class="rounded-lg p-4 card-panel">
      <CorrectionFactorsPanel
        :factors="correctionFactors"
        :yearly-data="yearlyCorrections"
        @update:soh-factor="correctionFactors.sohFactor = $event"
        @update:rte-factor="correctionFactors.rteFactor = $event"
        @update:capacity-factor="correctionFactors.capacityFactor = $event"
        @update:aging-factor="correctionFactors.agingFactor = $event"
        @update:yearly="
          ({ idx, field, value }) => {
            if (yearlyCorrections[idx]) yearlyCorrections[idx][field] = value
          }
        "
      />

      <div class="mt-4 flex justify-between">
        <button class="text-xs px-4 py-2 rounded transition-all theme-btn-secondary" @click="prevStep">
          {{ $t('simLab.btnPrev') }}
        </button>
        <button
          :disabled="!selectedAlgorithm"
          class="text-xs px-6 py-2 rounded font-bold transition-all"
          :class="selectedAlgorithm ? 'btn-gradient-ready' : 'btn-disabled-muted'"
          @click="runSimulation"
        >
          {{ $t('simLab.btnFrontendCalc') }}
        </button>
        <button
          :disabled="!selectedAlgorithm"
          class="text-xs px-6 py-2 rounded font-bold transition-all"
          :class="selectedAlgorithm ? 'btn-gradient-accent' : 'btn-disabled-muted'"
          @click="runBackendSimulation"
        >
          {{ $t('simLab.btnBackendCalc') }}
        </button>
      </div>
    </div>

    <!-- Step 4: Results -->
    <div v-show="currentStep === 4" class="rounded-lg p-4 card-panel">
      <SimulationResults
        ref="resultsComp"
        :results="simulationResults"
        :guarantee-soh="simParams.guaranteeSoh"
        @save="saveSimulationResult"
        @re-simulate="resetSimulation"
        @export="exportResults"
      />
    </div>

    <!-- Toast -->
    <div
      v-if="toast.show"
      :class="[
        'fixed top-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all',
        toast.type === 'success' ? 'bg-emerald-500 text-white' : 'bg-red-500 text-white'
      ]"
    >
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useBessStore, DEFAULT_DOD } from '../stores/bess.js'
import { useDraft, useDraftRef } from '../composables/useDraft'
import api from '../services/api.js'
import { useCountryList } from '../composables/useCountryList'
import ComboboxInput from './ComboboxInput.vue'
import SurveySelector from './SurveySelector.vue'
import AlgorithmSelector from './AlgorithmSelector.vue'
import CorrectionFactorsPanel from './CorrectionFactorsPanel.vue'
import SimulationResults from './SimulationResults.vue'

const emit = defineEmits(['applyConfig', 'error'])
const { t } = useI18n()
const store = useBessStore()
const { filterCountries } = useCountryList()

// ====== Wizard ======
const steps = [
  { label: 'simLab.stepSurvey' },
  { label: 'simLab.stepParams' },
  { label: 'simLab.stepAlgorithm' },
  { label: 'simLab.stepCorrection' },
  { label: 'simLab.stepResults' }
]
const currentStep = useDraftRef('sim-current-step', 0).state
function nextStep() {
  if (currentStep.value < steps.length - 1) currentStep.value++
}
function prevStep() {
  if (currentStep.value > 0) currentStep.value--
}

// ====== Survey lookup ======
const surveyList = ref([])
const searchResults = ref([])

async function fetchSurveyList() {
  try {
    const data = await api.get('/api/survey/list?per_page=200')
    surveyList.value = Array.isArray(data.data) ? data.data : data.data?.items || []
  } catch (e) {
    console.error('[SimulationLab] 获取调研表列表失败:', e)
  }
}

async function loadSurveyData() {
  const surveyId = useDraftRef('sim-survey-id', '').state
  if (!surveyId.value) {
    emit('error', t('simLab.enterSurveyId'), 'warning')
    return
  }
  try {
    const data = await api.get(`/api/survey/${surveyId.value}`)
    mapSurveyData(data.data)
  } catch (e) {
    emit('error', e.status === 404 ? t('simLab.surveyNotFound') : t('simLab.networkErrorManual'), 'warning')
  }
}

async function searchByProjectName(keyword) {
  if (!keyword?.trim()) {
    emit('error', t('simLab.enterProjectKeyword'), 'warning')
    return
  }
  try {
    const data = await api.get(`/api/survey/search?keyword=${encodeURIComponent(keyword)}`)
    if (data.success) {
      searchResults.value = data.data?.surveys || []
      if (!searchResults.value.length) emit('error', t('simLab.noMatchingProject'), 'warning')
    }
  } catch {
    emit('error', t('simLab.networkErrorSearch'), 'error')
  }
}

function selectSurvey(survey) {
  searchResults.value = []
  const surveyId = useDraftRef('sim-survey-id', '').state
  surveyId.value = survey.id
  mapSurveyData(survey)
}

function mapSurveyData(data) {
  surveyData.projectName = data.project_name || ''
  surveyData.ratedEnergy = data.total_mwh || 5
  surveyData.containerQty = data.container_qty || 1
  surveyData.pcsQty = data.pcs_qty || 1
  surveyData.temperature = data.temp_avg || 25
  surveyData.cyclesPerDay = data.cycles_per_day || 1
  surveyData.dod = data.dod || 100
  surveyData.cRate = data.c_rate || 0.5
  surveyData.batteryType = data.battery_type || 'LFP'
  surveyData.country = data.country || ''
  surveyData.city = data.city || ''
  surveyData.site = data.site || ''
  if (!surveyData.country && !surveyData.city && !surveyData.site && data.location) surveyData.site = data.location
  simParams.requiredEnergy = data.total_mwh || 240
}

// ====== Survey data form ======
const { state: surveyData } = useDraft('sim-survey-data', {
  projectName: '',
  ratedEnergy: 5,
  containerQty: 62,
  pcsQty: 1,
  temperature: 25,
  cyclesPerDay: 1,
  dod: DEFAULT_DOD,
  cRate: 0.5,
  batteryType: 'LFP',
  location: '',
  country: '',
  city: '',
  site: ''
})

// ====== Country combobox ======
const countryInput = ref('')
const countryOptions = computed(() => {
  return filterCountries(countryInput.value).map((c) => ({ label: c, value: c }))
})
watch(
  () => surveyData.country,
  (val) => {
    if (val && val !== countryInput.value) countryInput.value = val
  }
)

// ====== Simulation params ======
const { state: simParams } = useDraft('sim-params', {
  simulationYears: 25,
  guaranteeYears: 10,
  guaranteeSoh: 70,
  requiredEnergy: 240,
  initRte: 94.1,
  acEfficiency: 97.03,
  dcEfficiency: 98.5,
  selfDischarge: 2,
  bessAuxRun: 18.124,
  bessAuxStandby: 3.5,
  pcsAuxRun: 6.5,
  pcsAuxStandby: 1.0,
  auxPowerMode: 'manual',
  coolingType: 'liquid',
  ambientTemp: 25
})

// ====== Cooling estimates ======
const FIXED_AUX = 3.0
const COP_MAP = { 'forced-air': 2.0, liquid: 3.5, 'SiC-liquid': 5.0 }
const estimatedCoolingPower = computed(() => {
  if (simParams.auxPowerMode !== 'thermal') return null
  const ambient = simParams.ambientTemp || 25
  const cop = COP_MAP[simParams.coolingType] || COP_MAP.liquid
  const cellAh = 280,
    cellR = 0.00025,
    cRate = 0.5,
    cells = 5000
  const cellHeatkW = ((cellAh * cRate) ** 2 * cellR * cells) / 1000
  const deltaT = Math.max(0, ambient - 25)
  const infiltrationkW = (0.5 * 60 * deltaT) / 1000
  const totalHeatkW = (cellHeatkW + infiltrationkW) * 1.2
  const coolingkW = totalHeatkW / cop
  return {
    coolingkW: +coolingkW.toFixed(2),
    standbykW: +(coolingkW * 0.15).toFixed(2),
    totalRunkW: +(coolingkW + FIXED_AUX).toFixed(2),
    cellHeatkW: +cellHeatkW.toFixed(2),
    infiltrationkW: +infiltrationkW.toFixed(2),
    cop
  }
})

const systemRTE = computed(
  () => +(((((simParams.acEfficiency || 97) / 100) * (simParams.dcEfficiency || 98.5)) / 100) * 100).toFixed(2)
)
const annualEnergyThroughput = computed(
  () => +(surveyData.ratedEnergy || 0) * (surveyData.containerQty || 0) * (surveyData.cyclesPerDay || 1) * 365
)
const totalRunAux = computed(() =>
  simParams.auxPowerMode === 'thermal'
    ? estimatedCoolingPower.value?.totalRunkW || 0
    : (simParams.bessAuxRun || 0) + (simParams.pcsAuxRun || 0)
)
const totalStandbyAux = computed(() =>
  simParams.auxPowerMode === 'thermal'
    ? estimatedCoolingPower.value?.standbykW || 0
    : (simParams.bessAuxStandby || 0) + (simParams.pcsAuxStandby || 0)
)
const grossEnergyPreview = computed(() => {
  const energy = surveyData.ratedEnergy || 0
  const qty = surveyData.containerQty || 0
  const dod = (surveyData.dod || 100) / 100
  const rte = systemRTE.value / 100
  const acEff = (simParams.acEfficiency || 97) / 100
  return +(energy * qty * dod * rte * 1.0 * acEff).toFixed(1)
})

// ====== Algorithm state ======
const selectedAlgorithm = useDraftRef('sim-selected-algorithm', '').state
const algorithms = ref([])
const algoParams = reactive({})
const selectedAlgoDetail = ref(null)

function selectAlgorithm(algo) {
  selectedAlgorithm.value = algo.id
  selectedAlgoDetail.value = algo
  Object.keys(algoParams).forEach((k) => delete algoParams[k])
  if (algo.parameters)
    Object.keys(algo.parameters).forEach((key) => {
      algoParams[key] = algo.parameters[key].default || 0
    })
}
function resetAlgoParams() {
  const algo = selectedAlgoDetail.value
  if (!algo?.parameters) return
  Object.keys(algo.parameters).forEach((key) => {
    algoParams[key] = algo.parameters[key].default || 0
  })
  showToast(t('simLab.paramsReset'))
}
watch(selectedAlgorithm, (newId) => {
  if (newId) {
    const algo = algorithms.value.find((a) => a.id === newId)
    if (algo) selectAlgorithm(algo)
  }
})

// ====== AI / Manufacturers ======
const manufacturers = ref([])
const mfrInput = ref('')
const aiSimParams = reactive({
  manufacturerId: '',
  simulationYears: 25,
  temperature: 25,
  cyclesPerDay: 1,
  dod: DEFAULT_DOD,
  cRate: 0.5
})
const selectedManufacturer = computed(() => manufacturers.value.find((m) => m.id === aiSimParams.manufacturerId))
const manufacturerOptions = computed(() =>
  manufacturers.value.map((m) => ({ label: m.name, value: m.id, sub: m.chemistry_type || '' }))
)
function onMfrSelect(opt) {
  aiSimParams.manufacturerId = opt.value
}
watch(selectedManufacturer, (mfr) => {
  if (mfr && !mfrInput.value) mfrInput.value = mfr.name
})

async function fetchAlgorithms() {
  try {
    const data = await api.get('/api/algorithm/builtin_models')
    if (data.success && data.data.length > 0) {
      algorithms.value = data.data.map((alg) => ({
        id: alg.id,
        name: alg.name,
        name_en: alg.name_en || '',
        description: alg.description || t('simLab.noDescription'),
        type: getCategoryLabel(alg.category),
        accuracy: alg.accuracy_desc || t('simLab.unknown'),
        model_type: alg.model_type,
        parameters: alg.parameters,
        mathematical_form: alg.mathematical_form || '',
        formula_expression: alg.formula_expression || ''
      }))
    }
  } catch (e) {
    console.error('Failed to fetch algorithms:', e)
  }
  if (!algorithms.value.length) {
    const { BUILTIN_DEGRADATION_ALGORITHMS, mapToSimulationLabFormat } = await import('../data/builtinAlgorithms.js')
    algorithms.value = BUILTIN_DEGRADATION_ALGORITHMS.map(mapToSimulationLabFormat)
  }
  if (!selectedAlgorithm.value && algorithms.value.length > 0) {
    selectedAlgorithm.value = algorithms.value[0].id
    selectAlgorithm(algorithms.value[0])
  }
}

async function fetchManufacturers() {
  try {
    const data = await api.get('/api/ai-sim/manufacturers')
    if (data.success && data.data.length > 0) manufacturers.value = data.data
  } catch (e) {
    console.error('Failed to fetch manufacturers:', e)
  }
}

function getCategoryLabel(category) {
  const labels = {
    degradation: t('simLab.catDegradation'),
    financial: t('simLab.catFinancial'),
    engineering: t('simLab.catEngineering'),
    simulation: t('simLab.catSimulation')
  }
  return labels[category] || category
}

// ====== Correction factors ======
const { state: correctionFactors } = useDraft('sim-correction-factors', {
  sohFactor: 1.0,
  rteFactor: 1.0,
  capacityFactor: 1.0,
  agingFactor: 1.0
})
const yearlyCorrections = useDraftRef('sim-yearly-corrections', []).state
function initYearlyCorrections() {
  yearlyCorrections.value = []
  for (let i = 0; i <= simParams.simulationYears; i++)
    yearlyCorrections.value.push({ year: i, sohCorrection: 0, rteCorrection: 0 })
}

// ====== Results ======
const simulationResults = reactive({
  initSoh: null,
  guaranteeEndSoh: null,
  finalSoh: null,
  meetsGuarantee: false,
  sohCurve: [],
  rteCurve: [],
  netAvailCurve: [],
  tableData: []
})
const resultsComp = ref(null)

// ====== SOH calculation engine ======
function calculateSOH(modelType, params, t) {
  const R = 8.314
  const T = surveyData.temperature + 273.15
  const N_cycles = surveyData.cyclesPerDay * 365 * t
  const DOD_factor = Math.pow(surveyData.dod / 100, 0.5)
  const C_rate_factor = Math.pow(surveyData.cRate, 0.3)
  switch (modelType) {
    case 'double_exponential':
      return params.A * Math.exp(-params.k1 * t) + params.B * Math.exp(-params.k2 * t) + params.C
    case 'linear_log':
      return params.RTE0 - params.alpha * t - params.beta * Math.log(1 + params.gamma * t)
    case 'arrhenius': {
      const Q_cal = params.A * Math.exp((-params.Ea * 1000) / (R * T)) * Math.pow(t + 0.5, 0.5)
      const Q_cyc =
        params.A * Math.exp((-params.Ea * 1000) / (R * T)) * Math.pow(N_cycles, 0.7) * DOD_factor * C_rate_factor
      return Math.max(0.6, 1 - (Q_cal + Q_cyc))
    }
    case 'rainflow': {
      const damage =
        Math.pow(N_cycles / params.cycle_life_ref, params.damage_exponent) *
        Math.pow(surveyData.dod / 100 / params.dod_ref, 1.5)
      return Math.max(0.6, 1 - damage)
    }
    case 'semi_empirical': {
      const temp_factor = 1 - (params.temp_coeff * (surveyData.temperature - 25)) / 100
      const dod_factor = 1 - (params.dod_coeff * (surveyData.dod / 100 - 0.5)) / 100
      const c_rate_factor = 1 - params.c_rate_coeff * (surveyData.cRate - 0.5)
      return Math.max(0.6, 1 - ((1 - temp_factor * dod_factor * c_rate_factor * 0.98) * t) / 25)
    }
    default: {
      const A_cal = params.A_cal || 0.001
      const Ea_cal = params.Ea_cal || 35
      const alpha = params.alpha || 0.5
      const A_cyc = params.A_cyc || 0.00001
      const Ea_cyc = params.Ea_cyc || 25
      const beta = params.beta || 0.7
      const Q_cal = A_cal * Math.exp((-Ea_cal * 1000) / (R * T)) * Math.pow(t + 0.5, alpha)
      const Q_cyc = A_cyc * Math.exp((-Ea_cyc * 1000) / (R * T)) * Math.pow(N_cycles, beta) * DOD_factor * C_rate_factor
      return Math.max(0.6, 1 - (Q_cal + Q_cyc))
    }
  }
}

// ====== Simulation runners ======
function buildSohCurves(algo, getSoh) {
  const N = simParams.simulationYears + 1
  const sohCurve = []
  const rteCurve = []
  const netAvailCurve = []
  for (let i = 0; i < N; i++) {
    let soh = getSoh(i)
    soh = soh * correctionFactors.sohFactor
    if (yearlyCorrections.value[i]?.sohCorrection) soh += yearlyCorrections.value[i].sohCorrection
    let rte = simParams.initRte / 100 - 0.002 * i * correctionFactors.rteFactor
    if (yearlyCorrections.value[i]?.rteCorrection) rte += yearlyCorrections.value[i].rteCorrection
    const grossEnergy =
      surveyData.ratedEnergy *
      surveyData.containerQty *
      (surveyData.dod / 100) *
      rte *
      soh *
      (simParams.acEfficiency / 100)
    const bessAux =
      simParams.auxPowerMode === 'thermal' && estimatedCoolingPower.value
        ? estimatedCoolingPower.value.totalRunkW
        : simParams.bessAuxRun
    const auxEnergy = ((bessAux + simParams.pcsAuxRun) * i) / 1000
    const netAvail = Math.max(0, grossEnergy - auxEnergy) * correctionFactors.capacityFactor
    sohCurve.push(Math.min(100, Math.max(60, soh * 100)))
    rteCurve.push(Math.min(100, Math.max(80, rte * 100)))
    netAvailCurve.push(netAvail)
  }
  return { sohCurve, rteCurve, netAvailCurve }
}

function populateResults(curves) {
  const N = curves.sohCurve.length
  simulationResults.sohCurve = curves.sohCurve
  simulationResults.rteCurve = curves.rteCurve
  simulationResults.netAvailCurve = curves.netAvailCurve
  simulationResults.initSoh = curves.sohCurve[0]
  simulationResults.guaranteeEndSoh = curves.sohCurve[simParams.guaranteeYears]
  simulationResults.finalSoh = curves.sohCurve[N - 1]
  simulationResults.meetsGuarantee = curves.sohCurve[simParams.guaranteeYears] >= simParams.guaranteeSoh
  simulationResults.tableData = []
  for (let i = 0; i < N; i++) {
    simulationResults.tableData.push({
      year: i,
      soh: curves.sohCurve[i],
      rte: curves.rteCurve[i],
      netAvail: curves.netAvailCurve[i],
      meetsReq: curves.netAvailCurve[i] >= simParams.requiredEnergy
    })
  }
  store.degradation.soh = [...curves.sohCurve]
  store.degradation.rte = [...curves.rteCurve]
  store.results.totalAcUsable = [...curves.netAvailCurve]
  store.results.meetsReq = simulationResults.tableData.map((d) => d.meetsReq)
  emit('applyConfig', {
    soh: curves.sohCurve,
    rte: curves.rteCurve,
    source: 'simulation',
    simulationYears: simParams.simulationYears,
    guaranteeSoh: simParams.guaranteeSoh,
    auxPowerMode: simParams.auxPowerMode,
    coolingType: simParams.coolingType,
    ambientTemp: simParams.ambientTemp
  })
}

async function runSimulation() {
  currentStep.value = 4
  const algo = algorithms.value.find((a) => a.id === selectedAlgorithm.value)
  if (algo?.model_type === 'ai_simulation') {
    await runAISimulation()
    return
  }
  const curves = buildSohCurves(algo, (t) => calculateSOH(algo?.model_type || 'arrhenius', algoParams, t))
  populateResults(curves)
}

async function runAISimulation() {
  try {
    const result = await api.post('/api/ai-sim/simulation', {
      manufacturer_id: aiSimParams.manufacturerId || null,
      simulation_years: aiSimParams.simulationYears,
      temperature: aiSimParams.temperature,
      cycles_per_day: aiSimParams.cyclesPerDay,
      dod: aiSimParams.dod / 100,
      c_rate: aiSimParams.cRate,
      rte_initial: simParams.initRte
    })
    if (result.success && result.data) {
      const aiData = result.data
      const N = aiData.soh_curve.length
      simulationResults.sohCurve = aiData.soh_curve
      simulationResults.rteCurve = aiData.rte_curve
      simulationResults.initSoh = aiData.soh_curve[0]
      simulationResults.guaranteeEndSoh = aiData.soh_curve[Math.min(simParams.guaranteeYears, N - 1)]
      simulationResults.finalSoh = aiData.soh_curve[N - 1]
      simulationResults.meetsGuarantee = simulationResults.guaranteeEndSoh >= simParams.guaranteeSoh
      simulationResults.netAvailCurve = []
      simulationResults.tableData = []
      for (let i = 0; i < N; i++) {
        const soh = aiData.soh_curve[i] / 100
        const rte = aiData.rte_curve[i] / 100
        const grossEnergy =
          surveyData.ratedEnergy *
          surveyData.containerQty *
          (aiSimParams.dod / 100) *
          rte *
          soh *
          (simParams.acEfficiency / 100)
        const bessAuxAi =
          simParams.auxPowerMode === 'thermal' && estimatedCoolingPower.value
            ? estimatedCoolingPower.value.totalRunkW
            : simParams.bessAuxRun
        const auxEnergy = ((bessAuxAi + simParams.pcsAuxRun) * i) / 1000
        const netAvail = Math.max(0, grossEnergy - auxEnergy)
        simulationResults.netAvailCurve.push(netAvail)
        simulationResults.tableData.push({
          year: i,
          soh: aiData.soh_curve[i],
          rte: aiData.rte_curve[i],
          netAvail,
          meetsReq: netAvail >= simParams.requiredEnergy
        })
      }
      emit('applyConfig', {
        soh: simulationResults.sohCurve,
        rte: simulationResults.rteCurve,
        source: 'ai_simulation',
        simulationYears: aiSimParams.simulationYears,
        guaranteeSoh: simParams.guaranteeSoh,
        auxPowerMode: simParams.auxPowerMode,
        coolingType: simParams.coolingType,
        ambientTemp: simParams.ambientTemp
      })
      showToast(t('simLab.aiSimComplete'))
    } else {
      showToast(result.error || t('simLab.aiSimFailed'), 'error')
    }
  } catch (e) {
    showToast(t('simLab.aiSimFailedWithError', { message: e.message }), 'error')
  }
}

async function runBackendSimulation() {
  currentStep.value = 4
  try {
    const algo = algorithms.value.find((a) => a.id === selectedAlgorithm.value)
    const modelType = algo?.model_type || 'arrhenius'
    const modelParams = {}
    if (algo?.parameters) {
      for (const [key, cfg] of Object.entries(algo.parameters)) {
        modelParams[key] = algoParams[key] ?? cfg.default
      }
    }
    const body = {
      design_output: {
        container: { ratedEnergyMWh: surveyData.ratedEnergy || store.systemParams.ratedEnergy },
        pcs: { ratedPowerMW: store.systemParams.pcsPower },
        containerQty: surveyData.containerQty || store.systemParams.initContainerQty,
        pcsQty: store.systemParams.initPcsQty,
        duration: surveyData.duration || store.systemParams.duration
      },
      survey_params: {
        ratedEnergy: surveyData.ratedEnergy || store.systemParams.ratedEnergy,
        temperature: surveyData.temperature || store.systemParams.temperature,
        cyclesPerDay: surveyData.cyclesPerDay || store.systemParams.cyclesPerDay,
        dod: surveyData.dod || store.systemParams.dod || 80,
        requiredEnergy: store.systemParams.requiredEnergy,
        cRate: store.systemParams.cRate || 0.5,
        auxPowerMode: simParams.auxPowerMode || store.systemParams.auxPowerMode,
        ambientTemp: simParams.ambientTemp || store.systemParams.ambientTemp,
        coolingType: simParams.coolingType || store.systemParams.coolingType
      },
      degradation: {
        soh: [...store.degradation.soh],
        rte: [...store.degradation.rte],
        dod: [...store.degradation.dod],
        augQty: [...store.degradation.augQty]
      },
      algorithm: {
        model: modelType,
        correctionFactor: correctionFactors.sohFactor || 1.0,
        modelParams: Object.keys(modelParams).length > 0 ? modelParams : undefined
      }
    }
    const data = await api.post('/api/simulation/run', body)
    if (data.success && data.data) {
      const result = data.data
      const sohArr = result.soh || []
      const rteArr = result.rte || []
      simulationResults.sohCurve = sohArr
      simulationResults.rteCurve = rteArr
      simulationResults.netAvailCurve = result.totalAcUsable || []
      simulationResults.initSoh = sohArr[0] || 100
      simulationResults.finalSoh = sohArr[sohArr.length - 1] || 0
      simulationResults.guaranteeEndSoh = sohArr[simParams.guaranteeYears] || 0
      simulationResults.meetsGuarantee = (sohArr[simParams.guaranteeYears] || 0) >= simParams.guaranteeSoh
      simulationResults.tableData = sohArr.map((s, i) => ({
        year: i,
        soh: s,
        rte: rteArr[i] || 0,
        netAvail: (result.totalAcUsable || [])[i] || 0,
        meetsReq: (result.meetsReq || [])[i] || false
      }))
      store.results = {
        ...store.results,
        totalAcUsable: result.totalAcUsable || [],
        initGross: result.initGross || [],
        initAux: result.initAux || [],
        meetsReq: result.meetsReq || [],
        augGross: result.augGross || [],
        augAux: result.augAux || [],
        augAcUsable: result.augAcUsable || [],
        augAccumQty: result.augAccumQty || []
      }
      store.degradation.soh = [...sohArr]
      store.degradation.rte = [...rteArr]
      if (result.dod) store.degradation.dod = [...result.dod]
      if (result.augQty) store.degradation.augQty = [...result.augQty]
      emit('applyConfig', {
        soh: sohArr,
        rte: rteArr,
        source: 'backend-simulation',
        simulationYears: simParams.simulationYears,
        guaranteeSoh: simParams.guaranteeSoh
      })
    }
  } catch (e) {
    console.error('Backend simulation error:', e)
  }
}

// ====== Save / Export / Reset ======
async function saveSimulationResult() {
  const token = sessionStorage.getItem('auth_token')
  if (!token) {
    showToast(t('simLab.pleaseLogin'), 'error')
    return
  }
  const algo = algorithms.value.find((a) => a.id === selectedAlgorithm.value)
  const projectName = surveyData.projectName || t('simLab.unnamedProject')
  const timestamp = new Date().toISOString().slice(0, 19).replace(/[-T:]/g, '')
  const data = {
    name: `${projectName}_${timestamp}`,
    description: t('simLab.descriptionTemplate', { algo: algo?.name || t('simLab.unknown') }),
    simulation_type: algo?.category || 'comprehensive',
    algorithm_model_id: selectedAlgorithm.value,
    params: {
      surveyData,
      simParams,
      algoParams: { ...algoParams },
      correctionFactors: { ...correctionFactors },
      yearlyCorrections: yearlyCorrections.value
    },
    results: {
      sohCurve: simulationResults.sohCurve,
      rteCurve: simulationResults.rteCurve,
      netAvailCurve: simulationResults.netAvailCurve,
      tableData: simulationResults.tableData
    },
    summary: {
      initSoh: simulationResults.initSoh,
      guaranteeEndSoh: simulationResults.guaranteeEndSoh,
      finalSoh: simulationResults.finalSoh,
      meetsGuarantee: simulationResults.meetsGuarantee
    },
    status: 'completed'
  }
  try {
    const respData = await api.post('/api/versions/default/results', data)
    if (respData.success) showToast(t('simLab.saveSuccess'))
    else showToast(respData.error || t('simLab.saveFailed'), 'error')
  } catch (e) {
    showToast(t('simLab.saveFailedWithError', { message: e.message }), 'error')
  }
}

function exportResults() {
  const N = simulationResults.tableData.length
  if (!N) return
  const eq = t('export.eqHeader')
  const sep = t('export.separator')
  const date = new Date().toISOString().slice(0, 10)
  const projectName = surveyData.projectName || store.survey.projectName || t('simLab.csvUnnamed')
  const header = [
    eq,
    '  ' + t('export.reportTitle'),
    '  ' + t('export.projectName') + ': ' + projectName,
    '  ' + t('export.generatedDate') + ': ' + date,
    '  ' + t('export.version') + ': v1.0',
    eq,
    ''
  ]
  const params = [
    sep + ' ' + t('export.keyParams') + ' ' + sep,
    t('export.ratedEnergy') + ',' + (store.systemParams.ratedEnergy || store.survey.ratedEnergy || 'N/A'),
    t('export.totalPower') + ',' + (store.systemParams.pcsPower || store.survey.totalPower || 'N/A'),
    t('export.duration') + ',' + (store.systemParams.duration || store.survey.duration || 'N/A'),
    t('export.simYears') + ',' + N,
    ''
  ]
  const csvRows = [
    [t('export.colYear'), t('export.colSoh'), t('export.colRte'), t('export.colAvail'), t('export.colGuarantee')].join(
      ','
    ),
    ...simulationResults.tableData.map((r) =>
      [
        r.year,
        r.soh != null ? r.soh.toFixed(2) : '',
        r.rte != null ? r.rte.toFixed(2) : '',
        r.netAvail != null ? r.netAvail.toFixed(1) : '',
        r.meetsReq ? t('simLab.pass') : t('simLab.fail')
      ].join(',')
    )
  ]
  const footer = ['', sep, t('export.disclaimer')]
  const csvContent = [...header, ...params, ...csvRows, ...footer].join('\n')
  const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = t('simLab.simExportFilename', { name: projectName, date })
  link.click()
}

function resetSimulation() {
  currentStep.value = 0
  simulationResults.initSoh = null
  simulationResults.guaranteeEndSoh = null
  simulationResults.finalSoh = null
  simulationResults.meetsGuarantee = false
  simulationResults.sohCurve = []
  simulationResults.rteCurve = []
  simulationResults.netAvailCurve = []
  simulationResults.tableData = []
}

// ====== Toast ======
const toast = reactive({ show: false, message: '', type: 'success' })
function showToast(message, type = 'success') {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => {
    toast.show = false
  }, 3000)
}

// ====== Lifecycle ======
onMounted(async () => {
  try {
    await fetchSurveyList()
    const designRatedEnergy = store.systemParams.ratedEnergy || store.survey.ratedEnergy
    if (designRatedEnergy && (surveyData.ratedEnergy === 5 || !surveyData.ratedEnergy))
      surveyData.ratedEnergy = designRatedEnergy
    const designContainerQty = store.systemParams.initContainerQty
    if (designContainerQty && (surveyData.containerQty === 62 || !surveyData.containerQty))
      surveyData.containerQty = designContainerQty
    const designReqEnergy = store.survey.requiredEnergy || store.systemParams.requiredEnergy
    if (designReqEnergy && (simParams.requiredEnergy === 240 || !simParams.requiredEnergy))
      simParams.requiredEnergy = designReqEnergy
    const designTemp = store.survey.temperature
    if (designTemp && (surveyData.temperature === 25 || !surveyData.temperature)) surveyData.temperature = designTemp
    const designDod = store.survey.dod
    if (designDod && (surveyData.dod === 100 || !surveyData.dod)) surveyData.dod = designDod
    const designCRate = store.survey.cRate
    if (designCRate && (surveyData.cRate === 0.5 || !surveyData.cRate)) surveyData.cRate = designCRate
    const designPcsQty = store.systemParams.initPcsQty
    if (designPcsQty && (surveyData.pcsQty === 2 || !surveyData.pcsQty)) surveyData.pcsQty = designPcsQty
    if (
      store.results.totalAcUsable?.length &&
      Array.isArray(store.degradation?.soh) &&
      Array.isArray(store.degradation?.rte)
    ) {
      try {
        const rawSoh = [...store.degradation.soh]
        const needsPct = rawSoh.length > 0 && rawSoh[0] <= 1
        const sohPct = needsPct ? rawSoh.map((v) => (v != null ? v * 100 : 0)) : rawSoh
        simulationResults.sohCurve = sohPct
        simulationResults.rteCurve = [...store.degradation.rte]
        simulationResults.netAvailCurve = [...store.results.totalAcUsable]
        simulationResults.initSoh = sohPct[0] ?? 100
        simulationResults.finalSoh = sohPct[sohPct.length - 1] ?? 0
        simulationResults.tableData = sohPct.map((s, i) => ({
          year: i,
          soh: s ?? 0,
          rte: store.degradation.rte[i] ?? 0,
          netAvail: store.results.totalAcUsable[i] ?? 0,
          meetsReq: store.results.meetsReq?.[i] || false
        }))
      } catch (e) {
        console.error('[SimulationLab] 恢复仿真结果失败:', e)
      }
    }
    initYearlyCorrections()
    await fetchAlgorithms()
    await fetchManufacturers()
  } catch (e) {
    console.error('[SimulationLab] onMounted 初始化失败:', e)
  }
})
</script>

<style scoped>
input:focus,
select:focus,
textarea:focus {
  border-color: var(--color-input-focus);
  outline: none;
}
button:not(:disabled):hover {
  opacity: 0.9;
}
.combobox-wrapper {
  position: relative;
}
.combobox-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 999;
  max-height: 200px;
  overflow-y: auto;
  border-radius: 6px;
  background: var(--color-card);
  border: 1px solid var(--color-border);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.combobox-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 10px;
  cursor: pointer;
  font-size: 11px;
  transition: background 0.15s;
}
.combobox-option:hover,
.combobox-option.active {
  background: var(--color-accent-glow);
}
.option-name {
  color: var(--color-text);
}
.option-code {
  color: var(--color-text-secondary);
  font-size: 10px;
}
.combobox-empty {
  padding: 8px 10px;
  color: var(--color-text-secondary);
  font-size: 11px;
  text-align: center;
}
</style>
