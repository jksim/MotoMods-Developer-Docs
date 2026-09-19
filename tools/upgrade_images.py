#!/usr/bin/env python3
"""Replace any image with a larger archived rendition, where one exists.

Squarespace served resized variants at `?format=NNNw` beside the original at
the bare URL, and the Wayback Machine captured an arbitrary subset of each.
A first fetch takes whichever candidate answers first, so this pass tries them
all, measures what comes back, and keeps the largest.
"""
import json, os, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_assets import (DOCS, MANIFEST, SELF, STAMPS, load_cdx_index,
                          cdx_candidates, try_url, on_disk)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def dimensions(data):
    """Pixel size of PNG/JPEG/GIF bytes, or None if it cannot be read."""
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        w, h = struct.unpack('>II', data[16:24])
        return w, h
    if data[:3] == b'\xff\xd8\xff':
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
        return None
    if data[:6] in (b'GIF87a', b'GIF89a'):
        w, h = struct.unpack('<HH', data[6:10])
        return w, h
    return None


def main():
    apply_changes = '--apply' in sys.argv
    manifest = json.load(open(MANIFEST))
    index = load_cdx_index()
    upgraded, checked = [], 0

    for target, info in sorted(manifest.items()):
        if info.get('local'):
            continue                     # came from a capture, not the archive
        current = on_disk(target)
        if not current:
            continue
        path = os.path.join(DOCS, current)
        have = dimensions(open(path, 'rb').read())
        if not have:
            continue                     # not a raster image (pdf, zip, svg)
        checked += 1

        origin = info['origin']
        src = SELF + origin if origin.startswith('/') else origin
        urls = [f'https://web.archive.org/web/{ts}id_/{u}'
                for u, ts in cdx_candidates(index, origin)]
        urls += [f'https://web.archive.org/web/{s}/{src}' for s in STAMPS[:2]]

        best, best_dim, best_url = None, have, None
        for url in urls:
            data, _, _ = try_url(current, url)
            if not data:
                continue
            got = dimensions(data)
            if got and got[0] * got[1] > best_dim[0] * best_dim[1]:
                best, best_dim, best_url = data, got, url
        if best:
            upgraded.append((current, have, best_dim, len(best)))
            print(f'  {current}: {have[0]}x{have[1]} -> {best_dim[0]}x{best_dim[1]}')
            if apply_changes:
                open(path, 'wb').write(best)

    print(f'\nchecked {checked} archive-sourced images, '
          f'{len(upgraded)} have a larger rendition available')
    if upgraded and not apply_changes:
        print('re-run with --apply to replace them')
    return 0


if __name__ == '__main__':
    sys.exit(main())
