export const EXCHANGE_RATES = {
  USD: 1,
  SAR: 3.75,
  AED: 3.6725,
  CNY: 7.24,
}

const POWER_FACTORS = { W: 1e-6, kW: 1e-3, MW: 1, GW: 1e3 }
const ENERGY_FACTORS = { Wh: 1e-6, kWh: 1e-3, MWh: 1, GWh: 1e3 }
const AREA_FACTORS = { sqm: 1, sqft: 10.7639 }

export function toInternal(value, unitCategory, unit) {
  if (unitCategory === 'power') return value * (POWER_FACTORS[unit] || 1)
  if (unitCategory === 'energy') return value * (ENERGY_FACTORS[unit] || 1)
  if (unitCategory === 'area') return unit === 'sqft' ? value / AREA_FACTORS.sqft : value
  if (unitCategory === 'currency') return value / (EXCHANGE_RATES[unit] || 1)
  return value
}

export function toDisplay(value, unitCategory, unit) {
  if (unitCategory === 'power') return value / (POWER_FACTORS[unit] || 1)
  if (unitCategory === 'energy') return value / (ENERGY_FACTORS[unit] || 1)
  if (unitCategory === 'area') return unit === 'sqft' ? value * AREA_FACTORS.sqft : value
  if (unitCategory === 'currency') return value * (EXCHANGE_RATES[unit] || 1)
  return value
}

export function formatCurrency(value, currency = 'USD') {
  const displayed = toDisplay(value, 'currency', currency)
  const symbols = { USD: '$', SAR: 'SAR ', AED: 'AED ', CNY: '¥' }
  const symbol = symbols[currency] || '$'
  return `${symbol}${displayed.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
}

export function formatArea(value, unit = 'sqm') {
  if (unit === 'sqft') {
    const sqft = value * AREA_FACTORS.sqft
    return `${sqft.toLocaleString('en-US', { maximumFractionDigits: 0 })} sq.ft`
  }
  return `${value.toLocaleString('en-US', { maximumFractionDigits: 0 })} m²`
}
