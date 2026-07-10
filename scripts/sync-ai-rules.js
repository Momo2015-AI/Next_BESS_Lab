#!/usr/bin/env node
// 同步所有AI工具规则文件
// 用法: node scripts/sync-ai-rules.js
// 从 .cursorrules 生成 AGENTS.md 和 .continue/continue.yaml

const fs = require('fs');
const path = require('path');

const SOURCE_FILE = '.cursorrules';
const TARGETS = [
  {
    file: 'AGENTS.md',
    transform: (content) => {
      return `# 项目代码规范

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

## AI 工具规则

本项目使用 \`.cursorrules\` 作为 AI 编码规则的唯一权威来源。规则通过 \`scripts/sync-ai-rules.js\` 自动同步。

---

${content}`;
    }
  },
  {
    file: '.continue/continue.yaml',
    transform: (content) => {
      const indented = content.split('\n').map(l => '      ' + l).join('\n');
      return `# AI Code Rules
# Auto-generated from .cursorrules - DO NOT EDIT MANUALLY

rules:
  - name: code-standards
    description: "Follow project code standards"
    content: |
${indented}`;
    }
  }
];

function main() {
  const sourcePath = path.join(__dirname, '..', SOURCE_FILE);

  if (!fs.existsSync(sourcePath)) {
    console.error(`ERROR: ${SOURCE_FILE} not found`);
    process.exit(1);
  }

  const sourceContent = fs.readFileSync(sourcePath, 'utf8');
  let synced = 0;
  let errors = 0;

  for (const target of TARGETS) {
    const filePath = path.join(__dirname, '..', target.file);
    try {
      const content = target.transform(sourceContent);
      fs.writeFileSync(filePath, content, 'utf8');
      console.log(`SYNCED: ${target.file}`);
      synced++;
    } catch (err) {
      console.error(`ERROR syncing ${target.file}: ${err.message}`);
      errors++;
    }
  }

  console.log(`\nDone: ${synced} synced, ${errors} errors`);

  if (errors > 0) {
    process.exit(1);
  }
}

main();
