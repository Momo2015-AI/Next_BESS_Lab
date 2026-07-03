<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>历史项目</h1>
      <p>查看和管理历史项目记录</p>
    </div>
    <SectionCard number="00" title="项目历史" subtitle="功能开发中">
      <p class="placeholder-text">项目数据将通过后端 API 持久化，支持版本管理和历史回溯。</p>
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
