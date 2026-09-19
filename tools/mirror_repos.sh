#!/usr/bin/env bash
# Mirror-clone every upstream repository the documentation references.
#
# A fork tracks its upstream; it does not preserve it. These are full mirror
# clones — every branch, tag and note — so the code the docs describe survives
# independently of GitHub.
set -uo pipefail

DEST="${1:?usage: mirror_repos.sh <destination>}"
mkdir -p "$DEST"

REPOS=(
  nuttx                        # the Moto Mod firmware stack
  muc-loader                   # MuC bootloader
  bootrom-tools                # boot ROM tooling
  manifesto                    # hardware manifest compiler
  openocd                      # patched OpenOCD for JTAG/SWD debugging
  mdk_examples                 # umbrella examples repo
  mdkutility                   # MDK Utility app
  mdkaudio                     # audio personality card example
  mdkbattery                   # battery personality card example
  mdkdisplay                   # display personality card example
  mdksensor                    # sensor personality card example
  MotorolaMobilityLLC.github.io  # hosts the Moto Mods SDK API reference
)

fail=0
for repo in "${REPOS[@]}"; do
  target="$DEST/$repo.git"
  if [ -d "$target" ]; then
    echo "== $repo: updating"
    git --git-dir="$target" remote update --prune >/dev/null 2>&1 || { echo "   FAILED"; fail=$((fail+1)); }
  else
    echo "== $repo: cloning"
    git clone --mirror "https://github.com/MotorolaMobilityLLC/$repo.git" "$target" >/dev/null 2>&1 \
      || { echo "   FAILED"; fail=$((fail+1)); continue; }
  fi
  refs=$(git --git-dir="$target" for-each-ref | wc -l)
  commits=$(git --git-dir="$target" rev-list --all --count 2>/dev/null || echo 0)
  size=$(du -sh "$target" | cut -f1)
  echo "   $refs refs, $commits commits, $size"
done

echo
echo "mirrors in $DEST: $(ls -d "$DEST"/*.git 2>/dev/null | wc -l), failures: $fail"
exit $fail
