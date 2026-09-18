#!/usr/bin/env python3
"""Verify every internal link and image in docs/ resolves to a file.

mkdocs --strict catches unresolved Markdown links but says nothing about the
raw HTML blocks the conversion preserves, so both are checked here.
"""
import os, posixpath, re, sys
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')

MD_LINK = re.compile(r'!?\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
HTML_REF = re.compile(r'(?:src|href)="([^"]+)"')


def page_targets(page):
    text = open(page, encoding='utf-8').read()
    return set(MD_LINK.findall(text)) | set(HTML_REF.findall(text))


def main():
    pages = sorted(
        os.path.join(dp, f)
        for dp, _, fs in os.walk(DOCS) for f in fs if f.endswith('.md'))
    broken, anchors_only, checked = [], 0, 0

    for page in pages:
        rel_dir = posixpath.dirname(os.path.relpath(page, DOCS).replace(os.sep, '/'))
        for target in page_targets(page):
            if target.startswith(('http://', 'https://', 'mailto:', 'tel:', 'data:')):
                continue
            if target.startswith('#'):
                anchors_only += 1
                continue
            path = unquote(target.split('#')[0])
            if not path:
                continue
            checked += 1
            resolved = posixpath.normpath(posixpath.join(rel_dir, path))
            if not os.path.exists(os.path.join(DOCS, resolved)):
                broken.append((os.path.relpath(page, ROOT), target))

    for page, target in broken:
        print(f'BROKEN {page} -> {target}')
    print(f'\n{len(pages)} pages, {checked} internal references checked, '
          f'{anchors_only} same-page anchors, {len(broken)} broken')
    return 1 if broken else 0


if __name__ == '__main__':
    sys.exit(main())
