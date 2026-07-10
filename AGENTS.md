# 项目代码规范

所有开发者（人类和 AI）必须遵守以下规范。

## 快速检查清单

修改代码前自查：

- [ ] 所有文本使用 $t() 国际化，无硬编码
- [ ] 无内联事件处理器 (onfocus/onblur/onmouseover/onmouseout)
- [ ] 无内联 style 属性，使用 CSS 类
- [ ] 组件不超过 400 行
- [ ] ECharts 实例在 onUnmounted 中 dispose
- [ ] resize 监听器在 onUnmounted 中移除
- [ ] deep watch 有防抖
- [ ] 后端查询有索引，无 N+1
- [ ] 列表查询有分页

## 完整规范

详见 [CODE_STYLE.md](./CODE_STYLE.md)

## AI 工具规则

本项目使用 `.cursorrules` 作为 AI 编码规则的唯一权威来源。规则通过 `scripts/sync-ai-rules.js` 自动同步。

---

## Frontend (Vue 3 + Vite + Tailwind CSS 4)

### Naming
- Components: PascalCase (.vue)
- Composables: camelCase + use prefix (useDraft.js)
- Store: camelCase (bess.js)
- CSS classes: kebab-case (tool-page, step-content)
- Constants: UPPER_SNAKE_CASE

### Mandatory Rules
1. All text must use $t('key') for i18n. NO hardcoded Chinese or English.
2. NO inline event handlers (onfocus/onblur/onmouseover/onmouseout). Use CSS :focus-visible or @focus/@blur.
3. NO inline style attributes. Use CSS classes.
4. Single component max 400 lines. Split if larger.
5. ECharts instances must be disposed in onUnmounted.
6. window.addEventListener('resize') must have matching removeEventListener in onUnmounted.
7. setInterval must be cleared in onUnmounted.
8. MutationObserver must be disconnected in onUnmounted.
9. watch({ deep: true }) must be debounced (300-500ms).
10. Use tree-shakable echarts imports from 'echarts/core', NOT 'import * as echarts from echarts'.

### Shared Styles
- Extract common styles to src/assets/styles/shared.css
- Page layout classes: .tool-page, .phase-page, .tool-header

### Performance
- Input changes triggering calculations must debounce 300ms+
- localStorage writes must debounce 500ms+

## Backend (Python + Flask)

### Naming
- Modules: snake_case
- Classes: PascalCase
- Functions: snake_case
- Constants: UPPER_SNAKE_CASE

### Mandatory Rules
1. All foreign key columns must have indexes.
2. NO N+1 queries. Use joinedload/selectinload.
3. List queries must be paginated.
4. Bulk delete+insert must be wrapped in transactions.
5. Model to_dict() methods must be explicitly defined. NO runtime dynamic injection.
6. Auth endpoints must NOT re-query User.

## Reference
- Full spec: CODE_STYLE.md
- Translations: src/i18n/zh.js and src/i18n/en.js
