import pathlib, re

files = list(pathlib.Path('.').rglob('*.vue'))
hard = {}
dyn = {}
for p in files:
    lines = p.read_text(encoding='utf-8').splitlines()
    h = d = 0
    for ln in lines:
        if re.search(r'v-bind:style=|:style=', ln):
            d += 1
        elif re.search(r'style="', ln):
            h += 1
    if h or d:
        hard[p.as_posix()] = h
        dyn[p.as_posix()] = d

print('=== 硬编码 style=" (违规) ===')
tot = 0
for k, v in sorted(hard.items(), key=lambda x: -x[1]):
    tot += v
    print(f'{v:>4}  {k}')
print('TOTAL hard:', tot)
print()
print('=== :style 动态绑定 (合规) ===')
totd = 0
for k, v in sorted(dyn.items(), key=lambda x: -x[1]):
    totd += v
    print(f'{v:>4}  {k}')
print('TOTAL dynamic:', totd)
