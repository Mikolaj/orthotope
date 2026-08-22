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
# Spent: it ran on 2026-08-20 and README's Run 16 chapter carries the curve.
# It refuses to start over its own artifacts, as the run drivers do and for
# the same reason -- they are overwritten in place with nothing said, which
# is what happened to its -A8m pair on 2026-08-23, when a case ran the
# version before this one: that one cd'd to an absolute path and so ran
# HERE rather than in the case's shadow. HALF names the binary and OUT the
# artifacts' prefix, so a case can point both at stand-ins; the defaults
# are the probe's own. Its complaints ride out in the exit status as every
# other driver's do -- they used to be echoed into the log at exit 0, so
# six processes could come out short or dead under `AREA CURVE COMPLETE`.
# Found 2026-08-22 by review. Cases: `areacurve-exit-carries-its-complaints`
# and `areacurve-runs-clean-on-a-full-count`.
#
# About an hour: six processes of 120 benches at criterion's default budget.
set -u
cd "$(dirname "$0")" || exit 1
HALF=${HALF:-run16-a32m}
case $HALF in /*|./*) B=$HALF ;; *) B=./$HALF ;; esac
OUT=${OUT:-probe-areacurve}
[ -x "$B" ] || { echo "no $B here"; exit 1; }
EXISTING=$(ls -1 "$OUT"-*.json "$OUT"-*.log 2>/dev/null)
if [ -n "$EXISTING" ]; then
  echo "$OUT already has artifacts here:"
  printf '%s\n' "$EXISTING" | sed 's/^/  /'
  echo "relaunching would overwrite them in place. Move them aside first."
  exit 1
fi
SEL=('-m' 'glob' '*/list' '*/build' '*/mut-odo'
     '*/sum-only-early' '*/sum-only-late')
ARMS=$(( ${#SEL[@]} - 2 ))
SHAPES=$("$B" --list 2>/dev/null | cut -d/ -f1 | sort -u | wc -l)
EXPECT=$(( ARMS * SHAPES ))
exec > "$OUT-driver.log" 2>&1
echo "start $(date -Is); expecting $EXPECT benches a process"
md5sum "$B"
BAD=0
for A in 8m 16m 32m 64m 128m 256m; do
  out=$OUT-$A
  echo "=== $(date -Is) start -A$A"
  "$B" "${SEL[@]}" --json "$out.json" +RTS -A$A -I0 -T -M8G -RTS \
    > "$out.log" 2>&1
  rc=$?
  nb=$(grep -c '^benchmarking ' "$out.log")
  echo "=== $(date -Is) done  -A$A rc=$rc benchmarking=$nb"
  [ "$nb" = "$EXPECT" ] \
    || { echo "    !! -A$A: expected $EXPECT, got $nb"; BAD=$((BAD + 1)); }
  [ "$rc" = 0 ] || { echo "    !! -A$A: nonzero exit"; BAD=$((BAD + 1)); }
  grep -E '^=== roster' "$out.log" | sed 's/^/    /'
done
if [ "$BAD" -eq 0 ]; then echo "AREA CURVE COMPLETE $(date -Is)"
else echo "AREA CURVE DONE $(date -Is) WITH $BAD COMPLAINT(S) ABOVE"; fi
[ "$BAD" -eq 0 ] || exit 1
