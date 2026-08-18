#!/bin/bash
# 2026-08-18, the closing batch: three probes, sequenced.
# (1) Upfront-dose x class completion of findings2 item 39: rep1:0 (pure
#     vgg/list through the driver, ref 18.70 flat) after an UPFRONT dose,
#     sub-threshold (prepoison, 2304 B) and own-group (prepoisonbig,
#     3600 B), at -A64m.  Registered leans: prepoison lifts rep1:0 toward
#     the ~24 ceiling; prepoisonbig leaves it at ~18.7 (ReproSmall's
#     class discrimination reproduced in-driver).  Both high would break
#     coherence and name an instrument difference to chase.
# (2) The cifar counterexample (findings2 item 21) re-examined at the
#     DEFAULT nursery with today's instrument discipline: fixed-n alone
#     legs, criterion alone, and a clean two-bench pair (poison
#     cnn-L1-6x6-c1/list, roster position 1, precedes cifar at 6), two
#     reps.  Registered lean: the two-bench pair shows at most a few
#     percent and the +10.2% does not reproduce -- it was roster-context
#     (the item 35/39 interleaving cost), retiring the counterexample.
# (3) Probe 6.4: the bq-expand +-2% at 64m (item 30e), three interleaved
#     alone/after criterion pairs.  Registered lean: inside the 1.5%
#     band, no real bq tax.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3
B=./run15-lookrts
SP=small-pinned-churn-investigation
M=$SP/dist-newstyle/build/x86_64-linux/ghc-9.12.4/mixedload-0.1/x/MixedLoad/build/MixedLoad/MixedLoad
D=$SP/goal3
exec > $D/probe64-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"

# (1) upfront-dose class cells
$M 1 1000 base rep1:0 prepoison +RTS -A64m -RTS > $D/p64-upfront-small.log 2>&1
echo "done upfront-small"
$M 1 1000 base rep1:0 prepoisonbig +RTS -A64m -RTS > $D/p64-upfront-big.log 2>&1
echo "done upfront-big"

# (2) cifar at the default nursery
V=cifar-L2-16-c64-k3; P=cnn-L1-6x6-c1
for n in 2000 4000; do
  /usr/bin/time -f %e -o $D/p64-cifar-alone-n$n.time \
    $B -m glob "$V/list" -n $n > $D/p64-cifar-alone-n$n.log 2>&1
  echo "cifar fixed-n n=$n wall=$(cat $D/p64-cifar-alone-n$n.time)"
done
$B -m glob "$V/list" --json $D/p64-cifar-calone.json > $D/p64-cifar-calone.log 2>&1
echo "cifar calone $(awk "/^benchmarking $V\/list\$/{f=1} f&&/^time /{print \$2, \$3; exit}" $D/p64-cifar-calone.log)"
for r in 1 2; do
  o=$D/p64-cifar-pair-r$r
  $B -m glob "$P/list" "$V/list" --json $o.json > $o.log 2>&1
  first=$(awk '/^benchmarking /{print $2; exit}' $o.log)
  ord=ok; [ "$first" = "$P/list" ] || ord="INVALID(ran $first first)"
  echo "cifar pair r$r victim=$(awk "/^benchmarking $V\/list\$/{f=1} f&&/^time /{print \$2, \$3; exit}" $o.log) $ord"
done

# (3) bq-expand tie-break at -A64m, interleaved alone/after x3
for r in 1 2 3; do
  $B -m glob 'vgg-14-c512-k3/bq-expand' --json $D/p64-bq-alone-r$r.json +RTS -A64m > $D/p64-bq-alone-r$r.log 2>&1
  a=$(awk "/^benchmarking vgg-14-c512-k3\/bq-expand\$/{f=1} f&&/^time /{print \$2, \$3; exit}" $D/p64-bq-alone-r$r.log)
  $B -m glob 'cnn-slice-c32/list' 'vgg-14-c512-k3/bq-expand' --json $D/p64-bq-after-r$r.json +RTS -A64m > $D/p64-bq-after-r$r.log 2>&1
  first=$(awk '/^benchmarking /{print $2; exit}' $D/p64-bq-after-r$r.log)
  ord=ok; [ "$first" = "cnn-slice-c32/list" ] || ord="INVALID(ran $first first)"
  b=$(awk "/^benchmarking vgg-14-c512-k3\/bq-expand\$/{f=1} f&&/^time /{print \$2, \$3; exit}" $D/p64-bq-after-r$r.log)
  echo "bq r$r alone=$a after=$b $ord"
done

echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-PROBE64
