<template>
  <div class="h-full flex flex-col gap-3">
    <div class="flex items-center justify-between">
      <h3 class="text-sm font-bold" style="color: var(--color-accent);">
        Efficiency Chain (10-Factor Model)
      </h3>
      <div class="flex gap-2">
        <button @click="setRfpMode" class="text-xs px-3 py-1 rounded transition-all"
          style="background: var(--color-card-dark); color: var(--color-text); border: 1px solid var(--color-border);">
          RFP Mode
        </button>
        <button @click="resetDefaults" class="text-xs px-3 py-1 rounded transition-all"
          style="background: var(--color-card-dark); color: var(--color-text-muted); border: 1px solid var(--color-border);">
          Reset
        </button>
        <button @click="applyFactors" class="text-xs px-4 py-1 rounded font-bold transition-all"
          :style="modified ? { background: 'linear-gradient(135deg, var(--color-success), var(--color-accent))', color: 'white' } : { background: 'var(--color-card-dark)', color: 'var(--color-text-muted)' }">
          Apply
        </button>
      </div>
    </div>

    <div class="rounded-lg p-3 flex items-center gap-4" style="background: var(--color-card-dark); border: 1px solid var(--color-border);">
      <div class="flex items-center gap-2">
        <span class="text-xs" style="color: var(--color-text-muted);">Preview SOH:</span>
        <input v-model.number="previewSoh" type="number" min="60" max="100" class="text-xs px-2 py-1 rounded"
          style="width:60px; background: var(--color-input-bg-dark); color: var(--color-text); border: 1px solid var(--color-input-border);" />
      </div>
      <div class="flex gap-4">
        <div class="text-xs"><span style="color: var(--color-text-muted);">Charge:</span> <span style="color: var(--color-accent); font-weight: bold;">{{ (previewResult.etaCharge * 100).toFixed(2) }}%</span></div>
        <div class="text-xs"><span style="color: var(--color-text-muted);">Discharge:</span> <span style="color: var(--color-accent); font-weight: bold;">{{ (previewResult.etaDischarge * 100).toFixed(2) }}%</span></div>
        <div class="text-xs"><span style="color: var(--color-text-muted);">RTE:</span> <span class="font-bold" :style="{ color: previewResult.rte >= 0.85 ? 'var(--color-success)' : previewResult.rte >= 0.80 ? '#f59e0b' : '#ef4444' }">{{ (previewResult.rte * 100).toFixed(2) }}%</span></div>
      </div>
    </div>

    <div class="overflow-auto flex-1" style="min-height: 0;">
      <table class="w-full text-xs" style="border-collapse: collapse;">
        <thead>
          <tr style="border-bottom: 2px solid var(--color-border);">
            <th class="text-left py-2 px-2" style="color: var(--color-text-muted);">#</th>
            <th class="text-left py-2 px-2" style="color: var(--color-text-muted);">Component</th>
            <th class="text-center py-2 px-2" style="color: var(--color-text-muted);">η Charge</th>
            <th class="text-center py-2 px-2" style="color: var(--color-text-muted);">η Discharge</th>
            <th class="text-center py-2 px-2" style="color: var(--color-text-muted);">SOH Link</th>
            <th class="text-center py-2 px-2" style="color: var(--color-text-muted);">Rate</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="f in factors" :key="f.id"
            class="transition-all"
            :style="{ borderBottom: '1px solid var(--color-border)', opacity: f.degrade ? 1 : 0.85 }">
            <td class="py-1.5 px-2" style="color: var(--color-text-muted);">{{ f.id }}</td>
            <td class="py-1.5 px-2" style="color: var(--color-text);">{{ f.name }}</td>
            <td class="py-1.5 px-2 text-center">
              <input v-model.number="f.eta_c" type="number" min="0.5" max="1" step="0.001"
                class="text-xs rounded text-center"
                style="width:72px; background: var(--color-input-bg-dark); color: var(--color-text); border: 1px solid var(--color-input-border); padding: 2px 4px;" />
            </td>
            <td class="py-1.5 px-2 text-center">
              <input v-model.number="f.eta_d" type="number" min="0.5" max="1" step="0.001"
                class="text-xs rounded text-center"
                style="width:72px; background: var(--color-input-bg-dark); color: var(--color-text); border: 1px solid var(--color-input-border); padding: 2px 4px;" />
            </td>
            <td class="py-1.5 px-2 text-center">
              <input v-model="f.degrade" type="checkbox"
                style="accent-color: var(--color-accent);" />
            </td>
            <td class="py-1.5 px-2 text-center">
              <input v-if="f.degrade" v-model.number="f.degrade_rate" type="number" min="0" max="1" step="0.01"
                class="text-xs rounded text-center"
                style="width:56px; background: var(--color-input-bg-dark); color: var(--color-text); border: 1px solid var(--color-input-border); padding: 2px 4px;" />
              <span v-else style="color: var(--color-text-muted);">-</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="text-xs" style="color: var(--color-text-muted);">
      SOH-linked factors degrade as: η(t) = η₀ × (1 − rate × (1 − SOH(t)/100))
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'

const factors = ref([])
const defaults = ref([])
const modified = ref(false)
const previewSoh = ref(100)

const previewResult = reactive({
  etaCharge: 1.0,
  etaDischarge: 1.0,
  rte: 1.0,
  chargeBreakdown: [],
  dischargeBreakdown: [],
})

watch(factors, () => { modified.value = true }, { deep: true })
watch(previewSoh, () => updatePreview())

onMounted(async () => {
  await loadFactors()
})

async function loadFactors() {
  try {
    const resp = await fetch('/api/efficiency/factors')
    const data = await resp.json()
    factors.value = data.factors.map(f => ({...f}))
    defaults.value = data.factors.map(f => ({...f}))
    modified.value = false
    updatePreview()
  } catch (e) {
    console.error('Failed to load efficiency factors:', e)
  }
}

function updatePreview() {
  const soh = Math.max(60, Math.min(100, previewSoh.value || 100))
  const result = computeChain(factors.value, soh)
  previewResult.etaCharge = result.etaCharge
  previewResult.etaDischarge = result.etaDischarge
  previewResult.rte = result.rte
}

function computeChain(fs, sohPct) {
  let etaC = 1, etaD = 1
  const sohRatio = sohPct / 100
  for (const f of fs) {
    let ec = f.eta_c, ed = f.eta_d
    if (f.degrade) {
      const degradation = 1 - f.degrade_rate * (1 - sohRatio)
      ec = Math.max(0, Math.min(1, f.eta_c * degradation))
      ed = Math.max(0, Math.min(1, f.eta_d * degradation))
    }
    etaC *= ec
    etaD *= ed
  }
  return { etaCharge: etaC, etaDischarge: etaD, rte: etaC * etaD }
}

async function applyFactors() {
  try {
    const payload = factors.value.map(f => ({
      eta_c: f.eta_c, eta_d: f.eta_d, degrade: f.degrade, degrade_rate: f.degrade_rate,
    }))
    await fetch('/api/efficiency/factors', {
      method: 'PUT', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ factors: payload }),
    })
    modified.value = false
  } catch (e) {
    console.error('Failed to apply factors:', e)
  }
}

function setRfpMode() {
  const f = factors.value.find(f => f.id === 10)
  if (f) {
    f.eta_d = 1.0
    modified.value = true
  }
}

async function resetDefaults() {
  await fetch('/api/efficiency/factors/reset', { method: 'POST' })
  await loadFactors()
}
</script>
