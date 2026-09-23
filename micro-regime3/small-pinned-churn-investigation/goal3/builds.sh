#!/bin/bash
# 2026-08-18: the builds behind the two near-real-life -A probes,
# sequential so the machine is never doubly loaded.
# (1) horde-ad convVjpBench, optimized, ghc-9.14.1 (the tree the other
#     optimized binaries live in; links ../orthotope via the active
#     packages line), with the uncommitted probe edit in
#     bench/ConvVjpBench.hs (cnn-48x48 and cnn-24x24-c16h64 groups).
# (2) The gradbench horde-ad tool (Hackage horde-ad 0.3 + ox-arrays 0.2
#     over the LOCAL orthotope via the appended cabal.project.local
#     line), one-time, the heavy item.
set -u
exec > /home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation/goal3/builds-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"

cd /home/mikolaj/r/horde-ad
~/.ghcup/bin/cabal build convVjpBench --enable-optimization -w ~/.ghcup/bin/ghc-9.14.1
echo "convVjpBench build exit: $?"

cd /home/mikolaj/r/gradbench
~/.ghcup/bin/cabal build --project-dir tools/horde-ad gradbench
echo "gradbench tool build exit: $?"

echo "end: $(date)"
echo DONE-BUILDS
