<template>
  <div class="flex-1 overflow-auto rounded-xl p-4 space-y-3 card">
    <div>
      <h2 class="section-title" style="color: var(--color-accent); border-color: var(--color-accent); text-transform: uppercase; letter-spacing: 0.05em;">{{ $t('formulaLab.physicsTitle') }}</h2>
      <p class="text-[11px] mt-0.5" style="color: var(--color-text-secondary);">{{ $t('formulaLab.physicsDesc') }}</p>
    </div>

    <div class="p-3 rounded-lg space-y-1.5" style="background: var(--color-bg-secondary); border: 1px solid var(--color-accent-glow);">
      <div class="text-[11px] font-bold" style="color: var(--color-accent);">
        {{ $t('formulaLab.op1Title') }}
      </div>
      <div class="p-2.5 rounded font-mono leading-relaxed overflow-x-auto text-[11px]" style="background: var(--color-bg); border: 1px solid var(--color-border); color: var(--color-text-secondary);">
        E<sub>gross</sub>(i) =
        <input type="number" :value="params.ratedEnergy" step="0.1" class="formula-input w-12"
          @input="$emit('update', 'ratedEnergy', Number($event.target.value))"> MWh
        × <input type="number" :value="params.initContainerQty" step="1" class="formula-input w-14"
          @input="$emit('update', 'initContainerQty', Number($event.target.value))"> {{ $t('paramPanel.units') }}
        × SOH(i) × RTE(i) × DOD(i)
        × ( <input type="number" :value="params.acEfficiency" step="0.01" class="formula-input w-14"
          @input="$emit('update', 'acEfficiency', Number($event.target.value))"> / 100 )
      </div>
    </div>

    <div class="p-3 rounded-lg space-y-2" style="background: var(--color-bg-secondary); border: 1px solid rgba(245,158,11,0.2);">
      <div class="text-[11px] font-bold" style="color: #f59e0b;">
        {{ $t('formulaLab.op2Title') }}
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3 font-mono text-[11px]">
        <div class="p-2 rounded space-y-1" style="background: var(--color-bg); border: 1px solid var(--color-border);">
          <span class="font-bold block text-[10px]" style="color: #f59e0b;">A. {{ $t('paramPanel.dailyRunTotal') }}:</span>
          <div>{{ $t('paramPanel.dailyRunTotal') }} (RunHours) =
            <input type="number" :value="params.duration" step="0.5" class="formula-input w-10"
              @input="$emit('update', 'duration', Number($event.target.value))"> h ×
            <input type="number" :value="params.cyclesPerDay" step="1" class="formula-input w-8"
              @input="$emit('update', 'cyclesPerDay', Number($event.target.value))"> {{ $t('paramPanel.times') }}
          </div>
          <div class="pt-0.5" style="border-top: 1px solid var(--color-border);">{{ $t('paramPanel.dailyStandby') }} (StandbyHours) = Max(0, 24 - RunHours)</div>
        </div>
        <div class="p-2 rounded space-y-1" style="background: var(--color-bg); border: 1px solid var(--color-border);">
          <span class="font-bold block text-[10px]" style="color: #f59e0b;">B. {{ $t('paramPanel.auxPower') }}:</span>
          <div class="grid grid-cols-2 gap-x-2 text-[10px]">
            <div>{{ $t('paramPanel.bessAuxRun') }}: <input type="number" :value="params.bessAuxRun" step="0.001" class="formula-input w-16"
              @input="$emit('update', 'bessAuxRun', Number($event.target.value))"> kW</div>
            <div>{{ $t('paramPanel.bessAuxStandby') }}: <input type="number" :value="params.bessAuxStandby" step="0.1" class="formula-input w-12"
              @input="$emit('update', 'bessAuxStandby', Number($event.target.value))"> kW</div>
            <div>{{ $t('paramPanel.pcsAuxRun') }}: <input type="number" :value="params.pcsAuxRun" step="0.1" class="formula-input w-12"
              @input="$emit('update', 'pcsAuxRun', Number($event.target.value))"> kW</div>
            <div>{{ $t('paramPanel.pcsAuxStandby') }}: <input type="number" :value="params.pcsAuxStandby" step="0.1" class="formula-input w-12"
              @input="$emit('update', 'pcsAuxStandby', Number($event.target.value))"> kW</div>
          </div>
        </div>
      </div>
      <div class="p-2.5 rounded font-mono leading-relaxed overflow-x-auto text-[11px]" style="background: var(--color-bg); border: 1px solid var(--color-border); color: var(--color-text-secondary);">
        Aux<sub>total</sub> = { {{ $t('paramPanel.initContainerQty') }} × [({{ $t('paramPanel.bessAuxRun') }} × RunHours + {{ $t('paramPanel.bessAuxStandby') }} × StandbyHours) / 1000] +
        <input type="number" :value="params.initPcsQty" step="1" class="formula-input w-12"
          @input="$emit('update', 'initPcsQty', Number($event.target.value))"> {{ $t('paramPanel.units') }}
        × [({{ $t('paramPanel.pcsAuxRun') }} × RunHours + {{ $t('paramPanel.pcsAuxStandby') }} × StandbyHours) / 1000] } / {{ $t('paramPanel.cyclesPerDay') }}
      </div>
    </div>

    <div class="p-3 rounded-lg space-y-1.5" style="background: var(--color-bg-secondary); border: 1px solid rgba(236,72,153,0.2);">
      <div class="text-[11px] font-bold" style="color: #ec4899;">
        {{ $t('formulaLab.op3Title') }}
      </div>
      <div class="p-2.5 rounded font-mono overflow-x-auto text-[11px]" style="background: var(--color-bg); border: 1px solid var(--color-border); color: var(--color-text-secondary);">
        {{ $t('formulaLab.op3Title') }}
        <div class="my-1 p-1.5 rounded text-[10px]" style="background: var(--color-input-bg); border: 1px solid var(--color-border); color: #ec4899;">
          {{ $t('formulaLab.op3Title') }} (Age) = i - k
        </div>
        E<sub>aug_net</sub>(i) = SUM(k≤i) [ {{ $t('paramPanel.ratedEnergy') }} × {{ $t('matrixTable.augQty') }} × SOH<sub>target</sub> × RTE(i) × DOD(i) × η<sub>ac</sub> - {{ $t('matrixTable.augQty') }} × {{ $t('paramPanel.singleCycleAux') }} ]
      </div>
    </div>

    <div class="p-3 rounded-lg space-y-1.5" style="background: var(--color-bg-secondary); border: 1px solid rgba(16,185,129,0.2);">
      <div class="text-[11px] font-bold" style="color: var(--color-success);">
        {{ $t('formulaLab.op4Title') }}
      </div>
      <div class="p-2.5 rounded font-mono overflow-x-auto text-[11px]" style="background: var(--color-bg); border: 1px solid var(--color-border); color: var(--color-text-secondary);">
        E<sub>net_total</sub>(i) = Max(0, E<sub>gross_init</sub> - Aux<sub>init</sub>) + E<sub>aug_net</sub>(i)
        <div class="mt-1" style="color: var(--color-text-secondary);">
          {{ $t('matrixTable.meetsReq') }}: E<sub>net_total</sub>(i) >=
          <input type="number" :value="params.requiredEnergy" step="1" class="formula-input w-14" style="color: #f59e0b;"
            @input="$emit('update', 'requiredEnergy', Number($event.target.value))"> MWh
          ? <span style="color: var(--color-success);">"{{ $t('common.yes') }}"</span> : <span style="color: var(--color-danger);">"{{ $t('common.no') }}"</span>
        </div>
      </div>
    </div>

    <div class="pt-3" style="border-top: 1px solid var(--color-border);">
      <h2 class="section-title" style="color: #f59e0b; border-color: #f59e0b; text-transform: uppercase; letter-spacing: 0.05em;">{{ $t('formulaLab.financeTitle') }}</h2>
    </div>

    <div class="p-3 rounded-lg space-y-1.5" style="background: var(--color-bg-secondary); border: 1px solid rgba(234,179,8,0.2);">
      <div class="text-[11px] font-bold" style="color: #eab308;">
        {{ $t('formulaLab.op5Title') }}
      </div>
      <div class="text-[10px] mb-1.5 leading-relaxed" style="color: var(--color-text-muted);">
        {{ $t('formulaLab.op5Desc') }}
      </div>
      <div class="p-2.5 rounded font-mono overflow-x-auto text-[11px] leading-relaxed" style="background: var(--color-bg); border: 1px solid var(--color-border); color: var(--color-text-secondary);">
        Revenue<sub>year</sub> = EnergyArbitrage + CapacityPayment + AncillaryService
        <div class="pl-4 text-[10px] space-y-0.5 mt-1" style="color: var(--color-text-secondary);">
          <div>EnergyArbitrage<sub>year</sub> = DischargedMWh × (PeakPrice - OffPeakPrice) × SpreadCaptureRate</div>
          <div>CapacityPayment<sub>year</sub> = ContractedMW × CapacityPrice<sub>perMW</sub></div>
          <div>AncillaryService<sub>year</sub> = AvailableMW × AncillaryPrice<sub>perMW</sub></div>
        </div>
      </div>
    </div>

    <div class="p-3 rounded-lg space-y-1.5" style="background: var(--color-bg-secondary); border: 1px solid rgba(249,115,22,0.2);">
      <div class="text-[11px] font-bold" style="color: #f97316;">
        {{ $t('formulaLab.op6Title') }}
      </div>
      <div class="text-[10px] mb-1.5 leading-relaxed" style="color: var(--color-text-muted);">
        {{ $t('formulaLab.op6Desc') }}
      </div>
      <div class="p-2.5 rounded font-mono overflow-x-auto text-[11px] leading-relaxed" style="background: var(--color-bg); border: 1px solid var(--color-border); color: var(--color-text-secondary);">
        <div>CAPEX<sub>total</sub> = ContainerCost + PCSCost + BOP + DevelopmentFee</div>
        <div class="pl-4 text-[10px] mt-1" style="color: var(--color-text-secondary);">
          ContainerCost = UnitCost<sub>perMWh</sub> × TotalMWh<br>
          PCSCost = UnitCost<sub>perMW</sub> × TotalMW<br>
          BOP = BOPCost<sub>perMWh</sub> × TotalMWh<br>
          DevelopmentFee = DevCost<sub>perMW</sub> × TotalMW
        </div>
        <div class="mt-2">OPEX<sub>year</sub> = FixedO&M + VarO&M + Insurance + LandLease</div>
        <div class="pl-4 text-[10px] mt-1" style="color: var(--color-text-secondary);">
          FixedO&M<sub>year</sub> = FixedRate<sub>perKW</sub> × TotalMW × 1000 × (1+escalation)<sup>year</sup><br>
          VarO&M<sub>year</sub> = VarRate<sub>perMWh</sub> × AnnualThroughput × (1+escalation)<sup>year</sup><br>
          Insurance<sub>year</sub> = CAPEX × InsuranceRate<br>
          LandLease<sub>year</sub> = {{ $t('formulaLab.op6Title') }}
        </div>
      </div>
    </div>

    <div class="p-3 rounded-lg space-y-1.5" style="background: var(--color-bg-secondary); border: 1px solid rgba(244,63,94,0.2);">
      <div class="text-[11px] font-bold" style="color: #e11d48;">
        {{ $t('formulaLab.op7Title') }}
      </div>
      <div class="text-[10px] mb-1.5 leading-relaxed" style="color: var(--color-text-muted);">
        {{ $t('formulaLab.op7Desc') }}
      </div>
      <div class="p-2.5 rounded font-mono overflow-x-auto text-[11px] leading-relaxed" style="background: var(--color-bg); border: 1px solid var(--color-border); color: var(--color-text-secondary);">
        LCOS = TotalDiscountedCosts / TotalDiscountedEnergy
        <div class="pl-4 text-[10px] space-y-0.5 mt-1" style="color: var(--color-text-secondary);">
          <div>TotalDiscountedCosts = CAPEX + SUM(OPEX<sub>t</sub>/(1+r)<sup>t</sup>) + SUM(Augmentation<sub>t</sub>/(1+r)<sup>t</sup>) - Residual/(1+r)<sup>T</sup></div>
          <div>TotalDiscountedEnergy = SUM(AnnualDischargedMWh<sub>t</sub>/(1+r)<sup>t</sup>)</div>
        </div>
      </div>
    </div>

    <div class="p-3 rounded-lg space-y-1.5" style="background: var(--color-bg-secondary); border: 1px solid rgba(99,102,241,0.2);">
      <div class="text-[11px] font-bold" style="color: #6366f1;">
        {{ $t('formulaLab.op8Title') }}
      </div>
      <div class="text-[10px] mb-1.5 leading-relaxed" style="color: var(--color-text-muted);">
        {{ $t('formulaLab.op8Desc') }}
      </div>
      <div class="p-2.5 rounded font-mono overflow-x-auto text-[11px] leading-relaxed" style="background: var(--color-bg); border: 1px solid var(--color-border); color: var(--color-text-secondary);">
        NPV(r) = -CAPEX + SUM(CF<sub>t</sub>/(1+r)<sup>t</sup>) = 0
        <div class="pl-4 text-[10px] space-y-0.5 mt-1" style="color: var(--color-text-secondary);">
          <div>Newton-Raphson: r<sub>k+1</sub> = r<sub>k</sub> - NPV(r<sub>k</sub>)/NPV'(r<sub>k</sub>)</div>
          <div>Project IRR: {{ $t('financialDashboard.projectIRR') }}</div>
          <div>Equity IRR: {{ $t('financialDashboard.equityIRR') }}</div>
        </div>
      </div>
    </div>

    <div class="p-3 rounded-lg space-y-1.5" style="background: var(--color-bg-secondary); border: 1px solid rgba(6,182,212,0.2);">
      <div class="text-[11px] font-bold" style="color: var(--color-accent-secondary);">
        {{ $t('formulaLab.op9Title') }}
      </div>
      <div class="text-[10px] mb-1.5 leading-relaxed" style="color: var(--color-text-muted);">
        {{ $t('formulaLab.op9Desc') }}
      </div>
      <div class="p-2.5 rounded font-mono overflow-x-auto text-[11px] leading-relaxed" style="background: var(--color-bg); border: 1px solid var(--color-border); color: var(--color-text-secondary);">
        DSCR<sub>year</sub> = (EBITDA - Tax) / DebtService<sub>year</sub>
        <div class="pl-4 text-[10px] space-y-0.5 mt-1" style="color: var(--color-text-secondary);">
          <div>EBITDA = Revenue - OPEX</div>
          <div>TaxableIncome = EBITDA - Depreciation - Interest</div>
          <div>Tax = Max(0, TaxableIncome × TaxRate)</div>
          <div>DebtService<sub>year</sub> = InterestPayment + PrincipalRepayment</div>
        </div>
      </div>
    </div>

    <div class="p-3 rounded-lg space-y-1.5" style="background: var(--color-bg-secondary); border: 1px solid rgba(132,204,22,0.2);">
      <div class="text-[11px] font-bold" style="color: #84cc16;">
        {{ $t('formulaLab.op10Title') }}
      </div>
      <div class="text-[10px] mb-1.5 leading-relaxed" style="color: var(--color-text-muted);">
        {{ $t('formulaLab.op10Desc') }}
      </div>
      <div class="p-2.5 rounded font-mono overflow-x-auto text-[11px] leading-relaxed" style="background: var(--color-bg); border: 1px solid var(--color-border); color: var(--color-text-secondary);">
        {{ $t('formulaLab.op10Title') }}
        <div class="pl-4 text-[10px] space-y-0.5 mt-1" style="color: var(--color-text-secondary);">
          <div>Static: CumulativeCashFlow(year) >= 0</div>
          <div>Dynamic: DiscountedCumulativeCashFlow(year) >= 0</div>
        </div>
      </div>
    </div>

    <div class="p-3 rounded-lg space-y-1.5" style="background: var(--color-bg-secondary); border: 1px solid rgba(139,92,246,0.2);">
      <div class="text-[11px] font-bold" style="color: #8b5cf6;">
        {{ $t('formulaLab.op11Title') }}
      </div>
      <div class="text-[10px] mb-1.5 leading-relaxed" style="color: var(--color-text-muted);">
        {{ $t('formulaLab.op11Desc') }}
      </div>
      <div class="p-2.5 rounded font-mono overflow-x-auto text-[11px] leading-relaxed" style="background: var(--color-bg); border: 1px solid var(--color-border); color: var(--color-text-secondary);">
        AugCapex<sub>year</sub> = AugQty × RatedEnergy × ContainerCost<sub>base</sub> × (1 - CostDeclineRate)<sup>year</sup> + AugQty × InstallCost
        <div class="pl-4 text-[10px] mt-1" style="color: var(--color-text-secondary);">
          CostDeclineRate: {{ $t('financialDashboard.costDecline') }}<br>
          InstallCost: {{ $t('financialDashboard.augInstallCost') }}
        </div>
      </div>
    </div>

    <div class="mt-4">
      <div 
        class="flex items-center justify-between p-3 rounded-lg cursor-pointer transition-all"
        style="background: linear-gradient(135deg, #1e3a5f, #2F5496);"
        @click="showAuxPanel = !showAuxPanel">
        <div class="flex items-center gap-2">
          <span class="text-white text-xs font-bold">BESS 辅助功耗计算器</span>
          <span class="text-white/70 text-[10px]">(点击展开/收起 -- 与辅耗计算页面实时同步)</span>
        </div>
        <span class="text-white/90 text-lg transition-transform" :style="{ transform: showAuxPanel ? 'rotate(180deg)' : 'rotate(0deg)' }">&#9660;</span>
      </div>
      
      <div 
        v-show="showAuxPanel" 
        class="mt-2 rounded-lg p-3 space-y-3 border transition-all"
        style="background-color: var(--color-card); border-color: rgba(47,84,150,0.3);">

        <div class="rounded-lg p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <div class="flex justify-between items-center mb-2">
            <span class="text-xs font-bold" style="color: var(--color-accent-secondary);">1. 直流侧总能耗 (DC Total Aux)</span>
            <span class="text-xs px-2 py-0.5 rounded font-bold" style="background-color: var(--color-accent-secondary); color: white;">{{ auxResults.dcTotalAux.toFixed(2) }} MWh</span>
          </div>
          <div class="text-[10px] font-mono rounded p-2 leading-relaxed" style="background-color: var(--color-input-bg-dark); color: var(--color-text);">
            DC_Aux = [(
            <input type="number" v-model.number="auxState.days" class="formula-input w-12" />天 × 
            <input type="number" v-model.number="auxState.cycles" step="0.5" class="formula-input w-8" />次 × 
            <input type="number" v-model.number="auxState.hours" step="0.5" class="formula-input w-8" />h × 
            <span style="color: var(--color-text-muted);">2</span> × 
            <input type="number" v-model.number="auxState.bRun" class="formula-input w-8" />kW) + 
            (<span style="color: var(--color-text-muted);">24</span>h - 
            <input type="number" v-model.number="auxState.cycles" step="0.5" class="formula-input w-8" />次 × 
            <input type="number" v-model.number="auxState.hours" step="0.5" class="formula-input w-8" />h × 
            <span style="color: var(--color-text-muted);">2</span>) × 
            <input type="number" v-model.number="auxState.days" class="formula-input w-8" />天 × 
            <input type="number" v-model.number="auxState.bStd" step="0.5" class="formula-input w-8" />kW] × 
            <input type="number" v-model.number="auxState.units" class="formula-input w-8" />台 / 1000
          </div>
          <div class="text-[10px] mt-2" style="color: var(--color-text-muted);">
            tRun = days × cycles × hours × 2; tStd = days × 24 - tRun; DC_Aux = (tRun × bRun + tStd × bStd) × units / 1000
          </div>
        </div>

        <div class="rounded-lg p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <div class="flex justify-between items-center mb-2">
            <span class="text-xs font-bold" style="color: var(--color-accent-secondary);">2. 交流侧总能耗 (AC Total Aux)</span>
            <span class="text-xs px-2 py-0.5 rounded font-bold" style="background-color: var(--color-accent-secondary); color: white;">{{ auxResults.acTotalAux.toFixed(2) }} MWh</span>
          </div>
          <div class="text-[10px] font-mono rounded p-2 leading-relaxed" style="background-color: var(--color-input-bg-dark); color: var(--color-text);">
            AC_Aux = [(
            <input type="number" v-model.number="auxState.days" class="formula-input w-12" />天 × 
            <input type="number" v-model.number="auxState.cycles" step="0.5" class="formula-input w-8" />次 × 
            <input type="number" v-model.number="auxState.hours" step="0.5" class="formula-input w-8" />h × 
            <span style="color: var(--color-text-muted);">2</span> × 
            <input type="number" v-model.number="auxState.pRun" step="0.5" class="formula-input w-8" />kW) + 
            (<span style="color: var(--color-text-muted);">24</span>h - 
            <input type="number" v-model.number="auxState.cycles" step="0.5" class="formula-input w-8" />次 × 
            <input type="number" v-model.number="auxState.hours" step="0.5" class="formula-input w-8" />h × 
            <span style="color: var(--color-text-muted);">2</span>) × 
            <input type="number" v-model.number="auxState.days" class="formula-input w-8" />天 × 
            <input type="number" v-model.number="auxState.pStd" step="0.5" class="formula-input w-8" />kW + 
            <input type="number" v-model.number="auxState.days" class="formula-input w-8" />天 × 
            <span style="color: var(--color-text-muted);">24</span>h × 
            <input type="number" v-model.number="auxState.pStation" step="0.5" class="formula-input w-8" />kW] / 1000
          </div>
          <div class="text-[10px] mt-2" style="color: var(--color-text-muted);">
            AC_Aux = (tRun × pRun + tStd × pStd + days × 24 × pStation) / 1000
          </div>
        </div>

        <div class="rounded-lg p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <div class="flex justify-between items-center mb-2">
            <span class="text-xs font-bold" style="color: var(--color-accent-secondary);">3. 全系统总辅助能耗 (Total System Aux)</span>
            <span class="text-xs px-2 py-0.5 rounded font-bold" style="background-color: var(--color-accent-secondary); color: white;">{{ auxResults.totalSystemAux.toFixed(2) }} MWh</span>
          </div>
          <div class="text-[10px] font-mono rounded p-2" style="background-color: var(--color-input-bg-dark); color: var(--color-text);">
            Total_Aux = {{ auxResults.dcTotalAux.toFixed(2) }} MWh + {{ auxResults.acTotalAux.toFixed(2) }} MWh
          </div>
        </div>

        <div class="rounded-lg p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <div class="flex justify-between items-center mb-2">
            <span class="text-xs font-bold" style="color: var(--color-accent-secondary);">4. POI并网点期末净可用电量 (POI Net Delivery)</span>
            <span class="text-xs px-2 py-0.5 rounded font-bold" style="background-color: var(--color-accent-secondary); color: white;">{{ auxResults.annualNetDischarge.toFixed(2) }} MWh</span>
          </div>
          <div class="text-[10px] font-mono rounded p-2 leading-relaxed" style="background-color: var(--color-input-bg-dark); color: var(--color-text);">
            POI_Net = (<input type="number" v-model.number="auxState.cap" class="formula-input w-8" />MWh × 
            <input type="number" v-model.number="auxState.units" class="formula-input w-8" />台 × 
            {{ auxResults.sqrtRte.toFixed(4) }} × 
            <input type="number" v-model.number="auxState.cycles" step="0.5" class="formula-input w-8" />次 × 
            <input type="number" v-model.number="auxState.days" class="formula-input w-8" />天 × 
            <input type="number" v-model.number="auxState.acEff" step="0.002" class="formula-input w-10" /> × 
            <input type="number" v-model.number="auxState.pcsEff" step="0.002" class="formula-input w-10" />) - 
            {{ auxResults.totalSystemAux.toFixed(2) }} MWh
          </div>
          <div class="text-[10px] mt-2" style="color: var(--color-text-muted);">
            Gross = cap × units × sqrt(dcRte) × cycles × days × acEff × pcsEff; Net = Gross - Total_Aux
          </div>
        </div>
      </div>
    </div>

    <div class="mt-4">
      <div 
        class="algorithm-panel-header flex items-center justify-between p-3 rounded-lg cursor-pointer transition-all"
        style="background-color: var(--color-accent);"
        @click="showAlgorithmPanel = !showAlgorithmPanel">
        <div class="flex items-center gap-2">
          <span class="text-white text-xs font-medium">⚙️ 算法模型管理</span>
          <span class="text-white/70 text-[10px]">(点击展开/收起)</span>
        </div>
        <span class="text-white/90 text-lg transition-transform" :style="{ transform: showAlgorithmPanel ? 'rotate(180deg)' : 'rotate(0deg)' }">▼</span>
      </div>
      
      <div 
        v-show="showAlgorithmPanel" 
        class="algorithm-panel-body mt-2 rounded-lg border transition-all"
        style="background-color: var(--color-bg); border-color: var(--color-accent-glow);">
        <AlgorithmLab />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AlgorithmLab from '../views/AlgorithmLab.vue'
import { useAuxPower } from '../composables/useAuxPower.js'

defineProps({ params: Object })
defineEmits(['update'])

const showAlgorithmPanel = ref(false)
const showAuxPanel = ref(false)

const { state: auxState, results: auxResults } = useAuxPower()
</script>
