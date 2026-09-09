#!/usr/bin/env bash
# Name the subsystem, and test whether the cell survives being run alone.
#
# Two questions, one script, because the second is the control for the first.
#
# ALONE. Run27's cells come out of a 35-bench process. If `lib-stage1`'s 17%
# gap between the two binaries SURVIVES being run on its own, the gap belongs
# to the binary; if it VANISHES, the gap is what the 15 benches before it left
# in the block allocator, and no amount of reading the code was ever going to
# find it. Registered before running: either answer is a result, and the
# vanishing one is the stronger, since it names the mechanism outright.
#
# COUNTERS. Per call, by differencing two fixed-iteration runs in fresh
# processes -- `-n 200` minus `-n 100` over 100 -- which is the suite's own
# way of getting a per-call figure that owes nothing to criterion's analysis
# or to startup. Instructions are already known to be equal to 1.5 ppm across
# the compilers, so they are here as the control that says the differencing
# worked, and the cache and TLB lines are the reading: if the slow mode is a
# memory mode, its misses part while its instructions do not.
#
#   ./probe-flip-counters.sh [-o OUTDIR] [-b DIR] [-a ARM]...
#
# Writes nothing outside OUTDIR.

set -euo pipefail

OUT="$(cd "$(dirname "$0")" && pwd)/counters-out"
BIN="$(cd "$(dirname "$0")" && pwd)"
GROUP="flip-last-rows"
ARMS=()

while [ $# -gt 0 ]; do
  case "$1" in
    -o) OUT="$2"; shift 2;;
    -b) BIN="$2"; shift 2;;
    -g) GROUP="$2"; shift 2;;
    -a) ARMS+=("$2"); shift 2;;
    *) echo "unknown argument: $1" >&2; exit 2;;
  esac
done
[ ${#ARMS[@]} -gt 0 ] || ARMS=(lib-stage1 lib-stage2-lean
                               mut-odo-vecdims-add-in-leaf-u2
                               mut-odo-vecdims-add-in-leaf-u2-last
                               mut-odo-vecdims)

# Match Run 27's own launch environment; SATURATE is the block-pool preamble
# and a leg without it is a different program state (see probe-flip-reroll.sh).
: "${SATURATE:=1}"
: "${WILDLOG:=1}"
export SATURATE WILDLOG

command -v perf >/dev/null || { echo "perf is not on PATH" >&2; exit 2; }
for h in g912 ghead; do
  [ -x "$BIN/run27-$h" ] || { echo "missing $BIN/run27-$h" >&2; exit 2; }
done
LOAD=$(cut -d' ' -f1 /proc/loadavg)
if [ "${FORCE-0}" != 1 ] && awk "BEGIN{exit !($LOAD > 0.35)}"; then
  echo "load average is $LOAD; this wants a quiet box (FORCE=1 to override)." >&2
  exit 2
fi
mkdir -p "$OUT"

# Keep only what this kernel will actually count, and decide that by the
# EXIT STATUS of the invocation the probe itself will run -- not by grepping
# perf's wording. The first form of this loop grepped for "not supported" and
# friends and so kept `all_l2_cache_misses` and `l3_read_miss_latency`, which
# `perf list` prints and `-e` rejects with "event syntax error"; the whole
# counter half of the probe then failed with a usage message and produced no
# file at all. `all_l2_cache_misses` is kept in the candidates deliberately,
# as the filter's own control: a run that does not drop it is a run whose
# filter has stopped working.
#
# Five events and not six: the sixth multiplexes on this PMU, which scales
# every count and adds noise to a differencing that exists to be exact.
CAND=(instructions:u cycles:u cache-references:u cache-misses:u
      L1-dcache-load-misses:u all_l2_cache_misses)
EVENTS=()
for e in "${CAND[@]}"; do
  if perf stat -e "$e" -x, -o /dev/null -- true >/dev/null 2>&1
  then EVENTS+=("$e"); else echo "dropping event $e (perf rejects it)"; fi
done
[ ${#EVENTS[@]} -gt 0 ] || { echo "no countable events" >&2; exit 2; }
case " ${EVENTS[*]} " in
  *" all_l2_cache_misses "*)
    echo "the filter kept an event known to be rejected here; it is broken" >&2
    exit 2;;
esac
EV=$(IFS=,; echo "${EVENTS[*]}")
echo "counting: $EV"

{
  echo "# probe-flip-counters $(date -Is) group=$GROUP load=$LOAD"
  echo "# events $EV"
  echo "# env WILDLOG=$WILDLOG SATURATE=$SATURATE"
  for h in g912 ghead; do
    echo "# run27-$h $(md5sum "$BIN/run27-$h" | cut -d' ' -f1)"
  done
} > "$OUT/provenance.txt"

for h in g912 ghead; do
  for arm in "${ARMS[@]}"; do
    # `-m glob` and not the bare positional, which is a PREFIX: the legs
    # of 2026-09-09 selected ten benches for `mut-odo-vecdims` and four
    # for `-add-in-leaf-u2`, and the reader quoted the first of each.
    # The pattern carries no wildcard, so glob matching is exact match.
    # The reader counts the reports and refuses a leg holding more than
    # one, which is the only check on a selector here -- `--list` prints
    # nothing at all once one is given.
    sel="$GROUP/$arm"
    # (1) the alone leg: criterion's own estimate, one bench per process.
    j="$OUT/alone-$h-$arm.json"
    [ -f "$j" ] || {
      echo "== alone $h $arm"
      "$BIN/run27-$h" classes -m glob "$sel" --json "$j" \
           > "$OUT/alone-$h-$arm.log" 2>&1
    }
    # (2) the counter legs, fresh process each, differenced by the reader.
    for n in 100 200; do
      f="$OUT/perf-$h-$arm-n$n.txt"
      [ -f "$f" ] || {
        echo "== perf $h $arm n=$n"
        perf stat -e "$EV" -x, -o "$f" -- \
          "$BIN/run27-$h" classes -m glob "$sel" -n "$n" \
          > "$OUT/perf-$h-$arm-n$n.log" 2>&1 || true
      }
    done
  done
done

echo
echo "read it with:  ./probe-flip-counters-read.py $OUT"
