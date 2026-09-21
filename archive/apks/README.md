# Sample application binaries

Published by Motorola on Google Play; listings removed. Recovered from a
third-party mirror.

| File | Package | Version | Signer |
| --- | --- | --- | --- |
| `mdkaudio.apk` | `com.motomodsdev.mdkaudio` | 1.00.003 | Motorola |
| `mdkbattery.apk` | `com.motomodsdev.mdkbattery` | 1.00.003 | Motorola |
| `mdkdisplay.apk` | `com.motomodsdev.mdkdisplay` | 1.00.003 | Motorola |
| `mdkutility.apk` | `com.motomodsdev.mdkutility` | 1.00.003 | Motorola |
| `mdksensor.apk` | `com.motomodsdev.mdksensor` | 1.00.002 | Android Debug |

All five signatures verify. Four are signed with Motorola's release key:

```
CN=Common MotoBLUR 2-1-1, OU=MMI, O=Motorola, L=Libertyville, ST=Illinois, C=US
RSA 2048, issued 2011-03-15, expires 2036-03-15
SHA-256  c463fa2a0351086dd6328d9daf6218146ee1651521c1cb6b4c538f85eeec7a3c
```

`mdksensor.apk` is signed with the Android Studio debug key
(`CN=Android Debug, O=Android, C=US`, RSA 1024), not Motorola's release key.

Per-file package, version, size, SHA-256 and signer: `index.json`.
Re-check with `tools/verify_apks.sh archive/apks`.

Version 1.00.006 is the latest per the source and the archived Play listing.
