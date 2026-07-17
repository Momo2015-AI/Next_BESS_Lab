<template>
  <div class="h-full overflow-y-auto custom-scrollbar">
    <div class="max-w-6xl mx-auto space-y-4 py-2">
      <!-- A: Battery Cell Library -->
      <ProductLibraryPanel
        v-model:mfr-filter="cellFilter"
        badge="A"
        badge-class="tag-glow text-accent-secondary"
        :title="$t('productConfig.cellLibrary')"
        :subtitle="'Battery Cell Library'"
        :items="displayItems.cells"
        item-type="cell"
        :selected-id="selectedCell"
        :mfr-list="mfrList.cells"
        add-label="$t('productConfig.addCell')"
        add-btn-class="tag-glow border-accent text-accent-secondary"
        accent-color="var(--color-accent-secondary)"
        accent-glow="var(--color-accent-glow)"
        @select="selectedCell = $event"
        @delete="deleteItem('cells', $event)"
        @add="openAddModal('cell')"
      />

      <!-- B: Container Library -->
      <ProductLibraryPanel
        v-model:mfr-filter="containerFilter"
        badge="B"
        badge-class="tag-warning"
        :title="$t('productConfig.containerLibrary')"
        :subtitle="'Container Library'"
        :items="displayItems.containers"
        item-type="container"
        :selected-id="selectedContainer"
        :mfr-list="mfrList.containers"
        add-label="$t('productConfig.addContainer')"
        add-btn-class="tag-warning border-warning text-warning"
        accent-color="var(--color-warning)"
        accent-glow="var(--color-warning-glow)"
        @select="selectedContainer = $event"
        @delete="deleteItem('containers', $event)"
        @add="openAddModal('container')"
      />

      <!-- C: PCS Library -->
      <ProductLibraryPanel
        v-model:mfr-filter="pcsFilter"
        v-model:power-filter="pcsPowerFilter"
        badge="C"
        badge-class="tag-glow text-accent"
        :title="$t('productConfig.pcsLibrary')"
        :subtitle="'PCS Library'"
        :items="displayItems.pcs"
        item-type="pcs"
        :selected-id="selectedPcs"
        :mfr-list="mfrList.pcs"
        :show-power-filter="true"
        add-label="$t('productConfig.addPCS')"
        add-btn-class="tag-glow border-accent text-accent"
        accent-color="var(--color-accent)"
        accent-glow="var(--color-accent-glow)"
        @select="selectedPcs = $event"
        @delete="deleteItem('pcs', $event)"
        @add="openAddModal('pcs')"
      />

      <!-- D: CI Cabinet Library -->
      <ProductLibraryPanel
        badge="D"
        badge-class="tag-glow text-accent"
        :title="$t('productConfig.ciCabinet')"
        :subtitle="'Commercial & Industrial'"
        :items="cabinets"
        item-type="cabinet"
        :selected-id="selectedCabinet"
        :show-mfr-filter="false"
        :show-add-btn="false"
        :deletable="false"
        grid-class="grid-cols-4"
        accent-color="var(--color-accent)"
        accent-glow="var(--color-accent-glow)"
        @select="selectedCabinet = $event"
      />

      <!-- E: Scenario Templates -->
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
            <div class="text-xs font-bold mb-1">{{ s.name }}</div>
            <div class="text-[10px] leading-relaxed text-muted">{{ s.description }}</div>
          </div>
        </div>
        <div v-if="configSummary" class="border-t pt-3 border-color-muted">
          <h4 class="text-xs font-bold mb-2 text-secondary">{{ $t('productConfig.currentSelection') }}</h4>
          <div class="grid grid-cols-3 gap-3 text-[10px]">
            <div class="rounded p-2 bg-card-dark">
              <span class="text-muted">{{ $t('productConfig.cellSelected') }}</span>
              <div class="font-mono mt-0.5">{{ configSummary.cell || $t('productConfig.notSelected') }}</div>
            </div>
            <div class="rounded p-2 bg-card-dark">
              <span class="text-muted">{{ $t('productConfig.containerSelected') }}</span>
              <div class="font-mono mt-0.5">{{ configSummary.container || $t('productConfig.notSelected') }}</div>
            </div>
            <div class="rounded p-2 bg-card-dark">
              <span class="text-muted">{{ $t('productConfig.pcsSelected') }}</span>
              <div class="font-mono mt-0.5">{{ configSummary.pcs || $t('productConfig.notSelected') }}</div>
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

      <!-- Add Product Modal -->
      <AddProductModal
        :show="showModal"
        :type="modalType"
        :title="modalTitle"
        :uploading="specUploading"
        :spec-result="specResult"
        @close="showModal = false"
        @save="saveProduct"
        @spec-upload="onSpecUpload"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useProducts } from '../composables/useProducts'
import baseProducts from '../data/products.json'
import { useI18n } from 'vue-i18n'
import ProductLibraryPanel from './ProductLibraryPanel.vue'
import AddProductModal from './AddProductModal.vue'

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

const {
  cells: cellsFromProducts,
  containers: containersFromProducts,
  pcs: pcsFromProducts,
  loadAll,
  createProduct,
  deleteProduct
} = useProducts()
const localData = ref(JSON.parse(JSON.stringify(baseProducts)))

const displayItems = computed(() => ({
  cells: cellsFromProducts.value.length > 0 ? cellsFromProducts.value : localData.value.cells || [],
  containers: containersFromProducts.value.length > 0 ? containersFromProducts.value : localData.value.containers || [],
  pcs: pcsFromProducts.value.length > 0 ? pcsFromProducts.value : localData.value.pcs || []
}))

const mfrList = computed(() => ({
  cells: [...new Set(displayItems.value.cells.map((c) => c.mfr).filter(Boolean))],
  containers: [...new Set(displayItems.value.containers.map((c) => c.mfr).filter(Boolean))],
  pcs: [...new Set(displayItems.value.pcs.map((p) => p.mfr).filter(Boolean))]
}))

async function loadLibraryData() {
  try {
    await loadAll()
    if (
      cellsFromProducts.value.length === 0 &&
      containersFromProducts.value.length === 0 &&
      pcsFromProducts.value.length === 0
    ) {
      await seedLibrary()
    }
  } catch (error) {
    console.error(t('productConfig.loadFailed'))
    localData.value = JSON.parse(JSON.stringify(baseProducts))
  }
}

async function seedLibrary() {
  try {
    const response = await fetch('/api/products/seed', { method: 'POST' })
    const contentType = response.headers.get('content-type') || ''
    if (!contentType.includes('application/json')) throw new Error(t('productConfig.seedFailed'))
    const data = await response.json()
    if (data.success) await loadLibraryData()
  } catch (error) {
    console.error(t('productConfig.seedFailed'))
  }
}

async function deleteItem(key, id) {
  try {
    await deleteProduct(key, id)
    return
  } catch (error) {
    console.error(t('productConfig.deleteFailed'))
  }
  localData.value[key] = localData.value[key].filter((item) => item.id !== id)
  saveLocal()
}

const showModal = ref(false)
const modalType = ref('cell')
const specUploading = ref(false)
const specResult = ref('')

const modalTitle = computed(() => {
  if (modalType.value === 'cell') return t('productConfig.addCell')
  if (modalType.value === 'container') return t('productConfig.addContainer')
  return t('productConfig.addPCS')
})

function openAddModal(type) {
  modalType.value = type
  showModal.value = true
  specResult.value = ''
}

async function saveProduct(formData) {
  const type = modalType.value
  const category = type === 'cell' ? 'cells' : type === 'container' ? 'containers' : 'pcs'
  const apiData = { ...formData }

  if (type === 'cell') {
    apiData.ratedEnergyMWh = parseFloat(
      (((apiData.capacityAh || 0) * (apiData.voltageNominal || 3.2)) / 1e6).toFixed(6)
    )
    apiData.energyDensity =
      apiData.energyDensity || (apiData.weight > 0 ? Math.round((apiData.ratedEnergyMWh * 1e6) / apiData.weight) : null)
  }

  try {
    await createProduct(category, apiData)
    showModal.value = false
    return
  } catch (error) {
    console.error(t('productConfig.saveFailed'))
    alert(t('productConfig.saveFailed') + ': ' + (error.message || t('productConfig.unknownError')))
  }

  // Local fallback
  const id = type + '-' + formData.model?.toLowerCase().replace(/\s+/g, '-') + '-' + Date.now().toString(36)
  const item = { id, ...formData }
  if (!localData.value[category]) localData.value[category] = []
  localData.value[category].push(item)
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
    if (!contentType.includes('application/json')) throw new Error(t('productConfig.extractFailed'))
    const data = await resp.json()
    if (data.extracted) {
      specResult.value = t('productConfig.extractedFields', { count: Object.keys(data.extracted).length })
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

const scenarios = baseProducts.scenarios
const cabinets = baseProducts.cabinets || []

const configSummary = computed(() => {
  const cell = displayItems.value.cells.find((c) => c.id === selectedCell.value)
  const container = displayItems.value.containers.find((c) => c.id === selectedContainer.value)
  const pcs = displayItems.value.pcs.find((p) => p.id === selectedPcs.value)
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
  const cell = displayItems.value.cells.find((c) => c.id === selectedCell.value)
  const container = displayItems.value.containers.find((c) => c.id === selectedContainer.value)
  const pcs = displayItems.value.pcs.find((p) => p.id === selectedPcs.value)
  const payload = { cell, container, pcs }
  if (container) {
    payload.ratedEnergy = container.ratedEnergyMWh
    payload.acEfficiency = pcs ? pcs.efficiency : 97.03
  }
  emit('applyConfig', payload)
}

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
