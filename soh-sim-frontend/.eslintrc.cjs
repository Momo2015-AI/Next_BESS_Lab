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
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  rules: {
    // 禁止硬编码文本
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',

    // Vue 规则
    'vue/multi-word-component-names': 'off',
    'vue/no-unused-vars': 'warn',
    'vue/block-order': ['error', {
      'order': ['template', 'script', 'style'],
    }],

    // 字符串引号
    'quotes': ['error', 'single'],

    // 分号
    'semi': ['error', 'never'],

    // 缩进
    'indent': ['error', 2],

    // 最大行数
    'max-lines': ['warn', { max: 400 }],
  },
}
