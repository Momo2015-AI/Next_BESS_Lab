# 代码质量审查报告

审查日期: 2026-07-01
审查范围: soh-sim-frontend, soh-sim-backend
审查人: Agnes-2.0-Flash (AI Agent)

---

## 一、中英文变量名混用

### 严重程度：高

### 问题表现

1. **模板标签中英混用**
   - `src/components/ProductConfig.vue:9` `电芯选型库 Battery Cell Library`
   - `src/components/HomePage.vue:66` footer 硬编码英文 `SOH-SIM Platform · BESS Design & Evaluation`

2. **数据属性全英文，UI 全中文**
   - `BatteryDCDesign.vue`: `batteryConfig.cellCapacity` 对应模板 `额定容量 (Ah)`
   - `EngineeringCalc.vue`: `siteData.containerQty` 对应模板 `集装箱数量`
   - 这种分离增加理解成本

3. **i18n 覆盖不全**
   - 约 25+ 个组件未使用 `$t()`，硬编码中文
   - 受影响组件：`EngineeringCalc.vue`、`BatteryDCDesign.vue`、`SimulationLab.vue`、`Sidebar.vue`（部分）、`Phase1-5Page.vue`（全部）、`SurveyPage.vue`、`AuthPage.vue`、`EpcPage.vue`、`ToolSurveyViewPage.vue` 等
   - 仅 `DataInjection.vue`、`FormulaLab.vue`、`RunningConditions.vue` 等少数组件完全使用 i18n

4. **旧版组件共存**
   - `ModernSidebar.vue`：emoji 图标 + 硬编码中文菜单（`仪表盘`、`仿真实验室`）
   - `Sidebar.vue`：SVG 图标 + `$t()` 国际化
   - 两套侧边栏共存，维护混乱

### 解决方案

1. **统一使用 i18n**：所有硬编码中文替换为 `$t('key')`，补充 `zh.js`/`en.js` 翻译
2. **变量名保持英文**：数据属性、函数名、组件名统一 camelCase/PascalCase
3. **删除 ModernSidebar.vue**：旧版组件不再使用
4. **建立命名规范文档**：制定 `NAMING.md` 明确各类命名规则

---

## 二、缺乏统一代码规范

### 严重程度：中高

### 问题表现

1. **内联样式泛滥**
   - `EngineeringCalc.vue` 中 30+ 处 `onfocus`/`onblur` 内联 JS
   - `SimulationLab.vue` 1200+ 行，大量内联 `style` 属性
   - 样式无法复用，主题切换困难

2. **内联事件处理器**
   - 所有 input 元素重复 `onfocus="this.style.borderColor='...'"` 模式
   - 违反 Vue 最佳实践，无法被响应式系统追踪

3. **组件大小超标**
   - `SimulationLab.vue`: 1361 行
   - `EpcPage.vue`: 1045+ 行
   - `EngineeringCalc.vue`: 611 行
   - `ProductConfig.vue`: 663 行
   - `RunningConditions.vue`: 901+ 行
   - 建议单组件不超过 300-400 行

4. **CSS 变量命名虽一致但分散**
   - 变量命名风格 `--color-{category}-{variant}` 基本统一
   - 但多个组件重复定义相同的 `.tool-page`、`.phase-page` 样式

### 解决方案

1. **移除内联事件处理器**：改用 CSS `:focus-visible` 伪类 + 过渡动画
2. **提取共享样式**：将公共样式提取到 `assets/styles/shared.css`
3. **拆分大型组件**：按功能步骤拆分为子组件
4. **使用 ESLint + Prettier**：统一代码风格

---

## 三、代码重复性较高

### 严重程度：高

### 问题表现

1. **页面模板重复**
   - 15+ 个 ToolPage/PhasePage 共享相同的结构（header + content + style）
   - 每个文件都重复：
     ```css
     .tool-page { padding: 24px; }
     .tool-header { margin-bottom: 24px; }
     .tool-header h1 { font-size: 24px; font-weight: 700; margin: 0 0 8px; }
     ```

2. **ECharts 配置重复**
   - 6 个组件各自管理 chart 实例、resize、dispose
   - 模式完全一致：`echarts.init()` → `setOption()` → `window.addEventListener('resize')` → `dispose()`

3. **输入框样式重复**
   - 每个 input 都重复 `onfocus`/`onblur`/`onmouseover`/`onmouseout` 内联样式
   - `EngineeringCalc.vue` 出现 30+ 次

4. **计算逻辑重复**
   - `FinancialDashboard.vue` 的 `computeAll()` 和后端 `services/pipeline.py` 都有金融计算逻辑
   - `calculate_efficiency_chain()` 在前端 EfficiencyChain.vue 和后端 services/efficiency.py 都有实现

### 解决方案

1. **创建 `useChart()` composable**：统一管理 ECharts 实例生命周期
2. **提取页面布局组件**：`<ToolLayout title="..." desc="...">` 统一页面结构
3. **创建共享输入组件**：`<NumberInput v-model="..." label="..." />` 替代内联样式
4. **统一计算逻辑**：前端通过 API 调用后端计算，或共享同一套计算函数

---

## 四、前端性能问题

### 严重程度：高

### 问题清单

| # | 问题 | 文件 | 行号 | 严重程度 |
|---|------|------|------|---------|
| 1 | computeAll 无防抖触发 | FinancialDashboard.vue | 780-781 | 严重 |
| 2 | resize 监听器泄漏 | FinancialDashboard.vue | 794 | 中等 |
| 3 | MutationObserver 未清理 | CostWaterfallChart.vue | 305-316 | 中等 |
| 4 | setInterval 未清理 | useExchangeRate.js | 193-195 | 中等 |
| 5 | echarts 全量导入 | 6 个文件 | - | 低 |
| 6 | 内联事件处理器 | 所有主要组件 | - | 低 |
| 7 | EnergyFlowSankey 输入无防抖 | EnergyFlowSankey.vue | 274 | 低 |
| 8 | useDraft 序列化开销 | useDraft.js | 142-163 | 低 |
| 9 | 图表渲染队列堆积 | FinancialDashboard.vue | 442-444 | 低 |
| 10 | deep watch props.params | FinancialDashboard.vue | 780 | 低 |

### 详细分析

**A1. FinancialDashboard.vue - 4个 ECharts 实例 + 子组件图表**
- 同时渲染 6 个 ECharts 实例
- 每个 `tooltip.formatter` 回调中包含字符串拼接和 HTML 构建
- `renderCharts()` 在 `computeAll()` 内部通过 `setTimeout(..., 300)` 延迟执行

**B1. FinancialDashboard.vue:780 - 全局 deep watch 触发全量重算**
```js
watch([() => props.params, () => props.soh, () => props.augQty], ..., { deep: true })
watch(f, ..., { deep: true })  // f 包含 20+ 个字段
```
- 用户调整任何一个输入框（如 `offPeakPrice` 从 200 改为 201），就触发完整的金融计算 + 6 个图表重绘

**B2. useDraft.js:142 - 全局 deep watch 触发 localStorage 序列化**
```js
watch(state, ..., { deep: true })  // 每次属性变化都 JSON.stringify + localStorage.setItem
```

**D1. resize 事件监听器泄漏**
- `FinancialDashboard.vue:794`、`CostWaterfallChart.vue:338`、`EnergyFlowSankey.vue:288`
- `window.addEventListener('resize', ...)` 但 `onUnmounted` 中没有对应的 `removeEventListener`
- 组件卸载后 resize 回调仍然持有 ECharts 实例的闭包引用，导致实例无法被 GC 回收

**D2. MutationObserver 未清理**
- `CostWaterfallChart.vue:305-316`、`EnergyFlowSankey.vue:250-261`
- `watchTheme()` 创建 `MutationObserver` 但返回的 observer 实例没有在 `onUnmounted` 中调用 `disconnect()`
- 每次主题切换都会创建新的 observer 但不销毁旧的，造成 observer 累积

**D3. setInterval 未清理**
- `useExchangeRate.js:193-195`
- `setInterval` 在 `onMounted` 中创建，但没有对应的 `clearInterval` 清理
- 组件卸载后定时器仍在运行并持续发起 API 请求

### 优化建议

**P0（立即修复）**：
```js
// FinancialDashboard.vue - 添加防抖
import { debounce } from 'lodash-es'
const debouncedCompute = debounce(() => computeAll(), 300)
watch(f, debouncedCompute, { deep: true })

// 修复 resize 泄漏
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
```

**P1（近期优化）**：
```js
// useChart.js - 统一图表管理
export function useChart(containerRef) {
  const chart = ref(null)
  onMounted(() => { chart.value = echarts.init(containerRef.value) })
  onUnmounted(() => { chart.value?.dispose() })
  return chart
}
```

---

## 五、后端性能问题

### 问题清单

| # | 文件 | 问题 | 严重程度 |
|---|------|------|---------|
| HIGH-1 | database.py:24 | 无数据库索引 | 严重 |
| HIGH-2 | routes/products.py:703 | N+1 层级查询（7-8 次独立查询） | 严重 |
| HIGH-3 | 多处 auth 路由 | 重复 User.query.get()（token_required 已获取过） | 中等 |
| HIGH-4 | routes/project.py:143 | 无分页的大列表查询 | 中等 |
| HIGH-5 | routes/boq.py:48 | DELETE 操作无事务保护（先删后增） | 中等 |
| MEDIUM-1 | cache_manager.py:62 | 内存缓存容量过小（50 条）且无持久化 | 中等 |
| MEDIUM-2 | cache_manager.py:42 | LRU 淘汰算法 O(N) 复杂度 | 低 |
| MEDIUM-3 | cache_manager.py:73 | 缓存键生成方式脆弱（str() 不稳定） | 低 |
| MEDIUM-4 | services/pipeline.py:93 | O(N^2) 能量核算循环 | 低 |
| MEDIUM-7 | routes/auth.py:17 | Token 黑名单使用内存集合，无持久化 | 中等 |
| LOW-1 | app.py:78 | 单线程开发服务器 | 高（生产环境） |

### 详细分析

**[HIGH-1] database.py:24 - 无数据库索引**
- 20+ 个数据库模型，但没有任何显式索引配置
- Flask-SQLAlchemy 默认只为 primary key 创建索引
- 外键列（`project_id`、`tenant_id`、`user_id`）频繁用于查询过滤，但没有索引，导致全表扫描

**[HIGH-2] routes/products.py:703-773 - 严重的 N+1 查询**
- `get_hierarchy` 端点在同一个请求中执行 7-8 次独立数据库查询
- 每次查询通过 `_apply_tenant_filter` 包装
- 嵌套层级查询：cell -> pack -> rack -> cluster -> container
- 建议改为单次 JOIN 查询或使用 `joinedload`

**[HIGH-3] 每个认证端点重复查询 User**
- `routes/simulation.py:24`、`routes/project.py:24`、`routes/auth.py:96`
- 几乎所有需要认证的端点都在函数体内执行 `User.query.get(user_id)`
- `token_required` 装饰器已经获取了 user 对象，但每个路由又重复查询了一次
- 每个请求至少多一次数据库查询

**[MEDIUM-1] cache_manager.py:62 - 内存缓存问题**
- `LRUCache(capacity=50, ttl=7200)` 仅缓存 50 条记录
- 纯内存存储，应用重启后丢失
- 对于计算密集型 API（如 degradation prediction），50 条缓存远远不够

**[MEDIUM-4] services/pipeline.py:93-110 - O(N^2) 复杂度**
- `calculate_energy_accounting` 中嵌套循环
- 外层遍历 N 年，内层遍历 k 从 0 到 i
- 扩容数量的累积计算是 O(N^2)
- 虽然 N=26 很小，但如果未来扩展会成为瓶颈

### 优化建议

**数据库索引**：
```python
# database.py - 为常用查询列添加索引
class Project(db.Model):
    __table_args__ = (
        db.Index('ix_project_tenant_id', 'tenant_id'),
        db.Index('ix_project_status', 'status'),
    )
```

**消除 N+1**：
```python
# routes/products.py
from sqlalchemy.orm import joinedload
products = Product.query.options(
    joinedload(Product.cells),
    joinedload(Product.containers)
).all()
```

**引入 Redis 缓存**：
```python
from flask_caching import Cache
cache = Cache(config={'CACHE_TYPE': 'RedisCache'})
cache.init_app(app)
```

**添加分页**：
```python
# routes/project.py
versions = Version.query.filter_by(project_id=pid) \
    .order_by(Version.created_at.desc()) \
    .paginate(page=page, per_page=20)
```

---

## 六、数据库性能问题

### 问题清单

| # | 文件 | 问题 | 严重程度 |
|---|------|------|---------|
| DB-1 | database.py | SQLite 单写锁，并发写入阻塞 | 高 |
| DB-2 | database.py:43-49 | to_dict 动态方法注入，影响查找性能 | 中 |
| DB-3 | routes/boq.py:48 | 先删后增无事务保护，高并发数据不一致 | 中 |
| DB-4 | database.py:52-914 | 模型定义过于集中（935 行，20+ 个模型） | 低 |

### 详细分析

**[DB-1] SQLite 单写锁**
- 当前使用 SQLite，不适合生产环境
- 并发写入时只有一个写者，其他写者阻塞
- 无 WAL 模式配置，高并发下性能急剧下降

**[DB-2] to_dict 动态注入**
- `database.py:43-49` 通过循环为每个模型动态注入 `to_dict` 方法
- 运行时修改类属性，影响方法查找性能
- 不利于 IDE 静态分析和代码导航

**[DB-3] BOQ 先删后增无事务**
- `routes/boq.py:48` 使用 `BoqItem.query.filter_by(...).delete()`
- 先删除所有旧条目再插入新条目，没有事务保护
- 高并发下会导致数据不一致

### 解决方案

1. **迁移到 PostgreSQL**：解决并发写入瓶颈，获得更好的索引支持
2. **移除动态 to_dict**：每个模型显式定义 `to_dict()` 方法
3. **BOQ 保存使用事务**：
   ```python
   with db.session.begin():
       BoqItem.query.filter_by(version_id=vid).delete()
       for item in new_items:
           db.session.add(item)
   ```
4. **拆分模型文件**：按模块拆分到 `models/project.py`、`models/simulation.py` 等

---

## 七、严重程度汇总

| 类别 | 严重程度 | 影响范围 | 修复难度 |
|------|---------|---------|---------|
| 前端性能（无防抖+内存泄漏） | 严重 | FinancialDashboard 交互卡顿 | 低 |
| 数据库索引缺失 | 严重 | 所有列表查询变慢 | 低 |
| 中英文混用+i18n覆盖不全 | 高 | 所有组件，影响可维护性 | 中 |
| 代码重复（页面结构+ECharts） | 高 | 15+ 页面，6 个图表组件 | 中 |
| N+1 查询 | 高 | 产品层级 API | 中 |
| 组件过大（>600 行） | 中 | 6 个组件 | 高 |
| 内联样式/事件处理器 | 中 | 所有主要组件 | 中 |
| SQLite 并发限制 | 中 | 生产环境部署 | 高 |

---

## 八、修复优先级

| 优先级 | 问题 | 预计工作量 | 收益 |
|--------|------|-----------|------|
| P0 | 前端防抖 + 内存泄漏修复 | 1-2 天 | 立竿见影的交互流畅度提升 |
| P0 | 数据库索引添加 | 半天 | 查询速度 5-10 倍提升 |
| P1 | i18n 全覆盖 + 命名规范统一 | 3-5 天 | 可维护性大幅提升 |
| P1 | ECharts composable 提取 | 1-2 天 | 代码重复减少 60% |
| P1 | 大型组件拆分 | 5-7 天 | 可读性和可测试性提升 |
| P2 | PostgreSQL 迁移 + Redis 缓存 | 3-5 天 | 并发能力和缓存命中率提升 |
| P2 | ESLint + Prettier 配置 | 半天 | 代码风格统一 |

---

## 附录：受影响的组件清单

### 未使用 i18n 的组件（硬编码中文）
- `EngineeringCalc.vue`
- `BatteryDCDesign.vue`
- `SimulationLab.vue`
- `Sidebar.vue` (部分)
- `Phase1Page.vue` - `Phase5Page.vue`
- `SurveyPage.vue`
- `AuthPage.vue`
- `EpcPage.vue`
- `ToolSurveyViewPage.vue`
- `ToolProjectsPage.vue`
- `ToolReportPage.vue`

### 大型组件（>400 行）
- `SimulationLab.vue`: 1361 行
- `EpcPage.vue`: 1045+ 行
- `RunningConditions.vue`: 901+ 行
- `ProductConfig.vue`: 663 行
- `EngineeringCalc.vue`: 611 行
- `SurveyPage.vue`: 486 行

### 内存泄漏风险点
- `FinancialDashboard.vue:794` - resize 监听器未清理
- `CostWaterfallChart.vue:338` - resize 监听器未清理
- `EnergyFlowSankey.vue:288` - resize 监听器未清理
- `CostWaterfallChart.vue:305-316` - MutationObserver 未清理
- `EnergyFlowSankey.vue:250-261` - MutationObserver 未清理
- `useExchangeRate.js:193-195` - setInterval 未清理
