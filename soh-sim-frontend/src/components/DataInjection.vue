<template>
  <div class="flex-1 overflow-auto bg-slate-900/80 rounded-xl p-4 border border-slate-800/80 space-y-4">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="bg-slate-950 p-3 rounded-lg border border-slate-800 flex flex-col">
        <span class="text-xs font-bold text-yellow-400 mb-1">SOH 25年衰减序列 (逐行粘贴)</span>
        <p class="text-[10px] text-slate-500 mb-2">格式：每行一个数值（支持逗号/分号/制表符分隔），不足26位用末位补全</p>
        <textarea v-model="sohText" class="flex-1 w-full min-h-[200px] bg-slate-900 border border-slate-700 rounded p-2 text-xs font-mono text-yellow-300 focus:outline-none resize-none"
          placeholder="0.9925&#10;0.9318&#10;0.9014..."></textarea>
        <div class="flex gap-2 mt-2">
          <button @click="parseSoh" class="flex-1 bg-yellow-600 hover:bg-yellow-500 text-slate-950 font-bold py-1.5 rounded text-xs transition-all">解析推入 SOH</button>
          <button @click="resetSoh" class="px-3 bg-slate-800 hover:bg-slate-700 text-slate-300 py-1.5 rounded text-xs transition-all">重置默认</button>
        </div>
      </div>
      <div class="bg-slate-950 p-3 rounded-lg border border-slate-800 flex flex-col">
        <span class="text-xs font-bold text-sky-400 mb-1">RTE 系统效率序列 (逐行粘贴)</span>
        <p class="text-[10px] text-slate-500 mb-2">格式：每行一个数值（支持逗号/分号/制表符分隔），不足26位用末位补全</p>
        <textarea v-model="rteText" class="flex-1 w-full min-h-[200px] bg-slate-900 border border-slate-700 rounded p-2 text-xs font-mono text-sky-300 focus:outline-none resize-none"
          placeholder="0.941&#10;0.9384&#10;0.9372..."></textarea>
        <div class="flex gap-2 mt-2">
          <button @click="parseRte" class="flex-1 bg-sky-600 hover:bg-sky-500 text-slate-950 font-bold py-1.5 rounded text-xs transition-all">解析推入 RTE</button>
          <button @click="resetRte" class="px-3 bg-slate-800 hover:bg-slate-700 text-slate-300 py-1.5 rounded text-xs transition-all">重置默认</button>
        </div>
      </div>
    </div>
    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
      <span class="text-xs font-bold text-slate-400">当前 SOH & RTE 序列预览 (Year 0-25)</span>
      <div class="grid grid-cols-2 gap-4 mt-2 text-[11px] font-mono">
        <div class="overflow-auto max-h-32">
          <div class="text-yellow-400 font-bold mb-1">SOH:</div>
          <div class="grid grid-cols-7 gap-x-1 gap-y-0.5">
            <div v-for="(v, i) in soh" :key="'s-'+i" class="text-yellow-300/70">{{ 'Y'+i }}:{{ (v*100).toFixed(1) }}%</div>
          </div>
        </div>
        <div class="overflow-auto max-h-32">
          <div class="text-sky-400 font-bold mb-1">RTE:</div>
          <div class="grid grid-cols-7 gap-x-1 gap-y-0.5">
            <div v-for="(v, i) in rte" :key="'r-'+i" class="text-sky-300/70">{{ 'Y'+i }}:{{ (v*100).toFixed(1) }}%</div>
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

const defaultSoh = [0.9925, 0.9318, 0.9014, 0.877, 0.856, 0.8371, 0.8197, 0.8036, 0.7885, 0.7742, 0.7606, 0.7475, 0.735, 0.723, 0.7113, 0.7, 0.689, 0.678, 0.6672, 0.6564, 0.6458, 0.6354, 0.6252, 0.6152, 0.6074, 0.6008]
const defaultRte = [0.941, 0.9384, 0.9372, 0.9363, 0.9355, 0.9347, 0.934, 0.9333, 0.9326, 0.932, 0.9314, 0.9308, 0.9302, 0.9296, 0.929, 0.9285, 0.9279, 0.9273, 0.9268, 0.9262, 0.9256, 0.9251, 0.9245, 0.924, 0.9235, 0.923]

const sohText = ref(defaultSoh.map(v => v.toFixed(4)).join('\n'))
const rteText = ref(defaultRte.map(v => v.toFixed(4)).join('\n'))

function parseSequence(raw) {
  const arr = raw.split(/[\n,;\t]+/).map(v => v.replace('%', '').trim()).filter(Boolean).map(Number)
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
  sohText.value = defaultSoh.map(v => v.toFixed(4)).join('\n')
}
function resetRte() {
  emit('update:rte', defaultRte.slice())
  rteText.value = defaultRte.map(v => v.toFixed(4)).join('\n')
}
</script>
