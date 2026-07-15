<template>
  <div class="admin-section">
    <div class="admin-section-header">
      <h2>{{ $t('admin.productLibrary') }}</h2>
      <p class="admin-section-desc">{{ $t('admin.productLibraryDesc') }}</p>
    </div>

    <!-- 子标签：产品分类 -->
    <div class="admin-subtabs">
      <button
        v-for="cat in categories"
        :key="cat.key"
        :class="['admin-subtab', { active: activeCategory === cat.key }]"
        @click="activeCategory = cat.key"
      >
        {{ $t(cat.labelKey) }}
        <span class="subtab-count">{{ productCount(cat.key) }}</span>
      </button>
    </div>

    <div v-if="loading" class="admin-loading">{{ $t('admin.loading') }}</div>

    <template v-else>
      <!-- 工具栏 -->
      <div class="product-toolbar">
        <input v-model="searchQuery" type="text" :placeholder="$t('admin.searchProduct')" class="product-search" />
        <select v-model="mfrFilter" class="product-filter">
          <option value="">{{ $t('admin.allManufacturers') }}</option>
          <option v-for="m in currentMfrList" :key="m" :value="m">{{ m }}</option>
        </select>
        <button class="admin-btn admin-btn-primary" @click="openAddModal">+ {{ $t('admin.addProduct') }}</button>
      </div>

      <!-- 产品表格 -->
      <div class="product-table-wrap">
        <table class="product-table">
          <thead>
            <tr>
              <th v-for="col in currentColumns" :key="col.key" :style="col.width ? { width: col.width } : {}">
                {{ $t(col.labelKey) }}
              </th>
              <th class="actions-col">{{ $t('admin.actions') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in filteredProducts" :key="item.id">
              <td v-for="col in currentColumns" :key="col.key">
                <template v-if="col.key === 'status'">
                  <span :class="['status-badge', item.status === 'active' ? 'status-active' : 'status-inactive']">
                    {{ item.status }}
                  </span>
                </template>
                <template v-else-if="col.key === 'efficiency' && item.efficiency != null">
                  {{ item.efficiency }}%
                </template>
                <template v-else-if="col.key === 'ratedEnergyMWh'">
                  {{ formatNumber(item.ratedEnergyMWh) }} MWh
                </template>
                <template v-else-if="col.key === 'ratedPowerMW'">
                  {{ formatNumber(item.ratedPowerMW) }} MW
                </template>
                <template v-else>
                  {{ item[col.key] ?? '-' }}
                </template>
              </td>
              <td class="product-actions">
                <button class="admin-btn admin-btn-sm" @click="openEditModal(item)">{{ $t('admin.edit') }}</button>
                <button
                  v-if="!item.isBuiltin"
                  class="admin-btn admin-btn-sm admin-btn-danger"
                  @click="confirmDelete(item)"
                >
                  {{ $t('admin.delete') }}
                </button>
              </td>
            </tr>
            <tr v-if="filteredProducts.length === 0">
              <td :colspan="currentColumns.length + 1" class="product-empty">
                {{ $t('admin.noProducts') }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <!-- 新增/编辑 Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-content product-modal">
        <h3>{{ editingItem ? $t('admin.editProduct') : $t('admin.addProduct') }}</h3>
        <div class="modal-form">
          <div v-for="field in currentFormFields" :key="field.key" class="form-group">
            <label>{{ $t(field.labelKey) }}</label>
            <input
              v-if="field.type === 'text' || field.type === 'number'"
              v-model="formData[field.key]"
              :type="field.type"
              :placeholder="field.placeholder"
              :step="field.step"
            />
            <select v-else-if="field.type === 'select'" v-model="formData[field.key]">
              <option v-for="opt in field.options" :key="opt" :value="opt">{{ opt }}</option>
            </select>
          </div>
        </div>
        <div class="modal-actions">
          <button class="admin-btn" @click="showModal = false">{{ $t('admin.cancel') }}</button>
          <button class="admin-btn admin-btn-primary" @click="saveProduct">{{ $t('admin.save') }}</button>
        </div>
      </div>
    </div>

    <!-- 删除确认 -->
    <div v-if="showDeleteConfirm" class="modal-overlay" @click.self="showDeleteConfirm = false">
      <div class="modal-content modal-sm">
        <p>{{ $t('admin.confirmDeleteProduct', { name: deleteTarget?.model || deleteTarget?.id }) }}</p>
        <div class="modal-actions">
          <button class="admin-btn" @click="showDeleteConfirm = false">{{ $t('admin.cancel') }}</button>
          <button class="admin-btn admin-btn-danger" @click="doDelete">{{ $t('admin.delete') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '../services/api.js'

const { t } = useI18n()

// ---- 分类定义 ----
const categories = [
  { key: 'cells', labelKey: 'admin.cellLibrary', apiCategory: 'cells' },
  { key: 'containers', labelKey: 'admin.containerLibrary', apiCategory: 'containers' },
  { key: 'pcs', labelKey: 'admin.pcsLibrary', apiCategory: 'pcs' }
]

const activeCategory = ref('containers')
const loading = ref(false)
const searchQuery = ref('')
const mfrFilter = ref('')

// 产品数据
const allProducts = ref({ cells: [], containers: [], pcs: [] })

// Modal 状态
const showModal = ref(false)
const editingItem = ref(null)
const formData = ref({})

// 删除确认
const showDeleteConfirm = ref(false)
const deleteTarget = ref(null)

// ---- 列定义 ----
const columnDefs = {
  cells: [
    { key: 'model', labelKey: 'admin.colModel', width: '140px' },
    { key: 'mfr', labelKey: 'admin.colMfr', width: '100px' },
    { key: 'chemistry', labelKey: 'admin.colChemistry', width: '80px' },
    { key: 'capacityAh', labelKey: 'admin.colCapacity', width: '90px' },
    { key: 'cycleLife', labelKey: 'admin.colCycleLife', width: '80px' },
    { key: 'status', labelKey: 'admin.colStatus', width: '80px' }
  ],
  containers: [
    { key: 'model', labelKey: 'admin.colModel', width: '140px' },
    { key: 'mfr', labelKey: 'admin.colMfr', width: '100px' },
    { key: 'ratedEnergyMWh', labelKey: 'admin.colEnergy', width: '100px' },
    { key: 'ratedPowerMW', labelKey: 'admin.colPower', width: '90px' },
    { key: 'cooling', labelKey: 'admin.colCooling', width: '100px' },
    { key: 'cycleLife', labelKey: 'admin.colCycleLife', width: '80px' },
    { key: 'status', labelKey: 'admin.colStatus', width: '80px' }
  ],
  pcs: [
    { key: 'model', labelKey: 'admin.colModel', width: '140px' },
    { key: 'mfr', labelKey: 'admin.colMfr', width: '100px' },
    { key: 'ratedPowerMW', labelKey: 'admin.colPower', width: '90px' },
    { key: 'efficiency', labelKey: 'admin.colEfficiency', width: '80px' },
    { key: 'acVoltage', labelKey: 'admin.colAcVoltage', width: '100px' },
    { key: 'cooling', labelKey: 'admin.colCooling', width: '100px' },
    { key: 'status', labelKey: 'admin.colStatus', width: '80px' }
  ]
}

// 表单字段定义
const formFieldDefs = {
  cells: [
    { key: 'model', labelKey: 'admin.fieldModel', type: 'text', placeholder: 'e.g. LFP-280AH' },
    { key: 'mfr', labelKey: 'admin.fieldMfr', type: 'text', placeholder: 'e.g. CATL' },
    { key: 'chemistry', labelKey: 'admin.fieldChemistry', type: 'select', options: ['LFP', 'NMC', 'LTO'] },
    { key: 'capacityAh', labelKey: 'admin.fieldCapacityAh', type: 'number', step: '0.1' },
    { key: 'voltageNominal', labelKey: 'admin.fieldVoltage', type: 'number', step: '0.01' },
    { key: 'cycleLife', labelKey: 'admin.fieldCycleLife', type: 'number', step: '1' },
    { key: 'unitPrice', labelKey: 'admin.fieldUnitPrice', type: 'number', step: '0.01' }
  ],
  containers: [
    { key: 'model', labelKey: 'admin.fieldModel', type: 'text', placeholder: 'e.g. TENER-6.25' },
    { key: 'mfr', labelKey: 'admin.fieldMfr', type: 'text', placeholder: 'e.g. CATL' },
    { key: 'ratedEnergyMWh', labelKey: 'admin.fieldEnergy', type: 'number', step: '0.01' },
    { key: 'ratedPowerMW', labelKey: 'admin.fieldPower', type: 'number', step: '0.1' },
    {
      key: 'cooling',
      labelKey: 'admin.fieldCooling',
      type: 'select',
      options: ['Liquid Cooling', 'Air Cooling', 'Hybrid']
    },
    { key: 'cycleLife', labelKey: 'admin.fieldCycleLife', type: 'number', step: '1' },
    { key: 'unitPrice', labelKey: 'admin.fieldUnitPrice', type: 'number', step: '0.01' }
  ],
  pcs: [
    { key: 'model', labelKey: 'admin.fieldModel', type: 'text', placeholder: 'e.g. PCS-2500' },
    { key: 'mfr', labelKey: 'admin.fieldMfr', type: 'text', placeholder: 'e.g. Sungrow' },
    { key: 'ratedPowerMW', labelKey: 'admin.fieldPower', type: 'number', step: '0.01' },
    { key: 'efficiency', labelKey: 'admin.fieldEfficiency', type: 'number', step: '0.1' },
    { key: 'acVoltage', labelKey: 'admin.fieldAcVoltage', type: 'text', placeholder: 'e.g. 690V' },
    {
      key: 'cooling',
      labelKey: 'admin.fieldCooling',
      type: 'select',
      options: ['Liquid Cooling', 'Air Cooling', 'Forced Air']
    },
    { key: 'unitPrice', labelKey: 'admin.fieldUnitPrice', type: 'number', step: '0.01' }
  ]
}

// ---- 计算属性 ----
const currentColumns = computed(() => columnDefs[activeCategory.value] || [])
const currentFormFields = computed(() => formFieldDefs[activeCategory.value] || [])
const currentProducts = computed(() => allProducts.value[activeCategory.value] || [])

const currentMfrList = computed(() => {
  const mfrs = new Set()
  currentProducts.value.forEach((p) => {
    if (p.mfr) mfrs.add(p.mfr)
  })
  return [...mfrs].sort()
})

const filteredProducts = computed(() => {
  let list = currentProducts.value
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter((p) => (p.model || '').toLowerCase().includes(q) || (p.mfr || '').toLowerCase().includes(q))
  }
  if (mfrFilter.value) {
    list = list.filter((p) => p.mfr === mfrFilter.value)
  }
  return list
})

// ---- 方法 ----
function productCount(catKey) {
  return (allProducts.value[catKey] || []).length
}

function formatNumber(v) {
  if (v == null) return '-'
  return Number(v).toLocaleString()
}

async function loadProducts() {
  loading.value = true
  try {
    const results = await Promise.all([
      api.get('/api/products/cells?page_size=200'),
      api.get('/api/products/containers?page_size=200'),
      api.get('/api/products/pcs?page_size=200')
    ])
    allProducts.value = {
      cells: results[0]?.data || results[0]?.items || [],
      containers: results[1]?.data || results[1]?.items || [],
      pcs: results[2]?.data || results[2]?.items || []
    }
  } catch (e) {
    console.error('Failed to load products:', e)
  } finally {
    loading.value = false
  }
}

function openAddModal() {
  editingItem.value = null
  formData.value = {}
  showModal.value = true
}

function openEditModal(item) {
  editingItem.value = item
  formData.value = { ...item }
  showModal.value = true
}

async function saveProduct() {
  const cat = activeCategory.value
  const apiCategory = categories.find((c) => c.key === cat)?.apiCategory || cat
  try {
    if (editingItem.value) {
      await api.put(`/api/products/${apiCategory}/${editingItem.value.id}`, formData.value)
    } else {
      await api.post(`/api/products/${apiCategory}`, formData.value)
    }
    showModal.value = false
    await loadProducts()
  } catch (e) {
    console.error('Save product failed:', e)
    alert(t('admin.saveFailed'))
  }
}

function confirmDelete(item) {
  deleteTarget.value = item
  showDeleteConfirm.value = true
}

async function doDelete() {
  if (!deleteTarget.value) return
  const cat = activeCategory.value
  const apiCategory = categories.find((c) => c.key === cat)?.apiCategory || cat
  try {
    await api.del(`/api/products/${apiCategory}/${deleteTarget.value.id}`)
    showDeleteConfirm.value = false
    deleteTarget.value = null
    await loadProducts()
  } catch (e) {
    console.error('Delete product failed:', e)
    alert(t('admin.deleteFailed'))
  }
}

onMounted(() => {
  loadProducts()
})
</script>
