#!/bin/bash
# Goal-2 Stage A addendum, 2026-08-18.
# (1) Criterion-alone legs at -A4m for the three Stage A victims: at 4 MB there
#     is no fresh-heap transient (findings2 item 11), so criterion-alone is
#     valid there and gives the -A4m tax same-instrument against the pois-*
#     cells, separating instrument offset from real tax.
# (2) The three-compiler completion for the issue draft: ReproSmall compiled
#     with ghcup 9.14.1 (full 5-mode matrix at 32m/1G) and GHC HEAD
#     (poisonmid/poisontiny only -- its other cells are in
#     repro-matrix-2026-08-18.txt already).
set -u
cd /home/mikolaj/r/orthotope/micro-regime3
B=./run15-lookrts
D=small-pinned-churn-investigation/goal2
exec > $D/stageA2-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"

for S in vgg-14-c512-k3 stretch-wide-2xM stretch-inner256; do
  $B -m glob "$S/list" --json $D/calone-$S-A4m.json +RTS -A4m > $D/calone-$S-A4m.log 2>&1
  echo "calone $S -A4m $(awk "/^benchmarking $S\/list\$/{f=1} f&&/^time /{print \$2, \$3; exit}" $D/calone-$S-A4m.log)"
done

cd small-pinned-churn-investigation
~/.ghcup/bin/ghc-9.14.1 -O1 -rtsopts -outputdir goal2/oy-9141 -o goal2/ReproSmall-9141 ReproSmall.hs > goal2/build-9141.log 2>&1 || { echo BUILD-9141-FAILED; }
~/r/horde-ad/ghc/_build/stage1/bin/ghc -O1 -rtsopts -outputdir goal2/oy-head -o goal2/ReproSmall-head ReproSmall.hs > goal2/build-head.log 2>&1 || { echo BUILD-HEAD-FAILED; }

for a in "-A32m" "-A1G"; do
  for mode in "" poison poisonmid poisontiny poisonbig; do
    echo "== repro-9141 [$a] mode='$mode'"
    ./goal2/ReproSmall-9141 $mode +RTS $a -I0 -T -RTS
  done
done > goal2/repro-matrix-9141.txt 2>&1

for a in "-A32m" "-A1G"; do
  for mode in poisonmid poisontiny; do
    echo "== repro-head-b [$a] mode='$mode'"
    ./goal2/ReproSmall-head $mode +RTS $a -I0 -T -RTS
  done
done > goal2/repro-matrix2-head.txt 2>&1

echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-STAGEA2
