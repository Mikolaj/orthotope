#!/usr/bin/env bash
# Post-run step 4's readings, and 4a's and 10a's, taken in parallel into
# one directory, a file a reading --
#
#     ./post-run-readings.sh run35            # writes log-read-run35/
#
# Per population and half, against the other half where a reading takes
# two: --compare, --compare --predictions, --aa --brief and --cells, as
# POP-HALF-compare.txt, -pred.txt, -aa.txt and -cells.tsv, and on a class
# --block --brief and --block --compare --brief, as CLASS-HALF-block.txt
# and -blockcmp.txt, --block refusing the main set. On the main set,
# basis first: --chapter and --alloc as main-chapter.txt and
# main-alloc.txt, and per half --deflation and --winsor as
# main-HALF-deflation.txt and main-HALF-winsor.txt. Over the run:
# --floor-pairs and read-all.sh --for-brief, as floor-pairs.txt and
# for-brief.txt.
#
# ONCE $R-evening.txt ENDS `EVENING COMPLETE:`, and not before, the
# readings that want the counts: --compare --counts per population,
# basis first, as POP-counts-cmp.txt, and --half-movers against the
# note's COMPARE run as half-movers.txt. Before then a counts column
# reads `--`, and Run 34 took its 4a that way and took it again.
#
# Run 34's session wrote the step-4 readings by hand, a population and
# a half at a time. It only reads, so a busy machine is fine;
# READ_JOBS sets how many run at once, 6 unless given. Each
# reading's exit prints beside its file, and the files are for grep, as
# the chapter's step 4 says. Exit 0 when every reading ran, 1 when any
# exited 2 or worse -- did not happen -- and 2 when nothing could be
# read: usage, no note, no JSON on the basis half.
set -u
cd "$(dirname "$0")" || exit 2
if [ $# -ne 1 ]; then
  echo "usage: ./post-run-readings.sh RUN     # e.g. run35" >&2
  exit 2
fi
R=$1
[ -f "$R-pair.txt" ] || { echo "no $R-pair.txt -- the halves and the COMPARE run are read off it" >&2; exit 2; }
HALVES_SET=$(./pair-halves.sh "$R") || exit 2
eval "$HALVES_SET"
D="log-read-$R"
mkdir -p "$D" || exit 2

POPS=""
for f in "$R-$BASIS"-*.json; do
  [ -f "$f" ] || continue
  p=${f#"$R-$BASIS-"}
  POPS="$POPS ${p%.json}"
done
[ -n "$POPS" ] || { echo "no $R-$BASIS-*.json here, so there is nothing to read" >&2; exit 2; }
COMPLETE=0
tail -1 "$R-evening.txt" 2>/dev/null | grep -q 'EVENING COMPLETE:' && COMPLETE=1

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
      job "$p-$h-compare.txt ./read-run.py $j --compare $R-$o-$p.json"
      job "$p-$h-pred.txt ./read-run.py $j --compare $R-$o-$p.json --predictions"
      [ "$p" = main ] || job "$p-$h-blockcmp.txt ./read-run.py $j --block --compare $R-$o-$p.json --brief"
    fi
  done
done
for h in $BASIS $OTHER; do
  job "main-$h-deflation.txt ./read-run.py $R-$h-main.json --deflation"
  job "main-$h-winsor.txt ./read-run.py $R-$h-main.json --winsor"
done
job "main-chapter.txt ./read-run.py $R-$BASIS-main.json --compare $R-$OTHER-main.json --chapter"
job "main-alloc.txt ./read-run.py $R-$BASIS-main.json --compare $R-$OTHER-main.json --alloc"
job "floor-pairs.txt ./read-run.py --floor-pairs $R"
job "for-brief.txt ./read-all.sh $R --for-brief"
if [ "$COMPLETE" = 1 ]; then
  for p in $POPS; do
    s="-$p"; [ "$p" = main ] && s=""
    job "$p-counts-cmp.txt ./read-run.py $R-$BASIS-$p.json --compare $R-$OTHER-$p.json --counts $R-counts-$BASIS$s.txt $R-counts-$OTHER$s.txt"
  done
  if [ -n "$COMPARE" ]; then
    job "half-movers.txt ./read-run.py --half-movers $R"
  fi
fi

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
cat "$JOBS.rc"
N=$(grep -c . "$JOBS.rc")
LOST=$(awk '{ sub(/^rc=/, "", $1) } $1 + 0 >= 2' "$JOBS.rc" | grep -c .)
rm -f "$JOBS" "$JOBS.rc"
echo "$N reading(s) into $D/, $LOST of them exiting 2 or worse"
if [ "$COMPLETE" = 0 ]; then
  echo "-- the counts comparisons and --half-movers: not before EVENING COMPLETE,"
  echo "   which $R-evening.txt does not end with yet; run this again then"
elif [ -z "$COMPARE" ]; then
  echo "-- --half-movers: skipped, $R-pair.txt having no COMPARE line to read against"
fi
[ "$LOST" = 0 ] || exit 1
exit 0
