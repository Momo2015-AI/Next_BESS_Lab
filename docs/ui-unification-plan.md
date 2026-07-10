# UI 统一化开发计划

> 创建日期: 2026-07-10
> 分支: ENG0709
> 状态: 待执行

---

## 一、现状诊断

### 1.1 三套不兼容的布局体系

| 布局模式 | 根容器 class | 使用页面 | 结构 |
|----------|-------------|----------|------|
| **Phase 布局** | `.phase-page` | Phase1, Phase2, Phase3, Phase5 | `phase-header` + `phase-body` + `steps-nav` + `step-content` |
| **Tool 布局** | `.tool-page` | 15 个 Tool 页面 + AuthPage + AdminPanelPage | `tool-header` + 内容区域 |
| **自定义布局** | 各自不同 | Phase4, Orchestrator, EPC, Survey | 每个都不同 |

```
Phase1/2/3/5:  .phase-page → .phase-header → .phase-body → .steps-nav → .step-content
Tool 页面:     .tool-page → .tool-header → 各自内容
Phase4:        .h-full.overflow-y-auto → .max-w-5xl.mx-auto → .grid.grid-cols-2 (Tailwind)
Orchestrator:  .orchestrator-page → .page-header → .project-bar
EPC:           .epc-page → .epc-header → .epc-tabs
Survey:        .survey-page → .tool-page.max-w-4xl.mx-auto → .tool-header
```

### 1.2 双重 CSS 变量命名系统

`style.css :root` 中同时存在两套变量：

| 新系 (`--bg-*`, `--text-*`) | 旧系 (`--color-*`) | 使用者 |
|------------------------------|---------------------|--------|
| `--bg-card` | `--color-card` | `shared.css` 用旧系，`app-shell.css`/`admin-panel.css` 用新系 |
| `--text-primary` | `--color-text` | 同上 |
| `--text-secondary` | `--color-text-secondary` | 同上 |
| `--border-color` | `--color-border` | 同上 |
| `--accent-blue` | `--color-accent` | 同上 |

### 1.3 `shared.css` 严重膨胀

```
shared.css 总计 1148 行：
  ├── ~330 行：EPC 模块样式（手动编写，有语义）
  ├── ~400 行：u-* 自动生成工具类（第一轮）
  ├── ~280 行：u-* 自动生成工具类（第二轮）
  └── ~140 行：语义化状态类（手动编写，有价值）
```

代表性怪物类名：`.u-background-color-var-color-card-border-1px-solid-var-color-border-border-top-2px-solid-var-color-accent`

### 1.4 内联 style 残留（13 个文件，372 处）

| 文件 | 数量 | 优先级 |
|------|------|--------|
| `FinancialInputs.vue` | **94** | P0 |
| `PcsACDesign.vue` | **71** | P0 |
| `ScenarioCompare.vue` | **52** | P0 |
| `RunningConditions.vue` | **46** | P0 |
| `SensitivityAnalysis.vue` | **33** | P0 |
| `FinancialCharts.vue` | 27 | P1 |
| `FinancialTable.vue` | 27 | P1 |
| `CurrencyConverter.vue` | 8 | P2 |
| `ProductConfig.vue` | 7 | P2 |
| `FinancialMetrics.vue` | 4 | P2 |
| `FormulaLab.vue` | 2 | P2 |
| `HomePage.vue` | 1 | P2 |
| `epc/EpcThermal.vue` | 1 | P2 |

### 1.5 Emoji 图标残留（8 个文件，19 处）

| 文件 | Emoji | 数量 |
|------|-------|------|
| `ToolProjectsPage.vue` | 📁📋🔧✨💾 | 5 |
| `DesignComparePanel.vue` | 📊⚡🔄⚙ | 4 |
| `OrchestratorPage.vue` | 🔬 | 1 |
| `VersionCompare.vue` | 🔄📊🎯 | 3 |
| `DesignEnginePanel.vue` | ⚡⚙ | 2 |
| `AugmentationCompare.vue` | 📊🔄 | 2 |
| `PcsACDesign.vue` | ⚡ | 1 |
| `ParameterPanel.vue` | ⚙ | 1 |

> 违反 CODE_STYLE.md 规则：禁止 emoji 作为图标，应使用 AppIcon 组件

### 1.6 硬编码颜色值（16 个文件）

| 文件 | 数量 | 说明 |
|------|------|------|
| `DesignEnginePanel.vue` | 13 | 新引擎组件，硬编码严重 |
| `OrchestratorPage.vue` | 10 | 新工作流页面 |
| `NexBessLogo.vue` | 8 | Logo 组件（可接受） |
| `DesignComparePanel.vue` | 8 | 新对比组件 |
| `AugmentationCompare.vue` | 9 | 补容对比 |
| `SohChart.vue` | 9 | 图表色板 |
| `ToolProjectsPage.vue` | 7 | 项目管理 |
| `FinancialCharts.vue` | 7 | 财务图表 |
| 其余 8 文件 | 各 1-4 | 零散 |

### 1.7 CSS 文件加载不一致

```
main.js 全局加载：
  ✅ style.css      — Design tokens (:root + [data-theme='dark'])
  ✅ shared.css     — EPC 样式 + u-* 工具类

未全局加载（仅组件局部 import）：
  ❌ app-shell.css  — App.vue 局部
  ❌ admin-panel.css — AdminPanel 组件局部
  ❌ aux-power.css   — ToolAuxPower 组件局部
```

### 1.8 图标体系

| 位置 | 用途 | 说明 |
|------|------|------|
| `src/components/AppIcon.vue` | 所有 UI 功能图标 | 内联 SVG，378 行，40+ 图标 |
| `public/favicon.svg` | 浏览器标签图标 | 已更新为 Mobius 无穷符号 ✅ |
| `public/icons.svg` | SVG sprite 合集 | 存在但使用情况不明 |
| `src/components/NexBessLogo.vue` | 品牌 Logo | 内联 SVG 组件，双主题适配 |

---

## 二、改造原则

1. **Design Token 单一来源**：统一为 `--color-*` 前缀，删除 `--bg-*`/`--text-*` 旧别名
2. **统一布局组件**：所有页面使用 `<AppPage>` 包裹，消除 3 套布局
3. **零内联 style**：全部提取为 CSS 类或 CSS 变量
4. **零 Emoji 图标**：全部替换为 `<AppIcon>`
5. **零硬编码颜色**：全部使用 CSS 变量
6. **最小改动原则**：不重写组件逻辑，只改样式和布局

---

## 三、执行计划

### PR1：基础设施（Token 统一 + shared.css 重写 + AppPage 组件）

#### Step 1: Design Token 统一（1 天）

**目标**：消除双命名系统，所有变量统一为 `--color-*` 前缀。

**操作**：
- `style.css :root` 中保留 `--color-*` 系列（旧系），删除或设为别名 `--bg-*`/`--text-*`（新系）
- `app-shell.css` 中所有 `--bg-card` → `--color-card`，`--text-primary` → `--color-text` 等
- `admin-panel.css` 同上
- 保留临时别名 `--bg-card: var(--color-card)` 防止遗漏导致样式丢失

**验证**：切换 light/dark 主题，检查所有页面颜色正常。

#### Step 2: 重写 `shared.css`（1 天）

**目标**：从 1148 行 → ~400 行。

**操作**：
- **删除**：全部 `u-*` 自动生成类（~680 行）
- **保留**：EPC 语义化类（`.panel-card`, `.metric-card`, `.data-table` 等）
- **保留**：手动编写的状态类（`.card-selected`, `.tab-active`, `.btn-primary` 等）
- **删除前**：全局搜索每个 `u-*` 类名，确认引用并替换为语义化类或 CSS 变量

**验证**：所有页面无样式丢失。

#### Step 3: 创建 `AppPage.vue` 布局组件（0.5 天）

**目标**：统一所有页面的布局结构。

```vue
<!-- src/components/AppPage.vue -->
<template>
  <div class="app-page">
    <div class="app-page-header">
      <h1>{{ $t(titleKey) }}</h1>
      <p v-if="descKey" class="app-page-desc">{{ $t(descKey) }}</p>
      <div class="app-page-actions"><slot name="actions" /></div>
    </div>
    <div class="app-page-body">
      <slot />
    </div>
  </div>
</template>
```

**在 `shared.css` 中新增**：
```css
.app-page { padding: 24px; }
.app-page-header { margin-bottom: 24px; }
.app-page-header h1 { font-size: 24px; font-weight: 700; margin: 0 0 8px; }
.app-page-desc { color: var(--color-text-secondary); font-size: 14px; margin: 0; }
.app-page-actions { display: flex; gap: 8px; margin-top: 12px; }
.app-page-body { min-height: 400px; }
```

**PR1 总预估**：2.5 天

---

### PR2：页面迁移（统一使用 AppPage）

#### Step 4: 迁移 Phase 页面（0.5 天）

| 页面 | 当前 | 目标 |
|------|------|------|
| Phase1Page | `.phase-page` | `<AppPage title-key="phase1.title" desc-key="phase1.desc">` |
| Phase2Page | `.phase-page` | `<AppPage>` + 保留 `steps-nav` / `step-content` |
| Phase3Page | `.phase-page` | `<AppPage>` + actions slot 放 runPipeline 按钮 |
| Phase5Page | `.phase-page` | `<AppPage>` |

#### Step 5: 迁移 Tool 页面（0.5 天）

15 个 Tool 页面已统一使用 `.tool-page` + `.tool-header`，批量替换为 `<AppPage>`。

#### Step 6: 迁移异构页面（1 天）

| 页面 | 当前 | 目标 | 风险 |
|------|------|------|------|
| Phase4Page | Tailwind `h-full max-w-5xl mx-auto grid grid-cols-2` | `<AppPage>` | 中 — Tailwind 深度耦合 |
| OrchestratorPage | `.orchestrator-page` | `<AppPage>` + 保留 `project-bar` | 低 |
| EpcPage | `.epc-page` | `<AppPage>` + 保留 `.epc-tabs` | 低 |
| SurveyPage | `.survey-page` + `.tool-page` 嵌套 | `<AppPage>` | 低 |
| AuthPage | `.tool-page` | `<AppPage>` | 低 |
| AdminPanelPage | `.tool-page` | `<AppPage>` | 低 |

**PR2 总预估**：2 天

---

### PR3：消除内联 style（按优先级分批）

#### Step 7: P0 文件（5 个文件，296 处）

| 文件 | 数量 | 策略 |
|------|------|------|
| `FinancialInputs.vue` | 94 | 提取表单输入类到 shared.css |
| `PcsACDesign.vue` | 71 | 提取电气参数卡片样式 |
| `ScenarioCompare.vue` | 52 | 提取对比卡片样式 |
| `RunningConditions.vue` | 46 | 提取条件卡片样式 |
| `SensitivityAnalysis.vue` | 33 | 提取分析图表样式 |

**预估**：2 天

#### Step 8: P1 文件（2 个文件，54 处）

| 文件 | 数量 |
|------|------|
| `FinancialCharts.vue` | 27 |
| `FinancialTable.vue` | 27 |

**预估**：0.5 天

#### Step 9: P2 文件（6 个文件，22 处）

零散内联 style，逐个替换。

**预估**：0.5 天

**PR3 总预估**：3 天

---

### PR4：Emoji 替换 + 硬编码颜色清理

#### Step 10: Emoji → AppIcon（0.5 天）

| 文件 | Emoji | 替换为 |
|------|-------|--------|
| `ToolProjectsPage.vue` | 📁📋🔧✨💾 | `folder`, `document`, `settings`, `sparkles`, `save` |
| `DesignComparePanel.vue` | 📊⚡🔄⚙ | `bar-chart`, `zap`, `refresh`, `settings` |
| `OrchestratorPage.vue` | 🔬 | `flask` |
| `VersionCompare.vue` | 🔄📊🎯 | `refresh`, `bar-chart`, `target` |
| `DesignEnginePanel.vue` | ⚡⚙ | `zap`, `settings` |
| `AugmentationCompare.vue` | 📊🔄 | `bar-chart`, `refresh` |
| `PcsACDesign.vue` | ⚡ | `zap` |
| `ParameterPanel.vue` | ⚙ | `settings` |

> 需要在 `AppIcon.vue` 中新增 `refresh` 和 `sparkles` 图标定义（如果不存在）

#### Step 11: 硬编码颜色 → CSS 变量（0.5 天）

16 个文件中的 `#xxx` 替换为 `var(--color-*)`。

**例外**：`NexBessLogo.vue` 中的 SVG 渐变色可保留硬编码（SVG 内联渐变不适合用 CSS 变量）。

**PR4 总预估**：1 天

---

### PR5：CSS 文件加载统一

#### Step 12: 全局加载所有共享 CSS（0.5 天）

```js
// main.js
import './style.css'
import './assets/styles/shared.css'
import './assets/styles/app-shell.css'    // 新增全局加载
import './assets/styles/admin-panel.css'  // 新增全局加载
```

移除组件中的局部 import，确保 CSS 加载顺序一致。

**PR5 总预估**：0.5 天

---

## 四、总览

| PR | 内容 | 工时 | 依赖 |
|----|------|------|------|
| **PR1** | Token 统一 + shared.css 重写 + AppPage 组件 | 2.5 天 | 无 |
| **PR2** | 所有页面迁移到 AppPage | 2 天 | PR1 |
| **PR3** | 消除 372 处内联 style | 3 天 | PR1 |
| **PR4** | Emoji 替换 + 硬编码颜色清理 | 1 天 | PR1 |
| **PR5** | CSS 加载统一 | 0.5 天 | PR1 |
| **总计** | | **9 天** | |

### 执行顺序

```
PR1 (基础设施) → PR2 (页面迁移) ─┬→ PR3 (内联style)
                                  ├→ PR4 (Emoji+颜色)
                                  └→ PR5 (CSS加载)
```

PR1 是前置依赖，PR2-5 可以并行（但建议 PR2 先做，因为页面迁移后更容易定位内联 style）。

---

## 五、风险与缓解

| 风险 | 等级 | 缓解 |
|------|------|------|
| Token 合并导致部分组件颜色丢失 | **高** | Step 1 保留别名，渐进式删除 |
| `u-*` 类删除后组件样式丢失 | **高** | 删除前全局搜索引用，逐类替换 |
| Phase4 Tailwind 迁移风险 | **中** | 可保留 Tailwind 作为页面内布局，仅外层换 AppPage |
| 内联 style 消除引入动态计算 bug | **中** | 动态值保留 `:style` 但用 CSS 变量 |
| AppIcon 缺少需要的图标 | **低** | 提前在 AppIcon.vue 中补齐 `refresh`, `sparkles` 等 |

---

## 六、不改的内容

| 组件/文件 | 原因 |
|-----------|------|
| `AppIcon.vue` 图标体系 | 已集中管理，只需补充少量图标 |
| `NexBessLogo.vue` | 品牌 Logo，独立设计 |
| `favicon.svg` | 已更新 ✅ |
| Tailwind CSS 框架 | 保留作为工具类辅助，不强制移除 |
| 组件业务逻辑 | 只改样式和布局，不动功能 |
