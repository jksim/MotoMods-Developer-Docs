# Google Play listings

The five sample Android apps the documentation tells you to install — MDK
Utility, Audio, Battery, Display and Sensor — were distributed only through
Google Play. Every listing now returns 404.

The apps' **source is preserved in full** (see `docs/about.md`); it is the
published binaries that are gone. They are not recoverable from any
authoritative source:

- no `.apk` was ever committed to any of the repositories
- none of the repositories has a GitHub release, so nothing was attached to one
- no `.apk` appears anywhere in the site captures
- the Wayback Machine cannot have one: Google Play never served APKs from a
  fetchable URL, so no crawler could reach the binary

Rebuilding from source would not reproduce them either. The published apps used
`com.motomodsdev.*` package ids while the open-source repositories build
`com.motorola.samples.*`, so Motorola published from a configuration that is not
in the public source — and a rebuild would carry a different signing key.

What is here is the listing pages themselves, as the Wayback Machine captured
them: app descriptions, screenshots and version metadata. They are stored as
captured (`id_` replay, without the Wayback toolbar). `index.json` records each
app's Play URL, capture timestamp and extracted metadata.

`com.motomodsdev.mdkaudio` has no usable capture and so is absent.

## Third-party mirrors

Copies appear to exist on apkcombo, listed as version 1.00.006 dated December
2017 — a version string that matches the `versionName` in the preserved source.
APKMirror has nothing; APKPure blocks automated requests, so it is unknown.

Nothing from those mirrors is included here. A binary from an APK mirror cannot
be shown to be Motorola's build from metadata alone, and no published hash or
surviving listing exists to check one against.

The check that would settle it is the APK's signature, which cannot be forged.
`tools/verify_apks.sh <directory>` runs it: for every APK in a directory it
prints the package and version, whether the signature actually covers the
archive's contents — so a repack fails even when it carries the original
certificate file — and the signing certificate's subject and SHA-256
fingerprint. Five APKs that verify and share one certificate naming Motorola
are almost certainly the original builds; anything self-signed, debug-signed or
mismatched is not.

Both mirrors gate downloads behind bot protection (a Cloudflare challenge on
APKPure, a JavaScript token flow on apkcombo), so the files have to be fetched
by hand in a browser before they can be checked.
