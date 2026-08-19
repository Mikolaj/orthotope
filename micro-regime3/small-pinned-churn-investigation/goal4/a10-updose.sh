#!/bin/bash
# The UPFRONT route's count-vs-bytes (the issue's dose sentence says
# "logarithmic in the object count", measured at a fixed 2304 B object
# -- the same proxy confound item 63 dissolved for the interleaved
# route). Sub-saturation upfront doses at -A32m via ReproSmall's new
# dose:N (N * 288 objects): a count-matched pair at two sizes and two
# bytes-matched pairs, two runs each, second halves against this
# binary's own alone.
#   count-matched: poison dose:70 (20k x 2304 B, 46 MB) vs poisontiny
#     dose:70 (20k x 800 B, 16 MB)
#   bytes-matched: poisontiny dose:200 (58k x 800 B, 46 MB) vs poison
#     dose:70; and poison dose:700 (202k, 464 MB) vs poisontiny
#     dose:2000 (576k, 461 MB)
# Registered lean, judged not remembered: BYTES, unifying with item 63
# -- tiny70 under poison70, tiny200 at poison70's level, tiny2000 at
# poison700's; count-matched equality instead keeps the issue's
# sentence as written and splits the two routes' dose metrics.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation
R=goal4/ReproSmall
exec > goal4/a10-updose-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
md5sum $R
run() { local name=$1; shift
  $R "$@" -RTS > goal4/a10-ud-$name.log 2>&1
  echo "== $name: $(grep -h 'victim:\|dose=' goal4/a10-ud-$name.log | tr '\n' ' ')"
  echo
}
for r in r1 r2; do
  run alone-$r          victim +RTS -A32m -I0 -T
  run poison70-$r       poison dose:70 victim +RTS -A32m -I0 -T
  run tiny70-$r         poisontiny dose:70 victim +RTS -A32m -I0 -T
  run tiny200-$r        poisontiny dose:200 victim +RTS -A32m -I0 -T
  run poison700-$r      poison dose:700 victim +RTS -A32m -I0 -T
  run tiny2000-$r       poisontiny dose:2000 victim +RTS -A32m -I0 -T
done
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-A10-UPDOSE
