<template>
  <div class="home-page h-full overflow-auto p-8">
    <div class="max-w-6xl mx-auto">
      <div class="mb-8">
        <h1 class="text-2xl font-bold" style="color: #2F5496;">{{ $t('home.title') }}</h1>
        <p class="text-sm mt-2" style="color: #666666;">{{ $t('home.subtitle') }}</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div 
          @click="$emit('navigate', 'survey')"
          class="oracle-card cursor-pointer group"
          style="border: 1px solid #E0E0E0;">
          <div class="p-6">
            <div class="w-12 h-12 rounded-lg mb-4 flex items-center justify-center" style="background-color: #F7931E; color: white;">
              <span class="text-xl">📋</span>
            </div>
            <h3 class="text-lg font-bold mb-2" style="color: #2F5496;">{{ $t('home.survey.title') }}</h3>
            <p class="text-sm" style="color: #666666;">{{ $t('home.survey.desc') }}</p>
            <div class="mt-4 flex items-center text-sm" style="color: #2F5496; opacity: 0; group-hover: opacity: 1; transition: opacity 0.2s;">
              <span>{{ $t('home.learnMore') }}</span>
              <span class="ml-1">→</span>
            </div>
          </div>
        </div>

        <div 
          @click="$emit('navigate', 'foundation')"
          class="oracle-card cursor-pointer group"
          style="border: 1px solid #E0E0E0;">
          <div class="p-6">
            <div class="w-12 h-12 rounded-lg mb-4 flex items-center justify-center" style="background-color: #2F5496; color: white;">
              <span class="text-xl">⚙️</span>
            </div>
            <h3 class="text-lg font-bold mb-2" style="color: #2F5496;">{{ $t('home.foundation.title') }}</h3>
            <p class="text-sm" style="color: #666666;">{{ $t('home.foundation.desc') }}</p>
            <div class="mt-4 flex items-center text-sm" style="color: #2F5496; opacity: 0; group-hover: opacity: 1; transition: opacity 0.2s;">
              <span>{{ $t('home.learnMore') }}</span>
              <span class="ml-1">→</span>
            </div>
          </div>
        </div>

        <div 
          @click="$emit('navigate', 'solution')"
          class="oracle-card cursor-pointer group"
          style="border: 1px solid #E0E0E0;">
          <div class="p-6">
            <div class="w-12 h-12 rounded-lg mb-4 flex items-center justify-center" style="background-color: #4A7BC4; color: white;">
              <span class="text-xl">🚀</span>
            </div>
            <h3 class="text-lg font-bold mb-2" style="color: #2F5496;">{{ $t('home.solution.title') }}</h3>
            <p class="text-sm" style="color: #666666;">{{ $t('home.solution.desc') }}</p>
            <div class="mt-4 flex items-center text-sm" style="color: #2F5496; opacity: 0; group-hover: opacity: 1; transition: opacity 0.2s;">
              <span>{{ $t('home.learnMore') }}</span>
              <span class="ml-1">→</span>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-8">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div class="oracle-section" style="border: 1px solid #E0E0E0;">
            <div class="p-6 border-b" style="border-color: #E0E0E0;">
              <h2 class="text-lg font-bold" style="color: #2F5496;">{{ $t('home.foundation.title') }}</h2>
            </div>
            <div class="p-6 grid grid-cols-2 gap-4">
              <div 
                v-for="item in foundationItems" 
                :key="item.id"
                @click="$emit('navigate', item.id)"
                class="oracle-tile cursor-pointer p-4 rounded-lg"
                style="background-color: #F5F7FA; border: 1px solid #E0E0E0;">
                <div class="text-sm font-medium mb-1" style="color: #2F5496;">{{ item.label }}</div>
                <div class="text-xs" style="color: #666666;">{{ item.desc }}</div>
              </div>
            </div>
          </div>

          <div class="oracle-section" style="border: 1px solid #E0E0E0;">
            <div class="p-6 border-b" style="border-color: #E0E0E0;">
              <h2 class="text-lg font-bold" style="color: #2F5496;">{{ $t('home.solution.title') }}</h2>
            </div>
            <div class="p-6 grid grid-cols-2 gap-4">
              <div 
                v-for="item in solutionItems" 
                :key="item.id"
                @click="$emit('navigate', item.id)"
                class="oracle-tile cursor-pointer p-4 rounded-lg"
                style="background-color: #F5F7FA; border: 1px solid #E0E0E0;">
                <div class="text-sm font-medium mb-1" style="color: #2F5496;">{{ item.label }}</div>
                <div class="text-xs" style="color: #666666;">{{ item.desc }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineEmits(['navigate'])

const foundationItems = ref([
  { id: 'param', label: '参数配置面板', desc: '基础参数统一管理' },
  { id: 'conditions', label: '运行工况', desc: '运行条件定义' },
  { id: 'products', label: '产品与方案配置', desc: '产品库管理' },
  { id: 'batteryPCS', label: '电池与PCS配对', desc: '设备匹配配置规则' },
  { id: 'formula', label: '算法与公式', desc: '算法模型配置' },
])

const solutionItems = ref([
  { id: 'dc-design', label: '直流侧设计', desc: '电池系统设计' },
  { id: 'ac-design', label: '交流侧设计', desc: 'PCS系统设计' },
  { id: 'simulationLab', label: '仿真实验室', desc: 'SOH/RTE计算' },
  { id: 'financial', label: '财务看板', desc: '财务指标分析' },
  { id: 'matrix', label: '生命周期矩阵', desc: '25年数据表格' },
  { id: 'inject', label: '数据注入', desc: 'SOH/RTE修正' },
  { id: 'chart', label: '可视化图表', desc: '曲线展示' },
  { id: 'scenario', label: '多场景对比', desc: '方案比较' },
  { id: 'sensitivity', label: '敏感性分析', desc: '参数影响评估' },
  { id: 'engineering', label: '工程计算', desc: '辅助计算' },
  { id: 'export', label: '数据导出', desc: '报告生成' },
])
</script>

<style scoped>
.oracle-card {
  background-color: #FFFFFF;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.oracle-card:hover {
  box-shadow: 0 4px 12px rgba(47, 84, 150, 0.15);
  border-color: #2F5496;
  transform: translateY(-2px);
}

.oracle-section {
  background-color: #FFFFFF;
  border-radius: 8px;
}

.oracle-tile {
  transition: all 0.2s ease;
}

.oracle-tile:hover {
  background-color: #E8EEF5;
  border-color: #2F5496;
}

.group:hover .opacity-0 {
  opacity: 1 !important;
}
</style>
