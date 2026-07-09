<template>
  <div
    class="fixed left-0 top-0 h-full w-64 bg-gray-900 text-white shadow-xl z-50 transform transition-transform duration-300 ease-in-out"
    :class="{ '-translate-x-full': !isOpen, 'translate-x-0': isOpen }"
  >
    <!-- Logo/Header -->
    <div class="p-4 border-b border-gray-700 flex items-center">
      <div
        class="bg-gradient-to-r from-blue-500 to-purple-600 w-10 h-10 rounded-lg flex items-center justify-center mr-3"
      >
        <span class="font-bold">ES</span>
      </div>
      <h1 class="text-xl font-bold">{{ $t('sidebar.platform') }}</h1>
    </div>

    <!-- Navigation Menu -->
    <nav class="mt-6">
      <ul>
        <li v-for="item in menuItems" :key="item.id" class="mb-1">
          <a
            href="#"
            class="flex items-center px-6 py-3 text-sm font-medium hover:bg-gray-800 hover:text-white transition-colors duration-200"
            :class="{ 'bg-gray-800 text-white border-l-4 border-blue-500': activeTab === item.id }"
            @click.prevent="selectTab(item.id)"
          >
            <span class="mr-3">{{ item.icon }}</span>
            <span>{{ $t(item.title) }}</span>
          </a>
        </li>
      </ul>
    </nav>

    <!-- User Profile Section -->
    <div class="absolute bottom-0 w-full p-4 border-t border-gray-700">
      <div class="flex items-center">
        <div
          class="w-10 h-10 rounded-full bg-gradient-to-r from-green-400 to-blue-500 flex items-center justify-center"
        >
          <span class="font-bold">U</span>
        </div>
        <div class="ml-3">
          <p class="text-sm font-medium">{{ $t('sidebar.userName') }}</p>
          <p class="text-xs text-gray-400">{{ $t('sidebar.engineer') }}</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Overlay for mobile -->
  <div v-if="isOpen" class="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden" @click="toggleSidebar" />
</template>

<script setup>
import { ref, defineEmits } from 'vue'

const emit = defineEmits(['tab-change'])

const isOpen = ref(true)

// 定义菜单项
const menuItems = ref([
  { id: 'dashboard', title: 'sidebar.dashboard', icon: '📊' },
  { id: 'simulation', title: 'sidebar.simulation', icon: '🔬' },
  { id: 'design', title: 'sidebar.design', icon: '⚙️' },
  { id: 'analysis', title: 'sidebar.analysis', icon: '📈' },
  { id: 'optimization', title: 'sidebar.optimization', icon: '🎯' },
  { id: 'configuration', title: 'sidebar.configuration', icon: '🔧' },
  { id: 'reports', title: 'sidebar.reports', icon: '📋' },
  { id: 'settings', title: 'sidebar.settings', icon: '⚙️' }
])

const activeTab = ref('dashboard')

const selectTab = (tabId) => {
  activeTab.value = tabId
  emit('tab-change', tabId)
}

const toggleSidebar = () => {
  isOpen.value = !isOpen.value
}

// 暴露方法供父组件调用
defineExpose({
  toggleSidebar,
  isOpen
})
</script>

<style scoped>
/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: var(--color-text);
}

::-webkit-scrollbar-thumb {
  background: #4b5563;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--color-text-secondary);
}
</style>
