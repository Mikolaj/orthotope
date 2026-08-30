#!/bin/bash
# The first half of the quiet evening, unattended: the `runs` re-take and
# then task 1's eight populations, all on probe-bang-g912.
#
# The re-take runs FIRST although it belongs to task 2, and the reason is
# the threshold: `lib-stage2-disp` has to be cut to the crossover the class
# measures, so the class has to be read before the arm is timed, and
# putting it at minute 30 rather than at hour four leaves the rest of this
# script as the window a rebuild fits in. Nothing else here depends on
# anything else here.
#
# About four hours by Run 21's own wall-clock log. Wait on the last line of
# probe-bangtime-wallclock.log, never on a process list.
set -u
cd "$(dirname "$0")" || exit 1
export WILDLOG=1 SATURATE=1
./probe-times.sh runs || echo "!! the re-take complained -- read the wall-clock log"
./probe-times.sh main rev revsome slice scaled window bcast bcastmid \
  || echo "!! a population complained -- read the wall-clock log"
echo "=== $(date -Is) EVENING A COMPLETE" | tee -a probe-bangtime-wallclock.log
