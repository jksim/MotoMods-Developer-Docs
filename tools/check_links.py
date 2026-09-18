#!/usr/bin/env python3
"""Verify internal links, in the Markdown sources and in the built site.

Two passes, because they catch different mistakes:

- `docs/` checks that every link and image names a file that exists. This
  catches a converter that emitted the wrong path.
- `site/` checks the published HTML. MkDocs rewrites `.md` links to page URLs
  only inside Markdown; a link written in a raw HTML block is passed through
  untouched and ships pointing at a `.md` file the server does not serve. The
  source pass cannot see that, because the `.md` file really does exist.
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


def site_base_path():
    """The URL prefix the site is published under, from mkdocs.yml site_url."""
    try:
        conf = open(os.path.join(ROOT, 'mkdocs.yml'), encoding='utf-8').read()
    except OSError:
        return ''
    m = re.search(r'^site_url:\s*(\S+)', conf, re.M)
    if not m:
        return ''
    return '/' + m.group(1).split('://', 1)[-1].partition('/')[2].strip('/')


def check_built_site():
    """Check the published HTML: no .md links, and every local href resolves."""
    site = os.path.join(ROOT, 'site')
    if not os.path.isdir(site):
        print('site/ not built — skipping published-URL pass '
              '(run `mkdocs build` first)')
        return []
    base = site_base_path()
    problems = []
    for dirpath, _, files in os.walk(site):
        for name in files:
            if not name.endswith('.html'):
                continue
            page = os.path.join(dirpath, name)
            rel_page = os.path.relpath(page, site)
            html = open(page, encoding='utf-8', errors='replace').read()
            for target in set(HTML_REF.findall(html)):
                if ':' in target.split('/')[0] or target.startswith(('#', '//')):
                    continue                 # any URL scheme, including javascript:
                path = unquote(target.split('#')[0].split('?')[0])
                if not path:
                    continue
                if path.endswith('.md'):
                    problems.append((rel_page, target,
                                     'links to a .md file, which is not served'))
                    continue
                if path.startswith('/'):
                    # Root-absolute: served from the site root, under the base
                    # path the theme prepends.
                    if base and path.startswith(base):
                        path = path[len(base):]
                    resolved = posixpath.normpath(path.lstrip('/') or '.')
                else:
                    resolved = posixpath.normpath(
                        posixpath.join(posixpath.dirname(rel_page), path))
                if resolved.startswith('..'):
                    problems.append((rel_page, target, 'escapes the site root'))
                    continue
                full = os.path.join(site, resolved)
                if not (os.path.exists(full) or
                        os.path.exists(os.path.join(full, 'index.html'))):
                    problems.append((rel_page, target, 'no such file in site/'))
    return problems


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
    print(f'sources: {len(pages)} pages, {checked} internal references checked, '
          f'{anchors_only} same-page anchors, {len(broken)} broken')

    published = check_built_site()
    for page, target, why in published:
        print(f'BROKEN site/{page} -> {target}  ({why})')
    if published or os.path.isdir(os.path.join(ROOT, 'site')):
        print(f'built site: {len(published)} broken published link(s)')
    return 1 if (broken or published) else 0


if __name__ == '__main__':
    sys.exit(main())
