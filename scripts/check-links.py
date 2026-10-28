#!/usr/bin/env python3
"""Check that relative links/images in Markdown files exist and catalog.json is consistent.
Usage: python3 scripts/check-links.py   (run from anywhere; exits 1 on any failure)"""
import json, os, re, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bad = []
for dp, dn, fn in os.walk(root):
    dn[:] = [d for d in dn if d not in ('.git', 'node_modules')]
    for f in fn:
        if not f.endswith('.md'): continue
        p = os.path.join(dp, f)
        text = open(p, encoding='utf-8').read()
        text = re.sub(r'```.*?```', '', text, flags=re.S)
        refs = re.findall(r'\]\(([^)\s]+)\)', text) + re.findall(r'(?:src|href)="([^"]+)"', text)
        heads = {re.sub(r'[^\w\- ]', '', h.strip().lower()).replace(' ', '-') for h in re.findall(r'^#+\s+(.*)$', text, flags=re.M)}
        for r in refs:
            if re.match(r'(https?:|mailto:|grokbot:)', r): continue
            if r.startswith('#'):
                if r[1:] not in heads: bad.append(f'{os.path.relpath(p, root)}: missing anchor {r}')
                continue
            t = r.split('#')[0]
            if not t or '<' in t: continue
            if not os.path.exists(os.path.normpath(os.path.join(dp, t))):
                bad.append(f'{os.path.relpath(p, root)}: broken link {r}')
cat = json.load(open(os.path.join(root, 'catalog.json')))
for b in cat:
    for k in ('id', 'title', 'stage', 'summary', 'folder', 'xai_template_url', 'chains_with'):
        if k not in b: bad.append(f'catalog {b.get("id")}: missing {k}')
    d = os.path.join(root, b['folder'])
    if not os.path.isdir(d): bad.append(f'catalog {b["id"]}: folder missing')
    if (b['stage'] == 'launch') != bool(b['xai_template_url']): bad.append(f'catalog {b["id"]}: stage/url mismatch')
    prof = open(os.path.join(d, 'profile.md')).read()
    if f'**Title:** {b["title"]}' not in prof: bad.append(f'catalog {b["id"]}: title differs from profile.md')
    rd = open(os.path.join(d, 'README.md')).read()
    if f'Stage: **{b["stage"]}**' not in rd: bad.append(f'catalog {b["id"]}: README stage differs')
    top = open(os.path.join(root, 'README.md')).read()
    if not re.search(rf'\| {re.escape(b["title"])} \| {b["stage"]} \|', top): bad.append(f'catalog {b["id"]}: root README table row/stage differs')
    if f'stage-{b["stage"]}-' not in top: bad.append(f'catalog {b["id"]}: gallery badge missing')
    if b['xai_template_url'] and b['xai_template_url'] not in top: bad.append(f'catalog {b["id"]}: url missing in root README')
print('\n'.join(bad) or 'OK: all relative links, anchors and catalog checks pass')
sys.exit(1 if bad else 0)
