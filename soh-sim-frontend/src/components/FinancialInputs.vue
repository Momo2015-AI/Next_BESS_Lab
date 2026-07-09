<template>
  <div class="grid grid-cols-2 gap-3">
    <!-- I. Revenue Stack -->
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelOffPeakPrice') }}
          </label>
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelPeakPrice') }}
          </label>
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelSpreadCapture') }}
          </label>
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelCalendarDays') }}
          </label>
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelCapacityPrice') }}
          </label>
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelAncillaryPrice') }}
          </label>
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelPriceEscalation') }}
          </label>
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelEfficiencyLoss') }}
          </label>
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
    <!-- II. CapEx & OpEx -->
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelContainerCost') }}
          </label>
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelSubstationCost') }}
          </label>
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelTransmissionCost') }}
          </label>
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelInsuranceRate') }}
          </label>
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelOmEscalation') }}
          </label>
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
    <!-- III. Financing & Tax -->
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelDiscountRate') }}
          </label>
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelDebtRatio') }}
          </label>
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelEquityRatio') }}
          </label>
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelCostOfEquity') }}
          </label>
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelLoanTenure') }}
          </label>
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelDepreciationYears') }}
          </label>
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelResidualRate') }}
          </label>
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelDepreciationMethod') }}
          </label>
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
    <!-- IV. Augmentation -->
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelAugContainerCost') }}
          </label>
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelCostDecline') }}
          </label>
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelAugInstallCost') }}
          </label>
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelDecommissionCost') }}
          </label>
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
    <!-- V. Sensitivity -->
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
          <label class="block mb-0.5" style="color: var(--color-text-muted)">
            {{ $t('financial.labelVolatilityRange') }}
          </label>
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
</template>

<script setup>
import { inject } from 'vue'

const f = inject('financialParams')
</script>
