#!/usr/bin/env bash
# The file-instance reading of Run 33's basis, 2026-09-16: run33-exit ran
# `runs-16384/lib-stage2-lean-u1` 15 percent slower than a byte-identical
# copy of itself, and the cached pages of the file have since been evicted.
# Part 1 times the original, the copy and Run 32's basis, twice each,
# interleaved; part 2 reads the physical frame of the fill loop's line and
# the sum loop's line in the original and the copy while each runs, which
# needs sudo. A probe and never a check: exits 0 whatever it finds.
#
#     bash probe-r33-instance.sh
set -u
cd "$(dirname "$0")" || exit 1
BENCH='runs-16384/lib-stage2-lean-u1'

echo "== part 1: cycles for 300 iterations, this run over the other two"
for i in 1 2; do
  for b in run33-exit probe-copy-r33exit run32-nospec; do
    perf stat -x, -e cycles:u -o /tmp/st-r33.txt \
      "./$b" classes runs -m glob "$BENCH" -n 300 > /dev/null 2>&1
    c=$(grep cycles:u /tmp/st-r33.txt | cut -d, -f1)
    echo "pass$i $b $c"
  done
done
rm -f /tmp/st-r33.txt

echo "== part 2: physical frames of the two hot lines, original then copy"
for b in run33-exit probe-copy-r33exit; do
  "./$b" classes runs -m glob "$BENCH" -L 60 > /dev/null 2>&1 &
  pid=$!
  sleep 10
  echo "-- $b"
  sudo python3 probe-pageflags.py "$pid" 0x430980 0x4bad80
  wait "$pid"
done
