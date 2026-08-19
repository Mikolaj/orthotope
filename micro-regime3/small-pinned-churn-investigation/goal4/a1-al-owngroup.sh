#!/bin/bash
# padding-plan.txt A1: the -AL x own-group interaction (flagged untested
# in speculative-todos' cross-matrix). ReproSmall poisonbig (3600 B
# own-group, work item 27601's class), then the victim, under -A4m plain
# and -A4m -AL64m, alone legs beside them; mem-in-use is printed by the
# program. Does raising -AL let the 27601-class accumulation form at a
# small area?
# Registered lean, judged not remembered (plan A1): bounded by the 64 MB
# allowance, mild. Decision-adjacent: gates advertising "-A4m -AL64m".
# Binary: goal4/ReproSmall -- ReproSmall.hs with the k:/iters: arguments
# added 2026-08-18, defaults reproducing every recorded cell; its alone
# legs here are this binary's own baselines.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation
R=goal4/ReproSmall
exec > goal4/a1-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
md5sum $R
run() { local name=$1; shift
  echo "== $name: $*"
  $R "$@" -RTS > goal4/a1-$name.log 2>&1
  cat goal4/a1-$name.log
}
run alone-4m            +RTS -A4m -I0 -T
run alone-4m-al64m      +RTS -A4m -AL64m -I0 -T
run poisonbig-4m        poisonbig +RTS -A4m -I0 -T
run poisonbig-4m-al64m  poisonbig +RTS -A4m -AL64m -I0 -T
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-A1
