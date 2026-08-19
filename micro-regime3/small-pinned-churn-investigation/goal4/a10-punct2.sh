#!/bin/bash
# Item 62's three loose ends, on the current ReproSmall build (its own
# alone anchors re-taken within-binary):
# (1) the 64m cell CONVERGED (iters:1200, 600-iteration halves, where
#     300 iterations left both runs' halves still falling). Registered
#     lean: clean -- the +9.8% was the transient, and the punctuation
#     band stays 32m-only; elevated instead widens the band and splits
#     this victim from the driver's clean 64m probes.
# (2) the cadence cell: the read control at k:100 at -A32m. Registered
#     lean (weak): roughly the k:1000 level -- the term is
#     per-iteration punctuation, not per-call work; a ~10x smaller
#     reading instead makes it per-call.
# (3) the deconfounded perf design: {alone, read control} x {32m, 48m},
#     difference of differences -- the probe's own work is identical at
#     both areas and cancels, so the term's channel is readable where
#     item 62's single pair was confounded. Registered lean: the 32m
#     difference carries excess cache-misses well beyond the 48m
#     difference (the LLC channel); flat LLC excess instead says the
#     term is not a miss-count effect (item 25's honeymoon pattern).
set -u
cd /home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation
R=goal4/ReproSmall
exec > goal4/a10-punct2-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
md5sum $R
run() { local name=$1; shift
  $R "$@" -RTS > goal4/a10-p2-$name.log 2>&1
  echo "== $name: $(grep victim: goal4/a10-p2-$name.log)"
}
run alone-64m-long    iters:1200 victim +RTS -A64m -I0 -T
run readctl-64m-long  internoallocr iters:1200 victim +RTS -A64m -I0 -T
run alone-32m         victim +RTS -A32m -I0 -T
run readctl-32m       internoallocr victim +RTS -A32m -I0 -T
run readctl-k100-32m  internoallocr k:100 victim +RTS -A32m -I0 -T
for area in 32m 48m; do
  for m in "" internoallocr; do
    tag=${m:-alone}
    perf stat -e instructions,cycles,cache-misses,dTLB-load-misses \
      -o goal4/a10-p2-perf-$tag-$area.txt \
      $R $m victim +RTS -A$area -I0 -T -RTS > /dev/null 2>&1
  done
done
grep -H -E 'instructions|cycles|cache-misses|dTLB' goal4/a10-p2-perf-*.txt
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-A10-PUNCT2
