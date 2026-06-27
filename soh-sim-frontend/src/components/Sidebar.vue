<template>
  <aside class="sidebar w-64 flex-shrink-0 overflow-hidden flex flex-col" style="background-color: #FFFFFF; border-right: 1px solid #E0E0E0;">
    <nav class="flex-1 overflow-y-auto p-3">
      <div class="mb-6">
        <button
          @click="$router.push('/')"
          class="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all"
          :class="$route.path === '/' ? 'sidebar-active' : 'sidebar-item'">
          <span>🏠</span>
          <span>{{ $t('sidebar.home') }}</span>
        </button>
      </div>

      <div class="mb-6">
        <div class="text-xs font-semibold uppercase tracking-wider mb-2 px-2" style="color: #999999;">项目流程</div>
        <button
          v-for="item in phaseItems"
          :key="item.id"
          @click="$router.push(item.path)"
          class="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all"
          :class="$route.path === item.path ? 'sidebar-active' : 'sidebar-item'">
          <span class="status-dot" :class="'dot-' + item.status"></span>
          <span>{{ item.label }}</span>
          <span v-if="item.status === 'completed'" class="ml-auto text-xs" style="color: #2e7d32;">&#10003;</span>
        </button>
      </div>

      <div class="mb-6">
        <div class="text-xs font-semibold uppercase tracking-wider mb-2 px-2" style="color: #999999;">专用工具</div>
        <button
          v-for="item in toolItems"
          :key="item.id"
          @click="$router.push(item.path)"
          class="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all"
          :class="$route.path === item.path ? 'sidebar-active' : 'sidebar-item'">
          <span>{{ item.icon }}</span>
          <span>{{ item.label }}</span>
        </button>
      </div>
    </nav>

    <div class="p-4 border-t" style="border-color: #E0E0E0;">
      <button
        @click="$router.push('/auth')"
        class="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all"
        :class="$route.path === '/auth' ? 'sidebar-active' : 'sidebar-item'">
        <span>🔐</span>
        <span>{{ $t('sidebar.auth') }}</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useBessStore } from '../stores/bess.js'

const store = useBessStore()

const toolItems = [
  { id: 'formula', path: '/tools/formula', label: '算法与公式', icon: '🔬' },
  { id: 'auxpower', path: '/tools/auxpower', label: '辅助功耗', icon: '⚡' },
  { id: 'engineering', path: '/tools/engineering', label: '工程计算', icon: '🏗' },
  { id: 'datainject', path: '/tools/datainject', label: '数据注入', icon: '📥' },
  { id: 'conditions', path: '/tools/conditions', label: '运行工况', icon: '🌤' },
  { id: 'params', path: '/tools/params', label: '参数面板', icon: '⚙' },
](() => [
  { id: 'phase1', path: '/phase1', label: 'Phase 1: 项目立项', status: store.phases.phase1.status },
  { id: 'phase2', path: '/phase2', label: 'Phase 2: 系统设计', status: store.phases.phase2.status },
  { id: 'phase3', path: '/phase3', label: 'Phase 3: 性能分析', status: store.phases.phase3.status },
  { id: 'phase4', path: '/phase4', label: 'Phase 4: 经济评估', status: store.phases.phase4.status },
  { id: 'phase5', path: '/phase5', label: 'Phase 5: 成果输出', status: store.phases.phase5.status },
])
</script>

<style scoped>
.sidebar-item { color: #666666; cursor: pointer; }
.sidebar-item:hover { background-color: #F5F7FA; color: #2F5496; }
.sidebar-active { background-color: #E8EEF5; color: #2F5496; font-weight: 600; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; flex-shrink: 0; }
.dot-pending { background: #ccc; }
.dot-in_progress { background: #2F5496; }
.dot-completed { background: #2e7d32; }
</style>
