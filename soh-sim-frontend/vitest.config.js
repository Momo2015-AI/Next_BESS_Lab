import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  test: {
    environment: 'jsdom',
    globals: true,
    include: ['src/**/*.{spec,test}.{js,ts}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov'],
      include: ['src/composables/**', 'src/services/**', 'src/components/**', 'src/pages/**'],
    },
  },
  resolve: {
    alias: {
      '@': '/src',
    },
  },
})
