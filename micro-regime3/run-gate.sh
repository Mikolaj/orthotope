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
# WHAT THIS GATE FAILS ON, stated once because a gate that stops the evening
# has to earn it: THE APPARATUS, never the world. A missing binary, a selection
# that is not the arms it names, a nonzero exit, a half that asserted no heap
# state, an instrument switched on and absent from the log -- each of those
# makes the night's data unusable whatever the machine does, so each exits 1.
# A box that measures differently than it did last run is the world, and the
# evening is still valid under it: that reads, records and returns 0. The
# distinction was drawn 2026-08-23 after the machine check stopped Run 18 and
# cost the hours it was meant to save; the other paths here were walked the
# same day and all of them are apparatus, as are preflight.sh's.
#
# The order is a palindrome -- other, basis, basis, other -- so each binary
# carries the same mean position and drift over the hour cannot read as a
# difference between them. Same reason the pad probe reversed its second pass,
# and the part of this a person retyping the command would most likely drop.
#
# `*/list` is in the selection for two reasons: it is the control that says
# the baseline did not move, and without a baseline `--selftest` has no
# ratios to check. The expected bench count is read from the binary, not
# written down, so a roster change does not turn a correct run into an alarm,
# and every arm SEL names is checked against `--list` before the first
# process, so a roster change that parks one -- `build` and `mut-odo`, to
# `Only` on 2026-09-04 with SEL still naming them -- refuses here rather than
# failing every process on its count after the forty minutes.
#
# About forty minutes. Read it with, for the run and the two half names,
#   ./read-run.py <run>-gate-<basis>-a.json \
#     --compare <run>-gate-<other>-a.json

# Driven by the cases in defects.py without a binary or a run: the whole gate,
# four processes and its verdict, against a stand-in that answers --list.
# A fix here wants a case there first.

set -u
cd "$(dirname "$0")" || exit 1

if [ $# -lt 1 ]; then
  echo "usage: ./run-gate.sh RUN [--show]   # e.g. run12, and it names every"
  echo "                                    # file; --show spends nothing"
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
# `--show` prints the selection and the count derived from it, spends no
# machine and exits 0. The note's `gate arms` line is written by the PREPARING
# session, hours before this script is ever run, and until 2026-09-04 the only
# way to write it was to read SEL out of this file by eye. Run 25's preparation
# did read it by eye and wrote the PREVIOUS run's five globs into its note --
# `build` and `mut-odo`, parked by the prune of that same day. preflight.sh
# calls this at its own step, so the note's line is derived from the script
# that will run and the two cannot drift.
SHOW=0
if [ $# -gt 1 ]; then
  case "$2" in
    --show) SHOW=1 ;;
    *) echo "./run-gate.sh: unknown argument '$2'"
       echo "usage: ./run-gate.sh RUN [--show]"; exit 2 ;;
  esac
fi

# The pair's two halves, as in run-major.sh and for the same reason: BASIS is
# the half the bench count is read from and the one the run's tables come
# from. Both come from the note's `HALVES:` line through pair-halves.sh, so
# the gate and the run cannot name different pairs.
HALVES_SET=$(./pair-halves.sh "$PREFIX") || exit 1   # the note's HALVES
eval "$HALVES_SET"                                # line, and nothing else
# A pair is two halves; run-major.sh says what one name in both costs. Here
# the palindrome collapses to one binary read against itself.
if [ "$OTHER" = "$BASIS" ]; then
  echo "!! OTHER and BASIS are both '$BASIS' -- a pair is two halves"
  exit 1
fi
SEL=('-m' 'glob' '*/list' '*/bq-expand' '*/mut-odo-vecdims'
     '*/sum-only-early' '*/sum-only-late')   # the form the decision of
                             # 2026-08-22 superseded and the family root, both
                             # timed from Run 25 on; `build` and `mut-odo`
                             # until the prune of 2026-09-04 parked both
ARMS=$(( ${#SEL[@]} - 2 ))   # the globs above, one bench per shape each,
                             # DERIVED because a literal drifts: run-major.sh
                             # refuses that drift for CLASSES and this had the
                             # same shape, where editing SEL alone makes all
                             # four processes report the wrong expected count
                             # and the gate exit 1 after its forty minutes

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
  echo "to live. Every pair here is hand-built, so that file is written by"
  echo "hand too, with the recipe for each half -- the only copy there is"
  echo "there is. Write it first: forty minutes of gate cannot be replayed"
  echo "from a scroll-back."
  exit 1
fi

SHAPES=$(./"$PREFIX-$BASIS" --list 2>/dev/null | cut -d/ -f1 | sort -u | wc -l)
[ "$SHAPES" -gt 0 ] || { echo "--list gave nothing; wrong binary?"; exit 1; }
# Every arm SEL names, listed once per shape BY BOTH HALVES, before the
# machine is spent. Case: `gate-refuses-an-arm-its-list-lacks`.
for h in $OTHER $BASIS; do
  LISTED=$(./"$PREFIX-$h" --list 2>/dev/null)
  for pat in "${SEL[@]:2}"; do
    n=$(printf '%s\n' "$LISTED" | grep -c "^[^/]*/${pat#*/}\$")
    [ "$n" = "$SHAPES" ] || { echo "!! SEL names $pat, which $PREFIX-$h's --list carries $n time(s) over $SHAPES shapes: an Only arm, or one renamed -- the gate would fail every process on its count after its forty minutes"; exit 1; }
  done
done
EXPECT=$((ARMS * SHAPES))
# Everything above is derivation and refusal; below is the machine. So --show
# leaves here, having paid for the roster check the loop above just made and
# for nothing else.
if [ "$SHOW" = 1 ]; then
  echo "run-gate.sh selection for $PREFIX, basis $BASIS:"
  for pat in "${SEL[@]:2}"; do echo "  glob   $pat"; done
  echo "  arms   $ARMS"
  echo "  shapes $SHAPES"
  echo "  expect $EXPECT benches a process"
  exit 0
fi
# The two binaries by content, for the block below: run-evening.sh inherits
# a clean block only for the binaries it names, so a rebuilt half gets its
# gate run again rather than the old verdict (2026-09-04).
HALVES_MD5="$BASIS=$(md5sum "./$PREFIX-$BASIS" | cut -d' ' -f1) $OTHER=$(md5sum "./$PREFIX-$OTHER" | cut -d' ' -f1)"

BAD=0                        # mechanical complaints, not the reading's verdict
PROC=0                       # of those, the ones a PROCESS raised. The line
                             # sending a reader to the logs is true only of
                             # these, and used to print for a machine-check
                             # failure too -- which sends them to four clean
                             # logs to look for a verdict about the box
RESULTS=""

run () {   # $1 = half, $2 = pass
  local half=$1 pass=$2 out rc nb
  out="${PREFIX}-gate-${half}-${pass}"
  echo "=== $(date -Is) start ${out}"
  ./"$PREFIX-${half}" "${SEL[@]}" --json "${out}.json" > "${out}.log" 2>&1
  rc=$?
  nb=$(grep -c '^benchmarking ' "${out}.log")
  echo "=== $(date -Is) done  ${out} rc=${rc} benchmarking=${nb}"
  # Named, as run-major.sh's is and for the same reason: four of these in
  # one log, and only the adjacent line saying which process each is about.
  [ "$nb" = "$EXPECT" ] || { echo "    !! $out: expected $EXPECT, got $nb -- the selection is not the $ARMS arm(s) SEL names"; BAD=$((BAD + 1)); PROC=$((PROC + 1)); }
  [ "$rc" = 0 ] || { echo "    !! nonzero exit -- read ${out}.log before trusting anything from it"; BAD=$((BAD + 1)); PROC=$((PROC + 1)); }
  # THE LAUNCH SWITCHES, asserted here as run-major.sh asserts them and
  # sooner: this gate is forty minutes and the run it stands before is
  # several hours, so a binary that cannot assert what the launch line
  # asked of it is worth catching on the rehearsal rather than on the
  # evening. Each is asked for only when its own switch is set, so an
  # uninstrumented pair run without either is silent here -- which is
  # what the launch-env line below records instead.
  if [ -n "${SATURATE:-}" ] && [ "${SATURATE}" != 0 ]; then
    [ "$(grep -c '^@@saturate ' "${out}.log")" = 1 ] || { echo "    !! $out: SATURATE=$SATURATE was set and this log does not carry exactly one @@saturate line -- the process did not assert its state"; BAD=$((BAD + 1)); PROC=$((PROC + 1)); }
  fi
  if [ -n "${WILDLOG:-}" ] && [ "${WILDLOG}" != 0 ]; then
    [ "$(grep -c '^@@wild ' "${out}.log")" -gt 0 ] || { echo "    !! $out: WILDLOG=$WILDLOG was set and this log carries no @@wild stamps -- the instrument is not in this binary, and the run this gate stands before would be uninstrumented"; BAD=$((BAD + 1)); PROC=$((PROC + 1)); }
  fi
  RESULTS="${RESULTS}
    ${out}  rc=${rc} benchmarking=${nb}"
}

echo "=== $(date -Is) gate begins; expecting $EXPECT benches a process"
# THE LAUNCH ENVIRONMENT, recorded set or unset as run-major.sh records it
# and for its reason: a gate run without the switches proves the pair
# mechanically and nothing about the instrument the evening is for.
echo "=== $(date -Is) launch env: WILDLOG=${WILDLOG-unset}\
 SATURATE=${SATURATE-unset}; $NOTE's LAUNCH block says what this pair wants"
run "$OTHER" a
run "$BASIS" a
run "$BASIS" b
run "$OTHER" b
echo "=== $(date -Is) gate complete"

# THE ONE CHECK THAT ASKS ABOUT THE BOX AND NOT THE CODE, added 2026-08-14.
# `list` is the denominator of every published ratio and the arm measured
# insusceptible to placement, and the run file's fingerprint keeps its net per
# call per shape -- so the previous run's absolutes are in runs/ after its JSONs
# are gone, and this needs no artifact kept. The gate's own selection carries
# `*/list` and both `sum-only` halves on every shape, so the comparison is net
# against net, and it happens HERE because this is the cheapest hour to learn
# it. IT DOES NOT GATE, since 2026-08-23: a box that moved between runs cannot
# reach a within-run claim, which is every claim a run publishes, so
# stopping for it buys nothing and costs the night. Run 18 stopped here at
# +4.81% and the evening went on waiting for `run anyway, re-baseline`, an
# answer never in doubt. The mode now returns 0 for a moved box, whichever way
# and however far, and 1 only for a comparison it cannot make at all. What it
# reads is the geomean against the 0.82% worst excursion eleven kept processes
# show, with the per-shape residual beside it telling a level shift from a
# move the shapes disagree on -- a single shape wandering 7% being ordinary.
MACHINE=$(./read-run.py "$PREFIX-gate-$BASIS-a.json" --machine 2>&1)
MACHINE_RC=$?
printf '%s\n' "$MACHINE"
if [ "$MACHINE_RC" != 0 ]; then
  BAD=$((BAD + 1))
  RESULTS="$RESULTS
      !! the machine check FAILED -- read it before the evening"
fi
# A moved box is not a failure and must still be impossible to miss. The whole
# reading goes into the note below; this puts one line where the complaints are,
# so a reader skimming the verdict meets it there. Advisory: not counted in BAD,
# and deliberately not spelled `!!`, which this file reserves for what stops a
# run -- the distinction being the whole point of the change above.
case $MACHINE in
  *'BOX MOVED'*)
    RESULTS="$RESULTS
      -- the box MOVED since the fingerprint. The run goes ahead; the write-up
         owes a paragraph naming it, and the box question goes to a person
         once the machine is free. The reading is below." ;;
esac

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
    [ "$PROC" -eq 0 ] ||
      echo "  Expected $EXPECT benches a process. Read the logs before anything else."
  fi
  echo "    halves md5: $HALVES_MD5"
  echo "  The machine check, which is not a reading but an answer:"
  printf '%s\n' "$MACHINE" | sed 's/^/    /'
  echo "  That is exit codes and counts; the reading is still to do, with"
  echo "    ./read-run.py $PREFIX-gate-$BASIS-a.json \\"
  echo "      --compare $PREFIX-gate-$OTHER-a.json"
  echo "    ./read-run.py $PREFIX-gate-$BASIS-a.json --pair bq-expand mut-odo-vecdims"
  echo "  Write its verdict above this block, where a reader looking up from"
  echo "  the end meets it first; a note carrying a 'not yet run' line loses"
  echo "  that line with the same edit."
} >> "$NOTE"
echo "=== appended to $NOTE"
[ "$BAD" -eq 0 ] || exit 1
