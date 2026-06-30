# 需求实施计划

- [x] 1. 后端：创建统一计算管道服务层 (R8.1, R8.3)
  - 在 `soh-sim-backend/services/pipeline.py` 中从 app.py 提取并整合计算逻辑
  - 实现 Arrhenius 衰减预测函数（日历老化 + 循环老化）
  - 实现 25 年容量对账函数（存量评估 + 补容老化位移 + 达标判定）
  - 实现财务指标计算函数（NPV/IRR/LCOS/DSCR/ROI）
  - 实现统一入口 `calculate_full_pipeline(systemParams, degradation, financial)` 按顺序调用上述函数

- [ ]* 1.1 为 pipeline.py 编写单元测试
  - 测试 Arrhenius 衰减预测（给定已知参数，验证输出 SOH 数组长度=26、值域[0,100]）
  - 测试容量对账逻辑（给定固定 SOH/RTE/DOD，验证 totalAcUsable >= 0）
  - 测试财务指标计算（给定固定现金流，验证 NPV/IRR 符号一致性）

- [x] 2. 后端：实现 `/api/pipeline/calculate` 路由 (R8.1, R8.3, R4.6)
  - 在 `soh-sim-backend/routes/pipeline.py` 创建 Blueprint
  - 实现 POST 处理器：参数校验 → 调用 pipeline 服务 → 返回 PipelineResponse
  - 输入校验：systemParams 必填字段检查（ratedEnergy/initContainerQty/duration/temperature/requiredEnergy）
  - 字段级错误信息返回 `{error, field, value, constraint}`，状态码 400
  - 异步处理：计算超 3 秒返回 202 + `{taskId}`，实现 GET `/api/pipeline/task/<taskId>` 查询
  - 在 app.py 中注册 pipeline Blueprint
  - 确保现有 `/api/soh/calculate`、`/api/health` 行为不变 (R8 向后兼容)

- [ ]* 2.1 为 pipeline 路由编写集成测试
  - 提交完整参数验证返回 200 且 response 包含所有 16 个字段
  - 提交缺失 ratedEnergy 参数验证返回 400 及 field 级错误
  - 验证 `/api/soh/calculate` 仍正常响应

- [x] 3. 检查点 - 后端 pipeline API 就绪，所有测试通过

- [x] 4. 前端：安装 Pinia 并创建全局 Store (R7.1, R7.3)
  - `cd soh-sim-frontend && npm install pinia`
  - 在 `src/main.js` 中注册 Pinia 插件
  - 创建 `src/stores/` 目录
  - 创建 `src/stores/bess.js`：实现 useBessStore，包含 state（project/survey/systemParams/selectedProducts/degradation/results/financial/phases）
  - 实现 getters（simulationDefaults 从 survey 派生默认仿真参数）
  - 实现 actions（updatePhaseParams 更新阶段参数并自动标记完成状态；runPipeline 调用 POST /api/pipeline/calculate 并写入 results 和 financial.metrics）
  - 创建 `src/constants.js`：定义 `NUM_YEARS = 26` 全局常量

- [ ]* 4.1 为 Pinia store 编写单元测试
  - 测试 simulationDefaults getter 在 survey 缺失时的默认值回退
  - 测试 updatePhaseParams 更新后对应 phase.status 变为 completed
  - 测试 runPipeline 在 API 返回 400 时的错误处理行为

- [x] 5. 前端：搭建 Vue Router 五阶段路由 (R1.1, R7.2)
  - 在 `src/router/index.js` 中定义路由表：`/`、`/phase1`、`/phase2`、`/phase3`、`/phase4`、`/phase5`
  - 创建所有 Phase 页面占位组件（Phase1Page.vue ~ Phase5Page.vue），初始渲染阶段标题
  - 在 App.vue 中将 v-show 切换替换为 `<router-view />`
  - 确保路由切换后组件状态通过 Pinia store 保持

- [x] 6. 检查点 - 前端路由框架就绪，可通过 URL 导航到各阶段页面

- [x] 7. 前端：重构首页为流程总览仪表盘 (R1.4)
  - 重构 `src/components/HomePage.vue`
  - 展示五阶段进度条（Phase 1~5），每个阶段显示 pending/in_progress/completed 状态图标
  - 展示项目列表卡片（项目名称、状态、最后修改时间），支持按名称搜索
  - 展示关键指标摘要（当前 SOH 值、EOL 预测时间、NPV/IRR 汇总）

- [x] 8. 前端：重构侧边导航栏 (R1.1, R1.2, R1.3)
  - 重构 `src/components/Sidebar.vue`
  - 将导航项从"首页/基础层/方案层/工具"改为"项目立项/系统设计/性能分析/经济评估/成果输出"
  - 每项旁显示阶段完成状态图标（pending/in_progress/completed）
  - 点击导航项时使用 `vue-router` 跳转（`router.push`），移除旧的 emit('navigate') 机制

- [x] 9. 前端：创建 Phase1Page 项目立项页面 (R2.1, R2.2, R2.3, R2.4, R2.5)
  - 在 Phase1Page.vue 中实现三步引导流程：
    - 步骤 1.1 — 项目调研表：嵌入 SurveyForm.vue 组件，保留现有表单逻辑
    - 步骤 1.2 — 选址与资源评估：嵌入 RunningConditions.vue 组件（提取选址/电网相关部分）
    - 步骤 1.3 — 需求确认：新增加总卡片，汇总前两步的关键参数（额定能量、储能时长、功率需求）
  - 子步骤间通过"下一步/上一步"按钮导航，最后一步的"确认提交"按钮调用 bessStore.updatePhaseParams('phase1', surveyData)
  - 实现必填字段校验（项目名称、额定能量、温度），为空时禁止进入下一步并高亮缺失字段 (R2.5)
  - 调研表数据通过 bessStore 持久化到后端 `/api/survey/submit` (R2.2)
  - 提交后自动将 duration/cyclesPerDay/requiredEnergy/temperature 映射到 bessStore.systemParams (R2.3)

- [x] 10. 前端：创建 Phase2Page 系统设计页面 (R3.1, R3.2, R3.3, R3.4)
  - 在 Phase2Page.vue 中实现四步引导流程：
    - 步骤 2.1 — 设备选型库：嵌入 ProductConfig.vue 组件
    - 步骤 2.2 — 直流侧设计：嵌入 BatteryDCDesign.vue 组件
    - 步骤 2.3 — 交流侧设计：嵌入 PcsACDesign.vue 组件
    - 步骤 2.4 — 系统集成配置：嵌入 BatteryPCSConfig.vue 组件
  - 子步骤间通过"下一步/上一步"按钮导航
  - 完成系统设计后，将 ratedEnergy/initContainerQty/initPcsQty/pcsPower/duration 汇总写入 bessStore.systemParams (R3.4)

- [x] 11. 前端：创建 Phase3Page 性能分析页面 (R4.1, R4.2, R4.3, R4.4)
  - 在 Phase3Page.vue 中实现四步引导流程：
    - 步骤 3.1 — 衰减预测：嵌入 SimulationLab.vue 组件，其输出接入 bessStore 而非 App.vue
    - 步骤 3.2 — 容量对账：嵌入 MatrixTable.vue 组件，数据源改为 bessStore.results
    - 步骤 3.3 — 可视化分析：嵌入 SohChart.vue 组件，数据源改为 bessStore.results 和 bessStore.degradation
    - 步骤 3.4 — 多场景对比：嵌入 ScenarioCompare.vue 组件
  - 添加"运行计算管道"按钮，调用 bessStore.runPipeline() → POST /api/pipeline/calculate
  - 计算完成后自动刷新 MatrixTable/SohChart 图表数据 (R4.4)
  - 实现计算进行中 loading 状态展示和异步轮询（>3秒时的 202 处理）(R4.6)
  - 支持 DataInjection 组件作为步骤 3.1 的手动覆写入口 (R4.1)

- [x] 12. 前端：创建 Phase4Page 经济评估页面 (R5.1, R5.2, R5.3, R5.4, R5.5)
  - 在 Phase4Page.vue 中实现五步引导流程：
    - 步骤 4.1 — 投资估算 (CAPEX)：新增表单组件，输入设备采购成本/EPC费用/前期开发费，写入 bessStore.financial.capex
    - 步骤 4.2 — 运营模型 (OPEX)：新增表单组件，输入运维/保险/电网费用，写入 bessStore.financial.opex
    - 步骤 4.3 — 收入模型：提取 FinancialDashboard.vue 中收入相关部分，写入 bessStore.financial.revenue
    - 步骤 4.4 — 财务指标：提取 FinancialDashboard.vue 中指标展示部分，数据源改为 bessStore.financial.metrics
    - 步骤 4.5 — 敏感性分析：嵌入 SensitivityAnalysis.vue 组件
  - 当 bessStore.results 变化时（Phase 3 重新计算），自动刷新财务指标 (R5.2)
  - 财务指标表格以红/绿/黄色标识达标状态（IRR>=8% 为绿色）(R5.5)

- [x] 13. 前端：创建 Phase5Page 成果输出页面 (R6.1, R6.2, R6.3, R6.4)
  - 在 Phase5Page.vue 中实现四步引导流程：
    - 步骤 5.1 — 技术报告：新增 ReportPage 组件，调用 POST `/api/report/technical` 生成 PDF 并触发下载 (R6.3)
    - 步骤 5.2 — 设备清单：新增 BomPage 组件，调用 POST `/api/report/bom` 生成 PDF 并触发下载
    - 步骤 5.3 — 数据导出：嵌入 DataExport.vue 组件
    - 步骤 5.4 — 项目存档：实现"保存项目"按钮，将 bessStore 全量数据通过 `/api/project/sync-params` 持久化到数据库 (R6.4)

- [x] 14. 前端：清理 App.vue (R7.1, R7.4)
  - 移除 App.vue 中的 `calculate()` 函数及其内部计算逻辑 (R7.4)
  - 移除 5 个 deep watch（params/soh/rte/dod/augQty 变更监听）
  - 移除 `v-show` tab 切换逻辑和 `currentTab` ref
  - 移除组件 import 和 props/events 传递（已由各 PhasePage 管理）
  - 保留 Toast 通知机制（showToast）和项目同步基础逻辑
  - 替换主内容区为 `<router-view />`

- [x] 15. 前端：完善 Phase 子步骤导航与进度追踪 (R1.2, R1.3)
  - 确保所有 PhasePage 使用统一的子步骤导航组件（上一步/下一步按钮 + 步骤指示器）
  - 当 Phase 内最后一步完成时，更新 bessStore.phases[phase].status 为 completed
  - 首页进度条和侧边栏导航状态指示器实时反映 bessStore.phases 状态

- [x] 16. 检查点 - 全流程端到端验证
  - 确保 `/api/pipeline/calculate` 返回 16 字段完整 JSON
  - 确保五阶段页面可通过导航依次访问
  - 确保 Phase1→Phase2→Phase3→Phase4→Phase5 数据通过 Pinia store 连贯流转
  - 确保现有功能（产品库 CRUD、文件上传解析、健康检查）未退化
