#!/bin/bash
# The third half-hour of the evening, and the additional probe [the
# ceiling]'s seventh reading asked for by name: "whether those account for
# the measured 1.16 to 1.67 of time over instructions wants a counter
# reading of stalls and mispredicts, not another dump."
#
# The second term IS a ratio of cycles per instruction, so counting cycles
# beside instructions reads it off the counters instead of off the clock --
# a second instrument for the same quantity, owing criterion nothing -- and
# the three event columns beside them say what the cycles went on. Five
# arms and every population: the two library arms, the forcing term they
# are corrected by, the shipped fill `lib-stage1` falls through to, and the
# `list` baseline.
#
# Wants the quiet machine, cycles being load-sensitive where instructions
# are not, so it runs here rather than on a working desktop. Minutes: 285
# cells at two processes each.
set -u
cd "$(dirname "$0")" || exit 1
export ARMS="list lib-stage1 lib-stage2 mut-odo-vecdims-add-in-leaf-u2 sum-only-early"
export BIN=./probe-bang-g912
export OUT=probe-stalls-g912
BAD=0
echo "=== $(date -Is) start the stall sweep, main set"
./probe-stalls.sh || { echo "!! main set complained"; BAD=1; }
for c in rev revsome bcast bcastmid reshape1 slice window scaled runs; do
  echo "=== $(date -Is) start the stall sweep, $c"
  CLASS=$c ./probe-stalls.sh || { echo "!! $c complained"; BAD=1; }
done
echo "=== $(date -Is) EVENING C COMPLETE, complaints=$BAD" | tee -a probe-bangtime-wallclock.log
