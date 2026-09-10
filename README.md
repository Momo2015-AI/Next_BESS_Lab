# Next_BESS_Lab — 储能项目设计·开发·评估一体化平台

> 面向 BESS（Battery Energy Storage System，电池储能系统）的全生命周期技术经济仿真平台。
> 覆盖项目立项、方案设计、性能仿真、经济评估、成果交付五大阶段，为开发商、方案工程师、EPC 承包商、财务分析师提供同一套数据底座上的协作工具链。

---

## 目录

- [平台定位](#平台定位)
- [核心特性](#核心特性)
- [系统架构](#系统架构)
- [功能矩阵](#功能矩阵)
- [角色与权限](#角色与权限)
- [开发思路](#开发思路)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [文档索引](#文档索引)
- [质量与规范](#质量与规范)
- [贡献指南](#贡献指南)

---

## 平台定位

储能项目从立项到交付涉及多专业协作：开发商关心投资回报，方案工程师关心系统设计，EPC 承包商关心工程合规，财务分析师关心现金流与融资结构。传统工作流中各角色使用割裂的表格与脚本，数据难以贯通，方案比选依赖人工。

Next_BESS_Lab 将整条链路产品化为一个平台：

| 传统方式 | Next_BESS_Lab |
|----------|---------------|
| Excel 手工测算退化曲线 | 阿伦尼乌斯模型 + 厂家校准参数自动生成 26 年 SOH/RTE 曲线 |
| 方案比选依赖经验 | 设计引擎按策略生成多方案，编排器按目标函数自动排序 |
| 财务模型与设计脱节 | CAPEX/OPEX 从设计方案自动估算，财务引擎联动仿真结果 |
| 各角色数据割裂 | 统一数据模型 + RBAC 角色视图，全流程同源数据 |

---

## 核心特性

### 三引擎编排

平台核心计算能力由三个引擎承载，编排器（Orchestrator）串联为端到端工作流：

```
Survey 调研参数
    │
    ▼
Design Engine ──→ 多策略设计方案（经济优先 / 均衡 / 灵活分期 / 厂商导向）
    │
    ▼
Simulation Engine ──→ 26 年 SOH/RTE/DOD 退化曲线 + 补容策略对比
    │
    ▼
Financial Engine ──→ NPV / IRR / LCOS / DSCR / 投资回收期 + 敏感性分析
    │
    ▼
Orchestrator ──→ 方案对比 + 排序推荐 + 版本管理
```

### 退化与能量核算

- **阿伦尼乌斯衰减模型**：日历老化与循环老化双机制，覆盖温度、DOD、C-rate、循环次数多因素影响
- **厂家校准参数库**：内置 CATL、BYD 等主流厂家标定参数，含 RMSE 精度指标
- **能量会计矩阵**：26 年逐年核算可用电量、辅助功耗、补容量，支持手动辅耗与热模型辅耗双模式
- **补容策略对比**：固定周期 / 按需补容 / 超配方案，补容 CAPEX 按 Wright 学习率 5%/年递减

### AI 增强能力

- **参数校准**：`train_model.py` 支持从 CSV 导入实测数据，贝叶斯优化自动校准模型参数
- **PINN 物理信息神经网络**：实验性 SOH 预测模型（TensorFlow）
- **强化学习策略优化**：DQN 代理用于充放电策略优化实验

### 工程交付

- **EPC 模块族**：电气（HV）、热管理、消防、SCADA、并网合规、架构设计、投标报价、IPP 财务模型
- **BOQ 工程量清单**：分区种子 + 在线编辑
- **报告与导出**：调研表、仿真结果、财务报表多格式导出（Excel / PDF）

---

## 系统架构

### 总体架构

```
┌────────────────────────────────────────────────────────────┐
│                     前端 Vue 3 + Vite                       │
│  5 阶段页面 │ 工具箱 │ EPC │ 编排器 │ 管理面板               │
│  Pinia 单一数据源 │ ECharts │ vue-i18n (中/英/阿)            │
└──────────────────────────┬─────────────────────────────────┘
                           │ REST API (/api)
┌──────────────────────────▼─────────────────────────────────┐
│                     后端 Flask 3                            │
│  routes/     ~25 个 Blueprint，统一响应格式，JWT 认证        │
│  services/   三引擎 + 编排器 + 管线 + EPC 模块族             │
│  models/     SQLAlchemy ORM，多租户隔离                     │
│  algorithms/ 强化学习策略优化（实验）                        │
└──────────────────────────┬─────────────────────────────────┘
                           │ SQLAlchemy
┌──────────────────────────▼─────────────────────────────────┐
│              SQLite (soh_sim.db) / 多租户模型                │
└────────────────────────────────────────────────────────────┘
```

### 后端分层

| 层级 | 目录 | 职责 |
|------|------|------|
| 路由层 | `routes/` | Blueprint 定义 REST 端点，参数校验，JWT 鉴权，统一响应 `{ success, data, error, message }` |
| 服务层 | `services/` | 业务逻辑。三引擎继承 `BaseEngine`，通过 `engine_bus` 总线协作，`orchestrator` 负责端到端编排 |
| 数据层 | `models/` | SQLAlchemy 模型，显式定义 `to_dict()`，外键带索引 |
| 算法层 | `algorithms/` | 实验性算法模块（强化学习充放电策略） |

### 引擎协作机制

- **BaseEngine 契约**：所有引擎实现 `validate_input()` 与 `run()` 统一接口
- **DesignEngine**：约束求解 + 产品匹配 + 拓扑生成，从产品库（电芯 → Pack → Rack → 集装箱 → PCS）自动匹配生成 3-5 个候选方案
- **SimulationEngine**：核心管线由 `services/simulation/engine.py` 承载，`pipeline.py` 保留为向后兼容代理
- **FinancialEngine**：CAPEX/OPEX 自动估算、收入模型按项目地点自动选择、融资与税收默认结构、敏感性分析
- **Orchestrator**：验证输入 → 生成方案 → 串行执行仿真+财务 → 按目标指标（LCOS/IRR/NPV/CAPEX）排序 → 可选落库为 `ProjectVersion`

### 前端架构

- **单一数据源**：`stores/bess.js` 集中定义全系统默认参数（`DEFAULT_SURVEY`、`DEFAULT_SYSTEM_PARAMS`），所有组件引用同一 canonical 值，改一处即全局联动
- **物理量互推**：时长、倍率、需量电量从额定能量/功率自动推导，避免各表单独立填写造成不一致
- **组合式函数**：`useChart`、`useFinancialModel`、`useSensitivityCharts` 等 15+ composables 承载可复用逻辑
- **权限路由守卫**：`router/index.js` 基于 `sessionStorage` 中的用户权限做三级视图控制（full / readonly / hidden）

### 技术栈

| 层级 | 技术 |
|------|------|
| 前端框架 | Vue 3.5 + Vite 8 + Pinia 3 |
| UI | Tailwind CSS 4（玻璃态设计系统，亮/暗双主题） |
| 图表 | ECharts 6（按需引入）+ Plotly |
| 国际化 | vue-i18n 11（中 / 英 / 阿，RTL 支持） |
| 后端框架 | Flask 3 + SQLAlchemy |
| 科学计算 | NumPy + SciPy + Pandas |
| AI | TensorFlow（PINN / DQN 实验模块） |
| 认证 | JWT Bearer Token + Flask-Limiter 速率限制 |
| 测试 | Vitest（前端）+ Pytest（后端） |
| 质量 | ESLint + Prettier + Black + isort + Flake8 + Husky |

---

## 功能矩阵

### 五大业务阶段

| 阶段 | 页面 | 能力 |
|------|------|------|
| Phase 1 立项 | 调研表、运行工况 | 项目信息录入、环境条件、需量确认、文件上传 |
| Phase 2 设计 | 系统设计、电池/PCS 配置、产品库 | 电芯到集装箱的层级设计、产品选型与配对 |
| Phase 3 性能分析 | 仿真实验室、SOH 图表、矩阵表 | 26 年退化仿真、效率链、热力图、数据注入 |
| Phase 4 经济评估 | 财务看板、敏感性分析 | NPV/IRR/LCOS、现金流表、成本瀑布图、多币种 |
| Phase 5 成果输出 | 报告、方案对比 | 报告生成、多方案雷达图对比、版本回溯 |

### 工具箱

算法公式实验舱、参数面板、辅耗计算器、工程计算器、数据注入、校正因子模板、配置规则、历史项目、快速配置器。

### 一键编排

从调研参数直达推荐方案：设计引擎生成多策略候选 → 仿真+财务全量计算 → 按目标指标排序 → 结果可保存为项目版本，支持多版本指标差异对比与一键回溯。

### EPC 模块族

高压电气（HV）、热管理、消防安全、SCADA、并网合规、架构设计、投标报价（Bid）、IPP 财务模型、SCADA 监控。

---

## 角色与权限

### 角色体系

平台内置 6 种业务角色，对应储能项目的真实协作链条：

| 角色 | 标识 | 核心职责 | 高频模块 |
|------|------|----------|----------|
| 项目开发商 | `developer` | 项目立项、经济评估、投资决策 | Phase 1 / Phase 4 / 编排器 / IPP 模型 |
| 方案工程师 | `solution_engineer` | 系统设计、产品选型、仿真分析 | Phase 2 / Phase 3 / 仿真实验室 / 公式实验舱 |
| EPC 承包商 | `epc_contractor` | 工程设计、安全合规、施工交付 | EPC 模块族 / BOQ / 并网合规 |
| 财务分析师 | `financial_analyst` | 财务建模、CAPEX/OPEX、IPP 报价 | 财务看板 / 敏感性分析 / IPP 模型 |
| 项目经理 | `project_manager` | 全流程管理、报告归档、项目协调 | 全阶段视图 / 报告 / 历史项目 |
| 系统管理员 | `admin` | 用户管理、系统配置、跨租户管理 | 管理面板 / 用户与角色管理 |

### 权限模型

- **三级权限**：每个功能模块对每个角色为 `full`（可编辑）/ `readonly`（只读）/ `hidden`（不可见）
- **权限点覆盖**：5 个阶段 + 12 个核心工具 + 8 个高级工具 + EPC + 引擎 + 管理面板，共 24 个权限点
- **动态覆盖**：管理员可对角色或特定用户进行权限覆盖，支持设置失效时间，过期后自动恢复默认
- **多租户隔离**：数据模型原生支持租户（Tenant），用户、项目、方案数据按租户隔离
- **前端守卫**：路由级权限拦截，无权限路由自动重定向；菜单按权限动态渲染

---

## 开发思路

### 1. 引擎化与契约优先

所有计算能力收敛为继承 `BaseEngine` 的引擎，统一 `validate_input() / run()` 契约。新增引擎只需实现接口并注册到编排器，编排流程与方案排序逻辑零改动。计算核心（`services/simulation/engine.py`）与兼容层（`pipeline.py`）分离，接口演进有退路。

### 2. 单一数据源与物理一致性

前端所有默认参数集中于 Pinia store，组件禁止写死字面量。物理上互相关联的量（能量-功率-时长-倍率-需量）通过推导函数互算，保证任意入口修改后全局自洽。后端同理：DB 为空时回退 JSON 产品库，DB 优先、JSON 兜底，两套来源字段映射对齐。

### 3. 规范驱动的人机协作

本项目面向人类与 AI 协作开发：

- `CODE_STYLE.md`（RFC 2119 语义，MUST/SHOULD/MAY）为唯一规范权威
- `.cursorrules` 为 AI 编码规则权威源，通过 `scripts/sync-ai-rules.js` 自动同步到 `AGENTS.md` 与 `.continue/continue.yaml`，并配套 `check-ai-rules-consistency.js` 一致性校验
- Husky + lint-staged 在提交时强制执行规范
- CI 三条流水线（前端 / 后端 / 规则一致性）机器把关

### 4. 计算可信与可追溯

- 退化模型基于公开的电化学理论（阿伦尼乌斯方程），算法文档 `docs/Algorithm-Design.md` 完整推导公式
- 厂家参数携带 RMSE 与数据点数量，模型精度可评估
- `train_model.py` 支持实测数据校准，模型参数可保存/加载/复现
- 26 年参数矩阵支持高级用户手动覆写，透明可干预

### 5. 工程健壮性

- 统一响应格式与全局错误处理器（400/401/403/404/405/429/500）
- JWT 密钥缺失时生产环境拒绝启动（fail-fast）
- 种子用户密码随机生成，避免默认弱口令
- 列表查询强制分页，外键强制索引，批量写操作强制事务
- 速率限制保护认证端点

### 6. 渐进式国际化与可访问性

所有用户文本强制走 `$t()`，配套 `scripts/check-i18n.js` 覆盖率检查；三语（中/英/阿）含 RTL 适配；亮/暗双主题通过 CSS 自定义属性实现，`data-theme` 切换。

---

## 快速开始

### 环境要求

- Node.js >= 20
- Python >= 3.10

### 后端

```bash
# 必须设置 JWT 密钥，否则拒绝启动
export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

cd soh-sim-backend
pip install -r requirements.txt
python app.py
# 默认监听 http://localhost:5000
```

### 前端

```bash
cd soh-sim-frontend
npm install
npm run dev
# 默认监听 http://localhost:5173，/api 已代理到后端
```

### 运行测试

```bash
# 后端
cd soh-sim-backend
SECRET_KEY=test pytest

# 前端
cd soh-sim-frontend
npm run test
```

### 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `SECRET_KEY` | 是 | JWT 签名密钥，缺失时后端拒绝启动 |
| `CORS_ORIGINS` | 否 | 允许的跨域来源，逗号分隔 |
| `TEST_DATABASE_URI` | 否 | 测试数据库连接，默认 SQLite 内存库 |
| `VITE_BACKEND_PORT` | 否 | 前端代理目标端口，默认 5000 |

---

## 项目结构

```
Next_BESS_Lab/
├── soh-sim-frontend/          # Vue 3 + Vite 前端
│   └── src/
│       ├── pages/             # 25 个业务页面（5 阶段 + 工具箱 + EPC + 编排器）
│       ├── components/        # 70+ 业务组件
│       ├── composables/       # 15+ 组合式函数
│       ├── stores/            # Pinia 单一数据源
│       ├── services/          # API 客户端
│       ├── i18n/              # 中/英/阿语言包
│       └── router/            # 路由与权限守卫
├── soh-sim-backend/           # Python + Flask 后端
│   ├── routes/                # ~25 个 Blueprint（含 routes/epc/ 子模块族）
│   ├── services/              # 三引擎 + 编排器 + 管线 + EPC 服务
│   │   ├── design/            # 设计引擎
│   │   ├── simulation/        # 仿真引擎
│   │   └── financial/         # 财务引擎
│   ├── models/                # SQLAlchemy 数据模型（含 RBAC）
│   ├── algorithms/            # 强化学习策略优化（实验）
│   ├── pinn_model.py          # PINN 物理信息神经网络
│   ├── train_model.py         # 参数校准 CLI 工具
│   └── tests/                 # Pytest 测试
├── docs/                      # SRS、算法设计、数据库结构、API 规范
├── scripts/                   # 规范检查与 AI 规则同步脚本
├── .templates/                # 前端/后端代码模板
├── CODE_STYLE.md              # 代码规范（RFC 2119）
└── CONTRIBUTING.md            # 贡献指南
```

---

## 文档索引

| 文档 | 内容 |
|------|------|
| [docs/SRS.md](./docs/SRS.md) | 软件需求规格说明书 |
| [docs/Algorithm-Design.md](./docs/Algorithm-Design.md) | 阿伦尼乌斯衰减模型算法推导 |
| [docs/Database-Structure.md](./docs/Database-Structure.md) | 数据库与数据模型 |
| [docs/API-Specification.yaml](./docs/API-Specification.yaml) | API 规范 |
| [docs/test-plan-3engines.md](./docs/test-plan-3engines.md) | 三引擎测试计划 |
| [CODE_STYLE.md](./CODE_STYLE.md) | 代码规范手册 |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | 贡献指南与提交规范 |

---

## 质量与规范

### 提交前检查

```bash
# 全局检查（前端 lint + 后端 black/flake8 + i18n 覆盖率）
bash scripts/check-code-style.sh
```

### CI 流水线

`.github/workflows/ci.yml` 包含三个 job：

- **frontend**：Prettier 格式化 → ESLint → TypeScript 检查 → Vitest
- **backend**：Black → isort → Flake8 → Pytest
- **rules-consistency**：校验 `.cursorrules` 与 `AGENTS.md`、`.continue/continue.yaml` 同步一致

### 关键工程约束

- 组件行数软限制 400 行（超限需评审），逻辑优先抽离到 composable
- 所有文本 `$t()` 国际化，无硬编码文案
- ECharts 按需引入，实例与监听器在 `onUnmounted` 清理
- deep watch 强制防抖，输入计算防抖 300ms+
- 后端禁 N+1 查询，列表强制分页，批量写强制事务

---

## 贡献指南

提交使用 Conventional Commits 格式：`<type>(<scope>): <subject>`，type 取值 `feat | fix | chore | refactor | docs | style | test | perf`。

分支模型：`main`（生产）/ `develop`（开发）/ `feature/*` / `fix/*`。

所有开发者（人类与 AI）必须遵守 [CODE_STYLE.md](./CODE_STYLE.md)，AI 工具规则以 `.cursorrules` 为权威源。
