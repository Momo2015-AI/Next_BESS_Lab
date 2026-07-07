import pathlib, re
from collections import Counter

val_counter = Counter()
files = list(pathlib.Path('.').rglob('*.vue'))
for p in files:
    for ln in p.read_text(encoding='utf-8').splitlines():
        if re.search(r'v-bind:style=|:style=', ln):
            continue
        for m in re.finditer(r'style="([^"]*)"', ln):
            s = re.sub(r'\s+', ' ', m.group(1).strip())
            val_counter[s] += 1

def make_class(val):
    parts = []
    for decl in val.split(';'):
        decl = decl.strip()
        if not decl:
            continue
        if ':' not in decl:
            continue
        prop, _, v = decl.partition(':')
        prop = prop.strip().replace('-', ' ').strip()
        # tokenize
        toks = re.findall(r'[a-zA-Z0-9_-]+', v)
        parts.append(prop + '-' + '-'.join(toks))
    return 'is-' + '__'.join(parts)

mapping = {}
for val, c in val_counter.most_common():
    mapping[val] = make_class(val)

# 打印前 30 个映射，供人工确认命名合理
for i, (val, cls) in enumerate(mapping.items()):
    if i >= 30:
        break
    print(f'{cls}')
    print(f'   <- {val}  (x{val_counter[val]})')
