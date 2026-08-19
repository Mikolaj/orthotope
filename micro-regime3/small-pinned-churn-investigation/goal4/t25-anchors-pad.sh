#!/bin/bash
# padding-plan.txt task 2.5: THE DEFAULT-NURSERY ANCHORS on the PADDED
# binary. The three anchor shapes' list after one poison
# (cnn-L1-6x6-c1/list, roster position 1, so it precedes all three),
# two-bench pairs order-asserted, plus clean alone legs, at the default
# area (the baked -I0 -T -M8G line, no -A override) -- the design item
# 40b used to re-read cifar's +10.2% anchor headline as +5.4-5.7%
# clean-pair. Compare against THAT, not the headline; absolutes are this
# binary's own, so the alone legs here are the denominators.
# Registered lean, judged not remembered (plan 2.5 + 2.4's shape): if
# task 2.1's class split extends to the default area, each pair tax
# shrinks toward the own-group level (the poison's spray is padded here,
# own-group by construction); a null -- taxes at the unpadded binary's
# level -- reads the small-area residue (item 30's 3-6%) as
# class-independent, itself a finding for the decision table.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3
B=./newform-padded; P=cnn-L1-6x6-c1
D=small-pinned-churn-investigation/goal4
exec > $D/t25-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
md5sum $B
for V in cnn-slice-c32 cifar-L2-16-c64-k3 stretch-wide-2xM; do
  for r in r1 r2; do
    $B -m glob "$V/list" --json $D/t25-$V-alone-$r.json > $D/t25-$V-alone-$r.log 2>&1
    $B -m glob "$P/list" "$V/list" --json $D/t25-$V-after-$r.json > $D/t25-$V-after-$r.log 2>&1
    a=$(awk "/^benchmarking $V\/list\$/{f=1} f&&/^time /{print \$2 \$3; exit}" $D/t25-$V-alone-$r.log)
    b=$(awk "/^benchmarking $V\/list\$/{f=1} f&&/^time /{print \$2 \$3; exit}" $D/t25-$V-after-$r.log)
    first=$(awk '/^benchmarking /{print $2; exit}' $D/t25-$V-after-$r.log | cut -d/ -f1)
    ok=$([ "$first" = "$P" ] && echo ok || echo "INVALID(ran $first first)")
    printf '  %-22s %s alone=%-10s after=%-10s %s\n' "$V" "$r" "$a" "$b" "$ok"
  done
done
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-T25
