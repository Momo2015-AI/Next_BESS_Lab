<template>
  <div class="flex-1 overflow-auto rounded-xl p-4 space-y-3 card">
    <div>
      <h2 class="section-title text-accent">
        {{ $t('formulaLab.physicsTitle') }}
      </h2>
      <p class="text-[11px] mt-0.5 text-secondary">
        {{ $t('formulaLab.physicsDesc') }}
      </p>
    </div>

    <div class="p-3 rounded-lg space-y-1.5 accent-border-glow">
      <div class="text-[11px] font-bold text-accent">
        {{ $t('formulaLab.op1Title') }}
      </div>
      <div class="p-2.5 rounded font-mono leading-relaxed overflow-x-auto text-[11px] card-panel text-secondary">
        E
        <sub>gross</sub>
        (i) =
        <input
          type="number"
          :value="params.ratedEnergy"
          step="0.1"
          class="formula-input w-12"
          @input="$emit('update', 'ratedEnergy', Number($event.target.value))"
        />
        MWh ×
        <input
          type="number"
          :value="params.initContainerQty"
          step="1"
          class="formula-input w-14"
          @input="$emit('update', 'initContainerQty', Number($event.target.value))"
        />
        {{ $t('paramPanel.units') }} × SOH(i) × RTE(i) × DOD(i) × (
        <input
          type="number"
          :value="params.acEfficiency"
          step="0.01"
          class="formula-input w-14"
          @input="$emit('update', 'acEfficiency', Number($event.target.value))"
        />
        / 100 )
      </div>
    </div>

    <div class="p-3 rounded-lg space-y-2 warning-border-glow">
      <div class="text-[11px] font-bold text-warning">
        {{ $t('formulaLab.op2Title') }}
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3 font-mono text-[11px]">
        <div class="p-2 rounded space-y-1 card-panel">
          <span class="font-bold block text-[10px] text-warning">A. {{ $t('paramPanel.dailyRunTotal') }}:</span>
          <div>
            {{ $t('paramPanel.dailyRunTotal') }} (RunHours) =
            <input
              type="number"
              :value="params.duration"
              step="0.5"
              class="formula-input w-10"
              @input="$emit('update', 'duration', Number($event.target.value))"
            />
            h ×
            <input
              type="number"
              :value="params.cyclesPerDay"
              step="1"
              class="formula-input w-8"
              @input="$emit('update', 'cyclesPerDay', Number($event.target.value))"
            />
            {{ $t('paramPanel.times') }}
          </div>
          <div class="pt-0.5 border-t-border">
            {{ $t('paramPanel.dailyStandby') }} (StandbyHours) = Max(0, 24 - RunHours)
          </div>
        </div>
        <div class="p-2 rounded space-y-1 card-panel">
          <span class="font-bold block text-[10px] text-warning">B. {{ $t('paramPanel.auxPower') }}:</span>
          <div class="grid grid-cols-2 gap-x-2 text-[10px]">
            <div>
              {{ $t('paramPanel.bessAuxRun') }}:
              <input
                type="number"
                :value="params.bessAuxRun"
                step="0.001"
                class="formula-input w-16"
                @input="$emit('update', 'bessAuxRun', Number($event.target.value))"
              />
              kW
            </div>
            <div>
              {{ $t('paramPanel.bessAuxStandby') }}:
              <input
                type="number"
                :value="params.bessAuxStandby"
                step="0.1"
                class="formula-input w-12"
                @input="$emit('update', 'bessAuxStandby', Number($event.target.value))"
              />
              kW
            </div>
            <div>
              {{ $t('paramPanel.pcsAuxRun') }}:
              <input
                type="number"
                :value="params.pcsAuxRun"
                step="0.1"
                class="formula-input w-12"
                @input="$emit('update', 'pcsAuxRun', Number($event.target.value))"
              />
              kW
            </div>
            <div>
              {{ $t('paramPanel.pcsAuxStandby') }}:
              <input
                type="number"
                :value="params.pcsAuxStandby"
                step="0.1"
                class="formula-input w-12"
                @input="$emit('update', 'pcsAuxStandby', Number($event.target.value))"
              />
              kW
            </div>
          </div>
        </div>
      </div>
      <div class="p-2.5 rounded font-mono leading-relaxed overflow-x-auto text-[11px] card-panel text-secondary">
        Aux
        <sub>total</sub>
        = { {{ $t('paramPanel.initContainerQty') }} × [({{ $t('paramPanel.bessAuxRun') }} × RunHours +
        {{ $t('paramPanel.bessAuxStandby') }} × StandbyHours) / 1000] +
        <input
          type="number"
          :value="params.initPcsQty"
          step="1"
          class="formula-input w-12"
          @input="$emit('update', 'initPcsQty', Number($event.target.value))"
        />
        {{ $t('paramPanel.units') }} × [({{ $t('paramPanel.pcsAuxRun') }} × RunHours +
        {{ $t('paramPanel.pcsAuxStandby') }} × StandbyHours) / 1000] } / {{ $t('paramPanel.cyclesPerDay') }}
      </div>
    </div>

    <div class="p-3 rounded-lg space-y-1.5 pink-border-glow">
      <div class="text-[11px] font-bold text-info">
        {{ $t('formulaLab.op3Title') }}
      </div>
      <div class="p-2.5 rounded font-mono overflow-x-auto text-[11px] card-panel text-secondary">
        {{ $t('formulaLab.op3Title') }}
        <div class="my-1 p-1.5 rounded text-[10px] card-input text-info">
          {{ $t('formulaLab.op3Title') }} (Age) = i - k
        </div>
        E
        <sub>aug_net</sub>
        (i) = SUM(k≤i) [ {{ $t('paramPanel.ratedEnergy') }} × {{ $t('matrixTable.augQty') }} × SOH
        <sub>target</sub>
        × RTE(i) × DOD(i) × η
        <sub>ac</sub>
        - {{ $t('matrixTable.augQty') }} × {{ $t('paramPanel.singleCycleAux') }} ]
      </div>
    </div>

    <div class="p-3 rounded-lg space-y-1.5 green-border-glow">
      <div class="text-[11px] font-bold text-success">
        {{ $t('formulaLab.op4Title') }}
      </div>
      <div class="p-2.5 rounded font-mono overflow-x-auto text-[11px] card-panel text-secondary">
        E
        <sub>net_total</sub>
        (i) = Max(0, E
        <sub>gross_init</sub>
        - Aux
        <sub>init</sub>
        ) + E
        <sub>aug_net</sub>
        (i)
        <div class="mt-1 text-secondary">
          {{ $t('matrixTable.meetsReq') }}: E
          <sub>net_total</sub>
          (i) >=
          <input
            type="number"
            :value="params.requiredEnergy"
            step="1"
            class="formula-input w-14 text-warning"
            @input="$emit('update', 'requiredEnergy', Number($event.target.value))"
          />
          MWh ?
          <span class="text-success">"{{ $t('common.yes') }}"</span>
          :
          <span class="text-danger">"{{ $t('common.no') }}"</span>
        </div>
      </div>
    </div>

    <div class="p-3 rounded-lg space-y-1.5 blue-border-glow">
      <div class="text-[11px] font-bold text-accent">
        {{ $t('formulaLab.opAcRteTitle') }}
      </div>
      <div class="text-[10px] mb-1 leading-relaxed text-muted">
        {{ $t('formulaLab.opAcRteDesc') }}
      </div>
      <div class="p-2.5 rounded font-mono overflow-x-auto text-[11px] space-y-2 card-panel text-secondary">
        <div>
          <span class="text-accent">
            AC-RTE
            <sub>不带辅耗</sub>
          </span>
          = DC-RTE
          <sub>year1</sub>
          × η
          <sub>AC</sub>
          × 100%
        </div>
        <div class="border-t-border pt-2">
          <span class="text-accent">
            AC-RTE
            <sub>带辅耗</sub>
          </span>
          = AC-RTE
          <sub>不带辅耗</sub>
          × (1 - Ratio
          <sub>aux</sub>
          )
        </div>
        <div class="text-[10px] pl-4 space-y-0.5 mt-1 text-muted">
          <div>
            Ratio
            <sub>aux</sub>
            = Aux
            <sub>init</sub>
            [0] / E
            <sub>gross_init</sub>
            [0]
          </div>
          <div>
            η
            <sub>AC</sub>
            = acEfficiency / 100
          </div>
          <div class="text-warning mt-0.5">
            {{ $t('formulaLab.opAcRteNote') }}
          </div>
        </div>
      </div>
    </div>

    <div class="pt-3 border-t-border">
      <h2 class="section-title text-warning">
        {{ $t('formulaLab.financeTitle') }}
      </h2>
    </div>

    <div class="p-3 rounded-lg space-y-1.5 yellow-border-glow">
      <div class="text-[11px] font-bold text-warning">
        {{ $t('formulaLab.op5Title') }}
      </div>
      <div class="text-[10px] mb-1.5 leading-relaxed text-muted">
        {{ $t('formulaLab.op5Desc') }}
      </div>
      <div class="p-2.5 rounded font-mono overflow-x-auto text-[11px] leading-relaxed card-panel text-secondary">
        Revenue
        <sub>year</sub>
        = EnergyArbitrage + CapacityPayment + AncillaryService
        <div class="pl-4 text-[10px] space-y-0.5 mt-1 text-secondary">
          <div>
            EnergyArbitrage
            <sub>year</sub>
            = DischargedMWh × (PeakPrice - OffPeakPrice) × SpreadCaptureRate
          </div>
          <div>
            CapacityPayment
            <sub>year</sub>
            = ContractedMW × CapacityPrice
            <sub>perMW</sub>
          </div>
          <div>
            AncillaryService
            <sub>year</sub>
            = AvailableMW × AncillaryPrice
            <sub>perMW</sub>
          </div>
        </div>
      </div>
    </div>

    <div class="p-3 rounded-lg space-y-1.5 orange-border-glow">
      <div class="text-[11px] font-bold text-warning">
        {{ $t('formulaLab.op6Title') }}
      </div>
      <div class="text-[10px] mb-1.5 leading-relaxed text-muted">
        {{ $t('formulaLab.op6Desc') }}
      </div>
      <div class="p-2.5 rounded font-mono overflow-x-auto text-[11px] leading-relaxed card-panel text-secondary">
        <div>
          CAPEX
          <sub>total</sub>
          = ContainerCost + PCSCost + BOP + DevelopmentFee
        </div>
        <div class="pl-4 text-[10px] mt-1 text-secondary">
          ContainerCost = UnitCost
          <sub>perMWh</sub>
          × TotalMWh
          <br />
          PCSCost = UnitCost
          <sub>perMW</sub>
          × TotalMW
          <br />
          BOP = BOPCost
          <sub>perMWh</sub>
          × TotalMWh
          <br />
          DevelopmentFee = DevCost
          <sub>perMW</sub>
          × TotalMW
        </div>
        <div class="mt-2">
          OPEX
          <sub>year</sub>
          = FixedO&M + VarO&M + Insurance + LandLease
        </div>
        <div class="pl-4 text-[10px] mt-1 text-secondary">
          FixedO&M
          <sub>year</sub>
          = FixedRate
          <sub>perKW</sub>
          × TotalMW × 1000 × (1+escalation)
          <sup>year</sup>
          <br />
          VarO&M
          <sub>year</sub>
          = VarRate
          <sub>perMWh</sub>
          × AnnualThroughput × (1+escalation)
          <sup>year</sup>
          <br />
          Insurance
          <sub>year</sub>
          = CAPEX × InsuranceRate
          <br />
          LandLease
          <sub>year</sub>
          = {{ $t('formulaLab.op6Title') }}
        </div>
      </div>
    </div>

    <div class="p-3 rounded-lg space-y-1.5 danger-border-glow">
      <div class="text-[11px] font-bold text-danger">
        {{ $t('formulaLab.op7Title') }}
      </div>
      <div class="text-[10px] mb-1.5 leading-relaxed text-muted">
        {{ $t('formulaLab.op7Desc') }}
      </div>
      <div class="p-2.5 rounded font-mono overflow-x-auto text-[11px] leading-relaxed card-panel text-secondary">
        LCOS = TotalDiscountedCosts / TotalDiscountedEnergy
        <div class="pl-4 text-[10px] space-y-0.5 mt-1 text-secondary">
          <div>
            TotalDiscountedCosts = CAPEX + SUM(OPEX
            <sub>t</sub>
            /(1+r)
            <sup>t</sup>
            ) + SUM(Augmentation
            <sub>t</sub>
            /(1+r)
            <sup>t</sup>
            ) - Residual/(1+r)
            <sup>T</sup>
          </div>
          <div>
            TotalDiscountedEnergy = SUM(AnnualDischargedMWh
            <sub>t</sub>
            /(1+r)
            <sup>t</sup>
            )
          </div>
        </div>
      </div>
    </div>

    <div class="p-3 rounded-lg space-y-1.5 indigo-border-glow">
      <div class="text-[11px] font-bold text-info">
        {{ $t('formulaLab.op8Title') }}
      </div>
      <div class="text-[10px] mb-1.5 leading-relaxed text-muted">
        {{ $t('formulaLab.op8Desc') }}
      </div>
      <div class="p-2.5 rounded font-mono overflow-x-auto text-[11px] leading-relaxed card-panel text-secondary">
        NPV(r) = -CAPEX + SUM(CF
        <sub>t</sub>
        /(1+r)
        <sup>t</sup>
        ) = 0
        <div class="pl-4 text-[10px] space-y-0.5 mt-1 text-secondary">
          <div>
            Newton-Raphson: r
            <sub>k+1</sub>
            = r
            <sub>k</sub>
            - NPV(r
            <sub>k</sub>
            )/NPV'(r
            <sub>k</sub>
            )
          </div>
          <div>Project IRR: {{ $t('financialDashboard.projectIRR') }}</div>
          <div>Equity IRR: {{ $t('financialDashboard.equityIRR') }}</div>
        </div>
      </div>
    </div>

    <div class="p-3 rounded-lg space-y-1.5 cyan-border-glow">
      <div class="text-[11px] font-bold text-accent-secondary">
        {{ $t('formulaLab.op9Title') }}
      </div>
      <div class="text-[10px] mb-1.5 leading-relaxed text-muted">
        {{ $t('formulaLab.op9Desc') }}
      </div>
      <div class="p-2.5 rounded font-mono overflow-x-auto text-[11px] leading-relaxed card-panel text-secondary">
        DSCR
        <sub>year</sub>
        = (EBITDA - Tax) / DebtService
        <sub>year</sub>
        <div class="pl-4 text-[10px] space-y-0.5 mt-1 text-secondary">
          <div>EBITDA = Revenue - OPEX</div>
          <div>TaxableIncome = EBITDA - Depreciation - Interest</div>
          <div>Tax = Max(0, TaxableIncome × TaxRate)</div>
          <div>
            DebtService
            <sub>year</sub>
            = InterestPayment + PrincipalRepayment
          </div>
        </div>
      </div>
    </div>

    <div class="p-3 rounded-lg space-y-1.5 lime-border-glow">
      <div class="text-[11px] font-bold lime-text">
        {{ $t('formulaLab.op10Title') }}
      </div>
      <div class="text-[10px] mb-1.5 leading-relaxed text-muted">
        {{ $t('formulaLab.op10Desc') }}
      </div>
      <div class="p-2.5 rounded font-mono overflow-x-auto text-[11px] leading-relaxed card-panel text-secondary">
        {{ $t('formulaLab.op10Title') }}
        <div class="pl-4 text-[10px] space-y-0.5 mt-1 text-secondary">
          <div>Static: CumulativeCashFlow(year) >= 0</div>
          <div>Dynamic: DiscountedCumulativeCashFlow(year) >= 0</div>
        </div>
      </div>
    </div>

    <div class="p-3 rounded-lg space-y-1.5 purple-border-glow">
      <div class="text-[11px] font-bold text-info">
        {{ $t('formulaLab.op11Title') }}
      </div>
      <div class="text-[10px] mb-1.5 leading-relaxed text-muted">
        {{ $t('formulaLab.op11Desc') }}
      </div>
      <div class="p-2.5 rounded font-mono overflow-x-auto text-[11px] leading-relaxed card-panel text-secondary">
        AugCapex
        <sub>year</sub>
        = AugQty × RatedEnergy × ContainerCost
        <sub>base</sub>
        × (1 - CostDeclineRate)
        <sup>year</sup>
        + AugQty × InstallCost
        <div class="pl-4 text-[10px] mt-1 text-secondary">
          CostDeclineRate: {{ $t('financialDashboard.costDecline') }}
          <br />
          InstallCost: {{ $t('financialDashboard.augInstallCost') }}
        </div>
      </div>
    </div>

    <div class="mt-4">
      <div
        class="flex items-center justify-between p-3 rounded-lg cursor-pointer transition-all algorithm-panel-header"
        @click="showAuxPanel = !showAuxPanel"
      >
        <div class="flex items-center gap-2">
          <span class="text-white text-xs font-bold">BESS 辅助功耗计算器</span>
          <span class="text-white/70 text-[10px]">(点击展开/收起 -- 与辅耗计算页面实时同步)</span>
        </div>
        <span
          class="text-white/90 text-lg transition-transform"
          :style="{ transform: showAuxPanel ? 'rotate(180deg)' : 'rotate(0deg)' }"
        >
          &#9660;
        </span>
      </div>

      <div v-show="showAuxPanel" class="mt-2 rounded-lg p-3 space-y-3 border transition-all bg-card blue-border-glow">
        <div class="rounded-lg p-3 card-panel-bordered">
          <div class="flex justify-between items-center mb-2">
            <span class="text-xs font-bold text-accent-secondary">1. 直流侧总能耗 (DC Total Aux)</span>
            <span class="text-xs px-2 py-0.5 rounded font-bold bg-accent-secondary text-white">
              {{ auxResults.dcTotalAux.toFixed(2) }} MWh
            </span>
          </div>
          <div class="text-[10px] font-mono rounded p-2 leading-relaxed card-input-dark">
            DC_Aux = [(
            <input v-model.number="auxState.days" type="number" class="formula-input w-12" />
            天 ×
            <input v-model.number="auxState.cycles" type="number" step="0.5" class="formula-input w-8" />
            次 ×
            <input v-model.number="auxState.hours" type="number" step="0.5" class="formula-input w-8" />
            h ×
            <span class="text-muted">2</span>
            ×
            <input v-model.number="auxState.bRun" type="number" class="formula-input w-8" />
            kW) + (
            <span class="text-muted">24</span>
            h -
            <input v-model.number="auxState.cycles" type="number" step="0.5" class="formula-input w-8" />
            次 ×
            <input v-model.number="auxState.hours" type="number" step="0.5" class="formula-input w-8" />
            h ×
            <span class="text-muted">2</span>
            ) ×
            <input v-model.number="auxState.days" type="number" class="formula-input w-8" />
            天 ×
            <input v-model.number="auxState.bStd" type="number" step="0.5" class="formula-input w-8" />
            kW] ×
            <input v-model.number="auxState.units" type="number" class="formula-input w-8" />
            台 / 1000
          </div>
          <div class="text-[10px] mt-2 text-muted">
            tRun = days × cycles × hours × 2; tStd = days × 24 - tRun; DC_Aux = (tRun × bRun + tStd × bStd) × units /
            1000
          </div>
        </div>

        <div class="rounded-lg p-3 card-panel-bordered">
          <div class="flex justify-between items-center mb-2">
            <span class="text-xs font-bold text-accent-secondary">2. 交流侧总能耗 (AC Total Aux)</span>
            <span class="text-xs px-2 py-0.5 rounded font-bold bg-accent-secondary text-white">
              {{ auxResults.acTotalAux.toFixed(2) }} MWh
            </span>
          </div>
          <div class="text-[10px] font-mono rounded p-2 leading-relaxed card-input-dark">
            AC_Aux = [(
            <input v-model.number="auxState.days" type="number" class="formula-input w-12" />
            天 ×
            <input v-model.number="auxState.cycles" type="number" step="0.5" class="formula-input w-8" />
            次 ×
            <input v-model.number="auxState.hours" type="number" step="0.5" class="formula-input w-8" />
            h ×
            <span class="text-muted">2</span>
            ×
            <input v-model.number="auxState.pRun" type="number" step="0.5" class="formula-input w-8" />
            kW) + (
            <span class="text-muted">24</span>
            h -
            <input v-model.number="auxState.cycles" type="number" step="0.5" class="formula-input w-8" />
            次 ×
            <input v-model.number="auxState.hours" type="number" step="0.5" class="formula-input w-8" />
            h ×
            <span class="text-muted">2</span>
            ) ×
            <input v-model.number="auxState.days" type="number" class="formula-input w-8" />
            天 ×
            <input v-model.number="auxState.pStd" type="number" step="0.5" class="formula-input w-8" />
            kW +
            <input v-model.number="auxState.days" type="number" class="formula-input w-8" />
            天 ×
            <span class="text-muted">24</span>
            h ×
            <input v-model.number="auxState.pStation" type="number" step="0.5" class="formula-input w-8" />
            kW] / 1000
          </div>
          <div class="text-[10px] mt-2 text-muted">
            AC_Aux = (tRun × pRun + tStd × pStd + days × 24 × pStation) / 1000
          </div>
        </div>

        <div class="rounded-lg p-3 card-panel-bordered">
          <div class="flex justify-between items-center mb-2">
            <span class="text-xs font-bold text-accent-secondary">3. 全系统总辅助能耗 (Total System Aux)</span>
            <span class="text-xs px-2 py-0.5 rounded font-bold bg-accent-secondary text-white">
              {{ auxResults.totalSystemAux.toFixed(2) }} MWh
            </span>
          </div>
          <div class="text-[10px] font-mono rounded p-2 card-input-dark">
            Total_Aux = {{ auxResults.dcTotalAux.toFixed(2) }} MWh + {{ auxResults.acTotalAux.toFixed(2) }} MWh
          </div>
        </div>

        <div class="rounded-lg p-3 card-panel-bordered">
          <div class="flex justify-between items-center mb-2">
            <span class="text-xs font-bold text-accent-secondary">4. POI并网点期末净可用电量 (POI Net Delivery)</span>
            <span class="text-xs px-2 py-0.5 rounded font-bold bg-accent-secondary text-white">
              {{ auxResults.annualNetDischarge.toFixed(2) }} MWh
            </span>
          </div>
          <div class="text-[10px] font-mono rounded p-2 leading-relaxed card-input-dark">
            POI_Net = (
            <input v-model.number="auxState.cap" type="number" class="formula-input w-8" />
            MWh ×
            <input v-model.number="auxState.units" type="number" class="formula-input w-8" />
            台 × {{ auxResults.sqrtRte.toFixed(4) }} ×
            <input v-model.number="auxState.cycles" type="number" step="0.5" class="formula-input w-8" />
            次 ×
            <input v-model.number="auxState.days" type="number" class="formula-input w-8" />
            天 ×
            <input v-model.number="auxState.acEff" type="number" step="0.002" class="formula-input w-10" />
            ×
            <input v-model.number="auxState.pcsEff" type="number" step="0.002" class="formula-input w-10" />
            ) - {{ auxResults.totalSystemAux.toFixed(2) }} MWh
          </div>
          <div class="text-[10px] mt-2 text-muted">
            Gross = cap × units × sqrt(dcRte) × cycles × days × acEff × pcsEff; Net = Gross - Total_Aux
          </div>
        </div>
      </div>
    </div>

    <div class="mt-4">
      <div
        class="algorithm-panel-header flex items-center justify-between p-3 rounded-lg cursor-pointer transition-all bg-accent"
        @click="showAlgorithmPanel = !showAlgorithmPanel"
      >
        <div class="flex items-center gap-2">
          <span class="text-white text-xs font-medium">⚙️ 算法模型管理</span>
          <span class="text-white/70 text-[10px]">(点击展开/收起)</span>
        </div>
        <span
          class="text-white/90 text-lg transition-transform"
          :style="{ transform: showAlgorithmPanel ? 'rotate(180deg)' : 'rotate(0deg)' }"
        >
          ▼
        </span>
      </div>

      <div
        v-show="showAlgorithmPanel"
        class="algorithm-panel-body mt-2 rounded-lg border transition-all accent-border-glow"
      >
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
