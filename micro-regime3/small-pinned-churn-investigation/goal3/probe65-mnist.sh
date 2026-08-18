#!/bin/bash
# 2026-08-18, the second real-suite datum: sequentialMnistTest on the
# existing ghc-9.14.1 binary, FOUR arms interleaved in cycles (drift
# cancels within a cycle), two cycles:
#   bare          -- the baked -A1G -I0, the incumbent and control
#   -A64m         -- item 17's CAFlessTest winner
#   -A32m         -- the half-tax point and the saturated-mix optimum
#                    (item 34); the open 32-vs-64 question for real suites
#   -A4m -AL64m   -- the low-memory point (item 38: within ~1% of -A64m
#                    at 1.8x less peak RSS on CAFlessTest)
# Registered leans: -A64m beats bare on wall at far less RSS (item 17
# generalizes); 32m-vs-64m is genuinely open -- repetitive phases argue
# for span-matched smaller areas, clean phases for 64m; -A4m -AL64m lands
# within a couple percent of -A64m at the lowest RSS of the four.
# Adaptive cost control in place of the old 360 s gate: if the first run
# exceeds 720 s, only one cycle runs (4 runs, no reps).
# RUNS ONLY ON MIKOLAJ'S GO-AHEAD.
set -u
D=/home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation/goal3
S=/home/mikolaj/r/horde-ad/dist-newstyle/build/x86_64-linux/ghc-9.14.1/horde-ad-0.4.0.0/t/sequentialMnistTest/build/sequentialMnistTest/sequentialMnistTest
cd /home/mikolaj/r/horde-ad
exec > $D/probe65-mnist-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"

run() { # tag rtsflags...
  local T=$1; shift
  /usr/bin/time -v $S "$@" > $D/p65m-$T.log 2>&1
  local ok=$?
  local w=$(command grep -oP 'Elapsed \(wall clock\).*: \K.*' $D/p65m-$T.log)
  local rss=$(command grep -oP 'Maximum resident set size \(kbytes\): \K\d+' $D/p65m-$T.log)
  echo "done $T exit=$ok wall=$w rssMB=$((rss / 1024))"
}

run bare-r1
run a64m-r1 +RTS -A64m -RTS
run a32m-r1 +RTS -A32m -RTS
run al-r1 +RTS -A4m -AL64m -RTS

w=$(command grep -oP 'Elapsed \(wall clock\).*: \K.*' $D/p65m-bare-r1.log)
secs=$(python3 -c "p='$w'.split(':'); print(int(float(p[-1]) + 60*float(p[-2]) + (3600*float(p[-3]) if len(p)>2 else 0)))")
if [ "$secs" -le 720 ]; then
  run bare-r2
  run a64m-r2 +RTS -A64m -RTS
  run a32m-r2 +RTS -A32m -RTS
  run al-r2 +RTS -A4m -AL64m -RTS
else
  echo "ADAPT: bare run ${secs}s > 720s -- second cycle skipped"
fi

echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-PROBE65-MNIST
