#!/usr/bin/env bash
# The copy test of post-run step 4a on Run 34's four half-local movers
# against Run 32, 2026-09-17: does a mover belong to the binary or to a
# file instance? Each cell is timed on four instances of two binaries --
#   a  hugebin/run34-HALF       the instance the evening ran
#   b  hugebin/probe-copy-r34   a second tmpfs copy of the same bytes
#   d  hugebin/probe-copy-r32   Run 32's same half, copied to the tmpfs
#   e  ./run32-HALF             Run 32's same half from disk, as it launched
# -- cycles and instructions in user space for `-n 2N` and `-n N`, the
# difference over N, so a process's fixed cost and its preamble drop out.
# SATURATE=1, the state the evening measured in. Two passes in palindrome
# order, a b d e e d b a, so a drift over the probe cancels. A probe and
# never a check: exits 0 whatever it finds, and needs a quiet machine.
#
#     bash probe-r34-instance.sh > probe-r34-instance.log 2>&1
set -u
export GHCRTS="${GHCRTS:+$GHCRTS }-V0"  # the RTS clock off (README)
cd "$(dirname "$0")" || exit 2
mountpoint -q hugebin \
  || { echo "hugebin/ is not mounted; nothing ran"; exit 2; }
for p in "exit nospec" "gheadexit ghead"; do
  set -- $p
  cp "run34-$1" "hugebin/probe-copy-r34-$1"
  cp "run32-$2" "hugebin/probe-copy-r32-$2"
done
md5sum run34-exit hugebin/run34-exit hugebin/probe-copy-r34-exit \
       run34-gheadexit hugebin/run34-gheadexit hugebin/probe-copy-r34-gheadexit \
       run32-nospec hugebin/probe-copy-r32-nospec \
       run32-ghead hugebin/probe-copy-r32-ghead

tmp=$(mktemp)
# A BINARY GONE, A PROCESS THAT FAILED OR A COUNT NOT READ fails the cell,
# logged `!!`: an empty operand in the arithmetic below is 0, and such a
# cell was logged at 0 an iteration (2026-10-16, by review).
count() {  # count BINARY CLASS BENCH ITERS -> "cycles instructions"
  [ -x "$1" ] || { echo "!! $1 is not here to run"; return 1; }
  SATURATE=1 perf stat -x, -e cycles:u,instructions:u -o "$tmp" \
    "$1" classes -m glob "$3" -n "$4" > /dev/null 2>&1 \
    || { echo "!! $1 exited $? on $3"; return 1; }
  c=$(grep ',cycles:u' "$tmp" | cut -d, -f1)
  i=$(grep ',instructions:u' "$tmp" | cut -d, -f1)
  case "$c,$i" in
    ,*|*,|*[!0-9,]*) echo "!! perf counted no event of $1 on $3 ('$c,$i')"
                     return 1 ;;
  esac
  printf '%s %s\n' "$c" "$i"
}
# half34 half32 bench N
CELLS="exit nospec scaled-rank1-m1/mut-odo-vecdims-add-in-leaf-u1 4000
exit nospec scaled-rank1-m1/sum-only-early 8000
gheadexit ghead small-bcast32/mut-odo-vecdims-add-in-leaf-u2-aa 4000000
gheadexit ghead small-bcast32/mut-odo-vecdims-add-in-leaf-u2 4000000
gheadexit ghead small-bcast32/sum-only-early 8000000
gheadexit ghead rev-cnn-L1-24x24-c1/lib-stage2-lean 200000
gheadexit ghead rev-cnn-L1-24x24-c1/sum-only-early 400000"
echo "variant bench N cycles/iter instructions/iter"
printf '%s\n' "$CELLS" | while read -r h34 h32 bench n; do
  for v in a b d e e d b a; do
    case $v in
      a) bin=hugebin/run34-$h34 ;;
      b) bin=hugebin/probe-copy-r34-$h34 ;;
      d) bin=hugebin/probe-copy-r32-$h32 ;;
      e) bin=./run32-$h32 ;;
    esac
    r1=; r2=
    if r1=$(count "$bin" x "$bench" "$n") \
       && r2=$(count "$bin" x "$bench" $((2 * n))); then
      read -r c1 i1 <<< "$r1"; read -r c2 i2 <<< "$r2"
      echo "$v $bench $n $(( (c2 - c1) / n )) $(( (i2 - i1) / n ))"
    else
      echo "$v $bench $n ${r2:-$r1}"
    fi
  done
done
rm -f "$tmp"
echo "done $(date -Is)"
