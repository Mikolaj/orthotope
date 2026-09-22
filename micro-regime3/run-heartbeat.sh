#!/usr/bin/env bash
# The run list's heartbeat, as a command rather than as a shell loop typed
# into the chapter: one line per tick carrying the run's JSON count,
# the last stage line and the wall-clock log's last line.
#
#     HEARTBEAT_ONCE=1 ./run-heartbeat.sh run31   # one tick, then exit:
#                                                 # the line a timed
#                                                 # waiter prints
#
# NOT ARMED BY THE RUN LIST: nothing is armed beside the evening, whose
# exit wakes the session, so this stays for a probe of an hour or two
# watching itself and for the cases in defects.py. README's paragraph
# `Nothing is armed beside the evening` carries the ruling.
#
# WHY IT IS A SCRIPT. The loop lived in README's run list, eleven lines of
# `while true`, two `2>/dev/null` redirects and a `cut -c1-90` that a
# session retyped every run -- and the list is where a fact that changes
# what an executor DOES belongs, not where a program belongs. What the
# chapter keeps is the one line that arms it and the reasons behind it.
#
# EVERY, 45 minutes by default, governs the loop only OUTSIDE a monitor: a
# monitor lives at most thirty minutes and the loop ticks once before it
# first sleeps, so under one it never reaches the sleep. Overridable so a
# short probe can watch itself without editing the chapter.
#
# THE TAILS TAKE `2>/dev/null` and the count survives a failed glob: for the
# first half-hour neither file exists -- run-major.sh creates the wall-clock
# log when the SEQUENCE starts, not when the evening does -- and a tick is
# wanted then as much as later, a run that died in the gate being the one a
# heartbeat is most use for. So a missing file ticks as an empty field and
# never as an error.
#
# IT NEVER EXITS unless HEARTBEAT_ONCE is set; whoever starts the loop
# stops it, and nothing here does.
#
# Driven by the cases in defects.py: one tick over a planted run, and the
# tick a run that has produced nothing yet still owes.
set -u
cd "$(dirname "$0")" || exit 1

if [ $# -ne 1 ]; then
  echo "usage: ./run-heartbeat.sh RUN     # e.g. run31; HEARTBEAT_ONCE=1" >&2
  echo "                                  # ticks once, for a timed waiter;" >&2
  echo "                                  # README says why the run list" >&2
  echo "                                  # arms nothing beside the evening" >&2
  exit 2
fi
R=$1
EVERY=${HEARTBEAT_SECONDS:-2700}
ONCE=${HEARTBEAT_ONCE:-}

tick () {
  local n
  n=$(ls "$R"-*.json 2>/dev/null | wc -l)
  echo "heartbeat: $n JSONs\
 | $(tail -n1 "$R-evening.txt" 2>/dev/null | cut -c1-90)\
 | $(tail -n1 "$R-wallclock.log" 2>/dev/null | cut -c1-140)"
}

while true; do
  tick
  if [ -n "$ONCE" ]; then exit 0; fi
  sleep "$EVERY"
done
