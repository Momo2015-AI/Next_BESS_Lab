<template>
  <div class="h-full overflow-auto p-4">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg font-bold text-teal-400">BESS 辅助功耗计算</h2>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-4 gap-3 mb-4">
      <div class="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-4 border-t-4 border-teal-500">
        <div class="text-xs text-slate-400 uppercase font-bold mb-2">⚡ 选定天数内系统总能耗</div>
        <div class="text-2xl font-bold text-white">{{ results.totalSystemAux.toFixed(2) }}<span class="text-sm text-sky-400 ml-1">MWh</span></div>
      </div>
      <div class="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-4 border-t-4 border-emerald-500">
        <div class="text-xs text-slate-400 uppercase font-bold mb-2">🔋 单主仓单天平均能耗</div>
        <div class="text-2xl font-bold text-white">{{ results.singleUnitDailyKwh.toFixed(2) }}<span class="text-sm text-sky-400 ml-1">kWh/台·天</span></div>
      </div>
      <div class="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-4 border-t-4 border-amber-500">
        <div class="text-xs text-slate-400 uppercase font-bold mb-2">🌐 POI并网点最终净电量</div>
        <div class="text-2xl font-bold text-white">{{ results.annualNetDischarge.toFixed(2) }}<span class="text-sm text-sky-400 ml-1">MWh</span></div>
      </div>
      <div class="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-4 border-t-4 border-rose-500">
        <div class="text-xs text-slate-400 uppercase font-bold mb-2">⏱️ 选定天数内累计运行时间</div>
        <div class="text-2xl font-bold text-white">{{ results.tRun.toFixed(1) }}<span class="text-sm text-sky-400 ml-1">小时</span></div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <div class="bg-slate-800/50 rounded-xl p-4 border border-slate-700">
        <h3 class="text-sm font-medium text-slate-300 mb-4 flex items-center gap-2">
          <span class="w-1 h-4 bg-teal-500 rounded"></span>
          仿真参数全局调节
        </h3>

        <div class="mb-4">
          <div class="text-[10px] font-bold uppercase text-slate-500 mb-3 pb-2 border-b border-slate-700/50">1. 运行策略、时间与容量</div>
          <div v-for="param in strategyParams" :key="param.key" class="mb-3">
            <label class="block text-xs text-slate-400 mb-1">{{ param.label }}</label>
            <div v-if="param.hasSlider" class="flex items-center gap-3">
              <input type="range" :min="param.min" :max="param.max" :step="param.step" v-model.number="state[param.key]"
                class="flex-1 h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-teal-500" />
              <input type="number" :min="param.min" :max="param.max" :step="param.step" v-model.number="state[param.key]"
                class="w-20 bg-slate-700 border border-slate-600 rounded px-2 py-1 text-xs text-slate-200 text-right font-bold" />
            </div>
            <input v-else type="number" :min="param.min" :max="param.max" v-model.number="state[param.key]"
              class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-xs text-slate-200 font-bold" />
          </div>
        </div>

        <div class="mb-4">
          <div class="text-[10px] font-bold uppercase text-slate-500 mb-3 pb-2 border-b border-slate-700/50">2. 效率拓扑边界</div>
          <div v-for="param in efficiencyParams" :key="param.key" class="mb-3">
            <label class="block text-xs text-slate-400 mb-1">{{ param.label }}</label>
            <div class="flex items-center gap-3">
              <input type="range" :min="param.min" :max="param.max" :step="param.step" v-model.number="state[param.key]"
                class="flex-1 h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-teal-500" />
              <input type="number" :min="param.min" :max="param.max" :step="param.step" v-model.number="state[param.key]"
                class="w-20 bg-slate-700 border border-slate-600 rounded px-2 py-1 text-xs text-slate-200 text-right font-bold" />
            </div>
          </div>
        </div>

        <div class="mb-4">
          <div class="text-[10px] font-bold uppercase text-slate-500 mb-3 pb-2 border-b border-slate-700/50">3. 4象限动静态辅助功率</div>
          <div v-for="param in auxParams" :key="param.key" class="mb-3">
            <label class="block text-xs text-slate-400 mb-1">{{ param.label }}</label>
            <div class="flex items-center gap-3">
              <input type="range" :min="param.min" :max="param.max" :step="param.step" v-model.number="state[param.key]"
                class="flex-1 h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-teal-500" />
              <input type="number" :min="param.min" :max="param.max" :step="param.step" v-model.number="state[param.key]"
                class="w-20 bg-slate-700 border border-slate-600 rounded px-2 py-1 text-xs text-slate-200 text-right font-bold" />
            </div>
          </div>
        </div>

        <div>
          <div class="text-[10px] font-bold uppercase text-slate-500 mb-3 pb-2 border-b border-slate-700/50">4. 外部固定自耗</div>
          <div v-for="param in externalParams" :key="param.key" class="mb-3">
            <label class="block text-xs text-slate-400 mb-1">{{ param.label }}</label>
            <div class="flex items-center gap-3">
              <input type="range" :min="param.min" :max="param.max" :step="param.step" v-model.number="state[param.key]"
                class="flex-1 h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-teal-500" />
              <input type="number" :min="param.min" :max="param.max" :step="param.step" v-model.number="state[param.key]"
                class="w-20 bg-slate-700 border border-slate-600 rounded px-2 py-1 text-xs text-slate-200 text-right font-bold" />
            </div>
          </div>
        </div>
      </div>

      <div class="space-y-4">
        <div class="bg-slate-800/50 rounded-xl p-4 border border-slate-700">
          <div class="flex justify-between items-center mb-3">
            <h3 class="text-sm font-medium text-slate-300 flex items-center gap-2">
              <span class="w-1 h-4 bg-sky-500 rounded"></span>
              公式沙盒与实时账本推导
            </h3>
            <span :class="['text-xs px-2 py-1 rounded-full font-bold', statusClass]">{{ statusText }}</span>
          </div>

          <div class="bg-slate-900 rounded-lg p-3 mb-3">
            <div class="flex justify-between items-center mb-2">
              <span class="text-xs text-sky-400 font-bold">1. 直流侧总能耗 (DC Total Aux)</span>
              <span class="text-xs bg-sky-500 text-slate-900 px-2 py-0.5 rounded font-bold">{{ results.dcTotalAux.toFixed(2) }} MWh</span>
            </div>
            <div class="text-xs font-mono text-slate-300 bg-slate-800 rounded p-2">
              DC_Aux = [(<span class="text-teal-400">{{ state.days }}</span>天 × <span class="text-teal-400">{{ state.cycles }}</span>次 × <span class="text-teal-400">{{ state.hours }}</span>h × <span class="text-blue-400">2</span> × <span class="text-teal-400">{{ state.bRun }}</span>kW) + ((<span class="text-teal-400">{{ state.days }}</span>×24 - <span class="text-teal-400">{{ results.tRun.toFixed(1) }}</span>h) × <span class="text-teal-400">{{ state.bStd }}</span>kW)] × <span class="text-teal-400">{{ state.units }}</span>台 / 1000
            </div>
            <div class="text-[10px] text-slate-500 mt-2">
              📖 <strong class="text-slate-400">物理解析：</strong>运行态能耗按往返次数计算，待机态能耗按总时间减去运行时间计算，两者相加乘以台数折算为MWh。
            </div>
          </div>

          <div class="bg-slate-900 rounded-lg p-3 mb-3">
            <div class="flex justify-between items-center mb-2">
              <span class="text-xs text-sky-400 font-bold">2. 交流侧总能耗 (AC Total Aux)</span>
              <span class="text-xs bg-sky-500 text-slate-900 px-2 py-0.5 rounded font-bold">{{ results.acTotalAux.toFixed(2) }} MWh</span>
            </div>
            <div class="text-xs font-mono text-slate-300 bg-slate-800 rounded p-2">
              AC_Aux = [(<span class="text-teal-400">{{ state.days }}</span>天 × <span class="text-teal-400">{{ state.cycles }}</span>次 × <span class="text-teal-400">{{ state.hours }}</span>h × <span class="text-blue-400">2</span> × <span class="text-teal-400">{{ state.pRun }}</span>kW) + ((<span class="text-teal-400">{{ state.days }}</span>×24 - <span class="text-teal-400">{{ results.tRun.toFixed(1) }}</span>h) × <span class="text-teal-400">{{ state.pStd }}</span>kW) + (<span class="text-teal-400">{{ state.days }}</span>天 × 24h × <span class="text-teal-400">{{ state.pStation }}</span>kW)] / 1000
            </div>
            <div class="text-[10px] text-slate-500 mt-2">
              📖 <strong class="text-slate-400">物理解析：</strong>PCS动静态耗电口径与直流侧时间序列对齐，站宇主变自耗全天候固定拉满。
            </div>
          </div>

          <div class="bg-gradient-to-br from-slate-900 to-slate-800 rounded-lg p-3 mb-3 border-l-4 border-amber-500">
            <div class="flex justify-between items-center mb-2">
              <span class="text-xs text-amber-400 font-bold">3. 全系统总辅助能耗 (Total System Aux)</span>
              <span class="text-xs bg-amber-500 text-slate-900 px-2 py-0.5 rounded font-bold">{{ results.totalSystemAux.toFixed(2) }} MWh</span>
            </div>
            <div class="text-xs font-mono text-slate-300 bg-slate-800/50 rounded p-2">
              Total_Aux = <span class="text-teal-400">{{ results.dcTotalAux.toFixed(2) }}</span> MWh + <span class="text-teal-400">{{ results.acTotalAux.toFixed(2) }}</span> MWh
            </div>
            <div class="text-[10px] text-slate-500 mt-2">
              📖 <strong class="text-slate-400">物理解析：</strong>合并选定周期内全场所有动静态总耗电，作为电网POI交割结算前的扣除底数。
            </div>
          </div>

          <div class="bg-gradient-to-br from-slate-900 to-slate-800 rounded-lg p-3 border-l-4 border-rose-500">
            <div class="flex justify-between items-center mb-2">
              <span class="text-xs text-rose-400 font-bold">4. POI并网点期末净可用电量 (POI Net Delivery)</span>
              <span class="text-xs bg-rose-500 text-white px-2 py-0.5 rounded font-bold">{{ results.annualNetDischarge.toFixed(2) }} MWh</span>
            </div>
            <div class="text-xs font-mono text-slate-300 bg-slate-800/50 rounded p-2">
              POI_Net = (<span class="text-teal-400">{{ state.cap }}</span>MWh × <span class="text-teal-400">{{ state.units }}</span>台 × <span class="text-teal-400">{{ results.sqrtRte.toFixed(4) }}</span> × <span class="text-teal-400">{{ state.cycles }}</span>次 × <span class="text-teal-400">{{ state.days }}</span>天 × <span class="text-teal-400">{{ state.acEff }}</span> × <span class="text-teal-400">{{ state.pcsEff }}</span>) - <span class="text-teal-400">{{ results.totalSystemAux.toFixed(2) }}</span> MWh
            </div>
            <div class="text-[10px] text-slate-500 mt-2">
              📖 <strong class="text-slate-400">物理解析：</strong>括号内的放电量随计算天数线性增减，扣除总能耗即为净交割电量。
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>import { ref, reactive, computed, watch } from 'vue';
const emit = defineEmits(['error']);
const state = reactive({
 days: 365,
 cycles: 2,
 hours: 2,
 cap: 5,
 units: 62,
 dcRte: 0.941,
 pcsEff: 0.987,
 acEff: 0.975,
 bRun: 20,
 bStd: 4,
 pRun: 5,
 pStd: 1.5,
 pStation: 7.2
});
const results = ref({
 tRun: 0,
 tStd: 0,
 sqrtRte: 0,
 dcTotalAux: 0,
 acTotalAux: 0,
 totalSystemAux: 0,
 annualGrossDischarge: 0,
 annualNetDischarge: 0,
 singleUnitDailyKwh: 0
});
const strategyParams = [
 { key: 'days', label: '本次计算总天数 (Days)', min: 1, max: 365, step: 1, hasSlider: true },
 { key: 'cycles', label: '每天充放电循环次数', min: 0.5, max: 3, step: 0.5, hasSlider: true },
 { key: 'hours', label: '单次放电时长 (h)', min: 1, max: 6, step: 0.5, hasSlider: true },
 { key: 'cap', label: '单舱标称铭牌容量 (MWh)', min: 0.1, max: 100, hasSlider: false },
 { key: 'units', label: '当前运行总台数 (台)', min: 1, max: 1000, hasSlider: false }
];
const efficiencyParams = [
 { key: 'dcRte', label: 'DC-RTE (直流往返效率)', min: 0.85, max: 0.98, step: 0.005, hasSlider: true },
 { key: 'pcsEff', label: 'PCS 充/放电效率', min: 0.95, max: 0.995, step: 0.002, hasSlider: true },
 { key: 'acEff', label: '交流侧综合效率 (变损/线损)', min: 0.95, max: 0.995, step: 0.002, hasSlider: true }
];
const auxParams = [
 { key: 'bRun', label: '电池舱【运行】温控功率 (kW)', min: 5, max: 40, step: 1, hasSlider: true },
 { key: 'bStd', label: '电池舱【待机】温控功率 (kW)', min: 1, max: 15, step: 0.5, hasSlider: true },
 { key: 'pRun', label: 'PCS变流器【运行】损耗 (kW)', min: 1, max: 20, step: 0.5, hasSlider: true },
 { key: 'pStd', label: 'PCS变流器【待机】损耗 (kW)', min: 0.5, max: 10, step: 0.5, hasSlider: true }
];
const externalParams = [
 { key: 'pStation', label: '站宇及主变固定自耗 (kW)', min: 1, max: 30, step: 0.5, hasSlider: true }
];
const statusClass = computed(() => {
 if (state.days < 365) {
 return 'bg-emerald-500/20 text-emerald-400';
 }
 if (results.value.annualNetDischarge >= 210000) {
 return 'bg-emerald-500/20 text-emerald-400';
 }
 return 'bg-rose-500/20 text-rose-400';
});
const statusText = computed(() => {
 if (state.days < 365) {
 return `阶段交割模式 (${state.days}天)`;
 }
 if (results.value.annualNetDischarge >= 210000) {
 return '全年交割电量合规';
 }
 return '⚠️ 跌破年化保底红线！';
});
function calculate() {
 const sqrtRte = Math.sqrt(state.dcRte);
 const tRun = state.days * state.cycles * state.hours * 2;
 const tStd = (state.days * 24) - tRun;
 const dcTotalAux = ((tRun * state.bRun) + (tStd * state.bStd)) * state.units / 1000;
 const acTotalAux = ((tRun * state.pRun) + (tStd * state.pStd) + (state.days * 24 * state.pStation)) / 1000;
 const totalSystemAux = dcTotalAux + acTotalAux;
 const annualGrossDischarge = state.cap * state.units * sqrtRte * state.cycles * state.days * state.acEff * state.pcsEff;
 const annualNetDischarge = annualGrossDischarge - totalSystemAux;
 const singleUnitDailyKwh = (dcTotalAux * 1000) / Math.max(state.units, 1) / Math.max(state.days, 1);
 results.value = {
 tRun: Math.round(tRun * 10) / 10,
 tStd: Math.round(tStd * 10) / 10,
 sqrtRte: Math.round(sqrtRte * 10000) / 10000,
 dcTotalAux: Math.round(dcTotalAux * 100) / 100,
 acTotalAux: Math.round(acTotalAux * 100) / 100,
 totalSystemAux: Math.round(totalSystemAux * 100) / 100,
 annualGrossDischarge: Math.round(annualGrossDischarge * 100) / 100,
 annualNetDischarge: Math.round(annualNetDischarge * 100) / 100,
 singleUnitDailyKwh: Math.round(singleUnitDailyKwh * 100) / 100
 };
}
watch(state, () => {
 calculate();
}, { deep: true });
calculate();
</script>