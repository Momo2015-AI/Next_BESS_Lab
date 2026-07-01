# 项目代码规范

所有开发者（人类和 AI）必须遵守以下规范。

## 快速检查清单

修改代码前自查：

- [ ] 所有文本使用 $t() 国际化，无硬编码
- [ ] 无内联事件处理器 (onfocus/onblur/onmouseover/onmouseout)
- [ ] 无内联 style 属性，使用 CSS 类
- [ ] 组件不超过 400 行
- [ ] ECharts 实例在 onUnmounted 中 dispose
- [ ] resize 监听器在 onUnmounted 中移除
- [ ] deep watch 有防抖
- [ ] 后端查询有索引，无 N+1
- [ ] 列表查询有分页

## 完整规范

详见 [CODE_STYLE.md](./CODE_STYLE.md)

## AI 工具配置

本项目已配置以下 AI 工具的规则文件，确保代码规范一致：

- `.cursorrules` - Cursor
- `.github/copilot-instructions.md` - GitHub Copilot
- `CLAUDE.md` - Claude Code / opencode
- `.continue/continue.yaml` - Continue
- `.windsurfrules` - Windsurf

所有 AI 工具读取同一套规范，无需手动指定。
