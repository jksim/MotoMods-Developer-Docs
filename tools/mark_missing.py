#!/usr/bin/env python3
"""Resolve or annotate the assets that no capture preserved.

Two passes:

1. Reuse — the portal uploaded some images twice under different Squarespace
   item ids. If a recovered asset has the same filename, point at that instead.
2. Annotate — whatever is genuinely lost is replaced with a note naming the
   file, so a reader sees an honest gap rather than a broken image.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
MISSING = os.path.join(ROOT, 'build', 'missing_assets.json')

# `name-a1b2c3.png` is the converter's disambiguating suffix for two URLs that
# share a filename; strip it to find the copy that did survive.
DEDUP_SUFFIX = re.compile(r'-[0-9a-f]{6}(\.[A-Za-z0-9]+)$')


def pages():
    return [os.path.join(dp, f)
            for dp, _, fs in os.walk(DOCS) for f in fs if f.endswith('.md')]


def replace_everywhere(fn):
    changed = 0
    for page in pages():
        text = open(page, encoding='utf-8').read()
        new = fn(text)
        if new != text:
            open(page, 'w', encoding='utf-8').write(new)
            changed += 1
    return changed


def main():
    missing = json.load(open(MISSING))
    if not missing:
        print('nothing missing')
        return 0

    reused, annotated = [], []
    for item in missing:
        asset = item['asset']
        name = os.path.basename(asset)
        stem_alt = DEDUP_SUFFIX.sub(r'\1', name)

        # 1. An identical filename that did survive.
        alt = os.path.join(DOCS, os.path.dirname(asset), stem_alt)
        if stem_alt != name and os.path.isfile(alt):
            replace_everywhere(lambda t, a=name, b=stem_alt: t.replace(a, b))
            reused.append((name, stem_alt))
            continue

        # 2. Genuinely lost: say so where it was used.
        note = (f'*(Not preserved: `{name}` was not captured by the Wayback '
                f'Machine and no copy survives.)*')
        img = re.compile(r'!\[[^\]]*\]\([^)]*' + re.escape(name) + r'[^)]*\)')
        link = re.compile(r'\[([^\]]+)\]\([^)]*' + re.escape(name) + r'[^)]*\)')
        hits = replace_everywhere(
            lambda t, i=img, l=link, n=note: l.sub(r'\1 ' + n, i.sub(n, t)))
        annotated.append((name, hits))

    for old, new in reused:
        print(f'reused  {old} -> {new}')
    for name, hits in annotated:
        print(f'noted   {name} (on {hits} page{"s" if hits != 1 else ""})')
    print(f'\n{len(reused)} reused, {len(annotated)} annotated as missing')
    return 0


if __name__ == '__main__':
    sys.exit(main())
