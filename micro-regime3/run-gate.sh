#!/usr/bin/env bash
# The gate a paired run wants before its evening: five benches over the shape
# set, on both halves, twice each.
#
#     ./run-gate.sh
#
# The order is a palindrome -- unaligned, aligned, aligned, unaligned -- so
# each binary carries the same mean position and drift over the hour cannot
# read as a difference between them. Same reason the pad probe reversed its
# second pass, and the part of this a person retyping the command would most
# likely drop.
#
# `*/list` is in the selection for two reasons: it is the control that says
# the baseline did not move, and without a baseline `--selftest` has no
# ratios to check. The expected bench count is read from the binary, not
# written down, so a roster change does not turn a correct run into an alarm.
#
# About forty minutes. Read it with
#   ./read-run.py gate-aligned-a.json --compare gate-unaligned-a.json

set -u
cd "$(dirname "$0")" || exit 1

SEL=('-m' 'glob' '*/list' '*/build' '*/mut-odo'
     '*/sum-only-early' '*/sum-only-late')
ARMS=5                       # the globs above, one bench per shape each

for h in unaligned aligned; do
  [ -x "./micro-$h" ] || { echo "missing ./micro-$h -- run ./make-pair.py"; exit 1; }
done

SHAPES=$(./micro-aligned --list 2>/dev/null | cut -d/ -f1 | sort -u | wc -l)
[ "$SHAPES" -gt 0 ] || { echo "--list gave nothing; wrong binary?"; exit 1; }
EXPECT=$((ARMS * SHAPES))

run () {   # $1 = half, $2 = pass
  local half=$1 pass=$2 out rc nb
  out="gate-${half}-${pass}"
  echo "=== $(date -Is) start ${out}"
  ./micro-"${half}" "${SEL[@]}" --json "${out}.json" > "${out}.log" 2>&1
  rc=$?
  nb=$(grep -c '^benchmarking ' "${out}.log")
  echo "=== $(date -Is) done  ${out} rc=${rc} benchmarking=${nb}"
  [ "$nb" = "$EXPECT" ] || echo "    !! expected $EXPECT, got $nb -- the selection is not the five arms"
}

echo "=== $(date -Is) gate begins; expecting $EXPECT benches a process"
run unaligned a
run aligned   a
run aligned   b
run unaligned b
echo "=== $(date -Is) gate complete"
