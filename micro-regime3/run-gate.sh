#!/usr/bin/env bash
# The gate a paired run wants before its evening: four arms over the `rev`
# stride class, on both halves, twice each.
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
# has to earn it: THE APPARATUS, never the world. A missing binary, a
# selection that is not the arms it names, a nonzero exit, a half that
# asserted no heap state, an instrument switched on and absent from the log
# -- each of those makes the night's data unusable whatever the machine
# does, so each exits 1. A box that measures differently than it did last
# run is the world, and the evening is still valid under it: the evening's
# machine check, which left this script on 2026-10-05, reads and records it
# and stops nothing. The distinction was drawn 2026-08-23 after the machine
# check stopped Run 18 and cost the hours it was meant to save; the other
# paths here were walked the same day and all of them are apparatus, as are
# preflight.sh's.
#
# The order is a palindrome -- other, basis, basis, other -- so each binary
# carries the same mean position and drift over the gate cannot read as a
# difference between them. Same reason the pad probe reversed its second pass,
# and the part of this a person retyping the command would most likely drop.
#
# ONE SMALL CLASS AND FOUR ARMS since 2026-10-05, by the owner, where it was
# the main set's nineteen shapes and five arms: `rev`'s three views carry
# the one attribution the gate earned -- Run 41's `bq-expand` build outlier,
# 1.3542 across the halves on `rev` against 1.3048 to 1.3142 on Runs 40
# and 42 to 45, as the main set read it at 1.3620 -- and the run is five
# minutes where it was thirty-three. `scaled` would have missed it, reading
# `bq-expand` level on every run. The machine check left with the main set,
# for run-evening.sh to take on the main-set basis JSON after the sequence.
#
# `*/list` is in the selection for two reasons: it is the control that says
# the baseline did not move, and without a baseline `--selftest` has no
# ratios to check; the two `sum-only` halves are the forcing pass every net
# the readings divide is corrected by. The expected bench count is read from
# the binary, not written down, so a roster change does not turn a correct run
# into an alarm, and every arm SEL names is checked against `classes --list`
# before the first process, so a roster change that parks one -- `build` and
# `mut-odo`, to `Only` on 2026-09-04 with SEL still naming them -- refuses here
# rather than failing every process on its count after the run.
#
# About five minutes. Read it with, for the run and the two half names,
#   ./read-run.py <run>-gate-<basis>-a.json \
#     --compare <run>-gate-<other>-a.json

# Driven by the cases in defects.py without a binary or a run: the whole gate,
# four processes and the block it files in the note, against a stand-in that
# answers `classes --list`. A fix here wants a case there first.

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
if [ $# -gt 2 ]; then
  # An argument absorbed without effect and without error is this tree's
  # `silent-option` family by name, and the first draft of this block read
  # $2 alone: `./run-gate.sh run25 --show anything` printed the selection
  # and exited 0, so a typed-wrong third word looked like a clean read.
  # Found 2026-09-04 by reading this back.
  echo "./run-gate.sh: too many arguments -- got $#, wanted RUN [--show]"
  exit 2
fi
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
GATE_CLASS=rev                 # the class the gate runs over, header above
SEL=('-m' 'glob' '*/list' '*/bq-expand'
     '*/sum-only-early' '*/sum-only-late')   # the form the decision of
                             # 2026-08-22 superseded beside the baseline and
                             # the forcing pass; `mut-odo-vecdims` until the
                             # gate left the main set on 2026-10-05, `build`
                             # and `mut-odo` until the prune of 2026-09-04
# What the processes are handed: the globs above, each taken over the class
# by its prefix, `*/list` becoming `rev-*/list`. SEL keeps the suffixes so
# that one list names the arms and the class is stated once.
CSEL=(classes "${SEL[0]}" "${SEL[1]}")
for pat in "${SEL[@]:2}"; do CSEL+=("$GATE_CLASS-$pat"); done
ARMS=$(( ${#SEL[@]} - 2 ))   # the globs above, one bench per view each,
                             # DERIVED because a literal drifts: run-major.sh
                             # refuses that drift for CLASSES and this had the
                             # same shape, where editing SEL alone makes all
                             # four processes report the wrong expected count
                             # and the gate exit 1 after its run

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
  echo "there is. Write it first: a gate's run cannot be replayed"
  echo "from a scroll-back."
  exit 1
fi
SHAPES=$(./"$PREFIX-$BASIS" classes --list 2>/dev/null | cut -d/ -f1 \
           | grep "^$GATE_CLASS-" | sort -u | wc -l)
[ "$SHAPES" -gt 0 ] || { echo "classes --list gave no $GATE_CLASS- view; wrong binary, or a class retired?"; exit 1; }
# Every arm SEL names, listed once per view of the class BY BOTH HALVES,
# before the machine is spent. Case: `gate-refuses-an-arm-its-list-lacks`.
for h in $OTHER $BASIS; do
  LISTED=$(./"$PREFIX-$h" classes --list 2>/dev/null)
  for pat in "${SEL[@]:2}"; do
    n=$(printf '%s\n' "$LISTED" | grep -c "^$GATE_CLASS-[^/]*/${pat#*/}\$")
    [ "$n" = "$SHAPES" ] || { echo "!! SEL names $pat, which $PREFIX-$h's classes --list carries $n time(s) over $SHAPES $GATE_CLASS view(s): an Only arm, or one renamed -- the gate would fail every process on its count after its run"; exit 1; }
  done
done
EXPECT=$((ARMS * SHAPES))
# Everything above is derivation and refusal; below is the machine. So --show
# leaves here, having paid for the roster check the loop above just made and
# for nothing else.
if [ "$SHOW" = 1 ]; then
  echo "run-gate.sh selection for $PREFIX, basis $BASIS:"
  echo "  class  $GATE_CLASS"
  for pat in "${CSEL[@]:3}"; do echo "  glob   $pat"; done
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
                             # these: a missing binary ran no process and
                             # left no log to read
RESULTS=""

run () {   # $1 = half, $2 = pass
  local half=$1 pass=$2 out rc nb bin
  out="${PREFIX}-gate-${half}-${pass}"
  # The launch path is half-bin.sh's, as run-major.sh's is, and named
  # here for the same reason: which instance ran is not in the artifacts.
  bin=$(./half-bin.sh "$PREFIX" "$half") || { echo "    !! ${out}: no binary for ${half}"; BAD=$((BAD + 1)); return; }   # BAD, not PROC: no process ran and no log exists to read
  echo "=== $(date -Is) start ${out} from ${bin}"
  "$bin" "${CSEL[@]}" --json "${out}.json" > "${out}.log" 2>&1
  rc=$?
  nb=$(grep -c '^benchmarking ' "${out}.log")
  echo "=== $(date -Is) done  ${out} rc=${rc} benchmarking=${nb}"
  # Named, as run-major.sh's is and for the same reason: four of these in
  # one log, and only the adjacent line saying which process each is about.
  [ "$nb" = "$EXPECT" ] || { echo "    !! $out: expected $EXPECT, got $nb -- the selection is not the $ARMS arm(s) SEL names"; BAD=$((BAD + 1)); PROC=$((PROC + 1)); }
  [ "$rc" = 0 ] || { echo "    !! nonzero exit -- read ${out}.log before trusting anything from it"; BAD=$((BAD + 1)); PROC=$((PROC + 1)); }
  # THE LAUNCH SWITCHES, asserted here as run-major.sh asserts them and
  # sooner: this gate is five minutes and the run it stands before is
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

# The gate belongs to the pair, so its verdict is recorded beside the pair
# rather than in a session's memory. README's procedure leans on this, and the
# note is named after $PREFIX rather than found by an `ls -t` glob: with two
# pairs in the directory that glob returns whichever note was touched last,
# which is how a gate of THIS pair would come to be filed under another's.
#
# What goes in is the mechanical half only -- four exit codes and four bench
# counts, which is what this script knows. Whether the pair is sound was the
# reading's verdict and a person's to write until 2026-10-05, when the owner
# retired it; the line still says which half it is, an unconditional "the
# gate ran" being what a truncated JSON behind a green scroll-back looks like.
# Kept as a backstop, the note having been checked before the processes ran:
# it can only fire if something removed the file while the gate ran.
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
  echo "  That is exit codes and counts. The reading is the write-up's and"
  echo "  owes no verdict here: ./read-run.py --gate-draft $PREFIX puts the"
  echo "  four readings side by side, and run-evening.sh files it."
} >> "$NOTE"
echo "=== appended to $NOTE"
[ "$BAD" -eq 0 ] || exit 1
