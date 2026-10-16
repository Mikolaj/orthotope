#!/bin/bash
# Stretch goal 2: the comment reproducer's matrix on 9.14.1 and HEAD, so
# the comment can make the issue's all-three-compilers claim. Builds
# goal4/ReproV2-9141 and goal4/ReproV2-head from the same source the
# comment embeds, then the key modes at both areas (single runs; the
# 9.12.4 matrix carries the reps and this is a cross-compiler
# confirmation, item 44's spot-cell pattern).
# Registered leans, judged not remembered: both compilers reproduce the
# 9.12.4 split within run-to-run spread -- small sprays poison at both
# areas, own-group and the controls stay at the punctuation term (item
# 44's 9.14.1 spot cells and item 16's HEAD column are the precedent).
set -u
cd /home/mikolaj/r/orthotope/micro-regime3/small-pinned-churn-investigation \
  || exit 2
exec > goal4/a9-compilers-driver.log 2>&1
echo "start: $(date), loadavg: $(cat /proc/loadavg)"
# A FAILED BUILD STOPS THE SCRIPT, the previous binaries removed first:
# one that failed left the last run's ReproV2-* to be run and read as
# this build's (2026-10-16, by review).
rm -f goal4/ReproV2-9141 goal4/ReproV2-head
ghc-9.14.1 -O1 -rtsopts -outputdir goal4/rv2-objs-9141 \
  -o goal4/ReproV2-9141 goal4/ReproV2.hs \
  || { echo "COMPILE FAILED, 9.14.1"; exit 1; }
/home/mikolaj/r/horde-ad/ghc/_build/stage1/bin/ghc -O1 -rtsopts \
  -outputdir goal4/rv2-objs-head -o goal4/ReproV2-head goal4/ReproV2.hs \
  || { echo "COMPILE FAILED, HEAD"; exit 1; }
md5sum goal4/ReproV2.hs goal4/ReproV2-9141 goal4/ReproV2-head
ghc-9.14.1 --version
/home/mikolaj/r/horde-ad/ghc/_build/stage1/bin/ghc --version
for cc in 9141 head; do
  R=goal4/ReproV2-$cc
  for area in 32m 1G; do
    for m in "" inter interbig interunboxed interunboxedbig internoalloc internoallocr; do
      tag=${m:-alone}
      $R $m victim +RTS -A$area -I0 -T -RTS > goal4/a9-$cc-$tag-$area.log 2>&1
      echo "== $cc $tag $area: $(grep victim: goal4/a9-$cc-$tag-$area.log)"
    done
  done
done
echo "end: $(date), loadavg: $(cat /proc/loadavg)"
echo DONE-A9-COMPILERS
