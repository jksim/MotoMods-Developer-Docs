#!/usr/bin/env bash
# Report what signed each APK in a directory, and whether the signature holds.
#
# The Moto Mods sample apps were only ever published on Google Play, which is
# gone. Copies on APK mirrors cannot be shown to be Motorola's build from
# metadata alone — but a signature can't be forged. apksigner both reads the
# certificate and checks it actually covers the archive's contents, so a repack
# fails even if it carries the original certificate file.
set -uo pipefail

DIR="${1:?usage: verify_apks.sh <directory-of-apks>}"
SDK="${ANDROID_HOME:-$HOME/Android/Sdk}"
APKSIGNER=$(ls -d "$SDK"/build-tools/*/apksigner 2>/dev/null | sort -V | tail -1)
AAPT=$(ls -d "$SDK"/build-tools/*/aapt2 2>/dev/null | sort -V | tail -1)
export JAVA_HOME="${JAVA_HOME:-$HOME/android-studio/jbr}"
export PATH="$JAVA_HOME/bin:$PATH"

[ -x "$APKSIGNER" ] || { echo "apksigner not found under $SDK"; exit 1; }

shopt -s nullglob
apks=("$DIR"/*.apk)
[ ${#apks[@]} -gt 0 ] || { echo "no .apk files in $DIR"; exit 1; }

declare -A signers=()
for apk in "${apks[@]}"; do
  echo "=== $(basename "$apk")  ($(stat -c%s "$apk" | numfmt --grouping) bytes)"

  if [ -n "$AAPT" ]; then
    "$AAPT" dump badging "$apk" 2>/dev/null \
      | grep -E "^package:|^application-label:" | head -2 | sed 's/^/    /'
  fi

  out=$("$APKSIGNER" verify --print-certs --verbose "$apk" 2>&1)
  verdict=$(echo "$out" | grep -E "^(Verified using|DOES NOT VERIFY|Verifies)" | head -3 | tr '\n' ' ')
  # apksigner labels the signer differently per signature scheme: old v1 APKs
  # print "Signer #1 certificate DN", newer ones "V3.0 Signer: certificate DN".
  subject=$(echo "$out" | grep -m1 "certificate DN:"            | sed 's/.*certificate DN: //')
  sha256=$(echo "$out"  | grep -m1 "certificate SHA-256 digest:" | sed 's/.*digest: //')

  if echo "$out" | grep -q "DOES NOT VERIFY"; then
    echo "    SIGNATURE INVALID -- contents do not match the signature"
    echo "$out" | grep -m3 "ERROR" | sed 's/^/      /'
  else
    echo "    signature verifies: ${verdict:-ok}"
  fi
  echo "    signed by: ${subject:-<no certificate found>}"
  echo "    cert SHA-256: ${sha256:-n/a}"

  [ -n "$sha256" ] && signers["$sha256"]="${signers[$sha256]:-}$(basename "$apk") "
  echo
done

echo "=== signing keys across ${#apks[@]} file(s) ==="
if [ "${#signers[@]}" -eq 0 ]; then echo "  no certificates read"; exit 1; fi
for fp in "${!signers[@]}"; do
  echo "  $fp"
  echo "     ${signers[$fp]}"
done
[ "${#signers[@]}" -eq 1 ] && echo "  all files share one signing key" \
                           || echo "  ${#signers[@]} distinct signing keys -- inspect before trusting"
