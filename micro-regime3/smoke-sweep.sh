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
# a third in whatever regime the shell happens to carry. About two minutes.
#
# What it proves: every mode runs, each table installer found its table and
# wrote something, and the claims installer refuses the filtered run this
# sweep necessarily is. What it does not: that the right rows went to the
# right place -- that guarantee is `install`'s, and the README paragraph
# under this block says so.

set -u
cd "$(dirname "$0")" || exit 1

if [ $# -lt 1 ]; then
  echo "usage: ./smoke-sweep.sh RUN      # e.g. run14, and it names the pair"
  exit 2
fi
R="$1"
OTHER=${OTHER:-a1g}          # the pair's two halves, as in run-major.sh and
BASIS=${BASIS:-lookrts}      # run-gate.sh: keep the three in step

SHAPE=${SHAPE:-cnn-slice-c32}      # the smallest main-set shape, so the
CLASS=${CLASS:-window-28x28-k5}    # sweep is minutes; the class one
                                   # exercises --block
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
mode smoke.json --cells --exclude concat-runs
mode smoke.json --cells --exclude-shape lenet-L1-28-c1-k5
mode smoke.json --claims          # reads the page's verdicts back too, so
                                  # this is also the read-back's only
                                  # pre-run exercise

echo "=== the installers, into a copy and never at README"
cp README.md README.smoke.md
mode smoke.json --markdown --in-place --readme README.smoke.md
mode smoke.json --fingerprint --in-place --readme README.smoke.md
mode smoke-class.json --block --in-place --readme README.smoke.md
# The fourth installer is exercised by its REFUSAL, which is the only
# answer available here: a one-shape run holds none of the claims' arms,
# and the claims install refuses a filtered run rather than writing a
# subset. So nonzero is the pass, and a zero exit would mean it installed
# a claims section out of five arms. Non-vacuous 2026-08-16, the block run
# standalone: silent over a filtered run, and over a FULL one -- where the
# install succeeds -- it reports that the refusal did not happen.
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
