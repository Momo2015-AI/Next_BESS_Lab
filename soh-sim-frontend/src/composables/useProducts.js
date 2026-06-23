import { ref, computed } from 'vue'
import localProducts from '../data/products.json'

const cells = ref([])
const packs = ref([])
const racks = ref([])
const clusters = ref([])
const containers = ref([])
const pcs = ref([])
const configRules = ref([])
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
  cells_per_pack: 'cellsPerPack',
  series_count: 'seriesCount',
  parallel_count: 'parallelCount',
  nominal_voltage: 'nominalVoltage',
  nominal_capacity_ah: 'nominalCapacityAh',
  nominal_energy_kwh: 'nominalEnergyKwh',
  max_charge_current: 'maxChargeCurrent',
  max_discharge_current: 'maxDischargeCurrent',
  bms_type: 'bmsType',
  pack_model: 'packModel',
  packs_per_rack: 'packsPerRack',
  cooling: 'cooling',
  racks_per_cluster: 'racksPerCluster',
  nominal_energy_mwh: 'nominalEnergyMwh',
  nominal_power_mw: 'nominalPowerMw',
  bmu_type: 'bmuType',
  cluster_model: 'clusterModel',
  clusters_per_container: 'clustersPerContainer',
  pack_nominal_voltage: 'packNominalVoltage',
  pack_nominal_capacity_ah: 'packNominalCapacityAh',
  pack_nominal_energy_kwh: 'packNominalEnergyKwh',
  rack_nominal_voltage: 'rackNominalVoltage',
  rack_nominal_capacity_ah: 'rackNominalCapacityAh',
  rack_nominal_energy_kwh: 'rackNominalEnergyKwh',
  cluster_nominal_voltage: 'clusterNominalVoltage',
  cluster_nominal_capacity_ah: 'clusterNominalCapacityAh',
  cluster_nominal_energy_mwh: 'clusterNominalEnergyMwh',
  cluster_nominal_power_mw: 'clusterNominalPowerMw',
  container_nominal_energy_mwh: 'containerNominalEnergyMwh',
  container_nominal_power_mw: 'containerNominalPowerMw',
  is_default: 'isDefault',
  series_per_pack: 'seriesPerPack',
  parallel_per_pack: 'parallelPerPack',
  series_per_rack: 'seriesPerRack',
  parallel_per_rack: 'parallelPerRack',
  series_per_cluster: 'seriesPerCluster',
  parallel_per_cluster: 'parallelPerCluster',
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

async function fetchConfigRules() {
  try {
    const resp = await fetch('/api/products/config-rules')
    if (!resp.ok) return []
    const data = await resp.json()
    return (data.items || []).map(toCamel)
  } catch {
    return []
  }
}

function loadFromLocalJson() {
  cells.value = localProducts.cells || []
  packs.value = localProducts.packs || []
  racks.value = localProducts.racks || []
  clusters.value = localProducts.clusters || []
  containers.value = localProducts.containers || []
  pcs.value = localProducts.pcs || []
  configRules.value = localProducts.config_rules || []
  source.value = 'local'
  loaded.value = true
}

export function useProducts() {
  async function loadAll() {
    if (loaded.value) return
    loading.value = true
    try {
      const [c, p, r, cl, ct, pc, rules] = await Promise.all([
        fetchCategory('cells'),
        fetchCategory('packs'),
        fetchCategory('racks'),
        fetchCategory('clusters'),
        fetchCategory('containers'),
        fetchCategory('pcs'),
        fetchConfigRules(),
      ])
      const totalFromApi = c.length + p.length + r.length + cl.length + ct.length + pc.length
      if (totalFromApi === 0) {
        try {
          await fetch('/api/products/seed', { method: 'POST' })
          const [c2, p2, r2, cl2, ct2, pc2, rules2] = await Promise.all([
            fetchCategory('cells'),
            fetchCategory('packs'),
            fetchCategory('racks'),
            fetchCategory('clusters'),
            fetchCategory('containers'),
            fetchCategory('pcs'),
            fetchConfigRules(),
          ])
          if (c2.length + p2.length + r2.length + cl2.length + ct2.length + pc2.length > 0) {
            cells.value = c2
            packs.value = p2
            racks.value = r2
            clusters.value = cl2
            containers.value = ct2
            pcs.value = pc2
            configRules.value = rules2
            source.value = 'api'
            loaded.value = true
            return
          }
        } catch {
          loadFromLocalJson()
          return
        }
      }
      cells.value = c
      packs.value = p
      racks.value = r
      clusters.value = cl
      containers.value = ct
      pcs.value = pc
      configRules.value = rules
      source.value = 'api'
      loaded.value = true
    } catch (e) {
      console.error('加载产品库失败，使用本地数据:', e)
      loadFromLocalJson()
    } finally {
      loading.value = false
    }
  }

  async function refreshProducts() {
    loading.value = true
    try {
      await fetch('/api/products/refresh', { method: 'POST' })
      await loadAll()
    } catch (e) {
      console.error('刷新产品库失败:', e)
    } finally {
      loading.value = false
    }
  }

  async function matchConfigRule(params) {
    try {
      const resp = await fetch('/api/products/match-config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params),
      })
      const data = await resp.json()
      return data
    } catch {
      return { success: false, matched: false }
    }
  }

  async function getHierarchy(params) {
    try {
      const resp = await fetch('/api/products/hierarchy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params),
      })
      const data = await resp.json()
      return data
    } catch {
      return { success: false, data: {} }
    }
  }

  function getCellById(id) {
    return cells.value.find(c => c.id === id)
  }

  function getCellByModel(model) {
    return cells.value.find(c => c.model === model)
  }

  function getPackById(id) {
    return packs.value.find(p => p.id === id)
  }

  function getPackByModel(model) {
    return packs.value.find(p => p.model === model)
  }

  function getRackById(id) {
    return racks.value.find(r => r.id === id)
  }

  function getRackByModel(model) {
    return racks.value.find(r => r.model === model)
  }

  function getClusterById(id) {
    return clusters.value.find(c => c.id === id)
  }

  function getClusterByModel(model) {
    return clusters.value.find(c => c.model === model)
  }

  function getContainerById(id) {
    return containers.value.find(c => c.id === id)
  }

  function getContainerByModel(model) {
    return containers.value.find(c => c.model === model)
  }

  function getPcsById(id) {
    return pcs.value.find(p => p.id === id)
  }

  function getPcsByModel(model) {
    return pcs.value.find(p => p.model === model)
  }

  function getPackByCellModel(cellModel) {
    return packs.value.filter(p => p.cellModel === cellModel)
  }

  function getRackByPackModel(packModel) {
    return racks.value.filter(r => r.packModel === packModel)
  }

  function getClusterByRackModel(rackModel) {
    return clusters.value.filter(c => c.rackModel === rackModel)
  }

  function getContainerByClusterModel(clusterModel) {
    return containers.value.filter(c => c.clusterModel === clusterModel)
  }

  function getContainerByCellModel(cellModel) {
    return containers.value.filter(c => c.cellModel === cellModel)
  }

  const cellModels = computed(() => [...new Set(cells.value.map(c => c.model).filter(Boolean))])
  const cellMfrs = computed(() => [...new Set(cells.value.map(c => c.mfr).filter(Boolean))])
  const packModels = computed(() => [...new Set(packs.value.map(p => p.model).filter(Boolean))])
  const packMfrs = computed(() => [...new Set(packs.value.map(p => p.mfr).filter(Boolean))])
  const rackModels = computed(() => [...new Set(racks.value.map(r => r.model).filter(Boolean))])
  const rackMfrs = computed(() => [...new Set(racks.value.map(r => r.mfr).filter(Boolean))])
  const clusterModels = computed(() => [...new Set(clusters.value.map(c => c.model).filter(Boolean))])
  const clusterMfrs = computed(() => [...new Set(clusters.value.map(c => c.mfr).filter(Boolean))])
  const containerModels = computed(() => [...new Set(containers.value.map(c => c.model).filter(Boolean))])
  const containerMfrs = computed(() => [...new Set(containers.value.map(c => c.mfr).filter(Boolean))])
  const pcsModels = computed(() => [...new Set(pcs.value.map(p => p.model).filter(Boolean))])
  const pcsMfrs = computed(() => [...new Set(pcs.value.map(p => p.mfr).filter(Boolean))])

  return {
    cells, packs, racks, clusters, containers, pcs, configRules,
    loading, loaded, source,
    loadAll, refreshProducts,
    matchConfigRule, getHierarchy,
    getCellById, getCellByModel,
    getPackById, getPackByModel, getPackByCellModel,
    getRackById, getRackByModel, getRackByPackModel,
    getClusterById, getClusterByModel, getClusterByRackModel,
    getContainerById, getContainerByModel, getContainerByClusterModel, getContainerByCellModel,
    getPcsById, getPcsByModel,
    cellModels, cellMfrs,
    packModels, packMfrs,
    rackModels, rackMfrs,
    clusterModels, clusterMfrs,
    containerModels, containerMfrs,
    pcsModels, pcsMfrs,
  }
}