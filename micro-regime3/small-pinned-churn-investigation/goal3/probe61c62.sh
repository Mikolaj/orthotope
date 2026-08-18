#!/bin/bash
# 2026-08-18, the closing control of probe 6.1 plus probe 6.2, sequenced.
# (1) rep1:0 = pure vgg-14-c512-k3/list through the driver, no sprayer:
#     if it reads ~16.8 (the fixed-n alone plateau) the driver instrument
#     is clean and the interleaved calls are the disturbance; if ~24 (the
#     p61c level) the driver loop itself degrades the victim and every
#     driver-based per-call reading needs that offset read against it.
# (2) Probe 6.2 (plan section 6.2): CAFlessTest, the same ghc-9.14.1
#     optimized binary item 17 used, interleaved A/B/A/B under
#     /usr/bin/time -v: A = +RTS -A64m (item 17's winner), B = +RTS -A4m
#     -AL64m (item 32's discovery). Wall, user, sys, peak RSS per run.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation
M=dist-newstyle/build/x86_64-linux/ghc-9.12.4/mixedload-0.1/x/MixedLoad/build/MixedLoad/MixedLoad
D=goal3
exec > $D/probe61c62-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"

$M 1 1000 base rep1:0 +RTS -A64m -RTS > $D/p61c-novictim-ctrl-64m.log 2>&1
echo "done rep1:0 control"

C=/home/mikolaj/r/horde-ad/dist-newstyle/build/x86_64-linux/ghc-9.14.1/horde-ad-0.4.0.0/t/CAFlessTest/build/CAFlessTest/CAFlessTest
cd /home/mikolaj/r/horde-ad
for r in 1 2; do
  /usr/bin/time -v $C +RTS -A64m -RTS \
    > /home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation/$D/p62-a64m-r$r.log 2>&1
  echo "done p62 A(-A64m) r$r exit=$?"
  /usr/bin/time -v $C +RTS -A4m -AL64m -RTS \
    > /home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation/$D/p62-al-r$r.log 2>&1
  echo "done p62 B(-A4m -AL64m) r$r exit=$?"
done

echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-PROBE61C62
