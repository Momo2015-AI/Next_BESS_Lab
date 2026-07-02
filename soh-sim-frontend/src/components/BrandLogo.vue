<template>
  <router-link to="/" class="brand-logo">
    <svg class="brand-svg" width="88" height="50" viewBox="0 0 88 50" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path
        class="brand-x-path"
        d="M16 6C24 6 36 20 44 25C52 30 64 44 72 44C80 44 84 36 84 25C84 14 80 6 72 6C64 6 52 20 44 25C36 30 24 44 16 44C8 44 4 36 4 25C4 14 8 6 16 6Z"
        stroke="url(#staticDarkTitanium)"
        stroke-width="7.5"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
      <defs>
        <linearGradient id="staticDarkTitanium" x1="4" y1="6" x2="84" y2="44" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#222F4D" />
          <stop offset="50%" stop-color="#5572B5" />
          <stop offset="100%" stop-color="#1A253E" />
        </linearGradient>
        <linearGradient id="pureVoidGlow" x1="4" y1="25" x2="84" y2="25" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#00E5FF" />
          <stop offset="50%" stop-color="#FFFFFF" />
          <stop offset="100%" stop-color="#3A8BFF" />
        </linearGradient>
      </defs>
    </svg>

    <div class="brand-text">
      <span class="brand-nex">NEX</span>
      <span class="brand-bess">Bess</span>
      <span class="brand-dot">.</span>
    </div>
  </router-link>
</template>

<style scoped>
.brand-logo {
  display: flex;
  align-items: center;
  gap: 16px;
  text-decoration: none;
  user-select: none;
}

.brand-svg {
  flex-shrink: 0;
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.brand-x-path {
  opacity: 0.9;
  stroke-dasharray: 400;
  stroke-dashoffset: 0;
  transition:
    stroke 0.4s ease,
    opacity 0.4s ease;
}

.brand-logo:hover .brand-svg {
  transform: scale(1.06);
}

.brand-logo:hover .brand-x-path {
  opacity: 1;
  stroke: url(#pureVoidGlow);
  animation: xFlow 3.2s linear infinite;
}

@keyframes xFlow {
  0% {
    stroke-dashoffset: 400;
  }
  100% {
    stroke-dashoffset: -400;
  }
}

.brand-text {
  display: flex;
  align-items: baseline;
  letter-spacing: -0.5px;
}

.brand-nex {
  font-size: 22px;
  font-weight: 200;
  color: var(--text-primary);
  opacity: 0.95;
}

.brand-bess {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
}

.brand-dot {
  font-size: 22px;
  font-weight: 800;
  color: var(--accent-blue);
  margin-left: 1px;
  filter: drop-shadow(0 0 4px var(--accent-blue));
}
</style>
