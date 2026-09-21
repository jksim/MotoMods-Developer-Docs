---
title: "About This Archive"
---

# About This Archive

This site is a reconstruction. Motorola published the Moto Mods developer
documentation at `developer.motorola.com`, then retired the product and took
the portal down. What follows is what the Wayback Machine preserved of it,
converted into readable Markdown and rebuilt as a static site.

Nothing here is new writing. Where a page says "buy", "sign up" or "contact
us", it is the original 2016 copy talking to a developer who no longer exists;
those paths are dead and are kept only because removing them would misrepresent
what the documentation said.

## What was captured

Two generations of the portal were archived, and both are represented here.

**The 2016 Squarespace portal** was the complete developer site: system
architecture, eleven firmware protocols, seven Android software guides, the MDK
user guide, developer tooling, nine worked examples, hardware pages and the
partner programme. **56 of the 63 pages** on this site come from it.

**The 2017 Drupal portal** replaced it with a smaller documentation set. Most of
its pages are the same text reflowed into a new template, but a few were
genuinely revised — its *Debug and Log* and *MDK Overview* run several times
longer than the originals — and those are the versions you read here. **5 pages**
come from it, along with the downloads list and the certification programme.

Every page records its origin in the front matter of its source file:

```yaml
source_url: http://developer.motorola.com/explore/firmware/display
source_capture: 2016 Squarespace portal
```

The duplicate pages that did not earn a place in the navigation are not lost:
all **72 pages**, in every capture of them, are kept as untouched HTML in the
`archive/` directory of the repository, with `archive/index.json` recording
where each came from.

## What was recovered

| | |
| --- | --- |
| Documentation pages | 63 |
| Images and diagrams | 106 |
| Design files, schematics and archives | 8 |
| Total assets | ~23 MB |
| Assets that could not be recovered | 9 |

About a third of the images were served from `static1.squarespace.com` and were
never mirrored into the page captures. Those were recovered by querying the
Wayback Machine's CDX index for the exact archived URL — often a resized
`?format=1000w` variant, since the original URL itself was never captured — and
downloading that.

## What is missing

Nine assets exist in no capture anywhere, and the pages that used them say so
where they appeared:

**Diagrams** — `firmwaredisplay-diagram-01.png`, `fwaudio-diagram-1.png`,
`fwaudio-diagram-2.png`, `modusb-diagram-01.png`. These illustrated the display,
audio and USB protocol pages. The surrounding text is intact.

**Design files** — `mdk_back_cover_STEP.zip`,
`personality-card-assembly_STEP_0.zip`, `personality-card-housing_STEP.zip`,
`personality-card-housing_STL.zip`. The MDK schematic PDF, the back-cover STL,
the perforated PCB STEP file, ModLib and the four daughterboard hardware
archives all survived and are on the [Downloads](downloads.md) page.

Beyond assets, some things were never static pages and so could not be
captured: the developer forums (hosted by element14), the login-gated partner
material, and the contact and registration forms. Links to those are preserved
as they were written, and no longer lead anywhere.

The Moto Mods SDK for Android API reference was not lost — see below.

## How it was rebuilt

The conversion is scripted and reproducible; the tooling lives in `tools/` in
the repository.

1. **`discover.py`** walks both snapshots and identifies every Moto Mods page,
   classifying it by which portal generation served it.
2. **`manifest.py`** decides which capture becomes which page and in what order
   — the one place the site's shape is defined.
3. **`convert.py`** extracts each page's content region, drops navigation,
   tracking and dead forms, rewrites internal links and asset URLs, and
   converts to Markdown. Protocol tables are kept as HTML: they use `rowspan`,
   `colspan` and repeated header groups that a Markdown table cannot express.
4. **`fetch_assets.py`** localises every image and file, pulling from the
   captures first and the Wayback Machine second.
5. **`mark_missing.py`** annotates what could not be found.
6. **`gen_mkdocs.py`** writes the navigation.

Text was not edited. Headings, typos and all — *Software: Mod Mangement* is
spelled that way because it was spelled that way — the words are Motorola's.

## Source code links

The documentation links to the platform's source repositories — the NuttX
firmware stack, the MuC loader, the boot ROM tooling, the manifest compiler, a
patched OpenOCD, and the example projects for each personality card — and the
build instructions tell you to clone them.

Those links, including the `git clone` commands, have been repointed to copies
under [github.com/jksim](https://github.com/jksim), so that following the
instructions does not depend on the original account surviving. The copies are
standalone repositories rather than forks — pushed from verified local mirrors,
with full history, independent of the upstream fork network. This is the one
place the text has been changed rather than reproduced.

The originals were:

| Preserved copy | Original |
| --- | --- |
| `jksim/nuttx` | `MotorolaMobilityLLC/nuttx` |
| `jksim/muc-loader` | `MotorolaMobilityLLC/muc-loader` |
| `jksim/bootrom-tools` | `MotorolaMobilityLLC/bootrom-tools` |
| `jksim/manifesto` | `MotorolaMobilityLLC/manifesto` |
| `jksim/openocd` | `MotorolaMobilityLLC/openocd` |
| `jksim/mdk_examples` | `MotorolaMobilityLLC/mdk_examples` |
| `jksim/mdkutility` | `MotorolaMobilityLLC/mdkutility` |
| `jksim/mdkaudio` | `MotorolaMobilityLLC/mdkaudio` |
| `jksim/mdkbattery` | `MotorolaMobilityLLC/mdkbattery` |
| `jksim/mdkdisplay` | `MotorolaMobilityLLC/mdkdisplay` |
| `jksim/mdksensor` | `MotorolaMobilityLLC/mdksensor` |

### The sample Android apps

The example pages tell you to install five sample apps — MDK Utility, Audio,
Battery, Display and Sensor — from Google Play. All five listings now return
404, and the published binaries are not recoverable: no `.apk` was ever
committed to the repositories or attached to a release, none appears in the
site captures, and Google Play never served APKs from a URL a crawler could
reach.

The **source for all five is preserved** in the repositories above, which is
the substantive part. A rebuild would not reproduce the published apps though:
they shipped as `com.motomodsdev.*` while the open-source projects build
`com.motorola.samples.*`, so Motorola published from a configuration that is
not in the public source.

The Play listings themselves were captured by the Wayback Machine and are kept
in `archive/play-store/` — descriptions, screenshots and version metadata for
four of the five. The Play links in the documentation are left as they were
written.

All five binaries were since recovered from a third-party mirror and are kept
in `archive/apks/`, with each file's package, version, SHA-256 and signing
certificate recorded. Four carry Motorola's release signing key; MDK Sensor
carries the Android Studio debug key. They are version 1.00.003 and 1.00.002,
behind the 1.00.006 the source and the archived listing describe.

### The SDK API reference

The Moto Mods SDK for Android API reference — the javadoc for
`com.motorola.mod`, linked from every page under Android Software — was
published from a subdirectory of Motorola's GitHub Pages site. It is preserved
at [jksim/motomods_sdk](https://github.com/jksim/motomods_sdk) and served at
[jksim.github.io/motomods_sdk](https://jksim.github.io/motomods_sdk/), with the
files unchanged and at the same paths, so only the host differs from the URLs
the documentation originally used.

## Corrections

If you have a better capture of a missing diagram, spot a conversion error, or
hold rights to this material and would like it amended or removed, please open
an issue on the repository.

## Attribution

The documentation is © Motorola Mobility LLC, reproduced for historical and
educational reference. This project is not affiliated with, sponsored by, or
endorsed by Motorola, Lenovo, or Google. Moto, Moto Mods and Moto Z are
trademarks of their respective owners.
