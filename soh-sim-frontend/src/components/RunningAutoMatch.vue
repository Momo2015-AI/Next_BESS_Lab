<template>
  <FormCardSection number="06" :title="$t('runningConditions.section06')" :z-index="1">
    <template #extra>
      <label class="flex items-center gap-2 text-xs cursor-pointer ins-3">
        <input v-model="autoMatchEnabled" type="checkbox" class="accent-teal-500" />
        {{ $t('runningConditions.autoMatch') }}
      </label>
    </template>
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
  </FormCardSection>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useProducts } from '../composables/useProducts'
import { useDraftRef } from '../composables/useDraft'
import FormCardSection from './FormCardSection.vue'

const { t } = useI18n()

const {
  cells,
  packs,
  racks,
  clusters,
  containers,
  getPackByCellModel,
  getRackByPackModel,
  getClusterByRackModel,
  getContainerByCellModel,
  getContainerByClusterModel,
  matchConfigRule
} = useProducts()

const selectedCellModel = useDraftRef('rc-selected-cell-model', '').state
const selectedPackModel = useDraftRef('rc-selected-pack-model', '').state
const selectedRackModel = useDraftRef('rc-selected-rack-model', '').state
const selectedClusterModel = useDraftRef('rc-selected-cluster-model', '').state
const selectedContainerModel = useDraftRef('rc-selected-container-model', '').state

const matchedConfig = useDraftRef('rc-matched-config', null).state
const autoMatchEnabled = useDraftRef('rc-auto-match-enabled', true).state

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

defineExpose({
  reset() {
    selectedCellModel.value = ''
    selectedPackModel.value = ''
    selectedRackModel.value = ''
    selectedClusterModel.value = ''
    selectedContainerModel.value = ''
    matchedConfig.value = null
  }
})
</script>

<style scoped>
.ins-3 {
  color: var(--color-text-secondary);
}
.ins-4 {
  background: var(--color-accent-glow);
}
.ins-5 {
  color: var(--color-accent);
}
</style>
