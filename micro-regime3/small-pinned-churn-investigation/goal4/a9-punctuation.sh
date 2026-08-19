#!/bin/bash
# Stretch goal 4: the punctuation term probed (item 60's first OPEN).
# The read control (internoallocr) against alone across -A16m..64m on
# ReproSmall's victim, plus one perf pair at -A32m -- is the term tied
# to the L3-sized area, and is its channel the LLC again?
# Registered leans, judged not remembered: (1) the term peaks near the
# 32 MB L3 and falls off on both sides -- small at 16m and 64m; a flat
# or rising-at-64m term instead says it is not a cache-size resonance
# (and contradicts the driver's clean 64m read probe only if this
# victim's 64m cell is also elevated). (2) perf: elevated LLC misses at
# ~flat instructions and dTLB, item 18a's channel.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation
R=goal4/ReproSmall
exec > goal4/a9-punct-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
md5sum $R
for area in 16m 24m 32m 48m 64m; do
  for m in "" internoallocr; do
    tag=${m:-alone}
    $R $m victim +RTS -A$area -I0 -T -RTS > goal4/a9-punct-$tag-$area.log 2>&1
    echo "== $tag $area: $(grep victim: goal4/a9-punct-$tag-$area.log)"
  done
done
for m in "" internoallocr; do
  tag=${m:-alone}
  perf stat -e instructions,cycles,cache-misses,dTLB-load-misses \
    -o goal4/a9-punct-perf-$tag.txt \
    $R $m victim +RTS -A32m -I0 -T -RTS > /dev/null 2>&1
done
cat goal4/a9-punct-perf-alone.txt goal4/a9-punct-perf-internoallocr.txt
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-A9-PUNCT
