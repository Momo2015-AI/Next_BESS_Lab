# SOH-SIM — 储能系统仿真平台

> 面向 BESS（电池储能系统）的全生命周期技术经济仿真平台，覆盖从前期调研、方案设计、运行仿真到财务评估的完整业务链路。

**所有开发者（人类和 AI）必须遵守 [CODE_STYLE.md](./CODE_STYLE.md) 中的代码规范。**

---

## 项目结构

```
soh-sim-frontend/       # Vue 3 + Vite 前端 (Tailwind CSS 4)
soh-sim-backend/        # Python + Flask 后端 (SQLAlchemy ORM)
├── services/
│   ├── design/         # 设计引擎 — 自动生成系统配置方案
│   ├── simulation/     # 仿真引擎 — 26年退化曲线 + 能量核算
│   ├── financial/      # 财务引擎 — NPV/IRR/LCOS/DSCR 计算
│   ├── orchestrator.py # 编排器 — 串联三引擎全流程
│   ├── epc/            # EPC 模块 — 电气/土建/消防/SCADA
│   └── pipeline.py     # 核心管线 — SOH/RTE/DOD 退化 + 能量会计
├── routes/             # Flask Blueprint 路由 (~25个)
└── models/             # SQLAlchemy 数据模型
scripts/                # 代码检查与同步脚本
docs/                   # 项目文档
```

---

## 快速开始

```bash
# 前端
cd soh-sim-frontend && npm install && npm run dev

# 后端
cd soh-sim-backend && pip install -r requirements.txt && python app.py
```

---

## 核心架构

### 三引擎编排 (v2.0)

```
Survey 调研参数
    │
    ▼
Design Engine ──→ 多策略设计方案 (经济优先/平衡/性能优先)
    │
    ▼
Simulation Engine ──→ 26年 SOH/RTE/DOD 退化 + 补容策略对比
    │
    ▼
Financial Engine ──→ NPV/IRR/LCOS/投资回收期 + 敏感性分析
    │
    ▼
Orchestrator ──→ 方案对比 + 版本管理
```

### 补容策略对比

- **固定周期** (fixed_periodic) — 每 5 年补容一次
- **按需补容** (on_demand) — 每年检查，SOH 不足时补容
- **超配方案** (overbuild) — 初始多装 20%，前 3 年无需补容

每种策略自动计算完整经济指标（含 Wright 学习率 5%/年递减的补容 CAPEX）。

### 项目版本管理

- 工作流结果自动保存为 `ProjectVersion`
- 支持多版本对比（指标差异 + 雷达图）
- 支持版本回溯（一键恢复到编排器）

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端框架 | Vue 3.5 + Vite 8 + Pinia 3 |
| UI 框架 | Tailwind CSS 4 (玻璃态设计系统) |
| 图表 | ECharts 6 (按需引入) |
| 国际化 | vue-i18n 11 (中/英/阿) |
| 后端框架 | Flask 3 + SQLAlchemy |
| 科学计算 | NumPy + SciPy + Pandas |
| 认证 | JWT Bearer Token |
| 测试 | Vitest (前端) + Pytest (后端) |

---

## 代码规范

详见 [CODE_STYLE.md](./CODE_STYLE.md)（v1.2，当前实际执行标准）。

### 快速检查清单

- [ ] 所有文本使用 `$t()` 国际化
- [ ] 无内联样式/事件处理器
- [ ] 组件 ≤ 400 行
- [ ] ECharts 按需引入 + onUnmounted dispose
- [ ] 后端 FK 有索引，无 N+1 查询
- [ ] 列表查询有分页

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## AI 工具配置

本项目使用 `.cursorrules` 作为 AI 编码规则的唯一权威来源。

| 文件 | 工具 |
|------|------|
| `.cursorrules` | Cursor / ZCode / 通用 AI（**权威源**） |
| `AGENTS.md` | 通用 AI 工具 |
| `.continue/continue.yaml` | Continue |

同步命令：`node scripts/sync-ai-rules.js`

---

## 常用脚本

```bash
# 前端检查
cd soh-sim-frontend
npm run lint          # ESLint
npm run format:check  # Prettier
npm run type-check    # TypeScript
npm run i18n:check    # 国际化覆盖率

# 后端检查
cd soh-sim-backend
black --check .       # 格式
flake8                # Lint

# 全局检查
bash scripts/check-code-style.sh
```
