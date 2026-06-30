<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>报告输出</h1>
      <p>生成仿真报告、导出 PDF/Excel</p>
    </div>
    <div class="placeholder">
      <p class="text-lg mb-2" style="color: var(--color-text-muted);">报告生成功能开发中</p>
      <p style="color: var(--color-text-secondary); font-size: 14px;">
        请前往 <router-link to="/phase2" style="color: var(--color-accent);">Phase 2 分析页</router-link> 查看仿真结果，或使用
        <router-link to="/tools/simulation-view" style="color: var(--color-accent);">仿真分析</router-link> 运行仿真后导出 CSV。
      </p>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.tool-page { padding: 24px; }
.tool-header { margin-bottom: 24px; }
.tool-header h1 { font-size: 24px; font-weight: 700; margin: 0 0 8px; color: var(--color-text); }
.tool-header p { color: #666; font-size: 14px; margin: 0; }
.placeholder { background: var(--color-card); border-radius: 12px; padding: 48px 24px; text-align: center; border: 1px dashed var(--color-border); }
</style>
