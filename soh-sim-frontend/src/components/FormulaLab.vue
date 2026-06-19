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
        E<sub>aug_net</sub>(i) = SUM(k≤i) [ 标称能量 × 投入箱数 × SOH<sub>target</sub> × RTE(i) × DOD(i) × η<sub>ac</sub> - 投入箱数 × 单舱单次辅耗 ]
      </div>
    </div>

    <div class="bg-slate-950 p-3 rounded-lg border border-emerald-900/40 space-y-1.5">
      <div class="text-[11px] font-bold text-emerald-400">
        算子 4 — 全周期单次循环净放电对账底线判定
      </div>
      <div class="p-2.5 bg-slate-900/80 rounded font-mono overflow-x-auto border border-slate-850 text-slate-300 text-[11px]">
        E<sub>net_total</sub>(i) = Max(0, E<sub>gross_init</sub> - Aux<sub>init</sub>) + E<sub>aug_net</sub>(i)
        <div class="mt-1 text-slate-400">
          判定判据：E<sub>net_total</sub>(i) >=
          <input type="number" :value="params.requiredEnergy" step="1" class="formula-input w-14 text-amber-400"
            @input="$emit('update', 'requiredEnergy', Number($event.target.value))"> MWh
          ? <span class="text-emerald-400">"Yes"</span> : <span class="text-red-400">"No"</span>
        </div>
      </div>
    </div>

    <div class="border-t border-slate-800 pt-3">
      <h2 class="text-sm font-bold text-amber-400 uppercase tracking-wider border-l-4 border-amber-500 pl-2 mb-3">财务投资算法引擎 Investment & Finance</h2>
    </div>

    <div class="bg-slate-950 p-3 rounded-lg border border-yellow-900/40 space-y-1.5">
      <div class="text-[11px] font-bold text-yellow-400">
        算子 5 — 收入叠加模型 (Multi-Stack Revenue)
      </div>
      <div class="text-[10px] text-slate-500 mb-1.5 leading-relaxed">
        大型储能电站通常叠加多个收入来源以提升项目 IRR。参考 Masdar 等中东项目，独立储能收益主要来源于电能量套利价差+容量市场费用+辅助服务费三项叠加。不同市场结构下，各收入占比差异显著（套利 40-70%、容量 20-40%、辅助服务 10-20%）。
      </div>
      <div class="p-2.5 bg-slate-900/80 rounded font-mono overflow-x-auto border border-slate-850 text-slate-300 text-[11px] leading-relaxed">
        Revenue<sub>year</sub> = EnergyArbitrage + CapacityPayment + AncillaryService
        <div class="pl-4 text-[10px] text-slate-400 space-y-0.5 mt-1">
          <div>EnergyArbitrage<sub>year</sub> = DischargedMWh × (PeakPrice - OffPeakPrice) × SpreadCaptureRate</div>
          <div>CapacityPayment<sub>year</sub> = ContractedMW × CapacityPrice<sub>perMW</sub></div>
          <div>AncillaryService<sub>year</sub> = AvailableMW × AncillaryPrice<sub>perMW</sub></div>
          <div class="text-amber-400/80">所有收入项按 PriceEscalation 年涨幅递增，价差捕获率反映实际交易中无法完全捕捉理论价差的折扣</div>
        </div>
      </div>
    </div>

    <div class="bg-slate-950 p-3 rounded-lg border border-orange-900/40 space-y-1.5">
      <div class="text-[11px] font-bold text-orange-400">
        算子 6 — CAPEX / OPEX 全成本结构
      </div>
      <div class="text-[10px] text-slate-500 mb-1.5 leading-relaxed">
        资本性支出包含储能集装箱采购+变流器采购+BOP辅助系统+项目开发费四部分。运营费用含固定运维（按装机容量计算，覆盖人力+例行维护）、可变运维（按吞吐电量计算，覆盖非计划检修）、保险费（按CAPEX比率）和土地租赁费四项。所有OPEX项按年涨幅递增以反映通胀和老化效应。
      </div>
      <div class="p-2.5 bg-slate-900/80 rounded font-mono overflow-x-auto border border-slate-850 text-slate-300 text-[11px] leading-relaxed">
        <div>CAPEX<sub>total</sub> = ContainerCost + PCSCost + BOP + DevelopmentFee</div>
        <div class="pl-4 text-[10px] text-slate-400 mt-1">
          ContainerCost = UnitCost<sub>perMWh</sub> × TotalMWh<br>
          PCSCost = UnitCost<sub>perMW</sub> × TotalMW<br>
          BOP = BOPCost<sub>perMWh</sub> × TotalMWh (含变压器/开关柜/电缆/消防/暖通)<br>
          DevelopmentFee = DevCost<sub>perMW</sub> × TotalMW (含可研/环评/接入/土地)
        </div>
        <div class="mt-2">OPEX<sub>year</sub> = FixedO&M + VarO&M + Insurance + LandLease</div>
        <div class="pl-4 text-[10px] text-slate-400 mt-1">
          FixedO&M<sub>year</sub> = FixedRate<sub>perKW</sub> × TotalMW × 1000 × (1+escalation)<sup>year</sup><br>
          VarO&M<sub>year</sub> = VarRate<sub>perMWh</sub> × AnnualThroughput × (1+escalation)<sup>year</sup><br>
          Insurance<sub>year</sub> = CAPEX × InsuranceRate<br>
          LandLease<sub>year</sub> = 固定年费
        </div>
      </div>
    </div>

    <div class="bg-slate-950 p-3 rounded-lg border border-rose-900/40 space-y-1.5">
      <div class="text-[11px] font-bold text-rose-400">
        算子 7 — LCOS (Levelized Cost of Storage) 平准化储能成本
      </div>
      <div class="text-[10px] text-slate-500 mb-1.5 leading-relaxed">
        LCOS是储能项目经济性的核心对标指标，类比光伏LCOE。它计算全生命周期内每放出1度电的折现总成本，包含初始投资、运维支出、增容支出，扣除末期残值。项目盈利的前提是LCOS低于售电均价。Masdar 级项目通常要求 LCOS &lt; 0.06 美元/kWh (折合人民币约 0.40 元/kWh)。
      </div>
      <div class="p-2.5 bg-slate-900/80 rounded font-mono overflow-x-auto border border-slate-850 text-slate-300 text-[11px] leading-relaxed">
        LCOS = TotalDiscountedCosts / TotalDiscountedEnergy
        <div class="pl-4 text-[10px] text-slate-400 space-y-0.5 mt-1">
          <div>TotalDiscountedCosts = CAPEX + SUM(OPEX<sub>t</sub>/(1+r)<sup>t</sup>) + SUM(Augmentation<sub>t</sub>/(1+r)<sup>t</sup>) - Residual/(1+r)<sup>T</sup></div>
          <div>TotalDiscountedEnergy = SUM(AnnualDischargedMWh<sub>t</sub>/(1+r)<sup>t</sup>)</div>
          <div class="text-rose-400/80">r = WACC (加权平均资本成本), 中东项目通常 6-8%, 其他地区 7-10%; T = 25年项目寿命</div>
        </div>
      </div>
    </div>

    <div class="bg-slate-950 p-3 rounded-lg border border-indigo-900/40 space-y-1.5">
      <div class="text-[11px] font-bold text-indigo-400">
        算子 8 — IRR (Internal Rate of Return) 内部收益率, 牛顿迭代法数值求解
      </div>
      <div class="text-[10px] text-slate-500 mb-1.5 leading-relaxed">
        IRR为净现值为零时的折现率，是投资者最关注的决策指标。全投资IRR (Project IRR) 不区分资金来源、反映项目本身的盈利能力；自有资金IRR (Equity IRR) 考虑了杠杆效应后股东的回报率。一般储能项目目标 Project IRR 为 6-10%、Equity IRR 为 10-15%。采用 Newton-Raphson 法迭代求解 f(r)=0 的根。
      </div>
      <div class="p-2.5 bg-slate-900/80 rounded font-mono overflow-x-auto border border-slate-850 text-slate-300 text-[11px] leading-relaxed">
        NPV(r) = -CAPEX + SUM(CF<sub>t</sub>/(1+r)<sup>t</sup>) = 0
        <div class="pl-4 text-[10px] text-slate-400 space-y-0.5 mt-1">
          <div>Newton-Raphson 迭代: r<sub>k+1</sub> = r<sub>k</sub> - NPV(r<sub>k</sub>)/NPV'(r<sub>k</sub>)</div>
          <div>Project IRR: 全投资现金流(不含融资成本)折现求解</div>
          <div>Equity IRR: 自有资金投入替代初始CAPEX, 扣除年还本付息后折现求解</div>
          <div class="text-indigo-400/80">收敛判别: |NPV| &lt; 10<sup>-6</sup> 或 |Δr| &lt; 10<sup>-8</sup>; 最多迭代 100 次; 边界保护 -99%~999%</div>
        </div>
      </div>
    </div>

    <div class="bg-slate-950 p-3 rounded-lg border border-cyan-900/40 space-y-1.5">
      <div class="text-[11px] font-bold text-cyan-400">
        算子 9 — DSCR (Debt Service Coverage Ratio) 偿债覆盖倍率
      </div>
      <div class="text-[10px] text-slate-500 mb-1.5 leading-relaxed">
        DSCR衡量项目每年可用于还本付息的现金是否充足，是银行和金融机构放贷的核心审批指标。分子为息税折旧前利润减所得税后的可偿债现金流，分母为当年应付本息。银行通常要求DSCR全程不低于1.2-1.3倍，若某年DSCR跌破1.0则意味着项目无法自行偿债。
      </div>
      <div class="p-2.5 bg-slate-900/80 rounded font-mono overflow-x-auto border border-slate-850 text-slate-300 text-[11px] leading-relaxed">
        DSCR<sub>year</sub> = (EBITDA - Tax) / DebtService<sub>year</sub>
        <div class="pl-4 text-[10px] text-slate-400 space-y-0.5 mt-1">
          <div>EBITDA = Revenue - OPEX</div>
          <div>TaxableIncome = EBITDA - Depreciation - Interest</div>
          <div>Tax = Max(0, TaxableIncome × TaxRate)</div>
          <div>DebtService<sub>year</sub> = InterestPayment + PrincipalRepayment</div>
          <div class="text-cyan-400/80">等额本息还款法: 年还款额 = Debt × r × (1+r)<sup>n</sup> / ((1+r)<sup>n</sup> - 1); 银行最低要求 1.3, 优质项目通常 > 1.5</div>
        </div>
      </div>
    </div>

    <div class="bg-slate-950 p-3 rounded-lg border border-lime-900/40 space-y-1.5">
      <div class="text-[11px] font-bold text-lime-400">
        算子 10 — Payback Period 静态与动态投资回收期
      </div>
      <div class="text-[10px] text-slate-500 mb-1.5 leading-relaxed">
        回收期是累计净现金流首次由负转正的时间点。静态回收期不考虑资金时间价值，直接累加名义现金流；动态回收期将所有现金流按WACC折现后再累加。储能项目静态回收期通常为8-12年，动态回收期为10-15年。回收期越短，项目抗风险能力越强。
      </div>
      <div class="p-2.5 bg-slate-900/80 rounded font-mono overflow-x-auto border border-slate-850 text-slate-300 text-[11px] leading-relaxed">
        累计净现金流首次转正的年份 = 回收期
        <div class="pl-4 text-[10px] text-slate-400 space-y-0.5 mt-1">
          <div>静态回收期: CumulativeCashFlow(year) >= 0 的最小 year</div>
          <div>动态回收期: DiscountedCumulativeCashFlow(year) >= 0 的最小 year</div>
          <div class="text-lime-400/80">按累积现金流转正的前后两年线性插值, 精确到 0.1 年</div>
        </div>
      </div>
    </div>

    <div class="bg-slate-950 p-3 rounded-lg border border-violet-900/40 space-y-1.5">
      <div class="text-[11px] font-bold text-violet-400">
        算子 11 — 增容成本逐年递减学习曲线效应
      </div>
      <div class="text-[10px] text-slate-500 mb-1.5 leading-relaxed">
        锂电池和储能系统遵循 Wright 定律，累计出货量翻倍时成本下降一定比例（学习率约18-20%）。在25年运营周期中后期增容的集装箱采购成本将因技术进步和规模效应而显著低于建设期。参考 BNEF 等机构数据，直流侧设备成本年均降幅约5-8%/年，AC侧约3-5%/年。
      </div>
      <div class="p-2.5 bg-slate-900/80 rounded font-mono overflow-x-auto border border-slate-850 text-slate-300 text-[11px] leading-relaxed">
        AugCapex<sub>year</sub> = AugQty × RatedEnergy × ContainerCost<sub>base</sub> × (1 - CostDeclineRate)<sup>year</sup> + AugQty × InstallCost
        <div class="pl-4 text-[10px] text-slate-400 mt-1">
          CostDeclineRate: 年化成本降幅, 参考 BNEF 数据通常 5-8%/年<br>
          安装成本(InstallCost): 包括吊装/接线/调试等一次性费用, 假设不随学习曲线下降
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ params: Object })
defineEmits(['update'])
</script>
