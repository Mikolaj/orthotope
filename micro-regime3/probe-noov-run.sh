#!/bin/bash
# Task 6's quiet process: the shim's containment test timed, off against
# on, which the open list names as the only instrument that can
# adjudicate a pad removed against a straddle introduced -- the counter
# calls it a win and the alignment survey calls it a loss.
#
# The main set rather than `runs`, both being allowed: the test is a
# LAYOUT change over the whole roster, so the population with 24 shapes
# and every arm's loops in it is the one that can see a straddle. The
# halves are two builds, so the reading is the roster's shift and the
# arms whose fills carried a pad, never one arm's absolute.
set -u
cd "$(dirname "$0")" || exit 1
export WILDLOG=1 SATURATE=1
BAD=0
for h in off on; do
  BIN=./probe-noov-$h-g912 OUT=probe-noov-$h ./probe-times.sh main \
    || { echo "!! probe-noov-$h complained"; BAD=$((BAD + 1)); }
done
# Complaints ride the COMPLETE line, as probe-evening-c's do: the line a
# session waits on is the log's last, and a complaint on stdout alone
# never reaches it.
echo "=== $(date -Is) NOOVERLAP PAIR COMPLETE, complaints=$BAD" \
  | tee -a probe-noov-off-wallclock.log
exit $((BAD > 0))
