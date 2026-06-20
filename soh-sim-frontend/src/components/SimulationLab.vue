<template>
  <div class="flex flex-col gap-4 h-full overflow-auto p-4">
    <!-- 步骤指示器 -->
    <div class="flex items-center gap-2 bg-slate-900/60 p-2 rounded-lg border border-slate-800">
      <div v-for="(step, idx) in steps" :key="idx" 
        :class="['flex items-center gap-1 px-3 py-1 rounded text-xs transition-all',
          currentStep >= idx ? 'bg-teal-500/20 text-teal-400 border border-teal-500/30' : 'text-slate-500']">
        <span class="w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold"
          :class="currentStep >= idx ? 'bg-teal-500 text-white' : 'bg-slate-700 text-slate-400'">
          {{ idx + 1 }}
        </span>
        {{ step.label }}
      </div>
    </div>

    <!-- 步骤1: 调研表数据 -->
    <div v-show="currentStep === 0" class="bg-slate-900/40 rounded-lg border border-slate-800 p-4">
      <h3 class="text-sm font-bold text-teal-400 mb-3 flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-teal-400"></span>
        调研表数据获取
      </h3>
      
      <div class="grid grid-cols-2 gap-4">
        <!-- 调研表ID输入 -->
        <div class="space-y-2">
          <label class="text-xs text-slate-400">调研表串码ID</label>
          <div class="flex gap-2">
            <input v-model="surveyId" type="text" placeholder="输入调研表ID或扫描二维码"
              class="flex-1 bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs focus:border-teal-500 focus:outline-none">
            <button @click="loadSurveyData" 
              class="bg-teal-500 hover:bg-teal-600 text-white text-xs px-3 py-1.5 rounded transition-all">
              加载
            </button>
          </div>
        </div>

        <!-- 项目信息 -->
        <div class="space-y-2">
          <label class="text-xs text-slate-400">项目名称</label>
          <input v-model="surveyData.projectName" type="text" placeholder="自动填充或手动输入"
            class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-xs focus:border-teal-500 focus:outline-none">
        </div>
      </div>

      <!-- 调研表数据展示 -->
      <div class="mt-4 grid grid-cols-3 gap-3">
        <div class="bg-slate-800/50 rounded p-3 border border-slate-700">
          <label class="text-[10px] text-slate-500 block mb-1">额定能量 (MWh)</label>
          <input v-model.number="surveyData.ratedEnergy" type="number" step="0.1"
            class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs text-teal-400 focus:border-teal-500 focus:outline-none">
        </div>
        <div class="bg-slate-800/50 rounded p-3 border border-slate-700">
          <label class="text-[10px] text-slate-500 block mb-1">集装箱数量</label>
          <input v-model.number="surveyData.containerQty" type="number"
            class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs text-teal-400 focus:border-teal-500 focus:outline-none">
        </div>
        <div class="bg-slate-800/50 rounded p-3 border border-slate-700">
          <label class="text-[10px] text-slate-500 block mb-1">PCS数量</label>
          <input v-model.number="surveyData.pcsQty" type="number"
            class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs text-teal-400 focus:border-teal-500 focus:outline-none">
        </div>
        <div class="bg-slate-800/50 rounded p-3 border border-slate-700">
          <label class="text-[10px] text-slate-500 block mb-1">运行温度 (°C)</label>
          <input v-model.number="surveyData.temperature" type="number" step="0.5"
            class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs text-teal-400 focus:border-teal-500 focus:outline-none">
        </div>
        <div class="bg-slate-800/50 rounded p-3 border border-slate-700">
          <label class="text-[10px] text-slate-500 block mb-1">每日循环次数</label>
          <input v-model.number="surveyData.cyclesPerDay" type="number" step="0.5"
            class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs text-teal-400 focus:border-teal-500 focus:outline-none">
        </div>
        <div class="bg-slate-800/50 rounded p-3 border border-slate-700">
          <label class="text-[10px] text-slate-500 block mb-1">DOD (%)</label>
          <input v-model.number="surveyData.dod" type="number" step="1" min="0" max="100"
            class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs text-teal-400 focus:border-teal-500 focus:outline-none">
        </div>
        <div class="bg-slate-800/50 rounded p-3 border border-slate-700">
          <label class="text-[10px] text-slate-500 block mb-1">倍率 (C)</label>
          <input v-model.number="surveyData.cRate" type="number" step="0.1" min="0.1" max="2"
            class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs text-teal-400 focus:border-teal-500 focus:outline-none">
        </div>
        <div class="bg-slate-800/50 rounded p-3 border border-slate-700">
          <label class="text-[10px] text-slate-500 block mb-1">电池类型</label>
          <select v-model="surveyData.batteryType"
            class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs text-teal-400 focus:border-teal-500 focus:outline-none">
            <option value="LFP">LFP (磷酸铁锂)</option>
            <option value="NCM">NCM (三元锂)</option>
            <option value="LTO">LTO (钛酸锂)</option>
          </select>
        </div>
        <div class="bg-slate-800/50 rounded p-3 border border-slate-700">
          <label class="text-[10px] text-slate-500 block mb-1">项目地点</label>
          <input v-model="surveyData.location" type="text"
            class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs text-teal-400 focus:border-teal-500 focus:outline-none">
        </div>
      </div>

      <div class="mt-4 flex justify-end">
        <button @click="nextStep" 
          class="bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 hover:to-emerald-600 text-white text-xs px-4 py-2 rounded transition-all">
          下一步：补全仿真参数
        </button>
      </div>
    </div>

    <!-- 步骤2: 仿真参数补全 -->
    <div v-show="currentStep === 1" class="bg-slate-900/40 rounded-lg border border-slate-800 p-4">
      <h3 class="text-sm font-bold text-teal-400 mb-3 flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-teal-400"></span>
        仿真参数补全
      </h3>

      <div class="grid grid-cols-4 gap-3">
        <!-- 基础参数 -->
        <div class="col-span-4 bg-slate-800/30 rounded p-3 border border-slate-700">
          <h4 class="text-xs text-slate-300 mb-2 font-medium">基础配置</h4>
          <div class="grid grid-cols-4 gap-3">
            <div>
              <label class="text-[10px] text-slate-500 block mb-1">仿真年限 (年)</label>
              <select v-model.number="simParams.simulationYears"
                class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 focus:outline-none">
                <option value="10">10年</option>
                <option value="15">15年</option>
                <option value="20">20年</option>
                <option value="25">25年</option>
                <option value="30">30年</option>
              </select>
            </div>
            <div>
              <label class="text-[10px] text-slate-500 block mb-1">最低保障年限 (年)</label>
              <select v-model.number="simParams.guaranteeYears"
                class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 focus:outline-none">
                <option value="5">5年</option>
                <option value="10">10年</option>
                <option value="15">15年</option>
                <option value="20">20年</option>
              </select>
            </div>
            <div>
              <label class="text-[10px] text-slate-500 block mb-1">保障SOH底线 (%)</label>
              <input v-model.number="simParams.guaranteeSoh" type="number" step="1" min="60" max="90"
                class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 focus:outline-none">
            </div>
            <div>
              <label class="text-[10px] text-slate-500 block mb-1">承诺能量底线 (MWh)</label>
              <input v-model.number="simParams.requiredEnergy" type="number" step="1"
                class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 focus:outline-none">
            </div>
          </div>
        </div>

        <!-- 效率参数 -->
        <div class="col-span-2 bg-slate-800/30 rounded p-3 border border-slate-700">
          <h4 class="text-xs text-slate-300 mb-2 font-medium">效率参数</h4>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="text-[10px] text-slate-500 block mb-1">初始RTE (%)</label>
              <input v-model.number="simParams.initRte" type="number" step="0.1" min="85" max="95"
                class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 focus:outline-none">
            </div>
            <div>
              <label class="text-[10px] text-slate-500 block mb-1">AC效率 (%)</label>
              <input v-model.number="simParams.acEfficiency" type="number" step="0.1" min="95" max="99"
                class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 focus:outline-none">
            </div>
            <div>
              <label class="text-[10px] text-slate-500 block mb-1">DC效率 (%)</label>
              <input v-model.number="simParams.dcEfficiency" type="number" step="0.1" min="95" max="99"
                class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 focus:outline-none">
            </div>
            <div>
              <label class="text-[10px] text-slate-500 block mb-1">自放电率 (%/月)</label>
              <input v-model.number="simParams.selfDischarge" type="number" step="0.1" min="0" max="5"
                class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 focus:outline-none">
            </div>
          </div>
        </div>

        <!-- 辅耗参数 -->
        <div class="col-span-2 bg-slate-800/30 rounded p-3 border border-slate-700">
          <h4 class="text-xs text-slate-300 mb-2 font-medium">辅耗参数</h4>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="text-[10px] text-slate-500 block mb-1">BESS运行辅耗 (kW)</label>
              <input v-model.number="simParams.bessAuxRun" type="number" step="0.1"
                class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 focus:outline-none">
            </div>
            <div>
              <label class="text-[10px] text-slate-500 block mb-1">BESS待机辅耗 (kW)</label>
              <input v-model.number="simParams.bessAuxStandby" type="number" step="0.1"
                class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 focus:outline-none">
            </div>
            <div>
              <label class="text-[10px] text-slate-500 block mb-1">PCS运行辅耗 (kW)</label>
              <input v-model.number="simParams.pcsAuxRun" type="number" step="0.1"
                class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 focus:outline-none">
            </div>
            <div>
              <label class="text-[10px] text-slate-500 block mb-1">PCS待机辅耗 (kW)</label>
              <input v-model.number="simParams.pcsAuxStandby" type="number" step="0.1"
                class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 focus:outline-none">
            </div>
          </div>
        </div>
      </div>

      <div class="mt-4 flex justify-between">
        <button @click="prevStep" 
          class="bg-slate-700 hover:bg-slate-600 text-slate-300 text-xs px-4 py-2 rounded transition-all">
          上一步
        </button>
        <button @click="nextStep" 
          class="bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 hover:to-emerald-600 text-white text-xs px-4 py-2 rounded transition-all">
          下一步：选择仿真算法
        </button>
      </div>
    </div>

    <!-- 步骤3: 仿真算法选择 -->
    <div v-show="currentStep === 2" class="bg-slate-900/40 rounded-lg border border-slate-800 p-4">
      <h3 class="text-sm font-bold text-teal-400 mb-3 flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-teal-400"></span>
        仿真算法选择
      </h3>

      <div class="grid grid-cols-3 gap-3">
        <!-- 算法选择卡片 -->
        <div v-for="algo in algorithms" :key="algo.id"
          @click="selectedAlgorithm = algo.id"
          :class="['bg-slate-800/50 rounded-lg p-4 border-2 cursor-pointer transition-all',
            selectedAlgorithm === algo.id ? 'border-teal-500 bg-teal-500/10' : 'border-slate-700 hover:border-slate-500']">
          <div class="flex items-center gap-2 mb-2">
            <span :class="['w-4 h-4 rounded-full', selectedAlgorithm === algo.id ? 'bg-teal-500' : 'bg-slate-600']"></span>
            <h4 class="text-xs font-bold" :class="selectedAlgorithm === algo.id ? 'text-teal-400' : 'text-slate-300'">
              {{ algo.name }}
            </h4>
          </div>
          <p class="text-[10px] text-slate-400 mb-2">{{ algo.description }}</p>
          <div class="text-[10px] text-slate-500">
            <span class="inline-block bg-slate-700 rounded px-1.5 py-0.5 mr-1">{{ algo.type }}</span>
            <span class="text-slate-400">精度: {{ algo.accuracy }}</span>
          </div>
        </div>
      </div>

      <!-- 算法参数调整 -->
      <div v-if="selectedAlgorithm === 'arrhenius'" class="mt-4 bg-slate-800/30 rounded p-3 border border-slate-700">
        <h4 class="text-xs text-slate-300 mb-2 font-medium">阿伦尼乌斯模型参数</h4>
        <div class="grid grid-cols-4 gap-3">
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">A_cal (日历老化系数)</label>
            <input v-model.number="algoParams.A_cal" type="number" step="0.001"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 focus:outline-none">
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">Ea_cal (活化能 kJ/mol)</label>
            <input v-model.number="algoParams.Ea_cal" type="number" step="1"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 focus:outline-none">
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">alpha (时间指数)</label>
            <input v-model.number="algoParams.alpha" type="number" step="0.01" min="0.3" max="0.7"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 focus:outline-none">
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">A_cyc (循环老化系数)</label>
            <input v-model.number="algoParams.A_cyc" type="number" step="0.0001"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 focus:outline-none">
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">Ea_cyc (活化能 kJ/mol)</label>
            <input v-model.number="algoParams.Ea_cyc" type="number" step="1"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 focus:outline-none">
          </div>
          <div>
            <label class="text-[10px] text-slate-500 block mb-1">beta (循环指数)</label>
            <input v-model.number="algoParams.beta" type="number" step="0.01" min="0.5" max="1.0"
              class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 focus:outline-none">
          </div>
        </div>
      </div>

      <div class="mt-4 flex justify-between">
        <button @click="prevStep" 
          class="bg-slate-700 hover:bg-slate-600 text-slate-300 text-xs px-4 py-2 rounded transition-all">
          上一步
        </button>
        <button @click="nextStep" 
          class="bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 hover:to-emerald-600 text-white text-xs px-4 py-2 rounded transition-all">
          下一步：校正因子设置
        </button>
      </div>
    </div>

    <!-- 步骤4: 手工校正因子 -->
    <div v-show="currentStep === 3" class="bg-slate-900/40 rounded-lg border border-slate-800 p-4">
      <h3 class="text-sm font-bold text-teal-400 mb-3 flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-teal-400"></span>
        手工校正因子设置
      </h3>

      <div class="grid grid-cols-2 gap-4">
        <!-- 全局校正因子 -->
        <div class="bg-slate-800/30 rounded p-3 border border-slate-700">
          <h4 class="text-xs text-slate-300 mb-2 font-medium">全局校正因子</h4>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="text-[10px] text-slate-500 block mb-1">SOH校正系数</label>
              <input v-model.number="correctionFactors.sohFactor" type="number" step="0.01" min="0.9" max="1.1"
                class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 focus:outline-none">
              <p class="text-[10px] text-slate-500 mt-1">范围: 0.9-1.1，默认1.0</p>
            </div>
            <div>
              <label class="text-[10px] text-slate-500 block mb-1">RTE校正系数</label>
              <input v-model.number="correctionFactors.rteFactor" type="number" step="0.01" min="0.9" max="1.1"
                class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 focus:outline-none">
              <p class="text-[10px] text-slate-500 mt-1">范围: 0.9-1.1，默认1.0</p>
            </div>
            <div>
              <label class="text-[10px] text-slate-500 block mb-1">容量校正系数</label>
              <input v-model.number="correctionFactors.capacityFactor" type="number" step="0.01" min="0.9" max="1.1"
                class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 focus:outline-none">
              <p class="text-[10px] text-slate-500 mt-1">范围: 0.9-1.1，默认1.0</p>
            </div>
            <div>
              <label class="text-[10px] text-slate-500 block mb-1">老化加速因子</label>
              <input v-model.number="correctionFactors.agingFactor" type="number" step="0.01" min="1.0" max="1.5"
                class="w-full bg-slate-900 border border-slate-600 rounded px-2 py-1 text-xs focus:border-teal-500 focus:outline-none">
              <p class="text-[10px] text-slate-500 mt-1">范围: 1.0-1.5，默认1.0</p>
            </div>
          </div>
        </div>

        <!-- 年度校正表 -->
        <div class="bg-slate-800/30 rounded p-3 border border-slate-700">
          <h4 class="text-xs text-slate-300 mb-2 font-medium">年度校正表（可选）</h4>
          <div class="overflow-auto max-h-40">
            <table class="w-full text-[10px]">
              <thead class="text-slate-500">
                <tr>
                  <th class="py-1 px-2 text-left">年份</th>
                  <th class="py-1 px-2 text-left">SOH校正</th>
                  <th class="py-1 px-2 text-left">RTE校正</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, idx) in yearlyCorrections" :key="idx" class="border-t border-slate-700">
                  <td class="py-1 px-2 text-slate-400">{{ row.year }}</td>
                  <td class="py-1 px-2">
                    <input v-model.number="row.sohCorrection" type="number" step="0.001"
                      class="w-16 bg-slate-900 border border-slate-600 rounded px-1 py-0.5 text-xs focus:border-teal-500 focus:outline-none">
                  </td>
                  <td class="py-1 px-2">
                    <input v-model.number="row.rteCorrection" type="number" step="0.001"
                      class="w-16 bg-slate-900 border border-slate-600 rounded px-1 py-0.5 text-xs focus:border-teal-500 focus:outline-none">
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- 校正说明 -->
      <div class="mt-3 bg-slate-800/20 rounded p-2 border border-slate-700 text-[10px] text-slate-400">
        <p><strong class="text-slate-300">校正因子说明：</strong></p>
        <ul class="list-disc list-inside mt-1 space-y-0.5">
          <li>校正系数 > 1 表示增加衰减（保守估计）</li>
          <li>校正系数 < 1 表示减少衰减（乐观估计）</li>
          <li>年度校正可针对特定年份进行精细调整</li>
          <li>校正结果将应用于最终仿真输出</li>
        </ul>
      </div>

      <div class="mt-4 flex justify-between">
        <button @click="prevStep" 
          class="bg-slate-700 hover:bg-slate-600 text-slate-300 text-xs px-4 py-2 rounded transition-all">
          上一步
        </button>
        <button @click="runSimulation" 
          class="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white text-xs px-6 py-2 rounded font-bold transition-all shadow-md">
          执行仿真计算
        </button>
      </div>
    </div>

    <!-- 步骤5: 仿真结果 -->
    <div v-show="currentStep === 4" class="bg-slate-900/40 rounded-lg border border-slate-800 p-4">
      <h3 class="text-sm font-bold text-teal-400 mb-3 flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-teal-400"></span>
        仿真结果
      </h3>

      <!-- 结果摘要 -->
      <div class="grid grid-cols-4 gap-3 mb-4">
        <div class="bg-slate-800/50 rounded p-3 border border-slate-700 text-center">
          <p class="text-[10px] text-slate-500">初始SOH</p>
          <p class="text-lg font-bold text-teal-400">{{ simulationResults.initSoh?.toFixed(2) || '--' }}%</p>
        </div>
        <div class="bg-slate-800/50 rounded p-3 border border-slate-700 text-center">
          <p class="text-[10px] text-slate-500">保障年限末SOH</p>
          <p class="text-lg font-bold" :class="simulationResults.guaranteeEndSoh >= simParams.guaranteeSoh ? 'text-emerald-400' : 'text-red-400'">
            {{ simulationResults.guaranteeEndSoh?.toFixed(2) || '--' }}%
          </p>
        </div>
        <div class="bg-slate-800/50 rounded p-3 border border-slate-700 text-center">
          <p class="text-[10px] text-slate-500">仿真年限末SOH</p>
          <p class="text-lg font-bold text-sky-400">{{ simulationResults.finalSoh?.toFixed(2) || '--' }}%</p>
        </div>
        <div class="bg-slate-800/50 rounded p-3 border border-slate-700 text-center">
          <p class="text-[10px] text-slate-500">保障判定</p>
          <p class="text-lg font-bold" :class="simulationResults.meetsGuarantee ? 'text-emerald-400' : 'text-red-400'">
            {{ simulationResults.meetsGuarantee ? '达标' : '未达标' }}
          </p>
        </div>
      </div>

      <!-- SOH曲线图 -->
      <div class="bg-slate-800/30 rounded p-3 border border-slate-700">
        <h4 class="text-xs text-slate-300 mb-2 font-medium">SOH衰减曲线</h4>
        <div ref="chartContainer" class="h-48"></div>
      </div>

      <!-- 数据表格 -->
      <div class="mt-3 bg-slate-800/30 rounded p-3 border border-slate-700 overflow-auto max-h-32">
        <table class="w-full text-[10px]">
          <thead class="text-slate-500">
            <tr>
              <th class="py-1 px-2 text-left">年份</th>
              <th class="py-1 px-2 text-left">SOH (%)</th>
              <th class="py-1 px-2 text-left">RTE (%)</th>
              <th class="py-1 px-2 text-left">净可用 (MWh)</th>
              <th class="py-1 px-2 text-left">保障线</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, idx) in simulationResults.tableData" :key="idx" 
              :class="['border-t border-slate-700', row.meetsReq ? '' : 'bg-red-500/10']">
              <td class="py-1 px-2 text-slate-400">{{ row.year }}</td>
              <td class="py-1 px-2 text-teal-400">{{ row.soh.toFixed(2) }}</td>
              <td class="py-1 px-2 text-sky-400">{{ row.rte.toFixed(2) }}</td>
              <td class="py-1 px-2 text-emerald-400">{{ row.netAvail.toFixed(1) }}</td>
              <td class="py-1 px-2" :class="row.meetsReq ? 'text-emerald-400' : 'text-red-400'">
                {{ row.meetsReq ? '达标' : '未达标' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="mt-4 flex justify-between">
        <button @click="resetSimulation" 
          class="bg-slate-700 hover:bg-slate-600 text-slate-300 text-xs px-4 py-2 rounded transition-all">
          重新仿真
        </button>
        <button @click="exportResults" 
          class="bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 hover:to-emerald-600 text-white text-xs px-4 py-2 rounded transition-all">
          导出结果
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'

const steps = [
  { label: '调研表数据' },
  { label: '参数补全' },
  { label: '算法选择' },
  { label: '校正因子' },
  { label: '仿真结果' },
]

const currentStep = ref(0)
const surveyId = ref('')
const selectedAlgorithm = ref('arrhenius')

// 调研表数据
const surveyData = reactive({
  projectName: '',
  ratedEnergy: 5,
  containerQty: 62,
  pcsQty: 1,
  temperature: 25,
  cyclesPerDay: 1,
  dod: 100,
  cRate: 0.5,
  batteryType: 'LFP',
  location: '',
})

// 仿真参数
const simParams = reactive({
  simulationYears: 25,
  guaranteeYears: 10,
  guaranteeSoh: 70,
  requiredEnergy: 240,
  initRte: 94.1,
  acEfficiency: 97.03,
  dcEfficiency: 98.5,
  selfDischarge: 2,
  bessAuxRun: 18.124,
  bessAuxStandby: 3.5,
  pcsAuxRun: 6.5,
  pcsAuxStandby: 1.0,
})

// 算法列表
const algorithms = [
  { id: 'arrhenius', name: '阿伦尼乌斯模型', description: '基于温度活化能的经典衰减模型', type: '物理模型', accuracy: '±5%' },
  { id: 'empirical', name: '经验公式模型', description: '基于历史数据的统计回归模型', type: '统计模型', accuracy: '±8%' },
  { id: 'ml', name: '机器学习模型', description: '基于神经网络的预测模型', type: 'AI模型', accuracy: '±3%' },
]

// 算法参数
const algoParams = reactive({
  A_cal: 0.003,
  Ea_cal: 25,
  alpha: 0.5,
  A_cyc: 0.0002,
  Ea_cyc: 20,
  beta: 0.7,
})

// 校正因子
const correctionFactors = reactive({
  sohFactor: 1.0,
  rteFactor: 1.0,
  capacityFactor: 1.0,
  agingFactor: 1.0,
})

// 年度校正表
const yearlyCorrections = ref([])
const initYearlyCorrections = () => {
  yearlyCorrections.value = []
  for (let i = 0; i <= simParams.simulationYears; i++) {
    yearlyCorrections.value.push({
      year: i,
      sohCorrection: 0,
      rteCorrection: 0,
    })
  }
}
initYearlyCorrections()

// 仿真结果
const simulationResults = reactive({
  initSoh: null,
  guaranteeEndSoh: null,
  finalSoh: null,
  meetsGuarantee: false,
  sohCurve: [],
  rteCurve: [],
  netAvailCurve: [],
  tableData: [],
})

const chartContainer = ref(null)
let chartInstance = null

// 加载调研表数据
const loadSurveyData = async () => {
  if (!surveyId.value) {
    alert('请输入调研表ID')
    return
  }
  // 模拟从后端加载数据
  try {
    const resp = await fetch(`/api/survey/${surveyId.value}`)
    if (resp.ok) {
      const data = await resp.json()
      Object.assign(surveyData, data)
    } else {
      alert('调研表ID不存在，请手动填写数据')
    }
  } catch {
    alert('网络错误，请手动填写数据')
  }
}

// 步骤导航
const nextStep = () => {
  if (currentStep.value < steps.length - 1) {
    currentStep.value++
  }
}

const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

// 执行仿真计算
const runSimulation = () => {
  currentStep.value = 4
  
  const N = simParams.simulationYears + 1
  const sohCurve = []
  const rteCurve = []
  const netAvailCurve = []
  
  // 阿伦尼乌斯模型计算
  const R = 8.314 // J/(mol·K)
  const T = (surveyData.temperature + 273.15) // Kelvin
  
  for (let i = 0; i < N; i++) {
    const t = i // 年
    const N_cycles = surveyData.cyclesPerDay * 365 * t // 总循环次数
    
    // 日历老化
    const Q_cal = algoParams.A_cal * Math.exp(-algoParams.Ea_cal * 1000 / (R * T)) * Math.pow(t + 0.5, algoParams.alpha)
    
    // 循环老化
    const DOD_factor = Math.pow(surveyData.dod / 100, 0.5)
    const C_rate_factor = Math.pow(surveyData.cRate, 0.3)
    const Q_cyc = algoParams.A_cyc * Math.exp(-algoParams.Ea_cyc * 1000 / (R * T)) * Math.pow(N_cycles, algoParams.beta) * DOD_factor * C_rate_factor
    
    // 总衰减
    let soh = 1 - (Q_cal + Q_cyc)
    
    // 应用校正因子
    soh = soh * correctionFactors.sohFactor
    if (yearlyCorrections.value[i]?.sohCorrection) {
      soh += yearlyCorrections.value[i].sohCorrection
    }
    
    // RTE衰减
    let rte = simParams.initRte / 100 - 0.002 * i * correctionFactors.rteFactor
    if (yearlyCorrections.value[i]?.rteCorrection) {
      rte += yearlyCorrections.value[i].rteCorrection
    }
    
    // 净可用能量
    const grossEnergy = surveyData.ratedEnergy * surveyData.containerQty * (surveyData.dod / 100) * rte * soh * (simParams.acEfficiency / 100)
    const auxEnergy = (simParams.bessAuxRun + simParams.pcsAuxRun) * simParams.simulationYears / 1000
    const netAvail = Math.max(0, grossEnergy - auxEnergy) * correctionFactors.capacityFactor
    
    sohCurve.push(soh * 100)
    rteCurve.push(rte * 100)
    netAvailCurve.push(netAvail)
  }
  
  // 填充结果
  simulationResults.sohCurve = sohCurve
  simulationResults.rteCurve = rteCurve
  simulationResults.netAvailCurve = netAvailCurve
  simulationResults.initSoh = sohCurve[0]
  simulationResults.guaranteeEndSoh = sohCurve[simParams.guaranteeYears]
  simulationResults.finalSoh = sohCurve[N - 1]
  simulationResults.meetsGuarantee = sohCurve[simParams.guaranteeYears] >= simParams.guaranteeSoh
  
  // 表格数据
  simulationResults.tableData = []
  for (let i = 0; i < N; i++) {
    simulationResults.tableData.push({
      year: i,
      soh: sohCurve[i],
      rte: rteCurve[i],
      netAvail: netAvailCurve[i],
      meetsReq: netAvailCurve[i] >= simParams.requiredEnergy,
    })
  }
  
  // 渲染图表
  nextTick(() => {
    renderChart()
  })
}

// 渲染图表
const renderChart = () => {
  if (!chartContainer.value) return
  
  if (chartInstance) {
    chartInstance.dispose()
  }
  
  chartInstance = echarts.init(chartContainer.value)
  
  const years = Array.from({ length: simulationResults.sohCurve.length }, (_, i) => i)
  
  chartInstance.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: ['SOH', 'RTE', '保障线'], top: 0, textStyle: { color: '#94a3b8', fontSize: 10 } },
    grid: { left: 40, right: 20, top: 30, bottom: 20 },
    xAxis: { type: 'category', data: years, axisLabel: { color: '#64748b', fontSize: 10 } },
    yAxis: { type: 'value', min: 50, max: 100, axisLabel: { color: '#64748b', fontSize: 10 } },
    series: [
      { name: 'SOH', type: 'line', data: simulationResults.sohCurve, smooth: true, lineStyle: { color: '#14b8a6' }, itemStyle: { color: '#14b8a6' } },
      { name: 'RTE', type: 'line', data: simulationResults.rteCurve, smooth: true, lineStyle: { color: '#0ea5e9' }, itemStyle: { color: '#0ea5e9' } },
      { name: '保障线', type: 'line', data: Array.from({ length: years.length }, () => simParams.guaranteeSoh), lineStyle: { color: '#f59e0b', type: 'dashed' }, itemStyle: { color: '#f59e0b' } },
    ],
  })
}

// 重置仿真
const resetSimulation = () => {
  currentStep.value = 0
  simulationResults.initSoh = null
  simulationResults.guaranteeEndSoh = null
  simulationResults.finalSoh = null
  simulationResults.meetsGuarantee = false
  simulationResults.sohCurve = []
  simulationResults.rteCurve = []
  simulationResults.netAvailCurve = []
  simulationResults.tableData = []
}

// 导出结果
const exportResults = () => {
  const csvContent = '年份,SOH(%),RTE(%),净可用(MWh),保障判定\n' +
    simulationResults.tableData.map(row => 
      `${row.year},${row.soh.toFixed(2)},${row.rte.toFixed(2)},${row.netAvail.toFixed(1)},${row.meetsReq ? '达标' : '未达标'}`
    ).join('\n')
  
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `仿真结果_${surveyData.projectName || '未命名'}_${new Date().toISOString().slice(0,10)}.csv`
  link.click()
}

onMounted(() => {
  initYearlyCorrections()
})
</script>

<style scoped>
.tab-btn {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  transition: all 0.2s;
}
.tab-btn.active {
  background: rgba(20, 184, 166, 0.2);
  color: #14b8a6;
  border: 1px solid rgba(20, 184, 166, 0.3);
}
</style>