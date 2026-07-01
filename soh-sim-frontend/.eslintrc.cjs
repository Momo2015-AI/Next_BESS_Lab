module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-recommended',
    'plugin:i18n-json/recommended',
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  plugins: ['vue', 'i18n'],
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',

    'vue/multi-word-component-names': 'off',
    'vue/no-unused-vars': 'warn',
    'vue/block-order': ['error', {
      'order': ['template', 'script', 'style'],
    }],

    'quotes': ['error', 'single'],
    'semi': ['error', 'never'],
    'indent': ['error', 2],
    'max-lines': ['warn', { max: 400 }],

    'vue/no-v-html': 'warn',

    'i18n-json/keys-sorted': 'off',
    'i18n-json/no-duplicate-keys': 'error',
    'i18n-json/sorted-keys': 'off',
  },
  overrides: [
    {
      files: ['src/i18n/*.js'],
      rules: {
        'i18n-json/valid-json': 'error',
      },
    },
  ],
}