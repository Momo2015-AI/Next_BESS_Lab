import { useI18n } from 'vue-i18n'
import * as echarts from 'echarts/core'

export function useChartOptions() {
  const { t } = useI18n()

  function cumCashFlowGradient(colors) {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
    return new echarts.graphic.LinearGradient(0, 0, 0, 1, [
      { offset: 0, color: isDark ? 'rgba(14,165,233,0.25)' : 'rgba(59,130,246,0.15)' },
      { offset: 1, color: 'transparent' }
    ])
  }

  function getCashFlowOption(rows, colors, paybackYear) {
    const years = rows.map((r) => r.year)
    const cumCF = rows.map((r) => r.cumCashFlow)
    const netCF = rows.map((r) => r.cashFlow)

    return {
      tooltip: {
        trigger: 'axis',
        formatter: (params) => {
          const year = params[0].axisValue
          const row = rows.find((r) => r.year === parseInt(year))
          if (!row) return ''
          const cfClass = row.cashFlow >= 0 ? 'text-success' : 'text-danger'
          const cumClass = row.cumCashFlow >= 0 ? 'text-success' : 'text-danger'
          const yearLabel =
            year === 0
              ? `${t('financialDashboard.chartYear')} ${t('financialDashboard.construction')}`
              : t('financialDashboard.chartYearLabel', { year })
          let html = `<div class="font-bold mb-1">${yearLabel}</div>`
          html += `<div>${t('financialDashboard.chartAnnualCashFlow')}: <span class="font-bold ${cfClass}">${row.cashFlow >= 0 ? '+' : ''}${row.cashFlow.toFixed(0)} ${t('financialDashboard.wanUnit')}</span></div>`
          html += `<div>${t('financialDashboard.chartCumCashFlow')}: <span class="font-bold ${cumClass}">${row.cumCashFlow >= 0 ? '+' : ''}${row.cumCashFlow.toFixed(0)} ${t('financialDashboard.wanUnit')}</span></div>`
          if (row.year > 0) {
            html += '<div style="border-top:1px solid var(--color-border);margin-top:4px;padding-top:4px">'
            html += `<div>${t('financialDashboard.totalRevenue')}: ${row.revenue.toFixed(0)} ${t('financialDashboard.wanUnit')}</div>`
            html += `<div>${t('financialDashboard.opex')}: ${row.opex.toFixed(0)} ${t('financialDashboard.wanUnit')}</div>`
            html += `<div>${t('financialDashboard.ebitda')}: ${row.ebitda.toFixed(0)} ${t('financialDashboard.wanUnit')}</div>`
            html += `<div>${t('financialDashboard.chartDepreciation')}: ${row.depreciation.toFixed(0)} ${t('financialDashboard.wanUnit')}</div>`
            html += `<div>${t('financialDashboard.chartInterest')}: ${row.interest.toFixed(0)} ${t('financialDashboard.wanUnit')}</div>`
            html += `<div>${t('financialDashboard.chartTax')}: ${row.tax.toFixed(0)} ${t('financialDashboard.wanUnit')}</div>`
            if (row.debtService > 0) {
              html += `<div>${t('financialDashboard.chartDebtService')}: ${row.debtService.toFixed(0)} ${t('financialDashboard.wanUnit')}</div>`
              html += `<div>${t('financialDashboard.dscr')}: ${row.dscr ? row.dscr.toFixed(2) : '-'}x</div>`
            }
            html += '</div>'
          }
          return html
        }
      },
      legend: {
        top: 0,
        textStyle: { color: colors.legendText, fontSize: 10 },
        data: [t('financialDashboard.chartCumCashFlow'), t('financialDashboard.chartAnnualCashFlow')]
      },
      grid: { top: 30, right: 20, bottom: 25, left: 65 },
      xAxis: {
        type: 'category',
        data: years,
        axisLabel: { color: colors.axisLabel, fontSize: 9 },
        name: t('financialDashboard.chartYear'),
        nameTextStyle: { color: colors.axisLabel, fontSize: 9 }
      },
      yAxis: [
        {
          type: 'value',
          axisLabel: {
            color: colors.axisLabel,
            fontSize: 9,
            formatter: (v) => (v / 10000).toFixed(1) + t('financialDashboard.chartYiUnit')
          },
          splitLine: { lineStyle: { color: colors.gridLine } }
        }
      ],
      series: [
        {
          name: t('financialDashboard.chartCumCashFlow'),
          type: 'line',
          data: cumCF,
          smooth: true,
          symbol: 'circle',
          symbolSize: 4,
          lineStyle: { color: colors.info, width: 2.5 },
          itemStyle: { color: colors.info, borderWidth: 1, borderColor: 'var(--color-text-on-accent)' },
          areaStyle: { color: cumCashFlowGradient(colors) },
          markLine: {
            silent: true,
            symbol: 'none',
            data: [
              {
                yAxis: 0,
                lineStyle: { color: colors.danger, type: 'dashed', width: 1.5 },
                label: { formatter: t('financialDashboard.chartBreakeven'), color: colors.danger, fontSize: 9 }
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
                    {
                      coord: [paybackYear, 0],
                      value:
                        t('financialDashboard.chartPaybackPrefix') +
                        paybackYear +
                        t('financialDashboard.chartPaybackSuffix'),
                      itemStyle: { color: colors.warning }
                    }
                  ]
                }
              : undefined
        },
        {
          name: t('financialDashboard.chartAnnualCashFlow'),
          type: 'bar',
          data: netCF,
          itemStyle: {
            color: (params) => (params.value >= 0 ? colors.success : colors.danger),
            borderRadius: [2, 2, 0, 0]
          },
          barWidth: 8
        }
      ]
    }
  }

  function getRevenueOption(rows, colors, fmtNum) {
    const years = rows.map((r) => r.year)

    return {
      tooltip: {
        trigger: 'axis',
        formatter: (params) => {
          const year = params[0].axisValue
          const row = rows.find((r) => r.year === parseInt(year))
          if (!row) return ''
          let html = `<div class="font-bold mb-1">${t('financialDashboard.chartYearLabel', { year })}</div>`
          html += `<div>${t('financialDashboard.chartArbitrage')}: <span class="font-bold" style="color:${colors.acLine}">${row.arbitrage.toFixed(0)} ${t('financialDashboard.wanUnit')}</span></div>`
          html += `<div>${t('financialDashboard.chartCapacity')}: <span class="font-bold" style="color:${colors.purple}">${row.capacity.toFixed(0)} ${t('financialDashboard.wanUnit')}</span></div>`
          html += `<div>${t('financialDashboard.chartAncillary')}: <span class="font-bold" style="color:${colors.orange}">${row.ancillary.toFixed(0)} ${t('financialDashboard.wanUnit')}</span></div>`
          html += '<div style="border-top:1px solid var(--color-border);margin-top:4px;padding-top:4px">'
          html += `<div>${t('financialDashboard.totalRevenue')}: <span class="font-bold">${row.revenue.toFixed(0)} ${t('financialDashboard.wanUnit')}</span></div>`
          const arbitragePct = row.revenue > 0 ? ((row.arbitrage / row.revenue) * 100).toFixed(1) : 0
          const capacityPct = row.revenue > 0 ? ((row.capacity / row.revenue) * 100).toFixed(1) : 0
          const ancillaryPct = row.revenue > 0 ? ((row.ancillary / row.revenue) * 100).toFixed(1) : 0
          html += `<div>${t('financialDashboard.chartRevenueStructure')}${t('financialDashboard.chartArbitrage')}${arbitragePct}% + ${t('financialDashboard.chartCapacity')}${capacityPct}% + ${t('financialDashboard.chartAncillary')}${ancillaryPct}%</div>`
          html += `<div>${t('financialDashboard.chartGeneration')}: ${row.energy.toFixed(0)} MWh</div>`
          html += '</div>'
          return html
        }
      },
      legend: {
        top: 0,
        textStyle: { color: colors.legendText, fontSize: 10 },
        data: [
          t('financialDashboard.chartArbitrage'),
          t('financialDashboard.chartCapacity'),
          t('financialDashboard.chartAncillary')
        ]
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
          name: t('financialDashboard.chartArbitrage'),
          type: 'bar',
          stack: 'revenue',
          data: rows.map((r) => r.arbitrage),
          itemStyle: { color: colors.acLine },
          barWidth: 18
        },
        {
          name: t('financialDashboard.chartCapacity'),
          type: 'bar',
          stack: 'revenue',
          data: rows.map((r) => r.capacity),
          itemStyle: { color: colors.purple },
          barWidth: 18
        },
        {
          name: t('financialDashboard.chartAncillary'),
          type: 'bar',
          stack: 'revenue',
          data: rows.map((r) => r.ancillary),
          itemStyle: { color: colors.orange },
          barWidth: 18
        }
      ]
    }
  }

  function getDscrOption(rows, colors, fmtNum) {
    const years = rows.map((r) => r.year)
    const dscrData = rows.map((r) => r.dscr || 0)

    return {
      tooltip: {
        trigger: 'axis',
        formatter: (params) => {
          const year = params[0].axisValue
          const row = rows.find((r) => r.year === parseInt(year))
          if (!row) return ''
          const dscrColor = row.dscr >= 1.3 ? 'text-success' : 'text-danger'
          let html = `<div class="font-bold mb-1">${t('financialDashboard.chartYearLabel', { year })}</div>`
          html += `<div>${t('financialDashboard.chartEbitda')}: <span class="font-bold" style="color:${colors.cyan}">${row.ebitda.toFixed(0)} ${t('financialDashboard.wanUnit')}</span></div>`
          html += `<div>${t('financialDashboard.chartDebtService')}: <span class="font-bold" style="color:${colors.redLight}">${row.debtService.toFixed(0)} ${t('financialDashboard.wanUnit')}</span></div>`
          if (row.debtService > 0) {
            html += '<div style="border-top:1px solid var(--color-border);margin-top:4px;padding-top:4px">'
            html += `<div>${t('financialDashboard.dscr')}: <span class="font-bold text-base ${dscrColor}">${row.dscr.toFixed(2)}x</span></div>`
            html += `<div class="${dscrColor}">${row.dscr >= 1.3 ? t('financialDashboard.chartBankOk') : t('financialDashboard.chartBankFail')}</div>`
            html += `<div>${t('financialDashboard.chartInterestExpense')}: ${row.interest.toFixed(0)} ${t('financialDashboard.wanUnit')}</div>`
            html += `<div>${t('financialDashboard.chartPrincipalRepayment')}: ${(row.debtService - row.interest).toFixed(0)} ${t('financialDashboard.wanUnit')}</div>`
            html += '</div>'
          } else {
            html += `<div>${t('financialDashboard.dscr')}: ${t('financialDashboard.chartNoDebt')}</div>`
          }
          return html
        }
      },
      legend: {
        top: 0,
        textStyle: { color: colors.legendText, fontSize: 10 },
        data: [
          t('financialDashboard.chartEbitda'),
          t('financialDashboard.chartDebtService'),
          t('financialDashboard.chartDscrLine')
        ]
      },
      grid: { top: 30, right: 45, bottom: 25, left: 55 },
      xAxis: { type: 'category', data: years, axisLabel: { color: colors.axisLabel, fontSize: 9 } },
      yAxis: [
        {
          type: 'value',
          axisLabel: { color: colors.axisLabel, fontSize: 9, formatter: (v) => fmtNum(v) },
          splitLine: { lineStyle: { color: colors.gridLine } },
          name: t('financialDashboard.wanUnit')
        },
        {
          type: 'value',
          min: 0,
          max: 4,
          axisLabel: { color: colors.axisLabel, fontSize: 9 },
          splitLine: { show: false },
          name: t('financialDashboard.chartMultiple')
        }
      ],
      series: [
        {
          name: t('financialDashboard.chartEbitda'),
          type: 'bar',
          data: rows.map((r) => r.ebitda),
          itemStyle: { color: colors.cyan, borderRadius: [2, 2, 0, 0] },
          barWidth: 10,
          barGap: '30%'
        },
        {
          name: t('financialDashboard.chartDebtService'),
          type: 'bar',
          data: rows.map((r) => r.debtService),
          itemStyle: { color: colors.redLight, borderRadius: [2, 2, 0, 0] },
          barWidth: 10
        },
        {
          name: t('financialDashboard.chartDscrLine'),
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
                label: { formatter: t('financialDashboard.chartDscrThreshold'), color: colors.danger, fontSize: 9 }
              },
              {
                yAxis: 1.5,
                lineStyle: { color: colors.warning, type: 'dashed', width: 1 },
                label: { formatter: t('financialDashboard.chartIdealDscr'), color: colors.warning, fontSize: 8 }
              }
            ]
          }
        }
      ]
    }
  }

  function getCapexOption(capexData, colors) {
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
    } = capexData

    const capexItems = [
      { value: containerCost, name: t('financialDashboard.chartContainer'), color: colors.info },
      { value: pcsCost, name: t('financialDashboard.chartPcs'), color: colors.purple },
      { value: bopCost, name: t('financialDashboard.chartBop'), color: colors.warning },
      { value: substationCost, name: t('financialDashboard.chartSubstation'), color: 'var(--color-chart-cyan)' },
      { value: transmissionCost, name: t('financialDashboard.chartTransmission'), color: 'var(--color-chart-orange)' },
      { value: landCost, name: t('financialDashboard.chartLand'), color: 'var(--color-success)' },
      { value: devCost, name: t('financialDashboard.chartDev'), color: colors.muted }
    ].filter((item) => item.value > 0)

    // sensitivityData reserved for future tornado overlay
    return {
      tooltip: {
        trigger: 'item',
        formatter: (params) => {
          const perMWh = params.value / totalCapMWh
          const perMW = params.value / totalCapMW
          return `${params.name}<br/>${t('financialDashboard.chartAmount')}: ${params.value.toFixed(0)} ${t('financialDashboard.wanUnit')} (${params.percent.toFixed(1)}%)<br/>${t('financialDashboard.chartUnitPrice')}: ${perMWh.toFixed(1)} ${t('financialDashboard.wanUnit')}/MWh = ${perMW.toFixed(1)} ${t('financialDashboard.wanUnit')}/MW`
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
            formatter: (params) => `${params.name}\n${params.value.toFixed(0)}${t('financialDashboard.wanUnit')}`,
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
    }
  }

  return { getCashFlowOption, getRevenueOption, getDscrOption, getCapexOption }
}
