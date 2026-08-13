#!/usr/bin/env bash
# The gate a paired run wants before its evening: five benches over the shape
# set, on both halves, twice each.
#
#     ./run-gate.sh run12          # the run names the binaries and every file
#
# The run goes in every name this directory holds -- binaries, pair note, gate
# artifacts -- so that two runs' files cannot collide however alike their half
# names are. They can be very alike: Run 10 and Run 11 both had a half called
# `aligned`, and this script, which guards nothing and named its output
# `gate-<half>-<pass>`, silently overwrote Run 10's two aligned gate files.
# Nothing was noticed until Run 12 was being set up. A name that carries the
# run cannot do that, which is why the argument is required rather than
# defaulted.
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
# About forty minutes. Read it with, for the run and the two half names,
#   ./read-run.py <run>-gate-<basis>-a.json \
#     --compare <run>-gate-<other>-a.json

set -u
cd "$(dirname "$0")" || exit 1

if [ $# -lt 1 ]; then
  echo "usage: ./run-gate.sh RUN      # e.g. run12, and it names every file"
  exit 2
fi
PREFIX="$1"                  # the binaries, the note and this gate's own
                             # artifacts all begin with the run, so a verdict
                             # cannot land on a pair it is not about and no two
                             # runs can write the same filename. One scheme for
                             # everything a run leaves: run-major.sh names its
                             # JSONs the same way, and excludes `$R-gate-`
                             # from its relaunch guard so this does not read
                             # as a previous attempt
# The pair's two halves, as in run-major.sh and for the same reason: BASIS is
# the half the bench count is read from and the one the run's tables come
# from. Keep the two scripts' names in step, a gate being about the pair the
# run will use.
OTHER=${OTHER:-maxskippa}
BASIS=${BASIS:-maxskip}
SEL=('-m' 'glob' '*/list' '*/build' '*/mut-odo'
     '*/sum-only-early' '*/sum-only-late')
ARMS=5                       # the globs above, one bench per shape each

NOTE="$PREFIX-pair.txt"

for h in $OTHER $BASIS; do
  [ -x "./$PREFIX-$h" ] || { echo "missing ./$PREFIX-$h -- $NOTE has the recipe"; exit 1; }
done

# The note is checked HERE and not at the end, where the verdict is written.
# It used to be checked only there, after the four processes, so a pair with
# no note beside it cost the whole forty minutes before anything said the
# verdict had nowhere to live -- and a gate whose verdict cannot be recorded
# is a gate nobody will trust tomorrow. Refuse before spending the machine.
if [ ! -f "$NOTE" ]; then
  echo "no $NOTE beside the pair, so this gate's verdict would have nowhere"
  echo "to live. make-pair.py writes that file; a hand-built pair wants one"
  echo "by hand, with the recipe for each half -- which is the only copy"
  echo "there is. Write it first: forty minutes of gate cannot be replayed"
  echo "from a scroll-back."
  exit 1
fi

SHAPES=$(./"$PREFIX-$BASIS" --list 2>/dev/null | cut -d/ -f1 | sort -u | wc -l)
[ "$SHAPES" -gt 0 ] || { echo "--list gave nothing; wrong binary?"; exit 1; }
EXPECT=$((ARMS * SHAPES))

BAD=0                        # mechanical complaints, not the reading's verdict
RESULTS=""

run () {   # $1 = half, $2 = pass
  local half=$1 pass=$2 out rc nb
  out="${PREFIX}-gate-${half}-${pass}"
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
# Kept as a backstop, the note having been checked before the processes ran:
# it can only fire if something removed the file during the forty minutes.
if [ ! -f "$NOTE" ]; then
  echo "!! $NOTE went missing while the gate ran, so its verdict has nowhere"
  echo "   to live. The run artifacts are on disk regardless --"
  echo "   $PREFIX-gate-*.json/.log."
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
  echo "    ./read-run.py $PREFIX-gate-$BASIS-a.json \\"
  echo "      --compare $PREFIX-gate-$OTHER-a.json"
  echo "    ./read-run.py $PREFIX-gate-$BASIS-a.json --pair build mut-odo"
  echo "  Write its verdict above this block, where a reader looking up from"
  echo "  the end meets it first; a note carrying a 'not yet run' line loses"
  echo "  that line with the same edit."
} >> "$NOTE"
echo "=== appended to $NOTE"
[ "$BAD" -eq 0 ] || exit 1
