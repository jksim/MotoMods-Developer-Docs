#!/usr/bin/env python3
"""Discover every Moto Mods page across the two Wayback snapshots.

Emits a JSON inventory keyed by the original site path, recording which
snapshot files provide it and which is the richest copy.
"""
import json, os, re, sys
from bs4 import BeautifulSoup

OLD = os.path.join(os.path.dirname(__file__), '..', 'old_website')
SNAPSHOTS = ['html', 'html_v1']          # html is the later, more complete grab
SECTIONS = ('build', 'explore', 'get-started', 'documentation', 'partner',
            'support', 'tools-kits', 'buy', 'products')

# Old MOTODEV-era product pages live under /products too; keep only Moto Mods ones.
MODS_PRODUCTS = {
    'products', 'products/mdk', 'products/perforated-board',
    'products/hat-adapter-board', 'products/audio-personality-card',
    'products/battery-personality-card', 'products/display-personality-card',
    'products/temperature-sensor-personality-card',
}


def site_path(rel):
    """Map a snapshot file path to the URL path it was captured from."""
    p = rel[:-len('/index.html')] if rel.endswith('/index.html') else rel
    if p.endswith('.html'):
        p = p[:-len('.html')]
    return p


def classify(soup, raw):
    if soup.find('main', id='page'):
        return 'squarespace'
    if 'Drupal 8' in raw and soup.select_one('.region-content'):
        return 'drupal'
    return None


def main():
    inv = {}
    for snap in SNAPSHOTS:
        root = os.path.join(OLD, snap)
        for dirpath, _, files in os.walk(root):
            rel_dir = os.path.relpath(dirpath, root)
            top = rel_dir.split('/')[0]
            if top not in SECTIONS:
                continue
            for name in files:
                if not name.endswith('.html'):
                    continue
                rel = os.path.relpath(os.path.join(dirpath, name), root)
                path = site_path(rel)
                # Query-string captures (?login=1, ?rq=faq …) are duplicates.
                if '?' in path or '#' in path:
                    continue
                if path.split('/')[0] == 'products' and path not in MODS_PRODUCTS:
                    continue
                raw = open(os.path.join(root, rel), encoding='utf-8',
                           errors='replace').read()
                soup = BeautifulSoup(raw, 'lxml')
                gen = classify(soup, raw)
                if gen is None:
                    continue
                title = soup.find('title')
                title = title.get_text(strip=True) if title else ''
                title = re.sub(r'\s*[—|]\s*Motorola Developer Portal\s*$', '', title)
                entry = inv.setdefault(path, {'path': path, 'sources': []})
                entry['sources'].append({
                    'snapshot': snap, 'file': rel, 'gen': gen,
                    'bytes': len(raw), 'title': title,
                })
    # Prefer the largest capture; ties go to the later `html` snapshot.
    for entry in inv.values():
        best = max(entry['sources'],
                   key=lambda s: (s['bytes'], s['snapshot'] == 'html'))
        entry['best'] = best
        entry['gen'] = best['gen']
        entry['title'] = best['title']
    json.dump(inv, open(sys.argv[1], 'w'), indent=2, sort_keys=True)
    by_gen = {}
    for e in inv.values():
        by_gen.setdefault(e['gen'], []).append(e['path'])
    for gen in sorted(by_gen):
        print(f"\n--- {gen} ({len(by_gen[gen])}) ---")
        for p in sorted(by_gen[gen]):
            e = inv[p]
            print(f"  {p:52} {e['best']['snapshot']:8} {e['best']['bytes']:7}  {e['title']}")


if __name__ == '__main__':
    main()
