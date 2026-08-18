#!/bin/bash
# 2026-08-18, staged: the convVjpBench -A matrix (near-real-life CNN
# gradient, improved orthotope linked, probe groups cnn-48x48 and
# cnn-24x24-c16h64 from the uncommitted bench edit). Fixed-n two-point
# differencing per cell (the Stage A instrument): victim rate =
# (wall(2n) - wall(n)) / n, artifact-build startup subtracted by the
# differencing. Arms: baked (-A1G -I0), -A64m, -A32m, -A4m -AL64m.
# Interleaved by cycles; one artifact file per cell, no reuse.
# RUNS ONLY ON A DECLARED-QUIET MACHINE.
set -u
B=/home/mikolaj/r/horde-ad/dist-newstyle/build/x86_64-linux/ghc-9.14.1/horde-ad-0.4.0.0/b/convVjpBench/build/convVjpBench/convVjpBench
D=/home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation/goal3
cd /home/mikolaj/r/horde-ad
exec > $D/probe66-conv-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"

cell() { # bench tagbench n1 armtag rtsflags...
  local BE=$1 TB=$2 N1=$3 TA=$4; shift 4
  local n
  for n in $N1 $((2*N1)); do
    /usr/bin/time -f %e -o $D/p66-$TB-$TA-n$n.time \
      $B -m glob "$BE" -n $n +RTS "$@" > $D/p66-$TB-$TA-n$n.log 2>&1
    echo "$TB $TA n=$n wall=$(cat $D/p66-$TB-$TA-n$n.time)"
  done
}
for r in 1 2; do
  for A in "baked:" "a64m:-A64m" "a32m:-A32m" "al:-A4m -AL64m"; do
    TA="${A%%:*}-r$r"; F="${A#*:}"
    # shellcheck disable=SC2086
    cell 'cnn-24x24/S-exec' cnn24 20 "$TA" $F
    # shellcheck disable=SC2086
    cell 'cnn-48x48/S-exec' cnn48 8 "$TA" $F
    # shellcheck disable=SC2086
    cell 'cnn-24x24-c16h64/S-exec' cnnbig 10 "$TA" $F
  done
done

echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-PROBE66-CONV
