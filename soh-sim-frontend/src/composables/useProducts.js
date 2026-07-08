import { ref, computed } from 'vue'
import api from '../services/api.js'
import localProducts from '../data/products.json'

const cells = ref([])
const packs = ref([])
const racks = ref([])
const clusters = ref([])
const containers = ref([])
const pcs = ref([])
const configRules = ref([])
const loading = ref(false)
const source = ref('')

const CAMEL_MAP = {
  capacity_ah: 'capacityAh',
  voltage_nominal: 'voltageNominal',
  voltage_max: 'voltageMax',
  voltage_min: 'voltageMin',
  voltage_range: 'voltageRange',
  // 统一能量字段：
  rated_energy_mwh: 'ratedEnergyMWh', // 容器/簇/电芯统一
  energy_wh: 'ratedEnergyMWh', // 兼容旧电芯字段
  nominal_energy_kwh: 'ratedEnergyMWh', // 兼容旧Pack/Rack字段
  nominal_energy_mwh: 'ratedEnergyMWh', // 兼容旧簇字段
  // 统一功率字段：
  rated_power_mw: 'ratedPowerMW', // 所有设备统一
  nominal_power_mw: 'ratedPowerMW', // 兼容旧簇字段
  cycle_life: 'cycleLife',
  calendar_life: 'calendarLife',
  energy_density: 'energyDensity',
  soh_curve: 'sohCurve',
  certifications: 'certifications',
  unit_price: 'unitPrice',
  remarks: 'remarks',
  cell_model: 'cellModel',
  cell_config: 'cellConfig',
  rated_power_kva: 'ratedPowerKVA',
  ac_voltage: 'acVoltage',
  dc_voltage_range: 'dcVoltageRange',
  cells_per_pack: 'cellsPerPack',
  series_count: 'seriesCount',
  parallel_count: 'parallelCount',
  nominal_voltage: 'nominalVoltage',
  nominal_capacity_ah: 'nominalCapacityAh',
  max_charge_current: 'maxChargeCurrent',
  max_discharge_current: 'maxDischargeCurrent',
  bms_type: 'bmsType',
  pack_model: 'packModel',
  packs_per_rack: 'packsPerRack',
  cooling: 'cooling',
  racks_per_cluster: 'racksPerCluster',
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
  is_builtin: 'isBuiltin',
  tenant_id: 'tenantId'
}

function toCamel(obj) {
  const result = {}
  for (const [k, v] of Object.entries(obj)) {
    const key = CAMEL_MAP[k] || k
    result[key] = v
  }
  return result
}

async function fetchCategory(category, _force = false) {
  try {
    const data = await api.get(`/api/products/${category}`)
    return (data.items || []).map(toCamel)
  } catch {
    return []
  }
}

async function fetchConfigRules(_force = false) {
  try {
    const data = await api.get('/api/products/config-rules')
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
}

export function useProducts() {
  /**
   * 强制重新加载（用于新增/删除/修改产品后刷新下拉框）
   */
  async function loadAll(force = false) {
    loading.value = true
    try {
      const [c, p, r, cl, ct, pc, rules] = await Promise.all([
        fetchCategory('cells', force),
        fetchCategory('packs', force),
        fetchCategory('racks', force),
        fetchCategory('clusters', force),
        fetchCategory('containers', force),
        fetchCategory('pcs', force),
        fetchConfigRules(force)
      ])
      const totalFromApi = c.length + p.length + r.length + cl.length + ct.length + pc.length
      if (totalFromApi === 0) {
        try {
          await api.post('/api/products/seed')
          const [c2, p2, r2, cl2, ct2, pc2, rules2] = await Promise.all([
            fetchCategory('cells', true),
            fetchCategory('packs', true),
            fetchCategory('racks', true),
            fetchCategory('clusters', true),
            fetchCategory('containers', true),
            fetchCategory('pcs', true),
            fetchConfigRules(true)
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
    } catch (e) {
      console.error('加载产品库失败，使用本地数据:', e)
      loadFromLocalJson()
    } finally {
      loading.value = false
    }
  }

  /**
   * 强制刷新所有产品（用于产品变更后立即生效）
   */
  async function refreshProducts() {
    await loadAll(true)
  }

  /**
   * 新增产品
   */
  async function createProduct(category, data) {
    const result = await api.post(`/api/products/${category}`, data)
    await loadAll(true)
    return result
  }

  /**
   * 更新产品
   */
  async function updateProduct(category, itemId, data) {
    const result = await api.put(`/api/products/${category}/${itemId}`, data)
    await loadAll(true)
    return result
  }

  /**
   * 删除产品
   */
  async function deleteProduct(category, itemId) {
    const result = await api.del(`/api/products/${category}/${itemId}`)
    await loadAll(true)
    return result
  }

  async function matchConfigRule(params) {
    try {
      const data = await api.post('/api/products/match-config', params)
      return data
    } catch {
      return { success: false, matched: false }
    }
  }

  async function getHierarchy(params) {
    try {
      const data = await api.post('/api/products/hierarchy', params)
      return data
    } catch {
      return { success: false, data: {} }
    }
  }

  function getCellById(id) {
    return cells.value.find((c) => c.id === id)
  }

  function getCellByModel(model) {
    return cells.value.find((c) => c.model === model)
  }

  function getPackById(id) {
    return packs.value.find((p) => p.id === id)
  }

  function getPackByModel(model) {
    return packs.value.find((p) => p.model === model)
  }

  function getRackById(id) {
    return racks.value.find((r) => r.id === id)
  }

  function getRackByModel(model) {
    return racks.value.find((r) => r.model === model)
  }

  function getClusterById(id) {
    return clusters.value.find((c) => c.id === id)
  }

  function getClusterByModel(model) {
    return clusters.value.find((c) => c.model === model)
  }

  function getContainerById(id) {
    return containers.value.find((c) => c.id === id)
  }

  function getContainerByModel(model) {
    return containers.value.find((c) => c.model === model)
  }

  function getPcsById(id) {
    return pcs.value.find((p) => p.id === id)
  }

  function getPcsByModel(model) {
    return pcs.value.find((p) => p.model === model)
  }

  function getPackByCellModel(cellModel) {
    return packs.value.filter((p) => p.cellModel === cellModel)
  }

  function getRackByPackModel(packModel) {
    return racks.value.filter((r) => r.packModel === packModel)
  }

  function getClusterByRackModel(rackModel) {
    return clusters.value.filter((c) => c.rackModel === rackModel)
  }

  function getContainerByClusterModel(clusterModel) {
    return containers.value.filter((c) => c.clusterModel === clusterModel)
  }

  function getContainerByCellModel(cellModel) {
    return containers.value.filter((c) => c.cellModel === cellModel)
  }

  const cellModels = computed(() => [...new Set(cells.value.map((c) => c.model).filter(Boolean))])
  const cellMfrs = computed(() => [...new Set(cells.value.map((c) => c.mfr).filter(Boolean))])
  const packModels = computed(() => [...new Set(packs.value.map((p) => p.model).filter(Boolean))])
  const packMfrs = computed(() => [...new Set(packs.value.map((p) => p.mfr).filter(Boolean))])
  const rackModels = computed(() => [...new Set(racks.value.map((r) => r.model).filter(Boolean))])
  const rackMfrs = computed(() => [...new Set(racks.value.map((r) => r.mfr).filter(Boolean))])
  const clusterModels = computed(() => [...new Set(clusters.value.map((c) => c.model).filter(Boolean))])
  const clusterMfrs = computed(() => [...new Set(clusters.value.map((c) => c.mfr).filter(Boolean))])
  const containerModels = computed(() => [...new Set(containers.value.map((c) => c.model).filter(Boolean))])
  const containerMfrs = computed(() => [...new Set(containers.value.map((c) => c.mfr).filter(Boolean))])
  const pcsModels = computed(() => [...new Set(pcs.value.map((p) => p.model).filter(Boolean))])
  const pcsMfrs = computed(() => [...new Set(pcs.value.map((p) => p.mfr).filter(Boolean))])

  return {
    cells,
    packs,
    racks,
    clusters,
    containers,
    pcs,
    configRules,
    loading,
    source,
    loadAll,
    refreshProducts,
    createProduct,
    updateProduct,
    deleteProduct,
    matchConfigRule,
    getHierarchy,
    getCellById,
    getCellByModel,
    getPackById,
    getPackByModel,
    getPackByCellModel,
    getRackById,
    getRackByModel,
    getRackByPackModel,
    getClusterById,
    getClusterByModel,
    getClusterByRackModel,
    getContainerById,
    getContainerByModel,
    getContainerByClusterModel,
    getContainerByCellModel,
    getPcsById,
    getPcsByModel,
    cellModels,
    cellMfrs,
    packModels,
    packMfrs,
    rackModels,
    rackMfrs,
    clusterModels,
    clusterMfrs,
    containerModels,
    containerMfrs,
    pcsModels,
    pcsMfrs
  }
}
