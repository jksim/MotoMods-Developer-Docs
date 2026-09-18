#!/usr/bin/env python3
"""Copy the original captured HTML into archive/, untouched.

The Markdown in docs/ is a readable reconstruction; this is the evidence it was
built from. Pages are filed under the path they were served from, and every
capture of a page is kept, including the 2017 portal's duplicates that did not
earn a page of their own.
"""
import json, os, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manifest import PAGES, ARCHIVE_ONLY

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = os.path.join(ROOT, 'old_website')
ARCHIVE = os.path.join(ROOT, 'archive')

README = """# Original captures

Unmodified HTML as the Wayback Machine captured it from
`developer.motorola.com`. Nothing here has been edited: links, styles and
image URLs still point at hosts that are long gone, so these files are for
verification and provenance rather than for reading.

Each page is filed under the path it was served from. Where both snapshots
captured a page, both copies are kept:

- `squarespace/` — the 2016-17 Moto Mods developer portal
- `drupal/` — the 2017-18 Motorola Developer Portal that replaced it

`index.json` records, for every page, which snapshot each copy came from, its
size, its `<title>`, and whether the rebuilt site draws from it.

The reconstruction in `docs/` is generated from these files by `tools/`.
"""


def main():
    inv = json.load(open(sys.argv[1]))
    used = {orig for orig, _, _ in PAGES}
    wanted = used | set(ARCHIVE_ONLY)
    shutil.rmtree(ARCHIVE, ignore_errors=True)
    os.makedirs(ARCHIVE, exist_ok=True)

    index, copied = {}, 0
    for path, entry in sorted(inv.items()):
        if path not in wanted:
            continue
        gen_dir = 'squarespace' if entry['gen'] == 'squarespace' else 'drupal'
        copies = []
        for source in entry['sources']:
            dest = os.path.join(ARCHIVE, gen_dir, source['snapshot'],
                                path, 'index.html')
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copyfile(os.path.join(OLD, source['snapshot'], source['file']),
                            dest)
            copies.append({
                'snapshot': source['snapshot'],
                'captured_file': source['file'],
                'archived_as': os.path.relpath(dest, ROOT),
                'bytes': source['bytes'],
            })
            copied += 1
        index[path] = {
            'source_url': f'http://developer.motorola.com/{path}',
            'title': entry['title'],
            'portal': gen_dir,
            'used_in_site': path in used,
            'copies': copies,
        }

    json.dump(index, open(os.path.join(ARCHIVE, 'index.json'), 'w'),
              indent=2, sort_keys=True)
    open(os.path.join(ARCHIVE, 'README.md'), 'w').write(README)
    print(f'archived {copied} captures of {len(index)} pages')


if __name__ == '__main__':
    main()
