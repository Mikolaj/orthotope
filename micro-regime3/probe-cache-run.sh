#!/bin/bash
# The timed half of the past-cache probe: the two past-cache views on
# probe-cache-spot, the four arms the question is about beside `list` and
# the forcing controls the correction needs, one process, under the launch
# environment every recorded process has carried since Run 21.
#
# WANTS A QUIET MACHINE: a DRAM-bound reading is exactly what a
# neighbour's memory traffic moves. Minutes. Artifacts
# probe-cache-runs.{json,log} and probe-cache-wallclock.log; read with
#   ./read-run.py probe-cache-runs.json --pair lib-stage2 lib-stage1 --per-shape
# and the same for lib-stage2-disp against each route.
set -u
cd "$(dirname "$0")" || exit 1
BIN=./probe-cache-spot
[ -x "$BIN" ] || { echo "no $BIN here: run ./probe-cache-build.sh first"; exit 2; }
for f in probe-cache-runs.json probe-cache-runs.log; do
  [ -e "$f" ] && { echo "$f exists already; move it aside first"; exit 2; }
done
BUSY=$(./machine-busy.sh)
[ "${BUSY%.*}" -lt 5 ] || { echo "machine $BUSY% busy: not a quiet window"; exit 2; }
SEL=()
for arm in list sum-only-early sum-only-late \
           lib-stage1 lib-stage2 lib-stage2-disp mut-odo-vecdims; do
  SEL+=("runs-cache-*/$arm")
done
WANT=$(( 2 * ${#SEL[@]} ))
echo "=== $(date -Is) probe-cache begins on $BIN, md5 $(md5sum "$BIN" | cut -d' ' -f1), $WANT benches expected" \
  | tee probe-cache-wallclock.log
WILDLOG=1 SATURATE=1 "$BIN" classes -m glob "${SEL[@]}" --json probe-cache-runs.json \
  > probe-cache-runs.log 2>&1
rc=$?
nb=$(grep -c '^benchmarking ' probe-cache-runs.log)
echo "=== $(date -Is) done rc=$rc benchmarking=$nb of $WANT expected" | tee -a probe-cache-wallclock.log
[ "$rc" = 0 ] && [ "$nb" = "$WANT" ]
