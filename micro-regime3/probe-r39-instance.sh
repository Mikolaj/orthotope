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
export GHCRTS="${GHCRTS:+$GHCRTS }-V0"  # the RTS clock off (README)
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
# A BINARY GONE, A PROCESS THAT FAILED OR A COUNT NOT READ fails the cell,
# logged `!!`, as copy-test.sh's does (2026-10-16, by review): an empty
# operand in the arithmetic below is 0.
cyc () {  # cyc BIN SEL CELL N -> user cycles of one process, or fails
  [ -x "./$1" ] || { echo "!! $1 is not here to run"; return 1; }
  perf stat -x, -e cycles:u -o "$ST" "./$1" $2 -m glob "$3" -n "$4" \
    > /dev/null 2>&1 || { echo "!! $1 exited $? on $3"; return 1; }
  v=$(grep cycles:u "$ST" | cut -d, -f1)
  case $v in
    ''|*[!0-9]*) echo "!! perf counted no cycles of $1 on $3 ('$v')"
                 return 1 ;;
  esac
  printf '%s\n' "$v"
}
# EVERY CELL HELD TO EACH BINARY'S ROSTER, as probe-stalls.sh holds its
# names: a binary that lacks the shape or arm selects no bench, and its
# two empty processes differenced to a figure (2026-10-16, by review).
MISS=
while read -r h c s a n; do
  sel=classes; [ "$c" = main ] && sel=
  for b in "run39-$h" "probe-copy-run39-$h" "run38-$h"; do
    [ -x "./$b" ] || continue
    # shellcheck disable=SC2086  # an empty selector is no argument
    "./$b" $sel --list 2>/dev/null | grep -qxF "$s/$a" \
      || MISS="$MISS $b:$s/$a"
  done
done <<< "$CELLS"
echo "pass half cell binary cycles/iter"
for pass in 1 2 3; do
  while read -r h c s a n; do
    sel=classes; [ "$c" = main ] && sel=
    for b in "run39-$h" "probe-copy-run39-$h" "run38-$h"; do
      case " $MISS " in
        *" $b:$s/$a "*) echo "$pass $h $s/$a $b !! not timed by this binary"
                       continue ;;
      esac
      one=; two=
      if one=$(cyc "$b" "$sel" "$s/$a" "$n") \
         && two=$(cyc "$b" "$sel" "$s/$a" $((2 * n))); then
        echo "$pass $h $s/$a $b $(( (two - one) / n ))"
      else
        echo "$pass $h $s/$a $b ${two:-$one}"
      fi
    done
  done <<< "$CELLS"
done
rm -f "$ST"
