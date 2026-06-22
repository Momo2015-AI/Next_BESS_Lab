<template>
  <div class="h-full overflow-y-auto custom-scrollbar">
    <div class="max-w-6xl mx-auto space-y-4 py-2">

      <div class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded flex items-center justify-center font-bold text-xs" style="background-color: var(--color-accent-glow); color: var(--color-accent-secondary);">A</span>
          <div>
            <h3 class="font-bold text-sm" style="color: var(--color-text);">电芯选型库 <span class="text-[10px] font-normal ml-1" style="color: var(--color-text-muted);">Battery Cell Library</span></h3>
          </div>
          <div class="ml-auto flex gap-2">
            <select v-model="cellFilter" 
              class="text-xs rounded px-2 py-1"
              style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
              onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';"
              onblur="this.style.borderColor='var(--color-input-border)';">
              <option value="">全部厂商</option>
              <option v-for="m in localMfrList('cells')" :key="m" :value="m">{{ m }}</option>
            </select>
            <button @click="openAddModal('cell')" 
              class="text-[10px] px-2 py-1 rounded transition-colors"
              style="background-color: var(--color-accent-glow); border: 1px solid var(--color-accent); color: var(--color-accent-secondary);"
              onmouseover="this.style.backgroundColor='var(--color-accent-dark)';"
              onmouseout="this.style.backgroundColor='var(--color-accent-glow)';">+ 新增电芯</button>
          </div>
        </div>
        <div class="grid grid-cols-3 gap-2">
          <div v-for="cell in localFiltered('cells', cellFilter)" :key="cell.id"
            @click="selectedCell = cell.id"
            class="border rounded-lg p-3 cursor-pointer transition-all group relative"
            :style="selectedCell === cell.id ? { borderColor: 'var(--color-accent-secondary)', backgroundColor: 'var(--color-accent-glow)' } : { borderColor: 'var(--color-border)', backgroundColor: 'var(--color-card-dark)' }"
            onmouseover="if(this.style.borderColor !== 'var(--color-accent-secondary)') this.style.borderColor='var(--color-input-border)';"
            onmouseout="if(this.style.borderColor !== 'var(--color-accent-secondary)') this.style.borderColor='var(--color-border)';">
            <button @click.stop="deleteItem('cells', cell.id)" 
              class="absolute top-1 right-1 text-xs opacity-0 group-hover:opacity-100 transition-opacity"
              style="color: var(--color-text-muted);"
              onmouseover="this.style.color='var(--color-danger)';"
              onmouseout="this.style.color='var(--color-text-muted)';">×</button>
            <div class="flex justify-between items-start mb-1">
              <span class="text-xs font-bold" style="color: var(--color-text);">{{ cell.model }}</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded" :style="cell.status === 'mass-production' ? { backgroundColor: 'var(--color-success-glow)', color: 'var(--color-success)' } : { backgroundColor: 'var(--color-warning-glow)', color: 'var(--color-warning)' }">{{ cell.status === 'mass-production' ? '量产' : '预研' }}</span>
            </div>
            <div class="text-[10px] mb-2" style="color: var(--color-text-muted);">{{ cell.mfr }}</div>
            <div class="grid grid-cols-2 gap-x-2 gap-y-0.5 text-[10px]">
              <div style="color: var(--color-text-muted);">容量</div><div style="color: var(--color-text-secondary); text-align:right;">{{ cell.capacityAh }} Ah</div>
              <div style="color: var(--color-text-muted);">标压</div><div style="color: var(--color-text-secondary); text-align:right;">{{ cell.voltageNominal }} V</div>
              <div style="color: var(--color-text-muted);">能量</div><div style="color: var(--color-text-secondary); text-align:right;">{{ cell.energyWh }} Wh</div>
              <div style="color: var(--color-text-muted);">循环</div><div style="color: var(--color-text-secondary); text-align:right;">{{ cell.cycleLife }}+</div>
            </div>
          </div>
        </div>
      </div>

      <div class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded flex items-center justify-center font-bold text-xs" style="background-color: var(--color-warning-glow); color: var(--color-warning);">B</span>
          <div>
            <h3 class="font-bold text-sm" style="color: var(--color-text);">集装箱库 <span class="text-[10px] font-normal ml-1" style="color: var(--color-text-muted);">Container Library</span></h3>
          </div>
          <div class="ml-auto flex gap-2">
            <select v-model="containerFilter" 
              class="text-xs rounded px-2 py-1"
              style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
              onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';"
              onblur="this.style.borderColor='var(--color-input-border)';">
              <option value="">全部厂商</option>
              <option v-for="m in localMfrList('containers')" :key="m" :value="m">{{ m }}</option>
            </select>
            <button @click="openAddModal('container')" 
              class="text-[10px] px-2 py-1 rounded transition-colors"
              style="background-color: var(--color-warning-glow); border: 1px solid var(--color-warning); color: var(--color-warning);"
              onmouseover="this.style.backgroundColor='rgba(234, 179, 8, 0.2)';"
              onmouseout="this.style.backgroundColor='var(--color-warning-glow)';">+ 新增集装箱</button>
          </div>
        </div>
        <div class="grid grid-cols-3 gap-2">
          <div v-for="c in localFiltered('containers', containerFilter)" :key="c.id"
            @click="selectedContainer = c.id"
            class="border rounded-lg p-3 cursor-pointer transition-all group relative"
            :style="selectedContainer === c.id ? { borderColor: 'var(--color-warning)', backgroundColor: 'var(--color-warning-glow)' } : { borderColor: 'var(--color-border)', backgroundColor: 'var(--color-card-dark)' }"
            onmouseover="if(this.style.borderColor !== 'var(--color-warning)') this.style.borderColor='var(--color-input-border)';"
            onmouseout="if(this.style.borderColor !== 'var(--color-warning)') this.style.borderColor='var(--color-border)';">
            <button @click.stop="deleteItem('containers', c.id)" 
              class="absolute top-1 right-1 text-xs opacity-0 group-hover:opacity-100 transition-opacity"
              style="color: var(--color-text-muted);"
              onmouseover="this.style.color='var(--color-danger)';"
              onmouseout="this.style.color='var(--color-text-muted)';">×</button>
            <div class="flex justify-between items-start mb-1">
              <span class="text-xs font-bold" style="color: var(--color-text);">{{ c.model }}</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded" :style="c.status === 'mass-production' ? { backgroundColor: 'var(--color-success-glow)', color: 'var(--color-success)' } : { backgroundColor: 'var(--color-warning-glow)', color: 'var(--color-warning)' }">{{ c.status === 'mass-production' ? '量产' : '预研' }}</span>
            </div>
            <div class="text-[10px] mb-2" style="color: var(--color-text-muted);">{{ c.mfr }}</div>
            <div class="grid grid-cols-2 gap-x-2 gap-y-0.5 text-[10px]">
              <div style="color: var(--color-text-muted);">能量</div><div style="color: var(--color-text-secondary); text-align:right;">{{ c.ratedEnergyMWh }} MWh</div>
              <div style="color: var(--color-text-muted);">功率</div><div style="color: var(--color-text-secondary); text-align:right;">{{ c.ratedPowerMW }} MW</div>
              <div style="color: var(--color-text-muted);">电芯</div><div style="color: var(--color-text-secondary); text-align:right;">{{ c.cellModel }}</div>
              <div style="color: var(--color-text-muted);">散热</div><div style="color: var(--color-text-secondary); text-align:right;">{{ c.cooling }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded flex items-center justify-center font-bold text-xs" style="background-color: var(--color-accent-glow); color: var(--color-accent);">C</span>
          <div>
            <h3 class="font-bold text-sm" style="color: var(--color-text);">PCS 变流器库 <span class="text-[10px] font-normal ml-1" style="color: var(--color-text-muted);">PCS Library</span></h3>
          </div>
          <div class="ml-auto flex gap-2">
            <select v-model="pcsFilter" 
              class="text-xs rounded px-2 py-1"
              style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
              onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';"
              onblur="this.style.borderColor='var(--color-input-border)';">
              <option value="">全部厂商</option>
              <option v-for="m in localMfrList('pcs')" :key="m" :value="m">{{ m }}</option>
            </select>
            <select v-model="pcsPowerFilter" 
              class="text-xs rounded px-2 py-1"
              style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);"
              onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';"
              onblur="this.style.borderColor='var(--color-input-border)';">
              <option value="0">全部功率</option>
              <option value="1.25">1.25 MW</option>
              <option value="1.725">1.725 MW</option>
              <option value="2.5">2.5 MW</option>
              <option value="3.45">3.45 MW</option>
            </select>
            <button @click="openAddModal('pcs')" 
              class="text-[10px] px-2 py-1 rounded transition-colors"
              style="background-color: var(--color-accent-glow); border: 1px solid var(--color-accent); color: var(--color-accent);"
              onmouseover="this.style.backgroundColor='var(--color-accent-dark)';"
              onmouseout="this.style.backgroundColor='var(--color-accent-glow)';">+ 新增 PCS</button>
          </div>
        </div>
        <div class="grid grid-cols-3 gap-2">
          <div v-for="p in localFiltered('pcs', pcsFilter, pcsPowerFilter)" :key="p.id"
            @click="selectedPcs = p.id"
            class="border rounded-lg p-3 cursor-pointer transition-all group relative"
            :style="selectedPcs === p.id ? { borderColor: 'var(--color-accent)', backgroundColor: 'var(--color-accent-glow)' } : { borderColor: 'var(--color-border)', backgroundColor: 'var(--color-card-dark)' }"
            onmouseover="if(this.style.borderColor !== 'var(--color-accent)') this.style.borderColor='var(--color-input-border)';"
            onmouseout="if(this.style.borderColor !== 'var(--color-accent)') this.style.borderColor='var(--color-border)';">
            <button @click.stop="deleteItem('pcs', p.id)" 
              class="absolute top-1 right-1 text-xs opacity-0 group-hover:opacity-100 transition-opacity"
              style="color: var(--color-text-muted);"
              onmouseover="this.style.color='var(--color-danger)';"
              onmouseout="this.style.color='var(--color-text-muted)';">×</button>
            <div class="flex justify-between items-start mb-1">
              <span class="text-xs font-bold" style="color: var(--color-text);">{{ p.model }}</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded" style="background-color: var(--color-success-glow); color: var(--color-success);">量产</span>
            </div>
            <div class="text-[10px] mb-2" style="color: var(--color-text-muted);">{{ p.mfr }}</div>
            <div class="grid grid-cols-2 gap-x-2 gap-y-0.5 text-[10px]">
              <div style="color: var(--color-text-muted);">功率</div><div style="color: var(--color-text-secondary); text-align:right;">{{ p.ratedPowerMW }} MW</div>
              <div style="color: var(--color-text-muted);">效率</div><div style="color: var(--color-text-secondary); text-align:right;">{{ p.efficiency }}%</div>
              <div style="color: var(--color-text-muted);">AC电压</div><div style="color: var(--color-text-secondary); text-align:right;">{{ p.acVoltage }}</div>
              <div style="color: var(--color-text-muted);">散热</div><div style="color: var(--color-text-secondary); text-align:right;">{{ p.cooling }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="rounded-lg p-4" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-6 h-6 rounded flex items-center justify-center font-bold text-xs" style="background-color: var(--color-accent-glow); color: var(--color-accent-secondary);">D</span>
          <div>
            <h3 class="font-bold text-sm" style="color: var(--color-text);">典型场景方案 Template <span class="text-[10px] font-normal ml-1" style="color: var(--color-text-muted);">Scenario Templates</span></h3>
          </div>
        </div>
        <div class="grid grid-cols-5 gap-2 mb-4">
          <div v-for="s in scenarios" :key="s.id"
            @click="applyScenario(s)"
            class="border rounded-lg p-3 cursor-pointer transition-all text-center"
            :style="selectedScenario === s.id ? { borderColor: 'var(--color-accent-secondary)', backgroundColor: 'var(--color-accent-glow)' } : { borderColor: 'var(--color-border)', backgroundColor: 'var(--color-card-dark)' }"
            onmouseover="if(this.style.borderColor !== 'var(--color-accent-secondary)') this.style.borderColor='var(--color-input-border)';"
            onmouseout="if(this.style.borderColor !== 'var(--color-accent-secondary)') this.style.borderColor='var(--color-border)';">
            <div class="text-xs font-bold mb-1" style="color: var(--color-text);">{{ s.name }}</div>
            <div class="text-[10px] leading-relaxed" style="color: var(--color-text-muted);">{{ s.description }}</div>
          </div>
        </div>
        <div v-if="configSummary" class="border-t pt-3" style="border-color: var(--color-border);">
          <h4 class="text-xs font-bold mb-2" style="color: var(--color-text-secondary);">当前方案摘要 Current Selection</h4>
          <div class="grid grid-cols-3 gap-3 text-[10px]">
            <div class="rounded p-2" style="background-color: var(--color-card-dark);">
              <span style="color: var(--color-text-muted);">电芯</span>
              <div class="font-mono mt-0.5" style="color: var(--color-text);">{{ configSummary.cell || '未选择' }}</div>
            </div>
            <div class="rounded p-2" style="background-color: var(--color-card-dark);">
              <span style="color: var(--color-text-muted);">集装箱</span>
              <div class="font-mono mt-0.5" style="color: var(--color-text);">{{ configSummary.container || '未选择' }}</div>
            </div>
            <div class="rounded p-2" style="background-color: var(--color-card-dark);">
              <span style="color: var(--color-text-muted);">PCS</span>
              <div class="font-mono mt-0.5" style="color: var(--color-text);">{{ configSummary.pcs || '未选择' }}</div>
            </div>
          </div>
          <div class="mt-3 flex justify-end">
            <button @click="applyToSimulation"
              class="text-xs px-6 py-1.5 rounded shadow-md transition-all active:scale-95"
              style="background-color: var(--color-accent-secondary); color: white;"
              onmouseover="this.style.opacity='0.9';"
              onmouseout="this.style.opacity='1';">
              应用至仿真参数 Apply to Simulation
            </button>
          </div>
        </div>
      </div>

      <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center" style="background-color: rgba(0,0,0,0.6);" @click.self="showModal = false">
        <div class="rounded-xl p-5 w-[480px] max-h-[80vh] overflow-y-auto shadow-2xl" style="background-color: var(--color-card); border: 1px solid var(--color-border);">
          <h3 class="font-bold text-sm mb-4" style="color: var(--color-text);">{{ modalTitle }}</h3>
          <div class="space-y-3">
            <template v-if="modalType === 'cell'">
              <div class="grid grid-cols-2 gap-2 text-[10px]">
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">厂商</label><input v-model="modalForm.mfr" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">型号</label><input v-model="modalForm.model" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">化学体系</label><input v-model="modalForm.chemistry" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">容量 Ah</label><input v-model.number="modalForm.capacityAh" type="number" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">标称电压 V</label><input v-model.number="modalForm.voltageNominal" type="number" step="0.1" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">循环寿命</label><input v-model.number="modalForm.cycleLife" type="number" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">尺寸</label><input v-model="modalForm.dimensions" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">重量 kg</label><input v-model="modalForm.weight" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
              </div>
            </template>
            <template v-else-if="modalType === 'container'">
              <div class="grid grid-cols-2 gap-2 text-[10px]">
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">厂商</label><input v-model="modalForm.mfr" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">型号</label><input v-model="modalForm.model" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">额定能量 MWh</label><input v-model.number="modalForm.ratedEnergyMWh" type="number" step="0.001" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">额定功率 MW</label><input v-model.number="modalForm.ratedPowerMW" type="number" step="0.001" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">电芯型号</label><input v-model="modalForm.cellModel" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">散热方式</label><input v-model="modalForm.cooling" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">尺寸</label><input v-model="modalForm.dimensions" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">重量 t</label><input v-model="modalForm.weight" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
              </div>
            </template>
            <template v-else-if="modalType === 'pcs'">
              <div class="grid grid-cols-2 gap-2 text-[10px]">
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">厂商</label><input v-model="modalForm.mfr" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">型号</label><input v-model="modalForm.model" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">额定功率 MW</label><input v-model.number="modalForm.ratedPowerMW" type="number" step="0.001" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">效率 %</label><input v-model.number="modalForm.efficiency" type="number" step="0.1" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">AC电压</label><input v-model="modalForm.acVoltage" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">DC范围</label><input v-model="modalForm.dcVoltageRange" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
                <div><label class="block mb-0.5" style="color: var(--color-text-muted);">散热</label><input v-model="modalForm.cooling" class="w-full rounded px-2 py-1.5 text-xs" style="background-color: var(--color-input-bg-dark); border: 1px solid var(--color-input-border); color: var(--color-text);" onfocus="this.style.borderColor='var(--color-accent)'; this.style.outline='none';" onblur="this.style.borderColor='var(--color-input-border)';"></div>
              </div>
            </template>

            <div class="border-t pt-3" style="border-color: var(--color-border);">
              <p class="text-[10px] mb-2" style="color: var(--color-text-muted);">或上传规格书自动提取 (支持 PDF/CSV)</p>
              <div class="flex gap-2 text-[10px]">
                <input ref="specInput" type="file" accept=".pdf,.csv,.xlsx,.xls" class="hidden" @change="onSpecUpload">
                <button @click="$refs.specInput.click()" class="px-3 py-1.5 rounded transition-colors" style="background-color: var(--color-card-dark); border: 1px solid var(--color-border); color: var(--color-text-secondary);" onmouseover="this.style.borderColor='var(--color-accent)';" onmouseout="this.style.borderColor='var(--color-border)';">
                  上传规格书
                </button>
                <span v-if="specUploading" class="self-center" style="color: var(--color-accent-secondary);">解析中...</span>
                <span v-if="specResult" class="self-center" style="color: var(--color-success);">{{ specResult }}</span>
              </div>
            </div>
          </div>
          <div class="flex justify-end gap-2 mt-4 pt-3 border-t" style="border-color: var(--color-border);">
            <button @click="showModal = false" class="text-xs px-3 py-1.5" style="color: var(--color-text-muted);" onmouseover="this.style.color='var(--color-text-secondary)';" onmouseout="this.style.color='var(--color-text-muted)';">取消</button>
            <button @click="saveProduct" class="text-xs px-4 py-1.5 rounded transition-colors" style="background-color: var(--color-accent-secondary); color: white;" onmouseover="this.style.opacity='0.9';" onmouseout="this.style.opacity='1';">保存</button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import baseProducts from '../data/products.json'

const emit = defineEmits(['applyConfig'])

const selectedCell = ref('')
const selectedContainer = ref('')
const selectedPcs = ref('')
const selectedScenario = ref(null)

const cellFilter = ref('')
const containerFilter = ref('')
const pcsFilter = ref('')
const pcsPowerFilter = ref('0')

// 从API加载的数据
const cellLibrary = ref([])
const containerLibrary = ref([])
const pcsLibrary = ref([])

// 兼容旧数据结构
const localData = ref(JSON.parse(JSON.stringify(baseProducts)))

// API加载产品库
async function loadLibraryData() {
  try {
    // 并行加载三个库
    const [cellsRes, containersRes, pcsRes] = await Promise.all([
      fetch('/api/library/cells'),
      fetch('/api/library/containers'),
      fetch('/api/library/pcs')
    ])
    
    const [cellsData, containersData, pcsData] = await Promise.all([
      cellsRes.json(),
      containersRes.json(),
      pcsRes.json()
    ])
    
    if (cellsData.success) cellLibrary.value = cellsData.data || []
    if (containersData.success) containerLibrary.value = containersData.data || []
    if (pcsData.success) pcsLibrary.value = pcsData.data || []
    
    // 如果数据库为空，初始化默认数据
    if (cellLibrary.value.length === 0 && containerLibrary.value.length === 0 && pcsLibrary.value.length === 0) {
      await seedLibrary()
    }
  } catch (error) {
    console.error('加载产品库失败:', error)
    // 降级使用本地数据
    localData.value = JSON.parse(JSON.stringify(baseProducts))
  }
}

// 初始化产品库
async function seedLibrary() {
  try {
    const response = await fetch('/api/library/seed', { method: 'POST' })
    const data = await response.json()
    if (data.success) {
      await loadLibraryData()
    }
  } catch (error) {
    console.error('初始化产品库失败:', error)
  }
}

function localMfrList(key) {
  // 优先使用API数据，否则降级使用本地数据
  const data = key === 'cells' ? cellLibrary.value : 
               key === 'containers' ? containerLibrary.value : 
               key === 'pcs' ? pcsLibrary.value : []
  
  if (data.length > 0) {
    return [...new Set(data.map(c => c.mfr).filter(Boolean))]
  }
  return [...new Set(localData.value[key]?.map(c => c.mfr) || [])]
}

function localFiltered(key, mfrFilter, powerFilter) {
  // 优先使用API数据
  let list = []
  if (key === 'cells' && cellLibrary.value.length > 0) {
    list = cellLibrary.value.map(c => ({
      id: c.id,
      model: c.model,
      mfr: c.mfr,
      chemistry: c.chemistry,
      capacityAh: c.capacityAh,
      voltageNominal: c.voltageNominal,
      voltageMax: c.voltageMax,
      voltageMin: c.voltageMin,
      energyWh: c.energyWh,
      cycleLife: c.cycleLife,
      calendarLife: c.calendarLife,
      dimensions: c.dimensions,
      weight: c.weight,
      energyDensity: c.energyDensity,
      status: c.status,
      certifications: c.certifications,
      unitPrice: c.unitPrice,
      remarks: c.remarks,
    }))
  } else if (key === 'containers' && containerLibrary.value.length > 0) {
    list = containerLibrary.value.map(c => ({
      id: c.id,
      model: c.model,
      mfr: c.mfr,
      spec: c.spec,
      ratedEnergyMWh: c.ratedEnergyMWh,
      ratedPowerMW: c.ratedPowerMW,
      dcVoltageRange: c.dcVoltageRange,
      maxDcCurrent: c.maxDcCurrent,
      cellModel: c.cellModel,
      seriesCount: c.seriesCount,
      parallelCount: c.parallelCount,
      dimensions: c.dimensions,
      weight: c.weight,
      cooling: c.cooling,
      rte: c.rte,
      auxRun: c.auxRun,
      auxStandby: c.auxStandby,
      status: c.status,
      certifications: c.certifications,
      unitPrice: c.unitPrice,
      remarks: c.remarks,
    }))
  } else if (key === 'pcs' && pcsLibrary.value.length > 0) {
    list = pcsLibrary.value.map(p => ({
      id: p.id,
      model: p.model,
      mfr: p.mfr,
      ratedPowerMW: p.ratedPowerMW,
      efficiency: p.efficiency,
      acVoltage: p.acVoltage,
      dcVoltageRange: p.dcVoltageRange,
      maxDcCurrent: p.maxDcCurrent,
      frequencyRange: p.frequencyRange,
      dimensions: p.dimensions,
      weight: p.weight,
      cooling: p.cooling,
      auxRun: p.auxRun,
      auxStandby: p.auxStandby,
      status: p.status,
      certifications: p.certifications,
      unitPrice: p.unitPrice,
      remarks: p.remarks,
    }))
  } else {
    list = localData.value[key] || []
  }
  
  if (mfrFilter) list = list.filter(c => c.mfr === mfrFilter)
  if (key === 'pcs' && powerFilter && powerFilter !== '0') {
    list = list.filter(p => p.ratedPowerMW === Number(powerFilter))
  }
  return list
}

async function deleteItem(key, id) {
  // 如果有API数据，调用API删除
  try {
    const endpoint = key === 'cells' ? '/api/library/cells' : 
                     key === 'containers' ? '/api/library/containers' : '/api/library/pcs'
    const response = await fetch(`${endpoint}/${id}`, { method: 'DELETE' })
    const data = await response.json()
    if (data.success) {
      // 重新加载数据
      await loadLibraryData()
      return
    }
  } catch (error) {
    console.error('API删除失败:', error)
  }
  // 降级使用本地删除
  localData.value[key] = localData.value[key].filter(item => item.id !== id)
  saveLocal()
}

const showModal = ref(false)
const modalType = ref('cell')
const modalForm = ref({})
const specInput = ref(null)
const specUploading = ref(false)
const specResult = ref('')

function openAddModal(type) {
  modalType.value = type
  showModal.value = true
  specResult.value = ''
  if (type === 'cell') {
    modalForm.value = { mfr: '', model: '', chemistry: 'LFP', capacityAh: '', voltageNominal: 3.2, cycleLife: '', dimensions: '', weight: '', status: 'mass-production' }
  } else if (type === 'container') {
    modalForm.value = { mfr: '', model: '', ratedEnergyMWh: '', ratedPowerMW: '', cellModel: '', cooling: '', dimensions: '', weight: '', status: 'mass-production' }
  } else {
    modalForm.value = { mfr: '', model: '', ratedPowerMW: '', efficiency: '', acVoltage: '', dcVoltageRange: '', cooling: '', status: 'mass-production' }
  }
}

async function saveProduct() {
  const type = modalType.value
  const f = modalForm.value
  
  // 构建API请求数据
  let apiData = { ...f }
  if (type === 'cell') {
    apiData.capacityAh = f.capacityAh
    apiData.voltageNominal = f.voltageNominal
    apiData.energyWh = (f.capacityAh || 0) * (f.voltageNominal || 3.2)
    apiData.cycleLife = f.cycleLife
  } else if (type === 'container') {
    apiData.ratedEnergyMWh = f.ratedEnergyMWh
    apiData.ratedPowerMW = f.ratedPowerMW
    apiData.cellModel = f.cellModel
    apiData.cooling = f.cooling
  } else if (type === 'pcs') {
    apiData.ratedPowerMW = f.ratedPowerMW
    apiData.efficiency = f.efficiency
    apiData.acVoltage = f.acVoltage
    apiData.dcVoltageRange = f.dcVoltageRange
    apiData.cooling = f.cooling
  }
  
  // 调用API保存
  try {
    const endpoint = type === 'cell' ? '/api/library/cells' : 
                     type === 'container' ? '/api/library/containers' : '/api/library/pcs'
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(apiData)
    })
    const data = await response.json()
    if (data.success) {
      // 重新加载数据
      await loadLibraryData()
      showModal.value = false
      return
    }
  } catch (error) {
    console.error('API保存失败:', error)
  }
  
  // 降级使用本地保存
  const id = type + '-' + f.model?.toLowerCase().replace(/\s+/g, '-') + '-' + Date.now().toString(36)
  let item = { id, ...f }

  if (type === 'cell') {
    item.energyWh = (f.capacityAh || 0) * (f.voltageNominal || 3.2)
    item.voltageRange = '2.5-3.65'
    item.sohCurve = 'default'
  } else if (type === 'container') {
    item.type = '20ft Standard'
    item.cycleLife = 8000
  } else if (type === 'pcs') {
    item.ratedPowerKVA = (f.ratedPowerMW || 0) * 1040
    item.topology = '3-Level NPC'
    item.isolation = 'Transformerless'
  }

  if (!localData.value[type + 's']) {
    localData.value[type + 's'] = []
  }
  localData.value[type + 's'].push(item)
  saveLocal()
  showModal.value = false
}

async function onSpecUpload(e) {
  const file = e.target.files?.[0]
  if (!file) return
  specUploading.value = true
  specResult.value = ''
  try {
    const formData = new FormData()
    formData.append('file', file)
    const resp = await fetch('/api/upload/extract', { method: 'POST', body: formData })
    const data = await resp.json()
    if (data.extracted) {
      const ext = data.extracted
      if (modalType.value === 'cell') {
        if (ext.capacity_ah || ext.total_mwh) modalForm.value.capacityAh = ext.capacity_ah || ext.total_mwh
        if (ext.cycle_life) modalForm.value.cycleLife = ext.cycle_life
      }
      specResult.value = '已提取 ' + Object.keys(ext).length + ' 个字段'
    } else {
      specResult.value = '未能自动提取，请手动填写'
    }
  } catch { specResult.value = '上传失败' }
  specUploading.value = false
}

function saveLocal() {
  if (typeof localStorage === 'undefined') return
  try { localStorage.setItem('soh-products', JSON.stringify(localData.value)) } catch(e) {}
}

try {
  if (typeof localStorage !== 'undefined') {
    const saved = localStorage.getItem('soh-products')
    if (saved) {
      const parsed = JSON.parse(saved)
      localData.value = { ...baseProducts, ...parsed }
    }
  }
} catch(e) {}

const mfrList = computed(() => ({
  cells: localMfrList('cells'),
  containers: localMfrList('containers'),
  pcs: localMfrList('pcs'),
}))

const scenarios = baseProducts.scenarios

const filteredCells = computed(() => localFiltered('cells', cellFilter.value))
const filteredContainers = computed(() => localFiltered('containers', containerFilter.value))
const filteredPcs = computed(() => localFiltered('pcs', pcsFilter.value, pcsPowerFilter.value))

const configSummary = computed(() => {
  const cell = localData.value.cells?.find(c => c.id === selectedCell.value)
  const container = localData.value.containers?.find(c => c.id === selectedContainer.value)
  const pcs = localData.value.pcs?.find(p => p.id === selectedPcs.value)
  return {
    cell: cell ? `${cell.mfr} ${cell.model} (${cell.capacityAh}Ah)` : null,
    container: container ? `${container.mfr} ${container.model} (${container.ratedEnergyMWh}MWh)` : null,
    pcs: pcs ? `${pcs.mfr} ${pcs.model} (${pcs.ratedPowerMW}MW)` : null,
  }
})

function applyScenario(s) {
  selectedScenario.value = s.id
  emit('applyConfig', {
    duration: s.duration, requiredEnergy: s.requiredEnergy,
    initContainerQty: s.initContainerQty, initPcsQty: s.initPcsQty,
    ratedEnergy: s.ratedEnergy, scenario: s.name,
  })
}

function applyToSimulation() {
  // 优先使用API数据
  let cell, container, pcs
  if (cellLibrary.value.length > 0) {
    cell = cellLibrary.value.find(c => c.id === selectedCell.value)
  } else {
    cell = localData.value.cells?.find(c => c.id === selectedCell.value)
  }
  
  if (containerLibrary.value.length > 0) {
    container = containerLibrary.value.find(c => c.id === selectedContainer.value)
  } else {
    container = localData.value.containers?.find(c => c.id === selectedContainer.value)
  }
  
  if (pcsLibrary.value.length > 0) {
    pcs = pcsLibrary.value.find(p => p.id === selectedPcs.value)
  } else {
    pcs = localData.value.pcs?.find(p => p.id === selectedPcs.value)
  }
  
  const payload = { cell, container, pcs }
  if (container) {
    payload.ratedEnergy = container.ratedEnergyMWh
    payload.acEfficiency = pcs ? pcs.efficiency : 97.03
  }
  emit('applyConfig', payload)
}

// 组件挂载时加载产品库数据
onMounted(() => {
  loadLibraryData()
})
</script>
