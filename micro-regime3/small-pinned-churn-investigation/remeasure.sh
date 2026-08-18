#!/bin/bash
# Re-measure the two claim-sets whose artifacts a reused filename destroyed.
# Per-shape filenames this time, and every process asserts which bench ran first.
cd /home/mikolaj/r/orthotope/micro-regime3
B=./run15-lookrts; P=cnn-slice-c32   # roster position 4, so it precedes 7..24
echo "=== victim set: does the tax fall on every shape's list? -A32m ==="
for W in conv1d-24 gather48-src-50 stretch-inner256 stretch-bigstride stretch-wide-2xM \
         stretch-tab7MB stretch-tall-Mx2 vgg-14-c512-k3 stretch-primes stretch-square-1341; do
  $B -m glob "$W/list" --json /tmp/rv-$W-alone.json +RTS -A32m > /tmp/rv-$W-alone.log 2>&1
  $B -m glob "$P/list" "$W/list" --json /tmp/rv-$W-after.json +RTS -A32m > /tmp/rv-$W-after.log 2>&1
  a=$(awk "/^benchmarking $W\/list\$/{f=1} f&&/^time /{print \$2 \$3; exit}" /tmp/rv-$W-alone.log)
  b=$(awk "/^benchmarking $W\/list\$/{f=1} f&&/^time /{print \$2 \$3; exit}" /tmp/rv-$W-after.log)
  first=$(awk '/^benchmarking /{print $2; exit}' /tmp/rv-$W-after.log | cut -d/ -f1)
  ok=$([ "$first" = "$P" ] && echo ok || echo "INVALID(ran $first first)")
  printf '  %-24s alone=%-10s after=%-10s %s\n' "$W" "$a" "$b" "$ok"
done
echo
echo "=== arm specificity: which arms of one shape does the tax touch? ==="
for arm in list bq-expand mut-odo-vecdims bq-scan-rem-gm-mulback offtab build; do
  $B -m glob "vgg-14-c512-k3/$arm" --json /tmp/ra-$arm-alone.json +RTS -A32m > /tmp/ra-$arm-alone.log 2>&1
  $B -m glob "$P/list" "vgg-14-c512-k3/$arm" --json /tmp/ra-$arm-after.json +RTS -A32m > /tmp/ra-$arm-after.log 2>&1
  a=$(awk "/^benchmarking vgg-14-c512-k3\/$arm\$/{f=1} f&&/^time /{print \$2 \$3; exit}" /tmp/ra-$arm-alone.log)
  b=$(awk "/^benchmarking vgg-14-c512-k3\/$arm\$/{f=1} f&&/^time /{print \$2 \$3; exit}" /tmp/ra-$arm-after.log)
  first=$(awk '/^benchmarking /{print $2; exit}' /tmp/ra-$arm-after.log | cut -d/ -f1)
  ok=$([ "$first" = "$P" ] && echo ok || echo "INVALID(ran $first first)")
  printf '  %-24s alone=%-10s after=%-10s %s\n' "$arm" "$a" "$b" "$ok"
done
echo DONE-REDO
