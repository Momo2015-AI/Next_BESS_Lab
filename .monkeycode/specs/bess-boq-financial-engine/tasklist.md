# 需求实施计划

- [x] 1. 后端：创建统一单位与汇率工具模块 (R3.4)
  - 创建 `soh-sim-backend/services/units.py`
  - 实现 `EXCHANGE_RATES` 常量表 (SAR=3.75, AED=3.6725, CNY=7.24)
  - 实现 `to_internal(value, unit, currency)` 和 `to_display(value, unit, currency)` 转换函数
  - 实现 `convert_currency(value, from_curr, to_curr)` 函数

- [x] 2. 后端：创建完整财务计算引擎 (R2.1, R2.3, R2.4, R2.5, R2.6, R2.7, R2.8, R2.9)
  - 创建 `soh-sim-backend/services/financial.py`
  - 实现 `_aggregate_boq_to_capex(boq_items)` — 7 分类映射到 equipment/epc/development
  - 实现 `_calculate_revenue_stack(params, year, totalAcUsable)` — 5 种收入叠加 (arbitrage/capacity/ancillary/ppa/capacityAuction)，含 price_escalation 通胀传导
  - 实现 `_calculate_debt_schedule(totalCapex, financing)` — 等额本息/等额本金还款计划
  - 实现 `_calculate_depreciation(totalCapex, years, residualRate)` — 15 年直线折旧
  - 实现 `_calculate_annual_cashflow(year, revenue, opex, depreciation, interest, tax)` — 单年现金流
  - 实现 `calculate_full_financial(totalAcUsable, financialParams, boqData)` — 主入口，返回 FullFinancialResponse
  - `_compute_irr` 从 `services/pipeline.py:242` 移入此处并作为内部函数
  - 实现 Project IRR 和 Equity IRR 双口径计算
  - 现金流末尾 year[0]=-CAPEX，year[1..25]=收入−OPEX−税
  - 当 tax=0 且 depreciation=0 时仍正确输出简化指标（向后兼容）
- [x]* 2.1 为 financial.py 编写单元测试
  - 测试给定固定 totalAcUsable 和 financialParams，验证 NPV > 0 / IRR > 0 符号一致性
  - 测试 5 种收入各自独立启用时的年收入数值
  - 测试等额本息 vs 等额本金前 5 年利息差异
  - 测试 BOQ→CAPEX 7 分类映射正确性（电池→equipment, PCS→equipment, BOP→epc 等）

- [x] 3. 后端：实现 `/api/financial/calculate` 路由 (R2.1)
  - 创建 `soh-sim-backend/routes/financial.py`，创建 `financial_bp` Blueprint
  - 实现 `POST /api/financial/calculate`：校验 totalAcUsable 必填 → 调用 `calculate_full_financial()` → 返回 JSON
  - 实现 `POST /api/financial/capex-from-boq`：接收 boq_items → 调用 `_aggregate_boq_to_capex()` → 返回 capex 摘要
  - 错误处理：totalAcUsable 为空返回 400 + field 级错误；IRR 无解返回 irr:null 不抛异常
  - 在 `app.py` 中注册 `financial_bp`

- [x] 4. 检查点 - 财务引擎后端 API 可独立调通

- [x] 5. 后端：数据库迁移 — 新增 BOQ 表与扩展现有表 (R1, R3.1, R3.3, R4)
  - 在 `database.py` 中新增 `BoqSection` 模型 (id/code/name/name_zh/default_unit/sort_order)
  - 在 `database.py` 中新增 `BoqItem` 模型 (id/project_id/section_code/seq/name/spec/unit/quantity/unit_price/total_price/note/is_alternative/version)
  - 在 `FinancialData` 模型中新增 `currency` (String(3), default='USD') 和 `unit_system` (String(10), default='metric')
  - 在 `Survey` 模型中新增字段：pcc_voltage(Float), pcc_short_circuit_mva(Float), grid_code(String(50)), temp_max(Float), temp_min(Float), temp_avg(Float), sand_protection(String(10)), humidity_cycle(String(20))
  - 添加 `_JSON_COLUMNS` 配置和 `_serialize_value` 支持新表
  - 添加 BoqSection 和 BoqItem 到 `to_dict()` 序列化逻辑

- [x] 6. 后端：种子数据 — 初始化 7 级 BOQ 分类模板 (R1.2)
  - 在 `database.py` 或新建 `services/boq.py` 中实现 `seed_boq_sections()`
  - 插入 7 条 BOQ 分类记录：100-Battery System, 200-PCS, 300-BOP, 400-Civil Works, 500-Grid Connection, 600-EMS, 700-Commissioning & O&M
  - 每项含 code/name/name_zh/default_unit/sort_order
  - 在 `app.py` 的 `with app.app_context()` 块中调用 `seed_boq_sections()`

- [x] 7. 后端：实现 BOQ CRUD API (R1.3, R1.5, R5.1, R5.2)
  - 创建 `soh-sim-backend/routes/boq.py`，创建 `boq_bp` Blueprint
  - 实现 `GET /api/boq/sections` — 返回 7 个预设 BOQ 分类模板
  - 实现 `GET /api/boq/items?project_id=X` — 返回指定项目的 BOQ 条目，按 section_code + seq 排序
  - 实现 `POST /api/boq/items` — 批量保存 BOQ 条目（接收 BoqItem[]），自动计算每个条目的 total_price = quantity * unit_price
  - 实现 `POST /api/boq/version` — 创建报价版本快照
  - 在 `app.py` 中注册 `boq_bp`

- [x] 8. 后端：重构 pipeline.py 财务计算委托到新引擎 (R2.10)
  - 修改 `services/pipeline.py:calculate_financial_metrics` 为委托到 `services/financial.py:calculate_full_financial`
  - 保持现有 `/api/pipeline/calculate` 返回结构不变（向后兼容）
  - 移除 pipeline.py 中的 `_compute_irr` 函数（已在 financial.py 中）
  - 更新 `calculate_full_pipeline` 签名，传递 `boq_data` 参数（可选）

- [x] 9. 检查点 - 后端所有 API 就绪，`/api/pipeline/calculate` 输出兼容，新旧并存

- [x] 10. 前端：创建单位工具模块 (R3.4, R3.5, R3.6)
  - 创建 `soh-sim-frontend/src/utils/units.js`
  - 实现 `EXCHANGE_RATES` 常量
  - 实现 `toInternal(value, unit)` 和 `toDisplay(value, unit, currency)` 转换函数
  - 实现 `formatCurrency(value, currency)` 显示格式化（保留 2 位小数 + 千分位）
  - 实现 `formatArea(value, unit)` 面积格式化（m² / sq.ft）

- [x] 11. 前端：扩展 BESS Store — BOQ 与财务状态 (R1, R2, R5)
  - 修改 `soh-sim-frontend/src/stores/bess.js`
  - 新增 `boq` state：items[], activeVersion('main'|'alternative'), totalPrice
  - 重构 `financial` state：multi_revenue 5 种独立 enable + 单价、financing 配置、tax 配置、扩展 metrics (projectIrr/equityIrr/dscr_min/dscr_avg/roi/cashflowTable/capexBreakdown)
  - 新增 action `refreshFinancialResults()` — 构造请求体 → 调用 `POST /api/financial/calculate` → 写入 financial.metrics 和 cashflowTable
  - 新增 action `fetchBoqItems(projectId)` — 调用 `GET /api/boq/items`
  - 新增 action `saveBoqItems(projectId, items)` — 调用 `POST /api/boq/items`
  - 新增 action `aggregateCapexFromBoq()` — 调用 `POST /api/financial/capex-from-boq`
  - 更新 `runPipeline()` 以传递扩展后的 financial_params 到 `/api/pipeline/calculate`

- [x] 12. 前端：创建 BOQ 编辑器组件 (R1.1, R1.3, R1.4, R1.5, R1.6, R5.1, R5.2, R5.3)
  - 创建 `soh-sim-frontend/src/components/BoqEditor.vue`
  - 实现 7 级分类折叠面板，每类显示序号/名称/规格/单位/数量/单价/合价/备注
  - 数量列根据 store.systemParams 自动预填建议值（containerQty→电池系统集装箱数量, pcsPower→PCS 数量）
  - 单价/数量变更时实时自动重算合价 → 小计 → 总价
  - 实现 Main BOQ / Alternative BOQ 双 tab 切换
  - "汇总到 CAPEX" 按钮 → 调用 store.aggregateCapexFromBoq() 并写入 store.financial.capex
  - 挂载时调用 store.fetchBoqItems(store.project.id) 加载已有数据

- [x] 13. 前端：重构 FinancialDashboard — 移除前端计算、接入后端 API (R2.1, R6.1, R6.2, R6.3, R6.4)
  - 修改 `soh-sim-frontend/src/components/FinancialDashboard.vue`
  - 移除 `computeAll()` 函数及所有局部计算逻辑
  - 移除 CAPEX/OPEX 输入表单（已由 BoqEditor 接管）
  - 移除局部 `f` reactive 对象
  - 新增 `props: { boqDriven: Boolean }` — 控制是否显示手工 CAPEX 输入回退模式
  - 组件挂载时调用 `store.refreshFinancialResults()` 获取后端计算结果
  - 指标卡片数据源改为 `store.financial.metrics`：Project IRR / Equity IRR / NPV / LCOS / DSCR(min/avg) / Payback / ROI
  - 颜色编码：IRR >= 8% 绿色，6-8% 黄色，<6% 红色
  - 保留并更新 ECharts 图表：25 年现金流 S 曲线、收入堆叠、DSCR 趋势、CAPEX 饼图（数据来源改为 cashflowTable）
  - 新增 5 种收入类型的启用/禁用开关，变更后触发重新计算

- [x] 14. 前端：重构 Phase4Page — BOQ 先行 + 财务仪表盘整合 (R5.1, R6.1)
  - 修改 `soh-sim-frontend/src/pages/Phase4Page.vue`
  - 步骤重排序：4.1 BOQ 报价 → 4.2 成本汇总 → 4.3 收入模型 → 4.4 财务指标 → 4.5 敏感性分析
  - 步骤 4.1：嵌入 `BoqEditor.vue`
  - 步骤 4.2：展示 CAPEX 汇总（从 BOQ 自动汇总），支持小计修改
  - 步骤 4.3：嵌入 FinancialDashboard 的收入模型配置部分
  - 步骤 4.4：嵌入 FinancialDashboard（boqDriven=true），展示完整指标和图表
  - 步骤 4.5：保留 SensitivityAnalysis 组件

- [x] 15. 前端：扩展调研表 — 中东并网与环境字段 (R4.1, R4.2, R4.3)
  - 找到 SurveyForm.vue 或 Phase1Page 中的调研表部分
  - 新增 "电网接入" 分组：接入点电压等级(kV)、PCC 短路容量(MVA)、并网标准下拉框(SEC/ESMA/GSO/other)
  - 新增 "环境条件" 分组：最高温度(°C)、最低温度、年平均温度、沙尘防护(IP55/IP65)、湿度循环(low/medium/high)
  - 环境温度最高值 > 40°C 时，自动更新 store.systemParams.temperature 并触发 pipeline 重新计算

- [x] 16. 检查点 - 全链路端到端验证
  - 确保 `POST /api/financial/calculate` 返回完整 FullFinancialResponse 结构（metrics + cashflowTable + capexBreakdown）
  - 确保 `POST /api/boq/items` 保存后 `GET /api/boq/items?project_id=X` 返回一致数据
  - 确保 Phase4Page 中 BOQ → CAPEX → 财务指标 链路连通
  - 确保 FinancialDashboard 从后端获取数据后 4 个图表正常渲染
  - 确保 `/api/pipeline/calculate` 返回结构向后兼容
  - 确保现有功能（Phase1-5 其他页面、工具页、产品库）未退化
