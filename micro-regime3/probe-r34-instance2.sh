#!/usr/bin/env bash
# Confirmation of probe-r34-instance.sh, 2026-09-17: the evening's tmpfs
# instance (a, hugebin/run34-HALF) against a second tmpfs copy of the same
# bytes (b, hugebin/probe-copy-r34-HALF), alternated eight times a cell,
# a b b a a b b a a b b a a b b a, raw cycles an iteration from `-n 2N`
# less `-n N` over N, under SATURATE=1. A probe: exits 0 whatever it finds.
set -u
export GHCRTS="${GHCRTS:+$GHCRTS }-V0"  # the RTS clock off (README)
cd "$(dirname "$0")" || exit 1
tmp=$(mktemp)
# A BINARY GONE, A PROCESS THAT FAILED OR A COUNT NOT READ fails the cell,
# logged `!!`, as probe-r34-instance.sh's does (2026-10-16, by review).
count() {
  [ -x "$1" ] || { echo "!! $1 is not here to run"; return 1; }
  SATURATE=1 perf stat -x, -e cycles:u -o "$tmp" \
    "$1" classes -m glob "$2" -n "$3" > /dev/null 2>&1 \
    || { echo "!! $1 exited $? on $2"; return 1; }
  c=$(grep ',cycles:u' "$tmp" | cut -d, -f1)
  case $c in
    ''|*[!0-9]*) echo "!! perf counted no cycles of $1 on $2 ('$c')"
                 return 1 ;;
  esac
  printf '%s\n' "$c"
}
CELLS="exit scaled-rank1-m1/mut-odo-vecdims-add-in-leaf-u1 4000
gheadexit rev-cnn-L1-24x24-c1/lib-stage2-lean 200000
gheadexit small-bcast32/mut-odo-vecdims-add-in-leaf-u2 4000000"
printf '%s\n' "$CELLS" | while read -r h bench n; do
  for v in a b b a a b b a a b b a a b b a; do
    case $v in a) bin=hugebin/run34-$h ;; b) bin=hugebin/probe-copy-r34-$h ;; esac
    c1=; c2=
    if c1=$(count "$bin" "$bench" "$n") \
       && c2=$(count "$bin" "$bench" $((2 * n))); then
      echo "$v $bench $(( (c2 - c1) / n ))"
    else
      echo "$v $bench ${c2:-$c1}"
    fi
  done
done
rm -f "$tmp"
echo "done $(date -Is)"
