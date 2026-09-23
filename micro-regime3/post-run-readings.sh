#!/usr/bin/env bash
# Post-run step 4's readings, and 4a's, 4b's and 10a's, taken in parallel
# into one directory, a file a reading --
#
#     ./post-run-readings.sh run35            # writes log-read-run35/
#     ./post-run-readings.sh run35 --list     # prints what it would take
#
# Per population and half, against the other half where a reading takes
# two: --compare, --compare --predictions, --aa --brief and --cells, as
# POP-HALF-compare.txt, -pred.txt, -aa.txt and -cells.tsv, and on a class
# --block --brief and --block --compare --brief, as CLASS-HALF-block.txt
# and -blockcmp.txt, --block refusing the main set. On the main set,
# basis first: --chapter and --alloc --per-shape as main-chapter.txt
# and main-alloc.txt -- the per-shape half being the PER-ARM allocation
# ratio across the halves, which a pair whose variable moves allocation
# needs and which the agreement counts above it do not give; Run 36
# computed it in a script instead and published its reciprocal's
# complement on one arm -- and per half --deflation and --winsor as
# main-HALF-deflation.txt and main-HALF-winsor.txt. Where the note names a
# COMPARE run, per half --compare against that run's same half and
# --bridge, as main-HALF-vs-compare.txt and main-HALF-bridge.txt. Over the
# run: --floor-pairs as floor-pairs.txt, and --wild over every $R-*.log
# as wild-LOG.txt. LAST, once the rest have landed, read-all.sh
# --for-brief as for-brief.txt, which fills the brief's slots off them.
#
# ONCE $R-evening.txt ENDS `EVENING COMPLETE`, either form, and not before, the
# readings that want the counts: --compare --counts per population,
# basis first, as POP-counts-cmp.txt, step 4b's --cell-movers as
# cell-movers.txt, whose rank is the time ratio over the count ratio,
# and --half-movers against the note's COMPARE run as half-movers.txt;
# and each -pred.txt and class -blockcmp.txt reads the two sweeps beside
# its comparison, so a counts or countdiff span is read and the class
# paragraph quotes its counts. Before then a counts column reads `--`,
# and Run 34 took its 4a that way and took it again.
#
# Run 34's session wrote the step-4 readings by hand, a population and
# a half at a time. It only reads, so a busy machine is fine;
# READ_JOBS sets how many run at once, 6 unless given. Each
# reading's exit prints beside its file, and the files are for grep, as
# the chapter's step 4 says. Exit 0 when every reading ran, 1 when any
# did not -- exited 2 or worse, a --wild over a log whose file says it
# carries no samples excepted, or died in a traceback -- and 2 when
# nothing could be read: usage, no note, no JSON on the basis half.
set -u
cd "$(dirname "$0")" || exit 2
LIST=0
if [ $# -eq 2 ] && [ "$2" = --list ]; then LIST=1
elif [ $# -ne 1 ]; then
  echo "usage: ./post-run-readings.sh RUN [--list]    # e.g. run35" >&2
  exit 2
fi
R=$1
[ -f "$R-pair.txt" ] || { echo "no $R-pair.txt -- the halves and the COMPARE run are read off it" >&2; exit 2; }
HALVES_SET=$(./pair-halves.sh "$R") || exit 2
eval "$HALVES_SET"
D="log-read-$R"

POPS=""
for f in "$R-$BASIS"-*.json; do
  [ -f "$f" ] || continue
  p=${f#"$R-$BASIS-"}
  POPS="$POPS ${p%.json}"
done
[ -n "$POPS" ] || { echo "no $R-$BASIS-*.json here, so there is nothing to read" >&2; exit 2; }
COMPLETE=0
# The complained form, `EVENING COMPLETE WITH N COMPLAINT(S)`, is complete
# too: run-counts-all.sh writes it last either way. Case:
# `readings-take-the-counts-after-a-complained-evening`.
tail -1 "$R-evening.txt" 2>/dev/null | grep -qE 'EVENING COMPLETE(:| WITH)' && COMPLETE=1

# One line a reading, `OUT ARGV...`: the names here are the drivers'
# own and carry no space, which is what lets xargs split them.
JOBS=$(mktemp) || exit 2
job () { printf '%s\n' "$*" >> "$JOBS"; }
for p in $POPS; do
  for h in $BASIS $OTHER; do
    o=$OTHER; [ "$h" = "$BASIS" ] || o=$BASIS
    j="$R-$h-$p.json"
    job "$p-$h-aa.txt ./read-run.py $j --aa --brief"
    job "$p-$h-cells.tsv ./read-run.py $j --cells"
    [ "$p" = main ] || job "$p-$h-block.txt ./read-run.py $j --block --brief"
    if [ -f "$R-$o-$p.json" ]; then
      # A counts or countdiff span wants the sweeps, this half's first,
      # and they exist only once the evening is complete.
      s="-$p"; [ "$p" = main ] && s=""
      pc=""; [ "$COMPLETE" = 1 ] && pc=" --counts $R-counts-$h$s.txt $R-counts-$o$s.txt"
      job "$p-$h-compare.txt ./read-run.py $j --compare $R-$o-$p.json"
      job "$p-$h-pred.txt ./read-run.py $j --compare $R-$o-$p.json --predictions$pc"
      [ "$p" = main ] || job "$p-$h-blockcmp.txt ./read-run.py $j --block --compare $R-$o-$p.json --brief$pc"
    fi
  done
done
for h in $BASIS $OTHER; do
  job "main-$h-deflation.txt ./read-run.py $R-$h-main.json --deflation"
  job "main-$h-winsor.txt ./read-run.py $R-$h-main.json --winsor"
done
job "main-chapter.txt ./read-run.py $R-$BASIS-main.json --compare $R-$OTHER-main.json --chapter"
job "main-alloc.txt ./read-run.py $R-$BASIS-main.json --compare $R-$OTHER-main.json --alloc --per-shape"
job "floor-pairs.txt ./read-run.py --floor-pairs $R"
for f in "$R"-*.log; do
  [ -f "$f" ] && job "wild-${f%.log}.txt ./read-run.py $f --wild"
done
# The COMPARE run's halves off its own note, and by role: its basis is
# this basis's counterpart whatever either is called. Out of the
# environment first, since pair-halves.sh holds an inherited BASIS to the
# note it reads.
if [ -n "$COMPARE" ]; then
  CH=$(env -u BASIS -u OTHER -u COMPARE ./pair-halves.sh "$COMPARE" 2>/dev/null)
  CB=$(printf '%s\n' "$CH" | sed -n 's/^BASIS=\([A-Za-z0-9_]*\);.*/\1/p')
  CO=$(printf '%s\n' "$CH" | sed -n 's/.*OTHER=\([A-Za-z0-9_]*\);.*/\1/p')
  for pair in "$BASIS $CB" "$OTHER $CO"; do
    set -- $pair
    [ -n "${2:-}" ] && [ -f "$COMPARE-$2-main.json" ] || continue
    job "main-$1-vs-compare.txt ./read-run.py $R-$1-main.json --compare $COMPARE-$2-main.json"
    job "main-$1-bridge.txt ./read-run.py $R-$1-main.json --compare $COMPARE-$2-main.json --bridge"
  done
fi
if [ "$COMPLETE" = 1 ]; then
  for p in $POPS; do
    s="-$p"; [ "$p" = main ] && s=""
    job "$p-counts-cmp.txt ./read-run.py $R-$BASIS-$p.json --compare $R-$OTHER-$p.json --counts $R-counts-$BASIS$s.txt $R-counts-$OTHER$s.txt"
  done
  job "cell-movers.txt ./read-run.py --cell-movers $R"
  if [ -n "$COMPARE" ]; then
    job "half-movers.txt ./read-run.py --half-movers $R"
  fi
fi

if [ "$LIST" = 1 ]; then
  cat "$JOBS"
  echo "for-brief.txt ./read-all.sh $R --for-brief    # last, off the rest"
  rm -f "$JOBS"
  exit 0
fi
# REWRITTEN WHOLE: a file an earlier call left, a reading against a COMPARE
# run the note has since dropped among them, is read by --for-brief as
# this call's.
# BUT ONLY WHAT A CALL OF THIS SCRIPT WROTE: a file here that neither this
# call's jobs nor the previous call's `.written` names is somebody else's,
# and it is moved to $D-kept/ and named rather than deleted with the rest.
# Run 39's session kept readings of its own here and the second call took
# them. Case: `readings-keep-a-file-they-did-not-write`.
if [ -d "$D" ]; then
  KEPT=
  for f in "$D"/* "$D"/.[!.]*; do
    [ -e "$f" ] || continue
    b=${f##*/}
    case $b in for-brief.txt|.written) continue ;; esac
    cut -d' ' -f1 "$JOBS" | grep -qxF -- "$b" && continue
    [ -f "$D/.written" ] && grep -qxF -- "$b" "$D/.written" && continue
    mkdir -p "$D-kept" && mv "$f" "$D-kept/" && KEPT="$KEPT $b"
  done
  [ -z "$KEPT" ] || echo "kept aside in $D-kept/, being no reading this script writes:$KEPT"
fi
rm -rf "$D" && mkdir "$D" || exit 2
# A -cells.tsv is stdout alone, for a script to read: the reader's header
# and warnings go to stderr, and the same population's other files carry
# them.
# shellcheck disable=SC2016  # $1 and $@ are the inner shell's
xargs -P "${READ_JOBS:-6}" -L 1 sh -c \
  'out=$1; shift; case $out in
     *.tsv) "$@" > "'"$D"'/$out" 2> /dev/null ;;
     *) "$@" > "'"$D"'/$out" 2>&1 ;;
   esac; echo "rc=$? $out"' sh \
  < "$JOBS" | sort -k2 > "$JOBS.rc"
./read-all.sh "$R" --for-brief > "$D/for-brief.txt" 2>&1
echo "rc=$? for-brief.txt" >> "$JOBS.rc"
cat "$JOBS.rc"
N=$(grep -c . "$JOBS.rc")
# A --wild reading exits 2 on a log carrying no samples, which the run's
# wallclock log and its riders' driver logs never do: that is the verdict
# --for-brief quotes, and not a reading that did not happen -- where its
# file says so, a --wild exit 2 for any other reason counting as lost.
# And a reading that died in a traceback exits 1, a reading's own verdict
# code, so the files are read for one.
LOST=0; BARE=0
while read -r rc out; do
  case $rc in rc=0|rc=1) continue ;; esac
  if [ "$rc" = rc=2 ] && [ "${out#wild-}" != "$out" ] \
     && grep -q 'no paired `@@wild` samples\|^NO LOAD FIELDS' "$D/$out"; then
    BARE=$((BARE + 1))
  else
    LOST=$((LOST + 1))
  fi
done < "$JOBS.rc"
CRASHED=$(cd "$D" && grep -l 'Traceback (most recent call last)' -- * 2>/dev/null | sort | tr '\n' ' ')
{ cut -d' ' -f1 "$JOBS"; echo for-brief.txt; } > "$D/.written"
rm -f "$JOBS" "$JOBS.rc"
echo "$N reading(s) into $D/: $LOST did not happen, exiting 2 or worse, and $BARE --wild reading(s) exited 2 on a log carrying no samples"
[ -z "$CRASHED" ] || { echo "!! crashed: ${CRASHED% }"; LOST=$((LOST + 1)); }
if [ "$COMPLETE" = 0 ]; then
  echo "-- the counts comparisons and --half-movers: not before EVENING COMPLETE,"
  echo "   which $R-evening.txt does not end with yet; run this again then"
elif [ -z "$COMPARE" ]; then
  echo "-- --half-movers: skipped, $R-pair.txt having no COMPARE line to read against"
fi
[ "$LOST" = 0 ] || exit 1
exit 0
