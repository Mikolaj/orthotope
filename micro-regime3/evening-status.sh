#!/usr/bin/env bash
# The one status line a session gives when asked mid-evening, off two tails
# and a count, and nothing heavier: README's run list says a status call
# costs 0.81 of a core on a box being timed, and Run 39's session, asked,
# ran a grep over the wallclock log and a read of the previous run's beside
# it, one of them inside the window of a bench `--wild` later called
# intruded. This reads the evening's last stamp, how many processes the
# sequence has finished, and the last one it started.
#
#     ./evening-status.sh run39
#
# Cases: `evening-status-is-one-line`, `evening-status-refuses-usage`.
set -u
cd "$(dirname "$0")" || exit 1
if [ $# -ne 1 ]; then
  echo "usage: ./evening-status.sh RUN   # one line, mid-evening"
  exit 2
fi
R=$1
EV=$(tail -1 "$R-evening.txt" 2>/dev/null | sed 's/^=== //' | cut -c1-200)
W="$R-wallclock.log"
if [ -f "$W" ]; then
  DONE=$(grep -c '^=== [^ ]* done ' "$W")
  LAST=$(grep '^=== [^ ]* start ' "$W" | tail -1 | awk '{print $2, $4}')
  echo "$R: ${EV:-no $R-evening.txt}; sequence $DONE done, last start $LAST"
else
  echo "$R: ${EV:-no $R-evening.txt}; no $W yet"
fi
