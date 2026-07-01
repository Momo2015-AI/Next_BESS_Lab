# SOH-SIM - 储能系统仿真平台

> **所有开发者（人类和 AI）必须遵守 [CODE_STYLE.md](./CODE_STYLE.md) 中的代码规范。**
> **修改代码前必读 [快速检查清单](./CODE_STYLE.md#快速检查清单)。**

## 项目结构

```
soh-sim-frontend/    # Vue 3 前端
soh-sim-backend/     # Flask 后端
CODE_STYLE.md        # 完整代码规范
AGENTS.md            # AI 工具规则索引
CHECKLIST.md         # 提交前检查清单
```

## 快速开始

```bash
# 前端
cd soh-sim-frontend && npm install && npm run dev

# 后端
cd soh-sim-backend && pip install -r requirements.txt && python app.py
```

## 代码规范

详见 [CODE_STYLE.md](./CODE_STYLE.md)

## AI 工具配置

本项目已配置以下 AI 工具的规则文件：

- `.cursorrules` - Cursor
- `.github/copilot-instructions.md` - GitHub Copilot
- `CLAUDE.md` - Claude Code / opencode
- `.continue/continue.yaml` - Continue
- `.windsurfrules` - Windsurf
