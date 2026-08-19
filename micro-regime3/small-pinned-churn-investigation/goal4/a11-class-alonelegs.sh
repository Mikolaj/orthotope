#!/bin/bash
# Item 64's instrument completed for the stride-class populations: the
# clean alone-leg for every class view's list denominator, run15-lookrts
# classes mode, default area, one bench per process -- the class tables
# are published tables with the same in-roster deflation question as
# the main set's.
# No lean beyond the record's: in-roster class absolutes sit above
# these by the interleaved-route context at the default area (~+5%
# scale, items 21/40b/51); single runs, the ~2% multi-process draw band
# (item 30d) is the error bar.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3
B=./run15-lookrts
D=small-pinned-churn-investigation/goal4
exec > $D/a11-classlegs-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
md5sum $B
CLASSES=$($B classes --list 2>/dev/null | cut -d/ -f1 | awk '!seen[$0]++')
n=0
for S in $CLASSES; do
  $B classes -m glob "$S/list" --json $D/a11-cl-$S.json > $D/a11-cl-$S.log 2>&1
  awk -v s="$S:" '/^time /{print s, $2, $3; exit}' $D/a11-cl-$S.log
  n=$((n+1))
done
echo "views measured: $n"
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-A11-CLASSLEGS
