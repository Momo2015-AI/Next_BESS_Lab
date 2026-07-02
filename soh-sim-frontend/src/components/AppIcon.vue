<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    :stroke="color || 'var(--icon-color)'"
    :stroke-width="strokeWidth"
    stroke-linecap="round"
    stroke-linejoin="round"
    :class="['app-icon', { 'app-icon-spin': spin }]"
    xmlns="http://www.w3.org/2000/svg"
  >
    <!-- Nav -->
    <template v-if="name === 'home'">
      <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
      <polyline points="9 22 9 12 15 12 15 22" />
    </template>
    <template v-else-if="name === 'chevron-right'">
      <polyline points="9 18 15 12 9 6" />
    </template>
    <template v-else-if="name === 'chevron-down'">
      <polyline points="6 9 12 15 18 9" />
    </template>
    <template v-else-if="name === 'chevron-left'">
      <polyline points="15 18 9 12 15 6" />
    </template>
    <template v-else-if="name === 'sidebar'">
      <polyline points="4 17 10 11 4 5" /><line x1="12" y1="19" x2="20" y2="19" />
    </template>
    <template v-else-if="name === 'menu'">
      <line x1="3" y1="6" x2="21" y2="6" /><line x1="3" y1="12" x2="21" y2="12" /><line x1="3" y1="18" x2="21" y2="18" />
    </template>

    <!-- Battery & Energy -->
    <template v-else-if="name === 'battery'">
      <rect x="1" y="6" width="18" height="12" rx="2" />
      <line x1="22" y1="10" x2="22" y2="14" />
      <line x1="7" y1="10" x2="7" y2="14" />
      <line x1="11" y1="7" x2="11" y2="17" />
      <line x1="15" y1="9" x2="15" y2="15" />
    </template>
    <template v-else-if="name === 'lightning'">
      <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
    </template>
    <template v-else-if="name === 'soh-ring'">
      <path d="M12 2a10 10 0 100 20 10 10 0 000-20z" /><circle cx="12" cy="12" r="4" />
    </template>
    <template v-else-if="name === 'clock-cycle'">
      <circle cx="12" cy="12" r="10" /><path d="M12 6v6l4 2" />
    </template>
    <template v-else-if="name === 'waveform'">
      <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
    </template>

    <!-- Charts -->
    <template v-else-if="name === 'bar-chart'">
      <line x1="18" y1="20" x2="18" y2="10" /><line x1="12" y1="20" x2="12" y2="4" /><line x1="6" y1="20" x2="6" y2="14" />
    </template>
    <template v-else-if="name === 'line-chart'">
      <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
    </template>
    <template v-else-if="name === 'pie-chart'">
      <path d="M21.21 15.89A10 10 0 118 2.83" /><path d="M22 12A10 10 0 0012 2v10z" />
    </template>
    <template v-else-if="name === 'target'">
      <circle cx="12" cy="12" r="10" /><circle cx="12" cy="12" r="6" /><circle cx="12" cy="12" r="2" />
    </template>
    <template v-else-if="name === 'monitor'">
      <rect x="2" y="3" width="20" height="14" rx="2" /><line x1="8" y1="21" x2="16" y2="21" /><line x1="12" y1="17" x2="12" y2="21" />
    </template>

    <!-- Tools & Actions -->
    <template v-else-if="name === 'search'">
      <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
    </template>
    <template v-else-if="name === 'settings'">
      <circle cx="12" cy="12" r="3" />
      <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 01-2.83 2.83l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 012.83-2.83l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z" />
    </template>
    <template v-else-if="name === 'upload'">
      <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" /><polyline points="17 8 12 3 7 8" /><line x1="12" y1="3" x2="12" y2="15" />
    </template>
    <template v-else-if="name === 'download'">
      <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" /><polyline points="7 10 12 15 17 10" /><line x1="12" y1="15" x2="12" y2="3" />
    </template>
    <template v-else-if="name === 'edit'">
      <path d="M12 20h9" /><path d="M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z" />
    </template>
    <template v-else-if="name === 'trash'">
      <polyline points="3 6 5 6 21 6" /><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" />
    </template>
    <template v-else-if="name === 'loading'">
      <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
    </template>
    <template v-else-if="name === 'wrench'">
      <path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z" />
    </template>
    <template v-else-if="name === 'info'">
      <circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" />
    </template>
    <template v-else-if="name === 'code'">
      <rect x="2" y="3" width="20" height="18" rx="3" /><path d="M6 9l4 4-4 4" /><line x1="13" y1="15" x2="18" y2="15" />
    </template>

    <!-- Status & Feedback -->
    <template v-else-if="name === 'check-circle'">
      <path d="M22 11.08V12a10 10 0 11-5.93-9.14" /><polyline points="22 4 12 14.01 9 11.01" />
    </template>
    <template v-else-if="name === 'x-circle'">
      <circle cx="12" cy="12" r="10" /><line x1="15" y1="9" x2="9" y2="15" /><line x1="9" y1="9" x2="15" y2="15" />
    </template>
    <template v-else-if="name === 'alert'">
      <circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><circle cx="12" cy="16" r="0.8" fill="currentColor" />
    </template>
    <template v-else-if="name === 'danger'">
      <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" /><line x1="12" y1="9" x2="12" y2="13" /><circle cx="12" cy="17" r="0.8" fill="currentColor" />
    </template>
    <template v-else-if="name === 'trending-up'">
      <circle cx="12" cy="12" r="10" /><polyline points="8 14 11 11 13 13 16 10" />
    </template>
    <template v-else-if="name === 'trending-down'">
      <circle cx="12" cy="12" r="10" /><polyline points="8 10 11 13 13 11 16 14" />
    </template>
    <template v-else-if="name === 'stable'">
      <circle cx="12" cy="12" r="10" /><line x1="8" y1="12" x2="16" y2="12" />
    </template>

    <!-- User & Auth -->
    <template v-else-if="name === 'user'">
      <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" /><circle cx="12" cy="7" r="4" />
    </template>
    <template v-else-if="name === 'lock'">
      <rect x="3" y="11" width="18" height="11" rx="2" /><path d="M7 11V7a5 5 0 0110 0v4" />
    </template>
    <template v-else-if="name === 'shield'">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
    </template>

    <!-- Misc -->
    <template v-else-if="name === 'dollar'">
      <line x1="12" y1="1" x2="12" y2="23" /><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6" />
    </template>
    <template v-else-if="name === 'flask'">
      <path d="M12 2.69l5.66 5.66a8 8 0 11-11.31 0z" />
    </template>
    <template v-else-if="name === 'document'">
      <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" /><polyline points="14 2 14 8 20 8" /><line x1="16" y1="13" x2="8" y2="13" /><line x1="16" y1="17" x2="8" y2="17" />
    </template>
    <template v-else-if="name === 'sun'">
      <circle cx="12" cy="12" r="5" />
      <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" />
    </template>
    <template v-else-if="name === 'moon'">
      <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" />
    </template>
    <template v-else-if="name === 'close'">
      <rect x="3" y="3" width="18" height="18" rx="3" /><line x1="9" y1="9" x2="15" y2="15" /><line x1="15" y1="9" x2="9" y2="15" />
    </template>
    <template v-else-if="name === 'dashboard'">
      <circle cx="12" cy="12" r="4" /><circle cx="18" cy="6" r="2" /><circle cx="6" cy="18" r="2" />
    </template>
    <template v-else-if="name === 'sliders'">
      <line x1="4" y1="21" x2="4" y2="14" /><line x1="4" y1="10" x2="4" y2="3" /><line x1="12" y1="21" x2="12" y2="12" /><line x1="12" y1="8" x2="12" y2="3" /><line x1="20" y1="21" x2="20" y2="16" /><line x1="20" y1="12" x2="20" y2="3" /><circle cx="4" cy="12" r="2" /><circle cx="12" cy="10" r="2" /><circle cx="20" cy="14" r="2" />
    </template>
    <template v-else-if="name === 'folder'">
      <path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z" />
    </template>
    <template v-else-if="name === 'clipboard'">
      <path d="M16 4h2a2 2 0 012 2v14a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2h2" /><rect x="8" y="2" width="8" height="4" rx="1" /><line x1="9" y1="12" x2="15" y2="12" /><line x1="9" y1="16" x2="15" y2="16" />
    </template>
    <template v-else-if="name === 'play'">
      <circle cx="12" cy="12" r="10" /><polygon points="10 8 16 12 10 16 10 8" />
    </template>
    <template v-else-if="name === 'energy-flow'">
      <path d="M5 12h14M12 5l7 7-7 7" />
    </template>
    <template v-else-if="name === 'power-outage'">
      <path d="M2 15c4-6 16-6 20 0" /><path d="M2 9c4-4 16-4 20 0" /><line x1="12" y1="15" x2="12" y2="21" />
    </template>
    <template v-else-if="name === 'insight'">
      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" /><circle cx="12" cy="12" r="3" />
    </template>
  </svg>
</template>

<script setup>
defineProps({
  name: {
    type: String,
    required: true,
  },
  size: {
    type: [Number, String],
    default: 18,
  },
  color: {
    type: String,
    default: '',
  },
  spin: {
    type: Boolean,
    default: false,
  },
  strokeWidth: {
    type: [Number, String],
    default: 1.6,
  },
})
</script>

<style scoped>
.app-icon {
  flex-shrink: 0;
  transition: stroke 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.app-icon-spin {
  animation: app-icon-rotate 1.2s linear infinite;
}

@keyframes app-icon-rotate {
  to {
    transform: rotate(360deg);
  }
}
</style>
