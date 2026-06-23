<template>
  <div class="h-full overflow-y-auto custom-scrollbar">
    <div class="max-w-5xl mx-auto space-y-4 py-2">
      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold" style="background: var(--color-accent-glow); color: var(--color-accent);">01</span>
          <div>
            <h3 class="section-title" style="color: var(--color-accent); border-color: var(--color-accent);">{{ $t('runningConditions.section01') }}</h3>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-3">
          <div class="col-span-2">
            <label class="label-text">{{ $t('runningConditions.projectName') }}</label>
            <input v-model="form.projectName" class="input-field" :placeholder="$t('runningConditions.projectName')">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.projectType') }}</label>
            <select v-model="form.projectType" class="input-field">
              <option value="">{{ $t('common.select') }}</option>
              <option value="utility">{{ $t('runningConditions.projectTypes.utility') }}</option>
              <option value="cni">{{ $t('runningConditions.projectTypes.ci') }}</option>
              <option value="residential">{{ $t('runningConditions.projectTypes.residential') }}</option>
              <option value="microgrid">{{ $t('runningConditions.projectTypes.microgrid') }}</option>
              <option value="solar-plus-bess">{{ $t('runningConditions.projectTypes.solar') }}</option>
              <option value="wind-plus-bess">{{ $t('runningConditions.projectTypes.wind') }}</option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.location') }}</label>
            <input v-model="form.location" class="input-field" :placeholder="$t('runningConditions.location')">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.ratedPower') }}</label>
            <input v-model.number="form.totalMW" type="number" class="input-field" placeholder="200">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.ratedEnergy') }}</label>
            <input v-model.number="form.totalMWh" type="number" class="input-field" placeholder="800">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.chargeDuration') }}</label>
            <input v-model.number="form.durationHours" type="number" class="input-field" placeholder="4">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.dayCycles') }}</label>
            <input v-model.number="form.cyclesPerDay" type="number" class="input-field" placeholder="1">
          </div>
        </div>
      </div>

      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold" style="background: var(--color-accent-glow); color: var(--color-accent);">02</span>
          <div>
            <h3 class="section-title" style="color: var(--color-accent); border-color: var(--color-accent);">{{ $t('runningConditions.section02') }}</h3>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="label-text">{{ $t('runningConditions.altitude') }}</label>
            <input v-model.number="form.altitude" type="number" class="input-field" placeholder="≤2000">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.maxTemp') }}</label>
            <input v-model.number="form.tempMax" type="number" class="input-field" placeholder="45">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.minTemp') }}</label>
            <input v-model.number="form.tempMin" type="number" class="input-field" placeholder="-20">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.avgTemp') }}</label>
            <input v-model.number="form.tempAvg" type="number" class="input-field" placeholder="25">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.humidity') }}</label>
            <input v-model.number="form.humidity" type="number" class="input-field" placeholder="≤95">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.seismicZone') }}</label>
            <select v-model="form.seismicZone" class="input-field">
              <option value="">{{ $t('common.select') }}</option>
              <option value="zone1">{{ $t('runningConditions.seismicZones.low') }}</option>
              <option value="zone2">Zone II</option>
              <option value="zone3">{{ $t('runningConditions.seismicZones.mid') }}</option>
              <option value="zone4">{{ $t('runningConditions.seismicZones.high') }}</option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.corrosionLevel') }}</label>
            <select v-model="form.corrosionClass" class="input-field">
              <option value="">{{ $t('common.select') }}</option>
              <option value="c1">{{ $t('runningConditions.corrosionLevels.c1') }}</option>
              <option value="c2">{{ $t('runningConditions.corrosionLevels.c2') }}</option>
              <option value="c3">{{ $t('runningConditions.corrosionLevels.c3') }}</option>
              <option value="c4">{{ $t('runningConditions.corrosionLevels.c4') }}</option>
              <option value="c5">{{ $t('runningConditions.corrosionLevels.c5') }}</option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.installType') }}</label>
            <select v-model="form.installationType" class="input-field">
              <option value="">{{ $t('common.select') }}</option>
              <option value="outdoor">{{ $t('runningConditions.installTypes.outdoor') }}</option>
              <option value="indoor">{{ $t('runningConditions.installTypes.indoor') }}</option>
              <option value="semi-outdoor">{{ $t('runningConditions.installTypes.semi') }}</option>
            </select>
          </div>
        </div>
      </div>

      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold" style="background: var(--color-accent-glow); color: var(--color-accent);">03</span>
          <div>
            <h3 class="section-title" style="color: var(--color-accent); border-color: var(--color-accent);">{{ $t('runningConditions.section03') }}</h3>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="label-text">{{ $t('runningConditions.gridVoltage') }}</label>
            <select v-model="form.gridVoltage" class="input-field">
              <option value="">{{ $t('common.select') }}</option>
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
            <select v-model="form.gridFreq" class="input-field">
              <option value="">{{ $t('common.select') }}</option>
              <option value="50Hz">50 Hz</option>
              <option value="60Hz">60 Hz</option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.shortCircuit') }}</label>
            <input v-model.number="form.scCapacity" type="number" class="input-field" placeholder="5000">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.neutralGround') }}</label>
            <select v-model="form.neutralGrounding" class="input-field">
              <option value="">{{ $t('common.select') }}</option>
              <option value="solid">{{ $t('runningConditions.neutralGrounds.solid') }}</option>
              <option value="resistance">{{ $t('runningConditions.neutralGrounds.resistance') }}</option>
              <option value="arc-suppression">{{ $t('runningConditions.neutralGrounds.arcSuppression') }}</option>
              <option value="ungrounded">{{ $t('runningConditions.neutralGrounds.ungrounded') }}</option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.dcVoltage') }}</label>
            <input v-model="form.dcVoltageRange" class="input-field" placeholder="1000-1500">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.acVoltage') }}</label>
            <input v-model="form.acVoltage" class="input-field" placeholder="690">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.pfRange') }}</label>
            <input v-model="form.pfRange" class="input-field" placeholder="0.99leading-0.99lagging">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.thdiReq') }}</label>
            <input v-model.number="form.thdiLimit" type="number" class="input-field" placeholder="5">
          </div>
        </div>
      </div>

      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold" style="background: var(--color-accent-glow); color: var(--color-accent);">04</span>
          <div>
            <h3 class="section-title" style="color: var(--color-accent); border-color: var(--color-accent);">{{ $t('runningConditions.section04') }}</h3>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="label-text">{{ $t('runningConditions.rteTarget') }}</label>
            <input v-model.number="form.rteTarget" type="number" step="0.01" class="input-field" placeholder="85">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.acAvailability') }}</label>
            <input v-model.number="form.availabilityTarget" type="number" step="0.01" class="input-field" placeholder="99">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.sohYear1') }}</label>
            <input v-model.number="form.sohYear1" type="number" step="0.01" class="input-field" placeholder="93.2">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.sohYear25') }}</label>
            <input v-model.number="form.sohYear25" type="number" step="0.01" class="input-field" placeholder="60">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.calendarLife') }}</label>
            <input v-model.number="form.calendarLife" type="number" class="input-field" placeholder="25">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.cycleLife') }}</label>
            <input v-model.number="form.cycleLife" type="number" class="input-field" placeholder="6000">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.auxConsumption') }}</label>
            <input v-model.number="form.auxConsumption" type="number" step="0.01" class="input-field" placeholder="5">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.responseTime') }}</label>
            <input v-model.number="form.responseTime" type="number" class="input-field" placeholder="50">
          </div>
        </div>
      </div>

      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold" style="background: var(--color-accent-glow); color: var(--color-accent);">05</span>
          <div>
            <h3 class="section-title" style="color: var(--color-accent); border-color: var(--color-accent);">{{ $t('runningConditions.section05') }}</h3>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="label-text">{{ $t('runningConditions.cellChemistry') }}</label>
            <select v-model="form.cellChemistry" class="input-field">
              <option value="">{{ $t('common.select') }}</option>
              <option value="LFP">{{ $t('runningConditions.chemistries.lfp') }}</option>
              <option value="NMC">{{ $t('runningConditions.chemistries.nmc') }}</option>
              <option value="LTO">{{ $t('runningConditions.chemistries.lto') }}</option>
              <option value="sodium-ion">{{ $t('runningConditions.chemistries.naion') }}</option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.cellCapacity') }}</label>
            <input v-model="form.cellCapacityRange" class="input-field" placeholder="280-700">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.cellCycleLife') }}</label>
            <input v-model.number="form.cellCycleLife" type="number" class="input-field" placeholder="6000">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.eolCriteria') }}</label>
            <input v-model.number="form.eolThreshold" type="number" step="0.1" class="input-field" placeholder="70">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.cellTempRange') }}</label>
            <input v-model="form.cellTempRange" class="input-field" placeholder="-20 ~ +55">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.cellVoltageDiff') }}</label>
            <input v-model.number="form.cellVoltageDiff" type="number" class="input-field" placeholder="20">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.cellTempDiff') }}</label>
            <input v-model.number="form.cellTempDiff" type="number" step="0.5" class="input-field" placeholder="3">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.thermalRunaway') }}</label>
            <select v-model="form.thermalRunawayPrev" class="input-field">
              <option value="">{{ $t('common.select') }}</option>
              <option value="pack-level">{{ $t('runningConditions.thermalRunaways.pack') }}</option>
              <option value="cluster-level">{{ $t('runningConditions.thermalRunaways.cluster') }}</option>
              <option value="rack-level">{{ $t('runningConditions.thermalRunaways.rack') }}</option>
            </select>
          </div>
        </div>
      </div>

      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold" style="background: var(--color-accent-glow); color: var(--color-accent);">06</span>
          <div>
            <h3 class="section-title" style="color: var(--color-accent); border-color: var(--color-accent);">{{ $t('runningConditions.section06') }}</h3>
          </div>
          <div class="ml-auto">
            <label class="flex items-center gap-2 text-xs cursor-pointer" style="color: var(--color-text-secondary);">
              <input type="checkbox" v-model="autoMatchEnabled" class="accent-teal-500">
              {{ $t('runningConditions.autoMatch') }}
            </label>
          </div>
        </div>
        <div class="grid grid-cols-5 gap-3">
          <div>
            <label class="label-text">{{ $t('runningConditions.cellModel') }}</label>
            <select v-model="selectedCellModel" class="input-field" @change="onCellChange">
              <option value="">{{ $t('common.select') }}</option>
              <option v-for="cell in cells" :key="cell.id" :value="cell.model">
                {{ cell.mfr }} - {{ cell.model }} ({{ cell.capacityAh }}Ah)
              </option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.packModel') }}</label>
            <select v-model="selectedPackModel" class="input-field" @change="onPackChange">
              <option value="">{{ $t('common.select') }}</option>
              <option v-for="pack in availablePacks" :key="pack.id" :value="pack.model">
                {{ pack.model }} ({{ pack.nominalEnergyKwh }}kWh)
              </option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.rackModel') }}</label>
            <select v-model="selectedRackModel" class="input-field" @change="onRackChange">
              <option value="">{{ $t('common.select') }}</option>
              <option v-for="rack in availableRacks" :key="rack.id" :value="rack.model">
                {{ rack.model }} ({{ rack.nominalEnergyKwh }}kWh)
              </option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.clusterModel') }}</label>
            <select v-model="selectedClusterModel" class="input-field" @change="onClusterChange">
              <option value="">{{ $t('common.select') }}</option>
              <option v-for="cluster in availableClusters" :key="cluster.id" :value="cluster.model">
                {{ cluster.model }} ({{ cluster.nominalEnergyMwh }}MWh)
              </option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.containerModel') }}</label>
            <select v-model="selectedContainerModel" class="input-field">
              <option value="">{{ $t('common.select') }}</option>
              <option v-for="container in availableContainers" :key="container.id" :value="container.model">
                {{ container.model }} ({{ container.ratedEnergyMwh }}MWh)
              </option>
            </select>
          </div>
        </div>
        <div v-if="matchedConfig" class="mt-3 p-3 rounded" style="background: var(--color-accent-glow);">
          <div class="text-xs font-bold mb-1" style="color: var(--color-accent);">{{ $t('runningConditions.matchedConfig') }}: {{ matchedConfig.name }}</div>
          <div class="text-[10px] space-y-0.5" style="color: var(--color-text-secondary);">
            <div>{{ $t('runningConditions.packEnergy') }}: {{ matchedConfig.packNominalEnergyKwh }} kWh</div>
            <div>{{ $t('runningConditions.rackEnergy') }}: {{ (matchedConfig.rackNominalEnergyKwh / 1000).toFixed(2) }} MWh</div>
            <div>{{ $t('runningConditions.clusterEnergy') }}: {{ matchedConfig.clusterNominalEnergyMwh }} MWh</div>
            <div>{{ $t('runningConditions.containerEnergy') }}: {{ matchedConfig.containerNominalEnergyMwh }} MWh</div>
          </div>
        </div>
      </div>

      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold" style="background: var(--color-accent-glow); color: var(--color-accent);">07</span>
          <div>
            <h3 class="section-title" style="color: var(--color-accent); border-color: var(--color-accent);">{{ $t('runningConditions.section06') }}</h3>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="label-text">{{ $t('runningConditions.pcsRatedPower') }}</label>
            <input v-model.number="form.pcsRatedPower" type="number" step="0.001" class="input-field" placeholder="2.5">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.pcsEfficiency') }}</label>
            <input v-model.number="form.pcsEfficiency" type="number" step="0.01" class="input-field" placeholder="98.5">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.overload') }}</label>
            <select v-model="form.pcsOverload" class="input-field">
              <option value="">{{ $t('common.select') }}</option>
              <option value="standard">{{ $t('runningConditions.overloads.standard') }}</option>
              <option value="enhanced">{{ $t('runningConditions.overloads.advanced') }}</option>
              <option value="high">{{ $t('runningConditions.overloads.premium') }}</option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.thdiReq') }}</label>
            <input v-model.number="form.pcsTHDi" type="number" step="0.1" class="input-field" placeholder="3">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.pfRange') }}</label>
            <input v-model="form.pcsPF" class="input-field" placeholder="-0.9 ~ +0.9">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.responseTime') }}</label>
            <input v-model.number="form.pcsResponseTime" type="number" class="input-field" placeholder="50">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.gridSupport') }}</label>
            <select v-model="form.pcsGridSupport" class="input-field">
              <option value="">{{ $t('common.select') }}</option>
              <option value="basic">{{ $t('runningConditions.gridSupports.basic') }}</option>
              <option value="advanced">{{ $t('runningConditions.gridSupports.advanced') }}</option>
              <option value="full">{{ $t('runningConditions.gridSupports.full') }}</option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.coolingType') }}</label>
            <select v-model="form.pcsCooling" class="input-field">
              <option value="">{{ $t('common.select') }}</option>
              <option value="forced-air">{{ $t('runningConditions.coolingTypes.forcedAir') }}</option>
              <option value="liquid">{{ $t('runningConditions.coolingTypes.liquid') }}</option>
              <option value="SiC-liquid">{{ $t('runningConditions.coolingTypes.fullSiC') }}</option>
            </select>
          </div>
        </div>
      </div>

      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold" style="background: var(--color-accent-glow); color: var(--color-accent);">07</span>
          <div>
            <h3 class="section-title" style="color: var(--color-accent); border-color: var(--color-accent);">{{ $t('runningConditions.section07') }}</h3>
          </div>
        </div>
        <div class="grid grid-cols-3 gap-3 text-[10px]">
          <div>
            <span class="label-text">{{ $t('runningConditions.certifications.cell') }}</span>
            <div class="rounded p-2 space-y-1.5" style="background: var(--color-input-bg);">
              <label v-for="opt in certOptions.cell" :key="opt" class="flex items-center gap-1.5 cursor-pointer" style="color: var(--color-text-secondary);">
                <input type="checkbox" :value="opt" v-model="form.certCell" class="accent-teal-500">{{ opt }}
              </label>
            </div>
          </div>
          <div>
            <span class="label-text">{{ $t('runningConditions.certifications.system') }}</span>
            <div class="rounded p-2 space-y-1.5" style="background: var(--color-input-bg);">
              <label v-for="opt in certOptions.system" :key="opt" class="flex items-center gap-1.5 cursor-pointer" style="color: var(--color-text-secondary);">
                <input type="checkbox" :value="opt" v-model="form.certSystem" class="accent-amber-500">{{ opt }}
              </label>
            </div>
          </div>
          <div>
            <span class="label-text">{{ $t('runningConditions.certifications.grid') }}</span>
            <div class="rounded p-2 space-y-1.5" style="background: var(--color-input-bg);">
              <label v-for="opt in certOptions.grid" :key="opt" class="flex items-center gap-1.5 cursor-pointer" style="color: var(--color-text-secondary);">
                <input type="checkbox" :value="opt" v-model="form.certGrid" class="accent-blue-500">{{ opt }}
              </label>
            </div>
          </div>
        </div>
        <div class="mt-2 grid grid-cols-2 gap-3 text-[10px]">
          <div>
            <span class="label-text">{{ $t('runningConditions.certifications.extra') }}</span>
            <div class="rounded p-2 space-y-1.5" style="background: var(--color-input-bg);">
              <label v-for="opt in certOptions.extra" :key="opt" class="flex items-center gap-1.5 cursor-pointer" style="color: var(--color-text-secondary);">
                <input type="checkbox" :value="opt" v-model="form.certExtra" class="accent-purple-500">{{ opt }}
              </label>
            </div>
          </div>
          <div>
            <span class="label-text">{{ $t('runningConditions.certifications.gridCode') }}</span>
            <div class="rounded p-2 space-y-1.5" style="background: var(--color-input-bg);">
              <label v-for="opt in certOptions.gridCode" :key="opt" class="flex items-center gap-1.5 cursor-pointer" style="color: var(--color-text-secondary);">
                <input type="checkbox" :value="opt" v-model="form.certGridCode" class="accent-emerald-500">{{ opt }}
              </label>
            </div>
          </div>
        </div>
      </div>

      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold" style="background: var(--color-accent-glow); color: var(--color-accent);">08</span>
          <div>
            <h3 class="section-title" style="color: var(--color-accent); border-color: var(--color-accent);">{{ $t('runningConditions.section08') }}</h3>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="label-text">{{ $t('runningConditions.epcModel') }}</label>
            <select v-model="form.epcModel" class="input-field">
              <option value="">{{ $t('common.select') }}</option>
              <option value="turnkey">{{ $t('runningConditions.epcModels.turnkey') }}</option>
              <option value="supply-only">{{ $t('runningConditions.epcModels.supplyOnly') }}</option>
              <option value="supply-supervision">{{ $t('runningConditions.epcModels.supplySupervision') }}</option>
              <option value="epcm">{{ $t('runningConditions.epcModels.epcm') }}</option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.omYears') }}</label>
            <input v-model.number="form.omYears" type="number" class="input-field" placeholder="5">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.performanceGuarantee') }}</label>
            <select v-model="form.prRequirement" class="input-field">
              <option value="">{{ $t('common.select') }}</option>
              <option value="availability-guarantee">{{ $t('runningConditions.pgs.availability') }}</option>
              <option value="rte-guarantee">{{ $t('runningConditions.pgs.rte') }}</option>
              <option value="soh-guarantee">{{ $t('runningConditions.pgs.soh') }}</option>
              <option value="full-guarantee">{{ $t('runningConditions.pgs.full') }}</option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.warrantyYears') }}</label>
            <input v-model.number="form.warrantyYears" type="number" class="input-field" placeholder="5">
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.scada') }}</label>
            <select v-model="form.scadaReq" class="input-field">
              <option value="">{{ $t('common.select') }}</option>
              <option value="none">{{ $t('runningConditions.scadaOptions.none') }}</option>
              <option value="basic">{{ $t('runningConditions.scadaOptions.basic') }}</option>
              <option value="advanced">{{ $t('runningConditions.scadaOptions.advanced') }}</option>
              <option value="full">{{ $t('runningConditions.scadaOptions.full') }}</option>
            </select>
          </div>
          <div>
            <label class="label-text">{{ $t('runningConditions.spareParts') }}</label>
            <select v-model="form.sparePartsStrategy" class="input-field">
              <option value="">{{ $t('common.select') }}</option>
              <option value="none">{{ $t('runningConditions.sparePartsOptions.none') }}</option>
              <option value="standard">{{ $t('runningConditions.sparePartsOptions.standard') }}</option>
              <option value="enhanced">{{ $t('runningConditions.sparePartsOptions.enhanced') }}</option>
              <option value="full">{{ $t('runningConditions.sparePartsOptions.full') }}</option>
            </select>
          </div>
        </div>
      </div>

      <div class="card p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded text-xs flex items-center justify-center font-bold" style="background: var(--color-accent-glow); color: var(--color-accent);">09</span>
          <div>
            <h3 class="section-title" style="color: var(--color-accent); border-color: var(--color-accent);">{{ $t('runningConditions.section09') }}</h3>
          </div>
        </div>
        <p class="label-text mb-3">{{ $t('runningConditions.uploadHint') }}</p>
        <div
          class="border-2 border-dashed rounded-lg p-6 text-center transition-colors cursor-pointer"
          :style="uploadHover ? 'border-color: var(--color-accent); background: var(--color-accent-glow);' : 'border-color: var(--color-input-border);'"
          @dragover.prevent="uploadHover = true"
          @dragleave.prevent="uploadHover = false"
          @drop.prevent="onDrop"
          @click="triggerUpload"
        >
          <input ref="fileInput" type="file" accept=".pdf,.doc,.docx,.xls,.xlsx,.csv" class="hidden" @change="onFileChange">
          <div v-if="uploading" style="color: var(--color-accent);" class="text-xs">
            <div class="animate-spin w-4 h-4 border-2 border-t-transparent rounded-full mx-auto mb-2" style="border-color: var(--color-accent); border-top-color: transparent;"></div>
            {{ $t('runningConditions.uploading') }}
          </div>
          <div v-else-if="uploadResult" class="text-xs">
            <span style="color: var(--color-success);" class="font-bold">{{ $t('common.done') }}</span>
            <span style="color: var(--color-text-muted);" class="ml-2">{{ uploadResult.fieldsExtracted }} {{ $t('runningConditions.uploadDone') }}</span>
            <button @click.stop="applyExtracted" class="ml-3 underline text-xs" style="color: var(--color-accent);">{{ $t('runningConditions.applyForm') }}</button>
            <button @click.stop="uploadResult = null" class="ml-3 underline text-xs" style="color: var(--color-text-muted);">{{ $t('runningConditions.clearForm') }}</button>
          </div>
          <div v-else>
            <div class="text-2xl mb-1 opacity-40">📄</div>
            <p class="text-xs" style="color: var(--color-text-secondary);">{{ $t('runningConditions.dragDrop') }} <span style="color: var(--color-accent);" class="underline">{{ $t('runningConditions.clickSelect') }}</span></p>
            <p class="text-[10px] mt-1" style="color: var(--color-text-muted);">{{ $t('runningConditions.uploadSupport') }}</p>
          </div>
        </div>
      </div>

      <div class="text-right pb-4">
        <button @click="clearAll" class="text-xs underline mr-4" style="color: var(--color-text-muted);">{{ $t('runningConditions.resetAll') }}</button>
        <button @click="exportCSV" class="text-xs px-4 py-1.5 rounded mr-2 transition-colors" style="background: var(--color-input-bg); border: 1px solid var(--color-input-border); color: var(--color-text-secondary);">{{ $t('runningConditions.exportCSV') }}</button>
        <button @click="applyToSimulation" class="btn-primary">
          {{ $t('runningConditions.applyEngine') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useProducts } from '../composables/useProducts'

const { t } = useI18n()
const emit = defineEmits(['applyParams'])

const {
  cells, packs, racks, clusters, containers,
  cellModels, cellMfrs,
  getPackByCellModel, getRackByPackModel, getClusterByRackModel,
  getContainerByCellModel, getContainerByClusterModel,
  matchConfigRule, loadAll,
} = useProducts()

const selectedCellModel = ref('')
const selectedPackModel = ref('')
const selectedRackModel = ref('')
const selectedClusterModel = ref('')
const selectedContainerModel = ref('')

const matchedConfig = ref(null)
const autoMatchEnabled = ref(true)

const form = reactive({
  projectName: '',
  projectType: '',
  location: '',
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
  sparePartsStrategy: '',
})

const certOptions = {
  cell: ['IEC 62619 (锂电安全)', 'IEC 62620 (性能测试)', 'UL 1642 (电芯安全)', 'UN 38.3 (运输安全)', 'GB/T 36276 (中国国标)'],
  system: ['UL 9540 (系统级安全)', 'UL 9540A (火烧蔓延测试)', 'UL 1973 (模组标准)', 'IEC 62933-5-2 (并网安全)', 'NFPA 855 (消防规范)', 'IEC 62477-1 (PCS安全)'],
  grid: ['IEEE 1547 (并网互联)', 'IEC 61000-6-2/4 (EMC抗扰/发射)', 'UL 1741 (逆变器)', 'IEC 62933-4-2 (环境评估)', 'IEC 60730 (自动控制)'],
  extra: ['ISO 14001 (环境管理)', 'ISO 45001 (职业健康)', 'ISO 9001 (质量管理)', 'CE Marking (欧盟)', 'UKCA (英国)', 'RCM (澳大利亚)'],
  gridCode: ['UK G99 (英国)', 'VDE-AR-N 4110 (德国)', 'EN 50549-1 (欧盟)', 'IEEE 2800 (美国 BPS)', 'AEMO Grid Code (澳大利亚)', 'SASO/IEC (中东/沙特)'],
}

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
    const data = await resp.json()
    if (data.extracted) {
      uploadResult.value = { extracted: data.extracted, fieldsExtracted: Object.keys(data.extracted).length }
    } else {
      uploadResult.value = { extracted: {}, fieldsExtracted: 0, error: data.error || '未能提取参数' }
    }
  } catch {
    uploadResult.value = { extracted: {}, fieldsExtracted: 0, error: '解析服务不可用' }
  }
  uploading.value = false
}

function applyExtracted() {
  if (!uploadResult.value?.extracted) return
  const ext = uploadResult.value.extracted
  const mapping = {
    project_name: 'projectName', project_type: 'projectType', location: 'location',
    total_mw: 'totalMW', total_mwh: 'totalMWh', duration_h: 'durationHours',
    cycles_per_day: 'cyclesPerDay', altitude_m: 'altitude',
    temp_max_c: 'tempMax', temp_min_c: 'tempMin', temp_avg_c: 'tempAvg',
    humidity_pct: 'humidity', seismic_zone: 'seismicZone', corrosion_class: 'corrosionClass',
    installation_type: 'installationType', grid_voltage_kv: 'gridVoltage', grid_freq_hz: 'gridFreq',
    sc_capacity_mva: 'scCapacity', neutral_grounding: 'neutralGrounding',
    dc_voltage_range: 'dcVoltageRange', ac_voltage_v: 'acVoltage',
    pf_range: 'pfRange', thdi_pct: 'thdiLimit', rte_target_pct: 'rteTarget',
    availability_target_pct: 'availabilityTarget', soh_year1_pct: 'sohYear1',
    soh_year25_pct: 'sohYear25', calendar_life_y: 'calendarLife',
    cycle_life: 'cycleLife', aux_consumption_pct: 'auxConsumption', response_time_ms: 'responseTime',
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
  const rows = [['Key', 'Value']]
  for (const [k, v] of Object.entries(form)) {
    rows.push([k, v ?? ''])
  }
  const csv = '\uFEFF' + rows.map(r => r.map(c => `"${String(c).replace(/"/g, '""')}"`).join(',')).join('\n')
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url; a.download = `BESS_Conditions_${form.projectName || 'Export'}.csv`
  document.body.appendChild(a); a.click(); document.body.removeChild(a)
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
  if (result.success && result.matched && result.rule) {
    matchedConfig.value = result.rule
    selectedPackModel.value = result.rule.packModel || selectedPackModel.value
    selectedRackModel.value = result.rule.rackModel || ''
    selectedClusterModel.value = result.rule.clusterModel || ''
    selectedContainerModel.value = result.rule.containerModel || ''
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
    if (result.success && result.matched && result.rule) {
      matchedConfig.value = result.rule
      selectedRackModel.value = result.rule.rackModel || selectedRackModel.value
      selectedClusterModel.value = result.rule.clusterModel || ''
      selectedContainerModel.value = result.rule.containerModel || ''
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
    if (result.success && result.matched && result.rule) {
      matchedConfig.value = result.rule
      selectedClusterModel.value = result.rule.clusterModel || selectedClusterModel.value
      selectedContainerModel.value = result.rule.containerModel || ''
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
    if (result.success && result.matched && result.rule) {
      matchedConfig.value = result.rule
      selectedContainerModel.value = result.rule.containerModel || selectedContainerModel.value
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
    location: form.location,
  }
  emit('applyParams', mapped)
}
</script>
