<template>
  <AppPage title-key="tools.configTitle" desc-key="tools.configDesc">
    <BatteryPCSConfig />
    <BatteryDCDesign class="mt-4" />
    <PcsACDesign class="mt-4" />
  </AppPage>
</template>

<script setup>
import AppPage from '../components/AppPage.vue'
import BatteryPCSConfig from '../components/BatteryPCSConfig.vue'
import BatteryDCDesign from '../components/BatteryDCDesign.vue'
import PcsACDesign from '../components/PcsACDesign.vue'
</script>

<style scoped>
.mt-4 {
  margin-top: 16px;
}
</style>
