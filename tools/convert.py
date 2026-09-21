#!/usr/bin/env python3
"""Rebuild the Moto Mods developer docs as Markdown from the Wayback captures.

Reads the inventory produced by discover.py, pulls the content region out of
each captured page, rewrites internal links and asset URLs, and writes MkDocs
Markdown. Assets that are referenced but absent from the captures are recorded
in assets.json for fetch_assets.py to retrieve from the Wayback Machine.
"""
import hashlib, json, os, posixpath, re, sys, html as htmllib
from collections import defaultdict
from urllib.parse import unquote
from bs4 import BeautifulSoup, NavigableString, Comment
from markdownify import MarkdownConverter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manifest import (PAGES, ARCHIVE_ONLY, REDIRECTS, MIRROR_OWNER,
                      MIRRORED_REPOS, UPSTREAM_OWNER, SDK_REFERENCE_FROM,
                      SDK_REFERENCE_TO, PLAY_APKS)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = os.path.join(ROOT, 'old_website')
DOCS = os.path.join(ROOT, 'docs')
IMG_DIR = 'assets/img'
FILE_DIR = 'assets/files'

SQS_HOST = re.compile(r'^https?://static1?\.squarespace\.com', re.I)
SELF_HOST = re.compile(r'^https?://developer\.motorola\.com', re.I)
ASSET_EXT = re.compile(r'\.(png|jpe?g|gif|svg|webp|pdf|zip|tar\.gz|stl|mp4)$', re.I)

# Blocks that are chrome, tracking or dead interactivity rather than content.
DROP_SELECTORS = [
    'script', 'style', 'noscript', 'iframe', 'form', 'select', 'button',
    '.sqs-block-form', '.newsletter-block', '.sqs-block-socialaccountlinks',
    '.sqs-block-socialaccountlinks-v2', '.anchor-links', '.sqs-block-button',
    '.social-links', '.sqs-svg-icon--wrapper', '#block-backtotop',
    '.block-webform', '.visually-hidden', '.sr-only', '.breadcrumb',
    '.page-header', '.sqs-block-summary-v2', '.product-price', '.sqs-money-native',
    # In-page tab strip on the 2017 Tools & Kits page; MkDocs renders its own
    # table of contents, and one of the sections it linked to was never
    # captured, leaving a dead anchor.
    '#block-toolskitstabs',
]

assets = {}      # local docs-relative path -> {'sources': [...], 'origin': url}
warnings = []
unmapped = set()  # internal paths with no page in the rebuild
repairs = {}      # page -> links recovered from an alternate capture
mirrored = set()  # repositories whose links were repointed at the mirrors
sdk_repointed = []  # SDK javadoc links sent to the preserved copy
play_repointed = []  # Play Store links sent to the archived APKs


# --------------------------------------------------------------------------- #
# asset handling
# --------------------------------------------------------------------------- #
_basename_index = None


def basename_index():
    """Every non-HTML file in both snapshots, indexed by filename.

    HTTrack rewrote many Squarespace URLs on its way to disk — the same image
    lives at static/<ids>/<stamp>/name.png in one capture and images/<stamp>/
    name.png in the other — so a filename lookup recovers assets that a
    path-for-path lookup misses.
    """
    global _basename_index
    if _basename_index is None:
        _basename_index = defaultdict(list)
        for snap in ('html', 'html_v1'):
            for dirpath, _, files in os.walk(os.path.join(OLD, snap)):
                for name in files:
                    if not name.lower().endswith(('.html', '.htm')):
                        _basename_index[name.lower()].append(
                            os.path.join(dirpath, name))
    return _basename_index


def snapshot_candidates(url):
    """Where a captured copy of `url` might sit inside the two snapshots."""
    if SQS_HOST.match(url):
        rel = re.sub(SQS_HOST, '', url).split('?')[0].lstrip('/')
    elif url.startswith('/'):
        rel = url.split('?')[0].lstrip('/')
    elif not url.startswith('http'):
        rel = url.lstrip('./')           # HTTrack-relativised link
    else:
        return []
    rel = unquote(htmllib.unescape(rel))
    out = []
    for snap in ('html', 'html_v1'):
        out.append(os.path.join(OLD, snap, rel))
        out.append(os.path.join(OLD, snap, rel, 'index.html'))

    # Fall back to the filename, preferring a copy filed under the same
    # Squarespace upload stamp so same-named images can't be confused.
    base = posixpath.basename(rel.rstrip('/'))
    if len(base) > 4:
        stamp = re.search(r'/(\d{10,})/[^/]*$', '/' + rel)
        hits = basename_index().get(base.lower(), [])
        hits.sort(key=lambda p: (stamp is None or stamp.group(1) not in p))
        out.extend(hits)
    return out


def asset_target(url):
    """Pick a stable, readable docs-relative path for an asset URL."""
    clean = htmllib.unescape(url.split('?')[0].split('#')[0])
    base = posixpath.basename(clean.rstrip('/')) or 'asset'
    base = re.sub(r'[^A-Za-z0-9._+-]', '-', base)
    if not ASSET_EXT.search(base):
        base += '.png'                       # Squarespace serves extensionless images
    ext = os.path.splitext(base)[1].lower()
    folder = FILE_DIR if ext in ('.pdf', '.zip', '.stl', '.gz') else IMG_DIR
    target = f'{folder}/{base}'
    prior = assets.get(target)
    if prior and prior['origin'] != url:     # name clash between different files
        stem, ext = os.path.splitext(base)
        digest = hashlib.sha1(url.encode()).hexdigest()[:6]
        target = f'{folder}/{stem}-{digest}{ext}'
    return target


def register_asset(url):
    """Record an asset and return the path the Markdown should point at."""
    target = asset_target(url)
    entry = assets.setdefault(target, {'origin': url, 'local': None})
    if entry['local'] is None:
        for cand in snapshot_candidates(url):
            if os.path.isfile(cand) and os.path.getsize(cand) > 0:
                entry['local'] = cand
                break
    return target


def rewrite_asset_url(url, depth):
    """Turn an absolute asset URL into a link relative to the current page."""
    target = register_asset(url)
    return ('../' * depth) + target


# --------------------------------------------------------------------------- #
# link handling
# --------------------------------------------------------------------------- #
PATH_TO_DOC = {orig: out for orig, out, _ in PAGES}
PATH_TO_DOC.update(REDIRECTS)


GITHUB_REPO = re.compile(
    r'^(https?://github\.com/)' + re.escape(UPSTREAM_OWNER) + r'/([A-Za-z0-9_.-]+)',
    re.I)


def repoint_to_mirror(href):
    """Send a source-code link to the preserved copy, path and all.

    The documentation links deep into these repositories — individual drivers,
    board configs — so only the owner is swapped; everything after the repo
    name is left alone.
    """
    m = GITHUB_REPO.match(href)
    if not m:
        return href
    repo = m.group(2)
    if repo.lower() not in {r.lower() for r in MIRRORED_REPOS}:
        return href
    mirrored.add(repo)
    return f'{m.group(1)}{MIRROR_OWNER}/{repo}' + href[m.end():]


GITHUB_IN_TEXT = re.compile(
    r'(https?://github\.com/)' + re.escape(UPSTREAM_OWNER) + r'/([A-Za-z0-9_.-]+)',
    re.I)


SDK_REF = re.compile(r'https?://' + re.escape(SDK_REFERENCE_FROM), re.I)
PLAY_LINK = re.compile(
    r'https?://play\.google\.com/store/apps/details\?id=([A-Za-z0-9_.]+)', re.I)


def repoint_play(href, depth):
    """Send a Play Store link to the archived APK, or None if not one."""
    m = PLAY_LINK.match(href.strip())
    if not m:
        return None
    target = PLAY_APKS.get(m.group(1))
    if not target:
        return None
    play_repointed.append(m.group(1))
    return ('../' * depth) + target


def repoint_sdk(url):
    """Send the SDK javadoc links at the preserved copy."""
    if not SDK_REF.search(url):
        return url
    sdk_repointed.append(1)
    return SDK_REF.sub('https://' + SDK_REFERENCE_TO, url)


def repoint_text(text):
    """Repoint repository URLs inside code blocks.

    The build instructions tell the reader to `git clone` these repositories,
    so a link that only works while the upstream account survives is the one
    place durability matters most.
    """
    def sub(m):
        repo = m.group(2)
        if repo.lower() not in {r.lower() for r in MIRRORED_REPOS}:
            return m.group(0)
        mirrored.add(repo)
        return f'{m.group(1)}{MIRROR_OWNER}/{repo}'
    return repoint_sdk(GITHUB_IN_TEXT.sub(sub, text))


def to_site_path(href):
    """Reduce a link to a site-root path, or return None if it leaves the site.

    Handles the portal's own absolute URLs and the handful of Squarespace links
    that lost their leading slash and ended up as `http://partner/contact-form`.
    """
    if SELF_HOST.match(href):
        return SELF_HOST.sub('', href) or '/'
    m = re.match(r'^https?://([^/]+)(/.*)?$', href)
    if m and '.' not in m.group(1):
        return '/' + m.group(1) + (m.group(2) or '')
    return href if href.startswith('/') else None


def candidate_paths(href, page_path):
    """Site paths a link might mean, best guess first.

    HTTrack rewrote links in the html_v1 capture to be relative to where it
    filed the page on disk, which is not always where the page was served
    from, so a relative link is tried both ways: resolved against the page,
    and with its leading `../` hops dropped and read as a site-root path.
    """
    root = to_site_path(href)
    if root is not None:
        return [root]
    if href.startswith(('http:', 'https:', 'javascript:')):
        return []
    out = [posixpath.normpath(posixpath.join('/' + posixpath.dirname(page_path), href))]
    stripped = re.sub(r'^(?:\.\./)+', '', href)
    if stripped != href:
        out.append('/' + stripped)
    return out


def rewrite_internal_link(href, out_md, page_path):
    """Map an original site URL onto the rebuilt page that now holds it."""
    for candidate in candidate_paths(href, page_path):
        path, _, frag = candidate.partition('#')
        path = path.split('?')[0].strip('/').lstrip('./')
        if path in PATH_TO_DOC:
            rel = posixpath.relpath(PATH_TO_DOC[path],
                                    posixpath.dirname(out_md) or '.')
            return rel + (('#' + frag) if frag else '')
    return None


# --------------------------------------------------------------------------- #
# content extraction
# --------------------------------------------------------------------------- #
def content_region(soup, gen):
    """Return (content node, sidebar node, is_article).

    `is_article` marks the Squarespace documentation template, whose in-page
    <h1> is the real page heading. Landing, product and form pages reuse <h1>
    for section banners, so those take their heading from <title> instead.
    """
    if gen == 'squarespace':
        main = soup.find('main', id='page')
        if not main:
            return None, None, False
        content = main.find(id='content') or main
        sidebar = content.select_one('.sidebar')
        entry = content.select_one('.entry-content')
        return (entry or content), sidebar, entry is not None
    region = soup.select_one('.region-content')
    if not region:
        return None, None, False
    article = region.find('article')
    if article and len(article.get_text(strip=True)) > 0.6 * len(region.get_text(strip=True)):
        return article, None, False
    return region, None, False


def rebuild_product_grid(node):
    """Turn the Squarespace storefront grid into a plain card list.

    The original markup nests four wrapper divs per tile around a lazy-loaded
    image and a price of 0.00 (the boards were never actually sold here).
    """
    grid = node.select_one('#productList')
    if not grid:
        return
    cards = []
    for a in grid.select('a.product'):
        img = a.find('img')
        src = img.get('data-src') or img.get('data-image') or img.get('src') if img else None
        title = a.select_one('.product-title')
        title = title.get_text(' ', strip=True) if title else a.get('id', '').replace('thumb-', '')
        cards.append((a.get('href', ''), src, title))
    markup = ['<ul class="mm-cards">']
    for href, src, title in cards:
        img_html = f'<img src="{src}" alt="{title}">' if src else ''
        markup.append(f'<li><a href="{href}">{img_html}<span>{title}</span></a></li>')
    markup.append('</ul>')
    grid.replace_with(BeautifulSoup('\n'.join(markup), 'lxml').find('ul'))


def repair_root_links(body, entry, gen):
    """Restore links that a capture collapsed to the site root.

    HTTrack sometimes rewrote a link as href="/" instead of localising it,
    losing the destination. It did this to different links in each capture, so
    neither snapshot is reliably better — but the pages are otherwise
    identical, so a link lost in one can be recovered from another by matching
    its text.
    """
    broken = [a for a in body.find_all('a', href=True)
              if a['href'].strip() in ('/', '') and a.get_text(strip=True)]
    if not broken:
        return 0
    chosen = entry['best']
    alternates = {}
    for source in entry['sources']:
        if (source['snapshot'], source['file']) == (chosen['snapshot'], chosen['file']):
            continue
        path = os.path.join(OLD, source['snapshot'], source['file'])
        try:
            other = BeautifulSoup(open(path, encoding='utf-8',
                                       errors='replace').read(), 'lxml')
        except OSError:
            continue
        node, _, _ = content_region(other, gen)
        if node is None:
            continue
        for a in node.find_all('a', href=True):
            href = a['href'].strip()
            text = re.sub(r'\s+', ' ', a.get_text(' ', strip=True)).lower()
            if text and href not in ('/', ''):
                alternates.setdefault(text, href)

    repaired = 0
    for a in broken:
        text = re.sub(r'\s+', ' ', a.get_text(' ', strip=True)).lower()
        href = alternates.get(text)
        if href:
            a['href'] = href
            repaired += 1
        else:
            warnings.append(f'{entry["path"]}: link "{a.get_text(" ", strip=True)[:60]}" '
                            f'collapsed to the site root in every capture')
    return repaired


def clean(node):
    rebuild_product_grid(node)
    for sel in DROP_SELECTORS:
        for el in node.select(sel):
            el.decompose()
    for c in node.find_all(string=lambda t: isinstance(t, Comment)):
        c.extract()
    # Squarespace lazy-loads images: the real URL hides in data-src.
    for img in node.find_all('img'):
        src = img.get('data-src') or img.get('data-image') or img.get('src')
        if not src or 'open-in-new-window' in src:
            img.decompose()
            continue
        for attr in list(img.attrs):
            if attr not in ('alt', 'title'):
                del img[attr]
        img['src'] = src
    # Collapse the duplicate <img> pairs Squarespace emits per image block.
    seen = set()
    for img in node.find_all('img'):
        key = img['src']
        if key in seen:
            img.decompose()
        else:
            seen.add(key)
    for el in node.find_all(['div', 'span', 'section']):
        if not el.get_text(strip=True) and not el.find('img'):
            el.decompose()
    return node


CMS_ID = re.compile(r'^(block|item|page|yui|field)')
ANCHOR_MARK = 'MMDOCSANCHOR{}ENDANCHOR'


def preserve_anchors(node):
    """Keep the anchors the original pages linked to.

    Both portals emitted explicit ids — `<h2 id="application">` on headings,
    bare `<a id="accessing-muc-shell">` elsewhere — and linked to them within
    and across pages. Markdown would re-slug every heading from its text and
    drop the rest, so meaningful ids are re-attached: headings via attr_list,
    anything else via a marker that becomes an anchor after conversion.
    """
    linked = {a['href'][1:] for a in node.find_all('a', href=True)
              if a['href'].startswith('#') and len(a['href']) > 1}
    seen = set()
    for h in node.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        anchor = (h.get('id') or '').strip()
        text = h.get_text(' ', strip=True)
        if not anchor or not text or anchor in seen:
            continue
        if CMS_ID.match(anchor) and anchor not in linked:
            continue
        seen.add(anchor)
        h.clear()
        h.append(NavigableString(f'{text} {{#{anchor}}}'))

    for el in node.find_all(id=True):
        anchor = el['id'].strip()
        if anchor in seen or anchor not in linked:
            continue
        seen.add(anchor)
        marker = NavigableString('\n\n' + ANCHOR_MARK.format(anchor) + '\n\n')
        if el.name == 'a' and not el.get_text(strip=True):
            el.replace_with(marker)      # a bare named anchor
        else:
            el.insert_before(marker)


def detect_language(code):
    """Guess a highlighting language for a code block.

    The original pages never tagged their code, and they mix Moto Mod firmware
    (C on NuttX), Android app code (Java), hardware manifests (ini), Kconfig
    menu transcripts and bare constant lists. Only confident matches are
    labelled; the rest are left plain, which reads better than mislabelled
    highlighting.
    """
    s = code.strip()
    if not s:
        return ''
    java = (
        r'^\s*(package|import)\s+[\w.]+;', r'\b(public|private|protected)\s+'
        r'(static\s+)?(final\s+)?(class|void|int|boolean|String)\b',
        r'@Override\b', r'\bnew\s+[A-Z]\w*\s*\(',
        r'\bMod(Manager|Display|Protocol|Device|Battery|Connection|Listener)\b',
        r'\bandroid\.[\w.]+', r'\bIntent\b', r'\bLog\.[dewiv]\(',
    )
    c = (
        r'^\s*#\s*(include|ifdef|ifndef|define|endif|if|else|pragma)\b',
        r'\bstruct\s+\w+\s*[\*\{]', r'\(\s*\*\s*\w+\s*\)\s*\(',
        r'\bextern\s+(struct|const|int|void)\b', r'\buint\d+_t\b',
        r'\bsize_t\b', r'\bstatic\s+(int|void|struct|const)\b',
        r'->\s*\w+\s*=', r'\bCONFIG_\w+\b.*\b(ifdef|ifndef|defined)\b',
    )
    if any(re.search(p, s, re.M) for p in java):
        return 'java'
    if any(re.search(p, s, re.M) for p in c):
        return 'c'
    if re.search(r'^\s*<\?xml', s, re.M) or (
            re.search(r'^\s*<[a-zA-Z][\w:-]*[\s>/]', s, re.M) and s.count('<') > 2):
        return 'xml'
    if re.search(r'^\s*\$ |^\s*(sudo|cd|make|git|adb|fastboot|export|apt-get|wget|tar|sh)\s',
                 s, re.M):
        return 'console'
    if re.search(r'^\s*\[[\w-]+ [\w.]+\]\s*$', s, re.M):
        return 'ini'
    lines = [l for l in s.splitlines() if l.strip()]
    if lines and all(re.match(r'^\s*(?:[;#].*|[\w.]+\s*=\s*\S*)$', l) for l in lines):
        return 'ini'                     # Kconfig / defconfig fragments
    if re.match(r'^\s*[\{\[]', s) and re.search(r'"\w+"\s*:', s):
        return 'json'
    return ''


def render_card_grid(grid):
    """Emit the card grid as md_in_html so MkDocs rewrites its links.

    A raw HTML block is passed through untouched, which leaves `href="mdk.md"`
    in the published page pointing at a file that is not served. Marking the
    list up for md_in_html puts the links back under Markdown, so MkDocs maps
    them to real page URLs and --strict validates them.
    """
    items = []
    for a in grid.select('a[href]'):
        img = a.find('img')
        label = a.find('span')
        label = label.get_text(' ', strip=True) if label else a.get_text(' ', strip=True)
        inner = f'![{label}]({img["src"]})' if img is not None else ''
        items.append(f'<li markdown="span">[{inner}'
                     f'<span>{label}</span>]({a["href"]})</li>')
    return ('<ul class="mm-cards" markdown="block">\n'
            + '\n'.join(items) + '\n</ul>')


def stash_blocks(node):
    """Swap tables and code blocks for placeholders so Markdown can't mangle them.

    Moto Mods protocol tables use rowspan, colspan and repeated <thead> rows,
    none of which survive a Markdown table, so they are re-emitted as HTML.
    """
    blocks = []

    def placeholder(el, rendered):
        blocks.append(rendered)
        el.replace_with(NavigableString(f'\n\nMMDOCSBLOCK{len(blocks) - 1}ENDBLOCK\n\n'))

    for pre in node.find_all('pre'):
        code = repoint_text(pre.get_text())
        lang = detect_language(code)
        fence = '```'
        while fence in code:
            fence += '`'
        placeholder(pre, f'{fence}{lang}\n{code.strip()}\n{fence}')
    for grid in node.select('ul.mm-cards'):
        placeholder(grid, render_card_grid(grid))
    for table in node.find_all('table'):
        for tag in table.find_all(True):
            for attr in list(tag.attrs):
                if attr not in ('colspan', 'rowspan'):
                    del tag[attr]
        placeholder(table, f'<div class="md-typeset__scrollwrap"><div class="md-typeset__table">\n'
                           f'{table.decode()}\n</div></div>')
    return blocks


class Converter(MarkdownConverter):
    """markdownify tuned for these pages: ATX headings, no stray escaping."""


def to_markdown(node):
    return Converter(heading_style='ATX', bullets='-', escape_asterisks=False,
                     escape_underscores=False, wrap=False).convert_soup(node)


def tidy(md):
    md = md.replace('\xa0', ' ')
    # The downloads page put each file size in a span right after the link,
    # with no whitespace between them.
    md = re.sub(r'\)(\d+(?:\.\d+)?\s*(?:KB|MB|GB)\b)', r') \1', md)
    md = re.sub(r'[ \t]+\n', '\n', md)
    md = re.sub(r'\n{3,}', '\n\n', md)
    md = re.sub(r'^\s*\n', '', md)
    return md.strip() + '\n'


def restore_blocks(md, blocks):
    md = re.sub(r'MMDOCSBLOCK(\d+)ENDBLOCK', lambda m: blocks[int(m.group(1))], md)
    return re.sub(r'MMDOCSANCHOR(\S+?)ENDANCHOR',
                  lambda m: f'<a id="{m.group(1)}"></a>', md)


# --------------------------------------------------------------------------- #
def convert_page(entry, out_md, nav_title):
    src = os.path.join(OLD, entry['best']['snapshot'], entry['best']['file'])
    raw = open(src, encoding='utf-8', errors='replace').read()
    soup = BeautifulSoup(raw, 'lxml')
    body, sidebar, is_article = content_region(soup, entry['gen'])
    if body is None:
        warnings.append(f'{entry["path"]}: no content region')
        return None

    refs = []
    if sidebar:
        links = sidebar.select_one('.external-links')
        if links:
            clean(links)
            for a in links.find_all('a', href=True):
                label = a.get_text(' ', strip=True)
                if label:
                    # These are collected before the link pass runs, so they
                    # need the same repointing applied.
                    href = repoint_sdk(repoint_to_mirror(a['href']))
                    refs.append((repoint_sdk(label), href))

    repaired = repair_root_links(body, entry, entry['gen'])
    if repaired:
        repairs[entry['path']] = repaired
    body = clean(body)
    depth = out_md.count('/')

    # Documentation pages carry their real heading in the content <h1>;
    # everywhere else <h1> is a section banner, so use the captured <title>
    # and demote the banners so the page keeps a single top-level heading.
    title = entry['title'] or nav_title
    h1s = body.find_all('h1')
    if is_article and h1s:
        t = h1s[0].get_text(' ', strip=True)
        if t:
            title = t
        h1s[0].decompose()
        h1s = h1s[1:]
    for extra in h1s:
        extra.name = 'h2' 

    for a in body.find_all('a', href=True):
        href = a['href'].strip()
        if href.startswith('javascript:'):
            a.unwrap()          # accordion toggles from the FAQ page
            continue
        if href.startswith(('mailto:', 'tel:', '#')):
            continue
        apk = repoint_play(href, depth)
        if apk:
            a['href'] = apk
            # The label says "on Google Play Store", which is no longer where
            # it goes.
            for text_node in a.find_all(string=True):
                moved = re.sub(r'\s*on Google Play Store', ' (archived APK)',
                               str(text_node))
                if moved != str(text_node):
                    text_node.replace_with(NavigableString(moved))
            continue
        if SDK_REF.search(href):
            a['href'] = repoint_sdk(href)
            for text_node in a.find_all(string=True):
                moved = repoint_sdk(str(text_node))
                if moved != str(text_node):
                    text_node.replace_with(NavigableString(moved))
            continue
        if GITHUB_REPO.match(href):
            a['href'] = repoint_to_mirror(href)
            # Many of these links are labelled with the URL itself, so the
            # visible text has to move with the target.
            for text_node in a.find_all(string=True):
                moved = repoint_text(str(text_node))
                if moved != str(text_node):
                    text_node.replace_with(NavigableString(moved))
            continue
        local = to_site_path(href)
        if ASSET_EXT.search((local or href).split('?')[0]) and (
                local is not None or SQS_HOST.match(href)):
            a['href'] = rewrite_asset_url(local or href, depth)
            continue
        new = rewrite_internal_link(href, out_md, entry['path'])
        if new:
            a['href'] = new
        elif local:
            # Nothing in the rebuild covers this path. Fall back to the live
            # archive, and report it: a link that leaves the site is usually a
            # gap in the manifest rather than a page that truly never existed.
            unmapped.add(local.split('#')[0].split('?')[0].rstrip('/'))
            a['href'] = ('https://web.archive.org/web/2017/'
                         'http://developer.motorola.com' + local)

    for img in body.find_all('img'):
        img['src'] = rewrite_asset_url(img['src'], depth)

    preserve_anchors(body)
    blocks = stash_blocks(body)
    md = restore_blocks(tidy(to_markdown(body)), blocks)

    if refs:
        lines = ['', '## Related references', '']
        for label, href in refs:
            label = re.sub(r'\s+', ' ', label).strip()
            lines.append(f'- [{label}]({href})')
        md = md.rstrip() + '\n' + '\n'.join(lines) + '\n'

    title = re.sub(r'\s+', ' ', title.replace('\xa0', ' ')).strip()
    era = '2016 Squarespace portal' if entry['gen'] == 'squarespace' else '2017 Drupal portal'
    front = front_matter(title, f'http://developer.motorola.com/{entry["path"]}', era)
    return front + f'# {title}\n\n' + md


def front_matter(title, source_url, era):
    return ('---\n'
            f'title: {json.dumps(title)}\n'
            f'source_url: {source_url}\n'
            f'source_capture: {era}\n'
            '---\n\n')


def write(out_md, text):
    dest = os.path.join(DOCS, out_md)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, 'w', encoding='utf-8').write(text)


SPLITS = {
    # The certification page inlines the full 170 KB licence agreement below
    # this heading; it reads (and searches) far better as its own page.
    'partner/certification-program.md': (
        '**CERTIFIED MOD DEVELOPMENT AND LICENSE AGREEMENT**',
        'partner/license-agreement.md',
        'Certified Mod Development and License Agreement',
    ),
}


def apply_split(out_md, md):
    """Peel a long appendix off a page, leaving a link in its place."""
    marker, tail_md, tail_title = SPLITS[out_md]
    head, sep, tail = md.partition(marker)
    if not sep:
        warnings.append(f'{out_md}: split marker not found')
        return md, None
    rel = posixpath.relpath(tail_md, posixpath.dirname(out_md) or '.')
    head = head.rstrip() + f'\n\nRead the full [{tail_title}]({rel}).\n'
    return head, tail.strip()


def convert_terms_page():
    """The MDK terms of use were a bare HTML file outside both portals."""
    src = os.path.join(OLD, 'html', 'assets', 'html',
                       'moto-mods-dev-kit-terms-and-conditions.html')
    if not os.path.isfile(src):
        warnings.append('terms and conditions page missing from snapshots')
        return None
    soup = BeautifulSoup(open(src, encoding='utf-8', errors='replace').read(), 'lxml')
    body = clean(soup.body)
    for h in body.find_all(['h1', 'h3']):
        if 'TERMS AND CONDITIONS' in h.get_text():
            h.decompose()
            break
    title = 'Moto Mods Development Kit Terms & Conditions'
    md = tidy(to_markdown(body))
    return (front_matter(title, 'http://developer.motorola.com/assets/html/'
                                'moto-mods-dev-kit-terms-and-conditions.html',
                         '2017 Drupal portal')
            + f'# {title}\n\n' + md)


def main():
    inv = json.load(open(sys.argv[1]))
    written = 0
    for orig, out_md, nav_title in PAGES:
        entry = inv.get(orig)
        if not entry:
            warnings.append(f'{orig}: not present in any snapshot')
            continue
        md = convert_page(entry, out_md, nav_title)
        if md is None:
            continue
        if out_md in SPLITS:
            md, tail = apply_split(out_md, md)
            if tail:
                _, tail_md, tail_title = SPLITS[out_md]
                write(tail_md, front_matter(
                    tail_title, f'http://developer.motorola.com/{entry["path"]}',
                    '2017 Drupal portal') + f'# {tail_title}\n\n' + tail + '\n')
                written += 1
        write(out_md, md)
        written += 1

    terms = convert_terms_page()
    if terms:
        write('legal/mdk-terms-and-conditions.md', terms)
        written += 1

    os.makedirs(os.path.join(ROOT, 'build'), exist_ok=True)
    json.dump(assets, open(os.path.join(ROOT, 'build', 'assets.json'), 'w'),
              indent=2, sort_keys=True)
    have = sum(1 for a in assets.values() if a['local'])
    print(f'wrote {written} pages')
    print(f'assets: {len(assets)} referenced, {have} found in snapshots, '
          f'{len(assets) - have} to fetch')
    for w in warnings:
        print('WARN', w)
    if mirrored:
        print(f'\nrepointed source links to {MIRROR_OWNER}/ for '
              f'{len(mirrored)} repositor{"y" if len(mirrored) == 1 else "ies"}: '
              + ', '.join(sorted(mirrored)))
    if sdk_repointed:
        print(f'repointed {len(sdk_repointed)} SDK reference link(s) to '
              f'{SDK_REFERENCE_TO}')
    if play_repointed:
        print(f'repointed {len(play_repointed)} Play Store link(s) to the '
              f'archived APKs')
    if repairs:
        print(f'\nrecovered {sum(repairs.values())} root-collapsed link(s) from '
              f'alternate captures, across {len(repairs)} page(s):')
        for path, n in sorted(repairs.items()):
            print(f'  {path}: {n}')
    if unmapped:
        print(f'\n{len(unmapped)} internal path(s) fall back to the Wayback '
              f'Machine — add a REDIRECTS entry if the rebuild covers them:')
        for path in sorted(unmapped):
            print(f'  {path}')


if __name__ == '__main__':
    main()
