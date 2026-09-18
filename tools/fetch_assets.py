#!/usr/bin/env python3
"""Populate docs/assets from the snapshots, falling back to the Wayback Machine.

Roughly a third of the images on the 2016 portal were served from
static1.squarespace.com and were never mirrored into the captures, so anything
missing locally is pulled from web.archive.org's copy of the original URL.

The Wayback Machine answers an unavailable capture with a 200 and an HTML
error page, so every download is checked against the magic bytes for its type
before it is kept.
"""
import concurrent.futures as futures
import json, os, re, shutil, sys, time, urllib.error, urllib.request
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
MANIFEST = os.path.join(ROOT, 'build', 'assets.json')
SELF = 'http://developer.motorola.com'
# Snapshot stamps to try, in the order most likely to hold a live capture.
STAMPS = ['2017id_', '2016id_', '2018id_', '2022id_', '2019id_']
# Prefixes worth indexing in bulk: the portal's own files and the Squarespace
# bucket its 2016 incarnation served images from.
CDX_PREFIXES = [
    'static1.squarespace.com/static/5715eee9b09f95a12b44e0ed*',
    'developer.motorola.com/sites/default/files*',
    'developer.motorola.com/static*',
]
CDX_CACHE = os.path.join(ROOT, 'build', 'cdx_index.txt')
UA = {'User-Agent': 'moto-mods-docs-archive/1.0 (documentation preservation)'}
TIMEOUT = 90

MAGIC = {
    '.png':  [b'\x89PNG\r\n\x1a\n'],
    '.jpg':  [b'\xff\xd8\xff'],
    '.jpeg': [b'\xff\xd8\xff'],
    '.gif':  [b'GIF87a', b'GIF89a'],
    '.webp': [b'RIFF'],
    '.pdf':  [b'%PDF'],
    '.zip':  [b'PK\x03\x04', b'PK\x05\x06'],
    '.svg':  [b'<svg', b'<?xml'],
    '.mp4':  [b'\x00\x00\x00'],
}


def sniff(data):
    """The file extension the bytes actually are, or None."""
    for ext, magics in MAGIC.items():
        if ext in ('.jpeg', '.svg', '.mp4'):
            continue                     # aliases and too-loose signatures
        if any(data.startswith(m) for m in magics):
            return ext
    if data.lstrip()[:5].lower() in (b'<svg ', b'<?xml'):
        return '.svg'
    return None


def looks_valid(target, data):
    """Reject Wayback's HTML error pages and any other wrong-type response.

    Returns the extension the content really has, so a Squarespace URL with no
    extension (which the converter optimistically named `.png`) can be filed
    under the right one.
    """
    if not data or len(data) < 64:
        return None
    ext = os.path.splitext(target)[1].lower()
    actual = sniff(data)
    if actual is None:
        return None
    if ext in ('.jpg', '.jpeg') and actual == '.jpg':
        return ext
    if ext == actual:
        return ext
    # Images are interchangeable here: the extension came from the converter's
    # guess, not from the server.
    if {ext, actual} <= {'.png', '.jpg', '.jpeg', '.gif', '.webp'}:
        return actual
    return None


def fetch(url, tries=5):
    """GET with backoff; archive.org answers 429 freely when pushed."""
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (403, 404):
                raise
            time.sleep(5 * (attempt + 1))
        except Exception as e:
            last = e
            time.sleep(5 * (attempt + 1))
    raise last


def load_cdx_index():
    """Every archived capture under the prefixes the docs draw assets from.

    A direct fetch of an original asset URL often 404s because the only
    capture is of a resized variant (`…png?format=1000w`); the index gives the
    exact URL and timestamp that were actually archived.
    """
    if os.path.isfile(CDX_CACHE) and os.path.getsize(CDX_CACHE) > 0:
        rows = [l.split() for l in open(CDX_CACHE) if l.strip()]
        print(f'using cached CDX index ({len(rows)} captures)')
        return rows
    rows = []
    for prefix in CDX_PREFIXES:
        url = ('https://web.archive.org/cdx/search/cdx?url=' + quote(prefix, safe='*')
               + '&collapse=urlkey&fl=original,timestamp,mimetype,statuscode&limit=20000')
        try:
            body = fetch(url).decode('utf-8', 'replace')
        except Exception as e:
            print(f'  CDX query failed for {prefix}: {type(e).__name__}')
            continue
        got = [l.split() for l in body.splitlines() if l.strip()]
        rows.extend(got)
        print(f'  CDX {prefix}: {len(got)} captures')
        time.sleep(3)
    os.makedirs(os.path.dirname(CDX_CACHE), exist_ok=True)
    with open(CDX_CACHE, 'w') as fh:
        fh.write('\n'.join(' '.join(r) for r in rows) + '\n')
    return rows


def cdx_key(url):
    """The host-independent tail of an asset URL, used to match CDX rows."""
    return re.sub(r'^https?://[^/]+', '', url.split('?')[0])


def cdx_candidates(index, origin):
    """Archived captures of an asset, largest rendition first.

    Squarespace variants carry a `?format=NNNw` width, so preferring the
    biggest keeps the diagrams readable.
    """
    key = cdx_key(origin)
    if not key:
        return []
    hits = [r for r in index if len(r) >= 4 and key in r[0] and r[3] in ('200', '301')]

    def width(row):
        m = re.search(r'format=(\d+)w', row[0])
        return int(m.group(1)) if m else 0

    hits.sort(key=lambda r: (-width(r), r[1]))
    return [(r[0], r[1]) for r in hits]


def try_url(target, url):
    try:
        data = fetch(url)
    except urllib.error.HTTPError as e:
        return None, None, f'HTTP {e.code}'
    except Exception as e:
        return None, None, type(e).__name__
    ext = looks_valid(target, data)
    if ext:
        return data, ext, None
    return None, None, 'not the asset (error page or wrong type)'


def fetch_archived(target, origin, index):
    """Recover one asset: exact captures first, then year-guessed snapshots."""
    src = SELF + origin if origin.startswith('/') else origin
    last = 'no capture'
    for captured_url, stamp in cdx_candidates(index, origin)[:6]:
        data, ext, why = try_url(
            target, f'https://web.archive.org/web/{stamp}id_/{captured_url}')
        if data:
            return data, ext, captured_url
        last = why
    for stamp in STAMPS:
        data, ext, why = try_url(target, f'https://web.archive.org/web/{stamp}/{src}')
        if data:
            return data, ext, src
        last = why
    return None, None, last


def apply_renames(renames):
    """Point the Markdown at assets whose real type differed from the guess."""
    pages = [os.path.join(dp, f)
             for dp, _, fs in os.walk(DOCS) for f in fs if f.endswith('.md')]
    for old, new in renames.items():
        old_name, new_name = os.path.basename(old), os.path.basename(new)
        for page in pages:
            text = open(page, encoding='utf-8').read()
            if old_name in text:
                open(page, 'w', encoding='utf-8').write(
                    text.replace(old_name, new_name))
        print(f'  renamed {old} -> {new} (content was {os.path.splitext(new)[1]})')


IMAGE_EXTS = ('.png', '.jpg', '.jpeg', '.gif', '.webp')


def already_have(target):
    """True if this asset is on disk, including under a corrected extension.

    Squarespace served images from extensionless URLs, so the converter has to
    guess `.png`; when a download turns out to be a JPEG it is filed under the
    real extension instead. Without this check the guessed name looks missing
    on every later run, and the asset is re-fetched — landing on whichever
    rendition the Wayback Machine happens to serve, which is how a 1000px
    diagram quietly became a 500px one.
    """
    stem, ext = os.path.splitext(target)
    candidates = [target]
    if ext.lower() in IMAGE_EXTS:
        candidates += [stem + e for e in IMAGE_EXTS]
    return any(os.path.isfile(os.path.join(DOCS, c)) and
               os.path.getsize(os.path.join(DOCS, c)) > 0 for c in candidates)


def main():
    manifest = json.load(open(MANIFEST))
    copied = fetched = 0
    todo = []
    for target, info in sorted(manifest.items()):
        dest = os.path.join(DOCS, target)
        if already_have(target):
            continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if info['local']:
            shutil.copyfile(info['local'], dest)
            copied += 1
        else:
            todo.append((target, info['origin'], dest))

    print(f'copied {copied} assets from the snapshots; '
          f'fetching {len(todo)} from the Wayback Machine')
    index = load_cdx_index() if todo else []
    misses, renames = [], {}
    # The Wayback Machine throttles hard; two workers keeps it answering.
    with futures.ThreadPoolExecutor(max_workers=2) as pool:
        jobs = {pool.submit(fetch_archived, t, o, index): (t, o, d)
                for t, o, d in todo}
        for job in futures.as_completed(jobs):
            target, origin, dest = jobs[job]
            data, ext, note = job.result()
            if data:
                if ext and not target.lower().endswith(ext):
                    fixed = os.path.splitext(target)[0] + ext
                    renames[target] = fixed
                    target, dest = fixed, os.path.join(DOCS, fixed)
                open(dest, 'wb').write(data)
                fetched += 1
                print(f'  ok   {target} ({len(data):,} bytes)')
            else:
                misses.append({'asset': target, 'origin': origin, 'reason': note})
                print(f'  MISS {target}  <- {origin}  ({note})')

    if renames:
        apply_renames(renames)
    print(f'\ncopied {copied}, fetched {fetched}, still missing {len(misses)}')
    os.makedirs(os.path.join(ROOT, 'build'), exist_ok=True)
    json.dump(misses, open(os.path.join(ROOT, 'build', 'missing_assets.json'), 'w'),
              indent=2)
    return 0


if __name__ == '__main__':
    sys.exit(main())
