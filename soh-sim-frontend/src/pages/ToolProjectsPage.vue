<template>
  <div class="tool-page">
    <div class="tool-header">
      <h1>历史项目</h1>
      <p>查看和管理历史项目记录</p>
    </div>
    <div class="placeholder">
      <p class="text-lg mb-2" style="color: var(--color-text-muted)">项目历史功能开发中</p>
      <p style="color: var(--color-text-secondary); font-size: 14px">
        项目数据将通过后端 API 持久化，支持版本管理和历史回溯。
      </p>
    </div>
  </div>
</template>

<script setup></script>

<style scoped>
.tool-page {
  padding: 24px;
}
.tool-header {
  margin-bottom: 24px;
}
.tool-header h1 {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 8px;
  color: var(--color-text);
}
.tool-header p {
  color: #666;
  font-size: 14px;
  margin: 0;
}
.placeholder {
  background: var(--color-card);
  border-radius: 12px;
  padding: 48px 24px;
  text-align: center;
  border: 1px dashed var(--color-border);
}
</style>
