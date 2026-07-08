<template>
  <div class="rounded-xl p-4 card-bordered">
    <h3 class="text-sm font-medium mb-4 flex items-center gap-2 text-secondary">
      <span class="w-1 h-4 rounded bg-accent-2" />
      仿真参数全局调节
    </h3>

    <div class="mb-4">
      <div class="text-[10px] font-bold uppercase mb-3 pb-2 text-muted border-b">1. 运行策略、时间与容量</div>
      <div v-for="param in strategyParams" :key="param.key" class="mb-3">
        <label class="block text-xs mb-1 text-muted">{{ param.label }}</label>
        <div v-if="param.hasSlider" class="flex items-center gap-3">
          <input
            v-model.number="state[param.key]"
            type="range"
            :min="param.min"
            :max="param.max"
            :step="param.step"
            class="flex-1 h-2 rounded-lg appearance-none cursor-pointer slider-track"
          />
          <input
            v-model.number="state[param.key]"
            type="number"
            :min="param.min"
            :max="param.max"
            :step="param.step"
            class="w-20 rounded px-2 py-1 text-xs text-right font-bold form-field-input"
          />
        </div>
        <input
          v-else
          v-model.number="state[param.key]"
          type="number"
          :min="param.min"
          :max="param.max"
          class="w-full rounded px-3 py-2 text-xs font-bold form-field-input"
        />
      </div>
    </div>

    <div class="mb-4">
      <div class="text-[10px] font-bold uppercase mb-3 pb-2 text-muted border-b">2. 效率拓扑边界</div>
      <div v-for="param in efficiencyParams" :key="param.key" class="mb-3">
        <label class="block text-xs mb-1 text-muted">{{ param.label }}</label>
        <div class="flex items-center gap-3">
          <input
            v-model.number="state[param.key]"
            type="range"
            :min="param.min"
            :max="param.max"
            :step="param.step"
            class="flex-1 h-2 rounded-lg appearance-none cursor-pointer slider-track"
          />
          <input
            v-model.number="state[param.key]"
            type="number"
            :min="param.min"
            :max="param.max"
            :step="param.step"
            class="w-20 rounded px-2 py-1 text-xs text-right font-bold form-field-input"
          />
        </div>
      </div>
    </div>

    <div class="mb-4">
      <div class="text-[10px] font-bold uppercase mb-3 pb-2 text-muted border-b">3. 4象限动静态辅助功率</div>
      <div v-for="param in auxParams" :key="param.key" class="mb-3">
        <label class="block text-xs mb-1 text-muted">{{ param.label }}</label>
        <div class="flex items-center gap-3">
          <input
            v-model.number="state[param.key]"
            type="range"
            :min="param.min"
            :max="param.max"
            :step="param.step"
            class="flex-1 h-2 rounded-lg appearance-none cursor-pointer slider-track"
          />
          <input
            v-model.number="state[param.key]"
            type="number"
            :min="param.min"
            :max="param.max"
            :step="param.step"
            class="w-20 rounded px-2 py-1 text-xs text-right font-bold form-field-input"
          />
        </div>
      </div>
    </div>

    <div>
      <div class="text-[10px] font-bold uppercase mb-3 pb-2 text-muted border-b">4. 外部固定自耗</div>
      <div v-for="param in externalParams" :key="param.key" class="mb-3">
        <label class="block text-xs mb-1 text-muted">{{ param.label }}</label>
        <div class="flex items-center gap-3">
          <input
            v-model.number="state[param.key]"
            type="range"
            :min="param.min"
            :max="param.max"
            :step="param.step"
            class="flex-1 h-2 rounded-lg appearance-none cursor-pointer slider-track"
          />
          <input
            v-model.number="state[param.key]"
            type="number"
            :min="param.min"
            :max="param.max"
            :step="param.step"
            class="w-20 rounded px-2 py-1 text-xs text-right font-bold form-field-input"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { strategyParams, efficiencyParams, auxParams, externalParams } from '../composables/useAuxPower.js'

const state = defineModel({ type: Object, required: true })
</script>

<style scoped src="../assets/styles/aux-power.css"></style>
