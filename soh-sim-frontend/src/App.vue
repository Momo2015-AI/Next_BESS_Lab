<template>
  <div class="h-screen flex flex-col overflow-hidden" style="background-color: #F5F7FA;">
    <div v-if="toast.show" class="fixed top-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transition-all"
      :style="toast.type === 'success' ? { backgroundColor: '#10b981', color: 'white' } :
              toast.type === 'error' ? { backgroundColor: '#ef4444', color: 'white' } :
              toast.type === 'warning' ? { backgroundColor: '#f59e0b', color: 'white' } :
              { backgroundColor: '#666666', color: 'white' }">
      {{ toast.message }}
    </div>

    <header class="flex justify-between items-center flex-shrink-0 z-10"
      style="background-color: #FFFFFF; border-bottom: 1px solid #E0E0E0; padding: 10px 20px;">
      <div class="flex items-center gap-4">
        <router-link to="/" class="flex items-center gap-2 cursor-pointer" style="text-decoration: none;">
          <div class="w-8 h-8 rounded-lg flex items-center justify-center" style="background-color: #2F5496; color: white;">
            <span class="text-sm font-bold">S</span>
          </div>
          <span class="font-bold text-sm hidden sm:block" style="color: #2F5496;">SOH-SIM</span>
        </router-link>
      </div>
      <div class="flex items-center gap-3">
      </div>
    </header>

    <div class="flex flex-1 overflow-hidden">
      <Sidebar />
      <main class="flex-1 overflow-auto">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import Sidebar from './components/Sidebar.vue'

const toast = reactive({
  show: false,
  message: '',
  type: 'info',
})

const showToast = (message, type = 'info') => {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => { toast.show = false }, 3000)
}

// Expose showToast globally for child component access via provide
import { provide } from 'vue'
provide('showToast', showToast)
</script>

<style scoped>
</style>
