<template>
  <div class="h-full flex flex-col gap-3">
    <div class="flex items-center justify-between">
      <h3 class="text-sm font-bold text-accent">Degradation Model Configuration</h3>
      <div class="flex gap-2">
        <button
          class="text-xs px-3 py-1 rounded transition-all"
          class="u-background-var-color-card-dark-color-var-color-text-muted-border-1px-solid-var-color-border"
          @click="resetAll"
        >
          Reset
        </button>
        <button
          class="text-xs px-4 py-1 rounded font-bold transition-all"
          :style="dirty ? { background: 'linear-gradient(135deg, var(--color-success), var(--color-accent))', color: 'white' } : { background: 'var(--color-card-dark)', color: 'var(--color-text-muted)' }"
          @click="applyConfig"
        >
          Apply
        </button>
      </div>
    </div>

    <div class="rounded-lg p-3 bg-card-dark border-card">
      <label class="label-text text-xs u-display-block-margin-bottom-4px">Degradation Model</label>
      <div class="flex gap-2">
        <button
          v-for="m in models"
          :key="m.value"
          class="text-xs px-3 py-1 rounded transition-all"
          :style="model === m.value ? { background: 'var(--color-accent)', color: 'white' } : { background: 'var(--color-bg)', color: 'var(--color-text)', border: '1px solid var(--color-border)' }"
          @click="model = m.value"
        >
          {{ m.label }}
        </button>
      </div>
    </div>

    <template v-if="model === 'arrhenius'">
      <div class="rounded-lg p-3 bg-card-dark border-card">
        <div class="flex items-center gap-3 mb-2">
          <label class="label-text text-xs">Correction Factor:</label>
          <input
            v-model.number="correctionFactor"
            type="number"
            min="0.1"
            max="5"
            step="0.1"
            class="form-field-input text-xs px-2 py-1 rounded"
 class="u-width-70px"
          />
        </div>
        <p class="text-xs u-color-var-color-text-muted-opacity-0-6">
          Multiplier applied to degradation rate. Use 1.0 for standard Arrhenius prediction.
        </p>
      </div>
    </template>

    <template v-if="model === 'gb36276'">
      <div class="rounded-lg p-3 bg-card-dark border-card">
        <div class="flex items-center justify-between mb-2">
          <label class="label-text text-xs font-bold">GB/T 36276 Standard Curves</label>
          <div class="flex gap-2">
            <label
              class="text-xs px-2 py-1 rounded cursor-pointer transition-all"
 class="u-background-var-color-bg-color-var-color-text-border-1px-solid-var-color-border"
            >
              Import CSV
              <input type="file" accept=".csv" @change="handleCsvImport" />class="u-display-none"
            </label>
            <button
              class="text-xs px-2 py-1 rounded"
 class="u-background-var-color-bg-color-var-color-text-muted-border-1px-solid-var-color-border"
              @click="resetCurves"
            >
              Reset
            </button>
          </div>
        </div>
        <div class="overflow-auto u-max-height-180px">
          <table class="w-full text-xs border-collapse">
            <thead>
              <tr>class="border-b"
                <th class="text-left py-1 px-2 text-muted">Curve</th>
                <th class="text-center py-1 px-2 text-muted">P-Rate</th>
                <th class="text-center py-1 px-2 text-muted">T [deg C]</th>
                <th class="text-center py-1 px-2 text-muted">Data Points</th>
                <th class="text-center py-1 px-2 text-muted">SOH @ 8000 cyc</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(c, i) in gbCurves" :key="i">class="border-b"
                <td class="py-1 px-2 text-default">
                  {{ c.label }}
                </td>
                <td class="text-center py-1 px-2 text-default">{{ c.p_rate }}P</td>
                <td class="text-center py-1 px-2 text-default">{{ c.temperature }}°C</td>
                <td class="text-center py-1 px-2 text-muted">
                  {{ (c.data || []).length }}
                </td>
                <td
                  class="text-center py-1 px-2 font-bold"
                  :style="{
                    color:
                      getSohAt8000(c) >= 80
                        ? 'var(--color-success)'
                        : getSohAt8000(c) >= 60
                          ? 'var(--color-warning)'
                          : 'var(--color-danger)'
                  }"
                >
                  {{ getSohAt8000(c).toFixed(1) }}%
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

    <div class="rounded-lg p-3 bg-card-dark border-card">
      <label class="label-text text-xs font-bold block mb-2">Environmental Acceleration</label>
      <div class="flex flex-col gap-2">
        <div class="flex items-center justify-between">
          <span class="text-xs text-default">Temperature (Arrhenius)</span>
          <label class="text-xs flex items-center gap-2">
            <input v-model="env.accelerate_temperature" type="checkbox" @change="markDirty" />
            <span>Enable</span>class="text-muted"
          </label>
        </div>
        <div v-if="env.accelerate_temperature" class="flex items-center gap-2 ml-4">
          <span class="text-xs text-muted">Ea [J/mol]</span>
          <input
            v-model.number="env.activation_energy"
            type="number"
            min="10000"
            max="50000"
            step="1000"
            class="form-field-input text-xs px-2 py-1 rounded"
 class="u-width-80px"
            @change="markDirty"
          />
          <span class="text-xs text-muted">Ref T [deg C]</span>
          <input
            v-model.number="env.ref_temperature"
            type="number"
            min="10"
            max="40"
            class="form-field-input text-xs px-2 py-1 rounded"
 class="w-50"
            @change="markDirty"
          />
        </div>

        <div class="flex items-center justify-between">
          <span class="text-xs text-default">Dust Factor</span>
          <label class="text-xs flex items-center gap-2">
            <input v-model="env.accelerate_dust" type="checkbox" @change="markDirty" />
            <span>Enable</span>class="text-muted"
          </label>
        </div>
        <div v-if="env.accelerate_dust" class="flex items-center gap-2 ml-4">
          <span class="text-xs text-muted">Factor</span>
          <input
            v-model.number="env.dust_factor"
            type="number"
            min="1.0"
            max="2.0"
            step="0.01"
            class="form-field-input text-xs px-2 py-1 rounded"
 class="u-width-60px"
            @change="markDirty"
          />
        </div>

        <div class="flex items-center justify-between">
          <span class="text-xs text-default">Humidity (Peck)</span>
          <label class="text-xs flex items-center gap-2">
            <input v-model="env.accelerate_humidity" type="checkbox" @change="markDirty" />
            <span>Enable</span>class="text-muted"
          </label>
        </div>
        <div v-if="env.accelerate_humidity" class="flex items-center gap-2 ml-4">
          <span class="text-xs text-muted">Ref RH%</span>
          <input
            v-model.number="env.ref_humidity"
            type="number"
            min="10"
            max="90"
            class="form-field-input text-xs px-2 py-1 rounded"
 class="w-50"
            @change="markDirty"
          />
          <span class="text-xs text-muted">Field RH%</span>
          <input
            v-model.number="env.field_humidity"
            type="number"
            min="10"
            max="100"
            class="form-field-input text-xs px-2 py-1 rounded"
 class="w-50"
            @change="markDirty"
          />
          <span class="text-xs text-muted">n</span>
          <input
            v-model.number="env.humidity_exponent"
            type="number"
            min="1"
            max="5"
            step="0.5"
            class="form-field-input text-xs px-2 py-1 rounded"
 class="u-width-40px"
            @change="markDirty"
          />
        </div>
      </div>
    </div>

    <div class="rounded-lg p-3 bg-card-dark border-card">
      <div class="flex items-center gap-3 mb-2">
        <span class="text-xs text-muted">Preview T:</span>
        <input
          v-model.number="previewTemp"
          type="number"
          min="15"
          max="60"
          class="form-field-input text-xs px-2 py-1 rounded"
 class="w-50"
        />
        <span class="text-xs text-muted">DOD:</span>
        <input
          v-model.number="previewDod"
          type="number"
          min="50"
          max="100"
          class="form-field-input text-xs px-2 py-1 rounded"
 class="w-50"
        />
        <span class="text-xs text-muted">Cyc/day:</span>
        <input
          v-model.number="previewCyc"
          type="number"
          min="0.5"
          max="3"
          step="0.5"
          class="form-field-input text-xs px-2 py-1 rounded"
 class="u-width-45px"
        />
        <button
          class="text-xs px-3 py-1 rounded"
 class="u-background-var-color-bg-color-var-color-text-border-1px-solid-var-color-border"
          @click="runPreview"
        >
          Refresh
        </button>
      </div>

      <div class="overflow-auto u-max-height-160px">
        <table v-if="previewData" class="w-full text-xs border-collapse">
          <thead>
            <tr>class="border-b"
              <th class="text-left py-1 px-2 text-muted">Year</th>
              <th class="text-center py-1 px-2 text-muted">SOH</th>
              <th class="text-center py-1 px-2 text-muted">RTE</th>
              <th class="text-center py-1 px-2 text-muted">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(s, y) in yearLabels" :key="y">class="border-b"
              <td class="py-1 px-2 text-default">Year {{ y }}</td>
              <td
                class="text-center py-1 px-2 font-bold"
                :style="{
                  color: s >= 80 ? 'var(--color-success)' : s >= 60 ? 'var(--color-warning)' : 'var(--color-danger)'
                }"
              >
                {{ s.toFixed(2) }}%
              </td>
              <td class="text-center py-1 px-2 text-muted">
                {{ (previewRte[y] || 0).toFixed(2) }}%
              </td>
              <td class="text-center py-1 px-2">
                <span
                  v-if="s >= 85"
                  class="text-xs px-1 rounded"
 class="u-background-rgba-16-185-129-0-15-color-var-color-success"
                >
                  Healthy
                </span>
                <span
                  v-else-if="s >= 70"
                  class="text-xs px-1 rounded"
 class="u-background-rgba-245-158-11-0-15-color-var-color-warning"
                >
                  Warning
                </span>
                <span
                  v-else
                  class="text-xs px-1 rounded"
 class="u-background-rgba-239-68-68-0-15-color-var-color-danger"
                >
                  Critical
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import { debounce } from 'lodash-es'
import { useBessStore } from '../stores/bess.js'
import { NUM_YEARS } from '../constants.js'

const store = useBessStore()

const models = [
  { label: 'Arrhenius', value: 'arrhenius' },
  { label: 'GB/T 36276', value: 'gb36276' }
]

const model = ref('arrhenius')
const correctionFactor = ref(1.0)
const env = reactive({ ...store.environmental })
const gbCurves = ref([])
const dirty = ref(false)

const previewTemp = ref(25)
const previewDod = ref(80)
const previewCyc = ref(1)
const previewData = ref(null)
const previewRte = ref([])

const yearLabels = computed(() => {
  return (previewData.value || []).map((s, y) => (y === 0 ? 100 : previewData.value[y] || 0))
})

function markDirty() {
  dirty.value = true
}

async function resetCurves() {
  await store.resetGb36276Curves()
  gbCurves.value = [...store.gb36276Curves]
  markDirty()
}

async function handleCsvImport(e) {
  const file = e.target.files[0]
  if (!file) return
  const text = await file.text()
  const lines = text.trim().split('\n')
  const header = lines[0].split(',')
  if (header.length < 2 || header[0].toLowerCase() !== 'cycles' || isNaN(+header[1])) {
    alert('Invalid CSV format. Header must be: cycles,soh1,soh2,soh3,...')
    return
  }
  const sohNames = header.slice(1)
  const data = []
  for (const h of sohNames) {
    const parts = h.split('_')
    const pRate = parseFloat(parts[1]) || 0.125
    const temp = parseInt(parts[3]) || 25
    data.push({ label: h.replace(/_/g, ' '), p_rate: pRate, temperature: temp, data: [] })
  }
  for (let i = 1; i < lines.length; i++) {
    const vals = lines[i].split(',')
    const cycles = parseInt(vals[0])
    for (let j = 0; j < data.length; j++) {
      const soh = parseFloat(vals[j + 1])
      if (!isNaN(soh)) {
        data[j].data.push({ cycles, soh })
      }
    }
  }
  gbCurves.value = data
  markDirty()
}

async function runPreview() {
  const params = {
    model: model.value,
    temperature: previewTemp.value,
    cyclesPerDay: previewCyc.value,
    dod: previewDod.value,
    cRate: 0.125,
    correctionFactor: correctionFactor.value,
    environmental: { ...env },
    gb36276Curves: gbCurves.value
  }
  try {
    const result = await store.previewDegradation(params)
    previewData.value = result.soh
    previewRte.value = result.rte
  } catch (e) {
    console.error('Preview failed:', e)
  }
}

function getSohAt8000(curve) {
  if (!curve.data || curve.data.length === 0) return 100
  const sorted = [...curve.data].sort((a, b) => a.cycles - b.cycles)
  for (const d of sorted) {
    if (d.cycles >= 8000) return d.soh
  }
  return sorted[sorted.length - 1].soh
}

async function resetAll() {
  model.value = 'arrhenius'
  correctionFactor.value = 1.0
  Object.assign(env, store.environmental)
  await store.resetGb36276Curves()
  gbCurves.value = [...store.gb36276Curves]
  dirty.value = false
}

async function applyConfig() {
  await store.updateEnvironmental({ ...env })
  if (model.value === 'gb36276' && gbCurves.value.length > 0) {
    await store.updateGb36276Curves(gbCurves.value)
  }
  store.degradationModel = model.value
  dirty.value = false
}

watch(() => model.value, markDirty)
watch(() => correctionFactor.value, markDirty)

const debouncedEnvUpdate = debounce(() => {
  /* env changed */
}, 300)
watch(env, debouncedEnvUpdate, { deep: true })

onMounted(async () => {
  await store.loadDegradationConfig()
  model.value = store.degradationModel
  Object.assign(env, store.environmental)
  gbCurves.value = [...store.gb36276Curves]
  await runPreview()
})
</script>

<style scoped>
h3 {
  margin: 0;
}
</style>
