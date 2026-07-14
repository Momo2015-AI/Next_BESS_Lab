import { config } from '@vue/test-utils'

// Mock vue-i18n globally
config.global.mocks = {
  $t: (key) => key
}

// Stub localStorage
const store = {}
global.localStorage = {
  getItem: (key) => store[key] || null,
  setItem: (key, value) => {
    store[key] = value
  },
  removeItem: (key) => {
    delete store[key]
  },
  clear: () => {
    Object.keys(store).forEach((k) => delete store[k])
  }
}
