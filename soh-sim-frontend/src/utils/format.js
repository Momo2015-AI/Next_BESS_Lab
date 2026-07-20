import i18n from '../i18n'

export function formatCurrency(val) {
  if (val == null) return '—'
  const num = Number(val)
  if (isNaN(num)) return '—'
  if (num >= 1e8) return '$' + (num / 1e8).toFixed(2) + ' ' + i18n.global.t('common.hundredMillion')
  if (num >= 1e6) return '$' + (num / 1e6).toFixed(2) + 'M'
  if (num >= 1e3) return '$' + (num / 1e3).toFixed(0) + 'K'
  return '$' + num.toFixed(0)
}
