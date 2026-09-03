#!/usr/bin/env bash
# The counted work over EVERY population -- the main set and each class
# the basis binary lists, control then basis apiece -- which is the run
# list's step 20 and the second of the evening's two calls:
#
#     ./run-counts-all.sh run24 &   # the harness wakes you when it exits
#
# IT IS NOT INSIDE run-evening.sh: the counts want no quiet machine
# (run-counts.sh says why) where every stage that driver chains does, so
# this one runs beside whatever the box's owner is doing. What that bought
# and what it obliges are README's run list steps 19a and 20.
#
# It appends to `$R-evening.txt` and `$R-evening-out.txt` as run-evening.sh
# does -- one file the session reads and run-status.sh reads -- and its
# last line is EVENING COMPLETE, tallying the complaints of BOTH calls, so
# a complaint from the sequence is not lost behind a clean sweep here.
#
# WHAT STOPS IT: a status file ending at a stage still running, or at a
# stopped evening. The first is the one ordering error possible here and
# it spoils both readings, the counts and the timings they run beside; the
# second has no run to count. Nothing else does -- a population whose
# sweep refuses is a complaint and the next population runs -- and
# run-counts.sh refuses over its own previous artifact, which is what
# makes a re-take after a blocked perf safe.
#
# No launch environment, deliberately rather than by omission: an
# instruction count is what the preamble's dose is counted into and
# cancelled out of, so under SATURATE every cell would spend two doses for
# nothing.
#
# Driven by the cases in defects.py against stand-ins, every population in
# seconds (`counts-all-sweeps-every-population`, and the refusals beside
# it). A fix here wants a case there first.
set -u
cd "$(dirname "$0")" || exit 1

if [ $# -ne 1 ]; then
  echo "usage: ./run-counts-all.sh RUN &     # e.g. run24"
  exit 2
fi
R=$1
NOTE="$R-pair.txt"
STATUS="$R-evening.txt"
OUT="$R-evening-out.txt"

HALVES=$(./pair-halves.sh "$R") || exit 1
eval "$HALVES"
for h in $OTHER $BASIS; do
  [ -x "./$R-$h" ] || { echo "missing ./$R-$h -- $NOTE has the recipe"; exit 1; }
done
if [ ! -f "$STATUS" ]; then
  echo "no $STATUS, so the quiet stages have not run and the counted work"
  echo "is not what $R owes next: ./run-evening.sh $R & runs them."
  echo "Nothing ran."
  exit 1
fi
case $(tail -1 "$STATUS") in
  *': start'|*'EVENING STOPPED'*)
    echo "$STATUS does not end where the counted work begins:"
    tail -1 "$STATUS" | sed 's/^/  /'
    echo "a stage still running would be counted beside its own timings,"
    echo "and a stopped evening has no run to count. Nothing ran."
    exit 1 ;;
esac

stamp () { echo "=== $(date -Is) $*" | tee -a "$STATUS"; }
# Every sweep's own output goes to $OUT whole and one line of it to the
# status file, as run-evening.sh does it and for the same reason: the
# status file is what a session reads, and it must stay a screenful.
sweep () {   # sweep LABEL cmd...   -> the command's status, recorded.
  local label=$1; shift
  stamp "$label: start"
  { echo; echo "##### $label"; } >> "$OUT"
  "$@" >> "$OUT" 2>&1
  local rc=$?
  if [ "$rc" = 0 ]; then
    stamp "$label: done, rc=0"
  else
    stamp "$label: done, rc=$rc -- COMPLAINT, read $OUT under '##### $label'"
  fi
  return "$rc"
}

stamp "counted work begins for $R: basis $BASIS, control $OTHER"
# The main set first and then each class the basis binary lists, in its
# order, control then basis apiece.
CLASSES=$(./"$R-$BASIS" classes --list 2>/dev/null | cut -d- -f1 | awk '!seen[$0]++')
for c in '' $CLASSES; do
  for h in $OTHER $BASIS; do
    sweep "counts $h ${c:-main}" ./run-counts.sh "$R" "$h" $c || true
  done
done

# Off the status file rather than counted in this process, which is what
# carries the first call's complaints into the last line (header).
N=$(grep -c -- '-- COMPLAINT,' "$STATUS")
if [ "$N" -eq 0 ]; then
  stamp "EVENING COMPLETE: every stage of both calls exited 0. Read\
 $R-wallclock.log's '!!' lines anyway, then the post-run list, its step 0\
 first"
  exit 0
fi
stamp "EVENING COMPLETE WITH $N COMPLAINT(S) OVER BOTH CALLS -- read each\
 in $OUT before any figure; the post-run list's step 0 is still first"
exit 1
