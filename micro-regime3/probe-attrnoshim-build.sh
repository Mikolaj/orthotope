#!/bin/bash
# The -g3 twin of the NO-SHIM build, for attributing what is left of the
# short-run residue once the shim's padding is out of it. Same caveat as
# probe-attr-build.sh: a -g3 build is a twin to read, never one to time.
set -eu
cd "$(dirname "$0")"
[ -e probe-attrnoshim-g912 ] && { echo "probe-attrnoshim-g912 exists already"; exit 1; }
cabal build micro --builddir=db-attrns \
  --ghc-options="-fspec-constr -fobject-determinism -g3 -fforce-recomp"
cp "$(cabal list-bin micro --builddir=db-attrns)" probe-attrnoshim-g912
rm -rf db-attrns
echo "ATTR NOSHIM TWIN BUILT"
