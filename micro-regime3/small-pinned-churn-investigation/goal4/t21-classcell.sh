#!/bin/bash
# padding-plan.txt task 2.1: THE 32M MATCHED-DOSE CLASS CELL, the plan's
# 0.2 discriminator (findings2 item 13 ran this design at 1G only).
# Victim conv1d-24/list at -A32m, fixed-n two-point differencing on the
# run15 binary; poisons cnn-slice-c32/list (2304 B, sub-threshold) and
# cnn-L1-24x24-c1/list (41 KB, own-group) at -n 200k/400k each. Victim
# alone at both n's is added for the tax denominator -- conv1d-24 has no
# recorded -A32m alone plateau, so nothing is repeated.
# Registered lean, judged not remembered (plan 2.1): the class split
# holds at 32m as in ReproSmall (sub-threshold well above own-group),
# which is what gives padding its payoff; the opposite result re-scopes
# tasks 2.4-2.5's predictions downward and is itself a finding for the
# GHC follow-up comment.
# Read-out (item 13's recipe): victim-in-pair us/iter =
# ((pair(400k) - pair(200k)) - (poison-alone(400k) - poison-alone(200k)))
# / 200k; alone us/iter = (alone(400k) - alone(200k)) / 200k.
set -u
cd /home/mikolaj/r/orthotope/micro-regime3
B=./run15-lookrts
D=small-pinned-churn-investigation/goal4
exec > $D/t21-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
md5sum $B

run() {
  local name=$1 n=$2; shift 2
  /usr/bin/time -f %e -o $D/t21-$name.time \
    $B -m glob "$@" -n "$n" +RTS -A32m > $D/t21-$name.log 2>&1
  local first
  first=$(awk '/^benchmarking /{print $2; exit}' $D/t21-$name.log)
  echo "$name: wall $(cat $D/t21-$name.time) s, first=$first, benches=$(grep -c '^benchmarking ' $D/t21-$name.log)"
}

run alone-conv1d-200k 200000 'conv1d-24/list'
run alone-conv1d-400k 400000 'conv1d-24/list'
run alone-slice-200k  200000 'cnn-slice-c32/list'
run alone-slice-400k  400000 'cnn-slice-c32/list'
run alone-cnnL1-200k  200000 'cnn-L1-24x24-c1/list'
run alone-cnnL1-400k  400000 'cnn-L1-24x24-c1/list'
run pair-slice-200k   200000 'cnn-slice-c32/list' 'conv1d-24/list'
run pair-slice-400k   400000 'cnn-slice-c32/list' 'conv1d-24/list'
run pair-cnnL1-200k   200000 'cnn-L1-24x24-c1/list' 'conv1d-24/list'
run pair-cnnL1-400k   400000 'cnn-L1-24x24-c1/list' 'conv1d-24/list'

python3 - "$D" <<'EOF'
import sys
d = sys.argv[1]
w = lambda n: float(open(f"{d}/t21-{n}.time").read())
alone = (w("alone-conv1d-400k") - w("alone-conv1d-200k")) / 200e3 * 1e6
print(f"victim alone: {alone:.2f} us/iter")
for p, nm in [("slice", "cnn-slice-c32 (sub-threshold)"),
              ("cnnL1", "cnn-L1-24x24-c1 (own-group)")]:
    v = ((w(f"pair-{p}-400k") - w(f"pair-{p}-200k"))
         - (w(f"alone-{p}-400k") - w(f"alone-{p}-200k"))) / 200e3 * 1e6
    print(f"after {nm}: {v:.2f} us/iter  ({(v/alone-1)*100:+.1f}%)")
EOF
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-T21
