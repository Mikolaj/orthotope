#!/bin/bash
# Run 16's second registered probe: the area curve.
#
# The gate's own five-bench selection over the shape set, on run16-a32m, at
# six allocation areas. -rtsopts is live so no build is owed, and the note
# measured that +RTS does override the baked area. It answers what
# registrations 2 and 3 cannot: whether 32m is a local optimum or merely the
# better of the two points the pair compared. Killed as a reading by a
# minimum that is not at or near 32m.
#
# EVERY +RTS LINE REPEATS THE BAKED OPTIONS IN FULL. A +RTS line inherits
# none of them, so a bare `+RTS -A64m` would run at -I0 and -M8G unset --
# a regime nobody chose, and figures that are not this run's.
#
# About an hour: six processes of 120 benches at criterion's default budget.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3
B=./run16-a32m
[ -x "$B" ] || { echo "no $B here"; exit 1; }
SEL=('-m' 'glob' '*/list' '*/build' '*/mut-odo'
     '*/sum-only-early' '*/sum-only-late')
ARMS=$(( ${#SEL[@]} - 2 ))
SHAPES=$($B --list 2>/dev/null | cut -d/ -f1 | sort -u | wc -l)
EXPECT=$(( ARMS * SHAPES ))
exec > probe-areacurve-driver.log 2>&1
echo "start $(date -Is); expecting $EXPECT benches a process"
md5sum $B
for A in 8m 16m 32m 64m 128m 256m; do
  out=probe-areacurve-$A
  echo "=== $(date -Is) start -A$A"
  $B "${SEL[@]}" --json $out.json +RTS -A$A -I0 -T -M8G -RTS > $out.log 2>&1
  rc=$?
  nb=$(grep -c '^benchmarking ' $out.log)
  echo "=== $(date -Is) done  -A$A rc=$rc benchmarking=$nb"
  [ "$nb" = "$EXPECT" ] || echo "    !! -A$A: expected $EXPECT, got $nb"
  [ "$rc" = 0 ] || echo "    !! -A$A: nonzero exit"
  grep -E '^=== roster' $out.log | sed 's/^/    /'
done
echo "AREA CURVE COMPLETE $(date -Is)"
