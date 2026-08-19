#!/bin/bash
# Does an APPLICATION-SCALE victim pay the punctuation term at -A32m?
# All driver probe cells to date were -A64m (items 37/41/55, clean);
# ReproSmall's term is 32m-only (items 62/66/68). The driver's rep1
# system at -A32m: base (allocating sprays), noalloc (read probe),
# noallocw (write probe), 1000 rounds each, current MixedLoad build,
# within-binary.
# Registered lean, judged not remembered: the driver victim does NOT
# pay it -- its regime differs from ReproSmall's on both candidate
# ingredients (~6 collections per iteration against 0.75, so the
# punctuation cadence cannot phase-shift a once-per-iteration GC; live
# span 16 MB, under the area) -- so the probes read at the rep1:0
# offset level as they did at 64m. Probes elevated toward base instead
# would generalize the term to real victims and earn it a line in the
# maintainer brief.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation
M=dist-newstyle/build/x86_64-linux/ghc-9.12.4/mixedload-0.1/x/MixedLoad/build/MixedLoad/MixedLoad
exec > goal4/a12-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
md5sum $M
for m in "" noalloc noallocw; do
  tag=${m:-base}
  $M 1 1000 base rep1:1000 $m +RTS -A32m -RTS > goal4/a12-$tag-32m.log 2>&1
  echo "== $tag: vgg tail $(grep 'vgg-14-c512-k3/list' goal4/a12-$tag-32m.log | tail -1)"
  python3 goal3/windows.py goal4/a12-$tag-32m.log 20 120 800 1000
done
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-A12
