# P2-1 / P2-2 可执行重构计划

> 方法论（用户指定）：**先补测试，再按组件拆分**。每一步重构前先用测试锁定现状行为，确保重构等价、可回滚。
> 规范依据：`AGENTS.md` / `CODE_STYLE.md`（组件 ≤400 行、无内联 style、service 层、统一响应、租户隔离+索引、列表分页）。

---

## 0. 现状盘点（证据）

### P2-1 前端 EPC
| 文件 | 行数 | 角色 | 问题 |
|------|------|------|------|
| `soh-sim-frontend/src/pages/EpcPage.vue` | 1447 | 路由入口（`router/index.js:122`） | 超 400 行；9 个模块 tab 全部内联；约 330 行 CSS 未抽离（`EpcPage.vue:1108-1437`）；裸 `fetch` 未用 `api.js` |
| `soh-sim-frontend/src/components/EpcModules.vue` | 1174 | **未被任何文件引用**（仅 `EpcPage` 在路由中） | 与 `EpcPage` 结构**完全重复**（相同 9 个 tab `P0-3…P1-4`、相同 9 个表单、相同 `renderPlotly/purgePlotly` 导入、`EpcModules.vue:921-924`）；孤立副本 |
| `soh-sim-frontend/src/composables/usePlotly.js` | 66 | 已提取的 Plotly 组合式 | 良好，可作图表预览组件基础 |
| `soh-sim-frontend/src/services/api.js` | 156 | 已建立统一请求层 | 良好，但未在 EPC 组件中复用 |

两文件均使用 `:style` 动态内联绑定（`EpcModules.vue:9-13`），违反“无内联 style”规则。

### P2-2 后端 routes
| 文件 | 行数 | 问题 |
|------|------|------|
| `routes/ai_sim.py` | 407 | 内联 `db.session`、裸 `jsonify`，未用 `api_response`，未确认租户过滤 |
| `routes/auth.py` | 458 | 租户 ID 硬编码默认 UUID（`auth.py:194`），用户操作逻辑可直接下沉 service |
| `routes/export.py` | 356 | 业务逻辑内联，响应格式不一致 |
| `routes/products.py` | 858 | 最大文件，内联 SQL/计算最多 |
| `routes/report.py` | 897 | 内联计算与图表构造 |

已具备但未充分利用：
- `utils/api_response.py` → `success_response` / `error_response` / `paginated_response`（契约 `{success,data,error,message}` + `pagination`）
- `services/`（boq/degradation/efficiency/financial/pipeline/units）→ 模式已存在，目标路由未复用
- `token_required` 装饰器（`auth.py:426`）已注入 `request.current_user`

**两侧均无任何测试框架**：后端无 `test_*.py`/pytest；前端 `package.json` 无 vitest/jest。

---

## 1. P2-1 前端 EPC 组件拆分

### 阶段 0 — 补测试（锁定现状，禁止先改）
- [ ] **0.1 搭建 vitest 基建**：`package.json` 加 `vitest`、`@vue/test-utils`、`jsdom`；新增 `vitest.config.js`（`environment: 'jsdom'`）；`npm run test` 脚本。
- [ ] **0.2 usePlotly 单测**：`__tests__/usePlotly.spec.js` — `loadPlotly` 懒加载（CDN 注入一次复用）、`renderPlotly` 调用 `Plotly.newPlot`、`purgePlotly` 在 `onUnmounted` 清理且不抛错。
- [ ] **0.3 api.js 单测**：`__tests__/api.spec.js` — mock `fetch`：401 清 token 跳登录、非 JSON 走 blob、超时抛 `ApiError`、成功按 `{success,data}` 解析。
- [ ] **0.4 EpcPage 表征测试（拆前快照）**：`__tests__/EpcPage.characterization.spec.js` — 渲染 9 个 tab、各表单 `v-model` 双向绑定、`apiCall` 成功/失败分支（emit `error`）。**此测试在拆分过程中必须保持通过。**

### 阶段 1 — 按组件拆分
- [ ] **1.1 消除重复（先定 source of truth）**：确认 `EpcPage.vue` 为唯一路由入口，**删除孤立的 `EpcModules.vue`**（或改造为共享模块组件由 `EpcPage` 引入——二选一，推荐删除，避免双份维护）。
- [ ] **1.2 提取状态/行为 composable**：新建 `src/composables/useEpcModules.js`，迁入 9 个 `reactive` 表单（`archForm…bidForm`）、9 个结果 `ref`、`apiCall` 及每个模块的 action 函数（`designArchitecture` 等），改为调用 `services/api.js`。组件退化为纯展示。
- [ ] **1.3 拆 9 个子组件** `src/components/epc/`：
  `EpcArchitecture.vue` / `EpcGridCompliance.vue` / `EpcSafety.vue` / `EpcIppFinance.vue` / `EpcComplianceMatrix.vue` / `EpcThermal.vue` / `EpcScadaEms.vue` / `EpcHvConnection.vue` / `EpcBidDoc.vue`。每个接收 `v-model` 表单、emit 结果，单文件 ≤400 行。
- [ ] **1.4 提取图表预览**：新建 `src/components/epc/EpcChartPreview.vue`，内部用 `usePlotly.js` 渲染，负责 `onMounted` 渲染 + `onUnmounted` `purgePlotly`。
- [ ] **1.5 收敛页面壳**：`EpcPage.vue` 仅保留 tab 导航 + 布局，循环渲染 9 个子组件；所有请求经 `services/api.js`（去掉裸 `fetch`）。
- [ ] **1.6 样式治理**：`EpcPage.vue` 约 330 行 CSS（`:1108-1437`）抽到 `src/assets/styles/shared.css`；`:style` 动态绑定（如 tab 激活态）改为 `:class` + CSS 变量，消除内联 style。
- [ ] **1.7 每拆一个子组件补单测**（`render` + 关键交互），阶段 0.4 表征测试随结构迁移更新后保持通过。

**P2-1 验收**：所有 EPC 组件 ≤400 行；零内联 `style`；`npm run lint` + `npm run test` 通过；`EpcModules.vue` 不再孤立重复。

---

## 2. P2-2 后端 routes 重构

### 阶段 0 — 补测试
- [ ] **0.1 搭建 pytest 基建**：`pyproject.toml` 加 `pytest`；新增 `tests/conftest.py` — app fixture、临时 DB（SQLite 内存或测试库）、`test_client`、注入 `Authorization` token 的 helper（走 `token_required`）。
- [ ] **0.2 五路由接口测试**：`tests/test_ai_sim.py` / `test_auth.py` / `test_export.py` / `test_products.py` / `test_report.py`，断言**统一响应契约** `{success, data, error, message}`，覆盖 200/400/401/404/500 与租户数据隔离。

### 阶段 1 — 抽 service 层 + 统一响应 + 租户隔离
- [ ] **1.1 统一响应**：5 个路由全部改用 `success_response` / `error_response` / `paginated_response`，删除裸 `jsonify` 不一致形态。
- [ ] **1.2 抽取业务逻辑到 `services/`**：新建 `services/ai_sim.py`、`services/export.py`、`services/products.py`、`services/report.py`（auth 用户操作下沉 `services/users.py`）。路由退化为：校验入参 → 调 service → 返响应。
- [ ] **1.3 租户隔离**：所有查询按 `request.current_user.tenant_id` 过滤；移除 `auth.py:194` 硬编码默认租户（注册场景保留、运行期查询移除）；外键 `tenant_id` 列加索引（`CODE_STYLE` #1）；避免 N+1（用 `joinedload`/`selectinload`）。
- [ ] **1.4 列表分页**：列表类接口用 `paginated_response`（page/page_size/total）。
- [ ] **1.5 迁移后回归**：每个路由迁移保留/补充阶段 0.2 测试并全部通过。

**P2-2 验收**：`routes/` 无裸 `db.session` 业务逻辑；响应格式 100% 统一；租户隔离 + 索引 + 分页齐备；`pytest` 通过。

---

## 3. 执行顺序与估算（人日）

| 顺序 | 任务 | 所属 | 估算 | 依赖 |
|------|------|------|------|------|
| 1 | 前端 vitest 基建 + 0.2/0.3 单测 | P2-1 | 0.5d | — |
| 2 | EpcPage 表征测试 0.4 | P2-1 | 0.5d | 1 |
| 3 | useEpcModules.js + 9 子组件 + 图表组件 | P2-1 | 2.5d | 2 |
| 4 | 删重复 / 样式治理 / 接 api.js | P2-1 | 1d | 3 |
| 5 | 后端 pytest 基建 + conftest | P2-2 | 0.5d | — |
| 6 | 五路由接口测试 | P2-2 | 1.5d | 5 |
| 7 | service 抽取 + 统一响应 + 租户隔离 + 分页 | P2-2 | 3d | 6 |
| **合计** | | | **~10d** | |

> 建议顺序：P2-1 与 P2-2 的“阶段 0 测试”可并行启动；拆分/抽取（阶段 1）各自在测试守护下进行。

## 4. 风险与缓解
- **重复文件 source of truth 误判**：1.1 先确认 `EpcPage` 为路由入口再删 `EpcModules`，避免误删线上组件。
- **service 抽取行为漂移**：P2-2 阶段 0.2 测试在抽取前覆盖关键路径，保证等价。
- **租户隔离遗漏**：1.3 以“每个查询必须带 `tenant_id` 过滤”为代码评审硬性检查项。

## 5. 总验收清单
- [ ] 前端 `npm run lint` + `npm run test` 通过，覆盖率 ≥ 70%
- [ ] 后端 `pytest` 通过，覆盖率 ≥ 70%
- [ ] 所有 EPC 组件 ≤ 400 行，无内联 `style`
- [ ] 后端 5 路由响应 100% 统一（无裸 `jsonify`）
- [ ] 后端租户隔离 + `tenant_id` 索引 + 列表分页齐备
- [ ] `EpcModules.vue` 重复已消除
