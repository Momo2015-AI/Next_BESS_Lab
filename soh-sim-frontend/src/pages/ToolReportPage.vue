<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>报告输出</h1>
      <p>生成仿真报告、导出 PDF/Excel</p>
    </div>
    <SectionCard number="00" title="报告生成" subtitle="功能开发中">
      <p class="placeholder-text">
        请前往
        <router-link to="/phase2" class="inline-link">Phase 2 分析页</router-link>
        查看仿真结果，或使用
        <router-link to="/tools/simulation-view" class="inline-link">仿真分析</router-link>
        运行仿真后导出 CSV。
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
.inline-link {
  color: var(--color-accent);
  text-decoration: none;
  font-weight: 500;
}
.inline-link:hover {
  text-decoration: underline;
}
</style>
