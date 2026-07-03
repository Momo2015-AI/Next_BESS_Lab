<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>工程计算</h1>
      <p>场地面积、BOM 清单、备品备件、充放电时间</p>
    </div>
    <EngineeringCalc @error="(msg) => $emit('error', msg)" />
  </div>
</template>

<script setup>
import EngineeringCalc from '../components/EngineeringCalc.vue'
</script>

<style scoped></style>
