<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>配置规则</h1>
      <p>管理系统配置规则与约束</p>
    </div>
    <div class="placeholder">
      <p class="text-lg mb-2" style="color: var(--color-text-muted);">规则引擎配置开发中</p>
      <p style="color: var(--color-text-secondary); font-size: 14px;">
        Grid Code 合规规则、电池配置约束、财务计算规则等将集中在此管理。
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
