#!/usr/bin/env node
// 同步所有AI工具规则文件
// 用法: node scripts/sync-ai-rules.js
// 从 .ai-rules-core.md 生成所有AI工具规则文件

const fs = require('fs');
const path = require('path');

const CORE_FILE = '.ai-rules-core.md';
const AI_FILES = [
  '.cursorrules',
  '.github/copilot-instructions.md',
  'CLAUDE.md',
  '.continue/continue.yaml',
  '.windsurfrules',
  'AGENTS.md',
];

function main() {
  const corePath = path.join(__dirname, '..', CORE_FILE);
  
  if (!fs.existsSync(corePath)) {
    console.error(`ERROR: ${CORE_FILE} not found`);
    process.exit(1);
  }

  const coreContent = fs.readFileSync(corePath, 'utf8');
  let synced = 0;
  let errors = 0;

  for (const file of AI_FILES) {
    const filePath = path.join(__dirname, '..', file);
    try {
      // 根据文件格式调整头部
      let content = coreContent;
      
      if (file.endsWith('.yaml')) {
        // Continue YAML 格式
        content = `# AI Code Rules\n# Auto-generated from ${CORE_FILE} - DO NOT EDIT MANUALLY\n\nrules:\n  - name: code-standards\n    description: "Follow project code standards"\n    content: |\n${coreContent.split('\n').map(l => '      ' + l).join('\n')}`;
      } else if (file === 'AGENTS.md') {
        // AGENTS.md 保留原有头部结构
        content = `# 项目代码规范\n\n所有开发者（人类和 AI）必须遵守以下规范。\n\n## 快速检查清单\n\n修改代码前自查：\n\n- [ ] 所有文本使用 $t() 国际化，无硬编码\n- [ ] 无内联事件处理器 (onfocus/onblur/onmouseover/onmouseout)\n- [ ] 无内联 style 属性，使用 CSS 类\n- [ ] 组件不超过 400 行\n- [ ] ECharts 实例在 onUnmounted 中 dispose\n- [ ] resize 监听器在 onUnmounted 中移除\n- [ ] deep watch 有防抖\n- [ ] 后端查询有索引，无 N+1\n- [ ] 列表查询有分页\n\n## 完整规范\n\n详见 [CODE_STYLE.md](./CODE_STYLE.md)\n\n## AI 工具配置\n\n本项目已配置以下 AI 工具的规则文件，确保代码规范一致：\n\n- \`.cursorrules\` - Cursor\n- \`.github/copilot-instructions.md\` - GitHub Copilot\n- \`CLAUDE.md\` - Claude Code / opencode\n- \`.continue/continue.yaml\` - Continue\n- \`.windsurfrules\` - Windsurf\n\n所有 AI 工具读取同一套规范，无需手动指定。\n\n---\n\n${coreContent}`;
      } else {
        // 其他 Markdown 文件直接同步
        content = `# Project Code Standards\n\nYou are a professional frontend/backend AI developer. Follow these rules when generating code:\n\n${coreContent}`;
      }

      fs.writeFileSync(filePath, content, 'utf8');
      console.log(`SYNCED: ${file}`);
      synced++;
    } catch (err) {
      console.error(`ERROR syncing ${file}: ${err.message}`);
      errors++;
    }
  }

  console.log(`\nDone: ${synced} synced, ${errors} errors`);
  
  if (errors > 0) {
    process.exit(1);
  }
}

main();
