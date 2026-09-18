#!/bin/bash
# Task 1's within-evening form: ONE binary over the roster N times in one
# sitting. It separates per-process variation from sampling inside a bench
# directly, needing no pair and no second recipe, and README's task 1 calls
# it the cheapest unspent measurement in the file -- six A/A pairs and 570
# benches, where before the prune of 2026-09-04 it would have been sixteen
# and 1352.
#
# Run 23 took the BETWEEN-evening half: one binary twice, two evenings
# apart, the floor moving 2.12% -> 2.03% on the same carrying pair with 44
# of 49 arms inside a point. This is the other half, and the binary is
# run26-g912 -- Run 26's own basis -- so every process here is
# --compare-able with run26-g912-main.json, this morning's reading of the
# same binary at 03:19. That makes the fourth process free and the
# between-evening term a same-day one.
#
# WANTS A QUIET MACHINE. About 49 minutes a process by Run 26's own
# wallclock log (570 benches, 02:29:46 to 03:19:12 and 03:19:12 to
# 04:08:26), so the default N=3 is some two and a half hours.
#
# The launch environment is Run 21's, WILDLOG=1 SATURATE=1, exported here
# so that the processes are comparable with the run's own; probe-times.sh
# asserts both per process and complains where one is missing.
#
# Artifacts probe-within<i>-main.{json,log} and probe-within<i>-wallclock.log,
# with every stage's verdict appended to probe-within-evening.txt as it
# lands, the last line being the one to wait on.
set -u
cd "$(dirname "$0")" || exit 1

N=${N:-3}
BINARY=${BINARY:-./run26-g912}
MAXBUSY=${MAXBUSY:-5}
LOG=probe-within-evening.txt

log () { echo "=== $(date -Is) $*" | tee -a "$LOG"; }

[ -x "$BINARY" ] || { echo "no $BINARY here"; exit 2; }

# The alarm the riders and run-evening.sh take, from the one place that
# says what busy means. Taken ONCE, before the first process: a later
# process runs in whatever the box has become, which is what the log is
# for.
# AN UNREADABLE READING REFUSES BY NAME: `[ "" -lt 5 ]` refused too, at
# exit 2, behind `integer expression expected` and a message naming an
# empty percentage (2026-09-18, by review).
BUSY=$(./machine-busy.sh) || BUSY=
case $BUSY in ''|*[!0-9.]*) echo "machine-busy.sh gave no reading (${BUSY:-empty})"; exit 2 ;; esac
awk -v x="$BUSY" -v m="$MAXBUSY" 'BEGIN { exit !(x < m) }' \
  || { echo "machine $BUSY% busy: not a quiet window"; exit 2; }

export WILDLOG=1 SATURATE=1
log "within-evening series begins: $N process(es) of $BINARY, md5\
 $(md5sum "$BINARY" | cut -d' ' -f1), on the main set; alarm $BUSY% busy,\
 under the $MAXBUSY% bar"

BAD=0
for i in $(seq 1 "$N"); do
  log "process $i of $N: start"
  BIN=$BINARY OUT=probe-within$i ./probe-times.sh main
  rc=$?
  log "process $i of $N: done, rc=$rc"
  [ "$rc" = 0 ] || BAD=$((BAD + 1))
done

log "WITHIN-EVENING COMPLETE: $N process(es), complaints=$BAD -- read the\
 '!!' lines of each probe-within<i>-wallclock.log anyway, then the six A/A\
 pairs across the processes with ./read-run.py probe-within<i>-main.json --aa"
exit $((BAD > 0))
