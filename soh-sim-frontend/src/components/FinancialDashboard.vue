<template>
  <div class="h-full overflow-y-auto custom-scrollbar">
    <div class="max-w-6xl mx-auto space-y-3 py-2">

      <div class="grid grid-cols-6 gap-2">
        <div v-for="m in metrics" :key="m.label"
          :class="['border rounded-lg p-3 text-center', m.color]">
          <div class="text-[10px] text-slate-400 uppercase tracking-wider">{{ m.label }}</div>
          <div class="text-lg font-bold font-mono mt-0.5" :class="m.textColor">{{ m.value }}</div>
          <div class="text-[9px] text-slate-600 mt-0.5">{{ m.unit }}</div>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-3">
          <h3 class="font-bold text-xs text-slate-200 mb-2 flex items-center gap-2">
            <span class="w-5 h-5 rounded bg-teal-500/20 text-teal-400 text-[10px] flex items-center justify-center font-bold">I</span>
            收入模型 Revenue Stack
          </h3>
          <div class="grid grid-cols-2 gap-2 text-[10px]">
            <div>
              <label class="text-slate-500 block mb-0.5">低谷购电价 $/MWh</label>
              <input v-model.number="f.offPeakPrice" type="number" step="0.1" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">高峰售电价 $/MWh</label>
              <input v-model.number="f.peakPrice" type="number" step="0.1" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">价差捕获率 %</label>
              <input v-model.number="f.spreadCapture" type="number" step="0.1" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">日历日可用天数</label>
              <input v-model.number="f.operatingDays" type="number" step="1" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">容量市场单价 $/MW-yr</label>
              <input v-model.number="f.capacityPrice" type="number" step="100" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">辅助服务单价 $/MW-yr</label>
              <input v-model.number="f.ancillaryPrice" type="number" step="100" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">电价年涨幅 %</label>
              <input v-model.number="f.priceEscalation" type="number" step="0.1" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">充放电效率扣减 %</label>
              <input v-model.number="f.efficiencyLossPct" type="number" step="0.01" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
          </div>
        </div>

        <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-3">
          <h3 class="font-bold text-xs text-slate-200 mb-2 flex items-center gap-2">
            <span class="w-5 h-5 rounded bg-amber-500/20 text-amber-400 text-[10px] flex items-center justify-center font-bold">II</span>
            CAPEX & OPEX 成本结构
          </h3>
          <div class="grid grid-cols-2 gap-2 text-[10px]">
            <div>
              <label class="text-slate-500 block mb-0.5">集装箱单价 万元/MWh</label>
              <input v-model.number="f.containerCostPerMWh" type="number" step="1" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">PCS 单价 万元/MW</label>
              <input v-model.number="f.pcsCostPerMW" type="number" step="1" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">BOP 配套 万元/MWh</label>
              <input v-model.number="f.bopCostPerMWh" type="number" step="1" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">开发费 万元/MW</label>
              <input v-model.number="f.developmentCostPerMW" type="number" step="1" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">固定 O&M 元/kW-年</label>
              <input v-model.number="f.fixedOpexPerKW" type="number" step="0.5" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">可变 O&M 元/MWh</label>
              <input v-model.number="f.varOpexPerMWh" type="number" step="0.1" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">保险费率 % of CAPEX</label>
              <input v-model.number="f.insuranceRate" type="number" step="0.01" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">O&M 年涨幅 %</label>
              <input v-model.number="f.opexEscalation" type="number" step="0.1" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-3 gap-3">
        <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-3">
          <h3 class="font-bold text-xs text-slate-200 mb-2 flex items-center gap-2">
            <span class="w-5 h-5 rounded bg-blue-500/20 text-blue-400 text-[10px] flex items-center justify-center font-bold">III</span>
            融资与税务 Financing & Tax
          </h3>
          <div class="grid grid-cols-1 gap-2 text-[10px]">
            <div>
              <label class="text-slate-500 block mb-0.5">折现率 WACC %</label>
              <input v-model.number="f.discountRate" type="number" step="0.1" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">债务融资比例 %</label>
              <input v-model.number="f.debtRatio" type="number" step="1" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">贷款利率 %</label>
              <input v-model.number="f.interestRate" type="number" step="0.1" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">贷款年限</label>
              <input v-model.number="f.loanTenure" type="number" step="1" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">所得税率 %</label>
              <input v-model.number="f.taxRate" type="number" step="0.5" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">折旧年限</label>
              <input v-model.number="f.depreciationYears" type="number" step="1" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">残值率 %</label>
              <input v-model.number="f.residualRate" type="number" step="0.5" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
          </div>
        </div>

        <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-3">
          <h3 class="font-bold text-xs text-slate-200 mb-2 flex items-center gap-2">
            <span class="w-5 h-5 rounded bg-purple-500/20 text-purple-400 text-[10px] flex items-center justify-center font-bold">IV</span>
            增容与设备成本递减
          </h3>
          <div class="grid grid-cols-1 gap-2 text-[10px]">
            <div>
              <label class="text-slate-500 block mb-0.5">增容集装箱单价 万元/MWh</label>
              <input v-model.number="f.augContainerCostPerMWh" type="number" step="1" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">设备成本年降幅 (学习率) %</label>
              <input v-model.number="f.costDeclineRate" type="number" step="0.1" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">增容安装费 万元/台</label>
              <input v-model.number="f.augInstallCost" type="number" step="0.5" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
            <div>
              <label class="text-slate-500 block mb-0.5">退役成本 万元/MWh</label>
              <input v-model.number="f.decommissioningCost" type="number" step="1" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
          </div>
        </div>

        <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-3">
          <h3 class="font-bold text-xs text-slate-200 mb-2 flex items-center gap-2">
            <span class="w-5 h-5 rounded bg-emerald-500/20 text-emerald-400 text-[10px] flex items-center justify-center font-bold">V</span>
            敏感性分析范围
          </h3>
          <div class="text-[10px] text-slate-500 space-y-1.5">
            <div class="flex justify-between"><span>售电价波动范围</span><span class="text-slate-300">±{{ f.sensPct }}%</span></div>
            <div class="flex justify-between"><span>衰减率波动范围</span><span class="text-slate-300">±{{ f.sensPct }}%</span></div>
            <div class="flex justify-between"><span>融资利率波动</span><span class="text-slate-300">±{{ f.sensPct }}%</span></div>
            <div class="flex justify-between"><span>CAPEX 波动</span><span class="text-slate-300">±{{ f.sensPct }}%</span></div>
            <div>
              <label class="text-slate-500 block mb-0.5">波动幅度 %</label>
              <input v-model.number="f.sensPct" type="number" step="5" class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-200 focus:border-teal-500 focus:outline-none text-xs">
            </div>
          </div>
        </div>
      </div>

      <div class="bg-slate-900/70 border border-slate-800 rounded-lg p-3">
        <div class="flex justify-between items-center mb-2">
          <h3 class="font-bold text-xs text-slate-200">年度现金流明细表 Annual Cash Flow</h3>
          <button @click="recalc" class="text-[10px] bg-teal-600 hover:bg-teal-700 text-white px-3 py-1 rounded transition-colors">重新计算 Recalculate</button>
        </div>
        <div class="overflow-x-auto custom-scrollbar">
          <table class="w-full text-[10px] border-collapse">
            <thead>
              <tr class="text-slate-400 border-b border-slate-800">
                <th class="text-left py-1 px-2 sticky left-0 bg-slate-900/70 z-10">年份</th>
                <th class="text-right py-1 px-2">发电量 MWh</th>
                <th class="text-right py-1 px-2">套利收入 万元</th>
                <th class="text-right py-1 px-2">容量收入 万元</th>
                <th class="text-right py-1 px-2">辅助服务 万元</th>
                <th class="text-right py-1 px-2">总收入 万元</th>
                <th class="text-right py-1 px-2">OPEX 万元</th>
                <th class="text-right py-1 px-2">EBITDA 万元</th>
                <th class="text-right py-1 px-2">折旧 万元</th>
                <th class="text-right py-1 px-2">利息 万元</th>
                <th class="text-right py-1 px-2">税前利润 万元</th>
                <th class="text-right py-1 px-2">所得税 万元</th>
                <th class="text-right py-1 px-2">增容支出 万元</th>
                <th class="text-right py-1 px-2">还本付息 万元</th>
                <th class="text-right py-1 px-2">净现金流 万元</th>
                <th class="text-right py-1 px-2">累计净现金流 万元</th>
                <th class="text-right py-1 px-2" v-if="f.debtRatio > 0">DSCR</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in cashFlowTable" :key="'yr'+row.year"
                :class="['border-b border-slate-800/50', row.year === 0 ? 'text-amber-400 font-bold' : 'text-slate-300']">
                <td class="py-1 px-2 sticky left-0" :class="row.year === 0 ? 'bg-slate-900/70' : 'bg-slate-900/70'">{{ row.year === 0 ? '建设期' : row.year }}</td>
                <td class="text-right py-1 px-2 font-mono">{{ fmtNum(row.energy) }}</td>
                <td class="text-right py-1 px-2 font-mono">{{ fmtNum(row.arbitrage) }}</td>
                <td class="text-right py-1 px-2 font-mono">{{ fmtNum(row.capacity) }}</td>
                <td class="text-right py-1 px-2 font-mono">{{ fmtNum(row.ancillary) }}</td>
                <td class="text-right py-1 px-2 font-mono">{{ fmtNum(row.revenue) }}</td>
                <td class="text-right py-1 px-2 font-mono">{{ fmtNum(row.opex) }}</td>
                <td class="text-right py-1 px-2 font-mono" :class="row.ebitda < 0 ? 'text-red-400' : ''">{{ fmtNum(row.ebitda) }}</td>
                <td class="text-right py-1 px-2 font-mono">{{ fmtNum(row.depreciation) }}</td>
                <td class="text-right py-1 px-2 font-mono">{{ fmtNum(row.interest) }}</td>
                <td class="text-right py-1 px-2 font-mono" :class="row.taxableIncome < 0 ? 'text-red-400' : ''">{{ fmtNum(row.taxableIncome) }}</td>
                <td class="text-right py-1 px-2 font-mono">{{ fmtNum(row.tax) }}</td>
                <td class="text-right py-1 px-2 font-mono">{{ fmtNum(row.augCapex) }}</td>
                <td class="text-right py-1 px-2 font-mono">{{ fmtNum(row.debtService) }}</td>
                <td class="text-right py-1 px-2 font-mono font-bold" :class="row.cashFlow < 0 ? 'text-red-400' : 'text-emerald-400'">{{ fmtNum(row.cashFlow) }}</td>
                <td class="text-right py-1 px-2 font-mono" :class="row.cumCashFlow < 0 ? 'text-red-400' : ''">{{ fmtNum(row.cumCashFlow) }}</td>
                <td class="text-right py-1 px-2 font-mono" v-if="f.debtRatio > 0">{{ row.dscr ? row.dscr.toFixed(2) : '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'

const props = defineProps({ params: Object, results: Object, soh: Array, rte: Array, augQty: Array })

const f = reactive({
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
  fixedOpexPerKW: 35,
  varOpexPerMWh: 3,
  insuranceRate: 0.4,
  opexEscalation: 2.0,
  discountRate: 7,
  debtRatio: 70,
  interestRate: 4.5,
  loanTenure: 15,
  taxRate: 25,
  depreciationYears: 20,
  residualRate: 5,
  augContainerCostPerMWh: 90,
  costDeclineRate: 5,
  augInstallCost: 5,
  decommissioningCost: 10,
  sensPct: 20,
})

const metrics = ref([
  { label: 'Project IRR', value: '-', unit: '%', color: 'bg-slate-900/80 border-teal-500/30', textColor: 'text-teal-400' },
  { label: 'Equity IRR', value: '-', unit: '%', color: 'bg-slate-900/80 border-emerald-500/30', textColor: 'text-emerald-400' },
  { label: 'NPV (7%)', value: '-', unit: '万元', color: 'bg-slate-900/80 border-blue-500/30', textColor: 'text-blue-400' },
  { label: 'LCOS', value: '-', unit: '元/kWh', color: 'bg-slate-900/80 border-purple-500/30', textColor: 'text-purple-400' },
  { label: 'Payback', value: '-', unit: '年', color: 'bg-slate-900/80 border-amber-500/30', textColor: 'text-amber-400' },
  { label: 'Total CAPEX', value: '-', unit: '万元', color: 'bg-slate-900/80 border-rose-500/30', textColor: 'text-rose-400' },
])

const cashFlowTable = ref([])

function fmtNum(v) {
  if (v == null || isNaN(v)) return '-'
  if (Math.abs(v) >= 100) return v.toFixed(1)
  return v.toFixed(2)
}

function computeAll() {
  const p = props.params || {}
  const soh = props.soh || []
  const augQty = props.augQty || []
  const N = 26
  const ratedEnergy = p.ratedEnergy || 5
  const initContainerQty = p.initContainerQty || 62
  const initPcsQty = p.initPcsQty || 1
  const cyclesPerDay = p.cyclesPerDay || 1
  const duration = p.duration || 2
  const totalMW = (ratedEnergy * initContainerQty) / (duration || 1)
  const totalMWh = ratedEnergy * initContainerQty

  const containerCap = ratedEnergy * initContainerQty * 1000
  const totalCapMW = containerCap / (duration || 1) / 1000
  const totalCapMWh = containerCap / 1000

  const containerCost = f.containerCostPerMWh * (totalCapMWh || initContainerQty * ratedEnergy)
  const pcsCost = f.pcsCostPerMW * totalCapMW
  const bopCost = f.bopCostPerMWh * (totalCapMWh || initContainerQty * ratedEnergy)
  const devCost = f.developmentCostPerMW * totalCapMW
  const totalCapex = containerCost + pcsCost + bopCost + devCost

  const debtAmount = totalCapex * f.debtRatio / 100
  const equityAmount = totalCapex - debtAmount
  const annualDebtService = f.interestRate > 0 && f.loanTenure > 0
    ? debtAmount * (f.interestRate / 100) * Math.pow(1 + f.interestRate / 100, f.loanTenure) / (Math.pow(1 + f.interestRate / 100, f.loanTenure) - 1)
    : 0

  const annualDepreciation = f.depreciationYears > 0
    ? totalCapex * (1 - f.residualRate / 100) / f.depreciationYears
    : 0
  const residualValue = totalCapex * f.residualRate / 100

  const spread = (f.peakPrice - f.offPeakPrice) * f.spreadCapture / 100

  const rows = []

  rows.push({
    year: 0,
    energy: 0, arbitrage: 0, capacity: 0, ancillary: 0, revenue: 0,
    opex: 0, ebitda: 0, depreciation: 0, interest: 0, taxableIncome: 0,
    tax: 0, augCapex: -totalCapex, debtService: 0, cashFlow: -totalCapex,
    cumCashFlow: -totalCapex, dscr: null,
  })

  let cumCash = -totalCapex
  let remainingDebt = debtAmount
  let totalDiscountedCost = totalCapex
  let totalDiscountedEnergy = 0

  for (let i = 1; i <= 25; i++) {
    const idx = i
    const cSoh = soh[idx] != null ? soh[idx] : (soh.length > 0 ? soh[soh.length - 1] : 1)
    const yearEnergy = totalCapMWh * cyclesPerDay * f.operatingDays * cSoh * (1 - f.efficiencyLossPct / 100)

    const priceFactor = Math.pow(1 + f.priceEscalation / 100, i)
    const opexFactor = Math.pow(1 + f.opexEscalation / 100, i)

    const arbitrageRev = yearEnergy * spread / 10000 * priceFactor
    const capacityRev = totalCapMW * f.capacityPrice / 10000 * priceFactor
    const ancillaryRev = totalCapMW * f.ancillaryPrice / 10000 * priceFactor
    const totalRevenue = arbitrageRev + capacityRev + ancillaryRev

    const fixedOpex = f.fixedOpexPerKW * totalCapMW * 1000 / 10000 * opexFactor
    const varOpex = f.varOpexPerMWh * yearEnergy / 10000 * opexFactor
    const insurance = totalCapex * f.insuranceRate / 100
    const landLease = totalCapMW * 2 / 10000
    const totalOpex = fixedOpex + varOpex + insurance + landLease

    const ebitda = totalRevenue - totalOpex

    const dep = i <= f.depreciationYears ? annualDepreciation : 0

    let interestPaid = 0
    let principalPaid = 0
    let debtServiceYear = 0
    if (remainingDebt > 0 && i <= f.loanTenure) {
      interestPaid = remainingDebt * f.interestRate / 100
      principalPaid = Math.min(annualDebtService - interestPaid, remainingDebt)
      debtServiceYear = interestPaid + principalPaid
      remainingDebt = Math.max(0, remainingDebt - principalPaid)
    }

    const taxableIncome = ebitda - dep - interestPaid
    const tax = Math.max(0, taxableIncome * f.taxRate / 100)

    const augQtyYear = augQty[idx] || 0
    const costDeclineFactor = Math.pow(1 - f.costDeclineRate / 100, i)
    const augContainerPrice = f.augContainerCostPerMWh * costDeclineFactor
    const augCapexYear = augQtyYear > 0
      ? -(augQtyYear * ratedEnergy * augContainerPrice + augQtyYear * f.augInstallCost)
      : 0

    const cashFlow = ebitda - tax - debtServiceYear + augCapexYear
    cumCash += cashFlow

    const discFactor = Math.pow(1 + f.discountRate / 100, i)
    totalDiscountedCost += (totalOpex + (augCapexYear < 0 ? -augCapexYear : 0)) / discFactor
    totalDiscountedEnergy += yearEnergy / discFactor

    let dscr = null
    if (debtServiceYear > 0) dscr = (ebitda - tax) / debtServiceYear

    rows.push({
      year: i,
      energy: yearEnergy,
      arbitrage: arbitrageRev, capacity: capacityRev, ancillary: ancillaryRev,
      revenue: totalRevenue, opex: totalOpex, ebitda,
      depreciation: dep, interest: interestPaid,
      taxableIncome, tax,
      augCapex: augCapexYear, debtService: debtServiceYear,
      cashFlow, cumCashFlow: cumCash,
      dscr,
    })
  }

  totalDiscountedCost -= residualValue / Math.pow(1 + f.discountRate / 100, 25)
  if (f.decommissioningCost > 0) totalDiscountedCost += (f.decommissioningCost * totalCapMWh) / Math.pow(1 + f.discountRate / 100, 25)

  const lcos = totalDiscountedEnergy > 0 ? totalDiscountedCost / totalDiscountedEnergy * 10000 : 0

  const npv = rows.reduce((sum, r) => {
    const df = r.year === 0 ? 1 : Math.pow(1 + f.discountRate / 100, r.year)
    return sum + r.cashFlow / df
  }, 0)

  const irr = calcIRR(rows.map(r => r.cashFlow), rows.map(r => r.year))

  const equityFlows = rows.map(r => {
    if (r.year === 0) return -equityAmount
    return r.cashFlow
  })
  const equityIrr = calcIRR(equityFlows, rows.map(r => r.year))

  let payback = '-'
  let accum = -totalCapex
  for (let i = 1; i < rows.length; i++) {
    accum += rows[i].cashFlow
    if (accum >= 0) {
      const prevCum = accum - rows[i].cashFlow
      payback = ((i - 1) + (-prevCum) / rows[i].cashFlow).toFixed(1)
      break
    }
  }

  metrics.value[0].value = irr + '%'
  metrics.value[1].value = equityIrr + '%'
  metrics.value[2].value = npv.toFixed(0)
  metrics.value[3].value = lcos.toFixed(3)
  metrics.value[4].value = payback
  metrics.value[5].value = totalCapex.toFixed(0)

  cashFlowTable.value = rows
}

function calcIRR(flows, years) {
  let rate = 0.08
  for (let iter = 0; iter < 100; iter++) {
    let npv = 0, dnpv = 0
    const firstYear = years[0]
    for (let i = 0; i < flows.length; i++) {
      const t = years[i] - firstYear
      const df = Math.pow(1 + rate, t)
      npv += flows[i] / df
      if (t > 0) dnpv += -t * flows[i] / Math.pow(1 + rate, t + 1)
    }
    if (Math.abs(npv) < 1e-6) break
    const newRate = rate - npv / (dnpv || 1e-10)
    if (Math.abs(newRate - rate) < 1e-8) { rate = newRate; break }
    rate = newRate
    if (rate < -0.99) rate = -0.5
    if (rate > 100) rate = 10
  }
  return Math.max(-99, Math.min(999, rate * 100)).toFixed(2)
}

function recalc() {
  computeAll()
}

watch([() => props.params, () => props.soh, () => props.augQty], () => computeAll(), { deep: true, immediate: true })
watch(f, () => computeAll(), { deep: true })
</script>
