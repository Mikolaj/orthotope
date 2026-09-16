#!/usr/bin/env bash
# The huge-page text reading, 2026-09-16: whether running a half from a
# tmpfs mounted `huge=always` makes its code frames a function of the
# layout, and what that costs the cell the frame term was priced on.
# README's placement section says why: the physical frame of a code page
# is a placement term the shim cannot set, and a 2 MiB page fixes every
# frame below 2 MiB to its virtual bits.
#
# THE MOUNT IS ROOT'S AND IS NOT MADE HERE. Once, and in /etc/fstab so it
# survives a reboot, the path under the checkout so a session sees it:
#
#   tmpfs  /home/mikolaj/r/orthotope/micro-regime3/hugebin  tmpfs  size=1g,huge=always,mode=0755,uid=1000,gid=1000  0  0
#   mkdir -p ~/r/orthotope/micro-regime3/hugebin && sudo mount hugebin
#
# Then, for a half named on the command line, this copies it into the
# mount, times the cell on the on-disk file and on the mounted copy twice
# interleaved, and reads the mounted copy's frames with probe-pageflags.py
# under sudo, expecting a contiguous run of hundreds of pages and
# `phys==virt mod 2MiB: True`. A level pair says the change costs nothing
# on this cell and buys determinism; a move is the iTLB term and goes in
# the note as such. A probe and never a check: exits 0 whatever it finds.
#
#     bash probe-hugebin.sh run33-exit
set -u
cd "$(dirname "$0")" || exit 1
HALF=${1:?the binary of one half, e.g. run33-exit}
BENCH='runs-16384/lib-stage2-lean-u1'
mountpoint -q hugebin || { echo "hugebin is not mounted here; the header says how"; exit 0; }
cp "$HALF" "hugebin/$HALF" || exit 0
md5sum "$HALF" "hugebin/$HALF"

echo "== cycles for 300 iterations of $BENCH, on disk then on the mount"
for i in 1 2; do
  for b in "./$HALF" "hugebin/$HALF"; do
    perf stat -x, -e cycles:u -o /tmp/st-hugebin.txt \
      "$b" classes runs -m glob "$BENCH" -n 300 > /dev/null 2>&1
    c=$(grep cycles:u /tmp/st-hugebin.txt | cut -d, -f1)
    echo "pass$i $b $c"
  done
done
rm -f /tmp/st-hugebin.txt

echo "== frames of the mounted copy's hot lines, the u1 fill loop then the sum loop"
"hugebin/$HALF" classes runs -m glob "$BENCH" -L 60 > /dev/null 2>&1 &
pid=$!
sleep 10
sudo python3 probe-pageflags.py "$pid" 0x430980 0x4bad80
grep -E '^(FilePmdMapped|AnonHugePages)' "/proc/$pid/smaps_rollup"
wait "$pid"
