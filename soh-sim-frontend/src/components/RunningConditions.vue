<template>
  <div class="h-full overflow-y-auto custom-scrollbar">
    <div class="max-w-5xl mx-auto space-y-4 py-2">
      <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded bg-teal-500/20 text-teal-400 text-xs flex items-center justify-center font-bold">01</span>
          <div>
            <h3 class="font-bold text-sm text-slate-200">项目概况 <span class="text-[10px] text-slate-500 font-normal ml-1">Project Overview</span></h3>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-3">
          <div class="col-span-2">
            <label class="text-[10px] text-slate-400 block mb-1">项目名称 Project Name</label>
            <input v-model="form.projectName" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="项目名称">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">项目类型 Project Type</label>
            <select v-model="form.projectType" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- 请选择 -</option>
              <option value="utility">大型独立储能 Utility-Scale</option>
              <option value="cni">工商业储能 C&I</option>
              <option value="residential">户用储能 Residential</option>
              <option value="microgrid">微电网 Microgrid</option>
              <option value="solar-plus-bess">光伏配储 Solar+BESS</option>
              <option value="wind-plus-bess">风电配储 Wind+BESS</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">项目地点 Location</label>
            <input v-model="form.location" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="国家/地区">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">额定总功率 MW</label>
            <input v-model.number="form.totalMW" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="200">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">额定总能量 MWh</label>
            <input v-model.number="form.totalMWh" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="800">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">充放电时长 小时</label>
            <input v-model.number="form.durationHours" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="4">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">日循环次数 次/天</label>
            <input v-model.number="form.cyclesPerDay" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="1">
          </div>
        </div>
      </div>

      <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded bg-amber-500/20 text-amber-400 text-xs flex items-center justify-center font-bold">02</span>
          <div>
            <h3 class="font-bold text-sm text-slate-200">环境选址 <span class="text-[10px] text-slate-500 font-normal ml-1">Site & Environment</span></h3>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">海拔高度 米</label>
            <input v-model.number="form.altitude" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="≤2000">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">极端最高温度 °C</label>
            <input v-model.number="form.tempMax" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="45">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">极端最低温度 °C</label>
            <input v-model.number="form.tempMin" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="-20">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">年平均温度 °C</label>
            <input v-model.number="form.tempAvg" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="25">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">相对湿度 %RH</label>
            <input v-model.number="form.humidity" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="≤95">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">地震等级</label>
            <select v-model="form.seismicZone" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- -</option>
              <option value="zone1">Zone I (低)</option>
              <option value="zone2">Zone II</option>
              <option value="zone3">Zone III (中)</option>
              <option value="zone4">Zone IV (高)</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">防腐等级</label>
            <select v-model="form.corrosionClass" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- -</option>
              <option value="c1">C1 (极低)</option>
              <option value="c2">C2 (低)</option>
              <option value="c3" selected>C3 (中)</option>
              <option value="c4">C4 (高)</option>
              <option value="c5">C5 (极高)</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">安装方式</label>
            <select v-model="form.installationType" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- -</option>
              <option value="outdoor">户外 Outdoor</option>
              <option value="indoor">户内 Indoor</option>
              <option value="semi-outdoor">半户外 Semi</option>
            </select>
          </div>
        </div>
      </div>

      <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded bg-blue-500/20 text-blue-400 text-xs flex items-center justify-center font-bold">03</span>
          <div>
            <h3 class="font-bold text-sm text-slate-200">电网电气 <span class="text-[10px] text-slate-500 font-normal ml-1">Grid & Electrical</span></h3>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">并网电压等级 kV</label>
            <select v-model="form.gridVoltage" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- -</option>
              <option value="10kV">10 kV</option>
              <option value="35kV">35 kV</option>
              <option value="110kV">110 kV</option>
              <option value="220kV">220 kV</option>
              <option value="330kV">330 kV</option>
              <option value="500kV">500 kV</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">电网频率 Hz</label>
            <select v-model="form.gridFreq" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- -</option>
              <option value="50Hz">50 Hz</option>
              <option value="60Hz">60 Hz</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">短路容量 MVA</label>
            <input v-model.number="form.scCapacity" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="5000">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">中性点接地方式</label>
            <select v-model="form.neutralGrounding" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- -</option>
              <option value="solid">直接接地 Solid</option>
              <option value="resistance">经电阻接地 Resistance</option>
              <option value="arc-suppression">经消弧线圈 Arc-Suppression</option>
              <option value="ungrounded">不接地 Ungrounded</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">DC侧额定电压范围 V</label>
            <input v-model="form.dcVoltageRange" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="1000-1500">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">AC侧额定电压 V</label>
            <input v-model="form.acVoltage" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="690">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">功率因数范围</label>
            <input v-model="form.pfRange" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="0.99超前-0.99滞后">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">THDi 要求 %</label>
            <input v-model.number="form.thdiLimit" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="5">
          </div>
        </div>
      </div>

      <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded bg-purple-500/20 text-purple-400 text-xs flex items-center justify-center font-bold">04</span>
          <div>
            <h3 class="font-bold text-sm text-slate-200">系统性能 <span class="text-[10px] text-slate-500 font-normal ml-1">Performance KPIs</span></h3>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">RTE 目标 首年 %</label>
            <input v-model.number="form.rteTarget" type="number" step="0.01" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="85">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">AC可用率 目标 %</label>
            <input v-model.number="form.availabilityTarget" type="number" step="0.01" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="99">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">SOH 第1年末 %</label>
            <input v-model.number="form.sohYear1" type="number" step="0.01" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="93.2">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">SOH 第25年末 %</label>
            <input v-model.number="form.sohYear25" type="number" step="0.01" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="60">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">日历寿命 年</label>
            <input v-model.number="form.calendarLife" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="25">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">循环寿命 次</label>
            <input v-model.number="form.cycleLife" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="6000">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">辅助功耗 自耗电率 %</label>
            <input v-model.number="form.auxConsumption" type="number" step="0.01" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="5">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">响应时间 ms</label>
            <input v-model.number="form.responseTime" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="50">
          </div>
        </div>
      </div>

      <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded bg-green-500/20 text-green-400 text-xs flex items-center justify-center font-bold">05</span>
          <div>
            <h3 class="font-bold text-sm text-slate-200">电芯技术需求 <span class="text-[10px] text-slate-500 font-normal ml-1">Cell Requirements</span></h3>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">电芯化学体系</label>
            <select v-model="form.cellChemistry" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- -</option>
              <option value="LFP">LFP (磷酸铁锂)</option>
              <option value="NMC">NMC (镍锰钴)</option>
              <option value="LTO">LTO (钛酸锂)</option>
              <option value="sodium-ion">钠离子 Na-ion</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">单电芯容量范围 Ah</label>
            <input v-model="form.cellCapacityRange" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="280-700">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">电芯循环寿命 @25°C</label>
            <input v-model.number="form.cellCycleLife" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="6000">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">EOL 判定标准 %</label>
            <input v-model.number="form.eolThreshold" type="number" step="0.1" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="70">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">电芯工作温度范围 °C</label>
            <input v-model="form.cellTempRange" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="-20 ~ +55">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">电芯压差一致性要求 mV</label>
            <input v-model.number="form.cellVoltageDiff" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="20">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">电芯温差一致性要求 °C</label>
            <input v-model.number="form.cellTempDiff" type="number" step="0.5" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="3">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">热失控蔓延防止</label>
            <select v-model="form.thermalRunawayPrev" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- -</option>
              <option value="pack-level">Pack 级隔离 (标准)</option>
              <option value="cluster-level">簇级隔离</option>
              <option value="rack-level">Rack 级隔离 (MWh+标准)</option>
            </select>
          </div>
        </div>
      </div>

      <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded bg-cyan-500/20 text-cyan-400 text-xs flex items-center justify-center font-bold">06</span>
          <div>
            <h3 class="font-bold text-sm text-slate-200">PCS 变流器技术需求 <span class="text-[10px] text-slate-500 font-normal ml-1">PCS Requirements</span></h3>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">PCS 额定功率 MW</label>
            <input v-model.number="form.pcsRatedPower" type="number" step="0.001" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="2.5">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">PCS 额定效率 %</label>
            <input v-model.number="form.pcsEfficiency" type="number" step="0.01" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="98.5">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">过载能力</label>
            <select v-model="form.pcsOverload" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- -</option>
              <option value="standard">110% 10min / 120% 1min</option>
              <option value="enhanced">120% 10min / 150% 1min</option>
              <option value="high">130% 30min / 150% 10min</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">THDi 要求 %</label>
            <input v-model.number="form.pcsTHDi" type="number" step="0.1" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="3">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">功率因数范围</label>
            <input v-model="form.pcsPF" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="-0.9 ~ +0.9">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">响应时间 ms</label>
            <input v-model.number="form.pcsResponseTime" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="50">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">电网支撑功能</label>
            <select v-model="form.pcsGridSupport" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- -</option>
              <option value="basic">基础: LVRT + HVRT</option>
              <option value="advanced">高级: + 一次调频 + 惯量响应</option>
              <option value="full">完整: + 黑启动 + 构网型 Grid-Forming</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">冷却方式</label>
            <select v-model="form.pcsCooling" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- -</option>
              <option value="forced-air">强迫风冷 (标准)</option>
              <option value="liquid">液冷 (50°C不降额)</option>
              <option value="SiC-liquid">全液冷碳化硅 SiC (Masdar级)</option>
            </select>
          </div>
        </div>
      </div>

      <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded bg-rose-500/20 text-rose-400 text-xs flex items-center justify-center font-bold">07</span>
          <div>
            <h3 class="font-bold text-sm text-slate-200">认证与标准要求 <span class="text-[10px] text-slate-500 font-normal ml-1">Certification & Standards</span></h3>
          </div>
        </div>
        <div class="grid grid-cols-3 gap-3 text-[10px]">
          <div>
            <span class="text-slate-400 text-[10px] block mb-1">电芯级认证 Cell Level</span>
            <div class="bg-slate-800/60 rounded p-2 space-y-1.5">
              <label v-for="opt in certOptions.cell" :key="opt" class="flex items-center gap-1.5 cursor-pointer hover:text-slate-200 text-slate-400">
                <input type="checkbox" :value="opt" v-model="form.certCell" class="accent-teal-500">{{ opt }}
              </label>
            </div>
          </div>
          <div>
            <span class="text-slate-400 text-[10px] block mb-1">系统级 / 模组级</span>
            <div class="bg-slate-800/60 rounded p-2 space-y-1.5">
              <label v-for="opt in certOptions.system" :key="opt" class="flex items-center gap-1.5 cursor-pointer hover:text-slate-200 text-slate-400">
                <input type="checkbox" :value="opt" v-model="form.certSystem" class="accent-amber-500">{{ opt }}
              </label>
            </div>
          </div>
          <div>
            <span class="text-slate-400 text-[10px] block mb-1">并网与环境 Grid & Env</span>
            <div class="bg-slate-800/60 rounded p-2 space-y-1.5">
              <label v-for="opt in certOptions.grid" :key="opt" class="flex items-center gap-1.5 cursor-pointer hover:text-slate-200 text-slate-400">
                <input type="checkbox" :value="opt" v-model="form.certGrid" class="accent-blue-500">{{ opt }}
              </label>
            </div>
          </div>
        </div>
        <div class="mt-2 grid grid-cols-2 gap-3 text-[10px]">
          <div>
            <span class="text-slate-400 block mb-1">其它特殊认证</span>
            <div class="bg-slate-800/60 rounded p-2 space-y-1.5">
              <label v-for="opt in certOptions.extra" :key="opt" class="flex items-center gap-1.5 cursor-pointer hover:text-slate-200 text-slate-400">
                <input type="checkbox" :value="opt" v-model="form.certExtra" class="accent-purple-500">{{ opt }}
              </label>
            </div>
          </div>
          <div>
            <span class="text-slate-400 block mb-1">目标市场电网规范</span>
            <div class="bg-slate-800/60 rounded p-2 space-y-1.5">
              <label v-for="opt in certOptions.gridCode" :key="opt" class="flex items-center gap-1.5 cursor-pointer hover:text-slate-200 text-slate-400">
                <input type="checkbox" :value="opt" v-model="form.certGridCode" class="accent-emerald-500">{{ opt }}
              </label>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded bg-indigo-500/20 text-indigo-400 text-xs flex items-center justify-center font-bold">08</span>
          <div>
            <h3 class="font-bold text-sm text-slate-200">EPC 与运维范围 <span class="text-[10px] text-slate-500 font-normal ml-1">EPC & O&M Scope</span></h3>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">EPC 交付模式</label>
            <select v-model="form.epcModel" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- -</option>
              <option value="turnkey">交钥匙 Turnkey EPC</option>
              <option value="supply-only">纯供货 Supply Only</option>
              <option value="supply-supervision">供货+督导 Supply+Supervision</option>
              <option value="epcm">EPCM 管理承包</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">O&M 年限</label>
            <input v-model.number="form.omYears" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="5">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">性能保证 (PR) 要求</label>
            <select v-model="form.prRequirement" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- -</option>
              <option value="availability-guarantee">可用率保证 ≥97%</option>
              <option value="rte-guarantee">RTE 保证 (含 LD 罚则)</option>
              <option value="soh-guarantee">SOH 保证 (含容量衰减 LD)</option>
              <option value="full-guarantee">全保证: 可用率+RTE+SOH</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">质保年限</label>
            <input v-model.number="form.warrantyYears" type="number" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none" placeholder="5">
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">远程监控/SCADA</label>
            <select v-model="form.scadaReq" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- -</option>
              <option value="none">不需要</option>
              <option value="basic">基础: Modbus TCP</option>
              <option value="advanced">高级: IEC 61850 + DNP3</option>
              <option value="full">完整: + 云平台 + AI诊断</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] text-slate-400 block mb-1">备品备件策略</label>
            <select v-model="form.sparePartsStrategy" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 focus:border-teal-500 focus:outline-none">
              <option value="">- -</option>
              <option value="none">不含</option>
              <option value="standard">标准: 2年运行备件</option>
              <option value="enhanced">增强: 5年 + 关键部件</option>
              <option value="full">全包: 全套更换件 + 现场仓储</option>
            </select>
          </div>
        </div>
      </div>

      <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded bg-emerald-500/20 text-emerald-400 text-xs flex items-center justify-center font-bold">09</span>
          <div>
            <h3 class="font-bold text-sm text-slate-200">文档上传 <span class="text-[10px] text-slate-500 font-normal ml-1">Auto Extract Parameters</span></h3>
          </div>
        </div>
        <p class="text-[10px] text-slate-500 mb-3">上传项目技术规范书、SLD、负荷曲线等文档，自动提取工况参数填充上方表单</p>
        <div
          class="border-2 border-dashed rounded-lg p-6 text-center transition-colors cursor-pointer"
          :class="uploadHover ? 'border-teal-500 bg-teal-500/5' : 'border-slate-700 hover:border-slate-500'"
          @dragover.prevent="uploadHover = true"
          @dragleave.prevent="uploadHover = false"
          @drop.prevent="onDrop"
          @click="triggerUpload"
        >
          <input ref="fileInput" type="file" accept=".pdf,.doc,.docx,.xls,.xlsx,.csv" class="hidden" @change="onFileChange">
          <div v-if="uploading" class="text-teal-400 text-xs">
            <div class="animate-spin w-4 h-4 border-2 border-teal-400 border-t-transparent rounded-full mx-auto mb-2"></div>
            正在解析文档...
          </div>
          <div v-else-if="uploadResult" class="text-xs">
            <span class="text-green-400 font-bold">解析完成</span>
            <span class="text-slate-500 ml-2">{{ uploadResult.fieldsExtracted }} 个字段已提取</span>
            <button @click.stop="applyExtracted" class="ml-3 text-teal-400 underline text-xs hover:text-teal-300">应用至表单</button>
            <button @click.stop="uploadResult = null" class="ml-3 text-slate-500 underline text-xs hover:text-slate-400">清除</button>
          </div>
          <div v-else>
            <div class="text-2xl mb-1 opacity-40">📄</div>
            <p class="text-xs text-slate-400">拖拽文件到此处 或 <span class="text-teal-400 underline">点击选择</span></p>
            <p class="text-[10px] text-slate-600 mt-1">支持 PDF, DOCX, XLSX, CSV</p>
          </div>
        </div>
      </div>

      <div class="text-right pb-4">
        <button @click="clearAll" class="text-xs text-slate-500 hover:text-red-400 underline mr-4">清空 Reset</button>
        <button @click="exportCSV" class="text-xs bg-slate-800 border border-slate-700 hover:border-slate-500 text-slate-300 px-4 py-1.5 rounded mr-2 transition-colors">导出 CSV</button>
        <button @click="applyToSimulation"
          class="text-xs bg-gradient-to-r from-teal-500 to-emerald-600 hover:from-teal-600 hover:to-emerald-700 text-white px-6 py-1.5 rounded shadow-md transition-all active:scale-95">
          应用至仿真引擎
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const emit = defineEmits(['applyParams'])

const form = reactive({
  projectName: '',
  projectType: '',
  location: '',
  totalMW: null,
  totalMWh: null,
  durationHours: null,
  cyclesPerDay: 1,
  altitude: null,
  tempMax: null,
  tempMin: null,
  tempAvg: null,
  humidity: null,
  seismicZone: '',
  corrosionClass: 'c3',
  installationType: '',
  gridVoltage: '',
  gridFreq: '',
  scCapacity: null,
  neutralGrounding: '',
  dcVoltageRange: '',
  acVoltage: '',
  pfRange: '',
  thdiLimit: null,
  rteTarget: null,
  availabilityTarget: null,
  sohYear1: null,
  sohYear25: null,
  calendarLife: null,
  cycleLife: null,
  auxConsumption: null,
  responseTime: null,
  cellChemistry: '',
  cellCapacityRange: '',
  cellCycleLife: null,
  eolThreshold: 70,
  cellTempRange: '',
  cellVoltageDiff: null,
  cellTempDiff: null,
  thermalRunawayPrev: '',
  pcsRatedPower: null,
  pcsEfficiency: null,
  pcsOverload: '',
  pcsTHDi: null,
  pcsPF: '',
  pcsResponseTime: null,
  pcsGridSupport: '',
  pcsCooling: '',
  certCell: [],
  certSystem: [],
  certGrid: [],
  certExtra: [],
  certGridCode: [],
  epcModel: '',
  omYears: null,
  prRequirement: '',
  warrantyYears: null,
  scadaReq: '',
  sparePartsStrategy: '',
})

const certOptions = {
  cell: ['IEC 62619 (锂电安全)', 'IEC 62620 (性能测试)', 'UL 1642 (电芯安全)', 'UN 38.3 (运输安全)', 'GB/T 36276 (中国国标)'],
  system: ['UL 9540 (系统级安全)', 'UL 9540A (火烧蔓延测试)', 'UL 1973 (模组标准)', 'IEC 62933-5-2 (并网安全)', 'NFPA 855 (消防规范)', 'IEC 62477-1 (PCS安全)'],
  grid: ['IEEE 1547 (并网互联)', 'IEC 61000-6-2/4 (EMC抗扰/发射)', 'UL 1741 (逆变器)', 'IEC 62933-4-2 (环境评估)', 'IEC 60730 (自动控制)'],
  extra: ['ISO 14001 (环境管理)', 'ISO 45001 (职业健康)', 'ISO 9001 (质量管理)', 'CE Marking (欧盟)', 'UKCA (英国)', 'RCM (澳大利亚)'],
  gridCode: ['UK G99 (英国)', 'VDE-AR-N 4110 (德国)', 'EN 50549-1 (欧盟)', 'IEEE 2800 (美国 BPS)', 'AEMO Grid Code (澳大利亚)', 'SASO/IEC (中东/沙特)'],
}

const fileInput = ref(null)
const uploadHover = ref(false)
const uploading = ref(false)
const uploadResult = ref(null)

function triggerUpload() {
  fileInput.value?.click()
}

function onFileChange(e) {
  const file = e.target.files?.[0]
  if (file) parseFile(file)
}

function onDrop(e) {
  uploadHover.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file) parseFile(file)
}

async function parseFile(file) {
  uploading.value = true
  uploadResult.value = null
  try {
    const formData = new FormData()
    formData.append('file', file)
    const resp = await fetch('/api/upload/extract', { method: 'POST', body: formData })
    const data = await resp.json()
    if (data.extracted) {
      uploadResult.value = { extracted: data.extracted, fieldsExtracted: Object.keys(data.extracted).length }
    } else {
      uploadResult.value = { extracted: {}, fieldsExtracted: 0, error: data.error || '未能提取参数' }
    }
  } catch {
    uploadResult.value = { extracted: {}, fieldsExtracted: 0, error: '解析服务不可用' }
  }
  uploading.value = false
}

function applyExtracted() {
  if (!uploadResult.value?.extracted) return
  const ext = uploadResult.value.extracted
  const mapping = {
    project_name: 'projectName', project_type: 'projectType', location: 'location',
    total_mw: 'totalMW', total_mwh: 'totalMWh', duration_h: 'durationHours',
    cycles_per_day: 'cyclesPerDay', altitude_m: 'altitude',
    temp_max_c: 'tempMax', temp_min_c: 'tempMin', temp_avg_c: 'tempAvg',
    humidity_pct: 'humidity', seismic_zone: 'seismicZone', corrosion_class: 'corrosionClass',
    installation_type: 'installationType', grid_voltage_kv: 'gridVoltage', grid_freq_hz: 'gridFreq',
    sc_capacity_mva: 'scCapacity', neutral_grounding: 'neutralGrounding',
    dc_voltage_range: 'dcVoltageRange', ac_voltage_v: 'acVoltage',
    pf_range: 'pfRange', thdi_pct: 'thdiLimit', rte_target_pct: 'rteTarget',
    availability_target_pct: 'availabilityTarget', soh_year1_pct: 'sohYear1',
    soh_year25_pct: 'sohYear25', calendar_life_y: 'calendarLife',
    cycle_life: 'cycleLife', aux_consumption_pct: 'auxConsumption', response_time_ms: 'responseTime',
  }
  for (const [k, v] of Object.entries(ext)) {
    const target = mapping[k]
    if (target && v !== null && v !== undefined) {
      const f = form[target]
      if (typeof f === 'number' || f === null) form[target] = Number(v)
      else form[target] = String(v)
    }
  }
}

function exportCSV() {
  const rows = [['Key', 'Value']]
  for (const [k, v] of Object.entries(form)) {
    rows.push([k, v ?? ''])
  }
  const csv = '\uFEFF' + rows.map(r => r.map(c => `"${String(c).replace(/"/g, '""')}"`).join(',')).join('\n')
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url; a.download = `BESS_Conditions_${form.projectName || 'Export'}.csv`
  document.body.appendChild(a); a.click(); document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

function clearAll() {
  for (const k of Object.keys(form)) {
    if (Array.isArray(form[k])) form[k] = []
    else form[k] = typeof form[k] === 'number' || form[k] === null ? null : ''
  }
  uploadResult.value = null
}

function applyToSimulation() {
  const mapped = {
    duration: form.durationHours,
    cyclesPerDay: form.cyclesPerDay,
    requiredEnergy: form.totalMWh,
    altitude: form.altitude,
    tempMax: form.tempMax,
    tempMin: form.tempMin,
    tempAvg: form.tempAvg,
    humidity: form.humidity,
    gridVoltage: form.gridVoltage,
    rteTarget: form.rteTarget,
    availabilityTarget: form.availabilityTarget,
    projectName: form.projectName,
    projectType: form.projectType,
    location: form.location,
  }
  emit('applyParams', mapped)
}
</script>
