#!/usr/bin/env bash
# Post-run step 4a's copy test for Run 39, 2026-09-23: the eleven half-local
# movers against Run 38 all read FASTER on this run, counts level, so each
# is this run's binary, its file instance or the process. For the widest
# cell of every -u1 mover and of four of the six list-family ones, cycles
# an iteration on the timed file, on a fresh copy of it and on Run 38's
# same half, interleaved over three passes, each figure the
# difference of an -n 2N and an -n N process over N, which drops the
# process's start. The copy separates the instance from the binary: a copy
# reading with the timed file is the binary, one reading with Run 38 is the
# instance. A probe and never a check: exits 0 whatever it finds.
#
#     bash probe-r39-instance.sh > log-probe-r39-instance.txt 2>&1
set -u
cd "$(dirname "$0")" || exit 1
for h in gheadnospec gheadtwopass; do
  [ -e "probe-copy-run39-$h" ] || cp "run39-$h" "probe-copy-run39-$h"
done
# half class shape arm N; `main` is the main set, no class selector
CELLS='gheadnospec block block-run64-gap1 lib-stage2-lean-u1 4105
gheadnospec main alexnet-L1-55-c3-k11 lib-stage2-lean-u1 467
gheadnospec runs runs-16384 lib-stage2-lean-u1 279
gheadtwopass block block-run64-gap64 list-aa-distant 285
gheadtwopass compose compose-zero-mid list 21
gheadtwopass flip flip-fwd-rows96 list-aa-distant 22
gheadtwopass rev rev-cnn-L1-24x24-c1 lib-stage2-lean-u1 72810
gheadtwopass runs runs-512 list 23
gheadtwopass window window-64x64-k1x9 lib-stage2-lean-u1 17306'
ST=$(mktemp)
cyc () {  # cyc BIN SEL CELL N -> user cycles of one process
  perf stat -x, -e cycles:u -o "$ST" "./$1" $2 -m glob "$3" -n "$4" \
    > /dev/null 2>&1
  grep cycles:u "$ST" | cut -d, -f1
}
echo "pass half cell binary cycles/iter"
for pass in 1 2 3; do
  while read -r h c s a n; do
    sel=classes; [ "$c" = main ] && sel=
    for b in "run39-$h" "probe-copy-run39-$h" "run38-$h"; do
      one=$(cyc "$b" "$sel" "$s/$a" "$n")
      two=$(cyc "$b" "$sel" "$s/$a" $((2 * n)))
      echo "$pass $h $s/$a $b $(( (two - one) / n ))"
    done
  done <<< "$CELLS"
done
rm -f "$ST"
