#!/usr/bin/env bash
# The gate a paired run wants before its evening: five benches over the shape
# set, on both halves, twice each.
#
#     ./run-gate.sh
#
# The order is a palindrome -- other, basis, basis, other -- so each binary
# carries the same mean position and drift over the hour cannot read as a
# difference between them. Same reason the pad probe reversed its second pass,
# and the part of this a person retyping the command would most likely drop.
#
# `*/list` is in the selection for two reasons: it is the control that says
# the baseline did not move, and without a baseline `--selftest` has no
# ratios to check. The expected bench count is read from the binary, not
# written down, so a roster change does not turn a correct run into an alarm.
#
# About forty minutes. Read it with, for the two half names set below,
#   ./read-run.py gate-<basis>-a.json --compare gate-<other>-a.json

set -u
cd "$(dirname "$0")" || exit 1

PREFIX=micro                 # the binaries and the note are all one name, so
                             # a verdict cannot land on a pair it is not about
# The pair's two halves, as in run-major.sh and for the same reason: BASIS is
# the half the bench count is read from and the one the run's tables come
# from. Keep the two scripts' names in step, a gate being about the pair the
# run will use.
OTHER=${OTHER:-maxskip}
BASIS=${BASIS:-aligned}
SEL=('-m' 'glob' '*/list' '*/build' '*/mut-odo'
     '*/sum-only-early' '*/sum-only-late')
ARMS=5                       # the globs above, one bench per shape each

NOTE="$PREFIX-pair.txt"

for h in $OTHER $BASIS; do
  [ -x "./$PREFIX-$h" ] || { echo "missing ./$PREFIX-$h -- $NOTE has the recipe"; exit 1; }
done

SHAPES=$(./"$PREFIX-$BASIS" --list 2>/dev/null | cut -d/ -f1 | sort -u | wc -l)
[ "$SHAPES" -gt 0 ] || { echo "--list gave nothing; wrong binary?"; exit 1; }
EXPECT=$((ARMS * SHAPES))

BAD=0                        # mechanical complaints, not the reading's verdict
RESULTS=""

run () {   # $1 = half, $2 = pass
  local half=$1 pass=$2 out rc nb
  out="gate-${half}-${pass}"
  echo "=== $(date -Is) start ${out}"
  ./"$PREFIX-${half}" "${SEL[@]}" --json "${out}.json" > "${out}.log" 2>&1
  rc=$?
  nb=$(grep -c '^benchmarking ' "${out}.log")
  echo "=== $(date -Is) done  ${out} rc=${rc} benchmarking=${nb}"
  [ "$nb" = "$EXPECT" ] || { echo "    !! expected $EXPECT, got $nb -- the selection is not the five arms"; BAD=$((BAD + 1)); }
  [ "$rc" = 0 ] || { echo "    !! nonzero exit -- read ${out}.log before trusting anything from it"; BAD=$((BAD + 1)); }
  RESULTS="${RESULTS}
    ${out}  rc=${rc} benchmarking=${nb}"
}

echo "=== $(date -Is) gate begins; expecting $EXPECT benches a process"
run "$OTHER" a
run "$BASIS" a
run "$BASIS" b
run "$OTHER" b
echo "=== $(date -Is) gate complete"

# The gate belongs to the pair, so its verdict is recorded beside the pair
# rather than in a session's memory. README's procedure leans on this, and the
# note is named after $PREFIX rather than found by an `ls -t` glob: with two
# pairs in the directory that glob returns whichever note was touched last,
# which is how a gate of THIS pair would come to be filed under another's.
#
# What goes in is the mechanical half only -- four exit codes and four bench
# counts, which is what this script knows. Whether the pair is sound is the
# reading's verdict and a person's to write, so the line says which half it
# is; an unconditional "the gate ran" is what a truncated JSON behind a green
# scroll-back looks like.
if [ ! -f "$NOTE" ]; then
  echo "!! no $NOTE beside the pair, so the gate's verdict has nowhere to live."
  echo "   make-pair.py writes that file; a hand-built pair wants one by hand."
  echo "   The run artifacts are on disk regardless -- gate-*.json and .log."
  exit 1
fi
{ if [ "$BAD" -eq 0 ]; then
    echo "GATE: run $(date -Is). Mechanically clean: four processes, each"
    echo "  exit 0 with the $EXPECT benches asked for.$RESULTS"
  else
    echo "GATE: run $(date -Is). Mechanically FAILED, $BAD complaint(s):$RESULTS"
    echo "  Expected $EXPECT benches a process. Read the logs before anything else."
  fi
  echo "  That is exit codes and counts; the reading is still to do, with"
  echo "    ./read-run.py gate-$BASIS-a.json --compare gate-$OTHER-a.json"
  echo "    ./read-run.py gate-$BASIS-a.json --pair build mut-odo"
  echo "  Write its verdict here, and delete the 'not yet run' line above."
} >> "$NOTE"
echo "=== appended to $NOTE"
[ "$BAD" -eq 0 ] || exit 1
