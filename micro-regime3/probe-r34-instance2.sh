#!/usr/bin/env bash
# Confirmation of probe-r34-instance.sh, 2026-09-17: the evening's tmpfs
# instance (a, hugebin/run34-HALF) against a second tmpfs copy of the same
# bytes (b, hugebin/probe-copy-r34-HALF), alternated eight times a cell,
# a b b a a b b a a b b a a b b a, raw cycles an iteration from `-n 2N`
# less `-n N` over N, under SATURATE=1. A probe: exits 0 whatever it finds.
set -u
cd "$(dirname "$0")" || exit 1
tmp=$(mktemp)
count() {
  SATURATE=1 perf stat -x, -e cycles:u -o "$tmp" \
    "$1" classes -m glob "$2" -n "$3" > /dev/null 2>&1
  grep ',cycles:u' "$tmp" | cut -d, -f1
}
CELLS="exit scaled-rank1-m1/mut-odo-vecdims-add-in-leaf-u1 4000
gheadexit rev-cnn-L1-24x24-c1/lib-stage2-lean 200000
gheadexit small-bcast32/mut-odo-vecdims-add-in-leaf-u2 4000000"
printf '%s\n' "$CELLS" | while read -r h bench n; do
  for v in a b b a a b b a a b b a a b b a; do
    case $v in a) bin=hugebin/run34-$h ;; b) bin=hugebin/probe-copy-r34-$h ;; esac
    c1=$(count "$bin" "$bench" "$n"); c2=$(count "$bin" "$bench" $((2 * n)))
    echo "$v $bench $(( (c2 - c1) / n ))"
  done
done
rm -f "$tmp"
echo "done $(date -Is)"
