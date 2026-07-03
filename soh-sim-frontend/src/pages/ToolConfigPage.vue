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
.mt-4 {
  margin-top: 16px;
}
</style>
