<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>{{ $t('tools.configTitle') }}</h1>
      <p>{{ $t('tools.configDesc') }}</p>
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
