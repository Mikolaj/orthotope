#!/bin/bash
# padding-plan.txt task 2.4(a): the corrected poison scan rerun on the
# PADDED binary -- ../poison-scan.sh verbatim but for the binary, the
# artifact paths (goal4/, no /tmp reuse, no filename shared with the
# run15 scan whose cells live in ../../scan-a32m/) and the md5 echo.
# Victim stretch-inner256/list at roster position 24; every pair process
# asserts the order it got.
# Registered lean, judged not remembered (plan 2.4a): the cnn-slice-c32
# and cnn-L1-6x6-c1 rows collapse from +12.2/+9.6% toward the own-group
# level task 2.1 measures for their counts; the own-group rows stay on
# item 1's curve, which padding cannot touch.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3
B=./newform-padded; V=stretch-inner256; A=${1:-32m}
D=small-pinned-churn-investigation/goal4
exec > $D/t24-scan-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
md5sum $B
[ -f $D/t24-shapes.txt ] ||
  $B --list 2>/dev/null | cut -d/ -f1 | awk '!seen[$0]++' > $D/t24-shapes.txt
echo "victim=$V (roster position 24), -A$A"
$B -m glob "$V/list" --json $D/t24-p2p-alone.json +RTS -A$A > $D/t24-p2p-alone.log 2>&1
base=$(awk "/^benchmarking $V\/list\$/{f=1} f&&/^time /{print \$2; exit}" $D/t24-p2p-alone.log)
bu=$(awk "/^benchmarking $V\/list\$/{f=1} f&&/^time /{print \$3; exit}" $D/t24-p2p-alone.log)
echo "alone baseline: $base $bu   (benchmarking=$(grep -c '^benchmarking ' $D/t24-p2p-alone.log))"
echo
printf '%-24s %10s %10s %s\n' candidate victim delta order
for C in $(cat $D/t24-shapes.txt); do
  [ "$C" = "$V" ] && continue
  o=$D/t24-p2p-$C
  $B -m glob "$C/list" "$V/list" --json $o.json +RTS -A$A > $o.log 2>&1
  first=$(awk '/^benchmarking /{print $2; exit}' $o.log | cut -d/ -f1)
  t=$(awk "/^benchmarking $V\/list\$/{f=1} f&&/^time /{print \$2; exit}" $o.log)
  u=$(awk "/^benchmarking $V\/list\$/{f=1} f&&/^time /{print \$3; exit}" $o.log)
  nb=$(grep -c '^benchmarking ' $o.log)
  if [ "$first" != "$C" ]; then ord="INVALID(ran $first first)"; else ord=ok; fi
  [ "$u" = "$bu" ] || ord="$ord UNITS($u vs $bu)"
  d=$(python3 -c "print('%+.1f%%' % ((float('$t')/float('$base')-1)*100))" 2>/dev/null || echo '?')
  printf '%-24s %10s %10s %s nb=%s\n' "$C" "$t" "$d" "$ord" "$nb"
done
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-T24-SCAN
