#!/bin/bash
# The spill-free binary the run-length condition's second half wants
# (README.md#the-mutable-ceiling-taken, the sixth reading): the g912
# recipe with -fllvm in place of the assembler shim, which is the native
# backend's instrument and has no business in an LLVM build, plus the
# 64-byte loop heads README's LLVM paragraph names. -fforce-recomp and a
# fresh builddir because cabal answers "Up to date" for a -pgma or an
# environment change.
#
# It is a codegen instrument and not a regime: -fllvm is one this README
# will not publish from, and `sum-only` runs larger than the bench under
# it, so anything read off it is read with `--corr=insitu` and is
# comparable to no figure in README. What it is for is one arm-against-arm
# ordering inside one process, `-u2` against `-down` over the runs class,
# where both loops are spill-free and the NCG's placement term is gone.
#
# Wants no quiet machine. `check` is owed on the binary before a figure is
# read off it, which probe-nospill-check.log records.
set -eu
cd "$(dirname "$0")"
[ -e probe-nospill-g912 ] && { echo "probe-nospill-g912 exists already"; exit 1; }
cabal build micro --builddir=db-nospill \
  --ghc-options="-fspec-constr -fobject-determinism" \
  --ghc-options="-fllvm -optlc-align-loops=64 -fforce-recomp"
cp "$(cabal list-bin micro --builddir=db-nospill)" probe-nospill-g912
rm -rf db-nospill
echo "NOSPILL BUILT"
