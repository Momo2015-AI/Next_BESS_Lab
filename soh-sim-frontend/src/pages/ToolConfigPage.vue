<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>方案设计</h1>
      <p>电池系统配置（电池集装箱 + DC侧 + PCS/AC侧）</p>
    </div>
    <BatteryPCSConfig />
    <BatteryDCDesign class="mt-4" />
  </div>
</template>

<script setup>
import BatteryPCSConfig from '../components/BatteryPCSConfig.vue'
import BatteryDCDesign from '../components/BatteryDCDesign.vue'
</script>

<style scoped>
.tool-page { padding: 24px; }
.tool-header { margin-bottom: 24px; }
.tool-header h1 { font-size: 24px; font-weight: 700; margin: 0 0 8px; color: var(--color-text); }
.tool-header p { color: #666; font-size: 14px; margin: 0; }
.mt-4 { margin-top: 16px; }
</style>
