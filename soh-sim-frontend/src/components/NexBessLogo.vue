<template>
  <div class="nexbess-logo" :class="{ 'is-static': !hoverable, 'is-compact': compact }">
    <!-- X-Mobius 图标 -->
    <svg class="nx-svg" viewBox="0 0 88 50" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <defs>
        <linearGradient :id="staticGradId" x1="4" y1="25" x2="84" y2="25" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#8898C8" />
          <stop offset="45%" stop-color="#B0B8DD" />
          <stop offset="55%" stop-color="#B0B8DD" />
          <stop offset="100%" stop-color="#4E5E9A" />
        </linearGradient>
        <linearGradient :id="glowId" x1="4" y1="25" x2="84" y2="25" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#00E5FF" />
          <stop offset="45%" stop-color="#FFFFFF" />
          <stop offset="55%" stop-color="#FFFFFF" />
          <stop offset="100%" stop-color="#3A8BFF" />
        </linearGradient>
      </defs>

      <!-- 静态路径：蓝紫色渐变 -->
      <path
        class="nx-path nx-path--static"
        d="M16 6C24 6 36 20 44 25C52 30 64 44 72 44C80 44 84 36 84 25C84 14 80 6 72 6C64 6 52 20 44 25C36 30 24 44 16 44C8 44 4 36 4 25C4 14 8 6 16 6Z"
        stroke-width="7.5"
        stroke-linecap="round"
        stroke-linejoin="round"
        :stroke="`url(#${staticGradId})`"
      />

      <!-- 动态光流路径：hover 时渐显 -->
      <path
        class="nx-path nx-path--glow"
        d="M16 6C24 6 36 20 44 25C52 30 64 44 72 44C80 44 84 36 84 25C84 14 80 6 72 6C64 6 52 20 44 25C36 30 24 44 16 44C8 44 4 36 4 25C4 14 8 6 16 6Z"
        :stroke="`url(#${glowId})`"
        stroke-width="7.5"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
    </svg>

    <!-- 品牌文字：X 字号加大并与图标颜色呼应 -->
    <span class="nx-text" aria-label="NEXBessLab">
      <span class="nx-t-ne">NE</span>
      <span class="nx-t-x">X</span>
      <span class="nx-t-bess">Bess</span>
      <span class="nx-t-dot">.</span>
      <span class="nx-t-lab">Lab</span>
    </span>
  </div>
</template>

<script setup>
defineProps({
  /** 是否启用 hover 光流动效 */
  hoverable: { type: Boolean, default: true },
  /** 紧凑模式（更适合 header 等小空间） */
  compact: { type: Boolean, default: false }
})

let _idCounter = 0
const glowId = `nx-glow-${++_idCounter}`
const staticGradId = `nx-static-${++_idCounter}`
</script>

<style scoped>
/* ==========================================================================
   NEXBess Logo 组件 —— 双主题适配 + X-Mobius 虚空光流
   ========================================================================== */

.nexbess-logo {
  display: inline-flex;
  align-items: center;
  gap: 18px;
  user-select: none;
  cursor: default;
  background: transparent;
}

/* 有 hoverable 时才显示 pointer */
.nexbess-logo:not(.is-static) {
  cursor: pointer;
}

/* ==========================================================================
   SVG 图标
   ========================================================================== */
.nx-svg {
  width: 88px;
  height: 50px;
  flex-shrink: 0;
  transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

.nexbess-logo:not(.is-static):hover .nx-svg {
  transform: scale(1.06);
}

/* 紧凑模式缩小图标 */
.nexbess-logo.is-compact .nx-svg {
  width: 74px;
  height: 42px;
}

/* ==========================================================================
   X 路径层叠：静态材质 + 动态光流
   ========================================================================== */
.nx-path {
  transition: opacity 0.4s ease;
}

/* 静态层：蓝紫色渐变 */
.nx-path--static {
  opacity: 1;
}

/* 动态光流层：默认隐藏 */
.nx-path--glow {
  opacity: 0;
}

/* hover: 静态层淡出，光流层淡入并启动流动动画 */
.nexbess-logo:not(.is-static):hover .nx-path--static {
  opacity: 0;
}
.nexbess-logo:not(.is-static):hover .nx-path--glow {
  opacity: 1;
  stroke-dasharray: 400;
  animation: nx-flow 3.2s linear infinite;
}

@keyframes nx-flow {
  0% {
    stroke-dashoffset: 400;
  }
  100% {
    stroke-dashoffset: -400;
  }
}

/* ==========================================================================
   品牌文字
   ========================================================================== */
.nx-text {
  display: flex;
  align-items: baseline;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  letter-spacing: -0.5px;
  white-space: nowrap;
}

/* NE —— 与 BESS 统一字重 */
.nx-t-ne {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text);
}

/* X —— 加大 + 主题色呼应图标 */
.nx-t-x {
  font-size: 36px;
  font-weight: 700;
  color: var(--color-accent);
  line-height: 0.9;
}

/* Bess —— 稳重粗体 */
.nx-t-bess {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text);
}

/* Lab —— 与 Bess 一致 */
.nx-t-lab {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text);
}

/* . —— 主题色光晕 */
.nx-t-dot {
  font-size: 28px;
  font-weight: 800;
  color: var(--color-accent);
  margin-left: 1px;
}

/* 紧凑模式文字缩小 */
.nexbess-logo.is-compact .nx-t-ne,
.nexbess-logo.is-compact .nx-t-bess,
.nexbess-logo.is-compact .nx-t-lab,
.nexbess-logo.is-compact .nx-t-dot {
  font-size: 24px;
}
.nexbess-logo.is-compact .nx-t-x {
  font-size: 30px;
}
.nexbess-logo.is-compact {
  gap: 14px;
}
</style>
