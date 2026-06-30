# 需求文档 — BESS BOQ 报价模块与财务引擎后端化

## 简介

将财务计算逻辑从 Vue 前端迁移至 Python 后端，新增 BOQ（工程量清单）模块，统一单位为 MW/MWh/USD 口径，支撑储能集成商向中东开发商投标的全流程。

## 术语表

- **BOQ (Bill of Quantities)**：工程量清单，含分项、规格、数量、单价、合价
- **BOM (Bill of Materials)**：设备材料清单（系统内已有，BOQ 对其扩展为带报价的版本）
- **CAPEX / OPEX**：资本支出 / 运营支出
- **PPA (Power Purchase Agreement)**：长期购电协议，中东储能项目主流收入模式
- **DSCR (Debt Service Coverage Ratio)**：偿债备付率
- **LCOS (Levelized Cost of Storage)**：平准化储能成本
- **IRR**：内部收益率（Project IRR / Equity IRR）
- **PCS**：储能变流器
- **BOP (Balance of Plant)**：电站配套系统

---

## 需求

### R1 — BOQ 报价模块

**用户故事**: AS 集成商投标工程师，I want 按中东标准格式创建工程量清单报价，so that 能向开发商提交符合评标要求的商务标书。

#### 验收标准

1. The system SHALL 提供 BOQ 编辑界面，支持按分部分项添加条目，每项含：序号、设备/工程名称、规格型号、单位、数量、单价、合价、备注。
2. The system SHALL 支持预设 7 级 BOQ 分类模板：电池系统 / PCS / BOP / 土建 / 并网 / EMS / 调试与运维。
3. WHEN 用户在 BOQ 中填入库/修改单价/数量，the system SHALL 实时自动重算该分项合价及分类小计和总价。
4. The system SHALL 支持 Main BOQ + Alternative BOQ 双方案平行编辑和切换对比。
5. The system SHALL 基于 `ratedEnergy`、`initContainerQty`、`pcsPower`、`duration` 等系统设计参数，自动预填 BOQ 数量建议值。
6. WHEN BOQ 保存后，the system SHALL 将 CAPEX 总计同步至财务引擎，替代现有手工填写的 CAPEX 输入。

---

### R2 — 财务引擎后端迁移

**用户故事**: AS 系统架构师，I want 所有财务计算统一在后端执行，so that 计算结果可服务端校验、多模块复用、不可被客户端篡改。

#### 验收标准

1. The system SHALL 实现 `POST /api/financial/calculate` 端点，接收系统能量数据 + 财务参数，返回完整 25 年现金流表和核心指标。
2. WHEN 请求到达 `/api/financial/calculate`，the system SHALL 按以下顺序计算：CAPEX 汇总 → 年度收入（多收入叠加）→ OPEX → EBITDA → 折旧 → 利息 → 税前利润 → 所得税 → 净现金流 → NPV/IRR/LCOS/DSCR/回收期。
3. The system SHALL 支持多收入模型：套利收入 + 容量市场收入 + 辅助服务收入 + PPA 收入 + 容量拍卖收入，每种收入可独立启用/禁用。
4. The system SHALL 在收入计算中应用 `price_escalation`（年通胀传导因子），默认 2%/年。
5. The system SHALL 支持融资参数化：贷款比例、利率、贷款期限、等额本息/等额本金还款方式。
6. The system SHALL 支持税收建模：企业所得税率、增值税率、税收减免期（tax holiday years）。
7. The system SHALL 实现折旧建模：直线折旧法，折旧年限 15 年，残值率 5%。
8. The system SHALL 计算 Equity IRR（股本 IRR）和 Project IRR（项目 IRR）两个口径。
9. WHEN 请求中 `tax=0` 且 `depreciation=0`，the system SHALL 仍正确输出简化版指标（向后兼容当前 pipeline 行为）。
10. The system SHALL 在 `/api/pipeline/calculate` 响应中内嵌完整财务结果，保持与现有前端的向后兼容。

---

### R3 — 单位体系标准化

**用户故事**: AS 国际化业务用户，I want 系统内部统一使用国际标准单位（MW/MWh/USD），so that 中东/全球项目计算结果一致、无换算错误。

#### 验收标准

1. The system SHALL 内部一律使用 MW（功率）、MWh（能量）、USD（金额）进行存储和计算。
2. The system SHALL 在显示层根据用户 locale 自动转换：SAR/AED 汇率、MW→kW 等。
3. The system SHALL 在数据库 FinancialData 模型中新增 `currency` 字段，默认 `USD`。
4. The system SHALL 将所有 `/10000` 魔法数字的元→万元转换替换为显式的 `to_display_unit()` / `to_internal_unit()` 工具函数。
5. The system SHALL 废弃"亩"为面积单位，统一使用 m² 和 sq.ft 双显示（中东项目公制/英制混排）。
6. WHEN 新建项目，the system SHALL 默认 `currency=USD`、`power_unit=MW`、`energy_unit=MWh`。

---

### R4 — 调研表中东化（调研表字段扩展）

**用户故事**: AS 中东项目经理，I want 在项目调研表中填录并网标准和环境参数，so that 系统能输出符合 SEC/ESMA/GSO 要求的投标文件。

#### 验收标准

1. The system SHALL 在调研表中新增"电网接入"分组字段：接入点电压等级（kV）、PCC 短路容量（MVA）、并网标准代码（SEC/ESMA/GSO/其他）。
2. The system SHALL 在调研表中新增"环境条件"分组字段：最高环境温度（°C）、最低环境温度、年平均温度、沙尘防护等级（IP55/IP65）、湿度循环等级。
3. WHEN 填写了最高环境温度 > 40°C，the system SHALL 在衰减预测中自动施加温度加速因子（Arrhenius 模型中 T_ref 使用实际环境温度替代默认 25°C）。

---

### R5 — 财务与 BOQ 联动

**用户故事**: AS 集成商投标工程师，I want BOQ 汇总自动填入 CAPEX 且 BOM 变更同步更新 BOQ，so that 技术方案与商务报价始终保持一致。

#### 验收标准

1. WHEN BOQ 数据发生变化，the system SHALL 自动重新计算财务引擎并刷新指标仪表盘。
2. WHEN Phase 2 系统设计中的 ContainerQty/PcsQty 发生变化，the system SHALL 更新 BOQ 中对应条目的建议数量。
3. The system SHALL 提供"BOQ→CAPEX 摘要"映射表，将 7 类 BOQ 分类汇总为 equipment / epc / development 三大 CAPEX 类别。
4. IF BOQ 未填写，the system SHALL 允许用户手工输入 CAPEX（保持向后兼容）。

---

### R6 — 财务仪表盘重构

**用户故事**: AS 项目经理，I want 财务仪表盘展示完整 25 年现金流表和多个核心财务指标，so that 能直观评估项目经济可行性。

#### 验收标准

1. The system SHALL 在 Phase4Page 重构 FinancialDashboard，移除前端计算逻辑，改为调用 `/api/financial/calculate` 获取结果。
2. The system SHALL 在仪表盘中展示 7 个核心指标卡片：Project IRR / Equity IRR / NPV / LCOS / DSCR (min/avg) / 回收期 / 25 年总净利润。
3. The system SHALL 使用颜色编码标识指标健康度：IRR >= 8% 绿色，IRR 6-8% 黄色，IRR < 6% 红色。
4. The system SHALL 展示 25 年柱状图：年度收入 / OPEX / 净现金流 / 累计现金流 (S 曲线)。

---

## 设计决策（已确认）

1. **BOQ 数据存储**：独立 `boq_items` 表，关联 `project_id`，支持版本管理和复杂查询
2. **前端 BOQ 组件**：全新 `BoqEditor.vue`，与现有 BOM 组件职责分离
3. **多收入模型默认**：所有收入类型默认全部启用，用户自行关闭不需要的
4. **汇率数据源**：内嵌固定汇率表（SAR=3.75/USD，AED=3.6725/USD，CNY=7.24/USD）
