<template>
  <div class="epc-page">
    <div class="epc-header">
      <h1>EPC 工程化模块</h1>
      <p class="epc-desc">
        系统架构设计、电网合规分析、安全消防、IPP财务、合规矩阵、热管理、SCADA/EMS、高压接入、投标文档
      </p>
    </div>

    <!-- 模块标签页 -->
    <div class="epc-tabs">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        :class="{ active: activeModule === tab.id }"
        @click="activeModule = tab.id"
      >
        <AppIcon :name="tab.iconName" :size="18" class="tab-icon" />
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
            <input v-model.number="archForm.total_power_mw" type="number" class="form-field-input" placeholder="1400" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">系统能量 (MWh)</label>
            <input
              v-model.number="archForm.total_energy_mwh"
              type="number"
              class="form-field-input"
              placeholder="8400"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">架构类型</label>
            <select v-model="archForm.architecture_type" class="form-field-select">
              <option value="central">集中式</option>
              <option value="string">组串式</option>
              <option value="hybrid">混合式</option>
            </select>
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">耦合方式</label>
            <select v-model="archForm.coupling_type" class="form-field-select">
              <option value="AC">AC耦合</option>
              <option value="DC">DC耦合</option>
              <option value="hybrid">混合耦合</option>
            </select>
          </div>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-xs mb-1 field-label">电芯电压 (V)</label>
            <input
              v-model.number="archForm.cell_voltage"
              type="number"
              step="0.1"
              class="form-field-input"
              placeholder="3.2"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">电芯容量 (Ah)</label>
            <input v-model.number="archForm.cell_capacity" type="number" class="form-field-input" placeholder="280" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">PCS功率 (MW)</label>
            <input
              v-model.number="archForm.pcs_power_mw"
              type="number"
              step="0.01"
              class="form-field-input"
              placeholder="3.45"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">PCS最大DC电压 (V)</label>
            <input
              v-model.number="archForm.pcs_max_dc_voltage"
              type="number"
              class="form-field-input"
              placeholder="1500"
            />
          </div>
        </div>
        <button :disabled="loading" class="btn-primary" @click="designArchitecture">
          {{ loading ? '计算中...' : '执行架构设计' }}
        </button>

        <div v-if="archResult" class="mt-6 space-y-4">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
            <div v-for="item in archResult.topology_data.levels" :key="item.name" class="metric-card">
              <div class="metric-value">
                {{ item.count }}
              </div>
              <div class="metric-label">{{ item.name }} ({{ item.unit }})</div>
            </div>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
            <div class="metric-card">
              <div class="metric-value">
                {{ archResult.pcs_count }}
              </div>
              <div class="metric-label">PCS总数</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">{{ archResult.dc_bus_voltage }}V</div>
              <div class="metric-label">DC母线电压</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">
                {{ archResult.total_containers }}
              </div>
              <div class="metric-label">集装箱总数</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">
                {{ archResult.stage_count }}
              </div>
              <div class="metric-label">分期数</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">{{ archResult.duration_hours }}h</div>
              <div class="metric-label">储能时长</div>
            </div>
          </div>
          <div v-if="archResult.stages" class="mt-4">
            <h4 class="text-sm font-bold mb-2 section-title">分期建设方案</h4>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
              <div v-for="stage in archResult.stages" :key="stage.stage" class="stage-card">
                <div class="font-bold text-sm stage-title">{{ stage.stage }}期</div>
                <div class="text-xs tx-muted-dark">{{ stage.power_mw }}MW / {{ stage.energy_mwh }}MWh</div>
                <div class="text-xs tx-muted">
                  {{ stage.estimated_date }}
                </div>
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
            <select v-model="gcForm.grid_standard" class="form-field-select">
              <option v-for="s in gridStandards" :key="s.code" :value="s.code">
                {{ s.name }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">并网点电压 (kV)</label>
            <input v-model.number="gcForm.grid_voltage_kv" type="number" class="form-field-input" placeholder="33" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">电网频率 (Hz)</label>
            <input
              v-model.number="gcForm.grid_frequency_hz"
              type="number"
              step="0.01"
              class="form-field-input"
              placeholder="50"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">PCS数量</label>
            <input v-model.number="gcForm.pcs_count" type="number" class="form-field-input" placeholder="10" />
          </div>
        </div>
        <button :disabled="loading" class="btn-primary" @click="analyzeGridCompliance">
          {{ loading ? '分析中...' : '执行合规分析' }}
        </button>

        <div v-if="gcResult" class="mt-6 space-y-4">
          <div
            class="flex items-center gap-4 p-4 rounded-lg"
            :class="gcResult.overall_pass ? 'pass-banner' : 'fail-banner'"
          >
            <span class="status-icon">{{ gcResult.overall_pass ? 'pass' : 'fail' }}</span>
            <div>
              <div class="font-bold" :class="gcResult.overall_pass ? 'pass-text' : 'fail-text'">
                {{ gcResult.overall_pass ? '全部合规' : '存在不合规项' }}
              </div>
              <div v-if="gcResult.failed_items.length" class="text-xs tx-muted-dark">
                不合规: {{ gcResult.failed_items.join(', ') }}
              </div>
            </div>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="metric-card">
              <div class="metric-value" :class="gcResult.lvrt_pass ? 'pass-text' : 'fail-text'">
                {{ gcResult.lvrt_pass ? 'PASS' : 'FAIL' }}
              </div>
              <div class="metric-label">LVRT低电压穿越</div>
            </div>
            <div class="metric-card">
              <div class="metric-value" :class="gcResult.hvrt_pass ? 'pass-text' : 'fail-text'">
                {{ gcResult.hvrt_pass ? 'PASS' : 'FAIL' }}
              </div>
              <div class="metric-label">HVRT高电压穿越</div>
            </div>
            <div class="metric-card">
              <div class="metric-value" :class="gcResult.freq_response_pass ? 'pass-text' : 'fail-text'">
                {{ gcResult.freq_response_pass ? 'PASS' : 'FAIL' }}
              </div>
              <div class="metric-label">频率响应</div>
            </div>
            <div class="metric-card">
              <div class="metric-value" :class="gcResult.reactive_pass ? 'pass-text' : 'fail-text'">
                {{ gcResult.reactive_pass ? 'PASS' : 'FAIL' }}
              </div>
              <div class="metric-label">无功功率 ({{ gcResult.reactive_capacity_mvar }}MVar)</div>
            </div>
            <div class="metric-card">
              <div class="metric-value" :class="gcResult.power_quality_pass ? 'pass-text' : 'fail-text'">
                {{ gcResult.thd }}%
              </div>
              <div class="metric-label">THD (限值5%)</div>
            </div>
            <div class="metric-card">
              <div class="metric-value" :class="gcResult.anti_islanding_pass ? 'pass-text' : 'fail-text'">
                {{ gcResult.anti_islanding_time_s }}s
              </div>
              <div class="metric-label">防孤岛 (限值2s)</div>
            </div>
            <div class="metric-card">
              <div class="metric-value" :class="gcResult.comm_pass ? 'pass-text' : 'fail-text'">
                {{ gcResult.comm_pass ? 'PASS' : 'FAIL' }}
              </div>
              <div class="metric-label">通信合规</div>
            </div>
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
            <input
              v-model.number="sfForm.system_capacity_mwh"
              type="number"
              class="form-field-input"
              placeholder="100"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">集装箱数量</label>
            <input v-model.number="sfForm.container_count" type="number" class="form-field-input" placeholder="20" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">化学体系</label>
            <select v-model="sfForm.chemistry_type" class="form-field-select">
              <option value="LFP">LFP (磷酸铁锂)</option>
              <option value="NCM">NCM (三元)</option>
              <option value="NCA">NCA</option>
              <option value="LTO">LTO (钛酸锂)</option>
            </select>
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">灭火系统</label>
            <select v-model="sfForm.suppression_type" class="form-field-select">
              <option value="Novec1230">Novec 1230</option>
              <option value="Aerosol">气溶胶</option>
              <option value="Water-mist">细水雾</option>
            </select>
          </div>
        </div>
        <button :disabled="loading" class="btn-primary" @click="analyzeSafety">
          {{ loading ? '分析中...' : '执行安全分析' }}
        </button>

        <div v-if="sfResult" class="mt-6 space-y-4">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="metric-card">
              <div class="metric-value">
                {{ sfResult.zone_count }}
              </div>
              <div class="metric-label">防火分区数</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">{{ sfResult.container_spacing_m }}m</div>
              <div class="metric-label">集装箱间距</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">{{ sfResult.thermal_runaway_temp_c }}°C</div>
              <div class="metric-label">热失控温度</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">{{ sfResult.propagation_time_min }}min</div>
              <div class="metric-label">蔓延时间</div>
            </div>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="metric-card">
              <div class="metric-value" :class="sfResult.ul_9540a_pass ? 'pass-text' : 'fail-text'">
                {{ sfResult.ul_9540a_pass ? 'PASS' : 'FAIL' }}
              </div>
              <div class="metric-label">UL 9540A</div>
            </div>
            <div class="metric-card">
              <div class="metric-value" :class="sfResult.nfpa_855_pass ? 'pass-text' : 'fail-text'">
                {{ sfResult.nfpa_855_pass ? 'PASS' : 'FAIL' }}
              </div>
              <div class="metric-label">NFPA 855</div>
            </div>
            <div class="metric-card">
              <div class="metric-value" :class="sfResult.iec_62619_pass ? 'pass-text' : 'fail-text'">
                {{ sfResult.iec_62619_pass ? 'PASS' : 'FAIL' }}
              </div>
              <div class="metric-label">IEC 62619</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">{{ sfResult.suppression_capacity_kg }}kg</div>
              <div class="metric-label">灭火剂容量</div>
            </div>
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
            <input
              v-model.number="ippForm.project_life_years"
              type="number"
              class="form-field-input"
              placeholder="25"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">总CAPEX (USD)</label>
            <input
              v-model.number="ippForm.total_capex_usd"
              type="number"
              class="form-field-input"
              placeholder="500000000"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">容量 (MW)</label>
            <input v-model.number="ippForm.capacity_mw" type="number" class="form-field-input" placeholder="100" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">能量 (MWh)</label>
            <input v-model.number="ippForm.energy_mwh" type="number" class="form-field-input" placeholder="200" />
          </div>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-xs mb-1 field-label">容量价格 ($/kW/月)</label>
            <input
              v-model.number="ippForm.capacity_price_usd_kw_month"
              type="number"
              step="0.1"
              class="form-field-input"
              placeholder="8.0"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">电量价格 ($/kWh)</label>
            <input
              v-model.number="ippForm.energy_price_usd_kwh"
              type="number"
              step="0.01"
              class="form-field-input"
              placeholder="0.05"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">PPA递增率</label>
            <input
              v-model.number="ippForm.ppa_escalation_rate"
              type="number"
              step="0.01"
              class="form-field-input"
              placeholder="0.02"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">贷款比例</label>
            <input
              v-model.number="ippForm.debt_ratio"
              type="number"
              step="0.05"
              class="form-field-input"
              placeholder="0.7"
            />
          </div>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-xs mb-1 field-label">贷款利率</label>
            <input
              v-model.number="ippForm.debt_interest_rate"
              type="number"
              step="0.01"
              class="form-field-input"
              placeholder="0.05"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">贷款期限 (年)</label>
            <input v-model.number="ippForm.debt_tenor_years" type="number" class="form-field-input" placeholder="15" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">年OPEX (USD)</label>
            <input
              v-model.number="ippForm.annual_opex_usd"
              type="number"
              class="form-field-input"
              placeholder="5000000"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">可用率保证</label>
            <input
              v-model.number="ippForm.availability_guarantee"
              type="number"
              step="0.01"
              class="form-field-input"
              placeholder="0.98"
            />
          </div>
        </div>
        <button :disabled="loading" class="btn-primary" @click="calculateIPP">
          {{ loading ? '计算中...' : '执行财务计算' }}
        </button>

        <div v-if="ippResult" class="mt-6 space-y-4">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="metric-card">
              <div class="metric-value primary-text">${{ formatNum(ippResult.npv_usd) }}</div>
              <div class="metric-label">NPV</div>
            </div>
            <div class="metric-card">
              <div class="metric-value primary-text">{{ ippResult.irr }}%</div>
              <div class="metric-label">项目IRR</div>
            </div>
            <div class="metric-card">
              <div class="metric-value primary-text">{{ ippResult.equity_irr }}%</div>
              <div class="metric-label">股权IRR</div>
            </div>
            <div class="metric-card">
              <div class="metric-value primary-text">${{ ippResult.lcoe_usd_kwh }}/kWh</div>
              <div class="metric-label">LCOE</div>
            </div>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
            <div class="metric-card">
              <div class="metric-value">
                {{ ippResult.dscr_avg }}
              </div>
              <div class="metric-label">平均DSCR</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">
                {{ ippResult.dscr_min }}
              </div>
              <div class="metric-label">最小DSCR</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">{{ ippResult.payback_years }}年</div>
              <div class="metric-label">回收期</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- P0-5: 合规矩阵 -->
    <div v-show="activeModule === 'matrix'" class="epc-panel space-y-4">
      <div class="panel-card">
        <h3 class="panel-title">合规矩阵生成</h3>
        <div class="flex gap-4 mb-4">
          <select v-model="matrixForm.template" class="form-field-select max-w-sm">
            <option value="UAE_DEWA_VII_BESS">UAE DEWA VII BESS RFP</option>
          </select>
          <button :disabled="loading" class="btn-primary" @click="generateMatrix">
            {{ loading ? '生成中...' : '生成合规矩阵' }}
          </button>
        </div>

        <div v-if="matrixResult" class="mt-4">
          <div class="grid grid-cols-4 gap-3 mb-4">
            <div class="metric-card">
              <div class="metric-value">
                {{ matrixResult.total }}
              </div>
              <div class="metric-label">总条款</div>
            </div>
            <div class="metric-card">
              <div class="metric-value pass-text">
                {{ matrixResult.compliant }}
              </div>
              <div class="metric-label">合规</div>
            </div>
            <div class="metric-card">
              <div class="metric-value fail-text">
                {{ matrixResult.non_compliant }}
              </div>
              <div class="metric-label">不合规</div>
            </div>
            <div class="metric-card">
              <div class="metric-value warn-text">
                {{ matrixResult.partial }}
              </div>
              <div class="metric-label">部分合规</div>
            </div>
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
                  <td class="px-3 py-2 font-mono text-xs">
                    {{ item.section }}
                  </td>
                  <td class="px-3 py-2">
                    {{ item.requirement }}
                  </td>
                  <td class="px-3 py-2 text-xs tx-muted">
                    {{ item.category }}
                  </td>
                  <td class="px-3 py-2">
                    <span class="status-badge" :class="statusClass(item.compliance_status)">
                      {{ statusLabel(item.compliance_status) }}
                    </span>
                  </td>
                  <td class="px-3 py-2 text-xs tx-muted-dark">
                    {{ item.response }}
                  </td>
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
            <input v-model.number="tmForm.ambient_max_c" type="number" class="form-field-input" placeholder="45" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">电芯容量 (Ah)</label>
            <input v-model.number="tmForm.cell_capacity_ah" type="number" class="form-field-input" placeholder="280" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">充放电倍率 (C)</label>
            <input v-model.number="tmForm.c_rate" type="number" step="0.1" class="form-field-input" placeholder="0.5" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">冷却方式</label>
            <select v-model="tmForm.cooling_type" class="form-field-select">
              <option value="liquid">液冷</option>
              <option value="air">风冷</option>
            </select>
          </div>
        </div>
        <button :disabled="loading" class="btn-primary" @click="calculateThermal">
          {{ loading ? '计算中...' : '执行热管理计算' }}
        </button>

        <div v-if="tmResult" class="mt-6 space-y-4">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="metric-card">
              <div class="metric-value">{{ tmResult.cooling_power_kw }}kW</div>
              <div class="metric-label">制冷功率</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">{{ tmResult.coolant_flow_rate_lpm }}L/min</div>
              <div class="metric-label">冷却液流量</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">{{ tmResult.max_cell_temp_c }}°C</div>
              <div class="metric-label">最高电芯温度</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">{{ formatNum(tmResult.annual_cooling_energy_kwh) }}kWh</div>
              <div class="metric-label">年制冷能耗</div>
            </div>
          </div>
          <div v-if="tmResult.derating_curve" class="mt-4">
            <h4 class="text-sm font-bold mb-2 section-title">高温降额曲线</h4>
            <div class="flex gap-1 items-end h-32 derating-chart">
              <div v-for="point in tmResult.derating_curve" :key="point.temp" class="flex-1 flex flex-col items-center">
                <div
                  class="w-full rounded-t derating-bar"
                  :style="{ height: point.power_pct + '%', backgroundColor: getDeratingColor(point.power_pct) }"
                />
                <div class="text-xs mt-1 tx-muted">{{ point.temp }}°C</div>
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
            <input v-model.number="seForm.container_count" type="number" class="form-field-input" placeholder="20" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">PCS数量</label>
            <input v-model.number="seForm.pcs_count" type="number" class="form-field-input" placeholder="10" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">通信协议</label>
            <select v-model="seForm.communication_protocol" class="form-field-select">
              <option value="IEC_61850">IEC 61850</option>
              <option value="Modbus_TCP">Modbus TCP</option>
              <option value="DNP3">DNP3</option>
            </select>
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">调度策略</label>
            <select v-model="seForm.dispatch_strategy" class="form-field-select">
              <option value="peak_shaving">削峰填谷</option>
              <option value="arbitrage">套利</option>
              <option value="frequency_regulation">调频</option>
            </select>
          </div>
        </div>
        <button :disabled="loading" class="btn-primary" @click="designScada">
          {{ loading ? '设计中...' : '执行SCADA设计' }}
        </button>

        <div v-if="seResult" class="mt-6 space-y-4">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="metric-card">
              <div class="metric-value">
                {{ seResult.total_data_points }}
              </div>
              <div class="metric-label">总数据点</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">
                {{ seResult.analog_points }}
              </div>
              <div class="metric-label">模拟量</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">
                {{ seResult.digital_points }}
              </div>
              <div class="metric-label">数字量</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">
                {{ seResult.control_points }}
              </div>
              <div class="metric-label">控制点</div>
            </div>
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
            <input v-model.number="hvForm.total_power_mw" type="number" class="form-field-input" placeholder="100" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">并网点电压 (kV)</label>
            <input v-model.number="hvForm.poc_voltage_kv" type="number" class="form-field-input" placeholder="33" />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">短路容量 (MVA)</label>
            <input
              v-model.number="hvForm.short_circuit_capacity_mva"
              type="number"
              class="form-field-input"
              placeholder="500"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 field-label">并网点类型</label>
            <select v-model="hvForm.poc_type" class="form-field-select">
              <option value="substation">变电站</option>
              <option value="overhead_line">架空线</option>
              <option value="cable">电缆</option>
            </select>
          </div>
        </div>
        <button :disabled="loading" class="btn-primary" @click="designHV">
          {{ loading ? '设计中...' : '执行高压接入设计' }}
        </button>

        <div v-if="hvResult" class="mt-6 space-y-4">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="metric-card">
              <div class="metric-value">
                {{ hvResult.transformer_count }}
              </div>
              <div class="metric-label">变压器数量</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">{{ hvResult.transformer_capacity_mva }}MVA</div>
              <div class="metric-label">变压器容量</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">
                {{ hvResult.transformer_ratio }}
              </div>
              <div class="metric-label">变比</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">{{ hvResult.mv_breaker_rating_ka }}kA</div>
              <div class="metric-label">断路器额定值</div>
            </div>
          </div>
          <div v-if="hvResult.protection_scheme" class="info-box">
            <div class="text-sm font-bold mb-2 section-title">保护配置</div>
            <div class="grid grid-cols-2 md:grid-cols-5 gap-2">
              <div v-for="prot in hvResult.protection_scheme" :key="prot.name" class="protection-item">
                <div class="font-bold">
                  {{ prot.name }}
                </div>
                <div class="tx-muted">
                  {{ prot.type }}
                </div>
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
          <select v-model="bidForm.template" class="form-field-select max-w-sm">
            <option value="technical_proposal">技术方案</option>
          </select>
          <button :disabled="loading" class="btn-primary" @click="generateBidDoc">
            {{ loading ? '生成中...' : '生成投标文档' }}
          </button>
        </div>

        <div v-if="bidResult" class="mt-4">
          <div v-for="chapter in bidResult.chapters" :key="chapter.num" class="mb-4">
            <div class="chapter-title">{{ chapter.num }}. {{ chapter.title }}</div>
            <div v-for="sec in chapter.sections" :key="sec.num" class="section-item">
              <div class="font-medium text-sm">{{ sec.num }} {{ sec.title }}</div>
              <div class="text-xs mt-1 whitespace-pre-line tx-muted-dark">
                {{ sec.content }}
              </div>
              <div class="text-xs mt-1 tx-muted">数据来源: {{ sec.data_source }}</div>
            </div>
          </div>
        </div>

        <!-- 交互式图表预览 -->
        <div class="mt-6 pt-4 border-top">
          <div class="flex items-center justify-between mb-3">
            <h4 class="text-base font-bold section-title">交互式图表预览</h4>
            <span class="text-xs tx-muted">基于 Plotly，支持缩放/悬停/导出</span>
          </div>
          <div class="flex flex-wrap gap-2 mb-3">
            <button
              v-for="c in chartTypes"
              :key="c.id"
              :disabled="chartLoading === c.id"
              class="chart-btn"
              :class="{ active: activeChart === c.id }"
              @click="previewChart(c.id)"
            >
              {{ chartLoading === c.id ? '加载中...' : c.label }}
            </button>
          </div>
          <div v-if="chartError" class="text-xs p-2 rounded mb-3 error-box">
            {{ chartError }}
          </div>
          <div v-if="chartHtml" ref="chartContainer" class="border rounded-lg p-2 chart-container" v-html="chartHtml" />
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

const tabs = [
  { id: 'architecture', label: '系统架构', priority: 'P0-3', iconName: 'home' },
  { id: 'gridCompliance', label: '电网合规', priority: 'P0-1', iconName: 'target' },
  { id: 'safety', label: '安全消防', priority: 'P0-2', iconName: 'shield' },
  { id: 'ipp', label: 'IPP财务', priority: 'P0-4', iconName: 'dollar' },
  { id: 'matrix', label: '合规矩阵', priority: 'P0-5', iconName: 'grid' },
  { id: 'thermal', label: '热管理', priority: 'P1-1', iconName: 'thermometer' },
  { id: 'scada', label: 'SCADA/EMS', priority: 'P1-2', iconName: 'data-flow' },
  { id: 'hv', label: '高压接入', priority: 'P1-3', iconName: 'lightning' },
  { id: 'bidDoc', label: '投标文档', priority: 'P1-4', iconName: 'document' }
]

const gridStandards = ref([])

// Form data
const archForm = reactive({
  total_power_mw: 100,
  total_energy_mwh: 200,
  architecture_type: 'central',
  coupling_type: 'AC',
  cell_voltage: 3.2,
  cell_capacity: 280,
  pcs_power_mw: 3.45,
  pcs_max_dc_voltage: 1500
})
const gcForm = reactive({
  grid_standard: 'UAE_S_5010',
  grid_voltage_kv: 33,
  grid_frequency_hz: 50,
  pcs_count: 10,
  pcs_power_mw: 3.45
})
const sfForm = reactive({
  system_capacity_mwh: 100,
  container_count: 20,
  chemistry_type: 'LFP',
  suppression_type: 'Novec1230'
})
const ippForm = reactive({
  project_life_years: 25,
  total_capex_usd: 500000000,
  capacity_mw: 100,
  energy_mwh: 200,
  capacity_price_usd_kw_month: 8.0,
  energy_price_usd_kwh: 0.05,
  ppa_escalation_rate: 0.02,
  debt_ratio: 0.7,
  debt_interest_rate: 0.05,
  debt_tenor_years: 15,
  annual_opex_usd: 5000000,
  availability_guarantee: 0.98
})
const matrixForm = reactive({ template: 'UAE_DEWA_VII_BESS' })
const tmForm = reactive({ ambient_max_c: 45, cell_capacity_ah: 280, c_rate: 0.5, cooling_type: 'liquid' })
const seForm = reactive({
  container_count: 20,
  pcs_count: 10,
  communication_protocol: 'IEC_61850',
  dispatch_strategy: 'peak_shaving'
})
const hvForm = reactive({
  total_power_mw: 100,
  poc_voltage_kv: 33,
  short_circuit_capacity_mva: 500,
  poc_type: 'substation'
})
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
    const resp = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
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
  } catch (e) {
    /* ignore */
  }
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
  { id: 'ipp_cashflow', label: 'IPP 现金流瀑布图' }
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
      body: JSON.stringify(body)
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
  const map = { compliant: '合规', non_compliant: '不合规', partial: '部分合规', 'N/A': '待确认' }
  return map[status] || status
}

function statusClass(status) {
  const map = { compliant: 'pass', non_compliant: 'fail', partial: 'warn', 'N/A': 'neutral' }
  return map[status] || 'neutral'
}

function getDeratingColor(pct) {
  if (pct > 80) return 'var(--color-success)'
  if (pct > 50) return 'var(--color-warning)'
  return 'var(--color-danger)'
}

onMounted(() => {
  loadStandards()
})
</script>

<style scoped>
.epc-page {
  padding: 24px;
}

.epc-header {
  margin-bottom: 24px;
}
.epc-header h1 {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 8px;
}
.epc-desc {
  color: var(--text-secondary, var(--color-text-secondary));
  font-size: 14px;
  margin: 0;
}

/* Tab navigation */
.epc-tabs {
  display: flex;
  gap: 4px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  border-bottom: 1px solid var(--color-border);
  padding-bottom: 0;
}

.epc-tabs button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  border-bottom: none;
  background: var(--color-card);
  cursor: pointer;
  font-size: 13px;
  transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
  color: var(--color-text-secondary);
  position: relative;
  top: 1px;
}

.epc-tabs button.active {
  background: var(--color-card);
  color: var(--color-accent);
  border-color: var(--color-accent);
  font-weight: 500;
  border-bottom: 1px solid var(--color-card);
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

/* Priority badges - semantic status colors */
.pri-P0-1 {
  background: var(--color-success);
  color: white;
}
.pri-P0-2 {
  background: var(--color-accent-glow);
  color: var(--color-accent);
}
.pri-P0-3 {
  background: var(--color-accent-dark);
  color: var(--color-accent);
}
.pri-P0-4 {
  background: rgba(245, 158, 11, 0.15);
  color: var(--color-warning);
}
.pri-P0-5 {
  background: rgba(139, 92, 246, 0.15);
  color: var(--color-info);
}
.pri-P1-1 {
  background: var(--color-tab-hover);
  color: var(--color-text-secondary);
}
.pri-P1-2 {
  background: var(--color-card-dark);
  color: var(--color-text-secondary);
}
.pri-P1-3 {
  background: var(--color-step-bg);
  color: var(--color-text-secondary);
}
.pri-P1-4 {
  background: var(--color-bg);
  color: var(--color-text-secondary);
}

/* Panel card — design spec */
.panel-card {
  background: var(--section-card-bg);
  border-radius: var(--section-card-radius);
  padding: 24px 28px;
  border: 1px solid var(--section-card-border);
  box-shadow: var(--section-card-shadow);
  margin-bottom: var(--section-card-gap);
}

.panel-title {
  font-size: var(--section-title-size);
  font-weight: var(--section-title-weight);
  margin: 0 0 16px;
  color: var(--section-title-color);
  letter-spacing: -0.01em;
}

.section-title {
  color: var(--color-text-secondary);
  font-size: 14px;
}

/* Form inputs — design spec */
.field-label {
  color: var(--form-label-color);
  font-size: var(--form-label-size);
  font-weight: var(--form-label-weight);
}

/* Buttons */
/* Metric cards */
.metric-card {
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 12px;
  text-align: center;
}

.metric-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-text);
}

.metric-label {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  margin-top: 2px;
}

.primary-text {
  color: var(--color-accent) !important;
}
.pass-text {
  color: var(--color-success) !important;
}
.fail-text {
  color: var(--color-danger) !important;
}
.warn-text {
  color: var(--color-warning) !important;
}

/* Stage cards */
.stage-card {
  background: var(--color-accent-glow);
  border-radius: 8px;
  padding: 12px;
  border: 1px solid var(--color-accent-dark);
}

/* Banners */
.pass-banner {
  background: rgba(16, 185, 129, 0.15);
  border-radius: 8px;
}

.fail-banner {
  background: rgba(239, 68, 68, 0.1);
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
  background: var(--color-table-header);
  font-weight: 600;
  color: var(--color-text);
}

.border-row {
  border-bottom: 1px solid var(--color-border);
}

.status-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.pass {
  background: var(--color-success);
  color: white;
}
.status-badge.fail {
  background: var(--color-danger);
  color: white;
}
.status-badge.warn {
  background: var(--color-warning);
  color: white;
}
.status-badge.neutral {
  background: var(--color-card);
  color: var(--color-text-secondary);
}

/* Derating chart */
.derating-chart {
  background: var(--color-card);
  border-radius: 8px;
  padding: 8px;
  border: 1px solid var(--color-border);
}

.derating-bar {
  min-height: 4px;
  transition: height 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Info box */
.info-box {
  background: var(--color-card);
  border-radius: 8px;
  padding: 16px;
  border: 1px solid var(--color-border);
}

.info-list div {
  color: var(--color-text-secondary);
}

/* Protection items */
.protection-item {
  background: var(--color-card);
  border-radius: 6px;
  padding: 8px;
  border: 1px solid var(--color-border);
  font-size: 12px;
}

/* Chapter / section */
.chapter-title {
  background: var(--color-bg-secondary);
  color: var(--color-accent);
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 8px;
}

.section-item {
  margin-left: 16px;
  padding: 12px;
  background: var(--color-card);
  border-radius: 6px;
  margin-bottom: 8px;
}

/* Chart buttons */
.chart-btn {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  border: 1px solid var(--color-accent);
  background: var(--color-card);
  color: var(--color-accent);
  cursor: pointer;
  transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

.chart-btn:hover {
  background: var(--color-accent-glow);
}

.chart-btn.active {
  background: var(--color-accent);
  color: white;
}

.chart-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Chart container */
.chart-container {
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background: var(--color-card);
  min-height: 300px;
}

/* Error box */
.error-box {
  background: rgba(239, 68, 68, 0.1);
  color: var(--color-danger);
  border-radius: 6px;
}

/* Empty state */
.empty-state {
  color: var(--color-text-muted);
}

/* Border top */
.border-top {
  border-top: 1px solid var(--color-border);
}

.space-y-4 > * + * {
  margin-top: 16px;
}

/* Utility helpers */
.tx-muted {
  color: var(--color-text-muted);
}
.tx-muted-dark {
  color: var(--color-text-secondary);
}
.max-w-sm {
  max-width: 300px;
}
</style>
