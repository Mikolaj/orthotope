#!/bin/bash
# 2026-08-18: the gradbench matrix COMPLETION -- the five evals the
# validation crash truncated (item 43's correction), rerun with
# tools/manual built so their eval-side validation passes and the full
# default workload sets run. Same arms, cycles and instrument as
# probe66-gb.sh; v2 filenames, no reuse. gmm/lstm/hello/particle/saddle
# are NOT rerun -- their item 43 cells are complete.
set -u
cd /home/mikolaj/r/gradbench
G=./target/release-with-debug/gradbench
T=tools/horde-ad/dist-newstyle/build/x86_64-linux/ghc-9.12.4/gradbench-0.1.0.0/x/gradbench/build/gradbench/gradbench
D=/home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation/goal3
exec > $D/probe66-gb2-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"

for r in 1 2; do
  for A in "baked:" "a64m:+RTS -A64m -RTS" "a32m:+RTS -A32m -RTS" "al:+RTS -A4m -AL64m -RTS"; do
    TA="${A%%:*}"; F="${A#*:}"
    for E in det kmeans llsq lse ode; do
      /usr/bin/time -f "%e s, %M KB peak" -o $D/p66gb2-$E-$TA-r$r.time \
        timeout 1800 $G run \
          --eval "uv run python/gradbench/gradbench/evals/$E/run.py --min-seconds 5" \
          --tool "$T $F" -o $D/p66gb2-$E-$TA-r$r.jsonl \
          > $D/p66gb2-$E-$TA-r$r.log 2>&1
      echo "done $E $TA r$r exit=$? $(cat $D/p66gb2-$E-$TA-r$r.time)"
    done
  done
done

echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-PROBE66-GB2
