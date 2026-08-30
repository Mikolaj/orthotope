#!/bin/bash
# WHICH SOURCE LINE the instructions of a fill go to, which is item 4's
# attribution: the counted work says stage two spends a few percent more
# than stage one on a view that will not canonicalize, and says nothing
# about where.
#
#     ./probe-attr.sh slice-primes lib-stage1 lib-stage2 sum-only-early
#
# perf samples instructions:u on the -g3 twin, which is the only binary
# here that can answer -- the timed one carries no line table and GHC's
# LLVM backend emits none even under -g3. **A -g3 build is a different
# program on the native backend and what differs is register allocation**
# (README.md#what-is-open), so what transfers is WHICH LINE runs and in
# what proportion, and the twin's right to speak for the timed binary is
# checked rather than assumed: the per-iteration event counts below are
# printed beside the counted-work sweep's, and the two agreeing is the
# control.
#
# Wants no quiet machine: a proportion over an instruction histogram is
# load-independent, as the count it is a histogram of.
#
# Artifacts probe-attr-<shape>-<arm>.{data,txt} and probe-attr-<shape>.txt.
set -u
cd "$(dirname "$0")" || exit 1
[ $# -ge 2 ] || { echo "usage: ./probe-attr.sh SHAPE ARM [ARM ...]"; exit 2; }
B=${BIN:-./probe-attr-g912}
case $B in /*|./*) ;; *) B=./$B ;; esac
[ -x "$B" ] || { echo "no $B -- probe-attr-build.sh makes it"; exit 1; }
SH=$1; shift
N=${N:-2000}
# 200000 and not less: at a shorter period the kernel throttles, and a
# throttled run does not fail -- it drops samples, biases what is left
# toward whatever runs when sampling resumes, and reports an event
# total short by the samples it lost. Measured 2026-08-30: at 20000
# this shape returned 9K samples where 46K were due and an event count
# a fifth of the truth, with `??:0` inflated from 7% to 21%. The
# refusal below is what makes that loud rather than plausible.
PERIOD=${PERIOD:-200000}
command -v perf > /dev/null 2>&1 || { echo "!! no perf on PATH"; exit 1; }
# The shape has to be one the binary holds, or the glob selects nothing,
# the process benchmarks nothing and every histogram below is of the
# runtime's own startup -- which reads exactly like a measured one. Held
# to `classes --list` for the same reason probe-stalls.sh holds its own.
# MAIN SET OR A CLASS, decided by which listing holds the shape: the
# conv shapes this was extended for are the MAIN set's, and passing
# `classes` for one of them selects nothing at all -- a process that
# benchmarks nothing and exits 0, which is the failure shape every driver
# here refuses. A name in neither listing, or in both, refuses too.
SEL=classes
LIST=$("$B" classes --list 2>/dev/null)
MLIST=$("$B" --list 2>/dev/null)
inc() { printf '%s\n' "$1" | cut -d/ -f1 | grep -qxF "$2"; }
if inc "$MLIST" "$SH" && inc "$LIST" "$SH"; then
  echo "!! $SH is in BOTH the main listing and the class listing, so which"
  echo "   population it names is not decidable here -- nothing ran"; exit 2
elif inc "$MLIST" "$SH"; then
  SEL=; LIST=$MLIST
elif inc "$LIST" "$SH"; then
  SEL=classes
else
  echo "!! $SH is in neither $B --list nor $B classes --list -- nothing ran"
  exit 2
fi
# TAG names a repetition, which is what the histogram's stability has to
# be read off: at N=200 the per-role split moved by more than the split
# itself between two runs whose TOTALS agreed to a tenth of a percent,
# which is Poisson on a few thousand samples and not a property of the
# code. RAISE N, never lower PERIOD -- a shorter period throttles the
# counter and costs the scale, where more iterations cost seconds.
OUT=probe-attr-$SH${TAG:+-$TAG}.txt
[ -e "$OUT" ] && { echo "$OUT exists; move it aside first"; exit 1; }
BAD=0
{
  echo "# $B $(md5sum "$B" | cut -d' ' -f1) $(date -Is) sel=${SEL:-main}"
  echo "# shape=$SH N=$N period=$PERIOD event=instructions:u"
  echo "# A -g3 TWIN, so the counts are its own; the control is that its"
  echo "# per-iteration total matches the timed binary's counted work."
} > "$OUT"
for A in "$@"; do
  printf '%s\n' "$LIST" | cut -d/ -f2 | grep -qxF "$A" \
    || { echo "!! $A is not an arm of the roster -- skipped" | tee -a "$OUT"; BAD=1; continue; }
  D=probe-attr-$SH${TAG:+-$TAG}-$A.data
  perf record -q -e instructions:u -c "$PERIOD" -o "$D" \
    "$B" $SEL -m glob "$SH/$A" -n "$N" > /dev/null 2>&1
  rc=$?
  R=$(perf report --stdio --sort srcline -i "$D" 2>/dev/null)
  TOT=$(printf '%s\n' "$R" | sed -n 's/^# Event count (approx.): *\([0-9]*\)/\1/p')
  NS=$(printf '%s\n' "$R" | sed -n 's/^# Samples: *\(.*\) of event.*/\1/p')
  LOST=$(printf '%s\n' "$R" | sed -n 's/^# Total Lost Samples: *\([0-9]*\)/\1/p')
  # THE SAMPLED TOTAL AGAINST A COUNTED ONE, because `Total Lost Samples`
  # does not see throttling: at too short a period the kernel disables the
  # counter for part of the run rather than dropping samples it admits to,
  # so the header reads 0 lost and the event total is short by however long
  # the PMU was off -- measured 2026-08-30, PERIOD=20000 on
  # slice-coprime-r7 returning 84.8M against a true 276M under a clean
  # `Total Lost Samples: 0`. One counting process a cell settles it, and it
  # validates the histogram's SCALE besides, which nothing else here does.
  TRUE=$(perf stat -x, -e instructions:u \
           "$B" $SEL -m glob "$SH/$A" -n "$N" 2>&1 >/dev/null \
         | sed -n 's/^\([0-9]*\),.*instructions:u.*/\1/p')
  if [ "${LOST:-0}" != 0 ]; then
    echo "!! $A: perf lost $LOST sample(s), so this histogram is biased toward"\
         "whatever ran when sampling resumed -- raise PERIOD" | tee -a "$OUT"
    BAD=1
  fi
  case ${TRUE:-} in
    ''|*[!0-9]*) echo "!! $A: perf stat gave no count, so the histogram's scale"\
                      "is unchecked" | tee -a "$OUT"; BAD=1 ;;
    *) if [ "$(( 100 * TOT / TRUE ))" -lt 95 ] || [ "$(( 100 * TOT / TRUE ))" -gt 105 ]
       then
         echo "!! $A: the sampled total is $TOT against a counted $TRUE,"\
              "$(( 100 * TOT / TRUE ))% -- the counter was off for part of"\
              "the run, so raise PERIOD; this histogram is not usable" \
           | tee -a "$OUT"
         BAD=1
       fi ;;
  esac
  { echo
    echo "=== $A  rc=$rc  samples=$NS  events=$TOT  counted=${TRUE:-?}  per iteration=$((TOT / N))"
    printf '%s\n' "$R" | grep -E '^ +[0-9]+\.[0-9]+%' \
      | awk -v t="$TOT" -v n="$N" '{gsub("%","",$1);
          printf "   %7.3f%%  %14.0f  %s\n", $1, $1/100*t/n, $2}'
  } >> "$OUT"
  [ "$rc" = 0 ] || BAD=1
done
cat "$OUT"
exit $BAD
