# 代码质量修复计划

**日期**: 2026-07-02
**审查依据**: CODE_STYLE.md v2.0 + checkpoint-20260701 代码质量审查报告
**目标**: 消除所有 CI 红X 并达到 CODE_STYLE.md 合规标准

---

## 当前状态概览

| 检查项 | 状态 | 违规数 |
|--------|------|--------|
| ESLint errors | ✅ 0 errors | 0 |
| Prettier | ✅ 通过 | 0 |
| Black/isort | ✅ 通过 | 0 |
| Flake8 | ✅ 通过 | 0 |
| AI 规则一致性 | ✅ 通过 | 0 |
| 内联事件处理器 | ⚠️ WARNING | 550 处 |
| 内联 style 属性 | ❌ 违规 | 1847 处 |
| ECharts 全量导入 | ❌ 违规 | 10 个文件 |
| to_dict 动态注入 | ❌ 违规 | 27 个模型 |
| 组件 > 400 行 | ⚠️ Warning | 20+ 个文件 |
| 硬编码中文 | ❌ 违规 | 59 个文件 |
| 共享样式重复 | ⚠️ 部分 | 15+ 文件 |

---

## 修复优先级矩阵

| 阶段 | 工作量 | 收益 | 风险 |
|------|--------|------|------|
| P0: ECharts 按需导入 | 2 小时 | 减少打包体积 ~300KB | 极低 |
| P0: to_dict 显式定义 | 4 小时 | 符合规范，IDE 友好 | 低 |
| P1: 共享样式提取 | 1 天 | 减少 15+ 文件重复代码 | 低 |
| P1: 内联事件处理器 | 3-5 天 | 符合规范，主题切换支持 | 中 |
| P2: 内联 style 提取 | 5-7 天 | 符合规范，可维护性提升 | 中 |
| P2: 大型组件拆分 | 2-3 周 | 可读性/可测试性提升 | 高 |
| P3: i18n 全覆盖 | 3-5 天 | 国际化支持 | 中 |

---

## 阶段一：P0 - 低风险快速修复

### 任务 1.1: ECharts 按需导入（10 个文件）

**影响文件**：
- `src/components/ScenarioCompare.vue` (L446)
- `src/components/SimulationLab.vue` (L1250)
- `src/components/SensitivityAnalysis.vue` (L220)
- `src/components/FinancialDashboard.vue` (L978)
- `src/components/BatteryPCSConfig.vue` (L368)
- `src/components/BatteryHealthHeatmap.vue` (L48)
- `src/components/CostWaterfallChart.vue` (L77)
- `src/components/SohChart.vue` (L161)
- `src/components/EnergyFlowSankey.vue` (L139)

**修复方案**：
将 `import * as echarts from 'echarts'` 替换为与 `useChart.js` 一致的 tree-shakable 导入：

```js
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart, PieChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, GridComponent } from 'echarts/components'
echarts.use([CanvasRenderer, LineChart, BarChart, PieChart, TitleComponent, TooltipComponent, GridComponent])
```

**注意**：每个文件需要分析其实际使用的图表类型（Line/Bar/Pie/Sankey/Gauge/Heatmap），只导入所需的 chart 类型。

**验证**：`npm run lint:no-fix` 仍需通过，构建产物体积减小。

---

### 任务 1.2: to_dict 显式定义（27 个模型）

**当前状态**：34 个模型中 7 个有显式 `to_dict()`，27 个使用 `_model_to_dict` 动态注入。

**修复方案**：
为每个缺少显式 `to_dict()` 的模型添加显式方法。参考已有的 7 个模板：

```python
# database.py 中已有模板（L626-635）
def to_dict(self):
    return {
        'id': self.id,
        'name': self.name,
        'tenant_id': self.tenant_id,
        'created_at': self.created_at.isoformat() if self.created_at else None,
    }
```

**涉及模型**（需逐一添加）：
- Tenant、Survey、Project、ProjectVersion、Simulation、SimulationResult、CorrectionTemplate、BatteryPCSConfig、SohRteData、FinancialData、ProductConfig、FormulaConfig、AlgorithmModel、BoqSection、BoqItem、BatteryManufacturer、PinnModelWeights、SystemArchitecture、GridComplianceAnalysis、SafetyFireDesign、IPPFinancialModel、ComplianceMatrix、ThermalManagement、ScadaEmsDesign、HVInterconnection、BidDocument

**验证**：
1. `python3 -c "from database import *; print('OK')"` 无报错
2. 所有 API 响应仍正确返回字典
3. `grep -c "def to_dict" database.py` 应为 34

---

## 阶段二：P1 - 中等工作量

### 任务 2.1: 共享样式提取

**目标**：将 `.tool-page`、`.phase-page`、`.tool-header` 等重复样式提取到 `src/assets/styles/shared.css`。

**重复模式**（每个文件都复制一遍）：
```css
.tool-page { padding: 24px; }
.tool-header { margin-bottom: 24px; }
.tool-header h1 { font-size: 24px; font-weight: 700; margin: 0 0 8px; }
.phase-page { padding: 24px; }
.phase-header { margin-bottom: 20px; }
```

**修复方案**：
1. 在 `src/assets/styles/shared.css` 中统一定义所有共享类
2. 在每个组件中删除重复定义，改为 `import '@/assets/styles/shared.css'` 或在 `<style>` 中保留 scoped 样式
3. 需要检查的文件：15+ 个 ToolPage/PhasePage 组件

**验证**：`npm run format:check` 通过，页面布局无变化。

---

### 任务 2.2: 内联事件处理器消除（550 处）

**目标**：将所有 `onfocus`/`onblur`/`onmouseover`/`onmouseout` 改为 CSS 伪类。

**常见模式**：
```html
<!-- 当前（违规） -->
<input onfocus="this.style.borderColor='blue'" onblur="this.style.borderColor='#ccc'" />

<!-- 修复后（合规） -->
<input class="input-field" />
```
```css
.input-field {
  border: 1px solid var(--color-input-border);
  transition: border-color 0.2s;
}
.input-field:focus-visible {
  border-color: var(--color-accent);
}
```

**受影响最大的文件**：
| 文件 | 数量 |
|------|------|
| SimulationLab.vue | 96 |
| ProductConfig.vue | 60 |
| PcsACDesign.vue | 44 |
| SurveyPage.vue | 42 |
| EngineeringCalc.vue | 42 |
| BatteryDCDesign.vue | 42 |
| FinancialDashboard.vue | 35 |
| ScenarioCompare.vue | 32 |

**修复方案**：
1. 在 `shared.css` 中定义通用输入框样式类 `.input-field`、`.input-field-focus` 等
2. 逐个文件替换内联事件为 CSS 类
3. 对于需要动态颜色的场景（不同输入框不同颜色），使用 CSS 变量或特定类名

**验证**：`bash scripts/check-code-style.sh` 不再报告内联事件 WARNING。

---

## 阶段三：P2 - 高工作量

### 任务 3.1: 内联 style 属性消除（1847 处）

**目标**：将所有 `style="..."` 替换为 CSS 类。

**主要重灾区**：
- `BatteryDCDesign.vue`：约 500+ 处内联 style
- `SimulationLab.vue`：约 400+ 处
- `ProductConfig.vue`：约 300+ 处

**修复方案**：
1. 识别重复的内联 style 模式（如 `background-color: var(--color-card-dark); border: 1px solid var(--color-border)`）
2. 提取为共享类名（如 `.card-dark`、`.card-bordered`）
3. 对于动态计算的样式（如 `width: ${val}%`），保留 `:style` 绑定但减少静态内联 style

**注意**：此任务工作量最大，建议按组件逐个推进。

---

### 任务 3.2: 大型组件拆分（20+ 文件）

**超标组件**：
| 组件 | 行数 | 建议拆分 |
|------|------|---------|
| SimulationLab.vue | 1880 | SurveyStep/ParamsStep/AlgoStep/CorrectionStep/ResultStep |
| FinancialDashboard.vue | 1739 | RevenuePanel/CostPanel/FinancingPanel/CashFlowTable/CashFlowChart |
| ProductConfig.vue | 1400 | CellSelector/PackSelector/RackSelector/ClusterSelector |
| RunningConditions.vue | 1228 | SiteConditions/GridConditions/FinancialConditions |
| BatteryPCSConfig.vue | 1112 | PCSConfigForm/PCSConnectionDiagram/PCSChart |
| EpcPage.vue | 1341 | SystemArch/GridCompliance/FireSafety/IPPFinance |

**修复方案**：
1. 按功能步骤/模块拆分为子组件
2. 使用 `defineProps`/`defineEmits` 传递数据和事件
3. 每个子组件不超过 400 行
4. 父组件只负责布局和状态管理

**验证**：`npm run lint:no-fix` 中 max-lines warnings 归零。

---

## 阶段四：P3 - 国际化

### 任务 4.1: i18n 全覆盖（59 个文件）

**目标**：所有硬编码中文替换为 `$t('key')`。

**当前状态**：约 59 个文件包含硬编码中文。

**修复方案**：
1. 在 `zh.js` 和 `en.js` 中补充缺失的翻译 key
2. 逐个文件将硬编码文本替换为 `$t('key')`
3. 删除 `ModernSidebar.vue`（旧版 emoji 组件）
4. 统一变量命名（数据属性保持英文，UI 文本走 i18n）

**验证**：`npm run i18n:check` 通过，中英文翻译数量一致。

---

## 执行策略

### 推荐执行顺序

```
P0-ECharts (2h) → P0-to_dict (4h) → P1-shared-css (1天) → P1-events (3-5天)
→ P2-inline-style (5-7天) → P2-component-split (2-3周) → P3-i18n (3-5天)
```

### 每次修复后的验证步骤

1. `npm run lint:no-fix` → 0 errors
2. `npm run format:check` → 全部通过
3. `python3 -m black --check .` → 全部通过
4. `python3 -m flake8 .` → 全部通过
5. `bash scripts/check-code-style.sh` → 无 ERROR

### 风险控制

- 每个阶段完成后立即提交并推送
- 每个阶段完成后运行完整 CI 验证
- 大型组件拆分前先在子组件上验证功能不变
- i18n 替换前先备份翻译文件
