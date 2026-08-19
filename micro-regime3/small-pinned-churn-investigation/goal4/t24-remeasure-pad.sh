#!/bin/bash
# padding-plan.txt task 2.4(b): ../remeasure.sh's FIRST block (the
# victim-set remeasure; the arm-specificity block is task 2.2/2.3's
# territory on this session's binaries) rerun on the PADDED binary,
# artifacts under goal4/ with fresh names. Poison cnn-slice-c32/list --
# whose spray the padded binary allocates at 410 doubles, own-group.
# Registered lean, judged not remembered (plan 2.4b): the ~+14%
# in-roster deflation of the list denominator shrinks by the class delta
# task 2.1 measures and no further.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3
B=./newform-padded; P=cnn-slice-c32   # roster position 4, precedes 7..24
D=small-pinned-churn-investigation/goal4
exec > $D/t24-remeasure-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
md5sum $B
echo "=== victim set: does the tax fall on every shape's list? -A32m, padded ==="
for W in conv1d-24 gather48-src-50 stretch-inner256 stretch-bigstride stretch-wide-2xM \
         stretch-tab7MB stretch-tall-Mx2 vgg-14-c512-k3 stretch-primes stretch-square-1341; do
  $B -m glob "$W/list" --json $D/t24-rvp-$W-alone.json +RTS -A32m > $D/t24-rvp-$W-alone.log 2>&1
  $B -m glob "$P/list" "$W/list" --json $D/t24-rvp-$W-after.json +RTS -A32m > $D/t24-rvp-$W-after.log 2>&1
  a=$(awk "/^benchmarking $W\/list\$/{f=1} f&&/^time /{print \$2 \$3; exit}" $D/t24-rvp-$W-alone.log)
  b=$(awk "/^benchmarking $W\/list\$/{f=1} f&&/^time /{print \$2 \$3; exit}" $D/t24-rvp-$W-after.log)
  first=$(awk '/^benchmarking /{print $2; exit}' $D/t24-rvp-$W-after.log | cut -d/ -f1)
  ok=$([ "$first" = "$P" ] && echo ok || echo "INVALID(ran $first first)")
  printf '  %-24s alone=%-10s after=%-10s %s\n' "$W" "$a" "$b" "$ok"
done
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-T24-REMEASURE
