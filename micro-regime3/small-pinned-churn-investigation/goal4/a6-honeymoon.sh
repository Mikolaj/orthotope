#!/bin/bash
# padding-plan.txt A6, EXPLORATORY: the honeymoon micro-mechanism (item
# 25 -- early and late windows carry equal cache-misses and dTLB-misses
# per iteration while cycles/iter differ ~17%, so the fresh-heap
# advantage is in miss cost/overlap, not count). perf mem over early
# (-n 100) and long (-n 2000) windows of stretch-inner256/list at -A1G,
# run15 binary, load-latency profiles compared; plus a load/store split
# attempt via AMD ls_dispatch events, which may not exist on this
# machine (|| true, the failure is itself the record).
# No registered lean beyond item 25's: the difference should show in
# latency/overlap, not in counts. The -A15m/16m chunk-boundary probe
# stays dormant unless this revives it (plan A6).
set -u
cd /home/mikolaj/r/orthotope/micro-regime3
B=./run15-lookrts
D=small-pinned-churn-investigation/goal4
exec > $D/a6-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
md5sum $B
G='stretch-inner256/list'
for n in 100 2000; do
  perf mem record -o $D/a6-mem-n$n.data -- \
    $B -m glob "$G" -n $n +RTS -A1G > $D/a6-mem-n$n.log 2>&1 || true
  perf mem report --stdio -i $D/a6-mem-n$n.data \
    > $D/a6-mem-n$n-report.txt 2>&1 || true
  echo "== perf mem, n=$n: $(head -3 $D/a6-mem-n$n-report.txt | tail -1)"
done
for n in 100 2000; do
  perf stat -e ls_dispatch.ld_dispatch,ls_dispatch.store_dispatch \
    -o $D/a6-lsdispatch-n$n.txt -- \
    $B -m glob "$G" -n $n +RTS -A1G > /dev/null 2>&1 || true
  cat $D/a6-lsdispatch-n$n.txt 2>/dev/null || echo "ls_dispatch events unavailable"
done
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-A6
