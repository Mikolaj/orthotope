#!/bin/bash
# The control for item 4's answer: the g912 recipe WITHOUT the assembler
# shim, so the alignment padding is GHC's own and not align-as.py's. If
# the residue on a long-run view is the shim's padding, it moves here;
# if it is code, it does not.
set -eu
cd "$(dirname "$0")"
[ -e probe-noshim-g912 ] && { echo "probe-noshim-g912 exists already"; exit 1; }
cabal build micro --builddir=db-noshim \
  --ghc-options="-fspec-constr -fobject-determinism -fforce-recomp"
cp "$(cabal list-bin micro --builddir=db-noshim)" probe-noshim-g912
rm -rf db-noshim
echo "NOSHIM BUILT"
