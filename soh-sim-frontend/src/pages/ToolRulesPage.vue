<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>配置规则</h1>
      <p>管理系统配置规则与约束</p>
    </div>
    <SectionCard number="00" title="规则引擎" subtitle="功能开发中">
      <p class="placeholder-text">
        Grid Code 合规规则、电池配置约束、财务计算规则等将集中在此管理。
      </p>
    </SectionCard>
  </div>
</template>

<script setup>
import SectionCard from '../components/SectionCard.vue'
</script>

<style scoped>
.placeholder-text {
  color: var(--color-text-muted);
  font-size: 14px;
  text-align: center;
  padding: 16px 0;
}
</style>
