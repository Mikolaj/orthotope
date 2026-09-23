#!/bin/bash
# Probe 6.1 (plan section 6.1), 2026-08-18: the repetitive-phase driver --
# pad/unpin priced end-to-end in the training-loop phase shape. rep:1000 =
# 1000 sub-threshold sprays (cnn-slice-c32/mut-odo-vecdims) then one
# vgg-14-c512-k3/list and one stretch-inner256/list per round, identical
# every round; dose 10^6 by round 1000. The schedule is fixed, so the two
# base runs are a true A/A pair. Registered predictions: base's victims
# fall to Stage A's poisoned rates within ~100-200 rounds; pad's and
# unpin's hold the alone plateaus.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation
M=dist-newstyle/build/x86_64-linux/ghc-9.12.4/mixedload-0.1/x/MixedLoad/build/MixedLoad/MixedLoad
D=goal3
exec > $D/probe61-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"

run() { # tag variant A
  local T=$1 V=$2 A=$3
  $M 1 1000 "$V" rep:1000 +RTS -A$A -RTS > $D/p61-$T.log 2>&1
  echo "done $T ($(tail -1 $D/p61-$T.log))"
}
for A in 32m 64m; do
  run base-r1-$A base $A
  run base-r2-$A base $A
  run pad-$A pad $A
  run unpin-$A unpin $A
done

echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-PROBE61
