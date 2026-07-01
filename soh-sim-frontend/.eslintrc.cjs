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
    'eslint-config-prettier',
  ],
  plugins: ['prettier'],
  rules: {
    'prettier/prettier': 'error',
    // 通用规则
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'quotes': ['error', 'single'],
    'semi': ['error', 'never'],
    'no-var': 'error',
    'prefer-const': 'error',
    'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],

    // Vue 规则
    'vue/multi-word-component-names': 'off',
    'vue/no-unused-vars': 'warn',
    'vue/block-order': ['error', {
      order: ['template', 'script', 'style'],
    }],
    'vue/component-name-in-template-casing': ['error', 'PascalCase'],

    // 禁止内联事件处理器（自定义规则思路：检查模板中的 onfocus 等）
    // NOTE: ESLint 原生不支持提取模板中的属性，需要 vue-eslint-parser + 自定义规则
    // 当前通过 CI check-code-style.sh 脚本检测

    // 组件大小
    'max-lines': ['warn', { max: 400, skipBlankLines: true, skipComments: true }],

    // 禁止使用 any（TypeScript 规则，js 文件忽略）
    // '@typescript-eslint/no-explicit-any': 'error',
  },
  overrides: [
    {
      files: ['*.ts', '*.tsx', '*.vue'],
      parser: 'vue-eslint-parser',
      parserOptions: {
        parser: '@typescript-eslint/parser',
        ecmaVersion: 'latest',
        sourceType: 'module',
      },
      extends: [
        'plugin:@typescript-eslint/recommended',
      ],
      rules: {
        '@typescript-eslint/no-explicit-any': 'error',
        '@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
        '@typescript-eslint/explicit-function-return-type': 'off',
        '@typescript-eslint/no-non-null-assertion': 'warn',
      },
    },
    {
      files: ['*.jsx', '*.js'],
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },
    },
  ],
}
