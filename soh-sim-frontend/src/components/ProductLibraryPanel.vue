<template>
  <div class="rounded-lg p-4 card-panel">
    <div class="flex items-center gap-2 mb-3">
      <span class="w-6 h-6 rounded flex items-center justify-center font-bold text-xs" :class="badgeClass">
        {{ badge }}
      </span>
      <div>
        <h3 class="font-bold text-sm">
          {{ title }}
          <span class="text-[10px] font-normal ml-1 text-muted">{{ subtitle }}</span>
        </h3>
      </div>
      <div class="ml-auto flex gap-2">
        <select v-if="showMfrFilter" v-model="mfrFilter" class="text-xs rounded px-2 py-1 form-field-select">
          <option value="">{{ $t('productConfig.allVendors') }}</option>
          <option v-for="m in mfrList" :key="m" :value="m">{{ m }}</option>
        </select>
        <select v-if="showPowerFilter" v-model="powerFilter" class="text-xs rounded px-2 py-1 form-field-select">
          <option value="0">{{ $t('productConfig.allPower') }}</option>
          <option value="1.25">{{ $t('productConfig.power1_25') }}</option>
          <option value="1.725">{{ $t('productConfig.power1_725') }}</option>
          <option value="2.5">{{ $t('productConfig.power2_5') }}</option>
          <option value="3.45">{{ $t('productConfig.power3_45') }}</option>
        </select>
        <button
          v-if="showAddBtn"
          class="text-[10px] px-2 py-1 rounded transition-colors"
          :class="addBtnClass"
          @click="$emit('add')"
        >
          {{ addLabel }}
        </button>
      </div>
    </div>
    <div :class="['grid gap-2', gridClass]">
      <ProductCard
        v-for="item in filteredItems"
        :key="item.id"
        :item="item"
        :type="itemType"
        :selected="selectedId === item.id"
        :deletable="deletable"
        :accent-color="accentColor"
        :accent-glow="accentGlow"
        @select="$emit('select', item.id)"
        @delete="$emit('delete', item.id)"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import ProductCard from './ProductCard.vue'

const props = defineProps({
  badge: { type: String, default: '' },
  badgeClass: { type: String, default: 'tag-glow text-accent-secondary' },
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  items: { type: Array, default: () => [] },
  itemType: { type: String, required: true },
  selectedId: { type: String, default: '' },
  mfrList: { type: Array, default: () => [] },
  showMfrFilter: { type: Boolean, default: true },
  showPowerFilter: { type: Boolean, default: false },
  showAddBtn: { type: Boolean, default: true },
  addLabel: { type: String, default: '' },
  addBtnClass: { type: String, default: '' },
  deletable: { type: Boolean, default: true },
  gridClass: { type: String, default: 'grid-cols-3' },
  accentColor: { type: String, default: 'var(--color-accent-secondary)' },
  accentGlow: { type: String, default: 'var(--color-accent-glow)' }
})

defineEmits(['select', 'delete', 'add'])

const mfrFilter = defineModel('mfrFilter', { type: String, default: '' })
const powerFilter = defineModel('powerFilter', { type: String, default: '0' })

const filteredItems = computed(() => {
  let list = props.items
  if (mfrFilter.value) list = list.filter((c) => c.mfr === mfrFilter.value)
  if (props.itemType === 'pcs' && powerFilter.value && powerFilter.value !== '0') {
    list = list.filter((p) => p.ratedPowerMW === Number(powerFilter.value))
  }
  return list
})
</script>
