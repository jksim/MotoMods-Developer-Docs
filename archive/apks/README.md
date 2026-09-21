# Sample application binaries

Two sets. `index.json` and `rebuilt.json` carry per-file package, version,
size, SHA-256 and signer.

## Originals — here in `archive/apks/`

Motorola's release builds, recovered from a third-party mirror. Listings on
Google Play and the Lenovo App Store are both gone.

| File | Package | Version | Signer |
| --- | --- | --- | --- |
| `mdkaudio.apk` | `com.motomodsdev.mdkaudio` | 1.00.003 | Motorola |
| `mdkbattery.apk` | `com.motomodsdev.mdkbattery` | 1.00.003 | Motorola |
| `mdkdisplay.apk` | `com.motomodsdev.mdkdisplay` | 1.00.003 | Motorola |
| `mdkutility.apk` | `com.motomodsdev.mdkutility` | 1.00.003 | Motorola |
| `mdksensor.apk` | `com.motomodsdev.mdksensor` | 1.00.002 | Android Debug |

Motorola's release key:

```
CN=Common MotoBLUR 2-1-1, OU=MMI, O=Motorola, L=Libertyville, ST=Illinois, C=US
RSA 2048, issued 2011-03-15, expires 2036-03-15
SHA-256  c463fa2a0351086dd6328d9daf6218146ee1651521c1cb6b4c538f85eeec7a3c
```

`mdksensor.apk` carries the Android Studio debug key, not Motorola's.

## Rebuilds — served with the site from `docs/assets/apks/`

Built from the preserved source at version 1.00.006, which no mirror had. The
example pages link to these. Package ids are `com.motorola.samples.*`, as the
open-source projects declare; debug-signed, so installable.

Toolchain: Gradle 2.14.1, Android Gradle Plugin 2.2.3, JDK 8, build-tools
25.0.2 — the versions the projects specify.

Two changes are needed to build:

1. `jcenter()` is shut down. AGP 2.2.3 is on neither Google's maven nor Maven
   Central; Aliyun's jcenter mirror still serves it.
2. The Moto Mods SDK is not in the repositories. Per the documentation, put
   `modlib-01.00.000.jar` from `ModLib-01.00.000.zip` in `app/libs/` and
   `version.xml` in `app/src/main/res/values/`.

Unsigned release builds are produced by the same run but are not published.

## Verifying

```console
$ tools/verify_apks.sh archive/apks
$ tools/verify_apks.sh docs/assets/apks
```
