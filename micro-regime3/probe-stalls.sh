#!/bin/bash
# Per-iteration perf counts, any events, for chosen arms and shapes of one
# binary: run-counts.sh's differenced method with BIN, OUT, CLASS, ONLY,
# ARMS, EVENTS and N as its knobs.
#
# Written for the counter reading [the ceiling]'s seventh reading named and
# did not take: "whether those account for the measured 1.16 to 1.67 of time over
# instructions wants a counter reading of stalls and mispredicts, not
# another dump."  That second term is what task 1 has left once the
# unboxing fix retires the first, so this is the instrument for its
# mechanism.
#
#     ARMS="lib-stage1 lib-stage2" OUT=probe-stalls-g912 ./probe-stalls.sh
#     ARMS="lib-stage1 lib-stage2" CLASS=bcast OUT=probe-stalls-g912 ./probe-stalls.sh
#
# run-counts.sh's method exactly -- two fixed-iteration processes a cell,
# `-n 2N` and `-n N`, the difference over N -- so the fixed cost of a
# process, of criterion's setup and of the saturating preamble all cancel
# and nothing here owes criterion's estimator anything.  What differs is
# only the event list, so a figure from this file and one from a counts
# file are the same kind of quantity read off different counters, and
# instructions:u is kept in the list precisely so the two can be checked
# against each other.
#
# A THIRD PROCESS, `-n 3N`, checks that the difference is one process's
# slope, since a cell can differ from process to process in more than its
# fixed cost: Run 40's `runs-3` consumers drew one of three op-cache modes
# per process, and a difference across two modes printed figures outside
# every mode (2026-09-25).  A cell whose `(3N - 2N)` and `(2N - N)`
# slopes part by more than LINEAR_TOL, default 0.02, on cycles:u or
# instructions:u is followed by a `# NONLINEAR` line giving both, and one
# whose third process perf could not count by a `# UNCHECKED` line.  The
# published figure stays `(2N - N) / N`.  A minor GC inside one window
# does the same to a cell of a few thousand instructions, moving it by
# tens at N=100000, so a small cell wants an N that puts every window's
# GCs in step or a reading that tolerates tens.
#
# UNLIKE run-counts.sh THIS WANTS A QUIET MACHINE.  Instructions are
# layout- and load-independent, which is what lets that sweep run on a
# working desktop; cycles and stalls are neither -- a cycle spent waiting
# for a core somebody else is using counts here exactly as a cycle spent
# waiting for memory.  So this is an evening's measurement even though it
# is a counter reading.
#
# ARMS is required rather than defaulted to the roster: at five events a
# cell the sweep is dear, and the question is about two arms and their
# floor, not about fifty.  CLASS selects a stride-class population and
# names the artifact; without it the main set is swept.
#
# Output: $OUT[-CLASS].txt, one line a cell -- shape, arm, N, then one
# field per event in the order EVENTS names them, and the header names
# them so nothing downstream has to infer the order.  A cell whose `-n N`
# or `-n 2N` process perf could not count is a `!!` line and the exit
# status, as in run-counts.sh.
#
# Non-vacuity, 2026-08-30: probe-stalls-selftest.log.
set -u
cd "$(dirname "$0")" || exit 1
B=${BIN:-./probe-bang-g912}
case $B in /*|./*) ;; *) B=./$B ;; esac
OUT=${OUT:?set OUT to a probe-* name; a run prefix would be read as that runs own process}
case $OUT in probe-*|smoke-*) ;;
  *) echo "OUT is '$OUT': a probe's artifacts are probe-* or smoke-*, never a run's"; exit 2 ;;
esac
C=${CLASS-}
N=${N:-50}
TOL=${LINEAR_TOL:-0.02}
# Five events and not six: this box gives every one of these at 100% of
# the run with no multiplexing, and a sixth (L1-dcache-load-misses) comes
# back `<not counted>` at 0.00% because the general counters are spent.
# stalled-cycles-backend is `<not supported>` here at any width, which is
# the CPU and not the setting. Probed 2026-08-30, and the probe below
# re-asks it rather than trusting this comment.
EVENTS=${EVENTS:-instructions:u,cycles:u,stalled-cycles-frontend:u,branch-misses:u,cache-misses:u}
[ -x "$B" ] || { echo "no $B here"; exit 2; }
[ -n "${ARMS:-}" ] || { echo "set ARMS: this sweep is five events a cell and is not for a whole roster"; exit 2; }
F=$OUT${C:+-$C}.txt
[ -e "$F" ] && { echo "$F exists; move it aside first"; exit 2; }

# perf first, as run-counts.sh does it and for its reason: a machine that
# refuses the counters gives NaN for every cell and takes the whole sweep
# to say so.  Each event is probed separately, an event this CPU does not
# implement being the likelier refusal here than a paranoid level.
command -v perf > /dev/null 2>&1 || { echo "!! no perf on PATH. Nothing ran."; exit 2; }
# The whole list at once, not one event at a time: an event this CPU cannot
# count reads `<not supported>` alone or in company, but MULTIPLEXING only
# appears when the list is over-long, and a scaled count is the failure that
# would otherwise be silent -- field 5 is the percentage of the run the event
# was on a counter, and anything under 100 means the figure is an
# extrapolation. Both are refused here rather than left to a `!!` per cell.
# A permission refusal prints prose with no commas, which the field test
# below cannot see -- run-counts.sh's probe shape, first. 2026-09-01.
if ! perf stat -x, -e "$EVENTS" /bin/true 2>&1 | grep -q '^[0-9]\+,'; then
  echo "!! perf will not count anything here -- no event returned a number."
  echo "   kernel.perf_event_paranoid reads\
 $(cat /proc/sys/kernel/perf_event_paranoid 2>/dev/null || echo '?'), and anything above 1 is the"
  echo "   usual cause. That is what it READ and not a diagnosis."
  echo "   Nothing ran, no $F written."
  exit 2
fi
BADEV=$(perf stat -x, -e "$EVENTS" /bin/true 2>&1 \
        | awk -F, 'NF>4 && ($1 !~ /^[0-9]+$/ || $5 != "100.00") {print $3" ("$1" at "$5"%)"}')
if [ -n "$BADEV" ]; then
  echo "!! perf will not count these here, or not for the whole run:"
  printf '%s\n' "$BADEV" | sed 's/^/   /'
  echo "   kernel.perf_event_paranoid reads\
 $(cat /proc/sys/kernel/perf_event_paranoid 2>/dev/null || echo '?'), and an"
  echo "   event this CPU does not implement reads <not supported> instead."
  echo "   That is what it READ and not a diagnosis. Nothing ran, no $F written."
  exit 2
fi
_p=$(mktemp 2>/dev/null) && printf x > "$_p" 2>/dev/null || {
  echo "!! mktemp gives no writable file here (TMPDIR=${TMPDIR:-unset}), so perf"
  echo "   would write its counts nowhere. Nothing ran, no $F written."; rm -f "$_p"; exit 2; }
rm -f "$_p"

EVLIST=${EVENTS//,/ }
NEV=0; for e in $EVLIST; do NEV=$((NEV + 1)); done
read -r -a evarr <<< "$EVLIST"
SEL=${C:+classes}
LIST=$("$B" $SEL --list 2>/dev/null)
[ -n "$LIST" ] || { echo "!! --list gave nothing; wrong binary?"; exit 2; }
if [ -n "$C" ]; then
  LIST=$(printf '%s\n' "$LIST" | grep "^$C-") || LIST=
  [ -n "$LIST" ] || { echo "!! class prefix $C- matches no bench -- nothing ran, no $F written"; exit 2; }
fi
SHAPES=${ONLY:-$(printf '%s\n' "$LIST" | cut -d/ -f1 | awk '!seen[$0]++')}
# EVERY NAME IS HELD TO THE ROSTER, which run-counts.sh does not do for its
# own ONLY and ARMS: a shape or arm the binary does not have selects no
# bench, so the process starts, benchmarks nothing and exits 0, and the two
# fixed-iteration runs then difference to a row of process noise -- measured
# 2026-08-30 as `nosuchshape list 50 0 1409 255 2 17`, which is a cell that
# looks measured and is not. A name that is simply wrong cannot be told from
# one that is right by anything downstream, so it is refused here.
MISS=
for S in $SHAPES; do
  printf '%s\n' "$LIST" | cut -d/ -f1 | grep -qxF "$S" || MISS="$MISS $S"
done
for A in $ARMS; do
  printf '%s\n' "$LIST" | cut -d/ -f2 | grep -qxF "$A" || MISS="$MISS $A"
done
[ -z "$MISS" ] || { echo "!! not in $B${C:+ classes} --list:$MISS"
                    echo "   each would select no bench and difference to process noise,"
                    echo "   which reads exactly like a measured cell. Nothing ran, no $F written."
                    exit 2; }

count() {  # count SHAPE ARM ITERS -> one field per event, comma-separated
  local f; f=$(mktemp)
  perf stat -x, -e "$EVENTS" -o "$f" "$B" $SEL -m glob "$1/$2" -n "$3" > /dev/null 2>&1
  local out='' e c
  for e in ${EVENTS//,/ }; do
    c=$(grep ",$e," "$f" | cut -d, -f1)
    case $c in ''|*[!0-9]*) c=NaN ;; esac
    out="$out${out:+,}$c"
  done
  rm -f "$f"; printf '%s' "$out"
}

SCOPE="ARMS=$ARMS"
[ -z "$C" ] || SCOPE="$SCOPE class=$C"
[ -z "${ONLY-}" ] || SCOPE="$SCOPE ONLY=$ONLY"
{
  echo "# $B $(md5sum "$B" | cut -d' ' -f1) N=$N $(date -Is) $SCOPE"
  echo "# shape arm N $(echo "$EVENTS" | tr ',' ' ')"
  echo "# every cell is (-n 2N) minus (-n N), over N, as run-counts.sh takes it"
  echo "# and checked against (-n 3N) minus (-n 2N): LINEAR_TOL=$TOL"
  echo "# ARMS-RESTRICTED BY CONSTRUCTION: this sweep is never a roster column"
} > "$F"
BAD=0
NL=0
UC=0
for S in $SHAPES; do
  for A in $ARMS; do
    c3=$(count "$S" "$A" $((3 * N)))
    c2=$(count "$S" "$A" $((2 * N))); c1=$(count "$S" "$A" "$N")
    case "$c2$c1" in
      *NaN*) echo "!! $S $A: perf could not count" >> "$F"; BAD=1; continue ;;
    esac
    # The third process checks the figure and is no part of it, so its
    # failure leaves the cell standing, marked as unchecked (2026-09-25).
    IFS=, read -r -a c3arr <<< "$c3"
    IFS=, read -r -a c2arr <<< "$c2"
    IFS=, read -r -a c1arr <<< "$c1"
    line="$S $A $N"
    off=
    for i in $(seq 1 $NEV); do
      a=${c2arr[$((i - 1))]}; b=${c1arr[$((i - 1))]}
      line="$line $(( (a - b) / N ))"
      case "$c3" in *NaN*) continue ;; esac
      case ${evarr[$((i - 1))]} in cycles:u|instructions:u) ;; *) continue ;; esac
      # On the raw differences, N cancelling in the ratio: slopes truncated
      # to integers first parted by the truncation alone on a small cell,
      # 49 against 50 being two percent (2026-09-25).
      if awk -v p=$((a - b)) -v q=$((c3arr[i - 1] - a)) -v t="$TOL" \
           'BEGIN { exit !(p != 0 && (q / p - 1 > t || 1 - q / p > t)) }'; then
        off="$off ${evarr[$((i - 1))]} $(( (a - b) / N )) then\
 $(( (c3arr[i - 1] - a) / N ))"
      fi
    done
    echo "$line" >> "$F"
    case "$c3" in
      *NaN*) echo "# UNCHECKED $S $A: the -n $((3 * N)) process could not\
 count" >> "$F"
             UC=$((UC + 1)) ;;
    esac
    [ -z "$off" ] || { echo "# NONLINEAR $S $A:$off" >> "$F"; NL=$((NL + 1)); }
  done
done
echo "# end $(date -Is), $NL nonlinear cell(s), $UC unchecked" >> "$F"
[ "$NL" = 0 ] || echo "$NL cell(s) nonlinear past $TOL: their figures are no one process's, see the # NONLINEAR lines in $F"
[ "$UC" = 0 ] || echo "$UC cell(s) not checked against a third process, perf counting no -n $((3 * N)) run: the # UNCHECKED lines in $F"
exit $BAD
