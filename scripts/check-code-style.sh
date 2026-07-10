#!/bin/bash
# 代码规范自动检查脚本
# 用法: bash scripts/check-code-style.sh

set -e

echo "========================================="
echo "  代码规范检查"
echo "========================================="
echo ""

# 检查前端
echo "[1/3] 检查前端代码规范..."
cd soh-sim-frontend

# 检查硬编码中文
echo "  - 检查硬编码中文..."
CHINESE_FILES=$(grep -rl '[\x{4e00}-\x{9fff}]' src/ --include="*.vue" --include="*.js" 2>/dev/null | grep -v node_modules | grep -v i18n || true)
if [ -n "$CHINESE_FILES" ]; then
  echo "  WARNING: 以下文件包含硬编码中文（应使用 \$t() 国际化）:"
  echo "$CHINESE_FILES"
fi

# 检查内联事件处理器
echo "  - 检查内联事件处理器..."
INLINE_EVENTS=$(grep -rn 'onfocus=\|onblur=\|onmouseover=\|onmouseout=' src/ --include="*.vue" 2>/dev/null || true)
if [ -n "$INLINE_EVENTS" ]; then
  echo "  WARNING: 发现内联事件处理器（应改用 CSS :focus-visible 或 @focus/@blur）:"
  echo "$INLINE_EVENTS"
fi

# 检查组件大小
echo "  - 检查组件大小..."
LARGE_FILES=$(find src/ -name "*.vue" -exec wc -l {} \; | awk '$1 > 400 {print $2 ":" $1 " lines"}')
if [ -n "$LARGE_FILES" ]; then
  echo "  WARNING: 以下组件超过 400 行，应拆分:"
  echo "$LARGE_FILES"
fi

echo "  前端检查完成"
echo ""

# 检查后端
echo "[2/3] 检查后端代码规范..."
cd ../soh-sim-backend

# 检查 Python 格式
echo "  - 检查 Python 代码格式..."
if command -v black &> /dev/null; then
  black --check . || echo "  WARNING: 后端代码格式不符合 black 规范"
fi

# 检查 N+1 查询模式
echo "  - 检查 N+1 查询模式..."
N1_PATTERNS=$(grep -rn '\.query\.get\|\.filter_by.*\.all' routes/ services/ 2>/dev/null | grep -v joinedload | grep -v selectinload | head -20 || true)
if [ -n "$N1_PATTERNS" ]; then
  echo "  INFO: 以下查询可能需要注意性能（建议检查是否使用 joinedload/selectinload）:"
  echo "$N1_PATTERNS"
fi

echo "  后端检查完成"
echo ""

# 检查国际化文件
echo "[3/3] 检查国际化文件..."
cd ..
if [ -f "soh-sim-frontend/src/i18n/zh.js" ] && [ -f "soh-sim-frontend/src/i18n/en.js" ]; then
  ZH_COUNT=$(grep -c "'" soh-sim-frontend/src/i18n/zh.js || echo 0)
  EN_COUNT=$(grep -c "'" soh-sim-frontend/src/i18n/en.js || echo 0)
  echo "  zh.js: $ZH_COUNT translations"
  echo "  en.js: $EN_COUNT translations"
  if [ "$ZH_COUNT" != "$EN_COUNT" ]; then
    echo "  WARNING: 中英文翻译数量不一致"
  fi
else
  echo "  ERROR: 国际化文件缺失"
  exit 1
fi

echo ""
echo "========================================="
echo "  检查完成"
echo "========================================="
