<template>
  <div class="epc-page">
    <div class="epc-header">
      <h1>EPC 工程化模块</h1>
      <p class="epc-desc">系统架构设计、电网合规分析、安全消防、IPP财务、合规矩阵、热管理、SCADA/EMS、高压接入、投标文档</p>
    </div>

    <!-- 模块标签页 -->
    <div class="epc-tabs">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        @click="activeModule = tab.id"
        :class="{ active: activeModule === tab.id }"
      >
        <span class="tab-icon" v-html="tab.svg"></span>
        <span class="tab-label">{{ tab.label }}</span>
        <span class="tab-priority" :class="'pri-' + tab.priority">{{ tab.priority }}</span>
      </button>
    </div>

    <!-- P0-3: 系统架构 -->
    <div v-show="activeModule === 'architecture'" class="epc-panel space-y-4">
      <div class="panel-card">
        <h3 class="panel-title">系统架构设计</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-xs mb-1 field-label">系统功率 (MW)</label>
            <input v-model.number="archForm.total_power_mw" type="number" class="form-input" placeholder="1400" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">系统能量 (MWh)</label>
            <input v-model.number="archForm.total_energy_mwh" type="number" class="form-input" placeholder="8400" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">架构类型</label>
            <select v-model="archForm.architecture_type" class="form-input">
              <option value="central">集中式</option>
              <option value="string">组串式</option>
              <option value="hybrid">混合式</option>
            </select>
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">耦合方式</label>
            <select v-model="archForm.coupling_type" class="form-input">
              <option value="AC">AC耦合</option>
              <option value="DC">DC耦合</option>
              <option value="hybrid">混合耦合</option>
            </select>
          </div>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-xs mb-1 field-label">电芯电压 (V)</label>
            <input v-model.number="archForm.cell_voltage" type="number" step="0.1" class="form-input" placeholder="3.2" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">电芯容量 (Ah)</label>
            <input v-model.number="archForm.cell_capacity" type="number" class="form-input" placeholder="280" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">PCS功率 (MW)</label>
            <input v-model.number="archForm.pcs_power_mw" type="number" step="0.01" class="form-input" placeholder="3.45" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">PCS最大DC电压 (V)</label>
            <input v-model.number="archForm.pcs_max_dc_voltage" type="number" class="form-input" placeholder="1500" />
          </div>
        </div>
        <button @click="designArchitecture" :disabled="loading" class="btn-primary">
          {{ loading ? '计算中...' : '执行架构设计' }}
        </button>

        <div v-if="archResult" class="mt-6 space-y-4">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
            <div v-for="item in archResult.topology_data.levels" :key="item.name" class="metric-card">
              <div class="metric-value">{{ item.count }}</div>
              <div class="metric-label">{{ item.name }} ({{ item.unit }})</div>
            </div>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
            <div class="metric-card"><div class="metric-value">{{ archResult.pcs_count }}</div><div class="metric-label">PCS总数</div></div>
            <div class="metric-card"><div class="metric-value">{{ archResult.dc_bus_voltage }}V</div><div class="metric-label">DC母线电压</div></div>
            <div class="metric-card"><div class="metric-value">{{ archResult.total_containers }}</div><div class="metric-label">集装箱总数</div></div>
            <div class="metric-card"><div class="metric-value">{{ archResult.stage_count }}</div><div class="metric-label">分期数</div></div>
            <div class="metric-card"><div class="metric-value">{{ archResult.duration_hours }}h</div><div class="metric-label">储能时长</div></div>
          </div>
          <div v-if="archResult.stages" class="mt-4">
            <h4 class="text-sm font-bold mb-2 section-title">分期建设方案</h4>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
              <div v-for="stage in archResult.stages" :key="stage.stage" class="stage-card">
                <div class="font-bold text-sm stage-title">{{ stage.stage }}期</div>
                <div class="text-xs" style="color: #666;">{{ stage.power_mw }}MW / {{ stage.energy_mwh }}MWh</div>
                <div class="text-xs" style="color: #999;">{{ stage.estimated_date }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- P0-1: 电网合规 -->
    <div v-show="activeModule === 'gridCompliance'" class="epc-panel space-y-4">
      <div class="panel-card">
        <h3 class="panel-title">电网合规分析</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-xs mb-1 field-label">电网标准</label>
            <select v-model="gcForm.grid_standard" class="form-input">
              <option v-for="s in gridStandards" :key="s.code" :value="s.code">{{ s.name }}</option>
            </select>
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">并网点电压 (kV)</label>
            <input v-model.number="gcForm.grid_voltage_kv" type="number" class="form-input" placeholder="33" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">电网频率 (Hz)</label>
            <input v-model.number="gcForm.grid_frequency_hz" type="number" step="0.01" class="form-input" placeholder="50" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">PCS数量</label>
            <input v-model.number="gcForm.pcs_count" type="number" class="form-input" placeholder="10" />
          </div>
        </div>
        <button @click="analyzeGridCompliance" :disabled="loading" class="btn-primary">
          {{ loading ? '分析中...' : '执行合规分析' }}
        </button>

        <div v-if="gcResult" class="mt-6 space-y-4">
          <div class="flex items-center gap-4 p-4 rounded-lg" :class="gcResult.overall_pass ? 'pass-banner' : 'fail-banner'">
            <span class="status-icon">{{ gcResult.overall_pass ? 'pass' : 'fail' }}</span>
            <div>
              <div class="font-bold" :class="gcResult.overall_pass ? 'pass-text' : 'fail-text'">
                {{ gcResult.overall_pass ? '全部合规' : '存在不合规项' }}
              </div>
              <div class="text-xs" style="color: #666;" v-if="gcResult.failed_items.length">
                不合规: {{ gcResult.failed_items.join(', ') }}
              </div>
            </div>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="metric-card"><div class="metric-value" :class="gcResult.lvrt_pass ? 'pass-text' : 'fail-text'">{{ gcResult.lvrt_pass ? 'PASS' : 'FAIL' }}</div><div class="metric-label">LVRT低电压穿越</div></div>
            <div class="metric-card"><div class="metric-value" :class="gcResult.hvrt_pass ? 'pass-text' : 'fail-text'">{{ gcResult.hvrt_pass ? 'PASS' : 'FAIL' }}</div><div class="metric-label">HVRT高电压穿越</div></div>
            <div class="metric-card"><div class="metric-value" :class="gcResult.freq_response_pass ? 'pass-text' : 'fail-text'">{{ gcResult.freq_response_pass ? 'PASS' : 'FAIL' }}</div><div class="metric-label">频率响应</div></div>
            <div class="metric-card"><div class="metric-value" :class="gcResult.reactive_pass ? 'pass-text' : 'fail-text'">{{ gcResult.reactive_pass ? 'PASS' : 'FAIL' }}</div><div class="metric-label">无功功率 ({{ gcResult.reactive_capacity_mvar }}MVar)</div></div>
            <div class="metric-card"><div class="metric-value" :class="gcResult.power_quality_pass ? 'pass-text' : 'fail-text'">{{ gcResult.thd }}%</div><div class="metric-label">THD (限值5%)</div></div>
            <div class="metric-card"><div class="metric-value" :class="gcResult.anti_islanding_pass ? 'pass-text' : 'fail-text'">{{ gcResult.anti_islanding_time_s }}s</div><div class="metric-label">防孤岛 (限值2s)</div></div>
            <div class="metric-card"><div class="metric-value" :class="gcResult.comm_pass ? 'pass-text' : 'fail-text'">{{ gcResult.comm_pass ? 'PASS' : 'FAIL' }}</div><div class="metric-label">通信合规</div></div>
          </div>
        </div>
      </div>
    </div>

    <!-- P0-2: 安全消防 -->
    <div v-show="activeModule === 'safety'" class="epc-panel space-y-4">
      <div class="panel-card">
        <h3 class="panel-title">安全与消防设计</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-xs mb-1 field-label">系统容量 (MWh)</label>
            <input v-model.number="sfForm.system_capacity_mwh" type="number" class="form-input" placeholder="100" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">集装箱数量</label>
            <input v-model.number="sfForm.container_count" type="number" class="form-input" placeholder="20" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">化学体系</label>
            <select v-model="sfForm.chemistry_type" class="form-input">
              <option value="LFP">LFP (磷酸铁锂)</option>
              <option value="NCM">NCM (三元)</option>
              <option value="NCA">NCA</option>
              <option value="LTO">LTO (钛酸锂)</option>
            </select>
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">灭火系统</label>
            <select v-model="sfForm.suppression_type" class="form-input">
              <option value="Novec1230">Novec 1230</option>
              <option value="Aerosol">气溶胶</option>
              <option value="Water-mist">细水雾</option>
            </select>
          </div>
        </div>
        <button @click="analyzeSafety" :disabled="loading" class="btn-primary">
          {{ loading ? '分析中...' : '执行安全分析' }}
        </button>

        <div v-if="sfResult" class="mt-6 space-y-4">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="metric-card"><div class="metric-value">{{ sfResult.zone_count }}</div><div class="metric-label">防火分区数</div></div>
            <div class="metric-card"><div class="metric-value">{{ sfResult.container_spacing_m }}m</div><div class="metric-label">集装箱间距</div></div>
            <div class="metric-card"><div class="metric-value">{{ sfResult.thermal_runaway_temp_c }}°C</div><div class="metric-label">热失控温度</div></div>
            <div class="metric-card"><div class="metric-value">{{ sfResult.propagation_time_min }}min</div><div class="metric-label">蔓延时间</div></div>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="metric-card"><div class="metric-value" :class="sfResult.ul_9540a_pass ? 'pass-text' : 'fail-text'">{{ sfResult.ul_9540a_pass ? 'PASS' : 'FAIL' }}</div><div class="metric-label">UL 9540A</div></div>
            <div class="metric-card"><div class="metric-value" :class="sfResult.nfpa_855_pass ? 'pass-text' : 'fail-text'">{{ sfResult.nfpa_855_pass ? 'PASS' : 'FAIL' }}</div><div class="metric-label">NFPA 855</div></div>
            <div class="metric-card"><div class="metric-value" :class="sfResult.iec_62619_pass ? 'pass-text' : 'fail-text'">{{ sfResult.iec_62619_pass ? 'PASS' : 'FAIL' }}</div><div class="metric-label">IEC 62619</div></div>
            <div class="metric-card"><div class="metric-value">{{ sfResult.suppression_capacity_kg }}kg</div><div class="metric-label">灭火剂容量</div></div>
          </div>
        </div>
      </div>
    </div>

    <!-- P0-4: IPP财务 -->
    <div v-show="activeModule === 'ipp'" class="epc-panel space-y-4">
      <div class="panel-card">
        <h3 class="panel-title">IPP财务模型</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-xs mb-1 field-label">项目寿命 (年)</label>
            <input v-model.number="ippForm.project_life_years" type="number" class="form-input" placeholder="25" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">总CAPEX (USD)</label>
            <input v-model.number="ippForm.total_capex_usd" type="number" class="form-input" placeholder="500000000" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">容量 (MW)</label>
            <input v-model.number="ippForm.capacity_mw" type="number" class="form-input" placeholder="100" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">能量 (MWh)</label>
            <input v-model.number="ippForm.energy_mwh" type="number" class="form-input" placeholder="200" />
          </div>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-xs mb-1 field-label">容量价格 ($/kW/月)</label>
            <input v-model.number="ippForm.capacity_price_usd_kw_month" type="number" step="0.1" class="form-input" placeholder="8.0" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">电量价格 ($/kWh)</label>
            <input v-model.number="ippForm.energy_price_usd_kwh" type="number" step="0.01" class="form-input" placeholder="0.05" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">PPA递增率</label>
            <input v-model.number="ippForm.ppa_escalation_rate" type="number" step="0.01" class="form-input" placeholder="0.02" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">贷款比例</label>
            <input v-model.number="ippForm.debt_ratio" type="number" step="0.05" class="form-input" placeholder="0.7" />
          </div>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-xs mb-1 field-label">贷款利率</label>
            <input v-model.number="ippForm.debt_interest_rate" type="number" step="0.01" class="form-input" placeholder="0.05" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">贷款期限 (年)</label>
            <input v-model.number="ippForm.debt_tenor_years" type="number" class="form-input" placeholder="15" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">年OPEX (USD)</label>
            <input v-model.number="ippForm.annual_opex_usd" type="number" class="form-input" placeholder="5000000" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">可用率保证</label>
            <input v-model.number="ippForm.availability_guarantee" type="number" step="0.01" class="form-input" placeholder="0.98" />
          </div>
        </div>
        <button @click="calculateIPP" :disabled="loading" class="btn-primary">
          {{ loading ? '计算中...' : '执行财务计算' }}
        </button>

        <div v-if="ippResult" class="mt-6 space-y-4">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="metric-card"><div class="metric-value primary-text">${{ formatNum(ippResult.npv_usd) }}</div><div class="metric-label">NPV</div></div>
            <div class="metric-card"><div class="metric-value primary-text">{{ ippResult.irr }}%</div><div class="metric-label">项目IRR</div></div>
            <div class="metric-card"><div class="metric-value primary-text">{{ ippResult.equity_irr }}%</div><div class="metric-label">股权IRR</div></div>
            <div class="metric-card"><div class="metric-value primary-text">${{ ippResult.lcoe_usd_kwh }}/kWh</div><div class="metric-label">LCOE</div></div>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
            <div class="metric-card"><div class="metric-value">{{ ippResult.dscr_avg }}</div><div class="metric-label">平均DSCR</div></div>
            <div class="metric-card"><div class="metric-value">{{ ippResult.dscr_min }}</div><div class="metric-label">最小DSCR</div></div>
            <div class="metric-card"><div class="metric-value">{{ ippResult.payback_years }}年</div><div class="metric-label">回收期</div></div>
          </div>
        </div>
      </div>
    </div>

    <!-- P0-5: 合规矩阵 -->
    <div v-show="activeModule === 'matrix'" class="epc-panel space-y-4">
      <div class="panel-card">
        <h3 class="panel-title">合规矩阵生成</h3>
        <div class="flex gap-4 mb-4">
          <select v-model="matrixForm.template" class="form-input" style="max-width: 300px;">
            <option value="UAE_DEWA_VII_BESS">UAE DEWA VII BESS RFP</option>
          </select>
          <button @click="generateMatrix" :disabled="loading" class="btn-primary">
            {{ loading ? '生成中...' : '生成合规矩阵' }}
          </button>
        </div>

        <div v-if="matrixResult" class="mt-4">
          <div class="grid grid-cols-4 gap-3 mb-4">
            <div class="metric-card"><div class="metric-value">{{ matrixResult.total }}</div><div class="metric-label">总条款</div></div>
            <div class="metric-card"><div class="metric-value pass-text">{{ matrixResult.compliant }}</div><div class="metric-label">合规</div></div>
            <div class="metric-card"><div class="metric-value fail-text">{{ matrixResult.non_compliant }}</div><div class="metric-label">不合规</div></div>
            <div class="metric-card"><div class="metric-value warn-text">{{ matrixResult.partial }}</div><div class="metric-label">部分合规</div></div>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-sm data-table">
              <thead>
                <tr>
                  <th class="px-3 py-2 text-left header-cell">条款</th>
                  <th class="px-3 py-2 text-left header-cell">要求</th>
                  <th class="px-3 py-2 text-left header-cell">类别</th>
                  <th class="px-3 py-2 text-left header-cell">状态</th>
                  <th class="px-3 py-2 text-left header-cell">回应</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in matrixResult.matrix" :key="item.section" class="border-row">
                  <td class="px-3 py-2 font-mono text-xs">{{ item.section }}</td>
                  <td class="px-3 py-2">{{ item.requirement }}</td>
                  <td class="px-3 py-2 text-xs" style="color: #999;">{{ item.category }}</td>
                  <td class="px-3 py-2">
                    <span class="status-badge" :class="statusClass(item.compliance_status)">
                      {{ statusLabel(item.compliance_status) }}
                    </span>
                  </td>
                  <td class="px-3 py-2 text-xs" style="color: #666;">{{ item.response }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- P1-1: 热管理 -->
    <div v-show="activeModule === 'thermal'" class="epc-panel space-y-4">
      <div class="panel-card">
        <h3 class="panel-title">热管理设计</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-xs mb-1 field-label">最高环境温度 (°C)</label>
            <input v-model.number="tmForm.ambient_max_c" type="number" class="form-input" placeholder="45" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">电芯容量 (Ah)</label>
            <input v-model.number="tmForm.cell_capacity_ah" type="number" class="form-input" placeholder="280" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">充放电倍率 (C)</label>
            <input v-model.number="tmForm.c_rate" type="number" step="0.1" class="form-input" placeholder="0.5" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">冷却方式</label>
            <select v-model="tmForm.cooling_type" class="form-input">
              <option value="liquid">液冷</option>
              <option value="air">风冷</option>
            </select>
          </div>
        </div>
        <button @click="calculateThermal" :disabled="loading" class="btn-primary">
          {{ loading ? '计算中...' : '执行热管理计算' }}
        </button>

        <div v-if="tmResult" class="mt-6 space-y-4">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="metric-card"><div class="metric-value">{{ tmResult.cooling_power_kw }}kW</div><div class="metric-label">制冷功率</div></div>
            <div class="metric-card"><div class="metric-value">{{ tmResult.coolant_flow_rate_lpm }}L/min</div><div class="metric-label">冷却液流量</div></div>
            <div class="metric-card"><div class="metric-value">{{ tmResult.max_cell_temp_c }}°C</div><div class="metric-label">最高电芯温度</div></div>
            <div class="metric-card"><div class="metric-value">{{ formatNum(tmResult.annual_cooling_energy_kwh) }}kWh</div><div class="metric-label">年制冷能耗</div></div>
          </div>
          <div v-if="tmResult.derating_curve" class="mt-4">
            <h4 class="text-sm font-bold mb-2 section-title">高温降额曲线</h4>
            <div class="flex gap-1 items-end h-32 derating-chart">
              <div v-for="point in tmResult.derating_curve" :key="point.temp" class="flex-1 flex flex-col items-center">
                <div class="w-full rounded-t derating-bar" :style="{ height: point.power_pct + '%', backgroundColor: getDeratingColor(point.power_pct) }"></div>
                <div class="text-xs mt-1" style="color: #999;">{{ point.temp }}°C</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- P1-2: SCADA/EMS -->
    <div v-show="activeModule === 'scada'" class="epc-panel space-y-4">
      <div class="panel-card">
        <h3 class="panel-title">SCADA/EMS设计</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-xs mb-1 field-label">集装箱数量</label>
            <input v-model.number="seForm.container_count" type="number" class="form-input" placeholder="20" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">PCS数量</label>
            <input v-model.number="seForm.pcs_count" type="number" class="form-input" placeholder="10" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">通信协议</label>
            <select v-model="seForm.communication_protocol" class="form-input">
              <option value="IEC_61850">IEC 61850</option>
              <option value="Modbus_TCP">Modbus TCP</option>
              <option value="DNP3">DNP3</option>
            </select>
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">调度策略</label>
            <select v-model="seForm.dispatch_strategy" class="form-input">
              <option value="peak_shaving">削峰填谷</option>
              <option value="arbitrage">套利</option>
              <option value="frequency_regulation">调频</option>
            </select>
          </div>
        </div>
        <button @click="designScada" :disabled="loading" class="btn-primary">
          {{ loading ? '设计中...' : '执行SCADA设计' }}
        </button>

        <div v-if="seResult" class="mt-6 space-y-4">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="metric-card"><div class="metric-value">{{ seResult.total_data_points }}</div><div class="metric-label">总数据点</div></div>
            <div class="metric-card"><div class="metric-value">{{ seResult.analog_points }}</div><div class="metric-label">模拟量</div></div>
            <div class="metric-card"><div class="metric-value">{{ seResult.digital_points }}</div><div class="metric-label">数字量</div></div>
            <div class="metric-card"><div class="metric-value">{{ seResult.control_points }}</div><div class="metric-label">控制点</div></div>
          </div>
          <div class="info-box">
            <div class="text-sm font-bold mb-2 section-title">系统架构</div>
            <div class="text-sm space-y-1 info-list">
              <div>架构类型: {{ seResult.scada_architecture }}</div>
              <div>网络拓扑: {{ seResult.network_topology }}</div>
              <div>冗余等级: {{ seResult.redundancy_level }}</div>
              <div>加密方式: {{ seResult.encryption_type }}</div>
              <div>NERC-CIP: {{ seResult.nerc_cip_compliant ? 'pass' : 'fail' }}</div>
              <div>IEC 62443: {{ seResult.iec_62443_compliant ? 'pass' : 'fail' }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- P1-3: 高压接入 -->
    <div v-show="activeModule === 'hv'" class="epc-panel space-y-4">
      <div class="panel-card">
        <h3 class="panel-title">高压接入设计</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-xs mb-1 field-label">总功率 (MW)</label>
            <input v-model.number="hvForm.total_power_mw" type="number" class="form-input" placeholder="100" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">并网点电压 (kV)</label>
            <input v-model.number="hvForm.poc_voltage_kv" type="number" class="form-input" placeholder="33" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">短路容量 (MVA)</label>
            <input v-model.number="hvForm.short_circuit_capacity_mva" type="number" class="form-input" placeholder="500" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">并网点类型</label>
            <select v-model="hvForm.poc_type" class="form-input">
              <option value="substation">变电站</option>
              <option value="overhead_line">架空线</option>
              <option value="cable">电缆</option>
            </select>
          </div>
        </div>
        <button @click="designHV" :disabled="loading" class="btn-primary">
          {{ loading ? '设计中...' : '执行高压接入设计' }}
        </button>

        <div v-if="hvResult" class="mt-6 space-y-4">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="metric-card"><div class="metric-value">{{ hvResult.transformer_count }}</div><div class="metric-label">变压器数量</div></div>
            <div class="metric-card"><div class="metric-value">{{ hvResult.transformer_capacity_mva }}MVA</div><div class="metric-label">变压器容量</div></div>
            <div class="metric-card"><div class="metric-value">{{ hvResult.transformer_ratio }}</div><div class="metric-label">变比</div></div>
            <div class="metric-card"><div class="metric-value">{{ hvResult.mv_breaker_rating_ka }}kA</div><div class="metric-label">断路器额定值</div></div>
          </div>
          <div v-if="hvResult.protection_scheme" class="info-box">
            <div class="text-sm font-bold mb-2 section-title">保护配置</div>
            <div class="grid grid-cols-2 md:grid-cols-5 gap-2">
              <div v-for="prot in hvResult.protection_scheme" :key="prot.name" class="protection-item">
                <div class="font-bold">{{ prot.name }}</div>
                <div style="color: #999;">{{ prot.type }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- P1-4: 投标文档 -->
    <div v-show="activeModule === 'bidDoc'" class="epc-panel space-y-4">
      <div class="panel-card">
        <h3 class="panel-title">投标文档生成</h3>
        <div class="flex gap-4 mb-4">
          <select v-model="bidForm.template" class="form-input" style="max-width: 300px;">
            <option value="technical_proposal">技术方案</option>
          </select>
          <button @click="generateBidDoc" :disabled="loading" class="btn-primary">
            {{ loading ? '生成中...' : '生成投标文档' }}
          </button>
        </div>

        <div v-if="bidResult" class="mt-4">
          <div v-for="chapter in bidResult.chapters" :key="chapter.num" class="mb-4">
            <div class="chapter-title">{{ chapter.num }}. {{ chapter.title }}</div>
            <div v-for="sec in chapter.sections" :key="sec.num" class="section-item">
              <div class="font-medium text-sm">{{ sec.num }} {{ sec.title }}</div>
              <div class="text-xs mt-1 whitespace-pre-line" style="color: #666;">{{ sec.content }}</div>
              <div class="text-xs mt-1" style="color: #999;">数据来源: {{ sec.data_source }}</div>
            </div>
          </div>
        </div>

        <!-- 交互式图表预览 -->
        <div class="mt-6 pt-4 border-top">
          <div class="flex items-center justify-between mb-3">
            <h4 class="text-base font-bold section-title">交互式图表预览</h4>
            <span class="text-xs" style="color: #999;">基于 Plotly，支持缩放/悬停/导出</span>
          </div>
          <div class="flex flex-wrap gap-2 mb-3">
            <button v-for="c in chartTypes" :key="c.id" @click="previewChart(c.id)" :disabled="chartLoading === c.id" class="chart-btn" :class="{ active: activeChart === c.id }">
              {{ chartLoading === c.id ? '加载中...' : c.label }}
            </button>
          </div>
          <div v-if="chartError" class="text-xs p-2 rounded mb-3 error-box">{{ chartError }}</div>
          <div v-if="chartHtml" ref="chartContainer" class="border rounded-lg p-2 chart-container" v-html="chartHtml"></div>
          <div v-else-if="!chartLoading" class="text-xs text-center py-8 empty-state">
            点击上方按钮选择图表类型，预览投标方案交互式可视化
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

const emit = defineEmits(['error'])

const loading = ref(false)
const activeModule = ref('architecture')

// SVG icons matching Sidebar style
const icons = {
  architecture: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>`,
  gridCompliance: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 1v6m0 6v6m11-7h-6m-6 0H1m16.66-5.66l-4.24 4.24M6.58 17.42l-4.24 4.24m0-13.32l4.24 4.24m10.82 10.82l4.24 4.24"/></svg>`,
  safety: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>`,
  ipp: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>`,
  matrix: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="15" y1="3" x2="15" y2="21"/></svg>`,
  thermal: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/></svg>`,
  scada: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12h5m5 0h5m5 0h5"/><path d="M7 7l5 5 5-5"/><path d="M7 17l5-5 5 5"/></svg>`,
  hv: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>`,
  bidDoc: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>`,
}

const tabs = [
  { id: 'architecture', label: '系统架构', priority: 'P0-3', svg: icons.architecture },
  { id: 'gridCompliance', label: '电网合规', priority: 'P0-1', svg: icons.gridCompliance },
  { id: 'safety', label: '安全消防', priority: 'P0-2', svg: icons.safety },
  { id: 'ipp', label: 'IPP财务', priority: 'P0-4', svg: icons.ipp },
  { id: 'matrix', label: '合规矩阵', priority: 'P0-5', svg: icons.matrix },
  { id: 'thermal', label: '热管理', priority: 'P1-1', svg: icons.thermal },
  { id: 'scada', label: 'SCADA/EMS', priority: 'P1-2', svg: icons.scada },
  { id: 'hv', label: '高压接入', priority: 'P1-3', svg: icons.hv },
  { id: 'bidDoc', label: '投标文档', priority: 'P1-4', svg: icons.bidDoc },
]

const gridStandards = ref([])

// Form data
const archForm = reactive({ total_power_mw: 100, total_energy_mwh: 200, architecture_type: 'central', coupling_type: 'AC', cell_voltage: 3.2, cell_capacity: 280, pcs_power_mw: 3.45, pcs_max_dc_voltage: 1500 })
const gcForm = reactive({ grid_standard: 'UAE_S_5010', grid_voltage_kv: 33, grid_frequency_hz: 50, pcs_count: 10, pcs_power_mw: 3.45 })
const sfForm = reactive({ system_capacity_mwh: 100, container_count: 20, chemistry_type: 'LFP', suppression_type: 'Novec1230' })
const ippForm = reactive({ project_life_years: 25, total_capex_usd: 500000000, capacity_mw: 100, energy_mwh: 200, capacity_price_usd_kw_month: 8.0, energy_price_usd_kwh: 0.05, ppa_escalation_rate: 0.02, debt_ratio: 0.7, debt_interest_rate: 0.05, debt_tenor_years: 15, annual_opex_usd: 5000000, availability_guarantee: 0.98 })
const matrixForm = reactive({ template: 'UAE_DEWA_VII_BESS' })
const tmForm = reactive({ ambient_max_c: 45, cell_capacity_ah: 280, c_rate: 0.5, cooling_type: 'liquid' })
const seForm = reactive({ container_count: 20, pcs_count: 10, communication_protocol: 'IEC_61850', dispatch_strategy: 'peak_shaving' })
const hvForm = reactive({ total_power_mw: 100, poc_voltage_kv: 33, short_circuit_capacity_mva: 500, poc_type: 'substation' })
const bidForm = reactive({ template: 'technical_proposal' })

// Results
const archResult = ref(null)
const gcResult = ref(null)
const sfResult = ref(null)
const ippResult = ref(null)
const matrixResult = ref(null)
const tmResult = ref(null)
const seResult = ref(null)
const hvResult = ref(null)
const bidResult = ref(null)

async function apiCall(url, body) {
  loading.value = true
  try {
    const resp = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
    const result = await resp.json()
    if (result.success) {
      return result.data
    } else {
      emit('error', result.error || '操作失败')
      return null
    }
  } catch (e) {
    emit('error', '网络错误: ' + e.message)
    return null
  } finally {
    loading.value = false
  }
}

async function designArchitecture() {
  const data = await apiCall('/api/system-architecture/design', archForm)
  if (data) archResult.value = data
}

async function loadStandards() {
  try {
    const resp = await fetch('/api/grid-compliance/standards')
    gridStandards.value = await resp.json()
  } catch (e) { /* ignore */ }
}

async function analyzeGridCompliance() {
  const data = await apiCall('/api/grid-compliance/analyze', gcForm)
  if (data) gcResult.value = data
}

async function analyzeSafety() {
  const data = await apiCall('/api/safety-design/analyze', sfForm)
  if (data) sfResult.value = data
}

async function calculateIPP() {
  const data = await apiCall('/api/ipp-financial/calculate', ippForm)
  if (data) ippResult.value = data
}

async function generateMatrix() {
  const data = await apiCall('/api/compliance-matrix/generate', matrixForm)
  if (data) matrixResult.value = data
}

async function calculateThermal() {
  const data = await apiCall('/api/thermal-management/calculate', { ...tmForm, cells_per_container: 5000 })
  if (data) tmResult.value = data
}

async function designScada() {
  const data = await apiCall('/api/scada-ems/design', seForm)
  if (data) seResult.value = data
}

async function designHV() {
  const data = await apiCall('/api/hv-interconnection/design', hvForm)
  if (data) hvResult.value = data
}

async function generateBidDoc() {
  const data = await apiCall('/api/bid-document/generate', bidForm)
  if (data) bidResult.value = data
}

// Chart preview
const chartTypes = [
  { id: 'soh_rte_curve', label: 'SOH/RTE 衰减曲线' },
  { id: 'capacity_matrix', label: '容量矩阵热力图' },
  { id: 'grid_compliance', label: 'LVRT/HVRT 曲线' },
  { id: 'ipp_cashflow', label: 'IPP 现金流瀑布图' },
]
const chartHtml = ref('')
const chartLoading = ref('')
const chartError = ref('')
const activeChart = ref('')
const chartContainer = ref(null)

async function previewChart(chartType) {
  chartLoading.value = chartType
  chartError.value = ''
  chartHtml.value = ''
  try {
    const body = { ...bidForm, chart_type: chartType }
    if (bidResult.value) {
      body.bid_data = bidResult.value
    }
    const resp = await fetch(`/api/report/charts/${chartType}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
    const result = await resp.json()
    if (result.success) {
      chartHtml.value = result.html
      activeChart.value = chartType
    } else {
      chartError.value = result.error || '图表生成失败'
    }
  } catch (e) {
    chartError.value = '网络错误: ' + e.message
  } finally {
    chartLoading.value = ''
  }
}

function formatNum(n) {
  if (!n) return '0'
  if (Math.abs(n) >= 1e9) return (n / 1e9).toFixed(2) + 'B'
  if (Math.abs(n) >= 1e6) return (n / 1e6).toFixed(1) + 'M'
  if (Math.abs(n) >= 1e3) return (n / 1e3).toFixed(1) + 'K'
  return n.toFixed(0)
}

function statusLabel(status) {
  const map = { compliant: '合规', 'non_compliant': '不合规', partial: '部分合规', 'N/A': '待确认' }
  return map[status] || status
}

function statusClass(status) {
  const map = { compliant: 'pass', 'non_compliant': 'fail', partial: 'warn', 'N/A': 'neutral' }
  return map[status] || 'neutral'
}

function getDeratingColor(pct) {
  if (pct > 80) return '#10B981'
  if (pct > 50) return '#F59E0B'
  return '#EF4444'
}

onMounted(() => {
  loadStandards()
})
</script>

<style scoped>
.epc-page { padding: 24px; }

.epc-header { margin-bottom: 24px; }
.epc-header h1 { font-size: 24px; font-weight: 700; margin: 0 0 8px; }
.epc-desc { color: var(--text-secondary, #666); font-size: 14px; margin: 0; }

/* Tab navigation */
.epc-tabs {
  display: flex;
  gap: 4px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  border-bottom: 1px solid #E0E0E0;
  padding-bottom: 0;
}

.epc-tabs button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border: 1px solid var(--border, #ddd);
  border-radius: 6px;
  border-bottom: none;
  background: var(--bg, #fff);
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
  color: #666;
  position: relative;
  top: 1px;
}

.epc-tabs button.active {
  background: #fff;
  color: #0071e3;
  border-color: #0071e3;
  font-weight: 500;
  border-bottom: 1px solid #fff;
}

.tab-icon {
  width: 16px;
  height: 16px;
  opacity: 0.7;
}

.tab-label {
  font-size: 13px;
}

.tab-priority {
  font-size: 10px;
  padding: 1px 5px;
  border-radius: 3px;
  font-weight: 600;
  margin-left: 2px;
}

.pri-P0-1 { background: #D1FAE5; color: #065F46; }
.pri-P0-2 { background: #DBEAFE; color: #1E40AF; }
.pri-P0-3 { background: #E0E7FF; color: #3730A3; }
.pri-P0-4 { background: #FEF3C7; color: #92400E; }
.pri-P0-5 { background: #F3E8FF; color: #6B21A8; }
.pri-P1-1 { background: #F0F0F0; color: #666; }
.pri-P1-2 { background: #F0F0F0; color: #666; }
.pri-P1-3 { background: #F0F0F0; color: #666; }
.pri-P1-4 { background: #F0F0F0; color: #666; }

/* Panel card */
.panel-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #E0E0E0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.panel-title {
  font-size: 16px;
  font-weight: 700;
  margin: 0 0 16px;
  color: #0071e3;
}

.section-title {
  color: #666;
  font-size: 14px;
}

/* Form inputs */
.field-label {
  color: #999;
}

.form-input {
  width: 100%;
  padding: 6px 10px;
  border: 1px solid #D1D5DB;
  border-radius: 6px;
  font-size: 13px;
  outline: none;
  transition: border-color 0.15s;
}

.form-input:focus {
  border-color: #0071e3;
  box-shadow: 0 0 0 2px rgba(0,113,227,0.1);
}

/* Buttons */
.btn-primary {
  padding: 8px 24px;
  border-radius: 8px;
  background: #0071e3;
  color: #fff;
  border: none;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-primary:hover { background: #005bb5; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }

/* Metric cards */
.metric-card {
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  padding: 12px;
  text-align: center;
}

.metric-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #333;
}

.metric-label {
  font-size: 0.75rem;
  color: #999;
  margin-top: 2px;
}

.primary-text { color: #0071e3 !important; }
.pass-text { color: #10B981 !important; }
.fail-text { color: #EF4444 !important; }
.warn-text { color: #F59E0B !important; }

/* Stage cards */
.stage-card {
  background: #EFF6FF;
  border-radius: 8px;
  padding: 12px;
  border: 1px solid #BFDBFE;
}

/* Banners */
.pass-banner {
  background: #D1FAE5;
  border-radius: 8px;
}

.fail-banner {
  background: #FEE2E2;
  border-radius: 8px;
}

.status-icon {
  font-size: 24px;
  font-weight: 700;
}

/* Data table */
.data-table {
  border-collapse: collapse;
}

.header-cell {
  background: #F5F7FA;
  font-weight: 600;
  color: #333;
}

.border-row {
  border-bottom: 1px solid #E0E0E0;
}

.status-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.pass { background: #D1FAE5; color: #065F46; }
.status-badge.fail { background: #FEE2E2; color: #991B1B; }
.status-badge.warn { background: #FEF3C7; color: #92400E; }
.status-badge.neutral { background: #F3F4F6; color: #6B7280; }

/* Derating chart */
.derating-chart {
  background: #F9FAFB;
  border-radius: 8px;
  padding: 8px;
  border: 1px solid #E5E7EB;
}

.derating-bar {
  min-height: 4px;
  transition: height 0.3s;
}

/* Info box */
.info-box {
  background: #F9FAFB;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #E5E7EB;
}

.info-list div {
  color: #666;
}

/* Protection items */
.protection-item {
  background: #fff;
  border-radius: 6px;
  padding: 8px;
  border: 1px solid #E0E0E0;
  font-size: 12px;
}

/* Chapter / section */
.chapter-title {
  background: #E8EEF5;
  color: #0071e3;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 8px;
}

.section-item {
  margin-left: 16px;
  padding: 12px;
  background: #F9FAFB;
  border-radius: 6px;
  margin-bottom: 8px;
}

/* Chart buttons */
.chart-btn {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  border: 1px solid #0071e3;
  background: #fff;
  color: #0071e3;
  cursor: pointer;
  transition: all 0.15s;
}

.chart-btn:hover { background: #EFF6FF; }

.chart-btn.active {
  background: #0071e3;
  color: #fff;
}

.chart-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Chart container */
.chart-container {
  border: 1px solid #E0E0E0;
  border-radius: 8px;
  background: #fff;
  min-height: 300px;
}

/* Error box */
.error-box {
  background: #FEF2F2;
  color: #DC2626;
  border-radius: 6px;
}

/* Empty state */
.empty-state {
  color: #999;
}

/* Border top */
.border-top {
  border-top: 1px solid #E0E0E0;
}

.space-y-4 > * + * {
  margin-top: 16px;
}
</style>
