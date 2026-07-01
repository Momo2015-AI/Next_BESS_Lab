# 代码规范

本文档定义 soh-sim 项目的代码规范，所有开发者（人类和 AI）必须遵守。

---

## 前端规范 (Vue 3 + Vite)

### 命名约定

| 类型 | 规则 | 示例 |
|------|------|------|
| 组件文件 | PascalCase + .vue | `BatteryDCDesign.vue`, `FinancialDashboard.vue` |
| 组合式函数 | camelCase + use 前缀 | `useDraft.js`, `useAuxPower.js` |
| Store 模块 | camelCase + .js | `bess.js` |
| 路由名称 | kebab-case | `tool-auxpower`, `tool-financial` |
| CSS 类名 | kebab-case | `tool-page`, `step-content` |
| 常量 | UPPER_SNAKE_CASE | `ABBR_MAP`, `FACTOR_DEFAULTS` |
| 私有变量 | _ 前缀 | `_in_memory_factors` |
| 模板 ref | $ 后缀（可选） | `chartContainer` |

### 组件规范

- 单组件不超过 400 行，超过必须拆分为子组件
- 禁止使用内联事件处理器（`onfocus`/`onblur`/`onmouseover`/`onmouseout`）
- 禁止使用内联 `style` 属性，统一使用 CSS 类或 CSS 变量
- 所有文本必须使用 `$t('key')` 国际化，禁止硬编码中英文
- ECharts 实例必须通过 `useChart()` composable 管理，在 `onUnmounted` 中 dispose
- `watch({ deep: true })` 必须配合防抖（debounce 300-500ms）

### 共享样式

- 公共样式提取到 `src/assets/styles/shared.css`
- 页面布局类：`.tool-page`, `.phase-page`, `.tool-header`
- 输入框焦点样式使用 CSS `:focus-visible` 伪类 + `transition`
- 按钮 hover 效果使用 CSS `:hover` 伪类

### 图表管理

```javascript
// 正确：使用 composable 管理图表
import { useChart } from '@/composables/useChart'

const { chart, containerRef, dispose } = useChart()
// chart 实例在 onMounted 自动创建，onUnmounted 自动 dispose
```

### 性能要求

- 所有输入框变更触发计算必须防抖 300ms+
- localStorage 写入必须防抖 500ms+
- 多个图表同时渲染时，使用 `requestAnimationFrame` 或 `setTimeout` 错开渲染
- 路由组件必须使用动态导入（`() => import()`）

---

## 后端规范 (Python + Flask + SQLAlchemy)

### 命名约定

| 类型 | 规则 | 示例 |
|------|------|------|
| 模块/文件 | snake_case | `efficiency.py`, `cache_manager.py` |
| 类名 | PascalCase | `BatteryManufacturer`, `LRUCache` |
| 函数/方法 | snake_case | `calculate_efficiency_chain()` |
| 常量 | UPPER_SNAKE_CASE | `FACTOR_DEFAULTS`, `MANUFACTURERS_DB` |
| 私有变量 | _ 前缀 | `_token_blacklist` |

### 数据库规范

- 所有外键列必须添加索引
- 禁止 N+1 查询，使用 `joinedload` 或 `selectinload`
- 列表查询必须分页（每页 20-50 条）
- 批量删除+插入必须使用事务包裹
- 模型 `to_dict()` 方法必须在类中显式定义，禁止运行时动态注入

### API 规范

- 统一响应格式：`{ "success": true/false, "data": ..., "error": ... }`
- 所有认证端点使用 `token_required` 装饰器，避免重复查询 User
- 计算密集型端点考虑异步处理（Celery/RQ）
- 静态数据（如厂家列表）必须缓存

### 性能要求

- 内存缓存至少 200 条，生产环境使用 Redis
- LRU 淘汰算法使用 `OrderedDict`，O(1) 复杂度
- 缓存键使用序列化稳定的格式（如 `json.dumps(sort_keys=True)`）

---

## 国际化 (i18n) 规范

### 强制要求

- 所有面向用户的文本必须使用 `$t('key')`
- 禁止在模板中硬编码中文或英文
- 翻译文件按模块组织，key 使用点号分隔

### 翻译文件结构

```javascript
// src/i18n/zh.js
export default {
  sidebar: {
    home: '首页',
    toolAuxPower: '辅助功耗计算',
  },
  phase2: {
    step6: '效率链配置',
  },
}
```

```javascript
// src/i18n/en.js
export default {
  sidebar: {
    home: 'Home',
    toolAuxPower: 'Auxiliary Power Calculator',
  },
  phase2: {
    step6: 'Efficiency Chain',
  },
}
```

### 使用方式

```vue
<!-- 模板中使用 -->
<h3>{{ $t('phase2.step6') }}</h3>

<!-- 脚本中使用 -->
const { t } = useI18n()
console.log(t('sidebar.toolAuxPower'))
```

---

## 禁止事项

### 前端

1. 禁止使用内联事件处理器（`onfocus`/`onblur`/`onmouseover`/`onmouseout`）
2. 禁止硬编码中文/英文文本
3. 禁止在 `.vue` 文件中定义重复的 CSS 类（提取到 shared.css）
4. 禁止组件超过 400 行
5. 禁止 ECharts 实例在 `onUnmounted` 中未 dispose
6. 禁止 `window.addEventListener('resize')` 未在 `onUnmounted` 中 remove
7. 禁止 `setInterval` 未在 `onUnmounted` 中 clearInterval
8. 禁止 `MutationObserver` 未在 `onUnmounted` 中 disconnect
9. 禁止 `watch({ deep: true })` 无防抖触发重计算
10. 禁止 `import * as echarts` 全量导入，使用按需导入

### 后端

1. 禁止 N+1 查询
2. 禁止无索引的外键列查询
3. 禁止无分页的列表查询
4. 禁止无事务保护的批量删除+插入
5. 禁止运行时动态注入模型方法
6. 禁止生产环境使用 Flask 单线程服务器

---

## Git 提交规范

```
<type>(<scope>): <subject>

type: feat|fix|chore|refactor|docs|style|test|perf
scope: frontend|backend|docs|config
subject: 使用中文简短描述
```

示例：
```
feat(frontend): 添加效率链独立页面
fix(backend): 修复产品层级查询 N+1 问题
chore(frontend): 统一 i18n 翻译文件
```

---

## 代码审查清单

提交 PR 前自查：

- [ ] 所有文本使用 `$t()` 国际化
- [ ] 无内联事件处理器和内联样式
- [ ] 组件不超过 400 行
- [ ] 无内存泄漏（resize/MutationObserver/setInterval 已清理）
- [ ] 所有 deep watch 有防抖
- [ ] 后端查询有索引，无 N+1
- [ ] 列表查询有分页
- [ ] 运行 `npm run lint` 无错误
- [ ] 运行 `black .` 和 `isort .`（后端）
