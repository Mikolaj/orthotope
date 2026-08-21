#!/bin/bash
# Counted work: instructions per iteration for every timed arm on the main
# set, from two fixed-iteration processes a cell -- `-n 2N` and `-n N`, the
# difference over N -- so the count owes nothing to criterion's estimator, to
# the process's fixed cost or to the machine's load. An instruction count is
# layout-independent and repeats across builds, which is what makes it the
# second instrument README's TODO list names and Run 17's pair registers as
# a pilot.
#
#     ./run-counts.sh run17 wildlog        # the basis half, any time
#
# perf stat -e instructions:u counts the process's user-space instructions;
# kernel.perf_event_paranoid at 1 (2026-08-21) admits that without hand
# work. N comes from the environment, default 50; a cell is two processes of
# 2N and N iterations, so the sweep's length follows the slowest arm. Counts
# want no quiet machine, so this runs whenever. ONLY=<shape> and ARMS="a b"
# restrict it, for a smoke run and never for a recorded column. Output:
# RUN-counts-HALF.txt, one line a cell: shape, arm, N, instructions an
# iteration; a cell perf could not count is a `!!` line and the exit status.
set -u
cd "$(dirname "$0")" || exit 1
R="${1:?usage: ./run-counts.sh RUN HALF   # e.g. run17 wildlog}"
H="${2:?usage: ./run-counts.sh RUN HALF   # e.g. run17 wildlog}"
B=./$R-$H
[ -x "$B" ] || { echo "no $B here -- $R-pair.txt has the recipe"; exit 1; }
OUT=$R-counts-$H.txt
[ -e "$OUT" ] && { echo "$OUT exists; move it aside first"; exit 1; }
N=${N:-50}
LIST=$("$B" --list 2>/dev/null)
[ -n "$LIST" ] || { echo "!! --list gave nothing; wrong binary?"; exit 1; }
SHAPES=${ONLY:-$(printf '%s\n' "$LIST" | cut -d/ -f1 | awk '!seen[$0]++')}
ARMS=${ARMS:-$(printf '%s\n' "$LIST" | cut -d/ -f2 | awk '!seen[$0]++')}
count() {  # count SHAPE ARM ITERS -> user instructions of one process
  local f; f=$(mktemp)
  perf stat -x, -e instructions:u -o "$f" \
    "$B" -m glob "$1/$2" -n "$3" > /dev/null 2>&1
  local c; c=$(grep 'instructions:u' "$f" | cut -d, -f1); rm -f "$f"
  case $c in ''|*[!0-9]*) echo "NaN" ;; *) echo "$c" ;; esac
}
{
  echo "# $R-$H $(md5sum "$B" | cut -d' ' -f1) N=$N $(date -Is)"
  echo "# shape arm N instructions/iter"
} > "$OUT"
BAD=0
for S in $SHAPES; do
  for A in $ARMS; do
    c2=$(count "$S" "$A" $((2 * N))); c1=$(count "$S" "$A" "$N")
    if [ "$c2" = NaN ] || [ "$c1" = NaN ]; then
      echo "!! $S $A: perf could not count" >> "$OUT"; BAD=1
    else
      echo "$S $A $N $(( (c2 - c1) / N ))" >> "$OUT"
    fi
  done
done
echo "# end $(date -Is)" >> "$OUT"
exit $BAD
