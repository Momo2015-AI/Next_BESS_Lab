<template>
  <div class="h-full overflow-y-auto custom-scrollbar">
    <div class="max-w-5xl mx-auto space-y-4 py-2">
      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold ins-1">01</span>
          <div>
            <h3 class="section-title ins-2">
              {{ $t('runningConditions.section01') }}
            </h3>
          </div>
        </div>
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
            <div class="combobox-wrapper">
              <input
                v-model="countryInput"
                type="text"
                class="form-field-input"
                :placeholder="$t('runningConditions.country')"
                @focus="countryDropdown = true"
                @blur="onCountryBlur"
                @input="onCountryInput"
              />
              <div v-if="countryDropdown && filteredCountries.length > 0" class="combobox-dropdown">
                <div
                  v-for="c in filteredCountries"
                  :key="c"
                  class="combobox-option"
                  :class="{ active: c === form.country }"
                  @mousedown.prevent="selectCountry(c)"
                >
                  <span class="option-name">{{ c }}</span>
                </div>
              </div>
            </div>
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
      </div>

      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold ins-1">02</span>
          <div>
            <h3 class="section-title ins-2">
              {{ $t('runningConditions.section02') }}
            </h3>
          </div>
        </div>
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
      </div>

      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold ins-1">03</span>
          <div>
            <h3 class="section-title ins-2">
              {{ $t('runningConditions.section03') }}
            </h3>
          </div>
        </div>
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
      </div>

      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold ins-1">04</span>
          <div>
            <h3 class="section-title ins-2">
              {{ $t('runningConditions.section04') }}
            </h3>
          </div>
        </div>
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
      </div>

      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold ins-1">05</span>
          <div>
            <h3 class="section-title ins-2">
              {{ $t('runningConditions.section05') }}
            </h3>
          </div>
        </div>
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
      </div>

      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold ins-1">06</span>
          <div>
            <h3 class="section-title ins-2">
              {{ $t('runningConditions.section06') }}
            </h3>
          </div>
          <div class="ml-auto">
            <label class="flex items-center gap-2 text-xs cursor-pointer ins-3">
              <input v-model="autoMatchEnabled" type="checkbox" class="accent-teal-500" />
              {{ $t('runningConditions.autoMatch') }}
            </label>
          </div>
        </div>
        <div class="grid grid-cols-5 gap-3">
          <div>
            <label class="label-text">{{ $t('runningConditions.cellModel') }}</label>
            <select v-model="selectedCellModel" class="form-field-select" @change="onCellChange">
              <option value="">
                {{ $t('common.select') }}
              </option>
              <option v-for="cell in cells" :key="cell.id" :value="cell.model">
                {{ cell.mfr }} - {{ cell.model }} ({{ cell.capacityAh }}Ah)
              </option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.packModel') }}</label>
            <select v-model="selectedPackModel" class="form-field-select" @change="onPackChange">
              <option value="">
                {{ $t('common.select') }}
              </option>
              <option v-for="pack in availablePacks" :key="pack.id" :value="pack.model">
                {{ pack.model }} ({{ pack.ratedEnergyMWh }}MWh)
              </option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.rackModel') }}</label>
            <select v-model="selectedRackModel" class="form-field-select" @change="onRackChange">
              <option value="">
                {{ $t('common.select') }}
              </option>
              <option v-for="rack in availableRacks" :key="rack.id" :value="rack.model">
                {{ rack.model }} ({{ rack.ratedEnergyMWh }}MWh)
              </option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.clusterModel') }}</label>
            <select v-model="selectedClusterModel" class="form-field-select" @change="onClusterChange">
              <option value="">
                {{ $t('common.select') }}
              </option>
              <option v-for="cluster in availableClusters" :key="cluster.id" :value="cluster.model">
                {{ cluster.model }} ({{ cluster.ratedEnergyMWh }}MWh)
              </option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.containerModel') }}</label>
            <select v-model="selectedContainerModel" class="form-field-select">
              <option value="">
                {{ $t('common.select') }}
              </option>
              <option v-for="container in availableContainers" :key="container.id" :value="container.model">
                {{ container.model }} ({{ container.ratedEnergyMWh }}MWh)
              </option>
            </select>
          </div>
        </div>
        <div v-if="matchedConfig" class="mt-3 p-3 rounded ins-4">
          <div class="text-xs font-bold mb-1 ins-5">
            {{ $t('runningConditions.matchedConfig') }}: {{ matchedConfig.name }}
          </div>
          <div class="text-[10px] space-y-0.5 ins-3">
            <div>{{ $t('runningConditions.packEnergy') }}: {{ matchedConfig.packNominalEnergykWh }} kWh</div>
            <div>
              {{ $t('runningConditions.rackEnergy') }}: {{ (matchedConfig.rackNominalEnergykWh / 1000).toFixed(2) }} MWh
            </div>
            <div>{{ $t('runningConditions.clusterEnergy') }}: {{ matchedConfig.clusterNominalEnergyMWh }} MWh</div>
            <div>{{ $t('runningConditions.containerEnergy') }}: {{ matchedConfig.containerNominalEnergyMWh }} MWh</div>
          </div>
        </div>
      </div>

      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold ins-1">07</span>
          <div>
            <h3 class="section-title ins-2">
              {{ $t('runningConditions.pcsSectionTitle') }}
            </h3>
          </div>
        </div>
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
      </div>

      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold ins-1">08</span>
          <div>
            <h3 class="section-title ins-2">
              {{ $t('runningConditions.section07') }}
            </h3>
          </div>
        </div>
        <div class="grid grid-cols-3 gap-3 text-[10px]">
          <div>
            <span class="label-text">{{ $t('runningConditions.certifications.cell') }}</span>
            <div class="rounded p-2 space-y-1.5 ins-6">
              <label
                v-for="(opt, idx) in certOptionsI18n.cell"
                :key="certKeys.cell[idx]"
                class="flex items-center gap-1.5 cursor-pointer ins-3"
              >
                <input v-model="form.certCell" type="checkbox" :value="certKeys.cell[idx]" class="accent-teal-500" />
                {{ opt }}
              </label>
            </div>
          </div>
          <div>
            <span class="label-text">{{ $t('runningConditions.certifications.system') }}</span>
            <div class="rounded p-2 space-y-1.5 ins-6">
              <label
                v-for="(opt, idx) in certOptionsI18n.system"
                :key="certKeys.system[idx]"
                class="flex items-center gap-1.5 cursor-pointer ins-3"
              >
                <input
                  v-model="form.certSystem"
                  type="checkbox"
                  :value="certKeys.system[idx]"
                  class="accent-amber-500"
                />
                {{ opt }}
              </label>
            </div>
          </div>
          <div>
            <span class="label-text">{{ $t('runningConditions.certifications.grid') }}</span>
            <div class="rounded p-2 space-y-1.5 ins-6">
              <label
                v-for="(opt, idx) in certOptionsI18n.grid"
                :key="certKeys.grid[idx]"
                class="flex items-center gap-1.5 cursor-pointer ins-3"
              >
                <input v-model="form.certGrid" type="checkbox" :value="certKeys.grid[idx]" class="accent-blue-500" />
                {{ opt }}
              </label>
            </div>
          </div>
        </div>
        <div class="mt-2 grid grid-cols-2 gap-3 text-[10px]">
          <div>
            <span class="label-text">{{ $t('runningConditions.certifications.extra') }}</span>
            <div class="rounded p-2 space-y-1.5 ins-6">
              <label
                v-for="(opt, idx) in certOptionsI18n.extra"
                :key="certKeys.extra[idx]"
                class="flex items-center gap-1.5 cursor-pointer ins-3"
              >
                <input
                  v-model="form.certExtra"
                  type="checkbox"
                  :value="certKeys.extra[idx]"
                  class="accent-purple-500"
                />
                {{ opt }}
              </label>
            </div>
          </div>
          <div>
            <span class="label-text">{{ $t('runningConditions.certifications.gridCode') }}</span>
            <div class="rounded p-2 space-y-1.5 ins-6">
              <label
                v-for="(opt, idx) in certOptionsI18n.gridCode"
                :key="certKeys.gridCode[idx]"
                class="flex items-center gap-1.5 cursor-pointer ins-3"
              >
                <input
                  v-model="form.certGridCode"
                  type="checkbox"
                  :value="certKeys.gridCode[idx]"
                  class="accent-emerald-500"
                />
                {{ opt }}
              </label>
            </div>
          </div>
        </div>
      </div>

      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold ins-1">09</span>
          <div>
            <h3 class="section-title ins-2">
              {{ $t('runningConditions.section08') }}
            </h3>
          </div>
        </div>
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
      </div>

      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold ins-1">10</span>
          <div>
            <h3 class="section-title ins-2">
              {{ $t('runningConditions.section09') }}
            </h3>
          </div>
        </div>
        <p class="label-text mb-3">
          {{ $t('runningConditions.uploadHint') }}
        </p>
        <div
          class="border-2 border-dashed rounded-lg p-6 text-center transition-colors cursor-pointer"
          :style="
            uploadHover
              ? 'border-color: var(--color-accent); background: var(--color-accent-glow);'
              : 'border-color: var(--color-input-border);'
          "
          @dragover.prevent="uploadHover = true"
          @dragleave.prevent="uploadHover = false"
          @drop.prevent="onDrop"
          @click="triggerUpload"
        >
          <input
            ref="fileInput"
            type="file"
            accept=".pdf,.doc,.docx,.xls,.xlsx,.csv"
            class="hidden"
            @change="onFileChange"
          />
          <div v-if="uploading" class="ins-5 text-xs">
            <div class="animate-spin w-4 h-4 border-2 border-t-transparent rounded-full mx-auto mb-2 ins-7" />
            {{ $t('runningConditions.uploading') }}
          </div>
          <div v-else-if="uploadResult" class="text-xs">
            <span class="ins-8 font-bold">{{ $t('common.done') }}</span>
            <span class="ins-9 ml-2">{{ uploadResult.fieldsExtracted }} {{ $t('runningConditions.uploadDone') }}</span>
            <button class="ml-3 underline text-xs ins-5" @click.stop="applyExtracted">
              {{ $t('runningConditions.applyForm') }}
            </button>
            <button class="ml-3 underline text-xs ins-9" @click.stop="uploadResult = null">
              {{ $t('runningConditions.clearForm') }}
            </button>
          </div>
          <div v-else>
            <div class="text-2xl mb-1 opacity-40">📄</div>
            <p class="text-xs ins-3">
              {{ $t('runningConditions.dragDrop') }}
              <span class="ins-5 underline">
                {{ $t('runningConditions.clickSelect') }}
              </span>
            </p>
            <p class="text-[10px] mt-1 ins-9">
              {{ $t('runningConditions.uploadSupport') }}
            </p>
          </div>
        </div>
      </div>

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
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useBessStore, DEFAULT_SURVEY } from '../stores/bess.js'
import { useProducts } from '../composables/useProducts'
import { useDraft, useDraftRef } from '../composables/useDraft'
import { useCountryList } from '../composables/useCountryList'

const { t } = useI18n()
const store = useBessStore()
const emit = defineEmits(['applyParams'])

const { filterCountries } = useCountryList()

const {
  cells,
  packs,
  racks,
  clusters,
  containers,
  cellModels,
  cellMfrs,
  getPackByCellModel,
  getRackByPackModel,
  getClusterByRackModel,
  getContainerByCellModel,
  getContainerByClusterModel,
  matchConfigRule,
  loadAll
} = useProducts()

const selectedCellModel = useDraftRef('rc-selected-cell-model', '').state
const selectedPackModel = useDraftRef('rc-selected-pack-model', '').state
const selectedRackModel = useDraftRef('rc-selected-rack-model', '').state
const selectedClusterModel = useDraftRef('rc-selected-cluster-model', '').state
const selectedContainerModel = useDraftRef('rc-selected-container-model', '').state

const matchedConfig = useDraftRef('rc-matched-config', null).state
const autoMatchEnabled = useDraftRef('rc-auto-match-enabled', true).state

const { state: form, clearDraft: clearFormDraft } = useDraft('rc-form', {
  projectName: '',
  projectType: '',
  country: '',
  city: '',
  site: '',
  totalMW: null,
  totalMWh: null,
  durationHours: null,
  cyclesPerDay: DEFAULT_SURVEY.cyclesPerDay,
  altitude: null,
  tempMax: null,
  tempMin: null,
  tempAvg: null,
  humidity: null,
  seismicZone: '',
  corrosionClass: 'c3',
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

const certKeys = {
  cell: ['IEC 62619', 'IEC 62620', 'UL 1642', 'UN 38.3', 'GB/T 36276'],
  system: ['UL 9540', 'UL 9540A', 'UL 1973', 'IEC 62933-5-2', 'NFPA 855', 'IEC 62477-1'],
  grid: ['IEEE 1547', 'IEC 61000-6-2/4', 'UL 1741', 'IEC 62933-4-2', 'IEC 60730'],
  extra: ['ISO 14001', 'ISO 45001', 'ISO 9001', 'CE Marking', 'UKCA', 'RCM'],
  gridCode: ['UK G99', 'VDE-AR-N 4110', 'EN 50549-1', 'IEEE 2800', 'AEMO Grid Code', 'SASO/IEC']
}

// 国家 combobox 状态
const countryInput = ref('')
const countryDropdown = ref(false)
const filteredCountries = computed(() => {
  return filterCountries(countryInput.value)
})
function onCountryInput() {
  form.country = countryInput.value
  countryDropdown.value = true
}
function onCountryBlur() {
  setTimeout(() => {
    countryDropdown.value = false
  }, 150)
}
function selectCountry(c) {
  form.country = c
  countryInput.value = c
  countryDropdown.value = false
}

// --- auto-calc: durationHours ---
const isDurationAuto = ref(true)

// 国家输入框同步
watch(
  () => form.country,
  (val) => {
    if (val && val !== countryInput.value) countryInput.value = val
  }
)

function autoCalcDuration() {
  if (form.totalMWh > 0 && form.totalMW > 0) {
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
  if (form.tempMax != null && form.tempMin != null) {
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
  if (form.sohYear1 != null && form.sohYear25 != null) {
    return +((form.sohYear1 - form.sohYear25) / 24).toFixed(2)
  }
  return null
})

const certOptionsI18n = computed(() => ({
  cell: certKeys.cell.map((c) => t(`runningConditions.certificates.${c}`)),
  system: certKeys.system.map((s) => t(`runningConditions.certificates.${s}`)),
  grid: certKeys.grid.map((g) => t(`runningConditions.certificates.${g}`)),
  extra: certKeys.extra.map((e) => t(`runningConditions.certificates.${e}`)),
  gridCode: certKeys.gridCode.map((gc) => t(`runningConditions.certificates.${gc}`))
}))

const fileInput = ref(null)
const uploadHover = ref(false)
const uploading = ref(false)
const uploadResult = ref(null)

function triggerUpload() {
  fileInput.value?.click()
}

function onFileChange(e) {
  const file = e.target.files?.[0]
  if (file) parseFile(file)
}

function onDrop(e) {
  uploadHover.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file) parseFile(file)
}

async function parseFile(file) {
  uploading.value = true
  uploadResult.value = null
  try {
    const formData = new FormData()
    formData.append('file', file)
    const resp = await fetch('/api/upload/extract', { method: 'POST', body: formData })
    const contentType = resp.headers.get('content-type') || ''
    if (!contentType.includes('application/json')) {
      throw new Error(t('runningConditions.parseUnavailable'))
    }
    const data = await resp.json()
    if (data.extracted) {
      uploadResult.value = { extracted: data.extracted, fieldsExtracted: Object.keys(data.extracted).length }
    } else {
      uploadResult.value = {
        extracted: {},
        fieldsExtracted: 0,
        error: data.error || t('runningConditions.extractFailed')
      }
    }
  } catch {
    uploadResult.value = { extracted: {}, fieldsExtracted: 0, error: t('runningConditions.parseUnavailable') }
  }
  uploading.value = false
}

function applyExtracted() {
  if (!uploadResult.value?.extracted) return
  const ext = uploadResult.value.extracted
  const mapping = {
    project_name: 'projectName',
    project_type: 'projectType',
    country: 'country',
    city: 'city',
    site: 'site',
    total_mw: 'totalMW',
    total_mwh: 'totalMWh',
    duration_h: 'durationHours',
    cycles_per_day: 'cyclesPerDay',
    altitude_m: 'altitude',
    temp_max_c: 'tempMax',
    temp_min_c: 'tempMin',
    temp_avg_c: 'tempAvg',
    humidity_pct: 'humidity',
    seismic_zone: 'seismicZone',
    corrosion_class: 'corrosionClass',
    installation_type: 'installationType',
    grid_voltage_kv: 'gridVoltage',
    grid_freq_hz: 'gridFreq',
    sc_capacity_mva: 'scCapacity',
    neutral_grounding: 'neutralGrounding',
    dc_voltage_range: 'dcVoltageRange',
    ac_voltage_v: 'acVoltage',
    pf_range: 'pfRange',
    thdi_pct: 'thdiLimit',
    rte_target_pct: 'rteTarget',
    availability_target_pct: 'availabilityTarget',
    soh_year1_pct: 'sohYear1',
    soh_year25_pct: 'sohYear25',
    calendar_life_y: 'calendarLife',
    cycle_life: 'cycleLife',
    aux_consumption_pct: 'auxConsumption',
    response_time_ms: 'responseTime'
  }
  for (const [k, v] of Object.entries(ext)) {
    const target = mapping[k]
    if (target && v !== null && v !== undefined) {
      const f = form[target]
      if (typeof f === 'number' || f === null) form[target] = Number(v)
      else form[target] = String(v)
    }
  }
}

function exportCSV() {
  const eq = t('export.eqHeader')
  const sep = t('export.separator')
  const date = new Date().toISOString().slice(0, 10)
  const projectName = form.projectName || store.survey.projectName || 'Untitled'

  // 按类别分组
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

  // 报告标题头
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

  // 免责声明
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
  uploadResult.value = null
  selectedCellModel.value = ''
  selectedPackModel.value = ''
  selectedRackModel.value = ''
  selectedClusterModel.value = ''
  selectedContainerModel.value = ''
  matchedConfig.value = null
}

const availablePacks = computed(() => {
  if (!selectedCellModel.value) return packs.value
  return getPackByCellModel(selectedCellModel.value)
})

const availableRacks = computed(() => {
  if (!selectedPackModel.value) return racks.value
  return getRackByPackModel(selectedPackModel.value)
})

const availableClusters = computed(() => {
  if (!selectedRackModel.value) return clusters.value
  return getClusterByRackModel(selectedRackModel.value)
})

const availableContainers = computed(() => {
  if (!selectedClusterModel.value && !selectedCellModel.value) return containers.value
  if (selectedClusterModel.value) {
    const byCluster = getContainerByClusterModel(selectedClusterModel.value)
    if (byCluster.length > 0) return byCluster
  }
  if (selectedCellModel.value) {
    const byCell = getContainerByCellModel(selectedCellModel.value)
    if (byCell.length > 0) return byCell
  }
  return containers.value
})

async function onCellChange() {
  if (!autoMatchEnabled.value) return

  selectedPackModel.value = ''
  selectedRackModel.value = ''
  selectedClusterModel.value = ''
  selectedContainerModel.value = ''
  matchedConfig.value = null

  if (!selectedCellModel.value) return

  const packList = getPackByCellModel(selectedCellModel.value)
  if (packList.length > 0) {
    selectedPackModel.value = packList[0].model
  }

  const result = await matchConfigRule({ cellModel: selectedCellModel.value })
  if (result.success && result.data?.matched && result.data?.rule) {
    matchedConfig.value = result.data.rule
    selectedPackModel.value = result.data.rule.packModel || selectedPackModel.value
    selectedRackModel.value = result.data.rule.rackModel || ''
    selectedClusterModel.value = result.data.rule.clusterModel || ''
    selectedContainerModel.value = result.data.rule.containerModel || ''
  }
}

async function onPackChange() {
  if (!autoMatchEnabled.value) return

  selectedRackModel.value = ''
  selectedClusterModel.value = ''
  selectedContainerModel.value = ''

  if (!selectedPackModel.value) return

  const rackList = getRackByPackModel(selectedPackModel.value)
  if (rackList.length > 0) {
    selectedRackModel.value = rackList[0].model
  }

  if (selectedCellModel.value) {
    const result = await matchConfigRule({ cellModel: selectedCellModel.value, packModel: selectedPackModel.value })
    if (result.success && result.data?.matched && result.data?.rule) {
      matchedConfig.value = result.data.rule
      selectedRackModel.value = result.data.rule.rackModel || selectedRackModel.value
      selectedClusterModel.value = result.data.rule.clusterModel || ''
      selectedContainerModel.value = result.data.rule.containerModel || ''
    }
  }
}

async function onRackChange() {
  if (!autoMatchEnabled.value) return

  selectedClusterModel.value = ''
  selectedContainerModel.value = ''

  if (!selectedRackModel.value) return

  const clusterList = getClusterByRackModel(selectedRackModel.value)
  if (clusterList.length > 0) {
    selectedClusterModel.value = clusterList[0].model
  }

  if (selectedCellModel.value && selectedPackModel.value) {
    const result = await matchConfigRule({
      cellModel: selectedCellModel.value,
      packModel: selectedPackModel.value,
      rackModel: selectedRackModel.value
    })
    if (result.success && result.data?.matched && result.data?.rule) {
      matchedConfig.value = result.data.rule
      selectedClusterModel.value = result.data.rule.clusterModel || selectedClusterModel.value
      selectedContainerModel.value = result.data.rule.containerModel || ''
    }
  }
}

async function onClusterChange() {
  if (!autoMatchEnabled.value) return

  selectedContainerModel.value = ''

  if (!selectedClusterModel.value) return

  const containerList = getContainerByClusterModel(selectedClusterModel.value)
  if (containerList.length > 0) {
    selectedContainerModel.value = containerList[0].model
  }

  if (selectedCellModel.value && selectedPackModel.value && selectedRackModel.value) {
    const result = await matchConfigRule({
      cellModel: selectedCellModel.value,
      packModel: selectedPackModel.value,
      rackModel: selectedRackModel.value,
      clusterModel: selectedClusterModel.value
    })
    if (result.success && result.data?.matched && result.data?.rule) {
      matchedConfig.value = result.data.rule
      selectedContainerModel.value = result.data.rule.containerModel || selectedContainerModel.value
    }
  }
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
.ins-1 {
  background: var(--color-accent-glow);
  color: var(--color-accent);
}
.ins-2 {
  color: var(--color-accent);
  border-color: var(--color-accent);
}
.ins-3 {
  color: var(--color-text-secondary);
}
.ins-4 {
  background: var(--color-accent-glow);
}
.ins-5 {
  color: var(--color-accent);
}
.ins-6 {
  background: var(--color-input-bg);
}
.ins-7 {
  border-color: var(--color-accent);
  border-top-color: transparent;
}
.ins-8 {
  color: var(--color-success);
}
.ins-9 {
  color: var(--color-text-muted);
}
.ins-10 {
  background: var(--color-input-bg);
  border: 1px solid var(--color-input-border);
  color: var(--color-text-secondary);
}

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

/* Combobox 下拉面板 */
.combobox-wrapper {
  position: relative;
}
.combobox-wrapper .form-field-input {
  width: 100%;
}
.combobox-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 100;
  max-height: 220px;
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
.option-name {
  flex: 1;
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-align: left;
}
</style>
