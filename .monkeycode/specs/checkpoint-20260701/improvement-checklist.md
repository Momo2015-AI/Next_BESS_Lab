# 代码规范改进进度表

基于 CODE_STYLE.md v2.0 规范，针对 `soh-sim-frontend` 和 `soh-sim-backend` 的全面审查结果。

**审查日期**: 2026-07-01
**审查依据**: CODE_STYLE.md v2.0

---

## 前端改进清单

### P0 - 内存泄漏修复（立即，影响稳定性和性能）

| # | 文件 | 问题 | 行号 | 状态 |
|---|------|------|------|------|
| F1 | SimulationLab.vue | 缺少 onUnmounted（ECharts dispose + resize remove） | 全文件 | 待修复 |
| F2 | SensitivityAnalysis.vue | 缺少 onUnmounted（ECharts dispose + resize remove） | 全文件 | 待修复 |
| F3 | ScenarioCompare.vue | 缺少 onUnmounted（ECharts dispose + resize remove） | 全文件 | 待修复 |
| F4 | BatteryPCSConfig.vue | 缺少 onUnmounted（ECharts dispose） | 全文件 | 待修复 |
| F5 | FinancialDashboard.vue | resize 监听器未在 onUnmounted 中移除 | 794 | 待修复 |
| F6 | EnergyFlowSankey.vue | resize 未移除 + MutationObserver 未 disconnect | 288/251 | 待修复 |
| F7 | CostWaterfallChart.vue | MutationObserver 未 disconnect | 306 | 待修复 |
| F8 | CurrencyConverter.vue | setInterval 未 clearInterval | 212 | 待修复 |
| F9 | useExchangeRate.js | setInterval 未在 onUnmounted 清除 | 193 | 待修复 |

### P1 - 性能防抖（改善交互体验）

| # | 文件 | 问题 | 行号 | 状态 |
|---|------|------|------|------|
| G1 | FinancialDashboard.vue | watch(f) deep true 无防抖 | 781 | 待修复 |
| G2 | EfficiencyChain.vue | watch(factors) deep true 无防抖 | 212 | 待修复 |
| G3 | BatteryHealthHeatmap.vue | watch deep true 无防抖 | 210 | 待修复 |
| G4 | EnergyFlowSankey.vue | watch deep true 无防抖 | 269 | 待修复 |
| G5 | CostWaterfallChart.vue | watch deep true 无防抖 | 324 | 待修复 |
| G6 | DegradationConfig.vue | watch deep true 无防抖 | 313 | 待修复 |

### P2 - 大组件拆分（>400 行，按严重程度排序）

| # | 文件 | 行数 | 建议拆分方式 | 状态 |
|---|------|------|-------------|------|
| H1 | SimulationLab.vue | 1360 | 按步骤拆为 SurveyStep/ParamsStep/AlgoStep/CorrectionStep/ResultStep | 待拆分 |
| H2 | EpcPage.vue | 1045 | 按模块拆为 SystemArch/GridCompliance/FireSafety/IPPFinance 等 | 待拆分 |
| H3 | BatteryPCSConfig.vue | 989 | 拆为 PCSConfigForm/PCSConnectionDiagram/PCSChart | 待拆分 |
| H4 | RunningConditions.vue | 901 | 拆为 SiteConditions/GridConditions/FinancialConditions | 待拆分 |
| H5 | FinancialDashboard.vue | 795 | 拆为 RevenuePanel/CostPanel/FinancingPanel/CashFlowTable/CashFlowChart | 待拆分 |

### P3 - 内联事件处理器消除（按数量排序）

| # | 文件 | 数量 | 改用 CSS :focus-visible + transition | 状态 |
|---|------|------|--------------------------------------|------|
| I1 | SimulationLab.vue | 96 | | 待修复 |
| I2 | ProductConfig.vue | 60 | | 待修复 |
| I3 | PcsACDesign.vue | 44 | | 待修复 |
| I4 | SurveyPage.vue | 42 | | 待修复 |
| I5 | EngineeringCalc.vue | 42 | | 待修复 |
| I6 | BatteryDCDesign.vue | 42 | | 待修复 |
| I7 | FinancialDashboard.vue | 35 | | 待修复 |
| I8 | ScenarioCompare.vue | 32 | | 待修复 |

### P4 - ECharts 按需导入 + i18n + 内联 style

| # | 类别 | 涉及文件数 | 状态 |
|---|------|-----------|------|
| J1 | import * as echarts 改为按需导入 | 10 | 待修复 |
| J2 | 国际化 $t() 覆盖（硬编码文本清除） | ~50 | 待修复 |
| J3 | 内联 style 改为 CSS 类 | 34 | 待修复 |

---

## 后端改进清单

### P0 - 数据库索引缺失（全局性能）

| # | 文件 | 问题 | 状态 |
|---|------|------|------|
| B1 | database.py | 所有 29 个外键列缺少 Index __table_args__ | 待添加 |

### P1 - N+1 查询 + 重复查询修复

| # | 文件 | 问题 | 状态 |
|---|------|------|------|
| B2 | routes/project.py | 9 个端点重复 User.query.get(user_id) | 待修复 |
| B3 | routes/simulation.py | 7 个端点重复 User.query.get(user_id) | 待修复 |
| B4 | routes/auth.py:354 | role_required 重复查询 User | 待修复 |
| B5 | database.py:264-284 | seed_products 循环查询（N+1） | 待修复 |

### P2 - 列表分页 + 事务修复

| # | 文件 | 问题 | 状态 |
|---|------|------|------|
| B6 | routes/project.py:36,257 | get_projects/get_versions 无分页 | 待修复 |
| B7 | routes/products.py:352 | list_products 无分页 | 待修复 |
| B8 | routes/boq.py:26 | get_boq_items 无分页 | 待修复 |
| B9 | routes/simulation.py:247 | get_correction_templates 无分页 | 待修复 |
| B10 | routes/boq.py:48-70 | save_boq_items 无事务包裹 | 待修复 |
| B11 | routes/products.py:306-311 | refresh_products delete/seed 不在同一事务 | 待修复 |

### P3 - to_dict 规范化

| # | 文件 | 问题 | 状态 |
|---|------|------|------|
| B12 | database.py:917-929 | 13 个模型 to_dict 运行时动态注入 | 待重构 |
| B13 | database.py | 18 个模型缺少显式 to_dict() 方法 | 待添加 |

### P4 - 安全加固

| # | 文件 | 问题 | 状态 |
|---|------|------|------|
| B14 | app.py:41 | SECRET_KEY 硬编码回退值 | 待修复 |
| B15 | routes/auth.py:17 | Token 黑名单使用内存 set（应用重启丢失） | 待修复 |

---

## 改进总览

| 类别 | 待修复项 | P0 紧急 | P1 重要 | P2 一般 |
|------|---------|---------|---------|---------|
| 前端内存泄漏 | 9 | 9 | 0 | 0 |
| 前端性能防抖 | 6 | 0 | 6 | 0 |
| 前端大组件拆分 | 18 | 0 | 0 | 18 |
| 前端内联事件 | 450+ | 0 | 0 | 450+ |
| 前端其他（echarts/i18n/style） | 94 文件 | 0 | 0 | 94 |
| 后端索引 | 29 FK 列 | 29 | 0 | 0 |
| 后端 N+1/重复查询 | 18 | 0 | 18 | 0 |
| 后端分页/事务 | 7 | 0 | 7 | 0 |
| 后端 to_dict | 31 | 0 | 31 | 0 |
| 后端安全 | 2 | 0 | 2 | 0 |

**预计总工时**: P0 (2-3天) + P1 (5-7天) + P2 (10-15天) = 约 3-4 周
