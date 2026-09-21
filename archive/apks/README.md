# Sample application binaries

Four of the five sample apps the documentation tells you to install, as
published by Motorola. They were distributed only through Google Play, and
every listing is now gone; these were recovered from a third-party mirror and
then verified.

## Provenance

A binary from an APK mirror proves nothing by itself — but a signature cannot
be forged, and `apksigner` checks that the signature actually covers the
archive's contents, so a repack fails even when it carries the original
certificate file. All four verify under one certificate:

```
CN=Common MotoBLUR 2-1-1, OU=MMI, O=Motorola, L=Libertyville, ST=Illinois, C=US
RSA 2048, issued 2011-03-15, valid to 2036-03-15
SHA-256  c463fa2a0351086dd6328d9daf6218146ee1651521c1cb6b4c538f85eeec7a3c
```

That is Motorola Mobility's own release key — MMI, at Motorola's Libertyville,
Illinois address. These are Motorola's builds.

`index.json` records each file's package, version, size, SHA-256 and signer.

## What is not here: MDK Sensor

The fifth app failed verification and is deliberately excluded. Its signature
is valid, but the certificate is the stock Android debug key:

```
CN=Android Debug, O=Android, C=US      RSA 1024
```

That is the throwaway key Android Studio generates for local builds. Google
Play refuses to accept APKs signed with it, so this cannot be the binary
Motorola published — it is somebody's own build of the open-source project,
passed off by the mirror as the app. Its source is preserved like the others.

## A note on versions

These are version 1.00.003. The source repositories carry `versionName
1.00.006`, and the archived Play listing for MDK Utility also shows 1.00.006,
so a later release existed that this mirror did not have. What is here is
authentic but not the final published version.

## Verifying for yourself

```console
$ tools/verify_apks.sh archive/apks
```
