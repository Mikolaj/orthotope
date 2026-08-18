#!/bin/bash
# 2026-08-18, staged: the gradbench -A matrix -- ten evals, one tool
# binary (improved orthotope linked), arms as run-time +RTS overrides:
# baked (-A2G -I0 -M14G), -A64m, -A32m, -A4m -AL64m. Two interleaved
# cycles; per-cell unique filenames. gmm and lstm take --no-validation
# (their validation wants the unbuilt C++ manual tools); the short others
# take --min-seconds 5 so tool startup does not dominate their reading.
# The tool-reported per-evaluate timings in the jsonl logs are the
# instrument; the /usr/bin/time wall is the coarse cross-check.
# RUNS ONLY ON A DECLARED-QUIET MACHINE.
set -u
cd /home/mikolaj/r/gradbench
G=./target/release-with-debug/gradbench
T=tools/horde-ad/dist-newstyle/build/x86_64-linux/ghc-9.12.4/gradbench-0.1.0.0/x/gradbench/build/gradbench/gradbench
D=/home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation/goal3
exec > $D/probe66-gb-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"

evalflags() {
  case $1 in
    gmm|lstm) echo "--no-validation" ;;
    hello) echo "" ;;
    *) echo "--min-seconds 5" ;;
  esac
}
for r in 1 2; do
  for A in "baked:" "a64m:+RTS -A64m -RTS" "a32m:+RTS -A32m -RTS" "al:+RTS -A4m -AL64m -RTS"; do
    TA="${A%%:*}"; F="${A#*:}"
    for E in det gmm hello kmeans llsq lse lstm ode particle saddle; do
      /usr/bin/time -f "%e s, %M KB peak" -o $D/p66gb-$E-$TA-r$r.time \
        $G run --eval "uv run python/gradbench/gradbench/evals/$E/run.py $(evalflags $E)" \
           --tool "$T $F" -o $D/p66gb-$E-$TA-r$r.jsonl \
           > $D/p66gb-$E-$TA-r$r.log 2>&1
      echo "done $E $TA r$r exit=$? $(cat $D/p66gb-$E-$TA-r$r.time)"
    done
  done
done

echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-PROBE66-GB
