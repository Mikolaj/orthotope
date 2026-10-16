#!/bin/bash
# A after B after C, unattended, because the one decision between them --
# the threshold rule -- was applied at 02:30 on the re-take probe-evening-a.sh
# takes first, and its answer was NO REBUILD (probe-times-note.txt). With
# that spent there is nothing left for a session to do between the halves,
# and a session that has to be awake to start the next one is dead machine
# time whenever it is not.
set -u
cd "$(dirname "$0")" || exit 1
until grep -q 'EVENING A COMPLETE' probe-bangtime-wallclock.log 2>/dev/null; do sleep 60; done
# The halves' complaints carried on, where the chain announced a complete
# evening at exit 0 whatever they said (2026-10-16, by review).
BAD=0
./probe-evening-b.sh || BAD=1
./probe-evening-c.sh || BAD=1
echo "=== $(date -Is) THE EVENING IS COMPLETE, complaints=$BAD" \
  | tee -a probe-bangtime-wallclock.log
exit $((BAD > 0))
