#!/usr/bin/env bash
# Where a half is LAUNCHED from, since 2026-09-16: its byte-identical copy
# in hugebin/, a tmpfs mounted `huge=always` under this directory, so that
# a code page sits at its layout's offset in a 2 MiB frame and not in the
# 4 KiB frame the page cache drew when the on-disk file was first read --
# README's placement section prices that draw at 15 percent on one arm of
# Run 33's basis and 11 on one of its control. Which 2 MiB frame a copy
# gets is still a draw: two mounted copies of run34-exit parted by 7.5
# percent on one cell. The on-disk file stays the record: it is what the
# note provenances, what preflight reads, and what is offered for deletion;
# the copy is refreshed here whenever its md5 parts from the record's.
#
#     B=$(./half-bin.sh RUN HALF) || exit 2
#
# Prints the path to launch. Refuses, exit 2, when the on-disk half is not
# here or not executable. With NO mount at hugebin/ it prints the on-disk
# path and says so
# on stderr, which is the corpus's stub halves and a box without the
# mount -- a real pair is held to the mount by preflight's `launch` row
# and the run list, not here, since a refusal here would make every
# driver case want a mount. The mount, once, in /etc/fstab:
#
#   tmpfs  /home/mikolaj/r/orthotope/micro-regime3/hugebin  tmpfs  size=1g,huge=always,mode=0755,uid=1000,gid=1000  0  0
#
# then `mkdir -p hugebin && sudo mount hugebin`. A session started before
# the mount sees it from an unsandboxed call and not from a sandboxed one;
# a session started after sees it from both.
set -u
cd "$(dirname "$0")" || exit 2
[ $# -eq 2 ] || { echo "usage: B=\$(./half-bin.sh RUN HALF) || exit 2" >&2; exit 2; }
R=$1
H=$2
SRC=./$R-$H
[ -x "$SRC" ] || { echo "no $SRC here -- $R-pair.txt has the recipe" >&2; exit 2; }
# Only a real binary goes to the mount: the corpus's stub halves are shell
# scripts, and a stub launched from hugebin/ leaves its artifacts where a
# case does not look and its copy where a run's would be.
if mountpoint -q hugebin 2>/dev/null && [ "$(head -c 4 "$SRC" | tr -d '\0')" = $'\x7fELF' ]; then
  DST=hugebin/$R-$H
  if ! [ -x "$DST" ] || [ "$(md5sum < "$SRC")" != "$(md5sum < "$DST")" ]; then
    cp "$SRC" "$DST" || { echo "could not copy $SRC into hugebin/" >&2; exit 2; }
  fi
  echo "$DST"
else
  echo "half-bin: $SRC launches from disk, hugebin/ being unmounted or the" \
       "file no ELF binary; its code frames are the page cache's draw" \
       "(README, the placement section)" >&2
  echo "$SRC"
fi
