# 数据库与数据结构文档

## 1. 数据库概述

本系统使用 **SQLite** 作为数据库，具有以下特点：
- 轻量级、跨平台、无需额外安装
- 数据库文件：`soh_sim.db`
- 使用 Flask-SQLAlchemy 作为 ORM 框架
- 支持多租户数据隔离

## 2. 数据模型总览

| 模型 | 表名 | 说明 | 支持功能 |
|------|------|------|----------|
| Tenant | tenants | 租户 | 多租户数据隔离 |
| User | users | 用户 | 用户管理、权限控制 |
| Survey | surveys | 调研表 | 项目调研表填写 |
| Project | projects | 项目 | 项目全生命周期管理 |
| Simulation | simulations | 仿真 | 仿真实验室、25年矩阵 |
| BatteryPCSConfig | battery_pcs_configs | 电池PCS配置 | 电池与PCS配对 |
| SohRteData | soh_rte_data | SOH/RTE数据 | 数据注入、图表展示 |
| FinancialData | financial_data | 财务数据 | 财务看板 |
| ProductConfig | product_configs | 产品配置 | 产品与方案配置 |
| FormulaConfig | formula_configs | 公式配置 | 算法公式实验舱 |

## 3. 功能模块与数据表对应关系

```
前端组件                          数据表
─────────────────────────────────────────────────
SurveyForm.vue          →        Survey
ParameterPanel.vue      →        Simulation.input_params
RunningConditions.vue   →        Survey (环境条件字段)
BatteryPCSConfig.vue    →        BatteryPCSConfig
SimulationLab.vue       →        Simulation
ProductConfig.vue       →        ProductConfig
FinancialDashboard.vue  →        FinancialData
MatrixTable.vue         →        Simulation.results
DataInjection.vue       →        SohRteData
FormulaLab.vue          →        FormulaConfig
SohChart.vue            →        SohRteData / Simulation.results
```

## 4. 详细数据模型

### 4.1 Tenant（租户）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | String(36) | UUID主键 |
| name | String(100) | 租户名称 |
| code | String(50) | 租户编码（唯一） |
| status | String(20) | 状态：active/suspended |
| created_at | DateTime | 创建时间 |

### 4.2 User（用户）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | String(36) | UUID主键 |
| tenant_id | String(36) | 所属租户 |
| username | String(50) | 用户名（唯一） |
| email | String(100) | 邮箱（唯一） |
| password_hash | String(256) | 密码哈希 |
| role | String(20) | 角色：admin/engineer/user |
| status | String(20) | 状态 |
| created_at | DateTime | 创建时间 |
| last_login | DateTime | 最后登录时间 |

### 4.3 Survey（调研表）

| 字段名 | 类型 | 说明 | 对应功能 |
|--------|------|------|----------|
| id | String(36) | UUID主键 | 调研表ID |
| project_name | String(200) | 项目名称 | SurveyForm |
| contact_person | String(100) | 联系人 | SurveyForm |
| contact_phone | String(50) | 联系电话 | SurveyForm |
| contact_email | String(100) | 联系邮箱 | SurveyForm |
| location | String(200) | 项目地点 | SurveyForm |
| altitude | Float | 海拔高度(m) | RunningConditions |
| total_mw | Float | 总功率(MW) | SurveyForm |
| total_mwh | Float | 总容量(MWh) | SurveyForm |
| duration | Float | 储能时长(h) | ParameterPanel |
| cycles_per_day | Float | 每日循环次数 | ParameterPanel |
| temp_max | Float | 最高温度(°C) | RunningConditions |
| temp_min | Float | 最低温度(°C) | RunningConditions |
| temp_avg | Float | 平均温度(°C) | RunningConditions |
| humidity | Float | 相对湿度(%) | RunningConditions |
| grid_voltage | Float | 并网电压(kV) | RunningConditions |
| grid_frequency | Float | 电网频率(Hz) | RunningConditions |
| rte_target | Float | RTE目标(%) | Performance |
| soh_year1 | Float | SOH第一年(%) | Performance |
| soh_year25 | Float | SOH第25年(%) | Performance |
| calendar_life | Integer | 日历寿命(年) | Performance |
| cycle_life | Integer | 循环寿命(次) | Performance |
| availability_target | Float | 可用率目标(%) | Performance |
| aux_consumption | Float | 辅助功耗(%) | ParameterPanel |
| response_time | Float | 响应时间(ms) | Performance |
| dc_voltage_range | String(100) | 直流电压范围 | BatteryPCSConfig |
| ac_voltage | Float | 交流电压(V) | BatteryPCSConfig |
| thdi | Float | 谐波畸变(%) | Performance |
| remarks | Text | 备注 | SurveyForm |
| attachments | Text | 附件(JSON) | SurveyForm |
| status | String(20) | 状态 | 流程管理 |
| project_id | String(36) | 关联项目 | 关联 |

### 4.4 Project（项目）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | String(36) | UUID主键 |
| tenant_id | String(36) | 所属租户 |
| name | String(200) | 项目名称 |
| code | String(50) | 项目编号（唯一） |
| status | String(20) | 状态：draft/active/completed/archived |
| stage | String(50) | 阶段：survey/design/simulation/operation |
| config | Text | 项目配置(JSON) |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### 4.5 Simulation（仿真）

| 字段名 | 类型 | 说明 | 对应功能 |
|--------|------|------|----------|
| id | String(36) | UUID主键 | |
| project_id | String(36) | 关联项目 | |
| user_id | String(36) | 创建用户 | |
| name | String(200) | 仿真名称 | SimulationLab |
| description | Text | 仿真描述 | SimulationLab |
| algorithm_type | String(50) | 算法类型：arrhenius/custom | SimulationLab |
| duration_years | Integer | 仿真年限(默认25) | SimulationLab |
| correction_factor | Float | 校正因子 | SimulationLab |
| input_params | Text | 输入参数(JSON) | ParameterPanel |
| results | Text | 仿真结果(JSON矩阵) | MatrixTable |
| manual_corrections | Text | 手工校正(JSON) | SimulationLab |
| status | String(20) | 状态：pending/running/completed/failed | |
| started_at | DateTime | 开始时间 | |
| completed_at | DateTime | 完成时间 | |

### 4.6 BatteryPCSConfig（电池PCS配置）

| 字段名 | 类型 | 说明 | 对应功能 |
|--------|------|------|----------|
| id | String(36) | UUID主键 | |
| project_id | String(36) | 关联项目 | |
| name | String(200) | 配置名称 | BatteryPCSConfig |
| container_model | String(100) | 集装箱型号 | BatteryPCSConfig |
| container_qty | Integer | 集装箱数量 | BatteryPCSConfig |
| container_energy | Float | 单箱能量(MWh) | BatteryPCSConfig |
| container_power | Float | 单箱功率(MW) | BatteryPCSConfig |
| pcs_model | String(100) | PCS型号 | BatteryPCSConfig |
| pcs_qty | Integer | PCS数量 | BatteryPCSConfig |
| pcs_power | Float | 单PCS功率(MW) | BatteryPCSConfig |
| pcs_voltage | Float | PCS电压(V) | BatteryPCSConfig |
| total_energy | Float | 总能量(MWh) | 自动计算 |
| total_power | Float | 总功率(MW) | 自动计算 |
| pcs_ratio | Float | PCS配比 | 自动计算 |
| connection_type | String(50) | 连接方式 | BatteryPCSConfig |
| connection_diagram | Text | 连接图(JSON) | BatteryPCSConfig |
| single_line_diagram | Text | 单线图(JSON) | BatteryPCSConfig |

### 4.7 SohRteData（SOH/RTE数据）

| 字段名 | 类型 | 说明 | 对应功能 |
|--------|------|------|----------|
| id | String(36) | UUID主键 | |
| project_id | String(36) | 关联项目 | |
| simulation_id | String(36) | 关联仿真 | |
| name | String(200) | 数据名称 | DataInjection |
| soh_values | Text | SOH数组(JSON) | DataInjection/SohChart |
| rte_values | Text | RTE数组(JSON) | DataInjection/SohChart |
| dod_values | Text | DOD数组(JSON) | DataInjection |
| aug_qty_values | Text | 扩容数组(JSON) | MatrixTable |
| source | String(50) | 来源：manual/simulation/imported | DataInjection |
| import_file | String(200) | 导入文件名 | DataInjection |

### 4.8 FinancialData（财务数据）

| 字段名 | 类型 | 说明 | 对应功能 |
|--------|------|------|----------|
| id | String(36) | UUID主键 | |
| project_id | String(36) | 关联项目 | |
| name | String(200) | 配置名称 | FinancialDashboard |
| off_peak_price | Float | 低谷购电价($/MWh) | FinancialDashboard |
| peak_price | Float | 高峰售电价($/MWh) | FinancialDashboard |
| spread_capture | Float | 价差捕获率(%) | FinancialDashboard |
| operating_days | Integer | 运行天数 | FinancialDashboard |
| capacity_price | Float | 容量市场单价($/MW-yr) | FinancialDashboard |
| ancillary_price | Float | 辅助服务单价($/MW-yr) | FinancialDashboard |
| price_escalation | Float | 电价年涨幅(%) | FinancialDashboard |
| capex | Float | 初始投资($) | FinancialDashboard |
| capex_per_mwh | Float | 单位投资($/MWh) | FinancialDashboard |
| opex_per_year | Float | 年运维成本($) | FinancialDashboard |
| opex_per_mwh | Float | 单位运维($/MWh/yr) | FinancialDashboard |
| augmentation_cost | Float | 扩容成本($) | FinancialDashboard |
| debt_ratio | Float | 贷款比例(%) | FinancialDashboard |
| interest_rate | Float | 贷款利率(%) | FinancialDashboard |
| loan_term | Integer | 贷款期限(年) | FinancialDashboard |
| discount_rate | Float | 折现率(%) | FinancialDashboard |
| npv | Float | 净现值 | 计算结果 |
| irr | Float | 内部收益率 | 计算结果 |
| payback_years | Float | 回收期(年) | 计算结果 |
| lcos | Float | 储能度电成本 | 计算结果 |
| cashflow_data | Text | 25年现金流(JSON) | FinancialDashboard |

### 4.9 ProductConfig（产品配置）

| 字段名 | 类型 | 说明 | 对应功能 |
|--------|------|------|----------|
| id | String(36) | UUID主键 | |
| project_id | String(36) | 关联项目 | |
| name | String(200) | 配置名称 | ProductConfig |
| cell_model | String(100) | 电芯型号 | ProductConfig |
| cell_capacity | Float | 电芯容量(Ah) | ProductConfig |
| cell_voltage | Float | 电芯电压(V) | ProductConfig |
| cell_supplier | String(100) | 电芯供应商 | ProductConfig |
| container_model | String(100) | 集装箱型号 | ProductConfig |
| container_supplier | String(100) | 集装箱供应商 | ProductConfig |
| pcs_model | String(100) | PCS型号 | ProductConfig |
| pcs_supplier | String(100) | PCS供应商 | ProductConfig |
| certifications | Text | 认证要求(JSON数组) | ProductConfig |
| epc_company | String(100) | EPC公司 | ProductConfig |
| epc_contract_type | String(50) | EPC合同类型 | ProductConfig |

### 4.10 FormulaConfig（公式配置）

| 字段名 | 类型 | 说明 | 对应功能 |
|--------|------|------|----------|
| id | String(36) | UUID主键 | |
| user_id | String(36) | 创建用户 | |
| name | String(200) | 公式名称 | FormulaLab |
| formula_type | String(50) | 类型：soh/rte/financial/custom | FormulaLab |
| expression | Text | 数学表达式 | FormulaLab |
| parameters | Text | 参数定义(JSON) | FormulaLab |
| description | Text | 公式说明 | FormulaLab |
| is_public | Boolean | 是否公开 | FormulaLab |

## 5. 数据关系图

```
Tenant（租户）
    │
    ├── User（用户）
    │       │
    │       └── Simulation（仿真）
    │               │
    │               └── SohRteData（SOH/RTE数据）
    │
    └── Project（项目）
            │
            ├── Survey（调研表）
            │
            ├── Simulation（仿真）
            │       │
            │       └── SohRteData
            │
            ├── BatteryPCSConfig（电池PCS配置）
            │
            ├── SohRteData（SOH/RTE数据）
            │
            ├── FinancialData（财务数据）
            │
            └── ProductConfig（产品配置）
```

## 6. API 接口规划

### 调研表接口（已实现）
- `POST /api/survey/submit` - 提交调研表
- `GET /api/survey/<id>` - 获取调研表
- `PUT /api/survey/<id>` - 更新调研表
- `DELETE /api/survey/<id>` - 删除调研表
- `GET /api/survey/list` - 调研表列表

### 项目接口（已实现）
- `GET /api/project/<id>` - 获取项目
- `PUT /api/project/<id>` - 更新项目
- `GET /api/project/list` - 项目列表

### 仿真接口（待实现）
- `POST /api/simulation/create` - 创建仿真
- `POST /api/simulation/<id>/run` - 执行仿真
- `GET /api/simulation/<id>` - 获取仿真结果
- `GET /api/simulation/list` - 仿真列表

### 配置接口（待实现）
- `POST /api/battery-config/save` - 保存电池PCS配置
- `POST /api/soh-rte/save` - 保存SOH/RTE数据
- `POST /api/financial/save` - 保存财务数据
- `POST /api/product-config/save` - 保存产品配置

## 7. JSON 数据格式示例

### 仿真结果 (Simulation.results)
```json
{
  "initGross": [280.5, 262.3, ...],
  "initAux": [0.5, 0.5, ...],
  "initAcUsable": [280.0, 261.8, ...],
  "augGross": [0, 0, 30.2, ...],
  "augAux": [0, 0, 0.1, ...],
  "augAcUsable": [0, 0, 30.1, ...],
  "totalAcUsable": [280.0, 261.8, 291.9, ...],
  "meetsReq": [true, false, true, ...]
}
```

### SOH数据 (SohRteData.soh_values)
```json
[0.9925, 0.9318, 0.9014, 0.877, 0.856, 0.8371, 0.8197, 0.8036, 0.7885, 0.7742,
 0.7606, 0.7475, 0.735, 0.723, 0.7113, 0.7, 0.689, 0.678, 0.6672, 0.6564,
 0.6458, 0.6354, 0.6252, 0.6152, 0.6074, 0.6008]
```

### 连接图数据 (BatteryPCSConfig.connection_diagram)
```json
{
  "nodes": [
    {"id": "B1", "type": "battery", "label": "集装箱1"},
    {"id": "P1", "type": "pcs", "label": "PCS1"}
  ],
  "edges": [
    {"from": "B1", "to": "P1", "type": "dc"}
  ]
}
```

## 8. 状态流转

### 调研表状态
```
pending → reviewed → approved → 项目创建
                    → rejected → 返回修改
```

### 项目状态
```
draft → active → completed → archived
       ↓
       各阶段：survey → design → simulation → operation
```

### 仿真状态
```
pending → running → completed
                 → failed
```

## 9. 技术栈

- **数据库**: SQLite 3
- **ORM**: Flask-SQLAlchemy 3.0+
- **Python**: 3.8+
- **UUID**: Python uuid 模块
- **JSON**: Python json 模块

## 10. 文件结构

```
soh-sim-backend/
├── app.py              # Flask 应用入口
├── database.py         # 数据库配置与模型定义
├── requirements.txt    # Python 依赖
├── routes/
│   ├── __init__.py
│   └── survey.py       # 调研表API路由
└── soh_sim.db          # SQLite 数据库文件（运行后生成）
```