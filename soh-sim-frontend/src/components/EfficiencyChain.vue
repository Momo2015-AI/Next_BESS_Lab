<template>
  <div class="h-full flex flex-col gap-3">
    <div class="flex items-center justify-between">
      <h3 class="text-sm font-bold text-accent">Efficiency Chain (10-Factor Model)</h3>
      <div class="flex gap-2">
        <button
          class="text-xs px-3 py-1 rounded transition-all u-background-var-color-card-dark-color-var-color-text-border-1px-solid-var-color-border"
          @click="setRfpMode"
        >
          RFP Mode
        </button>
        <button
          class="text-xs px-3 py-1 rounded transition-all u-background-var-color-card-dark-color-var-color-text-muted-border-1px-solid-var-color-border"
          @click="resetDefaults"
        >
          Reset
        </button>
        <button
          class="text-xs px-4 py-1 rounded font-bold transition-all"
          :class="modified ? 'btn-modified' : 'btn-unmodified'"
          @click="applyFactors"
        >
          Apply
        </button>
      </div>
    </div>

    <div
      class="rounded-lg p-3 flex items-center gap-3 bg-card-dark border-card"
    >
      <span class="text-xs text-muted">SOH:</span>
      <input
        v-model.number="previewSoh"
        type="number"
        min="60"
        max="100"
        class="text-xs px-2 py-1 rounded u-width-56px-background-var-color-input-bg-dark-color-var-color-text-border-1px-solid-var-color-input-border"
      />
      <span class="text-xs text-muted">%</span>
    </div>

    <div
      class="rounded-lg p-3 flex flex-col gap-2.5 bg-card-dark border-card"
    >
      <div class="formula-row">
        <span class="formula-label">AC Side</span>
        <span class="formula-label text-accent">Charge:</span>
        <div class="formula-chain">
          <span
            v-for="f in acFactors"
            :key="'ac-' + f.id"
            class="formula-block"
            :class="{ linking: f.degrade }"
            :class="{ linking: f.degrade, 'border-degrade': f.degrade }"
          >
            <span class="block-name">{{ f.abbr }}</span>
            <span class="block-value">{{ (f._eta_c * 100).toFixed(2) }}</span>
          </span>
          <span class="formula-eq">{{ (acResult.charge * 100).toFixed(2) }}%</span>
        </div>
      </div>
      <div class="formula-row">
        <span class="formula-label" />
        <span class="formula-label text-muted">Disch:</span>
        <div class="formula-chain">
          <span
            v-for="f in acFactors"
            :key="'acd-' + f.id"
            class="formula-block"
            :class="{ linking: f.degrade, 'border-degrade': f.degrade }"
          >
            <span class="block-name">{{ f.abbr }}</span>
            <span class="block-value">{{ (f._eta_d * 100).toFixed(2) }}</span>
          </span>
          <span class="formula-eq">{{ (acResult.discharge * 100).toFixed(2) }}%</span>
        </div>
      </div>

      <div class="separator-line" />

      <div class="formula-row">
        <span class="formula-label">DC Side</span>
        <span class="formula-label text-accent">Charge:</span>
        <div class="formula-chain">
          <span
            v-for="f in dcFactors"
            :key="'dc-' + f.id"
            class="formula-block"
            :class="{ linking: f.degrade, 'border-degrade': f.degrade }"
          >
            <span class="block-name">{{ f.abbr }}</span>
            <span class="block-value">{{ (f._eta_c * 100).toFixed(2) }}</span>
          </span>
          <span class="formula-eq">{{ (dcResult.charge * 100).toFixed(2) }}%</span>
        </div>
      </div>
      <div class="formula-row">
        <span class="formula-label" />
        <span class="formula-label text-muted">Disch:</span>
        <div class="formula-chain">
          <span
            v-for="f in dcFactors"
            :key="'dcd-' + f.id"
            class="formula-block"
            :class="{ linking: f.degrade, 'border-degrade': f.degrade }"
          >
            <span class="block-name">{{ f.abbr }}</span>
            <span class="block-value">{{ (f._eta_d * 100).toFixed(2) }}</span>
          </span>
          <span class="formula-eq">{{ (dcResult.discharge * 100).toFixed(2) }}%</span>
        </div>
      </div>

      <div class="separator-line" />

      <div class="total-bar">
        <div class="total-item">
          <span class="total-label">η Charge</span>
          <span class="total-value text-accent">
            {{ (totalResult.charge * 100).toFixed(2) }}%
          </span>
          <span class="total-formula text-muted">
            = AC-c {{ (acResult.charge * 100).toFixed(1) }}% x DC-c {{ (dcResult.charge * 100).toFixed(1) }}%
          </span>
        </div>
        <div class="total-item">
          <span class="total-label">η Discharge</span>
          <span class="total-value text-muted">
            {{ (totalResult.discharge * 100).toFixed(2) }}%
          </span>
          <span class="total-formula text-muted">
            = AC-d {{ (acResult.discharge * 100).toFixed(1) }}% x DC-d {{ (dcResult.discharge * 100).toFixed(1) }}%
          </span>
        </div>
        <div class="total-item rte">
          <span class="total-label u-font-weight-bold">RTE</span>
          <span
            class="total-value u-font-weight-bold"
            :class="totalResult.rte >= 0.85 ? 'text-success' : totalResult.rte >= 0.8 ? 'text-warning' : 'text-danger'"
          >
            {{ (totalResult.rte * 100).toFixed(2) }}%
          </span>
          <span class="total-formula text-muted">
            = {{ (totalResult.charge * 100).toFixed(1) }}% x {{ (totalResult.discharge * 100).toFixed(1) }}%
          </span>
        </div>
      </div>
    </div>

    <div class="overflow-auto flex-1 u-min-height-0">
      <table class="w-full text-xs border-collapse">
        <thead>
          <tr class="section-header u-background-rgba-64-158-255-0-08">
            <th colspan="6" class="text-left py-1.5 px-2 u-color-var-color-accent-font-size-11px">
              AC Side (Grid → PCS)
            </th>
          </tr>
          <tr>class="u-border-bottom-2px-solid-var-color-border"
            <th class="text-left py-2 px-2 u-color-var-color-text-muted-width-22px">#</th>
            <th class="text-left py-2 px-2 text-muted">Component</th>
            <th class="text-center py-2 px-2 text-muted w-72">η Charge</th>
            <th class="text-center py-2 px-2 text-muted w-72">η Discharge</th>
            <th class="text-center py-2 px-2 u-color-var-color-text-muted-width-52px">SOH Link</th>
            <th class="text-center py-2 px-2 u-color-var-color-text-muted-width-56px">Rate</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="f in acFactors" :key="f.id">
            <tr class="border-b" :class="{ 'opacity-85': !f.degrade }">
              <td class="py-1.5 px-2 text-muted">
                {{ f.id }}
              </td>
              <td class="py-1.5 px-2 text-default">
                {{ f.name }}
              </td>
              <td class="py-1.5 px-2 text-center">
                <input v-model.number="f.eta_c" type="number" min="0.5" max="1" step="0.001" class="cell-input" />
              </td>
              <td class="py-1.5 px-2 text-center">
                <input v-model.number="f.eta_d" type="number" min="0.5" max="1" step="0.001" class="cell-input" />
              </td>
              <td class="py-1.5 px-2 text-center">
                <input v-model="f.degrade" type="checkbox" />class="u-accent-color-var-color-accent"
              </td>
              <td class="py-1.5 px-2 text-center">
                <input
                  v-if="f.degrade"
                  v-model.number="f.degrade_rate"
                  type="number"
                  min="0"
                  max="1"
                  step="0.01"
                  class="cell-input u-width-48px"
                />
                <span v-else>-</span>class="text-muted"
              </td>
            </tr>
          </template>
        </tbody>
        <thead>
          <tr class="section-header u-background-rgba-16-185-129-0-08">
            <th colspan="6" class="text-left py-1.5 px-2 u-color-var-color-success-font-size-11px">
              DC Side (PCS → Cell)
            </th>
          </tr>
          <tr>class="u-border-bottom-2px-solid-var-color-border"
            <th class="text-left py-2 px-2 u-color-var-color-text-muted-width-22px">#</th>
            <th class="text-left py-2 px-2 text-muted">Component</th>
            <th class="text-center py-2 px-2 text-muted w-72">η Charge</th>
            <th class="text-center py-2 px-2 text-muted w-72">η Discharge</th>
            <th class="text-center py-2 px-2 u-color-var-color-text-muted-width-52px">SOH Link</th>
            <th class="text-center py-2 px-2 u-color-var-color-text-muted-width-56px">Rate</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="f in dcFactors" :key="f.id">
            <tr class="border-b" :class="{ 'opacity-85': !f.degrade }">
              <td class="py-1.5 px-2 text-muted">
                {{ f.id }}
              </td>
              <td class="py-1.5 px-2 text-default">
                {{ f.name }}
              </td>
              <td class="py-1.5 px-2 text-center">
                <input v-model.number="f.eta_c" type="number" min="0.5" max="1" step="0.001" class="cell-input" />
              </td>
              <td class="py-1.5 px-2 text-center">
                <input v-model.number="f.eta_d" type="number" min="0.5" max="1" step="0.001" class="cell-input" />
              </td>
              <td class="py-1.5 px-2 text-center">
                <input v-model="f.degrade" type="checkbox" />class="u-accent-color-var-color-success"
              </td>
              <td class="py-1.5 px-2 text-center">
                <input
                  v-if="f.degrade"
                  v-model.number="f.degrade_rate"
                  type="number"
                  min="0"
                  max="1"
                  step="0.01"
                  class="cell-input u-width-48px"
                />
                <span v-else>-</span>class="text-muted"
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>

    <div class="text-xs text-muted">
      SOH-linked factors degrade as: η(t) = η₀ x (1 - rate x (1 - SOH(t)/100))
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { debounce } from 'lodash-es'
import api from '../services/api.js'

const ABBR_MAP = {
  1: 'HV',
  2: 'TR-H',
  3: 'MV',
  4: 'TR-L',
  5: 'LV',
  6: 'PCS',
  7: 'DC1',
  8: 'DC2',
  9: 'DCDC',
  10: 'Cell'
}

const factors = ref([])
const acFactors = computed(() => factors.value.filter((f) => f.id <= 6))
const dcFactors = computed(() => factors.value.filter((f) => f.id > 6))
const defaults = ref([])
const modified = ref(false)
const previewSoh = ref(100)

const acResult = reactive({ charge: 1, discharge: 1 })
const dcResult = reactive({ charge: 1, discharge: 1 })
const totalResult = reactive({ charge: 1, discharge: 1, rte: 1 })

watch(
  factors,
  debounce(() => {
    modified.value = true
    updatePreview()
  }, 300),
  { deep: true }
)
watch(previewSoh, () => updatePreview())

onMounted(async () => {
  await loadFactors()
})

async function loadFactors() {
  try {
    const data = await api.get('/api/efficiency/factors')
    factors.value = data.factors.map((f) => ({
      ...f,
      abbr: ABBR_MAP[f.id] || `F${f.id}`,
      _eta_c: f.eta_c,
      _eta_d: f.eta_d
    }))
    defaults.value = JSON.parse(JSON.stringify(factors.value))
    modified.value = false
    updatePreview()
  } catch (e) {
    console.error('Failed to load efficiency factors:', e)
  }
}

function calcSohDegrade(f, sohRatio) {
  const degradation = 1 - f.degrade_rate * (1 - sohRatio)
  const ec = Math.max(0, Math.min(1, f.eta_c * degradation))
  const ed = Math.max(0, Math.min(1, f.eta_d * degradation))
  return { ec, ed }
}

function computeSubtotal(fs, sohRatio) {
  let charge = 1,
    discharge = 1
  for (const f of fs) {
    const { ec, ed } = f.degrade ? calcSohDegrade(f, sohRatio) : { ec: f.eta_c, ed: f.eta_d }
    f._eta_c = ec
    f._eta_d = ed
    charge *= ec
    discharge *= ed
  }
  return { charge, discharge }
}

function updatePreview() {
  const sohPct = Math.max(60, Math.min(100, previewSoh.value || 100))
  const sohRatio = sohPct / 100

  const ac = computeSubtotal(acFactors.value, sohRatio)
  const dc = computeSubtotal(dcFactors.value, sohRatio)

  acResult.charge = ac.charge
  acResult.discharge = ac.discharge
  dcResult.charge = dc.charge
  dcResult.discharge = dc.discharge

  totalResult.charge = ac.charge * dc.charge
  totalResult.discharge = ac.discharge * dc.discharge
  totalResult.rte = totalResult.charge * totalResult.discharge
}

async function applyFactors() {
  try {
    const payload = factors.value.map((f) => ({
      eta_c: f.eta_c,
      eta_d: f.eta_d,
      degrade: f.degrade,
      degrade_rate: f.degrade_rate
    }))
    await api.put('/api/efficiency/factors', { factors: payload })
    modified.value = false
  } catch (e) {
    console.error('Failed to apply factors:', e)
  }
}

function setRfpMode() {
  const f = factors.value.find((f) => f.id === 10)
  if (f) {
    f.eta_d = 1.0
    modified.value = true
    updatePreview()
  }
}

async function resetDefaults() {
  await api.post('/api/efficiency/factors/reset')
  await loadFactors()
}
</script>

<style scoped>
h3 {
  margin: 0;
}

.cell-input {
  width: 64px;
  background: var(--color-input-bg-dark);
  color: var(--color-text);
  border: 1px solid var(--color-input-border);
  border-radius: 4px;
  padding: 2px 4px;
  font-size: 12px;
  text-align: center;
}

.formula-row {
  display: flex;
  align-items: center;
  gap: 6px;
}

.formula-label {
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  min-width: 40px;
  color: var(--color-text-muted);
  flex-shrink: 0;
}

.formula-chain {
  display: flex;
  align-items: center;
  gap: 0;
  flex-wrap: wrap;
}

.formula-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid var(--color-border);
  background: rgba(64, 158, 255, 0.06);
  min-width: 40px;
}

.formula-block.linking {
  background: rgba(245, 158, 11, 0.08);
}

.block-name {
  font-size: 9px;
  font-weight: 700;
  color: var(--color-text-muted);
  letter-spacing: 0.3px;
}

.block-value {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text);
}

.formula-eq {
  font-size: 11px;
  font-weight: 700;
  color: var(--color-accent);
  margin-left: 6px;
  flex-shrink: 0;
}

.separator-line {
  height: 1px;
  background: var(--color-border);
  margin: 4px 0;
}

.total-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  padding: 4px 0;
}

.total-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.total-item.rte {
  width: 100%;
}

.total-label {
  font-size: 11px;
  font-weight: 500;
  color: var(--color-text-muted);
  min-width: 70px;
}

.total-value {
  font-size: 13px;
  font-weight: 700;
  min-width: 52px;
}

.total-formula {
  font-size: 10px;
}
</style>
