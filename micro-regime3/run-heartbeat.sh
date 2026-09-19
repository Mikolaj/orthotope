#!/usr/bin/env bash
# The run list's heartbeat, as a command rather than as a shell loop typed
# into the chapter: one line every 45 minutes carrying the run's JSON count,
# the last stage line and the wall-clock log's last line.
#
#     ./run-heartbeat.sh run31      # armed as a PERSISTENT monitor, whose
#                                   # description is the tag `run31
#                                   # heartbeat` and nothing more
#
# NOT ARMED BY THE RUN LIST since 2026-09-19: the stage monitor tails the
# wall-clock log too, whose per-process stamps keep the session's prompt
# cache warm, so this stays for a probe watching itself and for the cases
# in defects.py. README's heartbeat paragraph carries the ruling.
#
# WHY IT IS A SCRIPT. The loop lived in README's run list, eleven lines of
# `while true`, two `2>/dev/null` redirects and a `cut -c1-90` that a
# session retyped every run -- and the list is where a fact that changes
# what an executor DOES belongs, not where a program belongs. What the
# chapter keeps is the one line that arms it and the reasons behind it.
#
# WHY 45 MINUTES AND NOT 60: the reason is the SESSION's and not the run's,
# and README's own heartbeat paragraph carries it. Overridable here so a
# short probe can watch itself without editing the chapter, and not
# overridden by any recorded run.
#
# THE TAILS TAKE `2>/dev/null` and the count survives a failed glob: for the
# first half-hour neither file exists -- run-major.sh creates the wall-clock
# log when the SEQUENCE starts, not when the evening does -- and a tick is
# wanted then as much as later, a run that died in the gate being the one a
# heartbeat is most use for. So a missing file ticks as an empty field and
# never as an error.
#
# IT NEVER EXITS, which is what `persistent` means for the monitor that
# carries it; whoever arms it stops it, and nothing here does.
#
# Driven by the cases in defects.py: one tick over a planted run, and the
# tick a run that has produced nothing yet still owes.
set -u
cd "$(dirname "$0")" || exit 1

if [ $# -ne 1 ]; then
  echo "usage: ./run-heartbeat.sh RUN     # e.g. run31, armed as a" >&2
  echo "                                  # persistent monitor; README's" >&2
  echo "                                  # heartbeat paragraph says why" >&2
  echo "                                  # the run list no longer arms it" >&2
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
