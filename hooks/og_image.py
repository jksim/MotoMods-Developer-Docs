"""Choose the Open Graph preview image for each page.

A page previews with its own first substantial image; pages with no usable
image of their own fall back to the site card. Resolution happens here rather
than in the template because the relative `src` in the rendered HTML has to be
turned into an absolute URL, and the image read for its dimensions.
"""
import os
import re
import struct
from urllib.parse import urljoin

IMG_SRC = re.compile(r'<img[^>]+src="([^"]+)"')
DEFAULT_CARD = 'assets/social-card.png'
# Icons and spacers make poor preview cards.
MIN_EDGE = 200
# Decorative fills that happen to be a page's first image.
SKIP = re.compile(r'background|bgimage|canvasreduced|spacer|divider', re.I)


def _dimensions(path):
    try:
        with open(path, 'rb') as fh:
            head = fh.read(32)
            if head[:8] == b'\x89PNG\r\n\x1a\n':
                return struct.unpack('>II', head[16:24])
            if head[:6] in (b'GIF87a', b'GIF89a'):
                return struct.unpack('<HH', head[6:10])
            if head[:3] == b'\xff\xd8\xff':
                fh.seek(0)
                data = fh.read()
                i = 2
                while i < len(data) - 1:
                    if data[i] != 0xFF:
                        i += 1
                        continue
                    marker = data[i + 1]
                    if marker in range(0xC0, 0xD0) and marker not in (0xC4, 0xC8, 0xCC):
                        h, w = struct.unpack('>HH', data[i + 5:i + 9])
                        return w, h
                    if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
                        i += 2
                        continue
                    if i + 4 > len(data):
                        break
                    i += 2 + struct.unpack('>H', data[i + 2:i + 4])[0]
    except (OSError, struct.error, IndexError):
        pass
    return None


def on_page_content(html, page, config, files):
    if page.meta.get('og_image'):
        return html
    site_url = (config.get('site_url') or '').rstrip('/') + '/'
    docs_dir = config['docs_dir']

    for src in IMG_SRC.findall(html):
        if src.startswith(('http://', 'https://', 'data:')):
            continue                      # off-site; not ours to advertise
        if SKIP.search(os.path.basename(src)):
            continue
        # The src is relative to the page's URL, which under directory URLs
        # sits one level deeper than the source file. Resolve it as a URL
        # first, then map that back onto docs/.
        url = urljoin(site_url + page.url, src)
        if not url.startswith(site_url):
            continue
        size = _dimensions(os.path.join(docs_dir, url[len(site_url):]))
        if not size or min(size) < MIN_EDGE:
            continue
        page.meta['og_image'] = url
        page.meta['og_image_size'] = size
        break

    if not page.meta.get('og_image'):
        page.meta['og_image'] = site_url + DEFAULT_CARD
        page.meta['og_image_size'] = _dimensions(
            os.path.join(docs_dir, DEFAULT_CARD))
        page.meta['og_image_alt'] = 'Exploded view of the Reference Moto Mod'
    return html
