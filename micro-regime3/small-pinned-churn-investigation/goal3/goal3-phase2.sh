#!/bin/bash
# Goal-3 phase 2, 2026-08-18: does source-level de-poisoning PAY at the
# workload's own poison rate (~6 sub-threshold sprays per round, no
# prepoison)?  Long base vs pad runs at -A64m (the area with the largest
# saturated tax): base should drift as its dose accumulates
# (1500 rounds ~ 9k sprays) while pad sprays nothing and stays flat; the
# early-window comparison also prices pad's own clean-state cost.
# The dose curve at 64m is unmeasured, so a flat base run is a finding,
# not a failure: it means this mix self-poisons too slowly to matter at
# ~10-minute horizons and the workaround's value is for higher-rate
# programs (the saturated cells of phase 1 are those programs' picture).
set -u
cd /home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation
M=dist-newstyle/build/x86_64-linux/ghc-9.12.4/mixedload-0.1/x/MixedLoad/build/MixedLoad/MixedLoad
D=goal3
exec > $D/phase2-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"

$M 1 1500 base +RTS -A64m -RTS > $D/p2-base-64m.log 2>&1
echo "done base ($(tail -1 $D/p2-base-64m.log))"
$M 1 1500 pad +RTS -A64m -RTS > $D/p2-pad-64m.log 2>&1
echo "done pad ($(tail -1 $D/p2-pad-64m.log))"

# Clean-state (no-prepoison, short) mixed baselines per -A, so the
# saturated cells of phase 1 can be priced against a clean twin.  The
# self-poison dose over 300 rounds (~1.8k sprays) sits at the bottom of
# the log curve, so these are approximately clean.
$M 1 300 base +RTS -A4m -RTS > $D/p2-clean-4m.log 2>&1
echo "done clean-4m ($(tail -1 $D/p2-clean-4m.log))"
$M 1 300 base +RTS -A4m -AL64m -RTS > $D/p2-clean-4mAL.log 2>&1
echo "done clean-4mAL ($(tail -1 $D/p2-clean-4mAL.log))"
$M 1 300 base +RTS -A32m -RTS > $D/p2-clean-32m.log 2>&1
echo "done clean-32m ($(tail -1 $D/p2-clean-32m.log))"
$M 1 300 strong +RTS -A32m -RTS > $D/p2-clean-strong-32m.log 2>&1
echo "done clean-strong-32m ($(tail -1 $D/p2-clean-strong-32m.log))"

echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-GOAL3-P2
