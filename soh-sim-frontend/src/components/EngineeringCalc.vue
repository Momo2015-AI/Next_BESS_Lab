<template>
  <div class="engineering-calc h-full overflow-auto p-4">
    <div class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border)">
      <h3 class="text-sm font-bold mb-4 flex items-center gap-2" style="color: var(--color-accent-secondary)">
        <span class="w-2 h-2 rounded-full" style="background-color: var(--color-accent-secondary)" />
        工程计算模块
      </h3>

      <!-- Tab导航 -->
      <div class="flex gap-2 mb-4">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          class="px-3 py-1.5 rounded text-xs transition-all"
          :style="
            activeTab === tab.id
              ? { backgroundColor: 'var(--color-accent-secondary)', color: 'white' }
              : { backgroundColor: 'var(--color-card-dark)', color: 'var(--color-text-secondary)' }
          "
          onmouseover="this.style.opacity = '0.9'"
          onmouseout="this.style.opacity = '1'"
          @click="activeTab = tab.id"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- 场地面积计算 -->
      <div v-if="activeTab === 'area'" class="space-y-4">
        <div class="grid grid-cols-3 gap-4">
          <div>
            <label class="block text-xs mb-1" style="color: var(--color-text-muted)">集装箱数量</label>
            <input
              v-model.number="siteData.containerQty"
              type="number"
              min="1"
              class="w-full rounded px-3 py-2 text-sm"
              style="
                background-color: var(--color-input-bg-dark);
                border: 1px solid var(--color-input-border);
                color: var(--color-text);
              "
              onfocus="
                this.style.borderColor = 'var(--color-accent-secondary)'
                this.style.outline = 'none'
              "
              onblur="this.style.borderColor = 'var(--color-input-border)'"
            />
          </div>
          <div>
            <label class="block text-xs mb-1" style="color: var(--color-text-muted)">PCS数量</label>
            <input
              v-model.number="siteData.pcsQty"
              type="number"
              min="1"
              class="w-full rounded px-3 py-2 text-sm"
              style="
                background-color: var(--color-input-bg-dark);
                border: 1px solid var(--color-input-border);
                color: var(--color-text);
              "
              onfocus="
                this.style.borderColor = 'var(--color-accent-secondary)'
                this.style.outline = 'none'
              "
              onblur="this.style.borderColor = 'var(--color-input-border)'"
            />
          </div>
          <div>
            <label class="block text-xs mb-1" style="color: var(--color-text-muted)">变压器数量</label>
            <input
              v-model.number="siteData.transformerQty"
              type="number"
              min="1"
              class="w-full rounded px-3 py-2 text-sm"
              style="
                background-color: var(--color-input-bg-dark);
                border: 1px solid var(--color-input-border);
                color: var(--color-text);
              "
              onfocus="
                this.style.borderColor = 'var(--color-accent-secondary)'
                this.style.outline = 'none'
              "
              onblur="this.style.borderColor = 'var(--color-input-border)'"
            />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-xs mb-1" style="color: var(--color-text-muted)">集装箱尺寸 (长×宽×高 m)</label>
            <div class="flex gap-2">
              <input
                v-model.number="siteData.containerLength"
                type="number"
                placeholder="长"
                class="w-full rounded px-3 py-2 text-sm"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
                onfocus="
                  this.style.borderColor = 'var(--color-accent-secondary)'
                  this.style.outline = 'none'
                "
                onblur="this.style.borderColor = 'var(--color-input-border)'"
              />
              <input
                v-model.number="siteData.containerWidth"
                type="number"
                placeholder="宽"
                class="w-full rounded px-3 py-2 text-sm"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
                onfocus="
                  this.style.borderColor = 'var(--color-accent-secondary)'
                  this.style.outline = 'none'
                "
                onblur="this.style.borderColor = 'var(--color-input-border)'"
              />
              <input
                v-model.number="siteData.containerHeight"
                type="number"
                placeholder="高"
                class="w-full rounded px-3 py-2 text-sm"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
                onfocus="
                  this.style.borderColor = 'var(--color-accent-secondary)'
                  this.style.outline = 'none'
                "
                onblur="this.style.borderColor = 'var(--color-input-border)'"
              />
            </div>
          </div>
          <div>
            <label class="block text-xs mb-1" style="color: var(--color-text-muted)">间距和通道系数</label>
            <input
              v-model.number="siteData.spacingFactor"
              type="number"
              step="0.1"
              min="1.2"
              class="w-full rounded px-3 py-2 text-sm"
              style="
                background-color: var(--color-input-bg-dark);
                border: 1px solid var(--color-input-border);
                color: var(--color-text);
              "
              onfocus="
                this.style.borderColor = 'var(--color-accent-secondary)'
                this.style.outline = 'none'
              "
              onblur="this.style.borderColor = 'var(--color-input-border)'"
            />
          </div>
        </div>

        <button
          class="text-xs px-4 py-2 rounded transition-colors"
          style="background-color: var(--color-accent-secondary); color: white"
          onmouseover="this.style.opacity = '0.9'"
          onmouseout="this.style.opacity = '1'"
          @click="calculateSiteArea"
        >
          计算场地面积
        </button>

        <!-- 计算结果 -->
        <div v-if="siteAreaResult" class="mt-4 p-4 rounded-lg" style="background-color: var(--color-card-dark)">
          <div class="text-xs mb-3" style="color: var(--color-text-muted)">场地面积计算结果</div>
          <div class="grid grid-cols-3 gap-4 text-sm">
            <div class="text-center">
              <div class="text-2xl font-bold" style="color: var(--color-accent-secondary)">
                {{ siteAreaResult.containerArea }}
              </div>
              <div class="text-xs" style="color: var(--color-text-muted)">集装箱占地面积 (m²)</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold" style="color: var(--color-accent)">
                {{ siteAreaResult.pcsArea }}
              </div>
              <div class="text-xs" style="color: var(--color-text-muted)">PCS占地面积 (m²)</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold" style="color: var(--color-warning)">
                {{ siteAreaResult.totalArea }}
              </div>
              <div class="text-xs" style="color: var(--color-text-muted)">总占地面积 (m²)</div>
            </div>
          </div>
          <div
            class="mt-3 pt-3 border-t border-slate-700 text-xs"
            style="border-color: var(--color-border); color: var(--color-text-muted)"
          >
            <div>
              考虑间距和通道后的实际占地面积:
              <span style="color: var(--color-text)">{{ siteAreaResult.actualArea }}</span>
              m²
            </div>
            <div>
              约等于
              <span style="color: var(--color-text)">{{ siteAreaResult.landAcres }}</span>
              亩
            </div>
          </div>
        </div>
      </div>

      <!-- BOM清单 -->
      <div v-if="activeTab === 'bom'" class="space-y-4">
        <div class="grid grid-cols-4 gap-4">
          <div>
            <label class="block text-xs mb-1" style="color: var(--color-text-muted)">系统能量 (MWh)</label>
            <input
              v-model.number="bomData.energy"
              type="number"
              class="w-full rounded px-3 py-2 text-sm"
              style="
                background-color: var(--color-input-bg-dark);
                border: 1px solid var(--color-input-border);
                color: var(--color-text);
              "
              onfocus="
                this.style.borderColor = 'var(--color-accent-secondary)'
                this.style.outline = 'none'
              "
              onblur="this.style.borderColor = 'var(--color-input-border)'"
            />
          </div>
          <div>
            <label class="block text-xs mb-1" style="color: var(--color-text-muted)">集装箱数量</label>
            <input
              v-model.number="bomData.containerQty"
              type="number"
              class="w-full rounded px-3 py-2 text-sm"
              style="
                background-color: var(--color-input-bg-dark);
                border: 1px solid var(--color-input-border);
                color: var(--color-text);
              "
              onfocus="
                this.style.borderColor = 'var(--color-accent-secondary)'
                this.style.outline = 'none'
              "
              onblur="this.style.borderColor = 'var(--color-input-border)'"
            />
          </div>
          <div>
            <label class="block text-xs mb-1" style="color: var(--color-text-muted)">PCS总容量 (MW)</label>
            <input
              v-model.number="bomData.pcsCapacity"
              type="number"
              class="w-full rounded px-3 py-2 text-sm"
              style="
                background-color: var(--color-input-bg-dark);
                border: 1px solid var(--color-input-border);
                color: var(--color-text);
              "
              onfocus="
                this.style.borderColor = 'var(--color-accent-secondary)'
                this.style.outline = 'none'
              "
              onblur="this.style.borderColor = 'var(--color-input-border)'"
            />
          </div>
          <div>
            <label class="block text-xs mb-1" style="color: var(--color-text-muted)">变压器容量 (MVA)</label>
            <input
              v-model.number="bomData.transformerCapacity"
              type="number"
              class="w-full rounded px-3 py-2 text-sm"
              style="
                background-color: var(--color-input-bg-dark);
                border: 1px solid var(--color-input-border);
                color: var(--color-text);
              "
              onfocus="
                this.style.borderColor = 'var(--color-accent-secondary)'
                this.style.outline = 'none'
              "
              onblur="this.style.borderColor = 'var(--color-input-border)'"
            />
          </div>
        </div>

        <button
          class="text-xs px-4 py-2 rounded transition-colors"
          style="background-color: var(--color-accent-secondary); color: white"
          onmouseover="this.style.opacity = '0.9'"
          onmouseout="this.style.opacity = '1'"
          @click="generateBOM"
        >
          生成BOM清单
        </button>

        <!-- BOM清单表格 -->
        <div v-if="bomResult.length > 0" class="mt-4 overflow-x-auto">
          <table class="w-full text-xs">
            <thead>
              <tr style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)">
                <th class="text-left py-2 px-2">序号</th>
                <th class="text-left py-2 px-2">设备名称</th>
                <th class="text-left py-2 px-2">规格型号</th>
                <th class="text-right py-2 px-2">单位</th>
                <th class="text-right py-2 px-2">数量</th>
                <th class="text-right py-2 px-2">备注</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(item, idx) in bomResult"
                :key="idx"
                style="color: var(--color-text-secondary); border-bottom: 1px solid var(--color-border)"
              >
                <td class="py-2 px-2">
                  {{ idx + 1 }}
                </td>
                <td class="py-2 px-2">
                  {{ item.name }}
                </td>
                <td class="py-2 px-2">
                  {{ item.spec }}
                </td>
                <td class="text-right py-2 px-2">
                  {{ item.unit }}
                </td>
                <td class="text-right py-2 px-2">
                  {{ item.qty }}
                </td>
                <td class="py-2 px-2" style="color: var(--color-text-muted)">
                  {{ item.note }}
                </td>
              </tr>
            </tbody>
          </table>

          <div class="mt-3 flex gap-2">
            <button
              class="text-xs px-3 py-1.5 rounded transition-colors"
              style="background-color: var(--color-accent); color: white"
              onmouseover="this.style.opacity = '0.9'"
              onmouseout="this.style.opacity = '1'"
              @click="exportBOM"
            >
              导出BOM
            </button>
          </div>
        </div>
      </div>

      <!-- 备品备件 -->
      <div v-if="activeTab === 'spare'" class="space-y-4">
        <div class="grid grid-cols-3 gap-4">
          <div>
            <label class="block text-xs mb-1" style="color: var(--color-text-muted)">电池容量 (MWh)</label>
            <input
              v-model.number="spareData.batteryCapacity"
              type="number"
              class="w-full rounded px-3 py-2 text-sm"
              style="
                background-color: var(--color-input-bg-dark);
                border: 1px solid var(--color-input-border);
                color: var(--color-text);
              "
              onfocus="
                this.style.borderColor = 'var(--color-accent-secondary)'
                this.style.outline = 'none'
              "
              onblur="this.style.borderColor = 'var(--color-input-border)'"
            />
          </div>
          <div>
            <label class="block text-xs mb-1" style="color: var(--color-text-muted)">PCS数量</label>
            <input
              v-model.number="spareData.pcsQty"
              type="number"
              class="w-full rounded px-3 py-2 text-sm"
              style="
                background-color: var(--color-input-bg-dark);
                border: 1px solid var(--color-input-border);
                color: var(--color-text);
              "
              onfocus="
                this.style.borderColor = 'var(--color-accent-secondary)'
                this.style.outline = 'none'
              "
              onblur="this.style.borderColor = 'var(--color-input-border)'"
            />
          </div>
          <div>
            <label class="block text-xs mb-1" style="color: var(--color-text-muted)">运行年限</label>
            <input
              v-model.number="spareData.years"
              type="number"
              class="w-full rounded px-3 py-2 text-sm"
              style="
                background-color: var(--color-input-bg-dark);
                border: 1px solid var(--color-input-border);
                color: var(--color-text);
              "
              onfocus="
                this.style.borderColor = 'var(--color-accent-secondary)'
                this.style.outline = 'none'
              "
              onblur="this.style.borderColor = 'var(--color-input-border)'"
            />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-xs mb-1" style="color: var(--color-text-muted)">电池更换策略</label>
            <select
              v-model="spareData.batteryStrategy"
              class="w-full rounded px-3 py-2 text-sm"
              style="
                background-color: var(--color-input-bg-dark);
                border: 1px solid var(--color-input-border);
                color: var(--color-text);
              "
              onfocus="
                this.style.borderColor = 'var(--color-accent-secondary)'
                this.style.outline = 'none'
              "
              onblur="this.style.borderColor = 'var(--color-input-border)'"
            >
              <option value="aggressive">激进型 (SOH&lt;80%即换)</option>
              <option value="moderate">均衡型 (SOH(SOH&lt;75%换)</option>
              <option value="conservative">保守型 (SOH(SOH&lt;70%换)</option>
            </select>
          </div>
          <div>
            <label class="block text-xs mb-1" style="color: var(--color-text-muted)">PCS备件系数</label>
            <input
              v-model.number="spareData.pcsSpareFactor"
              type="number"
              step="0.01"
              min="0.02"
              class="w-full rounded px-3 py-2 text-sm"
              style="
                background-color: var(--color-input-bg-dark);
                border: 1px solid var(--color-input-border);
                color: var(--color-text);
              "
              onfocus="
                this.style.borderColor = 'var(--color-accent-secondary)'
                this.style.outline = 'none'
              "
              onblur="this.style.borderColor = 'var(--color-input-border)'"
            />
          </div>
        </div>

        <button
          class="text-xs px-4 py-2 rounded transition-colors"
          style="background-color: var(--color-accent-secondary); color: white"
          onmouseover="this.style.opacity = '0.9'"
          onmouseout="this.style.opacity = '1'"
          @click="calculateSpare"
        >
          计算备品备件
        </button>

        <!-- 备品备件结果 -->
        <div v-if="spareResult.length > 0" class="mt-4">
          <div class="text-xs mb-3" style="color: var(--color-text-muted)">备品备件清单</div>

          <div class="grid grid-cols-2 gap-4">
            <!-- 电池备件 -->
            <div class="rounded-lg p-3" style="background-color: var(--color-card-dark)">
              <div class="text-xs mb-2" style="color: var(--color-warning)">电池系统备件</div>
              <div
                v-for="(item, idx) in spareResult.filter((i) => i.type === 'battery')"
                :key="idx"
                class="flex justify-between text-xs py-1"
                style="border-bottom: 1px solid var(--color-border)"
              >
                <span style="color: var(--color-text-secondary)">{{ item.name }}</span>
                <span style="color: var(--color-text)">{{ item.qty }} {{ item.unit }}</span>
              </div>
            </div>

            <!-- PCS备件 -->
            <div class="rounded-lg p-3" style="background-color: var(--color-card-dark)">
              <div class="text-xs mb-2" style="color: var(--color-accent)">PCS系统备件</div>
              <div
                v-for="(item, idx) in spareResult.filter((i) => i.type === 'pcs')"
                :key="idx"
                class="flex justify-between text-xs py-1"
                style="border-bottom: 1px solid var(--color-border)"
              >
                <span style="color: var(--color-text-secondary)">{{ item.name }}</span>
                <span style="color: var(--color-text)">{{ item.qty }} {{ item.unit }}</span>
              </div>
            </div>
          </div>

          <div
            class="mt-4 p-3 rounded-lg"
            style="background-color: var(--color-accent-glow); border: 1px solid var(--color-accent-dark)"
          >
            <div class="text-xs" style="color: var(--color-accent-secondary)">预计备件库存总价值</div>
            <div class="text-xl font-bold mt-1" style="color: var(--color-accent-secondary)">
              ¥ {{ spareTotalValue.toLocaleString() }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast提示 -->
    <div
      v-if="toast.show"
      class="fixed bottom-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all"
      :style="{
        backgroundColor: toast.type === 'success' ? 'var(--color-success)' : 'var(--color-danger)',
        color: 'white'
      }"
    >
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { useDraft, useDraftRef } from '../composables/useDraft'

const emit = defineEmits(['error'])

const activeTab = useDraftRef('eng-active-tab', 'area').state
const tabs = [
  { id: 'area', label: '场地面积' },
  { id: 'bom', label: 'BOM清单' },
  { id: 'spare', label: '备品备件' }
]

const toast = reactive({
  show: false,
  message: '',
  type: 'success'
})

const showToast = (message, type = 'success') => {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => {
    toast.show = false
  }, 3000)
}

const { state: siteData } = useDraft('eng-site-data', {
  containerQty: 10,
  pcsQty: 5,
  transformerQty: 2,
  containerLength: 12,
  containerWidth: 2.5,
  containerHeight: 2.8,
  spacingFactor: 1.3
})

const siteAreaResult = ref(null)

function calculateSiteArea() {
  const containerArea = siteData.containerQty * siteData.containerLength * siteData.containerWidth
  const pcsArea = siteData.pcsQty * 5 * 3
  const transformerArea = siteData.transformerQty * 10

  const subtotal = containerArea + pcsArea + transformerArea
  const actualArea = subtotal * siteData.spacingFactor
  const landAcres = (actualArea / 666.67).toFixed(2)

  siteAreaResult.value = {
    containerArea: containerArea.toFixed(2),
    pcsArea: pcsArea.toFixed(2),
    totalArea: subtotal.toFixed(2),
    actualArea: actualArea.toFixed(2),
    landAcres
  }

  showToast('场地面积计算完成')
}

const { state: bomData } = useDraft('eng-bom-data', {
  energy: 100,
  containerQty: 10,
  pcsCapacity: 50,
  transformerCapacity: 60
})

watch(
  () => bomData.pcsCapacity,
  (val) => {
    bomData.pcsQty = Math.ceil(val / 5)
  },
  { immediate: true }
)

const bomResult = ref([])

function generateBOM() {
  const bom = []
  let seq = 1

  const batteryPerContainer = bomData.energy / bomData.containerQty
  bom.push({
    seq: seq++,
    name: '电芯',
    spec: `${((batteryPerContainer * 1000) / 280).toFixed(0)}S`,
    unit: '颗',
    qty: Math.ceil(((bomData.energy * 1000) / 280) * 1.05),
    note: '含5%备损'
  })

  bom.push({
    seq: seq++,
    name: '电池模组',
    spec: `${((batteryPerContainer * 1000) / 4.5).toFixed(0)}kWh`,
    unit: '个',
    qty: Math.ceil(bomData.containerQty * 1.1),
    note: '含10%备件'
  })

  bom.push({
    seq: seq++,
    name: '电池集装箱',
    spec: '20ft/40ft 标准集装箱',
    unit: '台',
    qty: bomData.containerQty,
    note: ''
  })

  bom.push({
    seq: seq++,
    name: 'BMS电池管理系统',
    spec: '主控+从控',
    unit: '套',
    qty: bomData.containerQty,
    note: ''
  })

  const pcsPerUnit = bomData.pcsCapacity / bomData.pcsQty
  bom.push({
    seq: seq++,
    name: 'PCS功率模块',
    spec: `${pcsPerUnit.toFixed(1)}MW`,
    unit: '台',
    qty: bomData.pcsQty,
    note: ''
  })

  bom.push({
    seq: seq++,
    name: 'PCS变压器',
    spec: `${(pcsPerUnit * 1.1).toFixed(1)}MVA`,
    unit: '台',
    qty: bomData.pcsQty,
    note: ''
  })

  bom.push({
    seq: seq++,
    name: '主变压器',
    spec: `${bomData.transformerCapacity}MVA`,
    unit: '台',
    qty: 2,
    note: '一用一备'
  })

  bom.push({
    seq: seq++,
    name: '直流电缆',
    spec: 'YJV-1kV',
    unit: '米',
    qty: Math.ceil(bomData.containerQty * 100),
    note: ''
  })

  bom.push({
    seq: seq++,
    name: '交流电缆',
    spec: 'YJV-35kV',
    unit: '米',
    qty: Math.ceil(bomData.pcsQty * 50),
    note: ''
  })

  bom.push({
    seq: seq++,
    name: 'EMS能量管理系统',
    spec: '主控单元',
    unit: '套',
    qty: 1,
    note: ''
  })

  bom.push({
    seq: seq++,
    name: '消防系统',
    spec: 'Pack级消防',
    unit: '套',
    qty: bomData.containerQty,
    note: ''
  })

  bom.push({
    seq: seq++,
    name: '温控系统',
    spec: '集装箱空调',
    unit: '台',
    qty: bomData.containerQty * 2,
    note: ''
  })

  bomResult.value = bom
  showToast('BOM清单已生成')
}

function exportBOM() {
  if (bomResult.value.length === 0) return

  let csv = '储能电站BOM清单\n\n'
  csv += '序号,设备名称,规格型号,单位,数量,备注\n'

  bomResult.value.forEach((item) => {
    csv += `${item.seq},${item.name},${item.spec},${item.unit},${item.qty},"${item.note}"\n`
  })

  const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8' })
  const url = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.download = `BOM_${new Date().toISOString().slice(0, 10)}.csv`
  link.href = url
  link.click()
  window.URL.revokeObjectURL(url)

  showToast('BOM已导出')
}

const { state: spareData } = useDraft('eng-spare-data', {
  batteryCapacity: 100,
  pcsQty: 5,
  years: 25,
  batteryStrategy: 'moderate',
  pcsSpareFactor: 0.05
})

const spareResult = ref([])

function calculateSpare() {
  const result = []

  const sohThreshold = {
    aggressive: 0.8,
    moderate: 0.75,
    conservative: 0.7
  }[spareData.batteryStrategy]

  const expectedReplacements = Math.floor(spareData.years / 10)

  result.push({
    type: 'battery',
    name: '电芯模组',
    qty: Math.ceil(spareData.batteryCapacity * expectedReplacements * 0.1),
    unit: 'kWh'
  })

  result.push({
    type: 'battery',
    name: '电池簇',
    qty: Math.ceil(expectedReplacements * 0.5),
    unit: '簇'
  })

  result.push({
    type: 'battery',
    name: 'BMS从控单元',
    qty: Math.ceil(spareData.batteryCapacity / 10),
    unit: '个'
  })

  result.push({
    type: 'battery',
    name: '电池直流开关',
    qty: Math.ceil(spareData.batteryCapacity / 20),
    unit: '个'
  })

  result.push({
    type: 'pcs',
    name: '功率模块IGBT',
    qty: Math.ceil(spareData.pcsQty * spareData.pcsSpareFactor * 2),
    unit: '个'
  })

  result.push({
    type: 'pcs',
    name: 'PCS控制器',
    qty: 1,
    unit: '个'
  })

  result.push({
    type: 'pcs',
    name: 'PCS滤波器',
    qty: Math.ceil(spareData.pcsQty * 0.2),
    unit: '个'
  })

  result.push({
    type: 'pcs',
    name: '接触器',
    qty: Math.ceil(spareData.pcsQty * 2),
    unit: '个'
  })

  result.push({
    type: 'pcs',
    name: '直流隔离开关',
    qty: Math.ceil(spareData.pcsQty * 0.5),
    unit: '个'
  })

  spareResult.value = result
  showToast('备品备件计算完成')
}

const spareTotalValue = computed(() => {
  let total = 0
  spareResult.value.forEach((item) => {
    if (item.type === 'battery') {
      total += item.qty * 2000
    } else {
      total += item.qty * 5000
    }
  })
  return total
})
</script>

<style scoped>
.engineering-calc {
  height: 100%;
}
</style>
