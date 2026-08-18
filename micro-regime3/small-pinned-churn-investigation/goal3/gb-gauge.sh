#!/bin/bash
# 2026-08-18: gradbench duration gauge -- one pass over the tool's ten
# evals at the BAKED RTS options (-A2G -I0 -M14G), /usr/bin/time each,
# to size the 4-arm matrix; --no-validation because validating needs
# the unbuilt C++ manual tools, which killed the first gauge early. A duration map, not A/B data (machine state
# unasserted); the matrix runs later on a declared-quiet machine.
set -u
cd /home/mikolaj/r/gradbench
G=./target/release-with-debug/gradbench
T=tools/horde-ad/dist-newstyle/build/x86_64-linux/ghc-9.12.4/gradbench-0.1.0.0/x/gradbench/build/gradbench/gradbench
D=/home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation/goal3
exec > $D/gb-gauge-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"

for E in det gmm hello kmeans llsq lse lstm ode particle saddle; do
  /usr/bin/time -f "%e s, %M KB peak" -o $D/gb-gauge-$E.time \
    $G run --eval "uv run python/gradbench/gradbench/evals/$E/run.py --no-validation" \
       --tool "$T" -o $D/gb-gauge-$E.jsonl > $D/gb-gauge-$E.log 2>&1
  echo "done $E exit=$? $(cat $D/gb-gauge-$E.time)"
done

echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-GB-GAUGE
