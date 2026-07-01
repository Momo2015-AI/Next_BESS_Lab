#!/usr/bin/env node
// 检查国际化覆盖完整性
// 用法: node scripts/check-i18n.js

const fs = require('fs');
const path = require('path');

const SRC_DIR = path.join(__dirname, '..', 'soh-sim-frontend', 'src');

function findVueFiles(dir) {
  const files = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== 'node_modules') {
      files.push(...findVueFiles(fullPath));
    } else if (entry.name.endsWith('.vue') || entry.name.endsWith('.js')) {
      files.push(fullPath);
    }
  }
  
  return files;
}

function main() {
  console.log('Checking i18n coverage...\n');
  
  const files = findVueFiles(SRC_DIR);
  let issues = 0;
  let checked = 0;

  for (const file of files) {
    const content = fs.readFileSync(file, 'utf8');
    checked++;

    // 检查是否有硬编码中文
    const chinesePattern = /[\u4e00-\u9fff]/;
    const hasChinese = chinesePattern.test(content);
    
    // 检查是否使用 $t()
    const hasI18n = content.includes('$t(') || content.includes('useI18n');
    
    // 忽略 i18n 文件本身
    if (file.includes('i18n')) continue;

    if (hasChinese && !hasI18n) {
      console.log(`ISSUE: ${path.relative(SRC_DIR, file)}`);
      console.log(`  - Contains Chinese text but no $t() usage`);
      issues++;
    }
  }

  console.log(`\nChecked ${checked} files.`);
  console.log(`Found ${issues} files with hard-coded Chinese.`);

  if (issues > 0) {
    console.log('\nThese files need i18n migration.');
    process.exit(1);
  }
}

main();
