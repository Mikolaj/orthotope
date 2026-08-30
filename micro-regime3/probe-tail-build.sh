#!/bin/bash
# A no-shim build of whatever Main.hs currently says, for pricing a change
# to fillStage2 in instructions: no shim means no padding in the counts, so
# what moves is code. Paired with probe-noshim-g912, which is the same
# recipe over the source before the change.
set -eu
cd "$(dirname "$0")"
[ -e probe-tail-g912 ] && { echo "probe-tail-g912 exists already"; exit 1; }
cabal build micro --builddir=db-tail \
  --ghc-options="-fspec-constr -fobject-determinism -fforce-recomp"
cp "$(cabal list-bin micro --builddir=db-tail)" probe-tail-g912
rm -rf db-tail
echo "TAIL BUILT"
