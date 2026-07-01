<template>
  <div class="boq-editor h-full flex flex-col gap-3">
    <div class="flex items-center justify-between">
      <h2 class="text-lg font-bold" style="color: var(--color-text)">工程量清单 BOQ</h2>
      <div class="flex gap-2">
        <button class="px-3 py-1 text-xs rounded" :style="versionStyle('main')" @click="switchVersion('main')">
          Main BOQ
        </button>
        <button
          class="px-3 py-1 text-xs rounded"
          :style="versionStyle('alternative')"
          @click="switchVersion('alternative')"
        >
          Alternative
        </button>
      </div>
    </div>

    <div class="flex gap-2">
      <button
        class="px-3 py-1 text-xs rounded"
        style="background: var(--color-accent); color: #fff"
        @click="autoFillQuantities"
      >
        自动预填数量
      </button>
      <button
        class="px-3 py-1 text-xs rounded"
        style="background: var(--color-card); border: 1px solid var(--color-border); color: var(--color-text)"
        @click="save"
      >
        保存 BOQ
      </button>
      <button
        class="px-3 py-1 text-xs rounded"
        style="background: var(--color-card); border: 1px solid var(--color-accent); color: var(--color-accent)"
        @click="aggregateCapex"
      >
        汇总到 CAPEX
      </button>
    </div>

    <div class="flex-1 overflow-y-auto space-y-1" style="min-height: 0">
      <div
        v-for="section in sections"
        :key="section.code"
        class="rounded"
        style="border: 1px solid var(--color-border)"
      >
        <div
          class="flex items-center justify-between px-3 py-2 cursor-pointer select-none"
          style="background: var(--color-card)"
          @click="toggleSection(section.code)"
        >
          <div class="flex items-center gap-2">
            <span class="text-xs font-mono" style="color: var(--color-accent)">{{ section.code }}</span>
            <span class="text-sm font-bold" style="color: var(--color-text)">
              {{ section.name_zh || section.name }}
            </span>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs" style="color: var(--color-text-muted)">
              小计: {{ formatPrice(sectionSubtotal(section.code)) }}
            </span>
            <span class="text-xs" style="color: var(--color-text-muted)">
              {{ openSections[section.code] ? '▲' : '▼' }}
            </span>
          </div>
        </div>
        <div v-if="openSections[section.code]" class="p-2">
          <table class="w-full text-xs" style="border-collapse: collapse">
            <thead>
              <tr style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)">
                <th class="p-1 text-left w-8">#</th>
                <th class="p-1 text-left">设备/工程名称</th>
                <th class="p-1 text-left">规格型号</th>
                <th class="p-1 text-left w-12">单位</th>
                <th class="p-1 text-right w-20">数量</th>
                <th class="p-1 text-right w-24">单价 (USD)</th>
                <th class="p-1 text-right w-24">合价 (USD)</th>
                <th class="p-1 text-left w-24">备注</th>
                <th class="p-1 w-8" />
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, idx) in sectionItems(section.code)" :key="idx">
                <td class="p-1">
                  <input
                    v-model.number="item.seq"
                    class="w-full px-1 py-0.5 rounded text-xs"
                    style="
                      background: var(--color-input-bg-dark);
                      border: 1px solid var(--color-input-border);
                      color: var(--color-text);
                    "
                  />
                </td>
                <td class="p-1">
                  <input
                    v-model="item.name"
                    class="w-full px-1 py-0.5 rounded text-xs"
                    style="
                      background: var(--color-input-bg-dark);
                      border: 1px solid var(--color-input-border);
                      color: var(--color-text);
                    "
                  />
                </td>
                <td class="p-1">
                  <input
                    v-model="item.spec"
                    class="w-full px-1 py-0.5 rounded text-xs"
                    style="
                      background: var(--color-input-bg-dark);
                      border: 1px solid var(--color-input-border);
                      color: var(--color-text);
                    "
                  />
                </td>
                <td class="p-1">
                  <input
                    v-model="item.unit"
                    class="w-full px-1 py-0.5 rounded text-xs"
                    style="
                      background: var(--color-input-bg-dark);
                      border: 1px solid var(--color-input-border);
                      color: var(--color-text);
                    "
                  />
                </td>
                <td class="p-1">
                  <input
                    v-model.number="item.quantity"
                    type="number"
                    step="1"
                    class="w-full px-1 py-0.5 rounded text-xs text-right"
                    style="
                      background: var(--color-input-bg-dark);
                      border: 1px solid var(--color-input-border);
                      color: var(--color-text);
                    "
                    @input="updateItemTotal(item)"
                  />
                </td>
                <td class="p-1">
                  <input
                    v-model.number="item.unitPrice"
                    type="number"
                    step="0.01"
                    class="w-full px-1 py-0.5 rounded text-xs text-right"
                    style="
                      background: var(--color-input-bg-dark);
                      border: 1px solid var(--color-input-border);
                      color: var(--color-text);
                    "
                    @input="updateItemTotal(item)"
                  />
                </td>
                <td class="p-1 text-right font-mono" :style="{ color: 'var(--color-accent)' }">
                  {{ formatPrice(item.totalPrice || (item.quantity || 0) * (item.unitPrice || 0)) }}
                </td>
                <td class="p-1">
                  <input
                    v-model="item.note"
                    class="w-full px-1 py-0.5 rounded text-xs"
                    style="
                      background: var(--color-input-bg-dark);
                      border: 1px solid var(--color-input-border);
                      color: var(--color-text);
                    "
                  />
                </td>
                <td class="p-1 text-center">
                  <button class="text-xs" style="color: #ef4444" @click="removeItem(section.code, idx)">x</button>
                </td>
              </tr>
            </tbody>
          </table>
          <button
            class="mt-2 text-xs px-2 py-1 rounded"
            style="
              background: var(--color-card);
              border: 1px dashed var(--color-border);
              color: var(--color-text-muted);
            "
            @click="addItem(section.code)"
          >
            + 添加条目
          </button>
        </div>
      </div>
    </div>

    <div
      class="flex items-center justify-between px-3 py-2 rounded"
      style="background: var(--color-accent); color: #fff"
    >
      <span class="text-sm font-bold">BOQ 总价</span>
      <span class="text-lg font-mono font-bold">{{ formatPrice(totalPrice) }} USD</span>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted, computed } from 'vue'
import { useBessStore } from '../stores/bess.js'

const store = useBessStore()

const sections = ref([])
const openSections = reactive({})
const items = reactive([])

const BOQ_CATEGORY_UNITS = {
  100: 'MWh',
  200: 'MW',
  300: 'lot',
  400: 'sqm',
  500: 'lot',
  600: 'lot',
  700: 'lot'
}

const totalPrice = computed(() => {
  return items.reduce((sum, item) => {
    const q = item.quantity || 0
    const p = item.unitPrice || 0
    return sum + item.totalPrice || q * p
  }, 0)
})

onMounted(async () => {
  await loadSections()
  await loadItems()
})

async function loadSections() {
  try {
    const res = await fetch('/api/boq/sections')
    const json = await res.json()
    if (json.success) {
      sections.value = json.data
      json.data.forEach((s) => {
        openSections[s.code] = true
      })
    }
  } catch (e) {
    sections.value = [
      { code: '100', name_zh: '电池系统', unit: 'MWh' },
      { code: '200', name_zh: 'PCS 变流系统', unit: 'MW' },
      { code: '300', name_zh: '电站配套 BOP', unit: 'lot' },
      { code: '400', name_zh: '土建工程', unit: 'sqm' },
      { code: '500', name_zh: '并网接入', unit: 'lot' },
      { code: '600', name_zh: '能量管理系统 EMS', unit: 'lot' },
      { code: '700', name_zh: '调试与运维', unit: 'lot' }
    ]
    sections.value.forEach((s) => {
      openSections[s.code] = true
    })
  }
}

async function loadItems() {
  if (store.project.id) {
    await store.fetchBoqItems(store.project.id)
    items.length = 0
    store.boq.items.forEach((it) => {
      items.push({
        id: it.id,
        sectionCode: it.section_code,
        seq: it.seq,
        name: it.name,
        spec: it.spec,
        unit: it.unit,
        quantity: it.quantity,
        unitPrice: it.unit_price,
        totalPrice: it.total_price,
        note: it.note,
        version: it.version
      })
    })
  }
}

function sectionItems(code) {
  return items
    .map((item, idx) => ({ ...item, _idx: idx }))
    .filter((item) => item.sectionCode === code)
    .sort((a, b) => (a.seq || 0) - (b.seq || 0))
}

function sectionSubtotal(code) {
  return sectionItems(code).reduce((sum, item) => {
    return sum + (item.totalPrice || (item.quantity || 0) * (item.unitPrice || 0))
  }, 0)
}

function addItem(code) {
  const sectionItems_ = sectionItems(code)
  const seq = sectionItems_.length > 0 ? Math.max(...sectionItems_.map((it) => it.seq || 0)) + 1 : 1
  items.push({
    id: null,
    sectionCode: code,
    seq,
    name: '',
    spec: '',
    unit: BOQ_CATEGORY_UNITS[code] || 'lot',
    quantity: 1,
    unitPrice: 0,
    totalPrice: 0,
    note: '',
    version: 1
  })
}

function removeItem(code, idx) {
  const realIdx = items.findIndex((it) => it.sectionCode === code && it === sectionItems(code)[idx])
  if (realIdx >= 0) items.splice(realIdx, 1)
}

function updateItemTotal(item) {
  item.totalPrice = (item.quantity || 0) * (item.unitPrice || 0)
}

function toggleSection(code) {
  openSections[code] = !openSections[code]
}

function switchVersion(ver) {
  store.boq.activeVersion = ver
  loadItems()
}

function versionStyle(ver) {
  const active = store.boq.activeVersion === ver
  return {
    background: active ? 'var(--color-accent)' : 'var(--color-card)',
    color: active ? '#fff' : 'var(--color-text-muted)',
    border: active ? 'none' : '1px solid var(--color-border)'
  }
}

function autoFillQuantities() {
  const sp = store.systemParams
  const qtyHints = {
    100: { name: '电池集装箱', quantity: sp.initContainerQty || 10, unit: 'pcs' },
    200: { name: 'PCS 变流器', quantity: sp.initPcsQty || 2, unit: 'pcs' },
    300: { name: 'BOP 配套设施', quantity: 1, unit: 'lot' },
    400: { name: '土建基础', quantity: (sp.initContainerQty || 10) * 30, unit: 'sqm' },
    500: { name: '并网设备', quantity: 1, unit: 'lot' },
    600: { name: 'EMS 系统', quantity: 1, unit: 'lot' },
    700: { name: '调试与运维', quantity: 1, unit: 'lot' }
  }
  for (const [code, hint] of Object.entries(qtyHints)) {
    const existing = items.filter((it) => it.sectionCode === code)
    if (existing.length === 0) {
      items.push({
        id: null,
        sectionCode: code,
        seq: 1,
        name: hint.name,
        spec: '',
        unit: hint.unit,
        quantity: hint.quantity,
        unitPrice: 0,
        totalPrice: 0,
        note: '',
        version: 1
      })
    } else {
      existing.forEach((it) => {
        if (!it.quantity || it.quantity === 1) it.quantity = hint.quantity
      })
    }
  }
}

async function save() {
  if (!store.project.id) return
  const payload = items.map((it) => ({
    id: it.id,
    sectionCode: it.sectionCode,
    seq: it.seq || 1,
    name: it.name,
    spec: it.spec,
    unit: it.unit,
    quantity: it.quantity || 0,
    unitPrice: it.unitPrice || 0,
    totalPrice: it.totalPrice || (it.quantity || 0) * (it.unitPrice || 0),
    note: it.note,
    version: it.version || 1
  }))
  store.boq.items = payload
  store.boq.totalPrice = payload.reduce((sum, i) => sum + (i.totalPrice || 0), 0)
  await store.saveBoqItems(store.project.id)
}

async function aggregateCapex() {
  await save()
  await store.aggregateCapexFromBoq()
}

function formatPrice(val) {
  return (val || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}
</script>
