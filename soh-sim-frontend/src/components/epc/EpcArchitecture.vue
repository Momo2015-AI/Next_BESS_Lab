<template>
  <div class="epc-panel space-y-4">
    <div class="panel-card">
      <h3 class="panel-title">{{ $t('epcArch.title') }}</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcArch.systemPower') }}</label>
          <input v-model.number="archForm.total_power_mw" type="number" class="form-field-input" placeholder="1400" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcArch.systemEnergy') }}</label>
          <input v-model.number="archForm.total_energy_mwh" type="number" class="form-field-input" placeholder="8400" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcArch.archType') }}</label>
          <select v-model="archForm.architecture_type" class="form-field-select">
            <option value="central">{{ $t('epcArch.centralized') }}</option>
            <option value="string">{{ $t('epcArch.string') }}</option>
            <option value="hybrid">{{ $t('epcArch.hybrid') }}</option>
          </select>
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcArch.couplingType') }}</label>
          <select v-model="archForm.coupling_type" class="form-field-select">
            <option value="AC">{{ $t('epcArch.acCoupling') }}</option>
            <option value="DC">{{ $t('epcArch.dcCoupling') }}</option>
            <option value="hybrid">{{ $t('epcArch.hybridCoupling') }}</option>
          </select>
        </div>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcArch.cellVoltage') }}</label>
          <input
            v-model.number="archForm.cell_voltage"
            type="number"
            step="0.1"
            class="form-field-input"
            placeholder="3.2"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcArch.cellCapacity') }}</label>
          <input v-model.number="archForm.cell_capacity" type="number" class="form-field-input" placeholder="280" />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcArch.pcsPower') }}</label>
          <input
            v-model.number="archForm.pcs_power_mw"
            type="number"
            step="0.01"
            class="form-field-input"
            placeholder="3.45"
          />
        </div>
        <div>
          <label class="block text-xs mb-1 field-label">{{ $t('epcArch.pcsMaxDcVoltage') }}</label>
          <input
            v-model.number="archForm.pcs_max_dc_voltage"
            type="number"
            class="form-field-input"
            placeholder="1500"
          />
        </div>
      </div>
      <button :disabled="loading" class="btn-primary" @click="designArchitecture">
        {{ loading ? $t('epcArch.calculating') : $t('epcArch.designArch') }}
      </button>

      <div v-if="archResult" class="mt-6 space-y-4">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
          <div v-for="item in archResult.topology_data.levels" :key="item.name" class="metric-card">
            <div class="metric-value">{{ item.count }}</div>
            <div class="metric-label">{{ item.name }} ({{ item.unit }})</div>
          </div>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
          <div class="metric-card">
            <div class="metric-value">{{ archResult.pcs_count }}</div>
            <div class="metric-label">{{ $t('epcArch.pcsTotal') }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ archResult.dc_bus_voltage }}V</div>
            <div class="metric-label">{{ $t('epcArch.dcBusVoltage') }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ archResult.total_containers }}</div>
            <div class="metric-label">{{ $t('epcArch.totalContainers') }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ archResult.stage_count }}</div>
            <div class="metric-label">{{ $t('epcArch.stageCount') }}</div>
          </div>
          <div class="metric-card">
            <div class="metric-value">{{ archResult.duration_hours }}h</div>
            <div class="metric-label">{{ $t('epcArch.durationHours') }}</div>
          </div>
        </div>
        <div v-if="archResult.stages" class="mt-4">
          <h4 class="text-sm font-bold mb-2 section-title">{{ $t('epcArch.phases') }}</h4>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div v-for="stage in archResult.stages" :key="stage.stage" class="stage-card">
              <div class="font-bold text-sm stage-title">{{ stage.stage }}{{ $t('epcArch.phaseSuffix') }}</div>
              <div class="text-xs tx-muted-dark">{{ stage.power_mw }}MW / {{ stage.energy_mwh }}MWh</div>
              <div class="text-xs tx-muted">{{ stage.estimated_date }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useEpcModules } from '../../composables/useEpcModules.js'

const { loading, archForm, archResult, designArchitecture } = useEpcModules()
</script>
