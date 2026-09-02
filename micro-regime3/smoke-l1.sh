#!/usr/bin/env bash
# The pre-run list's step 12, the L1 ROSTER PASS, in one call.
#
#     ./smoke-l1.sh run22                  # main set + the scaled class
#     ./smoke-l1.sh run22 scaled runs      # and a leg per class named
#     ./smoke-l1.sh run22                  # the basis from the note's HALVES line
#
# Step 12 is owed when `--list` changed membership and the pair note
# records no pass. It is not a measurement: what it asks is whether the
# BASIS half runs the whole roster at -L1 and whether every single-file
# reader mode can read what comes out, which is where a structural fault
# shows -- Run 20's sunk sum-only cells, and Run 22's eight main-set
# cells whose forcing term is not smaller than the cell.
#
# WHICH CLASSES TO NAME. Any class serves the three-shape branch of
# `--block` only if it HAS three shapes: six do, `bcastmid` and
# `reshape1` have four and `runs` has eleven, so the default is `scaled`
# -- one of the five that crossed from two to three. Name a class
# besides whenever its population moved since the last pass, as `runs`
# had when it went from seven views to eleven: a reader mode that has
# never seen a population is exactly what this pass is for.
#
# WHAT IT DOES NOT DO. It does not touch the control half: step 12 is
# the BASIS's, the bench counts being read from it. It does not gate a
# figure -- the elapsed times it records are a sanity reading against
# the previous pass and nothing more, and it does not want a quiet
# machine. And it writes nothing of record: the outcome goes in the
# pair note by hand, on the `L1 ROSTER PASS:` line, because a pass
# recorded for a roster that has since moved is worse than none.
#
# THE NAMESPACE. Artifacts are `smoke-l1-$R-*`, which is the sanctioned
# scratch prefix and NOT the run's own -- nothing that reads `$R-*.json`
# or `$R-*.log` may see them (README, THE RUN'S PREFIX BELONGS TO THE
# RUN'S OWN PROCESSES). It refuses to run over a previous attempt's
# artifacts rather than overwriting them, as run-alonelegs.sh does:
# silently overwriting one is how a pass gets credited to the wrong
# roster.
#
# Exit 0 clean, 1 with findings, 2 when the run did not happen.
#
# NON-VACUITY, 2026-08-31, demonstrated rather than asserted, with a
# stub named outside every namespace here (`zzsmoke-stub-g912`, made and
# removed in one call) standing in for the basis half. It answers
# `--list`, `classes --list` and the class filter, and writes `{}` for
# its JSON:
#   * MISCOUNT=1, so it lists 10 benches and benchmarks 9, FAILs the
#     count check with `expected 10, got 9` on the main leg and
#     `expected 3, got 2` on the class one, and exits 1;
#   * the SAME stub unbroken passes both counts, which is the control
#     that says the FAIL above was the miscount and not the stub -- and
#     it then FAILs the required-mode gate, every mode refusing a `{}`
#     JSON, which is that stage's own non-vacuity and the reason the
#     stage is split into required and reported modes at all: it could
#     not fail before, so a leg whose every mode refused read clean;
#   * a class matching no bench exits 2, naming the class;
#   * a basis binary that is not there exits 2, naming it;
#   * an artifact of a previous attempt exits 2, naming the file;
#   * no argument at all exits 2 with the usage.
# Read those exits without a pipe: a pipeline reports its LAST command's
# status, which is how this proof read `exit=0` off a refusal the first
# time it was taken.
set -u
cd "$(dirname "$0")" || exit 1

if [ $# -lt 1 ]; then
  echo "usage: ./smoke-l1.sh RUN [CLASS ...]     # e.g. ./smoke-l1.sh run22 scaled runs"
  exit 2
fi
R=$1; shift
CLASSES=${*:-scaled}
HALVES_SET=$(./pair-halves.sh "$R") || exit 1   # the note's HALVES
eval "$HALVES_SET"                                # line, and nothing else
BIN="./$R-$BASIS"

[ -x "$BIN" ] || { echo "!! no $BIN -- wrong run, wrong BASIS, or the half is not built"; exit 2; }

# The expected counts come from the binary and never from a literal: a
# roster that grew makes a literal wrong and the pass credit the wrong
# number, which is the drift run-major.sh refuses for classes.
EXPECT_MAIN=$("$BIN" --list 2>/dev/null | wc -l)
[ "$EXPECT_MAIN" -gt 0 ] || { echo "!! $BIN --list is empty"; exit 2; }

declare -a LEGS=(main) EXPECT=("$EXPECT_MAIN")
for c in $CLASSES; do
  n=$("$BIN" classes --list 2>/dev/null | grep -c "^$c-")
  [ "$n" -gt 0 ] || { echo "!! class '$c' matches no bench of $BIN"; exit 2; }
  LEGS+=("$c"); EXPECT+=("$n")
done

for leg in "${LEGS[@]}"; do
  for f in "smoke-l1-$R-$leg.json" "smoke-l1-$R-$leg.log"; do
    [ -e "$f" ] && { echo "!! $f is here already -- a previous attempt's, and this pass will not overwrite it"; exit 2; }
  done
done

LOG="smoke-l1-$R.log"
[ -e "$LOG" ] && { echo "!! $LOG is here already -- move it aside first"; exit 2; }
: > "$LOG"
say () { echo "$*" | tee -a "$LOG"; }

say "=== $R: the L1 roster pass on the $BASIS half, ${#LEGS[@]} leg(s)"
BAD=0
for i in "${!LEGS[@]}"; do
  leg=${LEGS[$i]}; want=${EXPECT[$i]}
  out="smoke-l1-$R-$leg"
  t0=$SECONDS
  if [ "$leg" = main ]; then
    "$BIN" -L1 --json "$out.json" > "$out.log" 2>&1; rc=$?
  else
    "$BIN" classes "$leg-" -L1 --json "$out.json" > "$out.log" 2>&1; rc=$?
  fi
  el=$((SECONDS - t0))
  got=$(grep -c '^benchmarking' "$out.log")
  msg="  $leg rc=$rc benchmarking=$got elapsed=${el}s"
  if [ "$rc" -ne 0 ]; then msg="$msg  !! nonzero exit"; BAD=$((BAD + 1)); fi
  if [ "$got" != "$want" ]; then msg="$msg  !! expected $want, got $got"; BAD=$((BAD + 1)); fi
  say "$msg"
done

if [ "$BAD" -ne 0 ]; then
  say "=== $BAD finding(s) in the legs; the reader modes are not run over a bad pass"
  exit 1
fi

# Every single-file mode, over every leg, and the modes are in two
# groups because a stage that cannot fail is a stage nobody reads. The
# REQUIRED ones must exit 0 or the pass has a finding; the rest are
# asked outside their kind on purpose and are named rather than counted
# -- --deflation wants the riders, which the pass does not take, and
# --extremes wants --classes. Which group a mode is in depends on the
# leg: --block wants a stride class and refuses on the main set,
# --machine wants a population the run file's fingerprint holds and so
# refuses on a class.
say "=== every single-file reader mode over each leg"
ALWAYS=("" "--shapes" "--aa" "--aa --brief" "--claims" "--steps" "--cells" \
        "--markdown" "--fingerprint" "--selftest")
OPTIONAL=("--deflation" "--extremes")
for i in "${!LEGS[@]}"; do
  leg=${LEGS[$i]}; f="smoke-l1-$R-$leg.json"
  if [ "$leg" = main ]; then
    REQUIRED=("${ALWAYS[@]}" "--machine"); SKIPPED=("${OPTIONAL[@]}" "--block" "--block --brief")
  else
    REQUIRED=("${ALWAYS[@]}" "--block" "--block --brief"); SKIPPED=("${OPTIONAL[@]}" "--machine")
  fi
  failed=""
  for m in "${REQUIRED[@]}"; do
    ./read-run.py "$f" $m > /dev/null 2>&1 || failed="$failed ${m:-(default)}(rc=$?)"
  done
  refused=""
  for m in "${SKIPPED[@]}"; do
    ./read-run.py "$f" $m > /dev/null 2>&1 || refused="$refused ${m:-(default)}"
  done
  if [ -n "$failed" ]; then
    say "  $leg: !! REQUIRED mode(s) failed ->$failed"
    BAD=$((BAD + 1))
  else
    say "  $leg: all ${#REQUIRED[@]} required modes exit 0; refused outside their kind ->${refused:- none}"
  fi
done

if [ "$BAD" -ne 0 ]; then
  say "=== $BAD finding(s); the pass is NOT clean"
  exit 1
fi

say "=== pass clean; write it on the pair note's L1 ROSTER PASS: line,"
say "    with the roster it was taken on -- it belongs to the pair"
exit 0
