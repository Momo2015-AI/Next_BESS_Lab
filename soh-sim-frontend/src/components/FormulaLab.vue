<template>
  <div class="flex-1 overflow-auto bg-slate-900/80 rounded-xl p-4 border border-slate-800/80 space-y-3">
    <div>
      <h2 class="text-sm font-bold text-teal-400 uppercase tracking-wider border-l-4 border-teal-500 pl-2">核心物理公式仿真沙盒</h2>
      <p class="text-[11px] text-slate-400 mt-0.5">修改虚线框内数值，全栈穿透重算整个对账矩阵</p>
    </div>

    <div class="bg-slate-950 p-3 rounded-lg border border-blue-900/40 space-y-1.5">
      <div class="text-[11px] font-bold text-blue-400">
        算子 1 — 存量资产单次循环粗放电量公式 (Gross Discharge Energy)
      </div>
      <div class="p-2.5 bg-slate-900/80 rounded font-mono leading-relaxed overflow-x-auto border border-slate-850 text-slate-300 text-[11px]">
        E<sub>gross</sub>(i) =
        <input type="number" :value="params.ratedEnergy" step="0.1" class="formula-input w-12"
          @input="$emit('update', 'ratedEnergy', Number($event.target.value))"> MWh
        × <input type="number" :value="params.initContainerQty" step="1" class="formula-input w-14"
          @input="$emit('update', 'initContainerQty', Number($event.target.value))"> 台
        × SOH(i) × RTE(i) × DOD(i)
        × ( <input type="number" :value="params.acEfficiency" step="0.01" class="formula-input w-14"
          @input="$emit('update', 'acEfficiency', Number($event.target.value))"> / 100 )
      </div>
    </div>

    <div class="bg-slate-950 p-3 rounded-lg border border-amber-900/40 space-y-2">
      <div class="text-[11px] font-bold text-amber-400">
        算子 2 — 高精度时轴动静态复合自辅耗平摊校核模型
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3 font-mono text-[11px]">
        <div class="p-2 bg-slate-900/80 rounded border border-slate-850 space-y-1">
          <span class="text-amber-500 font-bold block text-[10px]">A. 运行待机时间轴：</span>
          <div>单日运行总时长 (RunHours) =
            <input type="number" :value="params.duration" step="0.5" class="formula-input w-10"
              @input="$emit('update', 'duration', Number($event.target.value))"> h ×
            <input type="number" :value="params.cyclesPerDay" step="1" class="formula-input w-8"
              @input="$emit('update', 'cyclesPerDay', Number($event.target.value))"> 次
          </div>
          <div class="pt-0.5 border-t border-slate-800">剩余静态待机时长 (StandbyHours) = Max(0, 24 - RunHours)</div>
        </div>
        <div class="p-2 bg-slate-900/80 rounded border border-slate-850 space-y-1">
          <span class="text-amber-500 font-bold block text-[10px]">B. 单体设备设定功率：</span>
          <div class="grid grid-cols-2 gap-x-2 text-[10px]">
            <div>集装箱运行: <input type="number" :value="params.bessAuxRun" step="0.001" class="formula-input w-16"
              @input="$emit('update', 'bessAuxRun', Number($event.target.value))"> kW</div>
            <div>集装箱待机: <input type="number" :value="params.bessAuxStandby" step="0.1" class="formula-input w-12"
              @input="$emit('update', 'bessAuxStandby', Number($event.target.value))"> kW</div>
            <div>PCS运行: <input type="number" :value="params.pcsAuxRun" step="0.1" class="formula-input w-12"
              @input="$emit('update', 'pcsAuxRun', Number($event.target.value))"> kW</div>
            <div>PCS待机: <input type="number" :value="params.pcsAuxStandby" step="0.1" class="formula-input w-12"
              @input="$emit('update', 'pcsAuxStandby', Number($event.target.value))"> kW</div>
          </div>
        </div>
      </div>
      <div class="p-2.5 bg-slate-900/80 rounded font-mono leading-relaxed overflow-x-auto border border-slate-850 text-slate-300 text-[11px]">
        Aux<sub>total</sub> = { 箱数 × [(运行功率 × RunHours + 待机功率 × StandbyHours) / 1000] +
        <input type="number" :value="params.initPcsQty" step="1" class="formula-input w-12"
          @input="$emit('update', 'initPcsQty', Number($event.target.value))"> 台
        × [(PCS运行 × RunHours + PCS待机 × StandbyHours) / 1000] } / 循环次数
      </div>
    </div>

    <div class="bg-slate-950 p-3 rounded-lg border border-pink-900/40 space-y-1.5">
      <div class="text-[11px] font-bold text-pink-400">
        算子 3 — 动态扩容资产流役龄位移追踪模型 (Augmentation Aging Displacement)
      </div>
      <div class="p-2.5 bg-slate-900/80 rounded font-mono overflow-x-auto border border-slate-850 text-slate-300 text-[11px]">
        在第 k 年投入的资产，当前计算年份 i 时的衰减表现：
        <div class="my-1 p-1.5 bg-slate-950 rounded border border-slate-850 text-pink-300 text-[10px]">
          相对役龄跨度 (Age) = i - k；动态追溯对应状态：SOH<sub>target</sub> = SOH[Age]
        </div>
        E<sub>aug_net</sub>(i) = Σ<sub>(k≤i)</sub> [ 标称能量 × 投入箱数 × SOH<sub>target</sub> × RTE(i) × DOD(i) × η<sub>ac</sub> - 投入箱数 × 单舱单次辅耗 ]
      </div>
    </div>

    <div class="bg-slate-950 p-3 rounded-lg border border-emerald-900/40 space-y-1.5">
      <div class="text-[11px] font-bold text-emerald-400">
        算子 4 — 全周期单次循环净放电对账底线判定
      </div>
      <div class="p-2.5 bg-slate-900/80 rounded font-mono overflow-x-auto border border-slate-850 text-slate-300 text-[11px]">
        E<sub>net_total</sub>(i) = Max(0, E<sub>gross_init</sub> - Aux<sub>init</sub>) + E<sub>aug_net</sub>(i)
        <div class="mt-1 text-slate-400">
          判定判据：E<sub>net_total</sub>(i) ≥
          <input type="number" :value="params.requiredEnergy" step="1" class="formula-input w-14 text-amber-400"
            @input="$emit('update', 'requiredEnergy', Number($event.target.value))"> MWh
          ? <span class="text-emerald-400">"Yes"</span> : <span class="text-red-400">"No"</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ params: Object })
defineEmits(['update'])
</script>
