# 代码规范手册

**版本**: v1.3
**最后更新**: 2026-07-17
**状态**: 当前实际执行标准（标注 [计划] 的为未来引入）

本文档使用 RFC 2119 关键词：
- **MUST**: 强制执行，违反不得合并
- **SHOULD**: 强烈建议，特殊情况可豁免但需注释说明
- **MAY**: 可选，由开发者自行决定
- **[计划]**: 未来版本引入，当前不强制

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.2 | 2026-07-10 | 清理过时引用、区分当前/计划状态、添加豁免清单、合并冗余文档 |
| v1.3 | 2026-07-17 | 组件行数改为软限制+评审判断（§1.2）、重基线豁免清单（§9）、新增前端可读性检查卡（§10） |
| v1.1 | 2026-07-01 | 添加 TypeScript、API设计、数据库设计、安全、测试、团队协作 |
| v1.0 | 2026-06-20 | 初始版本，前后端基础规范 |

---

## 一、前端规范 (Vue 3 + Vite + Tailwind CSS 4)

### 1.1 命名约定

| 类型 | 规则 | 示例 |
|------|------|------|
| 组件文件 | PascalCase + .vue | `BatteryDCDesign.vue` |
| 组合式函数 | camelCase + `use` 前缀 | `useDraft.js` |
| Store 模块 | camelCase | `bess.js` |
| 路由名称 | kebab-case | `tool-auxpower` |
| CSS 类名 | kebab-case | `tool-page` |
| 常量 | UPPER_SNAKE_CASE | `ABBR_MAP` |
| 私有变量 | `_` 前缀 | `_in_memory_factors` |
| Props | camelCase | `ratedEnergy` |
| Emits | camelCase | `updateConfig` |

### 1.2 组件规范

- 组件行数采用**软限制 + 评审判断**，而非硬性报错（与 ESLint `vue/max-lines-per-file` 的 Warning 一致）：
  - **< 400 行**：无需关注。
  - **400–800 行**：Warning 提醒。评审依据[前端代码审查可读性检查卡](#前端代码审查可读性检查卡)判断是否需拆分，不强制。
  - **> 800 行**：仍仅 Warning，但 PR 必须关联技术债工单，并经资深开发签字确认「暂不可拆 / 已排期拆分」方可合并。
- SHOULD 优先使用 Composition API 将逻辑抽离到 `use*` composable 以降低行数、提升可维护性；模板过大时进一步拆分为带 `props`/`emits` 的展示型子组件（注意避免「composable 汤」——只抽内聚单元，相关 state 与 behavior 留在同一 composable）。
- 评审关注**可读性**而非行数：一个 600 行但逻辑清晰、内聚、不可拆的组件，依然是好代码。
- MUST 禁止内联事件处理器（`onfocus`/`onblur`/`onmouseover`/`onmouseout`）
- MUST 禁止内联 `style` 属性，使用 CSS 类
- MUST 所有文本使用 `$t('key')` 国际化，禁止硬编码中英文
- MUST ECharts 实例在 `onUnmounted` 中 dispose
- MUST `window.addEventListener('resize')` 在 `onUnmounted` 中 removeEventListener
- MUST `setInterval` 在 `onUnmounted` 中 clearInterval
- MUST `MutationObserver` 在 `onUnmounted` 中 disconnect
- MUST `watch({ deep: true })` 配合防抖（300-500ms）
- MUST ECharts 使用按需引入，禁止 `import * as echarts`
- SHOULD 使用 `<script setup>` 语法
- SHOULD Props 声明类型和默认值

### 1.3 模板规范

**正确示例：**

```vue
<template>
  <div class="tool-page">
    <h2>{{ $t('sidebar.toolAuxPower') }}</h2>
    <input
      v-model="inputValue"
      @input="debouncedCalculate"
      class="input-field"
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { debounce } from 'lodash-es'

const inputValue = ref('')
const debouncedCalculate = debounce(() => {
  // 计算逻辑
}, 300)

watch(inputValue, debouncedCalculate)
</script>

<style scoped>
.input-field {
  background-color: var(--color-input-bg-dark);
  border: 1px solid var(--color-input-border);
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 12px;
  transition: border-color 0.2s;
}

.input-field:focus-visible {
  border-color: var(--color-accent);
  outline: none;
}
</style>
```

**错误示例：**

```vue
<template>
  <div>
    <h2>辅助功率计算</h2>           <!-- ❌ 硬编码中文 -->
    <input
      v-model="inputValue"
      @input="calculate"             <!-- ❌ 无防抖 -->
      style="border:1px solid #ccc"  <!-- ❌ 内联样式 -->
      onfocus="this.style.border='blue'"  <!-- ❌ 内联事件 -->
    />
  </div>
</template>
```

### 1.4 TypeScript 规范

#### 命名

| 类型 | 规则 | 示例 |
|------|------|------|
| 接口 | `IPascalCase` | `IBatteryConfig`, `ISimParams` |
| 类型别名 | `PascalCase` | `DegradationType`, `CellData` |
| 泛型 | 单字母 | `T`, `K`, `V` |
| 枚举 | `PascalCase` | `GridStandard`, `BatteryType` |
| .ts 文件 | kebab-case | `battery-types.ts` |

#### 类型定义

- SHOULD 优先使用 `interface` 定义对象类型
- SHOULD 使用 `type` 定义联合类型、交叉类型
- SHOULD 避免使用 `any`，优先使用具体类型或 `unknown`
- MAY 为复杂类型编写 JSDoc 注释

```typescript
// 接口定义对象
interface IBatteryConfig {
  cellModel: string
  capacityAh: number
  voltageNominal: number
}

// 类型别名定义联合类型
type DegradationModel = 'arrhenius' | 'linear_log' | 'double_exponential'
```

### 1.5 共享样式

- MUST 公共样式提取到 `src/assets/styles/shared.css`
- MUST 页面布局使用统一类：`.tool-page`, `.phase-page`, `.tool-header`
- MUST 输入框焦点使用 CSS `:focus-visible` + `transition`
- MUST 按钮 hover 使用 CSS `:hover` 伪类

### 1.6 图表管理

```javascript
// 正确：使用 composable 管理
import { useChart } from '@/composables/useChart'

const { chart, containerRef, dispose } = useChart()

// 正确：按需引入 ECharts
import * as echarts from 'echarts/core'
import { BarChart, LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([BarChart, LineChart, GridComponent, TooltipComponent, CanvasRenderer])
```

### 1.7 性能要求

- MUST 输入框变更触发计算必须防抖 300ms+
- MUST localStorage 写入必须防抖 500ms+
- SHOULD 多图表渲染使用 `requestAnimationFrame` 错开
- MUST 路由组件使用动态导入 `() => import()`

---

## 二、后端规范 (Python + Flask + SQLAlchemy)

### 2.1 命名约定

| 类型 | 规则 | 示例 |
|------|------|------|
| 模块/文件 | snake_case | `efficiency.py` |
| 类名 | PascalCase | `BatteryManufacturer` |
| 函数/方法 | snake_case | `calculate_efficiency_chain()` |
| 常量 | UPPER_SNAKE_CASE | `FACTOR_DEFAULTS` |
| 私有变量 | `_` 前缀 | `_token_blacklist` |
| 模块级私有 | `__` 前缀 | `__all__` |

### 2.2 模块规范

```python
"""模块文档字符串 - 描述模块功能和职责"""

# 标准库导入
import json
from datetime import datetime

# 第三方库导入
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload

# 本地导入
from services.efficiency import calculate_efficiency_chain
```

### 2.3 数据库规范

#### 表结构设计

- MUST 主键使用 Integer 自增 ID 或 UUID String(36)
- MUST 所有外键列添加索引
- MUST 所有表包含 `created_at` 和 `updated_at` 字段
- SHOULD 使用软删除（`is_deleted` 字段），禁止物理删除
- MUST `to_dict()` 方法显式定义，禁止运行时动态注入

```python
class Project(db.Model):
    __tablename__ = 'project'
    __table_args__ = (
        db.Index('ix_project_tenant_id', 'tenant_id'),
        db.Index('ix_project_status', 'status'),
        db.Index('ix_project_updated_at', 'updated_at'),
    )

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='draft')
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'name': self.name,
            'status': self.status,
        }
```

#### 索引策略

- MUST 单列索引：查询频繁的字段（`status`, `tenant_id`）
- SHOULD 复合索引：WHERE 条件中的字段组合
- MUST 唯一索引：业务唯一性约束
- MAY 全文索引：文本搜索字段

#### 查询规范

- MUST 禁止 N+1 查询，使用 `joinedload` 或 `selectinload`
- MUST 列表查询必须分页（每页 20-50 条）
- MUST 批量删除+插入使用事务包裹

```python
# 正确：使用 joinedload 预加载
products = Product.query.options(
    joinedload(Product.cells),
    joinedload(Product.containers)
).all()

# 正确：使用事务
with db.session.begin():
    BoqItem.query.filter_by(version_id=vid).delete()
    for item in new_items:
        db.session.add(item)

# 错误：N+1 查询
for project in projects:
    versions = Version.query.filter_by(project_id=project.id).all()  # ❌
```

### 2.4 API 设计规范

#### URL 设计

- MUST 使用 RESTful 风格
- SHOULD 资源名使用复数形式
- MUST 使用连字符分隔多单词路径

```
GET    /api/projects              # 获取项目列表
GET    /api/projects/:id          # 获取单个项目
POST   /api/projects              # 创建项目
PUT    /api/projects/:id          # 更新项目
DELETE /api/projects/:id          # 删除项目
```

#### 请求规范

- MUST Content-Type 使用 `application/json`
- MUST 请求体字段使用 camelCase
- MUST 查询参数使用 snake_case

#### 响应规范

统一响应格式：

```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "message": "操作成功"
}
```

错误码定义：

| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 客户端请求错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 409 | 资源冲突 |
| 422 | 请求体验证失败 |
| 429 | 请求频率超限 |
| 500 | 服务器内部错误 |

#### 分页规范

请求参数：
- `page`: 页码（从 1 开始）
- `page_size`: 每页数量（默认 20，最大 100）

响应格式：

```json
{
  "success": true,
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

#### 认证规范

- MUST 使用 JWT Bearer Token 认证
- MUST `token_required` 装饰器获取的 User 对象直接传递给路由函数
- MUST 禁止在路由函数中重复查询 User
- [计划] Token 黑名单使用 Redis 存储

### 2.5 性能要求

- MUST 内存缓存至少 200 条
- MUST LRU 淘汰算法使用 `OrderedDict`，O(1) 复杂度
- MUST 缓存键使用序列化稳定的格式
- [计划] 计算密集型端点使用 Celery/RQ 异步处理
- [计划] 生产环境使用 gunicorn/uwsgi，禁止 Flask 单线程服务器
- [计划] 生产环境使用 Redis 替代内存缓存

---

## 三、安全规范

### 3.1 前端安全

- MUST 用户输入必须转义，防止 XSS
- SHOULD 使用 CSP (Content Security Policy) 头
- MUST 禁止在前端存储敏感信息
- [计划] Token 存储在 httpOnly Cookie

### 3.2 后端安全

- MUST 密码使用 bcrypt/argon2 哈希存储，禁止明文
- MUST API 端点必须有认证和授权检查
- MUST SQL 查询使用参数化，防止 SQL 注入
- MUST 文件上传限制类型和大小
- MUST 敏感日志（密码、Token）必须脱敏
- SHOULD 实现请求频率限制（rate limiting）

### 3.3 日志安全

- MUST 日志不输出密码、Token、API Key
- MUST 日志不输出完整的请求体和响应体
- SHOULD 日志包含请求 ID（request_id）用于追踪

---

## 四、测试规范

### 4.1 前端测试

- SHOULD 组件有单元测试（Vitest + Vue Test Utils）
- SHOULD 关键工具函数有测试覆盖
- SHOULD 测试覆盖率目标：>70%

### 4.2 后端测试

- SHOULD 每个 API 端点有端到端测试
- SHOULD 服务层函数有单元测试
- SHOULD 数据库操作有集成测试
- SHOULD 测试覆盖率目标：>80%

### 4.3 测试命名

```
describe('ComponentName', () => {
  it('should render correctly', () => { ... })
  it('should handle empty data', () => { ... })
})

def test_get_projects_returns_paginated_list():
    pass

def test_create_project_validates_required_fields():
    pass
```

---

## 五、国际化 (i18n) 规范

### 5.1 强制要求

- MUST 所有面向用户的文本使用 `$t('key')`
- MUST 禁止模板中硬编码中文或英文
- MUST 翻译文件按模块组织，key 使用点号分隔

### 5.2 翻译文件

```javascript
// src/i18n/zh.js
export default {
  sidebar: {
    home: '首页',
    toolAuxPower: '辅助功耗计算',
  },
}

// src/i18n/en.js
export default {
  sidebar: {
    home: 'Home',
    toolAuxPower: 'Auxiliary Power Calculator',
  },
}
```

---

## 六、团队协作规范

### 6.1 分支管理

| 分支 | 用途 | 保护规则 |
|------|------|---------|
| `main` | 生产环境 | 禁止直接 push |
| `develop` | 开发环境 | 禁止直接 push |
| `feature/*` | 功能分支 | 从 develop 创建 |
| `fix/*` | Bug 修复分支 | 从 main 或 develop 创建 |
| `release/*` | 发布分支 | 从 develop 创建 |

### 6.2 提交规范

使用 Conventional Commits 格式：

```
<type>(<scope>): <subject>

type: feat|fix|chore|refactor|docs|style|test|perf
scope: frontend|backend|docs|config
subject: 使用中文简短描述，不超过 72 字符
```

示例：
```
feat(frontend): 添加效率链独立页面
fix(backend): 修复产品层级查询 N+1 问题
chore(config): 统一 AI 工具规则文件
refactor(frontend): 提取 useChart composable
perf(frontend): 添加 FinancialDashboard 防抖
```

### 6.3 代码审查

- SHOULD 至少 1 人审查
- SHOULD 审查者检查 [代码审查清单](#十代码审查清单)
- SHOULD 审查时间不超过 24 小时

### 6.4 合并规范

- MUST 合并前通过 CI 检查
- MUST 合并后删除功能分支
- SHOULD 使用 Squash Merge 合并到 main

---

## 七、工具配置

### 7.1 编辑器配置

项目根目录 `.vscode/settings.json` 已配置：

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  }
}
```

### 7.2 AI 工具规则

本项目使用 `.cursorrules` 作为 AI 编码规则的唯一权威来源。

| 文件 | 对应工具 | 说明 |
|------|---------|------|
| `.cursorrules` | Cursor / ZCode / 通用 | **权威源文件** |
| `AGENTS.md` | 通用 AI 工具 | 从 `.cursorrules` 同步 |
| `.continue/continue.yaml` | Continue | 从 `.cursorrules` 同步 |

同步机制：
```bash
# 修改 .cursorrules 后同步到其他 AI 工具
node scripts/sync-ai-rules.js

# 检查 AI 工具规则文件一致性
node scripts/check-ai-rules-consistency.js
```

---

## 八、项目脚本速查

### 前端

```bash
cd soh-sim-frontend

npm run lint              # ESLint 修复
npm run lint:no-fix       # ESLint 仅检查
npm run format            # Prettier 格式化
npm run format:check      # Prettier 格式检查
npm run type-check        # TypeScript 类型检查
npm run i18n:check        # 国际化覆盖率检查
```

### 后端

```bash
cd soh-sim-backend

black .                   # Black 格式化
isort .                   # isort 排序
flake8                    # Flake8 检查
```

### 全局检查

```bash
bash scripts/check-code-style.sh
```

---

## 九、存量代码豁免清单

以下规则对**存量代码**暂时豁免，但在**新增和修改的代码**中必须遵守：

| 规则 | 豁免说明 | 收敛计划 |
|------|---------|---------|
| 内联 `style` 属性 | 存量约 370 处违规 | 修改相关组件时顺手修复 |
| 组件 ≤ 400 行 | 存量 **34** 个组件超标（非原记录 26）；最大 `SimulationLab.vue` 2104 行、`RunningConditions.vue` 1617 行、`BatteryPCSConfig.vue` 1321 行 | 按风险排序逐步拆分，**日落 2026-12-31**；超 800 行须关联技术债工单 + 资深签字（见 §1.2） |
| `import * as echarts` | 经核查存量组件均为 `from 'echarts/core'` 按需引入（符合 §1.6），**无全量 `from 'echarts'` 违规**；原「3 个」记录失真 | 本条移除，无需修复 |
| TypeScript `any` | 存量 `.js` 文件较多 | 新 `.ts` 文件禁止使用 |

---

## 十、代码审查清单

提交 PR 前自查：

### 前端
- [ ] 所有文本使用 `$t()` 国际化
- [ ] 无内联事件处理器（`onfocus`/`onblur`）
- [ ] 无内联 `style` 属性
- [ ] 组件行数：新增组件建议 < 400 行；存量超 800 行需关联技术债工单 + 资深签字（见 §1.2）
- [ ] ECharts 实例在 `onUnmounted` 中 dispose
- [ ] `resize` 监听器在 `onUnmounted` 中移除
- [ ] `deep watch` 有防抖
- [ ] 运行 `npm run lint` 无错误
- [ ] 运行 `npm run type-check` 通过

#### 前端代码审查可读性检查卡

评审组件是否「过大」时，**不数行数，按以下清单判断**。任一为「否」即视为需拆分信号：

- [ ] 单一职责：组件只做一件事，无混杂的无关业务
- [ ] 可定位性：30 秒内能在文件中定位任意一段逻辑
- [ ] 内聚性：相关 state 与 behavior 是否已合理抽入 `use*` composable
- [ ] 模板可读性：模板结构清晰，无大段重复 / 嵌套过深
- [ ] 无 composable 汤：逻辑未被过度切碎导致更难追

> 说明：400–800 行组件若上述全为「是」，可判为好代码，无需拆分；> 800 行即便全为「是」，仍需技术债工单 + 资深签字（见 §1.2）。

### 后端
- [ ] 外键列有索引
- [ ] 无 N+1 查询（使用 `joinedload`/`selectinload`）
- [ ] 列表查询有分页
- [ ] 批量操作使用事务
- [ ] 无运行时动态注入 `to_dict`
- [ ] 认证端点未重复查询 User
- [ ] 运行 `black --check .` 通过
- [ ] 运行 `flake8` 无错误

### 通用
- [ ] 通过 CI/CD 流水线
- [ ] AI 规则文件已同步
- [ ] 相关文档已更新

---

## 十一、常见错误速查

| 错误 | 正确做法 |
|------|---------|
| `onfocus="this.style.border='1px solid blue'"` | `.input:focus { border-color: blue; }` |
| `style="color: red"` | `.error { color: red; }` |
| `import * as echarts from 'echarts'` | `import * as echarts from 'echarts/core'` + 按需引入 |
| `watch(data, handler, { deep: true })` | `watch(data, debounce(handler, 300))` |
| `window.addEventListener('resize', fn)` | `onMounted(()=>add) + onUnmounted(()=>remove)` |
| `User.query.get(user_id)` 在路由中 | 从 `token_required` 装饰器传入的 user 对象使用 |
