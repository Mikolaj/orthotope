#!/bin/bash
# Stretch goal 6: the clean alone-leg companion for every list
# denominator -- the instrument item 52's decision table names as the
# one that reaches the published absolutes. run15-lookrts (the
# published basis), default area, one bench per process, criterion
# default budget; the three Provenance anchors get a second rep, the
# rest single runs read against the known multi-process draw band
# (~2%, item 30d). Deliverable: the clean-alone column the README
# position-term entry's next rewrite can cite in place of the "~9%
# above what the shape does alone" estimate.
# No lean to register beyond the record's: in-roster list absolutes sit
# above these by the interleaved-route context, ~+5% scale at the
# default area (items 21/40b/51).
set -u
cd /home/mikolaj/r/orthotope/micro-regime3
B=./run15-lookrts
D=small-pinned-churn-investigation/goal4
exec > $D/a9-alonelegs-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
md5sum $B
SHAPES=$($B --list 2>/dev/null | cut -d/ -f1 | awk '!seen[$0]++')
for S in $SHAPES; do
  $B -m glob "$S/list" --json $D/a9-al-$S-r1.json > $D/a9-al-$S-r1.log 2>&1
  awk -v s="$S:" '/^time /{print s, $2, $3; exit}' $D/a9-al-$S-r1.log
done
for S in cnn-slice-c32 cifar-L2-16-c64-k3 stretch-wide-2xM; do
  $B -m glob "$S/list" --json $D/a9-al-$S-r2.json > $D/a9-al-$S-r2.log 2>&1
  awk -v s="$S-r2:" '/^time /{print s, $2, $3; exit}' $D/a9-al-$S-r2.log
done
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-A9-ALONELEGS
