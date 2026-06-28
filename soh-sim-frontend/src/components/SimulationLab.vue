<template>
  <div class="flex flex-col gap-4 h-full overflow-auto p-4">
    <div class="flex items-center gap-2 p-2 rounded-lg" style="background-color: var(--color-step-bg); border: 1px solid var(--color-step-border);">
      <div v-for="(step, idx) in steps" :key="idx" 
        :class="['flex items-center gap-1 px-3 py-1 rounded text-xs transition-all',
          currentStep >= idx ? 'text-teal-400' : 'text-slate-500']"
        :style="currentStep >= idx ? { backgroundColor: 'var(--color-step-active)', border: '1px solid var(--color-accent)' } : {}">
        <span class="w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold"
          :style="currentStep >= idx ? { backgroundColor: 'var(--color-accent)', color: 'white' } : { backgroundColor: 'var(--color-text-muted)', color: 'var(--color-text-light)' }">
          {{ idx + 1 }}
        </span>
        {{ step.label }}
      </div>
    </div>

    <div v-show="currentStep === 0" class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
      <h3 class="text-sm font-bold mb-3 flex items-center gap-2" style="color: var(--color-accent);">
        <span class="w-2 h-2 rounded-full" style="background-color: var(--color-accent);"></span>
        调研表数据获取
      </h3>
      
      <div class="grid grid-cols-2 gap-4">
        <div class="space-y-2">
          <label class="text-xs" style="color: var(--color-text-secondary);">调研表串码ID</label>
          <div class="flex gap-2">
            <input v-model="surveyId" type="text" placeholder="输入调研表ID或扫描二维码"
              class="flex-1 rounded px-3 py-1.5 text-xs" 
              style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border);"
              onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
              onblur="this.style.borderColor='var(--color-input-border)';">
            <button @click="loadSurveyData" 
              class="text-xs px-3 py-1.5 rounded transition-all"
              style="background-color: var(--color-accent); color: white;"
              onmouseover="this.style.opacity='0.9';"
              onmouseout="this.style.opacity='1';">
              加载
            </button>
          </div>
        </div>

        <div class="space-y-2">
          <label class="text-xs" style="color: var(--color-text-secondary);">项目名称搜索</label>
          <div class="flex gap-2">
            <input v-model="searchKeyword" type="text" placeholder="输入项目名称搜索"
              class="flex-1 rounded px-3 py-1.5 text-xs" 
              style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border);"
              onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
              onblur="this.style.borderColor='var(--color-input-border)';">
            <button @click="searchByProjectName" 
              class="text-xs px-3 py-1.5 rounded transition-all"
              style="background-color: var(--color-info); color: white;"
              onmouseover="this.style.opacity='0.9';"
              onmouseout="this.style.opacity='1';">
              搜索
            </button>
          </div>
        </div>
      </div>

      <div v-if="searchResults.length > 0" class="mt-4 rounded-lg p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
        <h4 class="text-xs font-medium mb-2" style="color: var(--color-text);">搜索结果</h4>
        <div class="max-h-40 overflow-auto">
          <div v-for="item in searchResults" :key="item.id"
            @click="selectSurvey(item)"
            class="flex justify-between items-center p-2 rounded cursor-pointer transition-all mb-1"
            style="background-color: var(--color-card); border: 1px solid var(--color-border);"
            onmouseover="this.style.backgroundColor='var(--color-step-active)'; this.style.borderColor='var(--color-accent)';"
            onmouseout="this.style.backgroundColor='var(--color-card)'; this.style.borderColor='var(--color-border)';">
            <div>
              <p class="text-xs" style="color: var(--color-accent);">{{ item.project_name }}</p>
              <p class="text-[10px]" style="color: var(--color-text-muted);">{{ item.location }} | {{ item.total_mw }}MW / {{ item.total_mwh }}MWh</p>
            </div>
            <span class="text-[10px] px-2 py-1 rounded" style="background-color: var(--color-accent); color: white;">选择</span>
          </div>
        </div>
      </div>

      <div class="mt-4 grid grid-cols-3 gap-3">
        <div class="rounded p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">额定能量 (MWh)</label>
          <input v-model.number="surveyData.ratedEnergy" type="number" step="0.1"
            class="w-full rounded px-2 py-1 text-xs" 
            style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border); color: var(--color-accent);"
            onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
            onblur="this.style.borderColor='var(--color-input-border)';">
        </div>
        <div class="rounded p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">集装箱数量</label>
          <input v-model.number="surveyData.containerQty" type="number"
            class="w-full rounded px-2 py-1 text-xs" 
            style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border); color: var(--color-accent);"
            onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
            onblur="this.style.borderColor='var(--color-input-border)';">
        </div>
        <div class="rounded p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">PCS数量</label>
          <input v-model.number="surveyData.pcsQty" type="number"
            class="w-full rounded px-2 py-1 text-xs" 
            style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border); color: var(--color-accent);"
            onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
            onblur="this.style.borderColor='var(--color-input-border)';">
        </div>
        <div class="rounded p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">运行温度 (°C)</label>
          <input v-model.number="surveyData.temperature" type="number" step="0.5"
            class="w-full rounded px-2 py-1 text-xs" 
            style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border); color: var(--color-accent);"
            onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
            onblur="this.style.borderColor='var(--color-input-border)';">
        </div>
        <div class="rounded p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">每日循环次数</label>
          <input v-model.number="surveyData.cyclesPerDay" type="number" step="0.5"
            class="w-full rounded px-2 py-1 text-xs" 
            style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border); color: var(--color-accent);"
            onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
            onblur="this.style.borderColor='var(--color-input-border)';">
        </div>
        <div class="rounded p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">DOD (%)</label>
          <input v-model.number="surveyData.dod" type="number" step="1" min="0" max="100"
            class="w-full rounded px-2 py-1 text-xs" 
            style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border); color: var(--color-accent);"
            onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
            onblur="this.style.borderColor='var(--color-input-border)';">
        </div>
        <div class="rounded p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">倍率 (C)</label>
          <input v-model.number="surveyData.cRate" type="number" step="0.1" min="0.1" max="2"
            class="w-full rounded px-2 py-1 text-xs" 
            style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border); color: var(--color-accent);"
            onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
            onblur="this.style.borderColor='var(--color-input-border)';">
        </div>
        <div class="rounded p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">电池类型</label>
          <select v-model="surveyData.batteryType"
            class="w-full rounded px-2 py-1 text-xs" 
            style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border); color: var(--color-accent);"
            onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
            onblur="this.style.borderColor='var(--color-input-border)';">
            <option value="LFP">LFP (磷酸铁锂)</option>
            <option value="NCM">NCM (三元锂)</option>
            <option value="LTO">LTO (钛酸锂)</option>
          </select>
        </div>
        <div class="rounded p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">项目地点</label>
          <input v-model="surveyData.location" type="text"
            class="w-full rounded px-2 py-1 text-xs" 
            style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border); color: var(--color-accent);"
            onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
            onblur="this.style.borderColor='var(--color-input-border)';">
        </div>
      </div>

      <div class="mt-4 flex justify-end">
        <button @click="nextStep" 
          class="text-xs px-4 py-2 rounded transition-all"
          style="background: linear-gradient(135deg, var(--color-accent), var(--color-accent-secondary)); color: white;"
          onmouseover="this.style.opacity='0.9';"
          onmouseout="this.style.opacity='1';">
          下一步：补全仿真参数
        </button>
      </div>
    </div>

    <div v-show="currentStep === 1" class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
      <h3 class="text-sm font-bold mb-3 flex items-center gap-2" style="color: var(--color-accent);">
        <span class="w-2 h-2 rounded-full" style="background-color: var(--color-accent);"></span>
        仿真参数补全
      </h3>

      <div class="grid grid-cols-4 gap-3">
        <div class="col-span-4 rounded p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <h4 class="text-xs mb-2 font-medium" style="color: var(--color-text);">基础配置</h4>
          <div class="grid grid-cols-4 gap-3">
            <div>
              <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">仿真年限 (年)</label>
              <select v-model.number="simParams.simulationYears" @change="initYearlyCorrections"
                class="w-full rounded px-2 py-1 text-xs" 
                style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border);"
                onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                onblur="this.style.borderColor='var(--color-input-border)';">
                <option value="10">10年</option>
                <option value="15">15年</option>
                <option value="20">20年</option>
                <option value="25">25年</option>
                <option value="30">30年</option>
              </select>
            </div>
            <div>
              <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">最低保障年限 (年)</label>
              <select v-model.number="simParams.guaranteeYears"
                class="w-full rounded px-2 py-1 text-xs" 
                style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border);"
                onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                onblur="this.style.borderColor='var(--color-input-border)';">
                <option value="5">5年</option>
                <option value="10">10年</option>
                <option value="15">15年</option>
                <option value="20">20年</option>
              </select>
            </div>
            <div>
              <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">保障SOH底线 (%)</label>
              <input v-model.number="simParams.guaranteeSoh" type="number" step="1" min="60" max="90"
                class="w-full rounded px-2 py-1 text-xs" 
                style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border);"
                onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                onblur="this.style.borderColor='var(--color-input-border)';">
            </div>
            <div>
              <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">承诺能量底线 (MWh)</label>
              <input v-model.number="simParams.requiredEnergy" type="number" step="1"
                class="w-full rounded px-2 py-1 text-xs" 
                style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border);"
                onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                onblur="this.style.borderColor='var(--color-input-border)';">
            </div>
          </div>
        </div>

        <div class="col-span-2 rounded p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <h4 class="text-xs mb-2 font-medium" style="color: var(--color-text);">效率参数</h4>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">初始RTE (%)</label>
              <input v-model.number="simParams.initRte" type="number" step="0.1" min="85" max="95"
                class="w-full rounded px-2 py-1 text-xs" 
                style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border);"
                onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                onblur="this.style.borderColor='var(--color-input-border)';">
            </div>
            <div>
              <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">AC效率 (%)</label>
              <input v-model.number="simParams.acEfficiency" type="number" step="0.1" min="95" max="99"
                class="w-full rounded px-2 py-1 text-xs" 
                style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border);"
                onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                onblur="this.style.borderColor='var(--color-input-border)';">
            </div>
            <div>
              <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">DC效率 (%)</label>
              <input v-model.number="simParams.dcEfficiency" type="number" step="0.1" min="95" max="99"
                class="w-full rounded px-2 py-1 text-xs" 
                style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border);"
                onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                onblur="this.style.borderColor='var(--color-input-border)';">
            </div>
            <div>
              <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">自放电率 (%/月)</label>
              <input v-model.number="simParams.selfDischarge" type="number" step="0.1" min="0" max="5"
                class="w-full rounded px-2 py-1 text-xs" 
                style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border);"
                onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                onblur="this.style.borderColor='var(--color-input-border)';">
            </div>
          </div>
        </div>

        <div class="col-span-2 rounded p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <h4 class="text-xs mb-2 font-medium" style="color: var(--color-text);">辅耗参数</h4>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">BESS运行辅耗 (kW)</label>
              <input v-model.number="simParams.bessAuxRun" type="number" step="0.1"
                class="w-full rounded px-2 py-1 text-xs" 
                style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border);"
                onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                onblur="this.style.borderColor='var(--color-input-border)';">
            </div>
            <div>
              <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">BESS待机辅耗 (kW)</label>
              <input v-model.number="simParams.bessAuxStandby" type="number" step="0.1"
                class="w-full rounded px-2 py-1 text-xs" 
                style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border);"
                onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                onblur="this.style.borderColor='var(--color-input-border)';">
            </div>
            <div>
              <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">PCS运行辅耗 (kW)</label>
              <input v-model.number="simParams.pcsAuxRun" type="number" step="0.1"
                class="w-full rounded px-2 py-1 text-xs" 
                style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border);"
                onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                onblur="this.style.borderColor='var(--color-input-border)';">
            </div>
            <div>
              <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">PCS待机辅耗 (kW)</label>
              <input v-model.number="simParams.pcsAuxStandby" type="number" step="0.1"
                class="w-full rounded px-2 py-1 text-xs" 
                style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border);"
                onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                onblur="this.style.borderColor='var(--color-input-border)';">
            </div>
          </div>
        </div>
      </div>

      <div class="mt-4 flex justify-between">
        <button @click="prevStep" 
          class="text-xs px-4 py-2 rounded transition-all"
          style="background-color: var(--color-card-dark); color: var(--color-text); border: 1px solid var(--color-border);"
          onmouseover="this.style.backgroundColor='var(--color-tab-hover)';"
          onmouseout="this.style.backgroundColor='var(--color-card-dark)';">
          上一步
        </button>
        <button @click="nextStep" 
          class="text-xs px-4 py-2 rounded transition-all"
          style="background: linear-gradient(135deg, var(--color-accent), var(--color-accent-secondary)); color: white;"
          onmouseover="this.style.opacity='0.9';"
          onmouseout="this.style.opacity='1';">
          下一步：选择仿真算法
        </button>
      </div>
    </div>

    <div v-show="currentStep === 2" class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
      <h3 class="text-sm font-bold mb-3 flex items-center gap-2" style="color: var(--color-accent);">
        <span class="w-2 h-2 rounded-full" style="background-color: var(--color-accent);"></span>
        仿真算法选择
      </h3>

      <div class="grid grid-cols-3 gap-3">
        <div v-for="algo in algorithms" :key="algo.id"
          @click="selectAlgorithm(algo)"
          class="rounded-lg p-4 border-2 cursor-pointer transition-all"
          :style="selectedAlgorithm === algo.id ? { backgroundColor: 'var(--color-step-active)', borderColor: 'var(--color-accent)' } : { backgroundColor: 'var(--color-card-dark)', borderColor: 'var(--color-border)' }">
          <div class="flex items-center gap-2 mb-2">
            <span class="w-4 h-4 rounded-full" :style="selectedAlgorithm === algo.id ? { backgroundColor: 'var(--color-accent)' } : { backgroundColor: 'var(--color-text-muted)' }"></span>
            <h4 class="text-xs font-bold" :style="selectedAlgorithm === algo.id ? { color: 'var(--color-accent)' } : { color: 'var(--color-text)' }">
              {{ algo.name }}
            </h4>
          </div>
          <p class="text-[10px] mb-2" style="color: var(--color-text-secondary);">{{ algo.description }}</p>
          <div class="text-[10px]" style="color: var(--color-text-muted);">
            <span class="inline-block rounded px-1.5 py-0.5 mr-1" style="background-color: var(--color-card);">{{ algo.type }}</span>
            <span style="color: var(--color-text-secondary);">精度: {{ algo.accuracy }}</span>
          </div>
          <div class="mt-2 text-[10px] font-mono truncate" style="color: var(--color-accent); opacity: 0.8;">
            {{ algo.mathematical_form }}
          </div>
        </div>
      </div>

      <div v-if="algorithms.length === 0" class="text-center py-8" style="color: var(--color-text-muted);">
        <div>暂无算法模型，请先在算法公式试验舱中添加或初始化</div>
      </div>

      <div v-if="selectedAlgoDetail" class="mt-4 rounded p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
        <div class="flex justify-between items-center mb-2">
          <h4 class="text-xs font-medium" style="color: var(--color-text);">{{ selectedAlgoDetail.name }} 参数</h4>
          <button @click="resetAlgoParams" class="text-[10px] rounded px-2 py-0.5 transition-colors" style="background-color: var(--color-card); color: var(--color-text-muted);">
            恢复默认
          </button>
        </div>
        <div class="grid grid-cols-4 gap-3">
          <div v-for="(param, key) in selectedAlgoDetail.parameters" :key="key">
            <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">{{ param.label }} ({{ param.unit || '' }})</label>
            <input v-model.number="algoParams[key]" type="number" 
              :step="param.step || 0.01" 
              :min="param.min" 
              :max="param.max"
              class="w-full rounded px-2 py-1 text-xs" 
              style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border);"
              onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
              onblur="this.style.borderColor='var(--color-input-border)';">
          </div>
        </div>
      </div>

      <div class="mt-4 flex justify-between">
        <button @click="prevStep" 
          class="text-xs px-4 py-2 rounded transition-all"
          style="background-color: var(--color-card-dark); color: var(--color-text); border: 1px solid var(--color-border);"
          onmouseover="this.style.backgroundColor='var(--color-tab-hover)';"
          onmouseout="this.style.backgroundColor='var(--color-card-dark)';">
          上一步
        </button>
        <button @click="nextStep" 
          class="text-xs px-4 py-2 rounded transition-all"
          style="background: linear-gradient(135deg, var(--color-accent), var(--color-accent-secondary)); color: white;"
          onmouseover="this.style.opacity='0.9';"
          onmouseout="this.style.opacity='1';">
          下一步：校正因子设置
        </button>
      </div>
    </div>

    <div v-show="currentStep === 3" class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
      <h3 class="text-sm font-bold mb-3 flex items-center gap-2" style="color: var(--color-accent);">
        <span class="w-2 h-2 rounded-full" style="background-color: var(--color-accent);"></span>
        手工校正因子设置
      </h3>

      <div class="grid grid-cols-2 gap-4">
        <div class="rounded p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <h4 class="text-xs mb-2 font-medium" style="color: var(--color-text);">全局校正因子</h4>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">SOH校正系数</label>
              <input v-model.number="correctionFactors.sohFactor" type="number" step="0.01" min="0.9" max="1.1"
                class="w-full rounded px-2 py-1 text-xs" 
                style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border);"
                onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                onblur="this.style.borderColor='var(--color-input-border)';">
              <p class="text-[10px] mt-1" style="color: var(--color-text-muted);">范围: 0.9-1.1，默认1.0</p>
            </div>
            <div>
              <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">RTE校正系数</label>
              <input v-model.number="correctionFactors.rteFactor" type="number" step="0.01" min="0.9" max="1.1"
                class="w-full rounded px-2 py-1 text-xs" 
                style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border);"
                onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                onblur="this.style.borderColor='var(--color-input-border)';">
              <p class="text-[10px] mt-1" style="color: var(--color-text-muted);">范围: 0.9-1.1，默认1.0</p>
            </div>
            <div>
              <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">容量校正系数</label>
              <input v-model.number="correctionFactors.capacityFactor" type="number" step="0.01" min="0.9" max="1.1"
                class="w-full rounded px-2 py-1 text-xs" 
                style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border);"
                onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                onblur="this.style.borderColor='var(--color-input-border)';">
              <p class="text-[10px] mt-1" style="color: var(--color-text-muted);">范围: 0.9-1.1，默认1.0</p>
            </div>
            <div>
              <label class="text-[10px] block mb-1" style="color: var(--color-text-muted);">老化加速因子</label>
              <input v-model.number="correctionFactors.agingFactor" type="number" step="0.01" min="1.0" max="1.5"
                class="w-full rounded px-2 py-1 text-xs" 
                style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border);"
                onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                onblur="this.style.borderColor='var(--color-input-border)';">
              <p class="text-[10px] mt-1" style="color: var(--color-text-muted);">范围: 1.0-1.5，默认1.0</p>
            </div>
          </div>
        </div>

        <div class="rounded p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <h4 class="text-xs mb-2 font-medium" style="color: var(--color-text);">年度校正表（可选）</h4>
          <div class="overflow-auto max-h-40">
            <table class="w-full text-[10px]">
              <thead>
                <tr style="color: var(--color-text-muted);">
                  <th class="py-1 px-2 text-left">年份</th>
                  <th class="py-1 px-2 text-left">SOH校正</th>
                  <th class="py-1 px-2 text-left">RTE校正</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, idx) in yearlyCorrections" :key="idx" style="border-top: 1px solid var(--color-border);">
                  <td class="py-1 px-2" style="color: var(--color-text-secondary);">{{ row.year }}</td>
                  <td class="py-1 px-2">
                    <input v-model.number="row.sohCorrection" type="number" step="0.001"
                      class="w-16 rounded px-1 py-0.5 text-xs" 
                      style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border);"
                      onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                      onblur="this.style.borderColor='var(--color-input-border)';">
                  </td>
                  <td class="py-1 px-2">
                    <input v-model.number="row.rteCorrection" type="number" step="0.001"
                      class="w-16 rounded px-1 py-0.5 text-xs" 
                      style="background-color: var(--color-input-bg); border: 1px solid var(--color-input-border);"
                      onfocus="this.style.borderColor='var(--color-input-focus)'; this.style.outline='none';"
                      onblur="this.style.borderColor='var(--color-input-border)';">
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="mt-3 rounded p-2" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
        <p style="color: var(--color-text-secondary); font-size: 10px;"><strong style="color: var(--color-text);">校正因子说明：</strong></p>
        <ul class="list-disc list-inside mt-1 space-y-0.5" style="font-size: 10px; color: var(--color-text-secondary);">
          <li>校正系数 &gt; 1 表示增加衰减（保守估计）</li>
          <li>校正系数 &lt; 1 表示减少衰减（乐观估计）</li>
          <li>年度校正可针对特定年份进行精细调整</li>
          <li>校正结果将应用于最终仿真输出</li>
        </ul>
      </div>

      <div class="mt-4 flex justify-between">
        <button @click="prevStep" 
          class="text-xs px-4 py-2 rounded transition-all"
          style="background-color: var(--color-card-dark); color: var(--color-text); border: 1px solid var(--color-border);"
          onmouseover="this.style.backgroundColor='var(--color-tab-hover)';"
          onmouseout="this.style.backgroundColor='var(--color-card-dark)';">
          上一步
        </button>
        <button @click="runSimulation" :disabled="!selectedAlgorithm"
          class="text-xs px-6 py-2 rounded font-bold transition-all"
          :style="selectedAlgorithm ? { background: 'linear-gradient(135deg, var(--color-success), var(--color-accent))', color: 'white' } : { background: 'var(--color-text-muted)', color: 'var(--color-text-light)' }">
          前端计算
        </button>
        <button @click="runBackendSimulation" :disabled="!selectedAlgorithm"
          class="text-xs px-6 py-2 rounded font-bold transition-all"
          :style="selectedAlgorithm ? { background: 'linear-gradient(135deg, var(--color-accent), var(--color-accent-secondary))', color: 'white' } : { background: 'var(--color-text-muted)', color: 'var(--color-text-light)' }">
          后端引擎计算
        </button>
      </div>
    </div>

    <div v-show="currentStep === 4" class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
      <div class="flex justify-between items-center mb-3">
        <h3 class="text-sm font-bold flex items-center gap-2" style="color: var(--color-accent);">
          <span class="w-2 h-2 rounded-full" style="background-color: var(--color-accent);"></span>
          仿真结果
        </h3>
        <button @click="saveSimulationResult" 
          class="text-xs px-3 py-1.5 rounded transition-all flex items-center gap-1"
          style="background-color: var(--color-info); color: white;"
          onmouseover="this.style.opacity='0.9';"
          onmouseout="this.style.opacity='1';">
          <span>💾</span> 保存结果
        </button>
      </div>

      <div class="grid grid-cols-4 gap-3 mb-4">
        <div class="rounded p-3 text-center" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <p class="text-[10px]" style="color: var(--color-text-muted);">初始SOH</p>
          <p class="text-lg font-bold" style="color: var(--color-accent);">{{ simulationResults.initSoh?.toFixed(2) || '--' }}%</p>
        </div>
        <div class="rounded p-3 text-center" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <p class="text-[10px]" style="color: var(--color-text-muted);">保障年限末SOH</p>
          <p class="text-lg font-bold" :style="simulationResults.guaranteeEndSoh >= simParams.guaranteeSoh ? { color: 'var(--color-success)' } : { color: 'var(--color-danger)' }">
            {{ simulationResults.guaranteeEndSoh?.toFixed(2) || '--' }}%
          </p>
        </div>
        <div class="rounded p-3 text-center" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <p class="text-[10px]" style="color: var(--color-text-muted);">仿真年限末SOH</p>
          <p class="text-lg font-bold" style="color: var(--color-accent-secondary);">{{ simulationResults.finalSoh?.toFixed(2) || '--' }}%</p>
        </div>
        <div class="rounded p-3 text-center" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
          <p class="text-[10px]" style="color: var(--color-text-muted);">保障判定</p>
          <p class="text-lg font-bold" :style="simulationResults.meetsGuarantee ? { color: 'var(--color-success)' } : { color: 'var(--color-danger)' }">
            {{ simulationResults.meetsGuarantee ? '达标' : '未达标' }}
          </p>
        </div>
      </div>

      <div class="rounded p-3" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
        <h4 class="text-xs mb-2 font-medium" style="color: var(--color-text);">SOH衰减曲线</h4>
        <div ref="chartContainer" class="h-48"></div>
      </div>

      <div class="mt-3 rounded p-3 overflow-auto max-h-32" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border);">
        <table class="w-full text-[10px]">
          <thead>
            <tr style="color: var(--color-text-muted);">
              <th class="py-1 px-2 text-left">年份</th>
              <th class="py-1 px-2 text-left">SOH (%)</th>
              <th class="py-1 px-2 text-left">RTE (%)</th>
              <th class="py-1 px-2 text-left">净可用 (MWh)</th>
              <th class="py-1 px-2 text-left">保障线</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, idx) in simulationResults.tableData" :key="idx" 
              :style="[{ borderTop: '1px solid var(--color-border)' }, row.meetsReq ? {} : { backgroundColor: 'rgba(239, 68, 68, 0.1)' }]">
              <td class="py-1 px-2" style="color: var(--color-text-secondary);">{{ row.year }}</td>
              <td class="py-1 px-2" style="color: var(--color-accent);">{{ row.soh.toFixed(2) }}</td>
              <td class="py-1 px-2" style="color: var(--color-accent-secondary);">{{ row.rte.toFixed(2) }}</td>
              <td class="py-1 px-2" style="color: var(--color-success);">{{ row.netAvail.toFixed(1) }}</td>
              <td class="py-1 px-2" :style="row.meetsReq ? { color: 'var(--color-success)' } : { color: 'var(--color-danger)' }">
                {{ row.meetsReq ? '达标' : '未达标' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="mt-4 flex justify-between">
        <button @click="resetSimulation" 
          class="text-xs px-4 py-2 rounded transition-all"
          style="background-color: var(--color-card-dark); color: var(--color-text); border: 1px solid var(--color-border);"
          onmouseover="this.style.backgroundColor='var(--color-tab-hover)';"
          onmouseout="this.style.backgroundColor='var(--color-card-dark)';">
          重新仿真
        </button>
        <button @click="exportResults" 
          class="text-xs px-4 py-2 rounded transition-all"
          style="background: linear-gradient(135deg, var(--color-accent), var(--color-accent-secondary)); color: white;"
          onmouseover="this.style.opacity='0.9';"
          onmouseout="this.style.opacity='1';">
          导出结果
        </button>
      </div>
    </div>

    <div v-if="toast.show" 
      :class="['fixed top-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all',
        toast.type === 'success' ? 'bg-emerald-500 text-white' : 'bg-red-500 text-white']">
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick, watch } from 'vue'
import * as echarts from 'echarts'

const emit = defineEmits(['applyConfig', 'error'])

const steps = [
  { label: '调研表数据' },
  { label: '参数补全' },
  { label: '算法选择' },
  { label: '校正因子' },
  { label: '仿真结果' },
]

const currentStep = ref(0)
const surveyId = ref('')
const searchKeyword = ref('')
const searchResults = ref([])
const selectedAlgorithm = ref('')

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

const algorithms = ref([])
const algoParams = reactive({})
const selectedAlgoDetail = ref(null)

const correctionFactors = reactive({
  sohFactor: 1.0,
  rteFactor: 1.0,
  capacityFactor: 1.0,
  agingFactor: 1.0,
})

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

const toast = reactive({ show: false, message: '', type: 'success' })

const loadSurveyData = async () => {
  if (!surveyId.value) {
    emit('error', '请输入调研表ID', 'warning')
    return
  }
  try {
    const resp = await fetch(`/api/survey/${surveyId.value}`)
    if (resp.ok) {
      const data = await resp.json()
      mapSurveyData(data)
    } else {
      emit('error', '调研表ID不存在，请手动填写数据', 'warning')
    }
  } catch {
    emit('error', '网络错误，请手动填写数据', 'error')
  }
}

const searchByProjectName = async () => {
  if (!searchKeyword.value.trim()) {
    emit('error', '请输入项目名称关键词', 'warning')
    return
  }
  try {
    const resp = await fetch(`/api/survey/search?keyword=${encodeURIComponent(searchKeyword.value)}`)
    const data = await resp.json()
    if (data.success) {
      searchResults.value = data.surveys
      if (data.surveys.length === 0) {
        emit('error', '未找到匹配的项目', 'warning')
      }
    } else {
      emit('error', data.error || '搜索失败', 'error')
    }
  } catch {
    emit('error', '网络错误，搜索失败', 'error')
  }
}

const selectSurvey = (survey) => {
  searchResults.value = []
  searchKeyword.value = survey.project_name
  surveyId.value = survey.id
  mapSurveyData(survey)
}

const mapSurveyData = (data) => {
  surveyData.projectName = data.project_name || ''
  surveyData.ratedEnergy = data.total_mwh || 5
  surveyData.containerQty = data.container_qty || 1
  surveyData.pcsQty = data.pcs_qty || 1
  surveyData.temperature = data.temp_avg || 25
  surveyData.cyclesPerDay = data.cycles_per_day || 1
  surveyData.dod = data.dod || 100
  surveyData.cRate = data.c_rate || 0.5
  surveyData.batteryType = data.battery_type || 'LFP'
  surveyData.location = data.location || ''
  
  simParams.requiredEnergy = data.total_mwh || 240
  simParams.duration = data.duration || 2
  simParams.cyclesPerDay = data.cycles_per_day || 1
}

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

const fetchAlgorithms = async () => {
  try {
    const resp = await fetch('/api/algorithms/public?category=degradation')
    const data = await resp.json()
    if (data.success && data.data.length > 0) {
      algorithms.value = data.data.map(alg => ({
        id: alg.id,
        name: alg.name,
        name_en: alg.name_en || '',
        description: alg.description || '无描述',
        type: getCategoryLabel(alg.category),
        accuracy: alg.accuracy_desc || '未知',
        model_type: alg.model_type,
        parameters: alg.parameters,
        mathematical_form: alg.mathematical_form || '',
        formula_expression: alg.formula_expression || '',
      }))
    }
  } catch (e) {
    console.error('获取算法列表失败:', e)
  }

  if (algorithms.value.length === 0) {
    const { BUILTIN_DEGRADATION_ALGORITHMS, mapToSimulationLabFormat } = await import('../data/builtinAlgorithms.js')
    algorithms.value = BUILTIN_DEGRADATION_ALGORITHMS.map(mapToSimulationLabFormat)
  }

  if (!selectedAlgorithm.value && algorithms.value.length > 0) {
    selectedAlgorithm.value = algorithms.value[0].id
    selectAlgorithm(algorithms.value[0])
  }
}

function getCategoryLabel(category) {
  const labels = {
    degradation: '容量衰减',
    financial: '财务模型',
    engineering: '工程计算',
    simulation: '仿真配置',
  }
  return labels[category] || category
}

const selectAlgorithm = (algo) => {
  selectedAlgorithm.value = algo.id
  selectedAlgoDetail.value = algo
  algoParams.value = {}
  if (algo.parameters) {
    Object.keys(algo.parameters).forEach(key => {
      algoParams[key] = algo.parameters[key].default || 0
    })
  }
}

const resetAlgoParams = () => {
  const algo = selectedAlgoDetail.value
  if (!algo || !algo.parameters) return
  Object.keys(algo.parameters).forEach(key => {
    algoParams[key] = algo.parameters[key].default || 0
  })
  showToast('参数已恢复为默认值')
}

watch(selectedAlgorithm, (newId) => {
  if (newId) {
    const algo = algorithms.value.find(a => a.id === newId)
    if (algo) {
      selectAlgorithm(algo)
    }
  }
})

const calculateSOH = (modelType, params, t) => {
  const R = 8.314
  const T = surveyData.temperature + 273.15
  const N_cycles = surveyData.cyclesPerDay * 365 * t
  const DOD_factor = Math.pow(surveyData.dod / 100, 0.5)
  const C_rate_factor = Math.pow(surveyData.cRate, 0.3)

  switch (modelType) {
    case 'double_exponential':
      return params.A * Math.exp(-params.k1 * t) + params.B * Math.exp(-params.k2 * t) + params.C

    case 'linear_log':
      return params.RTE0 - params.alpha * t - params.beta * Math.log(1 + params.gamma * t)

    case 'arrhenius': {
      const Q_cal = params.A * Math.exp(-params.Ea * 1000 / (R * T)) * Math.pow(t + 0.5, 0.5)
      const Q_cyc = params.A * Math.exp(-params.Ea * 1000 / (R * T)) * Math.pow(N_cycles, 0.7) * DOD_factor * C_rate_factor
      return Math.max(0.6, 1 - (Q_cal + Q_cyc))
    }

    case 'rainflow': {
      const damage = Math.pow(N_cycles / params.cycle_life_ref, params.damage_exponent) * Math.pow(surveyData.dod / 100 / params.dod_ref, 1.5)
      return Math.max(0.6, 1 - damage)
    }

    case 'semi_empirical': {
      const temp_factor = 1 - params.temp_coeff * (surveyData.temperature - 25) / 100
      const dod_factor = 1 - params.dod_coeff * (surveyData.dod / 100 - 0.5) / 100
      const c_rate_factor = 1 - params.c_rate_coeff * (surveyData.cRate - 0.5)
      const soc_factor = 0.98
      return Math.max(0.6, 1 - (1 - temp_factor * dod_factor * c_rate_factor * soc_factor) * t / 25)
    }

    default: {
      const A_cal = params.A_cal || 0.001
      const Ea_cal = params.Ea_cal || 35
      const alpha = params.alpha || 0.5
      const A_cyc = params.A_cyc || 0.00001
      const Ea_cyc = params.Ea_cyc || 25
      const beta = params.beta || 0.7
      
      const Q_cal = A_cal * Math.exp(-Ea_cal * 1000 / (R * T)) * Math.pow(t + 0.5, alpha)
      const Q_cyc = A_cyc * Math.exp(-Ea_cyc * 1000 / (R * T)) * Math.pow(N_cycles, beta) * DOD_factor * C_rate_factor
      return Math.max(0.6, 1 - (Q_cal + Q_cyc))
    }
  }
}

const runSimulation = () => {
  currentStep.value = 4
  
  const N = simParams.simulationYears + 1
  const sohCurve = []
  const rteCurve = []
  const netAvailCurve = []
  
  const algo = algorithms.value.find(a => a.id === selectedAlgorithm.value)
  const modelType = algo?.model_type || 'arrhenius'

  for (let i = 0; i < N; i++) {
    const t = i
    let soh = calculateSOH(modelType, algoParams, t)
    
    soh = soh * correctionFactors.sohFactor
    if (yearlyCorrections.value[i]?.sohCorrection) {
      soh += yearlyCorrections.value[i].sohCorrection
    }
    
    let rte = simParams.initRte / 100 - 0.002 * i * correctionFactors.rteFactor
    if (yearlyCorrections.value[i]?.rteCorrection) {
      rte += yearlyCorrections.value[i].rteCorrection
    }
    
    const grossEnergy = surveyData.ratedEnergy * surveyData.containerQty * (surveyData.dod / 100) * rte * soh * (simParams.acEfficiency / 100)
    const auxEnergy = (simParams.bessAuxRun + simParams.pcsAuxRun) * simParams.simulationYears / 1000
    const netAvail = Math.max(0, grossEnergy - auxEnergy) * correctionFactors.capacityFactor
    
    sohCurve.push(Math.min(100, Math.max(60, soh * 100)))
    rteCurve.push(Math.min(100, Math.max(80, rte * 100)))
    netAvailCurve.push(netAvail)
  }
  
  simulationResults.sohCurve = sohCurve
  simulationResults.rteCurve = rteCurve
  simulationResults.netAvailCurve = netAvailCurve
  simulationResults.initSoh = sohCurve[0]
  simulationResults.guaranteeEndSoh = sohCurve[simParams.guaranteeYears]
  simulationResults.finalSoh = sohCurve[N - 1]
  simulationResults.meetsGuarantee = sohCurve[simParams.guaranteeYears] >= simParams.guaranteeSoh
  
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
  
  nextTick(() => {
    setTimeout(() => renderChart(), 100)
  })

  // 将仿真结果 emit 给父组件，打通仿真→容量对账的数据流
  emit('applyConfig', {
    soh: simulationResults.sohCurve,
    rte: simulationResults.rteCurve,
    source: 'simulation',
    algorithmType: simParams.algorithmType,
    simulationYears: simParams.simulationYears,
    guaranteeSoh: simParams.guaranteeSoh,
  })
}

const runBackendSimulation = async () => {
  currentStep.value = 4
  try {
    const algo = algorithms.value.find(a => a.id === selectedAlgorithm.value)
    const modelType = algo?.model_type || 'arrhenius'
    const modelParams = {}
    if (algo?.parameters) {
      for (const [key, cfg] of Object.entries(algo.parameters)) {
        modelParams[key] = algoParams[key] ?? cfg.default
      }
    }
    const body = {
      systemParams: {
        ratedEnergy: surveyData.ratedEnergy || store.systemParams.ratedEnergy,
        initContainerQty: surveyData.containerQty || store.systemParams.initContainerQty,
        initPcsQty: store.systemParams.initPcsQty,
        pcsPower: store.systemParams.pcsPower,
        duration: surveyData.duration || store.systemParams.duration,
        temperature: surveyData.temperature || store.systemParams.temperature,
        cyclesPerDay: surveyData.cyclesPerDay || store.systemParams.cyclesPerDay,
        dod: surveyData.dod || store.systemParams.dod || 80,
        cRate: store.systemParams.cRate || 0.5,
        requiredEnergy: store.systemParams.requiredEnergy,
        acEfficiency: simParams.acEfficiency || store.systemParams.acEfficiency,
        bessAuxRun: store.systemParams.bessAuxRun,
        bessAuxStandby: store.systemParams.bessAuxStandby,
        pcsAuxRun: store.systemParams.pcsAuxRun,
        pcsAuxStandby: store.systemParams.pcsAuxStandby,
      },
      algorithm: {
        model: modelType,
        correctionFactor: correctionFactors.sohFactor || 1.0,
        modelParams: Object.keys(modelParams).length > 0 ? modelParams : undefined,
      },
    }
    const res = await fetch('/api/pipeline/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
    if (!res.ok) throw new Error('Backend simulation failed')
    const data = await res.json()
    if (data.result) {
      const sohArr = data.result.soh || []
      const rteArr = data.result.rte || []
      simulationResults.sohCurve = sohArr
      simulationResults.rteCurve = rteArr
      simulationResults.netAvailCurve = data.result.totalAcUsable || []
      simulationResults.initSoh = sohArr[0] || 100
      simulationResults.finalSoh = sohArr[sohArr.length - 1] || 0
      simulationResults.guaranteeEndSoh = sohArr[simParams.guaranteeYears] || 0
      simulationResults.meetsGuarantee = (sohArr[simParams.guaranteeYears] || 0) >= simParams.guaranteeSoh
      simulationResults.tableData = sohArr.map((s, i) => ({
        year: i,
        soh: s,
        rte: rteArr[i] || 0,
        netAvail: (data.result.totalAcUsable || [])[i] || 0,
        meetsReq: ((data.result.meetsReq || [])[i]) || false,
      }))
      nextTick(() => setTimeout(() => renderChart(), 100))
      emit('applyConfig', {
        soh: sohArr,
        rte: rteArr,
        source: 'backend-pipeline',
        algorithmType: modelType,
        simulationYears: simParams.simulationYears,
        guaranteeSoh: simParams.guaranteeSoh,
      })
    }
  } catch (e) {
    console.error('Backend simulation error:', e)
  }
}

const renderChart = () => {
  if (!chartContainer.value) return
  
  if (chartInstance) {
    chartInstance.dispose()
  }
  
  chartInstance = echarts.init(chartContainer.value)
  
  const years = Array.from({ length: simulationResults.sohCurve.length }, (_, i) => i)
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
  const textColor = isDark ? '#94a3b8' : '#64748b'
  const accentColor = isDark ? '#2dd4bf' : '#3b82f6'
  const secondaryColor = isDark ? '#38bdf8' : '#06b6d4'
  const warningColor = '#f59e0b'
  
  chartInstance.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: ['SOH', 'RTE', '保障线'], top: 0, textStyle: { color: textColor, fontSize: 10 } },
    grid: { left: 40, right: 20, top: 30, bottom: 20 },
    xAxis: { type: 'category', data: years, axisLabel: { color: textColor, fontSize: 10 } },
    yAxis: { type: 'value', min: 50, max: 100, axisLabel: { color: textColor, fontSize: 10 } },
    series: [
      { name: 'SOH', type: 'line', data: simulationResults.sohCurve, smooth: true, lineStyle: { color: accentColor }, itemStyle: { color: accentColor } },
      { name: 'RTE', type: 'line', data: simulationResults.rteCurve, smooth: true, lineStyle: { color: secondaryColor }, itemStyle: { color: secondaryColor } },
      { name: '保障线', type: 'line', data: Array.from({ length: years.length }, () => simParams.guaranteeSoh), lineStyle: { color: warningColor, type: 'dashed' }, itemStyle: { color: warningColor } },
    ],
  })
}

const saveSimulationResult = async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    showToast('请先登录', 'error')
    return
  }

  const projectName = surveyData.projectName || '未命名项目'
  const timestamp = new Date().toISOString().slice(0, 19).replace(/[-T:]/g, '')
  const resultName = `${projectName}_${timestamp}`

  const algo = algorithms.value.find(a => a.id === selectedAlgorithm.value)
  
  const data = {
    name: resultName,
    description: `使用${algo?.name || '未知算法'}进行仿真`,
    simulation_type: algo?.category || 'comprehensive',
    algorithm_model_id: selectedAlgorithm.value,
    params: {
      surveyData: surveyData,
      simParams: simParams,
      algoParams: { ...algoParams },
      correctionFactors: { ...correctionFactors },
      yearlyCorrections: yearlyCorrections.value,
    },
    results: {
      sohCurve: simulationResults.sohCurve,
      rteCurve: simulationResults.rteCurve,
      netAvailCurve: simulationResults.netAvailCurve,
      tableData: simulationResults.tableData,
    },
    summary: {
      initSoh: simulationResults.initSoh,
      guaranteeEndSoh: simulationResults.guaranteeEndSoh,
      finalSoh: simulationResults.finalSoh,
      meetsGuarantee: simulationResults.meetsGuarantee,
    },
    status: 'completed',
  }

  try {
    const resp = await fetch('http://localhost:5001/api/versions/default/results', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    })
    const respData = await resp.json()
    if (respData.success) {
      showToast('仿真结果保存成功')
    } else {
      showToast(respData.error || '保存失败', 'error')
    }
  } catch (e) {
    showToast('保存失败: ' + e.message, 'error')
  }
}

const showToast = (message, type = 'success') => {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => { toast.show = false }, 3000)
}

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
  fetchAlgorithms()
})
</script>