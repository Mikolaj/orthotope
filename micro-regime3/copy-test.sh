#!/usr/bin/env bash
# Post-run step 4a's copy test, for any run: each half-local mover's cell
# timed on the run's own file, on a fresh copy of it and on the previous
# run's same half, interleaved over three passes, each figure the
# difference of an -n 2N and an -n N process over N, which drops the
# process's start. The copy separates the file instance from the build,
# and the previous run's binary the build from the evening's process.
#
#     ./copy-test.sh run41 [PREV]    # writes run41-copy-test.log
#     ./read-run.py --copy-test run41-copy-test.log
#
# The cells are `./read-run.py --copy-cells`'s, one per population and half
# that --half-movers flags with its counts level, sized to about 1.4 seconds
# a process. Until 2026-09-26 each run hand-edited the previous run's
# probe-rNN-instance.sh, which git ignores, so no run inherited one.
# WANTS THE QUIET BOX, asked for at run list step 19a or taken where the
# note says QUIET-AFTER: allowed; it refuses a busy machine as the riders do.
# A reading and never a gate: exits 0 whatever it finds, 2 where it could
# not run.
set -u
cd "$(dirname "$0")" || exit 2
if [ $# -lt 1 ] || [ $# -gt 2 ]; then
  echo "usage: ./copy-test.sh RUN [PREV]    # e.g. run41" >&2
  exit 2
fi
R=$1
CELLS=$(./read-run.py --copy-cells "$@") || exit 2
if [ -z "$CELLS" ]; then
  echo "no cell to test: --copy-cells flagged no mover with its counts level"
  exit 0
fi
BUSY=$(./machine-busy.sh) || BUSY=
if [ -z "$BUSY" ] || awk -v b="$BUSY" -v m="${MAXBUSY:-5}" \
     'BEGIN { exit !(b > m) }'; then
  echo "the machine is busy: ${BUSY:-unreadable}% of its CPUs non-idle over" \
       "two seconds, against a ${MAXBUSY:-5}% bar -- ask for the quiet box" >&2
  exit 2
fi
command -v perf > /dev/null || { echo "perf is not on PATH" >&2; exit 2; }
LOG="$R-copy-test.log"
[ -e "$LOG" ] && { echo "$LOG exists; move it aside first" >&2; exit 2; }
while read -r timed _prev _pop _cell _n; do
  [ -e "probe-copy-$timed" ] || cp "$timed" "probe-copy-$timed" || exit 2
done <<< "$CELLS"
ST=$(mktemp)
cyc () {  # cyc BIN POP CELL N -> user cycles of one process
  sel=classes; [ "$2" = main ] && sel=
  # shellcheck disable=SC2086  # an empty selector is no argument
  perf stat -x, -e cycles:u -o "$ST" "./$1" $sel -m glob "$3" -n "$4" \
    > /dev/null 2>&1
  grep cycles:u "$ST" | cut -d, -f1
}
{
  echo "# copy test of $R, $(date -Iseconds)"
  echo "pass half cell binary cycles/iter"
} > "$LOG"
for pass in 1 2 3; do
  while read -r timed prev pop cell n; do
    for b in "$timed" "probe-copy-$timed" "$prev"; do
      one=$(cyc "$b" "$pop" "$cell" "$n")
      two=$(cyc "$b" "$pop" "$cell" $((2 * n)))
      echo "$pass $timed $cell $b $(( (two - one) / n ))" | tee -a "$LOG"
    done
  done <<< "$CELLS"
done
rm -f "$ST"
echo "read it: ./read-run.py --copy-test $LOG"
