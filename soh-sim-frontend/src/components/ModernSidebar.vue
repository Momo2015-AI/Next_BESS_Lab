<template>
  <div class="fixed left-0 top-0 h-full w-64 bg-gray-900 text-white shadow-xl z-50 transform transition-transform duration-300 ease-in-out" 
       :class="{ '-translate-x-full': !isOpen, 'translate-x-0': isOpen }">
    <!-- Logo/Header -->
    <div class="p-4 border-b border-gray-700 flex items-center">
      <div class="bg-gradient-to-r from-blue-500 to-purple-600 w-10 h-10 rounded-lg flex items-center justify-center mr-3">
        <span class="font-bold">ES</span>
      </div>
      <h1 class="text-xl font-bold">储能系统仿真平台</h1>
    </div>

    <!-- Navigation Menu -->
    <nav class="mt-6">
      <ul>
        <li v-for="item in menuItems" :key="item.id" class="mb-1">
          <a href="#" @click.prevent="selectTab(item.id)"
             class="flex items-center px-6 py-3 text-sm font-medium hover:bg-gray-800 hover:text-white transition-colors duration-200"
             :class="{ 'bg-gray-800 text-white border-l-4 border-blue-500': activeTab === item.id }">
            <span class="mr-3">{{ item.icon }}</span>
            <span>{{ item.title }}</span>
          </a>
        </li>
      </ul>
    </nav>

    <!-- User Profile Section -->
    <div class="absolute bottom-0 w-full p-4 border-t border-gray-700">
      <div class="flex items-center">
        <div class="w-10 h-10 rounded-full bg-gradient-to-r from-green-400 to-blue-500 flex items-center justify-center">
          <span class="font-bold">U</span>
        </div>
        <div class="ml-3">
          <p class="text-sm font-medium">用户名称</p>
          <p class="text-xs text-gray-400">储能工程师</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Overlay for mobile -->
  <div v-if="isOpen" @click="toggleSidebar" class="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden"></div>
</template>

<script setup>
import { ref, defineEmits } from 'vue';

const emit = defineEmits(['tab-change']);

const isOpen = ref(true);

// 定义菜单项
const menuItems = ref([
  { id: 'dashboard', title: '仪表盘', icon: '📊' },
  { id: 'simulation', title: '仿真实验室', icon: '🔬' },
  { id: 'design', title: '系统设计', icon: '⚙️' },
  { id: 'analysis', title: '财务分析', icon: '📈' },
  { id: 'optimization', title: '策略优化', icon: '🎯' },
  { id: 'configuration', title: '配置管理', icon: '🔧' },
  { id: 'reports', title: '报告中心', icon: '📋' },
  { id: 'settings', title: '系统设置', icon: '⚙️' }
]);

const activeTab = ref('dashboard');

const selectTab = (tabId) => {
  activeTab.value = tabId;
  emit('tab-change', tabId);
};

const toggleSidebar = () => {
  isOpen.value = !isOpen.value;
};

// 暴露方法供父组件调用
defineExpose({
  toggleSidebar,
  isOpen
});
</script>

<style scoped>
/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #1f2937;
}

::-webkit-scrollbar-thumb {
  background: #4b5563;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #6b7280;
}
</style>