#!/usr/bin/env bash
# The pre-run list's steps 4 to 10, in one call.
#
#     ./preflight.sh run19            # reads BASIS/OTHER as the others do
#
# Its defaults moved to Run 19's halves at pre-run step 3c on 2026-08-24,
# with run-major.sh's, run-gate.sh's, smoke-sweep.sh's and
# install-tables.sh's -- BASIS unchanged, OTHER from g914 to ghead. The
# non-vacuity note below was taken on Run 17's pair and names its halves;
# re-reading it wants `OTHER=det BASIS=wildlog` on the launch line, which
# is what those two variables are for.
#
# Eight tool calls became one. That is not the point: the point is that
# step 8 is the one README says is skipped most often, and a script cannot
# skip it. Each step below prints PASS or FAIL with what it read, and the
# exit status is the whole verdict -- so this is a thing to run, not to
# pipe, `tail` having eaten a nonzero status here before (README, the
# session notes on not piping a verification command).
#
# WHAT IT DOES NOT DO, and each is deliberate:
#   9b, the pair's own variable -- what the halves differ in is checked by
#       the command the PAIR NOTE names, or by the note saying which
#       variable leaves no trace. There is no general form of it, and a
#       script that guessed one would report a pair sound on a reading
#       that was never about that pair.
#   10a/10b, the --survey legs -- the build's, and their answer is the
#       binary's rather than the reading session's, so they go in the note
#       at 3b and not here. And 10's own `--library` figure is a registered
#       variable of the pair, read against the note and not against any
#       threshold here, so its PASS says the figure was read and no more.
#   11 and 12, the smoke sweep and the roster pass -- machine time, and
#       properties of the pair rather than of the session, so they are
#       recorded in the note and inherited. Running them here would pay for
#       them again.
#   13 onward -- the run list, which wants a quiet machine and a go-ahead.
#
# Non-vacuity, 2026-08-22, and demonstrated rather than asserted: two stub
# halves outside the run's namespace -- `zzrun-good` and `zzrun-bad`, made
# and removed in one call, answering `check`, `--list` and `diag` -- were
# broken one detection at a time. Halves disagreeing on `check` FAILs step
# 4,5; halves listing 9 benches against 10 FAILs step 6; a diag row ten
# times apart FAILs step 9 with `plain -O1 is ~10`. The same stubs unbroken
# PASS all three, which is the control that says the three FAILs were the
# breaks and not the stubs. On the real run17 pair it reads ten PASS and
# exits 0, reproducing every figure the Run 17 preparation read by hand:
# 1128 benches, byte-identical `check`, scan/mut 1.000, --library 25.3%.
# Step 10's zero-fill FAIL, 2026-08-23: no stub reaches it through this
# script, a stub answering `check` being no ELF, so its awk was fed
# `./loop-offsets.py /bin/true run14-lookrts` -- `0 self-loops` for the
# first -- and named /bin/true, where the run14 pair names nothing.
# RE-TAKEN 2026-08-23 against a binary that outlives run14, whose
# artifacts went the same day: `./loop-offsets.py /bin/true run18-g914`
# reads `0 self-loops` for the first and 32 for the second, so the arm
# of the check that fires on a zero fill is still reachable and still
# names the binary it fired on. Re-aim it again whenever the pair it
# names is offered for deletion.
#
# It has no ./check-scripts.py case, deliberately: this script's own steps
# are that suite and the reader's gates, so a case would run them twice to
# assert what they already assert. What is unique to it -- the three
# detections above -- is what the stub proof covers.
set -u
cd "$(dirname "$0")" || exit 1

if [ $# -lt 1 ]; then
  echo "usage: ./preflight.sh RUN      # e.g. run17"
  exit 2
fi
R=$1
OTHER=${OTHER:-ghead}
BASIS=${BASIS:-g912}
if [ "$OTHER" = "$BASIS" ]; then
  echo "!! OTHER and BASIS are both '$BASIS' -- a pair is two halves"
  exit 2
fi
for h in $OTHER $BASIS; do
  [ -x "./$R-$h" ] || { echo "missing ./$R-$h -- $R-pair.txt has the recipe"
                        exit 1; }
done

# Scratch OUTSIDE the run's own namespace: a $R-*.json or $R-*.log here is
# read by run-major.sh as a previous attempt and by read-all.sh as one of
# the run's own processes, which is how a half-written probe once turned
# eighteen clean gates into two failures (README, the Run 17 tasks).
TMP=$(mktemp -d "${TMPDIR:-/tmp}/preflight.XXXXXX") || exit 1
trap 'rm -rf "$TMP"' EXIT

BAD=0
say () {  # say STEP VERDICT DETAIL
  printf '  %-4s %-4s %s\n' "$1" "$2" "$3"
  [ "$2" = PASS ] || BAD=$((BAD + 1))
}
echo "preflight for $R: basis $BASIS, control $OTHER"
echo

"./$R-$BASIS" check > "$TMP/a.log" 2>&1; ra=$?
"./$R-$OTHER" check > "$TMP/b.log" 2>&1; rb=$?
if [ "$ra" != 0 ] || [ "$rb" != 0 ]; then
  say '4,5' FAIL "a check exited $ra/$rb -- read $TMP before it goes"
elif cmp -s "$TMP/a.log" "$TMP/b.log"; then
  say '4,5' PASS "both halves agree on every shape, byte-identical"
else
  say '4,5' FAIL "the halves' check output DIFFERS -- the pair is not sound"
fi

"./$R-$BASIS" --list 2>/dev/null > "$TMP/la"
"./$R-$OTHER" --list 2>/dev/null > "$TMP/lb"
N=$(wc -l < "$TMP/la")
if [ "$N" -eq 0 ]; then
  say 6 FAIL "--list gave nothing; wrong binary?"
elif cmp -s "$TMP/la" "$TMP/lb"; then
  say 6 PASS "$N benches, the two listings identical"
else
  say 6 FAIL "the halves ROSTER DIFFERENTLY -- one source built twice does not"
fi

./read-run.py --lint > "$TMP/lint" 2>&1 \
  && say 7 PASS "roster and shape annotations" \
  || say 7 FAIL "--lint: $(grep -m1 FAIL "$TMP/lint")"

./read-run.py --check-doc --quiet > "$TMP/doc" 2>&1 \
  && say 8 PASS "anchors, paths, widths, sweeps" \
  || say 8 FAIL "--check-doc: $(grep -m1 FAIL "$TMP/doc")"

./check-scripts.py --families > "$TMP/fam" 2>&1 \
  && say 8b PASS "defect families over this directory's Python source" \
  || say 8b FAIL "--families: $(tail -2 "$TMP/fam" | head -1)"

./check-scripts.py --properties > "$TMP/prop" 2>&1 \
  && say 8c PASS "properties over every run JSON here" \
  || say 8c FAIL "--properties: $(grep -m1 FAIL "$TMP/prop")"

./check-scripts.py > "$TMP/cs" 2>&1 \
  && say 8d PASS "every planted defect refused again" \
  || say 8d FAIL "check-scripts: $(tail -1 "$TMP/cs")"

# The regime, in the binary, which nothing later can confirm. Read as
# README reads it: baseOffsetsScan against baseOffsetsMut on vgg-14-c512,
# equal to three figures under SpecConstr and ten times apart at plain -O1.
SCAN=$("./$R-$BASIS" diag 2>/dev/null \
       | awk '/^vgg-14-c512 /{f=1} f && /baseOffsetsScan /{print $(NF-3); exit}')
MUT=$("./$R-$BASIS" diag 2>/dev/null \
      | awk '/^vgg-14-c512 /{f=1} f && /baseOffsetsMut /{print $(NF-3); exit}')
if [ -z "$SCAN" ] || [ -z "$MUT" ]; then
  say 9 FAIL "could not read the diag row; regime UNCONFIRMED"
else
  RATIO=$(python3 -c "print('%.3f' % ($SCAN/$MUT))")
  if python3 -c "import sys; sys.exit(0 if 0.98 < $SCAN/$MUT < 1.02 else 1)"
  then say 9 PASS "SpecConstr: scan/mut $RATIO on vgg-14-c512 ($SCAN vs $MUT)"
  else say 9 FAIL "regime is NOT SpecConstr: scan/mut $RATIO -- plain -O1 is ~10"
  fi
fi

# Held to what it read and not to its exit alone: the plain form exits 0
# whatever it finds, so `0 self-loops` in a half PASSed here against the
# header's "exit status is the whole verdict". Two `==` headers, one per
# half, each with a count above zero, is what a half of this benchmark
# reads -- the run-fill loop is in every build this README has timed.
if ./loop-offsets.py "$R-$OTHER" "$R-$BASIS" > "$TMP/fills" 2>&1; then
  HEADS=$(grep -c '^== ' "$TMP/fills")
  EMPTY=$(awk '/^== / && $3 == 0 { print $2 }' "$TMP/fills" | tr -d :)
  if [ "$HEADS" != 2 ]; then
    say 10 FAIL "loop-offsets reported on $HEADS half/halves, not 2"
  elif [ -n "$EMPTY" ]; then
    say 10 FAIL "no 28-byte fill at all in $(echo $EMPTY) -- a half of this?"
  else
    say 10 PASS "fills read for both halves (the comparison is yours)"
  fi
else
  say 10 FAIL "loop-offsets refused: $(tail -1 "$TMP/fills")"
fi
./loop-offsets.py --library "$R-$BASIS" "$R-$OTHER" > "$TMP/lib" 2>&1 \
  && say 10 PASS "$(grep -m1 'same offset' "$TMP/lib" | sed 's/^ *//')" \
  || say 10 FAIL "--library refused: $(tail -1 "$TMP/lib")"

# 10c. AND WHAT THE NOTE POINTS AT, which nothing else reads. The run
# file must OUTLIVE its artifacts and --check-doc now refuses one that
# names them; the pair note is the opposite -- it is MEANT to go with the
# pair -- so the rule it needs is the weaker one, that anything it cites
# outlives IT. That matters because the note is the entry point a later
# session re-enters a prepared run through, and a preparation may be days
# old, this chapter says so outright. A note pointing at a directory somebody
# tidied is a stale entry point, and the session that follows it finds out
# at the moment it is trusting the note most.
#
# Paths are taken from backticked and bare mentions of this directory's own
# artifact names. Anything outside the run's and probe's namespaces is not
# a path this can check and is left alone.
if [ -f "$R-pair.txt" ]; then
  MISSING=$(grep -oE '(probe-[A-Za-z0-9._-]+/?|'"$R"'-[A-Za-z0-9._-]+\.(json|log|txt))' \
              "$R-pair.txt" | sort -u \
            | while read -r q; do [ -e "${q%/}" ] || echo "$q"; done)
  if [ -z "$MISSING" ]; then
    say 10c PASS "every path $R-pair.txt names is still here"
  else
    say 10c FAIL "$R-pair.txt points at $(printf '%s\n' "$MISSING" | wc -l) \
path(s) that are gone: $(printf '%s ' $MISSING)"
  fi
fi

echo
if [ "$BAD" -eq 0 ]; then
  echo "all clear. NOT done here and still owed: 9b, the pair's own variable,"
  echo "which only $R-pair.txt can name; and 11 and 12, which the note records"
  echo "and a spent preparation inherits. Then the run list, from step 13."
else
  echo "$BAD step(s) FAILED -- read them before anything that costs an evening."
fi
exit $((BAD > 0))
