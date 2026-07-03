"""批量替换 Vue 文件中硬编码颜色值为 CSS 变量"""
import re
import sys
import os

BASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'soh-sim-frontend', 'src')

# 替换规则：(模式, 替换字符串, 文件列表/glob)
replacements = [
    # EpcModules.vue
    (r"style=\"border-color: #e0e0e0\"", 'style="border-color: var(--color-border)"', ['components/EpcModules.vue']),
    (r'style="color: #2f5496"', 'style="color: var(--color-accent)"', ['components/EpcModules.vue']),
    (r'style="color: #2F5496"', 'style="color: var(--color-accent)"', ['components/EpcModules.vue']),
    (r'style="color: #999"', 'style="color: var(--color-text-muted)"', ['components/EpcModules.vue']),
    (r'style="color: #666"', 'style="color: var(--color-text-secondary)"', ['components/EpcModules.vue']),
    (r'style="background-color: #2f5496"', 'style="background: var(--color-accent)"', ['components/EpcModules.vue']),
    (r'style="border-color: #bfdbfe"', 'style="border-color: var(--color-accent-glow)"', ['components/EpcModules.vue']),
    (r"borderColor: '#2F5496'", "borderColor: 'var(--color-accent)'", ['components/EpcModules.vue']),
]

for pattern, replacement, files in replacements:
    for f in files:
        path = os.path.join(BASE, f)
        with open(path, 'r', encoding='utf-8') as fh:
            content = fh.read()
        count = len(re.findall(pattern, content))
        if count:
            content = re.sub(pattern, replacement, content)
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(content)
            print(f'[{f}] {count} occurrences → {replacement[:40]}...')
        else:
            print(f'[{f}] no match for pattern')

print('Done.')
