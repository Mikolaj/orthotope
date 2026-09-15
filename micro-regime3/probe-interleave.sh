#!/bin/bash
# Paired timing of a few cells on two binaries, A then B then A then B,
# for a machine that is quiet for minutes and not hours: per pair the
# per-iteration user cycles of each binary, differenced -n 2N against -n N
# as run-counts.sh differences instructions, and the ratio B/A; per cell
# the median ratio over the pairs and its range. The cells come from
# probe-fetches-read.py, the ones whose window crossings moved. A probe:
# an input to README, run by hand, and never a published figure -- the
# floors and the A/A copies belong to a run.
#
#     ./probe-interleave.sh A B "main/stretch-wide-2xM/lib-stage2-lean" \
#                              "runs/runs-2/lib-stage2-lean" ...
#
# A cell is POPULATION/SHAPE/ARM, population `main` or a class name.
# PAIRS (default 5) and N (default 100) from the environment. cycles:u is
# the process's own user cycles, which a busy sibling core inflates less
# than wall time and a busy sibling thread more; a quiet window is still
# what the reading wants, and the range printed says how quiet it was.
set -u
cd "$(dirname "$0")" || exit 1
[ $# -ge 3 ] || { echo "usage: ./probe-interleave.sh A B CELL [CELL...]"; exit 2; }
A=$1; B=$2; shift 2
case $A in */*) ;; *) A=./$A ;; esac
case $B in */*) ;; *) B=./$B ;; esac
PAIRS=${PAIRS:-5}; N=${N:-100}
for X in "$A" "$B"; do [ -x "$X" ] || { echo "!! $X is not an executable here"; exit 2; }; done
command -v perf > /dev/null 2>&1 || { echo "!! no perf on PATH; nothing ran"; exit 2; }
cyc() {  # cyc BINARY SEL SHAPE ARM ITERS -> user cycles of one process
  local f; f=$(mktemp)
  # shellcheck disable=SC2086
  perf stat -x, -e cycles:u -o "$f" "$1" $2 -m glob "$3/$4" -n "$5" > /dev/null 2>&1
  local c; c=$(grep 'cycles:u' "$f" | cut -d, -f1); rm -f "$f"
  case $c in ''|*[!0-9]*) echo "NaN" ;; *) echo "$c" ;; esac
}
per_iter() {  # per_iter BINARY SEL SHAPE ARM -> cycles an iteration, differenced
  local c2 c1
  c2=$(cyc "$1" "$2" "$3" "$4" $((2 * N))); c1=$(cyc "$1" "$2" "$3" "$4" "$N")
  if [ "$c2" = NaN ] || [ "$c1" = NaN ]; then echo NaN; else echo $(( (c2 - c1) / N )); fi
}
echo "# A=$A B=$B PAIRS=$PAIRS N=$N $(date -Is)"
echo "# cell  pairs(B/A)...  median  range"
for CELL in "$@"; do
  P=${CELL%%/*}; REST=${CELL#*/}; S=${REST%%/*}; ARM=${REST#*/}
  if [ "$P" = main ]; then SEL=; else SEL=classes; fi
  RATIOS=""
  for _ in $(seq "$PAIRS"); do
    a=$(per_iter "$A" "$SEL" "$S" "$ARM"); b=$(per_iter "$B" "$SEL" "$S" "$ARM")
    if [ "$a" = NaN ] || [ "$b" = NaN ] || [ "$a" -eq 0 ]; then RATIOS="$RATIOS NaN"
    else RATIOS="$RATIOS $(awk -v a="$a" -v b="$b" 'BEGIN{printf "%.4f", b/a}')"; fi
  done
  STATS=$(printf '%s\n' $RATIOS | grep -v NaN | sort -n | awk '{v[NR]=$1} END{if(NR==0){print "NaN NaN"} else {m=(NR%2)?v[(NR+1)/2]:(v[NR/2]+v[NR/2+1])/2; printf "%.4f %.4f..%.4f", m, v[1], v[NR]}}')
  echo "$CELL $RATIOS  $STATS"
done
