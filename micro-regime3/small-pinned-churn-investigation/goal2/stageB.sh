#!/bin/bash
# Goal-2 Stage B phase 1 (pinned-churn-plan.txt 2.2), 2026-08-18: RTS variants
# on the two best -A values from Stage A (32m = half tax at modest alone cost,
# 64m = start of the alone-optimal band), POISONED-state cells first -- a
# variant that does not move the poisoned state is dead on arrival.
# Victim vgg-14-c512-k3/list (fixed-n alone plateaus taken in Stage A).
# Registered leans (plan 2.2), to be judged not remembered: -c null control;
# -G1 could form the scatter faster; -xn the one variant with a real shot;
# -Fd0/--disable-delayed-os-memory-return are kernel-term medicine only.
# Phase 2 (alone legs + reps for movers) is launched by hand after reading this.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3
B=./run15-lookrts
D=small-pinned-churn-investigation/goal2
exec > $D/stageB-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"

vcell() { # A variantflags tag
  local A=$1 V=$2 T=$3 o
  o=$D/vpois-vgg-A$A-$T
  $B -m glob 'cnn-slice-c32/list' 'vgg-14-c512-k3/list' --json $o.json +RTS -A$A $V > $o.log 2>&1
  local first=$(awk '/^benchmarking /{print $2; exit}' $o.log)
  local t=$(awk "/^benchmarking vgg-14-c512-k3\/list\$/{f=1} f&&/^time /{print \$2, \$3; exit}" $o.log)
  local ord=ok; [ "$first" = "cnn-slice-c32/list" ] || ord="INVALID(ran $first first)"
  echo "vpois vgg -A$A [$V] victim=$t $ord"
}
for A in 32m 64m; do
  vcell $A "" base
  vcell $A "-G1" G1
  vcell $A "-xn" xn
  vcell $A "-Fd0" Fd0
  vcell $A "--disable-delayed-os-memory-return" nodelay
  vcell $A "-c" c
done

# -AL, one point, bq-expand only (plan 2.2): does raising the large-object
# allowance at a small area relieve bq-expand's small-nursery cost?
for V in "" "-AL64m"; do
  T=$([ -z "$V" ] && echo plain || echo AL64m)
  $B -m glob 'vgg-14-c512-k3/bq-expand' --json $D/bqAL-A4m-$T.json +RTS -A4m $V > $D/bqAL-A4m-$T.log 2>&1
  echo "bqAL -A4m [$V] $(awk "/^benchmarking vgg-14-c512-k3\/bq-expand\$/{f=1} f&&/^time /{print \$2, \$3; exit}" $D/bqAL-A4m-$T.log)"
done

echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-STAGEB1
