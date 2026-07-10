# 方案 C 实施计划：引擎集中 + 业务可插拔

> 审定日期: 2026-07-10
> 分支: ENG0709
> 审核人: AI Code Review
> 状态: 已批准，待执行

---

## 一、现状诊断（已验证属实 ✅）

| # | 问题 | 严重性 | 验证结果 |
|---|------|--------|----------|
| 1 | 两套并行 API（新旧并存），前端混用 | 高 | ✅ Phase3 调旧 pipeline，Orchestrator 调新引擎 |
| 2 | `POST /api/financial/calculate` 两个 blueprint 注册同一端点 | 高 | ✅ 新引擎覆盖旧引擎 |
| 3 | `store.refreshFinancialResults()` 无人调用 — 死代码 | 中 | ✅ 零调用者 |
| 4 | `POST /api/soh/calculate` 被两个组件调用但后端不存在 | 高 | ✅ 无此端点 |
| 5 | `ScenarioCompare/SensitivityAnalysis` 用 raw fetch 绕过 auth | 中 | ✅ 确认 raw fetch |
| 6 | Phase3 调旧 pipeline API，Orchestrator 调新引擎 API | 中 | ✅ 两套逻辑并行 |

---

## 二、改造原则

1. **新引擎 API 是唯一权威路径**，旧 API 逐步下线
2. Phase 页面不 import 引擎类，只通过 API 调用
3. 数据流统一走 Pinia store，页面只读不写
4. **最小改动**：不重写 Phase 页面，只换 API 调用

---

## 三、执行计划

### PR 1：API 统一 + 死代码清除 + Phase3 迁移

#### 第 1 步：消除冲突和死代码（预估 1h）

**删除项**：
- `routes/financial.py` 中 `POST /api/financial/calculate`（旧端点）
- `stores/bess.js` 中 `refreshFinancialResults()` action
- `routes/financial.py` 中不再需要的 import

**保留项**：
- `POST /api/financial/capex-from-boq`（BOQ 编辑器仍在使用）
- `services/pipeline.py`（被新 SimulationEngine 内部引用）
- `services/financial/calculator.py`（被新 FinancialEngine 内部引用）

#### 第 2 步：新增 `store.runSimulationEngine()`（预估 2h）

在 `stores/bess.js` 中新增 action：

```text
store.runSimulationEngine()
  → POST /api/simulation/run       （退化 + 能量核算 + 补容策略）
  → POST /api/financial/calculate   （财务计算）
```

**关键设计**：
- **Response 适配层**：新 API 返回格式与旧 `/api/pipeline/calculate` 不同，需要在 action 中做字段 mapping，写回旧 state 路径以保持 Phase4/Phase5 兼容
- **错误回滚**：第二步（财务）失败时，清理第一步（仿真）写入的 store 状态，给用户明确错误提示
- **旧 `runPipeline()` 保留**，标记 `@deprecated`

#### 第 3 步：Phase3Page + SimulationLab 迁移（预估 3h）

| 文件 | 变更 |
|------|------|
| `pages/Phase3Page.vue` | `runPipeline()` → `runSimulationEngine()` |
| `components/SimulationLab.vue` | `runBackendSimulation()` 中 POST 改调 `/api/simulation/run` |

**风险点**：
- `SimulationLab.vue` 有 1400+ 行，大量消费旧 API 返回字段
- 需要做字段兼容，确保图表渲染、表格数据均正常

#### 第 4 步：ScenarioCompare + SensitivityAnalysis 修复（预估 1.5h）

| 文件 | 变更 |
|------|------|
| `ScenarioCompare.vue` | `raw fetch /api/soh/calculate` → `post('/api/simulation/run')` via `services/api.js` |
| `SensitivityAnalysis.vue` | `raw fetch /api/soh/calculate` → `post('/api/financial/sensitivity')` via `services/api.js` |

**执行前必须验证**：`SensitivityAnalysis` 现有请求体格式 vs `/api/financial/sensitivity` 期望格式是否兼容。

#### 第 5 步：删除旧 pipeline 端点（预估 0.5h）

- `routes/pipeline.py` 中 `POST /api/pipeline/calculate` **直接删除**
- `GET /api/pipeline/task/<id>` 如无人调用一并删除
- 清理不再需要的 import

#### 第 6 步：验证 + 提交（预估 1h）

- 前后端 lint 检查通过
- 手动功能测试：Phase3 仿真 → Phase4 财务看板 → Phase5 结果展示全链路

**PR 1 总预估**：~9h

---

### PR 2：Phase 页面全面接入新引擎 API

| 文件 | 变更 |
|------|------|
| `Phase2Page`（方案设计） | 通过 store action 调 `POST /api/design/auto` |
| `Phase4Page`（经济评估） | 通过 store action 调 `POST /api/financial/calculate` |
| `ToolSimulationViewPage` | 通过 store action 调 `POST /api/simulation/run` |
| `ToolFinancialPage` | 通过 store action 调 `POST /api/financial/calculate` |

**PR 2 总预估**：~4h

---

## 四、不改的内容

| 组件/文件 | 原因 |
|-----------|------|
| `OrchestratorPage` | 已完美走新 API ✅ |
| `DesignEnginePanel` | 已完美走新 API ✅ |
| Phase1/Phase5 | 不涉及引擎调用 |
| BOQ 编辑器 | `POST /api/financial/capex-from-boq` 保留 |
| `services/pipeline.py` | 被新 SimulationEngine 内部引用 |
| `services/financial/calculator.py` | 被新 FinancialEngine 内部引用 |

---

## 五、涉及文件清单

| 文件 | 变更类型 | PR |
|------|---------|-----|
| `stores/bess.js` | 修改 | PR1 |
| `routes/financial.py` | 删除旧端点 | PR1 |
| `routes/pipeline.py` | 删除旧端点 | PR1 |
| `pages/Phase3Page.vue` | 修改 | PR1 |
| `components/SimulationLab.vue` | 修改 | PR1 |
| `components/ScenarioCompare.vue` | 修改 | PR1 |
| `components/SensitivityAnalysis.vue` | 修改 | PR1 |
| 各 Phase/Tool 页面 | 新增调用 | PR2 |
| `i18n/zh.js, en.js` | 可能新增 | PR1 |

---

## 六、风险与缓解

| 风险 | 等级 | 缓解措施 |
|------|------|----------|
| SimulationLab 字段不兼容导致展示异常 | **高** | 先做 response 字段 diff，store 中做 mapping 适配层 |
| 财务第二步失败导致状态不一致 | **中** | action 内 try-catch + 回滚 |
| SensitivityAnalysis 参数格式不兼容 | **中** | 执行前先读两边的接口定义做比对 |
| 测试覆盖不足导致回归 | **中** | PR1 后做手动端到端测试（Phase3→Phase4→Phase5） |
