#!/usr/bin/env bash
# Where a half is LAUNCHED from: the on-disk file, hugebin/ BEING SUSPENDED
# since 2026-09-19. That mount -- a tmpfs `huge=always` under this directory
# -- held a code page at its layout's offset in a 2 MiB frame rather than in
# the 4 KiB frame the page cache drew when the on-disk file was first read,
# which README's placement section prices at 15 percent on one arm of Run
# 33's basis and 11 on one of its control. It was suspended because it does
# not come up at boot: its unit runs before /home is unlocked and exits 32,
# so it wants a root command every boot and a run may not depend on one.
# SO THE 4 KiB DRAW IS BACK, in both halves of a pair alike, and it bears on
# cross-run absolutes rather than on a pair's own two columns.
# THE MOUNT IS NOW AN EMERGENCY MEASURE, for a run whose question IS the
# placement term; the recipe below still stands for one. Which 2 MiB frame a
# copy gets was never settled anyway: two mounted copies of run34-exit parted
# by 7.5 percent on one cell, and a third reading on 2026-09-19 put the same
# instance 4.19 percent over a fresh copy, so the mount narrowed the term
# without removing it. The on-disk file is the record either way: it is what
# the note provenances, what preflight reads, and what is offered for
# deletion; a copy, where one is made, is refreshed here whenever its md5
# parts from the record's.
#
#     B=$(./half-bin.sh RUN HALF) || exit 2
#
# Prints the path to launch. Refuses, exit 2, when the on-disk half is not
# here or not executable. With NO mount at hugebin/ it prints the on-disk
# path and says so on stderr, which since the suspension is the ordinary
# case rather than the corpus's stub halves alone. NOTHING HOLDS A PAIR TO
# THE MOUNT ANY MORE: preflight's `launch` row and the run list did until
# 2026-09-19 and now only report which path was taken, so no refusal here
# was needed to lift it and none was added here. SINCE 2026-09-22
# PREFLIGHT'S 10f JUDGES THE PATH THIS SCRIPT RETURNS, failing a half that
# would launch from the mount on a run that set no PLACEMENT; the refusal is
# there and not here because this script also answers for the corpus's stub
# halves, which must keep launching wherever a case put them.
# The mount, for a run that wants it, once in /etc/fstab
# -- AND THE `noauto` IS WHY THE SUSPENSION HAPPENED, so it is not optional:
#
#   tmpfs  /home/mikolaj/r/orthotope/micro-regime3/hugebin  tmpfs  noauto,size=1g,huge=always,mode=0755,uid=1000,gid=1000  0  0
#
# then `mkdir -p hugebin && sudo mount hugebin` when a run wants it.
# WITHOUT `noauto` systemd generates a mount unit that runs AT BOOT, and on
# this box /home is not unlocked by then: the unit exits 32 with `mount point
# does not exist`, and the journal's next line is `Failed to create mount
# point ... Required key not available`, which is fscrypt saying the
# directory it wants is still encrypted. The mount point is there once
# someone has logged in, so the failure looks like a missing directory and is
# an ordering problem. Measured 2026-09-19, twice, on two reboots; the line
# above carried no `noauto` until 2026-09-20 and so failed every boot.
# A session started before the mount sees it from an unsandboxed call and not
# from a sandboxed one; a session started after sees it from both.
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
