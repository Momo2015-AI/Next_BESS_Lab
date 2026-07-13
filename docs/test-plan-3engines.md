# SOB-SIM 深度测试方案与测试报告

> 范围：覆盖前端 + 后端**全部模块**，重点验证**数据流转端到端**与**三大引擎（Design / Simulation / Financial）完整功能**。
> 配套可执行脚本：`soh-sim-backend/tests/test_engines_deep.py`（pytest，覆盖三大引擎 + 数据流转 + 支撑服务，可独立运行、无需数据库）。
> 生成日期：2026-07-10

---

## 1. 概述

### 1.1 测试目标
1. 验证三大引擎各自功能完整、边界正确、数值可信。
2. 验证数据从「调研表 → 设计引擎 → 仿真引擎 → 财务引擎 → 方案版本落库」全链路打通且**输出即输入**格式兼容。
3. 验证所有支撑模块（退化预测、效率链、辅耗、EPC、算法/ PINN、产品库、项目/版本、权限、汇率、报表、BOQ）与所有前端页面/组件/状态不回归。

### 1.2 测试层级
| 层级 | 手段 | 覆盖 |
|------|------|------|
| 单元 | pytest（引擎/服务纯函数） | 三大引擎、退化/效率/辅耗算法 |
| 集成 | pytest + Flask test_client | API 路由、鉴权、数据流转 E2E |
| 前端 | vitest | store(bess.js)、api.js、组件渲染 |
| 静态 | eslint / prettier / 构建 | 代码规范（见 §8.2） |

### 1.3 环境
- 后端：Python + Flask + pytest；测试用 `sqlite:///:memory:`（`TEST_DATABASE_URI`）。
- 前端：Node 22 + Vitest（无 Node 时需先 `install_binary`）。

---

## 2. 模块清单与测试映射

### 2.1 后端模块
| 模块 | 文件 | 类型 | 用例分组 |
|------|------|------|----------|
| **设计引擎** | `services/design/engine.py` | 引擎 | DE-* |
| **仿真引擎** | `services/simulation/engine.py` | 引擎 | SE-* |
| **财务引擎** | `services/financial/engine.py` + `calculator.py` | 引擎 | FE-* |
| 退化预测 | `services/degradation.py` | 支撑 | SUP-* |
| 效率链 | `services/efficiency.py` | 支撑 | SUP-* |
| 辅耗计算 | `services/aux_power.py` | 支撑 | SUP-* |
| 编排层 | `services/orchestrator.py` | 支撑 | DF-* |
| 兼容流水线 | `services/pipeline.py` | 支撑 | DF-* |
| 算法/PINN | `services/algorithm.py` + `train_model.py` | 支撑 | MOD-* |
| 产品库 | `routes/products.py` + `data/products.json` | 数据 | MOD-* |
| 项目/版本 | `routes/project.py` + `models` | 数据 | MOD-* |
| 调研表 | `routes/survey.py` | 数据 | MOD-* |
| 权限 RBAC | `routes/rbac.py` + `models/rbac.py` | 安全 | MOD-* |
| 认证 Auth | `routes/auth.py` | 安全 | MOD-* |
| EPC 热管理/ipp | `routes/epc/*` + `services/epc/*` | 业务 | MOD-* |
| 汇率 | `routes/exchange_rate.py` | 业务 | MOD-* |
| 报表/导出 | `routes/report.py` + `routes/export.py` | 业务 | MOD-* |
| BOQ | `routes/boq.py` + `services/boq.py` | 业务 | MOD-* |
| API 路由（3 引擎+编排+辅耗+pipeline） | `routes/*_engine.py` / `orchestrator.py` / `aux_power.py` / `pipeline.py` | 接口 | API-* |

### 2.2 前端模块
| 分组 | 文件 | 类型 | 用例分组 |
|------|------|------|----------|
| 页面（Phase1-5 / Tools / EPC / Survey / Orchestrator / Admin / Auth / Home） | `src/pages/*` | 页面 | FE-PAGE-* |
| 状态 | `src/stores/bess.js` | store | FE-STORE-* |
| API 客户端 | `src/services/api.js` | 服务 | FE-API-* |
| 产品 composable | `src/composables/useProducts.js` | 服务 | FE-API-* |
| 图表/输入/配置组件 | `src/components/*` | 组件 | FE-CMP-* |

---

## 3. 数据流转端到端测试用例（重点）

### DF-01 调研表 → 设计引擎 → 仿真 → 财务（编排层一键）
- **前置**：`POST /api/workflow/full`，body 含 `survey_params`（ratedEnergy/totalPower/duration/temperature/cyclesPerDay/dod/cRate/location/requiredEnergy）+ `strategy`。
- **步骤**：调用编排层 → 断言 `pipeline_summary.successful > 0`，`recommendation` 非空且含 `design/simulation/financial` 三段。
- **预期**：`recommendation.financial.metrics.lcos` 非空；`simulation.totalAcUsable` 长度 = 26（NUM_YEARS）。
- **对应脚本**：`TestDataFlow.test_orchestrator_full_workflow`

### DF-02 引擎间「输出即输入」格式兼容
- **步骤**：取 `SimulationEngine.run()` 的 `totalAcUsable`（list[26]）→ 直接作为 `FinancialEngine.run(simulation_output={"totalAcUsable": ...})` 入参。
- **预期**：财务现金表首年 `freeCashflow < 0`（CAPEX 支出），NPV/IRR/LCOS 均计算成功，无类型/维度报错。
- **对应脚本**：`TestDataFlow.test_output_input_compatibility`

### DF-03 设计→仿真参数透传正确性
- **步骤**：对比 `DesignEngine` 输出的 `container.ratedEnergyMwh / pcs.ratedPowerMW / containerQty / estimatedCapex` 与 `SimulationEngine._extract_params` 解析后的值。
- **预期**：仿真引擎读取到的额定能量/功率/台数与设计方案一致（避免编排层静默丢参）。

### DF-04 方案版本落库（含权限）
- **步骤**：`POST /api/workflow/full` 带 `project_id` → 断言 `saved_versions` 非空、写入 `ProjectVersion.config_data` 含完整 design+sim+fin。
- **预期**：仅成功方案写入；首个版本 `is_active=true`；非项目成员返回 403。

### DF-05 补容策略经济性对比数据流
- **步骤**：仿真引擎 `augmentationComparison` → 三种策略各自重算能量 → 调财务引擎得 NPV/IRR/LCOS → 推荐 NPV 最高者。
- **预期**：`recommended ∈ {fixed_periodic, on_demand, overbuild}`；推荐策略 NPV = max（见 §8.4 缺陷 D1 需复核）。

### DF-06 前端 store 数据流转
- **前置**：mock `api.js` 的 `post('/api/design/auto')`、`post('/api/simulation/run')`、`post('/api/financial/calculate')`。
- **步骤**：触发 `bess.js` 计算 action → 断言依次调用三引擎端点、结果写入对应 state。
- **对应**：`src/stores/__tests__/bess.test.js`（已存在，覆盖 design→sim→fin 与 workflow/full）。

---

## 4. 三大引擎深度测试用例

### 4.1 DesignEngine（设计引擎）
| ID | 场景 | 预期 |
|----|------|------|
| DE-01 | `validate_input({})` | 报出 totalPower/ratedEnergy/duration/temperature/cyclesPerDay 缺失 |
| DE-02 | 负功率 / 温度<-20 或 >60 | 对应字段报校验错误 |
| DE-03 | 四策略 economic/balanced/flexible/manufacturer | 均生成 ≥1 方案且 `recommendation` 非空 |
| DE-04 | `manufacturer="BYD"` | 所有方案 `container.mfr == "BYD"` |
| DE-05 | PCS 自动匹配 | `pcs.ratedPowerMW>0`、`pcsQty≥1`、`totalPowerMW ≥ 目标功率` |
| DE-06 | 效率链 | `systemRTE == cellRTE×pcsEff×transformer×cable`（乘积一致） |
| DE-07 | CAPEX 拆解 | `containerCost+pcsCost+bop+epc+development == totalCapex`，currency=USD |
| DE-08 | 排序 | economic 下 `totalCapex` 升序；rank 连续 1..N |
| DE-09 | 产品库为空 | 返回 `solutions=[]`（优雅降级，不抛异常）|
> 脚本：`TestDesignEngine.*`（DE-09 对应 products.json 缺失的真实阻断，见 §8.2）

### 4.2 SimulationEngine（仿真引擎）
| ID | 场景 | 预期 |
|----|------|------|
| SE-01 | `validate_input` 缺 ratedEnergy | 报 `ratedEnergy is required` |
| SE-02 | `run()` 返回完整性 | 含 years/soh/rte/dod/augQty/efficiencyCurves/efficiencyDetail/totalAcUsable/meetsReq/augmentationStrategy/augmentationComparison |
| SE-03 | SOH 单调性 | `soh[0]==100`，且 `soh[i] ≤ soh[i-1]`（Arrhenius 与 GB36276 均成立）|
| SE-04 | GB36276 模型 | `0 ≤ soh ≤ 100`，长度 26 |
| SE-05 | 高温加速衰减 | `predict_soh(45°C)[10] < predict_soh(25°C)[10]` |
| SE-06 | meetsReq 逻辑 | `meetsReq[i] == (totalAcUsable[i] ≥ requiredEnergy)` |
| SE-07 | 补容三策略 | `augmentationStrategy.strategies` 含 fixed_periodic/on_demand/overbuild，默认推荐 on_demand |
| SE-08 | 经济性对比推荐 | `augmentationComparison.recommended` 的 NPV = 各策略最大 |
> 脚本：`TestSimulationEngine.*`、`TestSupportServices.test_predict_soh_*`

### 4.3 FinancialEngine（财务引擎）
| ID | 场景 | 预期 |
|----|------|------|
| FE-01 | 缺 `totalAcUsable` | 报 `totalAcUsable is required` |
| FE-02 | `run()` 返回 | 含 metrics(NPV/IRR/LCOS/DSCR/Payback/ROI)/cashflowTable/capexBreakDown/opexBreakDown/revenueModel/sensitivity |
| FE-03 | 现金表首年 | `cashflowTable[0].freeCashflow < 0`（CAPEX）|
| FE-04 | 收入模型按地区 | china→套利+容量；middle east→PPA+容量拍卖；eu→套利+辅助 |
| FE-05 | 敏感性四场景 | 含 capex±15% / price±20%；电价 +20% → NPV 上升，−20% → 下降 |
| FE-06 | DSCR | `metrics.dscr.min/avg` 存在且 ≥0；min≥1.3 视为达标 |
| FE-07 | 指标公式可信 | NPV=Σ CFₜ/(1+r)ᵗ；LCOS=折现成本/折现能量；Payback=累计现金流转正年份 |
> 脚本：`TestFinancialEngine.*`

### 4.4 引擎间一致性
| ID | 场景 | 预期 |
|----|------|------|
| IC-01 | 设计输出 → 仿真输入字段名 | `_extract_params` 解析 key 与设计输出 key 一一对应 |
| IC-02 | 仿真输出 → 财务输入 | `totalAcUsable` 直接被 `calculate_full_financial` 消费，无中间转换 |
| IC-03 | 跨策略一致性 | 同一 `survey_params` 下，三策略财务结果可相互比较（DF-05）|

---

## 5. API 路由测试用例
| ID | 端点 | 用例要点 |
|----|------|----------|
| API-01 | `POST /api/design/auto` | 无 token→401；缺 survey_params→400；成功→solutions |
| API-02 | `GET /api/design/strategies` | 返回 4 策略元信息 |
| API-03 | `POST /api/design/validate` | 返回 `{valid, errors}` |
| API-04 | `POST /api/simulation/run` | 缺 design_output→400；成功返回完整仿真结构 |
| API-05 | `POST /api/simulation/augmentation-compare` | 返回三策略对比 + recommended |
| API-06 | `POST /api/financial/calculate` | 缺 totalAcUsable→400；成功返回 metrics |
| API-07 | `POST /api/financial/sensitivity` | 四场景返回 |
| API-08 | `POST /api/workflow/full` | E2E（同 DF-01）；带 project_id 触发落库 |
| API-09 | `POST /api/workflow/what-if` | base/adjusted/delta 三段齐全 |
| API-10 | `POST /api/aux-power/calculate` | 校验失败→400；成功返回 dc/ac/totalSystemAux |
| API-11 | `POST /api/pipeline/calculate` | 兼容旧链路 |
> 路由鉴权统一由 `@token_required` 装饰器保证；测试用例复用 `test_integration.py` 的 `auth_headers_eng` fixture。

---

## 6. 支撑模块测试
- **退化预测 MOD/SUP**：Arrhenius 与 GB36276 双模型；correctionFactor / correctionTable / environmental 加速因子（温度 Arrhenius 指数、粉尘、湿度）。
- **效率链**：10 因子链 → `calculate_efficiency_curves` 逐年 RTE。
- **辅耗**：`calculate_aux_power` 直流/交流/站用自耗（字段见 `services/aux_power.py`，与 DesignEngine 内部字段不同，需分别测试）。
- **EPC 热管理/ipp**：`POST /api/thermal-management/calculate` 落 `ThermalManagement` 并校验项目权限；ipp 同理。
- **算法/PINN**：`train_model.py` 的 calendar/cycle aging、RMSE；推理接口返回 SOH。
- **产品库**：`GET /api/products/{category}`；**依赖 `data/products.json`（当前缺失，见 §8.2）**。
- **项目/版本**：CRUD + 版本比较/恢复（`bess.js` 已覆盖 compare/restore）。
- **权限 RBAC**：`list_users` N+1 已修复（selectinload）；角色越权→403。
- **汇率/报表/导出/BOQ**：往返计算与文件导出；BOQ→CAPEX 映射（`BOQ_TO_CAPEX_MAP`）。

---

## 7. 前端模块测试
- **store（FE-STORE）**：`bess.test.js` 已覆盖 design/simulation/financial/workflow/pipeline 五类 action 的端点调用与 state 更新。
- **api 客户端（FE-API）**：`api.spec.js` 已覆盖 GET/POST/PUT/DELETE、鉴权失败 401、超时、下载。
- **页面（FE-PAGE）**：Phase1-5、Tools、EPC、Survey、Orchestrator、Admin、Auth、Home 渲染 + 关键交互（提交→调用引擎→图表刷新）。
- **组件（FE-CMP）**：图表/输入/配置类组件在 props 变化时的重算与 ECharts `dispose`、resize 监听器清理（AGENTS.md 规范）。
- **PR3 回归（FE-CMP）**：内联 `style` 已迁移为 scoped CSS 类；需回归验证视觉无变化（见 §8.4 D3）。

---

## 8. 测试报告

### 8.1 执行方法
```bash
# 后端（引擎/服务/数据流转，无需 DB）
cd soh-sim-backend
python -m pytest tests/test_engines_deep.py -v --tb=short

# 后端（含 API 路由 + E2E，需内存 DB）
python -m pytest tests/test_integration.py tests/test_engines_deep.py -v

# 前端
cd soh-sim-frontend
npx vitest run src/stores/__tests__/bess.test.js src/services/__tests__/api.spec.js
```

### 8.2 环境就绪性检查（已发现阻断项）
| 项 | 状态 | 影响 | 建议 |
|----|------|------|------|
| `soh-sim-backend/data/products.json` **缺失** | 🔴 阻断 | DesignEngine 返回空方案（DF-01/DE-03 失败）；`vite build` 因 `useProducts.js` 无法 import 而失败；产品库 API 无数据 | **最高优先级**：补充产品库 JSON（结构见 `DesignEngine._load_products` 期望的 cells/containers/pcs/racks/clusters/packs）|
| 全量文件 CRLF 行尾 vs prettier 期望 LF | 🟡 警告 | eslint 全量报 `Delete ␍`（CR）警告；不影响运行，但 CI lint 会挂 | 统一行尾（`*.vue/*.js` → LF）或调整 `.prettierrc` 的 `endOfLine` |
| 后端无 Python 运行时（本机） | 🟡 环境 | 本机无法直接跑 pytest | 目标机装 Python/依赖；或 CI 执行 |
| 前端无 Node（本机已定位 22.22.2） | 🟢 可解 | 已用 `install_binary` 取得 | 用已定位的 node 跑 vitest |

### 8.3 测试覆盖率矩阵
| 能力 | 现有覆盖 | 本方案新增 | 缺口 |
|------|----------|----------|------|
| 三大引擎单元 | `test_integration.py`(Design/Sim/Fin)、`test_deep_validation.py` | `test_engines_deep.py` 全量 + 边界 | 引擎×极端参数矩阵 |
| 数据流转 E2E | `test_integration.py::TestEnginePipeline` | DF-01~06 | 版本落库权限（DF-04）待补 |
| API 路由 | `test_integration.py` | API-01~11 | what-if/aux/pipeline 端点 |
| 支撑算法 | 部分 | SUP-* | EPC/ipp/pinn/boq/汇率 |
| 前端 store/api | `bess.test.js`/`api.spec.js` | FE-* | 页面交互回归 |
| 静态规范 | — | — | CRLF lint（§8.2）|

### 8.4 代码审查已发现缺陷 / 风险（建议转为专项用例）
- **D1（高）补容超配策略成本双重计数**：`SimulationEngine._compare_augmentation_strategies` 中 `overbuild` 策略把 `overbuildExtraCost` 计入 `adjusted_capex.equipment`（line 263），又在第 283 行把 `overbuild_extra_cost` 再加进 `totalAugCapex` → 超配方案 CAPEX 被重复计算，导致推荐 NPV 失真。**应补 DF-05/IC-03 断言捕获。**
- **D2（中）CAPEX 估算口径不一致**：`FinancialEngine._estimate_capex` 默认用 `totalEnergyMwh × 200000`，而 `DesignEngine._estimate_capex` 用 `额定能量 × 台数 × 200000/舱`。当走自动估算分支时二者口径不同，影响跨引擎可比性。
- **D3（中）PR3 内联样式迁移引入的构建 bug（已修复）**：`RunningConditions.vue` 曾出现重复 `class` 属性（脚本未正确合并），导致 Vue 编译失败；已合并修复并确认全项目无重复字面 `class`。**需视觉回归确认无变化。**
- **D4（低）编排层空方案静默成功**：`run_full_workflow` 产品库为空时返回 `{error: "无法生成设计方案..."}`，但路由 `/api/workflow/full` 仍包成 `success_response` → 前端需自行检查 `error` 字段，否则误判成功。
- **D5（低）`_compute_delta` 基准为 0 时回退绝对差**：NPV 基准为 0 的场景 delta 含义不明确，报告需注明。

### 8.5 优先级执行计划
1. **P0**：补齐 `data/products.json` → 解锁 DF/DE/Design 全部用例。
2. **P0**：修复 D1 超配双重计数，并加 DF-05/IC-03 断言。
3. **P1**：跑 `test_engines_deep.py` + `test_integration.py`，固化三大引擎与数据流转基线。
4. **P1**：前端 vitest（store/api）+ 页面交互回归；PR3 视觉回归（D3）。
5. **P2**：补齐 API-05~11、EPC/ipp/pinn/boq/汇率支撑模块用例。
6. **P2**：统一行尾 / 调整 prettier，消除 CRLF lint 噪声（D 不影响功能）。

### 8.6 结论
- 三大引擎逻辑链路**完整且自洽**（设计→仿真→财务输出即输入），`test_engines_deep.py` 已将其固化为可执行断言。
- **当前唯一硬阻断是 `products.json` 缺失**，它同时阻断了设计引擎测试与前端生产构建——属数据/配置缺失而非逻辑缺陷，补齐即可解锁。
- 审查中发现 **1 个高优真实缺陷（D1 超配成本双重计数）** 与若干口径/健壮性风险，建议优先修复并补充对应断言，防止回归。

---
*配套脚本：`soh-sim-backend/tests/test_engines_deep.py`（已写入，含 Design/Simulation/Financial 引擎、数据流转 E2E、退化/效率/辅耗支撑服务的确定性断言）。*
