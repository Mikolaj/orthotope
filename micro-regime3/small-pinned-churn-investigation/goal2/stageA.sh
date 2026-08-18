#!/bin/bash
# Goal-2 Stage A (pinned-churn-plan.txt 2.1), 2026-08-18.
# Instrument split -- a deviation from the plan's blanket fixed-n wording,
# forced by wall-time: a saturating poison dose (~10^5-10^6 sprays) plus a
# fixed-n ms-scale victim in one process would cost hours per cell, since
# criterion's -n applies to every selected bench.
#   ALONE plateaus: fixed-n two-point wall differencing (findings2 item 10).
#   POISONED (saturated) cells: predecessor-warmed criterion pair at default
#     budget -- the instrument findings2 items 9-11 validated (the poison leg
#     completes convergence before the victim window, and its ~5 s budget is
#     what delivers the saturating dose); tie-reps at -A32m link to item 5.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3
B=./run15-lookrts
D=small-pinned-churn-investigation/goal2
exec > $D/stageA-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"

# --- alone fixed-n plateaus, missing cells only (inner256 at 32m/64m/256m
# --- and every 1G cell already exist: findings2 items 10 and 15) ---
alone() { # shape A n  -> runs n and 2n
  local S=$1 A=$2 N=$3 n
  for n in $N $((2*N)); do
    /usr/bin/time -f %e -o $D/alone-$S-A$A-n$n.time \
      $B -m glob "$S/list" -n $n +RTS -A$A > $D/alone-$S-A$A-n$n.log 2>&1
    echo "alone $S -A$A n=$n wall=$(cat $D/alone-$S-A$A-n$n.time)"
  done
}
alone vgg-14-c512-k3 4m 400
alone vgg-14-c512-k3 32m 400
alone vgg-14-c512-k3 64m 400
alone vgg-14-c512-k3 256m 400
alone stretch-wide-2xM 4m 200
alone stretch-wide-2xM 32m 200
alone stretch-wide-2xM 64m 200
alone stretch-wide-2xM 256m 200
alone stretch-inner256 4m 200

# --- poisoned criterion pairs; 2 reps at the new -A values, 1 tie-rep at 32m ---
pois() { # shape A rep
  local S=$1 A=$2 R=$3 o=$D/pois-$1-A$2-r$3
  $B -m glob 'cnn-slice-c32/list' "$S/list" --json $o.json +RTS -A$A > $o.log 2>&1
  local first=$(awk '/^benchmarking /{print $2; exit}' $o.log)
  local t=$(awk "/^benchmarking $S\/list\$/{f=1} f&&/^time /{print \$2, \$3; exit}" $o.log)
  local ord=ok; [ "$first" = "cnn-slice-c32/list" ] || ord="INVALID(ran $first first)"
  echo "pois $S -A$A r$R victim=$t $ord"
}
for S in vgg-14-c512-k3 stretch-wide-2xM stretch-inner256; do
  pois $S 32m 1
  for A in 4m 64m 256m; do pois $S $A 1; pois $S $A 2; done
done

# --- bq-expand spot cells (predicted flat, item 6): alone + after, 64m/256m ---
for A in 64m 256m; do
  $B -m glob 'vgg-14-c512-k3/bq-expand' --json $D/bqalone-A$A.json +RTS -A$A > $D/bqalone-A$A.log 2>&1
  $B -m glob 'cnn-slice-c32/list' 'vgg-14-c512-k3/bq-expand' --json $D/bqafter-A$A.json +RTS -A$A > $D/bqafter-A$A.log 2>&1
  first=$(awk '/^benchmarking /{print $2; exit}' $D/bqafter-A$A.log)
  ord=ok; [ "$first" = "cnn-slice-c32/list" ] || ord="INVALID(ran $first first)"
  a=$(awk "/^benchmarking vgg-14-c512-k3\/bq-expand\$/{f=1} f&&/^time /{print \$2, \$3; exit}" $D/bqalone-A$A.log)
  b=$(awk "/^benchmarking vgg-14-c512-k3\/bq-expand\$/{f=1} f&&/^time /{print \$2, \$3; exit}" $D/bqafter-A$A.log)
  echo "bq -A$A alone=$a after=$b $ord"
done
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-STAGEA
