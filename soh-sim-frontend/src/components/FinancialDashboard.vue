<template>
  <div class="h-full overflow-y-auto custom-scrollbar flex flex-col">
    <div class="flex-1 overflow-y-auto space-y-3 py-2 px-4">
      <div class="grid grid-cols-4 md:grid-cols-8 gap-2 mb-3">
        <div
          v-for="(m, idx) in metrics"
          :key="m.label"
          class="rounded-lg p-3 text-center transition-all hover:shadow-md"
          :style="{
            backgroundColor: 'var(--color-card)',
            border: '1px solid var(--color-border)',
            borderTop: '3px solid ' + (metrics[idx]?.borderColor || 'var(--color-accent)')
          }"
        >
          <div class="text-[9px] uppercase tracking-wider truncate" style="color: var(--color-text-muted)">
            {{ m.label }}
          </div>
          <div class="text-base md:text-lg font-bold font-mono mt-1" :style="{ color: m.textColor }">
            {{ m.value }}
          </div>
          <div class="text-[8px] mt-0.5" style="color: var(--color-text-muted)">
            {{ m.unit }}
          </div>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div
          class="rounded-lg p-3"
          style="min-height: 300px; background-color: var(--color-card); border: 1px solid var(--color-border)"
        >
          <h3 class="font-bold text-xs mb-2" style="color: var(--color-text)">
            {{ $t('financial.chartCashFlow') }}
          </h3>
          <div ref="cashFlowChartRef" class="w-full" style="height: 280px" />
        </div>
        <div
          class="rounded-lg p-3"
          style="min-height: 300px; background-color: var(--color-card); border: 1px solid var(--color-border)"
        >
          <h3 class="font-bold text-xs mb-2" style="color: var(--color-text)">{{ $t('financial.chartRevenue') }}</h3>
          <div ref="revenueChartRef" class="w-full" style="height: 280px" />
        </div>
        <div
          class="rounded-lg p-3"
          style="min-height: 300px; background-color: var(--color-card); border: 1px solid var(--color-border)"
        >
          <h3 class="font-bold text-xs mb-2" style="color: var(--color-text)">{{ $t('financial.chartDscr') }}</h3>
          <div ref="dscrChartRef" class="w-full" style="height: 280px" />
        </div>
        <div
          class="rounded-lg p-3"
          style="min-height: 300px; background-color: var(--color-card); border: 1px solid var(--color-border)"
        >
          <h3 class="font-bold text-xs mb-2" style="color: var(--color-text)">{{ $t('financial.chartCapex') }}</h3>
          <div ref="capexChartRef" class="w-full" style="height: 280px" />
        </div>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div class="rounded-lg p-3" style="background-color: var(--color-card); border: 1px solid var(--color-border)">
          <h3 class="font-bold text-xs mb-2 flex items-center gap-2" style="color: var(--color-text)">
            <span
              class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold"
              style="background-color: var(--color-accent-glow); color: var(--color-accent)"
            >
              I
            </span>
            {{ $t('financial.sectionRevenueStack') }}
          </h3>
          <div class="grid grid-cols-2 gap-2 text-[10px]" style="color: var(--color-text-secondary)">
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelOffPeakPrice') }}</label>
              <input
                v-model.number="f.offPeakPrice"
                type="number"
                step="0.1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelPeakPrice') }}</label>
              <input
                v-model.number="f.peakPrice"
                type="number"
                step="0.1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelSpreadCapture') }}</label>
              <input
                v-model.number="f.spreadCapture"
                type="number"
                step="0.1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelCalendarDays') }}</label>
              <input
                v-model.number="f.operatingDays"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelCapacityPrice') }}</label>
              <input
                v-model.number="f.capacityPrice"
                type="number"
                step="100"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelAncillaryPrice') }}</label>
              <input
                v-model.number="f.ancillaryPrice"
                type="number"
                step="100"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelPriceEscalation') }}</label>
              <input
                v-model.number="f.priceEscalation"
                type="number"
                step="0.1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelEfficiencyLoss') }}</label>
              <input
                v-model.number="f.efficiencyLossPct"
                type="number"
                step="0.01"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
          </div>
        </div>
        <div class="rounded-lg p-3" style="background-color: var(--color-card); border: 1px solid var(--color-border)">
          <h3 class="font-bold text-xs mb-2 flex items-center gap-2" style="color: var(--color-text)">
            <span
              class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold"
              style="background-color: rgba(245, 158, 11, 0.2); color: var(--color-warning)"
            >
              II
            </span>
            {{ $t('financial.sectionCapexOpex') }}
          </h3>
          <div class="grid grid-cols-2 gap-2 text-[10px]" style="color: var(--color-text-secondary)">
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelContainerCost') }}</label>
              <input
                v-model.number="f.containerCostPerMWh"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelPcsCost') }}</label>
              <input
                v-model.number="f.pcsCostPerMW"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelBopCost') }}</label>
              <input
                v-model.number="f.bopCostPerMWh"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelSubstationCost') }}</label>
              <input
                v-model.number="f.substationCostPerMW"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelTransmissionCost') }}</label>
              <input
                v-model.number="f.transmissionCostPerMW"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelLandCost') }}</label>
              <input
                v-model.number="f.landCostPerMW"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelDevCost') }}</label>
              <input
                v-model.number="f.developmentCostPerMW"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelFixedOm') }}</label>
              <input
                v-model.number="f.fixedOpexPerKW"
                type="number"
                step="0.5"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelVarOm') }}</label>
              <input
                v-model.number="f.varOpexPerMWh"
                type="number"
                step="0.1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelInsuranceRate') }}</label>
              <input
                v-model.number="f.insuranceRate"
                type="number"
                step="0.01"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelOmEscalation') }}</label>
              <input
                v-model.number="f.opexEscalation"
                type="number"
                step="0.1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelVatRate') }}</label>
              <input
                v-model.number="f.vatRate"
                type="number"
                step="0.5"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-3 gap-3">
        <div class="rounded-lg p-3" style="background-color: var(--color-card); border: 1px solid var(--color-border)">
          <h3 class="font-bold text-xs mb-2 flex items-center gap-2" style="color: var(--color-text)">
            <span
              class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold"
              style="background-color: rgba(59, 130, 246, 0.2); color: var(--color-accent-secondary)"
            >
              III
            </span>
            {{ $t('financial.sectionFinancingTax') }}
          </h3>
          <div class="grid grid-cols-1 gap-2 text-[10px]" style="color: var(--color-text-secondary)">
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelDiscountRate') }}</label>
              <input
                v-model.number="f.discountRate"
                type="number"
                step="0.1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelDebtRatio') }}</label>
              <input
                v-model.number="f.debtRatio"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelEquityRatio') }}</label>
              <input
                v-model.number="f.equityRatio"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelLoanRate') }}</label>
              <input
                v-model.number="f.interestRate"
                type="number"
                step="0.1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelCostOfEquity') }}</label>
              <input
                v-model.number="f.costOfEquity"
                type="number"
                step="0.5"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelLoanTenure') }}</label>
              <input
                v-model.number="f.loanTenure"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelTaxRate') }}</label>
              <input
                v-model.number="f.taxRate"
                type="number"
                step="0.5"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelDepreciationYears') }}</label>
              <input
                v-model.number="f.depreciationYears"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelResidualRate') }}</label>
              <input
                v-model.number="f.residualRate"
                type="number"
                step="0.5"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelDepreciationMethod') }}</label>
              <select
                v-model="f.depreciationMethod"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              >
                <option value="straight-line">{{ $t('financial.optStraightLine') }}</option>
                <option value="double-declining">{{ $t('financial.optDoubleDeclining') }}</option>
              </select>
            </div>
          </div>
        </div>
        <div class="rounded-lg p-3" style="background-color: var(--color-card); border: 1px solid var(--color-border)">
          <h3 class="font-bold text-xs mb-2 flex items-center gap-2" style="color: var(--color-text)">
            <span
              class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold"
              style="background-color: rgba(168, 85, 247, 0.2); color: var(--color-info)"
            >
              IV
            </span>
            {{ $t('financial.sectionAugmentation') }}
          </h3>
          <div class="grid grid-cols-1 gap-2 text-[10px]" style="color: var(--color-text-secondary)">
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelAugContainerCost') }}</label>
              <input
                v-model.number="f.augContainerCostPerMWh"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelCostDecline') }}</label>
              <input
                v-model.number="f.costDeclineRate"
                type="number"
                step="0.1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelAugInstallCost') }}</label>
              <input
                v-model.number="f.augInstallCost"
                type="number"
                step="0.5"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelDecommissionCost') }}</label>
              <input
                v-model.number="f.decommissioningCost"
                type="number"
                step="1"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
          </div>
        </div>
        <div class="rounded-lg p-3" style="background-color: var(--color-card); border: 1px solid var(--color-border)">
          <h3 class="font-bold text-xs mb-2 flex items-center gap-2" style="color: var(--color-text)">
            <span
              class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold"
              style="background-color: rgba(16, 185, 129, 0.2); color: var(--color-success)"
            >
              V
            </span>
            {{ $t('financial.sectionSensitivity') }}
          </h3>
          <div class="text-[10px] space-y-1.5" style="color: var(--color-text-muted)">
            <div class="flex justify-between">
              <span>{{ $t('financial.labelPriceVolatility') }}</span>
              <span style="color: var(--color-text-secondary)">+/-{{ f.sensPct }}%</span>
            </div>
            <div class="flex justify-between">
              <span>{{ $t('financial.labelDegradationVolatility') }}</span>
              <span style="color: var(--color-text-secondary)">+/-{{ f.sensPct }}%</span>
            </div>
            <div class="flex justify-between">
              <span>{{ $t('financial.labelInterestVolatility') }}</span>
              <span style="color: var(--color-text-secondary)">+/-{{ f.sensPct }}%</span>
            </div>
            <div class="flex justify-between">
              <span>CAPEX {{ $t('financial.labelCapexVolatility') }}</span>
              <span style="color: var(--color-text-secondary)">+/-{{ f.sensPct }}%</span>
            </div>
            <div>
              <label class="block mb-0.5" style="color: var(--color-text-muted)">{{ $t('financial.labelVolatilityRange') }}</label>
              <input
                v-model.number="f.sensPct"
                type="number"
                step="5"
                class="w-full rounded px-2 py-1 text-xs"
                style="
                  background-color: var(--color-input-bg-dark);
                  border: 1px solid var(--color-input-border);
                  color: var(--color-text);
                "
              />
            </div>
          </div>
        </div>
      </div>

      <!-- 货币转换器 -->
      <CurrencyConverter />

      <!-- 产品库→CAPEX 自动联动 -->
      <ProductCAPEXLink @apply-config="handleProductConfig" />

      <div class="grid grid-cols-2 gap-3">
        <EnergyFlowSankey :params="params" :soh="soh" />
        <CostWaterfallChart :params="params" :cash-flow-table="cashFlowTable" />
      </div>

      <div class="rounded-lg p-3" style="background-color: var(--color-card); border: 1px solid var(--color-border)">
        <div class="flex justify-between items-center mb-2">
          <h3 class="font-bold text-xs" style="color: var(--color-text)">{{ $t('financial.tableCashFlowTitle') }}</h3>
          <button
            class="text-[10px] px-3 py-1 rounded transition-colors"
            style="background-color: var(--color-accent); color: white"
            @click="recalc"
          >
            {{ $t('financial.btnRecalculate') }}
          </button>
        </div>
        <div class="overflow-x-auto custom-scrollbar max-h-[300px]">
          <table class="w-full text-[10px] border-collapse">
            <thead>
              <tr class="sticky top-0 z-10" style="background-color: var(--color-card)">
                <th
                  class="text-left py-1 px-2 sticky left-0 z-20"
                  style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)"
                >
                  {{ $t('financial.colYear') }}
                </th>
                <th
                  class="text-right py-1 px-2"
                  style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)"
                >
                  {{ $t('financial.colGeneration') }}
                </th>
                <th
                  class="text-right py-1 px-2"
                  style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)"
                >
                  {{ $t('financial.colArbitrage') }}
                </th>
                <th
                  class="text-right py-1 px-2"
                  style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)"
                >
                  {{ $t('financial.colCapacity') }}
                </th>
                <th
                  class="text-right py-1 px-2"
                  style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)"
                >
                  {{ $t('financial.colAncillary') }}
                </th>
                <th
                  class="text-right py-1 px-2"
                  style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)"
                >
                  {{ $t('financial.colTotalRevenue') }}
                </th>
                <th
                  class="text-right py-1 px-2"
                  style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)"
                >
                  {{ $t('financial.colOpex') }}
                </th>
                <th
                  class="text-right py-1 px-2"
                  style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)"
                >
                  {{ $t('financial.colEbitda') }}
                </th>
                <th
                  class="text-right py-1 px-2"
                  style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)"
                >
                  {{ $t('financial.colNetCashFlow') }}
                </th>
                <th
                  class="text-right py-1 px-2"
                  style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)"
                >
                  {{ $t('financial.colCumCashFlow') }}
                </th>
                <th
                  v-if="f.debtRatio > 0"
                  class="text-right py-1 px-2"
                  style="color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)"
                >
                  {{ $t('financial.colDscr') }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="row in cashFlowTable"
                :key="'yr' + row.year"
                style="border-bottom: 1px solid var(--color-border)"
              >
                <td
                  class="py-1 px-2 sticky left-0 font-bold"
                  :style="
                    row.year === 0
                      ? { backgroundColor: 'var(--color-card)', color: 'var(--color-warning)' }
                      : { backgroundColor: 'var(--color-card)', color: 'var(--color-text-secondary)' }
                  "
                >
                  {{ row.year === 0 ? $t('financial.labelConstruction') : row.year }}
                </td>
                <td class="text-right py-1 px-2 font-mono" style="color: var(--color-text-secondary)">
                  {{ fmtNum(row.energy) }}
                </td>
                <td class="text-right py-1 px-2 font-mono" style="color: var(--color-text-secondary)">
                  {{ fmtNum(row.arbitrage) }}
                </td>
                <td class="text-right py-1 px-2 font-mono" style="color: var(--color-text-secondary)">
                  {{ fmtNum(row.capacity) }}
                </td>
                <td class="text-right py-1 px-2 font-mono" style="color: var(--color-text-secondary)">
                  {{ fmtNum(row.ancillary) }}
                </td>
                <td class="text-right py-1 px-2 font-mono" style="color: var(--color-text-secondary)">
                  {{ fmtNum(row.revenue) }}
                </td>
                <td class="text-right py-1 px-2 font-mono" style="color: var(--color-text-secondary)">
                  {{ fmtNum(row.opex) }}
                </td>
                <td
                  class="text-right py-1 px-2 font-mono"
                  :style="row.ebitda < 0 ? { color: 'var(--color-danger)' } : { color: 'var(--color-text-secondary)' }"
                >
                  {{ fmtNum(row.ebitda) }}
                </td>
                <td
                  class="text-right py-1 px-2 font-mono font-bold"
                  :style="row.cashFlow < 0 ? { color: 'var(--color-danger)' } : { color: 'var(--color-success)' }"
                >
                  {{ fmtNum(row.cashFlow) }}
                </td>
                <td
                  class="text-right py-1 px-2 font-mono"
                  :style="
                    row.cumCashFlow < 0 ? { color: 'var(--color-danger)' } : { color: 'var(--color-text-secondary)' }
                  "
                >
                  {{ fmtNum(row.cumCashFlow) }}
                </td>
                <td
                  v-if="f.debtRatio > 0"
                  class="text-right py-1 px-2 font-mono"
                  style="color: var(--color-text-secondary)"
                >
                  {{ row.dscr ? row.dscr.toFixed(2) : '-' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, nextTick, onMounted, onUnmounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { debounce } from 'lodash-es'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, PieChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, GridComponent, LegendComponent, GraphicComponent } from 'echarts/components'
import { useDraft } from '../composables/useDraft'
import CurrencyConverter from './CurrencyConverter.vue'
echarts.use([
  CanvasRenderer,
  BarChart,
  LineChart,
  PieChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  GraphicComponent
])
import CostWaterfallChart from './CostWaterfallChart.vue'
import EnergyFlowSankey from './EnergyFlowSankey.vue'
import ProductCAPEXLink from './ProductCAPEXLink.vue'
import { useExchangeRate } from '../composables/useExchangeRate.js'

const { t } = useI18n()
const props = defineProps({ params: Object, results: Object, soh: Array, rte: Array, augQty: Array })

// 使用汇率管理
const { displayCurrency, formatAmount, convert } = useExchangeRate()

const chartColors = computed(() => {
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
  return {
    backgroundColor: 'transparent',
    textStyle: { color: isDark ? 'var(--color-text-secondary)' : 'var(--color-text-secondary)', fontSize: 10 },
    axisLabel: isDark ? 'var(--color-text-secondary)' : 'var(--color-text-secondary)',
    legendText: isDark ? 'var(--color-text-secondary)' : 'var(--color-text-secondary)',
    gridLine: isDark ? '#1e293b' : 'var(--color-border-light)',
    success: isDark ? 'var(--color-success)' : 'var(--color-success)',
    danger: isDark ? 'var(--color-danger)' : 'var(--color-danger)',
    warning: isDark ? 'var(--color-warning)' : 'var(--color-warning)',
    info: isDark ? '#0ea5e9' : '#0ea5e9',
    acLine: isDark ? '#14b8a6' : '#14b8a6',
    purple: isDark ? 'var(--color-info)' : 'var(--color-info)',
    orange: isDark ? 'var(--color-chart-orange)' : 'var(--color-chart-orange)',
    cyan: isDark ? 'var(--color-chart-cyan)' : 'var(--color-chart-cyan)',
    redLight: isDark ? '#f87171' : '#f87171',
    muted: isDark ? 'var(--color-text-secondary)' : 'var(--color-text-secondary)'
  }
})

const { state: f, clearDraft: clearFDraft } = useDraft('financial-params', {
  offPeakPrice: 200,
  peakPrice: 600,
  spreadCapture: 85,
  operatingDays: 330,
  capacityPrice: 50000,
  ancillaryPrice: 30000,
  priceEscalation: 1.5,
  efficiencyLossPct: 5,
  containerCostPerMWh: 100,
  pcsCostPerMW: 25,
  bopCostPerMWh: 30,
  developmentCostPerMW: 20,
  landCostPerMW: 8,
  substationCostPerMW: 15,
  transmissionCostPerMW: 10,
  fixedOpexPerKW: 35,
  varOpexPerMWh: 3,
  insuranceRate: 0.4,
  opexEscalation: 2.0,
  discountRate: 7,
  debtRatio: 70,
  interestRate: 4.5,
  loanTenure: 15,
  costOfEquity: 12,
  equityRatio: 30,
  taxRate: 25,
  depreciationYears: 20,
  residualRate: 5,
  depreciationMethod: 'straight-line',
  vatRate: 5,
  gracePeriod: 2,
  augContainerCostPerMWh: 90,
  costDeclineRate: 5,
  augInstallCost: 5,
  decommissioningCost: 10,
  sensPct: 20
})

// 融资比例校验：确保债务+权益=100%
watch(
  [() => f.debtRatio, () => f.equityRatio],
  () => {
    if (f.debtRatio + f.equityRatio !== 100) {
      f.equityRatio = 100 - f.debtRatio
    }
  },
  { immediate: true }
)

const metrics = ref([
  { label: $t('financial.metricsProjectIrr'), value: '-', unit: '%', textColor: 'var(--color-accent-secondary)' },
  { label: $t('financial.metricsEquityIrr'), value: '-', unit: '%', textColor: 'var(--color-success)' },
  { label: $t('financial.metricsWacc'), value: '-', unit: '%', textColor: '#0ea5e9' },
  { label: $t('financial.metricsNpv'), value: '-', unit: `${$t('financial.wanUnit')} (${displayCurrency.value})`, textColor: 'var(--color-accent)' },
  { label: $t('financial.metricsLcos'), value: '-', unit: `${$t('financial.lcosUnit')} (${displayCurrency.value})`, textColor: 'var(--color-info)' },
  { label: $t('financial.metricsPayback'), value: '-', unit: $t('financial.metricsYearUnit'), textColor: 'var(--color-warning)' },
  { label: $t('financial.metricsTotalCapex'), value: '-', unit: `${$t('financial.wanUnit')} (${displayCurrency.value})`, textColor: 'var(--color-danger)' },
  { label: $t('financial.metricsMinDscr'), value: '-', unit: 'x', textColor: 'var(--color-chart-orange)' }
])

const cashFlowTable = ref([])
const cashFlowChartRef = ref(null)
const revenueChartRef = ref(null)
const dscrChartRef = ref(null)
const capexChartRef = ref(null)

let cashFlowChart = null,
  revenueChart = null,
  dscrChart = null,
  capexChart = null
let cachedRows = []
let cachedCapexData = null
let _resizeHandler = null

function disposeAll() {
  ;[cashFlowChart, revenueChart, dscrChart, capexChart].forEach((c) => {
    c?.dispose()
  })
  cashFlowChart = revenueChart = dscrChart = capexChart = null
}

function fmtNum(v) {
  if (v == null || isNaN(v)) return '-'
  if (Math.abs(v) >= 100) return v.toFixed(1)
  return v.toFixed(2)
}

function computeAll() {
  const p = props.params || {}
  const soh = props.soh || []
  const augQty = props.augQty || []
  const ratedEnergy = p.ratedEnergy || 5
  const initContainerQty = p.initContainerQty || 62
  const initPcsQty = p.initPcsQty || 1
  const cyclesPerDay = p.cyclesPerDay || 1
  const duration = p.duration || 2

  const totalCapMWh = ratedEnergy * initContainerQty
  const totalCapMW = totalCapMWh / (duration || 1)

  const containerCost = f.containerCostPerMWh * totalCapMWh
  const pcsCost = f.pcsCostPerMW * totalCapMW
  const bopCost = f.bopCostPerMWh * totalCapMWh
  const devCost = f.developmentCostPerMW * totalCapMW
  const landCost = f.landCostPerMW * totalCapMW
  const substationCost = f.substationCostPerMW * totalCapMW
  const transmissionCost = f.transmissionCostPerMW * totalCapMW
  const baseCapex = containerCost + pcsCost + bopCost + devCost + landCost + substationCost + transmissionCost
  const vatAmount = (baseCapex * f.vatRate) / 100
  const totalCapex = baseCapex + vatAmount

  cachedCapexData = {
    containerCost,
    pcsCost,
    bopCost,
    devCost,
    landCost,
    substationCost,
    transmissionCost,
    totalCapex,
    totalCapMW,
    totalCapMWh
  }

  const wacc = (f.costOfEquity * f.equityRatio) / 100 + (f.interestRate * (1 - f.taxRate / 100) * f.debtRatio) / 100
  const debtAmount = (totalCapex * f.debtRatio) / 100
  const equityAmount = totalCapex - debtAmount
  const annualDebtService =
    f.interestRate > 0 && f.loanTenure > 0
      ? (debtAmount * (f.interestRate / 100) * Math.pow(1 + f.interestRate / 100, f.loanTenure)) /
        (Math.pow(1 + f.interestRate / 100, f.loanTenure) - 1)
      : 0
  const residualValue = (totalCapex * f.residualRate) / 100
  const spread = ((f.peakPrice - f.offPeakPrice) * f.spreadCapture) / 100

  let annualDepreciation = 0
  if (f.depreciationYears > 0) {
    if (f.depreciationMethod === 'straight-line') {
      annualDepreciation = (totalCapex * (1 - f.residualRate / 100)) / f.depreciationYears
    } else if (f.depreciationMethod === 'double-declining') {
      const rate = 2 / f.depreciationYears
      annualDepreciation = totalCapex * rate * (1 - f.residualRate / 100)
    }
  }

  const rows = []
  rows.push({
    year: 0,
    energy: 0,
    arbitrage: 0,
    capacity: 0,
    ancillary: 0,
    revenue: 0,
    opex: 0,
    ebitda: 0,
    depreciation: 0,
    interest: 0,
    taxableIncome: 0,
    tax: 0,
    augCapex: -totalCapex,
    debtService: 0,
    cashFlow: -totalCapex,
    cumCashFlow: -totalCapex,
    dscr: null
  })

  let cumCash = -totalCapex
  let remainingDebt = debtAmount
  let totalDiscountedCost = totalCapex
  let totalDiscountedEnergy = 0
  let minDscr = Infinity

  for (let i = 1; i <= 25; i++) {
    const idx = i
    const cSoh = soh[idx] != null ? soh[idx] : soh.length > 0 ? soh[soh.length - 1] : 1
    const yearEnergy = totalCapMWh * cyclesPerDay * f.operatingDays * cSoh * (1 - f.efficiencyLossPct / 100)
    const priceFactor = Math.pow(1 + f.priceEscalation / 100, i)
    const opexFactor = Math.pow(1 + f.opexEscalation / 100, i)

    const arbitrageRev = ((yearEnergy * spread) / 10000) * priceFactor
    const capacityRev = ((totalCapMW * f.capacityPrice) / 10000) * priceFactor
    const ancillaryRev = ((totalCapMW * f.ancillaryPrice) / 10000) * priceFactor
    const totalRevenue = arbitrageRev + capacityRev + ancillaryRev

    const fixedOpex = ((f.fixedOpexPerKW * totalCapMW * 1000) / 10000) * opexFactor
    const varOpex = ((f.varOpexPerMWh * yearEnergy) / 10000) * opexFactor
    const insurance = (totalCapex * f.insuranceRate) / 100
    const landLease = (totalCapMW * 2) / 10000
    const totalOpex = fixedOpex + varOpex + insurance + landLease
    const ebitda = totalRevenue - totalOpex

    let dep = 0
    if (f.depreciationMethod === 'straight-line') {
      dep = i <= f.depreciationYears ? annualDepreciation : 0
    } else if (f.depreciationMethod === 'double-declining') {
      // 修正：正确的双倍余额递减法，在最后两年切换直线折旧
      const depreciableAmount = totalCapex - residualValue
      if (i <= f.depreciationYears - 2) {
        // 前N-2年使用双倍余额递减
        const rate = 2 / f.depreciationYears
        const bookValueStart = totalCapex - rows.slice(1, i).reduce((s, r) => s + r.depreciation, 0)
        dep = Math.min(bookValueStart * rate, bookValueStart - residualValue)
      } else if (i <= f.depreciationYears) {
        // 最后两年使用直线折旧（将剩余可折旧金额平均分配）
        const bookValueStart = totalCapex - rows.slice(1, i).reduce((s, r) => s + r.depreciation, 0)
        dep = Math.max(0, (bookValueStart - residualValue) / (f.depreciationYears - i + 1))
      }
    }

    let interestPaid = 0,
      principalPaid = 0,
      debtServiceYear = 0
    if (remainingDebt > 0 && i <= f.loanTenure) {
      interestPaid = (remainingDebt * f.interestRate) / 100
      // 修正：添加宽限期处理（中东标准：宽限期内只还利息不还本金）
      if (i <= f.gracePeriod) {
        principalPaid = 0
        debtServiceYear = interestPaid
      } else {
        principalPaid = Math.min(annualDebtService - interestPaid, remainingDebt)
        debtServiceYear = interestPaid + principalPaid
        remainingDebt = Math.max(0, remainingDebt - principalPaid)
      }
    }

    const taxableIncome = ebitda - dep - interestPaid
    const tax = Math.max(0, (taxableIncome * f.taxRate) / 100)

    const augQtyYear = augQty[idx] || 0
    const costDeclineFactor = Math.pow(1 - f.costDeclineRate / 100, i)
    const augContainerPrice = f.augContainerCostPerMWh * costDeclineFactor
    const augCapexYear =
      augQtyYear > 0 ? -(augQtyYear * ratedEnergy * augContainerPrice + augQtyYear * f.augInstallCost) : 0

    const cashFlow = ebitda - tax - debtServiceYear + augCapexYear
    cumCash += cashFlow

    const discFactor = Math.pow(1 + f.discountRate / 100, i)
    totalDiscountedCost += (totalOpex + (augCapexYear < 0 ? -augCapexYear : 0)) / discFactor
    totalDiscountedEnergy += yearEnergy / discFactor

    const dscr = debtServiceYear > 0 ? (ebitda - tax) / debtServiceYear : null
    if (dscr !== null && dscr < minDscr) minDscr = dscr

    rows.push({
      year: i,
      energy: yearEnergy,
      arbitrage: arbitrageRev,
      capacity: capacityRev,
      ancillary: ancillaryRev,
      revenue: totalRevenue,
      opex: totalOpex,
      ebitda,
      depreciation: dep,
      interest: interestPaid,
      taxableIncome,
      tax,
      augCapex: augCapexYear,
      debtService: debtServiceYear,
      cashFlow,
      cumCashFlow: cumCash,
      dscr
    })
  }

  // 修正BUG4：LCOS退役成本应为支出（加到成本而非减去），残值为收入（减去成本）
  totalDiscountedCost -= residualValue / Math.pow(1 + f.discountRate / 100, 25)
  const decommissioningCostAmount = f.decommissioningCost * totalCapMWh
  totalDiscountedCost += decommissioningCostAmount / Math.pow(1 + f.discountRate / 100, 25)
  // 在第25年现金流中添加退役成本支出
  if (rows.length > 25 && f.decommissioningCost > 0) {
    rows[25].cashFlow -= decommissioningCostAmount
    rows[25].cumCashFlow -= decommissioningCostAmount
  }

  const lcos = totalDiscountedEnergy > 0 ? (totalDiscountedCost / totalDiscountedEnergy) * 10000 : 0
  const npv = rows.reduce((s, r) => s + r.cashFlow / (r.year === 0 ? 1 : Math.pow(1 + f.discountRate / 100, r.year)), 0)
  const irr = calcIRR(
    rows.map((r) => r.cashFlow),
    rows.map((r) => r.year)
  )
  // 修正BUG3：Equity IRR应使用权益现金流序列（第0年为权益出资，后续为项目现金流）
  const equityFlows = [-equityAmount, ...rows.slice(1).map((r) => r.cashFlow)]
  const equityYears = [0, ...rows.slice(1).map((r) => r.year)]
  const equityIrr = calcIRR(equityFlows, equityYears)

  // 修正BUG2：Payback回收期公式错误，prevCum应为上一年的累计现金流
  let payback = '-'
  for (let i = 1; i < rows.length; i++) {
    if (rows[i].cumCashFlow >= 0 && rows[i - 1].cumCashFlow < 0) {
      payback = (i - 1 + Math.abs(rows[i - 1].cumCashFlow) / rows[i].cashFlow).toFixed(1)
      break
    }
  }

  // 转换为显示货币
  const convertToDisplay = (usdAmount) => {
    return convert(usdAmount, 'USD', displayCurrency.value)
  }

  metrics.value[0].value = irr + '%'
  metrics.value[1].value = equityIrr + '%'
  metrics.value[0].value = irr + '%'
  metrics.value[1].value = equityIrr + '%'
  metrics.value[2].value = wacc.toFixed(2) + '%'
  metrics.value[3].value = convertToDisplay(npv).toFixed(0)
  metrics.value[4].value = lcos.toFixed(3) // LCOS 保持原单位，因为已经是单位成本
  metrics.value[5].value = payback
  metrics.value[6].value = convertToDisplay(totalCapex).toFixed(0)
  metrics.value[7].value = minDscr !== Infinity ? minDscr.toFixed(2) : '-'

  cashFlowTable.value = rows
  cachedRows = rows

  nextTick(() => {
    setTimeout(() => renderCharts(), 300)
  })
}

function calcIRR(flows, years) {
  let rate = 0.08
  for (let iter = 0; iter < 100; iter++) {
    let npv = 0,
      dnpv = 0
    for (let i = 0; i < flows.length; i++) {
      const t = years[i] - years[0]
      const df = Math.pow(1 + rate, t)
      npv += flows[i] / df
      if (t > 0) dnpv += (-t * flows[i]) / Math.pow(1 + rate, t + 1)
    }
    if (Math.abs(npv) < 1e-6) break
    const newRate = rate - npv / (dnpv || 1e-10)
    if (Math.abs(newRate - rate) < 1e-8) {
      rate = newRate
      break
    }
    rate = newRate
    if (rate < -0.99) rate = -0.5
    if (rate > 100) rate = 10
  }
  return Math.max(-99, Math.min(999, rate * 100)).toFixed(2)
}

function renderCharts() {
  renderCashFlowChart()
  renderRevenueChart()
  renderDscrChart()
  renderCapexChart()
}

function renderCashFlowChart() {
  if (!cashFlowChartRef.value) return
  if (cashFlowChart) cashFlowChart.dispose()
  const colors = chartColors.value
  cashFlowChart = echarts.init(cashFlowChartRef.value, colors)

  const rows = cachedRows
  const years = rows.map((r) => r.year)
  const cumCF = rows.map((r) => r.cumCashFlow)
  const netCF = rows.map((r) => r.cashFlow)
  const paybackYear = parseFloat(metrics.value[4].value)

  cashFlowChart.setOption({
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const year = params[0].axisValue
        const row = rows.find((r) => r.year === parseInt(year))
        if (!row) return ''
        let html = `<div style="font-weight:bold;margin-bottom:8px;">${t('financial.tooltipYear')} ${year === 0 ? t('financial.tooltipConstruction') : year + t('financial.tooltipYearLabel')}</div>`
        html += `<div>${t('financial.tooltipNetCashFlow')}: <span style="color:${row.cashFlow >= 0 ? colors.success : colors.danger};font-weight:bold;">${row.cashFlow >= 0 ? '+' : ''}${row.cashFlow.toFixed(0)} ${t('financial.wanUnit')}</span></div>`
        html += `<div>${t('financial.tooltipCumCashFlow')}: <span style="color:${row.cumCashFlow >= 0 ? colors.success : colors.danger};font-weight:bold;">${row.cumCashFlow >= 0 ? '+' : ''}${row.cumCashFlow.toFixed(0)} ${t('financial.wanUnit')}</span></div>`
        if (row.year > 0) {
          html += '<div style="border-top:1px solid #eee;margin-top:6px;padding-top:6px;">'
          html += `<div>${t('financial.tooltipTotalRevenue')}: ${row.revenue.toFixed(0)} ${t('financial.wanUnit')}</div>`
          html += `<div>${t('financial.tooltipOpex')}: ${row.opex.toFixed(0)} ${t('financial.wanUnit')}</div>`
          html += `<div>${t('financial.tooltipEbitda')}: ${row.ebitda.toFixed(0)} ${t('financial.wanUnit')}</div>`
          html += `<div>${t('financial.tooltipDepreciation')}: ${row.depreciation.toFixed(0)} ${t('financial.wanUnit')}</div>`
          html += `<div>${t('financial.tooltipInterest')}: ${row.interest.toFixed(0)} ${t('financial.wanUnit')}</div>`
          html += `<div>${t('financial.tooltipTax')}: ${row.tax.toFixed(0)} ${t('financial.wanUnit')}</div>`
          if (row.debtService > 0) {
            html += `<div>${t('financial.tooltipDebtService')}: ${row.debtService.toFixed(0)} ${t('financial.wanUnit')}</div>`
            html += `<div>${t('financial.tooltipDscr')}: ${row.dscr ? row.dscr.toFixed(2) : '-'}x</div>`
          }
          html += '</div>'
        }
        return html
      }
    },
    legend: { top: 0, textStyle: { color: colors.legendText, fontSize: 10 }, data: [t('financial.cumCashFlow'), t('financial.annualNetCashFlow')] },
    grid: { top: 30, right: 20, bottom: 25, left: 65 },
    xAxis: {
      type: 'category',
      data: years,
      axisLabel: { color: colors.axisLabel, fontSize: 9 },
      name: t('financial.yearAxis'),
      nameTextStyle: { color: colors.axisLabel, fontSize: 9 }
    },
    yAxis: [
      {
        type: 'value',
        axisLabel: { color: colors.axisLabel, fontSize: 9, formatter: (v) => (v / 10000).toFixed(1) + t('financial.millionUnit') },
        splitLine: { lineStyle: { color: colors.gridLine } }
      }
    ],
    series: [
      {
        name: t('financial.cumCashFlow'),
        type: 'line',
        data: cumCF,
        smooth: true,
        symbol: 'circle',
        symbolSize: 4,
        lineStyle: { color: colors.info, width: 2.5 },
        itemStyle: { color: colors.info, borderWidth: 1, borderColor: 'var(--color-text-on-accent)' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color:
                document.documentElement.getAttribute('data-theme') === 'dark'
                  ? 'rgba(14,165,233,0.25)'
                  : 'rgba(59,130,246,0.15)'
            },
            { offset: 1, color: 'transparent' }
          ])
        },
        markLine: {
          silent: true,
          symbol: 'none',
          data: [
            {
              yAxis: 0,
              lineStyle: { color: colors.danger, type: 'dashed', width: 1.5 },
              label: { formatter: t('financial.breakevenLine'), color: colors.danger, fontSize: 9 }
            }
          ]
        },
        markPoint:
          paybackYear > 0 && paybackYear < 26
            ? {
                silent: true,
                symbol: 'pin',
                symbolSize: 24,
                data: [
                  { coord: [paybackYear, 0], value: t('financial.paybackPrefix') + paybackYear + t('financial.paybackSuffix'), itemStyle: { color: colors.warning } }
                ]
              }
            : undefined
      },
      {
        name: t('financial.annualNetCashFlow'),
        type: 'bar',
        data: netCF,
        itemStyle: {
          color: (params) => (params.value >= 0 ? colors.success : colors.danger),
          borderRadius: [2, 2, 0, 0]
        },
        barWidth: 8
      }
    ]
  })
  cashFlowChart.resize()
}

function renderRevenueChart() {
  if (!revenueChartRef.value) return
  if (revenueChart) revenueChart.dispose()
  const colors = chartColors.value
  revenueChart = echarts.init(revenueChartRef.value, colors)

  const rows = cachedRows.filter((r) => r.year > 0)
  const years = rows.map((r) => r.year)

  revenueChart.setOption({
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const year = params[0].axisValue
        const row = rows.find((r) => r.year === parseInt(year))
        if (!row) return ''
        let html = `<div style="font-weight:bold;margin-bottom:8px;">${t('financial.tooltipYearFormat', { year })}</div>`
        html += `<div>${t('financial.tooltipArbitrage')}: <span style="color:${colors.acLine};font-weight:bold;">${row.arbitrage.toFixed(0)} ${t('financial.wanUnit')}</span></div>`
        html += `<div>${t('financial.tooltipCapacity')}: <span style="color:${colors.purple};font-weight:bold;">${row.capacity.toFixed(0)} ${t('financial.wanUnit')}</span></div>`
        html += `<div>${t('financial.tooltipAncillary')}: <span style="color:${colors.orange};font-weight:bold;">${row.ancillary.toFixed(0)} ${t('financial.wanUnit')}</span></div>`
        html += '<div style="border-top:1px solid #eee;margin-top:6px;padding-top:6px;">'
        html += `<div>${t('financial.tooltipTotalRevenue')}: <span style="font-weight:bold;">${row.revenue.toFixed(0)} ${t('financial.wanUnit')}</span></div>`
        const arbitragePct = row.revenue > 0 ? ((row.arbitrage / row.revenue) * 100).toFixed(1) : 0
        const capacityPct = row.revenue > 0 ? ((row.capacity / row.revenue) * 100).toFixed(1) : 0
        const ancillaryPct = row.revenue > 0 ? ((row.ancillary / row.revenue) * 100).toFixed(1) : 0
        html += `<div>${t('financial.tooltipRevenueStructure')}: ${t('financial.tooltipArbitrage')}${arbitragePct}% + ${t('financial.tooltipCapacity')}${capacityPct}% + ${t('financial.tooltipAncillary')}${ancillaryPct}%</div>`
        html += `<div>${t('financial.tooltipGeneration')}: ${row.energy.toFixed(0)} MWh</div>`
        html += '</div>'
        return html
      }
    },
    legend: {
      top: 0,
      textStyle: { color: colors.legendText, fontSize: 10 },
      data: [t('financial.arbitrageSeries'), t('financial.capacitySeries'), t('financial.ancillarySeries')]
    },
    grid: { top: 30, right: 20, bottom: 25, left: 55 },
    xAxis: { type: 'category', data: years, axisLabel: { color: colors.axisLabel, fontSize: 9 } },
    yAxis: {
      type: 'value',
      axisLabel: { color: colors.axisLabel, fontSize: 9, formatter: (v) => fmtNum(v) },
      splitLine: { lineStyle: { color: colors.gridLine } }
    },
    series: [
      {
        name: t('financial.arbitrageSeries'),
        type: 'bar',
        stack: 'revenue',
        data: rows.map((r) => r.arbitrage),
        itemStyle: { color: colors.acLine },
        barWidth: 18
      },
      {
        name: t('financial.capacitySeries'),
        type: 'bar',
        stack: 'revenue',
        data: rows.map((r) => r.capacity),
        itemStyle: { color: colors.purple },
        barWidth: 18
      },
      {
        name: t('financial.ancillarySeries'),
        type: 'bar',
        stack: 'revenue',
        data: rows.map((r) => r.ancillary),
        itemStyle: { color: colors.orange },
        barWidth: 18
      }
    ]
  })
  revenueChart.resize()
}

function renderDscrChart() {
  if (!dscrChartRef.value) return
  if (dscrChart) dscrChart.dispose()
  const colors = chartColors.value
  dscrChart = echarts.init(dscrChartRef.value, colors)

  const rows = cachedRows.filter((r) => r.year > 0)
  const years = rows.map((r) => r.year)
  const dscrData = rows.map((r) => r.dscr || 0)

  dscrChart.setOption({
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const year = params[0].axisValue
        const row = rows.find((r) => r.year === parseInt(year))
        if (!row) return ''
        let html = `${t('financial.tooltipYearFormat', { year })}`
        html += `<div>${t('financial.tooltipEbitda')}: <span style="color:${colors.cyan};font-weight:bold;">${row.ebitda.toFixed(0)} ${t('financial.wanUnit')}</span></div>`
        html += `<div>${t('financial.tooltipDebtService')}: <span style="color:${colors.redLight};font-weight:bold;">${row.debtService.toFixed(0)} ${t('financial.wanUnit')}</span></div>`
        if (row.debtService > 0) {
          html += '<div style="border-top:1px solid #eee;margin-top:6px;padding-top:6px;">'
          html += `<div>DSCR: <span style="font-weight:bold;font-size:16px;color:${row.dscr >= 1.3 ? colors.success : colors.danger};">${row.dscr.toFixed(2)}x</span></div>`
          html += `<div style="color:${row.dscr >= 1.3 ? colors.success : colors.danger};">${row.dscr >= 1.3 ? t('financial.dscrSatisfied') : t('financial.dscrBelowMin')}</div>`
          html += `<div>${t('financial.tooltipInterest')}: ${row.interest.toFixed(0)} ${t('financial.wanUnit')}</div>`
          html += `<div>${t('financial.tooltipPrincipal')}: ${(row.debtService - row.interest).toFixed(0)} ${t('financial.wanUnit')}</div>`
          html += '</div>'
        } else {
          html += `<div>${t('financial.noDebtService')}</div>`
        }
        return html
      }
    },
    legend: { top: 0, textStyle: { color: colors.legendText, fontSize: 10 }, data: [t('financial.ebitdaSeries'), t('financial.debtServiceSeries'), 'DSCR'] },
    grid: { top: 30, right: 45, bottom: 25, left: 55 },
    xAxis: { type: 'category', data: years, axisLabel: { color: colors.axisLabel, fontSize: 9 } },
    yAxis: [
      {
        type: 'value',
        axisLabel: { color: colors.axisLabel, fontSize: 9, formatter: (v) => fmtNum(v) },
        splitLine: { lineStyle: { color: colors.gridLine } },
        name: t('financial.yAxisUnit')
      },
      {
        type: 'value',
        min: 0,
        max: 4,
        axisLabel: { color: colors.axisLabel, fontSize: 9 },
        splitLine: { show: false },
        name: t('financial.yAxisMultiplier')
      }
    ],
    series: [
      {
        name: t('financial.ebitdaSeries'),
        type: 'bar',
        data: rows.map((r) => r.ebitda),
        itemStyle: { color: colors.cyan, borderRadius: [2, 2, 0, 0] },
        barWidth: 10,
        barGap: '30%'
      },
      {
        name: t('financial.debtServiceSeries'),
        type: 'bar',
        data: rows.map((r) => r.debtService),
        itemStyle: { color: colors.redLight, borderRadius: [2, 2, 0, 0] },
        barWidth: 10
      },
      {
        name: 'DSCR',
        type: 'line',
        yAxisIndex: 1,
        data: dscrData,
        smooth: true,
        symbol: 'circle',
        symbolSize: 6,
        lineStyle: { color: colors.warning, width: 2.5 },
        itemStyle: {
          color: (params) => (params.value >= 1.3 ? colors.success : colors.danger),
          borderWidth: 2,
          borderColor: 'var(--color-text-on-accent)'
        },
        markLine: {
          silent: true,
          symbol: 'none',
          yAxisIndex: 1,
          data: [
            {
              yAxis: 1.3,
              lineStyle: { color: colors.danger, type: 'dashed', width: 1.5 },
              label: { formatter: t('financial.bankMinDscr'), color: colors.danger, fontSize: 9 }
            },
            {
              yAxis: 1.5,
              lineStyle: { color: colors.warning, type: 'dashed', width: 1 },
              label: { formatter: t('financial.idealDscr'), color: colors.warning, fontSize: 8 }
            }
          ]
        }
      }
    ]
  })
  dscrChart.resize()
}

function renderCapexChart() {
  if (!capexChartRef.value) return
  if (capexChart) capexChart.dispose()
  const colors = chartColors.value
  capexChart = echarts.init(capexChartRef.value, colors)

  if (!cachedCapexData) return
  const {
    containerCost,
    pcsCost,
    bopCost,
    devCost,
    landCost,
    substationCost,
    transmissionCost,
    totalCapMW,
    totalCapMWh
  } = cachedCapexData

  const capexItems = [
    { value: containerCost, name: t('financial.capexContainer'), color: colors.info },
    { value: pcsCost, name: t('financial.capexPcs'), color: colors.purple },
    { value: bopCost, name: t('financial.capexBop'), color: colors.warning },
    { value: substationCost, name: t('financial.capexSubstation'), color: 'var(--color-chart-cyan)' },
    { value: transmissionCost, name: t('financial.capexTransmission'), color: 'var(--color-chart-orange)' },
    { value: landCost, name: t('financial.capexLand'), color: 'var(--color-success)' },
    { value: devCost, name: t('financial.capexDev'), color: colors.muted }
  ].filter((item) => item.value > 0)

  const total = capexItems.reduce((sum, item) => sum + item.value, 0)

  // 计算敏感性分析数据
  const sensitivityData = calculateSensitivityData()

  capexChart.setOption({
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        const perMWh = params.value / totalCapMWh
        const perMW = params.value / totalCapMW
        return `${params.name}<br/>${t('financial.tooltipAmount')}: ${params.value.toFixed(0)} ${t('financial.wanUnit')} (${params.percent.toFixed(1)}%)<br/>${t('financial.tooltipUnitPrice')}: ${perMWh.toFixed(1)} ${t('financial.wanUnit')}/MWh = ${perMW.toFixed(1)} ${t('financial.wanUnit')}/MW`
      }
    },
    legend: {
      bottom: 0,
      textStyle: { color: colors.legendText, fontSize: 9 },
      data: capexItems.map((item) => item.name),
      orient: 'horizontal',
      itemWidth: 10,
      itemHeight: 10
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '65%'],
        center: ['50%', '45%'],
        avoidLabelOverlap: false,
        label: {
          show: true,
          position: 'outside',
          formatter: (params) => `${params.name}\n${params.value.toFixed(0)}${t('financial.wanSuffix')}`,
          fontSize: 8,
          color: colors.legendText,
          lineHeight: 12
        },
        labelLine: { show: true, length: 8, length2: 8 },
        emphasis: {
          label: { show: true, fontSize: 10, fontWeight: 'bold' },
          itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.3)' }
        },
        data: capexItems.map((item) => ({
          value: item.value,
          name: item.name,
          itemStyle: { color: item.color }
        }))
      }
    ]
  })
  capexChart.resize()
}

function calculateSensitivityData() {
  if (!cachedCapexData) return {}

  const { containerCost, pcsCost, bopCost, devCost } = cachedCapexData
  const sensitivityPct = f.sensPct || 20

  return {
    base: {
      container: containerCost,
      pcs: pcsCost,
      bop: bopCost,
      dev: devCost,
      total: containerCost + pcsCost + bopCost + devCost
    },
    positive: {
      container: containerCost * (1 + sensitivityPct / 100),
      pcs: pcsCost * (1 + sensitivityPct / 100),
      bop: bopCost * (1 + sensitivityPct / 100),
      dev: devCost * (1 + sensitivityPct / 100),
      total: (containerCost + pcsCost + bopCost + devCost) * (1 + sensitivityPct / 100)
    },
    negative: {
      container: containerCost * (1 - sensitivityPct / 100),
      pcs: pcsCost * (1 - sensitivityPct / 100),
      bop: bopCost * (1 - sensitivityPct / 100),
      dev: devCost * (1 - sensitivityPct / 100),
      total: (containerCost + pcsCost + bopCost + devCost) * (1 - sensitivityPct / 100)
    }
  }
}

// 处理产品配置
function handleProductConfig(config) {
  if (config.autoCalculatedCAPEX) {
    // 使用自动计算的CAPEX
    f.containerCostPerMWh = config.autoCalculatedCapexPerMWh * 0.6 // 60% for container
    f.pcsCostPerMW = config.autoCalculatedCapexPerMWh * config.ratedEnergy * 0.2 // 20% for PCS
    f.bopCostPerMWh = config.autoCalculatedCapexPerMWh * 0.2 // 20% for BOP
  }

  if (config.ratedEnergy) {
    // 更新能量参数
    if (props.params) {
      // eslint-disable-next-line vue/no-mutating-props
      props.params.ratedEnergy = config.ratedEnergy
    }
  }

  if (config.acEfficiency) {
    // 更新PCS效率
    if (props.params) {
      // eslint-disable-next-line vue/no-mutating-props
      props.params.acEfficiency = config.acEfficiency
    }
  }

  // 重新计算
  computeAll()
}

function recalc() {
  computeAll()
}
const debouncedRecalc = debounce(recalc, 300)

watch([() => props.params, () => props.soh, () => props.augQty], debouncedRecalc, { deep: true, immediate: true })
watch(f, debouncedRecalc, { deep: true })
watch(displayCurrency, () => {
  metrics.value[2].unit = `${t('financial.wanUnit')} (${displayCurrency.value})`
  metrics.value[3].unit = `${t('financial.lcosUnit')} (${displayCurrency.value})`
  metrics.value[5].unit = `${t('financial.wanUnit')} (${displayCurrency.value})`
  computeAll()
})

onMounted(() => {
  nextTick(() => computeAll())
})
onUnmounted(() => {
  disposeAll()
  if (_resizeHandler) {
    window.removeEventListener('resize', _resizeHandler)
    _resizeHandler = null
  }
})

_resizeHandler = () => {
  cashFlowChart?.resize()
  revenueChart?.resize()
  dscrChart?.resize()
  capexChart?.resize()
}
window.addEventListener('resize', _resizeHandler)
</script>

<style scoped>
input:focus,
select:focus,
textarea:focus {
  border-color: var(--color-input-focus);
  outline: none;
}

button:not(:disabled):hover {
  opacity: 0.9;
}
</style>
