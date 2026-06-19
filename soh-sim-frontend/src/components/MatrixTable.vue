<template>
  <div class="flex-1 min-h-0 flex flex-col">
    <div class="bg-slate-900/80 rounded-xl p-3 border border-slate-800/80 flex-shrink-0 mb-3">
      <div class="grid grid-cols-3 md:grid-cols-6 gap-3">
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">标称单舱 (MWh)</label>
          <input type="number" :value="params.ratedEnergy" step="0.1"
            class="w-full bg-slate-950 border border-slate-800 rounded px-2 py-1 text-teal-300 font-mono focus:outline-none text-[11px]"
            disabled>
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">初始集装箱数</label>
          <input type="number" :value="params.initContainerQty"
            class="w-full bg-slate-950 border border-slate-800 rounded px-2 py-1 text-teal-300 font-mono focus:outline-none text-[11px]"
            disabled>
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">PCS数量</label>
          <input type="number" :value="params.initPcsQty"
            class="w-full bg-slate-950 border border-slate-800 rounded px-2 py-1 text-teal-300 font-mono focus:outline-none text-[11px]"
            disabled>
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">单程时长 (h)</label>
          <input type="number" :value="params.duration" step="0.5"
            class="w-full bg-slate-950 border border-slate-800 rounded px-2 py-1 text-teal-300 font-mono focus:outline-none text-[11px]"
            disabled>
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">日循环次数</label>
          <input type="number" :value="params.cyclesPerDay" step="1"
            class="w-full bg-slate-950 border border-slate-800 rounded px-2 py-1 text-teal-300 font-mono focus:outline-none text-[11px]"
            disabled>
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">网侧AC效率 (%)</label>
          <input type="number" :value="params.acEfficiency" step="0.01"
            class="w-full bg-slate-950 border border-slate-800 rounded px-2 py-1 text-teal-300 font-mono focus:outline-none text-[11px]"
            disabled>
        </div>
      </div>
    </div>

    <div class="flex-1 min-h-0 overflow-auto border border-slate-800 rounded-xl bg-slate-900/40">
      <table class="w-full text-left border-collapse min-w-[1500px]">
        <thead>
          <tr class="bg-slate-950 text-center border-b border-slate-800 text-[10px] font-bold text-slate-400 sticky top-0 z-30">
            <th class="py-1.5 border-r border-slate-800" colspan="1">时间</th>
            <th class="py-1.5 bg-blue-950/30 border-r border-slate-800 text-blue-400" colspan="8">Initial Stock (存量设备)</th>
            <th class="py-1.5 bg-pink-950/20 border-r border-slate-800 text-pink-400" colspan="6">Augmentation Stream (补容资产)</th>
            <th class="py-1.5 bg-emerald-950/30 text-emerald-400" colspan="3">Total Accounting (综合轧账)</th>
          </tr>
          <tr class="bg-slate-950/90 text-[10px] font-semibold text-slate-300 border-b border-slate-800 text-center sticky top-[31px] z-30">
            <th class="p-1.5 border-r border-slate-800 bg-slate-950">年份</th>
            <th class="p-1.5 bg-blue-950/10">标称容量</th>
            <th class="p-1.5 bg-blue-950/10 text-orange-400">DOD%</th>
            <th class="p-1.5 bg-blue-950/10 text-sky-400">RTE%</th>
            <th class="p-1.5 bg-blue-950/10 text-yellow-400">SOH%</th>
            <th class="p-1.5 bg-blue-950/10">初始舱数</th>
            <th class="p-1.5 bg-blue-950/10">粗放电量</th>
            <th class="p-1.5 bg-blue-950/10 text-red-400">循环分摊辅耗</th>
            <th class="p-1.5 bg-blue-950/10 border-r border-slate-800 text-teal-400 font-bold">存量网侧净可用</th>
            <th class="p-1.5 bg-pink-950/10">补容标称</th>
            <th class="p-1.5 bg-pink-950/10 text-pink-400 font-bold">当季补容台数</th>
            <th class="p-1.5 bg-pink-950/10">累计台数</th>
            <th class="p-1.5 bg-pink-950/10 text-red-400">补容辅耗</th>
            <th class="p-1.5 bg-pink-950/10 text-pink-400">补容粗放</th>
            <th class="p-1.5 bg-pink-950/10 border-r border-slate-800 text-pink-400 font-bold">补容网侧净可用</th>
            <th class="p-1.5 bg-emerald-950/10 font-bold text-emerald-400">总网侧净输出</th>
            <th class="p-1.5 bg-emerald-950/10">是否达标</th>
            <th class="p-1.5 bg-emerald-950/10">承诺底线</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-850 text-[11px] font-mono">
          <tr v-for="i in 26" :key="i-1" class="hover:bg-slate-800/30 transition-all text-center">
            <td class="p-1 font-bold text-slate-500 border-r border-slate-800 bg-slate-950 sticky left-0 z-10">{{ i - 1 }}</td>

            <!-- 存量设备 -->
            <td class="p-1 text-slate-400">{{ params.ratedEnergy.toFixed(1) }}</td>
            <td class="p-0.5 bg-slate-900">
              <input type="number" :value="dod[i-1]" step="0.1"
                class="w-12 bg-slate-950 border border-slate-800 rounded text-center text-orange-400 font-mono text-[11px]"
                @input="updateDod(i-1, $event.target.value)">
            </td>
            <td class="p-0.5 bg-slate-900">
              <input type="number" :value="(rte[i-1]*100).toFixed(2)" step="0.01"
                class="w-14 bg-slate-950 border border-slate-800 rounded text-center text-sky-400 font-mono text-[11px]"
                @input="updateRte(i-1, $event.target.value)">
            </td>
            <td class="p-0.5 bg-slate-900">
              <input type="number" :value="(soh[i-1]*100).toFixed(2)" step="0.01"
                class="w-14 bg-slate-950 border border-slate-800 rounded text-center text-yellow-400 font-bold font-mono text-[11px]"
                @input="updateSoh(i-1, $event.target.value)">
            </td>
            <td class="p-1 text-slate-400">{{ params.initContainerQty }}</td>
            <td class="p-1 text-slate-300">{{ results.initGross[i-1]?.toFixed(2) }}</td>
            <td class="p-1 text-red-400 font-semibold">{{ results.initAux[i-1]?.toFixed(2) }}</td>
            <td class="p-1 font-bold text-teal-400 border-r border-slate-800 bg-slate-900/20">{{ results.initAcUsable[i-1]?.toFixed(2) }}</td>

            <!-- 补容资产 -->
            <td class="p-1 text-slate-500">{{ params.ratedEnergy.toFixed(1) }}</td>
            <td class="p-0.5 bg-slate-900">
              <input type="number" :value="augQty[i-1]" step="1" min="0"
                class="w-10 bg-slate-950 border border-pink-950 rounded text-center text-pink-400 font-bold text-[11px]"
                @input="updateAugQty(i-1, $event.target.value)">
            </td>
            <td class="p-1 text-slate-500">{{ results.augAccumQty[i-1] }}</td>
            <td class="p-1 text-red-400 font-semibold">{{ results.augAux[i-1]?.toFixed(2) }}</td>
            <td class="p-1 text-slate-400">{{ results.augGross[i-1]?.toFixed(2) }}</td>
            <td class="p-1 font-bold text-pink-400 border-r border-slate-800 bg-slate-900/10">{{ results.augAcUsable[i-1]?.toFixed(2) }}</td>

            <!-- 综合轧账 -->
            <td class="p-1 font-bold text-xs" :class="results.meetsReq[i-1] ? 'text-teal-400' : 'text-red-500'">
              {{ results.totalAcUsable[i-1]?.toFixed(2) }}
            </td>
            <td class="p-1 font-bold" :class="results.meetsReq[i-1] ? 'text-emerald-400 bg-emerald-950/20' : 'text-red-400 bg-red-950/30'">
              {{ results.meetsReq[i-1] ? 'Yes' : 'No' }}
            </td>
            <td class="p-1 text-amber-500 font-semibold">{{ params.requiredEnergy.toFixed(2) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({ params: Object, results: Object, soh: Array, rte: Array, dod: Array, augQty: Array })
const emit = defineEmits(['update:soh', 'update:rte', 'update:dod', 'update:augQty'])

function updateDod(idx, val) {
  const newArr = [...props.dod]
  newArr[idx] = Number(val) || 0
  emit('update:dod', newArr)
}
function updateRte(idx, val) {
  const newArr = [...props.rte]
  newArr[idx] = (Number(val) || 0) / 100
  emit('update:rte', newArr)
}
function updateSoh(idx, val) {
  const newArr = [...props.soh]
  newArr[idx] = (Number(val) || 0) / 100
  emit('update:soh', newArr)
}
function updateAugQty(idx, val) {
  const newArr = [...props.augQty]
  newArr[idx] = parseInt(val) || 0
  emit('update:augQty', newArr)
}
</script>
