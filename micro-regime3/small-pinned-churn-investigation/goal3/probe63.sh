#!/bin/bash
# Probe 6.3 (plan section 6.3, as sharpened by findings2 item 37),
# 2026-08-18: what cumulative state does class-independent tiny-call
# interleaving build?  The rep1 system is the cleanest carrier: rep1:0
# reads 18.70 flat, rep1:1000 ~23.7 and drifting, class-independent.
# Cells and REGISTERED LEANS (judged, not remembered):
#   (1) rep1:1000 +H2G      -- lean: does NOT cure (the drift and class-
#       independence resemble the H2G-immune family; a cure would instead
#       implicate 27601-style block placement).
#   (2) rep1:100            -- dose response in K: lean, between the two
#       levels and nearer 23.7 if saturating, proportional if linear.
#   (3) rep1:1000 x 3000 rounds -- drift horizon: lean, saturates.
#   (4) perf stat on rep1:0 and rep1:1000 -- lean: the added cost is LLC
#       misses at flat per-call instructions (the churn-tax channel); the
#       sprayer's own counters are a ~2% contamination, small enough to
#       read through.
#   (5) shuffle nosmall     -- lean: stays at the mix's elevated level
#       (item 35's small-class acquittal, now direct).
#   (6) shuffle +H2G        -- same question as (1) for the full mix.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation
M=dist-newstyle/build/x86_64-linux/ghc-9.12.4/mixedload-0.1/x/MixedLoad/build/MixedLoad/MixedLoad
D=goal3
exec > $D/probe63-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"

$M 1 1000 base rep1:1000 +RTS -A64m -H2G -RTS > $D/p63-h2g-rep1.log 2>&1
echo "done h2g-rep1"
$M 1 1000 base rep1:100 +RTS -A64m -RTS > $D/p63-dose100.log 2>&1
echo "done dose100"
$M 1 3000 base rep1:1000 +RTS -A64m -RTS > $D/p63-horizon.log 2>&1
echo "done horizon"
perf stat -e instructions,cycles,cache-misses,dTLB-load-misses \
  -o $D/p63-perf-ctrl.txt -- \
  $M 1 1000 base rep1:0 +RTS -A64m -RTS > $D/p63-perf-ctrl.log 2>&1
echo "done perf-ctrl"
perf stat -e instructions,cycles,cache-misses,dTLB-load-misses \
  -o $D/p63-perf-spray.txt -- \
  $M 1 1000 base rep1:1000 +RTS -A64m -RTS > $D/p63-perf-spray.log 2>&1
echo "done perf-spray"
$M 1 300 base nosmall +RTS -A64m -RTS > $D/p63-nosmall.log 2>&1
echo "done nosmall"
$M 1 300 base +RTS -A64m -H2G -RTS > $D/p63-h2g-shuffle.log 2>&1
echo "done h2g-shuffle"

echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-PROBE63
