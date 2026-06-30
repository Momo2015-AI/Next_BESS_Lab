<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>校正因子模板</h1>
      <p>管理 Arrhenius 等模型的校正因子模板</p>
    </div>
    <div class="placeholder">
      <p class="text-lg mb-2" style="color: var(--color-text-muted);">模板管理功能开发中</p>
      <p style="color: var(--color-text-secondary); font-size: 14px;">
        算法模型的校正因子预设模板将在此管理，支持按电池厂家/化学类型筛选和自定义。
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
