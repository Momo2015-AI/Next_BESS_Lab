<template>
  <div class="space-y-4">
    <!-- 模块标签页 -->
    <div class="flex flex-wrap gap-2 border-b border-color-muted">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        class="px-4 py-2 text-sm font-medium border-b-2 transition-all"
        :style="
          activeModule === tab.id
            ? { borderColor: 'var(--color-accent)', color: 'var(--color-accent)' }
            : { borderColor: 'transparent', color: 'var(--color-text-secondary)' }
        "
        @click="activeModule = tab.id"
      >
        {{ tab.icon }} {{ tab.label }}
      </button>
    </div>

    <!-- P0-3: 系统架构 -->
    <div v-show="activeModule === 'architecture'" class="space-y-4">
      <div class="bg-white rounded-lg p-6 shadow-sm border border-color-muted">
        <h3 class="text-lg font-bold mb-4 text-accent">系统架构设计</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-xs mb-1 text-muted">系统功率 (MW)</label>
            <input v-model.number="archForm.total_power_mw" type="number" class="form-field-input" placeholder="1400" />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">系统能量 (MWh)</label>
            <input
              v-model.number="archForm.total_energy_mwh"
              type="number"
              class="form-field-input"
              placeholder="8400"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">架构类型</label>
            <select v-model="archForm.architecture_type" class="form-field-select">
              <option value="central">集中式</option>
              <option value="string">组串式</option>
              <option value="hybrid">混合式</option>
            </select>
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">耦合方式</label>
            <select v-model="archForm.coupling_type" class="form-field-select">
              <option value="AC">AC耦合</option>
              <option value="DC">DC耦合</option>
              <option value="hybrid">混合耦合</option>
            </select>
          </div>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-xs mb-1 text-muted">电芯电压 (V)</label>
            <input
              v-model.number="archForm.cell_voltage"
              type="number"
              step="0.1"
              class="form-field-input"
              placeholder="3.2"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">电芯容量 (Ah)</label>
            <input v-model.number="archForm.cell_capacity" type="number" class="form-field-input" placeholder="280" />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">PCS功率 (MW)</label>
            <input
              v-model.number="archForm.pcs_power_mw"
              type="number"
              step="0.01"
              class="form-field-input"
              placeholder="3.45"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">PCS最大DC电压 (V)</label>
            <input
              v-model.number="archForm.pcs_max_dc_voltage"
              type="number"
              class="form-field-input"
              placeholder="1500"
            />
          </div>
        </div>
        <button
          :disabled="loading"
          class="px-6 py-2 rounded-lg text-white font-medium text-sm bg-accent"
          @click="designArchitecture"
        >
          {{ loading ? '计算中...' : '执行架构设计' }}
        </button>

        <div v-if="archResult" class="mt-6 space-y-4">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div
              v-for="item in archResult.topology_data.levels"
              :key="item.name"
              class="bg-gray-50 rounded-lg p-3 text-center"
            >
              <div class="text-2xl font-bold text-accent">
                {{ item.count }}
              </div>
              <div class="text-xs text-muted">{{ item.name }} ({{ item.unit }})</div>
            </div>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
            <div class="result-card">
              <div class="result-value">
                {{ archResult.pcs_count }}
              </div>
              <div class="result-label">PCS总数</div>
            </div>
            <div class="result-card">
              <div class="result-value">{{ archResult.dc_bus_voltage }}V</div>
              <div class="result-label">DC母线电压</div>
            </div>
            <div class="result-card">
              <div class="result-value">
                {{ archResult.total_containers }}
              </div>
              <div class="result-label">集装箱总数</div>
            </div>
            <div class="result-card">
              <div class="result-value">
                {{ archResult.stage_count }}
              </div>
              <div class="result-label">分期数</div>
            </div>
            <div class="result-card">
              <div class="result-value">{{ archResult.duration_hours }}h</div>
              <div class="result-label">储能时长</div>
            </div>
          </div>
          <div v-if="archResult.stages" class="mt-4">
            <h4 class="text-sm font-bold mb-2 text-secondary">分期建设方案</h4>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
              <div
                v-for="stage in archResult.stages"
                :key="stage.stage"
                class="bg-blue-50 rounded-lg p-3 border border-color-glow"
              >
                <div class="font-bold text-sm text-accent">第{{ stage.stage }}期</div>
                <div class="text-xs text-secondary">{{ stage.power_mw }}MW / {{ stage.energy_mwh }}MWh</div>
                <div class="text-xs text-muted">
                  {{ stage.estimated_date }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- P0-1: 电网合规 -->
    <div v-show="activeModule === 'gridCompliance'" class="space-y-4">
      <div class="bg-white rounded-lg p-6 shadow-sm border border-color-muted">
        <h3 class="text-lg font-bold mb-4 text-accent">电网合规分析</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-xs mb-1 text-muted">电网标准</label>
            <select v-model="gcForm.grid_standard" class="form-field-select">
              <option v-for="s in gridStandards" :key="s.code" :value="s.code">
                {{ s.name }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">并网点电压 (kV)</label>
            <input v-model.number="gcForm.grid_voltage_kv" type="number" class="form-field-input" placeholder="33" />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">电网频率 (Hz)</label>
            <input
              v-model.number="gcForm.grid_frequency_hz"
              type="number"
              step="0.01"
              class="form-field-input"
              placeholder="50"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">PCS数量</label>
            <input v-model.number="gcForm.pcs_count" type="number" class="form-field-input" placeholder="10" />
          </div>
        </div>
        <button
          :disabled="loading"
          class="px-6 py-2 rounded-lg text-white font-medium text-sm bg-accent"
          @click="analyzeGridCompliance"
        >
          {{ loading ? '分析中...' : '执行合规分析' }}
        </button>

        <div v-if="gcResult" class="mt-6 space-y-4">
          <div
            class="flex items-center gap-4 p-4 rounded-lg"
            :style="
              gcResult.overall_pass
                ? { backgroundColor: 'rgba(16, 185, 129, 0.15)' }
                : { backgroundColor: 'rgba(239, 68, 68, 0.1)' }
            "
          >
            <span class="text-3xl">{{ gcResult.overall_pass ? '✅' : '❌' }}</span>
            <div>
              <div
                class="font-bold"
                :style="gcResult.overall_pass ? { color: 'var(--color-success)' } : { color: 'var(--color-danger)' }"
              >
                {{ gcResult.overall_pass ? '全部合规' : '存在不合规项' }}
              </div>
              <div v-if="gcResult.failed_items.length" class="text-xs text-secondary">
                不合规: {{ gcResult.failed_items.join(', ') }}
              </div>
            </div>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="result-card">
              <div class="result-value" :class="gcResult.lvrt_pass ? 'text-green-600' : 'text-red-600'">
                {{ gcResult.lvrt_pass ? 'PASS' : 'FAIL' }}
              </div>
              <div class="result-label">LVRT低电压穿越</div>
            </div>
            <div class="result-card">
              <div class="result-value" :class="gcResult.hvrt_pass ? 'text-green-600' : 'text-red-600'">
                {{ gcResult.hvrt_pass ? 'PASS' : 'FAIL' }}
              </div>
              <div class="result-label">HVRT高电压穿越</div>
            </div>
            <div class="result-card">
              <div class="result-value" :class="gcResult.freq_response_pass ? 'text-green-600' : 'text-red-600'">
                {{ gcResult.freq_response_pass ? 'PASS' : 'FAIL' }}
              </div>
              <div class="result-label">频率响应</div>
            </div>
            <div class="result-card">
              <div class="result-value" :class="gcResult.reactive_pass ? 'text-green-600' : 'text-red-600'">
                {{ gcResult.reactive_pass ? 'PASS' : 'FAIL' }}
              </div>
              <div class="result-label">无功功率 ({{ gcResult.reactive_capacity_mvar }}MVar)</div>
            </div>
            <div class="result-card">
              <div class="result-value" :class="gcResult.power_quality_pass ? 'text-green-600' : 'text-red-600'">
                {{ gcResult.thd }}%
              </div>
              <div class="result-label">THD (限值5%)</div>
            </div>
            <div class="result-card">
              <div class="result-value" :class="gcResult.anti_islanding_pass ? 'text-green-600' : 'text-red-600'">
                {{ gcResult.anti_islanding_time_s }}s
              </div>
              <div class="result-label">防孤岛 (限值2s)</div>
            </div>
            <div class="result-card">
              <div class="result-value" :class="gcResult.comm_pass ? 'text-green-600' : 'text-red-600'">
                {{ gcResult.comm_pass ? 'PASS' : 'FAIL' }}
              </div>
              <div class="result-label">通信合规</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- P0-2: 安全消防 -->
    <div v-show="activeModule === 'safety'" class="space-y-4">
      <div class="bg-white rounded-lg p-6 shadow-sm border border-color-muted">
        <h3 class="text-lg font-bold mb-4 text-accent">安全与消防设计</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-xs mb-1 text-muted">系统容量 (MWh)</label>
            <input
              v-model.number="sfForm.system_capacity_mwh"
              type="number"
              class="form-field-input"
              placeholder="100"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">集装箱数量</label>
            <input v-model.number="sfForm.container_count" type="number" class="form-field-input" placeholder="20" />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">化学体系</label>
            <select v-model="sfForm.chemistry_type" class="form-field-select">
              <option value="LFP">LFP (磷酸铁锂)</option>
              <option value="NCM">NCM (三元)</option>
              <option value="NCA">NCA</option>
              <option value="LTO">LTO (钛酸锂)</option>
            </select>
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">灭火系统</label>
            <select v-model="sfForm.suppression_type" class="form-field-select">
              <option value="Novec1230">Novec 1230</option>
              <option value="Aerosol">气溶胶</option>
              <option value="Water-mist">细水雾</option>
            </select>
          </div>
        </div>
        <button
          :disabled="loading"
          class="px-6 py-2 rounded-lg text-white font-medium text-sm bg-accent"
          @click="analyzeSafety"
        >
          {{ loading ? '分析中...' : '执行安全分析' }}
        </button>

        <div v-if="sfResult" class="mt-6 space-y-4">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="result-card">
              <div class="result-value">
                {{ sfResult.zone_count }}
              </div>
              <div class="result-label">防火分区数</div>
            </div>
            <div class="result-card">
              <div class="result-value">{{ sfResult.container_spacing_m }}m</div>
              <div class="result-label">集装箱间距</div>
            </div>
            <div class="result-card">
              <div class="result-value">{{ sfResult.thermal_runaway_temp_c }}°C</div>
              <div class="result-label">热失控温度</div>
            </div>
            <div class="result-card">
              <div class="result-value">{{ sfResult.propagation_time_min }}min</div>
              <div class="result-label">蔓延时间</div>
            </div>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="result-card">
              <div class="result-value" :class="sfResult.ul_9540a_pass ? 'text-green-600' : 'text-red-600'">
                {{ sfResult.ul_9540a_pass ? 'PASS' : 'FAIL' }}
              </div>
              <div class="result-label">UL 9540A</div>
            </div>
            <div class="result-card">
              <div class="result-value" :class="sfResult.nfpa_855_pass ? 'text-green-600' : 'text-red-600'">
                {{ sfResult.nfpa_855_pass ? 'PASS' : 'FAIL' }}
              </div>
              <div class="result-label">NFPA 855</div>
            </div>
            <div class="result-card">
              <div class="result-value" :class="sfResult.iec_62619_pass ? 'text-green-600' : 'text-red-600'">
                {{ sfResult.iec_62619_pass ? 'PASS' : 'FAIL' }}
              </div>
              <div class="result-label">IEC 62619</div>
            </div>
            <div class="result-card">
              <div class="result-value">{{ sfResult.suppression_capacity_kg }}kg</div>
              <div class="result-label">灭火剂容量</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- P0-4: IPP财务 -->
    <div v-show="activeModule === 'ipp'" class="space-y-4">
      <div class="bg-white rounded-lg p-6 shadow-sm border border-color-muted">
        <h3 class="text-lg font-bold mb-4 text-accent">IPP财务模型</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-xs mb-1 text-muted">项目寿命 (年)</label>
            <input
              v-model.number="ippForm.project_life_years"
              type="number"
              class="form-field-input"
              placeholder="25"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">总CAPEX (USD)</label>
            <input
              v-model.number="ippForm.total_capex_usd"
              type="number"
              class="form-field-input"
              placeholder="500000000"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">容量 (MW)</label>
            <input v-model.number="ippForm.capacity_mw" type="number" class="form-field-input" placeholder="100" />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">能量 (MWh)</label>
            <input v-model.number="ippForm.energy_mwh" type="number" class="form-field-input" placeholder="200" />
          </div>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-xs mb-1 text-muted">容量价格 ($/kW/月)</label>
            <input
              v-model.number="ippForm.capacity_price_usd_kw_month"
              type="number"
              step="0.1"
              class="form-field-input"
              placeholder="8.0"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">电量价格 ($/kWh)</label>
            <input
              v-model.number="ippForm.energy_price_usd_kwh"
              type="number"
              step="0.01"
              class="form-field-input"
              placeholder="0.05"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">PPA递增率</label>
            <input
              v-model.number="ippForm.ppa_escalation_rate"
              type="number"
              step="0.01"
              class="form-field-input"
              placeholder="0.02"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">贷款比例</label>
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
            <label class="block text-xs mb-1 text-muted">贷款利率</label>
            <input
              v-model.number="ippForm.debt_interest_rate"
              type="number"
              step="0.01"
              class="form-field-input"
              placeholder="0.05"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">贷款期限 (年)</label>
            <input v-model.number="ippForm.debt_tenor_years" type="number" class="form-field-input" placeholder="15" />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">年OPEX (USD)</label>
            <input
              v-model.number="ippForm.annual_opex_usd"
              type="number"
              class="form-field-input"
              placeholder="5000000"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">可用率保证</label>
            <input
              v-model.number="ippForm.availability_guarantee"
              type="number"
              step="0.01"
              class="form-field-input"
              placeholder="0.98"
            />
          </div>
        </div>
        <button
          :disabled="loading"
          class="px-6 py-2 rounded-lg text-white font-medium text-sm bg-accent"
          @click="calculateIPP"
        >
          {{ loading ? '计算中...' : '执行财务计算' }}
        </button>

        <div v-if="ippResult" class="mt-6 space-y-4">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="result-card">
              <div class="result-value text-accent">${{ formatNum(ippResult.npv_usd) }}</div>
              <div class="result-label">NPV</div>
            </div>
            <div class="result-card">
              <div class="result-value text-accent">{{ ippResult.irr }}%</div>
              <div class="result-label">项目IRR</div>
            </div>
            <div class="result-card">
              <div class="result-value text-accent">{{ ippResult.equity_irr }}%</div>
              <div class="result-label">股权IRR</div>
            </div>
            <div class="result-card">
              <div class="result-value text-accent">${{ ippResult.lcoe_usd_kwh }}/kWh</div>
              <div class="result-label">LCOE</div>
            </div>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
            <div class="result-card">
              <div class="result-value">
                {{ ippResult.dscr_avg }}
              </div>
              <div class="result-label">平均DSCR</div>
            </div>
            <div class="result-card">
              <div class="result-value">
                {{ ippResult.dscr_min }}
              </div>
              <div class="result-label">最小DSCR</div>
            </div>
            <div class="result-card">
              <div class="result-value">{{ ippResult.payback_years }}年</div>
              <div class="result-label">回收期</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- P0-5: 合规矩阵 -->
    <div v-show="activeModule === 'matrix'" class="space-y-4">
      <div class="bg-white rounded-lg p-6 shadow-sm border border-color-muted">
        <h3 class="text-lg font-bold mb-4 text-accent">合规矩阵生成</h3>
        <div class="flex gap-4 mb-4">
          <select v-model="matrixForm.template" class="form-field-select mw-300">
            <option value="UAE_DEWA_VII_BESS">UAE DEWA VII BESS RFP</option>
          </select>
          <button
            :disabled="loading"
            class="px-6 py-2 rounded-lg text-white font-medium text-sm bg-accent"
            @click="generateMatrix"
          >
            {{ loading ? '生成中...' : '生成合规矩阵' }}
          </button>
        </div>

        <div v-if="matrixResult" class="mt-4">
          <div class="grid grid-cols-4 gap-3 mb-4">
            <div class="result-card">
              <div class="result-value">
                {{ matrixResult.total }}
              </div>
              <div class="result-label">总条款</div>
            </div>
            <div class="result-card">
              <div class="result-value text-green-600">
                {{ matrixResult.compliant }}
              </div>
              <div class="result-label">合规</div>
            </div>
            <div class="result-card">
              <div class="result-value text-red-600">
                {{ matrixResult.non_compliant }}
              </div>
              <div class="result-label">不合规</div>
            </div>
            <div class="result-card">
              <div class="result-value text-yellow-600">
                {{ matrixResult.partial }}
              </div>
              <div class="result-label">部分合规</div>
            </div>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-table-header">
                  <th class="px-3 py-2 text-left">条款</th>
                  <th class="px-3 py-2 text-left">要求</th>
                  <th class="px-3 py-2 text-left">类别</th>
                  <th class="px-3 py-2 text-left">状态</th>
                  <th class="px-3 py-2 text-left">回应</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in matrixResult.matrix" :key="item.section" class="border-b border-color-muted">
                  <td class="px-3 py-2 font-mono text-xs">
                    {{ item.section }}
                  </td>
                  <td class="px-3 py-2">
                    {{ item.requirement }}
                  </td>
                  <td class="px-3 py-2 text-xs text-muted">
                    {{ item.category }}
                  </td>
                  <td class="px-3 py-2">
                    <span
                      class="px-2 py-1 rounded text-xs font-medium"
                      :class="{
                        'bg-green-100 text-green-700': item.compliance_status === 'compliant',
                        'bg-red-100 text-red-700': item.compliance_status === 'non_compliant',
                        'bg-yellow-100 text-yellow-700': item.compliance_status === 'partial',
                        'bg-gray-100 text-gray-500': item.compliance_status === 'N/A'
                      }"
                    >
                      {{ statusLabel(item.compliance_status) }}
                    </span>
                  </td>
                  <td class="px-3 py-2 text-xs text-secondary">
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
    <div v-show="activeModule === 'thermal'" class="space-y-4">
      <div class="bg-white rounded-lg p-6 shadow-sm border border-color-muted">
        <h3 class="text-lg font-bold mb-4 text-accent">热管理设计</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-xs mb-1 text-muted">最高环境温度 (°C)</label>
            <input v-model.number="tmForm.ambient_max_c" type="number" class="form-field-input" placeholder="45" />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">电芯容量 (Ah)</label>
            <input v-model.number="tmForm.cell_capacity_ah" type="number" class="form-field-input" placeholder="280" />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">充放电倍率 (C)</label>
            <input v-model.number="tmForm.c_rate" type="number" step="0.1" class="form-field-input" placeholder="0.5" />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">冷却方式</label>
            <select v-model="tmForm.cooling_type" class="form-field-select">
              <option value="liquid">液冷</option>
              <option value="air">风冷</option>
            </select>
          </div>
        </div>
        <button
          :disabled="loading"
          class="px-6 py-2 rounded-lg text-white font-medium text-sm bg-accent"
          @click="calculateThermal"
        >
          {{ loading ? '计算中...' : '执行热管理计算' }}
        </button>

        <div v-if="tmResult" class="mt-6 space-y-4">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="result-card">
              <div class="result-value">{{ tmResult.cooling_power_kw }}kW</div>
              <div class="result-label">制冷功率</div>
            </div>
            <div class="result-card">
              <div class="result-value">{{ tmResult.coolant_flow_rate_lpm }}L/min</div>
              <div class="result-label">冷却液流量</div>
            </div>
            <div class="result-card">
              <div class="result-value">{{ tmResult.max_cell_temp_c }}°C</div>
              <div class="result-label">最高电芯温度</div>
            </div>
            <div class="result-card">
              <div class="result-value">{{ formatNum(tmResult.annual_cooling_energy_kwh) }}kWh</div>
              <div class="result-label">年制冷能耗</div>
            </div>
          </div>
          <div v-if="tmResult.derating_curve" class="mt-4">
            <h4 class="text-sm font-bold mb-2 text-secondary">高温降额曲线</h4>
            <div class="flex gap-1 items-end h-32">
              <div v-for="point in tmResult.derating_curve" :key="point.temp" class="flex-1 flex flex-col items-center">
                <div
                  class="w-full rounded-t"
                  :style="{
                    height: point.power_pct + '%',
                    backgroundColor:
                      point.power_pct > 80
                        ? 'var(--color-success)'
                        : point.power_pct > 50
                          ? 'var(--color-warning)'
                          : 'var(--color-danger)'
                  }"
                />
                <div class="text-xs mt-1 text-muted">{{ point.temp }}°C</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- P1-2: SCADA/EMS -->
    <div v-show="activeModule === 'scada'" class="space-y-4">
      <div class="bg-white rounded-lg p-6 shadow-sm border border-color-muted">
        <h3 class="text-lg font-bold mb-4 text-accent">SCADA/EMS设计</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-xs mb-1 text-muted">集装箱数量</label>
            <input v-model.number="seForm.container_count" type="number" class="form-field-input" placeholder="20" />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">PCS数量</label>
            <input v-model.number="seForm.pcs_count" type="number" class="form-field-input" placeholder="10" />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">通信协议</label>
            <select v-model="seForm.communication_protocol" class="form-field-select">
              <option value="IEC_61850">IEC 61850</option>
              <option value="Modbus_TCP">Modbus TCP</option>
              <option value="DNP3">DNP3</option>
            </select>
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">调度策略</label>
            <select v-model="seForm.dispatch_strategy" class="form-field-select">
              <option value="peak_shaving">削峰填谷</option>
              <option value="arbitrage">套利</option>
              <option value="frequency_regulation">调频</option>
            </select>
          </div>
        </div>
        <button
          :disabled="loading"
          class="px-6 py-2 rounded-lg text-white font-medium text-sm bg-accent"
          @click="designScada"
        >
          {{ loading ? '设计中...' : '执行SCADA设计' }}
        </button>

        <div v-if="seResult" class="mt-6 space-y-4">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="result-card">
              <div class="result-value">
                {{ seResult.total_data_points }}
              </div>
              <div class="result-label">总数据点</div>
            </div>
            <div class="result-card">
              <div class="result-value">
                {{ seResult.analog_points }}
              </div>
              <div class="result-label">模拟量</div>
            </div>
            <div class="result-card">
              <div class="result-value">
                {{ seResult.digital_points }}
              </div>
              <div class="result-label">数字量</div>
            </div>
            <div class="result-card">
              <div class="result-value">
                {{ seResult.control_points }}
              </div>
              <div class="result-label">控制点</div>
            </div>
          </div>
          <div class="p-4 bg-gray-50 rounded-lg">
            <div class="text-sm font-bold mb-2 text-secondary">系统架构</div>
            <div class="text-sm space-y-1 text-muted">
              <div>架构类型: {{ seResult.scada_architecture }}</div>
              <div>网络拓扑: {{ seResult.network_topology }}</div>
              <div>冗余等级: {{ seResult.redundancy_level }}</div>
              <div>加密方式: {{ seResult.encryption_type }}</div>
              <div>NERC-CIP: {{ seResult.nerc_cip_compliant ? '✅' : '❌' }}</div>
              <div>IEC 62443: {{ seResult.iec_62443_compliant ? '✅' : '❌' }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- P1-3: 高压接入 -->
    <div v-show="activeModule === 'hv'" class="space-y-4">
      <div class="bg-white rounded-lg p-6 shadow-sm border border-color-muted">
        <h3 class="text-lg font-bold mb-4 text-accent">高压接入设计</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label class="block text-xs mb-1 text-muted">总功率 (MW)</label>
            <input v-model.number="hvForm.total_power_mw" type="number" class="form-field-input" placeholder="100" />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">并网点电压 (kV)</label>
            <input v-model.number="hvForm.poc_voltage_kv" type="number" class="form-field-input" placeholder="33" />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">短路容量 (MVA)</label>
            <input
              v-model.number="hvForm.short_circuit_capacity_mva"
              type="number"
              class="form-field-input"
              placeholder="500"
            />
          </div>
          <div>
            <label class="block text-xs mb-1 text-muted">并网点类型</label>
            <select v-model="hvForm.poc_type" class="form-field-select">
              <option value="substation">变电站</option>
              <option value="overhead_line">架空线</option>
              <option value="cable">电缆</option>
            </select>
          </div>
        </div>
        <button
          :disabled="loading"
          class="px-6 py-2 rounded-lg text-white font-medium text-sm bg-accent"
          @click="designHV"
        >
          {{ loading ? '设计中...' : '执行高压接入设计' }}
        </button>

        <div v-if="hvResult" class="mt-6 space-y-4">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="result-card">
              <div class="result-value">
                {{ hvResult.transformer_count }}
              </div>
              <div class="result-label">变压器数量</div>
            </div>
            <div class="result-card">
              <div class="result-value">{{ hvResult.transformer_capacity_mva }}MVA</div>
              <div class="result-label">变压器容量</div>
            </div>
            <div class="result-card">
              <div class="result-value">
                {{ hvResult.transformer_ratio }}
              </div>
              <div class="result-label">变比</div>
            </div>
            <div class="result-card">
              <div class="result-value">{{ hvResult.mv_breaker_rating_ka }}kA</div>
              <div class="result-label">断路器额定值</div>
            </div>
          </div>
          <div v-if="hvResult.protection_scheme" class="p-4 bg-gray-50 rounded-lg">
            <div class="text-sm font-bold mb-2 text-secondary">保护配置</div>
            <div class="grid grid-cols-2 md:grid-cols-5 gap-2">
              <div
                v-for="prot in hvResult.protection_scheme"
                :key="prot.name"
                class="text-xs bg-white rounded p-2 border border-color-muted"
              >
                <div class="font-bold">
                  {{ prot.name }}
                </div>
                <div class="text-muted">
                  {{ prot.type }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- P1-4: 投标文档 -->
    <div v-show="activeModule === 'bidDoc'" class="space-y-4">
      <div class="bg-white rounded-lg p-6 shadow-sm border border-color-muted">
        <h3 class="text-lg font-bold mb-4 text-accent">投标文档生成</h3>
        <div class="flex gap-4 mb-4">
          <select v-model="bidForm.template" class="form-field-select mw-300">
            <option value="technical_proposal">技术方案</option>
          </select>
          <button
            :disabled="loading"
            class="px-6 py-2 rounded-lg text-white font-medium text-sm bg-accent"
            @click="generateBidDoc"
          >
            {{ loading ? '生成中...' : '生成投标文档' }}
          </button>
        </div>

        <div v-if="bidResult" class="mt-4">
          <div v-for="chapter in bidResult.chapters" :key="chapter.num" class="mb-4">
            <div class="font-bold text-sm p-2 rounded bg-secondary text-accent">
              {{ chapter.num }}. {{ chapter.title }}
            </div>
            <div v-for="sec in chapter.sections" :key="sec.num" class="ml-4 mt-2 p-3 bg-gray-50 rounded">
              <div class="font-medium text-sm">{{ sec.num }} {{ sec.title }}</div>
              <div class="text-xs mt-1 whitespace-pre-line text-secondary">
                {{ sec.content }}
              </div>
              <div class="text-xs mt-1 text-muted">数据来源: {{ sec.data_source }}</div>
            </div>
          </div>
        </div>

        <!-- 交互式图表预览 -->
        <div class="mt-6 pt-4 border-t border-color-muted">
          <div class="flex items-center justify-between mb-3">
            <h4 class="text-base font-bold text-accent">交互式图表预览</h4>
            <span class="text-xs text-muted">基于 Plotly，支持缩放/悬停/导出</span>
          </div>
          <div class="flex flex-wrap gap-2 mb-3">
            <button
              v-for="c in chartTypes"
              :key="c.id"
              :disabled="chartLoading === c.id"
              class="px-3 py-1.5 rounded-md text-xs font-medium border transition-all"
              :style="
                activeChart === c.id
                  ? { backgroundColor: 'var(--color-accent)', color: 'white', borderColor: 'var(--color-accent)' }
                  : {
                      backgroundColor: 'var(--color-card)',
                      color: 'var(--color-accent)',
                      borderColor: 'var(--color-accent)'
                    }
              "
              @click="previewChart(c.id)"
            >
              {{ chartLoading === c.id ? '加载中...' : c.label }}
            </button>
          </div>
          <div v-if="chartError" class="text-xs p-2 rounded mb-3 tag-glow text-danger">
            {{ chartError }}
          </div>
          <div v-if="chartReady" ref="chartContainer" class="chart-container-sm" />
          <div v-else-if="!chartLoading" class="text-xs text-center py-8 text-muted">
            点击上方按钮选择图表类型，预览投标方案交互式可视化
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, nextTick } from 'vue'
import { renderPlotly, purgePlotly } from '../composables/usePlotly.js'

const emit = defineEmits(['error'])

const loading = ref(false)
const activeModule = ref('architecture')

const tabs = [
  { id: 'architecture', label: '系统架构', icon: '🏗️' },
  { id: 'gridCompliance', label: '电网合规', icon: '🔌' },
  { id: 'safety', label: '安全消防', icon: '🛡️' },
  { id: 'ipp', label: 'IPP财务', icon: '🏦' },
  { id: 'matrix', label: '合规矩阵', icon: '📋' },
  { id: 'thermal', label: '热管理', icon: '🌡️' },
  { id: 'scada', label: 'SCADA/EMS', icon: '📡' },
  { id: 'hv', label: '高压接入', icon: '⚡' },
  { id: 'bidDoc', label: '投标文档', icon: '📄' }
]

const gridStandards = ref([])

// 表单数据
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

// 结果
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

// ==================== 交互式图表预览 ====================
const chartTypes = [
  { id: 'soh_rte_curve', label: 'SOH/RTE 衰减曲线' },
  { id: 'capacity_matrix', label: '容量矩阵热力图' },
  { id: 'grid_compliance', label: 'LVRT/HVRT 曲线' },
  { id: 'ipp_cashflow', label: 'IPP 现金流瀑布图' }
]
const chartReady = ref(false)
const chartLoading = ref('')
const chartError = ref('')
const activeChart = ref('')
const chartContainer = ref(null)

async function previewChart(chartType) {
  chartLoading.value = chartType
  chartError.value = ''
  chartReady.value = false
  if (chartContainer.value) {
    purgePlotly(chartContainer.value)
  }
  try {
    // 复用已生成的投标文档数据作为图表输入源，避免重复查询
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
    if (result.success && result.chart) {
      activeChart.value = chartType
      chartReady.value = true
      await nextTick()
      await renderPlotly(chartContainer.value, result.chart, result.div_id)
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

onMounted(() => {
  loadStandards()
})

onUnmounted(() => {
  if (chartContainer.value) {
    purgePlotly(chartContainer.value)
  }
})
</script>

<style scoped>
.result-card {
  background-color: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 12px;
  text-align: center;
}
.result-value {
  font-size: 1.25rem;
  font-weight: bold;
  color: var(--color-text);
}
.result-label {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  margin-top: 2px;
}
</style>
