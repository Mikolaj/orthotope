#!/bin/bash
# Goal-3 phase 1 (pinned-churn-plan.txt 3.2), 2026-08-18: the A/A spread of
# the driver, then the saturated-state cells (prepoison = the realistic
# operating point per plan section 3: the workload self-poisons, slowly --
# ~6 sub-threshold sprays per round -- so saturation is injected rather
# than waited for).  300 rounds per run; the steady tail is the last 20%.
# Phase 2 (no-prepoison long runs: does source-level de-poisoning pay?) is
# separate, launched after these verdicts.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation
M=dist-newstyle/build/x86_64-linux/ghc-9.12.4/mixedload-0.1/x/MixedLoad/build/MixedLoad/MixedLoad
D=goal3
exec > $D/phase1-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"

run() { # tag seed variant rtsflags...
  local T=$1 S=$2 V=$3; shift 3
  $M "$S" 300 "$V" prepoison +RTS "$@" -RTS > $D/p1-$T.log 2>&1
  echo "done $T ($(tail -1 $D/p1-$T.log))"
}

# A/A spread: 2 seeds x 2 reps, base, -A32m
run aa-s1r1 1 base -A32m
run aa-s2r1 2 base -A32m
run aa-s1r2 1 base -A32m
run aa-s2r2 2 base -A32m

# Saturated-state cells, seed 1
run base-4m       1 base -A4m
run base-4mAL     1 base -A4m -AL64m
run base-64m      1 base -A64m
run pad-32m       1 pad -A32m
run pad-64m       1 pad -A64m
run unpin-64m     1 unpin -A64m
run strong-4mAL   1 strong -A4m -AL64m
run strong-32m    1 strong -A32m
run strong-64m    1 strong -A64m
run strongpad-64m 1 strongpad -A64m

echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-GOAL3-P1
