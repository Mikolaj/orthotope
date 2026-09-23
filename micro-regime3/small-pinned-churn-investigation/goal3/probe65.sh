#!/bin/bash
# 2026-08-18, the item-39 closure batch driver cells only;
# the sequentialMnistTest half is split into probe65-mnist.sh and WAITS
# for Mikolaj's go-ahead.
# Registered leans, judged not remembered:
#   (1) switch:500 (1500 rounds, sprays stop at 500): the state PERSISTS
#       -- post-switch windows hold ~23-24, coherent with item 40a's flat
#       post-dose horizon; recovery to ~18.7 would instead re-read item
#       39 as concurrent displacement.
#   (2) noalloc (sprayer replaced by a non-allocating read): the state
#       does NOT form -- allocation is the ingredient; if it forms
#       anyway, the account moves to cache/code effects and perf is next.
#       Residual ambiguity registered: the noalloc probe also touches
#       less fresh memory per call; a touch-without-allocating variant
#       would be the follow-up discriminator on a negative.
#   (3) rep1:1 and rep1:10: cumulative exposure 10^3-10^4 by the end --
#       lean, K=1 stays near 18.7 (below the 10^5 saturation region),
#       K=10 intermediate at most.
#   (4) sequentialMnistTest, baked -A1G vs +RTS -A64m, interleaved, on
#       the existing ghc-9.14.1 binary: does item 17's CAFlessTest
#       verdict (-A64m faster at far less RSS) hold on a second real
#       suite?  Gated: if the first run exceeds 360 s the A/B is not
#       worth four of them and the script stops after one.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation
M=dist-newstyle/build/x86_64-linux/ghc-9.12.4/mixedload-0.1/x/MixedLoad/build/MixedLoad/MixedLoad
D=goal3
exec > $D/probe65-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"

$M 1 1500 base rep1:1000 switch:500 +RTS -A64m -RTS > $D/p65-switch.log 2>&1
echo "done switch"
$M 1 1000 base rep1:1000 noalloc +RTS -A64m -RTS > $D/p65-noalloc.log 2>&1
echo "done noalloc"
$M 1 1000 base rep1:1 +RTS -A64m -RTS > $D/p65-k1.log 2>&1
echo "done k1"
$M 1 1000 base rep1:10 +RTS -A64m -RTS > $D/p65-k10.log 2>&1
echo "done k10"

echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-PROBE65-DRIVERCELLS
