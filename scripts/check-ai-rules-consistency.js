#!/usr/bin/env node
// 检查AI工具规则文件的一致性
// 用法: node scripts/check-ai-rules-consistency.js

const fs = require('fs');
const path = require('path');

const SOURCE_FILE = '.cursorrules';
const TARGET_FILES = [
  'AGENTS.md',
  '.continue/continue.yaml',
];

function normalize(content) {
  // 移除头部差异和空白，只比较核心规则内容
  return content
    .replace(/#.*/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function extractRules(content) {
  // 提取 Mandatory Rules 部分的关键规则文本
  const rules = [];
  const lines = content.split('\n');
  let inRules = false;
  for (const line of lines) {
    if (line.includes('Mandatory Rules')) {
      inRules = true;
      continue;
    }
    if (inRules && line.match(/^#/)) {
      break;
    }
    if (inRules && line.trim().match(/^\d+\./)) {
      rules.push(line.trim());
    }
  }
  return rules.join(' ');
}

function main() {
  const sourcePath = path.join(__dirname, '..', SOURCE_FILE);

  if (!fs.existsSync(sourcePath)) {
    console.error(`ERROR: ${SOURCE_FILE} not found`);
    process.exit(1);
  }

  const sourceContent = fs.readFileSync(sourcePath, 'utf8');
  const sourceRules = extractRules(sourceContent);
  let inconsistencies = 0;
  let missing = 0;

  console.log('Checking AI rules consistency...\n');

  for (const file of TARGET_FILES) {
    const filePath = path.join(__dirname, '..', file);

    if (!fs.existsSync(filePath)) {
      console.log(`MISSING: ${file}`);
      missing++;
      continue;
    }

    const fileContent = fs.readFileSync(filePath, 'utf8');
    const fileRules = extractRules(fileContent);

    if (fileRules === sourceRules) {
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
