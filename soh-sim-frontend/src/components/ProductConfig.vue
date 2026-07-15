<template>
  <div class="h-full overflow-y-auto custom-scrollbar">
    <div class="max-w-6xl mx-auto space-y-4 py-2">
      <div class="rounded-lg p-4 card-panel">
        <div class="flex items-center gap-2 mb-3">
          <span
            class="w-6 h-6 rounded flex items-center justify-center font-bold text-xs tag-glow text-accent-secondary"
          >
            A
          </span>
          <div>
            <h3 class="font-bold text-sm">
              {{ $t('productConfig.cellLibrary') }}
              <span class="text-[10px] font-normal ml-1 text-muted">Battery Cell Library</span>
            </h3>
          </div>
          <div class="ml-auto flex gap-2">
            <select v-model="cellFilter" class="text-xs rounded px-2 py-1 form-field-select">
              <option value="">{{ $t('productConfig.allVendors') }}</option>
              <option v-for="m in localMfrList('cells')" :key="m" :value="m">
                {{ m }}
              </option>
            </select>
            <button
              class="text-[10px] px-2 py-1 rounded transition-colors tag-glow border-accent text-accent-secondary"
              @click="openAddModal('cell')"
            >
              {{ $t('productConfig.addCell') }}
            </button>
          </div>
        </div>
        <div class="grid grid-cols-3 gap-2">
          <div
            v-for="cell in localFiltered('cells', cellFilter)"
            :key="cell.id"
            class="border rounded-lg p-3 cursor-pointer transition-all group relative"
            :style="
              selectedCell === cell.id
                ? { borderColor: 'var(--color-accent-secondary)', backgroundColor: 'var(--color-accent-glow)' }
                : { borderColor: 'var(--color-border)', backgroundColor: 'var(--color-card-dark)' }
            "
            @click="selectedCell = cell.id"
          >
            <button
              class="absolute top-1 right-1 text-xs opacity-0 group-hover:opacity-100 transition-opacity text-muted"
              @click.stop="deleteItem('cells', cell.id)"
            >
              ×
            </button>
            <div class="flex justify-between items-start mb-1">
              <span class="text-xs font-bold">{{ cell.model }}</span>
              <span
                class="text-[10px] px-1.5 py-0.5 rounded"
                :style="
                  cell.status === 'mass-production'
                    ? { backgroundColor: 'var(--color-success-glow)', color: 'var(--color-success)' }
                    : { backgroundColor: 'var(--color-warning-glow)', color: 'var(--color-warning)' }
                "
              >
                {{
                  cell.status === 'mass-production'
                    ? $t('productConfig.massProduction')
                    : $t('productConfig.preResearch')
                }}
              </span>
            </div>
            <div class="text-[10px] mb-2 text-muted">
              {{ cell.mfr }}
            </div>
            <div class="grid grid-cols-2 gap-x-2 gap-y-0.5 text-[10px]">
              <div class="text-muted">{{ $t('productConfig.capacity') }}</div>
              <div class="text-secondary text-right">{{ cell.capacityAh }} Ah</div>
              <div class="text-muted">{{ $t('productConfig.nominalVoltage') }}</div>
              <div class="text-secondary text-right">{{ cell.voltageNominal }} V</div>
              <div class="text-muted">{{ $t('productConfig.voltageRange') }}</div>
              <div class="text-secondary text-right">{{ cell.voltageMin }}~{{ cell.voltageMax }}V</div>
              <div class="text-muted">{{ $t('productConfig.energy') }}</div>
              <div class="text-secondary text-right">{{ cell.ratedEnergyMWh }} MWh</div>
              <div class="text-muted">{{ $t('productConfig.energyDensity') }}</div>
              <div class="text-secondary text-right">{{ cell.energyDensity ?? '--' }} Wh/kg</div>
              <div class="text-muted">{{ $t('productConfig.cycleCalendar') }}</div>
              <div class="text-secondary text-right">{{ cell.cycleLife }}/{{ cell.calendarLife }}y</div>
            </div>
          </div>
        </div>
      </div>

      <div class="rounded-lg p-4 card-panel">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded flex items-center justify-center font-bold text-xs tag-warning">B</span>
          <div>
            <h3 class="font-bold text-sm">
              {{ $t('productConfig.containerLibrary') }}
              <span class="text-[10px] font-normal ml-1 text-muted">Container Library</span>
            </h3>
          </div>
          <div class="ml-auto flex gap-2">
            <select v-model="containerFilter" class="text-xs rounded px-2 py-1 form-field-select">
              <option value="">{{ $t('productConfig.allVendors') }}</option>
              <option v-for="m in localMfrList('containers')" :key="m" :value="m">
                {{ m }}
              </option>
            </select>
            <button
              class="text-[10px] px-2 py-1 rounded transition-colors tag-warning border-warning text-warning"
              @click="openAddModal('container')"
            >
              {{ $t('productConfig.addContainer') }}
            </button>
          </div>
        </div>
        <div class="grid grid-cols-3 gap-2">
          <div
            v-for="c in localFiltered('containers', containerFilter)"
            :key="c.id"
            class="border rounded-lg p-3 cursor-pointer transition-all group relative"
            :style="
              selectedContainer === c.id
                ? { borderColor: 'var(--color-warning)', backgroundColor: 'var(--color-warning-glow)' }
                : { borderColor: 'var(--color-border)', backgroundColor: 'var(--color-card-dark)' }
            "
            @click="selectedContainer = c.id"
          >
            <button
              class="absolute top-1 right-1 text-xs opacity-0 group-hover:opacity-100 transition-opacity text-muted"
              @click.stop="deleteItem('containers', c.id)"
            >
              ×
            </button>
            <div class="flex justify-between items-start mb-1">
              <span class="text-xs font-bold">{{ c.model }}</span>
              <span
                class="text-[10px] px-1.5 py-0.5 rounded"
                :style="
                  c.status === 'mass-production'
                    ? { backgroundColor: 'var(--color-success-glow)', color: 'var(--color-success)' }
                    : { backgroundColor: 'var(--color-warning-glow)', color: 'var(--color-warning)' }
                "
              >
                {{
                  c.status === 'mass-production' ? $t('productConfig.massProduction') : $t('productConfig.preResearch')
                }}
              </span>
            </div>
            <div class="text-[10px] mb-2 text-muted">
              {{ c.mfr }}
            </div>
            <div class="grid grid-cols-2 gap-x-2 gap-y-0.5 text-[10px]">
              <div class="text-muted">{{ $t('productConfig.energy') }}</div>
              <div class="text-secondary text-right">{{ c.ratedEnergyMWh }} MWh</div>
              <div class="text-muted">{{ $t('productConfig.power') }}</div>
              <div class="text-secondary text-right">{{ c.ratedPowerMW }} MW</div>
              <div class="text-muted">{{ $t('productConfig.cellModel') }}</div>
              <div class="text-secondary text-right">
                {{ c.cellModel }}
              </div>
              <div class="text-muted">{{ $t('productConfig.coolingMethod') }}</div>
              <div class="text-secondary text-right">
                {{ c.cooling }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="rounded-lg p-4 card-panel">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded flex items-center justify-center font-bold text-xs tag-glow text-accent">C</span>
          <div>
            <h3 class="font-bold text-sm">
              {{ $t('productConfig.pcsLibrary') }}
              <span class="text-[10px] font-normal ml-1 text-muted">PCS Library</span>
            </h3>
          </div>
          <div class="ml-auto flex gap-2">
            <select v-model="pcsFilter" class="text-xs rounded px-2 py-1 form-field-select">
              <option value="">{{ $t('productConfig.allVendors') }}</option>
              <option v-for="m in localMfrList('pcs')" :key="m" :value="m">
                {{ m }}
              </option>
            </select>
            <select v-model="pcsPowerFilter" class="text-xs rounded px-2 py-1 form-field-select">
              <option value="0">{{ $t('productConfig.allPower') }}</option>
              <option value="1.25">{{ $t('productConfig.power1_25') }}</option>
              <option value="1.725">{{ $t('productConfig.power1_725') }}</option>
              <option value="2.5">{{ $t('productConfig.power2_5') }}</option>
              <option value="3.45">{{ $t('productConfig.power3_45') }}</option>
            </select>
            <button
              class="text-[10px] px-2 py-1 rounded transition-colors tag-glow border-accent text-accent"
              @click="openAddModal('pcs')"
            >
              {{ $t('productConfig.addPCS') }}
            </button>
          </div>
        </div>
        <div class="grid grid-cols-3 gap-2">
          <div
            v-for="p in localFiltered('pcs', pcsFilter, pcsPowerFilter)"
            :key="p.id"
            class="border rounded-lg p-3 cursor-pointer transition-all group relative"
            :style="
              selectedPcs === p.id
                ? { borderColor: 'var(--color-accent)', backgroundColor: 'var(--color-accent-glow)' }
                : { borderColor: 'var(--color-border)', backgroundColor: 'var(--color-card-dark)' }
            "
            @click="selectedPcs = p.id"
          >
            <button
              class="absolute top-1 right-1 text-xs opacity-0 group-hover:opacity-100 transition-opacity text-muted"
              @click.stop="deleteItem('pcs', p.id)"
            >
              ×
            </button>
            <div class="flex justify-between items-start mb-1">
              <span class="text-xs font-bold">{{ p.model }}</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded tag-success">
                {{ $t('productConfig.massProduction') }}
              </span>
            </div>
            <div class="text-[10px] mb-2 text-muted">
              {{ p.mfr }}
            </div>
            <div class="grid grid-cols-2 gap-x-2 gap-y-0.5 text-[10px]">
              <div class="text-muted">{{ $t('productConfig.power') }}</div>
              <div class="text-secondary text-right">{{ p.ratedPowerMW }} MW</div>
              <div class="text-muted">{{ $t('productConfig.efficiency') }}</div>
              <div class="text-secondary text-right">{{ p.efficiency }}%</div>
              <div class="text-muted">{{ $t('productConfig.acVoltage') }}</div>
              <div class="text-secondary text-right">
                {{ p.acVoltage }}
              </div>
              <div class="text-muted">{{ $t('productConfig.coolingMethod') }}</div>
              <div class="text-secondary text-right">
                {{ p.cooling }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="rounded-lg p-4 card-panel">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded flex items-center justify-center font-bold text-xs tag-glow text-accent">D</span>
          <div>
            <h3 class="font-bold text-sm">
              {{ $t('productConfig.ciCabinet') }}
              <span class="text-[10px] font-normal ml-1 text-muted">Commercial & Industrial</span>
            </h3>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-2">
          <div
            v-for="c in cabinets"
            :key="c.id"
            class="border rounded-lg p-3 cursor-pointer transition-all group relative"
            :style="
              selectedCabinet === c.id
                ? { borderColor: 'var(--color-accent)', backgroundColor: 'var(--color-accent-glow)' }
                : { borderColor: 'var(--color-border)', backgroundColor: 'var(--color-card-dark)' }
            "
          >
            <div class="flex justify-between items-start mb-1">
              <span class="text-xs font-bold">{{ c.model }}</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded tag-success">
                {{
                  c.status === 'mass-production'
                    ? $t('productConfig.massProduction')
                    : $t('productConfig.inDevelopment')
                }}
              </span>
            </div>
            <div class="text-[10px] mb-2 text-muted">
              {{ c.mfr }}
            </div>
            <div class="grid grid-cols-2 gap-x-2 gap-y-0.5 text-[10px]">
              <div class="text-muted">{{ $t('productConfig.capacity') }}</div>
              <div class="text-secondary text-right">{{ c.ratedEnergykWh }} kWh</div>
              <div class="text-muted">{{ $t('productConfig.power') }}</div>
              <div class="text-secondary text-right">{{ c.ratedPowerkW }} kW</div>
              <div class="text-muted">{{ $t('productConfig.acVoltage') }}</div>
              <div class="text-secondary text-right">
                {{ c.acVoltage }}
              </div>
              <div class="text-muted">{{ $t('productConfig.coolingMethod') }}</div>
              <div class="text-secondary text-right">
                {{ c.cooling }}
              </div>
            </div>
            <div class="mt-2">
              <span class="text-[9px] px-1.5 py-0.5 rounded tag-glow text-accent">
                {{ c.scenario }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div class="rounded-lg p-4 card-panel">
        <div class="flex items-center gap-2 mb-3">
          <span
            class="w-6 h-6 rounded flex items-center justify-center font-bold text-xs tag-glow text-accent-secondary"
          >
            E
          </span>
          <div>
            <h3 class="font-bold text-sm">
              {{ $t('productConfig.scenarioTemplate') }}
              <span class="text-[10px] font-normal ml-1 text-muted">Scenario Templates</span>
            </h3>
          </div>
        </div>
        <div class="grid grid-cols-5 gap-2 mb-4">
          <div
            v-for="s in scenarios"
            :key="s.id"
            class="border rounded-lg p-3 cursor-pointer transition-all text-center"
            :style="
              selectedScenario === s.id
                ? { borderColor: 'var(--color-accent-secondary)', backgroundColor: 'var(--color-accent-glow)' }
                : { borderColor: 'var(--color-border)', backgroundColor: 'var(--color-card-dark)' }
            "
            @click="applyScenario(s)"
          >
            <div class="text-xs font-bold mb-1">
              {{ s.name }}
            </div>
            <div class="text-[10px] leading-relaxed text-muted">
              {{ s.description }}
            </div>
          </div>
        </div>
        <div v-if="configSummary" class="border-t pt-3 border-color-muted">
          <h4 class="text-xs font-bold mb-2 text-secondary">{{ $t('productConfig.currentSelection') }}</h4>
          <div class="grid grid-cols-3 gap-3 text-[10px]">
            <div class="rounded p-2 bg-card-dark">
              <span class="text-muted">{{ $t('productConfig.cellSelected') }}</span>
              <div class="font-mono mt-0.5">
                {{ configSummary.cell || $t('productConfig.notSelected') }}
              </div>
            </div>
            <div class="rounded p-2 bg-card-dark">
              <span class="text-muted">{{ $t('productConfig.containerSelected') }}</span>
              <div class="font-mono mt-0.5">
                {{ configSummary.container || $t('productConfig.notSelected') }}
              </div>
            </div>
            <div class="rounded p-2 bg-card-dark">
              <span class="text-muted">{{ $t('productConfig.pcsSelected') }}</span>
              <div class="font-mono mt-0.5">
                {{ configSummary.pcs || $t('productConfig.notSelected') }}
              </div>
            </div>
          </div>
          <div class="mt-3 flex justify-end">
            <button
              class="text-xs px-6 py-1.5 rounded shadow-md transition-all active:scale-95 bg-accent-secondary text-white"
              @click="applyToSimulation"
            >
              {{ $t('productConfig.applyToParams') }}
            </button>
          </div>
        </div>
      </div>

      <div
        v-if="showModal"
        class="fixed inset-0 z-50 flex items-center justify-center bg-overlay"
        @click.self="showModal = false"
      >
        <div class="rounded-xl p-5 w-[480px] max-h-[80vh] overflow-y-auto shadow-2xl card-panel">
          <h3 class="font-bold text-sm mb-4">
            {{ modalTitle }}
          </h3>
          <div class="space-y-3">
            <template v-if="modalType === 'cell'">
              <div class="grid grid-cols-2 gap-2 text-[10px]">
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.vendor') }}</label>
                  <input v-model="modalForm.mfr" class="w-full rounded px-2 py-1.5 text-xs form-field-input" />
                </div>
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.model') }}</label>
                  <input v-model="modalForm.model" class="w-full rounded px-2 py-1.5 text-xs form-field-input" />
                </div>
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.chemistry') }}</label>
                  <input v-model="modalForm.chemistry" class="w-full rounded px-2 py-1.5 text-xs form-field-input" />
                </div>
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.capacityAh') }}</label>
                  <input
                    v-model.number="modalForm.capacityAh"
                    type="number"
                    class="w-full rounded px-2 py-1.5 text-xs form-field-input"
                  />
                </div>
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.nominalVoltageV') }}</label>
                  <input
                    v-model.number="modalForm.voltageNominal"
                    type="number"
                    step="0.1"
                    class="w-full rounded px-2 py-1.5 text-xs form-field-input"
                  />
                </div>
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.cycleLife') }}</label>
                  <input
                    v-model.number="modalForm.cycleLife"
                    type="number"
                    class="w-full rounded px-2 py-1.5 text-xs form-field-input"
                  />
                </div>
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.dimensions') }}</label>
                  <input v-model="modalForm.dimensions" class="w-full rounded px-2 py-1.5 text-xs form-field-input" />
                </div>
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.weightKg') }}</label>
                  <input v-model="modalForm.weight" class="w-full rounded px-2 py-1.5 text-xs form-field-input" />
                </div>
              </div>
            </template>
            <template v-else-if="modalType === 'container'">
              <div class="grid grid-cols-2 gap-2 text-[10px]">
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.vendor') }}</label>
                  <input v-model="modalForm.mfr" class="w-full rounded px-2 py-1.5 text-xs card-input-dark" />
                </div>
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.model') }}</label>
                  <input v-model="modalForm.model" class="w-full rounded px-2 py-1.5 text-xs card-input-dark" />
                </div>
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.capacityAh') }}</label>
                  <input
                    v-model.number="modalForm.capacityAh"
                    type="number"
                    class="w-full rounded px-2 py-1.5 text-xs card-input-dark"
                  />
                </div>
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.nominalVoltageV') }}</label>
                  <input
                    v-model.number="modalForm.voltageNominal"
                    type="number"
                    step="0.1"
                    class="w-full rounded px-2 py-1.5 text-xs card-input-dark"
                  />
                </div>
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.voltageMaxV') }}</label>
                  <input
                    v-model.number="modalForm.voltageMax"
                    type="number"
                    step="0.05"
                    class="w-full rounded px-2 py-1.5 text-xs card-input-dark"
                  />
                </div>
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.voltageMinV') }}</label>
                  <input
                    v-model.number="modalForm.voltageMin"
                    type="number"
                    step="0.05"
                    class="w-full rounded px-2 py-1.5 text-xs card-input-dark"
                  />
                </div>
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.cycleLife') }}</label>
                  <input
                    v-model.number="modalForm.cycleLife"
                    type="number"
                    class="w-full rounded px-2 py-1.5 text-xs card-input-dark"
                  />
                </div>
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.calendarLifeY') }}</label>
                  <input
                    v-model.number="modalForm.calendarLife"
                    type="number"
                    class="w-full rounded px-2 py-1.5 text-xs card-input-dark"
                  />
                </div>
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.dimensions') }}</label>
                  <input v-model="modalForm.dimensions" class="w-full rounded px-2 py-1.5 text-xs card-input-dark" />
                </div>
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.weightKg') }}</label>
                  <input
                    v-model.number="modalForm.weight"
                    type="number"
                    step="0.01"
                    class="w-full rounded px-2 py-1.5 text-xs card-input-dark"
                  />
                </div>
              </div>
            </template>
            <template v-else-if="modalType === 'pcs'">
              <div class="grid grid-cols-2 gap-2 text-[10px]">
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.vendor') }}</label>
                  <input v-model="modalForm.mfr" class="w-full rounded px-2 py-1.5 text-xs card-input-dark" />
                </div>
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.model') }}</label>
                  <input v-model="modalForm.model" class="w-full rounded px-2 py-1.5 text-xs card-input-dark" />
                </div>
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.ratedPowerMW') }}</label>
                  <input
                    v-model.number="modalForm.ratedPowerMW"
                    type="number"
                    step="0.001"
                    class="w-full rounded px-2 py-1.5 text-xs card-input-dark"
                  />
                </div>
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.efficiencyPct') }}</label>
                  <input
                    v-model.number="modalForm.efficiency"
                    type="number"
                    step="0.1"
                    class="w-full rounded px-2 py-1.5 text-xs card-input-dark"
                  />
                </div>
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.acVoltage') }}</label>
                  <input v-model="modalForm.acVoltage" class="w-full rounded px-2 py-1.5 text-xs card-input-dark" />
                </div>
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.dcRange') }}</label>
                  <input
                    v-model="modalForm.dcVoltageRange"
                    class="w-full rounded px-2 py-1.5 text-xs card-input-dark"
                  />
                </div>
                <div>
                  <label class="block mb-0.5 text-muted">{{ $t('productConfig.coolingMethod') }}</label>
                  <input v-model="modalForm.cooling" class="w-full rounded px-2 py-1.5 text-xs card-input-dark" />
                </div>
              </div>
            </template>

            <div class="border-t pt-3 border-color-muted">
              <p class="text-[10px] mb-2 text-muted">{{ $t('productConfig.uploadSpec') }}</p>
              <div class="flex gap-2 text-[10px]">
                <input
                  ref="specInput"
                  type="file"
                  accept=".pdf,.csv,.xlsx,.xls"
                  class="hidden"
                  @change="onSpecUpload"
                />
                <button
                  class="px-3 py-1.5 rounded transition-colors bg-card-dark border-color-muted text-secondary"
                  @click="$refs.specInput.click()"
                >
                  {{ $t('productConfig.uploadSpecBtn') }}
                </button>
                <span v-if="specUploading" class="self-center text-accent-secondary">
                  {{ $t('productConfig.parsing') }}
                </span>
                <span v-if="specResult" class="self-center text-success">{{ specResult }}</span>
              </div>
            </div>
          </div>
          <div class="flex justify-end gap-2 mt-4 pt-3 border-t border-color-muted">
            <button class="text-xs px-3 py-1.5 text-muted" @click="showModal = false">{{ $t('common.cancel') }}</button>
            <button
              class="text-xs px-4 py-1.5 rounded transition-colors bg-accent-secondary text-white"
              @click="saveProduct"
            >
              {{ $t('common.save') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useProducts } from '../composables/useProducts'
import baseProducts from '../data/products.json'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
const emit = defineEmits(['applyConfig'])
const selectedCell = ref('')
const selectedContainer = ref('')
const selectedPcs = ref('')
const selectedCabinet = ref('')
const selectedScenario = ref(null)
const cellFilter = ref('')
const containerFilter = ref('')
const pcsFilter = ref('')
const pcsPowerFilter = ref('0')
// 从useProducts加载的数据
const {
  cells: cellsFromProducts,
  containers: containersFromProducts,
  pcs: pcsFromProducts,
  loadAll,
  createProduct,
  deleteProduct
} = useProducts()
// 本地数据（用于降级）
const localData = ref(JSON.parse(JSON.stringify(baseProducts)))
// API加载产品库
async function loadLibraryData() {
  try {
    await loadAll()
    // 如果数据库为空，初始化默认数据
    if (
      cellsFromProducts.value.length === 0 &&
      containersFromProducts.value.length === 0 &&
      pcsFromProducts.value.length === 0
    ) {
      await seedLibrary()
    }
  } catch (error) {
    console.error(t('productConfig.loadFailed'))
    // 降级使用本地数据
    localData.value = JSON.parse(JSON.stringify(baseProducts))
  }
}
// 初始化产品库
async function seedLibrary() {
  try {
    const response = await fetch('/api/products/seed', { method: 'POST' })
    const contentType = response.headers.get('content-type') || ''
    if (!contentType.includes('application/json')) {
      throw new Error(t('productConfig.seedFailed'))
    }
    const data = await response.json()
    if (data.success) {
      await loadLibraryData()
    }
  } catch (error) {
    console.error(t('productConfig.seedFailed'))
  }
}
function localMfrList(key) {
  // 优先使用useProducts数据，否则降级使用本地数据
  const data =
    key === 'cells'
      ? cellsFromProducts.value
      : key === 'containers'
        ? containersFromProducts.value
        : key === 'pcs'
          ? pcsFromProducts.value
          : []
  if (data.length > 0) {
    return [...new Set(data.map((c) => c.mfr).filter(Boolean))]
  }
  return [...new Set(localData.value[key]?.map((c) => c.mfr) || [])]
}
function localFiltered(key, mfrFilter, powerFilter) {
  // 优先使用useProducts数据
  let list = []
  if (key === 'cells' && cellsFromProducts.value.length > 0) {
    list = cellsFromProducts.value.map((c) => ({
      id: c.id,
      model: c.model,
      mfr: c.mfr,
      chemistry: c.chemistry,
      capacityAh: c.capacityAh,
      voltageNominal: c.voltageNominal,
      voltageMax: c.voltageMax,
      voltageMin: c.voltageMin,
      ratedEnergyMWh: c.ratedEnergyMWh,
      cycleLife: c.cycleLife,
      calendarLife: c.calendarLife,
      dimensions: c.dimensions,
      weight: c.weight,
      energyDensity: c.energyDensity,
      status: c.status,
      certifications: c.certifications,
      unitPrice: c.unitPrice,
      remarks: c.remarks
    }))
  } else if (key === 'containers' && containersFromProducts.value.length > 0) {
    list = containersFromProducts.value.map((c) => ({
      id: c.id,
      model: c.model,
      mfr: c.mfr,
      spec: c.spec,
      ratedEnergyMWh: c.ratedEnergyMWh,
      ratedPowerMW: c.ratedPowerMW,
      dcVoltageRange: c.dcVoltageRange,
      maxDcCurrent: c.maxDcCurrent,
      cellModel: c.cellModel,
      seriesCount: c.seriesCount,
      parallelCount: c.parallelCount,
      dimensions: c.dimensions,
      weight: c.weight,
      cooling: c.cooling,
      rte: c.rte,
      auxRun: c.auxRun,
      auxStandby: c.auxStandby,
      status: c.status,
      certifications: c.certifications,
      unitPrice: c.unitPrice,
      remarks: c.remarks
    }))
  } else if (key === 'pcs' && pcsFromProducts.value.length > 0) {
    list = pcsFromProducts.value.map((p) => ({
      id: p.id,
      model: p.model,
      mfr: p.mfr,
      ratedPowerMW: p.ratedPowerMW,
      efficiency: p.efficiency,
      acVoltage: p.acVoltage,
      dcVoltageRange: p.dcVoltageRange,
      maxDcCurrent: p.maxDcCurrent,
      frequencyRange: p.frequencyRange,
      dimensions: p.dimensions,
      weight: p.weight,
      cooling: p.cooling,
      auxRun: p.auxRun,
      auxStandby: p.auxStandby,
      status: p.status,
      certifications: p.certifications,
      unitPrice: p.unitPrice,
      remarks: p.remarks
    }))
  } else {
    list = localData.value[key] || []
  }
  if (mfrFilter) list = list.filter((c) => c.mfr === mfrFilter)
  if (key === 'pcs' && powerFilter && powerFilter !== '0') {
    list = list.filter((p) => p.ratedPowerMW === Number(powerFilter))
  }
  return list
}
async function deleteItem(key, id) {
  // 调用 Products API 删除（统一产品库）
  try {
    await deleteProduct(key, id)
    // 重新加载数据（useProducts 内部已自动 loadAll(true)）
    return
  } catch (error) {
    console.error(t('productConfig.deleteFailed'))
  }
  // 降级使用本地删除
  localData.value[key] = localData.value[key].filter((item) => item.id !== id)
  saveLocal()
}
const showModal = ref(false)
const modalType = ref('cell')
const modalForm = ref({})
const specInput = ref(null)
const specUploading = ref(false)
const specResult = ref('')
function openAddModal(type) {
  modalType.value = type
  showModal.value = true
  specResult.value = ''
  if (type === 'cell') {
    modalForm.value = {
      mfr: '',
      model: '',
      chemistry: 'LFP',
      capacityAh: '',
      voltageNominal: 3.2,
      voltageMax: '',
      voltageMin: '',
      cycleLife: '',
      calendarLife: 20,
      dimensions: '',
      weight: '',
      status: 'mass-production'
    }
  } else if (type === 'container') {
    modalForm.value = {
      mfr: '',
      model: '',
      ratedEnergyMWh: '',
      ratedPowerMW: '',
      cellModel: '',
      cooling: '',
      dimensions: '',
      weight: '',
      status: 'mass-production'
    }
  } else {
    modalForm.value = {
      mfr: '',
      model: '',
      ratedPowerMW: '',
      efficiency: '',
      acVoltage: '',
      dcVoltageRange: '',
      cooling: '',
      status: 'mass-production'
    }
  }
}
async function saveProduct() {
  const type = modalType.value
  const f = modalForm.value
  // 构建API请求数据
  const apiData = { ...f }
  // 单数转复数
  const category = type === 'cell' ? 'cells' : type === 'container' ? 'containers' : 'pcs'
  if (type === 'cell') {
    apiData.capacityAh = f.capacityAh
    apiData.voltageNominal = f.voltageNominal
    apiData.voltageMax = f.voltageMax || null
    apiData.voltageMin = f.voltageMin || null
    apiData.ratedEnergyMWh = parseFloat((((f.capacityAh || 0) * (f.voltageNominal || 3.2)) / 1e6).toFixed(6))
    apiData.cycleLife = f.cycleLife
    apiData.calendarLife = f.calendarLife || 20
    apiData.energyDensity =
      f.energyDensity || (f.weight > 0 ? Math.round((apiData.ratedEnergyMWh * 1e6) / f.weight) : null)
    apiData.dimensions = f.dimensions
    apiData.weight = f.weight ? parseFloat(f.weight) : null
  } else if (type === 'container') {
    apiData.ratedEnergyMWh = f.ratedEnergyMWh
    apiData.ratedPowerMW = f.ratedPowerMW
    apiData.cellModel = f.cellModel
    apiData.cooling = f.cooling
  } else if (type === 'pcs') {
    apiData.ratedPowerMW = f.ratedPowerMW
    apiData.efficiency = f.efficiency
    apiData.acVoltage = f.acVoltage
    apiData.dcVoltageRange = f.dcVoltageRange
    apiData.cooling = f.cooling
  }
  // 调用 Products API 保存（统一产品库，自动归属当前企业 + 刷新下拉框）
  try {
    await createProduct(category, apiData)
    showModal.value = false
    return
  } catch (error) {
    console.error(t('productConfig.saveFailed'))
    alert(t('productConfig.saveFailed') + ': ' + (error.message || t('productConfig.unknownError')))
  }
  // 降级使用本地保存
  const id = type + '-' + f.model?.toLowerCase().replace(/\s+/g, '-') + '-' + Date.now().toString(36)
  const item = { id, ...f }
  if (type === 'cell') {
    item.ratedEnergyMWh = parseFloat((((f.capacityAh || 0) * (f.voltageNominal || 3.2)) / 1e6).toFixed(6))
    item.voltageMax = f.voltageMax || null
    item.voltageMin = f.voltageMin || null
    item.voltageRange = f.voltageMin && f.voltageMax ? `${f.voltageMin}-${f.voltageMax}` : '2.5-3.65'
    item.calendarLife = f.calendarLife || 20
    item.energyDensity = f.weight > 0 ? Math.round((item.ratedEnergyMWh * 1e6) / f.weight) : null
    item.sohCurve = 'default'
  } else if (type === 'container') {
    item.type = '20ft Standard'
    item.cycleLife = 8000
  } else if (type === 'pcs') {
    item.ratedPowerKVA = (f.ratedPowerMW || 0) * 1040
    item.topology = '3-Level NPC'
    item.isolation = 'Transformerless'
  }
  if (!localData.value[type + 's']) {
    localData.value[type + 's'] = []
  }
  localData.value[type + 's'].push(item)
  saveLocal()
  showModal.value = false
}
async function onSpecUpload(e) {
  const file = e.target.files?.[0]
  if (!file) return
  specUploading.value = true
  specResult.value = ''
  try {
    const formData = new FormData()
    formData.append('file', file)
    const resp = await fetch('/api/upload/extract', { method: 'POST', body: formData })
    const contentType = resp.headers.get('content-type') || ''
    if (!contentType.includes('application/json')) {
      throw new Error(t('productConfig.extractFailed'))
    }
    const data = await resp.json()
    if (data.extracted) {
      const ext = data.extracted
      if (modalType.value === 'cell') {
        if (ext.capacity_ah || ext.total_mwh) modalForm.value.capacityAh = ext.capacity_ah || ext.total_mwh
        if (ext.cycle_life) modalForm.value.cycleLife = ext.cycle_life
      }
      specResult.value = t('productConfig.extractedFields', { count: Object.keys(ext).length })
    } else {
      specResult.value = t('productConfig.extractFailed')
    }
  } catch {
    specResult.value = t('productConfig.uploadFailed')
  }
  specUploading.value = false
}
function saveLocal() {
  if (typeof localStorage === 'undefined') return
  try {
    localStorage.setItem('soh-products', JSON.stringify(localData.value))
  } catch (e) {
    console.warn(e)
  }
}
try {
  if (typeof localStorage !== 'undefined') {
    const saved = localStorage.getItem('soh-products')
    if (saved) {
      const parsed = JSON.parse(saved)
      localData.value = { ...baseProducts, ...parsed }
    }
  }
} catch (e) {
  console.warn(e)
}
const mfrList = computed(() => ({
  cells: localMfrList('cells'),
  containers: localMfrList('containers'),
  pcs: localMfrList('pcs')
}))
const scenarios = baseProducts.scenarios
const cabinets = baseProducts.cabinets || []
const filteredCells = computed(() => localFiltered('cells', cellFilter.value))
const filteredContainers = computed(() => localFiltered('containers', containerFilter.value))
const filteredPcs = computed(() => localFiltered('pcs', pcsFilter.value, pcsPowerFilter.value))
const configSummary = computed(() => {
  const cell = localData.value.cells?.find((c) => c.id === selectedCell.value)
  const container = localData.value.containers?.find((c) => c.id === selectedContainer.value)
  const pcs = localData.value.pcs?.find((p) => p.id === selectedPcs.value)
  return {
    cell: cell ? `${cell.mfr} ${cell.model} (${cell.capacityAh}Ah)` : null,
    container: container ? `${container.mfr} ${container.model} (${container.ratedEnergyMWh}MWh)` : null,
    pcs: pcs ? `${pcs.mfr} ${pcs.model} (${pcs.ratedPowerMW}MW)` : null
  }
})
function applyScenario(s) {
  selectedScenario.value = s.id
  emit('applyConfig', {
    duration: s.duration,
    requiredEnergy: s.requiredEnergy,
    initContainerQty: s.initContainerQty,
    initPcsQty: s.initPcsQty,
    ratedEnergy: s.ratedEnergy,
    scenario: s.name
  })
}
function applyToSimulation() {
  // 优先使用useProducts数据
  let cell, container, pcs
  if (cellsFromProducts.value.length > 0) {
    cell = cellsFromProducts.value.find((c) => c.id === selectedCell.value)
  } else {
    cell = localData.value.cells?.find((c) => c.id === selectedCell.value)
  }
  if (containersFromProducts.value.length > 0) {
    container = containersFromProducts.value.find((c) => c.id === selectedContainer.value)
  } else {
    container = localData.value.containers?.find((c) => c.id === selectedContainer.value)
  }
  if (pcsFromProducts.value.length > 0) {
    pcs = pcsFromProducts.value.find((p) => p.id === selectedPcs.value)
  } else {
    pcs = localData.value.pcs?.find((p) => p.id === selectedPcs.value)
  }
  const payload = { cell, container, pcs }
  if (container) {
    payload.ratedEnergy = container.ratedEnergyMWh
    payload.acEfficiency = pcs ? pcs.efficiency : 97.03
  }
  emit('applyConfig', payload)
}
// 组件挂载时加载产品库数据
onMounted(() => {
  loadLibraryData()
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
</style>
