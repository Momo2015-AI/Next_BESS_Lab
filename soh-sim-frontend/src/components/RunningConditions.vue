<template>
  <div class="h-full overflow-y-auto custom-scrollbar">
    <div class="max-w-5xl mx-auto space-y-4 py-2">
      <!-- 01: Basic Project Info -->
      <FormCardSection number="01" :title="$t('runningConditions.section01')" :z-index="2">
        <div class="grid grid-cols-4 gap-3">
          <div class="col-span-2">
            <label class="label-text">{{ $t('runningConditions.projectName') }}</label>
            <input
              v-model="form.projectName"
              class="form-field-input"
              :placeholder="$t('runningConditions.projectName')"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.projectType') }}</label>
            <select v-model="form.projectType" class="form-field-select">
              <option value="">
                {{ $t('common.select') }}
              </option>
              <option value="utility">
                {{ $t('runningConditions.projectTypes.utility') }}
              </option>
              <option value="cni">
                {{ $t('runningConditions.projectTypes.ci') }}
              </option>
              <option value="residential">
                {{ $t('runningConditions.projectTypes.residential') }}
              </option>
              <option value="microgrid">
                {{ $t('runningConditions.projectTypes.microgrid') }}
              </option>
              <option value="solar-plus-bess">
                {{ $t('runningConditions.projectTypes.solar') }}
              </option>
              <option value="wind-plus-bess">
                {{ $t('runningConditions.projectTypes.wind') }}
              </option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.country') }}</label>
            <ComboboxInput
              v-model="countryInput"
              :options="countryOptions"
              :placeholder="$t('runningConditions.country')"
              @select="onCountrySelect"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.city') }}</label>
            <input v-model="form.city" class="form-field-input" :placeholder="$t('runningConditions.city')" />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.site') }}</label>
            <input v-model="form.site" class="form-field-input" :placeholder="$t('runningConditions.site')" />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.ratedPower') }}</label>
            <input v-model.number="form.totalMW" type="number" class="form-field-input" placeholder="200" />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.ratedEnergy') }}</label>
            <input v-model.number="form.totalMWh" type="number" class="form-field-input" placeholder="800" />
          </div>
          <div>
            <label class="label-text">
              {{ $t('runningConditions.chargeDuration') }}
              <span v-if="isDurationAuto" class="auto-badge">AUTO</span>
            </label>
            <div class="duration-input-row">
              <input
                v-model.number="form.durationHours"
                type="number"
                class="form-field-input"
                :disabled="isDurationAuto"
                placeholder="4"
              />
              <button
                type="button"
                class="lock-toggle-btn"
                :title="isDurationAuto ? 'Unlock' : 'Lock'"
                @click="isDurationAuto = !isDurationAuto"
              >
                {{ isDurationAuto ? '🔒' : '🔓' }}
              </button>
            </div>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.dayCycles') }}</label>
            <input v-model.number="form.cyclesPerDay" type="number" class="form-field-input" placeholder="1" />
          </div>
        </div>
      </FormCardSection>

      <!-- 02: Environmental Conditions -->
      <FormCardSection number="02" :title="$t('runningConditions.section02')">
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="label-text">{{ $t('runningConditions.altitude') }}</label>
            <input v-model.number="form.altitude" type="number" class="form-field-input" placeholder="≤2000" />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.maxTemp') }}</label>
            <input v-model.number="form.tempMax" type="number" class="form-field-input" placeholder="45" />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.minTemp') }}</label>
            <input v-model.number="form.tempMin" type="number" class="form-field-input" placeholder="-20" />
          </div>
          <div>
            <label class="label-text">
              {{ $t('runningConditions.avgTemp') }}
              <span v-if="isTempAvgAuto" class="auto-badge">AUTO</span>
            </label>
            <div class="duration-input-row">
              <input
                v-model.number="form.tempAvg"
                type="number"
                class="form-field-input"
                :disabled="isTempAvgAuto"
                placeholder="25"
              />
              <button
                type="button"
                class="lock-toggle-btn"
                :title="isTempAvgAuto ? 'Unlock' : 'Lock'"
                @click="isTempAvgAuto = !isTempAvgAuto"
              >
                {{ isTempAvgAuto ? '🔒' : '🔓' }}
              </button>
            </div>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.humidity') }}</label>
            <input v-model.number="form.humidity" type="number" class="form-field-input" placeholder="≤95" />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.seismicZone') }}</label>
            <select v-model="form.seismicZone" class="form-field-select">
              <option value="">
                {{ $t('common.select') }}
              </option>
              <option value="zone1">
                {{ $t('runningConditions.seismicZones.low') }}
              </option>
              <option value="zone2">
                {{ $t('runningConditions.seismicZones.mid') }}
              </option>
              <option value="zone3">
                {{ $t('runningConditions.seismicZones.mid') }}
              </option>
              <option value="zone4">
                {{ $t('runningConditions.seismicZones.high') }}
              </option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.corrosionLevel') }}</label>
            <select v-model="form.corrosionClass" class="form-field-select">
              <option value="">
                {{ $t('common.select') }}
              </option>
              <option value="c1">
                {{ $t('runningConditions.corrosionLevels.c1') }}
              </option>
              <option value="c2">
                {{ $t('runningConditions.corrosionLevels.c2') }}
              </option>
              <option value="c3">
                {{ $t('runningConditions.corrosionLevels.c3') }}
              </option>
              <option value="c4">
                {{ $t('runningConditions.corrosionLevels.c4') }}
              </option>
              <option value="c5">
                {{ $t('runningConditions.corrosionLevels.c5') }}
              </option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.installType') }}</label>
            <select v-model="form.installationType" class="form-field-select">
              <option value="">
                {{ $t('common.select') }}
              </option>
              <option value="outdoor">
                {{ $t('runningConditions.installTypes.outdoor') }}
              </option>
              <option value="indoor">
                {{ $t('runningConditions.installTypes.indoor') }}
              </option>
              <option value="semi-outdoor">
                {{ $t('runningConditions.installTypes.semi') }}
              </option>
            </select>
          </div>
        </div>
      </FormCardSection>

      <!-- 03: Grid Parameters -->
      <FormCardSection number="03" :title="$t('runningConditions.section03')">
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="label-text">{{ $t('runningConditions.gridVoltage') }}</label>
            <select v-model="form.gridVoltage" class="form-field-select">
              <option value="">
                {{ $t('common.select') }}
              </option>
              <option value="10kV">10 kV</option>
              <option value="35kV">35 kV</option>
              <option value="110kV">110 kV</option>
              <option value="220kV">220 kV</option>
              <option value="330kV">330 kV</option>
              <option value="500kV">500 kV</option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.gridFreq') }}</label>
            <select v-model="form.gridFreq" class="form-field-select">
              <option value="">
                {{ $t('common.select') }}
              </option>
              <option value="50Hz">50 Hz</option>
              <option value="60Hz">60 Hz</option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.shortCircuit') }}</label>
            <input v-model.number="form.scCapacity" type="number" class="form-field-input" placeholder="5000" />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.neutralGround') }}</label>
            <select v-model="form.neutralGrounding" class="form-field-select">
              <option value="">
                {{ $t('common.select') }}
              </option>
              <option value="solid">
                {{ $t('runningConditions.neutralGrounds.solid') }}
              </option>
              <option value="resistance">
                {{ $t('runningConditions.neutralGrounds.resistance') }}
              </option>
              <option value="arc-suppression">
                {{ $t('runningConditions.neutralGrounds.arcSuppression') }}
              </option>
              <option value="ungrounded">
                {{ $t('runningConditions.neutralGrounds.ungrounded') }}
              </option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.dcVoltage') }}</label>
            <input v-model="form.dcVoltageRange" class="form-field-input" placeholder="1000-1500" />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.acVoltage') }}</label>
            <input v-model="form.acVoltage" class="form-field-input" placeholder="690" />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.pfRange') }}</label>
            <input v-model="form.pfRange" class="form-field-input" placeholder="0.99leading-0.99lagging" />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.thdiReq') }}</label>
            <input v-model.number="form.thdiLimit" type="number" class="form-field-input" placeholder="5" />
          </div>
        </div>
      </FormCardSection>

      <!-- 04: Performance Requirements -->
      <FormCardSection number="04" :title="$t('runningConditions.section04')">
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="label-text">{{ $t('runningConditions.rteTarget') }}</label>
            <input
              v-model.number="form.rteTarget"
              type="number"
              step="0.01"
              class="form-field-input"
              placeholder="85"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.acAvailability') }}</label>
            <input
              v-model.number="form.availabilityTarget"
              type="number"
              step="0.01"
              class="form-field-input"
              placeholder="99"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.sohYear1') }}</label>
            <input
              v-model.number="form.sohYear1"
              type="number"
              step="0.01"
              class="form-field-input"
              placeholder="93.2"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.sohYear25') }}</label>
            <input
              v-model.number="form.sohYear25"
              type="number"
              step="0.01"
              class="form-field-input"
              placeholder="60"
            />
            <div v-if="annualSohDecline !== null" class="text-xs text-muted mt-1">~{{ annualSohDecline }}% / year</div>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.calendarLife') }}</label>
            <input v-model.number="form.calendarLife" type="number" class="form-field-input" placeholder="25" />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.cycleLife') }}</label>
            <input v-model.number="form.cycleLife" type="number" class="form-field-input" placeholder="6000" />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.auxConsumption') }}</label>
            <input
              v-model.number="form.auxConsumption"
              type="number"
              step="0.01"
              class="form-field-input"
              placeholder="5"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.responseTime') }}</label>
            <input v-model.number="form.responseTime" type="number" class="form-field-input" placeholder="50" />
          </div>
        </div>
      </FormCardSection>

      <!-- 05: Cell / BMS Specifications -->
      <FormCardSection number="05" :title="$t('runningConditions.section05')">
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="label-text">{{ $t('runningConditions.cellChemistry') }}</label>
            <select v-model="form.cellChemistry" class="form-field-select">
              <option value="">
                {{ $t('common.select') }}
              </option>
              <option value="LFP">
                {{ $t('runningConditions.chemistries.lfp') }}
              </option>
              <option value="NMC">
                {{ $t('runningConditions.chemistries.nmc') }}
              </option>
              <option value="LTO">
                {{ $t('runningConditions.chemistries.lto') }}
              </option>
              <option value="sodium-ion">
                {{ $t('runningConditions.chemistries.naion') }}
              </option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.cellCapacity') }}</label>
            <input v-model="form.cellCapacityRange" class="form-field-input" placeholder="280-700" />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.cellCycleLife') }}</label>
            <input v-model.number="form.cellCycleLife" type="number" class="form-field-input" placeholder="6000" />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.eolCriteria') }}</label>
            <input
              v-model.number="form.eolThreshold"
              type="number"
              step="0.1"
              class="form-field-input"
              placeholder="70"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.cellTempRange') }}</label>
            <input v-model="form.cellTempRange" class="form-field-input" placeholder="-20 ~ +55" />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.cellVoltageDiff') }}</label>
            <input v-model.number="form.cellVoltageDiff" type="number" class="form-field-input" placeholder="20" />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.cellTempDiff') }}</label>
            <input
              v-model.number="form.cellTempDiff"
              type="number"
              step="0.5"
              class="form-field-input"
              placeholder="3"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.thermalRunaway') }}</label>
            <select v-model="form.thermalRunawayPrev" class="form-field-select">
              <option value="">
                {{ $t('common.select') }}
              </option>
              <option value="pack-level">
                {{ $t('runningConditions.thermalRunaways.pack') }}
              </option>
              <option value="cluster-level">
                {{ $t('runningConditions.thermalRunaways.cluster') }}
              </option>
              <option value="rack-level">
                {{ $t('runningConditions.thermalRunaways.rack') }}
              </option>
            </select>
          </div>
        </div>
      </FormCardSection>

      <!-- 06: Product Auto-Matching -->
      <RunningAutoMatch ref="autoMatchRef" />

      <!-- 07: PCS Parameters -->
      <FormCardSection number="07" :title="$t('runningConditions.pcsSectionTitle')">
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="label-text">{{ $t('runningConditions.pcsRatedPower') }}</label>
            <input
              v-model.number="form.pcsRatedPower"
              type="number"
              step="0.001"
              class="form-field-input"
              placeholder="2.5"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.pcsEfficiency') }}</label>
            <input
              v-model.number="form.pcsEfficiency"
              type="number"
              step="0.01"
              class="form-field-input"
              placeholder="98.5"
            />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.overload') }}</label>
            <select v-model="form.pcsOverload" class="form-field-select">
              <option value="">
                {{ $t('common.select') }}
              </option>
              <option value="standard">
                {{ $t('runningConditions.overloads.standard') }}
              </option>
              <option value="enhanced">
                {{ $t('runningConditions.overloads.advanced') }}
              </option>
              <option value="high">
                {{ $t('runningConditions.overloads.premium') }}
              </option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.thdiReq') }}</label>
            <input v-model.number="form.pcsTHDi" type="number" step="0.1" class="form-field-input" placeholder="3" />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.pfRange') }}</label>
            <input v-model="form.pcsPF" class="form-field-input" placeholder="-0.9 ~ +0.9" />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.responseTime') }}</label>
            <input v-model.number="form.pcsResponseTime" type="number" class="form-field-input" placeholder="50" />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.gridSupport') }}</label>
            <select v-model="form.pcsGridSupport" class="form-field-select">
              <option value="">
                {{ $t('common.select') }}
              </option>
              <option value="basic">
                {{ $t('runningConditions.gridSupports.basic') }}
              </option>
              <option value="advanced">
                {{ $t('runningConditions.gridSupports.advanced') }}
              </option>
              <option value="full">
                {{ $t('runningConditions.gridSupports.full') }}
              </option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.coolingType') }}</label>
            <select v-model="form.pcsCooling" class="form-field-select">
              <option value="">
                {{ $t('common.select') }}
              </option>
              <option value="forced-air">
                {{ $t('runningConditions.coolingTypes.forcedAir') }}
              </option>
              <option value="liquid">
                {{ $t('runningConditions.coolingTypes.liquid') }}
              </option>
              <option value="SiC-liquid">
                {{ $t('runningConditions.coolingTypes.fullSiC') }}
              </option>
            </select>
          </div>
        </div>
      </FormCardSection>

      <!-- 08: Certifications -->
      <RunningCertifications
        v-model:cert-cell="form.certCell"
        v-model:cert-system="form.certSystem"
        v-model:cert-grid="form.certGrid"
        v-model:cert-extra="form.certExtra"
        v-model:cert-grid-code="form.certGridCode"
      />

      <!-- 09: EPC / Commercial -->
      <FormCardSection number="09" :title="$t('runningConditions.section08')">
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="label-text">{{ $t('runningConditions.epcModel') }}</label>
            <select v-model="form.epcModel" class="form-field-select">
              <option value="">
                {{ $t('common.select') }}
              </option>
              <option value="turnkey">
                {{ $t('runningConditions.epcModels.turnkey') }}
              </option>
              <option value="supply-only">
                {{ $t('runningConditions.epcModels.supplyOnly') }}
              </option>
              <option value="supply-supervision">
                {{ $t('runningConditions.epcModels.supplySupervision') }}
              </option>
              <option value="epcm">
                {{ $t('runningConditions.epcModels.epcm') }}
              </option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.omYears') }}</label>
            <input v-model.number="form.omYears" type="number" class="form-field-input" placeholder="5" />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.performanceGuarantee') }}</label>
            <select v-model="form.prRequirement" class="form-field-select">
              <option value="">
                {{ $t('common.select') }}
              </option>
              <option value="availability-guarantee">
                {{ $t('runningConditions.pgs.availability') }}
              </option>
              <option value="rte-guarantee">
                {{ $t('runningConditions.pgs.rte') }}
              </option>
              <option value="soh-guarantee">
                {{ $t('runningConditions.pgs.soh') }}
              </option>
              <option value="full-guarantee">
                {{ $t('runningConditions.pgs.full') }}
              </option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.warrantyYears') }}</label>
            <input v-model.number="form.warrantyYears" type="number" class="form-field-input" placeholder="5" />
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.scada') }}</label>
            <select v-model="form.scadaReq" class="form-field-select">
              <option value="">
                {{ $t('common.select') }}
              </option>
              <option value="none">
                {{ $t('runningConditions.scadaOptions.none') }}
              </option>
              <option value="basic">
                {{ $t('runningConditions.scadaOptions.basic') }}
              </option>
              <option value="advanced">
                {{ $t('runningConditions.scadaOptions.advanced') }}
              </option>
              <option value="full">
                {{ $t('runningConditions.scadaOptions.full') }}
              </option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.spareParts') }}</label>
            <select v-model="form.sparePartsStrategy" class="form-field-select">
              <option value="">
                {{ $t('common.select') }}
              </option>
              <option value="none">
                {{ $t('runningConditions.sparePartsOptions.none') }}
              </option>
              <option value="standard">
                {{ $t('runningConditions.sparePartsOptions.standard') }}
              </option>
              <option value="enhanced">
                {{ $t('runningConditions.sparePartsOptions.enhanced') }}
              </option>
              <option value="full">
                {{ $t('runningConditions.sparePartsOptions.full') }}
              </option>
            </select>
          </div>
        </div>
      </FormCardSection>

      <!-- 10: File Upload -->
      <RunningFileUpload ref="uploadRef" v-model:form="form" />

      <!-- Bottom Actions -->
      <div class="text-right pb-4">
        <button class="text-xs underline mr-4 ins-9" @click="clearAll">
          {{ $t('runningConditions.resetAll') }}
        </button>
        <button class="text-xs px-4 py-1.5 rounded mr-2 transition-colors ins-10" @click="exportCSV">
          {{ $t('runningConditions.exportCSV') }}
        </button>
        <button class="btn-primary" @click="applyToSimulation">
          {{ $t('runningConditions.applyEngine') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useBessStore } from '../stores/bess.js'
import { useProducts } from '../composables/useProducts'
import { useDraft } from '../composables/useDraft'
import { useCountryList } from '../composables/useCountryList'
import ComboboxInput from './ComboboxInput.vue'
import FormCardSection from './FormCardSection.vue'
import RunningAutoMatch from './RunningAutoMatch.vue'
import RunningCertifications from './RunningCertifications.vue'
import RunningFileUpload from './RunningFileUpload.vue'

const { t } = useI18n()
const store = useBessStore()
const emit = defineEmits(['applyParams'])

const { filterCountries } = useCountryList()
const { loadAll } = useProducts()

const autoMatchRef = ref(null)
const uploadRef = ref(null)

const { state: form } = useDraft('rc-form', {
  projectName: '',
  projectType: '',
  country: '',
  city: '',
  site: '',
  totalMW: null,
  totalMWh: null,
  durationHours: null,
  cyclesPerDay: 1,
  altitude: null,
  tempMax: null,
  tempMin: null,
  tempAvg: null,
  humidity: null,
  seismicZone: '',
  corrosionClass: '',
  installationType: '',
  gridVoltage: '',
  gridFreq: '',
  scCapacity: null,
  neutralGrounding: '',
  dcVoltageRange: '',
  acVoltage: '',
  pfRange: '',
  thdiLimit: null,
  rteTarget: null,
  availabilityTarget: null,
  sohYear1: null,
  sohYear25: null,
  calendarLife: null,
  cycleLife: null,
  auxConsumption: null,
  responseTime: null,
  cellChemistry: '',
  cellCapacityRange: '',
  cellCycleLife: null,
  eolThreshold: 70,
  cellTempRange: '',
  cellVoltageDiff: null,
  cellTempDiff: null,
  thermalRunawayPrev: '',
  pcsRatedPower: null,
  pcsEfficiency: null,
  pcsOverload: '',
  pcsTHDi: null,
  pcsPF: '',
  pcsResponseTime: null,
  pcsGridSupport: '',
  pcsCooling: '',
  certCell: [],
  certSystem: [],
  certGrid: [],
  certExtra: [],
  certGridCode: [],
  epcModel: '',
  omYears: null,
  prRequirement: '',
  warrantyYears: null,
  scadaReq: '',
  sparePartsStrategy: ''
})

// --- Country combobox via ComboboxInput ---
const countryInput = ref(form.country || '')
const countryOptions = computed(() => {
  return filterCountries(countryInput.value).map((c) => ({ label: c, value: c }))
})

function onCountrySelect(opt) {
  form.country = opt.label
}

watch(
  () => form.country,
  (val) => {
    if (val && val !== countryInput.value) countryInput.value = val
  }
)

// --- auto-calc: durationHours ---
const isDurationAuto = ref(true)

function autoCalcDuration() {
  if (form.totalMWh > 0 && form.totalMW > 0 && typeof form.totalMWh === 'number' && typeof form.totalMW === 'number') {
    form.durationHours = +(form.totalMWh / form.totalMW).toFixed(2)
  }
}

watch(
  () => [form.totalMWh, form.totalMW],
  () => {
    if (isDurationAuto.value) autoCalcDuration()
  }
)

// --- auto-calc: tempAvg ---
const isTempAvgAuto = ref(true)

function autoCalcTempAvg() {
  if (
    form.tempMax != null &&
    form.tempMin != null &&
    typeof form.tempMax === 'number' &&
    typeof form.tempMin === 'number'
  ) {
    form.tempAvg = +((form.tempMax + form.tempMin) / 2).toFixed(1)
  }
}

watch(
  () => [form.tempMax, form.tempMin],
  () => {
    if (isTempAvgAuto.value) autoCalcTempAvg()
  }
)

// --- computed: annualSohDecline ---
const annualSohDecline = computed(() => {
  if (
    form.sohYear1 != null &&
    form.sohYear25 != null &&
    typeof form.sohYear1 === 'number' &&
    typeof form.sohYear25 === 'number'
  ) {
    return +((form.sohYear1 - form.sohYear25) / 24).toFixed(2)
  }
  return null
})

// --- CSV Export ---
function exportCSV() {
  const eq = t('export.eqHeader')
  const sep = t('export.separator')
  const date = new Date().toISOString().slice(0, 10)
  const projectName = form.projectName || store.survey.projectName || 'Untitled'

  const categories = {
    general: [
      'projectName',
      'projectType',
      'country',
      'city',
      'site',
      'totalMW',
      'totalMWh',
      'durationHours',
      'cyclesPerDay',
      'installationType',
      'omYears',
      'prRequirement',
      'warrantyYears',
      'scadaReq',
      'sparePartsStrategy'
    ],
    battery: [
      'rteTarget',
      'availabilityTarget',
      'sohYear1',
      'sohYear25',
      'calendarLife',
      'cycleLife',
      'auxConsumption'
    ],
    pcs: ['dcVoltageRange', 'acVoltage', 'pfRange', 'thdiLimit'],
    env: ['altitude', 'tempMax', 'tempMin', 'tempAvg', 'humidity', 'seismicZone', 'corrosionClass'],
    grid: ['gridVoltage', 'gridFreq', 'scCapacity', 'neutralGrounding']
  }

  const catLabels = {
    general: t('export.catGeneral'),
    battery: t('export.catBattery'),
    pcs: t('export.catPCS'),
    env: t('export.catEnv'),
    grid: t('export.catGrid')
  }

  const rows = []
  rows.push([eq])
  rows.push(['  ' + t('export.conditionsTitle')])
  rows.push(['  ' + t('export.projectName') + ': ' + projectName])
  rows.push(['  ' + t('export.generatedDate') + ': ' + date])
  rows.push([eq])
  rows.push([])

  for (const [cat, keys] of Object.entries(categories)) {
    rows.push([sep + ' ' + catLabels[cat] + ' ' + sep])
    rows.push(['Key', 'Value'])
    for (const k of keys) {
      rows.push([k, form[k] ?? ''])
    }
    rows.push([])
  }

  rows.push([sep])
  rows.push([t('export.disclaimer')])

  const csv = '\uFEFF' + rows.map((r) => r.map((c) => `"${String(c).replace(/"/g, '""')}"`).join(',')).join('\n')
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `BESS_Conditions_${projectName}_${date}.csv`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

function clearAll() {
  for (const k of Object.keys(form)) {
    if (Array.isArray(form[k])) form[k] = []
    else form[k] = typeof form[k] === 'number' || form[k] === null ? null : ''
  }
  autoMatchRef.value?.reset()
  uploadRef.value?.reset()
}

onMounted(() => {
  loadAll()
})

function applyToSimulation() {
  const mapped = {
    duration: form.durationHours,
    cyclesPerDay: form.cyclesPerDay,
    requiredEnergy: form.totalMWh,
    altitude: form.altitude,
    tempMax: form.tempMax,
    tempMin: form.tempMin,
    tempAvg: form.tempAvg,
    humidity: form.humidity,
    gridVoltage: form.gridVoltage,
    rteTarget: form.rteTarget,
    availabilityTarget: form.availabilityTarget,
    projectName: form.projectName,
    projectType: form.projectType,
    country: form.country,
    city: form.city,
    site: form.site,
    location: [form.country, form.city, form.site].filter(Boolean).join(', ')
  }
  emit('applyParams', mapped)
}
</script>

<style scoped>
/* auto-calc styles */
.auto-badge {
  display: inline-block;
  font-size: 0.65rem;
  font-weight: 600;
  padding: 1px 6px;
  border-radius: 3px;
  background: #e8f5e9;
  color: #2e7d32;
  margin-left: 6px;
  vertical-align: middle;
}

.duration-input-row {
  display: flex;
  align-items: center;
  gap: 4px;
}

.duration-input-row .form-field-input {
  flex: 1;
}

.duration-input-row .form-field-input:disabled {
  background: var(--color-bg, #f5f5f5);
  color: var(--text-secondary, #888);
  cursor: not-allowed;
}

.lock-toggle-btn {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  border: 1px solid var(--color-border, #ddd);
  border-radius: 4px;
  background: var(--color-card, #fff);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  padding: 0;
}

.lock-toggle-btn:hover {
  background: var(--color-accent-glow, rgba(37, 99, 235, 0.08));
}

.text-muted {
  color: var(--color-text-muted, #999);
}

.ins-9 {
  color: var(--color-text-muted);
}
.ins-10 {
  background: var(--color-input-bg);
  border: 1px solid var(--color-input-border);
  color: var(--color-text-secondary);
}
</style>
