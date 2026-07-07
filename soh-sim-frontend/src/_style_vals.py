import pathlib, re
from collections import Counter

ROOT = pathlib.Path('.')
val_counter = Counter()
for p in ROOT.rglob('*.vue'):
    for ln in p.read_text(encoding='utf-8').splitlines():
        if re.search(r'v-bind:style=|:style=', ln):
            continue
        for m in re.finditer(r'style="([^"]*)"', ln):
            s = re.sub(r'\s+', ' ', m.group(1).strip())
            val_counter[s] += 1

total = sum(val_counter.values())
print(f'TOTAL hard inline style: {total}')
print(f'UNIQUE values: {len(val_counter)}')
print()
print('=== TOP 40 by frequency ===')
cum = 0
for i, (val, cnt) in enumerate(val_counter.most_common(40), 1):
    cum += cnt
    print(f'{i:>2}. [{cnt:>3} | cum {cum/total*100:5.1f}%] {val}')
print()
print('=== values with count >= 5 ===')
for val, cnt in sorted(val_counter.items(), key=lambda x: -x[1]):
    if cnt >= 5:
        print(f'[{cnt:>3}] {val}')
