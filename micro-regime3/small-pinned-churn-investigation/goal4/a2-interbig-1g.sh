#!/bin/bash
# padding-plan.txt A2: the 1G interleaved class residue (item 44 OPEN:
# interunboxed poisons at 1G, interbig does not). Dose-sweep interbig at
# -A1G (k:100, and the 3000-iteration horizon at the default k:1000) and
# a perf pair interunboxed-vs-interbig at -A1G (LLC and dTLB). Feeds the
# GHC follow-up comment's caveat.
# Registered leans, judged not remembered (from item 44's OPEN and item
# 39's signature): (1) interbig stays near-clean at 1G at k:100 and over
# the long horizon -- the residue split is class-real, not a dose or
# horizon artifact; interbig climbing toward interunboxed at k:100 or
# late in the horizon would instead re-read it as rate-dependent.
# (2) perf: interunboxed's added cost over interbig is LLC misses at
# ~flat victim instructions and ~flat dTLB, item 39's channel.
# Binary: goal4/ReproSmall (the k:/iters: build); alone legs are A1's --
# run a1-al-owngroup.sh first or take the two -A1G alone cells here.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation
R=goal4/ReproSmall
exec > goal4/a2-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
md5sum $R
run() { local name=$1; shift
  echo "== $name: $*"
  $R "$@" -RTS > goal4/a2-$name.log 2>&1
  cat goal4/a2-$name.log
}
run alone-1g-r1        +RTS -A1G -I0 -T
run alone-1g-r2        +RTS -A1G -I0 -T
run interbig-k100-1g   interbig k:100 +RTS -A1G -I0 -T
run interbig-horizon-1g interbig iters:3000 +RTS -A1G -I0 -T
echo "== perf pair, default k:1000, -A1G"
perf stat -e instructions,cycles,cache-misses,dTLB-load-misses \
  -o goal4/a2-perf-interunboxed.txt \
  $R interunboxed +RTS -A1G -I0 -T -RTS > goal4/a2-interunboxed-1g.log 2>&1
cat goal4/a2-interunboxed-1g.log
perf stat -e instructions,cycles,cache-misses,dTLB-load-misses \
  -o goal4/a2-perf-interbig.txt \
  $R interbig +RTS -A1G -I0 -T -RTS > goal4/a2-interbig-k1000-1g.log 2>&1
cat goal4/a2-interbig-k1000-1g.log
cat goal4/a2-perf-interunboxed.txt goal4/a2-perf-interbig.txt
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-A2
