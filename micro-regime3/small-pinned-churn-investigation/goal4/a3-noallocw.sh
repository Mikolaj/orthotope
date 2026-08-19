#!/bin/bash
# padding-plan.txt A3: touch-without-allocating (item 41's registered
# residual). MixedLoad's new noallocw mode WRITES a preallocated
# 288-double buffer at the sprayer's cadence, allocating nothing; the
# rep1:1000 base and noalloc cells are re-taken on the same rebuilt
# driver, so every comparison is within-binary (the rebuild moved
# layout; item 37/41's cells are the OLD binary's and are not compared
# against directly).
# Registered lean, judged not remembered (plan A3): still clean --
# allocation, not memory traffic, is the ingredient; noallocw at the
# base rep1:1000 level instead moves the account to write/dirty-page
# traffic and revives item 41(b)'s residual.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation
M=dist-newstyle/build/x86_64-linux/ghc-9.12.4/mixedload-0.1/x/MixedLoad/build/MixedLoad/MixedLoad
exec > goal4/a3-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
md5sum $M
$M 1 1000 base rep1:1000 +RTS -A64m -RTS > goal4/a3-base.log 2>&1
echo "done base"
$M 1 1000 base rep1:1000 noalloc +RTS -A64m -RTS > goal4/a3-noalloc.log 2>&1
echo "done noalloc"
$M 1 1000 base rep1:1000 noallocw +RTS -A64m -RTS > goal4/a3-noallocw.log 2>&1
echo "done noallocw"
for c in base noalloc noallocw; do
  echo "== $c: vgg/list tail, windows 20-120 / 800-1000"
  grep 'vgg-14-c512-k3/list' goal4/a3-$c.log
  python3 goal3/windows.py goal4/a3-$c.log 20 120 800 1000
done
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-A3
