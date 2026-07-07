import pathlib, re

# 清洗 CSS 变量/值 -> kebab token
def clean(tok):
    # var(--color-accent) -> color-accent ; #fff -> fff ; 250px -> 250px
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
        prop = prop.strip().replace('-', '-')  # keep
        prop = re.sub(r'[^a-zA-Z]+', '-', prop).strip('-')
        vtoks = [clean(t) for t in re.split(r'[\s,()]+', v) if t.strip()]
        segs.append(prop + '-' + '-'.join(vtoks))
    return 'u-' + '-'.join(segs)

if __name__ == '__main__':
    # 仅做演示：打印几个样例
    samples = [
        'color: var(--color-text-muted)',
        'background-color: var(--color-card); border: 1px solid var(--color-border)',
        'background: var(--color-card); border: 1px solid var(--color-border); border-radius: var(--radius-md); min-height: 250px',
        'width: 50px',
    ]
    for s in samples:
        print(make_class(s), '<-', s)
