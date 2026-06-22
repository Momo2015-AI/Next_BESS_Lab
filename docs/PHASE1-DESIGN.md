# BESS SOH 仿真系统 — 第一波设计与需求规格

> **文档状态**：Draft v0.1 · 待评审
> **范围**：第一波（单项目闭环：持久化 + 项目管理 + 报告导出）
> **编制日期**：2026-06-20
> **编制依据**：`.monkeycode/specs/soh-simulation/requirements.md`、现有代码、用户需求梳理文档

---

## 0. 文档目的

本文档是第一波迭代的 **SRS（软件需求规格）+ 技术设计** 合订本，供评审通过后作为开发依据。评审重点：

1. 范围边界是否正确（做什么、不做什么）
2. 数据模型是否覆盖业务实体
3. API 设计是否合理
4. 改动是否最小侵入现有代码

---

## 1. 背景与现状

> **文档更新记录（2026-06-21）**：同步远程 `6a69e47` 后重新评估。原 SRS 中部分已实现项标记为 ✅，不再重复规划。

### 1.1 系统当前状态

| 维度 | 现状 |
|------|------|
| 容量对账引擎 | ✅ 25 年容量矩阵 + 补容逻辑，前后端各一份等价实现 |
| 阿伦尼乌斯仿真 | ✅ `SimulationLab.vue` 已实现物理公式计算（Q_cal + Q_cyc），支持温度/循环/DOD/C-rate |
| 多算法选择 UI | ⚠️ 三种算法卡片（阿伦尼乌斯/经验/ML），但**只有阿伦尼乌斯真正实现**，经验/ML 是 UI 占位 |
| 串码ID加载调研表 | ⚠️ 前端 UI 已有（`SimulationLab.vue` 调用 `GET /api/survey/{id}`），但**后端无此接口**（会 404） |
| 校正因子 | ✅ `SimulationLab.vue` 支持全局校正系数 + 年度校正表 |
| 电池与PCS配对 | ✅ `BatteryPCSConfig.vue`（612行），含选型/数量/功率配比/连接图 |
| 财务引擎 | ✅ 前端有 IRR/NPV/LCOS/现金流/敏感性分析 |
| 产品库 | ✅ `products.json` 含 13 电芯 + 8 集装箱 + 14 PCS + 5 场景 |
| 文档解析 | ⚠️ 后端 `/api/upload/extract` 有 CSV/Excel/TXT/JSON/PDF 解析（PDF 解析粗糙） |
| Toast 提示 | ✅ `App.vue` 已有错误/成功/警告提示机制 |
| **App.vue bug** | ✅ **已修**（fetchCalculation 的 catch 块正确闭合） |
| **后端路径 bug** | ✅ **已修**（`os.path.join(tempfile.gettempdir(), ...)`，跨平台兼容） |
| **持久化** | ❌ 无数据库，所有数据在前端内存，刷新即丢 |
| **项目管理** | ❌ 无"项目"概念，调研表数据不绑定任何实体 |
| **报告导出** | ❌ 无 PDF/导出能力 |
| **仿真→容量打通** | ❌ SimulationLab 的 SOH 预测与 App.vue 的容量对账是两套割裂逻辑，互不调用 |

### 1.2 两套计算引擎的关系（重要）

```
SimulationLab (预测SOH曲线)          App.vue (容量对账)
    输入：温度/循环/DOD/电池类型        输入：SOH曲线/RTE曲线/DOD/补容
    输出：SOH%/年, RTE%/年             输出：25年容量表/达标判定
           │                                 │
           └──── 应该是上下游 ───────────────┘
                    （但目前割裂，未打通）
```

**第一波不合并它们**——只做持久化和报告导出。算法架构统一属于中长期任务。

### 1.2 第一波目标

把"一次性计算器"升级为**"能保存项目、能持久化、能导出技术报告+设备清单"的单项目闭环工具**。

---

## 2. 需求范围（Scope）

### 2.1 本期做什么（In Scope）

| ID | 需求 | 优先级 | 状态 |
|----|------|--------|------|
| FR-1 | 持久化层：引入 SQLite + SQLAlchemy，项目/调研/配置/结果/报告入库 | Must | ❌ 待做 |
| FR-2 | **调研表作为项目入口**：新建项目即填调研表（复用现有 `RunningConditions.vue`），数据入库绑定项目 | Must | ❌ 待做 |
| FR-3 | 项目管理：创建/列表/打开/删除项目，自动生成 UUID | Must | ❌ 待做 |
| FR-4 | 保存仿真：将当前 params + soh/rte/dod/augQty + 计算结果保存到指定项目 | Must | ❌ 待做 |
| FR-5 | 加载仿真：从数据库恢复某项目的完整配置与结果到前端 | Must | ❌ 待做 |
| FR-6 | 技术报告 PDF 导出（含系统配置 + 25 年容量表） | Must | ❌ 待做 |
| FR-7 | 设备清单 BOM PDF 导出（基于 products.json 的选型） | Must | ❌ 待做 |
| FR-8 | ~~修复 `App.vue` 的 `fetchCalculation` 语法 bug~~ | ~~Must~~ | ✅ **已完成**（`6a69e47`） |
| FR-9 | ~~修复后端 `UPLOAD_DIR` 硬编码路径~~ | ~~Must~~ | ✅ **已完成**（`6a69e47`） |
| FR-10 | 保留并接入调研表的"投标文件导入自动填充"功能（现有 `/api/upload/extract`），抽取结果可入库 | Must | ❌ 待做 |
| FR-11 | 后端新增 `GET /api/survey/{id}` 接口（前端 SimulationLab 已调用，后端缺失） | Must | ❌ 待做（补充） |

### 2.2 本期不做（Out of Scope）

明确划线，避免范围蔓延：

- ❌ 用户登录 / 注册 / 多租户（第二波，`tenant_id` 字段先预留）
- ❌ 付款 / 报告加密 / 解锁（第二波）
- ❌ 财务报告 PDF（用户明确本期不含；财务数据已算，仅不做 PDF 版本）
- ❌ **调研表客户外部链接填写**（第二波；本期仅工程师在系统内填写）
- ❌ 工程模块（占地/BOM 物料/人工/LTSA/甘特图，第三波）
- ❌ 电芯级阿伦尼乌斯化学仿真（第三波）
- ❌ 方案对比前端（第三波；后端 `calculate-multi` 已就绪）
- ❌ 微服务 / Redis / InfluxDB（架构原则：单体优先）

### 2.3 非功能需求

| 类别 | 要求 |
|------|------|
| 兼容性 | 后端必须兼容 Windows（当前开发机）与 Linux（未来部署） |
| 可维护性 | 后端从单文件 `app.py` 模块化拆分；前端 bug 修复 |
| 可迁移性 | 数据层用 SQLAlchemy ORM，切 PostgreSQL 仅改连接串 |
| 性能 | 仿真计算响应 ≤ 1s（现有水平保持）；报告生成 ≤ 5s |
| 向后兼容 | 现有 `/api/soh/calculate`、`/api/health`、`/api/upload/extract` 接口行为不变 |

---

## 3. 用例（Use Cases）

### UC-1：新建项目（填写调研表 = 项目入口）

- **参与者**：工程师（单用户，本期无鉴权）
- **前置条件**：前后端服务运行中
- **主事件流**：
  1. 用户在前端点击"新建项目" → 进入调研表页面（复用现有 `RunningConditions.vue`）
  2. 用户填写调研表（项目概况/环境选址/电网条件/电芯要求/PCS要求/认证/EPC），或点击"导入投标文件"自动抽取填充（FR-10）
  3. 用户点击"创建项目" → `POST /api/projects` 携带调研表数据
  4. 后端：生成 UUID → 建 project（name 取自调研表 projectName，status=draft）→ 建 survey（data_json 存全表）→ 返回项目对象
  5. 用户后续可继续编辑调研表 → `PUT /api/projects/{id}/survey` 更新
- **后置条件**：项目 + 调研数据持久化，项目进入 draft 状态

### UC-2：配置仿真并保存（主流程）

- **参与者**：工程师
- **前置条件**：项目已创建（UC-1）
- **主事件流**：
  1. 在项目中打开仿真页面（现有 Tab1~Tab3）
  2. 调研表中的关键工况字段（duration/cyclesPerDay/requiredEnergy 等）已自动映射到仿真参数（复用现有 `applyParams` 机制）
  3. 用户调整 params / soh / rte / dod / augQty，前端实时本地计算（现有行为不变）
  4. 用户点击"保存到项目" → `PUT /api/projects/{id}/simulation`，后端重算并存储配置 + 结果，项目 status 置为 active
- **后置条件**：仿真配置与结果持久化，刷新页面不丢失

### UC-3：打开历史项目

- **主事件流**：项目列表 → 选中 → `GET /api/projects/{id}` → 前端恢复 survey + params/soh/rte/dod/augQty/results
- **后置条件**：调研表与仿真页面状态完全还原

### UC-4：导出技术报告

- **主事件流**：打开项目 → 点击"导出技术报告" → `GET /api/projects/{id}/report?type=technical` → 浏览器下载 PDF
- **报告内容**：项目概览（含调研表关键信息）、系统配置参数、25 年容量衰减表（粗放电/辅耗/可用/达标）

### UC-5：导出设备清单（BOM）

- **主事件流**：打开项目 → 点击"导出设备清单" → `GET /api/projects/{id}/report?type=bom` → 下载 PDF
- **报告内容**：所选电芯/集装箱/PCS 的型号、厂家、关键参数、数量

---

## 4. 技术设计（Technical Design）

### 4.1 架构总览

```
┌──────────────────────────────────────────────────────┐
│            前端 Vue 3 + Vite（不变）                  │
│  App.vue（修 bug）+ 新增：项目列表/保存/导出按钮       │
└──────────────────────┬───────────────────────────────┘
                       │ HTTP /api
┌──────────────────────▼───────────────────────────────┐
│            后端 Flask（模块化重构）                    │
│  app.py（路由薄层）                                   │
│   ├─ routes/        项目/报告/仿真 路由               │
│   ├─ services/      业务逻辑（仿真/报告生成）          │
│   ├─ models.py      SQLAlchemy 数据模型               │
│   ├─ db.py          数据库连接与初始化                 │
│   └─ reports/       ReportLab 报告模板                │
└──────────────────────┬───────────────────────────────┘
                       │ SQLAlchemy ORM
┌──────────────────────▼───────────────────────────────┐
│            SQLite（单文件 bess.db）                    │
│  Project / Survey / SimulationConfig / Result / Report │
└──────────────────────────────────────────────────────┘
```

**设计原则**：
- **单体优先（Modular Monolith）**：一个 Flask 进程内按目录分模块，不拆服务
- **薄路由 + 厚 service**：`app.py`/`routes/` 只做参数校验和调用，业务逻辑在 `services/`
- **ORM 抽象**：所有 DB 访问经 SQLAlchemy，便于未来切 PostgreSQL

### 4.2 目录结构（改造后）

```
soh-sim-backend/
├── app.py                  # 应用工厂 + 路由注册（精简）
├── db.py                   # SQLAlchemy engine + session
├── models.py               # 5 张表的 ORM 模型
├── config.py               # 配置（DB路径、上传目录等）
├── requirements.txt        # 新增：sqlalchemy、reportlab
├── routes/
│   ├── __init__.py
│   ├── soh.py              # 现有 /api/soh/* 与 /api/health
│   ├── upload.py           # 现有 /api/upload/extract（修路径）
│   ├── projects.py         # 新增：项目 CRUD
│   └── reports.py          # 新增：报告导出
├── services/
│   ├── __init__.py
│   ├── simulation.py       # 从 app.py 抽出的 calculate()
│   └── report.py           # ReportLab 报告生成
└── instance/
    └── bess.db             # SQLite 数据库文件（gitignore）
```

### 4.3 数据模型

#### 表 1：projects

| 字段 | 类型 | 说明 |
|------|------|------|
| id | String(36) PK | UUID |
| name | String(200) | 项目名称（来自调研表 projectName） |
| status | String(20) | `draft`/`active`（draft=调研进行中，active=已进入仿真） |
| cell_model_id | String(50) NULL | 所选电芯（关联 products.json，仿真阶段填） |
| container_model_id | String(50) NULL | 所选集装箱（仿真阶段填） |
| pcs_model_id | String(50) NULL | 所选 PCS（仿真阶段填） |
| tenant_id | String(36) NULL | **预留**，第二波多租户启用 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

#### 表 2：surveys（调研表，项目入口）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | 自增 |
| project_id | String(36) FK→projects.id UNIQUE | 一对一绑定项目 |
| data_json | JSON | 完整调研表数据（RunningConditions.vue 的 form 全字段） |
| source | String(20) | `manual`（手填）/ `imported`（文件导入抽取）/ `mixed` |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

> `data_json` 直接存储 `RunningConditions.vue` 的 `form` 对象（项目概况/环境选址/电网条件/电芯要求/PCS要求/认证/EPC 等），避免把几十个字段拆成列。第二波做客户外部填表时，本表新增 `submitted_via`（internal/link）、`submit_token` 字段即可。

#### 表 3：simulation_configs

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | 自增 |
| project_id | String(36) FK→projects.id | 所属项目 |
| params_json | JSON | 全部 params（ratedEnergy 等 11 个字段） |
| soh_json | JSON | 长度 26 的 SOH 数组 |
| rte_json | JSON | 长度 26 的 RTE 数组 |
| dod_json | JSON | 长度 26 的 DOD 数组 |
| aug_qty_json | JSON | 长度 26 的补容数量数组 |
| created_at | DateTime | 版本时间 |

> 设计说明：一个项目可有多个历史配置（版本），最新一条为当前。本期前端只取最新一条，但表结构支持版本演进（呼应需求文档的"操作快照"）。

#### 表 4：simulation_results

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | 自增 |
| config_id | Integer FK→simulation_configs.id | 对应配置 |
| results_json | JSON | 计算结果（initGross/initAux/.../meetsReq） |
| calculated_at | DateTime | 计算时间 |

#### 表 5：reports

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer PK | 自增 |
| project_id | String(36) FK→projects.id | 所属项目 |
| type | String(20) | `technical` / `bom` |
| file_path | String(500) | 生成的 PDF 路径 |
| created_at | DateTime | 生成时间 |

> ER 关系：`projects 1—1 surveys`（项目入口）；`projects 1—N simulation_configs 1—1 simulation_results`；`projects 1—N reports`。

### 4.4 API 设计

#### 现有接口（保持不变）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| POST | `/api/soh/calculate` | 单场景仿真 |
| POST | `/api/soh/calculate-multi` | 多场景仿真 |
| POST | `/api/upload/extract` | 文档解析（仅修内部路径 bug） |

#### 新增接口

| 方法 | 路径 | 请求 | 响应 |
|------|------|------|------|
| POST | `/api/projects` | `{survey:{...调研表全字段}, source?}` | `201 {id, name, status}`（建项目+建调研表，name 取自 survey.projectName） |
| GET | `/api/projects` | — | `200 [{id, name, status, updatedAt}, ...]` |
| GET | `/api/projects/{id}` | — | `200 {project, survey, config?, results?}`（完整恢复所需全部数据） |
| PUT | `/api/projects/{id}/survey` | `{survey:{...}, source?}` | `200 {updatedAt}`（更新调研表；source 标记来源 manual/imported/mixed） |
| POST | `/api/projects/{id}/survey/import` | `multipart/form-data` 文件 | `200 {extracted, source:'imported'}`（调现有抽取逻辑，返回并入库） |
| PUT | `/api/projects/{id}/simulation` | `{params, soh, rte, dod, augQty}` | `200 {configId, results}`（后端计算并存结果，status→active） |
| DELETE | `/api/projects/{id}` | — | `204`（级联删除 survey/config/results/reports） |
| GET | `/api/projects/{id}/report?type=technical` | — | `200 application/pdf`（下载） |
| GET | `/api/projects/{id}/report?type=bom` | — | `200 application/pdf`（下载） |

**错误约定**：`4xx {error: "..."}`，`5xx {error: "..."}`。与现有接口风格一致。

> 调研表→仿真参数映射：后端在 `GET /api/projects/{id}` 返回时，附带从 survey 派生的仿真默认参数（duration/cyclesPerDay/requiredEnergy），前端用现有 `onApplyConditions` 机制注入。映射规则与现有 `RunningConditions.vue` 的 `applyParams` 一致。

### 4.5 报告设计（ReportLab）

#### 技术报告（technical）

```
┌─────────────────────────────────────┐
│  储能电站 SOH 仿真技术报告            │  ← 标题页
│  项目名称：xxx    报告日期：xxx       │
├─────────────────────────────────────┤
│  1. 项目概览                         │
│     - 项目名称 / 创建时间            │
│  2. 系统配置参数                     │  ← 来自 params
│     - 额定能量 / 集装箱数 / PCS数    │
│     - 时长 / 日循环 / AC效率 / 辅耗  │
│  3. 25 年容量衰减表                  │  ← 来自 results
│     表头：年份|SOH|RTE|DOD|粗放电|   │
│           辅耗|可用|补容累计|达标    │
│  4. 结论                             │
│     - 各年是否达标                   │
└─────────────────────────────────────┘
```

#### 设备清单（bom）

```
┌─────────────────────────────────────┐
│  设备清单 Bill of Materials          │
├─────────────────────────────────────┤
│  1. 电芯（Cell）                     │  ← products.json.cells
│     厂家 / 型号 / 容量 / 电压 /      │
│     能量 / 循环寿命                  │
│  2. 集装箱（Container）              │  ← products.json.containers
│     厂家 / 型号 / 额定能量 /         │
│     额定功率 / 冷却方式              │
│  3. PCS                              │  ← products.json.pcs
│     厂家 / 型号 / 额定功率 /         │
│     效率 / 拓扑                      │
│  4. 数量汇总                         │
│     集装箱 ×{initContainerQty} + 补容 │
│     PCS ×{initPcsQty}                │
└─────────────────────────────────────┘
```

**字体处理**：ReportLab 默认字体不含中文。方案：内嵌开源中文字体（如思源黑体子集），随仓库 `reports/fonts/` 分发；若体积敏感则用系统已安装字体（CJK 兼容性折中）。

> ⚠️ 字体是 ReportLab 中文报告的主要风险点，开发时会优先验证。

### 4.6 前端改造点

| 文件 | 改动 |
|------|------|
| `App.vue` | **修 `fetchCalculation` 语法 bug**；顶部 header 增加"项目"下拉（列表/新建）+"保存"按钮+"导出报告"按钮 |
| 新增 `api.js` | 封装后端项目/报告接口调用 |
| 新增 `ProjectBar.vue`（或并入 header） | 项目选择/新建/保存 UI |
| 现有组件 | 不改动业务逻辑，仅接收从后端恢复的数据 |

**数据流**：
- 现有：`params/soh/... → watch → 本地 calculate() → results`
- 新增分支：`打开项目 → GET /api/projects/{id} → 填充 params/soh/... → 触发 watch → results`
- 新增分支：`点击保存 → 收集 params/soh/... → PUT → 后端重算并存储`

### 4.7 依赖变更

**后端 `requirements.txt` 新增**：
```
sqlalchemy>=2.0
reportlab>=4.0
```

（`flask`、`flask-cors`、`numpy` 不变）

**前端**：无新增依赖。

---

## 5. 实施步骤（开发顺序）

每步可独立验证，失败可回退。S1~S3 已由远程主力版本完成。

| 步骤 | 内容 | 验证方式 | 状态 |
|------|------|----------|------|
| **S1** | ~~修 `App.vue` 的 `fetchCalculation` 语法 bug~~ | ~~前端能正常 build~~ | ✅ 已完成（`6a69e47`） |
| **S2** | ~~后端模块化拆分（routes/services/models/db/config）~~ | ~~跑现有接口，响应一致~~ | ⏳ 延后到 S4 一起做（当前单文件仍可用） |
| **S3** | ~~修 `UPLOAD_DIR` 硬编码路径~~ | ~~Windows 上传不报错~~ | ✅ 已完成（`6a69e47`） |
| **S4** | **后端模块化 + 引入 SQLAlchemy + 数据模型（5 张表） + DB 初始化** | 启动时自动建表 | ❌ 待做 |
| **S5** | 项目 CRUD 接口 + survey 接口（含 `GET /api/survey/{id}`） | curl/Postman 验证 | ❌ 待做 |
| **S6** | 保存/加载仿真（PUT/GET simulation） | 创建项目→保存→GET→数据一致 | ❌ 待做 |
| **S7** | ReportLab 报告生成（technical + bom） | 接口返回合法 PDF，中文正常 | ❌ 待做 |
| **S8** | 前端接项目列表/保存/导出 | 完整跑通 UC-1~UC-5 | ❌ 待做 |

---

## 6. 风险与对策

| 风险 | 影响 | 对策 |
|------|------|------|
| ReportLab 中文字体缺失 | 报告中文乱码 | S7 优先验证字体；备选方案：WeasyPrint 或前端 `window.print()` |
| 现有开发机无 Python/Node 环境 | 无法本地验证 | 部署到测试环境验证；或指导用户安装 |
| `calculate` 逻辑前后端复制两份（容量对账） | 改一处忘改另一处 | 第一波不动算法逻辑；中长期统一 |
| **SimulationLab 与容量对账割裂** | SOH 预测结果无法自动流入容量表 | 第一波不动；标记为中长期架构债务 |
| SQLite 并发写 | 多人同时保存冲突 | 本期单用户无此问题；多租户阶段迁移 PostgreSQL |
| **后端 `/api/survey/{id}` 缺失** | SimulationLab 串码加载 404 | FR-11 补充此接口 |

---

## 7. 评审检查清单

请评审时重点确认：

- [ ] **范围**：2.1 做什么 / 2.2 不做什么是否则符合预期？（尤其财务报告本期不做）
- [ ] **已完成项**：FR-8/FR-9（bug 修复）标记为已完成，是否认同？
- [ ] **数据模型**：5 张表是否覆盖需求？字段是否够用？`tenant_id` 预留是否认可？
- [ ] **API**：9 个新增接口（含 FR-11 补充的 `GET /api/survey/{id}`）是否够用？
- [ ] **报告内容**：technical / bom 两份的章节设计是否符合预期？
- [ ] **步骤**：S4~S8 的顺序是否认可？（S1~S3 已完成）
- [ ] **字体方案**：内嵌思源黑体子集是否可接受（体积约 2-5MB）？
- [ ] **字体方案**：内嵌思源黑体子集是否可接受（体积约 2-5MB）？

---

## 8. 后续波次预告（不在本期实现）

| 波次 | 内容 | 触发条件 |
|------|------|----------|
| **第二波** | 多租户 + 用户/RBAC + 付款解锁报告 + 调研表门户 + 审计日志 | 第一波验证可用、有真实多客户需求时 |
| **第三波** | 工程模块（占地/BOM物料/人工/LTSA/甘特图）+ 电芯级化学仿真 + 方案对比前端 | 业务进入交付施工阶段 |

迁移点预告：第二波启用 `tenant_id`；部署形态确定后 SQLite→PostgreSQL（改 `config.py` 一行连接串）。
