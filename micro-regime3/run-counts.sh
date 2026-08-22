#!/bin/bash
# Counted work: instructions per iteration for every timed arm on the main
# set, from two fixed-iteration processes a cell -- `-n 2N` and `-n N`, the
# difference over N -- so the count owes nothing to criterion's estimator, to
# the process's fixed cost or to the machine's load. An instruction count is
# layout-independent and repeats across builds, which is what makes it the
# second instrument README's TODO list names and Run 17's pair registers as
# a pilot.
#
#     ./run-counts.sh run18 g914           # the control half
#     ./run-counts.sh run18 g912           # the basis half
#
# The second argument is a HALF'S NAME and not its role, so which is the
# basis is the pair note's to say -- the same caution run-alonelegs.sh
# carries, and for the same reason it earned there.
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
# Both restrictions are read BEFORE the defaults overwrite them: `ARMS` is
# its own default's variable, so after the line below there is no telling
# a sweep the environment restricted from one it did not.
ARMS_ENV=${ARMS-}
SHAPES=${ONLY:-$(printf '%s\n' "$LIST" | cut -d/ -f1 | awk '!seen[$0]++')}
ARMS=${ARMS:-$(printf '%s\n' "$LIST" | cut -d/ -f2 | awk '!seen[$0]++')}
count() {  # count SHAPE ARM ITERS -> user instructions of one process
  local f; f=$(mktemp)
  perf stat -x, -e instructions:u -o "$f" \
    "$B" -m glob "$1/$2" -n "$3" > /dev/null 2>&1
  local c; c=$(grep 'instructions:u' "$f" | cut -d, -f1); rm -f "$f"
  case $c in ''|*[!0-9]*) echo "NaN" ;; *) echo "$c" ;; esac
}
# THE RESTRICTION GOES IN THE FILE, not just in the launch line. ONLY and
# ARMS are for a smoke run and never for a recorded column, and without
# this the two are the same artifact but for a line count -- a silent cap
# in the one form the README refuses, since what reads this file later
# cannot see the environment that wrote it. A full sweep says so outright
# rather than saying nothing, so the absence of a word is not what a
# reader has to notice. Case: `counts-file-says-it-was-restricted`.
SCOPE="full"
[ -z "${ONLY-}" ] || SCOPE="ONLY=$ONLY"
[ -z "${ARMS_ENV-}" ] || SCOPE="$SCOPE ARMS=$ARMS_ENV"
{
  echo "# $R-$H $(md5sum "$B" | cut -d' ' -f1) N=$N $(date -Is) $SCOPE"
  echo "# shape arm N instructions/iter"
  [ "$SCOPE" = full ] \
    || echo "# RESTRICTED: a smoke run of this script and NOT a recorded"\
            "column"
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
