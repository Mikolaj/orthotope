#!/usr/bin/env bash
# Does `flip-last-rows` re-roll per process, or is its cell fixed per binary?
#
# The question this answers is the one left open by the Core reading of
# 2026-09-09: on `flip-last-rows` the fill family's arms are the same twelve
# instructions, byte-identical between the two compilers and inside one cache
# line on both, yet `lib-stage1` reads 0.8284 of its basis cell on the HEAD
# half while every other shape in Run 27 stays inside 2.14%. Instructions,
# Core, assembly and loop offsets are all ruled out, so the variable is where
# the DATA lands -- the destination is a fresh 14.4 MB pinned allocation on
# every call (vector's unsafeNew -> mallocPlainForeignPtrAlignedBytes) handed
# out by the block allocator, whose state is what 34 preceding benches left.
#
# REGISTERED BEFORE RUNNING, so the verdict is not chosen after the fact:
#
#   (a) FIXED PER BINARY. Each arm's net cell reproduces across the three
#       repetitions of one binary inside that leg's own A/A spread, and the
#       g912-to-ghead gap on `lib-stage1` stays near 0.83. Then the cell is a
#       deterministic property of the executable plus the bench order, the
#       lottery is drawn at link time, and a roster change re-draws it. The
#       remedy is the A/A twin of item 13 -- a control, not a fix.
#
#   (b) PER PROCESS. Arms scatter across repetitions of ONE binary by about
#       the 15% the two bands are apart. Then no binary owns a cell, every
#       reading of this view is one draw, and the view needs repetition
#       rather than a control.
#
#   (c) THE ALLOCATOR IS THE VARIABLE. The -A legs re-roll the fill family's
#       ordering inside one binary with no code change at all. This is the
#       decisive one for the mechanism: same bytes, same offsets, only the
#       nursery moved, so what moved is placement.
#
# (a) and (b) are not exclusive of (c); (c) is what names the subsystem.
#
# The suite's own rules that bind here: one process per population, so a leg
# runs the whole `flip-last-rows` group and not one bench; halves interleaved,
# so drift is shared rather than assigned; and a quiet machine, since the
# `runs` class of Run 27 had to be re-measured for one intruding timer.
#
#   ./probe-flip-reroll.sh [-r REPS] [-o OUTDIR] [-b DIR] [--no-rts]
#
# Writes nothing outside OUTDIR. Reads the two Run 27 binaries in place.

set -euo pipefail

REPS=3
OUT="$(cd "$(dirname "$0")" && pwd)/reroll-out"
BIN="/home/mikolaj/r/orthotope/micro-regime3"
RTSLEGS=1
GROUP="flip-last-rows"

while [ $# -gt 0 ]; do
  case "$1" in
    -r) REPS="$2"; shift 2;;
    -o) OUT="$2"; shift 2;;
    -b) BIN="$2"; shift 2;;
    --no-rts) RTSLEGS=0; shift;;
    -g) GROUP="$2"; shift 2;;
    *) echo "unknown argument: $1" >&2; exit 2;;
  esac
done

# Run 27 launched every process under WILDLOG=1 SATURATE=1, and SATURATE is
# not decoration: it is the saturating preamble that sprays `cnn-slice-c32`
# copies to drive the block pool onto its plateau before a single bench runs.
# A leg without it is a different program state, so the default matches the
# run and the dose is a knob rather than an omission.
: "${SATURATE:=1}"
: "${WILDLOG:=1}"
export WILDLOG

for h in g912 ghead; do
  [ -x "$BIN/run27-$h" ] || { echo "missing binary $BIN/run27-$h" >&2; exit 2; }
done

# A busy box makes every leg a different measurement, which is the one way to
# get answer (b) for a reason that is not the program's. FORCE=1 to override.
LOAD=$(cut -d' ' -f1 /proc/loadavg)
if [ "${FORCE-0}" != 1 ] && awk "BEGIN{exit !($LOAD > 0.35)}"; then
  echo "load average is $LOAD; this wants a quiet box." >&2
  echo "re-run with FORCE=1 if you mean it, and say so in the write-up." >&2
  exit 2
fi

mkdir -p "$OUT"
NOTE="$OUT/provenance.txt"
{
  echo "# probe-flip-reroll $(date -Is) group=$GROUP reps=$REPS load=$LOAD"
  echo "# host $(uname -n) kernel $(uname -r)"
  for h in g912 ghead; do
    echo "# run27-$h $(md5sum "$BIN/run27-$h" | cut -d' ' -f1)"
  done
  echo "# env WILDLOG=$WILDLOG SATURATE=$SATURATE (default legs)"
} > "$NOTE"

leg () {           # leg <half> <cond> <rep> [-- rtsopts...]; SAT overrides dose
  local half=$1 cond=$2 rep=$3; shift 3
  local tag="$half-$cond-r$rep"
  local json="$OUT/reroll-$tag.json"
  [ -f "$json" ] && { echo "skip $tag (already there)"; return; }
  echo "== $tag dose=${SAT-$SATURATE} $(date +%H:%M:%S)"
  SATURATE="${SAT-$SATURATE}" "$BIN/run27-$half" classes "$GROUP" \
    --json "$json" "$@" > "$OUT/reroll-$tag.log" 2>&1
  echo "   exit $? $(date +%H:%M:%S)"
}

# Interleaved, control then basis, adjacent -- the run's own protocol, so a
# drift over the evening lands on both halves rather than on one.
for rep in $(seq 1 "$REPS"); do
  leg ghead default "$rep"
  leg g912  default "$rep"
done

# The knob. Same binary, same bytes, same offsets; only the nursery moves, and
# with it everything the block allocator hands out afterwards. -A32m is what
# micro.cabal bakes, so `default` above is the -A32m arm of this comparison
# and these two are its neighbours. Varying -A is forbidden for a RUN and is
# exactly the instrument for a probe.
if [ "$RTSLEGS" = 1 ]; then
  for rep in $(seq 1 "$REPS"); do
    leg g912 A16m "$rep" +RTS -A16m -RTS
    leg g912 A64m "$rep" +RTS -A64m -RTS
  done
fi

# The second knob, and the one aimed straight at the hypothesis. SATURATE
# doses the block pool before the first bench; the run used 1. If the fill
# family reorders itself between dose 0, 1 and 4 on ONE binary, then what
# decides this view's cells is the state of the pool and nothing else, which
# is the claim GHC #27601 makes about that allocator.
for rep in $(seq 1 "$REPS"); do
  SAT=0 leg g912 S0 "$rep"
  SAT=4 leg g912 S4 "$rep"
done

echo
echo "read it with:  ./probe-flip-reroll-read.py $OUT"
