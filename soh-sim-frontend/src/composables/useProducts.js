import { ref, computed } from 'vue'
import localProducts from '../data/products.json'

const cells = ref([])
const containers = ref([])
const pcs = ref([])
const cellPackMappings = ref([])
const loading = ref(false)
const loaded = ref(false)
const source = ref('')

const CAMEL_MAP = {
  capacity_ah: 'capacityAh',
  voltage_nominal: 'voltageNominal',
  voltage_range: 'voltageRange',
  energy_wh: 'energyWh',
  cycle_life: 'cycleLife',
  soh_curve: 'sohCurve',
  cell_model: 'cellModel',
  cell_config: 'cellConfig',
  rated_energy_mwh: 'ratedEnergyMWh',
  rated_power_mw: 'ratedPowerMW',
  rated_power_kva: 'ratedPowerKVA',
  ac_voltage: 'acVoltage',
  dc_voltage_range: 'dcVoltageRange',
}

function toCamel(obj) {
  const result = {}
  for (const [k, v] of Object.entries(obj)) {
    const key = CAMEL_MAP[k] || k
    result[key] = v
  }
  return result
}

async function fetchCategory(category) {
  try {
    const resp = await fetch(`/api/products/${category}`)
    if (!resp.ok) return []
    const data = await resp.json()
    return (data.items || []).map(toCamel)
  } catch {
    return []
  }
}

function loadFromLocalJson() {
  cells.value = localProducts.cells || []
  containers.value = localProducts.containers || []
  pcs.value = localProducts.pcs || []
  cellPackMappings.value = localProducts.cellPackMappings || []
  source.value = 'local'
  loaded.value = true
}

export function useProducts() {
  async function loadAll() {
    if (loaded.value) return
    loading.value = true
    try {
      const [c, ct, p] = await Promise.all([
        fetchCategory('cells'),
        fetchCategory('containers'),
        fetchCategory('pcs'),
      ])
      const totalFromApi = c.length + ct.length + p.length
      if (totalFromApi === 0) {
        try {
          await fetch('/api/products/seed', { method: 'POST' })
          const [c2, ct2, p2] = await Promise.all([
            fetchCategory('cells'),
            fetchCategory('containers'),
            fetchCategory('pcs'),
          ])
          if (c2.length + ct2.length + p2.length > 0) {
            cells.value = c2
            containers.value = ct2
            pcs.value = p2
            source.value = 'api'
            loaded.value = true
            return
          }
        } catch { /* seed failed, fallback below */ }
        loadFromLocalJson()
        return
      }
      cells.value = c
      containers.value = ct
      pcs.value = p
      source.value = 'api'
      loaded.value = true
    } catch (e) {
      console.error('加载产品库失败，使用本地数据:', e)
      loadFromLocalJson()
    } finally {
      loading.value = false
    }
  }

  function getCellById(id) {
    return cells.value.find(c => c.id === id)
  }

  function getContainerById(id) {
    return containers.value.find(c => c.id === id)
  }

  function getPcsById(id) {
    return pcs.value.find(p => p.id === id)
  }

  const cellMfrs = computed(() => [...new Set(cells.value.map(c => c.mfr).filter(Boolean))])
  const containerMfrs = computed(() => [...new Set(containers.value.map(c => c.mfr).filter(Boolean))])
  const pcsMfrs = computed(() => [...new Set(pcs.value.map(p => p.mfr).filter(Boolean))])

  return {
    cells, containers, pcs, cellPackMappings,
    loading, loaded, source,
    loadAll,
    getCellById, getContainerById, getPcsById,
    cellMfrs, containerMfrs, pcsMfrs,
  }
}
