#!/usr/bin/env bash
# The pre-run list's step 11, as a driver rather than a block to retype.
#
#     ./smoke-sweep.sh run14         # the run names the binaries
#
# Three -L1 processes over one shape and one class, then every reader mode
# over what they wrote. It exercises the READER, not the regime and not the
# statistics: -L1 is a rougher budget than any recorded run's and its
# timings go nowhere.
#
# What it adds over pasting the block is the same thing run-major.sh adds
# over pasting the sequence -- the counting -- and one thing more: a block
# has a bottom, and a session that stops reading partway through it runs
# the first half and reports the sweep done. That happened on 2026-08-15,
# four lines from the end, and the four it missed were the `--in-place`
# installs and the `cmp` that is the only non-vacuity check in the block.
#
# It uses binaries already built rather than `cabal run`, which would build
# a third in whatever regime the shell happens to carry. Minutes -- two
# runs on an idle machine took 3m35s and about four.
#
# What it proves: every mode runs, each table installer found its table and
# wrote something, and the claims installer refuses a run that is one shape
# of the main set, which every smoke run is. What it does not: that the
# right rows went to the right place -- that guarantee is `install`'s, and
# the README paragraph under this block says so.

# Driven by ./check-scripts.py without binaries: every reader mode, both
# installers and this file's own refusal checks, in seconds. A fix here
# wants a case there first.

set -u
cd "$(dirname "$0")" || exit 1

if [ $# -lt 1 ]; then
  echo "usage: ./smoke-sweep.sh RUN      # e.g. run14, and it names the pair"
  exit 2
fi
R="$1"
OTHER=${OTHER:-a32m}         # the pair's two halves, as in run-major.sh,
BASIS=${BASIS:-lookrts}      # run-gate.sh and install-tables.sh, which
                             # carries BASIS alone: FOUR files, and pre-run
                             # step 3c is where they are set together

# A pair is two halves; run-major.sh says what one name in both costs. Here
# the control-half process sweeps the basis and the sweep still reads clean.
if [ "$OTHER" = "$BASIS" ]; then
  echo "!! OTHER and BASIS are both '$BASIS' -- a pair is two halves"
  exit 1
fi

SHAPE=${SHAPE:-cnn-slice-c32}      # the smallest main-set shape, so the
CLASS=${CLASS:-window-28x28-k5}    # sweep is minutes; the second is one
                                   # SHAPE OF a class, not the class -- it
                                   # exercises --block at 47 arms, where
                                   # the prefix `window-` would select
                                   # three shapes and 141, and the count
                                   # alarm below, which holds every
                                   # process to one shape's arms, would
                                   # read that as a failure
# Overridable so the count alarm below has a live control, there being no
# way to provoke it on today's roster otherwise: criterion's bare pattern
# is a prefix, and no bench name here extends another's. Non-vacuous
# 2026-08-15 with `CLASS=no-such-class ./smoke-sweep.sh run14`, which is
# criterion's own documented trap -- a pattern matching nothing looks
# exactly like a fast run -- and reads `expected 47, got 0`.

for h in $OTHER $BASIS; do
  [ -x "./$R-$h" ] || { echo "missing ./$R-$h -- $R-pair.txt has the recipe"; exit 1; }
done

BAD=0
ARMS=$(./"$R-$BASIS" --list 2>/dev/null | grep -c "^$SHAPE/")
[ "$ARMS" -gt 0 ] || { echo "--list has no $SHAPE; wrong binary or shape?"; exit 1; }

run () {   # $1 = artifact, $2 = half, $3.. = args
  local out=$1 half=$2; shift 2
  ./"$R-$half" "$@" --json "$out" > "${out%.json}.log" 2>&1
  local rc=$? nb
  nb=$(grep -c '^benchmarking ' "${out%.json}.log")
  echo "  $out rc=$rc benchmarking=$nb"
  [ "$rc" = 0 ] || { echo "    !! nonzero exit -- read ${out%.json}.log"; BAD=$((BAD + 1)); }
  [ "$nb" = "$ARMS" ] || { echo "    !! expected $ARMS, got $nb -- the selection is not one shape's arms"; BAD=$((BAD + 1)); }
}

mode () {  # $1 = file, $2.. = the mode
  local f=$1; shift
  ./read-run.py "$f" "$@" >/dev/null 2>&1 \
    || { echo "  !! BROKEN: $f $*"; BAD=$((BAD + 1)); }
}

echo "=== $R: three -L1 processes, $ARMS arms apiece"
run smoke.json    "$BASIS" -L1 "$SHAPE"
run smoke-other.json "$OTHER" -L1 "$SHAPE"   # the control half goes through
                             # the same counting as the other two. It used
                             # to be a bare line whose rc and count were
                             # printed and never checked, so that process
                             # could exit nonzero or select nothing and the
                             # sweep still closed "clean" -- and it is the
                             # only evidence before the evening that the
                             # control half runs at all
run smoke-class.json "$BASIS" classes "$CLASS" -L1

echo "=== every reader mode over both"
for f in smoke.json smoke-class.json; do
  for m in --selftest --aa --shapes --markdown --cells --fingerprint; do
    mode "$f" "$m"
  done
  mode "$f" --pair bq-expand list
  mode "$f"
done
mode smoke-class.json --block
mode smoke.json --compare smoke-other.json
mode smoke.json --aa --brief
mode smoke-class.json --block --brief
mode smoke.json --cells --no-controls
mode smoke.json --cells --exclude bq-expand-b   # a REAL timed arm: the name
                             # has to be one the run carries or the filter
                             # removes nothing and the mode passes without
                             # being exercised. `concat-runs` was the name
                             # here until 2026-08-17 and is registered `Only
                             # fbConcatRuns` -- checked, never timed, in no
                             # --list and so in no run JSON, ever
# --exclude-shape has no positive form here, and that is structural: this run
# is ONE shape, so the only name that could remove anything empties it. Its
# REFUSAL is the check, as with --claims below -- nonzero is the pass, and a
# zero exit would mean the filter left the shape set it was told to empty.
# The name here used to be a main-set shape this run does not carry, so the
# filter matched nothing and the check could only ever pass.
if ./read-run.py smoke.json --cells --exclude-shape "$SHAPE" \
     >/dev/null 2>&1; then
  echo "  !! --exclude-shape $SHAPE did NOT refuse a run of that shape alone"
  BAD=$((BAD + 1))
fi
mode smoke.json --claims          # reads the page's verdicts back too, so
                                  # this is also the read-back's only
                                  # pre-run exercise

echo "=== the installers, into a copy and never at README"
cp README.md README.smoke.md
mode smoke.json --markdown --in-place --readme README.smoke.md
mode smoke.json --fingerprint --in-place --readme README.smoke.md
mode smoke-class.json --block --in-place --readme README.smoke.md
# The fourth installer is exercised by its REFUSAL, which is the only
# answer available here: the claims are registered over the whole main
# set, this run is one shape of it, and the install refuses anything less
# rather than writing a claims section out of one cell. So nonzero is the
# pass, and a zero exit would mean it installed one.
#
# The first version of this block said the refusal was the ARMS guard's --
# that a one-shape run holds none of the claims' arms. It holds all
# fifteen, shape filtering removing no arm, so that guard never fired and
# what the block was reading as the refusal was an IndexError inside the
# readings themselves. It passed for two days' worth of an afternoon on a
# crash. Both were fixed on 2026-08-16, when a toy run of this very block
# found it; the shape guard is what makes the sentence above true.
#
# Non-vacuous, same day: over a one-shape run the install exits 1 saying
# which shape count it got and writes nothing, and over the full main set
# it installs and exits 0, which is what this block would report.
cp README.smoke.md README.smoke.pre
if ./read-run.py smoke.json --claims --in-place --readme README.smoke.md \
     >/dev/null 2>&1; then
  echo "  !! --claims --in-place did NOT refuse a filtered run"
  BAD=$((BAD + 1))
elif ! cmp -s README.smoke.md README.smoke.pre; then
  echo "  !! --claims --in-place refused and wrote anyway"
  BAD=$((BAD + 1))
fi
rm -f README.smoke.pre
if cmp -s README.smoke.md README.md; then
  echo "  !! --in-place wrote nothing -- the copy is identical"
  BAD=$((BAD + 1))
fi

rm -f smoke.json smoke-other.json smoke-class.json README.smoke.md \
      smoke.log smoke-other.log smoke-class.log
if [ "$BAD" -eq 0 ]; then
  echo "=== sweep clean; record it on the pair note, it belongs to the pair"
else
  echo "=== sweep FAILED, $BAD complaint(s) above"
fi
[ "$BAD" -eq 0 ] || exit 1
