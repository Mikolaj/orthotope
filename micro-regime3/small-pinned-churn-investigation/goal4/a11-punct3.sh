#!/bin/bash
# The punctuation term's last cheap discriminators (items 62/66):
# (1) +RTS -s pair at -A32m, alone vs read control: does the probed run
#     COPY more during GC? Registered lean: identical collections and
#     copied bytes (the probe allocates nothing and the live set is
#     unchanged), leaving the excess instructions unattributed by -s; a
#     copied-bytes rise instead moves the account to promotion/copying
#     and is a real lead.
# (2) cadence shape: k:3000 beside item 66's k:100 (+3.8%) and k:1000
#     (+14.9%). Registered lean: saturating -- k:3000 near k:1000's
#     level; ~+45% instead reads the term as linear per-call cost.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation
R=goal4/ReproSmall
exec > goal4/a11-punct3-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
md5sum $R
for m in "" internoallocr; do
  tag=${m:-alone}
  $R $m victim +RTS -A32m -I0 -T -s -RTS > goal4/a11-p3-s-$tag.log 2>&1
  echo "== $tag: $(grep victim: goal4/a11-p3-s-$tag.log)"
  grep -E 'bytes copied|collections|bytes allocated in the heap' goal4/a11-p3-s-$tag.log
done
$R internoallocr k:3000 victim +RTS -A32m -I0 -T -RTS > goal4/a11-p3-k3000.log 2>&1
echo "== readctl-k3000-32m: $(grep victim: goal4/a11-p3-k3000.log)"
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-A11-PUNCT3
