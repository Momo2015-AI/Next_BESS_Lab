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

    <div v-show="currentStep === 0" class="rounded-lg p-4 card-panel">
      <h3 class="text-sm font-bold mb-3 flex items-center gap-2 text-accent">
        <span class="w-2 h-2 rounded-full bg-accent" />
        {{ $t('simLab.titleSurvey') }}
      </h3>

      <div class="grid grid-cols-2 gap-4">
        <div class="space-y-2">
          <label class="text-xs text-secondary">{{ $t('simLab.labelSurveyId') }}</label>
          <div class="flex gap-2">
            <div class="combobox-wrapper flex-1">
              <input
                v-model="surveyIdInput"
                type="text"
                :placeholder="$t('simLab.placeholderSurveyId')"
                class="w-full rounded px-3 py-1.5 text-xs card-input-dark"
                @focus="onSurveyInputFocus"
                @blur="onSurveyInputBlur"
                @input="onSurveyIdInput"
                @keydown.enter.prevent="onSurveyInputEnter"
              />
              <div v-if="showDropdown && filteredSurveyList.length > 0" class="combobox-dropdown">
                <div
                  v-for="s in filteredSurveyList"
                  :key="s.id"
                  class="combobox-option"
                  :class="{ active: s.id === surveyId }"
                  @mousedown.prevent="selectSurveyFromDropdown(s)"
                >
                  <span class="option-name">{{ s.project_name }}</span>
                  <span class="option-code">{{ s.id.slice(0, 8) }}...</span>
                </div>
              </div>
              <div
                v-else-if="showDropdown && surveyIdInput && filteredSurveyList.length === 0"
                class="combobox-dropdown"
              >
                <div class="combobox-empty">{{ $t('simLab.noMatch') }}</div>
              </div>
            </div>
            <button class="text-xs px-3 py-1.5 transition-all btn-accent-filled" @click="loadSurveyData">
              {{ $t('simLab.btnLoad') }}
            </button>
          </div>
        </div>

        <div class="space-y-2">
          <label class="text-xs text-secondary">{{ $t('simLab.labelProjectSearch') }}</label>
          <div class="flex gap-2">
            <input
              v-model="searchKeyword"
              type="text"
              :placeholder="$t('simLab.placeholderProjectSearch')"
              class="flex-1 rounded px-3 py-1.5 text-xs card-input-dark"
            />
            <button class="text-xs px-3 py-1.5 transition-all btn-card-outline" @click="searchByProjectName">
              {{ $t('simLab.btnSearch') }}
            </button>
          </div>
        </div>
      </div>

      <div v-if="searchResults.length > 0" class="mt-4 rounded-lg p-3 card-panel-bordered">
        <h4 class="text-xs font-medium mb-2">{{ $t('simLab.searchResults') }}</h4>
        <div class="max-h-40 overflow-auto">
          <div
            v-for="item in searchResults"
            :key="item.id"
            class="flex justify-between items-center p-2 rounded cursor-pointer transition-all mb-1 card-panel"
            @click="selectSurvey(item)"
          >
            <div>
              <p class="text-xs text-accent">
                {{ item.project_name }}
              </p>
              <p class="text-[10px] text-muted">
                {{ item.country || item.city || item.location || '' }} | {{ item.total_mw }}MW / {{ item.total_mwh }}MWh
              </p>
            </div>
            <span class="text-[10px] px-2 py-1 rounded bg-accent">{{ $t('simLab.btnSelect') }}</span>
          </div>
        </div>
      </div>

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
        <div class="rounded p-3 card-panel-bordered">
          <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelCountry') }}</label>
          <input
            v-model="surveyData.country"
            type="text"
            class="w-full rounded px-2 py-1 text-xs card-input text-accent"
          />
        </div>
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
                <option v-for="n in [10, 15, 20, 25, 30]" :key="n" :value="n">
                  {{ $t('simLab.years', { n }) }}
                </option>
              </select>
            </div>
            <div>
              <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelGuaranteeYears') }}</label>
              <select v-model.number="simParams.guaranteeYears" class="w-full rounded px-2 py-1 text-xs card-input">
                <option v-for="n in [5, 10, 15, 20]" :key="n" :value="n">
                  {{ $t('simLab.years', { n }) }}
                </option>
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

          <!-- Manual 模式 -->
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

          <!-- Thermal 模式 -->
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

    <div v-show="currentStep === 2" class="rounded-lg p-4 card-panel">
      <h3 class="text-sm font-bold mb-3 flex items-center gap-2 text-accent">
        <span class="w-2 h-2 rounded-full bg-accent" />
        {{ $t('simLab.titleAlgorithm') }}
      </h3>

      <div class="grid grid-cols-3 gap-3">
        <div
          v-for="algo in algorithms"
          :key="algo.id"
          class="rounded-lg p-4 border-2 cursor-pointer transition-all flex flex-col"
          :class="selectedAlgorithm === algo.id ? 'algo-selected' : 'algo-default'"
          @click="selectAlgorithm(algo)"
        >
          <div class="flex items-center gap-2 mb-2">
            <span
              class="w-4 h-4 rounded-full"
              :class="selectedAlgorithm === algo.id ? 'algo-dot-selected' : 'algo-dot-default'"
            />
            <h4
              class="text-xs font-bold"
              :class="selectedAlgorithm === algo.id ? 'algo-name-selected' : 'algo-name-default'"
            >
              {{ algo.name }}
            </h4>
          </div>
          <p v-if="algo.name_en" class="text-[10px] mb-2 text-muted italic">
            {{ algo.name_en }}
          </p>
          <p class="text-[10px] mb-2 text-secondary flex-1">
            {{ algo.description }}
          </p>
          <div class="text-[10px] text-muted">
            <span class="inline-block rounded px-1.5 py-0.5 mr-1 theme-bg-card">
              {{ algo.type }}
            </span>
            <span class="text-secondary">{{ $t('simLab.accuracy') }}: {{ algo.accuracy }}</span>
          </div>
          <div class="mt-2 text-[10px] font-mono truncate text-accent">
            {{ algo.mathematical_form }}
          </div>
          <div
            v-if="algo.formula_expression"
            class="mt-1 text-[10px] font-mono truncate text-secondary opacity-75"
            :title="algo.formula_expression"
          >
            = {{ algo.formula_expression }}
          </div>
        </div>
      </div>

      <div v-if="algorithms.length === 0" class="text-center py-8 text-muted">
        <div>{{ $t('simLab.noAlgo') }}</div>
      </div>

      <div v-if="selectedAlgoDetail" class="mt-4 rounded p-3 card-panel-bordered">
        <div class="flex justify-between items-center mb-2">
          <h4 class="text-xs font-medium">{{ $t('simLab.algoParams', { name: selectedAlgoDetail.name }) }}</h4>
          <button
            class="text-[10px] rounded px-2 py-0.5 transition-colors theme-bg-card text-muted"
            @click="resetAlgoParams"
          >
            {{ $t('simLab.btnRestoreDefault') }}
          </button>
        </div>
        <div class="grid grid-cols-4 gap-3">
          <div v-for="(param, key) in selectedAlgoDetail.parameters" :key="key">
            <label class="text-[10px] block mb-1 text-muted">{{ param.label }} ({{ param.unit || '' }})</label>
            <input
              v-model.number="algoParams[key]"
              type="number"
              :step="param.step || 0.01"
              :min="param.min"
              :max="param.max"
              class="w-full rounded px-2 py-1 text-xs card-input"
            />
          </div>
        </div>
      </div>

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
            <select v-model="aiSimParams.manufacturerId" class="w-full rounded px-2 py-1 text-xs card-input">
              <option value="">{{ $t('simLab.manufacturerPlaceholder') }}</option>
              <option v-for="mfr in manufacturers" :key="mfr.id" :value="mfr.id">
                {{ mfr.name }} ({{ mfr.chemistry_type }})
              </option>
            </select>
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

    <div v-show="currentStep === 3" class="rounded-lg p-4 card-panel">
      <h3 class="text-sm font-bold mb-3 flex items-center gap-2 text-accent">
        <span class="w-2 h-2 rounded-full bg-accent" />
        {{ $t('simLab.titleCorrection') }}
      </h3>

      <div class="grid grid-cols-2 gap-4">
        <div class="rounded p-3 card-panel-bordered">
          <h4 class="text-xs mb-2 font-medium">{{ $t('simLab.sectionGlobalCorrection') }}</h4>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelSohFactor') }}</label>
              <input
                v-model.number="correctionFactors.sohFactor"
                type="number"
                step="0.01"
                min="0.9"
                max="1.1"
                class="w-full rounded px-2 py-1 text-xs card-input"
              />
              <p class="text-[10px] mt-1 text-muted">{{ $t('simLab.rangeDefault1') }}</p>
            </div>
            <div>
              <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelRteFactor') }}</label>
              <input
                v-model.number="correctionFactors.rteFactor"
                type="number"
                step="0.01"
                min="0.9"
                max="1.1"
                class="w-full rounded px-2 py-1 text-xs card-input"
              />
              <p class="text-[10px] mt-1 text-muted">{{ $t('simLab.rangeDefault1') }}</p>
            </div>
            <div>
              <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelCapacityFactor') }}</label>
              <input
                v-model.number="correctionFactors.capacityFactor"
                type="number"
                step="0.01"
                min="0.9"
                max="1.1"
                class="w-full rounded px-2 py-1 text-xs card-input"
              />
              <p class="text-[10px] mt-1 text-muted">{{ $t('simLab.rangeDefault1') }}</p>
            </div>
            <div>
              <label class="text-[10px] block mb-1 text-muted">{{ $t('simLab.labelAgingFactor') }}</label>
              <input
                v-model.number="correctionFactors.agingFactor"
                type="number"
                step="0.01"
                min="1.0"
                max="1.5"
                class="w-full rounded px-2 py-1 text-xs card-input"
              />
              <p class="text-[10px] mt-1 text-muted">{{ $t('simLab.rangeDefault1_5') }}</p>
            </div>
          </div>
        </div>

        <div class="rounded p-3 card-panel-bordered">
          <h4 class="text-xs mb-2 font-medium">{{ $t('simLab.annualCorrection') }}</h4>
          <div class="overflow-auto max-h-40">
            <table class="w-full text-[10px]">
              <thead>
                <tr class="text-muted">
                  <th class="py-1 px-2 text-left">{{ $t('simLab.colYear') }}</th>
                  <th class="py-1 px-2 text-left">{{ $t('simLab.colSohCorrection') }}</th>
                  <th class="py-1 px-2 text-left">{{ $t('simLab.colRteCorrection') }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, idx) in yearlyCorrections" :key="idx" class="border-t">
                  <td class="py-1 px-2 text-secondary">
                    {{ row.year }}
                  </td>
                  <td class="py-1 px-2">
                    <input
                      v-model.number="row.sohCorrection"
                      type="number"
                      step="0.001"
                      class="w-16 rounded px-1 py-0.5 text-xs card-input"
                    />
                  </td>
                  <td class="py-1 px-2">
                    <input
                      v-model.number="row.rteCorrection"
                      type="number"
                      step="0.001"
                      class="w-16 rounded px-1 py-0.5 text-xs card-input"
                    />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="mt-3 rounded p-2 card-panel-bordered">
        <p class="text-secondary">
          <strong>{{ $t('simLab.correctionNotes') }}</strong>
        </p>
        <ul class="list-disc list-inside mt-1 space-y-0.5 text-secondary">
          <li>{{ $t('simLab.correctionNoteFactorGt') }}</li>
          <li>{{ $t('simLab.correctionNoteFactorLt') }}</li>
          <li>{{ $t('simLab.correctionNoteAnnual') }}</li>
          <li>{{ $t('simLab.correctionNoteApplied') }}</li>
        </ul>
      </div>

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

    <div v-show="currentStep === 4" class="rounded-lg p-4 card-panel">
      <div class="flex justify-between items-center mb-3">
        <h3 class="text-sm font-bold flex items-center gap-2 text-accent">
          <span class="w-2 h-2 rounded-full bg-accent" />
          {{ $t('simLab.titleResults') }}
        </h3>
        <button
          class="text-xs px-3 py-1.5 rounded transition-all flex items-center gap-1 bg-info"
          @click="saveSimulationResult"
        >
          <span>💾</span>
          {{ $t('simLab.btnSaveResult') }}
        </button>
      </div>

      <div class="grid grid-cols-4 gap-3 mb-4">
        <div class="rounded p-3 text-center card-panel-bordered">
          <p class="text-[10px] text-muted">{{ $t('simLab.labelInitSoh') }}</p>
          <p class="text-lg font-bold text-accent">{{ simulationResults.initSoh?.toFixed(2) || '--' }}%</p>
        </div>
        <div class="rounded p-3 text-center card-panel-bordered">
          <p class="text-[10px] text-muted">{{ $t('simLab.labelGuaranteeEndSoh') }}</p>
          <p
            class="text-lg font-bold"
            :class="simulationResults.guaranteeEndSoh >= simParams.guaranteeSoh ? 'text-success' : 'text-danger'"
          >
            {{ simulationResults.guaranteeEndSoh?.toFixed(2) || '--' }}%
          </p>
        </div>
        <div class="rounded p-3 text-center card-panel-bordered">
          <p class="text-[10px] text-muted">{{ $t('simLab.labelFinalSoh') }}</p>
          <p class="text-lg font-bold text-accent-secondary">{{ simulationResults.finalSoh?.toFixed(2) || '--' }}%</p>
        </div>
        <div class="rounded p-3 text-center card-panel-bordered">
          <p class="text-[10px] text-muted">{{ $t('simLab.labelGuaranteeCheck') }}</p>
          <p class="text-lg font-bold" :class="simulationResults.meetsGuarantee ? 'text-success' : 'text-danger'">
            {{ simulationResults.meetsGuarantee ? $t('simLab.pass') : $t('simLab.fail') }}
          </p>
        </div>
      </div>

      <div class="rounded p-3 card-panel-bordered">
        <h4 class="text-xs mb-2 font-medium">{{ $t('simLab.titleSohCurve') }}</h4>
        <div ref="chartContainer" class="chart-container-sm" />
      </div>

      <div class="mt-3 rounded p-3 overflow-auto max-h-32 card-panel-bordered">
        <table class="w-full text-[10px]">
          <thead>
            <tr class="text-muted">
              <th class="py-1 px-2 text-left">{{ $t('simLab.colYear') }}</th>
              <th class="py-1 px-2 text-left">{{ $t('simLab.colSoh') }}</th>
              <th class="py-1 px-2 text-left">{{ $t('simLab.colRte') }}</th>
              <th class="py-1 px-2 text-left">{{ $t('simLab.colNetAvail') }}</th>
              <th class="py-1 px-2 text-left">{{ $t('simLab.colGuaranteeLine') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(row, idx) in simulationResults.tableData"
              :key="idx"
              :class="['border-t', { 'bg-danger-10': !row.meetsReq }]"
            >
              <td class="py-1 px-2 text-secondary">
                {{ row.year }}
              </td>
              <td class="py-1 px-2 text-accent">
                {{ row.soh.toFixed(2) }}
              </td>
              <td class="py-1 px-2 text-accent-secondary">
                {{ row.rte.toFixed(2) }}
              </td>
              <td class="py-1 px-2 text-success">
                {{ row.netAvail.toFixed(1) }}
              </td>
              <td class="py-1 px-2" :class="row.meetsReq ? 'sim-row-pass' : 'sim-row-fail'">
                {{ row.meetsReq ? $t('simLab.pass') : $t('simLab.fail') }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="mt-4 flex justify-between">
        <button class="text-xs px-4 py-2 rounded transition-all theme-btn-secondary" @click="resetSimulation">
          {{ $t('simLab.btnReSimulate') }}
        </button>
        <button class="text-xs px-4 py-2 rounded transition-all btn-accent-filled" @click="exportResults">
          {{ $t('simLab.btnExport') }}
        </button>
      </div>
    </div>

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
import { ref, reactive, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useBessStore, DEFAULT_DOD } from '../stores/bess.js'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, GridComponent, LegendComponent } from 'echarts/components'
import { useDraft, useDraftRef } from '../composables/useDraft'
import api from '../services/api.js'
import { useChartTheme } from '../composables/useChartTheme.js'
echarts.use([CanvasRenderer, LineChart, TitleComponent, TooltipComponent, GridComponent, LegendComponent])

const emit = defineEmits(['applyConfig', 'error'])
const { t } = useI18n()

const steps = [
  { label: 'simLab.stepSurvey' },
  { label: 'simLab.stepParams' },
  { label: 'simLab.stepAlgorithm' },
  { label: 'simLab.stepCorrection' },
  { label: 'simLab.stepResults' }
]

const currentStep = useDraftRef('sim-current-step', 0).state
const surveyId = useDraftRef('sim-survey-id', '').state
const surveyIdInput = ref('')
const surveyList = ref([])
const showDropdown = ref(false)
const searchKeyword = ref('')
const searchResults = ref([])

const store = useBessStore()
const { themeObject } = useChartTheme()

watch(themeObject, () => {
  nextTick(renderChart)
})
const selectedAlgorithm = useDraftRef('sim-selected-algorithm', '').state

const { state: surveyData, clearDraft: clearSurveyDataDraft } = useDraft('sim-survey-data', {
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

const { state: simParams, clearDraft: clearSimParamsDraft } = useDraft('sim-params', {
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

const algorithms = ref([])
const algoParams = reactive({})
const selectedAlgoDetail = ref(null)

const manufacturers = ref([])
const aiSimParams = reactive({
  manufacturerId: '',
  simulationYears: 25,
  temperature: 25,
  cyclesPerDay: 1,
  dod: DEFAULT_DOD,
  cRate: 0.5
})

const selectedManufacturer = computed(() => {
  return manufacturers.value.find((m) => m.id === aiSimParams.manufacturerId)
})

const { state: correctionFactors, clearDraft: clearCorrectionFactorsDraft } = useDraft('sim-correction-factors', {
  sohFactor: 1.0,
  rteFactor: 1.0,
  capacityFactor: 1.0,
  agingFactor: 1.0
})

const yearlyCorrections = useDraftRef('sim-yearly-corrections', []).state
const initYearlyCorrections = () => {
  yearlyCorrections.value = []
  for (let i = 0; i <= simParams.simulationYears; i++) {
    yearlyCorrections.value.push({
      year: i,
      sohCorrection: 0,
      rteCorrection: 0
    })
  }
}

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

// 冷却功耗估算（前端预览，用于 thermal 模式 UI 展示）
const FIXED_AUX = 3.0 // BMS/消防/照明固定功耗 kW
const COP_MAP = { 'forced-air': 2.0, liquid: 3.5, 'SiC-liquid': 5.0 }
const estimatedCoolingPower = computed(() => {
  if (simParams.auxPowerMode !== 'thermal') return null
  const ambient = simParams.ambientTemp || 25
  const cop = COP_MAP[simParams.coolingType] || COP_MAP.liquid
  // 电芯发热: I²R × N_cells, 默认值
  const cellAh = 280,
    cellR = 0.00025,
    cRate = 0.5,
    cells = 5000
  const cellHeatkW = ((cellAh * cRate) ** 2 * cellR * cells) / 1000
  // 热渗透: U × A × ΔT
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

const systemRTE = computed(() => {
  const ac = simParams.acEfficiency || 97
  const dc = simParams.dcEfficiency || 98.5
  return +((ac / 100) * (dc / 100) * 100).toFixed(2)
})

const annualEnergyThroughput = computed(() => {
  const energy = surveyData.ratedEnergy || 0
  const qty = surveyData.containerQty || 0
  const cycles = surveyData.cyclesPerDay || 1
  return +(energy * qty * cycles * 365).toFixed(1)
})

const totalRunAux = computed(() => {
  if (simParams.auxPowerMode === 'thermal') return estimatedCoolingPower.value?.totalRunkW || 0
  return (simParams.bessAuxRun || 0) + (simParams.pcsAuxRun || 0)
})
const totalStandbyAux = computed(() => {
  if (simParams.auxPowerMode === 'thermal') return estimatedCoolingPower.value?.standbykW || 0
  return (simParams.bessAuxStandby || 0) + (simParams.pcsAuxStandby || 0)
})

const grossEnergyPreview = computed(() => {
  const energy = surveyData.ratedEnergy || 0
  const qty = surveyData.containerQty || 0
  const dod = (surveyData.dod || 100) / 100
  const soh = 1.0 // assume new
  const rte = systemRTE.value / 100
  const acEff = (simParams.acEfficiency || 97) / 100
  return +(energy * qty * dod * rte * soh * acEff).toFixed(1)
})

const chartContainer = ref(null)
let chartInstance = null
let _resizeHandler = null

const toast = reactive({ show: false, message: '', type: 'success' })

// 过滤后的调研表列表（根据输入模糊匹配）
const filteredSurveyList = computed(() => {
  const q = surveyIdInput.value.trim().toLowerCase()
  if (!q) return surveyList.value.slice(0, 20)
  return surveyList.value
    .filter((s) => s.id.toLowerCase().includes(q) || (s.project_name || '').toLowerCase().includes(q))
    .slice(0, 20)
})

// 输入时显示下拉
function onSurveyIdInput() {
  surveyId.value = ''
  showDropdown.value = true
}

// 聚焦时显示下拉
function onSurveyInputFocus() {
  if (surveyList.value.length > 0) {
    showDropdown.value = true
  }
}

// 失焦时延迟关闭下拉
function onSurveyInputBlur() {
  setTimeout(() => {
    showDropdown.value = false
  }, 150)
}

// 回车：优先选第一个匹配项，否则按手动输入 ID 加载
function onSurveyInputEnter() {
  if (showDropdown.value && filteredSurveyList.value.length > 0) {
    selectSurveyFromDropdown(filteredSurveyList.value[0])
  } else if (surveyIdInput.value.trim()) {
    surveyId.value = surveyIdInput.value.trim()
    showDropdown.value = false
    loadSurveyData()
  }
}

// 从下拉选中调研表
function selectSurveyFromDropdown(survey) {
  surveyId.value = survey.id
  surveyIdInput.value = survey.project_name
  showDropdown.value = false
  mapSurveyData(survey)
}

// 页面加载时预读取调研表列表
async function fetchSurveyList() {
  try {
    const data = await api.get('/api/survey/list?per_page=200')
    // 后端 paginated_response 返回 data 为数组（不是 { items: [...] }）
    surveyList.value = Array.isArray(data.data) ? data.data : data.data?.items || []
  } catch (e) {
    console.error('[SimulationLab] 获取调研表列表失败:', e)
  }
}

onMounted(() => {
  fetchSurveyList()
})

const loadSurveyData = async () => {
  if (!surveyId.value) {
    emit('error', t('simLab.enterSurveyId'), 'warning')
    return
  }
  try {
    const data = await api.get(`/api/survey/${surveyId.value}`)
    mapSurveyData(data.data)
  } catch (e) {
    if (e.status === 404) {
      emit('error', t('simLab.surveyNotFound'), 'warning')
    } else {
      emit('error', t('simLab.networkErrorManual'), 'error')
    }
  }
}

const searchByProjectName = async () => {
  if (!searchKeyword.value.trim()) {
    emit('error', t('simLab.enterProjectKeyword'), 'warning')
    return
  }
  try {
    const data = await api.get(`/api/survey/search?keyword=${encodeURIComponent(searchKeyword.value)}`)
    if (data.success) {
      searchResults.value = data.data?.surveys || []
      if ((data.data?.surveys || []).length === 0) {
        emit('error', t('simLab.noMatchingProject'), 'warning')
      }
    } else {
      emit('error', data.error || t('simLab.searchFailed'), 'error')
    }
  } catch {
    emit('error', t('simLab.networkErrorSearch'), 'error')
  }
}

const selectSurvey = (survey) => {
  searchResults.value = []
  searchKeyword.value = survey.project_name
  surveyId.value = survey.id
  surveyIdInput.value = survey.project_name + ' (' + survey.id.slice(0, 8) + '...)'
  mapSurveyData(survey)
}

const mapSurveyData = (data) => {
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
  if (!surveyData.country && !surveyData.city && !surveyData.site && data.location) {
    surveyData.site = data.location
  }

  simParams.requiredEnergy = data.total_mwh || 240
  simParams.duration = data.duration || 2
  simParams.cyclesPerDay = data.cycles_per_day || 1
}

const nextStep = () => {
  if (currentStep.value < steps.length - 1) {
    currentStep.value++
  }
}

const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const fetchAlgorithms = async () => {
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

  if (algorithms.value.length === 0) {
    const { BUILTIN_DEGRADATION_ALGORITHMS, mapToSimulationLabFormat } = await import('../data/builtinAlgorithms.js')
    algorithms.value = BUILTIN_DEGRADATION_ALGORITHMS.map(mapToSimulationLabFormat)
  }

  if (!selectedAlgorithm.value && algorithms.value.length > 0) {
    selectedAlgorithm.value = algorithms.value[0].id
    selectAlgorithm(algorithms.value[0])
  }
}

const fetchManufacturers = async () => {
  try {
    const data = await api.get('/api/ai-sim/manufacturers')
    if (data.success && data.data.length > 0) {
      manufacturers.value = data.data
    }
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

const selectAlgorithm = (algo) => {
  selectedAlgorithm.value = algo.id
  selectedAlgoDetail.value = algo
  algoParams.value = {}
  if (algo.parameters) {
    Object.keys(algo.parameters).forEach((key) => {
      algoParams[key] = algo.parameters[key].default || 0
    })
  }
}

const resetAlgoParams = () => {
  const algo = selectedAlgoDetail.value
  if (!algo || !algo.parameters) return
  Object.keys(algo.parameters).forEach((key) => {
    algoParams[key] = algo.parameters[key].default || 0
  })
  showToast(t('simLab.paramsReset'))
}

watch(selectedAlgorithm, (newId) => {
  if (newId) {
    const algo = algorithms.value.find((a) => a.id === newId)
    if (algo) {
      selectAlgorithm(algo)
    }
  }
})

const calculateSOH = (modelType, params, t) => {
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
      const soc_factor = 0.98
      return Math.max(0.6, 1 - ((1 - temp_factor * dod_factor * c_rate_factor * soc_factor) * t) / 25)
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

const runSimulation = async () => {
  currentStep.value = 4

  const algo = algorithms.value.find((a) => a.id === selectedAlgorithm.value)

  if (algo?.model_type === 'ai_simulation') {
    await runAISimulation()
    return
  }

  const N = simParams.simulationYears + 1
  const sohCurve = []
  const rteCurve = []
  const netAvailCurve = []

  const modelType = algo?.model_type || 'arrhenius'

  for (let i = 0; i < N; i++) {
    const t = i
    let soh = calculateSOH(modelType, algoParams, t)

    soh = soh * correctionFactors.sohFactor
    if (yearlyCorrections.value[i]?.sohCorrection) {
      soh += yearlyCorrections.value[i].sohCorrection
    }

    let rte = simParams.initRte / 100 - 0.002 * i * correctionFactors.rteFactor
    if (yearlyCorrections.value[i]?.rteCorrection) {
      rte += yearlyCorrections.value[i].rteCorrection
    }

    const grossEnergy =
      surveyData.ratedEnergy *
      surveyData.containerQty *
      (surveyData.dod / 100) *
      rte *
      soh *
      (simParams.acEfficiency / 100)
    // 前端预览: thermal 模式使用动态 aux，manual 模式使用手动值
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

  simulationResults.sohCurve = sohCurve
  simulationResults.rteCurve = rteCurve
  simulationResults.netAvailCurve = netAvailCurve
  simulationResults.initSoh = sohCurve[0]
  simulationResults.guaranteeEndSoh = sohCurve[simParams.guaranteeYears]
  simulationResults.finalSoh = sohCurve[N - 1]
  simulationResults.meetsGuarantee = sohCurve[simParams.guaranteeYears] >= simParams.guaranteeSoh

  simulationResults.tableData = []
  for (let i = 0; i < N; i++) {
    simulationResults.tableData.push({
      year: i,
      soh: sohCurve[i],
      rte: rteCurve[i],
      netAvail: netAvailCurve[i],
      meetsReq: netAvailCurve[i] >= simParams.requiredEnergy
    })
  }

  nextTick(() => {
    setTimeout(() => {
      const container = chartContainer.value
      if (container) {
        container.style.height = '12rem'
        renderChart()
      }
    }, 300)
  })

  // 持久化前端仿真结果到 store（防止切换 tab 后数据丢失）
  store.degradation.soh = [...sohCurve]
  store.degradation.rte = [...rteCurve]
  store.results.totalAcUsable = [...netAvailCurve]
  store.results.meetsReq = simulationResults.tableData.map((d) => d.meetsReq)

  emit('applyConfig', {
    soh: simulationResults.sohCurve,
    rte: simulationResults.rteCurve,
    source: 'simulation',
    algorithmType: simParams.algorithmType,
    simulationYears: simParams.simulationYears,
    guaranteeSoh: simParams.guaranteeSoh,
    auxPowerMode: simParams.auxPowerMode,
    coolingType: simParams.coolingType,
    ambientTemp: simParams.ambientTemp
  })
}

const runAISimulation = async () => {
  try {
    const data = {
      manufacturer_id: aiSimParams.manufacturerId || null,
      simulation_years: aiSimParams.simulationYears,
      temperature: aiSimParams.temperature,
      cycles_per_day: aiSimParams.cyclesPerDay,
      dod: aiSimParams.dod / 100,
      c_rate: aiSimParams.cRate,
      rte_initial: simParams.initRte
    }

    const result = await api.post('/api/ai-sim/simulation', data)

    if (result.success && result.data) {
      const aiData = result.data
      simulationResults.sohCurve = aiData.soh_curve
      simulationResults.rteCurve = aiData.rte_curve
      simulationResults.initSoh = aiData.soh_curve[0]
      simulationResults.guaranteeEndSoh =
        aiData.soh_curve[Math.min(simParams.guaranteeYears, aiData.soh_curve.length - 1)]
      simulationResults.finalSoh = aiData.soh_curve[aiData.soh_curve.length - 1]
      simulationResults.meetsGuarantee = simulationResults.guaranteeEndSoh >= simParams.guaranteeSoh

      const N = aiData.soh_curve.length
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
          netAvail: netAvail,
          meetsReq: netAvail >= simParams.requiredEnergy
        })
      }

      nextTick(() => {
        setTimeout(() => {
          const container = chartContainer.value
          if (container) {
            container.style.height = '12rem'
            renderChart()
          }
        }, 300)
      })

      emit('applyConfig', {
        soh: simulationResults.sohCurve,
        rte: simulationResults.rteCurve,
        source: 'ai_simulation',
        algorithmType: 'ai_simulation',
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
    console.error('AI simulation failed:', e)
    showToast(t('simLab.aiSimFailedWithError', { message: e.message }), 'error')
  }
}

const runBackendSimulation = async () => {
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
      nextTick(() => setTimeout(() => renderChart(), 100))
      // 持久化仿真结果到 store，防止切换 tab 后数据丢失
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
        algorithmType: modelType,
        simulationYears: simParams.simulationYears,
        guaranteeSoh: simParams.guaranteeSoh
      })
    }
  } catch (e) {
    console.error('Backend simulation error:', e)
  }
}

const renderChart = () => {
  if (!chartContainer.value) return

  if (chartInstance) {
    chartInstance.dispose()
  }

  chartInstance = echarts.init(chartContainer.value, themeObject.value)

  const years = Array.from({ length: simulationResults.sohCurve.length }, (_, i) => i)
  const textColor = themeObject.value.legendText
  const accentColor = themeObject.value.primary
  const secondaryColor = themeObject.value.cyan
  const warningColor = themeObject.value.warning
  const axisColor = themeObject.value.axisLabel

  chartInstance.setOption({
    tooltip: { trigger: 'axis' },
    legend: {
      data: [t('simLab.chartSoh'), t('simLab.chartRte'), t('simLab.chartGuaranteeLine')],
      top: 0,
      textStyle: { color: textColor, fontSize: 10 }
    },
    grid: { left: 40, right: 20, top: 30, bottom: 20 },
    xAxis: { type: 'category', data: years, axisLabel: { color: axisColor, fontSize: 10 } },
    yAxis: { type: 'value', min: 50, max: 100, axisLabel: { color: axisColor, fontSize: 10 } },
    series: [
      {
        name: t('simLab.chartSoh'),
        type: 'line',
        data: simulationResults.sohCurve,
        smooth: true,
        lineStyle: { color: accentColor },
        itemStyle: { color: accentColor }
      },
      {
        name: t('simLab.chartRte'),
        type: 'line',
        data: simulationResults.rteCurve,
        smooth: true,
        lineStyle: { color: secondaryColor },
        itemStyle: { color: secondaryColor }
      },
      {
        name: t('simLab.chartGuaranteeLine'),
        type: 'line',
        data: Array.from({ length: years.length }, () => simParams.guaranteeSoh),
        lineStyle: { color: warningColor, type: 'dashed' },
        itemStyle: { color: warningColor }
      }
    ]
  })

  chartInstance.resize()
}

const handleResize = () => {
  if (chartInstance) {
    chartInstance.resize()
  }
}

const saveSimulationResult = async () => {
  const token = sessionStorage.getItem('auth_token')
  if (!token) {
    showToast(t('simLab.pleaseLogin'), 'error')
    return
  }

  const projectName = surveyData.projectName || t('simLab.unnamedProject')
  const timestamp = new Date().toISOString().slice(0, 19).replace(/[-T:]/g, '')
  const resultName = `${projectName}_${timestamp}`

  const algo = algorithms.value.find((a) => a.id === selectedAlgorithm.value)

  const data = {
    name: resultName,
    description: t('simLab.descriptionTemplate', { algo: algo?.name || t('simLab.unknown') }),
    simulation_type: algo?.category || 'comprehensive',
    algorithm_model_id: selectedAlgorithm.value,
    params: {
      surveyData: surveyData,
      simParams: simParams,
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
    if (respData.success) {
      showToast(t('simLab.saveSuccess'))
    } else {
      showToast(respData.error || t('simLab.saveFailed'), 'error')
    }
  } catch (e) {
    showToast(t('simLab.saveFailedWithError', { message: e.message }), 'error')
  }
}

const showToast = (message, type = 'success') => {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => {
    toast.show = false
  }, 3000)
}

const resetSimulation = () => {
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

const exportResults = () => {
  const N = simulationResults.tableData.length
  if (!N) return

  const eq = t('export.eqHeader')
  const sep = t('export.separator')
  const date = new Date().toISOString().slice(0, 10)
  const projectName = surveyData.projectName || store.survey.projectName || t('simLab.csvUnnamed')

  // 报告标题头
  const header = [
    eq,
    '  ' + t('export.reportTitle'),
    '  ' + t('export.projectName') + ': ' + projectName,
    '  ' + t('export.generatedDate') + ': ' + date,
    '  ' + t('export.version') + ': v1.0',
    eq,
    ''
  ]

  // 关键参数
  const params = [
    sep + ' ' + t('export.keyParams') + ' ' + sep,
    t('export.ratedEnergy') + ',' + (store.systemParams.ratedEnergy || store.survey.ratedEnergy || 'N/A'),
    t('export.totalPower') + ',' + (store.systemParams.pcsPower || store.survey.totalPower || 'N/A'),
    t('export.duration') + ',' + (store.systemParams.duration || store.survey.duration || 'N/A'),
    t('export.simYears') + ',' + N,
    ''
  ]

  // 竖排报表：年份为行，指标为列
  const csvRows = [
    [t('export.colYear'), t('export.colSoh'), t('export.colRte'), t('export.colAvail'), t('export.colGuarantee')].join(
      ','
    ),
    ...simulationResults.tableData.map((r) =>
      [
        r.year,
        r.soh.toFixed(2),
        r.rte.toFixed(2),
        r.netAvail.toFixed(1),
        r.meetsReq ? t('simLab.pass') : t('simLab.fail')
      ].join(',')
    )
  ]

  // 免责声明
  const footer = ['', sep, t('export.disclaimer')]

  const csvContent = [...header, ...params, ...csvRows, ...footer].join('\n')

  // 添加 UTF-8 BOM，解决 Excel 打开中文乱码
  const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const name = surveyData.projectName || t('simLab.csvUnnamed')
  link.href = URL.createObjectURL(blob)
  link.download = t('simLab.simExportFilename', { name, date })
  link.click()
}

onMounted(() => {
  // 从 store 同步设计数据到表单（仅在 useDraft 为默认值时覆盖）
  const designRatedEnergy = store.systemParams.ratedEnergy || store.survey.ratedEnergy
  if (designRatedEnergy && (surveyData.ratedEnergy === 5 || !surveyData.ratedEnergy)) {
    surveyData.ratedEnergy = designRatedEnergy
  }
  const designContainerQty = store.systemParams.initContainerQty
  if (designContainerQty && (surveyData.containerQty === 62 || !surveyData.containerQty)) {
    surveyData.containerQty = designContainerQty
  }
  const designReqEnergy = store.survey.requiredEnergy || store.systemParams.requiredEnergy
  if (designReqEnergy && (simParams.requiredEnergy === 240 || !simParams.requiredEnergy)) {
    simParams.requiredEnergy = designReqEnergy
  }
  // 补充同步缺失的字段：temperature, dod, cRate, duration, pcsQty
  const designTemp = store.survey.temperature
  if (designTemp && (surveyData.temperature === 25 || !surveyData.temperature)) {
    surveyData.temperature = designTemp
  }
  const designDod = store.survey.dod
  if (designDod && (surveyData.dod === 100 || !surveyData.dod)) {
    surveyData.dod = designDod
  }
  const designCRate = store.survey.cRate
  if (designCRate && (surveyData.cRate === 0.5 || !surveyData.cRate)) {
    surveyData.cRate = designCRate
  }
  const designDuration = store.survey.duration || store.systemParams.duration
  if (designDuration && (surveyData.duration === 2 || !surveyData.duration)) {
    surveyData.duration = designDuration
  }
  const designPcsQty = store.systemParams.initPcsQty
  if (designPcsQty && (surveyData.pcsQty === 2 || !surveyData.pcsQty)) {
    surveyData.pcsQty = designPcsQty
  }
  // 从 store 恢复之前的仿真结果（防止切换 tab 后图表数据丢失）
  if (store.results.totalAcUsable?.length) {
    // DataInjection/MatrixTable 存储 SOH 为 0-1 小数，统一转为百分比显示
    const rawSoh = [...store.degradation.soh]
    const needsPct = rawSoh.length > 0 && rawSoh[0] <= 1
    const sohPct = needsPct ? rawSoh.map((v) => v * 100) : rawSoh
    simulationResults.sohCurve = sohPct
    simulationResults.rteCurve = [...store.degradation.rte]
    simulationResults.netAvailCurve = [...store.results.totalAcUsable]
    simulationResults.initSoh = sohPct[0] || 100
    simulationResults.finalSoh = sohPct[sohPct.length - 1] || 0
    simulationResults.tableData = sohPct.map((s, i) => ({
      year: i,
      soh: s,
      rte: store.degradation.rte[i] || 0,
      netAvail: store.results.totalAcUsable[i] || 0,
      meetsReq: store.results.meetsReq?.[i] || false
    }))
    nextTick(() => setTimeout(() => renderChart(), 200))
  }
  initYearlyCorrections()
  fetchAlgorithms()
  fetchManufacturers()
  _resizeHandler = handleResize
  window.addEventListener('resize', _resizeHandler)
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  if (_resizeHandler) {
    window.removeEventListener('resize', _resizeHandler)
    _resizeHandler = null
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

/* Combobox 下拉面板 — 跟随页面浅色/深色主题 */
.combobox-wrapper {
  position: relative;
}
.combobox-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 100;
  max-height: 200px;
  overflow-y: auto;
  overflow-x: hidden;
  background: var(--color-card);
  backdrop-filter: var(--backdrop-filter, blur(12px));
  -webkit-backdrop-filter: var(--backdrop-filter, blur(12px));
  border: 1px solid var(--color-border);
  border-radius: 6px;
  margin-top: 2px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}
.combobox-option {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  cursor: pointer;
  transition: background 0.15s ease;
  border-bottom: 1px solid var(--color-border-light);
}
.combobox-option:last-child {
  border-bottom: none;
}
.combobox-option:hover,
.combobox-option.active {
  background: var(--color-accent);
  color: #fff;
}
.combobox-option:hover .option-name,
.combobox-option.active .option-name {
  color: #fff;
}
.combobox-option:hover .option-code,
.combobox-option.active .option-code {
  color: rgba(255, 255, 255, 0.7);
}
.option-name {
  flex: 1;
  font-size: 12px;
  font-weight: 500;
  color: var(--color-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-align: left;
}
.option-code {
  flex-shrink: 0;
  font-size: 10px;
  color: var(--color-text-muted);
  font-family: monospace;
}
.combobox-empty {
  padding: 8px 10px;
  font-size: 11px;
  color: var(--color-text-muted);
  text-align: center;
}
</style>
