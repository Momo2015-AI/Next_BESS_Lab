<template>
  <div class="flex-1 overflow-auto bg-slate-900/80 rounded-xl p-4 border border-slate-800/80 space-y-4">
    <div>
      <h2 class="text-sm font-bold text-teal-400 border-l-4 border-teal-500 pl-2 mb-3">系统参数配置</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">标称单舱能量 (MWh)</label>
          <input type="number" :value="params.ratedEnergy" step="0.1"
            class="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1.5 text-teal-300 font-mono focus:outline-none focus:border-teal-500"
            @input="$emit('update', 'ratedEnergy', Number($event.target.value))">
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">初始集装箱数量 (台)</label>
          <input type="number" :value="params.initContainerQty" step="1"
            class="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1.5 text-teal-300 font-mono focus:outline-none focus:border-teal-500"
            @input="$emit('update', 'initContainerQty', Number($event.target.value))">
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">PCS变流数量 (台)</label>
          <input type="number" :value="params.initPcsQty" step="1"
            class="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1.5 text-teal-300 font-mono focus:outline-none focus:border-teal-500"
            @input="$emit('update', 'initPcsQty', Number($event.target.value))">
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">单程充电时间 (h)</label>
          <input type="number" :value="params.duration" step="0.5"
            class="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1.5 text-teal-300 font-mono focus:outline-none focus:border-teal-500"
            @input="$emit('update', 'duration', Number($event.target.value))">
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">单日循环次数 (次)</label>
          <input type="number" :value="params.cyclesPerDay" step="1"
            class="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1.5 text-teal-300 font-mono focus:outline-none focus:border-teal-500"
            @input="$emit('update', 'cyclesPerDay', Number($event.target.value))">
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">网侧AC效率 (%)</label>
          <input type="number" :value="params.acEfficiency" step="0.01"
            class="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1.5 text-teal-300 font-mono focus:outline-none focus:border-teal-500"
            @input="$emit('update', 'acEfficiency', Number($event.target.value))">
        </div>
      </div>
    </div>

    <div>
      <h2 class="text-sm font-bold text-amber-400 border-l-4 border-amber-500 pl-2 mb-3">自辅耗功率设定</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">集装箱运行功率 (kW)</label>
          <input type="number" :value="params.bessAuxRun" step="0.001"
            class="w-full bg-slate-950 border border-amber-900/60 rounded px-2 py-1.5 text-amber-300 font-mono focus:outline-none focus:border-amber-500"
            @input="$emit('update', 'bessAuxRun', Number($event.target.value))">
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">集装箱待机功率 (kW)</label>
          <input type="number" :value="params.bessAuxStandby" step="0.1"
            class="w-full bg-slate-950 border border-amber-900/60 rounded px-2 py-1.5 text-amber-300 font-mono focus:outline-none focus:border-amber-500"
            @input="$emit('update', 'bessAuxStandby', Number($event.target.value))">
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">PCS运行功率 (kW)</label>
          <input type="number" :value="params.pcsAuxRun" step="0.1"
            class="w-full bg-slate-950 border border-amber-900/60 rounded px-2 py-1.5 text-amber-300 font-mono focus:outline-none focus:border-amber-500"
            @input="$emit('update', 'pcsAuxRun', Number($event.target.value))">
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">PCS待机功率 (kW)</label>
          <input type="number" :value="params.pcsAuxStandby" step="0.1"
            class="w-full bg-slate-950 border border-amber-900/60 rounded px-2 py-1.5 text-amber-300 font-mono focus:outline-none focus:border-amber-500"
            @input="$emit('update', 'pcsAuxStandby', Number($event.target.value))">
        </div>
      </div>

      <div class="mt-3 p-3 bg-slate-950 border border-slate-800 rounded-lg font-mono text-[11px] text-slate-300 space-y-1">
        <div class="text-amber-400 font-bold text-[10px]">自辅耗时轴计算推导：</div>
        <div>
          日运行总时长 = {{ params.duration }}h × {{ params.cyclesPerDay }}次 = <span class="text-sky-300 font-bold">{{ (params.duration * params.cyclesPerDay).toFixed(1) }}h</span>
          &nbsp;日待机时长 = Max(0, 24 - {{ (params.duration * params.cyclesPerDay).toFixed(1) }}) = <span class="text-sky-300 font-bold">{{ Math.max(0, 24 - params.duration * params.cyclesPerDay).toFixed(1) }}h</span>
        </div>
        <div>
          单舱日辅耗 = ({{ params.bessAuxRun }}kW × {{ (params.duration * params.cyclesPerDay).toFixed(1) }}h + {{ params.bessAuxStandby }}kW × {{ Math.max(0, 24 - params.duration * params.cyclesPerDay).toFixed(1) }}h) / 1000
          = <span class="text-amber-300 font-bold">{{ ((params.bessAuxRun * params.duration * params.cyclesPerDay + params.bessAuxStandby * Math.max(0, 24 - params.duration * params.cyclesPerDay)) / 1000).toFixed(3) }} MWh/天</span>
        </div>
        <div>
          单PCS日辅耗 = ({{ params.pcsAuxRun }}kW × {{ (params.duration * params.cyclesPerDay).toFixed(1) }}h + {{ params.pcsAuxStandby }}kW × {{ Math.max(0, 24 - params.duration * params.cyclesPerDay).toFixed(1) }}h) / 1000
          = <span class="text-amber-300 font-bold">{{ ((params.pcsAuxRun * params.duration * params.cyclesPerDay + params.pcsAuxStandby * Math.max(0, 24 - params.duration * params.cyclesPerDay)) / 1000).toFixed(3) }} MWh/天</span>
        </div>
        <div class="pt-1 border-t border-slate-800">
          单次循环总自辅耗 = <span class="text-emerald-300 font-bold">
            ({{ params.initContainerQty }}台 × 单舱日辅耗 + {{ params.initPcsQty }}台 × 单PCS日辅耗) / {{ params.cyclesPerDay }}次
          </span>
        </div>
      </div>
    </div>

    <div>
      <h2 class="text-sm font-bold text-pink-400 border-l-4 border-pink-500 pl-2 mb-3">仿真条件边界</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">运行平均温度 (°C)</label>
          <input type="number" value="25" step="1" disabled
            class="w-full bg-slate-900 border border-slate-800 rounded px-2 py-1.5 text-slate-500 font-mono cursor-not-allowed">
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">平均放电倍率</label>
          <input type="number" value="0.5" step="0.1" disabled
            class="w-full bg-slate-900 border border-slate-800 rounded px-2 py-1.5 text-slate-500 font-mono cursor-not-allowed">
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">SOH/RTE起始年份</label>
          <input type="text" value="FOB + 6个月" disabled
            class="w-full bg-slate-900 border border-slate-800 rounded px-2 py-1.5 text-slate-500 font-mono cursor-not-allowed">
        </div>
        <div>
          <label class="block text-[10px] text-slate-400 mb-0.5">承诺保障线 (MWh/次)</label>
          <input type="number" :value="params.requiredEnergy" step="1"
            class="w-full bg-slate-950 border border-emerald-900/60 rounded px-2 py-1.5 text-emerald-300 font-mono focus:outline-none focus:border-emerald-500"
            @input="$emit('update', 'requiredEnergy', Number($event.target.value))">
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ params: Object })
defineEmits(['update'])
</script>
