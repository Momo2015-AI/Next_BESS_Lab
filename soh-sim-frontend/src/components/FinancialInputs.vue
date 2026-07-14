<template>
  <div class="grid grid-cols-2 gap-3">
    <!-- I. Revenue Stack -->
    <div class="rounded-lg p-3 ins-1">
      <h3 class="font-bold text-xs mb-2 flex items-center gap-2 ins-2">
        <span class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold ins-3">I</span>
        {{ $t('financial.sectionRevenueStack') }}
      </h3>
      <div class="grid grid-cols-2 gap-2 text-[10px] ins-4">
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelOffPeakPrice') }}
          </label>
          <input
            v-model.number="f.offPeakPrice"
            type="number"
            step="0.1"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelPeakPrice') }}
          </label>
          <input v-model.number="f.peakPrice" type="number" step="0.1" class="w-full rounded px-2 py-1 text-xs ins-6" />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelSpreadCapture') }}
          </label>
          <input
            v-model.number="f.spreadCapture"
            type="number"
            step="0.1"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelCalendarDays') }}
          </label>
          <input
            v-model.number="f.operatingDays"
            type="number"
            step="1"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelCapacityPrice') }}
          </label>
          <input
            v-model.number="f.capacityPrice"
            type="number"
            step="100"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelAncillaryPrice') }}
          </label>
          <input
            v-model.number="f.ancillaryPrice"
            type="number"
            step="100"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelPriceEscalation') }}
          </label>
          <input
            v-model.number="f.priceEscalation"
            type="number"
            step="0.1"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelEfficiencyLoss') }}
          </label>
          <input
            v-model.number="f.efficiencyLossPct"
            type="number"
            step="0.01"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
      </div>
    </div>
    <!-- II. CapEx & OpEx -->
    <div class="rounded-lg p-3 ins-1">
      <h3 class="font-bold text-xs mb-2 flex items-center gap-2 ins-2">
        <span class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold ins-7">II</span>
        {{ $t('financial.sectionCapexOpex') }}
      </h3>
      <div class="grid grid-cols-2 gap-2 text-[10px] ins-4">
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelContainerCost') }}
          </label>
          <input
            v-model.number="f.containerCostPerMWh"
            type="number"
            step="1"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">{{ $t('financial.labelPcsCost') }}</label>
          <input
            v-model.number="f.pcsCostPerMW"
            type="number"
            step="1"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">{{ $t('financial.labelBopCost') }}</label>
          <input
            v-model.number="f.bopCostPerMWh"
            type="number"
            step="1"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelSubstationCost') }}
          </label>
          <input
            v-model.number="f.substationCostPerMW"
            type="number"
            step="1"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelTransmissionCost') }}
          </label>
          <input
            v-model.number="f.transmissionCostPerMW"
            type="number"
            step="1"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">{{ $t('financial.labelLandCost') }}</label>
          <input
            v-model.number="f.landCostPerMW"
            type="number"
            step="1"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">{{ $t('financial.labelDevCost') }}</label>
          <input
            v-model.number="f.developmentCostPerMW"
            type="number"
            step="1"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">{{ $t('financial.labelFixedOm') }}</label>
          <input
            v-model.number="f.fixedOpexPerKW"
            type="number"
            step="0.5"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">{{ $t('financial.labelVarOm') }}</label>
          <input
            v-model.number="f.varOpexPerMWh"
            type="number"
            step="0.1"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelInsuranceRate') }}
          </label>
          <input
            v-model.number="f.insuranceRate"
            type="number"
            step="0.01"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelOmEscalation') }}
          </label>
          <input
            v-model.number="f.opexEscalation"
            type="number"
            step="0.1"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">{{ $t('financial.labelVatRate') }}</label>
          <input v-model.number="f.vatRate" type="number" step="0.5" class="w-full rounded px-2 py-1 text-xs ins-6" />
        </div>
      </div>
    </div>
    <!-- III. Financing & Tax -->
    <div class="rounded-lg p-3 ins-1">
      <h3 class="font-bold text-xs mb-2 flex items-center gap-2 ins-2">
        <span class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold ins-8">III</span>
        {{ $t('financial.sectionFinancingTax') }}
      </h3>
      <div class="grid grid-cols-1 gap-2 text-[10px] ins-4">
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelDiscountRate') }}
          </label>
          <input
            v-model.number="f.discountRate"
            type="number"
            step="0.1"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelDebtRatio') }}
          </label>
          <input v-model.number="f.debtRatio" type="number" step="1" class="w-full rounded px-2 py-1 text-xs ins-6" />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelEquityRatio') }}
          </label>
          <input v-model.number="f.equityRatio" type="number" step="1" class="w-full rounded px-2 py-1 text-xs ins-6" />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">{{ $t('financial.labelLoanRate') }}</label>
          <input
            v-model.number="f.interestRate"
            type="number"
            step="0.1"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelCostOfEquity') }}
          </label>
          <input
            v-model.number="f.costOfEquity"
            type="number"
            step="0.5"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelLoanTenure') }}
          </label>
          <input v-model.number="f.loanTenure" type="number" step="1" class="w-full rounded px-2 py-1 text-xs ins-6" />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">{{ $t('financial.labelTaxRate') }}</label>
          <input v-model.number="f.taxRate" type="number" step="0.5" class="w-full rounded px-2 py-1 text-xs ins-6" />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelDepreciationYears') }}
          </label>
          <input
            v-model.number="f.depreciationYears"
            type="number"
            step="1"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelResidualRate') }}
          </label>
          <input
            v-model.number="f.residualRate"
            type="number"
            step="0.5"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelDepreciationMethod') }}
          </label>
          <select v-model="f.depreciationMethod" class="w-full rounded px-2 py-1 text-xs ins-6">
            <option value="straight-line">{{ $t('financial.optStraightLine') }}</option>
            <option value="double-declining">{{ $t('financial.optDoubleDeclining') }}</option>
          </select>
        </div>
      </div>
    </div>
    <!-- IV. Augmentation -->
    <div class="rounded-lg p-3 ins-1">
      <h3 class="font-bold text-xs mb-2 flex items-center gap-2 ins-2">
        <span class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold ins-9">IV</span>
        {{ $t('financial.sectionAugmentation') }}
      </h3>
      <div class="grid grid-cols-1 gap-2 text-[10px] ins-4">
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelAugContainerCost') }}
          </label>
          <input
            v-model.number="f.augContainerCostPerMWh"
            type="number"
            step="1"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelCostDecline') }}
          </label>
          <input
            v-model.number="f.costDeclineRate"
            type="number"
            step="0.1"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelAugInstallCost') }}
          </label>
          <input
            v-model.number="f.augInstallCost"
            type="number"
            step="0.5"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelDecommissionCost') }}
          </label>
          <input
            v-model.number="f.decommissioningCost"
            type="number"
            step="1"
            class="w-full rounded px-2 py-1 text-xs ins-6"
          />
        </div>
      </div>
    </div>
    <!-- V. Sensitivity -->
    <div class="rounded-lg p-3 ins-1">
      <h3 class="font-bold text-xs mb-2 flex items-center gap-2 ins-2">
        <span class="w-5 h-5 rounded text-[10px] flex items-center justify-center font-bold ins-10">V</span>
        {{ $t('financial.sectionSensitivity') }}
      </h3>
      <div class="text-[10px] space-y-1.5 ins-5">
        <div class="flex justify-between">
          <span>{{ $t('financial.labelPriceVolatility') }}</span>
          <span class="ins-4">+/-{{ f.sensPct }}%</span>
        </div>
        <div class="flex justify-between">
          <span>{{ $t('financial.labelDegradationVolatility') }}</span>
          <span class="ins-4">+/-{{ f.sensPct }}%</span>
        </div>
        <div class="flex justify-between">
          <span>{{ $t('financial.labelInterestVolatility') }}</span>
          <span class="ins-4">+/-{{ f.sensPct }}%</span>
        </div>
        <div class="flex justify-between">
          <span>{{ $t('financial.labelCapexVolatility') }}</span>
          <span class="ins-4">+/-{{ f.sensPct }}%</span>
        </div>
        <div>
          <label class="block mb-0.5 ins-5">
            {{ $t('financial.labelVolatilityRange') }}
          </label>
          <input v-model.number="f.sensPct" type="number" step="5" class="w-full rounded px-2 py-1 text-xs ins-6" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { inject } from 'vue'

const f = inject('financialParams', () => {
  console.warn('financialParams not provided, using defaults')
  return {
    offPeakPrice: 0.3,
    peakPrice: 0.8,
    spreadCapture: 85,
    operatingDays: 330,
    capacityPrice: 30000,
    ancillaryPrice: 15000,
    priceEscalation: 2.0,
    efficiencyLossPct: 3.0,
    containerCost: 200000,
    pcsCost: 80000,
    bopCost: 50000,
    epcCost: 100000,
    developmentCost: 50000,
    omCost: 5000,
    insuranceRate: 0.5,
    propertyTaxRate: 0.2,
    debtRatio: 60,
    loanRate: 4.5,
    loanTerm: 15,
    depreciationYears: 15,
    residualRate: 5,
    taxRate: 25,
    taxHoliday: 5,
    discountRate: 8.0,
    augContainerCost: 180000,
    augInterval: 5,
    augRatio: 10,
    capexVolatility: 15,
    priceVolatility: 20,
    sensPct: 15
  }
})
</script>

<style scoped>
.ins-1 {
  background-color: var(--color-card);
  border: 1px solid var(--color-border);
}
.ins-2 {
  color: var(--color-text);
}
.ins-3 {
  background-color: var(--color-accent-glow);
  color: var(--color-accent);
}
.ins-4 {
  color: var(--color-text-secondary);
}
.ins-5 {
  color: var(--color-text-muted);
}
.ins-6 {
  background-color: var(--color-input-bg-dark);
  border: 1px solid var(--color-input-border);
  color: var(--color-text);
}
.ins-7 {
  background-color: rgba(245, 158, 11, 0.2);
  color: var(--color-warning);
}
.ins-8 {
  background-color: rgba(59, 130, 246, 0.2);
  color: var(--color-accent-secondary);
}
.ins-9 {
  background-color: rgba(168, 85, 247, 0.2);
  color: var(--color-info);
}
.ins-10 {
  background-color: rgba(16, 185, 129, 0.2);
  color: var(--color-success);
}
</style>
