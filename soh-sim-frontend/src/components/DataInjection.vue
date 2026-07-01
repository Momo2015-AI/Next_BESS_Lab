<template>
  <div class="flex-1 overflow-auto rounded-xl p-4 space-y-4 card">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div
        class="p-3 rounded-lg flex flex-col"
        style="background: var(--color-bg-secondary); border: 1px solid var(--color-border)"
      >
        <span class="text-xs font-bold mb-1" style="color: #f59e0b">{{ $t('dataInjection.sohTitle') }}</span>
        <p class="text-[10px] mb-2" style="color: var(--color-text-muted)">
          {{ $t('dataInjection.sohFormat') }}
        </p>
        <textarea
          v-model="sohText"
          class="flex-1 w-full min-h-[200px] rounded p-2 text-xs font-mono focus:outline-none resize-none"
          style="background: var(--color-input-bg); border: 1px solid var(--color-input-border); color: #f59e0b"
          placeholder="0.9925&#10;0.9318&#10;0.9014..."
        />
        <div class="flex gap-2 mt-2">
          <button
            class="flex-1 font-bold py-1.5 rounded text-xs transition-all"
            style="background: #d97706; color: white"
            @click="parseSoh"
          >
            {{ $t('dataInjection.parseSoh') }}
          </button>
          <button
            class="px-3 py-1.5 rounded text-xs transition-all"
            style="
              background: var(--color-bg-secondary);
              color: var(--color-text-secondary);
              border: 1px solid var(--color-border);
            "
            @click="resetSoh"
          >
            {{ $t('dataInjection.resetDefault') }}
          </button>
        </div>
      </div>
      <div
        class="p-3 rounded-lg flex flex-col"
        style="background: var(--color-bg-secondary); border: 1px solid var(--color-border)"
      >
        <span class="text-xs font-bold mb-1" style="color: var(--color-accent-secondary)">
          {{ $t('dataInjection.rteTitle') }}
        </span>
        <p class="text-[10px] mb-2" style="color: var(--color-text-muted)">
          {{ $t('dataInjection.rteFormat') }}
        </p>
        <textarea
          v-model="rteText"
          class="flex-1 w-full min-h-[200px] rounded p-2 text-xs font-mono focus:outline-none resize-none"
          style="
            background: var(--color-input-bg);
            border: 1px solid var(--color-input-border);
            color: var(--color-accent-secondary);
          "
          placeholder="0.941&#10;0.9384&#10;0.9372..."
        />
        <div class="flex gap-2 mt-2">
          <button
            class="flex-1 font-bold py-1.5 rounded text-xs transition-all"
            style="background: var(--color-accent-secondary); color: white"
            @click="parseRte"
          >
            {{ $t('dataInjection.parseRte') }}
          </button>
          <button
            class="px-3 py-1.5 rounded text-xs transition-all"
            style="
              background: var(--color-bg-secondary);
              color: var(--color-text-secondary);
              border: 1px solid var(--color-border);
            "
            @click="resetRte"
          >
            {{ $t('dataInjection.resetDefault') }}
          </button>
        </div>
      </div>
    </div>
    <div class="p-3 rounded-lg" style="background: var(--color-bg-secondary); border: 1px solid var(--color-border)">
      <span class="text-xs font-bold" style="color: var(--color-text-secondary)">
        {{ $t('dataInjection.currentPreview') }}
      </span>
      <div class="grid grid-cols-2 gap-4 mt-2 text-[11px] font-mono">
        <div class="overflow-auto max-h-32">
          <div class="font-bold mb-1" style="color: #f59e0b">
            {{ $t('dataInjection.sohLabel') }}
          </div>
          <div class="grid grid-cols-7 gap-x-1 gap-y-0.5">
            <div v-for="(v, i) in soh" :key="'s-' + i" style="color: #d97706">
              {{ 'Y' + i }}:{{ (v * 100).toFixed(1) }}%
            </div>
          </div>
        </div>
        <div class="overflow-auto max-h-32">
          <div class="font-bold mb-1" style="color: var(--color-accent-secondary)">
            {{ $t('dataInjection.rteLabel') }}
          </div>
          <div class="grid grid-cols-7 gap-x-1 gap-y-0.5">
            <div v-for="(v, i) in rte" :key="'r-' + i" style="color: var(--color-accent-secondary)">
              {{ 'Y' + i }}:{{ (v * 100).toFixed(1) }}%
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({ soh: Array, rte: Array })
const emit = defineEmits(['update:soh', 'update:rte'])

const defaultSoh = [
  0.9925, 0.9318, 0.9014, 0.877, 0.856, 0.8371, 0.8197, 0.8036, 0.7885, 0.7742, 0.7606, 0.7475, 0.735, 0.723, 0.7113,
  0.7, 0.689, 0.678, 0.6672, 0.6564, 0.6458, 0.6354, 0.6252, 0.6152, 0.6074, 0.6008
]
const defaultRte = [
  0.941, 0.9384, 0.9372, 0.9363, 0.9355, 0.9347, 0.934, 0.9333, 0.9326, 0.932, 0.9314, 0.9308, 0.9302, 0.9296, 0.929,
  0.9285, 0.9279, 0.9273, 0.9268, 0.9262, 0.9256, 0.9251, 0.9245, 0.924, 0.9235, 0.923
]

const sohText = ref(defaultSoh.map((v) => v.toFixed(4)).join('\n'))
const rteText = ref(defaultRte.map((v) => v.toFixed(4)).join('\n'))

function parseSequence(raw) {
  const arr = raw
    .split(/[\n,;\t]+/)
    .map((v) => v.replace('%', '').trim())
    .filter(Boolean)
    .map(Number)
  if (arr.length === 0) return null
  const result = new Array(26).fill(0)
  for (let i = 0; i < 26; i++) {
    const v = arr[i] ?? arr[arr.length - 1]
    result[i] = v > 1 ? v / 100 : v
  }
  return result
}

function parseSoh() {
  const arr = parseSequence(sohText.value)
  if (arr) emit('update:soh', arr)
}
function parseRte() {
  const arr = parseSequence(rteText.value)
  if (arr) emit('update:rte', arr)
}
function resetSoh() {
  emit('update:soh', defaultSoh.slice())
  sohText.value = defaultSoh.map((v) => v.toFixed(4)).join('\n')
}
function resetRte() {
  emit('update:rte', defaultRte.slice())
  rteText.value = defaultRte.map((v) => v.toFixed(4)).join('\n')
}
</script>
