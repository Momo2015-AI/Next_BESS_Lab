#!/usr/bin/env node
// 检查所有AI工具规则文件的一致性
// 用法: node scripts/check-ai-rules-consistency.js

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

function normalize(content) {
  // 移除头部差异，只比较核心内容
  return content
    .replace(/#.*/g, '')  // 移除注释行
    .replace(/\s+/g, ' ')  // 合并空白
    .trim();
}

function main() {
  const corePath = path.join(__dirname, '..', CORE_FILE);
  
  if (!fs.existsSync(corePath)) {
    console.error(`ERROR: ${CORE_FILE} not found`);
    console.log('Run: node scripts/sync-ai-rules.js first');
    process.exit(1);
  }

  const coreContent = fs.readFileSync(corePath, 'utf8');
  let inconsistencies = 0;
  let missing = 0;

  console.log('Checking AI rules consistency...\n');

  for (const file of AI_FILES) {
    const filePath = path.join(__dirname, '..', file);
    
    if (!fs.existsSync(filePath)) {
      console.log(`MISSING: ${file}`);
      missing++;
      continue;
    }

    const fileContent = fs.readFileSync(filePath, 'utf8');
    const normalizedCore = normalize(coreContent);
    const normalizedFile = normalize(fileContent);

    // 检查核心内容是否存在于文件中
    if (normalizedFile.includes(normalizedCore.substring(0, 200))) {
      console.log(`OK: ${file}`);
    } else {
      console.log(`INCONSISTENT: ${file}`);
      inconsistencies++;
    }
  }

  console.log(`\nResults: ${missing} missing, ${inconsistencies} inconsistent`);

  if (missing > 0 || inconsistencies > 0) {
    console.log('\nFix by running: node scripts/sync-ai-rules.js');
    process.exit(1);
  }
}

main();
