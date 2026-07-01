# 代码规范检查清单

将此文件添加到 IDE 的 TODO 列表或项目看板，每次开发前对照检查。

## 提交前检查

### 前端
- [ ] 运行 `npm run lint` 无错误
- [ ] 运行 `npm run format -- --check` 通过
- [ ] 所有文本使用 `$t()` 国际化
- [ ] 无内联事件处理器 (onfocus/onblur/onmouseover/onmouseout)
- [ ] 无内联 style 属性
- [ ] 组件不超过 400 行
- [ ] ECharts 实例在 onUnmounted 中 dispose
- [ ] resize 监听器在 onUnmounted 中移除
- [ ] deep watch 有防抖

### 后端
- [ ] 运行 `black --check .` 通过
- [ ] 运行 `isort --check-only .` 通过
- [ ] 运行 `flake8` 无错误
- [ ] 所有外键列有索引
- [ ] 无 N+1 查询
- [ ] 列表查询有分页
- [ ] 批量删除+插入使用事务

## 常见错误速查

| 错误 | 正确做法 |
|------|---------|
| `onfocus="this.style.border='1px solid blue'"` | `.input:focus { border-color: blue; }` |
| `style="color: red"` | `.error { color: red; }` |
| `import * as echarts` | `import * as echarts from 'echarts/core'` |
| `watch(data, handler, { deep: true })` | `watch(data, debounce(handler, 300))` |
| `window.addEventListener('resize', fn)` | `onMounted(()=>add) + onUnmounted(()=>remove)` |
| `User.query.get(user_id)` 在路由中 | 从 `token_required` 装饰器传入的 user 对象使用 |
