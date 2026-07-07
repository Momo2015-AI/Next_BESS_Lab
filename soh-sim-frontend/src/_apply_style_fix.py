import pathlib, re, sys

ROOT = pathlib.Path('.')
DRY = '--dry-run' in sys.argv
TARGETS = [a for a in sys.argv[1:] if a.endswith('.vue')]
VUES = [pathlib.Path(a) for a in TARGETS] if TARGETS else list(ROOT.rglob('*.vue'))

# ---------- 1. 收集所有唯一内联 style 值（排除 :style 动态绑定） ----------
val_counter = {}
for p in VUES:
    for ln in p.read_text(encoding='utf-8').splitlines():
        if re.search(r'v-bind:style=|:style=', ln):
            continue
        for m in re.finditer(r'style="([^"]*)"', ln):
            s = re.sub(r'\s+', ' ', m.group(1).strip())
            val_counter[s] = val_counter.get(s, 0) + 1

# ---------- 2. 手写语义映射（高频，覆盖 ~85%） ----------
MANUAL = {
    'color: var(--color-text-muted)': 'text-muted',
    'color: var(--color-text-secondary)': 'text-secondary',
    'color: var(--color-text)': 'text-default',
    'color: var(--color-accent-secondary)': 'text-accent-2',
    'background-color: var(--color-card); border: 1px solid var(--color-border)': 'card-bordered',
    'color: var(--color-accent)': 'text-accent',
    'background-color: var(--color-card-dark)': 'bg-card-dark',
    'color: var(--color-danger)': 'text-danger',
    'color: var(--color-text-muted); border-bottom: 1px solid var(--color-border)': 'text-muted border-b',
    'color: var(--color-warning)': 'text-warning',
    'color: var(--color-accent); border-color: var(--color-accent)': 'text-accent border-accent',
    'background: var(--color-accent-glow); color: var(--color-accent)': 'bg-accent-glow text-accent',
    'background-color: var(--color-card-dark); border: 1px solid var(--color-border)': 'bg-card-dark border-card',
    'background-color: var(--color-accent-secondary); color: white': 'bg-accent-2 text-white',
    'color: var(--color-text-secondary); border-bottom: 1px solid var(--color-border)': 'text-secondary border-b',
    'color: var(--color-success)': 'text-success',
    'min-height: 300px; background-color: var(--color-card); border: 1px solid var(--color-border)': 'min-h-300 card-bordered',
    'background: var(--color-input-bg)': 'bg-input',
    'background-color: var(--color-accent); color: white': 'bg-accent text-white',
    'background: var(--color-card-dark); border: 1px solid var(--color-border)': 'bg-card-dark border-card',
    'border-bottom: 1px solid var(--color-border)': 'border-b',
    'background-color: var(--color-accent-secondary)': 'bg-accent-2',
    'background-color: var(--color-input-bg-dark)': 'bg-input-dark',
    'background-color: var(--color-accent)': 'bg-accent',
    'background-color: var(--color-input-bg)': 'bg-input',
    'width: 50px': 'w-50',
    'background-color: var(--color-input-bg-dark); color: var(--color-text)': 'bg-input-dark text-default',
    'border-collapse: collapse': 'border-collapse',
    'border-color: var(--color-border)': 'border-default',
    'accent-color: var(--color-accent-secondary)': 'accent-accent-2',
    'color: var(--color-text-muted); width: 72px': 'text-muted w-72',
    'height: 280px': 'h-280',
    'font-weight: bold; color: var(--color-text)': 'font-bold text-default',
    'background-color: var(--color-success)': 'bg-success',
    'background-color: var(--color-warning)': 'bg-warning',
    'background-color: var(--color-danger)': 'bg-danger',
    'background: var(--color-bg-secondary); border: 1px solid var(--color-border)': 'bg-secondary border-card',
    'font-weight:bold;margin-bottom:8px;': 'font-bold mb-8',
    'border-top:1px solid #eee;margin-top:6px;padding-top:6px;': 'border-t-eee mt-6 pt-6',
    'opacity: 0.5; cursor: not-allowed': 'opacity-50 not-allowed',
}

# ---------- 3. 长尾自动兜底 ----------
def clean(tok):
    m = re.match(r'var\((--[\w-]+)\)$', tok.strip())
    if m:
        return m.group(1).lstrip('-').replace('_', '-')
    return re.sub(r'[^a-zA-Z0-9]+', '-', tok).strip('-')

def make_class(val):
    decls = [d.strip() for d in val.split(';') if d.strip()]
    segs = []
    for d in decls:
        if ':' not in d:
            continue
        prop, _, v = d.partition(':')
        prop = re.sub(r'[^a-zA-Z]+', '-', prop.strip()).strip('-')
        vtoks = [clean(t) for t in re.split(r'[\s,()]+', v) if t.strip()]
        segs.append(prop + '-' + '-'.join(vtoks))
    return 'u-' + '-'.join(segs)

mapping = {}
unmapped = []
for v in val_counter:
    if v in MANUAL:
        mapping[v] = MANUAL[v]
    else:
        mapping[v] = make_class(v)
        unmapped.append(v)

# ---------- 4. 写 CSS ----------
css_blocks = []
for val, cls in sorted(mapping.items(), key=lambda x: x[1]):
    if cls in [c for c in MANUAL.values()]:
        # 手写类：原样写
        decls = '; '.join(d.strip() for d in val.split(';') if d.strip())
        css_blocks.append(f'.{cls} {{ {decls} }}')
    else:
        decls = '; '.join(d.strip() for d in val.split(';') if d.strip())
        css_blocks.append(f'.{cls} {{ {decls} }}')
css_text = '/* INLINE-STYLE UTILITY CLASSES (auto-generated) */\n' + '\n'.join(css_blocks) + '\n'

if not DRY:
    shared = ROOT / 'assets/styles/shared.css'
    orig = shared.read_text(encoding='utf-8')
    marker = '\n/* ==== INLINE-STYLE UTILITY CLASSES ==== */\n'
    if 'INLINE-STYLE UTILITY CLASSES' not in orig:
        shared.write_text(encoding='utf-8', data=orig.rstrip() + marker + css_text)
    else:
        new_orig = re.split(r'/\* ==== INLINE-STYLE UTILITY CLASSES.*', orig)[0].rstrip()
        shared.write_text(encoding='utf-8', data=new_orig + marker + css_text)

# ---------- 5. 替换 .vue 中的 style="X" ----------
replaced = 0
for p in VUES:
    lines = p.read_text(encoding='utf-8').splitlines()
    new_lines = []
    for ln in lines:
        if re.search(r'v-bind:style=|:style=', ln):
            new_lines.append(ln)
            continue
        styles = re.findall(r'style="([^"]*)"', ln)
        if not styles:
            new_lines.append(ln)
            continue
        classes_to_add = []
        for s in styles:
            val = re.sub(r'\s+', ' ', s.strip())
            cls = mapping.get(val)
            if cls:
                classes_to_add.append(cls)
                replaced += 1
        new_ln = re.sub(r'\s*style="[^"]*"', '', ln)
        if classes_to_add:
            if 'class="' in new_ln:
                new_ln = re.sub(
                    r'class="([^"]*)"',
                    lambda m: f'class="{(m.group(1).strip() + " " + " ".join(classes_to_add)).strip()}"',
                    new_ln,
                    count=1,
                )
            else:
                new_ln = new_ln.rstrip()
                if not new_ln.endswith('>'):
                    new_ln += ' '
                new_ln += f'class="{" ".join(classes_to_add)}"'
        if DRY and new_ln != ln:
            with open('_dryrun.log', 'a', encoding='utf-8') as f:
                f.write(f'[{p.name}] BEFORE: {ln.strip()[:130]}\n')
                f.write(f'[{p.name}] AFTER : {new_ln.strip()[:130]}\n\n')
        new_lines.append(new_ln)
    if not DRY:
        p.write_text(encoding='utf-8', data='\n'.join(new_lines) + '\n')

print('unique values total:', len(val_counter))
print('mapped by manual:', len(val_counter) - len(unmapped))
print('mapped by auto :', len(unmapped))
print('total style= replaced:', replaced)
print('css classes written:', len(css_blocks) if not DRY else 'SKIP(dry)')
