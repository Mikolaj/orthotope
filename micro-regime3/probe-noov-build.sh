#!/bin/bash
# Task 6's pair: the same recipe with the shim's containment test off and
# on. OFF must reproduce the current build byte for byte -- that is what
# says the switch is a switch and not a basis change taken by accident.
set -eu
cd "$(dirname "$0")"
for t in off on; do
  [ -e "probe-noov-$t-g912" ] && { echo "probe-noov-$t-g912 exists"; exit 1; }
done
for t in off on; do
  [ "$t" = on ] && export LOOP_NOOVERLAP=1 || unset LOOP_NOOVERLAP
  LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 \
  cabal build micro --builddir=db-no \
    --ghc-options="-fspec-constr -fobject-determinism" \
    --ghc-options="-pgma $PWD/align-as.py -fforce-recomp"
  cp "$(cabal list-bin micro --builddir=db-no)" "probe-noov-$t-g912"
  rm -rf db-no
  echo "built probe-noov-$t-g912"
done
echo "NOOVERLAP PAIR BUILT"
